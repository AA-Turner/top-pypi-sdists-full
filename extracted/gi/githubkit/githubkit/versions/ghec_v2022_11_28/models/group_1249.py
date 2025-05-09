"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from githubkit.compat import GitHubModel, model_rebuild
from githubkit.typing import Missing
from githubkit.utils import UNSET


class ReposOwnerRepoReleasesReleaseIdPatchBody(GitHubModel):
    """ReposOwnerRepoReleasesReleaseIdPatchBody"""

    tag_name: Missing[str] = Field(default=UNSET, description="The name of the tag.")
    target_commitish: Missing[str] = Field(
        default=UNSET,
        description="Specifies the commitish value that determines where the Git tag is created from. Can be any branch or commit SHA. Unused if the Git tag already exists. Default: the repository's default branch.",
    )
    name: Missing[str] = Field(default=UNSET, description="The name of the release.")
    body: Missing[str] = Field(
        default=UNSET, description="Text describing the contents of the tag."
    )
    draft: Missing[bool] = Field(
        default=UNSET,
        description="`true` makes the release a draft, and `false` publishes the release.",
    )
    prerelease: Missing[bool] = Field(
        default=UNSET,
        description="`true` to identify the release as a prerelease, `false` to identify the release as a full release.",
    )
    make_latest: Missing[Literal["true", "false", "legacy"]] = Field(
        default=UNSET,
        description="Specifies whether this release should be set as the latest release for the repository. Drafts and prereleases cannot be set as latest. Defaults to `true` for newly published releases. `legacy` specifies that the latest release should be determined based on the release creation date and higher semantic version.",
    )
    discussion_category_name: Missing[str] = Field(
        default=UNSET,
        description='If specified, a discussion of the specified category is created and linked to the release. The value must be a category that already exists in the repository. If there is already a discussion linked to the release, this parameter is ignored. For more information, see "[Managing categories for discussions in your repository](https://docs.github.com/enterprise-cloud@latest//discussions/managing-discussions-for-your-community/managing-categories-for-discussions-in-your-repository)."',
    )


model_rebuild(ReposOwnerRepoReleasesReleaseIdPatchBody)

__all__ = ("ReposOwnerRepoReleasesReleaseIdPatchBody",)
