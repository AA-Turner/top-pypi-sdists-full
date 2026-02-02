import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class cutoffscorestransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        print('cutoffscorestransformer')
        
    def fit(self, X, y = None):
        print("fit cutoffscorestransformer")
        df = X
        score_mean = df["score"].mean()
        score_std = df["score"].std()
        score_cutoff = score_mean + 3*score_std
        df['cutoff'] = score_cutoff
        print(df)
        self.scores_df = df
        return self


    def transform(self, X, y = None):
        print("Transform cutoffscorestransformer")
        print(self.scores_df.values)
        return self.scores_df.values


 
