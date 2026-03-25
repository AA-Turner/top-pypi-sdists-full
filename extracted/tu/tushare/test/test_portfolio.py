import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


import tushare as ts

# 初始化pro接口实例
pro = ts.pro_api()


# 选取股票列表
df = pro.stock_basic()
df_stock = df.head(10)
print(df_stock)

# 保存到自定义组合
df_p1 = pro.p_save(name="我的股票池", desc="默认选取股票10只股票", items=df_stock.to_dict(orient='records'))
print(df_p1)


# 查看自定义组合
df = pro.p_list()
print(df)

# 查看组合成份
df = pro.p_get(name="我的股票池", fields="ts_code,create_time,update_time")
print(df)

# 删除组合
df = pro.p_delete(name="我的股票池")
print(df)
