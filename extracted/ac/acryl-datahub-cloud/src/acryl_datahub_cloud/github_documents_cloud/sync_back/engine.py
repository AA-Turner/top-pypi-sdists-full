"""Sync-back engine: write DataHub document edits back to GitHub.

Runs after the OSS import phase. Decoupled from ``PipelineContext`` (it only
needs a ``DataHubGraph``) so the same engine can later back a real-time DataHub
Action without rewriting the GitHub write logic.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

from acryl_datahub_cloud.github_documents_cloud.sync_back.config import (
    ConflictPolicy,
    SyncBackConfig,
    SyncBackMode,
)
from acryl_datahub_cloud.github_documents_cloud.sync_back.content_merge import (
    three_way_merge,
)
from acryl_datahub_cloud.github_documents_cloud.sync_back.document_mapper import (
    PROP_CONTENT_HASH,
    PROP_GITHUB_BLOB_SHA,
    PROP_GITHUB_BRANCH,
    PROP_GITHUB_FILE_PATH,
    PROP_GITHUB_REPO,
    PROP_IMPORT_SOURCE,
    PROP_IS_REPO_ROOT,
    DocumentKind,
    classify_document,
    derive_new_file_path,
    is_document_content_unchanged,
    parent_directory,
    resolve_existing_target,
)
from acryl_datahub_cloud.github_documents_cloud.sync_back.github_writer import (
    CommitFile,
    GitHubWriteClient,
)
from datahub.emitter.mce_builder import make_dataplatform_instance_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.ingestion.graph.filters import RemovedStatusFilter
from datahub.ingestion.source.github_documents.github_api import make_file_source_id
from datahub.ingestion.source.github_documents.github_documents_source import (
    LAST_EXPORTED_CONTENT_HASH_KEY,
    compute_file_content_hash,
)
from datahub.metadata.schema_classes import DocumentInfoClass

if TYPE_CHECKING:
    from datahub.ingestion.graph.client import DataHubGraph

logger = logging.getLogger(__name__)

_PLATFORM = "github"


@dataclass
class _PlannedChange:
    document_urn: str
    github_path: str
    content: str
    content_hash: str
    is_new: bool
    document_info: DocumentInfoClass
    concurrent_edit: bool = False
    had_overlapping_edits: bool = False


@dataclass
class _PlanOutcome:
    """Result of planning a single document: a change, a conflict skip, or neither."""

    change: Optional[_PlannedChange] = None
    conflict_skipped: bool = False


@dataclass
class SyncBackResult:
    files_committed: int = 0
    files_deleted: int = 0
    new_files: int = 0
    conflicts_skipped: int = 0
    concurrent_edits_resolved: int = 0
    deletions_skipped: int = 0
    pull_request_url: Optional[str] = None
    mcps: List[MetadataChangeProposalWrapper] = field(default_factory=list)


class SyncBackEngine:
    def __init__(
        self,
        *,
        graph: "DataHubGraph",
        writer: GitHubWriteClient,
        repo: str,
        config: SyncBackConfig,
        target_branch: str,
        base_directory: str,
        root_document_urn: Optional[str],
        on_conflict: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        self._graph = graph
        self._writer = writer
        self._repo = repo
        self._config = config
        self._target_branch = target_branch
        self._base_directory = base_directory.strip("/")
        self._root_document_urn = root_document_urn
        self._on_conflict = on_conflict

    def run(self) -> SyncBackResult:
        documents = self._collect_documents()
        active_urns = set(documents.keys())
        commit_base_branch = self._commit_base_branch()
        changes, conflicts = self._plan_changes(documents)
        deletions, deletion_conflicts = self._plan_deletions(
            active_urns, commit_base_branch
        )

        if not changes and not deletions:
            return SyncBackResult(
                conflicts_skipped=conflicts + deletion_conflicts,
                deletions_skipped=deletion_conflicts,
            )

        commit_files = [
            CommitFile(path=c.github_path, content=c.content) for c in changes
        ]
        _, commit_sha = self._writer.create_aggregated_commit(
            repo=self._repo,
            base_branch=commit_base_branch,
            files=commit_files,
            deletions=deletions,
            message=self._config.commit_message,
        )

        pull_request_url = self._publish_commit(
            commit_sha,
            [change.github_path for change in changes if change.concurrent_edit],
        )

        mcps = [self._build_stamp_mcp(change) for change in changes]
        new_files = sum(1 for c in changes if c.is_new)
        concurrent_edits_resolved = sum(1 for c in changes if c.concurrent_edit)
        return SyncBackResult(
            files_committed=len(changes),
            files_deleted=len(deletions),
            new_files=new_files,
            conflicts_skipped=conflicts + deletion_conflicts,
            concurrent_edits_resolved=concurrent_edits_resolved,
            deletions_skipped=deletion_conflicts,
            pull_request_url=pull_request_url,
            mcps=mcps,
        )

    def _commit_base_branch(self) -> str:
        """Branch to build the aggregated commit on top of.

        In pull_request mode, stack incremental edits on the existing sync
        branch only while its PR is still open. If the PR was merged or closed
        but the sync branch ref remains, start fresh from the target branch so
        we do not build on stale Git objects.
        """
        if self._config.mode != SyncBackMode.PULL_REQUEST:
            return self._target_branch
        sync_branch = self._config.sync_branch_name
        if not self._writer.branch_exists(self._repo, sync_branch):
            return self._target_branch
        existing = self._writer.find_open_pull_request(
            self._repo, sync_branch, self._target_branch
        )
        if existing is not None:
            return sync_branch
        return self._target_branch

    def _publish_commit(
        self, commit_sha: str, concurrent_edit_paths: List[str]
    ) -> Optional[str]:
        if self._config.mode == SyncBackMode.DIRECT_COMMIT:
            self._writer.update_branch_ref(self._repo, self._target_branch, commit_sha)
            return None

        branch = self._config.sync_branch_name
        self._writer.create_or_reset_branch(self._repo, branch, commit_sha)
        pr_body = self._build_pr_body(concurrent_edit_paths)
        existing = self._writer.find_open_pull_request(
            self._repo, branch, self._target_branch
        )
        if existing is not None:
            self._writer.update_pull_request_body(self._repo, existing.number, pr_body)
            return existing.url
        created = self._writer.create_pull_request(
            repo=self._repo,
            head_branch=branch,
            base_branch=self._target_branch,
            title=self._config.pr_title,
            body=pr_body,
        )
        return created.url

    def _build_pr_body(self, concurrent_edit_paths: List[str]) -> str:
        if not concurrent_edit_paths:
            return self._config.pr_body
        paths = "\n".join(f"- `{path}`" for path in sorted(concurrent_edit_paths))
        return (
            f"{self._config.pr_body.rstrip()}\n\n"
            "## Concurrent edits (review carefully)\n\n"
            "These files also changed on GitHub since the last import. DataHub's "
            "version was included using the configured conflict policy "
            f"(`{self._config.conflict_policy.value}`; `merge` prefers DataHub on "
            "overlapping sections):\n\n"
            f"{paths}"
        )

    def _collect_documents(self) -> Dict[str, DocumentInfoClass]:
        """Enumerate candidate documents: imported files plus new subtree docs."""
        documents: Dict[str, DocumentInfoClass] = {}

        instance_urn = make_dataplatform_instance_urn(_PLATFORM, self._repo)
        for urn in self._graph.get_urns_by_filter(
            entity_types=["document"],
            platform=_PLATFORM,
            platform_instance=instance_urn,
        ):
            info = self._graph.get_aspect(urn, DocumentInfoClass)
            if info is not None:
                documents[urn] = info

        if self._config.propagate_new_documents and self._root_document_urn:
            self._traverse_subtree(self._root_document_urn, documents)

        return documents

    def _collect_soft_deleted_documents(self) -> Dict[str, DocumentInfoClass]:
        """Imported file documents soft-deleted in DataHub (sidebar delete path)."""
        if not self._config.propagate_deleted_documents:
            return {}

        instance_urn = make_dataplatform_instance_urn(_PLATFORM, self._repo)
        documents: Dict[str, DocumentInfoClass] = {}
        for urn in self._graph.get_urns_by_filter(
            entity_types=["document"],
            platform=_PLATFORM,
            platform_instance=instance_urn,
            status=RemovedStatusFilter.ONLY_SOFT_DELETED,
        ):
            info = self._graph.get_aspect(urn, DocumentInfoClass)
            if info is None:
                continue
            props = info.customProperties or {}
            if props.get(PROP_GITHUB_REPO) != self._repo:
                continue
            if classify_document(props) != DocumentKind.EXISTING_FILE:
                continue
            documents[urn] = info
        return documents

    def _plan_deletions(
        self, active_urns: set[str], commit_base_branch: str
    ) -> Tuple[List[str], int]:
        """Return GitHub paths to delete for soft-deleted imported documents."""
        if not self._config.propagate_deleted_documents:
            return [], 0

        soft_deleted = self._collect_soft_deleted_documents()
        paths: List[str] = []
        conflicts = 0
        seen_paths: set[str] = set()

        for urn, info in soft_deleted.items():
            if urn in active_urns:
                continue

            props = info.customProperties or {}
            target = resolve_existing_target(props)
            if target is None or target.repo != self._repo:
                continue
            if target.github_path in seen_paths:
                continue

            if (
                self._has_github_side_conflict(target.github_path, props)
                and not self._should_apply_conflict_policy()
            ):
                if self._on_conflict is not None:
                    self._on_conflict(urn, target.github_path)
                conflicts += 1
                continue

            if (
                self._writer.get_current_blob_sha(
                    self._repo, target.github_path, commit_base_branch
                )
                is None
            ):
                # Already absent on the commit base (including deletions from a
                # prior sync-back commit on the open PR branch).
                continue

            seen_paths.add(target.github_path)
            paths.append(target.github_path)

        return paths, conflicts

    def _traverse_subtree(
        self, root_urn: str, documents: Dict[str, DocumentInfoClass]
    ) -> None:
        queue: List[str] = [root_urn]
        seen = {root_urn}
        while queue:
            parent_urn = queue.pop()
            for child_urn in self._graph.get_urns_by_filter(
                entity_types=["document"],
                extraFilters=[
                    {
                        "field": "parentDocument",
                        "condition": "EQUAL",
                        "values": [parent_urn],
                    }
                ],
            ):
                if child_urn in seen:
                    continue
                seen.add(child_urn)
                if child_urn not in documents:
                    info = self._graph.get_aspect(child_urn, DocumentInfoClass)
                    if info is not None:
                        documents[child_urn] = info
                queue.append(child_urn)

    def _plan_changes(
        self, documents: Dict[str, DocumentInfoClass]
    ) -> Tuple[List[_PlannedChange], int]:
        changes: List[_PlannedChange] = []
        conflicts = 0
        for urn, info in documents.items():
            kind = classify_document(info.customProperties)
            if kind == DocumentKind.FOLDER:
                continue

            text = info.contents.text if info.contents else None
            if text is None:
                continue
            content_hash = compute_file_content_hash(text)

            if kind == DocumentKind.EXISTING_FILE:
                outcome = self._plan_existing_file(urn, info, text, content_hash)
                if outcome.conflict_skipped:
                    conflicts += 1
                elif outcome.change is not None:
                    changes.append(outcome.change)
            elif self._config.propagate_new_documents:
                change = self._plan_new_document(
                    urn, info, text, content_hash, documents
                )
                if change is not None:
                    changes.append(change)
        return changes, conflicts

    def _plan_existing_file(
        self,
        urn: str,
        info: DocumentInfoClass,
        text: str,
        content_hash: str,
    ) -> _PlanOutcome:
        props = info.customProperties or {}
        if is_document_content_unchanged(props, content_hash):
            return _PlanOutcome()  # unchanged in DataHub

        target = resolve_existing_target(props)
        if target is None:
            return _PlanOutcome()

        if self._has_github_side_conflict(target.github_path, props):
            resolved = self._resolve_concurrent_content(target.github_path, props, text)
            if resolved is None:
                if self._on_conflict is not None:
                    self._on_conflict(urn, target.github_path)
                return _PlanOutcome(conflict_skipped=True)

            merged_text, had_overlapping_edits = resolved
            content_hash = compute_file_content_hash(merged_text)
            return _PlanOutcome(
                change=_PlannedChange(
                    document_urn=urn,
                    github_path=target.github_path,
                    content=merged_text,
                    content_hash=content_hash,
                    is_new=False,
                    document_info=info,
                    concurrent_edit=True,
                    had_overlapping_edits=had_overlapping_edits,
                )
            )

        return _PlanOutcome(
            change=_PlannedChange(
                document_urn=urn,
                github_path=target.github_path,
                content=text,
                content_hash=content_hash,
                is_new=False,
                document_info=info,
            )
        )

    def _should_apply_conflict_policy(self) -> bool:
        return self._config.conflict_policy != ConflictPolicy.SKIP

    def _resolve_concurrent_content(
        self, github_path: str, props: Dict[str, str], datahub_text: str
    ) -> Optional[Tuple[str, bool]]:
        """Return merged content and whether overlapping edits were detected."""
        policy = self._config.conflict_policy
        if policy == ConflictPolicy.SKIP:
            return None
        if policy == ConflictPolicy.DATAHUB_WINS:
            return datahub_text, True

        imported_sha = props.get(PROP_GITHUB_BLOB_SHA)
        github_text = self._writer.fetch_file_content(
            self._repo, github_path, self._target_branch
        )
        if github_text is None:
            return datahub_text, False
        if not imported_sha:
            return datahub_text, True

        try:
            base_text = self._writer.fetch_blob_content(self._repo, imported_sha)
        except Exception as exc:
            logger.warning(
                "Could not fetch import snapshot for %s (%s); using DataHub content.",
                github_path,
                exc,
            )
            return datahub_text, True

        merge_result = three_way_merge(base_text, datahub_text, github_text)
        return merge_result.content, merge_result.had_overlapping_edits

    def _has_github_side_conflict(self, path: str, props: Dict[str, str]) -> bool:
        """True if the GitHub file changed since import (would be clobbered)."""
        imported_sha = props.get(PROP_GITHUB_BLOB_SHA)
        if not imported_sha:
            return False
        current_sha = self._writer.get_current_blob_sha(
            self._repo, path, self._target_branch
        )
        return current_sha is not None and current_sha != imported_sha

    def _plan_new_document(
        self,
        urn: str,
        info: DocumentInfoClass,
        text: str,
        content_hash: str,
        documents: Dict[str, DocumentInfoClass],
    ) -> Optional[_PlannedChange]:
        directory = self._resolve_new_document_directory(info, documents)
        if directory is None:
            return None
        title = info.title or "untitled"
        path = derive_new_file_path(directory, title, self._config.new_file_extension)
        return _PlannedChange(
            document_urn=urn,
            github_path=path,
            content=text,
            content_hash=content_hash,
            is_new=True,
            document_info=info,
        )

    def _resolve_new_document_directory(
        self, info: DocumentInfoClass, documents: Dict[str, DocumentInfoClass]
    ) -> Optional[str]:
        """Resolve the GitHub directory a new document should be written into."""
        parent = info.parentDocument.document if info.parentDocument else None
        if parent is None:
            return None
        if parent == self._root_document_urn:
            return self._base_directory

        parent_info = documents.get(parent) or self._graph.get_aspect(
            parent, DocumentInfoClass
        )
        parent_props = parent_info.customProperties if parent_info else None
        if parent_props and parent_props.get(PROP_IS_REPO_ROOT) == "true":
            return self._base_directory
        return parent_directory(parent_props)

    def _build_stamp_mcp(self, change: _PlannedChange) -> MetadataChangeProposalWrapper:
        """Re-emit DocumentInfo with sync-back bookkeeping in customProperties.

        Reuses the OSS ``last_exported_content_hash`` loop-prevention key so the
        next import treats our own write as unchanged. New documents additionally
        gain the import identity props so future imports recognize them.
        """
        info = change.document_info
        props = dict(info.customProperties or {})
        props[LAST_EXPORTED_CONTENT_HASH_KEY] = change.content_hash
        if change.is_new:
            props[PROP_IMPORT_SOURCE] = _PLATFORM
            props[PROP_GITHUB_REPO] = self._repo
            props[PROP_GITHUB_BRANCH] = self._target_branch
            props[PROP_GITHUB_FILE_PATH] = change.github_path
            props[PROP_CONTENT_HASH] = change.content_hash
            props["import_source_id"] = make_file_source_id(
                self._repo, change.github_path
            )
        info.customProperties = props
        return MetadataChangeProposalWrapper(entityUrn=change.document_urn, aspect=info)
