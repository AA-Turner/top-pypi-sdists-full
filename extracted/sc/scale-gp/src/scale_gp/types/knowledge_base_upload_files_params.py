# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes, SequenceNotStr

__all__ = ["KnowledgeBaseUploadFilesParams"]


class KnowledgeBaseUploadFilesParams(TypedDict, total=False):
    chunking_strategy_config: Required[str]

    data_source_config: Required[str]

    files: Required[SequenceNotStr[FileTypes]]

    force_reupload: Required[bool]

    tagging_information: str
