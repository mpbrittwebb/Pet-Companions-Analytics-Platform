import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import streamlit as st



def preprocess(df):
    
    df.dropna(axis=1, inplace=True, how='all')
    df.dropna(axis=0, inplace=True, how='all')
    
    df.drop(labels = [ 'Pet Companions, inc.','Unnamed: 2', 'Unnamed: 7', 
                    'Unnamed: 13', 'Unnamed: 18', 'Unnamed: 21', 'Unnamed: 23',
                     'Unnamed: 24', 'Unnamed: 26', 'Unnamed: 28'], 
               axis = 1, inplace = True)
    
    df.rename(columns={'Unnamed: 3':'Client', 'Unnamed: 4':'Dog', 'Unnamed: 8':'Phone', 
                       'Unnamed: 11':'Breed', 'Unnamed: 14': 'Email', 'Unnamed: 17': 'Dog Gender',
                        'Unnamed: 22':'Full Days', 'Unnamed: 27':'Half Days', 'Unnamed: 29':'Dog Half Days'}, inplace=True)

    df[['Full Days', 'Half Days', 'Dog Half Days']] =  df[['Full Days', 'Half Days', 'Dog Half Days']].fillna(value=0)


    df.reset_index(drop=True, inplace=True)
    df.drop(axis=0, index=[0, 1], inplace=True)
    df.reset_index(drop=True, inplace=True)

    #typecast DogName from NaN to string
    df['Client'] = df['Client'].fillna("NaN")

    #typecast DogName from NaN to string
    df['Dog'] = df['Dog'].fillna("NaN")

    #typecast DogBreed from NaN to string
    df['Breed'] = df['Breed'].fillna("NaN")
    
    #set NaN full days to 0
    df['Full Days'] = df['Full Days'].fillna(0)
    
    #set NaN half days to 0
    df['Half Days'] = df['Half Days'].fillna(0)
    
    return df
    
    
    
#move all rows just containing dogs to rows with people
def match_dog_to_owner(df, deceased_dogs):
    #given a row with a dog move its information to a row with a person
    def move_dog(df, i, deceased_dogs):
        
        #counter starting at current row
        n = i
        
        #find row we want to move to
        while(df.loc[n,'Client'] == "NaN"): 
            n -= 1
        
        dogs = deceased_dogs.loc[deceased_dogs['Client']==df.loc[n,'Client'], 'Dog'].reset_index(drop=True)
        
        #check for another dog
        if df.loc[n, 'Dog']== "NaN":
        #no dog found
        
            
            if dogs.empty:
                
                df.loc[n,'Dog'] = df.loc[i,'Dog']
                 #move DogBreed
                df.loc[n,'Breed'] = df.loc[i, 'Breed']
            elif not df.loc[i,'Dog'] in dogs[0]:
                df.loc[n,'Dog'] = df.loc[i,'Dog']
                #move DogBreed
                df.loc[n,'Breed'] = df.loc[i, 'Breed']
              
            #move FullDays
            df.loc[n,'Full Days'] = df.loc[n,'Full Days'] + df.loc[i, 'Full Days']
              
            #move HalfDays
            df.loc[n,'Half Days'] = df.loc[n,'Half Days'] + df.loc[i,'Half Days'] + df.loc[i,'Dog Half Days']
            
        else:
            # owner has more than 1 dog
            if dogs.empty:
                df.loc[n, 'Dog'] = df.loc[n, 'Dog'] + ", " + df.loc[i, 'Dog']

                #add dog breed
                df.loc[n, 'Breed'] = df.loc[n, 'Breed'] + ", " + df.loc[i, 'Breed']
        
            
            elif not df.loc[i,'Dog'] in dogs[0]:
                #add another dog
                df.loc[n, 'Dog'] = df.loc[n, 'Dog'] + ", " + df.loc[i, 'Dog']

                #add dog breed
                df.loc[n, 'Breed'] = df.loc[n, 'Breed'] + ", " + df.loc[i, 'Breed']
            
            #add FullDays
            df.loc[n,'Full Days'] = df.loc[n, 'Full Days'] + df.loc[i, 'Full Days']
            
            #add HalfDays
            df.loc[n, 'Half Days'] = df.loc[n, 'Half Days'] + df.loc[i, 'Half Days'] + df.loc[i, 'Dog Half Days']
                
        return df
        
              
    #counter variable for index tracking
    i = 0
    
    #iterate through index
    while (i < len(df)):
        if df.loc[i,'Client'] == "NaN":
            df = move_dog(df, i, deceased_dogs)
        i += 1

    df = df[df['Client']!="NaN"]
    df = df[['Client', 'Email', 'Phone', 'Dog', 'Breed', 'Full Days', 'Half Days']]
    
    return df


def sort_by_remaining(df):
    #create a column with total owed days
    df['TotalDays'] = df['Half Days'] + df['Full Days']
    
    #sort on this column
    df.sort_values('TotalDays', inplace=True)
    
    #remove
    df.drop(columns=['TotalDays'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    return df

def suggested_renewal(name, packages_df, daycare_df):
    days_left = packages_df.loc[packages_df['Client']==name, 'Full Days'].reset_index(drop=True)[0] + packages_df.loc[packages_df['Client']==name, 'Half Days'].reset_index(drop=True)[0]
    future_visits = daycare_df[(daycare_df['Client']==name) & (daycare_df['Date'] >= date.today())]
    
    if len(future_visits) == 0: 
        packages_df.loc[packages_df['Client']==name, 'Suggested Renewal Date'] = 'no scheduled visits'
    elif days_left > len(future_visits) + 1:
        packages_df.loc[packages_df['Client']==name, 'Suggested Renewal Date'] = 'sufficient days left'
    elif days_left <= 1 and len(future_visits)>=1:
        packages_df.loc[packages_df['Client']==name, 'Suggested Renewal Date'] = 'renew now'
    else:
        renewal_date = future_visits.reset_index(drop=True).loc[days_left - 2, 'Date']
        packages_df.loc[packages_df['Client']==name, 'Suggested Renewal Date'] = renewal_date
    return packages_df


def daycare_visits(df, daycare_df):

    customer_names = list(df['Client'])
    
    df['Daycare Visits Last 90 Days'] = 0
    df['Suggested Renewal Date'] = ''
    
    
    days_since = date.today() - timedelta(days=90)
    for name in customer_names:
        df.loc[df['Client']==name, 'Daycare Visits Last 90 Days'] = len(daycare_df[(daycare_df['Client']==name) & (daycare_df['Date'] >= days_since) & (daycare_df['Date'] <= date.today())])
        test = daycare_df[(daycare_df['Client']==name) & (daycare_df['Date'] >= date.today())]
        df = suggested_renewal(name, df, daycare_df)
        
    return df

@st.cache_data
def Outstanding_Packages(file, deceased, daycare_report):
    df = pd.read_excel(file)
    df = preprocess(df)
    df = match_dog_to_owner(df, deceased)
    df = sort_by_remaining(df)
    df = df.reset_index(drop=True)
    df = daycare_visits(df, daycare_report)
    return df