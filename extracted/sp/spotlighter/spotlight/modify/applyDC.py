import numpy as np
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class ApplyDC:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame): self.df = df

    #차대구분에 따라 (-)처리 : 변경컬럼선택 / 차대컬럼선택 / 차변구분자 선택 / 시행
    @ErrRetryF    
    def run(self, cName1:str, cName2:str): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼

        #먼저 float64로 바꾼다
        self.df[cName1] = self.df[cName1].astype('float64')

        #Run
        IndicatorDebit = input("Indicator의 차변구분자를 입력하세요(기본값 'D')>>") or 'D'        
        self.df[cName1] = np.where(self.df[cName2] == IndicatorDebit
                 , self.df[cName1]*1
                 , self.df[cName1]*(-1))
        
        print("DONE")
        
