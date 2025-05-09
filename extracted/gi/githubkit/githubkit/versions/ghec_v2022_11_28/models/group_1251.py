"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from typing import Literal, Union

from pydantic import Field

from githubkit.compat import GitHubModel, model_rebuild
from githubkit.typing import Missing
from githubkit.utils import UNSET

from .group_0080 import RepositoryRulesetBypassActor
from .group_0085 import RepositoryRulesetConditions
from .group_0095 import (
    RepositoryRuleCreation,
    RepositoryRuleDeletion,
    RepositoryRuleNonFastForward,
    RepositoryRuleRequiredSignatures,
)
from .group_0096 import RepositoryRuleUpdate
from .group_0098 import RepositoryRuleRequiredLinearHistory
from .group_0099 import RepositoryRuleMergeQueue
from .group_0101 import RepositoryRuleRequiredDeployments
from .group_0104 import RepositoryRulePullRequest
from .group_0106 import RepositoryRuleRequiredStatusChecks
from .group_0108 import RepositoryRuleCommitMessagePattern
from .group_0110 import RepositoryRuleCommitAuthorEmailPattern
from .group_0112 import RepositoryRuleCommitterEmailPattern
from .group_0114 import RepositoryRuleBranchNamePattern
from .group_0116 import RepositoryRuleTagNamePattern
from .group_0118 import RepositoryRuleFilePathRestriction
from .group_0120 import RepositoryRuleMaxFilePathLength
from .group_0122 import RepositoryRuleFileExtensionRestriction
from .group_0124 import RepositoryRuleMaxFileSize
from .group_0127 import RepositoryRuleWorkflows
from .group_0129 import RepositoryRuleCodeScanning


class ReposOwnerRepoRulesetsPostBody(GitHubModel):
    """ReposOwnerRepoRulesetsPostBody"""

    name: str = Field(description="The name of the ruleset.")
    target: Missing[Literal["branch", "tag", "push"]] = Field(
        default=UNSET, description="The target of the ruleset"
    )
    enforcement: Literal["disabled", "active", "evaluate"] = Field(
        description="The enforcement level of the ruleset. `evaluate` allows admins to test rules before enforcing them. Admins can view insights on the Rule Insights page. `evaluate` is not available for the `repository` target."
    )
    bypass_actors: Missing[list[RepositoryRulesetBypassActor]] = Field(
        default=UNSET,
        description="The actors that can bypass the rules in this ruleset",
    )
    conditions: Missing[RepositoryRulesetConditions] = Field(
        default=UNSET,
        title="Repository ruleset conditions for ref names",
        description="Parameters for a repository ruleset ref name condition",
    )
    rules: Missing[
        list[
            Union[
                RepositoryRuleCreation,
                RepositoryRuleUpdate,
                RepositoryRuleDeletion,
                RepositoryRuleRequiredLinearHistory,
                RepositoryRuleMergeQueue,
                RepositoryRuleRequiredDeployments,
                RepositoryRuleRequiredSignatures,
                RepositoryRulePullRequest,
                RepositoryRuleRequiredStatusChecks,
                RepositoryRuleNonFastForward,
                RepositoryRuleCommitMessagePattern,
                RepositoryRuleCommitAuthorEmailPattern,
                RepositoryRuleCommitterEmailPattern,
                RepositoryRuleBranchNamePattern,
                RepositoryRuleTagNamePattern,
                RepositoryRuleFilePathRestriction,
                RepositoryRuleMaxFilePathLength,
                RepositoryRuleFileExtensionRestriction,
                RepositoryRuleMaxFileSize,
                RepositoryRuleWorkflows,
                RepositoryRuleCodeScanning,
            ]
        ]
    ] = Field(default=UNSET, description="An array of rules within the ruleset.")


model_rebuild(ReposOwnerRepoRulesetsPostBody)

__all__ = ("ReposOwnerRepoRulesetsPostBody",)
