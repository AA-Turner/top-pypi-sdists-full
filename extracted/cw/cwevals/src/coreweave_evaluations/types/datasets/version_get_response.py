# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["VersionGetResponse"]


class VersionGetResponse(BaseModel):
    case_count: int

    created_at: datetime

    dataset_id: str

    dataset_version_id: str

    last_commit_id: int
    """Publication cutoff used to read this version.

    A published snapshot excludes later writes.
    """

    namespace: Literal["wandb"]
    """Namespace that assigned the scope reference."""

    scope_ref: str

    status: Literal["pending", "published"]
    """pending means this version can still change.

    published means its contents are frozen.
    """

    trajectory_count: int

    uri: Optional[str] = None

    version_sequence: int

    parent_version_id: Optional[str] = None
