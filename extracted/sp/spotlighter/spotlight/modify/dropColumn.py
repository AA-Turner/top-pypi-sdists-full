import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class DropColumn:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cName:str): #Drop Column
        self.df.drop(columns=[cName], inplace=True) #use inplace
        print("DONE")
        
