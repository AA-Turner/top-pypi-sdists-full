"""Review state schema and CRUD functions for managing hierarchical PR review state.

Provides dataclasses for each schema level and load/save/update functions.
File location: .agdt/workflows/{identity}/{worktree_key}/reviews/review-state.json
"""

import contextlib
import json
import os
import re
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from ...file_locking import FileLockError, locked_file  # noqa: F401 — FileLockError re-exported
from ...state import get_state_dir

REVIEW_STATE_SUBDIR = "reviews"
REVIEW_STATE_FILENAME = "review-state.json"

_LOCK_TIMEOUT_SECONDS = 10.0
_SHORT_COMMIT_HASH_PATTERN = re.compile(r"^[0-9a-f]{12}$")


class ReviewStatus(StrEnum):
    """Status values for PR review items."""

    UNREVIEWED = "unreviewed"
    IN_PROGRESS = "in-progress"
    APPROVED = "approved"
    NEEDS_WORK = "needs-work"


# Statuses that indicate a file/folder review is complete
COMPLETE_STATUSES = frozenset({ReviewStatus.APPROVED.value, ReviewStatus.NEEDS_WORK.value})

# Processing path labels for the review-all-files workflow
PROCESSING_PATH_REVIEWED = "reviewed"
PROCESSING_PATH_INHERITED = "inherited"
PROCESSING_PATH_REVIEWED_NO_PRIOR = "reviewed-no-prior"


def compute_aggregate_status(statuses: list[str]) -> str:
    """Compute an aggregate status from a list of child statuses.

    This is the single source of truth for status derivation rules:
    - No statuses or all unreviewed → unreviewed
    - At least 1 started, not all complete → in-progress
    - All complete, all Approved → approved
    - All complete, any Needs Work → needs-work

    Args:
        statuses: List of status strings (ReviewStatus values).

    Returns:
        Derived aggregate status string.
    """
    if not statuses:
        return ReviewStatus.UNREVIEWED.value

    any_started = any(s != ReviewStatus.UNREVIEWED.value for s in statuses)
    all_complete = all(s in COMPLETE_STATUSES for s in statuses)

    if not any_started:
        return ReviewStatus.UNREVIEWED.value
    elif not all_complete:
        return ReviewStatus.IN_PROGRESS.value
    elif any(s == ReviewStatus.NEEDS_WORK.value for s in statuses):
        return ReviewStatus.NEEDS_WORK.value
    else:
        return ReviewStatus.APPROVED.value


@dataclass
class SuggestionEntry:
    """A suggestion posted on a specific line/range of a file."""

    threadId: int
    commentId: int
    line: int
    endLine: int
    severity: str
    outOfScope: bool
    linkText: str
    content: str
    replacement_code: str | None = None

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        d: dict = {
            "threadId": self.threadId,
            "commentId": self.commentId,
            "line": self.line,
            "endLine": self.endLine,
            "severity": self.severity,
            "outOfScope": self.outOfScope,
            "linkText": self.linkText,
            "content": self.content,
        }
        if self.replacement_code is not None and self.replacement_code.strip():
            d["replacementCode"] = self.replacement_code
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "SuggestionEntry":
        """Deserialize from a dictionary."""
        raw_rc = data.get("replacementCode")
        if raw_rc is None:
            raw_rc = data.get("replacement_code")
        return cls(
            threadId=data["threadId"],
            commentId=data["commentId"],
            line=data["line"],
            endLine=data["endLine"],
            severity=data["severity"],
            outOfScope=data["outOfScope"],
            linkText=data["linkText"],
            content=data["content"],
            replacement_code=raw_rc if isinstance(raw_rc, str) else None,
        )


@dataclass
class SkippedFile:
    """A file that was skipped during prompt generation.

    Note: The ``already_reviewed`` reason is deprecated and no longer produced
    by the review workflow. Only ``not_on_branch`` is actively used.
    The class is retained for backward-compatible deserialization.
    """

    path: str
    reason: str  # "not_on_branch" (active) or "already_reviewed" (deprecated)

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        return {"path": self.path, "reason": self.reason}

    @classmethod
    def from_dict(cls, data: dict) -> "SkippedFile":
        """Deserialize from a dictionary."""
        return cls(path=data["path"], reason=data["reason"])


