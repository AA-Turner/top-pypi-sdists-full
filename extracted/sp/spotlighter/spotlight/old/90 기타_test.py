# 추가로 제공한 4월 원장 가공. by Excel
# 엑셀을 데이터프레임으로 합친다.

# 선언부
import os
import glob
import myFileDialog as myFD
import tqdm
import pandas as pd

#1) 대상파일을 읽는다.
path = myFD.askdirectory()
listFiles = glob.glob(path + '/*.xlsx')    

pbar = tqdm.tqdm(total=len(listFiles), desc="개시")
dfNew = pd.DataFrame()
countRecord = 0

for item in listFiles:
    pbar.desc = item
    df = pd.read_excel(item)
    countRecord += df.shape[0]
    dfNew = pd.concat([dfNew,df])
    tmp = pbar.update(1)

pbar.close()


