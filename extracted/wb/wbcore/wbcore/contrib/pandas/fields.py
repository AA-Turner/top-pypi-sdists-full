from collections import defaultdict
from dataclasses import dataclass
from typing import List, Literal

import pandas as pd

from wbcore.serializers.fields.types import DisplayMode


@dataclass
class _BaseField:
    key: str
    label: str
    type: str = None
    decorators: List = None
    help_text: str = None

    def to_dict(self):
        base = {"key": self.key, "label": self.label, "type": self.type}
        if self.decorators:
            base["decorators"] = self.decorators

        for _attr in ["help_text", "extra"]:
            attr = getattr(self, _attr, None)
            if attr:
                base[_attr] = attr
        return base

    def to_representation(self, value: pd.Series) -> pd.Series:
        return value


@dataclass
class PKField(_BaseField):
    type: str = "primary_key"


@dataclass
class CharField(_BaseField):
    type: str = "text"

    def to_representation(self, value: pd.Series) -> pd.Series:
        return super().to_representation(value).astype("string", errors="ignore")


@dataclass
class DateField(_BaseField):
    type: str = "date"

    def to_representation(self, value: pd.Series) -> pd.Series:
        return pd.to_datetime(super().to_representation(value)).dt.strftime("%Y-%m-%d")


@dataclass
class DateRangeField(_BaseField):
    type: str = "daterange"


@dataclass
class BooleanField(_BaseField):
    type: str = "boolean"


@dataclass
class TextField(_BaseField):
    type: str = "texteditor"

    def to_representation(self, value: pd.Series) -> pd.Series:
        return super().to_representation(value).astype("string", errors="ignore")


@dataclass
class EmojiRatingField(_BaseField):
    type: str = "emojirating"


@dataclass
class FloatField(_BaseField):
    type: str = "number"
    precision: int = 2
    percent: bool = False
    display_mode: DisplayMode = None
    disable_formatting: bool = False

    def to_dict(self):
        base = super().to_dict()
        base.update(
            {
                "precision": self.precision,
            }
        )
        if self.percent:
            base["type"] = "percent"
        if self.display_mode:
            base["display_mode"] = self.display_mode.value
        base["disable_formatting"] = self.disable_formatting
        return base

    def to_representation(self, value: pd.Series) -> pd.Series:
        return super().to_representation(value).astype("float", errors="ignore")


@dataclass
class IntegerField(FloatField):
    type: str = "number"
    precision: int = 0

    def to_representation(self, value: pd.Series) -> pd.Series:
        return super().to_representation(value).astype("Int64", errors="ignore")


@dataclass
class YearField(IntegerField):
    precision: int = 0
    disable_formatting: bool = True

    def __post_init__(self):
        self.precision = 0


@dataclass
class ListField(_BaseField):
    type: str = "list"


@dataclass
class JsonField(_BaseField):
    type: str = "json"


@dataclass
class SparklineField(ListField):
    type: str = "sparkline"
    dimension: Literal["single"] | Literal["double"] = (
        "single"  # "single" for data [y1, y2, y3... ] or "double" if contain already the X axis as [[x1, y1], [x2, y2], ... ]
    )

    def to_dict(self):
        rv = super().to_dict()
        rv["sparkline_type"] = "bar"
        return rv

    def _sanitize_row(self, row):
        if not row:
            row = [[]]  # if row is [] or null, we default to an empty list of list
        if self.dimension == "single":  # This ensure that the returned data format contains a list of tuple of x,y
            row = list(map(lambda o: (o[0], o[1]), enumerate(row)))
        return row

    def to_representation(self, value: pd.Series) -> pd.Series:
        return super().to_representation(value).apply(lambda x: self._sanitize_row(x))


@dataclass(unsafe_hash=True)
class PandasFields:
    fields: List[_BaseField]

    def to_dict(self):
        fields = defaultdict(dict)

        for field in self.fields:
            fields[field.key] = field.to_dict()

        return fields
