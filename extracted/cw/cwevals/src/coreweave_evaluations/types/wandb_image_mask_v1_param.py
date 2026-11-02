# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WandbImageMaskV1Param"]


class WandbImageMaskV1Param(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """A segmentation mask file drawn over a W&B image.

    Row comparison across EvaluationVersions matches this value by every property except `uri`. An empty optional property matches a missing one.
    """

    sha256: Required[str]

    size: Required[int]

    uri: Required[str]
    """Row comparison across EvaluationVersions ignores this property."""

    _type: Literal["mask"]
