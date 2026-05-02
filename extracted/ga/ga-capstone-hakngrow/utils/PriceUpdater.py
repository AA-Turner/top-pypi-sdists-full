import Config as cfg

import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg


def update_price(ticker, interval, size):

    count_duplicate = 0
    count_create = 0

    df_prices = av.get_prices(cfg.AV_APIKEY, ticker, interval, size)

    for i in range(0, len(df_prices)):

        if not pg.is_price_duplicate(ticker, interval, df_prices[pg._COL_DATETIME][i]):

            print(f'{ticker} ({interval}) price on {str(df_prices[pg._COL_DATETIME][i])} created : {df_prices.iloc[i, :].values}')
            pg.create_prices([df_prices.iloc[i, :].values])
            count_create += 1

        else:

            print(f'Duplicate {ticker} ({interval}) price on {str(df_prices[pg._COL_DATETIME][i])}')
            count_duplicate += 1

    return count_create, count_duplicate


# update_price(av._TIC_MICROSOFT, av._INT_DAILY, av._SIZE_COMPACT)
