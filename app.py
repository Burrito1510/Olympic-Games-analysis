import numpy as np
import pandas as pd
import streamlit as st
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

path = '/Users/sanskritipathak/Desktop/Python/athlete_events.csv'
region= '/Users/sanskritipathak/Desktop/Python/noc_regions.csv'
df= pd.read_csv(path)
rdf=pd.read_csv(region)
df=preprocessor.preprocess(df,rdf)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://animationvisarts.com/wp-content/uploads/2016/11/Olympics-Logo.jpg")

usermenu=st.sidebar.radio(
    'What would you like to know?',
    ('Medal Tally','Overall Analysis','Country-wise analysis','Athlete-wise Analysis')
)
if usermenu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country= helper.countryyearlist(df)
    selectedyear= st.sidebar.selectbox("Select Year", years)
    selectedcon= st.sidebar.selectbox("Select Country", country)
    if selectedyear == 'Overall' and selectedcon == 'Overall':
        st.title("Overall Tally")
    if selectedyear != 'Overall' and selectedcon == 'Overall':
        st.title("Medal Tally in " + str(selectedyear) + " Olympics")
    if selectedyear == 'Overall' and selectedcon != 'Overall':
        st.title(selectedcon + "'s overall performance")
    if selectedyear != 'Overall' and selectedcon != 'Overall':
        st.title(selectedcon + "'s performance in " + str(selectedyear) + " Olympics")
    medalxtally= helper.fetchmedaltally(df,selectedyear,selectedcon)
    st.table(medalxtally)

if usermenu=='Overall Analysis':
    editions=df['Year'].unique().shape[0] -1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.chalhinairaha(df)
    fig = px.line(nations_over_time, x="Edition", y="Number of Countries")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)
    totalsports=helper.one(df)
    fig = px.line(totalsports, x="Edition", y="Number of Sports")
    st.title("Total sports per edition over the years")
    st.plotly_chart(fig)
    athlete=helper.isname(df)
    fig = px.line(athlete, x="Edition", y="Total Athlete")
    st.title("Total Athlete per edition over the years")
    st.plotly_chart(fig)
    st.title("Number of Events over time (Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x= df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True,cmap='Blues')
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.mostsuc(df,selected_sport)
    st.table(x)


if usermenu== 'Country-wise analysis':
    st.sidebar.title("Country-wise analysis")
    counlist=df['region'].dropna().unique().tolist()
    counlist.sort()
    country=st.sidebar.selectbox('Select a country',counlist)
    st.title(country+"'s Medal Tally over the years")
    xyz=helper.yearwisemedal(df,country)
    fig=px.line(xyz,x="Year",y="Medal")
    st.plotly_chart(fig)
    st.title(country + " excels in the following sports")
    pt = helper.countryheatmap(df,country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True,cmap='Blues')
    st.pyplot(fig)
    st.title("Top 10 athletes of " + country)
    top10_df = helper.mostsuccountry(df,country)
    st.table(top10_df)

if usermenu=='Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age with respect to Sports(Gold Medalist)")
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.wvh(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],palette="deep",style=temp_df['Sex'],s=20)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.mvw(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    