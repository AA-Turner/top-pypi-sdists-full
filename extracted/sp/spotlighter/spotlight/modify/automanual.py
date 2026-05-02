import numpy as np
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class AutoManual:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cNameBase:str, cNameAM:str): 

        strFlag = input("자동전표 기준으로 포함할 문자열을 입력하세요(복수는 Pipe 사용) (ex1. Auto) (ex2. Auto|System)  >>") or 'Auto'
        strA = input("자동전표인 경우 입력할 문자열(기본값 A)>>") or 'A'
        strM = input("기타 수동전표인 경우 입력할 문자열(기본값 M)>>") or 'M'        

        self.df[cNameAM] = np.where( self.df[cNameBase].str.contains(strFlag) , strA, strM)

        print("DONE")
        
