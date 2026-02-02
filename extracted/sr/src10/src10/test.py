import numpy as np
import pandas as pd
import configtrans1
import config_trans2
import configtrans4
import config_trans6


orig_df_columns_names = [
    'loggername',
    'year', # Longest shell measurement
    'month', # perpendicular to length
    'day', # with meat in shell
    'hour', # whole abalone
    'minute', # weight of meat
    'power'] # after being dried

orig_df_columns_dtype = {
    'loggername': "category",
    'year': "float64",
    'month': "float64",
    'day': "float64",
    'hour': "float64",
    'minute': "float64",
    'power': "float64"}

modified_df_columns_names = [
    'year', # Longest shell measurement
    'month', # perpendicular to length
    'day', # with meat in shell
    'hour', # whole abalone
    'logger1',
    'logger2'] # after being dried

modified_df_columns_dtype = {
    'year': "float64",
    'month': "float64",
    'day': "float64",
    'hour': "float64",
    'logger1': "float64",
    'logger2': "float64"}

anomalies_columns_names = [
    'score',
    'cutoff'
] # after being dried

anomalies_columns_dtype = {
    'score': "float64",
    'cutoff': "float64"
}

scores_columns_names = [
    'score'
] # after being dried

scores_columns_dtype = {
    'score': "float64"
}

cleandata1 = configtrans1.cleandatatransformer()

def cleandata():
    print("cleandata")
    df = pd.read_csv("000000_03.csv", header=None)

    if len(df.columns) == len(orig_df_columns_names):
           df.columns = orig_df_columns_names
                
    print(df)
    global cleandata1
    cleandata1.fit(df)
    return cleandata1.transform(df)
    
def standard_deviation(val):
    print("standard_deviation")
    df=pd.DataFrame(val)
    if len(df.columns) == len(modified_df_columns_names):
           df.columns = modified_df_columns_names
    print(df)
    aa = config_trans2.stddevtransformer()
    aa.fit(df)
    aa.transform(df)
    
def rcf():
        print("rcf")
        df = pd.read_csv("rcf_output.csv", header=None)
        print(df)
        return df.values
    
def cutoffscores(val):
    print("cutoffscores")
    df=pd.DataFrame(val)
    if len(df.columns) == len(scores_columns_names):
           df.columns = scores_columns_names
    print(df)
    aa = configtrans4.cutoffscorestransformer()
    aa.fit(df)
    return aa.transform(df)
    
def cleandata2(val):
    print("cleandata2")
    df=pd.DataFrame(val)
    if len(df.columns) == len(anomalies_columns_names):
           df.columns = anomalies_columns_names
            
    df.to_csv('cutoffscores.csv', index=False)
    print(df)
    global cleandata1
    return cleandata1.transform(df)
    
def finalresults(val):
    print("finalresulttransformer")
    df=pd.DataFrame(val)
    if len(df.columns) == (len(modified_df_columns_names)+len(anomalies_columns_names)):
           df.columns = modified_df_columns_names + anomalies_columns_names
    print(df)
    aa = config_trans6.finalresulttransformer()
    aa.fit(df)
    aa.transform(df)
    
    
    
    
val = cleandata()
val1 = standard_deviation(val)
val2 = rcf()
val3 = cutoffscores(val2)
val4 = cleandata2(val3)
val5 = finalresults(val4)