import os
import pandas as pd
import spotlight.common.myFileDialog as myfd

class ReadColumnLength:
    def run(self):
        path = myfd.askopenfilename("Select a sample GL file")
        encoding = input("encoding, 기본값 cp949>>") or 'cp949'
        sep = input("sep, 기본값 tsv>>") or '\t'
        df = pd.read_csv(path, encoding=encoding, sep=sep, low_memory=False)
        
        dfTmp = pd.DataFrame()
        for column in df:
            print(column,"->", df[column].astype(str).str.len().max())
            #di[column] = df[column].astype(str).str.len().max()

            di = {'ColumnName':column,
                  'Length':df[column].astype(str).str.len().max()
                }   

            dfDi = pd.DataFrame(di, index=[0])
            dfTmp = pd.concat([dfTmp, dfDi])
        
        dfTmp.to_excel("ColumnLength.xlsx", index=False)
        print("ColumnLength.xlsx 추출완료. Table 설계하세요")        

def runReadColumnLength():
    ReadColumnLength().run()

if __name__=='__main__':
    runReadColumnLength()
    
    



