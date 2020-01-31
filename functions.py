import pandas as pd

def column_cleaner(df):
    '''
    Takes a df as input and:
    1. deletes de index column since it's unnecessary
    2. changes the format of date to datatime
    3. add a "," next to the city removing "|" 
    4. some reviesw have the string "\ao" so it needs to be removed from the review.
    '''
    del df['index']
    # rename columns to delete white space from the column names
    df.columns = ['username', 'location', 'date', 'rating', 'content']
    df['date'] = pd.to_datetime(df['date'])
    df['location'] = df['location'].apply(lambda x: x.replace('|', ','))
    df['content'] = df['content'].apply(lambda x: x.replace('\xa0', ''))
    return df

def clean_data(df):
    '''unifies all the column changes from column_cleaner
    to be applied to the dataframe'''
    df = column_cleaner(df)
    return df