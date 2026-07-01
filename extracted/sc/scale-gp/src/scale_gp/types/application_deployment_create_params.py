# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ApplicationDeploymentCreateParams"]


class ApplicationDeploymentCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_variant_id: Required[str]

    endpoint: Required[str]

    is_active: Required[bool]

    name: Required[str]
