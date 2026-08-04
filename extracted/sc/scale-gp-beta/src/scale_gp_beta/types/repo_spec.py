# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["RepoSpec"]


class RepoSpec(BaseModel):
    """A single repo the agent should clone into its workspace.

    Mirrors the per-entry shape the golden agent's ``_validate_repos`` accepts:
    ``url`` is required, the rest are optional passthrough hints. Sent verbatim
    as ``task.params.repos`` so provisioning clones these instead of the
    deployment-global default.
    """

    url: str

    depth: Optional[int] = None

    path: Optional[str] = None
