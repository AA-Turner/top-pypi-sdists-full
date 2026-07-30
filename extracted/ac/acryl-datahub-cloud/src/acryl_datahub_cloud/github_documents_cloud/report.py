"""Reporting for the github-documents-cloud source.

Extends the OSS import report with cloud-only sync-back metrics so the OSS report
stays focused on import.
"""

from dataclasses import dataclass
from typing import Optional

from datahub.ingestion.source.github_documents.github_documents_report import (
    GitHubDocumentsSourceReport,
)


@dataclass
class GitHubDocumentsCloudSourceReport(GitHubDocumentsSourceReport):
    sync_back_enabled: bool = False
    sync_back_files_committed: int = 0
    sync_back_files_deleted: int = 0
    sync_back_new_files: int = 0
    sync_back_conflicts_skipped: int = 0
    sync_back_concurrent_edits_resolved: int = 0
    sync_back_deletions_skipped: int = 0
    sync_back_pull_request_url: Optional[str] = None
