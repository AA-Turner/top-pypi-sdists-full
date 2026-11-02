"""Repository ingestion + incremental update.

Walks a local repo path, respects ``.gitignore`` + a deny-list of
known-bloat directories, detects each file's language, then upserts
each into ``code.code_files`` and runs ``ingest_source`` to chunk +
embed it via the standard pipeline.

See ``/Users/armanisadeghi/code/common-docs/projects/knowledge-system/README.md`` §2.3 for code-repo indexing backlog.

Public entry points:

* ``ingest_repository(repo_path, *, user_id, organization_id=None,
                       repo_ref="main", concurrency=8, force=False,
                       emitter=None)`` —
  full repo walk + ingestion. Idempotent on (user_id, repo_url, path);
  files unchanged since last ingest are hash-skipped.
* ``incremental_update(repo_path, *, user_id, since_ref, until_ref="HEAD",
                        ...)`` —
  ``git diff``-driven update. Only re-ingests changed files, deletes
  removed files, handles renames.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import subprocess
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from matrx_orm import F

from matrx_rag._ext import get_db_model
from matrx_rag.ingestion import IngestionResult, ingest_source
from matrx_rag.progress import from_emitter

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Walk policy
# ---------------------------------------------------------------------------

_DENY_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        ".venv",
        "venv",
        "env",
        ".env",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
        "out",
        "target",
        ".next",
        ".nuxt",
        ".turbo",
        "coverage",
        ".coverage",
        ".tox",
        ".DS_Store",
        ".idea",
        ".vscode",
        "vendor",
    }
)

# (extension, language). The language tag drives chunker + embedding model.
_EXT_LANG = {
    ".py": "python",
    ".pyi": "python",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".kt": "kotlin",  # falls through to line-window
    ".scala": "scala",  # line-window
    ".rb": "ruby",  # line-window
    ".php": "php",  # line-window
    ".swift": "swift",  # line-window
    ".c": "c",  # line-window
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",  # line-window
    ".sh": "bash",  # line-window
    ".bash": "bash",
    ".zsh": "bash",
    ".sql": "sql",
    ".graphql": "graphql",
    ".proto": "protobuf",
    # docs that go through the prose chunker (still indexed as code_file)
    ".md": "markdown",
    ".mdx": "markdown",
    ".rst": "markdown",
}

DEFAULT_MAX_BYTES = 1_048_576  # 1 MB


# ---------------------------------------------------------------------------
# Walk
# ---------------------------------------------------------------------------


@dataclass
class _RepoFile:
    abs_path: str
    rel_path: str
    language: str
    size: int


def _git_ignored_files(repo_path: str) -> set[str]:
    """Use ``git ls-files`` to enumerate non-ignored files. Returns the
    set of repo-relative paths git considers tracked + untracked-but-
    not-ignored. Falls back to None when the path isn't a git repo —
    in which case the caller walks everything sans the deny list.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None  # type: ignore[return-value]
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _walk_repo(
    repo_path: str,
    *,
    max_bytes: int,
    extra_deny_dirs: set[str] | None = None,
) -> list[_RepoFile]:
    repo_root = Path(repo_path).resolve()
    if not repo_root.is_dir():
        raise ValueError(f"repo path is not a directory: {repo_path}")

    deny_dirs = set(_DENY_DIRS) | set(extra_deny_dirs or [])
    git_files = _git_ignored_files(str(repo_root))

    files: list[_RepoFile] = []
    if git_files is not None:
        # Trust git's enumeration — fastest + most correct path.
        for rel in git_files:
            ext = Path(rel).suffix.lower()
            lang = _EXT_LANG.get(ext)
            if not lang:
                continue
            abs_path = str(repo_root / rel)
            try:
                size = os.path.getsize(abs_path)
            except OSError:
                continue
            if size > max_bytes:
                continue
            # Even with git, double-check no deny-listed segment slipped in
            # via .gitignore exceptions.
            if any(seg in deny_dirs for seg in Path(rel).parts):
                continue
            files.append(_RepoFile(abs_path=abs_path, rel_path=rel, language=lang, size=size))
        return files

    # Non-git path — manual walk.
    for dirpath, dirnames, filenames in os.walk(repo_root, followlinks=False):
        dirnames[:] = [d for d in dirnames if d not in deny_dirs]
        for name in filenames:
            ext = Path(name).suffix.lower()
            lang = _EXT_LANG.get(ext)
            if not lang:
                continue
            abs_path = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(abs_path)
            except OSError:
                continue
            if size > max_bytes:
                continue
            rel = os.path.relpath(abs_path, repo_root)
            files.append(_RepoFile(abs_path=abs_path, rel_path=rel, language=lang, size=size))
    return files


