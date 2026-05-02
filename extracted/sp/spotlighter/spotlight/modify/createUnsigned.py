import numpy as np
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class CreateUnsigned:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame): self.df = df

    #차대구분에 따라 (-)처리 : 변경컬럼선택 / 차대컬럼선택 / 차변구분자 선택 / 시행
    @ErrRetryF    
    def run(self, cNameSigned:str, cNameUnsignedD:str, cNameUnsignedC:str): 

        #먼저 float64로 바꾼다
        self.df[cNameSigned] = self.df[cNameSigned].astype('float64')

        #Run        
        self.df[cNameUnsignedD] = np.where(self.df[cNameSigned] >= 0
                 , self.df[cNameSigned]
                 , 0)
        
        self.df[cNameUnsignedC] = np.where(self.df[cNameSigned] < 0
                 , self.df[cNameSigned] * -1
                 , 0)

        print("DONE")
        
