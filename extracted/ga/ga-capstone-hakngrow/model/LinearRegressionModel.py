import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

from sklearn.linear_model import LinearRegression

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg
import utils.ModelUtils as mdl

name = pg.get_symbol_name(av._TIC_MICROSOFT)
df_prices = pg.get_prices_with_features(av._TIC_MICROSOFT, av._INT_DAILY)

df_prices.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

print(df_prices.info())

df_train, df_test = mdl.train_test_split(df_prices, 1000)

predictions= []

train = df_train.drop(pg._COL_DATETIME, axis=1)
test = df_test.drop(pg._COL_DATETIME, axis=1)

print(train.shape)
print(test.shape)


train_X = train.drop(pg._COL_CLOSE, axis=1)
train_y = train[pg._COL_CLOSE]

print(train_X.iloc[0:1,:])

test_X = test.drop(pg._COL_CLOSE, axis=1)
test_y = test[pg._COL_CLOSE]



model = LinearRegression()
model.fit(train_X, train_y)

predictions = model.predict(test_X)

rmse = np.sqrt(np.mean(np.power((np.array(test_y) - np.array(predictions)), 2)))

print(rmse)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='Baseline Model'),

    html.Div(children=name),

    dcc.Graph(
        id='graph_model',
        figure={

            'data': [
                {'x': df_train[pg._COL_DATETIME], 'y': df_train[pg._COL_CLOSE], 'type': 'scatter', 'name': 'train'},
                {'x': df_test[pg._COL_DATETIME], 'y': df_test[pg._COL_CLOSE], 'type': 'scatter', 'name': 'test'},
                {'x': df_test[pg._COL_DATETIME], 'y': predictions, 'type': 'scatter', 'name': 'pred'},
            ],

            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)





