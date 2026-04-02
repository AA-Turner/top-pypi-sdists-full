from pandas import DataFrame

from seshat.transformer.splitter import Splitter


class TimeLineSplitter(Splitter):
    def split_df(self, default: DataFrame, *args, **kwargs):
        pass
