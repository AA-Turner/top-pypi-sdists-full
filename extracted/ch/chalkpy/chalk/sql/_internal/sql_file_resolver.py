from __future__ import annotations

import contextlib
import dataclasses
import inspect
import json
import os
import re
from datetime import timedelta
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

import yaml
from typing_extensions import ParamSpec, TypeAlias
from yaml.scanner import ScannerError

from chalk import Environments, OfflineResolver, OnlineResolver, Tags
from chalk._lsp.error_builder import SQLFileResolverErrorBuilder
from chalk.features import DataFrame, Feature, FeatureNotFoundException, Features, FeatureSetBase
from chalk.features.namespace_context import build_namespaced_name
from chalk.features.namespace_context import namespace as namespace_ctx
from chalk.features.pseudofeatures import Now
from chalk.features.resolver import Cron, ResolverArgErrorHandler, StreamResolver
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.spanner import SpannerSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteSourceImpl
from chalk.sql._internal.sql_settings import SQLResolverSettings
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.sql.finalized_query import Finalizer
from chalk.streams import KafkaSource, get_resolver_error_builder
from chalk.streams.base import StreamSource
from chalk.streams.types import StreamResolverSignature
from chalk.utils import MachineType
from chalk.utils.collections import get_unique_item, get_unique_item_if_exists
from chalk.utils.duration import CronTab, Duration, parse_chalk_duration, timedelta_to_duration
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.string import to_snake_case

P = ParamSpec("P")
T = TypeVar("T")

FeatureReference: TypeAlias = Union[str, Any]

if TYPE_CHECKING:
    import sqlglot.expressions
    from pydantic import BaseModel, ValidationError

    from chalk.sql import BaseSQLSourceProtocol, SQLSourceGroup

    def validator(*args: str, pre: bool = ...) -> Callable[[Callable[P, T]], Callable[P, T]]:
        ...

else:
    try:
        from pydantic.v1 import BaseModel, ValidationError, validator
    except ImportError:
        from pydantic import BaseModel, ValidationError, validator

_SOURCES: Mapping[str, Union[Type[BaseSQLSource], Type[StreamSource]]] = {
    "snowflake": SnowflakeSourceImpl,
    "postgres": PostgreSQLSourceImpl,
    "postgresql": PostgreSQLSourceImpl,
    "mysql": MySQLSourceImpl,
    "bigquery": BigQuerySourceImpl,
    "cloudsql": CloudSQLSourceImpl,
    "redshift": RedshiftSourceImpl,
    "sqlite": SQLiteSourceImpl,
    "kafka": KafkaSource,
    "spanner": SpannerSourceImpl,
}

_SQLGLOT_DIALECTS = frozenset(
    (
        "snowflake",
        "postgres",
        "mysql",
        "bigquery",
        "redshift",
        "sqlite",
        "databricks",
    )
)
"""These dialects are used if a "kind" of source is listed, rather than a specific source."""

_RESOLVER_TYPES = {
    "offline": OfflineResolver,
    "batch": OfflineResolver,
    "online": OnlineResolver,
    "realtime": OnlineResolver,
    "stream": StreamResolver,
    "streaming": StreamResolver,
}

CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX = ".chalk.sql"


class IncrementalSettingsSQLFileResolver(BaseModel):
    incremental_column: Optional[str]

    lookback_period: Optional[Duration]

    mode: Literal["row", "group", "parameter"] = "row"

    incremental_timestamp: Optional[Literal["feature_time", "resolver_execution_time"]] = "feature_time"

    @validator("lookback_period")
    @classmethod
    def validate_lookback_period(cls, value: Optional[str]):
        if value is None:
            return None
        if isinstance(value, timedelta):
            return value
        parse_chalk_duration(value)
        return value

    @validator("mode")
    @classmethod
    def validate_mode(cls, mode: Literal["row", "group", "parameter"], values: Dict[str, Any]):
        if mode in ["row", "group"] and not values["incremental_column"]:
            raise ValueError("'incremental_column' must be set if mode is 'row' or 'group'.")
        return mode


class CommentDict(BaseModel):
    total: Optional[bool]
    source: Optional[str]
    resolves: Optional[str]
    namespace: Optional[str]
    incremental: Optional[IncrementalSettingsSQLFileResolver]
    tags: Optional[List[str]]
    environment: Optional[List[str]]
    count: Optional[Literal[1, "one", "one_or_none", "all"]]
    cron: Optional[Any]
    machine_type: Optional[str]
    owner: Optional[str]
    type: Optional[str]
    timeout: Optional[str]
    fields: Optional[Dict[str, str]]
    unique_on: Optional[List[str]]
    partitioned_by: Optional[List[str]]

    @validator("tags", "environment", "unique_on", "partitioned_by", pre=True)
    @classmethod
    def validate_list_inputs(cls, value: Union[str, List[str], None]):
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            return [value]
        raise ValueError(f"Value {value} must be a string or a list of strings.")

    @validator("cron", pre=True)
    @classmethod
    def validate_cron_input(cls, value: Any):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, timedelta):
            return value
        if isinstance(value, Cron):
            return value
        raise ValueError(f"Value {value} must be a string or a Cron")

    @validator("timeout")
    @classmethod
    def validate_timedelta(cls, string: Optional[str]):
        if string is None:
            return None
        parse_chalk_duration(string)
        return string

    @validator("type")
    @classmethod
    def validate_type(cls, resolver_type: str | None):
        if resolver_type is None:
            return None
        if resolver_type not in _RESOLVER_TYPES:
            raise ValueError(
                (
                    f"Resolver type '{resolver_type}' not supported. "
                    f"'online', 'offline' and 'streaming' are supported options"
                )
            )
        return resolver_type


@dataclasses.dataclass(frozen=True)
class ResolverError:
    """Generic class for returning errors at any point during resolution process"""

    display: str
    path: str
    parameter: Optional[str]


@dataclasses.dataclass(frozen=True)
class ResolverResult:
    """Chief return class with resolver we actually use"""

    resolver: Optional[Union[OnlineResolver, OfflineResolver, StreamResolver]]
    errors: List[ResolverError]
    db: Optional[Union[BaseSQLSource, StreamSource, SQLSourceGroup]]
    fields: Optional[Dict[str, str]]
    args: Optional[Dict[str, str]]
    data_lineage: Optional[Dict[str, Dict[str, Dict[str, List[str]]]]] = None


@dataclasses.dataclass(frozen=True)
class SQLStringResult:
    """Class for getting the sql string from the file"""

    path: str
    sql_string: Optional[str]
    error: Optional[ResolverError]
    override_comment_dict: Optional[CommentDict] = None
    override_name: Optional[str] = None
    autogenerated: bool = False

    def __post_init__(self):
        # Validation: if autogenerated is True, override_name must not be None
        if self.autogenerated and self.override_name is None:
            raise ValueError("override_name must be non-None if autogenerated is True.")

    @classmethod
    def fail(cls, display_error: str, path: str) -> "SQLStringResult":
        return cls(
            path=path,
            sql_string=None,
            error=ResolverError(display=display_error, path=path, parameter=None),
        )


