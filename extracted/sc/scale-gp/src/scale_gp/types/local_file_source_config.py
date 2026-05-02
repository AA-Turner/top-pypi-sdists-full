# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["LocalFileSourceConfig"]


class LocalFileSourceConfig(BaseModel):
    source: Literal["LocalFile"]

    deduplication_strategy: Optional[Literal["Overwrite", "Fail"]] = None
    """
    Action to take if an artifact with the same name already exists in the knowledge
    base. Can be either Overwrite (default) or Fail.
    """
