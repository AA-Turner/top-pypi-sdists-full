# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["RepoSpecParam"]


class RepoSpecParam(TypedDict, total=False):
    """A single repo the agent should clone into its workspace.

    Mirrors the per-entry shape the golden agent's ``_validate_repos`` accepts:
    ``url`` is required, the rest are optional passthrough hints. Sent verbatim
    as ``task.params.repos`` so provisioning clones these instead of the
    deployment-global default.
    """

    url: Required[str]

    depth: int

    path: str
