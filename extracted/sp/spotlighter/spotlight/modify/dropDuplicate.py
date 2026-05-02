    
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class DropDuplicate:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self): #Drop Column
        print("drop_duplicates() with imported df")                
        cntBefore = self.df.shape[0]
        self.df.drop_duplicates(inplace=True)
        cntAfter = self.df.shape[0]
        print("제거된 중복행수 = ", cntBefore - cntAfter)
        print("DONE")
    
