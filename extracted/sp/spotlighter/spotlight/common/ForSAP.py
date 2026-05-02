#############################
# ForSAP : SAP 추출 data를 위해 별도로 생성한 Class 
# 별도 Class로 분리
#############################
import pandas as pd

class ForSAP:
          
    @classmethod
    def InvertMinus(cls, tgt:str) -> str:
        if len(tgt) <= 1 : return tgt #1글자거나(-) 1글자보다 적으면('') 그냥 바로 반환
        if tgt[-1] == '-':
            tgt = tgt.replace('-','')
            tgt = "-" + tgt
            return tgt
        return tgt

    @classmethod
    def ColumnStrToInt(cls, df:pd.DataFrame, ColumnName:str) -> None:    
    #숫자 뒤에 -를 붙여서 음수가 추출된 경우 앞으로 붙여주는 함수
        try:
            #df[ColumnName] = df[ColumnName].fillna(0).apply(str.strip).apply(lambda x : x.replace(',','') ).apply(lambda x:x.replace('','0')).astype('float64').astype('int64')
            #df[ColumnName] = pd.to_numeric(df[ColumnName].fillna(0).astype('str').apply(str.strip).apply(lambda x : x.replace(',','')).apply(InvertMinus).replace( '[,)]','', regex=True).replace('[(]','-',regex=True))
            tmp = df[ColumnName].fillna(0) #일단 공백을 죽이고
            tmp = tmp.astype('str') #문자로 만든 다음
            tmp = tmp.apply(str.strip) #trim처리하고
            tmp = tmp.apply(lambda x: x.replace(',','')) #쉼표는 없앤다.
            tmp = tmp.replace('^-$', '0', regex=True) #그냥 오직 -는 0으로 바꿔준다.
            # 이후 로직은 위 아래 중 택일해서 돌려아함
            #tmp = tmp.apply(InvertMinus) 
            Flag = input("음수표시가 ()면 1, 마지막글자-면 2, 이외엔 그냥 엔터>>")
            match Flag:
                case '1':
                    tmp = tmp.replace( '[,)]','', regex=True).replace('[(]','-',regex=True) #()를 마이너스로 바꿔주는 함수        
                case '2':
                    tmp = tmp.apply(cls.InvertMinus)
                case _:
                    print("선택하지 않았습니다.")                

            tmp = pd.to_numeric(tmp, errors='coerce') #에러는 0으로..
            df[ColumnName] = tmp

        except Exception as e:
            print(e)        

       ## 전표금액 가공부2. SAP은 100을 곱해줘야 한다.
    @classmethod
    def Multiple100(cls, df:pd.DataFrame, columnName:str):
        df[columnName] = df[columnName] * 100


########################################################################################################################################################################
