import pandas as pd

import psycopg2

from psycopg2 import DatabaseError

import utils.Config as cfg

_TBL_PRICES = 'prices'
_COL_ID = 'id'
_COL_ID = 'id'
_COL_TICKER = 'ticker'
_COL_INTERVAL = 'interval'
_COL_DATETIME = 'datetime'
_COL_OPEN = 'open'
_COL_HIGH = 'high'
_COL_LOW = 'low'
_COL_CLOSE = 'close'
_COL_VOLUME = 'volume'

_TBL_FEATURES = 'features'
_COL_PRICE_ID = 'price_id'
_COL_YEAR = 'year'
_COL_MONTH = 'month'
_COL_DAY = 'day'
_COL_WK_OF_YR = 'wk_of_yr'
_COL_DAY_OF_YR = 'day_of_yr'
_COL_DAY_OF_WK = 'day_of_wk'
_COL_START_OF_YR = 'start_of_yr'
_COL_END_OF_YR = 'end_of_yr'
_COL_START_OF_QTR = 'start_of_qtr'
_COL_END_OF_QTR = 'end_of_qtr'
_COL_START_OF_MTH = 'start_of_mth'
_COL_END_OF_MTH = 'end_of_mth'
_COL_START_OF_WK = 'start_of_wk'
_COL_END_OF_WK = 'end_of_wk'

_TBL_SYMBOLS = 'symbols'
_COL_NAME = 'name'

_CONN = None


def connect():

    global _CONN

    try:
        params = cfg.get_database_items()

        print('Connecting to the PostgreSQL database...')
        _CONN = psycopg2.connect(**params)

        cursor = _CONN.cursor()

        cursor.execute('SELECT version()')

        db_version = cursor.fetchone()
        print(db_version)

        cursor.close()

        return

    except (Exception, DatabaseError) as error:

        print(error)


def disconnect():

    try:
        if _CONN is not None:

            _CONN.close()
            print('Database connection closed!')

    except (Exception, DatabaseError) as error:

        print(error)


def get_cursor():

    return _CONN.cursor()


def get_symbol_name(ticker):

    sql = 'SELECT ' + _COL_NAME + ' FROM ' + _TBL_SYMBOLS + ' WHERE ' + _COL_TICKER + '=\'' + ticker + '\''

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        name = cursor.fetchone()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return name


def get_symbols():

    sql = 'SELECT ' + _COL_NAME + ', ' + _COL_TICKER + ' FROM ' + _TBL_SYMBOLS + ' ORDER BY ' + _COL_NAME

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        symbols = cursor.fetchall()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return symbols


def create_symbol(ticker, name):

    sql = 'INSERT INTO ' + _TBL_SYMBOLS + '(' + _COL_TICKER + \
                                         ', ' + _COL_NAME + ') VALUES(%s, %s)'
    try:
        cursor = get_cursor()

        cursor.executemany(sql, [[ticker, name]])

        _CONN.commit()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)


def get_features_by_price_id(price_id):

    sql = 'SELECT * FROM ' + _TBL_FEATURES + \
                 ' WHERE ' + _COL_PRICE_ID + '=' + str(price_id)

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        features = cursor.fetchone()

        cursor.close()

    except (Exception, DatabaseError) as error:
        print(error)

    return features


def get_features_by_datetime(ticker, interval, start_date, end_date):

    sql = 'SELECT ' + _TBL_PRICES + '.' + _COL_DATETIME + \
               ', ' + _TBL_FEATURES + '.' + _COL_YEAR + \
               ', ' + _TBL_FEATURES + '.' + _COL_MONTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY + \
               ', ' + _TBL_FEATURES + '.' + _COL_WK_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY_OF_WK + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_QTR + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_QTR + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_MTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_MTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_WK + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_WK + \
           ' FROM ' + _TBL_PRICES + \
     ' INNER JOIN ' + _TBL_FEATURES + \
             ' ON ' + _TBL_PRICES + '.' + _COL_ID + ' = ' + _TBL_FEATURES + '.' + _COL_PRICE_ID + \
          ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
          '\' AND ' + _COL_INTERVAL + '=\'' + interval + '\''

    if start_date is not None and end_date is not None:
        sql = sql + ' AND (' + _COL_DATETIME + '>=\'' + str(start_date) + \
                    '\' AND ' + _COL_DATETIME + '<=\'' + str(end_date) + '\')'
    elif start_date is not None:
        sql = sql + ' AND ' + _COL_DATETIME + '=\'' + str(start_date) + '\''

    sql = sql + ' ORDER BY ' + _COL_DATETIME + ' DESC'

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        df_features = pd.DataFrame(cursor.fetchall(), columns=[_COL_DATETIME,
                                                               _COL_YEAR, _COL_MONTH, _COL_DAY,
                                                               _COL_WK_OF_YR, _COL_DAY_OF_YR, _COL_DAY_OF_WK,
                                                               _COL_START_OF_YR, _COL_END_OF_YR,
                                                               _COL_START_OF_QTR, _COL_END_OF_QTR,
                                                               _COL_START_OF_MTH, _COL_END_OF_MTH,
                                                               _COL_START_OF_WK, _COL_END_OF_WK])
        cursor.close

        return df_features

    except (Exception, DatabaseError) as error:
        print(error)


