# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["VersionCreateParams"]


class VersionCreateParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    dataset_version_id: Optional[str]
    """Dataset version to freeze in the evaluation snapshot.

    - For a fixed evaluation, omit this field or supply its configured dataset
      version ID.
    - For a live evaluation, supply a dataset version ID, or omit the field to
      publish the dataset's head and use it. Supplying the head's ID also publishes
      it.
    """
