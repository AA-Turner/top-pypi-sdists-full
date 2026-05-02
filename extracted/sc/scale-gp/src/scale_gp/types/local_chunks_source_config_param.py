# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["LocalChunksSourceConfigParam"]


class LocalChunksSourceConfigParam(TypedDict, total=False):
    artifact_name: Required[str]
    """The file name assigned to the artifact, containing a file extension.

    Adding an extension is mandatory, to allow detecting file types for text
    extraction.
    """

    artifact_uri: Required[str]
    """
    A unique identifier for an artifact within the knowledge base, such as full path
    in a directory or file system.
    """

    source: Required[Literal["LocalChunks"]]

    deduplication_strategy: Literal["Overwrite", "Fail"]
    """
    Action to take if an artifact with the same name already exists in the knowledge
    base. Can be either Overwrite (default) or Fail.
    """
