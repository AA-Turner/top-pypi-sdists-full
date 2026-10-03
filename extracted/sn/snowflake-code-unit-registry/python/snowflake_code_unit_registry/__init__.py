"""Snowflake Code Unit Registry - State management library for database migrations.

This library provides file operations for managing code unit state using
typed structs generated from the JSON Schema.

Example:
    >>> from scai_state import CodeUnitRegistry, generate_id
    >>> from scai_state.types import CodeUnit, Kind, ObjectType, SourceMetadata, TargetMetadata
    >>> 
    >>> # Create code unit (ID will be auto-generated if not provided)
    >>> code_unit = CodeUnit(
    ...     kind=Kind.database_object,
    ...     source=SourceMetadata(objectType=ObjectType.table, database="DB", schema="dbo", name="Customer"),
    ...     target=TargetMetadata(objectType=ObjectType.table, database="DB", schema="DBO", name="CUSTOMER"),
    ... )
    >>> 
    >>> # Create on disk - returns the ID
    >>> registry = CodeUnitRegistry.init("/path/to/repo")
    >>> id = registry.create(code_unit)
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

import warnings

warnings.filterwarnings("ignore", message=r"Field name \"schema\" .* shadows an attribute in parent")

from snowflake_code_unit_registry._native import CodeUnitRegistry as _NativeRegistry
from snowflake_code_unit_registry._native import ScaiError
from snowflake_code_unit_registry._native import ScaiLogger as _NativeScaiLogger
from snowflake_code_unit_registry._native import compute_file_checksum
from snowflake_code_unit_registry._native import generate_id
from snowflake_code_unit_registry._native import (
    parse_database_bindings as _parse_database_bindings_native,
)
from snowflake_code_unit_registry._native import list_error_codes as _list_error_codes
from snowflake_code_unit_registry._native import current_schema_version
from snowflake_code_unit_registry._native import query_reference
from snowflake_code_unit_registry._native import validate_bindings as _validate_bindings_native
from snowflake_code_unit_registry._native import validate_script_io as _validate_script_io_native
from snowflake_code_unit_registry.cloud_state import run_cloud_state_schema_migrations
from snowflake_code_unit_registry.types import CodeUnit

if TYPE_CHECKING:
    from collections.abc import Sequence

__version__ = "0.8.83"
__all__ = [
    "CodeUnitRegistry",
    "ScaiLogger",
    "generate_id",
    "compute_file_checksum",
    "current_schema_version",
    "query_reference",
    "validate_bindings",
    "BindingDiff",
    "parse_database_bindings",
    "DatabaseBindings",
    "validate_script_io",
    "ScriptIoDiff",
    "run_cloud_state_schema_migrations",
    "CodeUnit",
    "ErrorCode",
    "ErrorInfo",
    "WriteOptions",
    "FindOptions",
    "BatchResult",
    "BatchFailure",
    "FileChange",
    "ChecksumScanError",
    "SourceCodeChanges",
    "ChecksumValidationReport",
    "ChecksumValidationEntry",
    "ValidationReport",
    "ValidationIssue",
    "ScaiError",
]


class ErrorCode(IntEnum):
    """Stable numeric error codes shared across Rust, C#, and Python.

    Compare against ``ScaiError.error_code``::

        try:
            registry.get_by_id("missing")
        except ScaiError as e:
            if e.error_code == ErrorCode.CODE_UNIT_NOT_FOUND:
                ...
    """

    REGISTRY_NOT_FOUND = 1001
    REGISTRY_ALREADY_EXISTS = 1002
    CODE_UNIT_NOT_FOUND = 1003
    CODE_UNIT_ALREADY_EXISTS = 1004
    INVALID_STATE_TRANSITION = 1005
    LOCK_ERROR = 1006
    VALIDATION_ERROR = 1007
    IO_ERROR = 1008
    JSON_ERROR = 1009
    INVALID_PATH = 1010
    FILTER_ERROR = 1011
    INVALID_CHECKSUM_MODE = 1013
    CYCLE_DETECTED = 1014
    WRITE_SUCCEEDED_REFRESH_FAILED = 1015
    SCOPED_REFRESH_REQUIRES_FULL_REFRESH = 1016
    SCOPED_REFRESH_UNRESOLVED_DEPENDENCY = 1017
    HOOK_REENTRANT = 1018
    DUPLICATE_BATCH_ID = 1019
    SCHEMA_VERSION_NEWER_THAN_SUPPORTED = 1020
    SCHEMA_MIGRATION_ERROR = 1021
    REGISTRY_SCHEMA_MIGRATION_REQUIRED = 1022
    FILE_IO_ERROR = 1023


def list_error_codes() -> list[tuple[str, int]]:
    """Return all ``(rust_variant_name, code)`` pairs from the native layer."""
    return _list_error_codes()


@dataclass
class TraceEntry:
    """A single entry in the error trace."""

    location: str
    message: str


@dataclass
class ErrorInfo:
    """Canonical structured error payload shared across all language bindings.

    ``code`` is the stable numeric error code (see :class:`ErrorCode`).
    ``details`` is optional and only populated for specific error codes.
    ``trace`` captures the error's location chain.
    """

    code: int
    message: str
    details: dict | None = None
    trace: list[TraceEntry] | None = None

    @classmethod
    def _from_dict(cls, data: dict) -> ErrorInfo:
        """Construct from a dict returned by the native layer."""
        trace_data = data.get("trace")
        trace = (
            [TraceEntry(location=e["location"], message=e["message"]) for e in trace_data]
            if trace_data
            else None
        )
        return cls(
            code=data["code"],
            message=data["message"],
            details=data.get("details"),
            trace=trace,
        )


@dataclass
class BatchFailure:
    """A single failure inside a :class:`BatchResult`."""

    id: str
    error: ErrorInfo


@dataclass
class BatchResult:
    """Result of a batch operation."""

    succeeded: list[str]
    failed: list[BatchFailure]
    side_effect_ids: list[str]

    @classmethod
    def _from_dict(cls, data: dict) -> BatchResult:
        """Construct from a dict returned by the native layer."""
        return cls(
            succeeded=data["succeeded"],
            failed=[
                BatchFailure(
                    id=f["id"],
                    error=ErrorInfo._from_dict(f["error"]),
                )
                for f in data["failed"]
            ],
            side_effect_ids=data.get("sideEffectIds", []),
        )


@dataclass
class FileChange:
    """A single file-level change: path, file type, and change type."""

    path: str
    file_type: str  # "source" | "converted"
    change_type: str  # "modified" | "removed" | "added"

    @classmethod
    def _from_dict(cls, data: dict) -> FileChange:
        return cls(
            path=data["path"],
            file_type=data["file_type"],
            change_type=data["change_type"],
        )


@dataclass
class ChecksumScanError:
    """A file entry that could not be checked due to an I/O error."""

    id: str  # code unit ID
    field: str  # "source" | "converted"
    message: str

    @classmethod
    def _from_dict(cls, data: dict) -> ChecksumScanError:
        return cls(
            id=data["id"],
            field=data["field"],
            message=data["message"],
        )


@dataclass
class SourceCodeChanges:
    """Result of scanning the project for source-code changes."""

    code_unit_changes: dict[str, list[FileChange]]
    untracked_files: list[FileChange]
    errors: list[ChecksumScanError]

    @classmethod
    def _from_dict(cls, data: dict) -> SourceCodeChanges:
        return cls(
            code_unit_changes={
                cu_id: [FileChange._from_dict(fc) for fc in changes]
                for cu_id, changes in data.get("code_unit_changes", {}).items()
            },
            untracked_files=[
                FileChange._from_dict(fc)
                for fc in data.get("untracked_files", [])
            ],
            errors=[
                ChecksumScanError._from_dict(e)
                for e in data.get("errors", [])
            ],
        )


@dataclass
class ChecksumValidationEntry:
    """Checksum validation result for a single file-entry field."""

    field: str
    status: str
    stored_checksum: str | None
    computed_checksum: str | None

    @classmethod
    def _from_dict(cls, data: dict) -> ChecksumValidationEntry:
        """Construct from a dict returned by the native layer."""
        return cls(
            field=data["field"],
            status=data["status"],
            stored_checksum=data.get("stored_checksum"),
            computed_checksum=data.get("computed_checksum"),
        )


@dataclass
class ChecksumValidationReport:
    """Checksum validation report for selected file-entry fields."""

    entries: list[ChecksumValidationEntry]

    @classmethod
    def _from_dict(cls, data: dict) -> ChecksumValidationReport:
        """Construct from a dict returned by the native layer."""
        return cls(
            entries=[
                ChecksumValidationEntry._from_dict(entry)
                for entry in data["entries"]
            ]
        )


@dataclass
class ValidationIssue:
    """A single validation issue tied to a specific file.

    ``error_code`` is populated when the issue originates from a core
    operation (e.g. schema migration) and is ``None`` for issues that are
    purely validation-layer concerns (e.g. duplicate ID).
    """

    file: str
    kind: str
    message: str
    error_code: int | None = None

    @classmethod
    def _from_dict(cls, data: dict) -> ValidationIssue:
        return cls(
            file=data["file"],
            kind=data["kind"],
            message=data["message"],
            error_code=data.get("error_code"),
        )


@dataclass
class ValidationReport:
    """Result of a registry validation run.

    ``is_valid`` is ``True`` only when ``issues`` is empty.
    """

    is_valid: bool
    files_checked: int
    issues: list[ValidationIssue]

    @classmethod
    def _from_dict(cls, data: dict) -> ValidationReport:
        return cls(
            is_valid=data["is_valid"],
            files_checked=data["files_checked"],
            issues=[ValidationIssue._from_dict(i) for i in data.get("issues", [])],
        )


@dataclass
class WriteOptions:
    """Options for write operations (create, update, upsert).

    Attributes:
        checksum_mode: Optional — ``"none"``, ``"source"``,
            ``"converted"``, ``"snapshot"``, or ``"all"``.
            When set, file-entry checksums are recomputed during the write.
    """

    checksum_mode: str | None = None


@dataclass
class FindOptions:
    """Options for :meth:`CodeUnitRegistry.find_all`."""

    filter: str | None = None
    fields: Sequence[str] | None = None
    include_dependencies: bool = False
    bindings: dict[str, str] | None = None
    """Literal token → replacement-value map applied to ``source.*`` and
    ``target.*`` string slots of returned code units. Substitution is
    grammar-agnostic single-pass replacement; CUR does not parse
    ``${...}``, ``<% ... %>``, or any other wrapper."""

    bindings_path: str | None = None
    """Path to a ``database-bindings.yml``; the read resolves it and returns bound
    units, so you pass a path instead of parsing the YAML and wrapping the names.

    Equivalent to passing :meth:`DatabaseBindings.token_map` as ``bindings`` --
    both sides at once, which is unambiguous because ``${NAME}`` and ``<%NAME%>``
    are disjoint grammars. Parse and IO errors are raised from the read rather than
    being handled in every caller.

    Mutually exclusive with ``bindings``: setting both raises, rather than one
    silently winning.

    Two limits, spelled out because the failure mode is silence:

    * it uses the default ``${NAME}`` source grammar, so a conversion that wrote a
      customer-specific source wrapper still needs the explicit ``bindings`` map --
      an unmatched token is left alone, so the gap does not announce itself;
    * a bound read also rewrites ``target.name`` / ``target.canonical_name``. If you
      derive a stable identity from those -- a baseline key, a stage path, an
      on-disk layout -- read **unbound** for that call. This convenience does not
      change that hazard, only how easily it is reached.
    """


@dataclass
class BindingDiff:
    """Structural diff returned by :func:`validate_bindings`.

    Each list is sorted ASCII-betically.
    """

    missing: list[str]
    """Names declared in ``scriptBindings[]`` but absent from ``provided``."""

    extra: list[str]
    """Names present in ``provided`` but not declared in ``scriptBindings[]``."""

    empty: list[str]
    """Names declared and provided whose value is empty after :py:meth:`str.strip`."""


def validate_bindings(
    script: CodeUnit | dict,
    provided: dict[str, str],
) -> BindingDiff:
    """Diff a script's declared ``scriptBindings[].name`` set against ``provided``.

    Narrow by design: no kind awareness, no value-shape rules, no sentinel
    rejection, no source/target asymmetry. Callers decide policy.

    Raises :class:`ScaiError` (code ``VALIDATION_ERROR``) only when ``script.kind``
    is not ``"script"``.
    """
    payload = (
        script
        if isinstance(script, dict)
        else script.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    raw = _validate_bindings_native(payload, provided)
    return BindingDiff(
        missing=list(raw.get("missing", [])),
        extra=list(raw.get("extra", [])),
        empty=list(raw.get("empty", [])),
    )


@dataclass
class DatabaseBindings:
    """A parsed ``database-bindings.yml`` plus the token maps a read consumes.

    ``source`` / ``snow`` are the raw ``name -> database`` maps as written.
    ``source_tokens`` / ``snow_tokens`` are those names wrapped in the literal
    tokens a bindable conversion emitted, ready to hand to
    :attr:`FindOptions.bindings`.
    """

    source: dict[str, str]
    """Raw ``name -> database`` map from the ``source:`` section."""

    snow: dict[str, str]
    """Raw ``name -> database`` map from the ``snow:`` section."""

    source_tokens: dict[str, str]
    """``${NAME} -> database`` (or the supplied wrapper forms)."""

    snow_tokens: dict[str, str]
    """``<%NAME%> -> database``."""


def parse_database_bindings(
    yaml: str,
    source_wrappers: Sequence[str] | None = None,
) -> DatabaseBindings:
    """Parse ``database-bindings.yml`` contents into token maps for a read.

    A bindable conversion records ``${NAME}`` in ``source.database`` and
    ``<%NAME%>`` in ``target.database`` so one artifact can be tested in whichever
    database it was deployed to. Passing the resulting map to
    :attr:`FindOptions.bindings` makes a read return physical names, instead of
    every consumer having to remember to resolve the token itself.

    ``source_wrappers`` overrides the source grammar when the conversion used a
    non-default wrapper; each entry is a format string containing ``{name}`` (e.g.
    ``"@{name}@"``), and every form becomes its own key. The Snowflake side is
    always ``<%NAME%>`` -- Snow CLI templating is invariant.

    Raises :class:`ScaiError` (code ``VALIDATION_ERROR``) when the document is not
    valid YAML or carries an unknown top-level section, and :class:`ValueError`
    when a wrapper is missing ``{name}``.

    .. warning::
       A bound read also rewrites ``target.name`` and ``target.canonicalName``. If
       you derive a stable identity from those -- a baseline key, a stage path, an
       on-disk layout -- read **without** bindings for that call. The substitution
       is silent: nothing errors, the identity simply changes and previously stored
       artifacts stop matching.
    """
    raw = _parse_database_bindings_native(
        yaml,
        list(source_wrappers) if source_wrappers is not None else None,
    )
    return DatabaseBindings(
        source=dict(raw.get("source", {})),
        snow=dict(raw.get("snow", {})),
        source_tokens=dict(raw.get("source_tokens", {})),
        snow_tokens=dict(raw.get("snow_tokens", {})),
    )


@dataclass
class ScriptIoDiff:
    """Structural diff returned by :func:`validate_script_io`.

    Each list is sorted ASCII-betically; entries are identity keys of the form
    ``binding:<name>`` or ``literal:<source>``.
    """

    missing: list[str]
    """Entries declared in ``scriptMetadata.IO[]`` but absent from ``provided``."""

    extra: list[str]
    """Entries present in ``provided`` but not declared in ``scriptMetadata.IO[]``."""

    direction_mismatch: list[str]
    """Entries present on both sides whose ``direction`` disagrees."""


def validate_script_io(
    script: CodeUnit | dict,
    provided: list[dict],
) -> ScriptIoDiff:
    """Diff a script's declared ``scriptMetadata.IO[]`` against test file refs.

    ``provided`` is a list of entries shaped like
    ``{"direction": "read"|"write", "path": {"kind": "binding"|"literal",
    "name"?: ..., "value"?: ...}}``.

    Narrow by design: no fixture existence, no ``compare:`` compatibility, no
    ``opaque`` refusal — those are runner-side rules. Callers decide policy on
    the returned diff.

    Raises :class:`ScaiError` (code ``VALIDATION_ERROR``) only when ``script.kind``
    is not ``"script"``.
    """
    payload = (
        script
        if isinstance(script, dict)
        else script.model_dump(mode="json", by_alias=True, exclude_none=True)
    )
    raw = _validate_script_io_native(payload, provided)
    return ScriptIoDiff(
        missing=list(raw.get("missing", [])),
        extra=list(raw.get("extra", [])),
        direction_mismatch=list(raw.get("direction_mismatch", [])),
    )


class CodeUnitRegistry:
    """Code-unit registry backed by a directory of JSON files."""

    def __init__(self, inner: _NativeRegistry):
        self._inner = inner

    @classmethod
    def exists(cls, repo_root: str) -> bool:
        """Returns True if a registry exists at the given path."""
        return _NativeRegistry.exists(repo_root)

    @classmethod
    def init(cls, repo_root: str) -> CodeUnitRegistry:
        """Initialize a new registry at the given path."""
        return cls(_NativeRegistry.init(repo_root))

    @classmethod
    def open(cls, repo_root: str) -> CodeUnitRegistry:
        """Open an existing registry at the given path."""
        return cls(_NativeRegistry.open(repo_root))

    # ── Create ────────────────────────────────────────────────────────────

    @staticmethod
    def _write_opts(options: WriteOptions | None) -> dict | None:
        if options is None:
            return None
        d: dict = {}
        if options.checksum_mode is not None:
            d["checksum_mode"] = options.checksum_mode
        return d or None

    def create(
        self, code_unit: CodeUnit, *, options: WriteOptions | None = None
    ) -> str:
        """Create a new code unit on disk.

        If code_unit.id is None, generates a new ID.
        Returns the ID of the created code unit.
        Errors if the code unit already exists.

        Args:
            code_unit: The code unit to create.
            options: Optional :class:`WriteOptions` controlling checksum
                behaviour during create.
        """
        return self._inner.create(
            code_unit.model_dump(mode="json", by_alias=True, exclude_none=True),
            options=self._write_opts(options),
        )

    def create_batch(
        self, batch: Sequence[CodeUnit], *, options: WriteOptions | None = None
    ) -> BatchResult:
        """Batch create multiple code units efficiently.

        If a code_unit.id is None, generates a new ID for it.
        Returns BatchResult with succeeded IDs and list of failures.

        Args:
            batch: Code units to create.
            options: Optional :class:`WriteOptions` applied to every unit.
        """
        dicts = [cu.model_dump(mode="json", by_alias=True, exclude_none=True) for cu in batch]
        return BatchResult._from_dict(
            self._inner.create_batch(dicts, options=self._write_opts(options))
        )

    # ── Get / Find ────────────────────────────────────────────────────────

    def get_by_id(self, id: str, fields: Sequence[str] | None = None) -> CodeUnit:
        """Get a code unit by ID."""
        return CodeUnit.model_validate(
            self._inner.get_by_id(id, list(fields) if fields else None)
        )

    def find_all(
        self,
        options: FindOptions | None = None,
    ) -> list[CodeUnit]:
        """Find all code units using a single ``FindOptions`` argument.

        Passing ``None`` uses default options (no filter, no projection,
        no dependency expansion).
        """
        options = options or FindOptions()

        if options.bindings is not None and options.bindings_path is not None:
            raise ValueError(
                "FindOptions: pass either 'bindings' or 'bindings_path', not both"
            )

        payload = {
            "filter": options.filter,
            "fields": list(options.fields) if options.fields is not None else None,
            "include_dependencies": options.include_dependencies,
            "bindings": dict(options.bindings) if options.bindings is not None else None,
            "bindings_path": (
                str(options.bindings_path) if options.bindings_path is not None else None
            ),
        }
        items = self._inner.find_all(
            payload,
        )
        return [CodeUnit.model_validate(item) for item in items]

    def find_by_object(
        self,
        partial: CodeUnit,
        fields: Sequence[str] | None = None,
    ) -> list[CodeUnit]:
        """Find all code units matching the non-null fields of a partial CodeUnit.

        Only the fields explicitly set on ``partial`` are used for matching.
        For nested objects, all present keys must match recursively.
        """
        partial_dict = partial.model_dump(
            mode="json", by_alias=True, exclude_unset=True
        )
        items = self._inner.find_by_object(
            partial_dict, list(fields) if fields else None
        )
        return [CodeUnit.model_validate(item) for item in items]

    # ── Update (PATCH) ────────────────────────────────────────────────────

    def update(
        self, id: str, updates: dict, *, options: WriteOptions | None = None
    ) -> None:
        """Update specific fields in a code unit by dot-notation paths.

        Args:
            id: Code unit ID.
            updates: Dict mapping dot-notation paths to new values.
            options: Optional :class:`WriteOptions` controlling checksum behaviour.
        """
        self._inner.update(id, updates, options=self._write_opts(options))

    def update_where(
        self, filter: str, updates: dict, *, options: WriteOptions | None = None
    ) -> BatchResult:
        """Update all code units matching a filter with the same updates.

        Args:
            filter: SQL WHERE expression.
            updates: Dict mapping dot-notation paths to new values.
            options: Optional :class:`WriteOptions` controlling checksum behaviour.
        """
        return BatchResult._from_dict(
            self._inner.update_where(filter, updates, options=self._write_opts(options))
        )

    def update_batch(
        self, batch: Sequence[tuple[str, dict]], *, options: WriteOptions | None = None
    ) -> BatchResult:
        """Batch update multiple code units efficiently.

        Args:
            batch: Sequence of (id, updates_dict) pairs.
            options: Optional :class:`WriteOptions` controlling checksum behaviour.
        """
        return BatchResult._from_dict(
            self._inner.update_batch(batch, options=self._write_opts(options))
        )

    # ── Upsert (merge) ───────────────────────────────────────────────────

    def upsert(
        self, code_unit: CodeUnit, *, options: WriteOptions | None = None
    ) -> str:
        """Create-or-merge a single code unit.

        If the code unit does not exist on disk, it is created.
        If it exists, the incoming fields are deep-merged into the existing
        document -- fields not present in ``code_unit`` are left untouched.
        Returns the ID of the upserted code unit.

        Args:
            code_unit: The code unit to upsert.
            options: Optional :class:`WriteOptions` controlling checksum behaviour.
        """
        return self._inner.upsert(
            code_unit.model_dump(mode="json", by_alias=True, exclude_none=True),
            options=self._write_opts(options),
        )

    def upsert_batch(
        self, batch: Sequence[CodeUnit], *, options: WriteOptions | None = None
    ) -> BatchResult:
        """Batch upsert multiple code units.

        Args:
            batch: Code units to upsert.
            options: Optional :class:`WriteOptions` controlling checksum behaviour.
        """
        dicts = [cu.model_dump(mode="json", by_alias=True, exclude_none=True) for cu in batch]
        return BatchResult._from_dict(
            self._inner.upsert_batch(dicts, options=self._write_opts(options))
        )

    def update_checksum(self, id: str, checksum_mode: str = "all") -> None:
        """Recompute checksums for selected file entries on an existing code unit.

        Args:
            id: Code unit ID.
            checksum_mode: Which entries to update — ``"none"``, ``"source"``,
                ``"converted"``, ``"snapshot"``, or ``"all"`` (default).
        """
        self._inner.update_checksum(id, checksum_mode)

    def validate_checksum(
        self, id: str, checksum_mode: str = "all"
    ) -> ChecksumValidationReport:
        """Validate checksums for an existing code unit.

        Returns:
            ``ChecksumValidationReport`` with per-field status entries.
        """
        return ChecksumValidationReport._from_dict(
            self._inner.validate_checksum(id, checksum_mode)
        )

    # ── Validation ────────────────────────────────────────────────────────

    def validate(self, checksum_mode: str = "all") -> ValidationReport:
        """Validate all code units in the registry.

        Performs JSON syntax, schema, deserialization, ID/filename,
        duplicate ID, referential integrity, and checksum checks.

        Args:
            checksum_mode: Which file checksums to verify — ``"none"``,
                ``"source"``, ``"converted"``, ``"snapshot"``, or ``"all"``
                (default).

        Returns:
            A ``ValidationReport`` with ``is_valid=True`` when no issues
            are found.
        """
        return ValidationReport._from_dict(
            self._inner.validate(checksum_mode)
        )

    def validate_unit(self, id: str, checksum_mode: str = "all") -> ValidationReport:
        """Validate a single code unit by ID.

        Args:
            id: Code unit ID.
            checksum_mode: Which file checksums to verify (default ``"all"``).
        """
        return ValidationReport._from_dict(
            self._inner.validate_unit(id, checksum_mode)
        )

    # ── Change detection ────────────────────────────────────────────────

    def find_sql_file_changes(
        self, checksum_mode: str = "all", filter: str | None = None
    ) -> SourceCodeChanges:
        """Detect source-code changes (modified, removed, untracked files).

        Args:
            checksum_mode: One of ``"source"``, ``"converted"``, or ``"all"``.
            filter: Optional SQL WHERE expression to restrict which code
                units are scanned.

        Returns:
            A ``SourceCodeChanges`` with per-code-unit changes and
            untracked files.
        """
        raw = self._inner.find_sql_file_changes(checksum_mode, filter)
        return SourceCodeChanges._from_dict(raw)

    # ── Delete ────────────────────────────────────────────────────────────

    def delete(self, id: str) -> None:
        """Delete a code unit by ID."""
        self._inner.delete(id)

    # ── Refresh ───────────────────────────────────────────────────────────

    def refresh_dependencies(self) -> None:
        """Recompute dependency-derived fields across the entire registry.

        Uses strict cycle detection: raises ``ScaiError`` with
        ``error_code=1014`` if any dependency cycle is found.
        """
        self._inner.refresh_dependencies()

    # ── Migration ─────────────────────────────────────────────────────────

    def migrate_schema_all(self) -> BatchResult:
        """Migrate all registry documents to the current schema version.

        Best-effort: per-file failures are reported in
        ``BatchResult.failed`` and processing continues.
        Already-current documents are skipped.

        Returns:
            ``BatchResult`` with migrated IDs in ``succeeded``
            and per-file errors in ``failed``.

        Raises:
            ScaiError: On batch-level failures (lock, sync).
                Partial progress may have occurred.
        """
        return BatchResult._from_dict(self._inner.migrate_schema_all())


class ScaiLogger:
    """Unified logger backed by the native Rust library.

    All SCAI processes share the same log location. Each entry is tagged
    with ``ps={process}`` and optionally ``pr={project_id}`` and
    ``sn={session_id}`` for filtering.

    Default log path: ``~/.snowflake/scai/logs/scai{YYYYMMDD}.log``

    Example::

        logger = ScaiLogger.init("CLI")
        logger.info("Conversion started")
        logger.log("debug", "Processing file", {"path": "db/dbo/t.sql"})
    """

    def __init__(self, inner: _NativeScaiLogger):
        self._inner = inner

    @classmethod
    def init(
        cls,
        process: str,
        *,
        project_id: str | None = None,
        session_id: str | None = None,
    ) -> ScaiLogger:
        """Initialize the logger.

        Log path: ``~/.snowflake/scai/logs/scai{YYYYMMDD}.log``

        Args:
            process: Process identity string stamped on every log entry
                (e.g. ``"CLI"``, ``"DET_ENGINE"``, ``"PLUGIN"``).
            project_id: Optional project ID included in log entries.
            session_id: Optional session ID included in log entries.
        """
        return cls(_NativeScaiLogger.init(process, project_id, session_id))

    def is_enabled(self, level: str) -> bool:
        """Return True if *level* would be logged (i.e. >= the configured minimum)."""
        return self._inner.is_enabled(level)

    def debug(self, message: str, *, context: dict | None = None) -> None:
        """Log at DEBUG level, optionally with structured *context*."""
        if context is not None:
            self._inner.log("debug", message, context)
        else:
            self._inner.debug(message)

    def info(self, message: str, *, context: dict | None = None) -> None:
        """Log at INFO level, optionally with structured *context*."""
        if context is not None:
            self._inner.log("info", message, context)
        else:
            self._inner.info(message)

    def warn(self, message: str, *, context: dict | None = None) -> None:
        """Log at WARN level, optionally with structured *context*."""
        if context is not None:
            self._inner.log("warn", message, context)
        else:
            self._inner.warn(message)

    def warning(self, message: str, *, context: dict | None = None) -> None:
        """Alias for :meth:`warn`."""
        self.warn(message, context=context)

    def error(
        self,
        message: str,
        *,
        exception: BaseException | None = None,
        context: dict | None = None,
    ) -> None:
        """Log at ERROR level.

        Args:
            message: Log message.
            exception: Optional exception. Its ``type``, ``message``, and
                ``stackTrace`` are serialised into the structured context
                automatically.
            context: Optional extra structured context. When *exception* is
                also given, caller-supplied keys override exception keys
                on conflict.
        """
        if exception is not None:
            exc_ctx: dict = {
                "type": type(exception).__qualname__,
                "message": str(exception),
                "stackTrace": "".join(traceback.format_tb(exception.__traceback__)),
            }
            if context:
                exc_ctx.update(context)
            self._inner.log("error", message, exc_ctx)
        elif context is not None:
            self._inner.log("error", message, context)
        else:
            self._inner.error(message)

    def log(
        self,
        level: str,
        message: str,
        context: dict | None = None,
    ) -> None:
        """Log with optional structured context (serialized as JSON).

        Args:
            level: ``"debug"``, ``"info"``, ``"warn"``, or ``"error"``.
            message: Log message.
            context: Optional dict of structured key-value context.
        """
        self._inner.log(level, message, context)

    def log_path(self) -> str:
        """Returns the path of the current log file."""
        return self._inner.log_path()
