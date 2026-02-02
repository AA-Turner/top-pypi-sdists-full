#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 18:20:22 2022

@author: danycajas
"""

import numpy as np
import pandas as pd
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")
pd.options.display.float_format = '{:.4%}'.format


#%%

# Date range
start = '2016-01-01'
end = '2019-12-30'

# Tickers of assets
assets = ["JCI", "TGT", "CMCSA", "CPB", "MO", "AMZN", "APA", "MMC", "JPM", "ZION", "SPY"]

assets.sort()

# Downloading data
data = yf.download(assets, start = start, end = end)
data = data.loc[:,('Adj Close', slice(None))]
data.columns = assets
data.to_csv("stock_prices_2.csv")

data = pd.read_csv("stock_prices.csv", parse_dates=True, index_col=0)
Y = data[assets].pct_change().dropna().iloc[-200:]

w_2 = pd.read_csv("HC_NCO.csv", parse_dates=False, index_col=0)


#%%
import riskfolio as rp
import mosek

port = rp.HCPortfolio(returns=Y)

model = "NCO"
codependence = "pearson"
covariance = "hist"
obj = "MinRisk"
rf = 0
linkage = "ward"
max_k = 10
leaf_order = True

rms = [
    "MV",
    "MAD",
    "MSV",
    "FLPM",
    "SLPM",
    "CVaR",
    "EVaR",
    "WR",
    "MDD",
    "ADD",
    "CDaR",
    "EDaR",
    "UCI",
]

w_1 = pd.DataFrame([])

for i in rms:
    w = port.optimization(
        model=model,
        codependence=codependence,
        covariance=covariance,
        obj=obj,
        rm=i,
        rf=rf,
        linkage=linkage,
        max_k=max_k,
        leaf_order=leaf_order,
    )

    w_1 = pd.concat([w_1, w], axis=1)

w_1.columns = rms

a = np.testing.assert_array_almost_equal(w_1.to_numpy(), w_2.to_numpy(), decimal=6)
if a is None:
    print("There are no errors in test_hc_nco_optimization")


#%%
# import matplotlib.pyplot as plt
# rm = "GMD"

# for rm in rms:
#     # lala = rp.Risk_Contribution(w_1[rm].to_frame(),
#     #                             cov=Y.cov(),
#     #                             returns=Y,
#     #                             rm=rm,
#     #                             rf=0,
#     #                             alpha=0.05,
#     #                             a_sim=100,
#     #                             beta=None,
#     #                             b_sim=None)
#     # print(lala)
#     ax = rp.plot_risk_con(w_1[rm].to_frame(),
#                           cov=Y.cov(),
#                           returns=Y,
#                           rm=rm,
#                           rf=0,
#                           alpha=0.05,
#                           color="tab:red",
#                           height=6,
#                           width=10,
#                           ax=None)
#     plt.show()


import riskfolio as rp

rm = "MAD"

ax = rp.plot_risk_con(w_1[rm].to_frame(),
                      cov=Y.cov(),
                      returns=Y,
                      rm=rm,
                      rf=0,
                      alpha=0.05,
                      percentage=True,
                      color="tab:red",
                      height=6,
                      width=10,
                      ax=None)

#%%

from scipy.stats import skew, kurtosis

s = skew(Y["JCI"])
k = kurtosis(Y["JCI"], fisher=False)

print(s, k)


#%%

import numpy as np

T = 1000
n = 10
X = np.random.randn(T,n)

def coskewness(X):
    T, n = X.shape
    mu = np.mean(X, axis=0).reshape(n, 1)
    x = X - np.repeat(mu.T, T, axis=0)
    ones = np.ones((1,n))
    W1 = np.kron(ones, x)
    W2 = np.kron(x, ones)
    M3 = (1/T) * x.T @ (W1 * W2)
    return M3

def cokurtosis(X):
    T, n = X.shape
    M4 = np.empty((n, 0))
    mu = np.mean(X, axis=0).reshape(n, 1)
    x = X - np.repeat(mu.T, T, axis=0)
    ones = np.ones((1,n))
    W1 = np.kron(x, np.kron(ones, ones))
    W2 = np.kron(ones, np.kron(x, ones))
    W3 = np.kron(ones, np.kron(ones, x))
    M4 = (1/T) * x.T @ (W1 * W2 * W3)
    return M4

def square_cokurtosis(X):
    T, n = X.shape
    mu = np.mean(X, axis=0).reshape(n, 1)
    x = X - np.repeat(mu.T, T, axis=0)
    ones = np.ones((1,n))
    W1 = np.kron(x, ones)
    W2 = np.kron(x, ones)
    Z = (W1 * W2)
    S4 = (1/T) * Z.T @ Z
    return S4

def square_semicokurtosis(X):
    T, n = X.shape
    mu = np.mean(X, axis=0).reshape(n, 1)
    x = X - np.repeat(mu.T, T, axis=0)
    x = np.minimum(x, 0)
    ones = np.ones((1,n))
    W1 = np.kron(x, ones)
    W2 = np.kron(x, ones)
    Z = (W1 * W2)
    SS4 = (1/T) * Z.T @ Z
    return SS4











