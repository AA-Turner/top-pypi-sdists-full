"""GitHub Issues Synchronization Service."""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlmodel import Session, select

from src.api.github_issues_api import GitHubIssuesAPI, GitHubIssuesSyncStats
from src.domain.repository import Repository
from src.domain.repository_issue import RepositoryIssue

logger = logging.getLogger(__name__)


class GitHubIssueSyncService:
    """Service for synchronizing GitHub issues to RepositoryIssue records"""

    def __init__(self, session: Session):
        """
        Initialize the sync service

        Args:
            session: Database session for persistence
        """
        self.session = session

    async def sync_repository_issues(
        self,
        repository_id: str,
        token: str,
        state_filter: str = "all",
        since: Optional[datetime] = None,
        dry_run: bool = False,
    ) -> GitHubIssuesSyncStats:
        """
        Sync all issues from a GitHub repository

        Args:
            repository_id: Internal repository ID
            token: GitHub access token
            state_filter: Issue state filter ("open", "closed", "all")
            since: Only sync issues updated after this date
            dry_run: If True, don't save changes to database

        Returns:
            Sync statistics
        """
        stats = GitHubIssuesSyncStats(started_at=datetime.now(timezone.utc))

        try:
            # Get repository information
            repository = self.session.get(Repository, repository_id)
            if not repository:
                stats.add_error(f"Repository {repository_id} not found")
                stats.mark_completed()
                return stats

            # Parse repository owner and name from URL or full_name
            if hasattr(repository, "full_name") and repository.full_name:
                owner, repo_name = repository.full_name.split("/", 1)
            else:
                stats.add_error("Repository missing full_name for GitHub API access")
                stats.mark_completed()
                return stats

            logger.info(f"Starting GitHub issues sync for {owner}/{repo_name}")

            # Fetch issues from GitHub
            async with GitHubIssuesAPI(token) as github_api:
                # Validate repository access
                if not await github_api.validate_repository_access(owner, repo_name):
                    stats.add_error(f"No access to repository {owner}/{repo_name}")
                    stats.mark_completed()
                    return stats

                # Determine since date for incremental sync
                sync_since = since or repository.last_issue_sync_at

                # Fetch all issues
                github_issues = await github_api.get_all_repository_issues(
                    owner, repo_name, state=state_filter, since=sync_since
                )

                stats.total_fetched = len(github_issues)
                logger.info(f"Fetched {stats.total_fetched} issues from GitHub")

                # Process each issue
                for github_issue in github_issues:
                    try:
                        # Skip pull requests (GitHub API includes them in issues)
                        if github_issue.get("pull_request"):
                            stats.issues_skipped += 1
                            continue

                        # Check if issue already exists
                        existing_issue = self._get_existing_issue(
                            repository_id, github_issue["number"]
                        )

                        if existing_issue:
                            # Update existing issue
                            if self._update_repository_issue(
                                existing_issue, github_issue, dry_run
                            ):
                                stats.issues_updated += 1
                            else:
                                stats.issues_skipped += 1
                        else:
                            # Create new issue
                            if self._create_repository_issue(
                                repository_id, github_issue, dry_run
                            ):
                                stats.issues_created += 1
                            else:
                                stats.add_error(
                                    f"Failed to create issue #{github_issue['number']}"
                                )

                    except Exception as e:
                        error_msg = f"Error processing issue #{github_issue.get('number', 'unknown')}: {str(e)}"
                        stats.add_error(error_msg)
                        logger.error(error_msg)

            # Update repository sync metadata
            if not dry_run:
                repository.last_issue_sync_at = datetime.now(timezone.utc)
                repository.last_issue_sync_count = (
                    stats.issues_created + stats.issues_updated
                )
                if repository.total_issues_synced is None:
                    repository.total_issues_synced = 0
                repository.total_issues_synced += stats.issues_created
                self.session.add(repository)
                self.session.commit()

            logger.info(
                f"Sync completed: {stats.issues_created} created, "
                f"{stats.issues_updated} updated, {stats.issues_skipped} skipped"
            )

        except Exception as e:
            error_msg = f"GitHub issues sync failed: {str(e)}"
            stats.add_error(error_msg)
            logger.error(error_msg)
            if not dry_run:
                self.session.rollback()

        stats.mark_completed()
        return stats

    def _get_existing_issue(
        self, repository_id: str, github_issue_id: int
    ) -> Optional[RepositoryIssue]:
        """Get existing repository issue by GitHub issue ID"""
        statement = select(RepositoryIssue).where(
            RepositoryIssue.repository_id == repository_id,
            RepositoryIssue.github_issue_id == github_issue_id,
        )
        return self.session.exec(statement).first()

    def _create_repository_issue(
        self, repository_id: str, github_issue: Dict, dry_run: bool
    ) -> bool:
        """
        Create a new RepositoryIssue from GitHub issue data

        Args:
            repository_id: Internal repository ID
            github_issue: GitHub issue data
            dry_run: If True, don't save to database

        Returns:
            True if successful, False otherwise
        """
        try:
            issue = RepositoryIssue.from_github_issue(github_issue, repository_id)

            if not dry_run:
                self.session.add(issue)
                self.session.flush()  # Ensure the issue gets an ID

            logger.debug(
                f"Created repository issue #{github_issue['number']}: {github_issue['title']}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to create repository issue: {str(e)}")
            return False

    def _update_repository_issue(
        self, existing_issue: RepositoryIssue, github_issue: Dict, dry_run: bool
    ) -> bool:
        """
        Update an existing RepositoryIssue with GitHub issue data

        Args:
            existing_issue: Existing RepositoryIssue record
            github_issue: Updated GitHub issue data
            dry_run: If True, don't save to database

        Returns:
            True if issue was updated, False if no changes needed
        """
        try:
            # Check if update is needed by comparing GitHub updated timestamp
            github_updated = datetime.fromisoformat(
                github_issue["updated_at"].replace("Z", "+00:00")
            )

            if github_updated <= existing_issue.github_updated_at:
                # Issue hasn't been updated on GitHub since last sync
                return False

            # Update the issue
            existing_issue.update_from_github(github_issue)

            if not dry_run:
                self.session.add(existing_issue)
                self.session.flush()

            logger.debug(
                f"Updated repository issue #{github_issue['number']}: {github_issue['title']}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to update repository issue: {str(e)}")
            return False

    def get_repository_issues(
        self,
        repository_id: str,
        is_open: Optional[bool] = None,
        search: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[RepositoryIssue]:
        """
        Get repository issues with filtering

        Args:
            repository_id: Repository to get issues from
            is_open: Filter by open/closed state
            search: Search term for title/body
            limit: Maximum number of issues to return
            offset: Number of issues to skip

        Returns:
            List of RepositoryIssue records
        """
        statement = select(RepositoryIssue).where(
            RepositoryIssue.repository_id == repository_id
        )

        if is_open is not None:
            statement = statement.where(RepositoryIssue.is_open == is_open)

        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                RepositoryIssue.title.contains(search_term)
                | RepositoryIssue.body.contains(search_term)
            )

        statement = statement.order_by(RepositoryIssue.github_updated_at.desc())
        statement = statement.offset(offset).limit(limit)

        return list(self.session.exec(statement).all())

    def get_repository_issue_by_github_id(
        self, repository_id: str, github_issue_id: int
    ) -> Optional[RepositoryIssue]:
        """Get a specific repository issue by GitHub issue ID"""
        return self._get_existing_issue(repository_id, github_issue_id)

    def get_sync_statistics(self, repository_id: str) -> Dict[str, int]:
        """
        Get sync statistics for a repository

        Args:
            repository_id: Repository to get stats for

        Returns:
            Dictionary with sync statistics
        """
        total_statement = select(RepositoryIssue).where(
            RepositoryIssue.repository_id == repository_id
        )
        total_issues = len(list(self.session.exec(total_statement).all()))

        open_statement = total_statement.where(RepositoryIssue.is_open == True)
        open_issues = len(list(self.session.exec(open_statement).all()))

        closed_issues = total_issues - open_issues

        return {
            "total_issues": total_issues,
            "open_issues": open_issues,
            "closed_issues": closed_issues,
        }
