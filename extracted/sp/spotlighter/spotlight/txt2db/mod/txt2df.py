import pandas as pd
import tqdm

import spotlight.common.myFileDialog as myfd

class Txt2Df: #50만행씩 READ
    def run(cls, fileName, delimiter : chr = "\t", encoding :str = 'cp949', headerBool : bool = True, chunksize = 500000) -> pd.DataFrame :

        dfCon = pd.DataFrame()    
        totalChunk = 0        

        if headerBool: #헤더가 있다고 받았으면
            headerArg = 0
        else:
            headerArg = None

        for chunk in pd.read_csv(fileName, encoding = encoding, delimiter=delimiter, low_memory=False, header = headerArg, chunksize=chunksize):   #delimiter
            dfCon = pd.concat([dfCon,chunk])
            totalChunk = totalChunk + chunk.shape[0]
            
        #print(fileName,":",totalChunk, "행 imported")        

        return dfCon