@dataclasses.dataclass(frozen=True)
class GlotResult:
    """Class for editing the sql string, and using sqlglot on sql string"""

    sql_string: str
    glot: Optional[Union[sqlglot.expressions.Select, sqlglot.expressions.Union]]
    args: Dict[str, str]
    default_args: List[Union[Optional[str], ellipsis]]
    comment_dict: Optional[CommentDict]
    docstring: Optional[str]
    errors: List[ResolverError]
    source: Union[BaseSQLSource, StreamSource, SQLSourceGroup, None]


@dataclasses.dataclass(frozen=True)
class ParseResult:
    """Class for important info gathered from glot"""

    sql_string: str
    comment_dict: CommentDict
    fields: Dict[str, str]
    namespace: str
    source: Union[BaseSQLSource, StreamSource, SQLSourceGroup, None]
    docstring: Optional[str]
    errors: List[ResolverError]

    # data_lineage is stored as a map { data_source: { table: { column: feature } } }
    data_lineage: Optional[Dict[str, Dict[str, Dict[str, List[str]]]]] = None


_filepath_to_sql_string: dict[str, str] = {}
"""Mapping from filepath to sql string. Used to skip reimporting the same sql file if the content is identical to what was already imported
If the content is different, then we'll import it again, but we may error later when attempting to add the resolver to the registry if we don't
allow overrides and we're not in a notebook.
"""


def get_sql_file_resolvers(
    *,
    sql_file_resolve_location: Path,
    sources: Sequence[BaseSQLSource | SQLSourceGroup],
    has_import_errors: bool,
) -> Iterable[ResolverResult]:
    """Iterate through all `.chalk.sql` filepaths, gather the sql strings, and get a resolver hopefully for each."""
    for dp, dn, fn in os.walk(os.path.expanduser(sql_file_resolve_location)):
        del dn  # unused
        for f in fn:
            filepath = os.path.join(dp, f)
            if not filepath.endswith(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX):
                continue
                # Already imported this file. Skipping it, assuming it did not change since the last time we imported it
            sql_string_result = _get_sql_string(filepath)
            existing_sql_string = _filepath_to_sql_string.get(filepath)
            if sql_string_result.sql_string is not None:
                if existing_sql_string is not None and existing_sql_string == sql_string_result.sql_string:
                    # The sql file is identical to what was already imported. skip it
                    continue
                _filepath_to_sql_string[filepath] = sql_string_result.sql_string
            yield get_sql_file_resolver(sources, sql_string_result, has_import_errors)
    for sql_string_result in _GENERATED_SQL_FILE_RESOLVER_REGISTRY.get_generated_sql_file_resolvers():
        yield get_sql_file_resolver(sources, sql_string_result, has_import_errors)


def get_sql_file_resolvers_from_paths(
    *,
    sources: Sequence[BaseSQLSource | SQLSourceGroup],
    paths: List[str],
    has_import_errors: bool,
) -> Iterable[ResolverResult]:
    for p in paths:
        sql_string_result = _get_sql_string(path=p)
        existing_sql_string = _filepath_to_sql_string.get(p)
        if sql_string_result.sql_string is not None:
            if existing_sql_string is not None and existing_sql_string == sql_string_result.sql_string:
                # The sql file is identical to what was already imported. skip it
                continue
            _filepath_to_sql_string[p] = sql_string_result.sql_string
        yield get_sql_file_resolver(
            sources=sources,
            sql_string_result=sql_string_result,
            has_import_errors=has_import_errors,
        )
    for sql_string_result in _GENERATED_SQL_FILE_RESOLVER_REGISTRY.get_generated_sql_file_resolvers():
        yield get_sql_file_resolver(sources, sql_string_result, has_import_errors)


