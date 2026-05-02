# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ApplicationDeploymentUpdateParams"]


class ApplicationDeploymentUpdateParams(TypedDict, total=False):
    is_active: bool

    name: str
