import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class cleandatatransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        print('init cleandatatransformer')
        
    def fit(self, X, y = None):
        print("fit cleandatatransformer!")
        self.origTable_ = X
        return self


    def transform(self, X, y = None):
        if(len(X.columns) == 7):
            print("transform cleandatatransformer 7")
            df = X
            tbl1 = pd.pivot_table(df,index=['year','month','day','hour'],values='power',columns ='loggername',aggfunc=sum)
            tbl2=tbl1.fillna(0)
            tbl2[tbl2 < 0] = 0
            tbl2.reset_index(inplace=True)
            self.origTable_ = tbl2
            print(tbl2)
            return tbl2.values
        elif (len(X.columns) == 2):
            print("transform cleandatatransformer 2")
            anomalies_df = X
            result = pd.concat([self.origTable_, anomalies_df], axis=1)
            print(result)
            return result.values