@dataclass
class OverallSummary:
    """Overall PR review summary metadata."""

    threadId: int
    commentId: int
    status: str = ReviewStatus.UNREVIEWED.value
    narrativeSummary: str | None = None

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        return {
            "threadId": self.threadId,
            "commentId": self.commentId,
            "status": self.status,
            "narrativeSummary": self.narrativeSummary,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OverallSummary":
        """Deserialize from a dictionary."""
        return cls(
            threadId=data["threadId"],
            commentId=data["commentId"],
            status=data.get("status", ReviewStatus.UNREVIEWED.value),
            narrativeSummary=data.get("narrativeSummary"),
        )


@dataclass
class FolderGroup:
    """Lightweight folder grouping — maps a folder name to its file paths.

    Unlike the former ``FolderEntry``, this class carries **no** Azure DevOps
    thread metadata (threadId / commentId / status).  Folder-level threads
    have been eliminated; folders are now lightweight groupings within the
    PR summary comment.
    """

    files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        return {
            "files": self.files,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FolderGroup":
        """Deserialize from a dictionary.

        File paths in the files list are normalized to ensure leading slash.
        """
        return cls(
            files=[normalize_file_path(f) for f in data.get("files", [])],
        )


# Keep backward-compatible alias so downstream code that still references the
# old name does not break at import time.
FolderEntry = FolderGroup


def _validate_file_entry_attribution(data: dict) -> None:
    """Validate optional runtime attribution fields before deserialization."""
    optional_fields = {
        "modelId": str,
        "providerType": str,
        "latencyMs": int,
        "finishReason": str,
        "tokensUsed": int,
        "processingPath": str,
    }
    for field_name, expected_type in optional_fields.items():
        value = data.get(field_name)
        if value is not None and type(value) is not expected_type:
            raise ValueError(f"FileEntry field {field_name!r} must be {expected_type.__name__} or None")

    cross_identity = data.get("crossIdentity", False)
    if type(cross_identity) is not bool:
        raise ValueError("FileEntry field 'crossIdentity' must be bool")


@dataclass
class FileEntry:
    """Review state for an individual file."""

    threadId: int
    commentId: int
    folder: str
    fileName: str
    status: str = ReviewStatus.UNREVIEWED.value
    summary: str | None = None
    changeTrackingId: int | None = None
    suggestions: list[SuggestionEntry] = field(default_factory=list)
    previousSuggestions: list[SuggestionEntry] | None = None
    suggestionVerificationStatus: str | None = None
    modelId: str | None = None
    providerType: str | None = None
    latencyMs: int | None = None
    finishReason: str | None = None
    tokensUsed: int | None = None
    processingPath: str | None = None
    crossIdentity: bool = False

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        result = {
            "threadId": self.threadId,
            "commentId": self.commentId,
            "folder": self.folder,
            "fileName": self.fileName,
            "status": self.status,
            "summary": self.summary,
            "changeTrackingId": self.changeTrackingId,
            "suggestions": [s.to_dict() for s in self.suggestions],
            "previousSuggestions": (
                [s.to_dict() for s in self.previousSuggestions] if self.previousSuggestions is not None else None
            ),
            "suggestionVerificationStatus": self.suggestionVerificationStatus,
        }
        if self.processingPath is not None:
            result["processingPath"] = self.processingPath
        if self.crossIdentity:
            result["crossIdentity"] = self.crossIdentity
        if self.modelId is not None:
            result["modelId"] = self.modelId
        if self.providerType is not None:
            result["providerType"] = self.providerType
        if self.latencyMs is not None:
            result["latencyMs"] = self.latencyMs
        if self.finishReason is not None:
            result["finishReason"] = self.finishReason
        if self.tokensUsed is not None:
            result["tokensUsed"] = self.tokensUsed
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "FileEntry":
        """Deserialize from a dictionary."""
        _validate_file_entry_attribution(data)
        suggestions = [SuggestionEntry.from_dict(s) for s in data.get("suggestions", [])]
        raw_prev = data.get("previousSuggestions")
        previous = [SuggestionEntry.from_dict(s) for s in raw_prev] if raw_prev is not None else None
        return cls(
            threadId=data["threadId"],
            commentId=data["commentId"],
            folder=data["folder"],
            fileName=data["fileName"],
            status=data.get("status", ReviewStatus.UNREVIEWED.value),
            summary=data.get("summary"),
            changeTrackingId=data.get("changeTrackingId"),
            suggestions=suggestions,
            previousSuggestions=previous,
            suggestionVerificationStatus=data.get("suggestionVerificationStatus"),
            modelId=data.get("modelId"),
            providerType=data.get("providerType"),
            latencyMs=data.get("latencyMs"),
            finishReason=data.get("finishReason"),
            tokensUsed=data.get("tokensUsed"),
            processingPath=data.get("processingPath"),
            crossIdentity=data.get("crossIdentity", False),
        )


def is_valid_prior_state(file_entry: FileEntry, prior_commit_hash: str | None) -> bool:
    """Check if a file entry represents a valid completed prior review.

    Args:
        file_entry: The file entry to validate.
        prior_commit_hash: The commit hash from the prior review session.

    Returns:
        True only when status is terminal, threadId and commentId are truthy,
        folder is non-empty, and prior_commit_hash is truthy.
    """
    if not prior_commit_hash:
        return False
    if file_entry.status not in COMPLETE_STATUSES:
        return False
    if not file_entry.threadId:
        return False
    if not file_entry.commentId:
        return False
    if not file_entry.folder:
        return False
    return True


def can_inherit_file(file_entry: FileEntry, is_unchanged: bool, prior_commit_hash: str | None) -> bool:
    """Check if a file can inherit its prior review state.

    Args:
        file_entry: The file entry from the prior state.
        is_unchanged: Whether the file has no changes since the last review.
        prior_commit_hash: The commit hash from the prior review session.

    Returns:
        True when both is_unchanged and is_valid_prior_state() are True.
    """
    return is_unchanged and is_valid_prior_state(file_entry, prior_commit_hash)


def determine_processing_path(file_entry: FileEntry | None, is_unchanged: bool, prior_commit_hash: str | None) -> str:
    """Determine the processing path label for a file.

    Args:
        file_entry: The file entry from the prior state, or None if no prior exists.
        is_unchanged: Whether the file has no changes since the last review.
        prior_commit_hash: The commit hash from the prior review session.

    Returns:
        One of PROCESSING_PATH_REVIEWED, PROCESSING_PATH_INHERITED,
        or PROCESSING_PATH_REVIEWED_NO_PRIOR.
    """
    if not is_unchanged:
        return PROCESSING_PATH_REVIEWED

    if file_entry is None:
        return PROCESSING_PATH_REVIEWED_NO_PRIOR

    if can_inherit_file(file_entry, is_unchanged, prior_commit_hash):
        return PROCESSING_PATH_INHERITED

    return PROCESSING_PATH_REVIEWED_NO_PRIOR


@dataclass
class ModelCommentRef:
    """A single model's review comment within a per-commit review thread.

    The first model's ref holds the commit thread's *root* comment id; any
    additional models are posted as replies within the same commit thread, so a
    second model reviewing the same commit appends rather than creating a new
    top-level comment. Each ref also tracks its own continuation reply comment
    ids for the >50k smart-cutoff roll-over.

    Attributes:
        modelId: Model identifier (e.g. "Claude Opus 4.6").
        commentId: Root comment id for this model's review within the thread.
        continuationCommentIds: Ordered continuation reply comment ids holding
            the overflow content when the rendered review exceeds the cutoff.
        status: Aggregate review status for this model on this commit.
        timestamp: ISO-8601 timestamp when this model's review was last updated.
    """

    modelId: str
    commentId: int = 0
    continuationCommentIds: list[int] = field(default_factory=list)
    status: str = ReviewStatus.UNREVIEWED.value
    timestamp: str | None = None

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        return {
            "modelId": self.modelId,
            "commentId": self.commentId,
            "continuationCommentIds": list(self.continuationCommentIds),
            "status": self.status,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelCommentRef":
        """Deserialize from a dictionary."""
        return cls(
            modelId=data["modelId"],
            commentId=data.get("commentId", 0),
            continuationCommentIds=list(data.get("continuationCommentIds", [])),
            status=data.get("status", ReviewStatus.UNREVIEWED.value),
            timestamp=data.get("timestamp"),
        )


@dataclass
class CommitComment:
    """Per-commit review comment registry entry.

    Tracks the single top-level thread created for one reviewed commit SHA, its
    per-model comment refs (root + replies), aggregate status, and the time it
    was last updated. Used to build the "Previous reviews" index and to route
    re-reviews / additional-model reviews to the correct thread.

    Attributes:
        commitHash: Full 40-char SHA of the reviewed commit.
        threadId: Azure DevOps thread id holding this commit's review comment(s).
        models: Per-model comment refs; the first entry's ``commentId`` is the
            thread's root comment id.
        status: Aggregate review status for this commit.
        timestamp: ISO-8601 timestamp when this commit's review was last updated.
    """

    commitHash: str
    threadId: int = 0
    models: list[ModelCommentRef] = field(default_factory=list)
    status: str = ReviewStatus.UNREVIEWED.value
    timestamp: str | None = None

    @property
    def rootCommentId(self) -> int:
        """Return the thread's root comment id (the first model's comment id)."""
        return self.models[0].commentId if self.models else 0

    def get_model(self, model_id: str) -> "ModelCommentRef | None":
        """Return the comment ref for *model_id*, or None when absent."""
        for ref in self.models:
            if ref.modelId == model_id:
                return ref
        return None

    def upsert_model(self, model_id: str) -> "ModelCommentRef":
        """Return the existing ref for *model_id* or append and return a new one."""
        existing = self.get_model(model_id)
        if existing is not None:
            return existing
        ref = ModelCommentRef(modelId=model_id)
        self.models.append(ref)
        return ref

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        return {
            "commitHash": self.commitHash,
            "threadId": self.threadId,
            "models": [m.to_dict() for m in self.models],
            "status": self.status,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CommitComment":
        """Deserialize from a dictionary."""
        return cls(
            commitHash=data["commitHash"],
            threadId=data.get("threadId", 0),
            models=[ModelCommentRef.from_dict(m) for m in data.get("models", [])],
            status=data.get("status", ReviewStatus.UNREVIEWED.value),
            timestamp=data.get("timestamp"),
        )


@dataclass
class ReviewSession:
    """Tracks an individual review session.

    Each session represents one AI agent reviewing the PR. Multiple sessions
    can exist for multi-model reviews or re-reviews.
    """

    sessionId: str
    modelId: str
    startedUtc: str
    completedUtc: str | None = None
    status: str = "pending"
    commitHash: str | None = None  # Full 40-char SHA of the commit this session reviewed (differs on re-reviews)
    activityLogCommentId: int | None = None
    engine: str | None = None  # Review engine used: "default" or "langchain" (None for backward compat)

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        result = {
            "sessionId": self.sessionId,
            "modelId": self.modelId,
            "startedUtc": self.startedUtc,
            "completedUtc": self.completedUtc,
            "status": self.status,
            "commitHash": self.commitHash,
            "activityLogCommentId": self.activityLogCommentId,
        }
        if self.engine is not None:
            result["engine"] = self.engine
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewSession":
        """Deserialize from a dictionary."""
        return cls(
            sessionId=data["sessionId"],
            modelId=data["modelId"],
            startedUtc=data["startedUtc"],
            completedUtc=data.get("completedUtc"),
            status=data.get("status", "pending"),
            commitHash=data.get("commitHash"),
            activityLogCommentId=data.get("activityLogCommentId"),
            engine=data.get("engine"),
        )


@dataclass
class ReviewState:
    """Top-level PR review state."""

    prId: int
    repoId: str
    repoName: str
    project: str
    organization: str
    latestIterationId: int
    scaffoldedUtc: str
    overallSummary: OverallSummary
    folders: dict[str, FolderGroup] = field(default_factory=dict)
    files: dict[str, FileEntry] = field(default_factory=dict)
    commitHash: str | None = None  # Canonical full 40-char SHA from lastMergeSourceCommit.commitId, set during scaffold
    modelId: str | None = None
    activityLogThreadId: int = 0
    sessions: list[ReviewSession] = field(default_factory=list)
    rebaseConflicts: bool = False
    skippedFiles: list[SkippedFile] = field(default_factory=list)
    commitComments: dict[str, CommitComment] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dictionary."""
        result = {
            "prId": self.prId,
            "repoId": self.repoId,
            "repoName": self.repoName,
            "project": self.project,
            "organization": self.organization,
            "latestIterationId": self.latestIterationId,
            "scaffoldedUtc": self.scaffoldedUtc,
            "overallSummary": self.overallSummary.to_dict(),
            "folders": {k: v.to_dict() for k, v in self.folders.items()},
            "files": {k: v.to_dict() for k, v in self.files.items()},
            "commitHash": self.commitHash,
            "modelId": self.modelId,
            "activityLogThreadId": self.activityLogThreadId,
            "sessions": [s.to_dict() for s in self.sessions],
        }
        result["rebaseConflicts"] = self.rebaseConflicts
        if self.skippedFiles:
            result["skippedFiles"] = [sf.to_dict() for sf in self.skippedFiles]
        if self.commitComments:
            result["commitComments"] = {k: v.to_dict() for k, v in self.commitComments.items()}
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewState":
        """Deserialize from a dictionary.

        File dict keys are normalized to ensure leading slash consistency.
        Missing ``commitHash`` defaults to ``None`` for direct callers, but
        ``load_review_state()`` enforces migration — it deletes state files
        lacking ``commitHash`` and raises ``FileNotFoundError``.

        Legacy multi-model fields (``reviewerModels``, ``bossModel``,
        ``modelVerdicts``, ``consolidationStatus``) present in older state files
        are silently ignored for backward compatibility.
        """
        overall_summary = OverallSummary.from_dict(data["overallSummary"])
        folders = {k: FolderGroup.from_dict(v) for k, v in data.get("folders", {}).items()}
        files = {normalize_file_path(k): FileEntry.from_dict(v) for k, v in data.get("files", {}).items()}
        sessions = [ReviewSession.from_dict(s) for s in data.get("sessions", [])]
        return cls(
            prId=data["prId"],
            repoId=data["repoId"],
            repoName=data["repoName"],
            project=data["project"],
            organization=data["organization"],
            latestIterationId=data["latestIterationId"],
            scaffoldedUtc=data["scaffoldedUtc"],
            overallSummary=overall_summary,
            folders=folders,
            files=files,
            commitHash=data.get("commitHash"),
            modelId=data.get("modelId"),
            activityLogThreadId=data.get("activityLogThreadId", 0),
            sessions=sessions,
            rebaseConflicts=data.get("rebaseConflicts", False),
            skippedFiles=[SkippedFile.from_dict(sf) for sf in data.get("skippedFiles", [])],
            commitComments={k: CommitComment.from_dict(v) for k, v in data.get("commitComments", {}).items()},
        )


def normalize_file_path(file_path: str) -> str:
    """
    Normalize a file path to ensure it has a leading slash and forward slashes.

    Args:
        file_path: The file path to normalize.

    Returns:
        Normalized path with leading slash and forward slashes.
    """
    file_path = file_path.replace("\\", "/")
    if not file_path.startswith("/"):
        return "/" + file_path
    return file_path


def get_review_state_file_path(pr_id: int) -> Path:
    """
    Get the path to the review-state.json file.

    After the migration to .agdt/workflows/, the path is scoped by
    identity and worktree_key (via ``get_state_dir()``), not by PR ID.
    The ``pr_id`` parameter is retained for caller compatibility but
    is no longer used in path construction.

    Args:
        pr_id: Pull request ID (retained for backward compatibility).

    Returns:
        Path to review-state.json.
    """
    return get_state_dir() / REVIEW_STATE_SUBDIR / REVIEW_STATE_FILENAME


def _get_lock_file_path(pr_id: int) -> Path:
    """Return the sidecar lock file path for review-state.json.

    The lock file is located alongside the data file:
    ``<state_dir>/reviews/review-state.json.lock``

    Args:
        pr_id: Pull request ID (forwarded to ``get_review_state_file_path``).
    """
    return get_review_state_file_path(pr_id).parent / "review-state.json.lock"


def _atomic_write_json(file_path: Path, content: str) -> None:
    """Write *content* to *file_path* atomically via a temp file + ``os.replace``.

    The temporary file is created in the **same directory** as *file_path*
    to guarantee that ``os.replace`` never crosses filesystem boundaries.
    On error, the temp file is cleaned up (best-effort) and the original
    file remains untouched.
    """
    fd = tempfile.NamedTemporaryFile(
        mode="w",
        dir=file_path.parent,
        suffix=".tmp",
        delete=False,
        encoding="utf-8",
    )
    try:
        fd.write(content)
        fd.flush()
        fd.close()
        os.replace(fd.name, str(file_path))
    except BaseException:
        fd.close()
        with contextlib.suppress(OSError):
            os.unlink(fd.name)
        raise


def _validate_and_deserialize(
    data: dict,
    pr_id: int,
    file_path: Path,
    *,
    delete_on_migration: bool,
) -> ReviewState:
    """Validate and deserialize review state data, with migration detection.

    Args:
        data: Parsed JSON data.
        pr_id: PR ID for error messages and PR ID mismatch detection.
        file_path: Local file path (for deletion if migration needed).
        delete_on_migration: If True, delete the local file when
            incompatible format is detected or PR ID mismatches.
            False when data came from the -agdt branch (nothing local
            to delete).

    Returns:
        ReviewState object.

    Raises:
        FileNotFoundError: If incompatible format detected or PR ID
            does not match ``pr_id``.
    """
    # PR ID mismatch: the per-worktree file may belong to a different PR
    # (e.g., worktree reused for another PR review).
    stored_id = data.get("prId") if isinstance(data, dict) else None
    if stored_id != pr_id:
        if delete_on_migration:
            print(
                f"Review state PR ID mismatch (file has {stored_id}, expected {pr_id}). Deleting and re-scaffolding.",
                file=sys.stderr,
            )
            if file_path.exists():
                file_path.unlink()
        else:
            print(
                f"Review state PR ID mismatch (file has {stored_id}, expected {pr_id}). Re-scaffolding required.",
                file=sys.stderr,
            )
        raise FileNotFoundError(f"Review state not found for PR {pr_id}: {file_path}")

    needs_migration = "commitHash" not in data
    folders = data.get("folders", {})
    if not needs_migration and isinstance(folders, dict):
        for folder_data in folders.values():
            if isinstance(folder_data, dict) and folder_data.get("threadId", 0) != 0:
                needs_migration = True
                break
    elif not isinstance(folders, dict):
        needs_migration = True

    if needs_migration:
        if delete_on_migration:
            print(
                f"Incompatible review state format detected for PR {pr_id}. Deleting and re-scaffolding.",
                file=sys.stderr,
            )
            if file_path.exists():
                file_path.unlink()
        else:
            print(
                f"Incompatible review state format detected for PR {pr_id}. Re-scaffolding required.",
                file=sys.stderr,
            )
        raise FileNotFoundError(f"Review state not found for PR {pr_id}: {file_path}")

    return ReviewState.from_dict(data)


def _load_from_branch(
    source_branch: str | None,
    worktree_key: str | None,
) -> dict | None:
    """Attempt to load review-state.json from the -agdt branch.

    Returns the parsed dict if found, or None if unavailable.
    Expected failure modes (import unavailable, worktree resolution,
    git plumbing, JSON parsing) are caught individually.
    """
    try:
        from ...state import get_value
        from ..git.agdt_branch import (
            GitPlumbingError,
            load_workflow_artifacts,
            resolve_worktree_key,
        )
    except ImportError:
        return None

    try:
        # Resolve source_branch
        effective_branch = source_branch
        if not effective_branch:
            effective_branch = get_value("versionControl.currentBranch")
        if not effective_branch or not str(effective_branch).strip():
            return None
        effective_branch = str(effective_branch).strip()

        # Resolve worktree_key — raises ValueError when unresolvable
        effective_key = worktree_key
        if not effective_key:
            try:
                effective_key = resolve_worktree_key()
            except ValueError:
                return None

        artifacts = load_workflow_artifacts(
            source_branch=effective_branch,
            worktree_key=effective_key,
            workflow_type="reviews",
        )
        if artifacts is None:
            return None

        # Find the review-state.json entry
        for path, content in artifacts.items():
            if path.endswith(REVIEW_STATE_FILENAME):
                if isinstance(content, dict):
                    return content
                if isinstance(content, str):
                    return json.loads(content)
        return None
    except (GitPlumbingError, json.JSONDecodeError, KeyError, TypeError):
        return None


def load_review_state(
    pr_id: int,
    *,
    fallback_to_branch: bool = True,
    source_branch: str | None = None,
    worktree_key: str | None = None,
) -> ReviewState:
    """
    Load review state from JSON file.

    Implements migration detection: if the state file uses the old format
    (``FolderEntry`` with ``threadId`` fields or missing ``commitHash``),
    or the stored ``prId`` does not match the requested *pr_id*, the local
    file is deleted and ``FileNotFoundError`` is raised so the caller
    proceeds with a fresh scaffolding run.  When data comes from the
    ``-agdt`` branch fallback, the same validation is performed but no
    local file is deleted (there is nothing local to remove).

    When the local file does not exist and ``fallback_to_branch`` is
    ``True``, attempts to read review-state.json from the ``-agdt``
    branch via ``load_workflow_artifacts()``.

    Args:
        pr_id: Pull request ID (retained for backward compatibility).
        fallback_to_branch: If True (default), attempt to load from the
            -agdt branch when local file is missing.
        source_branch: Optional source branch name for branch fallback.
            When None, resolved from state
            (``get_value("versionControl.currentBranch")``).
        worktree_key: Optional worktree key for branch fallback.
            When None, resolved via ``resolve_worktree_key()``.

    Returns:
        ReviewState object.

    Raises:
        FileNotFoundError: If review-state.json does not exist locally
            (and branch fallback is disabled or unavailable), or if an
            incompatible old-format file was detected (deleted when local,
            left in place when from branch fallback).
    """
    file_path = get_review_state_file_path(pr_id)

    if file_path.exists():
        lock_path = _get_lock_file_path(pr_id)
        # Use "r+" so the handle starts at offset 0 — required for
        # consistent byte-range locking on Windows (msvcrt.locking).
        with locked_file(lock_path, mode="r+", exclusive=False, timeout=_LOCK_TIMEOUT_SECONDS):
            content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)
        return _validate_and_deserialize(data, pr_id, file_path, delete_on_migration=True)

    # Local file not found — attempt branch fallback
    if fallback_to_branch:
        data = _load_from_branch(source_branch, worktree_key)
        if data is not None:
            return _validate_and_deserialize(data, pr_id, file_path, delete_on_migration=False)

    raise FileNotFoundError(f"Review state not found for PR {pr_id}: {file_path}")


def derive_commit_hash_short(pr_id: int) -> str:
    """Derive the short commit-hash artifact-directory segment from review-state.json.

    This is the fallback source of truth for ``commit_hash_short`` when the
    ``review.commit_hash_short`` state key is absent — e.g. it has not been
    written yet, or was written to a different scope after a bootstrap
    re-scope (see issue #1182). ``review-state.json`` is stored at a fixed
    location under the state dir (independent of the commit-hash-scoped
    artifact directory it is used to locate), so it does not suffer from the
    same chicken-and-egg problem.

    Reads the local file directly under a shared sidecar lock and never
    attempts branch fallback, so it stays a fast, local-only check suitable
    for high-frequency callers (queue/answers-directory resolution).

    Args:
        pr_id: Pull request ID whose review state to consult.

    Returns:
        The first 12 characters of ``commitHash`` when they form a safe,
        hexadecimal short SHA in a valid local review-state.json record;
        otherwise an empty string.
    """
    from ...state import is_safe_dir_segment

    try:
        file_path = get_review_state_file_path(pr_id)
        if not file_path.exists():
            return ""
        lock_path = _get_lock_file_path(pr_id)
        with locked_file(lock_path, mode="r+", exclusive=False, timeout=_LOCK_TIMEOUT_SECONDS):
            content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)
        if not isinstance(data, dict):
            return ""
        stored_pr_id = data.get("prId")
        if isinstance(stored_pr_id, bool) or not isinstance(stored_pr_id, int):
            return ""
        if stored_pr_id != pr_id:
            return ""
        commit_hash = data.get("commitHash")
    except (AttributeError, FileNotFoundError, OSError, TypeError, ValueError, KeyError, FileLockError):
        return ""
    if not isinstance(commit_hash, str) or not commit_hash:
        return ""
    derived = commit_hash.strip()[:12]
    if not is_safe_dir_segment(derived):
        return ""
    return derived if _SHORT_COMMIT_HASH_PATTERN.fullmatch(derived) else ""


def save_review_state(review_state: ReviewState) -> None:
    """
    Save review state to JSON file atomically.

    Acquires an exclusive lock on the sidecar ``.lock`` file, writes JSON
    to a temporary file in the same directory, then atomically replaces
    the target via ``os.replace()``.  After writing, calls ``mark_dirty()``
    so the auto-persist hook commits the change to the ``-agdt`` branch.

    Args:
        review_state: ReviewState object to save.

    Raises:
        FileLockError: If the exclusive lock cannot be acquired within
            the configured timeout.
    """
    file_path = get_review_state_file_path(review_state.prId)
    lock_path = _get_lock_file_path(review_state.prId)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(review_state.to_dict(), indent=2, ensure_ascii=False)

    # Use "r+" so the handle starts at offset 0 — required for
    # consistent byte-range locking on Windows (msvcrt.locking).
    with locked_file(lock_path, mode="r+", exclusive=True, timeout=_LOCK_TIMEOUT_SECONDS):
        _atomic_write_json(file_path, content)

    # Signal that review state has been mutated for auto-persist.
    try:
        from ..git.agdt_branch import mark_dirty

        mark_dirty()
    except ImportError:
        pass  # agdt_branch not available (e.g., minimal install)


@contextlib.contextmanager
def read_modify_write_review_state(pr_id: int) -> Iterator[ReviewState]:
    """Load, mutate, and atomically save review state under an exclusive lock.

    Holds an exclusive lock across the entire load → mutate → save cycle
    so that concurrent processes cannot interleave reads and writes.

    Usage::

        with read_modify_write_review_state(pr_id) as state:
            state.latestIterationId += 1

    If the caller raises an exception inside the context, the save is
    skipped and the exception propagates.  The lock is always released.

    Args:
        pr_id: Pull request ID.

    Yields:
        The loaded ``ReviewState`` for in-place mutation.

    Raises:
        FileNotFoundError: If the review-state.json file does not exist.
        FileLockError: If the exclusive lock cannot be acquired.
    """
    file_path = get_review_state_file_path(pr_id)
    lock_path = _get_lock_file_path(pr_id)

    # Use "r+" so the handle starts at offset 0 — required for
    # consistent byte-range locking on Windows (msvcrt.locking).
    with locked_file(lock_path, mode="r+", exclusive=True, timeout=_LOCK_TIMEOUT_SECONDS):
        # Read under the exclusive lock (no branch fallback — local only).
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content)
        state = _validate_and_deserialize(data, pr_id, file_path, delete_on_migration=True)

        yield state

        # Save atomically (still under the exclusive lock).
        new_content = json.dumps(state.to_dict(), indent=2, ensure_ascii=False)
        _atomic_write_json(file_path, new_content)

    # mark_dirty *after* the lock is released (same pattern as save_review_state).
    try:
        from ..git.agdt_branch import mark_dirty

        mark_dirty()
    except ImportError:
        pass  # agdt_branch not available (e.g., minimal install)


def get_file_entry(review_state: ReviewState, file_path: str) -> FileEntry | None:
    """
    Get a file entry from review state by file path.

    Args:
        review_state: ReviewState object.
        file_path: File path (with or without leading slash).

    Returns:
        FileEntry if found, None otherwise.
    """
    normalized = normalize_file_path(file_path)
    return review_state.files.get(normalized)


def get_folder_entry(review_state: ReviewState, folder_name: str) -> FolderGroup | None:
    """
    Get a folder entry from review state by folder name.

    Args:
        review_state: ReviewState object.
        folder_name: Folder name.

    Returns:
        FolderGroup if found, None otherwise.
    """
    return review_state.folders.get(folder_name)


def complete_active_session(review_state: ReviewState, now: datetime | None = None) -> ReviewSession | None:
    """Mark the active in-progress review session as completed.

    The consolidated review comment renders its embedded Activity Log
    directly from ``review_state.sessions`` (see
    ``consolidated_review._render_activity_log_block``), so a session stuck
    at ``status == "in_progress"`` leaves the PR-visible Activity Log stuck
    too, even after the workflow has advanced to its decision/completion
    step (see issue #1181). Call this once the review outcome is final —
    before re-rendering/cascading the consolidated comment — so the
    Activity Log reflects the terminal status.

    Sessions are scanned most-recent-first. When ``review_state.commitHash``
    is set, only sessions matching that commit are eligible, so a stale
    ``in_progress`` session from an earlier re-review (different commit) is
    left untouched. Sessions with ``commitHash=None`` remain eligible even
    when ``review_state.commitHash`` is set: ``ReviewSession.commitHash`` was
    added after sessions were first introduced, so pre-existing sessions may
    predate commit tracking and must not be permanently stuck "in_progress"
    for lacking a value that didn't exist yet when they were created.

    When ``review_state.modelId`` is set, eligibility is further scoped to
    that model's sessions so repeated completion attempts do not close another
    reviewer's concurrent session for the same commit. The helper only ever
    considers the single newest eligible session: if that session is already
    terminal, the call is a no-op rather than scanning backward to older
    sessions. When ``review_state.commitHash`` is unset, the newest eligible
    session (regardless of commit) is considered.

    Args:
        review_state: ReviewState object (mutated in place).
        now: Optional timestamp to use for ``completedUtc`` (for
            deterministic tests). Defaults to the current UTC time.

    Returns:
        The ReviewSession that was transitioned to "completed", or None if
        no matching in-progress session was found.
    """
    candidates = reversed(review_state.sessions)
    if review_state.commitHash:
        matching = [s for s in candidates if s.commitHash is None or s.commitHash == review_state.commitHash]
    else:
        matching = list(candidates)
    if review_state.modelId:
        matching = [s for s in matching if s.modelId == review_state.modelId]
    if not matching:
        return None

    session = matching[0]
    if session.status != "in_progress":
        return None
    session.status = "completed"
    session.completedUtc = (now or datetime.now(UTC)).isoformat()
    return session


def update_file_status(
    review_state: ReviewState,
    file_path: str,
    status: str,
    summary: str | None = None,
    suggestions: list[SuggestionEntry] | None = None,
) -> ReviewState:
    """
    Update the status (and optionally summary/suggestions) of a file in review state.

    Args:
        review_state: ReviewState object.
        file_path: File path to update.
        status: New status value (must be a valid ReviewStatus value).
        summary: Optional new summary text.
        suggestions: Optional new suggestions list (replaces existing).

    Returns:
        Updated ReviewState.

    Raises:
        KeyError: If file not found in review state.
        ValueError: If status is not a valid ReviewStatus value.
    """
    valid_statuses = {s.value for s in ReviewStatus}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {sorted(valid_statuses)}")

    normalized = normalize_file_path(file_path)
    if normalized not in review_state.files:
        raise KeyError(f"File not found in review state: {normalized}")

    file_entry = review_state.files[normalized]
    file_entry.status = status
    if summary is not None:
        file_entry.summary = summary
    if suggestions is not None:
        file_entry.suggestions = suggestions

    return review_state


def add_suggestion_to_file(
    review_state: ReviewState,
    file_path: str,
    suggestion: SuggestionEntry,
) -> ReviewState:
    """
    Add a suggestion to a file's suggestions list.

    Args:
        review_state: ReviewState object.
        file_path: File path to add suggestion to.
        suggestion: SuggestionEntry to add.

    Returns:
        Updated ReviewState.

    Raises:
        KeyError: If file not found in review state.
    """
    normalized = normalize_file_path(file_path)
    if normalized not in review_state.files:
        raise KeyError(f"File not found in review state: {normalized}")

    review_state.files[normalized].suggestions.append(suggestion)
    return review_state


def clear_suggestions_for_re_review(
    review_state: ReviewState,
    file_path: str,
) -> ReviewState:
    """
    Rotate current suggestions to previousSuggestions for a re-review.

    When a file is being re-reviewed (status is already "approved" or "needs-work"),
    the existing suggestions are moved to ``previousSuggestions`` as an audit trail
    and ``suggestions`` is cleared so that new suggestion threads can be created
    fresh.  Old threads in Azure DevOps are NOT resolved — only the local state
    pointer is cleared.

    The rotation fires when **both** conditions are met:

    1. Status is terminal (``approved`` or ``needs-work``).
    2. ``previousSuggestions is None`` (no prior rotation yet).

    Using ``None`` (not ``[]``) as the sentinel avoids a retry-safety bug: even
    when a terminal file had zero old suggestions, the rotation sets
    ``previousSuggestions = []`` which is distinct from ``None``, so a subsequent
    retry will correctly skip rotation and preserve any partially-accumulated new
    suggestions.

    Args:
        review_state: ReviewState object (mutated in-place).
        file_path: File path whose suggestions should be rotated.

    Returns:
        Updated ReviewState.

    Raises:
        KeyError: If file not found in review state.
    """
    normalized = normalize_file_path(file_path)
    if normalized not in review_state.files:
        raise KeyError(f"File not found in review state: {normalized}")

    file_entry = review_state.files[normalized]
    re_review_statuses = {ReviewStatus.APPROVED.value, ReviewStatus.NEEDS_WORK.value}

    # Only rotate when entering a fresh re-review (previousSuggestions is None).
    # Once rotation fires — even with an empty suggestions list — previousSuggestions
    # is set to [] (not None), so a subsequent retry won't re-trigger the rotation
    # and accidentally wipe partially-accumulated new suggestions.
    if file_entry.status in re_review_statuses and file_entry.previousSuggestions is None:
        file_entry.previousSuggestions = list(file_entry.suggestions)
        file_entry.suggestions = []

    return review_state


def sync_review_state_from_threads(
    pull_request_id: int,
    threads: list[dict | None],
    review_state: "ReviewState",
) -> "ReviewState":
    """Reconcile local review state with marker-identified threads from Azure DevOps.

    Scans *threads* for agdt-review markers and adds any missing entries to
    *review_state*.  File-summary entries are only added when their
    normalised file path is not already tracked, and the overall summary is
    only populated when ``review_state.overallSummary.threadId`` is unset
    (``0``).  This function is therefore limited to filling gaps for state
    recovery and does not overwrite populated entries.

    Threads whose marker contains a ``pr`` value that does not match
    *pull_request_id* are silently skipped to avoid cross-contamination
    when threads from multiple PRs are present.  Deleted threads and
    threads whose first comment is deleted are also skipped to avoid
    creating pointers to nonexistent resources.

    Args:
        pull_request_id: Pull request ID used to filter markers.
        threads: Raw thread dicts fetched from the Azure DevOps API.
            May contain ``None`` entries, which are silently skipped.
        review_state: The current ReviewState to reconcile into.

    Returns:
        The same *review_state* object, mutated in-place with any newly
        discovered entries.
    """
    from .marker import MARKER_TYPES, parse_marker

    for thread in threads:
        if not thread:
            continue
        if thread.get("isDeleted"):
            continue
        comments = thread.get("comments")
        if not comments:
            continue
        first_comment = comments[0]
        if not isinstance(first_comment, dict):
            continue
        if first_comment.get("isDeleted"):
            continue
        content = first_comment.get("content", "") or ""
        parsed = parse_marker(content)
        if parsed is None:
            continue

        # Skip markers from unsupported versions.
        marker_version = parsed.get("_version")
        if marker_version != "1":
            continue

        # Skip threads whose marker pr value doesn't match pull_request_id.
        marker_pr = parsed.get("pr")
        if marker_pr is not None and str(marker_pr) != str(pull_request_id):
            continue

        thread_id = thread.get("id", 0)
        comment_id = first_comment.get("id", 0)
        marker_type = parsed.get("type")

        # Skip unrecognised marker types.
        if not marker_type or marker_type not in MARKER_TYPES:
            continue

        if marker_type == "file-summary":
            file_path = parsed.get("file")
            if not file_path:
                continue
            normalized = normalize_file_path(file_path)
            if normalized in review_state.files:
                continue  # Already tracked
            # Derive folder and file name from the path
            parts = normalized.lstrip("/").split("/")
            folder = parts[0] if len(parts) > 1 else "root"
            file_name = parts[-1]
            review_state.files[normalized] = FileEntry(
                threadId=thread_id,
                commentId=comment_id,
                folder=folder,
                fileName=file_name,
                status=ReviewStatus.UNREVIEWED.value,
            )

        elif marker_type == "overall-summary":
            if review_state.overallSummary.threadId == 0:
                review_state.overallSummary.threadId = thread_id
                review_state.overallSummary.commentId = comment_id

    return review_state
