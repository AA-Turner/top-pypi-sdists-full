# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ThemeCreateParams", "ThemeVars"]


class ThemeCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    logo_blob: Required[str]

    theme_vars: Required[ThemeVars]

    title: Required[str]


class ThemeVars(TypedDict, total=False):
    accent_primary: Annotated[str, PropertyInfo(alias="accentPrimary")]

    accent_secondary: Annotated[str, PropertyInfo(alias="accentSecondary")]

    background: str

    foreground: str
