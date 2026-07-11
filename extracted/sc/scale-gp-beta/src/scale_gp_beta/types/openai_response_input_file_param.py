# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["OpenAIResponseInputFileParam"]


class OpenAIResponseInputFileParam(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A file input to the model."""

    type: Required[Literal["input_file"]]

    file_data: str

    file_id: str

    file_url: str

    filename: str
