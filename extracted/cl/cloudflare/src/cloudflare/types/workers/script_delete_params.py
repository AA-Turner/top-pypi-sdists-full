# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ScriptDeleteParams"]


class ScriptDeleteParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier."""

    force: bool
    """If true, delete the Worker even when other Workers still reference it.

    Service bindings in those Workers may be left broken. Durable Object namespaces
    implemented by the deleted Worker are deleted even if other Workers reference
    them.
    """
