# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ApplicationSpecCreateParams"]


class ApplicationSpecCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    description: Required[str]
    """The description of the Application Spec"""

    name: Required[str]
    """The name of the Application Spec"""

    run_online_evaluation: bool
    """Whether the application spec should run online evaluation, default is `false`"""

    theme_id: str
