import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import charts.ChartLabels as lbl

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg


df_prices = pg.get_prices_with_features(av._TIC_MICROSOFT, av._INT_DAILY)
name = pg.get_symbol_name(av._TIC_MICROSOFT)
opt_symbols = lbl.get_symbol_options()


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Table(
            html.Tr(children=[
                html.Td(children=[
                    html.H4(children=name),
                ]),
                html.Td(children=[
                    html.Label(lbl._LBL_TICKER),
                    dcc.Dropdown(
                        id='dd_ticker',
                        options=opt_symbols,
                        value=opt_symbols[0][lbl._OPT_VALUE]
                    )
                ]),
                html.Td(children=[

                ]),
                html.Td(children=[
                    html.Label(lbl._LBL_INTERVAL),
                ]),
                html.Td(children=[
                    dcc.Dropdown(
                        options=lbl.get_interval_options(),
                        value=av._INT_DAILY
                    )
                ]),
                html.Td(children=[
                    html.Label(lbl._LBL_MODEL),
                ]),
                html.Td(children=[
                    dcc.Dropdown(
                        options=lbl.get_model_options(),
                        value=lbl._OPT_BASELINE
                    )
                ]),
                html.Div(id='tdModel')
            ])
        )
    ]),

    generate_table(df_prices)
])

@app.callback(
    dash.dependencies.Output('tdModel', 'children'),
    [dash.dependencies.Input('dd_ticker', 'value')])
def update_table(value):
    print(value)
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)