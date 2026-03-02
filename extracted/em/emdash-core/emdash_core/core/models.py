"""Data models for EmDash entities."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ============================================================================
# Layer A: Code Structure Entities
# ============================================================================


@dataclass
class FileEntity:
    """Represents a source code file."""

    path: str
    name: str
    extension: str
    size_bytes: int
    lines_of_code: int
    hash: str
    last_modified: Optional[datetime] = None

    @classmethod
    def from_path(cls, file_path: Path, content_hash: str) -> "FileEntity":
        """Create a FileEntity from a file path."""
        stat = file_path.stat()
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = len(f.readlines())

        return cls(
            path=str(file_path),
            name=file_path.name,
            extension=file_path.suffix,
            size_bytes=stat.st_size,
            lines_of_code=lines,
            hash=content_hash,
            last_modified=datetime.fromtimestamp(stat.st_mtime),
        )


@dataclass
class ClassEntity:
    """Represents a class definition."""

    name: str
    qualified_name: str  # e.g., "module.ClassName"
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    is_abstract: bool = False
    decorators: list[str] = field(default_factory=list)
    base_classes: list[str] = field(default_factory=list)  # For inheritance
    attributes: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)  # Qualified names of methods


@dataclass
class FunctionEntity:
    """Represents a function or method definition."""

    name: str
    qualified_name: str  # e.g., "module.function" or "module.Class.method"
    file_path: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parameters: list[str] = field(default_factory=list)
    return_annotation: Optional[str] = None
    is_async: bool = False
    is_method: bool = False
    is_static: bool = False
    is_classmethod: bool = False
    decorators: list[str] = field(default_factory=list)
    cyclomatic_complexity: int = 1
    calls: list[str] = field(default_factory=list)  # Qualified names of called functions


@dataclass
class ModuleEntity:
    """Represents a Python module (imported)."""

    name: str
    import_path: str
    is_external: bool = False  # stdlib or third-party
    package: Optional[str] = None


@dataclass
class ImportStatement:
    """Represents an import statement."""

    file_path: str
    line_number: int
    module: str
    imported_names: list[str] = field(default_factory=list)
    alias: Optional[str] = None
    import_type: str = "import"  # "import" or "from_import"


# ============================================================================
# Layer B: Git History Entities
# ============================================================================


@dataclass
class CommitEntity:
    """Represents a git commit."""

    sha: str
    message: str
    timestamp: datetime
    author_name: str
    author_email: str
    committer_name: str
    committer_email: str
    insertions: int = 0
    deletions: int = 0
    files_changed: int = 0
    is_merge: bool = False
    parent_shas: list[str] = field(default_factory=list)


@dataclass
class FileModification:
    """Represents a file modification in a commit."""

    commit_sha: str
    file_path: str
    change_type: str  # "added", "modified", "deleted", "renamed"
    insertions: int = 0
    deletions: int = 0
    old_path: Optional[str] = None  # For renames


@dataclass
class AuthorEntity:
    """Represents a code contributor."""

    email: str
    name: str
    first_commit: Optional[datetime] = None
    last_commit: Optional[datetime] = None
    total_commits: int = 0
    total_lines_added: int = 0
    total_lines_deleted: int = 0


@dataclass
class PullRequestEntity:
    """Represents a GitHub pull request."""

    number: int
    title: str
    state: str  # "open", "closed", "merged"
    created_at: datetime
    author: str
    description: Optional[str] = None  # Full PR body text
    merged_at: Optional[datetime] = None
    reviewers: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    additions: int = 0
    deletions: int = 0
    files_changed: list[str] = field(default_factory=list)  # File paths modified
    commit_shas: list[str] = field(default_factory=list)
    base_branch: str = "main"
    head_branch: str = ""
    embedding: Optional[list[float]] = None  # Vector embedding for similarity


@dataclass
class TaskEntity:
    """Represents a subtask extracted from a PR description."""

    id: str  # Format: "pr_{number}_task_{index}"
    pr_number: int
    description: str
    is_completed: bool
    order: int  # Position in the task list


@dataclass
class RepositoryEntity:
    """Represents a repository."""

    url: str
    name: str
    owner: Optional[str] = None
    default_branch: str = "main"
    last_ingested: Optional[datetime] = None
    ingestion_status: str = "pending"
    commit_count: int = 0
    file_count: int = 0
    primary_language: str = "Python"


# ============================================================================
# Layer C: Analytics Entities
# ============================================================================


@dataclass
class ClusterEntity:
    """Represents a detected code cluster/community."""

    cluster_id: int
    algorithm: str  # "louvain", "label_propagation"
    modularity_score: float
    size: int  # Number of nodes in cluster
    members: list[str] = field(default_factory=list)  # Qualified names


# ============================================================================
# Aggregate Models
# ============================================================================


@dataclass
class CodebaseEntities:
    """Aggregate of all entities extracted from a codebase."""

    files: list[FileEntity] = field(default_factory=list)
    classes: list[ClassEntity] = field(default_factory=list)
    functions: list[FunctionEntity] = field(default_factory=list)
    modules: list[ModuleEntity] = field(default_factory=list)
    imports: list[ImportStatement] = field(default_factory=list)

    @classmethod
    def merge(cls, entities_list: list["FileEntities"]) -> "CodebaseEntities":
        """Merge multiple FileEntities into a single CodebaseEntities."""
        result = cls()
        for file_entities in entities_list:
            if file_entities:
                if file_entities.file:
                    result.files.append(file_entities.file)
                result.classes.extend(file_entities.classes)
                result.functions.extend(file_entities.functions)
                result.modules.extend(file_entities.modules)
                result.imports.extend(file_entities.imports)
        return result


@dataclass
class FileEntities:
    """Entities extracted from a single file."""

    file: Optional[FileEntity] = None
    classes: list[ClassEntity] = field(default_factory=list)
    functions: list[FunctionEntity] = field(default_factory=list)
    modules: list[ModuleEntity] = field(default_factory=list)
    imports: list[ImportStatement] = field(default_factory=list)


@dataclass
class GitData:
    """Aggregate of all Git history data."""

    repository: RepositoryEntity
    commits: list[CommitEntity] = field(default_factory=list)
    modifications: list[FileModification] = field(default_factory=list)
    authors: list[AuthorEntity] = field(default_factory=list)
    pull_requests: list[PullRequestEntity] = field(default_factory=list)
