#RECON 파일 추출
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.modify.modify import Modifier

class ReconGL(Modifier): #Inherit Modifier to use 'selectColumn'

    @ErrRetryF    
    def run(self):
        cNameAcct = self.selectColumn("Select Account Number (to group by)")
        cNameAmt = self.selectColumn("Select Amount LC (to sum)")
        self.export(cNameAcct, cNameAmt)
    
    def export(self, cNameAcct:str, cNameAmt:str): #cName1 : 변경할 컬럼, #cName2 : 차대컬럼

        #먼저 float64로 바꾼다
        self.df[cNameAmt] = self.df[cNameAmt].astype('float64')

        #Run
        fileName = input("검증결과 추출할 파일명을 입력하세요(기본값 GL_RECON.xlsx)>>") or 'GL_RECON.xlsx'
        
        self.df.groupby(cNameAcct)[cNameAmt].sum().to_excel(fileName)
        
        print("DONE")
        