def create_features(features):

    sql = 'INSERT INTO ' + _TBL_FEATURES + '(' + _COL_PRICE_ID + \
                                          ', ' + _COL_YEAR + \
                                          ', ' + _COL_MONTH + \
                                          ', ' + _COL_DAY + \
                                          ', ' + _COL_WK_OF_YR + \
                                          ', ' + _COL_DAY_OF_YR + \
                                          ', ' + _COL_DAY_OF_WK + \
                                          ', ' + _COL_START_OF_YR + \
                                          ', ' + _COL_END_OF_YR + \
                                          ', ' + _COL_START_OF_QTR + \
                                          ', ' + _COL_END_OF_QTR + \
                                          ', ' + _COL_START_OF_MTH + \
                                          ', ' + _COL_END_OF_MTH + \
                                          ', ' + _COL_START_OF_WK + \
                                          ', ' + _COL_END_OF_WK + \
                                          ') VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor = get_cursor()

        cursor.executemany(sql, features)

        _CONN.commit()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)


def create_prices(prices):

    sql = 'INSERT INTO ' + _TBL_PRICES + '(' + _COL_TICKER + \
                                         ', ' + _COL_INTERVAL + \
                                         ', ' + _COL_DATETIME + \
                                         ', ' + _COL_OPEN + \
                                         ', ' + _COL_HIGH + \
                                         ', ' + _COL_LOW + \
                                         ', ' + _COL_CLOSE + \
                                         ', ' + _COL_VOLUME + ') VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor = get_cursor()

        cursor.executemany(sql, prices)

        _CONN.commit()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)


def get_prices(ticker, interval, start_date, end_date, limit):

    sql = 'SELECT * FROM ' + _TBL_PRICES + \
                 ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
                 '\' AND ' + _COL_INTERVAL + '=\'' + interval + '\''

    if start_date is not None and end_date is not None:
        sql = sql + ' AND (' + _COL_DATETIME + '>=\'' + str(start_date) + \
                    '\' AND ' + _COL_DATETIME + '<=\'' + str(end_date) + '\')'
    elif start_date is not None:
        sql = sql + ' AND ' + _COL_DATETIME + '=\'' + str(start_date) + '\''

    sql = sql + ' ORDER BY ' + _COL_DATETIME + ' DESC'

    if limit is not None:
        sql = sql + ' LIMIT ' + limit

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        df_prices = pd.DataFrame(cursor.fetchall(), columns=[_COL_ID, _COL_TICKER, _COL_INTERVAL, _COL_DATETIME,
                                                             _COL_OPEN, _COL_HIGH, _COL_LOW, _COL_CLOSE, _COL_VOLUME])
        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return df_prices


