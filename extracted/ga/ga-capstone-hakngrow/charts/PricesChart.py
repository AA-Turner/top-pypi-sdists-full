import pandas as pd

import plotly.graph_objects as go

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg

df_prices = pg.get_prices(av._TIC_MICROSOFT, av._INT_DAILY)

fig = go.Figure(data=[go.Candlestick(x=df_prices[pg._COL_DATETIME], \
                                     open=df_prices[pg._COL_OPEN], \
                                     high=df_prices[pg._COL_HIGH], \
                                     low=df_prices[pg._COL_LOW], \
                                     close=df_prices[pg._COL_CLOSE])])

fig.show()
