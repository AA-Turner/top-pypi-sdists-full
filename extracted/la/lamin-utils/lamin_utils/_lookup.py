from __future__ import annotations

import keyword
import re
from collections import namedtuple
from typing import TYPE_CHECKING, Any, Literal

from ._logger import logger

if TYPE_CHECKING:
    from collections.abc import Iterable


def _append_records_to_list(df_dict: dict, value: str, record) -> None:
    """Append unique records to a list."""
    values_list = df_dict[value]

    if not isinstance(values_list, list):
        values_list = [values_list]
    try:
        df_dict[value] = list(dict.fromkeys(values_list + [record]))
    except TypeError:
        df_dict[value] = values_list


def _create_df_dict(
    df: Any = None,
    field: str | None = None,
    records: list | None = None,
    values: list | None = None,
    tuple_name: str | None = None,
) -> dict:
    """Create a dict with {lookup key: records in namedtuple}.

    Value is a list of namedtuples if multiple records match the same key.
    """
    if df is not None:
        records = df.itertuples(index=False, name=tuple_name)
        values = df[field]
    df_dict: dict = {}  # a dict of namedtuples as records and values as keys
    for i, row in enumerate(records):  # type:ignore
        value = values[i]  # type:ignore
        if not isinstance(value, str):
            continue
        if value == "":
            continue
        if value in df_dict:
            _append_records_to_list(df_dict=df_dict, value=value, record=row)
        else:
            df_dict[value] = row
    return df_dict


class _ListValueWrapper:
    """Wrapper that warns when a list value is accessed and applies keep strategy."""

    def __init__(
        self,
        field_name: str,
        values: list,
        keep: Literal["first", "last", False],
        return_field: str | None = None,
    ):
        self._field_name = field_name
        self._values = values
        self._keep = keep
        self._return_field = return_field
        self._accessed = False

    def _warn_and_process(self):
        """Issue warning and return processed value."""
        if not self._accessed:
            logger.warning(
                f"{len(self._values)} records found for '{self._field_name}'. "
                f"Returning based on keep='{self._keep}'."
            )
            self._accessed = True

        # Apply keep strategy
        if self._keep == "first":
            selected_value = self._values[0] if self._values else None
        elif self._keep == "last":
            selected_value = self._values[-1] if self._values else None
        elif self._keep is False:
            selected_value = self._values
        else:
            selected_value = self._values[0] if self._values else None

        # Apply return_field if specified
        if self._return_field is not None:
            if self._keep is False and isinstance(selected_value, list):
                return [
                    getattr(item, self._return_field)
                    if hasattr(item, self._return_field)
                    else item
                    for item in selected_value
                ]
            elif hasattr(selected_value, self._return_field):
                return getattr(selected_value, self._return_field)

        return selected_value

    def __getattr__(self, name):
        """Intercept any attribute access to trigger warning."""
        processed_value = self._warn_and_process()
        return getattr(processed_value, name)

    def __str__(self):
        """String representation triggers warning."""
        return str(self._warn_and_process())

    def __repr__(self):
        """Representation triggers warning."""
        return repr(self._warn_and_process())

    def __iter__(self):
        """Iteration triggers warning."""
        processed_value = self._warn_and_process()
        return iter(processed_value)

    def __len__(self):
        """Length check triggers warning."""
        processed_value = self._warn_and_process()
        return len(processed_value)

    def __getitem__(self, key):
        """Indexing triggers warning."""
        processed_value = self._warn_and_process()
        return processed_value[key]

    def __bool__(self):
        """Boolean conversion triggers warning."""
        processed_value = self._warn_and_process()
        return bool(processed_value)

    def __eq__(self, other):
        """Equality comparison triggers warning."""
        processed_value = self._warn_and_process()
        return processed_value == other


class Lookup:
    """Lookup object with dot and [] access."""

    # removed DataFrame type annotation to speed up import time
    def __init__(
        self,
        field: str | None = None,
        tuple_name="MyTuple",
        prefix: str = "bt",
        df: Any = None,
        values: Iterable | None = None,
        records: list | None = None,
        keep: Literal["first", "last", False] = "first",
    ) -> None:
        self._tuple_name = tuple_name
        if df is not None:
            if df.shape[0] > 500000:
                logger.warning(
                    "generating lookup object from >500k keys is not recommended and"
                    " extremely slow"
                )
            values = df[field]
        self._df_dict = _create_df_dict(
            df=df,
            field=field,
            records=records,
            values=values,  # type:ignore
            tuple_name=self._tuple_name,
        )
        lkeys = self._to_lookup_keys(values=values, prefix=prefix)  # type:ignore
        self._lookup_dict = self._create_lookup_dict(lkeys=lkeys, df_dict=self._df_dict)
        self._prefix = prefix
        self._keep = keep

    def _to_lookup_keys(self, values: Iterable, prefix: str) -> dict:
        """Convert a list of strings to tab-completion allowed formats.

        Returns:
            {lookup_key: value_or_values}
        """
        lkeys: dict = {}
        for value in list(values):
            if not isinstance(value, str):
                continue
            # replace any special character with _
            lkey = re.sub("[^0-9a-zA-Z_]+", "_", str(value)).lower()
            if lkey == "":  # empty strings are skipped
                continue
            if not lkey[0].isalpha():  # must start with a letter
                lkey = f"{prefix.lower()}_{lkey}"

            if lkey in lkeys:
                # if multiple values have the same lookup key
                # put the values into a list
                _append_records_to_list(df_dict=lkeys, value=lkey, record=value)
            else:
                lkeys[lkey] = value
        return lkeys

    def _create_lookup_dict(self, lkeys: dict, df_dict: dict) -> dict:
        lkey_dict: dict = {}  # a dict of namedtuples as records and lookup keys as keys
        for lkey, values in lkeys.items():
            if isinstance(values, list):
                combined_list = []
                for v in values:
                    records = df_dict.get(v)
                    if isinstance(records, list):
                        combined_list += records
                    else:
                        combined_list.append(records)
                lkey_dict[lkey] = combined_list
            else:
                lkey_dict[lkey] = df_dict.get(values)

        return lkey_dict

    def dict(self) -> dict:
        """Dictionary of the lookup."""
        return self._df_dict

    def lookup(self, return_field: str | None = None) -> tuple:
        """Lookup records with dot access."""
        # Create a copy to avoid modifying the original
        lookup_dict_copy = self._lookup_dict.copy()

        # Process values, wrapping lists in warning wrapper
        processed_dict = {}
        for key, value in lookup_dict_copy.items():
            # Handle Python keywords by appending an underscore
            if keyword.iskeyword(key):
                key = f"{key}_"
            if isinstance(value, list) and len(value) > 1:
                # Wrap list values that have more than one item
                processed_dict[key] = _ListValueWrapper(
                    key, value, self._keep, return_field
                )
            else:
                # Handle single values or single-item lists
                if isinstance(value, list) and len(value) == 1:
                    value = value[0]  # Unwrap single-item lists

                if return_field is not None and hasattr(value, return_field):
                    processed_dict[key] = getattr(value, return_field)
                else:
                    processed_dict[key] = value

        keys: list = list(processed_dict.keys()) + ["dict"]
        MyTuple = namedtuple("Lookup", keys)  # type:ignore

        return MyTuple(**processed_dict, dict=self.dict)  # type:ignore
