import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class FillNA:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cName:str): #fillna(0)

        flag = input("dtype이 object 또는 str입니까? (기본값 Y)>>")
        if flag:
            self.df[cName] = self.df[cName].fillna('0')
        else:
            self.df[cName] = self.df[cName].fillna(0)
                    
        print("DONE")
        
