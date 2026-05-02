# 231002. 영국 요청에 따라 특정 전표번호 식별을 위해 임시테이블 추가
from mylib import txt2df2db as mytdd
from mylib import myFileDialog as myfd
path = myfd.askopenfilename()

import pandas as pd
df= pd.read_excel(path)

mytdd.df2db(df,'frl','tmp_ami') #myLib 활용

