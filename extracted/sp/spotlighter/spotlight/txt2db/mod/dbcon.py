import pandas as pd
import pymysql
import sqlalchemy
pymysql.install_as_MySQLdb()
import MySQLdb    
import pyodbc

import spotlight.common.myFileDialog as myfd

class DbCon:

    def connect(cls, flag:str = 'mysql', dbName : str = 'spotlight') -> sqlalchemy.Engine:

        mySQL_ID = input("ID? (DBMS)>>")
        mySQL_PW = input("Password? (DBMS)>>")

        if flag=="mysql":
            #mySQL_ID = ""
            #mySQL_PW = ""
            #mySQL_DB = 'spotlight'
            mySQL_DB = dbName
            #MySQL에 연결하는 경우
            engine = sqlalchemy.create_engine("mysql+mysqldb://"+mySQL_ID+":"+mySQL_PW+"@127.0.0.1/"+mySQL_DB+"?charset=utf8")

        elif flag=="mssql":
            #MSSQL에 연결하는 경우
            engine = sqlalchemy.create_engine("mssql+pyodbc://SA:qkrguddnjs1!@mymssql")
            #engine.connect()
        
        engine.connect()
        print("DB에 연결되었습니다.")
        return engine #engine을 반환 

