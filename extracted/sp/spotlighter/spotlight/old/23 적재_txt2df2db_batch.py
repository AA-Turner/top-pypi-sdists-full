#전역부
from mylib import txt2df2db as mytdd
from mylib import myFileDialog as myfd
import os
import glob
import tqdm
import sys

def batch():
    
    path = myfd.askdirectory()
    listFiles = glob.glob(path + '/*.txt')

    pbar = tqdm.tqdm(total=len(listFiles) , desc="Files 순환")    

    for i in listFiles:
        pbar.desc = i

        print("Start:")        
        fileName = i
        chunksize = int(sys.argv[1])
        df = mytdd.txt2df(fileName, "\t", True, chunksize)
        mytdd.df2db(df, 'frl', 'frl_new', chunksize) #두번째 인자 : 연결할 데이터베이스
        print("End:")

        pbar.update(1)
    pbar.close()

#MAIN
if(__name__ == "__main__"):
    mytdd.getArgv1() #매개변수 없으면 추가
    print("순환을 개시합니다.")
    batch()

    