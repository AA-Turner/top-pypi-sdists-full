# pyright: reportPrivateUsage=false
from __future__ import annotations

import importlib
import importlib.util
import linecache
import os
import sys
import time
import traceback
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Tuple, Type, Union, cast, get_args, get_origin

import pyarrow as pa

from chalk._lsp.error_builder import DiagnosticBuilder, LSPErrorBuilder
from chalk.features import Feature, Features, FeatureSetBase, Filter, unwrap_feature
from chalk.features.feature_field import WindowConfigResolved
from chalk.features.pseudofeatures import Now

if TYPE_CHECKING:
    from chalk.features.feature_set import FeaturesProtocol

from chalk.features.resolver import RESOLVER_REGISTRY, Resolver
from chalk.features.underscore import (
    Underscore,
    UnderscoreAttr,
    UnderscoreCall,
    UnderscoreFunction,
    UnderscoreItem,
    UnderscoreRoot,
)
from chalk.gitignore.helper import IgnoreConfig, get_default_combined_ignore_config
from chalk.parsed.duplicate_input_gql import (
    DiagnosticGQL,
    DiagnosticSeverityGQL,
    FailedImport,
    PositionGQL,
    PublishDiagnosticsParams,
    RangeGQL,
)
from chalk.sql import SQLSourceGroup
from chalk.sql._internal.sql_file_resolver import get_sql_file_resolvers, get_sql_file_resolvers_from_paths
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import parse_chalk_duration_s, timedelta_to_duration
from chalk.utils.import_utils import py_path_to_module
from chalk.utils.log_with_context import get_logger
from chalk.utils.paths import get_directory_root

try:
    from types import UnionType
except ImportError:
    UnionType = Union

_logger = get_logger(__name__)
_import_logger = get_logger("chalk.import_logger")


has_imported_all_files = False


def import_all_files_once(
    file_allowlist: Optional[List[str]] = None,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
    override: bool = False,
) -> List[FailedImport]:
    global has_imported_all_files
    if has_imported_all_files:
        return []
    failed = import_all_files(
        file_allowlist=file_allowlist,
        project_root=project_root,
        only_sql_files=only_sql_files,
        override=override,
    )
    has_imported_all_files = True
    return failed


supported_aggs = (
    "approx_count_distinct",
    "approx_percentile",
    "array_agg",
    "count",
    "max",
    "mean",
    "min",
    "std",
    "std_sample",
    "stddev",
    "stddev_sample",
    "sum",
    "var",
    "var_sample",
)


class ChalkParseError(ValueError):
    pass