def get_sql_file_resolver(
    sources: Iterable[BaseSQLSource | SQLSourceGroup],
    sql_string_result: SQLStringResult,
    has_import_errors: bool = False,
) -> ResolverResult:
    from chalk.sql import SQLSourceGroup

    assert sql_string_result.sql_string is not None, f"SQL string from path {sql_string_result.path} should not be None"
    error_builder = SQLFileResolverErrorBuilder(
        uri=sql_string_result.path, sql_string=sql_string_result.sql_string, has_import_errors=has_import_errors
    )

    """Parse the sql strings and get a ResolverResult from each"""
    if sql_string_result.error:
        return ResolverResult(
            resolver=None,
            errors=[sql_string_result.error],
            db=None,
            fields=None,
            args=None,
        )
    path = sql_string_result.path

    errors: List[ResolverError] = []
    glot_result = _get_sql_glot(
        sql_string=sql_string_result.sql_string,
        path=path,
        sources=sources,
        error_builder=error_builder,
        override_comment_dict=sql_string_result.override_comment_dict,
    )
    if glot_result.errors:
        return ResolverResult(
            resolver=None,
            errors=glot_result.errors,
            db=None,
            fields=None,
            args=None,
        )

    parsed = _parse_glot(
        glot_result=glot_result,
        path=path,
        error_builder=error_builder,
    )
    if parsed.errors:
        return ResolverResult(
            resolver=None,
            errors=parsed.errors,
            db=parsed.source,
            fields=None,
            args=None,
        )
    with (
        namespace_ctx(parsed.comment_dict.namespace)
        if parsed.comment_dict and parsed.comment_dict.namespace
        else contextlib.nullcontext()
    ):
        # validate inputs and outputs as real features in graph
        inputs: List[Feature] = []
        for arg in glot_result.args.values():
            try:
                inputs.append(Feature.from_root_fqn(build_namespaced_name(name=arg)))
            except FeatureNotFoundException:  # other exceptions will be caught eventually
                message = f"SQL file resolver references an input feature '{arg}' which does not exist."
                if arg in FeatureSetBase.registry:
                    message += f" It appears '{arg}' is a feature class, not a feature."
                try:
                    error_builder.add_diagnostic_with_spellcheck(
                        spellcheck_item=arg,
                        spellcheck_candidates=[
                            feature.fqn
                            for feature in FeatureSetBase.registry[
                                build_namespaced_name(name=parsed.namespace)
                            ].features
                        ],
                        message=message,
                        code="152",
                        label="input feature not recognized",
                        range=error_builder.variable_range_by_name(arg),
                    )
                except Exception:
                    # it's possible the graph is incomplete due to other import errors and we cannot find spellcheck candidates
                    # in this case, a simple error will do
                    error_builder.add_diagnostic(
                        message=message,
                        code="152",
                        label="input feature not recognized",
                        range=error_builder.variable_range_by_name(arg),
                    )
                errors.append(
                    ResolverError(
                        display=message,
                        path=path,
                        parameter=arg,
                    )
                )
        outputs: List[Feature] = []
        query_fields: Dict[str, str] = {}
        for variable, output in parsed.fields.items():
            message = f"SQL file resolver references an output feature '{output}' which does not exist. "
            if output.endswith("*"):
                features = FeatureSetBase.registry[build_namespaced_name(name=parsed.namespace)].features
                for feature in features:
                    if (
                        feature.is_scalar
                        and not feature.is_autogenerated
                        and not feature.is_pseudofeature
                        and not feature.is_windowed
                    ):
                        outputs.append(feature)
                continue

            unrecognized_output = False
            try:
                feature = Feature.from_root_fqn(output)
                outputs.append(feature)
                query_fields[variable] = output
            except FeatureNotFoundException:
                # there's only one way to have a recognized output here, if the output is in the comment dict 'fields'
                unrecognized_output = True
                if parsed.comment_dict.fields is not None:
                    split = output.split(".", 1)
                    if len(split) > 1:
                        namespace = split[0]
                        output_name = split[1]
                        if output_name in parsed.comment_dict.fields:
                            field = parsed.comment_dict.fields.get(output_name)
                            output = f"{namespace}.{field}"
                            try:
                                feature = Feature.from_root_fqn(build_namespaced_name(name=output))
                                outputs.append(feature)
                                query_fields[output_name] = output
                                unrecognized_output = False
                            except:
                                pass
            except Exception as e:
                # it's possible the graph is incomplete due to other import errors and we cannot even use Feature.from_root_fqn without
                # throwing an unhandled error. In this case, we don't addi a diagnostic because we are confident the error
                # will surface later with a better stack
                errors.append(
                    ResolverError(
                        display=f"{message}: {e}",
                        path=path,
                        parameter=output,
                    )
                )
                continue

            if unrecognized_output:
                value = output.split(".", 1)[1] if "." in output else output
                assert glot_result.glot is not None, f"Failed to parse {glot_result.sql_string}"
                try:
                    error_builder.add_diagnostic_with_spellcheck(
                        spellcheck_item=output,
                        spellcheck_candidates=[
                            feature.fqn
                            for feature in FeatureSetBase.registry[
                                build_namespaced_name(name=parsed.namespace)
                            ].features
                        ],
                        message=message,
                        code="153",
                        label="output feature not recognized",
                        range=error_builder.value_range_by_name(glot_result.glot, value),
                    )
                except Exception:
                    # it's possible the graph is incomplete due to other import errors and we cannot find spellcheck candidates
                    # in this case, we don't add a diagnostic because we are confident the error will surface later with a better stack
                    pass
                errors.append(
                    ResolverError(
                        display=message,
                        path=path,
                        parameter=output,
                    )
                )
        if errors:
            return ResolverResult(resolver=None, errors=errors, db=parsed.source, fields=None, args=glot_result.args)

        if len(outputs) == 0:
            message = (
                "SQL file resolver has no detected outputs. Make sure that all select outputs are aliased to features "
                "defined within the feature set referenced by the `resolves` parameter."
            )
            error_builder.add_diagnostic(
                message=message,
                code="154",
                label="no outputs detected",
                range=error_builder.sql_range(),
            )
            errors.append(ResolverError(display=message, path=path, parameter=None))

        if parsed.comment_dict.unique_on is not None:
            unique_on = _validate_feature_strings_in_comments(
                feature_strings=parsed.comment_dict.unique_on,
                error_builder=error_builder,
                namespace=parsed.namespace,
                path=path,
                errors=errors,
                outputs=outputs,
                arg_name="unique_on",
            )
        else:
            unique_on = None
        if parsed.comment_dict.partitioned_by is not None:
            partitioned_by = _validate_feature_strings_in_comments(
                feature_strings=parsed.comment_dict.partitioned_by,
                error_builder=error_builder,
                namespace=parsed.namespace,
                path=path,
                errors=errors,
                outputs=outputs,
                arg_name="partitioned_by",
            )
        else:
            partitioned_by = None
        resolver_type_str = parsed.comment_dict.type if parsed.comment_dict.type else "online"
        resolver_type = _RESOLVER_TYPES[resolver_type_str]

        if resolver_type == StreamResolver:
            return _get_stream_resolver(path, glot_result, parsed, outputs, error_builder)

        incremental_dict = parsed.comment_dict.incremental.dict() if parsed.comment_dict.incremental else None
        finalizer = parse_finalizer(parsed.comment_dict.count)
        source = parsed.source

        if not isinstance(source, (BaseSQLSource, SQLSourceGroup)):
            raise ValueError(f"Datasource '{source}' is not configured. Is the driver installed?")

        # function for online resolver to process
        def fn(
            *input_values: Any,
            database: BaseSQLSource | SQLSourceGroup = source,
            sql_query: str = parsed.sql_string,
            field_dict: Dict[str, str] = query_fields,
            args_dict: Dict[str, str] = glot_result.args,
            incremental: Optional[Dict[str, Any]] = incremental_dict,
        ):
            arg_dict = {arg: input_value for input_value, arg in zip(input_values, args_dict.keys())}
            func = database.query_string(
                query=sql_query,
                fields=field_dict,
                args=arg_dict,
            )
            if incremental:
                func = func.incremental(**incremental)
            elif finalizer == Finalizer.ONE:
                func = func.one()
            elif finalizer == Finalizer.ONE_OR_NONE:
                func = func.one_or_none()
            elif finalizer == Finalizer.ALL:
                func = func.all()
            return func

        if errors:
            return ResolverResult(
                resolver=None,
                errors=errors,
                db=parsed.source,
                fields=parsed.fields,
                args=glot_result.args,
            )
        if finalizer is None:
            # If the root ns of the inputs is the same as what is being resolved, then it is always return one
            input_root_namespace = get_unique_item_if_exists(x.root_namespace for x in inputs if x.fqn != Now.fqn)
            output_root_namespace = get_unique_item(x.root_namespace for x in outputs)
            if input_root_namespace is not None and input_root_namespace == output_root_namespace:
                finalizer = Finalizer.ONE

        if finalizer == Finalizer.ONE or finalizer == Finalizer.ONE_OR_NONE:
            output = Features[tuple(outputs)]
        else:
            output = Features[DataFrame[tuple(outputs)]]
        if incremental_dict is None:
            incremental_settings = None
        else:
            incremental_mode = incremental_dict.get("mode", "row")
            if incremental_mode not in ["row", "group", "parameter"]:
                raise ValueError(f"Invalid incremental mode: {incremental_mode}")
            if incremental_dict.get("lookback_period") is not None:
                lookback_period = parse_chalk_duration(incremental_dict["lookback_period"])
            else:
                lookback_period = None
            incremental_timestamp = incremental_dict.get("incremental_timestamp", "feature_time")
            if incremental_timestamp not in ["feature_time", "resolver_execution_time"]:
                raise ValueError(f"Invalid incremental timestamp: {incremental_timestamp}")
            incremental_settings = IncrementalSettings(
                mode=incremental_mode,
                incremental_column=incremental_dict.get("incremental_column"),
                lookback_period=lookback_period,
                incremental_timestamp=incremental_timestamp,
            )

        default_args: List[Optional[ResolverArgErrorHandler]] = [
            None if default_value is ... else ResolverArgErrorHandler(default_value)
            for default_value in glot_result.default_args
        ]

        filename = os.path.basename(path)
        # attempt to instantiate the resolver
        try:
            if resolver_type not in (OnlineResolver, OfflineResolver):
                raise ValueError(f"Resolver type '{resolver_type}' is not supported for .chalk.sql resolvers")
            if not isinstance(parsed.source, (BaseSQLSource, SQLSourceGroup)):
                raise ValueError(f"Datasource '{parsed.source}' is not configured. Is the driver installed")
            if sql_string_result.autogenerated:
                """Autogenerated resolvers are expected to have a name passed in through make_sql_file_resolver"""
                assert (
                    sql_string_result.override_name is not None
                ), "override_name must be non-None if autogenerated is True."
                fqn = sql_string_result.override_name
            else:
                """Non-autogenerated resolvers will have a name derived from the filename"""
                fqn = filename.replace(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX, "")

            resolver = resolver_type(
                filename=path,
                function_definition=sql_string_result.sql_string,
                fqn=fqn,
                doc=parsed.docstring,
                inputs=inputs,
                output=output,
                fn=fn,
                environment=parsed.comment_dict.environment,
                tags=parsed.comment_dict.tags,
                cron=parsed.comment_dict.cron,
                machine_type=parsed.comment_dict.machine_type,
                when=None,
                state=None,
                default_args=default_args,
                owner=parsed.comment_dict.owner,
                timeout=parsed.comment_dict.timeout,
                is_sql_file_resolver=True,
                data_sources=[parsed.source],
                source_line=None,
                lsp_builder=get_resolver_error_builder(fn),
                static=False,
                parse=None,
                resource_hint=None,
                total=True if parsed.comment_dict.total else False,
                autogenerated=sql_string_result.autogenerated,
                unique_on=unique_on,
                partitioned_by=partitioned_by,
                data_lineage=parsed.data_lineage,
                sql_settings=SQLResolverSettings(
                    finalizer=finalizer if finalizer is not None else Finalizer.ALL,
                    fields_root_fqn=query_fields,
                    incremental_settings=incremental_settings,
                ),
            )
        except Exception as e:
            raise e
            message = f"SQL file resolver '{filename}'  could not be instantiated, {e}"
            error_builder.add_diagnostic(
                message=message,
                code="155",
                label="resolver instantiation failed",
                range=error_builder.full_range(),
            )
            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=None,
                )
            )
            return ResolverResult(
                resolver=None, errors=errors, db=parsed.source, fields=parsed.fields, args=glot_result.args
            )

        return ResolverResult(
            resolver=resolver,
            errors=errors,
            db=parsed.source,
            fields=parsed.fields,
            args=glot_result.args,
            data_lineage=parsed.data_lineage,
        )


