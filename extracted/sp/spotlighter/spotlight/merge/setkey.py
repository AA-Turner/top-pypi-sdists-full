import pandas as pd

from spotlight.modify.modify import Modifier
from spotlight.common.colors import Colors

class SetKey(Modifier): #Inhereted Modifier, so initializer has df var.

    cName:list #무조건 List로 받는다.    

    def __init__(self, df:pd.DataFrame = None): #Override
        self.df = df
        self.cName = []

    def run(self, msg:str = "") -> list:
        while True:            
            
            print(Colors.RED+msg+Colors.END)

            print(Colors.CYAN+"현재 KEY :", end='')
            print(self.cName, end='')
            print(Colors.END)
            flag:str = input(Colors.RED+"Add key(1) / End(2)>>"+Colors.END)
            match(flag):
                case '1':
                    cName = self.selectColumn(Colors.RED+"Select Join Column (df1)"+Colors.END, self.df)
                    if cName in self.cName: print("이미 입력한 KEY입니다.")
                    else: self.cName.append(cName)
                case '2':
                    if len(self.cName) == 0: print("아무 KEY도 입력되지 않았습니다.")
                    else: 
                        print("Key 입력을 종료합니다. 현재 KEY : ", end=''); print(self.cName)
                        return self.cName
                case _:
                    print("잘못 입력하였습니다.")
            