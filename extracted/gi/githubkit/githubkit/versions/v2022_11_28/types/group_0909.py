"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from typing_extensions import NotRequired, TypedDict


class OrgsOrgDependabotSecretsGetResponse200Type(TypedDict):
    """OrgsOrgDependabotSecretsGetResponse200"""

    total_count: int
    secrets: list[OrganizationDependabotSecretType]


class OrganizationDependabotSecretType(TypedDict):
    """Dependabot Secret for an Organization

    Secrets for GitHub Dependabot for an organization.
    """

    name: str
    created_at: datetime
    updated_at: datetime
    visibility: Literal["all", "private", "selected"]
    selected_repositories_url: NotRequired[str]


__all__ = (
    "OrganizationDependabotSecretType",
    "OrgsOrgDependabotSecretsGetResponse200Type",
)