def _get_sql_string(path: str) -> SQLStringResult:
    """Attempt to get a sql string from a filepath and gracefully exit if unable to"""

    if not path.endswith(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX):
        return SQLStringResult.fail(display_error=f"sql resolver file '{path}' must end in '.chalk.sql'", path=path)
    sql_string = None
    if os.path.isfile(path):
        with open(path) as f:
            sql_string = f.read()
    else:
        frame = inspect.currentframe()
        assert frame is not None, "could not inspect current frame"
        caller_frame = frame.f_back
        assert caller_frame is not None, "could not inspect caller frame"
        caller_filename = inspect.getsourcefile(caller_frame)
        assert caller_filename is not None, "could not find caller filename"
        dir_path = os.path.dirname(os.path.realpath(caller_filename))
        if isinstance(path, bytes):
            path = path.decode("utf-8")
        relative_path = os.path.join(dir_path, path)
        if os.path.isfile(relative_path):
            with open(relative_path) as f:
                sql_string = f.read()
    if sql_string is None:
        return SQLStringResult.fail(display_error=f"Cannot find file '{path}'", path=path)
    return SQLStringResult(path=path, sql_string=sql_string, error=None)


def _get_data_lineage(sql: str) -> Dict[str, Dict[str, List[str]]]:
    try:
        import sqlglot
        from sqlglot import exp
        from sqlglot.optimizer.scope import build_scope
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    try:
        # Parse the SQL into an abstract syntax tree (AST)
        ast = sqlglot.parse_one(sql)
        # TODO: @melrchen parse CTE's correctly
        for expression in ast.expressions:
            if isinstance(expression, exp.With):
                return {}

        root = build_scope(ast)
        #  assuming one source for simple query
        if not root or len(root.sources.keys()) > 1:
            return {}
        table = list(root.sources.keys())[0]

        lineage: Dict[str, Dict[str, List[str]]] = {table: {}}

        # get feature and column names from the query
        def process_select(select_expr: sqlglot.Expression):
            for expr in select_expr.expressions:
                if isinstance(expr, exp.Alias):
                    output_column = expr.alias
                    input_columns: List[str] = extract_columns(expr.this)
                elif isinstance(expr, exp.Column):
                    output_column = expr.name
                    input_columns: List[str] = [expr.name]
                elif isinstance(expr, exp.Binary):
                    output_column = expr.sql()  # For columns like `name + size`
                    input_columns = extract_columns(expr)
                else:
                    continue  # Skip expressions that don't contribute to lineage

                lineage[table][output_column] = input_columns

        # Extract columns from expressions
        def extract_columns(expr: sqlglot.Expression) -> List[str]:
            columns = []
            if isinstance(expr, exp.Column):
                columns.append(expr.name)
            elif isinstance(expr, exp.Func):
                for col in expr.find_all(exp.Column):
                    columns.append(col.name)
            elif isinstance(expr, exp.Binary):
                columns.extend(extract_columns(expr.left))
                columns.extend(extract_columns(expr.right))
            return columns

        # Process the main SELECT expression
        for select_expr in ast.find_all(exp.Select):
            process_select(select_expr)

        return lineage
    except Exception:
        return {}


