import pandas as pd

from spotlight.read import runReadColumnLength
from spotlight.txt2db import runTxt2Db
from spotlight.concatText import runConcatText
from spotlight.concatText import runConcatText
from spotlight.concatText.concatTextTest import ConcatTextTest
from spotlight.import2df.import2df import runImport2Df
from spotlight.save.save import Saver
from spotlight.save.savePart import SaverPart
from spotlight.automap.automap import AutoMap
from spotlight.modify.modify import Modifier
from spotlight.recon.recon import ReconGL
from spotlight.merge.merge import Merger
from spotlight.common.colors import Colors
from spotlight.common.protoSelector import ProtoABSSelector

class Spotlight(ProtoABSSelector):
    df:pd.DataFrame    
    def run(self):
        text =  "#"*10+"\n"
        text += Colors.RED + "\nPreprocessing\n" + Colors.END
        text += "11. Excel to Text\n"    
        text += "12. concatenate text\n"    
        text += "13. check text header (TEST)\n"    
        text += "14. Merge Text (i.e. BSEG+BKPF) (if already set df, automatically transferred to dfA)\n"    

        text += Colors.RED + "\nUSE SQL\n" + Colors.END
        text += "21. To Insert to SQL, Read columns'length\n"
        text += "22. Create Table => with mySQL\n"
        text += "23. Import file and Insert to DB\n"

        text += Colors.RED + "\nMain Run\n" + Colors.END
        text += "31. Read text to dataframe\n"
        text += "32. Auto_MAP\n"
        text += "33. Modify mode(After Auto_MAP)\n" #조정자는 별도 클래스로 분리 #아직 미구현        
        text += "34. To recon G/L and T/B, export SUM(AMT LC)groupby Acct\n" #조정자는 별도 클래스로 분리 #아직 미구현        

        text += Colors.RED + "\nSave\n" + Colors.END
        text += "41. Save text(임시파일 Load는 31 활용)\n"
        text += "42. Save a part of df(특정 계정과목 추출 등)\n"        

        text += Colors.RED + "\nGeneral\n" + Colors.END
        text += "90. MANUAL HANDLING - DEBUG\n"
        text += "98. df.info()\n"        
        text += "99. df.head(10)"

        #####
        textMain = Colors.RED + "MAIN MODE : enter '?' to help / 'q' to exit" + Colors.END

        while True:

            print("") #여기다 BREAK를 걸면 디버깅

            print(textMain)
            flag = input(">>")

            match flag:
                case '?': print(text)
                case 'q': print("END"); break
                
                case '11': print("USE VBA...(추후 연동예정)")
                case '12': runConcatText()
                case '13': ConcatTextTest().run()
                case '14': 
                    if isinstance(self.df, pd.DataFrame): self.df = Merger(self.df).run()
                    else: self.df = Merger().run()

                case '21': runReadColumnLength()
                case '22': print("USE mySQL")
                case '23': runTxt2Db()

                case '31': self.df = runImport2Df()
                case '32': self.df = AutoMap().autoMap(self.df)
                case '33':
                    md = Modifier(self.df) #의존성 주입
                    md.run()
                case '34': ReconGL(self.df).run()

                case '41': Saver(self.df).run()
                case '42': SaverPart(self.df).run()                
                case '90':
                    print("DEBUG NOW") #여기다 BREAKPOINT를 걸면 수기 디버깅가능
                case '98': self.df.info()
                case '99': print(self.df.head(10))
                case _: print("Retry"); continue

def run(): 
    spot = Spotlight()
    spot.run()

if __name__=="__main__":
    run()
