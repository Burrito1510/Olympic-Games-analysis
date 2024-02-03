import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


def medaltally(df):
    medalxtally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medalxtally=medalxtally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    # medalxtally.index = range(1,len(medalxtally)+1)
    medalxtally['Total']=medalxtally['Gold']+medalxtally['Silver']+medalxtally['Bronze']
    return medalxtally

def countryyearlist(df):
    Years=df['Year'].unique().tolist()
    Years.sort()
    Years.insert(0,'Overall')
    country=df['region'].unique().tolist()
    country= np.unique(df['region'].dropna().values).tolist()
    country.sort()
    return Years, country


def fetchmedaltally(df,year,country):
    medaldf=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='Overall' and country=='Overall':
        tempdf=medaldf
    if year=='Overall' and country!='Overall':
        flag=1
        tempdf=medaldf[medaldf['region']==country]
    if year!='Overall' and country=='Overall':
        tempdf=medaldf[medaldf['Year']==int(year)]
    if year!='Overall' and country!='Overall':
        tempdf=medaldf[(medaldf['Year']==int(year)) & (medaldf['region']==country)]

    if(flag==1):
        x=medalxtally=tempdf.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=medalxtally=tempdf.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']=x['Gold']+x['Silver']+x['Bronze']    
    return(x)

def chalhinairaha(df):
    nationsovertime= df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')    
    nationsovertime.rename(columns={'Year':'Edition','count':'Number of Countries'},inplace=True)
    return nationsovertime

def one(df):
    xyz= df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')    
    xyz.rename(columns={'Year':'Edition','count':'Number of Sports'},inplace=True)
    return xyz

def isname(df):
    athlete= df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_values('Year')    
    athlete.rename(columns={'Year':'Edition','count':'Total Athlete'},inplace=True)
    return athlete

def mostsuc(df,Sport):
    tempdf=df.dropna(subset=['Medal'])
    if Sport != 'Overall':
        tempdf=tempdf[tempdf['Sport']==Sport]
    tempdf=tempdf['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left').drop_duplicates(['Name'])
    tempdf=tempdf[['Name','count','region','Sport']]
    tempdf.rename(columns={'count':'Total Medals'},inplace=True)
    return tempdf

def yearwisemedal(df,country):
    tempdf= df.dropna(subset=['Medal'])
    tempdf.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    newdf=tempdf[tempdf['region']==country]
    finaldf=newdf.groupby('Year').count()['Medal'].reset_index()
    return finaldf

def countryheatmap(df,country):
    tempdf= df.dropna(subset=['Medal'])
    tempdf.drop_duplicates(['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    newdf=tempdf[tempdf['region']==country]
    pt= newdf.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def mostsuccountry(df,country):
    tempdf=df.dropna(subset=['Medal'])
    tempdf=tempdf[tempdf['region']==country]
    tempdf=tempdf['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left').drop_duplicates(['Name'])
    tempdf=tempdf[['Name','count','region','Sport']]
    tempdf.rename(columns={'count':'Total Medals'},inplace=True)
    return tempdf

def wvh(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def mvw(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final