def _get_sql_glot(
    sql_string: str,
    path: str,
    sources: Iterable[BaseSQLSource | SQLSourceGroup],
    error_builder: SQLFileResolverErrorBuilder,
    override_comment_dict: Optional[CommentDict] = None,
) -> GlotResult:
    """Get sqlglot from sql string and gracefully exit if unable to"""
    try:
        import sqlglot
        import sqlglot.errors
        import sqlglot.expressions
        import sqlglot.optimizer.scope
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    args = {}  # sql string -> input feature string

    # In order to ensure that the variables are ordered deterministically, we use a `dict`
    # instead of a `set`, since `dict` ensures iteration order matches insertion order.
    variables = {key: None for key in re.findall("\\${.*?\\}", sql_string)}
    errors: List[ResolverError] = []
    default_args: List[Union[Optional[str], ellipsis]] = []
    # replace ?{variable_name} with :variable_name for sqlalchemy, and keep track of input args necessary
    for variable_pattern in variables:
        has_default_arg = False
        variable = variable_pattern[2:-1]  # cut off ${ and }
        for split_var in ("|", " or "):  # default argument
            # TODO cannot parse something like {Transaction.category or "Waffles or Pancakes"} yet
            if split_var in variable:
                split = variable.split(split_var)
                if len(split) != 2:
                    message = (
                        f"If character '|' is used, both variable name and default value must be "
                        f"specified in '({variable})' like '?{{variable_name | \"default_value\"}}"
                    )
                    error_builder.add_diagnostic(
                        message=message,
                        code="140",
                        label="invalid variable",
                        range=error_builder.variable_range_by_name(variable),
                    )
                    errors.append(
                        ResolverError(
                            display=message,
                            path=path,
                            parameter=None,
                        )
                    )
                else:  # has default argument
                    variable = split[0].strip()
                    default_arg = split[1].strip()
                    default_arg = json.loads(default_arg)
                    f = Feature.from_root_fqn(variable)
                    default_arg = f.converter.from_json_to_rich(default_arg)
                    default_args.append(default_arg)
                    has_default_arg = True
        if not has_default_arg:
            default_args.append(...)
        period_replaced = variable.replace(".", "_")
        sql_safe_str = f"__chalk_{period_replaced}__"
        sql_string = sql_string.replace(variable_pattern, f":{sql_safe_str}")
        args[sql_safe_str] = variable
    comments = ""
    docstring = ""
    comment_row_to_file_row: Dict[int, int] = {}
    comment_row_offset: Dict[int, int] = {}
    comment_line_counter = 0
    """
    Comments and docstrings are required to be at the beginning of the file resolver.
    Thus, we need to make sure that for ranges, comments are mapped to the right line number
    as docstrings are not included in the comments variable above.

    We also need to keep track of the offset of the comment in order to properly detect the range.
    """
    for line_no, comment in enumerate(sql_string.splitlines()):
        if comment.strip().startswith("--"):
            stripped_comment = comment.strip().replace("--", "")
            comment_offset = len(comment) - len(stripped_comment)
            if stripped_comment.strip().startswith("-"):
                comments += f"{stripped_comment}\n"
            else:
                if count_colons(stripped_comment) != 1:
                    docstring += f"{stripped_comment.strip()}\n"
                else:
                    comments += f"{stripped_comment}\n"
                    comment_row_to_file_row[comment_line_counter] = line_no
                    comment_row_offset[comment_line_counter] = comment_offset
                    comment_line_counter += 1
        else:
            break

    if len(comments) == 0 and override_comment_dict is None:
        message = "SQL file resolvers require comments that describe key-value pairs in YAML form."
        error_builder.add_diagnostic(
            message=message,
            code="141",
            label="missing comments",
            range=error_builder.full_range(),
            code_href="https://docs.chalk.ai/docs/sql#sql-file-resolvers",
        )
        errors.append(
            ResolverError(
                display=message,
                path=path,
                parameter=None,
            )
        )
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=None,
            docstring=docstring,
            errors=errors,
            source=None,
        )
    if len(comments) != 0:
        try:
            comment_dict: Dict[str, Any] = yaml.safe_load(comments)
        except Exception as e:
            message = f"SQL File resolver comments must have key-values in YAML form: {e}"
            if isinstance(e, ScannerError) and e.problem_mark is not None:
                comment_line_no = e.problem_mark.line
                comment_col_no = e.problem_mark.column
                file_line_no = comment_row_to_file_row[comment_line_no]
                file_comment_no = comment_row_offset[comment_line_no] + comment_col_no
                error_builder.add_diagnostic(
                    message=message,
                    code="142",
                    label="Could not parse comments as YAML",
                    range=error_builder.custom_range(line_no=file_line_no + 1, col=file_comment_no + 1),
                )

            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=comments,
                )
            )
            return GlotResult(
                sql_string=sql_string,
                glot=None,
                args=args,
                default_args=default_args,
                comment_dict=None,
                docstring=docstring,
                errors=errors,
                source=None,
            )
    else:
        comment_dict = {}
    if override_comment_dict is not None:
        for key, value in override_comment_dict.dict().items():
            if value is not None:
                comment_dict[key] = value
    if "source" not in comment_dict:
        """This would be caught by the following BaseModel.parse_obj() but the error message is bad"""
        message = (
            "The datasource is a required field for SQL file resolvers. "
            "Please add a comment '-- source: my_name'  where 'my_name' refers to a named integration."
        )
        error_builder.add_diagnostic(
            message=message,
            code="143",
            label="missing source",
            range=error_builder.full_comment_range(),
            code_href="https://docs.chalk.ai/docs/integrations",
        )
        errors.append(
            ResolverError(
                display=message,
                path=path,
                parameter=json.dumps(comment_dict),
            )
        )
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=None,
            docstring=docstring,
            errors=errors,
            source=None,
        )
    if "resolves" not in comment_dict:
        """This would be caught by the following BaseModel.parse_obj() but the error message is bad"""
        message = (
            "A feature class must be specified for SQL file resolvers. "
            "Please add a comment '-- resolves: my_name'  where 'my_name' refers to a feature class."
        )
        error_builder.add_diagnostic(
            message=message,
            code="144",
            label="missing feature class: please use the 'resolves' keyword",
            range=error_builder.full_comment_range(),
            code_href="https://docs.chalk.ai/docs/integrations",
        )
        errors.append(
            ResolverError(
                display=message,
                path=path,
                parameter=json.dumps(comment_dict),
            )
        )
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=None,
            docstring=docstring,
            errors=errors,
            source=None,
        )

    try:
        comment_dict_object = CommentDict.parse_obj(comment_dict)
    except ValidationError as e:
        for error in e.errors():
            location = error["loc"][-1]  # the innermost error
            message = f"SQL file resolver could not validate comment '{location}': {error['msg']}"
            range = error_builder.comment_range_by_key(str(location))
            if range is None and location in IncrementalSettingsSQLFileResolver.__fields__:
                range = error_builder.comment_range_by_key("incremental")
            error_builder.add_diagnostic(
                message=message,
                code="145",
                label="Could not validate comment",
                range=range,
            )
            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=json.dumps(comment_dict),
                )
            )
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=None,
            docstring=docstring,
            errors=errors,
            source=None,
        )
    docstring = docstring.strip()

    source_name = comment_dict_object.source
    source = None
    if source_name not in _SOURCES:  # actual name of source
        for possible_source in sources:
            if possible_source.name == source_name:
                source = possible_source
    else:  # source type, e.g. snowflake
        for possible_source in sources:
            source_type = None if source_name is None else _SOURCES.get(source_name)
            if source_type is not None and isinstance(possible_source, source_type):
                if possible_source.name in _SOURCES:
                    source = possible_source
                    break
                if source:
                    message = (
                        f"SQL file resolver refers to '{source_name}' when more than one {source_name}-type source "
                        f"exists. Instead, refer to the integration by name among "
                        f"({[source.name for source in sources]})."
                    )
                    error_builder.add_diagnostic(
                        message=message,
                        code="149",
                        label="Refer to source via name instead",
                        range=error_builder.comment_range_by_key("source"),
                    )
                    errors.append(
                        ResolverError(
                            display=message,
                            path=path,
                            parameter=source_name,
                        )
                    )
                source = possible_source
    if source is None:
        message = (
            f"SQL file resolver refers to unrecognized source '{source_name}'. "
            f"Please refer to your source via its name on your Chalk dashboard, "
            f"and make sure the driver, e.g. chalkpy[snowflake], is installed"
        )
        error_builder.add_diagnostic(
            message=message,
            code="150",
            label="Source not found",
            range=error_builder.comment_range_by_key("source"),
        )
        errors.append(
            ResolverError(
                display=message,
                path=path,
                parameter=source_name,
            )
        )
    if errors:
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=comment_dict_object,
            docstring=docstring,
            errors=errors,
            source=None,
        )
    assert source is not None, "unrecognized source should be handled by now"
    source_dialect_string = source.get_sqlglot_dialect()
    try:
        glots = sqlglot.parse(sql=sql_string, read=source_dialect_string)
    except Exception as e:
        message = f"SQL file resolver could not SQL parse string: {e}"
        if isinstance(e, sqlglot.errors.ParseError):
            for error in e.errors:
                error_builder.add_diagnostic(
                    message=message,
                    code="146",
                    label="could not parse SQL",
                    range=error_builder.custom_range(
                        line_no=error["line"],
                        col=error["col"] - 2,
                        length=len(error["highlight"]),  # ????
                    ),
                )
        errors.append(ResolverError(display=message, path=path, parameter=None))
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=comment_dict_object,
            docstring=docstring,
            errors=errors,
            source=source,
        )
    if len(glots) > 1:
        message = f"SQL file resolver query {sql_string} has more than one 'SELECT' statements. Only one is permitted."
        error_builder.add_diagnostic(
            message=message,
            code="147",
            label="SQL query must be a single SELECT statement",
            range=error_builder.sql_range(),
        )
        errors.append(ResolverError(display=message, path=path, parameter=None))
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=comment_dict_object,
            docstring=docstring,
            errors=errors,
            source=source,
        )
    glot = glots[0]
    if not isinstance(glot, (sqlglot.expressions.Select, sqlglot.expressions.Union)):
        message = f"SQL file resolver query {sql_string} should be of 'SELECT' type"
        error_builder.add_diagnostic(
            message=message,
            code="147",
            label="SQL query must be a SELECT statement",
            range=error_builder.sql_range(),
        )
        errors.append(ResolverError(display=message, path=path, parameter=None))
        return GlotResult(
            sql_string=sql_string,
            glot=None,
            args=args,
            default_args=default_args,
            comment_dict=comment_dict_object,
            docstring=docstring,
            errors=errors,
            source=source,
        )
    if len(glot.selects) > len(glot.named_selects):
        for select in glot.selects:
            matched = False
            for named_select in glot.named_selects:
                if select.alias_or_name == named_select:
                    matched = True
            if not matched:
                message = (
                    f"SQL file resolver query with unnamed select '{str(select)}'. "
                    f"All selects must either match a feature name, e.g. 'id', or must be aliased, e.g. "
                    f"'SELECT COUNT (DISTINCT merchant_id) AS num_unique_merchant_ids. "
                    f"All names/aliases must match to features on the feature set defined "
                    f"by the 'resolves' comment parameter. "
                )
                error_builder.add_diagnostic(
                    message=message,
                    code="148",
                    label="all selects must map to features",
                    range=error_builder.value_range_by_name(glot=glot, name=str(select).lower()),
                )
                errors.append(
                    ResolverError(
                        display=message,
                        path=path,
                        parameter=None,
                    )
                )
    return GlotResult(
        sql_string=sql_string,
        glot=glot,
        args=args,
        default_args=default_args,
        comment_dict=comment_dict_object,
        docstring=docstring,
        errors=errors,
        source=source,
    )


