import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.options.display.notebook_repr_html=False  # 表格显示
plt.rcParams['figure.dpi'] = 72  # 图形分辨率
plt.rcParams['figure.figsize']=(12.8,7.2)
sns.set_theme(style='darkgrid',palette="Set1")  # 图形主题

data = {
    "No policy" : [8000,8000,8000,8000,8000],
    "Default policy 0.5n": [8000,6856,4570,4870,2143],
    "Default policy 0.8n": [8000,4092,5140,1278,992],
    "2/8 Default policy 0.5n": [8000,4800,5958,3152,2102],
    "2/8 Default policy 0.8n": [8000,4344,2360,2112,739],
    "Borrow hit rate 0.5n(%)": [100,100,100,100,97.74],
    "Borrow hit rate 0.8n(%)": [100,100,100,100,98.36],
    "2/8 Borrow hit rate 0.5n(%)": [100,100,100,100,98.33],
    "2/8 Borrow hit rate 0.8n(%)": [100,100,100,100,95.98],
}
data = pd.DataFrame(data, index=["-1","40","30","20","10"],columns=["Borrow hit rate 0.5n(%)","Borrow hit rate 0.8n(%)","2/8 Borrow hit rate 0.5n(%)","2/8 Borrow hit rate 0.8n(%)"])
sns.lineplot(data=data, ci=None)
plt.show()
