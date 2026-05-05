# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ContainerReferenceParam"]


class ContainerReferenceParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    container_id: Required[str]

    type: Required[Literal["container_reference"]]
