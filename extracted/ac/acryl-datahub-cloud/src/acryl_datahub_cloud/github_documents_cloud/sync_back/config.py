"""Configuration for GitHub sync-back (DataHub -> GitHub)."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field, field_validator

from datahub.configuration.common import ConfigModel


class SyncBackMode(str, Enum):
    """How DataHub edits are written back to GitHub."""

    # Commit aggregated changes straight to the target branch.
    DIRECT_COMMIT = "direct_commit"
    # Push aggregated changes to a dedicated branch and open/update one PR.
    PULL_REQUEST = "pull_request"


class ConflictPolicy(str, Enum):
    """How to handle files changed in both DataHub and GitHub since import."""

    # Leave the GitHub file untouched and report the conflict.
    SKIP = "skip"
    # Write the full DataHub document, replacing the current GitHub file.
    DATAHUB_WINS = "datahub_wins"
    # Three-way merge against the import snapshot; overlapping edits use DataHub.
    MERGE = "merge"


class SyncBackConfig(ConfigModel):
    """Controls writing DataHub document edits back to the GitHub repository.

    Disabled by default: when ``enabled`` is False the cloud source behaves
    exactly like the import-only source.
    """

    enabled: bool = Field(
        default=False,
        description="Enable writing DataHub document edits back to GitHub.",
    )
    mode: SyncBackMode = Field(
        default=SyncBackMode.PULL_REQUEST,
        description=(
            "How to write changes back. 'pull_request' opens (or updates) a "
            "single PR per run; 'direct_commit' commits straight to the target "
            "branch."
        ),
    )
    conflict_policy: ConflictPolicy = Field(
        default=ConflictPolicy.MERGE,
        description=(
            "When a document changed in both DataHub and GitHub since the last "
            "import: 'skip' leaves GitHub unchanged; 'datahub_wins' replaces the "
            "file with the DataHub version; 'merge' performs a three-way merge "
            "using the import snapshot as base and prefers DataHub on overlapping "
            "edits."
        ),
    )
    target_branch: Optional[str] = Field(
        default=None,
        description=(
            "Branch to write changes to. Defaults to the source 'branch' when unset."
        ),
    )
    propagate_new_documents: bool = Field(
        default=True,
        description=(
            "Also create GitHub files for new DataHub documents under the "
            "imported repository tree (not just edits to existing files)."
        ),
    )
    propagate_deleted_documents: bool = Field(
        default=True,
        description=(
            "When a previously imported document is soft-deleted in DataHub, "
            "delete the corresponding file from GitHub during sync-back."
        ),
    )
    new_file_extension: str = Field(
        default=".md",
        description=(
            "File extension used when creating GitHub files for new DataHub "
            "documents that do not already carry one."
        ),
    )
    sync_branch_name: str = Field(
        default="datahub-sync-back",
        description=(
            "Branch name used for pull_request mode. Reused across runs so a "
            "single open PR is updated rather than creating duplicates."
        ),
    )
    commit_message: str = Field(
        default="Sync document edits from DataHub",
        description="Commit message for sync-back commits.",
    )
    pr_title: str = Field(
        default="DataHub document sync-back",
        description="Title for the sync-back pull request (pull_request mode).",
    )
    pr_body: str = Field(
        default=(
            "Automated sync-back of document edits made in DataHub. "
            "Review and merge to persist these changes in the repository."
        ),
        description="Body for the sync-back pull request (pull_request mode).",
    )

    @field_validator("new_file_extension")
    @classmethod
    def normalize_extension(cls, value: str) -> str:
        ext = value.strip().lower()
        if not ext:
            return ".md"
        if not ext.startswith("."):
            ext = f".{ext}"
        return ext