# ---------------------------------------------------------------------------
# Per-file upsert + ingest
# ---------------------------------------------------------------------------


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def _upsert_code_file(
    *,
    user_id: str,
    organization_id: str | None,
    repo_root: str,
    repo_ref: str,
    file: _RepoFile,
) -> tuple[str, bool]:
    """Insert or update a ``code.code_files`` row. Returns
    ``(code_files_id, changed)``. ``changed=False`` means the row
    already exists with the same content hash — caller can skip ingest.

    NOTE (schema-drift fix): the raw SQL this replaced looked up and wrote a
    ``code.code_files.user_id`` column that does not exist on the live table
    (verified against the database now hosted as project brsgrqvjdzwihsvnfqkf) —
    the owner column is ``created_by``, exactly like every other resolver in
    this package. Both the SELECT and the INSERT would have raised
    ``UndefinedColumnError`` the first time this path actually ran; the ORM
    conversion fixes the drift as part of the port.
    """
    try:
        text = Path(file.abs_path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise RuntimeError(f"could not read {file.abs_path}: {exc}") from exc

    h = _content_hash(text)

    CodeFiles = get_db_model("CodeFiles")
    existing_rows = await CodeFiles.filter(created_by=user_id, path=file.rel_path).limit(1).values(
        "id", "content_hash", "metadata"
    )
    existing = existing_rows[0] if existing_rows else None
    if existing and existing["content_hash"] == h:
        return str(existing["id"]), False

    if existing:
        merged_metadata = dict(existing["metadata"] or {})
        merged_metadata.update({"repo_root": repo_root, "repo_ref": repo_ref})
        await CodeFiles.filter(id=existing["id"]).update(
            content=text,
            content_hash=h,
            language=file.language,
            name=Path(file.rel_path).name,
            organization_id=organization_id,
            metadata=merged_metadata,
            updated_at=datetime.now(UTC),
            version=F("version") + 1,
        )
        return str(existing["id"]), True

    created = await CodeFiles.create(
        created_by=user_id,
        organization_id=organization_id,
        path=file.rel_path,
        name=Path(file.rel_path).name,
        language=file.language,
        content=text,
        content_hash=h,
        version=1,
        metadata={"repo_root": repo_root, "repo_ref": repo_ref},
    )
    return str(created.id), True


async def _ingest_one(
    *,
    user_id: str,
    organization_id: str | None,
    repo_root: str,
    repo_ref: str,
    file: _RepoFile,
    force: bool,
) -> tuple[str, IngestionResult]:
    code_id, changed = await _upsert_code_file(
        user_id=user_id,
        organization_id=organization_id,
        repo_root=repo_root,
        repo_ref=repo_ref,
        file=file,
    )
    if not changed and not force:
        return file.rel_path, IngestionResult(
            source_kind="code_file",
            source_id=code_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=True,
            embedding_model="",
        )
    result = await ingest_source(
        "code_file", code_id, force=force, user_id=user_id, organization_id=organization_id
    )
    return file.rel_path, result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@dataclass
class RepoIngestSummary:
    repo_path: str
    repo_ref: str
    files_total: int
    files_indexed: int = 0
    files_skipped_unchanged: int = 0
    files_skipped_unsupported: int = 0
    files_failed: int = 0
    chunks_written: int = 0
    embeddings_written: int = 0
    language_histogram: dict[str, int] = field(default_factory=dict)
    failures: list[dict[str, Any]] = field(default_factory=list)
    elapsed_ms: int = 0


async def ingest_repository(
    repo_path: str,
    *,
    user_id: str,
    organization_id: str | None = None,
    repo_ref: str = "main",
    concurrency: int = 8,
    force: bool = False,
    max_bytes: int = DEFAULT_MAX_BYTES,
    extra_deny_dirs: set[str] | None = None,
    emitter: Any | None = None,
) -> RepoIngestSummary:
    if not organization_id:
        raise ValueError("ingest a repository into an organization: organization_id is required (the host carries it)")
    started = time.time()
    progress = from_emitter(emitter, source_kind="repository", source_id=repo_path)
    await progress.stage("fetch", message=f"Walking {repo_path}")

    files = _walk_repo(repo_path, max_bytes=max_bytes, extra_deny_dirs=extra_deny_dirs)
    summary = RepoIngestSummary(
        repo_path=repo_path,
        repo_ref=repo_ref,
        files_total=len(files),
    )
    for f in files:
        summary.language_histogram[f.language] = summary.language_histogram.get(f.language, 0) + 1

    await progress.stage(
        "extract",
        message=f"Found {len(files)} indexable files",
        pages_total=len(files),
        pages_done=0,
        extra={"language_histogram": dict(summary.language_histogram)},
    )

    if not files:
        await progress.stage("complete", message="Nothing to index", pages_total=0, pages_done=0)
        summary.elapsed_ms = int((time.time() - started) * 1000)
        return summary

    sem = asyncio.Semaphore(concurrency)
    completed = 0
    completed_lock = asyncio.Lock()

    async def one(file: _RepoFile):
        nonlocal completed
        async with sem:
            try:
                rel, result = await _ingest_one(
                    user_id=user_id,
                    organization_id=organization_id,
                    repo_root=repo_path,
                    repo_ref=repo_ref,
                    file=file,
                    force=force,
                )
                if result.error:
                    summary.files_failed += 1
                    summary.failures.append({"path": file.rel_path, "error": result.error})
                elif result.skipped_unchanged:
                    summary.files_skipped_unchanged += 1
                else:
                    summary.files_indexed += 1
                    summary.chunks_written += result.chunks_written
                    summary.embeddings_written += result.embeddings_written
            except Exception as exc:  # noqa: BLE001
                logger.warning("repo_ingest: %s failed: %s", file.rel_path, exc)
                summary.files_failed += 1
                summary.failures.append({"path": file.rel_path, "error": str(exc)})
            async with completed_lock:
                completed += 1
                if completed % 25 == 0 or completed == len(files):
                    await progress.stage(
                        "embed",
                        message=f"Indexed {completed}/{len(files)} files",
                        pages_total=len(files),
                        pages_done=completed,
                        chunks_total=summary.chunks_written,
                        chunks_done=summary.chunks_written,
                    )

    await asyncio.gather(*(one(f) for f in files))
    summary.elapsed_ms = int((time.time() - started) * 1000)
    await progress.stage(
        "complete",
        message=(
            f"Repo done — {summary.files_indexed} indexed, "
            f"{summary.files_skipped_unchanged} unchanged, "
            f"{summary.files_failed} failed, {summary.chunks_written} chunks"
        ),
        pages_total=summary.files_total,
        pages_done=summary.files_total,
        chunks_total=summary.chunks_written,
        chunks_done=summary.chunks_written,
        extra={"language_histogram": dict(summary.language_histogram)},
    )
    return summary


# ---------------------------------------------------------------------------
# Incremental update via git diff
# ---------------------------------------------------------------------------


async def incremental_update(
    repo_path: str,
    *,
    user_id: str,
    organization_id: str | None = None,
    since_ref: str,
    until_ref: str = "HEAD",
    repo_ref: str = "main",
    concurrency: int = 8,
    emitter: Any | None = None,
) -> RepoIngestSummary:
    if not organization_id:
        raise ValueError("ingest a repository into an organization: organization_id is required (the host carries it)")
    started = time.time()
    progress = from_emitter(emitter, source_kind="repository", source_id=repo_path)
    await progress.stage(
        "fetch",
        message=f"git diff {since_ref}..{until_ref}",
    )

    diff_proc = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", f"{since_ref}..{until_ref}"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    statuses: list[tuple[str, str]] = []
    for line in diff_proc.stdout.splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            statuses.append((parts[0], parts[-1]))

    summary = RepoIngestSummary(
        repo_path=repo_path,
        repo_ref=repo_ref,
        files_total=len(statuses),
    )

    sem = asyncio.Semaphore(concurrency)
    repo_root = str(Path(repo_path).resolve())

    async def handle_one(status: str, rel_path: str):
        ext = Path(rel_path).suffix.lower()
        lang = _EXT_LANG.get(ext)
        if not lang:
            summary.files_skipped_unsupported += 1
            return

        if status == "D":
            # Deleted: drop chunks + soft-delete the row, all through the ORM.
            CodeFiles = get_db_model("CodeFiles")
            rows = await CodeFiles.filter(created_by=user_id, path=rel_path).values("id")
            if rows:
                row_id = rows[0]["id"]
                await get_db_model("KgChunks").delete_where(
                    source_kind="code_file", source_id=str(row_id)
                )
                now = datetime.now(UTC)
                await CodeFiles.filter(id=row_id).update(deleted_at=now, updated_at=now)
            summary.files_indexed += 1
            return

        # Added or modified — re-ingest
        abs_path = os.path.join(repo_path, rel_path)
        if not os.path.exists(abs_path):
            summary.files_failed += 1
            summary.failures.append({"path": rel_path, "error": "missing on disk"})
            return
        try:
            size = os.path.getsize(abs_path)
        except OSError:
            summary.files_failed += 1
            summary.failures.append({"path": rel_path, "error": "stat failed"})
            return
        f = _RepoFile(abs_path=abs_path, rel_path=rel_path, language=lang, size=size)
        async with sem:
            try:
                rel, result = await _ingest_one(
                    user_id=user_id,
                    organization_id=organization_id,
                    repo_root=repo_root,
                    repo_ref=repo_ref,
                    file=f,
                    force=True,  # force re-embed since content changed
                )
                if result.error:
                    summary.files_failed += 1
                    summary.failures.append({"path": rel_path, "error": result.error})
                else:
                    summary.files_indexed += 1
                    summary.chunks_written += result.chunks_written
                    summary.embeddings_written += result.embeddings_written
            except Exception as exc:  # noqa: BLE001
                summary.files_failed += 1
                summary.failures.append({"path": rel_path, "error": str(exc)})

    await asyncio.gather(*(handle_one(s, p) for s, p in statuses))
    summary.elapsed_ms = int((time.time() - started) * 1000)
    await progress.stage(
        "complete",
        message=(
            f"Incremental — {summary.files_indexed} updated, "
            f"{summary.files_failed} failed, {summary.chunks_written} chunks"
        ),
    )
    return summary


__all__ = [
    "RepoIngestSummary",
    "incremental_update",
    "ingest_repository",
]
