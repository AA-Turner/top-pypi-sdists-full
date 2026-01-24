"""
Type annotations for inspector-scan service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector_scan/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_inspector_scan.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from .literals import OutputFormatType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = ("ResponseMetadataTypeDef", "ScanSbomRequestTypeDef", "ScanSbomResponseTypeDef")

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class ScanSbomRequestTypeDef(TypedDict):
    sbom: Mapping[str, Any]
    outputFormat: NotRequired[OutputFormatType]

class ScanSbomResponseTypeDef(TypedDict):
    sbom: dict[str, Any]
    ResponseMetadata: ResponseMetadataTypeDef
