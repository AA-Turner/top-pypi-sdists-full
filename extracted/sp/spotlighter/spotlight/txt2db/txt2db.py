import glob

import pandas as pd
import tqdm
import sqlalchemy

from spotlight.common import myFileDialog as myfd
from spotlight.txt2db.mod.dbcon import DbCon
from spotlight.txt2db.mod.txt2df import Txt2Df
from spotlight.txt2db.mod.df2db import Df2Db

class Txt2Db:

    path : str
    listFiles : list

    objEngine : sqlalchemy.Engine

    def run(cls):                
        cls.path = myfd.askdirectory() #폴더를 input 받는다.        
        cls.checkFiles() #폴더 내 텍스트 배열을 인식한다.   
        cls.importAndInsert() #파일을 순환 : import / insert

    def checkFiles(cls):
        ext = input("확장자(기본값, tsv)>>") or 'tsv'
        cls.listFiles = glob.glob(cls.path+'/*.'+ext)
        print(cls.listFiles)
    
    def importAndInsert(cls):
        cls.objEngine = DbCon().connect() #DB 연결

        pbar = tqdm.tqdm(total=len(cls.listFiles))
        objT2D = Txt2Df() #create object to import textfile
        objD2D = Df2Db(cls.objEngine)

        i = 0

        for file in cls.listFiles: #파일을 순환하면서,
            pbar.set_description(file)

            df = objT2D.run(file) #IMPORT
            objD2D.insert(df, 'lse') #and insert
            
            pbar.update(1)          
            # i += 1
            # if i == 1: print("DEBUG END"); break
        
        pbar.close()

def runTxt2Db(): #CALLER
    Txt2Db().run()
