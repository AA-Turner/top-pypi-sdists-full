import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, Input

import random

import plotly
import plotly.graph_objs as go

from collections import deque

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg

df_prices = pg.get_prices(av._TIC_MICROSOFT, av._INT_DAILY)

cols = [pg._COL_OPEN, pg._COL_HIGH, pg._COL_LOW, pg._COL_CLOSE]

arr_ohlc = df_prices.iloc[0:20, ][cols].values
arr_date = df_prices.iloc[0:20, ][pg._COL_DATETIME].values

X = deque(arr_ohlc, maxlen=20)
Y = deque(arr_date, maxlen=20)

next_price_idx = 20
max_price_idx = len(df_prices)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        ),
    ]
)

def get_next_price():

    global next_price_idx
    global max_price_idx
    global df_prices

    price = df_prices.iloc[next_price_idx, :].values

    print(price)

    if next_price_idx < max_price_idx:
        next_price_idx += 1


@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_scatter(intervals):

    print(get_next_price())

    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode='lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server(debug=True)