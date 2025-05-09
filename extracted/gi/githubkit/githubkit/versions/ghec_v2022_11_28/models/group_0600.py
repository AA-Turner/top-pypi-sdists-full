"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from githubkit.compat import GitHubModel, model_rebuild

from .group_0003 import SimpleUser


class WebhookGithubAppAuthorizationRevoked(GitHubModel):
    """github_app_authorization revoked event"""

    action: Literal["revoked"] = Field()
    sender: SimpleUser = Field(title="Simple User", description="A GitHub user.")


model_rebuild(WebhookGithubAppAuthorizationRevoked)

__all__ = ("WebhookGithubAppAuthorizationRevoked",)
