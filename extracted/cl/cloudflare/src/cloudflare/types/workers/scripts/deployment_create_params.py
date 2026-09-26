# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DeploymentCreateParams", "Version", "Annotations"]


class DeploymentCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier."""

    strategy: Required[Literal["percentage"]]

    versions: Required[Iterable[Version]]
    """Worker versions included in this deployment.

    Each object must contain a `version_id` UUID and a `percentage`; percentages
    across all objects must total 100. In the `cf` CLI, pass the entire array as one
    JSON value to `--versions`, either inline, for example
    `--versions '[{"version_id":"023e105f-2a42-4f8b-a1c1-73f6a2a30c0f","percentage":100}]'`,
    or from a JSON file with `--versions @versions.json`.
    """

    force: bool
    """
    If set to true, the deployment will be created even if normally blocked by
    something such rolling back to an older version when a secret has changed.
    """

    annotations: Annotations


class Version(TypedDict, total=False):
    percentage: Required[float]
    """Percentage of traffic served by this version."""

    version_id: Required[str]
    """Identifier of the Worker Version."""


class Annotations(TypedDict, total=False):
    workers_message: Annotated[str, PropertyInfo(alias="workers/message")]
    """Human-readable message about the deployment. Truncated to 1000 bytes if longer."""
