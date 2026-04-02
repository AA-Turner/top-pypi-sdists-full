from __future__ import annotations

from typing import Dict, Iterable, List

import pandas as pd
from pandas import DataFrame

from seshat.data_class import SFrame
from seshat.data_class.base import GroupSFrame
from seshat.general import configs


class DFrame(SFrame):
    frame_name = "df"
    data: DataFrame

    @property
    def empty(self, default_key=configs.DEFAULT_SF_KEY):
        return self.data.empty

    def make_group(self, default_key=configs.DEFAULT_SF_KEY):
        return GroupSFrame({default_key: self}, sframe_class=self.__class__)

    def get_columns(self, *args) -> Iterable[str]:
        return self.data.columns.tolist()

    def to_dict(self, *cols: str, key=configs.DEFAULT_SF_KEY) -> List[Dict]:
        selected = self.data[list(cols)] if cols else self.data
        selected = selected.loc[selected.astype(str).drop_duplicates().index]
        return selected.to_dict("records")

    def iterrows(self, column_name: str, key: str = configs.DEFAULT_SF_KEY):
        for row in self.data[column_name]:
            yield row

    def to_spf(self) -> SFrame:
        from seshat.data_class import SPFrame

        spark = SPFrame.get_spark()
        return SPFrame.from_raw(spark.createDataFrame(self.data))

    def extend_vertically(self, other: DataFrame):
        super().extend_vertically(other)
        self.data = pd.concat([self.data, other], axis=0).reset_index(drop=True)

    def extend_horizontally(
        self, other: DataFrame, on: str, left_on: str, right_on: str, how: str
    ):
        super().extend_horizontally(other, on, left_on, right_on, how)
        self.data = pd.merge(
            self.data,
            other,
            on=on,
            left_on=left_on,
            right_on=right_on,
            how=how,
        )

    @classmethod
    def read_csv(cls, path, *args, **kwargs) -> "DataFrame":
        kwargs.setdefault("on_bad_lines", "skip")
        return pd.read_csv(path, *args, **kwargs)

    @classmethod
    def from_raw(cls, data, *args, **kwargs) -> "DFrame":
        if not isinstance(data, DataFrame):
            data = DataFrame(data)
        return cls(data)
