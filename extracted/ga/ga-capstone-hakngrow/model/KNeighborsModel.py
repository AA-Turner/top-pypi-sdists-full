import numpy as np

from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

import dash
import dash_core_components as dcc
import dash_html_components as html

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg
import utils.ModelUtils as mdl

df_prices = pg.get_prices_with_features(av._TIC_MICROSOFT, av._INT_DAILY)
name = pg.get_symbol_name(av._TIC_MICROSOFT)

df_prices.drop(columns=['open', 'high', 'low', 'volume'], inplace=True)

df_train, df_test = mdl.train_test_split(df_prices, 1000)

print(df_train.shape)
print(df_test.shape)

train_X = df_train.drop(columns=[pg._COL_CLOSE, pg._COL_DATETIME], axis=1)
train_y = df_train[pg._COL_CLOSE]

test_X = df_test.drop(columns=[pg._COL_CLOSE, pg._COL_DATETIME], axis=1)
test_Y = df_test[pg._COL_CLOSE]

scaler = MinMaxScaler(feature_range=(0, 1))

train_X_scaled = scaler.fit_transform(train_X)
test_X_scaled = scaler.fit_transform(test_X)

#using gridsearch to find the best parameter
params = {'n_neighbors':[2,3,4,5,6,7,8,9]}
knn = neighbors.KNeighborsRegressor()
model = GridSearchCV(knn, params, cv=5)

#fit the model and make predictions
model.fit(train_X_scaled, train_y)
predictions = model.predict(test_X_scaled)

#rmse
rmse = np.sqrt(np.mean(np.power((np.array(test_Y)-np.array(predictions)),2)))
print(rmse)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H1(children='KNeighborsModel'),

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
