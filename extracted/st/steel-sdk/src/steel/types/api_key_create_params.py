# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["APIKeyCreateParams"]


class APIKeyCreateParams(TypedDict, total=False):
    name: str
    """A human-readable label for the new key. Defaults to Default."""

    project_id: Annotated[str, PropertyInfo(alias="projectId")]
    """
    The active project to bind the new key to, belonging to the authenticated
    organization. Required when authenticating with a global API key. Dashboard
    users may omit it to use their default project.
    """

    scope_type: Annotated[Literal["project", "global"], PropertyInfo(alias="scopeType")]
    """Defaults to `project`.

    Global API keys may only create project-scoped keys. Only organization admins
    using dashboard authentication may create a `global` key; projectId is ignored
    for those keys.
    """
