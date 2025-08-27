from __future__ import annotations

import functools
import glob
import itertools
import json
import os
import os.path
import pprint
import re
import shlex
import string
import textwrap
import traceback
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from pathlib import Path
from string import Template
from typing import Any, Callable, Dict, Iterable, List, Literal, NamedTuple, Optional, Tuple, cast

import click
from croniter import croniter
from mypy_extensions import KwArg, VarArg

from tinybird.ch_utils.engine import ENABLED_ENGINES
from tinybird.datafile.exceptions import IncludeFileNotFoundException, ParseException, ValidationException
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.feedback_manager import FeedbackManager

# Code from sql.py has been duplicated so I can change it without breaking absolutely everything in the app
# I'll try not to make logic changes, just error reporting changes
# from tinybird.sql import parse_indexes_structure, parse_table_structure, schema_to_sql_columns


class DatafileValidationError(Exception): ...


class DatafileSyntaxError(Exception):
    def __init__(self, message: str, lineno: int, pos: int, hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.context: Optional[str] = None
        self.hint = hint
        self.lineno = lineno
        self.pos = pos

    def add_context(self, context: str):
        self.context = context

    def get_context_from_file_contents(self, s: str) -> None:
        lines = s.splitlines()

        start_line = max(0, self.lineno - 3)  # 2 lines before
        end_line = self.lineno  # Only context before the error

        # Calculate padding needed for line numbers
        max_line_digits = len(str(end_line))

        context = []
        for i in range(start_line, end_line):
            line_num = str(i + 1).rjust(max_line_digits)
            line = lines[i].rstrip()
            context.append(f"{line_num}: {line}")

            # Add pointer line if this is the error line
            if i + 1 == self.lineno:
                pointer = " " * (max_line_digits + 2 + self.pos - 1) + "^"
                context.append(pointer)

        error_context = "\n".join(context)
        self.add_context(error_context)

    def __str__(self) -> str:
        output = f"{self.message}"
        output += f"\n\n{self.context}" if self.context else f" at {self.lineno}:{self.pos}."
        output += f"\n{self.hint}." if self.hint else ""
        return output


class SchemaSyntaxError(DatafileSyntaxError):
    def __init__(self, message: str, lineno: int, pos: int, hint: Optional[str] = None):
        super().__init__(message=message, lineno=lineno, pos=pos, hint=hint)


class IndexesSyntaxError(DatafileSyntaxError):
    def __init__(self, message: str, lineno: int, pos: int, hint: Optional[str] = None):
        super().__init__(message=message, lineno=lineno, pos=pos, hint=hint)


class MalformedColumnError(Exception):
    pass


class PipeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    COPY = "copy"
    DATA_SINK = "sink"
    STREAM = "stream"
    DEFAULT = "default"


class PipeNodeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    STANDARD = "standard"
    DEFAULT = "default"
    DATA_SINK = "sink"
    COPY = "copy"
    STREAM = "stream"
    EMPTY = ""


VALID_PIPE_NODE_TYPES = {
    PipeNodeTypes.MATERIALIZED,
    PipeNodeTypes.STANDARD,
    PipeNodeTypes.COPY,
    PipeNodeTypes.EMPTY,
    PipeNodeTypes.ENDPOINT,
    PipeNodeTypes.STREAM,
    PipeNodeTypes.DATA_SINK,
}
VISIBLE_PIPE_NODE_TYPES = {
    PipeNodeTypes.MATERIALIZED,
    PipeNodeTypes.COPY,
    PipeNodeTypes.ENDPOINT,
    PipeNodeTypes.DATA_SINK,
}


class DataFileExtensions:
    PIPE = ".pipe"
    DATASOURCE = ".datasource"
    INCL = ".incl"
    CONNECTION = ".connection"


class CopyModes:
    APPEND = "append"
    REPLACE = "replace"

    valid_modes = (APPEND, REPLACE)

    @staticmethod
    def is_valid(node_mode):
        return node_mode.lower() in CopyModes.valid_modes


class Parameters:
    ACCEPTED_ATTRIBUTES: set[str] = set()
    MANDATORY_ATTRIBUTES: set[str] = set()
    _PARAMS_ALIASES: dict[str, str] = {"name": "node", "mode": "copy_mode"}

    @classmethod
    def valid_params(cls) -> set[str]:
        return cls.ACCEPTED_ATTRIBUTES

    @classmethod
    def required_params(cls) -> set[str]:
        return cls.MANDATORY_ATTRIBUTES

    @staticmethod
    def canonical_name(name: str):
        return Parameters._PARAMS_ALIASES.get(name, name)


class PipeParameters(Parameters):
    MANDATORY_ATTRIBUTES = {"name", "sql", "type"}
    ACCEPTED_ATTRIBUTES = {"description"}.union(MANDATORY_ATTRIBUTES)


class CopyParameters(Parameters):
    TARGET_DATASOURCE = "target_datasource"
    COPY_SCHEDULE = "copy_schedule"
    COPY_MODE = "copy_mode"
    COPY_MODE_ALIAS = "mode"  # we need this because bot MODE and COPY_MODE go to `mode` variable inside the node
    MANDATORY_ATTRIBUTES = PipeParameters.MANDATORY_ATTRIBUTES.union({TARGET_DATASOURCE})
    ACCEPTED_ATTRIBUTES = PipeParameters.ACCEPTED_ATTRIBUTES.union(MANDATORY_ATTRIBUTES).union(
        {COPY_SCHEDULE, COPY_MODE_ALIAS}
    )


class MaterializedParameters(Parameters):
    MANDATORY_ATTRIBUTES = PipeParameters.MANDATORY_ATTRIBUTES.union({"datasource"})
    ACCEPTED_ATTRIBUTES = PipeParameters.ACCEPTED_ATTRIBUTES.union(MANDATORY_ATTRIBUTES).union({"deployment_method"})


class SinkParameters(Parameters):
    # For Kafka sinks
    KAFKA_MANDATORY_ATTRIBUTES = PipeParameters.MANDATORY_ATTRIBUTES.union(
        {"export_connection_name", "export_kafka_topic", "export_schedule"}
    )
    KAFKA_ACCEPTED_ATTRIBUTES = PipeParameters.ACCEPTED_ATTRIBUTES.union(KAFKA_MANDATORY_ATTRIBUTES)

    # For S3/GCS sinks
    BLOB_MANDATORY_ATTRIBUTES = PipeParameters.MANDATORY_ATTRIBUTES.union(
        {"export_connection_name", "export_schedule", "export_bucket_uri", "export_file_template"}
    )
    BLOB_ACCEPTED_ATTRIBUTES = PipeParameters.ACCEPTED_ATTRIBUTES.union(BLOB_MANDATORY_ATTRIBUTES).union(
        {"export_format", "export_compression", "export_write_strategy", "export_strategy"}
    )


DATAFILE_NEW_LINE = "\n"
DATAFILE_INDENT = " " * 4

ON_DEMAND = "@on-demand"
DEFAULT_CRON_PERIOD: int = 60

INTERNAL_TABLES: Tuple[str, ...] = (
    "datasources_ops_log",
    "pipe_stats",
    "pipe_stats_rt",
    "block_log",
    "data_connectors_log",
    "kafka_ops_log",
    "datasources_storage",
    "endpoint_errors",
    "bi_stats_rt",
    "bi_stats",
)

PREVIEW_CONNECTOR_SERVICES = ["s3", "s3_iamrole", "gcs"]

pp = pprint.PrettyPrinter()

valid_chars_name: str = string.ascii_letters + string.digits + "._`*<>+-'"
valid_chars_fn: str = valid_chars_name + "[](),=!?:/ \n\t\r"


class UnkownExtensionerror(Exception): ...


class DatafileKind(Enum):
    pipe = "pipe"
    datasource = "datasource"
    connection = "connection"

    @classmethod
    def from_extension(cls, extension: str) -> DatafileKind:
        extension_map = {
            ".pipe": cls.pipe,
            ".datasource": cls.datasource,
            ".connection": cls.connection,
        }
        if extension not in extension_map:
            raise UnkownExtensionerror(f"Unknown extension {extension} for data file")
        return extension_map[extension]


REQUIRED_KAFKA_PARAMS = {
    "kafka_connection_name",
    "kafka_topic",
    "kafka_group_id",
}

KAFKA_PARAMS = REQUIRED_KAFKA_PARAMS

REQUIRED_BLOB_STORAGE_PARAMS = {
    "import_connection_name",
    "import_schedule",
    "import_bucket_uri",
}
BLOB_STORAGE_PARAMS = REQUIRED_BLOB_STORAGE_PARAMS.union({"import_from_timestamp"})
VALID_BLOB_STORAGE_CRON_VALUES = {
    "@once",
    "@on-demand",
    "@auto",
}


class Datafile:
    def __init__(self) -> None:
        self.maintainer: Optional[str] = None
        self.nodes: List[Dict[str, Any]] = []
        self.tokens: List[Dict[str, Any]] = []
        self.version: Optional[int] = None
        self.description: Optional[str] = None
        self.raw: Optional[List[str]] = None
        self.includes: Dict[str, Any] = {}
        self.shared_with: List[str] = []
        self.warnings: List[str] = []
        self.filtering_tags: Optional[List[str]] = None
        self.kind: Optional[DatafileKind] = None

    def is_equal(self, other):
        if len(self.nodes) != len(other.nodes):
            return False

        return all(self.nodes[i] == other.nodes[i] for i, _ in enumerate(self.nodes))

    def set_kind(self, kind: DatafileKind):
        self.kind = kind

    def validate_standard_node(self, node: Dict[str, Any]):
        for key in node.keys():
            if key not in PipeParameters.valid_params():
                raise DatafileValidationError(
                    f"Standard node {repr(node['name'])} has an invalid attribute ({PipeParameters.canonical_name(key)})"
                )

    def validate_copy_node(self, node: Dict[str, Any]):
        if missing := [param for param in CopyParameters.required_params() if param not in node]:
            raise DatafileValidationError(
                f"Some copy node params have been provided, but the following required ones are missing: {missing}"
            )
        # copy mode must be append or replace
        if node.get("mode") and node["mode"] not in ["append", "replace"]:
            raise DatafileValidationError("COPY node mode must be append or replace")
        # copy schedule must be @on-demand or a cron-expression
        if (
            node.get("copy_schedule")
            and node["copy_schedule"] != ON_DEMAND
            and not croniter.is_valid(node["copy_schedule"])
        ):
            raise DatafileValidationError("COPY node schedule must be @on-demand or a valid cron expression.")
        for key in node.keys():
            if key not in CopyParameters.valid_params():
                raise DatafileValidationError(
                    f"Copy node {repr(node['name'])} has an invalid attribute ({CopyParameters.canonical_name(key)})"
                )

    def validate_materialized_node(self, node: Dict[str, Any]):
        if missing := [param for param in MaterializedParameters.required_params() if param not in node]:
            raise DatafileValidationError(
                f"Some materialized node params have been provided, but the following required ones are missing: {missing}"
            )
        for key in node.keys():
            if key not in MaterializedParameters.valid_params():
                raise DatafileValidationError(
                    f"Materialized node {repr(node['name'])} has an invalid attribute ({MaterializedParameters.canonical_name(key)})"
                )

    def validate_sink_node(self, node: Dict[str, Any]):
        export_connection_name = node.get("export_connection_name")

        if not export_connection_name:
            raise DatafileValidationError(
                f"Sink node {repr(node['name'])} is missing required parameter 'export_connection_name'"
            )

        # Determine connection type to validate appropriate parameters
        # First, try to determine from presence of Kafka-specific parameters
        has_kafka_topic = "export_kafka_topic" in node
        has_s3_gcs_params = any(param in node for param in ["export_bucket_uri", "export_file_template"])

        # If both types of parameters are present, that's an error
        if has_kafka_topic and has_s3_gcs_params:
            raise DatafileValidationError(
                f"Sink node {repr(node['name'])} has mixed Kafka and S3/GCS parameters. Use either Kafka parameters (export_kafka_topic) or S3/GCS parameters (export_bucket_uri, export_file_template), not both."
            )

        # If we have Kafka-specific parameters, treat as Kafka sink
        if has_kafka_topic:
            # Kafka sink validation
            if missing := [param for param in SinkParameters.KAFKA_MANDATORY_ATTRIBUTES if param not in node]:
                raise DatafileValidationError(
                    f"Kafka sink node {repr(node['name'])} is missing required parameters: {missing}"
                )

            # For Kafka sinks, only specific parameters should be present
            kafka_specific_params = (
                {"export_kafka_topic", "export_schedule", "export_connection_name"}
                | PipeParameters.MANDATORY_ATTRIBUTES
                | PipeParameters.ACCEPTED_ATTRIBUTES
            )
            for key in node.keys():
                if key not in kafka_specific_params:
                    raise DatafileValidationError(
                        f"Kafka sink node {repr(node['name'])} has invalid parameter '{key}'. Only export_kafka_topic, export_schedule, and export_connection_name are allowed for Kafka sinks."
                    )

        # If we have S3/GCS-specific parameters, treat as S3/GCS sink
        elif has_s3_gcs_params:
            # S3/GCS sink validation
            if missing := [param for param in SinkParameters.BLOB_MANDATORY_ATTRIBUTES if param not in node]:
                raise DatafileValidationError(
                    f"S3/GCS sink node {repr(node['name'])} is missing required parameters: {missing}"
                )

            # Check that only valid parameters are present
            for key in node.keys():
                if key not in SinkParameters.BLOB_ACCEPTED_ATTRIBUTES:
                    raise DatafileValidationError(
                        f"S3/GCS sink node {repr(node['name'])} has invalid parameter '{key}'"
                    )

        # If no type-specific parameters are present, we can't determine the type
        # This means the sink is missing required parameters for any sink type
        else:
            # Check if we have any export parameters at all besides connection_name and schedule
            export_params = {
                k
                for k in node.keys()
                if k.startswith("export_") and k not in {"export_connection_name", "export_schedule"}
            }
            if not export_params:
                raise DatafileValidationError(
                    f"Sink node {repr(node['name'])} is missing required parameters. "
                    f"For Kafka sinks, provide 'export_kafka_topic'. "
                    f"For S3/GCS sinks, provide 'export_bucket_uri' and 'export_file_template'."
                )
            else:
                # There are some export parameters, but they don't match known patterns
                raise DatafileValidationError(
                    f"Sink node {repr(node['name'])} has unrecognized export parameters: {export_params}. "
                    f"For Kafka sinks, use 'export_kafka_topic'. "
                    f"For S3/GCS sinks, use 'export_bucket_uri' and 'export_file_template'."
                )

        # Validate schedule format (common for both Kafka and S3/GCS)
        export_schedule = node.get("export_schedule")
        if export_schedule and export_schedule != ON_DEMAND and not croniter.is_valid(export_schedule):
            raise DatafileValidationError(
                f"Sink node {repr(node['name'])} has invalid export_schedule '{export_schedule}'. Must be @on-demand or a valid cron expression."
            )

    def validate(self):
        if self.kind == DatafileKind.pipe:
            if len(self.nodes) == 0:
                raise DatafileValidationError("Pipe data file must have at least one node")

            non_standard_nodes_count = 0
            for node in self.nodes:
                node_type = node.get("type", "").lower()
                if node_type not in {PipeNodeTypes.STANDARD, ""}:
                    non_standard_nodes_count += 1
                    if non_standard_nodes_count > 1:
                        raise DatafileValidationError("Multiple non-standard nodes in pipe. There can only be one")
                if node_type == PipeNodeTypes.MATERIALIZED:
                    self.validate_materialized_node(node)
                if node_type == PipeNodeTypes.COPY:
                    self.validate_copy_node(node)
                if node_type == PipeNodeTypes.DATA_SINK:
                    self.validate_sink_node(node)
                if node_type in {PipeNodeTypes.STANDARD, ""}:
                    self.validate_standard_node(node)
                if node_type not in VALID_PIPE_NODE_TYPES:
                    raise DatafileValidationError(
                        f"Invalid node '{repr(node['name'])}' of type ({node_type}). Allowed node types: {VISIBLE_PIPE_NODE_TYPES}"
                    )

            for token in self.tokens:
                if token["permission"].upper() != "READ":
                    raise DatafileValidationError(
                        f"Invalid permission {token['permission']} for token {token['token_name']}. Only READ is allowed for pipes"
                    )
        elif self.kind == DatafileKind.datasource:
            #  [x] Just one node
            #  [x] Engine is present
            #  [x] Token permissions are valid
            #  [x] If it's a kafka datasource, all required kafka params are present
            #  [x] If it's an S3 datasource, all required S3 params are present
            #  [ ] ...
            if len(self.nodes) > 1:
                # Our users are not aware of data source data files being a single-node data file, hence this error
                # message which might be confusing for us devs
                raise DatafileValidationError("Datasource files cannot have nodes defined")
            node = self.nodes[0]
            if "schema" not in node:
                raise DatafileValidationError("SCHEMA is mandatory")
            # Validate token permissions
            for token in self.tokens:
                if token["permission"].upper() not in {"READ", "APPEND"}:
                    raise DatafileValidationError(
                        f"Invalid permission {token['permission']} for token {token['token_name']}. Only READ and APPEND are allowed for datasources"
                    )

            # Validate sorting key if present
            if "engine" in node and isinstance(node["engine"], dict) and "args" in node["engine"]:
                for arg_name, arg_value in node["engine"]["args"]:
                    if arg_name.lower() == "sorting_key":
                        # Check for sorting key constraints
                        self._validate_sorting_key(arg_value, node)
                        break

            # Validate Kafka params
            if any(param in node for param in KAFKA_PARAMS) and (
                missing := [param for param in REQUIRED_KAFKA_PARAMS if param not in node]
            ):
                raise DatafileValidationError(
                    f"Some Kafka params have been provided, but the following required ones are missing: {missing}"
                )
            # Validate S3 params
            if any(param in node for param in BLOB_STORAGE_PARAMS):
                if missing := [param for param in REQUIRED_BLOB_STORAGE_PARAMS if param not in node]:
                    raise DatafileValidationError(
                        f"Some connection params have been provided, but the following required ones are missing: {missing}"
                    )
                if node["import_schedule"] not in VALID_BLOB_STORAGE_CRON_VALUES:
                    raise DatafileValidationError(
                        f"Invalid import schedule '{node['import_schedule']}'. Only {sorted(VALID_BLOB_STORAGE_CRON_VALUES)} values are allowed"
                    )

        else:
            # We cannot validate a datafile whose kind is unknown
            pass

    def _validate_sorting_key(self, sorting_key: str, node: Dict[str, Any]) -> None:
        """
        Validates that a sorting key doesn't reference:
        - Nullable columns
        - AggregateFunction types
        - Engine version columns for ReplacingMergeTree
        """
        if sorting_key == "tuple()" or not sorting_key:
            return  # Empty sorting key is valid

        engine_ver_column = self._extract_engine_ver_column(node)
        schema_columns = {col["name"]: col for col in node["columns"]}
        sorting_key_columns = self._parse_sorting_key_columns(sorting_key, engine_ver_column)

        self._validate_columns_against_schema(sorting_key_columns, schema_columns)

    def _extract_engine_ver_column(self, node: Dict[str, Any]) -> Optional[str]:
        engine_info = node.get("engine", {})

        if not isinstance(engine_info, dict):
            return None

        engine_type = engine_info.get("type", "")
        if engine_type != "ReplacingMergeTree":
            return None

        engine_args = engine_info.get("args", [])
        for arg_name, arg_value in engine_args:
            if arg_name == "ver":
                return arg_value

        return None

    def _parse_sorting_key_columns(self, sorting_key: str, engine_ver_column: Optional[str]) -> List[str]:
        """Parse sorting key to extract column names and validate constraints."""
        # Validate ENGINE_VER column constraint early
        if engine_ver_column and engine_ver_column in sorting_key:
            raise DatafileValidationError(
                f"ENGINE_VER column '{engine_ver_column}' cannot be included in the sorting key for ReplacingMergeTree. "
                f"Including the version column in the sorting key prevents deduplication because rows with different "
                f"versions will have different sorting keys and won't be considered duplicates. The sorting key should "
                f"define the record identity (what makes it unique), while ENGINE_VER tracks which version to keep."
            )

        # Remove tuple() wrapper if present
        column_str = sorting_key
        if column_str.startswith("tuple(") and column_str.endswith(")"):
            column_str = column_str[6:-1]

        sorting_key_columns = []

        for part in column_str.split(","):
            part = part.strip()

            if self._is_aggregate_function_expression(part):
                raise DatafileValidationError(
                    f"Sorting key contains aggregate function expression '{part}'. Aggregate function expressions cannot be used in sorting keys."
                )

            # Extract column names from the part
            extracted_columns = self._extract_column_names_from_part(part)
            sorting_key_columns.extend(extracted_columns)

        return sorting_key_columns

    def _is_aggregate_function_expression(self, part: str) -> bool:
        """Check if a sorting key part is an aggregate function expression."""
        if not ("(" in part and part.endswith(")")):
            return False

        func_start = part.find("(")
        func_name = part[:func_start].strip().lower()

        aggregate_function_names = {
            "sum",
            "count",
            "avg",
            "min",
            "max",
            "any",
            "grouparray",
            "groupuniqarray",
            "uniq",
            "summerge",
            "countmerge",
            "avgmerge",
            "minmerge",
            "maxmerge",
            "anymerge",
            "grouparraymerge",
            "groupuniqarraymerge",
            "uniqmerge",
        }

        return func_name in aggregate_function_names

    def _extract_column_names_from_part(self, part: str) -> List[str]:
        """Extract column names from a sorting key part."""
        columns = []

        if "(" in part and part.endswith(")"):
            # Function expression - extract column names from inside parentheses
            func_start = part.find("(")
            inner_content = part[func_start + 1 : -1].strip()
            for inner_part in inner_content.split(","):
                inner_part = inner_part.strip().strip("`")
                if inner_part and inner_part.isidentifier():
                    columns.append(inner_part)
        elif part:
            # Simple column name
            column_name = part.strip("`")
            if column_name:
                columns.append(column_name)

        return columns

    def _validate_columns_against_schema(
        self, sorting_key_columns: List[str], schema_columns: Dict[str, Dict[str, Any]]
    ) -> None:
        """Validate each column in the sorting key against the schema."""
        if not schema_columns:
            return  # No schema information available, can't validate

        for col_name in sorting_key_columns:
            if col_name not in schema_columns:
                continue

            self._validate_single_column(col_name, schema_columns[col_name])

    def _validate_single_column(self, col_name: str, column_info: Dict[str, Any]) -> None:
        """Validate a single column for use in sorting keys."""
        col_type = column_info.get("type", "").lower()
        is_nullable = column_info.get("nullable", False)
        if is_nullable:
            raise DatafileValidationError(
                f"Sorting key contains nullable column '{col_name}'. Nullable columns cannot be used in sorting keys."
            )
        if "aggregatefunction" in col_type:
            raise DatafileValidationError(
                f"Sorting key contains column '{col_name}' with AggregateFunction type. AggregateFunction columns cannot be used in sorting keys."
            )


def format_filename(filename: str, hide_folders: bool = False):
    return os.path.basename(filename) if hide_folders else filename


def _unquote(x: str):
    QUOTES = ('"', "'")
    if x[0] in QUOTES and x[-1] in QUOTES:
        x = x[1:-1]
    return x


def eval_var(s: str, skip: bool = False) -> str:
    if skip:
        return s
    # replace ENV variables
    # it's probably a bad idea to allow to get any env var
    return Template(s).safe_substitute(os.environ)


def parse_tags(tags: str) -> Tuple[str, List[str]]:
    """
    Parses a string of tags into:
    - kv_tags: a string of key-value tags: the previous tags we have for operational purposes. It
        has the format key=value&key2=value2 (with_staging=true&with_last_date=true)
    - filtering_tags: a list of tags that are used for filtering.

    Example: "with_staging=true&with_last_date=true,billing,stats" ->
        kv_tags = {"with_staging": "true", "with_last_date": "true"}
        filtering_tags = ["billing", "stats"]
    """
    kv_tags = []
    filtering_tags = []

    entries = tags.split(",")
    for entry in entries:
        trimmed_entry = entry.strip()
        if "=" in trimmed_entry:
            kv_tags.append(trimmed_entry)
        else:
            filtering_tags.append(trimmed_entry)

    all_kv_tags = "&".join(kv_tags)

    return all_kv_tags, filtering_tags


@dataclass
class TableIndex:
    """Defines a CH table INDEX"""

    name: str
    expr: str
    type_full: str
    granularity: Optional[str] = None

    def to_datafile(self):
        granularity_expr = f"GRANULARITY {self.granularity}" if self.granularity else ""
        return f"{self.name} {self.expr} TYPE {self.type_full} {granularity_expr}"

    def to_sql(self):
        return f"INDEX {self.to_datafile()}"

    def add_index_sql(self):
        return f"ADD {self.to_sql()}"

    def drop_index_sql(self):
        return f"DROP INDEX IF EXISTS {self.name}"

    def materialize_index_sql(self):
        return f"MATERIALIZE INDEX IF EXISTS {self.name}"

    def clear_index_sql(self):
        return f"CLEAR INDEX IF EXISTS {self.name}"


def parse_indexes_structure(indexes: Optional[List[str]]) -> List[TableIndex]:
    """
    >>> parse_indexes_structure(["index_name a TYPE set(100) GRANULARITY 100", "index_name_bf mapValues(d) TYPE bloom_filter(0.001) GRANULARITY 16"])
    [TableIndex(name='index_name', expr='a', type_full='set(100)', granularity='100'), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter(0.001)', granularity='16')]
    >>> parse_indexes_structure(["INDEX index_name a TYPE set(100) GRANULARITY 100", " INDEX  index_name_bf mapValues(d) TYPE bloom_filter(0.001) GRANULARITY 16"])
    [TableIndex(name='index_name', expr='a', type_full='set(100)', granularity='100'), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter(0.001)', granularity='16')]
    >>> parse_indexes_structure(["index_name type TYPE set(100) GRANULARITY 100", "index_name_bf mapValues(d) TYPE bloom_filter(0.001) GRANULARITY 16"])
    [TableIndex(name='index_name', expr='type', type_full='set(100)', granularity='100'), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter(0.001)', granularity='16')]
    >>> parse_indexes_structure(["index_name a TYPE set(100) GRANULARITY 100,", "index_name_bf mapValues(d) TYPE bloom_filter(0.001) GRANULARITY 16"])
    [TableIndex(name='index_name', expr='a', type_full='set(100)', granularity='100'), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter(0.001)', granularity='16')]
    >>> parse_indexes_structure(["index_name a TYPE set(100)", "index_name_bf mapValues(d) TYPE bloom_filter(0.001)"])
    [TableIndex(name='index_name', expr='a', type_full='set(100)', granularity=None), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter(0.001)', granularity=None)]
    >>> parse_indexes_structure(["index_name u64 * length(s) TYPE set(100)", "index_name_bf mapValues(d) TYPE bloom_filter"])
    [TableIndex(name='index_name', expr='u64 * length(s)', type_full='set(100)', granularity=None), TableIndex(name='index_name_bf', expr='mapValues(d)', type_full='bloom_filter', granularity=None)]
    >>> parse_indexes_structure(["index_name path TYPE ngrambf_v1(4,1024,1,42) GRANULARITY 1"])
    [TableIndex(name='index_name', expr='path', type_full='ngrambf_v1(4,1024,1,42)', granularity='1')]
    >>> parse_indexes_structure(["index_name path TYPE ngrambf_v1(4, 1024, 1, 42) GRANULARITY 1"])
    [TableIndex(name='index_name', expr='path', type_full='ngrambf_v1(4, 1024, 1, 42)', granularity='1')]
    >>> parse_indexes_structure(["index_name u64 * length(s)"])
    Traceback (most recent call last):
    ...
    tinybird.datafile.common.IndexesSyntaxError: Invalid INDEX syntax at 1:1.
    Usage: `[INDEX] name expr TYPE type_full GRANULARITY granularity`.

    >>> parse_indexes_structure(["index_name a TYPE set(100) GRANULARITY 100, index_name_bf mapValues(d) TYPE bloom_filter(0.001) GRANULARITY 16"])
    Traceback (most recent call last):
    ...
    tinybird.datafile.common.IndexesSyntaxError: Invalid INDEX syntax at 1:1.
    Usage: `[INDEX] name expr TYPE type_full GRANULARITY granularity`.

    >>> parse_indexes_structure(["", "    ", "     wrong_index_syntax,"])
    Traceback (most recent call last):
    ...
    tinybird.datafile.common.IndexesSyntaxError: Invalid INDEX syntax at 3:6.
    Usage: `[INDEX] name expr TYPE type_full GRANULARITY granularity`.

    >>> parse_indexes_structure(["my_index m['key'] TYPE ngrambf_v1(1, 1024, 1, 42) GRANULARITY 1"])
    [TableIndex(name='my_index', expr="m['key']", type_full='ngrambf_v1(1, 1024, 1, 42)', granularity='1')]
    >>> parse_indexes_structure(["my_index_lambda arrayMap(x -> tupleElement(x,'message'), column_name) TYPE ngrambf_v1(1, 1024, 1, 42) GRANULARITY 1"])
    [TableIndex(name='my_index_lambda', expr="arrayMap(x -> tupleElement(x,'message'), column_name)", type_full='ngrambf_v1(1, 1024, 1, 42)', granularity='1')]
    >>> parse_indexes_structure(["ip_range_minmax_idx (toIPv6(ip_range_start), toIPv6(ip_range_end)) TYPE minmax GRANULARITY 1"])
    [TableIndex(name='ip_range_minmax_idx', expr='(toIPv6(ip_range_start), toIPv6(ip_range_end))', type_full='minmax', granularity='1')]
    """
    parsed_indices: List[TableIndex] = []
    if not indexes:
        return parsed_indices

    # TODO(eclbg): It might not be obvious that we only allow one index per line.
    for i, index in enumerate(indexes):
        lineno = i + 1
        if not index.strip():
            continue
        leading_whitespaces = len(index) - len(index.lstrip())
        index = index.strip().rstrip(",")
        index = index.lstrip("INDEX").strip()
        if index.count("TYPE") != 1:
            raise IndexesSyntaxError(
                message="Invalid INDEX syntax",
                hint="Usage: `[INDEX] name expr TYPE type_full GRANULARITY granularity`",
                lineno=lineno,
                pos=leading_whitespaces + 1,
            )

        match = re.match(
            r"(\w+)\s+([\w\s*\[\]\*\(\),\'\"-><.]+)\s+TYPE\s+(\w+)(?:\(([\w\s*.,]+)\))?(?:\s+GRANULARITY\s+(\d+))?",
            index,
        )
        if match:
            index_name, a, index_type, value, granularity = match.groups()
            index_expr = f"{index_type}({value})" if value else index_type
            parsed_indices.append(TableIndex(index_name, a.strip(), f"{index_expr}", granularity))
        else:
            raise IndexesSyntaxError(
                message="Invalid INDEX syntax",
                hint="Usage: `[INDEX] name expr TYPE type_full GRANULARITY granularity`",
                lineno=1,
                pos=leading_whitespaces + 1,
            )
    return parsed_indices


def clean_comments_rstrip_keep_empty_lines(schema_to_clean: Optional[str]) -> str:
    """Remove the comments from the schema
    If the comments are between backticks, they will not be removed.
    Lines that are empty after removing comments are also removed. Lines are only rstripped of whitespaces
    >>> clean_comments_rstrip_keep_empty_lines(None)
    ''
    >>> clean_comments_rstrip_keep_empty_lines('')
    ''
    >>> clean_comments_rstrip_keep_empty_lines('    ')
    ''
    >>> clean_comments_rstrip_keep_empty_lines('\\n')
    ''
    >>> clean_comments_rstrip_keep_empty_lines('\\n\\n\\n\\n')
    ''
    >>> clean_comments_rstrip_keep_empty_lines('c Float32')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a comment')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a comment\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\t-- this is a comment\\t\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a comment\\r\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a comment\\n--this is a comment2\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a ```comment\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32\\n--this is a ```comment\\n')
    'c Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32, -- comment\\nd Float32 -- comment2')
    'c Float32,\\nd Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32, -- comment\\n   -- comment \\nd Float32 -- comment2')
    'c Float32,\\n\\nd Float32'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32 `json:$.aa--aa`\\n--this is a ```comment\\n')
    'c Float32 `json:$.aa--aa`'
    >>> clean_comments_rstrip_keep_empty_lines('c Float32 `json:$.cc--cc`\\nd Float32 `json:$.dd--dd`\\n--this is a ```comment\\n')
    'c Float32 `json:$.cc--cc`\\nd Float32 `json:$.dd--dd`'
    >>> clean_comments_rstrip_keep_empty_lines('c--c Float32 `json:$.cc--cc`\\n')
    'c'
    >>> clean_comments_rstrip_keep_empty_lines('`c--c` Float32 `json:$.cc--cc`\\n')
    '`c'
    """

    def clean_line_comments(line: str) -> str:
        if not line:
            return line
        i = 0
        inside_json_path = False
        while i < len(line):
            if i + 1 < len(line) and line[i] == "-" and line[i + 1] == "-" and not inside_json_path:
                return line[:i].rstrip()

            if not inside_json_path and line[i:].startswith("`json:"):
                inside_json_path = True
            elif inside_json_path and line[i] == "`":
                inside_json_path = False
            i += 1
        return line

    if schema_to_clean is None:
        return ""

    cleaned_schema = ""
    for line in schema_to_clean.splitlines():
        cleaned_line = clean_line_comments(line)
        cleaned_schema += cleaned_line + "\n"
    return cleaned_schema.rstrip()


SyntaxExpr = namedtuple("SyntaxExpr", ["name", "regex"])

NULL = SyntaxExpr("NULL", re.compile(r"\s+NULL([^a-z0-9_]|$)", re.IGNORECASE))
NOTNULL = SyntaxExpr("NOTNULL", re.compile(r"\s+NOT\s+NULL([^a-z0-9_]|$)", re.IGNORECASE))
DEFAULT = SyntaxExpr("DEFAULT", re.compile(r"\s+DEFAULT([^a-z0-9_]|$)", re.IGNORECASE))
MATERIALIZED = SyntaxExpr("MATERIALIZED", re.compile(r"\s+MATERIALIZED([^a-z0-9_]|$)", re.IGNORECASE))
ALIAS = SyntaxExpr("ALIAS", re.compile(r"\s+ALIAS([^a-z0-9_]|$)", re.IGNORECASE))
CODEC = SyntaxExpr("CODEC", re.compile(r"\s+CODEC([^a-z0-9_]|$)", re.IGNORECASE))
TTL = SyntaxExpr("TTL", re.compile(r"\s+TTL([^a-z0-9_]|$)", re.IGNORECASE))
JSONPATH = SyntaxExpr("JSONPATH", re.compile(r"\s+`json:", re.IGNORECASE))
COMMA = SyntaxExpr("COMMA", re.compile(r",", re.IGNORECASE))
NEW_LINE = SyntaxExpr("NEW_LINE", re.compile(r"\s$"))
TYPE = SyntaxExpr("TYPE", re.compile(r""))  # TYPE doesn't have a fixed initial string

REGEX_WHITESPACE = re.compile(r"\s*")
REGEX_COMMENT = re.compile(r"\-\-[^\n\r]*[\n\r]")


def mark_error_string(s: str, i: int, line: int = 1) -> str:
    """
    >>> mark_error_string('0123456789', 0)
    '0123456789\\n^---'
    >>> mark_error_string('0123456789', 9)
    '0123456789\\n         ^---'
    >>> mark_error_string('01234\\n56789', 1)
    '01234\\n ^---'
    """
    marker = "^---"
    ss = s.splitlines()[line - 1] if s else ""
    start = 0
    end = len(ss)
    return ss[start:end] + "\n" + (" " * (i - start)) + marker


def format_parse_error(
    table_structure: str,
    i: int,
    position: int,
    hint: Optional[str] = None,
    line: int = 0,
    keyword: Optional[str] = None,
) -> str:
    adjusted_position = position - (len(keyword) if keyword else 0)
    message = f"{hint}\n" if hint else ""
    message += mark_error_string(table_structure, adjusted_position - 1, line=line)

    if keyword:
        message += f" found at position {adjusted_position - len(keyword)}"
    else:
        message += (
            f" found {repr(table_structure[i]) if len(table_structure) > i else 'EOF'} at position {adjusted_position}"
        )
    return message


def clean_line_comments(line: str) -> str:
    if not line:
        return line
    i = 0
    inside_json_path = False
    while i < len(line):
        if i + 1 < len(line) and line[i] == "-" and line[i + 1] == "-" and not inside_json_path:
            return line[:i].strip()

        if not inside_json_path and line[i:].startswith("`json:"):
            inside_json_path = True
        elif inside_json_path and line[i] == "`":
            inside_json_path = False
        i += 1
    return line


def _parse_table_structure(schema: str) -> List[Dict[str, Any]]:
    # CH syntax from https://clickhouse.com/docs/en/sql-reference/statements/create/table/
    # name1 [type1] [NULL|NOT NULL] [DEFAULT|MATERIALIZED|ALIAS expr1] [compression_codec] [TTL expr1]
    try:
        # This removes lines that are empty after removing comments, which might make it hard to locate errors properly.
        # The parsing code afterwards seems to be mostly robust to empty lines.
        # Perhaps I'll deliberately not support reporting errors correctly when empty lines have been removed to start
        # with, and later I can see how to support it.
        # It also removes the indentation of the lines, which might make it hard to locate errors properly.
        # schema = clean_comments(schema + "\n")

        # I've swapped the above with this. A first test didn't show any side effects in parsing a schema, and it should
        # allow us to keep track of the line numbers in the error messages.
        schema = clean_comments_rstrip_keep_empty_lines(schema + "\n")
    except Exception:
        # logging.exception(f"Error cleaning comments: {e}")
        schema = REGEX_COMMENT.sub(" ", schema + "\n").strip()

    if REGEX_WHITESPACE.fullmatch(schema):
        return []

    i: int = 0

    # For error feedback only
    line: int = 1
    pos: int = 1

    # Find the first SyntaxExpr in lookup that matches the schema at the current offset
    def lookahead_matches(lookup: Iterable) -> Optional[SyntaxExpr]:
        s = schema[i:]
        match = next((x for x in lookup if x.regex.match(s)), None)
        return match

    def advance_single_char() -> None:
        nonlocal i, line, pos
        if schema[i] == "\n":
            line += 1
            pos = 1
        else:
            pos += 1
        i += 1

    # Advance all whitespaces characters and then len(s) more chars
    def advance(s: str) -> None:
        if i < len(schema):
            while schema[i] in " \t\r\n":
                advance_single_char()
            for _ in s:
                advance_single_char()

    def get_backticked() -> str:
        begin = i
        while i < len(schema):
            c = schema[i]
            advance_single_char()
            if c == "`":
                return schema[begin : i - 1]
            if c in " \t\r\n":
                raise SchemaSyntaxError(message="Expected closing backtick", lineno=line, pos=pos - 1)
        raise SchemaSyntaxError(message="Expected closing backtick", lineno=line, pos=pos)

    def parse_name() -> str:
        nonlocal i, line, pos
        if schema[i] != "`":
            # regular name
            begin = i
            while i < len(schema):
                c = schema[i]
                if c in " \t\r\n":
                    return schema[begin:i]
                if c not in valid_chars_name:
                    raise SchemaSyntaxError(
                        message=f"Column name contains invalid character {repr(c)}",
                        hint="Hint: use backticks",
                        lineno=line,
                        pos=pos,
                    )
                advance_single_char()
            return schema[begin:i]
        else:
            # backticked name
            advance_single_char()
            return get_backticked()

    def parse_expr(lookup: Iterable[SyntaxExpr], attribute: str) -> str:
        """Parse an expression for an attribute.

        The name of the attribute is used to generate the error message.
        """
        nonlocal i, line, pos

        begin: int = i
        context_stack: List[Optional[str]] = [None]
        while i < len(schema):
            context = context_stack[-1]
            c = schema[i]

            if (context == "'" and c == "'") or (context == '"' and c == '"') or (context == "(" and c == ")"):
                context_stack.pop()
            elif c == "'" and (context is None or context == "("):
                context_stack.append("'")
            elif c == '"' and (context is None or context == "("):
                context_stack.append('"')
            elif c == "(" and (context is None or context == "("):
                context_stack.append("(")
            elif context is None and lookahead_matches(lookup):
                if i == begin:
                    # This happens when we're parsing a column and an expr is missing for an attribute that requires it,
                    # like DEFAULT or CODEC. For example:
                    # SCHEMA >
                    #     timestamp DateTime DEFAULT,
                    #     col_b Int32
                    raise SchemaSyntaxError(
                        message=f"Missing mandatory value for {attribute}",
                        lineno=line,
                        pos=pos,
                    )
                return schema[begin:i].strip(" \t\r\n")
            elif (context is None and c not in valid_chars_fn) or (context == "(" and c not in valid_chars_fn):
                raise SchemaSyntaxError(message=f"Invalid character {repr(c)}", lineno=line, pos=pos)
            advance_single_char()

        # Check for unclosed contexts before returning
        if len(context_stack) > 1:
            last_context = context_stack[-1]
            closing_char = "'" if last_context == "'" else ('"' if last_context == '"' else ")")
            raise SchemaSyntaxError(message=f"Expected closing {closing_char}", lineno=line, pos=pos)

        if i == begin:
            # This happens when we're parsing a column and an expr is missing for an attribute that requires it, like
            # DEFAULT or CODEC, and we reach the end of the schema. For example:
            # SCHEMA >
            #     timestamp DateTime DEFAULT
            raise SchemaSyntaxError(
                message=f"Missing mandatory value for {attribute}",
                lineno=line,
                pos=pos,
            )
        return schema[begin:].strip(" \t\r\n")

    columns: List[Dict[str, Any]] = []

    name: str = ""
    _type: str = ""
    default: str = ""
    codec: str = ""
    jsonpath: str = ""
    last: Optional[SyntaxExpr] = None
    col_start: Tuple[int, int] = (0, 0)  # (0, 0) means not set. It's not a valid line/pos as they start at 1
    col_end: Tuple[int, int] = (0, 0)  # (0, 0) means not set. It's not a valid line/pos as they start at 1

    def add_column(found: str) -> None:
        nonlocal name, _type, default, codec, jsonpath, col_start, col_end
        lineno, pos = col_start
        default = "" if not default else f"DEFAULT {default}"
        codec = "" if not codec else f"CODEC{codec}"
        if not name or not (_type or default):
            raise SchemaSyntaxError(
                message="Column name and either type or DEFAULT are required",
                lineno=lineno,
                pos=pos,
            )
        columns.append(
            {
                "name": name,
                "type": _type,
                "codec": codec,
                "default_value": default,
                "jsonpath": jsonpath,
                # "col_start": col_start,
                # "col_end": col_end,
            }
        )
        name = ""
        _type = ""
        default = ""
        codec = ""
        jsonpath = ""

    valid_next: List[SyntaxExpr] = [TYPE]
    while i < len(schema):
        if not name:
            advance("")
            valid_next = [NULL, NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA, TYPE]
            col_start = (line, pos)
            name = parse_name()
            if name == "INDEX":
                raise SchemaSyntaxError(
                    message="Forbidden INDEX definition",
                    hint="Indexes are not allowed in SCHEMA section. Use the INDEXES section instead",
                    lineno=line,
                    pos=pos - len(name),  # We've already advanced the name
                )
            continue
        found = lookahead_matches(
            [NULL, NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA, NEW_LINE, TYPE]
        )
        if found and found not in valid_next:
            after = f" after {last.name}" if last else ""
            raise SchemaSyntaxError(message=f"Unexpected {found.name}{after}", lineno=line, pos=pos)
        if found == TYPE:
            advance("")
            valid_next = [NULL, NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA, NEW_LINE]
            type_start_pos = pos  # Save the position of the type start to use it in the error message
            detected_type = parse_expr(
                [NULL, NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA], "TYPE"
            )

            # Boolean type is supported in ClickHouse but its behavior is strange and will lead to unexpected results.
            # Better to use Bool or UInt8 instead. An example:
            #
            # SELECT
            #     CAST(true, 'Boolean') AS bool,
            #     toTypeName(bool)
            #
            # ┌─bool─┬─toTypeName(bool)─┐
            # │ true │ Bool             │
            # └──────┴──────────────────┘
            if "boolean" in detected_type.lower():
                raise SchemaSyntaxError(
                    message="Boolean type is not supported",
                    hint="Hint: use Bool or UInt8 instead",
                    lineno=line,
                    pos=pos,
                )
            if "datetime64" in detected_type.lower() and "datetime64(" not in detected_type.lower():
                raise SchemaSyntaxError(
                    message="DateTime64 type without precision is not supported",
                    hint="Hint: use DateTime64(3) instead",
                    lineno=line,
                    pos=pos,
                )
            if detected_type in ("Int", "UInt"):
                t = detected_type
                raise SchemaSyntaxError(
                    message=f"Precision is mandatory for {t} types",
                    hint=f"Hint: use one of {t}8, {t}16, {t}32, {t}64, {t}128, {t}256",
                    lineno=line,
                    pos=pos - len(t),
                )

            try:
                # Imported in the body to be compatible with the CLI
                from chtoolset.query import check_compatible_types

                # Check compatibility of the type with itself to verify it's a known type
                check_compatible_types(detected_type, detected_type)
            except ValueError as e:
                if (
                    "unknown data type family" in str(e).lower()
                    or "incompatible data types between aggregate function" in str(e).lower()
                ):
                    raise SchemaSyntaxError(message=str(e), lineno=line, pos=type_start_pos)
                else:
                    # TODO(eclbg): The resulting error message is a bit confusing, as the clickhouse error contains some
                    # references to positions that don't match the position in the schema.
                    raise SchemaSyntaxError(f"Error parsing type: {e}", lineno=line, pos=type_start_pos)
            except ModuleNotFoundError:
                pass
            _type = detected_type
        elif found == NULL:
            # Not implemented
            advance("")  # We need to advance to get the correct position
            raise SchemaSyntaxError(
                message="NULL column syntax not supported",
                hint="Hint: use Nullable(...)",
                lineno=line,
                pos=pos,
            )
        elif found == NOTNULL:
            advance("")  # We need to advance to get the correct position
            raise SchemaSyntaxError(
                message="NOT NULL column syntax not supported",
                hint="Hint: Columns are not nullable by default",
                lineno=line,
                pos=pos,
            )
        elif found == DEFAULT:
            advance("DEFAULT")
            valid_next = [
                CODEC,
                COMMA,
                JSONPATH,
                # The matches below are not supported. We're adding them here to say they aren't, instead of just
                # complaining about their placement.
                MATERIALIZED,
                TTL,
                NULL,
                NOTNULL,
            ]
            default = parse_expr([NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA], "DEFAULT")
        elif found == MATERIALIZED:
            advance("")
            raise SchemaSyntaxError(
                message="MATERIALIZED columns are not supported",
                lineno=line,
                pos=pos,
            )
        elif found == ALIAS:
            # Not implemented
            advance("")  # We need to advance to get the correct position
            raise SchemaSyntaxError(
                message="ALIAS columns are not supported",
                lineno=line,
                pos=pos,
            )
        elif found == CODEC:
            advance("CODEC")
            valid_next = [
                COMMA,
                JSONPATH,
                # The matches below are not supported. We're adding them here to say they aren't, instead of just
                # complaining about their placement.
                MATERIALIZED,
                TTL,
                NULL,
                NOTNULL,
            ]
            codec = parse_expr([NOTNULL, DEFAULT, MATERIALIZED, ALIAS, CODEC, TTL, JSONPATH, COMMA], "CODEC")
        elif found == TTL:
            advance("")  # We need to advance to get the correct position
            # Not implemented
            advance("")
            raise SchemaSyntaxError(
                message="column TTL is not supported",
                lineno=line,
                pos=pos,
            )
        elif found == JSONPATH:
            advance("`json:")
            jsonpath = get_backticked()
        elif found == COMMA:
            advance(",")
            valid_next = []
            col_end = (line, pos)
            add_column("COMMA")
        elif found == NEW_LINE:
            i += 1
        else:
            # Note(eclbg): I haven't found any case where this error is raised.
            raise ValueError(
                format_parse_error(
                    schema,
                    i,
                    pos,
                    "wrong value. Expected a data type, DEFAULT, CODEC, a jsonpath, a comma, or a new line",
                    line=line,
                )
            )
        last = found
    col_end = (line, i + 1)
    # Only add the last column if we've parsed something. This allows for a trailing comma after the last column.
    if name:
        add_column("EOF")

    # normalize columns
    for column in columns:
        nullable = column["type"].lower().startswith("nullable")
        column["type"] = column["type"] if not nullable else column["type"][len("Nullable(") : -1]  # ')'
        column["nullable"] = nullable
        column["codec"] = column["codec"] if column["codec"] else None
        column["name"] = column["name"]
        column["normalized_name"] = column["name"]
        column["jsonpath"] = column["jsonpath"] if column["jsonpath"] else None
        default_value = column["default_value"] if column["default_value"] else None
        if nullable and default_value and default_value.lower() == "default null":
            default_value = None
        column["default_value"] = default_value
    return columns


def try_to_fix_nullable_in_simple_aggregating_function(t: str) -> Optional[str]:
    # This workaround is to fix: https://github.com/ClickHouse/ClickHouse/issues/34407.
    # In the case of nullable columns and SimpleAggregateFunction  Clickhouse returns
    # Nullable(SimpleAggregateFunction(sum, Int32)) instead of SimpleAggregateFunction(sum, Nullable(Int32))
    # as it is done with other aggregate functions.
    # If not, the aggregation could return incorrect results.
    result = None
    if match := re.search(r"SimpleAggregateFunction\((\w+),\s*(?!(?:Nullable))([\w,.()]+)\)", t):
        fn = match.group(1)
        inner_type = match.group(2)
        result = f"SimpleAggregateFunction({fn}, Nullable({inner_type}))"
    return result


def col_name(name: str, backquotes: bool = True) -> str:
    """
    >>> col_name('`test`', True)
    '`test`'
    >>> col_name('`test`', False)
    'test'
    >>> col_name('test', True)
    '`test`'
    >>> col_name('test', False)
    'test'
    >>> col_name('', True)
    ''
    >>> col_name('', False)
    ''
    """
    if not name:
        return name
    if name[0] == "`" and name[-1] == "`":
        return name if backquotes else name[1:-1]
    return f"`{name}`" if backquotes else name


def schema_to_sql_columns(schema: List[Dict[str, Any]]) -> List[str]:
    """return an array with each column in SQL
    >>> schema_to_sql_columns([{'name': 'temperature', 'type': 'Float32', 'codec': None, 'default_value': None, 'nullable': False, 'normalized_name': 'temperature'}, {'name': 'temperature_delta', 'type': 'Float32', 'codec': 'CODEC(Delta(4), LZ4))', 'default_value': 'MATERIALIZED temperature', 'nullable': False, 'normalized_name': 'temperature_delta'}])
    ['`temperature` Float32', '`temperature_delta` Float32 MATERIALIZED temperature CODEC(Delta(4), LZ4))']
    >>> schema_to_sql_columns([{'name': 'temperature_delta', 'type': 'Float32', 'codec': '', 'default_value': 'MATERIALIZED temperature', 'nullable': False, 'normalized_name': 'temperature_delta'}])
    ['`temperature_delta` Float32 MATERIALIZED temperature']
    >>> schema_to_sql_columns([{'name': 'temperature_delta', 'type': 'Float32', 'codec': 'CODEC(Delta(4), LZ4))', 'default_value': '', 'nullable': False, 'normalized_name': 'temperature_delta'}])
    ['`temperature_delta` Float32 CODEC(Delta(4), LZ4))']
    >>> schema_to_sql_columns([{'name': 'temperature_delta', 'type': 'Float32', 'nullable': False, 'normalized_name': 'temperature_delta'}])
    ['`temperature_delta` Float32']
    >>> schema_to_sql_columns([{'name': 'temperature_delta', 'type': 'Float32', 'nullable': False, 'normalized_name': 'temperature_delta', 'jsonpath': '$.temperature_delta'}])
    ['`temperature_delta` Float32 `json:$.temperature_delta`']
    >>> schema_to_sql_columns([{'name': 'aggregation', 'type': 'SimpleAggregateFunction(sum, Int32)', 'nullable': True, 'normalized_name': 'aggregation', 'jsonpath': '$.aggregation'}])
    ['`aggregation` SimpleAggregateFunction(sum, Nullable(Int32)) `json:$.aggregation`']
    """
    columns: List[str] = []
    for x in schema:
        name = x["normalized_name"] if "normalized_name" in x else x["name"]
        if x["nullable"]:
            if (_type := try_to_fix_nullable_in_simple_aggregating_function(x["type"])) is None:
                _type = "Nullable(%s)" % x["type"]
        else:
            _type = x["type"]
        parts = [col_name(name, backquotes=True), _type]
        if x.get("jsonpath", None):
            parts.append(f"`json:{x['jsonpath']}`")
        if "default_value" in x and x["default_value"] not in ("", None):
            parts.append(x["default_value"])
        if "codec" in x and x["codec"] not in ("", None):
            parts.append(x["codec"])
        c = " ".join([x for x in parts if x]).strip()
        columns.append(c)
    return columns


def parse_table_structure(schema: str) -> List[Dict[str, Any]]:
    """Parse a table schema definition into a structured format.
    Columns follow the syntax: name [type] [DEFAULT expr] [CODEC codec] [JSONPATH `json:jsonpath`] [,]

    Args:
        schema: The schema definition string

    Returns:
        List of dictionaries containing column definitions

    Examples:
        >>> parse_table_structure('')  # Empty schema
        []

        >>> parse_table_structure('col Int32')  # Basic column
        [{'name': 'col', 'type': 'Int32', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

        >>> parse_table_structure('col1 Int32, col2 String')  # Multiple columns
        [{'name': 'col1', 'type': 'Int32', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col1'}, {'name': 'col2', 'type': 'String', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col2'}]

        >>> parse_table_structure('col Int32 DEFAULT 0')  # With DEFAULT
        [{'name': 'col', 'type': 'Int32', 'codec': None, 'default_value': 'DEFAULT 0', 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

        >>> parse_table_structure('col DEFAULT 42')  # Column without type but with default
        [{'name': 'col', 'type': '', 'codec': None, 'default_value': 'DEFAULT 42', 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

        >>> parse_table_structure('col String CODEC(ZSTD)')  # With CODEC
        [{'name': 'col', 'type': 'String', 'codec': 'CODEC(ZSTD)', 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

        >>> parse_table_structure('`column.name!@#$%` String')  # Quoted identifier
        [{'name': 'column.name!@#$%', 'type': 'String', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'column.name!@#$%'}]

        >>> parse_table_structure('col Nullable(Int32)')  # Nullable type
        [{'name': 'col', 'type': 'Int32', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': True, 'normalized_name': 'col'}]

        >>> parse_table_structure('col Array(Int32)')  # Complex type
        [{'name': 'col', 'type': 'Array(Int32)', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

        >>> parse_table_structure('col SimpleAggregateFunction(any, Int32)')  # Aggregate function
        [{'name': 'col', 'type': 'SimpleAggregateFunction(any, Int32)', 'codec': None, 'default_value': None, 'jsonpath': None, 'nullable': False, 'normalized_name': 'col'}]

    Error cases:
        >>> parse_table_structure('col')  # Missing type
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Column name and either type or DEFAULT are required at 1:1.

        >>> parse_table_structure('`col Int32')  # Unclosed backtick
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Expected closing backtick at 1:5.

        >>> parse_table_structure('col Int32 DEFAULT')  # Missing DEFAULT value
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Missing mandatory value for DEFAULT at 1:18.

        >>> parse_table_structure('col Int32 CODEC')  # Missing CODEC parameters
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Missing mandatory value for CODEC at 1:16.

        >>> parse_table_structure('col#name Int32')  # Invalid character in name
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Column name contains invalid character '#' at 1:4.
        Hint: use backticks.

        >>> parse_table_structure('col Int32 MATERIALIZED expr')  # Unsupported MATERIALIZED
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: MATERIALIZED columns are not supported at 1:11.

        >>> parse_table_structure('col Int32 TTL timestamp + INTERVAL 1 DAY')  # Unsupported TTL
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: column TTL is not supported at 1:11.

        >>> parse_table_structure('col Int32 NULL')  # Unsupported NULL
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: NULL column syntax not supported at 1:11.
        Hint: use Nullable(...).

        >>> parse_table_structure('col Int32 NOT NULL')  # Unsupported NOT NULL
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: NOT NULL column syntax not supported at 1:11.
        Hint: Columns are not nullable by default.

        >>> parse_table_structure('''
        ...     col Array(Int32)
        ...         CODEC(
        ...             ZSTD''')  # Unclosed CODEC parenthesis across lines
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Expected closing ) at 4:17.

        >>> parse_table_structure('''
        ...     timestamp DateTime
        ...         DEFAULT
        ...         CODEC(ZSTD)''')  # Missing DEFAULT value with following CODEC
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: Missing mandatory value for DEFAULT at 3:16.

        >>> parse_table_structure('''
        ...     col String
        ...         DEFAULT 'test'
        ...             MATERIALIZED
        ...                 now()''')  # MATERIALIZED with heavy indentation
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: MATERIALIZED columns are not supported at 4:13.

        >>> parse_table_structure('''
        ...     `column.with.dots`
        ...              Int32
        ...                  TTL
        ...                      timestamp + INTERVAL 1 DAY''')  # TTL with increasing indentation
        Traceback (most recent call last):
        ...
        tinybird.datafile.common.SchemaSyntaxError: column TTL is not supported at 4:18.
    """
    return _parse_table_structure(schema)


@dataclass
class DatafileParseWarning:
    message: str

    def __str__(self) -> str:
        return self.message


class ParseResult(NamedTuple):
    datafile: Datafile
    warnings: list[DatafileParseWarning]


def parse(
    s: str,
    kind: DatafileKind,
    default_node: Optional[str] = None,
    basepath: str = ".",
    replace_includes: bool = True,
    # TODO(eclbg): I think we could remove `skip_eval` in Forward, and pin it to False. This would let us remove some
    # other functions like `eval_var` that obscure things a bit.
    skip_eval: bool = False,
) -> ParseResult:
    lines = list(StringIO(s, newline=None))

    doc = Datafile()
    warnings: List[DatafileParseWarning] = []

    if kind is not None:
        doc.set_kind(kind)
    doc.raw = list(StringIO(s, newline=None))

    parser_state = namedtuple(
        "parser_state", ["multiline", "current_node", "command", "multiline_string", "is_sql", "start_lineno"]
    )

    parser_state.multiline = False
    parser_state.current_node = False
    parser_state.start_lineno = None

    def multiline_not_supported(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def error_if_multiline(*args: Any, **kwargs: Any) -> Any:
            if parser_state.multiline:
                parser_state.multiline = (
                    False  # So we don't offset the line number when processing the exception. A bit hacky
                )
                raise DatafileSyntaxError(
                    f"{kwargs['cmd'].upper()} does not support multiline arguments",
                    lineno=parser_state.start_lineno,  # We want to report the line where the command starts
                    pos=1,
                )
            return func(*args, **kwargs)

        return error_if_multiline

    def deprecated(severity: Literal["error", "warning"]) -> Callable[..., Any]:
        def inner(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def raise_deprecation_error(*args: Any, **kwargs: Any) -> Any:
                raise DatafileSyntaxError(
                    f"{kwargs['cmd'].upper()} has been deprecated",
                    lineno=kwargs["lineno"],
                    pos=1,
                )

            @functools.wraps(func)
            def add_deprecation_warning(*args: Any, **kwargs: Any) -> Any:
                warnings.append(
                    DatafileParseWarning(
                        message=f"{kwargs['cmd'].upper()} has been deprecated and will be ignored.",
                    )
                )

            if severity == "error":
                return raise_deprecation_error
            elif severity == "warning":
                return add_deprecation_warning

        return inner

    def not_supported_yet(extra_message: str = "") -> Callable[..., Any]:
        def inner(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def raise_not_supported_yet_error(*args: Any, **kwargs: Any) -> Any:
                extra_message_bit = f". {extra_message}" if extra_message else ""
                raise DatafileSyntaxError(
                    f"{kwargs['cmd']} is not supported yet{extra_message_bit}",
                    lineno=kwargs["lineno"],
                    pos=1,
                )

            return raise_not_supported_yet_error

        return inner

    def assign(attr):
        @multiline_not_supported
        def _fn(x, **kwargs):
            setattr(doc, attr, _unquote(x))

        return _fn

    def schema(*args, **kwargs):
        s = _unquote("".join(args))
        try:
            sh = parse_table_structure(s)
        except SchemaSyntaxError as e:
            raise e
        except Exception as e:
            # TODO(eclbg): Does it make sense to keep this exception? I'd like to get rid of all ParseException
            raise ParseException(FeedbackManager.error_parsing_schema(line=kwargs["lineno"], error=e))

        parser_state.current_node["schema"] = ",".join(schema_to_sql_columns(sh))
        parser_state.current_node["columns"] = sh

    def indexes(*args, **kwargs):
        s = _unquote("".join(args))
        if not s:
            return
        try:
            indexes = parse_indexes_structure(s.splitlines())
        except IndexesSyntaxError as e:
            raise e
        except Exception as e:
            # TODO(eclbg): We get here when an unidentified error happens but we still report a parsing error. We should
            # rethink this.
            raise ParseException(FeedbackManager.error_parsing_indices(line=kwargs["lineno"], error=e))

        parser_state.current_node["indexes"] = indexes

    def assign_var(v: str, allowed_values: Optional[set[str]] = None) -> Callable[[VarArg(str), KwArg(Any)], None]:
        @multiline_not_supported
        def _f(*args: str, **kwargs: Any):
            s = _unquote((" ".join(args)).strip())
            val = eval_var(s, skip=skip_eval)
            if allowed_values and val.lower() not in {v.lower() for v in allowed_values}:
                raise DatafileSyntaxError(
                    f"{val} is not an allowed value for {kwargs['cmd'].upper()}. Use one of: {allowed_values}",
                    lineno=kwargs["lineno"],
                    pos=1,
                )
            parser_state.current_node[v.lower()] = val

        return _f

    def assign_var_json(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        @multiline_not_supported
        def _f(*args: str, **kwargs: Any):
            s = _unquote((" ".join(args)).strip())
            tmp = eval_var(s, skip=skip_eval)
            struct = json.loads(tmp)
            parser_state.current_node[v.lower()] = struct

        return _f

    def kafka_key_avro_deserialization_deprecated(*args: str, **kwargs: Any):
        raise DatafileSyntaxError(
            f'{kwargs["cmd"].upper()} has been deprecated. Use "KAFKA_KEY_FORMAT avro" in the corresponding .datasource file instead',
            lineno=kwargs["lineno"],
            pos=1,
        )

    def kafka_target_partitions_deprecated(*args: str, **kwargs: Any):
        warnings.append(
            DatafileParseWarning(
                message=f"{kwargs['cmd'].upper()} has been deprecated and will be ignored.",
            )
        )

    def import_external_datasource_deprecated(*args: str, **kwargs: Any):
        warnings.append(
            DatafileParseWarning(
                message=f"{kwargs['cmd'].upper()} has been deprecated and will be ignored.",
            )
        )

    def import_service_deprecated(*args: str, **kwargs: Any):
        warnings.append(
            DatafileParseWarning(
                message=(
                    f"{kwargs['cmd'].upper()} has been deprecated and will be ignored. If you're using an S3 or GCS "
                    "connection, you don't need this setting anymore."
                )
            )
        )

    def import_strategy_deprecated(*args: str, **kwargs: Any):
        raise DatafileSyntaxError(
            f"{kwargs['cmd'].upper()} has been deprecated. It is now fixed to 'append'",
            lineno=kwargs["lineno"],
            pos=1,
        )

    def kafka_store_binary_headers_deprecated(*args: str, **kwargs: Any):
        raise DatafileSyntaxError(
            f"{kwargs['cmd'].upper()} has been deprecated. When KAFKA_STORE_HEADERS is True, __headers is always of type Map(String, String)",
            lineno=kwargs["lineno"],
            pos=1,
        )

    def export_service(*args: str, **kwargs: Any):
        warnings.append(
            DatafileParseWarning(
                message=(
                    f"{kwargs['cmd'].upper()} has been deprecated and will be ignored. If you're using an S3 or GCS "
                    "connection, you don't need this setting anymore."
                )
            )
        )

    @deprecated(severity="error")
    def sources(x: str, **kwargs: Any) -> None:
        pass  # Deprecated

    @multiline_not_supported
    def node(*args: str, **kwargs: Any) -> None:
        node = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(node)
        parser_state.current_node = node

    @multiline_not_supported
    def scope(*args: str, **kwargs: Any) -> None:
        scope = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(scope)
        parser_state.current_node = scope

    def description(*args: str, **kwargs: Any) -> None:
        description = (" ".join(args)).strip()

        if parser_state.current_node:
            parser_state.current_node["description"] = description
            if parser_state.current_node.get("name", "") == "default":
                doc.description = description
        else:
            doc.description = description

    def kafka_ssl_ca_pem(*args: str, **kwargs: Any) -> None:
        kafka_ssl_ca_pem = ("\n".join(args)).strip()
        parser_state.current_node["kafka_ssl_ca_pem"] = kafka_ssl_ca_pem

    def sql(var_name: str, **kwargs: Any) -> Callable[[str, KwArg(Any)], None]:
        # TODO(eclbg): We shouldn't allow SQL in datasource files
        def _f(sql: str, *args: Any, **kwargs: Any) -> None:
            if not parser_state.multiline:
                raise DatafileSyntaxError(
                    "SQL must be multiline",
                    hint="Use > to start a multiline SQL block",
                    lineno=kwargs["lineno"],
                    pos=1,
                )
            if not parser_state.current_node:
                raise DatafileSyntaxError(
                    "SQL must be called after a NODE command",
                    lineno=kwargs["lineno"],
                    pos=1,
                )
            parser_state.current_node[var_name] = (
                textwrap.dedent(sql).rstrip() if "%" not in sql.strip()[0] else sql.strip()
            )

        # HACK this cast is needed because Mypy
        return cast(Callable[[str, KwArg(Any)], None], _f)

    def assign_node_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any) -> None:
            if not parser_state.current_node:
                raise DatafileSyntaxError(
                    f"{v} must be called after a NODE command",
                    lineno=kwargs["lineno"],
                    pos=1,
                )
            return assign_var(v)(*args, **kwargs)

        return _f

    @multiline_not_supported
    def add_token(*args: str, **kwargs: Any) -> None:  # token_name, permissions):
        lineno = kwargs["lineno"]
        if len(args) < 2:
            raise DatafileSyntaxError(
                message='TOKEN takes two params: token name and permission e.g TOKEN "read api token" READ',
                lineno=lineno,
                pos=1,
            )
        if len(args) > 2:
            raise DatafileSyntaxError(
                f"Invalid number of arguments for TOKEN command: {len(args)}. Expected 2 arguments: token name and permission",
                lineno=lineno,
                pos=len("token") + len(args[0]) + 3,  # Naive handling of whitespace. Assuming there's 2
            )
        permission = args[1]
        if permission.upper() not in ["READ", "APPEND"]:
            raise DatafileSyntaxError(
                f"Invalid permission: {permission}. Only READ and APPEND are supported",
                lineno=lineno,
                pos=len("token") + len(args[0]) + 3,  # Naive handling of whitespace. Assuming there's 2
            )
        token_name = _unquote(args[0])
        doc.tokens.append({"token_name": token_name, "permission": permission.upper()})

    @not_supported_yet()
    def include(*args: str, **kwargs: Any) -> None:
        f = _unquote(args[0])
        f = eval_var(f)
        attrs = dict(_unquote(x).split("=", 1) for x in args[1:])
        nonlocal lines
        lineno = kwargs["lineno"]
        replace_includes = kwargs["replace_includes"]
        n = lineno
        args_with_attrs = " ".join(args)

        try:
            while True:
                n += 1
                if len(lines) <= n:
                    break
                if "NODE" in lines[n]:
                    doc.includes[args_with_attrs] = lines[n]
                    break
            if args_with_attrs not in doc.includes:
                doc.includes[args_with_attrs] = ""
        except Exception:
            pass

        # If this parse was triggered by format, we don't want to replace the file
        if not replace_includes:
            return

        # be sure to replace the include line
        p = Path(basepath)

        try:
            with open(p / f) as file:
                try:
                    ll = list(StringIO(file.read(), newline=None))
                    node_line = [line for line in ll if "NODE" in line]
                    if node_line and doc.includes[args_with_attrs]:
                        doc.includes[node_line[0].split("NODE")[-1].split("\n")[0].strip()] = ""
                except Exception:
                    pass
                finally:
                    file.seek(0)
                lines[lineno : lineno + 1] = [
                    "",
                    *list(StringIO(Template(file.read()).safe_substitute(attrs), newline=None)),
                ]
        except FileNotFoundError:
            raise IncludeFileNotFoundException(f, lineno)

    @deprecated(severity="warning")
    def version(*args: str, **kwargs: Any) -> None:
        pass  # whatever, it's deprecated

    def shared_with(*args: str, **kwargs: Any) -> None:
        # Count total workspaces collected
        total_workspaces = 0

        for entries in args:
            # In case they specify multiple workspaces, handle both line-separated and comma-separated values
            lines = entries.splitlines()
            for line in lines:
                # Split by comma and strip whitespace from each workspace name
                workspaces = [workspace.strip().rstrip(",") for workspace in line.split(",") if workspace.strip()]
                doc.shared_with += workspaces
                total_workspaces += len(workspaces)

        # Add warning once if any workspaces were found
        if total_workspaces > 0:
            warnings.append(
                DatafileParseWarning(
                    message=(
                        f"{kwargs['cmd'].upper()} is not fully implemented in Forward and will be ignored while this warning is present."
                    )
                )
            )

        # Validate that at least one workspace was provided
        if total_workspaces == 0:
            raise DatafileSyntaxError(
                "SHARED_WITH requires at least one workspace name",
                lineno=kwargs["lineno"],
                pos=1,
            )

    def __init_engine(v: str):
        if not parser_state.current_node:
            raise Exception(f"{v} must be called after a NODE command")
        if "engine" not in parser_state.current_node:
            parser_state.current_node["engine"] = {"type": None, "args": []}

    def set_engine(*args: str, **kwargs: Any) -> None:
        __init_engine("ENGINE")
        engine_type = _unquote((" ".join(args)).strip())
        parser_state.current_node["engine"]["type"] = eval_var(engine_type, skip=skip_eval)

    def add_engine_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any):
            __init_engine(f"ENGINE_{v}".upper())
            engine_arg = eval_var(_unquote((" ".join(args)).strip()), skip=skip_eval)
            if v.lower() == "ttl" and not engine_arg:
                return
            parser_state.current_node["engine"]["args"].append((v, engine_arg))

        return _f

    def tags(*args: str, **kwargs: Any) -> None:
        raw_tags = _unquote((" ".join(args)).strip())
        operational_tags, filtering_tags = parse_tags(raw_tags)

        # Pipe nodes or Data Sources
        if parser_state.current_node and operational_tags:
            operational_tags_args = (operational_tags,)
            assign_node_var("tags")(*operational_tags_args, **kwargs)

        if filtering_tags:
            if doc.filtering_tags is None:
                doc.filtering_tags = filtering_tags
            else:
                doc.filtering_tags += filtering_tags

    cmds_per_datafile_kind: dict[DatafileKind, dict[str, Callable]] = {
        DatafileKind.datasource: {
            "description": description,
            "token": add_token,
            "source": sources,
            "schema": schema,
            "indexes": indexes,
            "engine": set_engine,
            "partition_key": assign_var("partition_key"),
            "sorting_key": assign_var("sorting_key"),
            "primary_key": assign_var("primary_key"),
            "sampling_key": assign_var("sampling_key"),
            "ttl": assign_var("ttl"),
            "tags": tags,
            "include": include,
            "version": version,
            "kafka_connection_name": assign_var("kafka_connection_name"),
            "kafka_topic": assign_var("kafka_topic"),
            "kafka_group_id": assign_var("kafka_group_id"),
            "kafka_auto_offset_reset": assign_var("kafka_auto_offset_reset"),
            "kafka_store_raw_value": assign_var("kafka_store_raw_value"),
            "kafka_store_headers": assign_var("kafka_store_headers"),
            "kafka_store_binary_headers": kafka_store_binary_headers_deprecated,
            "kafka_key_format": assign_var("kafka_key_format"),
            "kafka_value_format": assign_var("kafka_value_format"),
            "kafka_target_partitions": kafka_target_partitions_deprecated,  # Deprecated
            "import_connection_name": assign_var("import_connection_name"),
            "import_schedule": assign_var("import_schedule"),
            "import_strategy": import_strategy_deprecated,  # Deprecated, always append
            "import_bucket_uri": assign_var("import_bucket_uri"),
            "import_from_timestamp": assign_var("import_from_timestamp"),
            "import_service": import_service_deprecated,  # Deprecated
            "import_external_datasource": import_external_datasource_deprecated,  # Deprecated, BQ and SFK
            "import_query": assign_var("import_query"),  # Deprecated, BQ and SFK
            "import_table_arn": assign_var("import_table_arn"),  # Only for DynamoDB
            "import_export_bucket": assign_var("import_export_bucket"),  # For DynamoDB
            "shared_with": shared_with,  # Not supported yet
            "export_service": export_service,  # Deprecated
            "forward_query": sql("forward_query"),
            "backfill": assign_var("backfill", allowed_values={"skip"}),
            # ENGINE_* commands are added dynamically after this dict's definition
        },
        DatafileKind.pipe: {
            "node": node,
            "scope": scope,
            "description": description,
            "type": assign_node_var("type"),
            "datasource": assign_node_var("datasource"),
            "tags": tags,
            "target_datasource": assign_node_var("target_datasource"),
            "copy_schedule": assign_node_var(CopyParameters.COPY_SCHEDULE),
            "copy_mode": assign_node_var("mode"),
            "mode": assign_node_var("mode"),
            "filter": assign_node_var("filter"),
            "token": add_token,
            "include": include,
            "sql": sql("sql"),
            "version": version,
            "deployment_method": assign_var("deployment_method", allowed_values={"alter"}),
            "export_connection_name": assign_var("export_connection_name"),
            "export_schedule": assign_var("export_schedule"),
            "export_bucket_uri": assign_var("export_bucket_uri"),
            "export_file_template": assign_var("export_file_template"),
            "export_format": assign_var("export_format"),
            "export_strategy": assign_var("export_strategy"),
            "export_compression": assign_var("export_compression"),
            "export_write_strategy": assign_var("export_write_strategy"),
            "export_kafka_topic": assign_var("export_kafka_topic"),
        },
        DatafileKind.connection: {
            "description": description,
            "type": assign_node_var("type"),
            "kafka_bootstrap_servers": assign_var("kafka_bootstrap_servers"),
            "kafka_key": assign_var("kafka_key"),
            "kafka_secret": assign_var("kafka_secret"),
            "kafka_schema_registry_url": assign_var("kafka_schema_registry_url"),
            "kafka_ssl_ca_pem": kafka_ssl_ca_pem,
            "kafka_security_protocol": assign_var("kafka_security_protocol"),
            "kafka_sasl_mechanism": assign_var("kafka_sasl_mechanism"),
            "kafka_sasl_oauthbearer_method": assign_var("kafka_sasl_oauthbearer_method"),
            "kafka_sasl_oauthbearer_aws_region": assign_var("kafka_sasl_oauthbearer_aws_region"),
            "kafka_sasl_oauthbearer_aws_role_arn": assign_var("kafka_sasl_oauthbearer_aws_role_arn"),
            "kafka_sasl_oauthbearer_aws_external_id": assign_var("kafka_sasl_oauthbearer_aws_external_id"),
            "kafka_key_avro_deserialization": kafka_key_avro_deserialization_deprecated,
            "s3_region": assign_var("s3_region"),
            "s3_arn": assign_var("s3_arn"),
            "s3_access_key": assign_var("s3_access_key"),
            "s3_secret": assign_var("s3_secret"),
            "gcs_service_account_credentials_json": assign_var_json("gcs_service_account_credentials_json"),
            "gcs_access_id": assign_var("gcs_hmac_access_id"),
            "gcs_secret": assign_var("gcs_hmac_secret"),
            "gcs_hmac_access_id": assign_var("gcs_hmac_access_id"),
            "gcs_hmac_secret": assign_var("gcs_hmac_secret"),
            "include": include,
        },
    }

    engine_vars = set()

    for _engine, (params, options) in ENABLED_ENGINES:
        for p in params:
            engine_vars.add(p.name)
        for o in options:
            engine_vars.add(o.name)
    for v in engine_vars:
        cmds_per_datafile_kind[DatafileKind.datasource][f"engine_{v}"] = add_engine_var(v)

    if default_node:
        node(default_node)

    cmds = cmds_per_datafile_kind[kind]

    lineno = 1
    try:
        while lineno <= len(lines):
            line = lines[lineno - 1]
            # shlex.shlex(line) removes comments that start with #. This doesn't affect multiline commands
            try:
                sa = shlex.shlex(line)
                sa.whitespace_split = True
                lexer = list(sa)
            except ValueError:
                sa = shlex.shlex(shlex.quote(line))
                sa.whitespace_split = True
                lexer = list(sa)
            if lexer:
                cmd, args = lexer[0], lexer[1:]
                if (
                    parser_state.multiline
                    and cmd.lower() in cmds
                    and not (line.startswith(" ") or line.startswith("\t"))
                ):
                    cmds[parser_state.command](
                        parser_state.multiline_string,
                        lineno=lineno,
                        replace_includes=replace_includes,
                        cmd=parser_state.command,
                    )
                    parser_state.multiline = False

                if not parser_state.multiline:
                    if len(args) >= 1 and args[0] == ">":
                        parser_state.multiline = True
                        parser_state.command = cmd.lower()
                        parser_state.start_lineno = lineno
                        parser_state.multiline_string = ""
                    else:
                        if cmd.lower() == "settings":
                            msg = (
                                "SETTINGS option is not allowed, use ENGINE_SETTINGS instead. See "
                                "https://www.tinybird.co/docs/cli/datafiles#data-source for more information."
                            )
                            raise DatafileSyntaxError(
                                # TODO(eclbg): add surrounding lines as context to the error so we can print it
                                # offending_line=line,
                                message=msg,
                                lineno=lineno,
                                pos=0,
                            )
                        if cmd.lower() in cmds:
                            cmds[cmd.lower()](*args, lineno=lineno, replace_includes=replace_includes, cmd=cmd)
                        else:
                            error_msg = f"{cmd.upper()} is not a valid option"
                            if kind:
                                error_msg += f" in {kind.value} files."
                            raise DatafileSyntaxError(
                                message=error_msg,
                                lineno=lineno,
                                pos=0,
                            )
                else:
                    parser_state.multiline_string += line
            lineno += 1
        # close final state
        if parser_state.multiline:
            cmds[parser_state.command](
                parser_state.multiline_string,
                lineno=lineno,
                replace_includes=replace_includes,
                cmd=parser_state.command,
            )
    except DatafileSyntaxError as e:
        # When the error is in a multiline block, add the start lineno to the error lineno so the error location is in
        # respect to the whole file
        if parser_state.multiline:
            e.lineno += parser_state.start_lineno or 0
        raise e
    except ParseException as e:
        raise ParseException(str(e), lineno=lineno)
    except IndexError as e:
        if "node" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_node_name())
        elif "sql" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_sql_command())
        elif "datasource" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_datasource_name())
        else:
            raise ValidationException(f"Validation error, found {line} in line {str(lineno)}: {str(e)}", lineno=lineno)
    except IncludeFileNotFoundException as e:
        raise IncludeFileNotFoundException(str(e), lineno=lineno)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise ParseException(f"Unexpected error: {e}", lineno=lineno)

    return ParseResult(datafile=doc, warnings=warnings)


