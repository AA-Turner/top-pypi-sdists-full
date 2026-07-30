"""Map DataHub documents to GitHub file targets for sync-back.

Pure, side-effect-free helpers so the path/classification logic is easy to unit
test independently of GitHub or DataHub I/O. The customProperties keys read here
are the ones written by the OSS import source (see ``_emit_file_document`` /
``_emit_folder_document`` in the OSS ``github_documents_source``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional

from datahub.ingestion.source.github_documents.github_documents_source import (
    LAST_EXPORTED_CONTENT_HASH_KEY,
)

# customProperties keys written by the OSS import source.
PROP_IMPORT_SOURCE = "import_source"
PROP_GITHUB_REPO = "github_repo"
PROP_GITHUB_BRANCH = "github_branch"
PROP_GITHUB_FILE_PATH = "github_file_path"
PROP_GITHUB_DIRECTORY_PATH = "github_directory_path"
PROP_GITHUB_BLOB_SHA = "github_blob_sha"
PROP_CONTENT_HASH = "content_hash"
PROP_IS_FOLDER = "is_folder_document"
PROP_IS_REPO_ROOT = "is_repo_root_document"


class DocumentKind(Enum):
    """Sync-back classification of a DataHub document."""

    EXISTING_FILE = "existing_file"
    FOLDER = "folder"
    NEW = "new"


@dataclass(frozen=True)
class SyncBackTarget:
    """A resolved GitHub destination for a document's content."""

    repo: str
    branch: str
    github_path: str


def classify_document(custom_properties: Optional[Dict[str, str]]) -> DocumentKind:
    """Classify a document from its import customProperties."""
    props = custom_properties or {}
    if props.get(PROP_IS_FOLDER) == "true" or props.get(PROP_IS_REPO_ROOT) == "true":
        return DocumentKind.FOLDER
    if props.get(PROP_GITHUB_FILE_PATH):
        return DocumentKind.EXISTING_FILE
    return DocumentKind.NEW


def is_document_content_unchanged(
    custom_properties: Optional[Dict[str, str]], content_hash: str
) -> bool:
    """True when DataHub content matches the last import or last sync-back write.

    Mirrors the OSS import skip check in ``_should_skip_unchanged_file`` so both
    directions use the same loop-prevention contract.
    """
    props = custom_properties or {}
    stored_hash = props.get(PROP_CONTENT_HASH)
    exported_hash = props.get(LAST_EXPORTED_CONTENT_HASH_KEY)
    return content_hash in (stored_hash, exported_hash)


def resolve_existing_target(
    custom_properties: Optional[Dict[str, str]],
) -> Optional[SyncBackTarget]:
    """Resolve the GitHub destination for an already-imported file document."""
    props = custom_properties or {}
    path = props.get(PROP_GITHUB_FILE_PATH)
    repo = props.get(PROP_GITHUB_REPO)
    branch = props.get(PROP_GITHUB_BRANCH)
    if not path or not repo or not branch:
        return None
    return SyncBackTarget(repo=repo, branch=branch, github_path=path)


def parent_directory(custom_properties: Optional[Dict[str, str]]) -> Optional[str]:
    """Return the GitHub directory represented by a parent document.

    Folder documents carry ``github_directory_path``; the repository root
    document represents the repository root (empty directory). Returns None when
    the document is not a directory-like container (so the caller can skip new
    documents nested under non-folder parents in v1).
    """
    props = custom_properties or {}
    if props.get(PROP_IS_REPO_ROOT) == "true":
        return ""
    directory = props.get(PROP_GITHUB_DIRECTORY_PATH)
    if directory is not None:
        return directory.strip("/")
    return None


def slugify_title(title: str) -> str:
    """Turn a document title into a filesystem-safe file base name."""
    slug = (title or "").strip().lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-.")
    return slug or "untitled"


def derive_new_file_path(
    parent_directory: str,
    title: str,
    extension: str,
) -> str:
    """Build a GitHub file path for a brand-new DataHub document.

    ``parent_directory`` is the already-resolved GitHub directory of the
    document's parent (empty string for the repository root). The path_prefix is
    already encoded in the parent directory, so it is not re-applied here.
    """
    base = slugify_title(_strip_extension(title, extension))
    filename = base if base.endswith(extension) else f"{base}{extension}"
    parent = parent_directory.strip("/")
    return f"{parent}/{filename}" if parent else filename


def _strip_extension(title: str, extension: str) -> str:
    lowered = (title or "").strip()
    if lowered.lower().endswith(extension.lower()):
        return lowered[: -len(extension)]
    return lowered
