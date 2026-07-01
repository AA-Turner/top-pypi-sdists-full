# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["KnowledgeBaseUploadFilesParams"]


class KnowledgeBaseUploadFilesParams(TypedDict, total=False):
    chunking_strategy_config: Required[str]

    data_source_config: Required[str]

    files: Required[SequenceNotStr[str]]

    force_reupload: Required[bool]

    custom_metadata: str
    """
    JSON-encoded dictionary of custom metadata to attach to all chunks generated
    from the uploaded files. These metadata fields become queryable via
    metadata_filters on the chunks query endpoint.
    """

    tagging_information: str