def _parse_glot(
    glot_result: GlotResult,
    path: str,
    error_builder: SQLFileResolverErrorBuilder,
) -> ParseResult:
    """Parse useful info from sqlglot and gracefully exit if unable to"""
    try:
        import sqlglot
        import sqlglot.expressions
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    # define a source SQL database. Can either specify name or kind if only one of the kind is present.
    comment_dict = glot_result.comment_dict
    assert comment_dict is not None, "comment dict failed to parse"
    docstring = glot_result.docstring
    source = glot_result.source
    errors: List[ResolverError] = []
    # get resolver fields: which columns selected will match to which chalk feature?
    assert comment_dict.resolves is not None, "comment dict failed to parse"
    namespace = build_namespaced_name(namespace=comment_dict.namespace, name=to_snake_case(comment_dict.resolves))
    if namespace not in FeatureSetBase.registry:
        message = f"No @features class with the name '{namespace}'"
        error_builder.add_diagnostic(
            message=message,
            code="151",
            label="Unrecognized namespace ",
            range=error_builder.comment_range_by_key("resolves"),
        )
        errors.append(ResolverError(display=message, path=path, parameter=namespace))

    stripped_sql = _remove_comments(glot_result.sql_string)
    lineage = _get_data_lineage(stripped_sql)
    # FIXME: @melrchen: need to make a name for unnamed datasources
    source_name = glot_result.source.name or "" if glot_result.source is not None else ""
    namespaced_lineage = (
        {
            table: {f"{namespace}.{feature}": columns for feature, columns in features.items()}
            for table, features in lineage.items()
        }
        if lineage
        else None
    )
    data_lineage_with_source = {source_name: namespaced_lineage} if namespaced_lineage else None

    if len(errors) > 0:
        return ParseResult(
            sql_string=glot_result.sql_string,
            comment_dict=comment_dict,
            fields={},
            namespace=namespace,
            source=source,
            docstring=docstring,
            data_lineage=data_lineage_with_source,
            errors=errors,
        )

    assert isinstance(
        glot_result.glot, (sqlglot.expressions.Select, sqlglot.expressions.Union)
    ), f"glot {glot_result.glot} is not a select or union statement"
    # sql target -> output feature string
    fields: Dict[str, str] = {
        column_name: f"{namespace}.{column_name}" for column_name in glot_result.glot.named_selects
    }

    return ParseResult(
        sql_string=glot_result.sql_string,
        comment_dict=comment_dict,
        fields=fields,
        namespace=namespace,
        source=source,
        docstring=docstring,
        data_lineage=data_lineage_with_source,
        errors=errors,
    )


