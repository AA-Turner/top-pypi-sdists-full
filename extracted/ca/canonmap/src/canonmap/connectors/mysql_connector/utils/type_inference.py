# src/canonmap/connectors/mysql_connector/utils/type_inference.py

from __future__ import annotations

from typing import Any, Optional, Tuple
from decimal import Decimal, InvalidOperation

import pandas as pd


def clean_numeric_string(value: Any) -> Optional[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    s = str(value).strip()
    if s == "":
        return None
    import re as _re
    s = _re.sub(r"[\s,$]", "", s)
    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    return s


def coerce_datetime_series(series: pd.Series) -> Tuple[pd.Series, bool]:
    dt = pd.to_datetime(series, errors="coerce", utc=False)
    ratio = dt.notna().mean()
    return dt, bool(ratio >= 0.9)


def coerce_boolean_series(series: pd.Series) -> Tuple[pd.Series, bool]:
    truthy = {"1", "true", "t", "yes", "y"}
    falsy = {"0", "false", "f", "no", "n"}

    def to_bool(x: Any) -> Optional[bool]:
        if x is None or pd.isna(x):
            return None
        s = str(x).strip().lower()
        if s in truthy:
            return True
        if s in falsy:
            return False
        return None

    converted = series.map(to_bool)
    ratio = converted.notna().mean()
    return converted, bool(ratio >= 0.9)


def coerce_numeric_series(series: pd.Series) -> Tuple[pd.Series, Optional[Tuple[int, int]], bool, bool]:
    cleaned = series.map(clean_numeric_string)

    def to_decimal(x: Optional[str]) -> Optional[Decimal]:
        if x in (None, ""):
            return None
        try:
            return Decimal(x)
        except (InvalidOperation, ValueError):
            return None

    decimals = cleaned.map(to_decimal)
    ok_ratio = decimals.notna().mean()
    if ok_ratio < 0.9:
        return series, None, False, False

    # Determine if integer
    int_like = decimals.dropna().map(lambda d: d == d.to_integral_value())
    is_integer = bool(int_like.all())

    if is_integer:
        int_series = decimals.map(lambda d: int(d) if d is not None else pd.NA).astype("Int64")
        return int_series, None, True, True

    # Estimate precision and scale
    max_digits = 1
    max_scale = 0
    for d in decimals.dropna():
        sign, digits, exp = d.as_tuple()
        digits_count = len(digits)
        scale = -exp if exp < 0 else 0
        integer_digits = digits_count - scale
        max_digits = max(max_digits, integer_digits + scale)
        max_scale = max(max_scale, scale)
    precision = min(max(1, max_digits), 38)
    scale = min(max(0, max_scale), 18)
    return decimals, (precision, scale), False, True


def infer_mysql_type_from_samples(samples: list[Any]) -> str:
    # Try datetime
    try:
        dt = pd.to_datetime(pd.Series(samples, dtype="string"), errors="coerce", utc=False)
        if float(dt.notna().mean()) >= 0.9:
            return "DATETIME NULL"
    except Exception:
        pass

    # Try numeric
    cleaned = [clean_numeric_string(v) for v in samples]

    def to_decimal(x: Optional[str]) -> Optional[Decimal]:
        if x in (None, ""):
            return None
        try:
            return Decimal(x)
        except (InvalidOperation, ValueError):
            return None

    decimals = [to_decimal(x) for x in cleaned]
    non_null = [d for d in decimals if d is not None]
    non_null_ratio = (len(non_null) / max(1, len([v for v in samples if v is not None])))
    if len(non_null) >= 1 and non_null_ratio >= 0.9:
        if all(d == d.to_integral_value() for d in non_null):
            return "BIGINT NULL"
        # Estimate precision/scale
        max_digits = 1
        max_scale = 0
        for d in non_null:
            sign, digits, exp = d.as_tuple()
            digits_count = len(digits)
            scale = -exp if exp < 0 else 0
            integer_digits = digits_count - scale
            max_digits = max(max_digits, integer_digits + scale)
            max_scale = max(max_scale, scale)
        precision = min(max(1, max_digits), 38)
        scale = min(max(0, max_scale), 18)
        return f"DECIMAL({precision},{scale}) NULL"

    # Try boolean
    truthy = {"1", "true", "t", "yes", "y"}
    falsy = {"0", "false", "f", "no", "n"}

    def to_bool(x: Any) -> Optional[bool]:
        if x is None:
            return None
        s = str(x).strip().lower()
        if s in truthy:
            return True
        if s in falsy:
            return False
        return None

    bools = [to_bool(v) for v in samples]
    non_na_bools = [b for b in bools if b is not None]
    if len(non_na_bools) >= 1 and (len(non_na_bools) / max(1, len([v for v in samples if v is not None])) >= 0.9):
        return "BOOLEAN NULL"

    # Fallback VARCHAR sized to samples
    try:
        lens = [len(str(v)) for v in samples if v is not None]
        max_len = max(lens) if lens else 255
    except Exception:
        max_len = 255
    if max_len > 1024:
        return "TEXT NULL"
    return f"VARCHAR({max(32, max_len)}) NULL"


