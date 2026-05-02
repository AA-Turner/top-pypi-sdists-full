import utils.PostgresUtils as pg

import model.FeatureEngineer as fe


def update_date_features(ticker, interval, start_date, end_date):

    price_dates = pg.get_price_dates(ticker, interval, start_date, end_date)

    if start_date is None and end_date is None:
        print(f'{len(price_dates)} {ticker} ({interval}) prices found.')
    elif start_date is not None and end_date is None:
        print(f'{len(price_dates)} {ticker} ({interval}) prices on {start_date} found.')
    elif start_date is not None and end_date is not None:
        print(f'{len(price_dates)} {ticker} ({interval}) prices between [{start_date}, {end_date}] found.')

    features_array = []
    count_duplicate = 0
    count_create = 0

    for i in range(0, len(price_dates)):

        if pg.get_features_by_price_id(price_dates[i][0]) is None:

            features = fe.get_date_features(price_dates[i][1])

            print(f'{ticker} ({interval}) features on {price_dates[i][1]} created: {features}')

            features_array.append([price_dates[i][0], \
                                   features[0], features[1], features[2], \
                                   features[3], features[4], features[5], \
                                   int(features[6][0]), int(features[6][1]), int(features[7][0]), int(features[7][1]), \
                                   int(features[8][0]), int(features[8][1]), int(features[9][0]), int(features[9][0])])
            count_create += 1

        else:

            print(f'Duplicate {ticker} ({interval}) features on {price_dates[i][1]}')
            count_duplicate += 1

    pg.create_features(features_array)

    return count_create, count_duplicate


#update_date_features(av._TIC_MICROSOFT, av._INT_DAILY)
