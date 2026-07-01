# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypedDict

__all__ = ["CategoricalChoice"]


class CategoricalChoice(TypedDict, total=False):
    label: Required[str]

    value: Required[Union[str, bool, float]]

    audit_required: bool
