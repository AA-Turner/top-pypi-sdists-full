# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["OfflineApplicationConfigurationParam"]


class OfflineApplicationConfigurationParam(TypedDict, total=False):
    metadata: Dict[str, object]
    """User defined metadata about the application"""