class ImportReplacements:
    _REPLACEMENTS: Tuple[Tuple[str, str, Optional[str]], ...] = (
        ("import_strategy", "mode", "replace"),
        ("import_connection_name", "connection", None),
        ("import_schedule", "cron", ON_DEMAND),
        ("import_query", "query", None),
        ("import_connector", "connector", None),
        ("import_external_datasource", "external_data_source", None),
        ("import_bucket_uri", "bucket_uri", None),
        ("import_from_timestamp", "from_time", None),
        ("import_table_arn", "dynamodb_table_arn", None),
        ("import_export_bucket", "dynamodb_export_bucket", None),
    )

    @staticmethod
    def get_datafile_parameter_keys() -> List[str]:
        return [x[0] for x in ImportReplacements._REPLACEMENTS]

    @staticmethod
    def get_api_param_for_datafile_param(connector_service: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        """Returns the API parameter name and default value for a given
        datafile parameter.
        """
        key = key.lower()
        for datafile_k, linker_k, value in ImportReplacements._REPLACEMENTS:
            if datafile_k == key:
                return linker_k, value
        return None, None

    @staticmethod
    def get_datafile_param_for_linker_param(connector_service: str, linker_param: str) -> Optional[str]:
        """Returns the datafile parameter name for a given linter parameter."""
        linker_param = linker_param.lower()
        for datafile_k, linker_k, _ in ImportReplacements._REPLACEMENTS:
            if linker_k == linker_param:
                return datafile_k
        return None

    @staticmethod
    def get_datafile_value_for_linker_value(
        connector_service: str, linker_param: str, linker_value: str
    ) -> Optional[str]:
        """Map linker values to datafile values."""
        linker_param = linker_param.lower()
        if linker_param != "cron":
            return linker_value
        if linker_value == "@once":
            return ON_DEMAND
        if connector_service in PREVIEW_CONNECTOR_SERVICES:
            return "@auto"
        return linker_value


class ExportReplacements:
    SERVICES = ("gcs_hmac", "s3", "s3_iamrole", "kafka")
    NODE_TYPES = (PipeNodeTypes.DATA_SINK, PipeNodeTypes.STREAM)
    _REPLACEMENTS = (
        ("export_service", "service", None),
        ("export_connection_name", "connection", None),
        ("export_schedule", "schedule_cron", ""),
        ("export_bucket_uri", "path", None),
        ("export_file_template", "file_template", None),
        ("export_format", "format", "csv"),
        ("export_compression", "compression", None),
        ("export_strategy", "strategy", "@new"),
        ("export_kafka_topic", "kafka_topic", None),
        ("kafka_connection_name", "connection", None),
        ("kafka_topic", "kafka_topic", None),
    )

    @staticmethod
    def get_export_service(node: Dict[str, Optional[str]]) -> str:
        if (node.get("type", "standard") or "standard").lower() == PipeNodeTypes.STREAM:
            return "kafka"
        return (node.get("export_service", "") or "").lower()

    @staticmethod
    def get_node_type(node: Dict[str, Optional[str]]) -> str:
        return (node.get("type", "standard") or "standard").lower()

    @staticmethod
    def is_export_node(node: Dict[str, Optional[str]]) -> bool:
        export_service = ExportReplacements.get_export_service(node)
        node_type = (node.get("type", "standard") or "standard").lower()
        if not export_service:
            return False
        if export_service not in ExportReplacements.SERVICES:
            raise CLIPipeException(f"Invalid export service: {export_service}")
        if node_type not in ExportReplacements.NODE_TYPES:
            raise CLIPipeException(f"Invalid export node type: {node_type}")
        return True

    @staticmethod
    def get_params_from_datafile(node: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        """Returns the export parameters for a given node."""
        params = {}
        node_type = ExportReplacements.get_node_type(node)
        for datafile_key, export_key, default_value in ExportReplacements._REPLACEMENTS:
            if node_type != PipeNodeTypes.STREAM and datafile_key.startswith("kafka_"):
                continue
            if node_type == PipeNodeTypes.STREAM and datafile_key.startswith("export_"):
                continue
            if datafile_key == "export_schedule" and node.get(datafile_key, None) == ON_DEMAND:
                node[datafile_key] = ""
            params[export_key] = node.get(datafile_key, default_value)
        return params

    @staticmethod
    def get_datafile_key(param: str, node: Dict[str, Optional[str]]) -> Optional[str]:
        """Returns the datafile key for a given export parameter."""
        node_type = ExportReplacements.get_node_type(node)
        for datafile_key, export_key, _ in ExportReplacements._REPLACEMENTS:
            if node_type != PipeNodeTypes.STREAM and datafile_key.startswith("kafka_"):
                continue
            if node_type == PipeNodeTypes.STREAM and datafile_key.startswith("export_"):
                continue
            if export_key == param.lower():
                return datafile_key.upper()
        return None


def get_project_filenames(folder: str, with_vendor=False) -> List[str]:
    folders: List[str] = [
        f"{folder}/*.datasource",
        f"{folder}/datasources/*.datasource",
        f"{folder}/*.pipe",
        f"{folder}/pipes/*.pipe",
        f"{folder}/endpoints/*.pipe",
        f"{folder}/materializations/*.pipe",
        f"{folder}/sinks/*.pipe",
        f"{folder}/copies/*.pipe",
        f"{folder}/playgrounds/*.pipe",
        f"{folder}/connections/*.connection",
    ]
    if with_vendor:
        folders.append(f"{folder}/vendor/**/**/*.datasource")

    filenames: List[str] = []
    for x in folders:
        filenames += glob.glob(x)
    return filenames


def get_project_fixtures(folder: str) -> List[str]:
    folders: List[str] = [
        f"{folder}/fixtures/*.ndjson",
        f"{folder}/fixtures/*.csv",
    ]
    filenames: List[str] = []
    for x in folders:
        filenames += glob.glob(x)
    return filenames


def has_internal_datafiles(folder: str) -> bool:
    folder = folder or "."
    filenames = get_project_filenames(folder)
    return any([f for f in filenames if "spans" in str(f) and "vendor" not in str(f)])


def peek(iterable):
    try:
        first = next(iterable)
    except Exception:
        return None, None
    return first, itertools.chain([first], iterable)


def normalize_array(items: List[Dict[str, Optional[Any]]]) -> List[Dict]:
    """
        Sorted() doesn't not support values with different types for the same column like None vs str.
        So, we need to cast all None to default value of the type of the column if exist and if all the values are None, we can leave them as None
    >>> normalize_array([{'x': 'hello World'}, {'x': None}])
    [{'x': 'hello World'}, {'x': ''}]
    >>> normalize_array([{'x': 3}, {'x': None}])
    [{'x': 3}, {'x': 0}]
    >>> normalize_array([{'x': {'y': [1,2,3,4]}}, {'x': {'z': "Hello" }}])
    [{'x': {'y': [1, 2, 3, 4]}}, {'x': {'z': 'Hello'}}]
    """
    types: Dict[str, type] = {}
    if len(items) == 0:
        return items

    columns = items[0].keys()
    for column in columns:
        for object in items:
            if object[column] is not None:
                types[column] = type(object[column])
                break

    for object in items:
        for column in columns:
            if object[column] is not None:
                continue

            # If None, we replace it for the default value
            if types.get(column, None):
                object[column] = types[column]()

    return items


def find_file_by_name(
    folder: str,
    name: str,
    verbose: bool = False,
    is_raw: bool = False,
    vendor_paths: Optional[List[Tuple[str, str]]] = None,
    resource: Optional[Dict] = None,
):
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return ds, None
    if os.path.isfile(f / "datasources" / ds):
        return ds, None

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return pipe, None

    pipe_paths = ["endpoints", "materializations", "sinks", "copies", "playgrounds", "pipes"]
    for pipe_path in pipe_paths:
        if os.path.isfile(f / pipe_path / pipe):
            return pipe, None

    token = name + ".token"
    if os.path.isfile(f / "tokens" / token):
        return token, None

    # look for the file in subdirectories if it's not found in datasources folder
    if vendor_paths:
        _resource = None
        for wk_name, wk_path in vendor_paths:
            file = None
            if name.startswith(f"{wk_name}."):
                file, _resource = find_file_by_name(
                    wk_path, name.replace(f"{wk_name}.", ""), verbose, is_raw, resource=resource
                )
            if file:
                return file, _resource

    if not is_raw:
        f, raw = find_file_by_name(
            folder,
            name,
            verbose=verbose,
            is_raw=True,
            vendor_paths=vendor_paths,
            resource=resource,
        )
        return f, raw

    # materialized node with DATASOURCE definition
    if resource and "nodes" in resource:
        for node in resource["nodes"]:
            params = node.get("params", {})
            if (
                params.get("type", None) == "materialized"
                and params.get("engine", None)
                and params.get("datasource", None)
            ):
                pipe = resource["resource_name"] + ".pipe"
                pipe_file_exists = (
                    os.path.isfile(os.path.join(folder, pipe))
                    or os.path.isfile(f / "endpoints" / pipe)
                    or os.path.isfile(f / "pipes" / pipe)
                )
                is_target_datasource = params["datasource"] == name
                if pipe_file_exists and is_target_datasource:
                    return pipe, {"resource_name": params.get("datasource")}

    if verbose:
        click.echo(FeedbackManager.warning_file_not_found_inside(name=name, folder=folder))

    return None, None


def get_name_version(ds: str) -> Dict[str, Any]:
    """
    Given a name like "name__dev__v0" returns ['name', 'dev', 'v0']
    >>> get_name_version('dev__name__v0')
    {'name': 'dev__name', 'version': 0}
    >>> get_name_version('name__v0')
    {'name': 'name', 'version': 0}
    >>> get_name_version('dev__name')
    {'name': 'dev__name', 'version': None}
    >>> get_name_version('name')
    {'name': 'name', 'version': None}
    >>> get_name_version('horario__3__pipe')
    {'name': 'horario__3__pipe', 'version': None}
    >>> get_name_version('horario__checker')
    {'name': 'horario__checker', 'version': None}
    >>> get_name_version('dev__horario__checker')
    {'name': 'dev__horario__checker', 'version': None}
    >>> get_name_version('tg__dActividades__v0_pipe_3907')
    {'name': 'tg__dActividades', 'version': 0}
    >>> get_name_version('tg__dActividades__va_pipe_3907')
    {'name': 'tg__dActividades__va_pipe_3907', 'version': None}
    >>> get_name_version('tg__origin_workspace.shared_ds__v3907')
    {'name': 'tg__origin_workspace.shared_ds', 'version': 3907}
    >>> get_name_version('tmph8egtl__')
    {'name': 'tmph8egtl__', 'version': None}
    >>> get_name_version('tmph8egtl__123__')
    {'name': 'tmph8egtl__123__', 'version': None}
    >>> get_name_version('dev__name__v0')
    {'name': 'dev__name', 'version': 0}
    >>> get_name_version('name__v0')
    {'name': 'name', 'version': 0}
    >>> get_name_version('dev__name')
    {'name': 'dev__name', 'version': None}
    >>> get_name_version('name')
    {'name': 'name', 'version': None}
    >>> get_name_version('horario__3__pipe')
    {'name': 'horario__3__pipe', 'version': None}
    >>> get_name_version('horario__checker')
    {'name': 'horario__checker', 'version': None}
    >>> get_name_version('dev__horario__checker')
    {'name': 'dev__horario__checker', 'version': None}
    >>> get_name_version('tg__dActividades__v0_pipe_3907')
    {'name': 'tg__dActividades', 'version': 0}
    >>> get_name_version('tg__origin_workspace.shared_ds__v3907')
    {'name': 'tg__origin_workspace.shared_ds', 'version': 3907}
    >>> get_name_version('tmph8egtl__')
    {'name': 'tmph8egtl__', 'version': None}
    >>> get_name_version('tmph8egtl__123__')
    {'name': 'tmph8egtl__123__', 'version': None}
    """
    tk = ds.rsplit("__", 2)
    if len(tk) == 1:
        return {"name": tk[0], "version": None}
    elif len(tk) == 2:
        if len(tk[1]):
            if tk[1][0] == "v" and re.match("[0-9]+$", tk[1][1:]):
                return {"name": tk[0], "version": int(tk[1][1:])}
            else:
                return {"name": tk[0] + "__" + tk[1], "version": None}
    elif len(tk) == 3 and len(tk[2]):
        if tk[2] == "checker":
            return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "version": None}
        if tk[2][0] == "v":
            parts = tk[2].split("_")
            try:
                return {"name": tk[0] + "__" + tk[1], "version": int(parts[0][1:])}
            except ValueError:
                return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "version": None}
        else:
            return {"name": "__".join(tk[0:]), "version": None}

    return {"name": ds, "version": None}


def get_resource_versions(datasources: List[str]):
    """
    return the latest version for all the datasources
    """
    versions = {}
    for x in datasources:
        t = get_name_version(x)
        name = t["name"]
        if t.get("version", None) is not None:
            versions[name] = t["version"]
    return versions


def is_file_a_datasource(filename: str) -> bool:
    extensions = Path(filename).suffixes
    if ".datasource" in extensions:  # Accepts '.datasource' and '.datasource.incl'
        return True

    if ".incl" in extensions:
        lines = []
        with open(filename) as file:
            lines = file.readlines()

        for line in lines:
            trimmed_line = line.strip().lower()
            if trimmed_line.startswith("schema") or trimmed_line.startswith("engine"):
                return True

    return False
