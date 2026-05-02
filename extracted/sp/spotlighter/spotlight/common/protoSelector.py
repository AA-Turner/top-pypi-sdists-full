#For inheritance
#Class var : df
#Class method : selectColumn

from abc import ABCMeta
from abc import abstractmethod

import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

class ProtoSelector:
    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame = None): #의존성 주입
        self.df = df

    @ErrRetryF
    def selectColumn(self, msg:str = "Select column", df:pd.DataFrame = None) -> str: #DF Injection은 선택. 기본값은 self.df 사용
        print('\n'+msg+'\n')
        if not isinstance(df,pd.DataFrame): df = self.df # USE Self.df when no injected df
        df.info()
        num = input(">>")
        num = int(num) 
        cName = df.columns[num] #선택한 번호에 해당하는 컬럼명을 반환한다.
        return cName
    
class ProtoABSSelector(ProtoSelector, metaclass=ABCMeta):
    @abstractmethod
    def run(self):
        pass