def _get_stream_resolver(
    path: str,
    glot_result: GlotResult,
    parsed: ParseResult,
    outputs: List[Feature],
    error_builder: SQLFileResolverErrorBuilder,
) -> ResolverResult:
    errors = []
    output_features = Features[DataFrame[tuple(outputs)]]

    if isinstance(output_features.features[0], type) and issubclass(output_features.features[0], DataFrame):
        output_feature_fqns = set(f.fqn for f in cast(Type[DataFrame], output_features.features[0]).columns)
    else:
        output_feature_fqns = set(f.fqn for f in output_features.features)

    signature = StreamResolverSignature(
        params=[],
        output_feature_fqns=output_feature_fqns,
    )

    sql_query: str = _remove_comments(parsed.sql_string)
    filename = os.path.basename(path)
    try:

        def fn():
            return sql_query

        # attempt to instantiate the resolver
        resolver = StreamResolver(
            function_definition=sql_query,
            fqn=filename.replace(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX, ""),
            filename=path,
            source=cast(StreamSource, parsed.source),
            fn=fn,
            environment=parsed.comment_dict.environment,
            doc=parsed.docstring,
            mode=None,
            machine_type=parsed.comment_dict.machine_type,
            message=None,
            output=output_features,
            signature=signature,
            state=None,
            sql_query=sql_query,
            owner=parsed.comment_dict.owner,
            parse=None,
            keys=None,  # TODO implement parse and keys for sql file resolvers?
            timestamp=None,
            source_line=None,
            tags=None,
            lsp_builder=get_resolver_error_builder(fn),
            autogenerated=False,
            updates_materialized_aggregations=True,
            sql_settings=None,
        )
    except Exception as e:
        message = f"Streaming SQL file resolver could not be instantiated, {e}"
        error_builder.add_diagnostic(
            message=message,
            code="141",
            label="resolver instantiation failed",
            range=error_builder.full_range(),
        )
        errors.append(
            ResolverError(
                display=message,
                path=path,
                parameter=None,
            )
        )
        return ResolverResult(resolver=None, errors=errors, db=parsed.source, fields=None, args=None)

    return ResolverResult(
        resolver=resolver,
        errors=errors,
        db=parsed.source,
        fields=parsed.fields,
        args=glot_result.args,
    )


def _validate_feature_strings_in_comments(
    feature_strings: list[str],
    error_builder: SQLFileResolverErrorBuilder,
    namespace: str,
    path: str,
    errors: list[ResolverError],
    outputs: list[Feature],
    arg_name: str,
) -> tuple[Feature, ...]:
    feature_list: list[Feature] = []
    for f in feature_strings:
        feature = None
        try:
            feature = Feature.from_root_fqn(f)
        except:
            if "." not in f:
                reconstructed_fqn = f"{namespace}.{f}"
                try:
                    feature = Feature.from_root_fqn(reconstructed_fqn)
                except:
                    pass
        if feature is None:
            message = f"SQL file resolver {path} references a 'unique_on' feature '{f}' which does not exist."

            error_builder.add_diagnostic_with_spellcheck(
                spellcheck_item=f,
                spellcheck_candidates=[
                    feature.fqn for feature in FeatureSetBase.registry[build_namespaced_name(name=namespace)].features
                ],
                message=message,
                code="153a",
                label="output feature not recognized",
                range=error_builder.comment_range_by_key(arg_name),
            )
            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=f,
                )
            )
            continue

        if feature not in outputs:
            message = (
                f"SQL file resolver {path} references a '{arg_name}' feature '{f}' which is not an output feature."
            )
            error_builder.add_diagnostic(
                message=message,
                code="153b",
                label=f"{arg_name} feature not in outputs",
                range=error_builder.comment_range_by_key(arg_name),
            )
            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=f,
                )
            )
        elif feature in feature_list:
            message = f"SQL file resolver {path} references '{arg_name}' feature '{f}' multiple times."
            error_builder.add_diagnostic(
                message=message,
                code="153b",
                label=f"{arg_name} feature stated multiple times",
                range=error_builder.comment_range_by_key(arg_name),
            )
            errors.append(
                ResolverError(
                    display=message,
                    path=path,
                    parameter=f,
                )
            )
        else:
            feature_list.append(feature)
    return tuple(feature_list)


def _remove_comments(sql_string: str) -> str:
    sql_string = re.sub(
        re.compile("/\\*.*?\\*/", re.DOTALL), "", sql_string
    )  # remove all occurrences streamed comments (/*COMMENT */) from string
    sql_string = re.sub(
        re.compile("//.*?\n"), "", sql_string
    )  # remove all occurrence single-line comments (//COMMENT\n ) from string
    sql_string = re.sub(
        re.compile("--.*?\n"), "", sql_string
    )  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return sql_string.strip()


def count_colons(s: str) -> int:
    count = 0
    inside_single_quotes = False
    inside_double_quotes = False

    for char in s:
        if char == '"':
            inside_double_quotes = not inside_double_quotes
        elif char == "'":
            inside_single_quotes = not inside_single_quotes
        elif char == ":" and not inside_single_quotes and not inside_double_quotes:
            count += 1
    return count


@dataclasses.dataclass(frozen=True)
class GeneratedSQLFileResolverInfo:
    filepath: str
    sql_string: str
    comment_dict: CommentDict


class GeneratedSQLFileResolverRegistry:
    def __init__(self):
        super().__init__()
        self.resolver_name_to_generated_infos: Dict[str, GeneratedSQLFileResolverInfo] = {}

    def add_sql_file_resolver(self, name: str, filepath: str, sql_string: str, comment_dict: CommentDict):
        if name in self.resolver_name_to_generated_infos:
            raise ValueError(f"A SQL file resolver already exists with name '{name}'. They must have unique names.")
        self.resolver_name_to_generated_infos[name] = GeneratedSQLFileResolverInfo(
            filepath=filepath,
            sql_string=sql_string,
            comment_dict=comment_dict,
        )

    def get_generated_sql_file_resolvers(self) -> Iterable[SQLStringResult]:
        for name, generated_info in self.resolver_name_to_generated_infos.items():
            yield SQLStringResult(
                path=generated_info.filepath,
                sql_string=generated_info.sql_string,
                error=None,
                override_comment_dict=generated_info.comment_dict,
                override_name=name,
                autogenerated=True,
            )


