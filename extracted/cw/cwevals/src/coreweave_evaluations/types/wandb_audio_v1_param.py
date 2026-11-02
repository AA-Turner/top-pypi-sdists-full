# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["WandbAudioV1Param"]


class WandbAudioV1Param(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    """A V1 W&B audio value in an evaluation input or output field.

    Row comparison across EvaluationVersions matches this value by every property except `uri`. An empty optional property matches a missing one.
    """

    extension_type: Required[Literal["wandb-audio"]]

    schema_version: Required[Literal[1]]

    sha256: Required[str]

    size: Required[int]

    uri: Required[str]
    """Row comparison across EvaluationVersions ignores this property."""

    wb_media_type: Required[Literal["audio-file"]]

    caption: str
