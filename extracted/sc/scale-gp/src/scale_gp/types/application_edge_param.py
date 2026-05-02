# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ApplicationEdgeParam"]


class ApplicationEdgeParam(TypedDict, total=False):
    from_field: Required[str]

    from_node: Required[str]

    to_field: Required[str]

    to_node: Required[str]
