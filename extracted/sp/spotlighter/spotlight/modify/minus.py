import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

#SAP 전표 다음 유형 2가지를 음수로 바꿔주는 클래스
# 유형1 : (100)
# 유형2 : 100-
class ToMinus:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df
    
    def run(self, cName:str):
        flag = input("1. (), 2. 후위- >>")
        match flag:
            case '1': self.runBracket(cName)
            case '2': self.runPostfix(cName)
            case _: print("아무것도 입력하지 않았습니다.")
    
    @ErrRetryF
    def runBracket(self, cName:str): #()

        self.df[cName] = self.df[cName].astype('str')

        self.df[cName] = self.df[cName].replace('[)]','',regex=True)
        self.df[cName] = self.df[cName].replace('[()]','-',regex=True)

        self.df[cName] = self.df[cName].astype('float64')

        print("DONE")

    @ErrRetryF
    def runPostfix(self, cName:str): #()
        
        self.df[cName] = self.df[cName].astype('str')    

        self.df[cName] = self.df[cName].apply(self.InvertMinus)

        self.df[cName] = self.df[cName].astype('float64')
                
        print("DONE")

    def InvertMinus(self, tgt:str) -> str:
        if len(tgt) <= 1 : return tgt #1글자거나(-) 1글자보다 적으면('') 그냥 바로 반환
        if tgt[-1] == '-':
            tgt = tgt.replace('-','')
            tgt = "-" + tgt
            return tgt
        return tgt