#231214 : class var로 df를 지정한 후, run method에서 저장방법을 결정함

import pandas as pd
import tqdm

from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.common.ErrRetry import ErrRetryF

@ErrRetryF
class Saver(ProtoABSSelector):

    # df:pd.DataFrame

    # def __init__(self, df:pd.DataFrame):
    #     self.df = df

    def run(self):
        msg = "1. Save to Text\n"
        msg += "2. Save to parquet\n"
        msg += "3. Save to pickle\n"        
        msg += "4. Save to excel\n"        
        print(msg)
        flag = input(">>")
        match(flag):
            case '1': self._saveText()
            case '2': self._saveParquet()
            case '3': self._savePickle()
            case '4': self._saveExcel()            
            case _: print("Wrong enter")

    def _saveText(self) -> None:
        path = input("저장할 Text filename을 지정하세요(기본값 result.tsv)>>") or 'result.tsv'
        encod = input("인코딩? (cp949)>>") or 'utf8'
        sep = input("Seperator? (기본값 \\t)") or '\t'

        pbar = tqdm.tqdm(total=self.df.shape[0], desc='Save')                

        lineStart = 0
        chunksize = 10000000 #천만으로 변경
        flagFirst = True #처음에만 헤더를 넣기 위한 Flag
        while True: #헤더가 추가되는 오류 디버그 231206
            lineEnd = min(lineStart + chunksize, self.df.shape[0])
            length = lineEnd - lineStart
            if flagFirst: self.df.iloc[lineStart:lineEnd, :].to_csv(index=False, sep=sep, encoding=encod, path_or_buf=path, mode='a')            
            else: self.df.iloc[lineStart:lineEnd, :].to_csv(index=False, sep=sep, encoding=encod, path_or_buf=path, mode='a', header=None)
            pbar.update(length)
            lineStart += length

            if flagFirst: flagFirst = False
            if lineEnd >= self.df.shape[0]: break       

        print("save done")
    
    def _saveParquet(self):
        path = input("저장할 Parquet filename을 지정하세요(기본값 result.parquet)>>") or 'result.parquet'      
        self.df.to_parquet(path)
        print("save done")

    def _savePickle(self):
        path = input("저장할 Pickle filename을 지정하세요(기본값 result.pickle)>>") or 'result.pickle'      
        self.df.to_pickle(path)
        print("save done")

    def _saveExcel(self):
        path = input("저장할 Excel filename을 지정하세요(기본값 result.xlsx)>>") or 'result.xlsx'      
        self.df.to_excel(path, index=None)
        print("save done")
