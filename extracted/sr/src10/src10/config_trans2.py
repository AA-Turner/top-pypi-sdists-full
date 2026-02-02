import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class stddevtransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        print('stddevtransformer')
        
    def fit(self, X, y = None):
        print("fit stddevtransformer!")
        return self


    def transform(self, X, y = None):
        print("transform stddevtransformer")
        df = X
        tbl1=df.drop(['year','month','day','hour'],axis=1)
        tbl2=tbl1.std(axis=1)
        df1=pd.DataFrame(tbl2)
        print(tbl2)
        return df1.values