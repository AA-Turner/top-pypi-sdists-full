import pandas as pd

import spotlight.common.myFileDialog as myfd

from spotlight.common.ErrRetry import ErrRetryF


class AutoMap:

    @ErrRetryF
    def autoMap(self, df:pd.DataFrame)->pd.DataFrame : 

        print("Auto Mapping. Read 매핑파일")
        #filenameImportMap = "ImportMAP.xlsx"
        #filenameImportMap = glob.glob(tgtdir+"/"+filenameImportMap)
        filenameImportMap = myfd.askopenfilename("MAP파일 선택")    
        dfMap = pd.read_excel(filenameImportMap, sheet_name='MAP_GL')

        ## a. MAP 대상 먼저 전처리
        dfMapMap = dfMap[dfMap['방법'] == 'MAP']
        dfTB = pd.DataFrame()
        for i in range(0, dfMapMap.shape[0]):    
            try:
                dfTB[dfMapMap.iloc[i]["tobe"]] = df[dfMapMap.iloc[i]["asis"]]
            except:
                dfTB[dfMapMap.iloc[i]["tobe"]] = df[str(dfMapMap.iloc[i]["asis"])]

        ## b. KEYIN 대상 추가 전처리
        dfMapKeyin = dfMap[dfMap['방법'] == 'KEYIN']

        for i in range(0, dfMapKeyin.shape[0]):        
            dfTB[dfMapKeyin.iloc[i]["tobe"]] = dfMapKeyin.iloc[i]["asis"]


        print("AUTO-MAP Done")
        return dfTB            