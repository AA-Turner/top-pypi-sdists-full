import pandas as pd

from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.save.save import Saver
from spotlight.common.ErrRetry import ErrRetryF
import spotlight.common.myFileDialog as myfd

class SaverPart(ProtoABSSelector):

    ref:str
    refLi:list
    cName:str
    dfTmp:pd.DataFrame

    def run(self):
        self.cName = self.selectColumn("기준컬럼 선택")

        msg = "1. 1개 기준으로 추출 (특정 계정과목만 추출하는 경우 등 )\n"
        msg += "2. 다중 기준으로 추출 (다수 계정과목을 추출하는 경우 등) : 직접 입력\n"
        msg += "3. 다중 기준으로 추출 (다수 계정과목을 추출하는 경우 등) : 엑셀로 Import\n"
        print(msg)
        flag = input(">>")
        match(flag):
            case '1': self.dfTmp = self._single()
            case '2': self.dfTmp = self._multi1()
            case '3': self.dfTmp = self._multi2()
            case _: print("잘못 입력");return
        
        print("추출결과>> ")
        print(str(self.dfTmp.shape[0])+ "행")
        print(self.dfTmp.head(10))
        print("저장합니다...")
        Saver(self.dfTmp).run()
    
    @ErrRetryF
    def _single(self) -> pd.DataFrame:
        print("단일 기준으로 추출합니다. i.e. 특정 1개 계정과목 원장만 추출")
        self.ref = self._setValue()        
        return self.df[self.df[self.cName] == self.ref]

    @ErrRetryF
    def _multi1(self) -> pd.DataFrame:
        print("복수 기준으로 추출합니다. i.e. 특정 계정과목들에 해당하는 원장만 추출 : 직접 입력")        
        self.refLi = self._addList()
        return self.df.loc[self.df[self.cName].isin(self.refLi)]

    @ErrRetryF
    def _multi2(self) -> pd.DataFrame:
        print("복수 기준으로 추출합니다. i.e. 특정 계정과목들에 해당하는 원장만 추출 : 엑셀로 입력받음")        
        dfTmp = pd.read_excel(myfd.askopenfilename("Select excel file"))        
        cNameTgt = self.selectColumn("엑셀에서 추출한 내역 중 필요한 컬럼 선택", dfTmp)
        self.refLi = dfTmp[cNameTgt].drop_duplicates().to_list() #중복을 제거함
        if input("String으로 변환하려면 Y>>") == 'Y': self.refLi = list(map(str,self.refLi))
        print(self.refLi)
        return self.df.loc[self.df[self.cName].isin(self.refLi)]

    def _addList(self) -> list:
        refLi:list = []
        print("입력을 받습니다..  (종료하려면 q)")
        while True:
            refTmp = self._setValue()
            if refTmp == 'q': return refLi            
            refLi.append(refTmp)
            print("현재 목록:")
            print(refLi)

    def _setValue(self) -> str | int:
        refTmp = input("추출할 값을 입력하세요(문자열)>>")
        if input("문자열로 적용하려면 1, 숫자로 형변환하려면 2(int로 형변환)>>") == '2': refTmp = int(refTmp)
        return refTmp



