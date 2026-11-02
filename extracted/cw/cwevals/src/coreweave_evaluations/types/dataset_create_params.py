# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["DatasetCreateParams"]


class DatasetCreateParams(TypedDict, total=False):
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

    name: Required[str]

    attributes: Dict[str, object]

    uri: Optional[str]
    """
    Location of externally stored data, such as s3://bucket/prefix/ or
    hf://datasets/org/name. The service stores this URI as metadata and does not
    read from it. Dataset versions inherit it until you supply a replacement when
    publishing a version.
    """
