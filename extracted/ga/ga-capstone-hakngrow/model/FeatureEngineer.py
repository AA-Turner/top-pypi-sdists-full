import calendar
import datetime

import utils.PostgresUtils as pg


def is_month_start_end(date):

    last_day_of_mth = calendar.monthrange(date.year, date.month)[1]

    return date.day == 1, date.day == last_day_of_mth


def is_quarter_start_end(date):

    start_qtr_mths = [1, 4, 7, 10]
    end_qtr_mths = [3, 6, 9, 13]

    # Check for start of quarter
    qtr_start = (date.month in start_qtr_mths) and (date.day == 1)

    # Check for end of quarter
    qtr_end = (date.month in end_qtr_mths) and (date.day == calendar.monthrange(date.year, date.month)[1])

    return qtr_start, qtr_end


def is_year_start_end(date):

    yr_start = (date.day == 1) and (date.month == 1)

    yr_end = (date.day == 31) and (date.month == 12)

    return yr_start, yr_end


def get_date_features(date):

    year = date.year
    month = date.month
    day = date.day

    (year, wkOfYr, dayOfWk) = datetime.date(year, month, day).isocalendar()

    dayOfYr = datetime.date(year, month, day).timetuple().tm_yday

    is_monday = (dayOfWk == 1)
    is_friday = (dayOfWk == 5)

    return year, month, day, wkOfYr, dayOfYr, dayOfWk, is_year_start_end(date), is_quarter_start_end(date), \
           is_month_start_end(date), (is_monday, is_friday)


def add_date_features(df_prices):

    df_prices[pg._COL_YEAR] = 0
    df_prices[pg._COL_MONTH] = 0
    df_prices[pg._COL_DAY] = 0

    df_prices[pg._COL_WK_OF_YR] = 0
    df_prices[pg._COL_DAY_OF_YR] = 0
    df_prices[pg._COL_DAY_OF_WK] = 0

    df_prices[pg._COL_START_OF_YR] = 0
    df_prices[pg._COL_END_OF_YR] = 0
    df_prices[pg._COL_START_OF_QTR] = 0
    df_prices[pg._COL_END_OF_QTR] = 0
    df_prices[pg._COL_START_OF_MTH] = 0
    df_prices[pg._COL_END_OF_MTH] = 0
    df_prices[pg._COL_START_OF_WK] = 0
    df_prices[pg._COL_END_OF_WK] = 0

    for i in range(0, len(df_prices)):

        features = get_date_features(df_prices[pg._COL_DATETIME][i])

        df_prices[pg._COL_YEAR][i] = features[0]
        df_prices[pg._COL_MONTH][i] = features[1]
        df_prices[pg._COL_DAY][i] = features[2]

        df_prices[pg._COL_WK_OF_YR] = features[3]
        df_prices[pg._COL_DAY_OF_YR] = features[4]
        df_prices[pg._COL_DAY_OF_WK] = features[5]

        df_prices[pg._COL_START_OF_YR] = features[6][0]
        df_prices[pg._COL_END_OF_YR] = features[6][1]
        df_prices[pg._COL_START_OF_QTR] = features[7][0]
        df_prices[pg._COL_END_OF_QTR] = features[7][1]
        df_prices[pg._COL_START_OF_MTH] = features[8][0]
        df_prices[pg._COL_END_OF_MTH] = features[8][1]
        df_prices[pg._COL_START_OF_WK] = features[9][0]
        df_prices[pg._COL_END_OF_WK] = features[9][1]

    return df_prices


def set_date_features(row):

    features = get_date_features(row[pg._COL_DATETIME])

    row[pg._COL_YEAR] = features[0]
    row[pg._COL_MONTH] = features[1]
    row[pg._COL_DAY] = features[2]

    row[pg._COL_WEEK_OF_YR] = features[3]
    row[pg._COL_DAY_OF_YR] = features[4]
    row[pg._COL_DAY_OF_WK] = features[5]

    row[pg._COL_START_OF_YR] = features[6][0]
    row[pg._COL_END_OF_YR] = features[6][1]
    row[pg._COL_START_OF_QTR] = features[7][0]
    row[pg._COL_END_OF_QTR] = features[7][1]
    row[pg._COL_START_OF_MTH] = features[8][0]
    row[pg._COL_END_OF_MTH] = features[8][1]
    row[pg._COL_START_OF_WK] = features[9][0]
    row[pg._COL_END_OF_WK] = features[9][1]


def get_date_features_array(df_prices):

    features_array = []

    for i in range(0, len(df_prices)):

        features_array.append([
            df_prices[pg._COL_ID], df_prices[pg._COL_YEAR], df_prices[pg._COL_YEAR], df_prices[pg._COL_YEAR], \
            df_prices[pg._COL_WK_OF_YR], df_prices[pg._COL_DAY_OF_YR], df_prices[pg._COL_DAY_OF_WK],
            df_prices[pg._COL_START_OF_YR], df_prices[pg._COL_END_OF_YR],
            df_prices[pg._COL_START_OF_QTR], df_prices[pg._COL_END_OF_QTR],
            df_prices[pg._COL_START_OF_MTH], df_prices[pg._COL_END_OF_MTH],
            df_prices[pg._COL_START_OF_WK], df_prices[pg._COL_END_OF_WK]
        ])

    return features_array
