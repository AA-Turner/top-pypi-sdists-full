import dash
import dash_core_components as dcc
import dash_html_components as html

from fbprophet import Prophet

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg
import utils.ModelUtils as mdl

df_prices = pg.get_prices_with_features(av._TIC_MICROSOFT, av._INT_DAILY)
name = pg.get_symbol_name(av._TIC_MICROSOFT)

df_prices.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

df_train, df_test = mdl.train_test_split(df_prices, 1000)

