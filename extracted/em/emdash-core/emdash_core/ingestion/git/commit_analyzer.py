"""Analyze Git commit history."""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from git import Repo

from ...core.models import (
    CommitEntity,
    AuthorEntity,
    FileModification,
    GitData,
    RepositoryEntity,
)
from ...utils.logger import log


class CommitAnalyzer:
    """Analyzes Git commit history and extracts metadata."""

    def __init__(self, repo: Repo, max_commits: int = None):
        """Initialize commit analyzer.

        Args:
            repo: Git repository
            max_commits: Maximum number of commits to analyze (None = all)
        """
        self.repo = repo
        self.max_commits = max_commits

    def analyze(self, repo_entity: RepositoryEntity) -> GitData:
        """Analyze commit history and extract Git data.

        Args:
            repo_entity: Repository entity

        Returns:
            GitData containing commits, authors, and modifications
        """
        log.info("Analyzing Git commit history...")

        commits = []
        modifications = []
        author_stats = defaultdict(lambda: {
            'name': '',
            'email': '',
            'commits': 0,
            'lines_added': 0,
            'lines_deleted': 0,
            'first_commit': None,
            'last_commit': None,
        })

        # Iterate through commits
        commit_count = 0
        for commit in self.repo.iter_commits():
            if self.max_commits and commit_count >= self.max_commits:
                break

            commit_entity = self._extract_commit(commit)
            commits.append(commit_entity)

            # Extract file modifications
            file_mods = self._extract_modifications(commit)
            modifications.extend(file_mods)

            # Update author statistics
            email = commit.author.email
            author_stats[email]['name'] = commit.author.name
            author_stats[email]['email'] = email
            author_stats[email]['commits'] += 1
            author_stats[email]['lines_added'] += commit.stats.total['insertions']
            author_stats[email]['lines_deleted'] += commit.stats.total['deletions']

            timestamp = datetime.fromtimestamp(commit.committed_date)
            if author_stats[email]['first_commit'] is None:
                author_stats[email]['first_commit'] = timestamp
            author_stats[email]['last_commit'] = timestamp

            commit_count += 1

        # Create author entities
        authors = [
            AuthorEntity(
                email=stats['email'],
                name=stats['name'],
                first_commit=stats['first_commit'],
                last_commit=stats['last_commit'],
                total_commits=stats['commits'],
                total_lines_added=stats['lines_added'],
                total_lines_deleted=stats['lines_deleted'],
            )
            for stats in author_stats.values()
        ]

        log.info(f"Analyzed {len(commits)} commits, {len(authors)} authors")

        return GitData(
            repository=repo_entity,
            commits=commits,
            modifications=modifications,
            authors=authors,
        )

    def _extract_commit(self, commit) -> CommitEntity:
        """Extract a commit entity from a git commit.

        Args:
            commit: GitPython commit object

        Returns:
            CommitEntity
        """
        parent_shas = [parent.hexsha for parent in commit.parents]

        return CommitEntity(
            sha=commit.hexsha,
            message=commit.message,
            timestamp=datetime.fromtimestamp(commit.committed_date),
            author_name=commit.author.name,
            author_email=commit.author.email,
            committer_name=commit.committer.name,
            committer_email=commit.committer.email,
            insertions=commit.stats.total['insertions'],
            deletions=commit.stats.total['deletions'],
            files_changed=commit.stats.total['files'],
            is_merge=len(parent_shas) > 1,
            parent_shas=parent_shas,
        )

    def _extract_modifications(self, commit) -> List[FileModification]:
        """Extract file modifications from a commit.

        Args:
            commit: GitPython commit object

        Returns:
            List of FileModification objects
        """
        modifications = []

        try:
            # Get diffs from parent (if exists)
            if commit.parents:
                diffs = commit.parents[0].diff(commit, create_patch=True)
            else:
                # First commit - all files are new
                diffs = commit.diff(None, create_patch=True)

            for diff in diffs:
                # Determine change type
                if diff.new_file:
                    change_type = "added"
                elif diff.deleted_file:
                    change_type = "deleted"
                elif diff.renamed_file:
                    change_type = "renamed"
                else:
                    change_type = "modified"

                # Get file path (handle renames)
                relative_path = diff.b_path if diff.b_path else diff.a_path
                old_relative_path = diff.a_path if diff.renamed_file else None

                # Convert relative paths to absolute paths (matching File nodes)
                repo_root = Path(self.repo.working_dir)
                file_path = str(repo_root / relative_path) if relative_path else None
                old_path = str(repo_root / old_relative_path) if old_relative_path else None

                # Calculate insertions/deletions (rough estimate from diff stats)
                insertions = 0
                deletions = 0

                if hasattr(diff, 'diff') and diff.diff:
                    diff_text = diff.diff.decode('utf-8', errors='ignore')
                    for line in diff_text.split('\n'):
                        if line.startswith('+') and not line.startswith('+++'):
                            insertions += 1
                        elif line.startswith('-') and not line.startswith('---'):
                            deletions += 1

                modifications.append(FileModification(
                    commit_sha=commit.hexsha,
                    file_path=file_path,
                    change_type=change_type,
                    insertions=insertions,
                    deletions=deletions,
                    old_path=old_path,
                ))

        except Exception as e:
            log.warning(f"Failed to extract modifications for commit {commit.hexsha}: {e}")

        return modifications
