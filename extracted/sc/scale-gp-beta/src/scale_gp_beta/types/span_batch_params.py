# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .span_create_param import SpanCreateParam

__all__ = ["SpanBatchParams"]


class SpanBatchParams(TypedDict, total=False):
    items: Required[Iterable[SpanCreateParam]]
