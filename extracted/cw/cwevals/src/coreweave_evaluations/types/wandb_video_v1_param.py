# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WandbVideoV1Param"]


class WandbVideoV1Param(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """A V1 W&B video value in an evaluation input or output field.

    Row comparison across EvaluationVersions matches this value by every property except `uri`. An empty optional property matches a missing one.
    """

    extension_type: Required[Literal["wandb-video"]]

    schema_version: Required[Literal[1]]

    sha256: Required[str]

    size: Required[int]

    uri: Required[str]
    """Row comparison across EvaluationVersions ignores this property."""

    wb_media_type: Required[Literal["video-file"]]

    caption: str

    height: int

    width: int
