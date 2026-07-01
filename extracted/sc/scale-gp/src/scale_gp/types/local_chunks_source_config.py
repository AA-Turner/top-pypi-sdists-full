# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["LocalChunksSourceConfig"]


class LocalChunksSourceConfig(BaseModel):
    artifact_name: str
    """The file name assigned to the artifact, containing a file extension.

    Adding an extension is mandatory, to allow detecting file types for text
    extraction.
    """

    artifact_uri: str
    """
    A unique identifier for an artifact within the knowledge base, such as full path
    in a directory or file system.
    """

    source: Literal["LocalChunks"]

    deduplication_strategy: Optional[Literal["Overwrite", "Fail"]] = None
    """
    Action to take if an artifact with the same name already exists in the knowledge
    base. Can be either Overwrite (default) or Fail.
    """
