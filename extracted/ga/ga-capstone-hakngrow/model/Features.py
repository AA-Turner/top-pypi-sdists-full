class Features:

    def __init__(self, id, price_id, year, month, day, wkOfYr, dayOfYr, dayOfWk,
                 startOfYr, endOfYr, startOfQtr, endOfQtr, startOfMth, endOfMth, startOfWk, endOfWk):

        self.id = id
        self.price_id = price_id

        self.year = year
        self.month = month
        self.day = day

        self.week_of_yr = wkOfYr
        self.day_of_yr = dayOfYr
        self.day_of_wk = dayOfWk

        self.start_of_yr = startOfYr
        self.end_of_yr = endOfYr
        self.start_of_qtr = startOfQtr
        self.end_of_qtr = endOfQtr
        self.start_of_mth = startOfMth
        self.end_of_mth = endOfMth
        self.start_of_wk = startOfWk
        self.end_of_wk = endOfWk
