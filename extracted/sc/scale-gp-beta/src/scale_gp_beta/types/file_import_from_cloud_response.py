# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .sgp_file import SGPFile

__all__ = ["FileImportFromCloudResponse", "Result", "ResultFile", "ResultFile_FailedFile"]


class ResultFile_FailedFile(BaseModel):
    """
    Minimal file representation for failed uploads containing only essential information.
    """

    filename: str
    """The original filename from the request"""

    mime_type: str
    """The original MIME type from the request"""

    object: Optional[Literal["failed_file"]] = None


ResultFile: TypeAlias = Union[SGPFile, ResultFile_FailedFile]


class Result(BaseModel):
    file: ResultFile
    """The file object (full File for success, minimal \\__FailedFile for failures)"""

    status: Literal["SUCCESS", "FAILED_FILE_DOES_NOT_EXIST", "FAILED_INVALID_PERMISSIONS", "FAILED_UNKNOWN_ERROR"]
    """The status of the upload attempt"""


class FileImportFromCloudResponse(BaseModel):
    results: List[Result]
    """Results for each file import attempt"""
