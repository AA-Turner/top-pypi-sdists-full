import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

class finalresulttransformer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        print('hello')
        
    def fit(self, X, y = None):
        print("fit!")
        return self

    def transform(self, X, y = None):
        df = X
        anomalies = df[df['score'] > df['cutoff']]
        print(anomalies)
        return anomalies.values