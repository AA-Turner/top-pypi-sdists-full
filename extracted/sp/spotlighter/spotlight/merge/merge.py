#DATAFRAME MERGE
import pandas as pd

from spotlight.common.ErrRetry import ErrRetryF
from spotlight.common.protoSelector import ProtoABSSelector
from spotlight.modify.modify import Modifier
from spotlight.import2df.import2df import runImport2Df
from spotlight.save.save import Saver
from spotlight.common.colors import Colors
from spotlight.merge.setkey import SetKey

class Merger(ProtoABSSelector): #Inherit Modifier to use 'selectColumn'
    dfA:pd.DataFrame
    dfB:pd.DataFrame
    dfJoin:pd.DataFrame
    #상속받은 df변수를 dfNow 성격으로 재활용함    
    flag:str #A | B | Join | NONE, 기본값 NOT
    
    def __init__(self, df:pd.DataFrame = None): #OVERRIDE
        if isinstance(df, pd.DataFrame): self.dfA = df
        else: pass        
        self.flag = "NONE"
    
    @ErrRetryF    
    def run(self) -> pd.DataFrame:

        text =  Colors.RED + "#"*10+"\n" + Colors.END
        text += "11. Set DF1\n"    
        text += "12. Set DF2\n"
        text += "21. MODIFY\n"
        text += "31. Join(Merge) DF1 & DF2\n"
        text += "41. Export DFJoin to textfile\n"
        text += "42. Connect DFJoin to Main Mode (이어서 바로 작업할 수 있게)\n\n"
        text += "50. Select DF(1,2,Join 중에) => MODIFY, Export, Connect와 연계됨\n\n"
        text += Colors.RED + "General\n" + Colors.END
        text += "90. MANUAL HANDLING - DEBUG\n"
        text += "91. df1.info()\n"        
        text += "92. df1.head(10)\n"        
        text += "93. df2.info()\n"        
        text += "94. df2.head(10)\n"
        text += "95. dfJoin.info()\n"        
        text += "96. dfJoin.head(10)\n"

        #####
        textMain = Colors.RED + "JOIN MODE : enter '?' to help / 'q' to exit" + Colors.END
        if self.flag != "NONE": textMain += Colors.RED + "Selected df:" + self.flag + Colors.END

        while True:

            print(textMain)
            flag = input(">>")

            match flag:
                case '?': print(text)
                case 'q': print("END to Main mode"); break                
                
                case '11': self.dfA = runImport2Df("Join할 파일을 선택하세요(1)")
                case '12': self.dfB = runImport2Df("Join할 파일을 선택하세요(2)")

                case '21': self.enterModify()
                
                case '31': 
                    self._merge()
                    self._selectDF('Join')

                case '41': Saver(self.df).run()
                case '42': print("Return to main mode with selected df"); return self.df

                case '90':
                    print("DEBUG NOW") #여기다 BREAKPOINT를 걸면 수기 디버깅가능
                case '91': self.dfA.info()
                case '92': print(self.dfA.head(10))

                case '93': self.dfB.info()
                case '94': print(self.dfB.head(10))

                case '95': self.dfJoin.info()
                case '96': print(self.dfJoin.head(10))

                case _: print("Retry"); continue

    def _merge(self) -> None:        
        #cNameJoinA:str = self.selectColumn("Select Join Column (df1)", self.dfA)
        #cNameJoinB:str = self.selectColumn("Select Join Column (df2)", self.dfB)
        cNameJoinA:list = SetKey(self.dfA).run("set Key : dfA")
        cNameJoinB:list = SetKey(self.dfB).run("set Key : dfA")        
        
        if not self.check(cNameJoinA, cNameJoinB): print("중단합니다."); return #VALIDATE

        howMerge = input("Select join method(기본값 : inner)>>") or 'inner'

        if (input("USE Indicator? (기본값 : N)") or 'N') == 'Y': self.dfJoin = self.dfA.merge(right=self.dfB, left_on=cNameJoinA, right_on=cNameJoinB, how=howMerge, indicator=True)
        else: self.dfJoin = self.dfA.merge(right=self.dfB, left_on=cNameJoinA, right_on=cNameJoinB, how=howMerge)

        print("dfA 행수 : ",self.dfA.shape[0])
        print("dfB 행수 : ",self.dfB.shape[0])
        print("dfJoin 행수 : ",self.dfJoin.shape[0])
        #print("검증 : ", self.dfJoin.shape[0] == self.dfA.shape[0] + self.dfB.shape[0])

        print("DONE")
        
    def check(self, cNameJoinA:list, cNameJoinB:list) -> bool:
        print("신뢰성 있는 JOIN을 위해서는 LEFT-KEY와 RIGHT-KEY가 PRIMARY KEY여야 합니다. (이외의 경우 중복값 발생)")
        print("(i.e. Left outer join 시에는 Right Table의 KEY가 PK여야만 함 (LEFT는 상관없음))")
        print(Colors.CYAN+"테스트를 실시합니다."+Colors.END)
        print("dfA>>")
        bA = self._checkDetail(self.dfA, cNameJoinA)
        print("dfB>>")
        bB = self._checkDetail(self.dfB, cNameJoinB)

        if bA and bB: print("검증 PASS. 진행합니다."); return True
        else: #검증에 실패했을 때
            flag = input("검증실패. 그럼에도 불구하고 진행하겠습니까?\n 이 경우 join으로 record count가 늘어나 신뢰성을 보장할 수 없습니다.(기본값 N)>>") or 'N'
            match(flag):
                case 'Y': return True
                case 'N': return False
                case _: print("잘못된 값 입력. 종료합니다."); return False

    #각 DF별 체크하는 메서드
    def _checkDetail(self, df:pd.DataFrame, cName:list) -> bool:
        dfValueCount = df[cName].value_counts()
        result = dfValueCount[(dfValueCount != 1)]

        if result.shape[0] == 0: print("중복되는 KEY가 없습니다."); return True
        elif result.shape[0] != 0: print("중복이 있는 KEY>>"); print(result); return False   

    def enterModify(self):
        print("entering modify mode to modify df(selected)...")
        flag:str = input("A or B or Join>>")
        dfTmp:pd.DataFrame
        match(flag):
            case 'A': dfTmp = self.dfA
            case 'B': dfTmp = self.dfB
            case 'Join': dfTmp = self.dfJoin
            case _: print("잘못된 입력입니다."); return
        Modifier(dfTmp).run()        

    def _selectDF(self, flag:str = ''):
        print("Select DF...")
        if flag in ['A','B','Join']: self.flag = flag
        else: self.flag:str = input("A or B or Join>>")
        match(self.flag):
            case 'A': 
                if isinstance(self.dfA,pd.DataFrame): self.df = self.dfA
                else: print("dfA not loaded yet")
            case 'B':
                if isinstance(self.dfB,pd.DataFrame): self.df = self.dfB
                else: print("dfB not loaded yet")
            case 'Join':
                if isinstance(self.dfJoin,pd.DataFrame): self.df = self.dfJoin
                else: print("dfJoin not loaded yet")            
            case _: print("잘못된 입력입니다."); return
        print("현재 선택된 df:"+self.flag)
        