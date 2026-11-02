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

    uri: Optional[str]
    """
    Location of this version's externally stored data, such as
    hf://datasets/org/name@revision. The service stores this URI as metadata and
    does not read from it.

    - Omit or send null to keep the current dataset head's URI.
    - Supplying a URI replaces it for this version, and later versions inherit the
      replacement.
    - This operation cannot clear an existing URI.
    """
