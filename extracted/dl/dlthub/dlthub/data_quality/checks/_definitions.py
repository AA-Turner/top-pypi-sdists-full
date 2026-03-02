from __future__ import annotations

import functools
from collections.abc import Callable, Sequence
from typing import Any, TypeVar, overload

from dlt.common.typing import ParamSpec

import dlt
from dlt.extract import DltResource, DltSource
from dlt.extract.decorators import (
    DltSourceFactoryWrapper,
    ResourceFactory,
    TResourceFunParams,
    TDltResourceImpl,
    SourceFactory,
    TDltSourceImpl,
    TSourceFunParams,
)
from dlt.common.schema import TColumnSchema, utils as schema_utils

from dlthub.data_quality.checks._base import LazyCheck
from dlthub.data_quality.checks import checks
from dlthub.data_quality.typing import (
    CHECKS_HINT_KEY,
    TSourceChecksHints,
    TCheckHint,
)


P = ParamSpec("P")
R = TypeVar("R")
TDltSourceOrResource = TypeVar("TDltSourceOrResource", DltSource, DltResource)


def get_schema_check_hints(schema: dlt.Schema) -> TSourceChecksHints:
    """Get all checks hints stored on the schema.

    This excludes internal dlt tables and columns, and checks defined on
    incomplete* tables and columns.

    *An incomplete table or column is typically the result of hints defined
    via `@dlt.resource` but not having received data yet.
    """
    checks_hints: TSourceChecksHints = {
        "dataset": [],
        "tables": {},
    }

    if schema.settings.get(CHECKS_HINT_KEY):
        # TODO add `CHECKS_HINT_KEY` to `dlt.Schema.settings` typing in `dlt-hub/dlt`
        checks_hints["dataset"] = schema.settings[CHECKS_HINT_KEY]["dataset"]  # type: ignore[literal-required]

    for table_schema in schema.data_tables(seen_data_only=True):
        table_name = table_schema["name"]
        if table_schema.get(CHECKS_HINT_KEY) is None:
            continue

        checks_hints["tables"][table_name] = table_schema[CHECKS_HINT_KEY]  # type: ignore[literal-required]

    return checks_hints


def create_check_hints_from_schema(schema: dlt.Schema) -> TSourceChecksHints:
    checks_hints: TSourceChecksHints = {
        "dataset": [],
        "tables": {},
    }

    for table_schema in schema.data_tables(seen_data_only=True):
        table_name = table_schema["name"]
        for column_name, column_schema in table_schema["columns"].items():
            if schema_utils.is_dlt_table_or_column(column_name, schema._dlt_tables_prefix):
                continue

            if table_name not in checks_hints["tables"]:
                checks_hints["tables"][table_name] = []

            checks_hints["tables"][table_name].extend(
                _column_hints_to_check_hints(
                    column_name,
                    column_schema,
                )
            )

    return checks_hints


def _column_hints_to_check_hints(
    column_name: str, column_schema: TColumnSchema
) -> list[TCheckHint]:
    check_hints: list[TCheckHint] = []
    if column_schema.get("nullable") is False:
        check_hints.append(
            TCheckHint(
                name="is_not_null",
                args={"column": column_name},
            )
        )

    if column_schema.get("unique") is True:
        check_hints.append(
            TCheckHint(
                name="is_unique",
                args={"column": column_name},
            )
        )

    if column_schema.get("primary_key") is True:
        check_hints.append(
            TCheckHint(
                name="is_primary_key",
                args={"columns": [column_name]},
            )
        )

    if column_schema.get("row_key") is True:
        check_hints.append(
            TCheckHint(
                name="is_unique",
                args={"column": column_name},
            )
        )

    return check_hints


def _check_def_to_hints(check: LazyCheck) -> TCheckHint:
    return TCheckHint(
        name=check.name,
        args=dict(check.arguments),
    )


def _check_hints_to_def(check_hints: TCheckHint) -> LazyCheck:
    check_def: LazyCheck = getattr(checks, check_hints["name"])(**check_hints["args"])
    return check_def


@overload
def with_checks(
    *checks: LazyCheck,
) -> Callable[[R], R]:
    # decorator pattern
    pass


@overload
def with_checks(
    source_or_resource: SourceFactory[TSourceFunParams, TDltSourceImpl],
    *checks: LazyCheck,
) -> SourceFactory[TSourceFunParams, TDltSourceImpl]:
    # adapter pattern for source factory (@dlt.source before call)
    pass


@overload
def with_checks(
    source_or_resource: ResourceFactory[TResourceFunParams, TDltResourceImpl],
    *checks: LazyCheck,
) -> ResourceFactory[TResourceFunParams, TDltResourceImpl]:
    # adapter pattern for resource factory (@dlt.resource before call)
    pass


@overload
def with_checks(
    source_or_resource: TDltSourceOrResource,
    *checks: LazyCheck,
) -> TDltSourceOrResource:
    # adapter pattern for instantiated source or resource
    pass


def with_checks(
    source_or_resource: Any = None,
    *checks: LazyCheck,
) -> Any:
    """Register checks on the source, resource, transformer or transformation."""

    # this function receives arguments from all overloads. we support both decorator and adapter
    # use so the first argument can be a check (decorate) - in this case we return a wrapper
    # that receives decorated object
    if isinstance(source_or_resource, LazyCheck):
        return functools.partial(_with_checks, checks=(source_or_resource,) + checks)

    if source_or_resource is None and not checks:
        raise ValueError(
            "`with_checks()` requires at least one check definition or a source/resource "
            "argument."
        )

    # if first argument is not a check, we have adapter pattern where we assume source or resource
    return _with_checks(source_or_resource=source_or_resource, checks=checks)


def _check_defs_to_source_hints(checks: Sequence[LazyCheck]) -> TSourceChecksHints:
    return TSourceChecksHints(
        dataset=[_check_def_to_hints(check) for check in checks],
        tables={},
    )


def _with_checks(
    source_or_resource: Any,
    checks: Sequence[LazyCheck],
) -> Any:
    if isinstance(source_or_resource, DltSource):
        source_check_hints = _check_defs_to_source_hints(checks)
        source_or_resource.schema._settings[CHECKS_HINT_KEY] = source_check_hints  # type: ignore[literal-required]

    elif isinstance(source_or_resource, DltSourceFactoryWrapper):
        source_check_hints = _check_defs_to_source_hints(checks)

        def _postprocess(source: DltSource) -> DltSource:
            source.schema._settings[CHECKS_HINT_KEY] = source_check_hints  # type: ignore[literal-required]
            return source

        source_or_resource.add_postprocessor(_postprocess)

    elif isinstance(source_or_resource, DltResource):
        # resolving checks outside allows to fail early
        resource_check_hints = [_check_def_to_hints(check) for check in checks]
        # NOTE could store checks hints under `additional_table_hints`
        # which would prevent rewriting the whole `_hints` and avoid `dlt` typing complaining
        source_or_resource._set_hints(
            source_or_resource._hints.copy() | {CHECKS_HINT_KEY: resource_check_hints}  # type: ignore[arg-type]
        )

    else:
        raise ValueError(
            f"`with_checks()` is applied on unsupported object type `{type(source_or_resource)}`"
        )

    return source_or_resource