_GENERATED_SQL_FILE_RESOLVER_REGISTRY = GeneratedSQLFileResolverRegistry()


def make_sql_file_resolver(
    name: str,
    sql: str,
    source: str | BaseSQLSourceProtocol | None = None,
    resolves: str | Any | None = None,
    kind: Literal["online", "offline", "streaming"] | None = None,
    incremental: IncrementalSettings | None = None,
    count: Literal[1, "one", "one_or_none", "all"] | None = None,
    timeout: Duration | None = None,
    cron: CronTab | Duration | Cron | None = None,
    owner: str | None = None,
    machine_type: MachineType | None = None,
    fields: dict[str, str | FeatureReference] | None = None,
    environment: Environments | None = None,
    tags: Tags | None = None,
    unique_on: Collection[FeatureReference] | None = None,
    partitioned_by: Collection[Any] | None = None,
    total: Optional[bool] = None,
):
    """Generate a Chalk SQL file resolver from a filepath and a sql string.
    This will generate a resolver in your web dashboard that can be queried,
    but will not output a `.chalk.sql` file.

    The optional parameters are overrides for the comment key-value pairs
    at the top of the sql file resolver. Comment key-value pairs specify
    important resolver information such as the source, feature namespace
    to resolve, and other details.
    Note that these will override any values specified in the sql string.
    See https://docs.chalk.ai/docs/sql#configuration for more information.

    See https://docs.chalk.ai/docs/sql#sql-file-resolvers for more information
    on SQL file resolvers.

    Parameters
    ----------
    name
        The name of your resolver
    sql
        The sql string for your query.
    kind
        The type of resolver.
        If not specified, defaults to "online".
    source
        Can either be a BaseSQLSource or a string.
        If a string is provided, it will be used to infer the source by
        first scanning for a source with the same name, then inferring
        the source if it is a type, e.g. `snowflake` if there is only
        one database of that type. Optional if `source` is specified in `sql`.
    resolves
        Describes the feature namespace to which the outputs belong.
        Optional if `resolves` is specified in `sql`.

    Other Parameters
    ----------------
    incremental
        Parameters for incremental queries.
        For more information, see https://docs.chalk.ai/docs/sql#incremental-queries.
    count
        If set to `one`, the resolver will return only one row.
        If set to `one_or_none`, the resolver will return at most one row.
        If set to `all`, the resolver will return all rows
    timeout
        You can specify the maximum duration to wait for the
        resolver's result. Once the resolver's runtime exceeds
        the specified duration, a timeout error will be returned
        along with each output feature.

        Please use supported Chalk durations
        'w', 'd', 'h', 'm', 's', and/or 'ms'.

        Read more at https://docs.chalk.ai/docs/timeout and https://docs.chalk.ai/api-docs#Duration
    cron
        You can schedule resolvers to run on a pre-determined
        schedule via the cron argument to resolver decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron
    environment
        Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:
            - `None` (default) - candidate to run in every environment
            - `str` - run only in this environment
            - `list[str]` - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments
    tags
        Allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags
    owner
        Individual or team responsible for this resolver.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    machine_type
        You can optionally specify that resolvers need to run on
        a machine other than the default. Must be configured in
        your deployment.
    fields
        An optional mapping from SQL column to Chalk feature.
        For example, let's say we have a Chalk feature class 'Transaction' with a primary key 'id'.
        If we have a SQL query like `SELECT txn_id from transactions`,
        we can map the `txn_id` to our Chalk feature with the mapping
        `txn_id: id`.
    unique_on
        A list of features that must be unique for each row of the output.
        This enables unique optimizations in the resolver execution.
        Only applicable to resolvers that return a DataFrame.
    partitioned_by
        A list of features that correspond to partition keys in the data source.
        This field indicates that this resolver executes its query against a data storage system that is
        partitioned by a particular set of columns.
        This is most common with data-warehouse sources like Snowflake, BigQuery or Databricks.
    total
        Whether this resolver returns all ids of a given namespace. To have this annotation, the resolver must
        take no arguments and return a DataFrame.


    Examples
    --------
    >>> from chalk import make_sql_file_resolver
    >>> from chalk.features import features
    >>> @features
    ... class User:
    ...     id: int
    ...     name: str
    >>> make_sql_file_resolver(
    ...     name="my_resolver",
    ...     sql="SELECT user_id as id, name FROM users",
    ...     source="snowflake",
    ...     resolves=User,
    ...     kind="offline",
    ... )
    """
    if name.endswith(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX):
        name = name.replace(CHALK_SQL_FILE_RESOLVER_FILENAME_SUFFIX, "")
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    if module is None:
        raise ValueError("Could not get caller module for 'make_sql_file_resolver'")
    module_file = module.__file__
    if module_file is None:
        raise ValueError("Could not get caller file for 'make_sql_file_resolver'")

    filename = module_file  # the resolver filename will be where 'make_sql_file_resolver' was called

    comment_dict = CommentDict(
        source=source if isinstance(source, str) or source is None else source.name,
        resolves=str(resolves) if resolves is not None else None,
        type=kind,
        incremental=incremental and _convert_incremental_settings(incremental),
        count=count,
        timeout=(
            timeout
            if timeout is None
            else timedelta_to_duration(timeout)
            if isinstance(timeout, timedelta)
            else timeout
        ),
        cron=cron,
        owner=owner,
        fields=None if fields is None else {k: str(v) for k, v in fields.items()},
        environment=(
            None if environment is None else [environment] if isinstance(environment, str) else list(environment)
        ),
        tags=None if tags is None else [tags] if isinstance(tags, str) else list(tags),
        total=total,
        namespace=None,
        machine_type=machine_type,
        unique_on=[str(f) for f in unique_on] if unique_on is not None else None,
        partitioned_by=[str(f) for f in partitioned_by] if partitioned_by is not None else None,
    )
    _GENERATED_SQL_FILE_RESOLVER_REGISTRY.add_sql_file_resolver(
        filepath=filename,
        sql_string=sql,
        comment_dict=comment_dict,
        name=name,
    )


def _convert_incremental_settings(settings: IncrementalSettings) -> IncrementalSettingsSQLFileResolver:
    return IncrementalSettingsSQLFileResolver(
        incremental_column=settings.incremental_column,
        lookback_period=(
            timedelta_to_duration(settings.lookback_period) if settings.lookback_period is not None else None
        ),
        mode=settings.mode,
        incremental_timestamp=settings.incremental_timestamp,
    )


def parse_finalizer(count: Literal[1, "one", "one_or_none", "all"] | None) -> Finalizer | None:
    if count == 1 or count == "one":
        return Finalizer.ONE
    if count == "one_or_none":
        return Finalizer.ONE_OR_NONE
    if count == "all":
        return Finalizer.ALL
    return None
