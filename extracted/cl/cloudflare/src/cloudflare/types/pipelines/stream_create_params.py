# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = ["StreamCreateParams", "Format", "FormatJson", "FormatParquet", "HTTP", "HTTPCORS", "Schema", "WorkerBinding"]


class StreamCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Specifies the public ID of the account."""

    name: Required[str]
    """Specifies the name of the Stream."""

    format: Format
    """Defines the data format of the events."""

    http: HTTP

    schema: Schema
    """Defines the schema of the events in the data stream."""

    worker_binding: WorkerBinding


class FormatJson(TypedDict, total=False):
    type: Required[Literal["json"]]

    decimal_encoding: Literal["number", "string", "bytes"]

    timestamp_format: Literal["rfc3339", "unix_millis"]

    unstructured: bool


class FormatParquet(TypedDict, total=False):
    type: Required[Literal["parquet"]]

    compression: Literal["uncompressed", "snappy", "gzip", "zstd", "lz4"]

    row_group_bytes: Optional[int]


Format: TypeAlias = Union[FormatJson, FormatParquet]


class HTTPCORS(TypedDict, total=False):
    """Specifies the CORS options for the HTTP endpoint."""

    origins: SequenceNotStr[str]


class HTTP(TypedDict, total=False):
    authentication: Required[bool]
    """Indicates that authentication is required for the HTTP endpoint."""

    enabled: Required[bool]
    """Indicates that the HTTP endpoint is enabled."""

    cors: HTTPCORS
    """Specifies the CORS options for the HTTP endpoint."""


class Schema(TypedDict, total=False):
    """Defines the schema of the events in the data stream."""

    fields: Iterable["SourceFieldParam"]

    inferred: Optional[bool]


class WorkerBinding(TypedDict, total=False):
    enabled: Required[bool]
    """Indicates that the worker binding is enabled."""


from .source_field_param import SourceFieldParam
