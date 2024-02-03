import pandas as pd

def preprocess(df,rdf):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with rdf
    df = df.merge(rdf, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df