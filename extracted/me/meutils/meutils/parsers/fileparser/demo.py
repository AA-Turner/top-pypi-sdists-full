#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/6/5 09:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd

from meutils.pipe import *
import pandas as pd


import  pdfplumber
with pdfplumber.open('银行间市场债券交易结算情况（按投资者）.pdf') as pdf:
    for page in pdf.pages:
        data = page.extract_table()


        cols = pd.MultiIndex.from_tuples(zip(*data[:2]))
        print(cols)
        df = pd.DataFrame(data[2:], columns=cols)

        print(df.fillna(method='ffill', axis=1))


#
# import camelot
# import pandas as pd
# # 使用Camelot读取PDF文件中的表格
# tables = camelot.read_pdf('银行间市场债券交易结算情况（按投资者）.pdf', pages='all', flavor='lattice')
#
# # # 将所有表格转换为 DataFrame 并合并
# # all_data = pd.concat([table.df for table in tables], ignore_index=True)
# #
# # all_data.to_excel('all_data.xlsx',index=False)
#
#
# print(tables[0].df)