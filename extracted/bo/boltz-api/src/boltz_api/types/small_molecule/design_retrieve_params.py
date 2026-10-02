# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DesignRetrieveParams"]


class DesignRetrieveParams(TypedDict, total=False):
    workspace_id: str
    """Workspace ID.

    Only used with admin API keys. Ignored (or validated) for workspace-scoped keys.
    """
