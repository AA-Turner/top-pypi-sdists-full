import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class M100:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cName:str): #100을 곱해준다

        self.df[cName] = self.df[cName].astype('float64')

        self.df[cName] = self.df[cName] * 100

        print("DONE")
        
