import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg
import utils.ModelUtils as mdl

name = pg.get_symbol_name(av._TIC_MICROSOFT)
df_prices = pg.get_prices(av._TIC_MICROSOFT, av._INT_DAILY)

df_train, df_test = mdl.train_test_split(df_prices, 1000)

print(len(df_prices), len(df_train), len(df_test))
print(min(df_train[pg._COL_DATETIME]), max(df_train[pg._COL_DATETIME]))
print(min(df_test[pg._COL_DATETIME]), max(df_test[pg._COL_DATETIME]))

predictions = []


def baseline(train, test):

    print('\n Shape of training set:')
    print(train.shape)
    print('\n Shape of testing set:')
    print(test.shape)

    test_size = len(test)

    global predictions

    for i in range(0, test_size):

        price = (train[pg._COL_CLOSE][-1 * test_size + i:].sum() + sum(predictions)) / test_size

        predictions.append(price)

    # checking the results (RMSE value)
    rmse = np.sqrt(np.mean(np.power((np.array(test[pg._COL_CLOSE]) - predictions), 2)))
    print('\n RMSE value on validation set:')
    print(rmse)

baseline(df_train, df_test)



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