def _try_parse_datetime(
    name: str,
    dt: datetime | str | None,
) -> datetime | None:
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt
    if isinstance(dt, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        try:
            return datetime.fromisoformat(dt)
        except ValueError as e:
            raise ChalkParseError(f"parsing {name}: {str(e)}")
    raise ChalkParseError(f"{name} must be a string or a datetime object. Found: {dt}")


def _try_parse_duration(
    name: str,
    d: timedelta | str | int | None,
) -> int | None:
    if d is None:
        return None
    try:
        return parse_chalk_duration_s(d)
    except ValueError as e:
        raise ChalkParseError(f"parsing {name}: {str(e)}")


def _try_parse_resolver_fqn(name: str, resolver: Any) -> str | None:
    if resolver is None:
        return None
    if isinstance(resolver, Resolver):
        return resolver.fqn
    if isinstance(resolver, str):
        return resolver
    raise ChalkParseError(
        f"{name} must be a string or a Resolver object. Found: {resolver}",
    )


def _check_types(
    feature_name: str,
    aggregation: str,
    joined_feature: Feature | None,
    this_annotation: Any,
) -> None:
    if joined_feature is None:
        if aggregation != "count":
            raise ChalkParseError(
                f"feature '{feature_name}' does not aggregate a child feature; expected 'count' aggregation"
            )
        _validate_types(
            annotation=this_annotation,
            permitted_types=(int, float),
            aggregation_name=aggregation,
            joined=False,
            feature_name=feature_name,
        )
        return

    joined_annotation = joined_feature.typ.parsed_annotation
    if aggregation not in {"count", "approx_count_distinct", "array_agg"}:
        _validate_types(
            annotation=joined_annotation,
            permitted_types=(int, float),
            aggregation_name=aggregation,
            joined=True,
            feature_name=joined_feature.name,
        )

    if aggregation in (
        "approx_percentile",
        "mean",
        "std",
        "std_sample",
        "stddev",
        "stddev_sample",
        "var",
        "var_sample",
    ):
        _validate_types(
            annotation=this_annotation,
            permitted_types=(float,),
            aggregation_name=aggregation,
            joined=False,
            feature_name=feature_name,
        )

    elif aggregation == "min" or aggregation == "max":
        if _get_underlying_type(this_annotation, feature_name) != _get_underlying_type(
            joined_annotation, joined_feature.name
        ):
            raise ChalkParseError(
                (
                    f"feature '{feature_name}' of type '{_get_printable_name(this_annotation)}' should match "
                    f"joined feature '{joined_feature.name}' of type '{_get_printable_name(joined_annotation)}' "
                    f"for '{aggregation}' aggregation"
                )
            )

    elif aggregation == "count":
        _validate_types(
            annotation=this_annotation,
            permitted_types=(int, float),
            aggregation_name=aggregation,
            joined=False,
            feature_name=feature_name,
        )

    elif aggregation == "sum":
        _validate_types(
            annotation=this_annotation,
            permitted_types=(int, float),
            aggregation_name=aggregation,
            joined=False,
            feature_name=feature_name,
        )
        if (
            _get_underlying_type(joined_annotation, feature_name) is float
            and _get_underlying_type(this_annotation, feature_name) is int
        ):
            raise ChalkParseError(
                f"feature '{feature_name}' should be a 'float' for 'sum' aggregation with joined feature '{joined_feature.name}'; found 'int'"
            )


def _validate_types(
    annotation: type, permitted_types: tuple[type, ...], aggregation_name: str, joined: bool, feature_name: str
):
    error_message = (
        f"feature '{feature_name}' should be of type {' or '.join(p.__name__ for p in permitted_types)} "
        + f"for aggregation '{aggregation_name}'; found '{_get_printable_name(annotation)}'"
    )
    if joined:
        error_message = "joined " + error_message
    t = _get_underlying_type(annotation, feature_name)
    if t not in permitted_types:
        raise ChalkParseError(error_message)


def _get_underlying_type(t: type, feature_name: str) -> type:
    if get_origin(t) in (Union, UnionType):
        args = get_args(t)
        return_type = None
        for arg in args:
            if arg == type(None):
                continue
            if return_type is not None:
                raise ChalkParseError(
                    f"feature {feature_name} is a Union over types {(str(s) for s in args)}, which includes "
                    + f"contradictory types '{str(return_type)}' and '{str(arg)}'"
                )
            return_type = arg
        return return_type if return_type is not None else t
    return t


def _parse_agg_function_call(expr: Underscore | None) -> Tuple[str, Underscore]:
    if not isinstance(expr, UnderscoreCall):
        raise ChalkParseError(
            "missing aggregation function call for materialized aggregate feature -- if materialization is enabled, the expression must include an aggregation function (e.g. .count())"
        )

    call_expr = expr
    if len(call_expr._chalk__args) > 0 or len(call_expr._chalk__kwargs) > 0:
        raise ChalkParseError("should not have any arguments or keyword arguments")

    function_attribute = call_expr._chalk__parent
    if not isinstance(function_attribute, UnderscoreAttr):
        raise ChalkParseError("expected an aggregation, like `.sum()`")

    aggregation = function_attribute._chalk__attr
    if aggregation not in supported_aggs:
        raise ChalkParseError(f"aggregation should be one of {', '.join(supported_aggs)}")

    return aggregation, function_attribute._chalk__parent


def _parse_projection(expr: Underscore | None) -> str:
    # TODO: get in here and find the filters
    if not isinstance(expr, UnderscoreAttr):
        raise ChalkParseError("expected a feature, like `_.amount`")

    attr = expr._chalk__attr
    if not isinstance(expr._chalk__parent, UnderscoreRoot):
        raise ChalkParseError("expected a single feature, like `_.amount`")

    return attr


def _get_has_many_class(
    parent: Type[Features],
    has_many_feature_name: str,
    group_names: list[str],
    aggregated_feature_name: str | None,
) -> Tuple[Type[Features], list[Feature], Feature | None]:
    """
    If the has-many class and aggregated features are found:
        Tuple[
            Type[Features], -- joined_class
            list[Feature],  -- the group_names translated to features on joined_class. Also includes the foreign join key
            Feature | None, -- the aggregated feature on joined_class, from aggregated_feature_name
            None            -- the error is None
        ]
    """
    try:
        has_many_feature = getattr(parent, has_many_feature_name)
    except Exception:
        raise ChalkParseError(f"could not find feature '{has_many_feature_name}' in the child namespace")

    underlying = unwrap_feature(has_many_feature, raise_error=False)

    if not isinstance(underlying, Feature):
        raise ChalkParseError(f"the attribute '{has_many_feature_name}' is not a feature")

    if not underlying.is_has_many:
        raise ChalkParseError(f"the attribute '{has_many_feature_name}' is not a has-many feature")

    joined_class = underlying.joined_class
    if joined_class is None:
        raise ChalkParseError(f"has-many feature '{has_many_feature_name}' is not joined to a class")

    foreign_join_keys = underlying.foreign_join_keys
    if len(foreign_join_keys) == 0:
        raise ChalkParseError(f"has-many feature '{has_many_feature_name}' is missing a foreign join key")

    group_by_features: list[Feature] = foreign_join_keys
    for group_name in group_names:
        joined_feature_wrapper = getattr(joined_class, group_name, None)
        if joined_feature_wrapper is None:
            raise ChalkParseError(f"joined class '{_get_printable_name(joined_class)}' missing feature '{group_name}'")

        joined_feature = unwrap_feature(joined_feature_wrapper)
        if not joined_feature.is_scalar:
            raise ChalkParseError(
                f"group feature '{joined_feature.window_stem}' not a scalar, like a 'float' or an 'int'"
            )
        group_by_features.append(joined_feature)

    if aggregated_feature_name is None:
        return joined_class, group_by_features, None

    aggregated_feature_wrapper = getattr(joined_class, aggregated_feature_name, None)
    if aggregated_feature_wrapper is None:
        raise ChalkParseError(
            f"joined class '{_get_printable_name(joined_class)}' missing feature '{aggregated_feature_name}'"
        )

    aggregated_feature = unwrap_feature(aggregated_feature_wrapper)
    if not aggregated_feature.is_scalar:
        raise ChalkParseError(
            f"joined feature '{aggregated_feature.window_stem}' not a scalar, like a 'float' or an 'int'"
        )

    return joined_class, group_by_features, aggregated_feature


def run_post_import_fixups():
    for _, fsb in FeatureSetBase.registry.items():
        for f in fsb.__chalk_group_by_materialized_windows__:
            # Fix up group by window materializations like .group_by(...).agg(...):
            #   num_theorem_lines_by_author: DataFrame = group_by_windowed(
            #       "1m", "2m", materialization={...},
            #       expression=_.theorems.group_by(_.author).agg(_.num_lines.sum()),
            #   )
            try:
                mat = parse_grouped_window(f=f)
                gbw = f.group_by_windowed
                assert gbw is not None
                gbw._window_materialization_parsed = mat
                f.window_materialization_parsed = mat
            except ChalkParseError as e:
                error = e.args[0]
                lsp_error_builder = fsb.__chalk_error_builder__
                lsp_error_builder.add_diagnostic(
                    message=f"The materialized feature '{f.name}' is incorrectly configured.",
                    label=error,
                    range=lsp_error_builder.property_value_kwarg_range(
                        feature_name=f.attribute_name,
                        kwarg="expression",
                    )
                    or lsp_error_builder.property_range(feature_name=f.attribute_name),
                    code="42",
                )

        for f in fsb.__chalk_materialized_windows__:
            # Fix up materialized windows without group by
            #   sum_spending: DataFrame = group_by_windowed(
            #       "1m", "2m", materialization={...},
            #       expression=_.transactions[_.amount].sum(),
            #   )
            assert f.underscore_expression is not None
            assert f.window_materialization is not None

            try:
                f.window_materialization_parsed = parse_windowed_materialization(f=f)
            except ChalkParseError as e:
                error = e.args[0]
                f.lsp_error_builder.add_diagnostic(
                    message=f"The windowed materialization on feature '{f.window_stem}' is incorrectly configured.",
                    label=error,
                    range=f.lsp_error_builder.property_value_kwarg_range(
                        feature_name=f.window_stem,
                        kwarg="expression",
                    )
                    or f.lsp_error_builder.property_range(feature_name=f.window_stem),
                    code="39",
                )


def parse_grouped_window(f: Feature) -> WindowConfigResolved:
    """
    _.transactions.group_by(_.mcc).agg(_.amount.sum())
    """
    assert f.features_cls is not None
    expr = f.underscore_expression
    if not isinstance(expr, UnderscoreCall):
        raise ChalkParseError("group expression should end with `.agg(...)`")
    pyarrow_dtype = f.converter.pyarrow_dtype
    kind = f.typ.parsed_annotation

    assert f.group_by_windowed is not None

    materialization = f.group_by_windowed._materialization
    bucket_duration_str = (
        materialization.get("bucket_duration", None) if isinstance(materialization, dict) else f.window_duration
    )
    assert bucket_duration_str is not None
    bucket_duration_seconds = parse_chalk_duration_s(bucket_duration_str)

    bucket_start = datetime.fromtimestamp(0, tz=timezone.utc)
    if isinstance(materialization, dict):
        bucket_start = materialization.get("bucket_start", bucket_start)

    call_expr = expr
    call_exp_parent = call_expr._chalk__parent
    if not isinstance(call_exp_parent, UnderscoreAttr):
        raise ChalkParseError("expected a `.agg(...) call")

    agg_function_name = call_exp_parent._chalk__attr
    if agg_function_name != "agg":
        raise ChalkParseError(f"expected a `.agg(...) call, but found the function call `{agg_function_name}`")

    if len(call_expr._chalk__kwargs):
        raise ChalkParseError("aggregations should not be supplied as keyword arguments")

    if len(call_expr._chalk__args) != 1:
        raise ChalkParseError("expected a single aggregation function")

    aggregation_expr = call_expr._chalk__args[0]

    aggregation, par = _parse_agg_function_call(aggregation_expr)

    # If it's an error, we'll tolerate `.count()`, so leave it be for now.
    try:
        child_feature_name = _parse_projection(par)
    except ChalkParseError:
        child_feature_name = None
    if not isinstance(par, UnderscoreAttr) and not isinstance(par, UnderscoreRoot):
        raise ChalkParseError("expected a feature, like `_.amount`")

    group_by_call = call_exp_parent._chalk__parent
    if not isinstance(group_by_call, UnderscoreCall):
        raise ChalkParseError("expected a group_by expression")

    group_by_call_parent = group_by_call._chalk__parent
    if not isinstance(group_by_call_parent, UnderscoreAttr):
        raise ChalkParseError("expected a group_by expression")

    group_by_call_attr = group_by_call_parent._chalk__attr
    if group_by_call_attr != "group_by":
        raise ChalkParseError("expected a group_by expression")

    group_key_exprs = group_by_call._chalk__args

    if len(group_by_call._chalk__kwargs) > 0:
        raise ChalkParseError("group_by should not have any keyword arguments, only arguments")

    group_keys: list[str] = []
    for group_key_expr in group_key_exprs:
        group_key = _parse_projection(group_key_expr)
        group_keys.append(group_key)

    # _.transactions.group_by(_.mcc).agg(_.amount.sum())

    has_many_parent = group_by_call_parent._chalk__parent

    # this one has filters in it
    filters: list[UnderscoreFunction] = []
    if isinstance(has_many_parent, UnderscoreItem):
        projections, filters = extract_filters_and_projections(has_many_parent)

        if len(projections) != 0:
            raise ChalkParseError(
                "projections for the group_by should appear in the `.agg` call, like `.agg(_.amount.sum())`"
            )

        has_many_parent = has_many_parent._chalk__parent

    has_many_name = _parse_projection(has_many_parent)

    joined_class, group_key_features, aggregated_feature = _get_has_many_class(
        parent=f.features_cls,
        has_many_feature_name=has_many_name,
        group_names=group_keys,
        aggregated_feature_name=child_feature_name,
    )
    _check_types(
        feature_name=f.name,
        aggregation=aggregation,
        joined_feature=aggregated_feature,
        this_annotation=kind,
    )

    parsed_filters = clean_filters(joined_class, filters)

    if bucket_start.tzinfo is None:
        bucket_start = bucket_start.replace(tzinfo=timezone.utc)
    bucket_start = bucket_start.astimezone(tz=timezone.utc)

    cfg = WindowConfigResolved(
        namespace=joined_class.namespace,
        group_by=group_key_features,
        bucket_duration_seconds=bucket_duration_seconds,
        bucket_start=bucket_start,
        aggregation=aggregation,
        aggregate_on=aggregated_feature,
        pyarrow_dtype=pyarrow_dtype,
        filters=parsed_filters,
        backfill_resolver=_try_parse_resolver_fqn(
            "backfill_resolver",
            f.window_materialization.get("backfill_resolver", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_schedule=f.window_materialization.get("backfill_schedule", None)
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_lookback_duration_seconds=_try_parse_duration(
            "backfill_lookback_duration",
            f.window_materialization.get("backfill_lookback_duration", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_start_time=_try_parse_datetime(
            "backfill_start_time",
            f.window_materialization.get("backfill_start_time", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        continuous_resolver=_try_parse_resolver_fqn(
            "continuous_resolver",
            f.window_materialization.get("continuous_resolver", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        continuous_buffer_duration_seconds=_try_parse_duration(
            "continuous_buffer_duration",
            f.window_materialization.get("continuous_buffer_duration", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
    )

    return cfg


def extract_filters_and_projections(
    expr: Underscore,
) -> Tuple[List[UnderscoreAttr], List[UnderscoreFunction]]:
    projections: list[UnderscoreAttr] = []
    filters: list[UnderscoreFunction] = []
    if not isinstance(expr, UnderscoreItem):
        raise ChalkParseError("expected a feature, like `_.amount`, or a filter, like `_.amount > 0`")

    keys = expr._chalk__key
    if not isinstance(keys, tuple):  # pyright: ignore[reportUnnecessaryIsInstance]
        keys = (keys,)

    for k in keys:
        if isinstance(k, UnderscoreFunction):
            filters.append(k)
        elif isinstance(k, UnderscoreAttr):
            projections.append(k)
        else:
            raise ChalkParseError("expected a feature, like `_.amount`, or a filter, like `_.amount > 0`")

    return projections, filters


def clean_filters(joined_class: Type[Features], filters: list[UnderscoreFunction]) -> List[Filter]:
    parsed_filters: List[Filter] = []
    for filt in filters:
        op = filt._chalk__function_name
        left = filt._chalk__args[0]
        right = filt._chalk__args[1]

        if op not in ("==", "!=", ">", "<", ">=", "<=", "in"):
            raise ChalkParseError(f"expected a boolean operation for the filter, like `_.amount > 0`, but found `{op}`")

        if isinstance(left, UnderscoreAttr):
            left_attr = left._chalk__attr
            if left_attr not in ("chalk_window", "chalk_now"):
                try:
                    left = getattr(joined_class, left_attr)
                except Exception:
                    raise ChalkParseError(f"could not find feature '{left_attr}' in the joined class")
            if left_attr == "chalk_now":
                left = Now

        if isinstance(right, UnderscoreAttr):
            right_attr = right._chalk__attr
            if right_attr not in ("chalk_window", "chalk_now"):
                try:
                    right = getattr(joined_class, right_attr)
                except Exception:
                    raise ChalkParseError(f"could not find feature '{right_attr}' in the joined class")
            if right_attr == "chalk_now":
                right = Now

        parsed_filter = Filter(lhs=left, operation=op, rhs=right)
        parsed_filters.append(parsed_filter)

    return parsed_filters


def parse_windowed_materialization(f: Feature) -> WindowConfigResolved | None:
    if f.window_duration is None:
        return None
    aggregation, getitem_expression = _parse_agg_function_call(f.underscore_expression)

    filters: list[UnderscoreFunction] = []
    aggregated_value = None
    if isinstance(getitem_expression, UnderscoreItem):
        agg_on = None

        keys = getitem_expression._chalk__key
        if not isinstance(keys, tuple):  # pyright: ignore[reportUnnecessaryIsInstance]
            keys = (keys,)

        for k in keys:
            if isinstance(k, UnderscoreFunction):
                filters.append(k)
            elif isinstance(k, UnderscoreAttr):
                agg_on = k
            else:
                raise ChalkParseError("expected a feature, like `_.amount`, or a filter, like `_.amount > 0`")

        if isinstance(agg_on, UnderscoreAttr):
            aggregated_value = agg_on._chalk__attr
            if not isinstance(agg_on._chalk__parent, UnderscoreRoot):
                raise ChalkParseError("expected a single feature from the child namespace, like `_.b`")
        elif aggregation != "count":
            raise ChalkParseError(f"missing attribute to aggregate, e.g. `_.a[_.amount].{aggregation}()`")

        child_attr_expression = getitem_expression._chalk__parent
    elif aggregation == "count":
        child_attr_expression = getitem_expression
    else:
        raise ChalkParseError(f"missing attribute to aggregate, e.g. `_.a[_.amount].{aggregation}()`")

    if not isinstance(child_attr_expression, UnderscoreAttr):
        raise ChalkParseError(f"expected reference to has-many feature, like _.children[...].{aggregation}()`")

    child_attr_name = child_attr_expression._chalk__attr
    if not isinstance(child_attr_expression._chalk__parent, UnderscoreRoot):
        raise ChalkParseError(f"expected single feature of the child namespace, like `_.{child_attr_name}`")

    if f.features_cls is None:
        raise ChalkParseError("feature class is None")

    joined_class, group_by_features, aggregated_feature = _get_has_many_class(
        parent=f.features_cls,
        has_many_feature_name=child_attr_name,
        group_names=[],
        aggregated_feature_name=aggregated_value,
    )

    _check_types(
        feature_name=f.window_stem,
        aggregation=aggregation,
        joined_feature=aggregated_feature,
        this_annotation=f.typ.parsed_annotation,
    )

    if f.window_materialization is None:
        raise ChalkParseError("missing 'materialization' in the windowed feature")

    parsed_filters = clean_filters(joined_class, filters)
    bucket_start = datetime.fromtimestamp(0, tz=timezone.utc)
    if f.window_materialization is True:
        bucket_duration = timedelta(seconds=f.window_duration)
    else:
        bucket_duration = f.window_materialization.get("bucket_duration", None)
        assert bucket_duration is None or isinstance(bucket_duration, timedelta)
        found = False
        for bd, values in f.window_materialization.get("bucket_durations", {}).items():
            assert isinstance(bd, timedelta)
            for value in ensure_tuple(values):
                assert isinstance(value, timedelta)
                if int(value.total_seconds()) == f.window_duration:
                    if found and bucket_duration is not None:
                        raise ChalkParseError(
                            (
                                "Multiple bucket durations found for the windowed feature "
                                f"{f.fqn}['{timedelta_to_duration(f.window_duration)}']: "
                                f"{timedelta_to_duration(bd)} and {timedelta_to_duration(bucket_duration)}"
                            )
                        )
                    bucket_duration = bd
                    found = True

        bucket_start = f.window_materialization.get("bucket_start", bucket_start)
        found = False
        for bs, values in f.window_materialization.get("bucket_starts", {}).items():
            assert isinstance(bs, datetime)
            for value in ensure_tuple(values):
                assert isinstance(value, timedelta)
                if int(value.total_seconds()) == f.window_duration:
                    if found:
                        raise ChalkParseError(
                            (
                                "Multiple bucket starts found for the windowed feature "
                                f"{f.fqn}['{timedelta_to_duration(f.window_duration)}']: "
                                f"{bs.isoformat()} and {bucket_start.isoformat()}"
                            )
                        )
                    bucket_start = bs
                    found = True

        if bucket_duration is None:
            raise ChalkParseError(
                f"No bucket duration was found for the window {timedelta_to_duration(f.window_duration)}"
            )

    if bucket_start.tzinfo is None:
        bucket_start = bucket_start.replace(tzinfo=timezone.utc)
    bucket_start = bucket_start.astimezone(tz=timezone.utc)

    return WindowConfigResolved(
        namespace=joined_class.namespace,
        group_by=group_by_features,
        bucket_duration_seconds=int(bucket_duration.total_seconds()),
        bucket_start=bucket_start,
        aggregation=aggregation,
        aggregate_on=aggregated_feature,
        pyarrow_dtype=f.converter.pyarrow_dtype,
        filters=parsed_filters,
        backfill_resolver=_try_parse_resolver_fqn(
            "backfill_resolver",
            f.window_materialization.get("backfill_resolver", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_schedule=f.window_materialization.get("backfill_schedule", None)
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_lookback_duration_seconds=_try_parse_duration(
            "backfill_lookback_duration",
            f.window_materialization.get("backfill_lookback_duration", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        backfill_start_time=_try_parse_datetime(
            "backfill_start_time",
            f.window_materialization.get("backfill_start_time", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        continuous_resolver=_try_parse_resolver_fqn(
            "continuous_resolver",
            f.window_materialization.get("continuous_resolver", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
        continuous_buffer_duration_seconds=_try_parse_duration(
            "continuous_buffer_duration",
            f.window_materialization.get("continuous_buffer_duration", None),
        )
        if isinstance(f.window_materialization, dict)
        else None,
    )


def import_all_files(
    file_allowlist: Optional[List[str]] = None,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
    check_ignores: bool = True,
    override: bool = False,
) -> List[FailedImport]:
    if project_root is None:
        project_root = get_directory_root()
    if project_root is None:
        return [
            FailedImport(
                filename="",
                module="",
                traceback="Could not find chalk.yaml in this directory or any parent directory",
            )
        ]

    python_files: list[Path] | None = None
    chalk_sql_files: list[str] | None = None

    if file_allowlist is not None:
        python_files = []
        chalk_sql_files = []
        for f in file_allowlist:
            if f.endswith(".py"):
                python_files.append(Path(f))
            elif f.endswith(".chalk.sql"):
                chalk_sql_files.append(f)

    if only_sql_files:
        return import_sql_file_resolvers(project_root, chalk_sql_files, override=override)

    failed_imports: List[FailedImport] = import_all_python_files_from_dir(
        project_root=project_root,
        file_allowlist=python_files,
        check_ignores=check_ignores,
    )
    has_import_errors = len(failed_imports) > 0
    failed_imports.extend(
        import_sql_file_resolvers(
            path=project_root,
            file_allowlist=chalk_sql_files,
            has_import_errors=has_import_errors,
            override=override,
        )
    )

    run_post_import_fixups()

    return failed_imports


def import_sql_file_resolvers(
    path: Path,
    file_allowlist: Optional[List[str]] = None,
    has_import_errors: bool = False,
    override: bool = False,
):
    if file_allowlist is not None:
        sql_resolver_results = get_sql_file_resolvers_from_paths(
            sources=[*BaseSQLSource.registry, *SQLSourceGroup.registry],
            paths=file_allowlist,
            has_import_errors=has_import_errors,
        )
    else:
        sql_resolver_results = get_sql_file_resolvers(
            sql_file_resolve_location=path,
            sources=[*BaseSQLSource.registry, *SQLSourceGroup.registry],
            has_import_errors=has_import_errors,
        )
    failed_imports: List[FailedImport] = []
    for result in sql_resolver_results:
        if result.resolver:
            result.resolver.add_to_registry(override=override)
        if result.errors and not has_import_errors:
            for error in result.errors:
                failed_imports.append(
                    FailedImport(
                        traceback=f"""EXCEPTION in Chalk SQL file resolver '{error.path}':
    {error.display}
""",
                        filename=error.path,
                        module=error.path,
                    )
                )
    return failed_imports


def get_resolver(
    resolver_fqn_or_name: str,
    project_root: Optional[Path] = None,
    only_sql_files: bool = False,
) -> Resolver:
    """
    Returns a resolver by name or fqn, including sql file resolvers.

    Parameters
    ----------
    resolver_fqn_or_name
        A string fqn or name of a resolver. Can also be a filename of sql file resolver
    project_root
        An optional path to import sql file resolvers from.
        If not supplied, will select the root directory of the Chalk project.
    only_sql_files
        If you have already imported all your features, sources, and resolvers, this flag
        can be used to restrict file search to sql file resolvers.

    Returns
    -------
    Resolver
    """
    failed_imports = import_all_files_once(project_root=project_root, only_sql_files=only_sql_files)
    if failed_imports:
        raise ValueError(f"File imports failed: {failed_imports}")
    if resolver_fqn_or_name.endswith(".chalk.sql"):
        resolver_fqn_or_name = resolver_fqn_or_name[: -len(".chalk.sql")]
    maybe_resolver = RESOLVER_REGISTRY.get_resolver(resolver_fqn_or_name)
    if maybe_resolver is not None:
        return maybe_resolver
    raise ValueError(f"No resolver with fqn or name {resolver_fqn_or_name} found")


def _get_py_files_fast(
    resolved_root: Path,
    venv_path: Optional[Path],
    ignore_config: Optional[IgnoreConfig],
) -> Iterable[Path]:
    """
    Gets all the .py files in the resolved_root directory and its subdirectories.
    Faster than the old method we were using because we are skipping the entire
    directory if the directory is determined to be ignored. But if any .gitignore
    or any .chalkignore file has negation, we revert to checking every filepath
    against each .*ignore file.

    :param resolved_root: Project root absolute path
    :param venv_path: Path of the venv folder to skip importing from.
    :param ignore_config: An optional CombinedIgnoreConfig object. If None, we simply don't check for ignores.
    :return: An iterable of Path each representing a .py file
    """

    for dirpath_str, dirnames, filenames in os.walk(resolved_root):
        dirpath = Path(dirpath_str).resolve()

        if (venv_path is not None and venv_path.samefile(dirpath)) or (
            ignore_config
            and not ignore_config.has_negation
            and ignore_config.ignored(os.path.join(str(dirpath), "#"))
            # Hack to make "dir/**" match "/Users/home/dir"
        ):
            dirnames.clear()  # Skip subdirectories
            continue  # Skip files

        for filename in filenames:
            if filename.endswith(".py"):
                filepath = dirpath / filename
                if not ignore_config or not ignore_config.ignored(filepath):
                    yield filepath


CHALK_IMPORT_FLAG: ContextVar[bool] = ContextVar("CHALK_IMPORT_FLAG", default=False)
""" A env var flag to be set to a truthy value during import to catch unsafe operations like ChalkClient().query()
Methods like that should check this env var flag and raise if run inappropriately """


class _UnderscoreValidationError(ValueError):
    """
    This exception class is thrown to indicate that a user-defined underscore expression is incorrect.
    It will not propagate outside of `supplement_diagnostics`.
    """

    ...


class ChalkImporter:
    def __init__(self):
        super().__init__()
        self.errors: Dict[str, FailedImport] = {}
        self.ranges: Dict[str, RangeGQL] = {}
        self.short_tracebacks: Dict[str, str] = {}
        self.repo_files = None

    def add_repo_files(self, repo_files: List[Path]):
        self.repo_files = repo_files

    def add_error(
        self,
        ex_type: Type[BaseException],
        ex_value: BaseException,
        ex_traceback: TracebackType,
        filename: Path,
        module_path: str,
    ):
        tb = traceback.extract_tb(ex_traceback)
        frame = 0
        error_file = str(filename)
        line_number = None
        for i, tb_frame in enumerate(tb):
            tb_filepath = Path(tb_frame.filename).resolve()
            if self.repo_files and tb_filepath in self.repo_files:
                line_number = tb_frame.lineno
                error_file = tb_frame.filename
            if filename == Path(tb_frame.filename).resolve():
                frame = i
        if error_file in self.errors:
            return
        error_message = f"""{(ex_type and ex_type.__name__) or 'Exception'} at '{error_file}{':' + str(line_number) if line_number is not None else ''}'"""
        full_traceback = f"""{error_message}:
{os.linesep.join(traceback.format_tb(ex_traceback)[frame:])}
{ex_type and ex_type.__name__}: {str(ex_value)}
"""
        self.errors[error_file] = FailedImport(
            traceback=full_traceback,
            filename=str(filename),
            module=module_path,
        )
        if line_number is not None:
            line = linecache.getline(str(filename), line_number)
            if line != "":
                self.ranges[error_file] = RangeGQL(
                    start=PositionGQL(
                        line=line_number,
                        character=len(line) - len(line.lstrip()),
                    ),
                    end=PositionGQL(
                        line=line_number,
                        character=max(len(line) - 1, 0),
                    ),
                )
                self.short_tracebacks[error_file] = error_message

    def get_failed_imports(self) -> List[FailedImport]:
        return list(self.errors.values())

    def convert_to_diagnostic(self, failed_import: FailedImport) -> Union[PublishDiagnosticsParams, None]:
        if failed_import.filename == "" or failed_import.filename not in self.ranges:
            return None

        range_ = self.ranges[failed_import.filename]
        traceback_ = self.errors[failed_import.filename].traceback
        builder = DiagnosticBuilder(
            severity=DiagnosticSeverityGQL.Error,
            message=traceback_,
            uri=failed_import.filename,
            range=range_,
            label="failed import",
            code="0",
            code_href=None,
        )
        return PublishDiagnosticsParams(
            uri=failed_import.filename,
            diagnostics=[builder.diagnostic],
        )

    def supplement_diagnostics(
        self,
        failed_imports: List[FailedImport],
        diagnostics: List[PublishDiagnosticsParams],
    ) -> List[PublishDiagnosticsParams]:
        """
        :param failed_imports: Errors encountered when importing customer code. This method converts them into LSP errors.
        :param diagnostics: this list is modified in-place with additioanl diagnostics
        :return: The same object as the input `diagnostics`
        """
        diagnostic_uris = {diagnostic.uri for diagnostic in diagnostics}
        for failed_import in failed_imports:
            if failed_import.filename not in diagnostic_uris:
                diagnostic_or_none = self.convert_to_diagnostic(failed_import)
                if diagnostic_or_none is not None:
                    diagnostics.append(diagnostic_or_none)

        for feature_class in FeatureSetBase.registry.values():
            # Iterate through every class, to find every underscore definition.
            for f in feature_class.features:
                if f.underscore_expression is not None:
                    # Validate that the underscore expression is well-formed.
                    # If it is not well-formed, then an `_UnderscoreValidationError` will
                    # be thrown.
                    try:
                        _supplemental_validate_underscore_expression(
                            state=_SupplementalState(),
                            class_namespace=feature_class,
                            underscore=f.underscore_expression,
                        )
                    except _UnderscoreValidationError as valid_exc:
                        import inspect

                        if f.underscore_expression._chalk_definition_location is not None:
                            # Underscore expressions attempt to obtain a best-effort location.
                            # Currently, the column is always 1, because we do not have a reliable
                            # way to get the column of a caller.
                            underscore_position = PositionGQL(
                                line=f.underscore_expression._chalk_definition_location.line,
                                character=f.underscore_expression._chalk_definition_location.column,
                            )
                            range = RangeGQL(
                                start=underscore_position,
                                end=underscore_position,
                            )
                        else:
                            # This is a fallback used if there is no provided location.
                            range = RangeGQL(
                                start=PositionGQL(line=1, character=1),
                                end=PositionGQL(line=1, character=1),
                            )
                        diagnostics.append(
                            PublishDiagnosticsParams(
                                uri=inspect.getfile(feature_class),
                                diagnostics=[
                                    DiagnosticGQL(
                                        range=range,
                                        message=f"The underscore expression used to define feature '{f.namespace}.{f.name}' is invalid: "
                                        + str(valid_exc),
                                        severity=DiagnosticSeverityGQL.Warning,
                                        code="701",
                                        codeDescription=None,
                                        relatedInformation=None,
                                    )
                                ],
                            )
                        )

        return diagnostics


CHALK_IMPORTER = ChalkImporter()


def import_all_python_files_from_dir(
    project_root: Path,
    check_ignores: bool = True,
    file_allowlist: Optional[List[Path]] = None,
) -> List[FailedImport]:
    project_root = project_root.absolute()

    cwd = os.getcwd()
    os.chdir(project_root)
    # If we don't import both of these, we get in trouble.
    repo_root = Path(project_root)
    resolved_root = repo_root.resolve()
    _logger.debug(f"REPO_ROOT: {resolved_root}")
    sys.path.insert(0, str(resolved_root))
    sys.path.insert(0, str(repo_root.parent.resolve()))
    # Due to the path modifications above, we might have already imported
    # some files under a different module name, and Python doesn't detect
    # duplicate inputs of the same filename under different module names.
    # We can manually detect this by building a set of all absolute
    # filepaths we imported, and then comparing filepaths against this
    # set before attempting to import the module again.
    already_imported_files = {
        Path(v.__file__).resolve(): k
        for (k, v) in sys.modules.copy().items()
        if hasattr(v, "__file__") and isinstance(v.__file__, str)
    }
    token = CHALK_IMPORT_FLAG.set(True)
    try:
        venv = os.environ.get("VIRTUAL_ENV")
        if file_allowlist is not None:
            repo_files = sorted(file_allowlist)
        else:
            venv_path = None if venv is None else Path(venv)
            ignore_config = get_default_combined_ignore_config(resolved_root) if check_ignores else None
            repo_files = sorted(
                list(_get_py_files_fast(resolved_root=resolved_root, venv_path=venv_path, ignore_config=ignore_config))
            )

        CHALK_IMPORTER.add_repo_files(repo_files)
        for filename in repo_files:
            # we want resolved_root in case repo_root contains a symlink
            if filename in already_imported_files:
                _logger.debug(
                    f"Skipping import of '{filename}' since it is already imported as module {already_imported_files[filename]}"
                )
                continue
            module_path = py_path_to_module(filename, resolved_root)
            if module_path.startswith(".eggs") or module_path.startswith("venv") or filename.name == "setup.py":
                continue
            try:
                start = time.perf_counter()
                importlib.import_module(module_path)
                end = time.perf_counter()
                _import_logger.debug(f"Imported '{module_path}' in {end-start} seconds")
            except Exception as e:
                if not LSPErrorBuilder.promote_exception(e):
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    assert ex_type is not None
                    assert ex_value is not None
                    assert ex_traceback is not None
                    CHALK_IMPORTER.add_error(ex_type, ex_value, ex_traceback, filename, module_path)
                    _logger.debug(f"Failed while importing {module_path}", exc_info=True)
            else:
                _logger.debug(f"Imported '{filename}' as module {module_path}")
                already_imported_files[filename] = module_path
    finally:
        CHALK_IMPORT_FLAG.reset(token)
        # Let's remove our added entries in sys.path so we don't pollute it
        sys.path.pop(0)
        sys.path.pop(0)
        # And let's go back to our original directory
        os.chdir(cwd)
    return CHALK_IMPORTER.get_failed_imports()


class _SupplementalState:
    def __init__(self):
        super().__init__()
        self._namespace_features: Dict[str, Dict[str, Feature[Any, Any]]] = {}

    def get_local_features_by_name(
        self,
        class_namespace: type[FeaturesProtocol],
    ) -> Dict[str, Feature[Any, Any]]:
        """
        Returns the features in the provided namespace.
        This function is cached by the namespace's string.
        """

        if class_namespace.namespace in self._namespace_features:
            return self._namespace_features[class_namespace.namespace]

        local_features_by_name: Dict[str, Feature[Any, Any]] = {}
        self._namespace_features[class_namespace.namespace] = local_features_by_name
        for f in class_namespace.features:
            local_features_by_name[f.name] = f

        return local_features_by_name


@dataclass(frozen=True)
class _ScalarExpr:
    dtype: pa.DataType


@dataclass(frozen=True)
class _NamespaceExpr:
    namespace: str


def _supplemental_validate_feature_in_namespace(
    state: _SupplementalState,
    *,
    class_namespace: type[FeaturesProtocol],
    feature_name: str,
    underscore: Underscore,
) -> Union[_ScalarExpr, _NamespaceExpr, None]:
    """
    Resolves references to features.
    """

    # This is a feature reference, in the current namespace.
    class_features = state.get_local_features_by_name(class_namespace)
    if feature_name not in class_features:
        # Complain about this definition!
        raise _UnderscoreValidationError(
            f"'{repr(underscore)}' is invalid because the feature class '{class_namespace.namespace}' does not have a feature named '{underscore._chalk__attr}'"
        )

    feature_definition = class_features[feature_name]
    if feature_definition.is_pseudofeature:
        return None
    if feature_definition.is_windowed:
        return None
    if feature_definition.is_scalar:
        return _ScalarExpr(dtype=feature_definition.converter.pyarrow_dtype)
    if feature_definition.is_has_one:
        foreign_feature_namespace = feature_definition.typ.as_features_cls()
        if foreign_feature_namespace is not None:
            return _NamespaceExpr(namespace=foreign_feature_namespace.namespace)


def _supplemental_validate_underscore_expression(
    state: _SupplementalState,
    *,
    class_namespace: type[FeaturesProtocol],
    underscore: Underscore,
) -> Union[_ScalarExpr, _NamespaceExpr, None]:
    """
    Validates that the provided `underscore` definition is legal when evaluated in `class_namespace`.
    Currently, does not perform type-checking; just checks that all names are in scope.

    If the underscore expression is invalid, raises a `_UnderscoreValidationError` with a message.
    The caller is responsible for converting this exception into a diagnostic message.
    """

    if isinstance(underscore, UnderscoreAttr) and isinstance(underscore._chalk__parent, UnderscoreRoot):
        if underscore._chalk__attr in ("chalk_window", "chalk_now"):
            # This is a special case, which can be skipped in validation.
            return _ScalarExpr(dtype=pa.timestamp("us", tz="UTC"))

        return _supplemental_validate_feature_in_namespace(
            state=state,
            class_namespace=class_namespace,
            feature_name=underscore._chalk__attr,
            underscore=underscore,
        )

    if isinstance(underscore, UnderscoreAttr):
        parent_result = _supplemental_validate_underscore_expression(
            state=state,
            class_namespace=class_namespace,
            underscore=underscore._chalk__parent,
        )

        if isinstance(parent_result, _ScalarExpr):
            if not pa.types.is_struct(parent_result.dtype):
                raise _UnderscoreValidationError(
                    f"the input '{underscore!r}' is a scalar value, so a feature called '{underscore._chalk__attr}' cannot be extracted from it"
                )
            st = cast(pa.StructType, parent_result.dtype)
            field = next((field for field in st if field.name == underscore._chalk__attr), None)
            if field is not None:
                return _ScalarExpr(dtype=field.type)
            raise _UnderscoreValidationError(
                f"could not find the struct field '{underscore._chalk__attr}' among the available fields [{', '.join(f.name for f in st)}]"
            )

        if isinstance(parent_result, _NamespaceExpr):
            if parent_result.namespace not in FeatureSetBase.registry:
                return None

            parent_class_namespace = FeatureSetBase.registry[parent_result.namespace]
            return _supplemental_validate_feature_in_namespace(
                state=state,
                class_namespace=parent_class_namespace,
                feature_name=underscore._chalk__attr,
                underscore=underscore,
            )

        return None

    if isinstance(underscore, UnderscoreFunction):
        if (underscore._chalk__function_name in ("max_by", "min_by") and len(underscore._chalk__args) == 2) or (
            underscore._chalk__function_name in ("max_by_n", "min_by_n") and len(underscore._chalk__args) == 3
        ):
            _supplemental_validate_underscore_expression(
                state=state,
                class_namespace=class_namespace,
                underscore=underscore._chalk__args[0],
            )
            # TODO: second arg is on a different namespace
        else:
            for arg in underscore._chalk__args:
                expr = _supplemental_validate_underscore_expression(
                    state=state,
                    class_namespace=class_namespace,
                    underscore=arg,
                )
                if isinstance(expr, _NamespaceExpr):
                    raise _UnderscoreValidationError(
                        f"the input '{arg!r}' is a feature namespace '{expr.namespace}' which cannot be used as a scalar value"
                    )


def _get_printable_name(typ: Any) -> str:
    try:
        return typ.__name__  # Union types don't have __name__, but have good string representations
    except:
        return str(typ)
