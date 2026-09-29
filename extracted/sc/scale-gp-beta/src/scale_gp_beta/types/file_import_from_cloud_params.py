# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FileImportFromCloudParams", "File"]


class FileImportFromCloudParams(TypedDict, total=False):
    files: Required[Iterable[File]]
    """List of files to import from cloud storage"""

    x_project_id: Annotated[str, PropertyInfo(alias="x-project-id")]


class File(TypedDict, total=False):
    container: Required[str]
    """The cloud storage container/bucket name"""

    file_type: Required[str]
    """The MIME type of the file"""

    filename: Required[str]
    """The name of the file"""

    filepath: Required[str]
    """The path to the file within the container"""
