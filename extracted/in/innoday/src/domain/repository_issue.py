"""Repository Issue domain models for GitHub issue synchronization."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.repository import Repository


class RepositoryIssue(SQLModel, table=True):
    """GitHub repository issues synced from registered repositories"""

    __tablename__ = "repository_issues"

    # Primary key
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        sa_column=Column(String, primary_key=True),
        description="Internal UUID for the repository issue",
    )

    # GitHub issue identification
    github_issue_id: int = Field(description="GitHub issue number")
    repository_id: str = Field(
        sa_column=Column(String, ForeignKey("repositories.id"), index=True),
        description="Repository this issue belongs to",
    )

    # Basic issue content
    title: str = Field(max_length=500, description="Issue title")
    body: Optional[str] = Field(default=None, description="Issue description/body")

    # Simple state tracking
    is_open: bool = Field(default=True, description="Issue open/closed state")

    # GitHub metadata
    github_url: str = Field(description="Direct URL to GitHub issue")
    github_created_at: datetime = Field(description="Issue creation time on GitHub")
    github_updated_at: datetime = Field(description="Last update time on GitHub")

    # Sync tracking
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When this record was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="When this record was last updated"
    )
    last_synced_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this issue was last synced from GitHub",
    )

    # Relationships
    repository: Optional["Repository"] = Relationship()

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "repository_id", "github_issue_id", name="uq_repo_github_issue"
        ),
    )

    def update_from_github(self, github_issue: dict) -> None:
        """Update this repository issue from GitHub API data"""
        self.title = github_issue.get("title", self.title)
        self.body = github_issue.get("body", self.body)
        self.is_open = github_issue.get("state", "open") == "open"
        self.github_url = github_issue.get("html_url", self.github_url)

        # Parse GitHub timestamps
        if "created_at" in github_issue:
            try:
                self.github_created_at = datetime.fromisoformat(
                    github_issue["created_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        if "updated_at" in github_issue:
            try:
                self.github_updated_at = datetime.fromisoformat(
                    github_issue["updated_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                pass

        # Update sync tracking
        self.updated_at = datetime.now(timezone.utc)
        self.last_synced_at = datetime.now(timezone.utc)

    @classmethod
    def from_github_issue(
        cls, github_issue: dict, repository_id: str
    ) -> "RepositoryIssue":
        """Create a new RepositoryIssue from GitHub API data"""
        issue = cls(
            github_issue_id=github_issue["number"],
            repository_id=repository_id,
            title=github_issue.get("title", ""),
            body=github_issue.get("body", ""),
            is_open=github_issue.get("state", "open") == "open",
            github_url=github_issue.get("html_url", ""),
        )

        # Parse GitHub timestamps
        if "created_at" in github_issue:
            try:
                issue.github_created_at = datetime.fromisoformat(
                    github_issue["created_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                issue.github_created_at = datetime.now(timezone.utc)

        if "updated_at" in github_issue:
            try:
                issue.github_updated_at = datetime.fromisoformat(
                    github_issue["updated_at"].replace("Z", "+00:00")
                )
            except (ValueError, AttributeError):
                issue.github_updated_at = datetime.now(timezone.utc)

        return issue

    def __str__(self) -> str:
        """String representation of the repository issue"""
        return f"Issue #{self.github_issue_id}: {self.title} ({'open' if self.is_open else 'closed'})"

    def __repr__(self) -> str:
        """Developer representation of the repository issue"""
        return f"RepositoryIssue(id='{self.id}', github_issue_id={self.github_issue_id}, repository_id='{self.repository_id}', title='{self.title[:50]}...')"
