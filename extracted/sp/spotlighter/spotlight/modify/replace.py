import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF

#정규식 추가할 수 있도록 변경 (정규식 before, after 받음)
'''
콤마 없애기 : '[,]',''
공백 없애기 : '[ ]',''
마지막 - 없애기 : '[-]$',''
'''
class Replacer:

    df:pd.DataFrame

    def __init__(self, df:pd.DataFrame):
        self.df = df

    @ErrRetryF
    def run(self, cName:str) -> None: #콤마 없애기

        self.df[cName] = self.df[cName].astype('string') #DEBUG : STRING
        print("string type으로 변경함")

        msg = "1. Kill Comma\n"
        msg += "2. Kill Space\n"
        msg += "9. User-defined Regular expression\n"
        print(msg)
        flag = input(">>")
        
        strBefore:str;strAfter:str
        
        match(flag):
            case '1': strBefore = '[,]' ; strAfter = ''
            case '2': strBefore = '[ ]' ; strAfter = ''
            case '9':
                strBefore = input("변경전 정규식을 직접 입력하세요. (i.e. [-]$) (기본값 : '[ ]')>>") or '[ ]'
                strAfter = input("변경후 정규식을 직접 입력하세요. (기본값 : '')>>") or ''
            case _:
                print("잘못 입력하였습니다."); return

        self._doReplace(cName,strBefore,strAfter)
        print("DONE")

    def _doReplace(self, cName:str, strBefore:str, strAfter:str) -> None:
        self.df[cName] = self.df[cName].replace(strBefore,strAfter,regex=True)
