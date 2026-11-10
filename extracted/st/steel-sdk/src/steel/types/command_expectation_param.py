# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CommandExpectationParam"]


class CommandExpectationParam(TypedDict, total=False):
    """Fails the command when the element does not have this role or name."""

    name: str

    role: str
