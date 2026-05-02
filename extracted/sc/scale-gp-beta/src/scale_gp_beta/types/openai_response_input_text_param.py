# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["OpenAIResponseInputTextParam"]


class OpenAIResponseInputTextParam(TypedDict, total=False):
    text: Required[str]

    type: Required[Literal["input_text"]]
