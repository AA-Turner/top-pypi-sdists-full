import collections.abc
from dataclasses import is_dataclass
from typing import TYPE_CHECKING, Any, FrozenSet, List, Mapping, Union

import attrs
import pandas as pd
import pyarrow as pa

from chalk import DataFrame
from chalk.client import ChalkBaseException, ChalkError, ErrorCode
from chalk.features import Feature
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl
    from pydantic import BaseModel
else:
    try:
        from pydantic.v1 import BaseModel
    except ImportError:
        from pydantic import BaseModel


class _UploadFeaturesValidationErrors:
    @staticmethod
    def expected_mapping(e: Any):
        return ChalkError(
            code=ErrorCode.INVALID_QUERY,
            message=(
                f"Multi upload detected a list of items, but some list items are `{type(e).__name__}`. If you "
                "wish to upload a list of items, be sure each item in the list is a mapping where "
                "each key is a feature and each value is the desired value for that feature"
                "in context of the other inputs specified by the other key:value pairs in the "
                "mapping."
            ),
        )

    @staticmethod
    def expected_same_length_lists(
        expected_length: int, expected_length_col: str, actual_length: int, actual_length_col: str
    ):
        expected_s = "" if expected_length == 1 else "s"
        actual_s = "" if actual_length == 1 else "s"
        return ChalkError(
            code=ErrorCode.INVALID_QUERY,
            message=(
                f"expected all values in mapping to be lists of the same length, found {expected_length} "
                f"value{expected_s} for '{expected_length_col}' and {actual_length} value{actual_s} for {actual_length_col}"
            ),
        )

    @staticmethod
    def expected_list_in_mapping(col_name: str, col_value: Any):
        return ChalkError(
            code=ErrorCode.INVALID_QUERY,
            message=f"expected all values in mapping to be lists, found '{type(col_value).__name__}' for '{col_name}'",
        )

    @staticmethod
    def structs_not_supported(fqn: str, obj: Any) -> ChalkError:
        return ChalkError(
            code=ErrorCode.INVALID_QUERY,
            message=(
                f"Multi-upload does not yet support uploading structs, "
                f"but values for feature '{fqn}' has the type {type(obj).__name__}"
            ),
        )


def _is_struct_like_object(obj: Any) -> bool:
    return (
        is_dataclass(obj)
        or (isinstance(obj, tuple) and hasattr(obj, "_fields"))
        or isinstance(obj, BaseModel)
        or attrs.has(obj.__class__)
        or isinstance(obj, Mapping)
    )


def _validate_mapping(inputs: Mapping[Union[str, Feature, Any], Any]) -> List[ChalkError]:
    if len(inputs) == 0:
        return []

    num_rows = None
    reference_col = None
    for k, v in inputs.items():
        if not isinstance(v, list):
            return [_UploadFeaturesValidationErrors.expected_list_in_mapping(str(k), v)]
        if num_rows is None:
            reference_col = k
            num_rows = len(v)
        elif num_rows != len(v):
            assert reference_col is not None
            return [
                _UploadFeaturesValidationErrors.expected_same_length_lists(num_rows, str(reference_col), len(v), str(k))
            ]
        if _is_struct_like_object(v[0]):
            return [_UploadFeaturesValidationErrors.structs_not_supported(str(k), v[0])]

    return []


def _validate_list(inputs: List) -> List[ChalkError]:
    if len(inputs) == 0:
        return []

    for e in inputs:
        if not isinstance(e, collections.abc.Mapping):
            return [_UploadFeaturesValidationErrors.expected_mapping(e)]

        for k, v in e.items():
            if _is_struct_like_object(v):
                return [_UploadFeaturesValidationErrors.structs_not_supported(k, v)]

    return []


def to_multi_upload_inputs(
    inputs: Union[
        List[Mapping[Union[str, Feature, Any], Any]],
        Mapping[Union[str, Feature, Any], List[Any]],
        pd.DataFrame,
        "pl.DataFrame",
        DataFrame,
    ],
) -> List[pa.Table]:
    tables: List[pa.Table] = []
    if isinstance(inputs, DataFrame):
        tables.append(inputs.to_pyarrow())
    elif isinstance(inputs, collections.abc.Mapping):
        if len(inputs) == 0:
            return []
        errs = _validate_mapping(inputs)
        if errs:
            raise ChalkBaseException(errs, detail="multi-upload input validation failed")
        tables.append(pa.Table.from_pydict({str(k): lv for (k, lv) in inputs.items()}))
    elif isinstance(inputs, list):
        if len(inputs) == 0:
            return []
        errs = _validate_list(inputs)
        if errs:
            raise ChalkBaseException(errs, detail="multi-upload input validation failed")
        common_keys_to_mappings: Mapping[FrozenSet, List[Mapping]] = collections.defaultdict(list)
        for mapping in inputs:
            common_keys_to_mappings[frozenset(mapping.keys())].append(mapping)
        for common_mappings_list in common_keys_to_mappings.values():
            fqn_to_values = collections.defaultdict(list)
            for mapping in common_mappings_list:
                for k, v in mapping.items():
                    fqn_to_values[k].append(v)
            tables.append(pa.Table.from_pydict(fqn_to_values))
    elif isinstance(inputs, pd.DataFrame):
        tables.append(pa.Table.from_pandas(inputs))
    else:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if isinstance(inputs, (pl.DataFrame, pl.LazyFrame)):  # pyright: ignore[reportUnnecessaryIsInstance]
            tables.append(inputs.to_arrow())
        else:
            try:
                df = pd.DataFrame(inputs)
            except:
                raise ValueError(
                    f"Multi upload received an input type that couldn't be interpreted: {str(type(inputs))}."
                )
            tables.append(pa.Table.from_pandas(df))

    if not tables:
        raise ValueError(f"Multi upload received an empty `inputs` object")

    return tables
