# 에프알엘코리아
# tsv 2 df # Test 용. df2db로 대체
#
# 특이사항
# 각 파일 앞 뒤 문자열 삭제 (앞 : 제목, 뒤 : 합계)
# 파일 내 double-quotes 삭제 필요 (EMeditor 활용

#S가 차변 #H가 대변 #세차

# 1. 데이터프레임으로 읽기
del myfd

from mylib import myFileDialog as myfd
path = myfd.askopenfilename()

import pandas as pd
df= pd.read_csv(path,sep="\t", low_memory=False)

df= pd.read_excel(path)

df.shape

# 컬럼명 strip()

tmp = df.columns.to_list()
tmplist = []
for i in tmp:
    tmplist.append(i.strip())
df.columns = tmplist

# 숫자로 만들기 - 거래통화
df['Amount'] = df['Amount'].str.replace(",","")
df['Amount'] = pd.to_numeric(df['Amount'])

# 숫자로 만들기 - 표시통화
df['Loc.curr.amount'] = df['Loc.curr.amount'].str.replace(",","")
df['Loc.curr.amount'] = pd.to_numeric(df['Loc.curr.amount'])

tmp1 = df.groupby('D/C')['Loc.curr.amount'].sum()
tmp1
tmp2 = df.groupby('D/C')['Amount'].sum()
tmp2

df.groupby(['G/L','D/C'])['Loc.curr.amount'].sum()

tmp = df['Unnamed: 29'].drop_duplicates()


path
#컬럼설계
for column in df:
    print(column,"->", df[column].astype(str).str.len().max())

df = df.drop_duplicates()

#문제 없어 보임


###
#메모. 2월은 그냥 따로 파이썬으로 읽어서 넣으면 된다.

string = "		1004	7300012425		2023	SC	2022/10/01	2022/10/01	    02	2022/11/02	12:11:38	0000/00/00	0000/00/00	PI-USER			[점포07]교통비: 보안택 미제거 고객 자택방	KRW			001	S		            5,000	KRW	            5,000	KRW	[점포07]교통비: 보안택 미제거 고객 자택방문	 택시기사님과 커뮤니케이션 미스로 본인		1004	S001135	75030KR001	S001135			0001	PCS-CSS"

string2="		1004	7300012425		2023	SC	2022/10/01	2022/10/01	    02	2022/11/02	12:11:38	0000/00/00	0000/00/00	PI-USER			[점포07]교통비: 보안택 미제거 고객 자택방	KRW			002	H		            5,000	KRW	            5,000	KRW	[점포07]교통비: 보안택 미제거 고객 자택방문	 택시기사님과 커뮤니케이션 미스로 본인		1004		10020KR999	S001135			0001	PCS-CSS"
string.count("\t")

string2.count("\t")

string3="		1004	7300012426		2023	SC	2022/10/12	2022/10/12	    02	2022/11/02	12:11:38	0000/00/00	0000/00/00	PI-USER			[점포07]교통비: 고객 클레임 보안택 미제거	KRW			001	S		            5,400	KRW	            5,400	KRW	[점포07]교통비: 고객 클레임 보안택 미제거 건 (매장 ->자택)			1004	S001176	75030KR001	S001176			0036	PCS-CSS"

string3.count("\t")