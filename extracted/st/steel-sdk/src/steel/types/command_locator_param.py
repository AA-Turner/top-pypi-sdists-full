# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CommandLocatorParam"]


class CommandLocatorParam(TypedDict, total=False):
    """Finds an element.

    Set exactly one of role, text, label, placeholder, alt, title, testid, css.
    """

    alt: str

    css: str

    exact: bool
    """Match the whole text. Text matches a case-insensitive substring by default."""

    label: str

    name: str
    """The accessible name. Works only with role."""

    nth: int
    """Picks one of several matches. Negative values count from the end."""

    placeholder: str

    role: str

    testid: str

    text: str

    title: str
