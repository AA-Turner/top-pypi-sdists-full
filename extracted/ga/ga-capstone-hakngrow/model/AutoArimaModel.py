from pmdarima.arima import auto_arima

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg
import utils.ModelUtils as mdl

df_prices = pg.get_prices_with_features(av._TIC_MICROSOFT, av._INT_DAILY)
name = pg.get_symbol_name(av._TIC_MICROSOFT)

df_prices.drop(columns=['datetime', 'open', 'high', 'low', 'volume'], inplace=True)

df_train, df_test = mdl.train_test_split(df_prices, 1000)

print(df_train.shape)
print(df_test.shape)

training = df_train['close']
validation = df_test['close']

model = auto_arima(training, start_p=1, start_q=1,max_p=3, max_q=3, m=12,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
model.fit(training)

forecast = model.predict(n_periods=1000)

forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])

forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])