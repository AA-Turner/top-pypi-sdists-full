# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Project      : AI.  @by PyCharm
# # @File         : kuaidi
# # @Time         : 2024/4/24 16:58
# # @Author       : betterme
# # @WeChat       : meutils
# # @Software     : PyCharm
# # @Description  :
#

from meutils.pipe import *
from meutils.decorators.retry import retrying
from meutils.api.ali_apis import express_query


@retrying
def query(express_no):
    appcode = '0ccd86184de94ca19c37cbb215b1f372'
    return express_query(express_no, appcode=appcode).get('result')


path = './快递登记系统.xlsx'
sheet_name = '快递信息'
df = pd.read_excel(path, sheet_name=sheet_name)
express_numbers = df['单号'] + ':' + df['收件人电话'].astype(str).str.strip().str[-4:]
df_ = pd.DataFrame(express_numbers.tolist() | xThreadPoolExecutor(query))
# df = pd.concat([df, df_[["updateTime", "takeTime"]]], axis=1)
df = pd.concat([df, df_], axis=1)

with pd.ExcelWriter('单号信息.xlsm') as writer:
    df.to_excel(writer, sheet_name)
