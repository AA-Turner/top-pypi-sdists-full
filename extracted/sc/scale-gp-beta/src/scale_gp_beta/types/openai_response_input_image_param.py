# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["OpenAIResponseInputImageParam"]


class OpenAIResponseInputImageParam(TypedDict, total=False):
    detail: Required[Literal["low", "high", "auto"]]

    type: Required[Literal["input_image"]]

    file_id: str

    image_url: str
