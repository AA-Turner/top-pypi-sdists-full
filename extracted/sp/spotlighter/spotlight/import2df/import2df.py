import pandas as pd
import tqdm

import spotlight.common.myFileDialog as myfd
from spotlight.common.ErrRetry import ErrRetry
from spotlight.common.common import mapcount

class Import2Df:    
    def run(self, msg:str = "") -> pd.DataFrame:
        
        help = "1. import txt\n"
        help += "2. import parquet\n"
        help += "3. import pickle\n"
        help += "4. import Excel\n"        
        print(help)
        flag = input(">>")
        match(flag):
            case '1': return self._importTxt(msg)
            case '2': return self._importParquet(msg)
            case '3': return self._importPickle(msg)
            case '4': return self._importExcel(msg)            
            case _: print("Wrong"); pass

    @ErrRetry
    def _importTxt(self, msg:str = "Text 파일을 선택하세요.") -> pd.DataFrame:       
        path = myfd.askopenfilename(msg)
        sep = input("Seperator? (기본값 \\t)>>") or '\t'
        encod = input("인코딩? (cp949)>>") or 'cp949'        
        
        cnt = mapcount(path,encod) -1 #Count Check _ Column 때문에 1을 빼야 함
        pbar = tqdm.tqdm(total=cnt, desc='Read')        

        df = pd.DataFrame()
        chunksize = 10000000 #천만
        dfReader = pd.read_csv(path, sep=sep, encoding=encod, low_memory=False, chunksize=chunksize)
        for count, chunk in enumerate(dfReader):
            df = pd.concat([df, chunk])
            pbar.update(chunk.shape[0])
        pbar.close()
        return df

    def _importParquet(self, msg:str = "Select parquet") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)
        return pd.read_parquet(path)

    def _importPickle(self, msg:str = "Select pickle") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)
        return pd.read_pickle(path)

    def _importExcel(self, msg:str = "Select Excel") -> pd.DataFrame:
        path = myfd.askopenfilename(msg)
        return pd.read_excel(path)

def runImport2Df(msg:str = "") -> pd.DataFrame:
    return Import2Df().run(msg)

if __name__=='__main__':
    runImport2Df()