def get_prices_with_features(ticker, interval, start_date, end_date, limit):

    sql = 'SELECT ' + _TBL_PRICES + '.' + _COL_DATETIME + \
               ', ' + _TBL_PRICES + '.' + _COL_OPEN + \
               ', ' + _TBL_PRICES + '.' + _COL_HIGH + \
               ', ' + _TBL_PRICES + '.' + _COL_LOW + \
               ', ' + _TBL_PRICES + '.' + _COL_CLOSE + \
               ', ' + _TBL_PRICES + '.' + _COL_VOLUME + \
               ', ' + _TBL_FEATURES + '.' + _COL_YEAR + \
               ', ' + _TBL_FEATURES + '.' + _COL_MONTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY + \
               ', ' + _TBL_FEATURES + '.' + _COL_WK_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_DAY_OF_WK + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_YR + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_QTR + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_QTR + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_MTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_MTH + \
               ', ' + _TBL_FEATURES + '.' + _COL_START_OF_WK + \
               ', ' + _TBL_FEATURES + '.' + _COL_END_OF_WK + \
          ' FROM ' + _TBL_PRICES + \
     ' INNER JOIN ' + _TBL_FEATURES + \
             ' ON ' + _TBL_PRICES + '.' + _COL_ID + ' = ' + _TBL_FEATURES + '.' + _COL_PRICE_ID + \
          ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
          '\' AND ' + _COL_INTERVAL + '=\'' + interval + '\''

    if start_date is not None and end_date is not None:
        sql = sql + ' AND (' + _COL_DATETIME + '>=\'' + str(start_date) + \
                    '\' AND ' + _COL_DATETIME + '<=\'' + str(end_date) + '\')'
    elif start_date is not None:
        sql = sql + ' AND ' + _COL_DATETIME + '=\'' + str(start_date) + '\''

    sql = sql + ' ORDER BY ' + _COL_DATETIME + ' DESC'

    if limit is not None:
        sql = sql + ' LIMIT ' + limit

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        df_prices = pd.DataFrame(cursor.fetchall(), columns=[_COL_DATETIME,
                                                             _COL_OPEN, _COL_HIGH, _COL_LOW, _COL_CLOSE,
                                                             _COL_VOLUME,
                                                             _COL_YEAR, _COL_MONTH, _COL_DAY,
                                                             _COL_WK_OF_YR, _COL_DAY_OF_YR, _COL_DAY_OF_WK,
                                                             _COL_START_OF_YR, _COL_END_OF_YR,
                                                             _COL_START_OF_QTR, _COL_END_OF_QTR,
                                                             _COL_START_OF_MTH, _COL_END_OF_MTH,
                                                             _COL_START_OF_WK, _COL_END_OF_WK])
        # df_prices.set_index(_COL_DATETIME, inplace=True)

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return df_prices


def get_price_dates(ticker, interval, start_date, end_date):

    sql = 'SELECT ' + _COL_ID + ', ' + _COL_DATETIME + \
                            ' FROM ' + _TBL_PRICES + \
                           ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
                           '\' AND ' + _COL_INTERVAL + '=\'' + interval + '\''

    if start_date is not None and end_date is not None:
        sql = sql + ' AND (' + _COL_DATETIME + '>=\'' + str(start_date) + \
                    '\' AND ' + _COL_DATETIME + '<=\'' + str(end_date) + '\')'
    elif start_date is not None:
        sql = sql + ' AND ' + _COL_DATETIME + '=\'' + str(start_date) + '\''

    sql = sql + ' ORDER BY ' + _COL_DATETIME + ' DESC'

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        dates = cursor.fetchall()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return dates


def get_price_ids(ticker, interval, start_date, end_date):

    sql = 'SELECT ' + _COL_ID + ' FROM ' + _TBL_PRICES + \
                               ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
                               '\' AND ' + _COL_INTERVAL + '=\'' + interval + '\''

    if start_date is not None and end_date is not None:
        sql = sql + ' AND (' + _COL_DATETIME + '>=\'' + str(start_date) + \
                    '\' AND ' + _COL_DATETIME + '<=\'' + str(end_date) + '\')'
    elif start_date is not None:
        sql = sql + ' AND ' + _COL_DATETIME + '=\'' + str(start_date) + '\''

    sql = sql + ' ORDER BY ' + _COL_DATETIME + ' DESC'

    try:
        cursor = get_cursor()

        cursor.execute(sql)

        ids = cursor.fetchall()

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return ids


def is_price_duplicate(ticker, interval, datetime):

    sql = 'SELECT ' + _COL_ID + \
           ' FROM ' + _TBL_PRICES + \
          ' WHERE ' + _COL_TICKER + '=\'' + ticker + \
          '\' AND ' + _COL_INTERVAL + '=\'' + interval + \
          '\' AND ' + _COL_DATETIME + '=\'' + str(datetime) + '\''
    try:
        cursor = get_cursor()

        cursor.execute(sql)

        is_duplicate = cursor.fetchone() is not None

        cursor.close

    except (Exception, DatabaseError) as error:
        print(error)

    return is_duplicate

connect()



