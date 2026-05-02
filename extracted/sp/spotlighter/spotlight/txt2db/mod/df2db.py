import tqdm
import pandas as pd
import pymysql
import sqlalchemy
pymysql.install_as_MySQLdb()
import MySQLdb    
import pyodbc

import spotlight.common.myFileDialog as myfd

class Df2Db:
    
    engine : sqlalchemy.Engine #class variable
    
    def __init__(cls, engine:sqlalchemy.Engine): #생성자 매개변수로 sqlalchemy.engine을 받는다
        cls.engine = engine 
        print("Engine connected")    
    
    def insert(cls, df : pd.DataFrame, tableName : str, chunksize=1000000): #insert dataframe to db # chunksize : 1백만. 이거보다 적으면 느려짐
        tgtNo = df.shape[0] #rows to insert        
        #pbar = tqdm.tqdm(total=tgtNo , desc="작업대상행수")

        startNo = 0
        endFlag = True
        resultInsertAcc = 0                

        while endFlag:        
            endNo = startNo + chunksize    
            if (endNo > tgtNo):
                endNo = tgtNo
                endFlag = False #이번 루프를 마지막으로 종료시키기
            dfTmp = df.iloc[startNo:endNo,:]   #df1 : 입력할 chunk
            #tmp = pbar.update(endNo-startNo)            
            resultInsert = dfTmp.to_sql(name=tableName, con=cls.engine, index=False, if_exists="append")
            #print(startNo,"/",endNo,"/ Insert 완료")
            startNo = startNo + chunksize
            resultInsertAcc = resultInsertAcc + resultInsert            
        #pbar.close()   
        print(resultInsertAcc,"행 Inserted")