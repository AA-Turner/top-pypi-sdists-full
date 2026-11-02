"""Repo-specialization of the general ``agdt-setup`` expectations document.

Consumes the general ``docs/setup-expectations/agdt-setup.md`` baseline and emits
a repo-specialized copy: inapplicable table rows are pruned, gated phases are
annotated, and concrete identifiers from a :class:`RepositoryConfiguration` are
filled in.

:func:`specialize_expectations` is a **pure** helper — it performs no filesystem
or state access and raises :class:`ValueError` on malformed input.
:func:`run_specialization` owns all I/O (existence check, read, write) and
converts every outcome — including caught exceptions — into a
:class:`SpecializationResult`. :func:`resolve_general_doc_path` locates the source document
(source checkout first, packaged resource second as an installed-wheel
fallback).
This module intentionally implements only the deterministic specialization slice
of issue #2300; the persisted-report handoff, ``agdt-run-specialization`` CLI
boundary, and orchestrator Step 4 wiring are tracked separately.
"""

from __future__ import annotations

import re
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RECOGNIZED_ADAPTERS: tuple[str, ...] = ("github", "jira", "markdown")
"""Issue-adapter values recognised for specialization; others trigger a warning."""

VALID_STATUSES: tuple[str, ...] = ("success", "skipped", "error")
"""Valid :class:`SpecializationResult` status discriminator values."""

SPECIALIZED_OUTPUT_FILENAME: str = "setup-expectations-specialized.md"
"""Well-known output filename written under the state directory (FR-007)."""

_NPM_PRUNE_KEYS: frozenset[str] = frozenset(
    {
        "--npm",
        "--no-npm",
        "NODE_EXTRA_CA_CERTS",
        "NPM_CONFIG_USERCONFIG",
        "~/.agdt/npmrc",
    }
)
"""Key-column values pruned from managed tables when ``has_npm`` is ``False``."""

_NPM_SYSTEM_ONLY_PRUNE_KEYS: frozenset[str] = frozenset(
    {
        "NODE_EXTRA_CA_CERTS",
        "NPM_CONFIG_USERCONFIG",
        "~/.agdt/npmrc",
    }
)
"""npm side-effect keys pruned when ``system_only`` is ``True`` (npm present but skipped).

``--system-only`` runs skip certificate prefetch and environment persistence, so
these environment-variable and file-system rows cannot occur and must not appear
in the specialized document. The CLI flags ``--npm`` / ``--no-npm`` are
intentionally excluded: they remain valid options the caller may pass.
"""

_SYSTEM_ONLY_PRUNE_KEYS: frozenset[str] = frozenset(
    {
        "~/.agdt/bin/",
        "~/.agdt/certs/",
        "~/.agdt/registry.json",
        "~/.agdt/registry.json.lock",
        "REQUESTS_CA_BUNDLE",
        "Shell profile (e.g., `~/.bashrc`)",
    }
)
"""Side-effect keys pruned unconditionally when ``system_only`` is ``True``.

``--system-only`` skips the ``certificate_prefetch`` (phase 2) and
``cli_installation`` (phase 3) phases, so none of these filesystem paths or
environment variables can be observed in this run and must not appear in the
specialized document.  It also suppresses all shell-profile writes (same effect
as ``--no-persist-env``), so the ``Shell profile`` row is pruned as well.
"""

_SHELL_PROFILE_KEY: str = "Shell profile (e.g., `~/.bashrc`)"
"""Key-column value for the shell-profile filesystem row.

Used to prune the row when ``--no-persist-env`` is set and ``system_only`` is
``False`` (the ``system_only`` path is already covered by
:data:`_SYSTEM_ONLY_PRUNE_KEYS`).
"""

_REPO_RE = re.compile(r"^(?:[A-Za-z0-9_.-]|%[0-9a-fA-F]{2})+/(?:[A-Za-z0-9_.-]|%[0-9a-fA-F]{2})+$")
_FLAG_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_PHASE_ITEM_RE = re.compile(r"^\d+\.\s")
_HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*$")
_PHASES_HEADING_RE = re.compile(r"(?m)^##\s+Phases[ \t]*$")

# Section heading texts used to scope row transformations.
_PHASES_HEADING = "Phases"
_CLI_FLAGS_HEADING = "CLI Flags"
_DECISION_HEADING = "Decision Points / Paths"
_EXIT_CODES_HEADING = "Exit Codes"
_FILE_SYSTEM_HEADING = "File System (`~/.agdt/`)"

# Version-guard decision rows (em-dash separator matches the source document).
_VERSION_GUARD_BLOCK_KEYS: frozenset[str] = frozenset({"Version guard — block", "Version guard — force"})


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RepositoryConfiguration:
    """Descriptor of a target repository's setup-relevant characteristics.

    All fields are required. ``effective_flags`` uses ``collections.abc.Mapping``
    to express a read-only interface.

    Attributes:
        repo: Owner/repo slug, e.g. ``"swai-factory/agentic-devtools"``.
        issue_adapter: Resolved adapter (``"github"``, ``"jira"``, ``"markdown"``,
            or an unrecognised value).
        has_npm: Effective npm enablement after applying CLI-flag overrides.
        ssl_hosts: Effective certificate-prefetch hosts.
        system_only: Whether ``--system-only`` is the effective mode.
        version_pin: Resolved version pin, or ``None`` when unpinned.
        effective_flags: Read-only mapping of resolved flag values.
    """

    repo: str
    issue_adapter: str
    has_npm: bool
    ssl_hosts: tuple[str, ...]
    system_only: bool
    version_pin: str | None
    effective_flags: Mapping[str, str | bool | None]


@dataclass(frozen=True)
class SpecializationResult:
    """Outcome of a specialization operation.

    Attributes:
        status: One of ``"success"``, ``"skipped"``, or ``"error"``.
        content: Specialized document (populated only on success).
        reason: Explanation for a skip or error (``None`` on success).
    """

    status: Literal["success", "skipped", "error"]
    content: str | None = None
    reason: str | None = None


# ---------------------------------------------------------------------------
# Value formatting / escaping helpers (pure)
# ---------------------------------------------------------------------------


def _has_newline(value: str) -> bool:
    """Return ``True`` if *value* contains a CR or LF character."""
    return "\n" in value or "\r" in value


def _escape_cell(value: str) -> str:
    """Escape a value for insertion into a Markdown table cell."""
    return value.replace("\\", "\\\\").replace("|", "\\|")


def _escape_html_comment(value: str) -> str:
    """Escape a value for insertion inside an HTML comment block."""
    escaped = value
    while "--" in escaped:
        escaped = escaped.replace("--", "- -")
    return escaped


def _bool_str(value: bool) -> str:
    """Render a boolean deterministically as ``"true"``/``"false"``."""
    return "true" if value else "false"


def _hosts_str(hosts: tuple[str, ...]) -> str:
    """Render an SSL-host tuple as a comma-joined string or ``"none"``."""
    return ",".join(hosts) if hosts else "none"


def _flag_value_str(value: str | bool | None) -> str:
    """Render an ``effective_flags`` value deterministically."""
    if value is None:
        return "none"
    if isinstance(value, bool):
        return _bool_str(value)
    return value


def _strip_code(cell: str) -> str:
    """Strip surrounding backticks from a table-cell key value."""
    cell = cell.strip()
    if len(cell) >= 2 and cell.startswith("`") and cell.endswith("`"):
        return cell[1:-1]
    return cell


def _heading_text(line: str) -> str | None:
    """Return the heading text for a Markdown heading line, else ``None``."""
    match = _HEADING_RE.match(line)
    if match is None:
        return None
    return match.group(1)


def _split_row(line: str) -> list[str] | None:
    """Split a Markdown table row into stripped cells, else ``None``."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def _join_row(cells: list[str]) -> str:
    """Render table *cells* back into a Markdown row."""
    return "| " + " | ".join(cells) + " |"


def _annotate_cell(cells: list[str], index: int, annotation: str) -> str:
    """Return a table row with *annotation* appended to the cell at *index*."""
    updated = list(cells)
    updated[index] = f"{updated[index]} {annotation}"
    return _join_row(updated)


# ---------------------------------------------------------------------------
# Identifier validation (pure)
# ---------------------------------------------------------------------------


def _validate_identifiers(config: RepositoryConfiguration) -> None:
    """Validate identifiers before substitution; raise ``ValueError`` on failure."""
    if not isinstance(config.has_npm, bool):
        raise ValueError(f"Invalid has_npm type: {type(config.has_npm).__name__}. Expected bool.")
    if not isinstance(config.system_only, bool):
        raise ValueError(f"Invalid system_only type: {type(config.system_only).__name__}. Expected bool.")
    if not isinstance(config.repo, str) or _REPO_RE.fullmatch(config.repo) is None:
        raise ValueError(f"Invalid repo slug: {config.repo!r}. Expected 'owner/repo' format.")
    if not isinstance(config.issue_adapter, str) or not config.issue_adapter or _has_newline(config.issue_adapter):
        raise ValueError("issue_adapter must be a non-empty single-line string.")
    if not isinstance(config.effective_flags, Mapping):
        raise ValueError(f"Invalid effective_flags type: {type(config.effective_flags).__name__}. Expected a mapping.")
    for key, value in config.effective_flags.items():
        if not isinstance(key, str):
            raise ValueError(f"Invalid effective_flags key type: {type(key).__name__}. Expected str.")
        if _FLAG_KEY_RE.fullmatch(key) is None:
            raise ValueError(f"Invalid effective_flags key: {key!r}.")
        if not isinstance(value, (str, bool, type(None))):
            raise ValueError(
                f"Invalid effective_flags value type for {key!r}: {type(value).__name__}. Expected str, bool, or None."
            )
        if isinstance(value, str) and _has_newline(value):
            raise ValueError(f"effective_flags value for {key!r} must not contain newlines.")
    if config.version_pin is not None:
        if not isinstance(config.version_pin, str):
            raise ValueError(f"Invalid version_pin type: {type(config.version_pin).__name__}. Expected str or None.")
        if _has_newline(config.version_pin):
            raise ValueError("version_pin must not contain newlines.")
    if not isinstance(config.ssl_hosts, tuple):
        raise ValueError(f"Invalid ssl_hosts type: {type(config.ssl_hosts).__name__}. Expected tuple[str, ...].")
    for host in config.ssl_hosts:
        if not isinstance(host, str):
            raise ValueError(f"Invalid ssl_hosts entry type: {type(host).__name__}. Expected str.")
        if not host or _has_newline(host):
            raise ValueError(f"Invalid ssl_hosts entry: {host!r}.")


# ---------------------------------------------------------------------------
# Metadata + annotation builders (pure)
# ---------------------------------------------------------------------------


def _metadata_block(config: RepositoryConfiguration) -> list[str]:
    """Build the HTML-comment specialization metadata block lines."""
    flags = ", ".join(f"{key}={_flag_value_str(config.effective_flags[key])}" for key in sorted(config.effective_flags))
    return [
        "",
        "<!-- agdt-setup-specialization",
        f"repo: {_escape_html_comment(config.repo)}",
        f"adapter: {_escape_html_comment(config.issue_adapter)}",
        f"effective_flags: {_escape_html_comment(flags)}",
        f"ssl_hosts: {_escape_html_comment(_hosts_str(config.ssl_hosts))}",
        f"version_pin: {_escape_html_comment(config.version_pin or 'none')}",
        "-->",
        "",
    ]


def _annotate_phase_line(line: str, section: str | None, config: RepositoryConfiguration) -> str:
    """Append ``*(expected: skipped)*`` to gated phase entries under ``## Phases``."""
    if section != _PHASES_HEADING or not config.system_only:
        return line
    if not _PHASE_ITEM_RE.match(line):
        return line
    if "`certificate_prefetch`" in line or "`cli_installation`" in line or "`autorun_setup`" in line:
        return f"{line} *(expected: skipped)*"
    return line


def _transform_row(
    line: str,
    cells: list[str],
    section: str | None,
    config: RepositoryConfiguration,
    has_pin: bool,
) -> str | None:
    """Return a (possibly annotated) table row, or ``None`` to prune it."""
    key = _strip_code(cells[0])

    # npm pruning — key-column values are globally unique across managed tables.
    if not config.has_npm and key in _NPM_PRUNE_KEYS:
        return None
    # --system-only pruning — cert-prefetch and CLI-installation phase outputs cannot
    # occur in this run regardless of npm state; prune before section-specific logic.
    if config.system_only and key in _SYSTEM_ONLY_PRUNE_KEYS:
        return None
    # In --system-only mode npm side-effect rows are also pruned (npm is present
    # but skipped). CLI flag rows (--npm, --no-npm) are retained as valid options.
    if config.system_only and config.has_npm and key in _NPM_SYSTEM_ONLY_PRUNE_KEYS:
        return None
    # --no-persist-env pruning — shell-profile writes are suppressed even when
    # system_only is False; the shell-profile row must not appear in the output.
    if not config.system_only and config.effective_flags.get("--no-persist-env") and key == _SHELL_PROFILE_KEY:
        return None

    if section == _CLI_FLAGS_HEADING:
        if key == "--issue-adapter":
            return _annotate_cell(cells, -1, f"*(effective adapter: {_escape_cell(config.issue_adapter)})*")
        if key == "--system-only":
            return _annotate_cell(cells, -1, f"*(effective: {_bool_str(config.system_only)})*")
        return line

    if section == _FILE_SYSTEM_HEADING:
        if key == "~/.agdt/certs/":
            hosts = _escape_cell(_hosts_str(config.ssl_hosts))
            return _annotate_cell(cells, -1, f"*(effective ssl_hosts: {hosts})*")
        return line

    if section == _DECISION_HEADING:
        if key in _VERSION_GUARD_BLOCK_KEYS:
            if len(cells) < 2:
                raise ValueError(f"Malformed decision row for {key!r}; expected at least 2 cells.")
            if has_pin:
                pin = _escape_cell(config.version_pin or "")
                return _annotate_cell(cells, 1, f"*(pin: {pin})*")
            return None
        return line

    if section == _EXIT_CODES_HEADING:
        if len(cells) >= 2 and cells[1] == "VERSION_BLOCKED":
            if has_pin:
                pin = _escape_cell(config.version_pin or "")
                return _annotate_cell(cells, -1, f"*(pin: {pin})*")
            return None
        return line

    return line


# ---------------------------------------------------------------------------
# Pure specialization helper
# ---------------------------------------------------------------------------


def specialize_expectations(document: str, config: RepositoryConfiguration) -> str:
    """Return a repo-specialized copy of the general expectations *document*.

    The transformation is deterministic and string-only: it prunes inapplicable
    table rows, annotates gated phases, and fills concrete identifiers from
    *config*. It performs no I/O.

    Args:
        document: The general expectations document content.
        config: The target repository's configuration descriptor.

    Returns:
        The specialized document as a string.

    Raises:
        ValueError: If *document* is empty/whitespace-only, is missing the
            required ``## Phases`` heading, or *config* contains an invalid
            identifier.
    """
    if not document.strip():
        raise ValueError("General expectations document is empty or whitespace-only.")
    if not _PHASES_HEADING_RE.search(document):
        raise ValueError("General expectations document is missing the required '## Phases' heading.")

    _validate_identifiers(config)

    adapter_recognized = config.issue_adapter in RECOGNIZED_ADAPTERS
    has_pin = bool(config.version_pin)

    out: list[str] = []
    section: str | None = None
    metadata_inserted = False

    for line in document.split("\n"):
        heading = _heading_text(line)
        if heading is not None:
            section = heading
            out.append(line)
            if not metadata_inserted:
                out.extend(_metadata_block(config))
                metadata_inserted = True
            continue

        cells = _split_row(line)
        if cells is None:
            out.append(_annotate_phase_line(line, section, config))
            continue

        transformed = _transform_row(line, cells, section, config, has_pin)
        if transformed is not None:
            out.append(transformed)

    result = "\n".join(out)

    if not adapter_recognized:
        warning = (
            f"<!-- WARNING: Unrecognized adapter type "
            f"'{_escape_html_comment(config.issue_adapter)}'; all adapter sections retained -->"
        )
        result = f"{warning}\n{result}"

    return result


# ---------------------------------------------------------------------------
# I/O wrapper + source-doc resolution
# ---------------------------------------------------------------------------


def resolve_general_doc_path() -> Path | None:
    """Resolve the general expectations document path.

    Resolution order:

    1. Canonical checkout doc (``docs/setup-expectations/agdt-setup.md``).
    2. Packaged resource fallback (installed-wheel safe).
    3. ``None`` when neither path exists.
    """
    module_path = Path(__file__).resolve()
    checkout = module_path.parents[3] / "docs" / "setup-expectations" / "agdt-setup.md"
    if checkout.exists():
        return checkout
    packaged = module_path.parents[2] / "resources" / "setup-expectations" / "agdt-setup.md"
    if packaged.exists():
        return packaged
    return None


_NOT_PROVIDED: object = object()
"""Sentinel used by :func:`cleanup_specialized_output` to distinguish
"startup_fingerprint not supplied" from ``None`` (file absent at startup)."""


@dataclass(frozen=True)
class _StartupFingerprintError:
    """Marker carrying a startup fingerprint inspection failure."""

    error: OSError


@dataclass(frozen=True)
class _StartupFingerprintState:
    """Bundle the startup state directory with the fingerprint captured for it."""

    state_dir: Path
    fingerprint: tuple[int, int, int] | None | _StartupFingerprintError


def capture_startup_fingerprint(state_dir: str | Path) -> tuple[int, int, int] | None | _StartupFingerprintError:
    """Capture the output fingerprint at the very start of a setup invocation.

    Call this before any setup work begins so the fingerprint reflects the
    state at startup, not at cleanup time.  Pass the result to
    :func:`cleanup_specialized_output` as *startup_fingerprint* so an older
    stale run cannot remove an artifact published by a concurrent newer run.

    Returns ``None`` when the output file does not exist at startup.
    Returns :class:`_StartupFingerprintError` when startup inspection fails.
    """
    output_path = Path(state_dir) / SPECIALIZED_OUTPUT_FILENAME
    try:
        return _output_fingerprint(output_path)
    except OSError as exc:
        return _StartupFingerprintError(error=exc)


def capture_startup_state(state_dir: str | Path) -> _StartupFingerprintState:
    """Capture a startup fingerprint together with the exact state directory it belongs to."""
    resolved_state_dir = Path(state_dir)
    return _StartupFingerprintState(
        state_dir=resolved_state_dir,
        fingerprint=capture_startup_fingerprint(resolved_state_dir),
    )


def cleanup_specialized_output(
    state_dir: str | Path,
    *,
    status: Literal["skipped", "error"] = "skipped",
    reason: str,
    startup_fingerprint: (
        tuple[int, int, int] | None | _StartupFingerprintError | _StartupFingerprintState | object
    ) = _NOT_PROVIDED,
) -> SpecializationResult:
    """Remove stale output only if it still matches the startup-owned artifact.

    This is the shared cleanup transaction used by early skip/error paths so a
    failed or skipped run cannot delete fresh output published by a concurrent
    successful run using the same state directory.

    Args:
        startup_fingerprint: Pre-captured fingerprint from
            :func:`capture_startup_fingerprint`.  When supplied, it is used
            directly so the guard reflects the state at setup startup rather
            than at cleanup time.  Omit (or pass :data:`_NOT_PROVIDED`) to
            compute the fingerprint now — the legacy behaviour, which is
            subject to a race if a newer run has published between startup and
            this call.
    """
    if isinstance(startup_fingerprint, _StartupFingerprintState):
        state_dir = startup_fingerprint.state_dir
        startup_fingerprint = startup_fingerprint.fingerprint

    output_path = Path(state_dir) / SPECIALIZED_OUTPUT_FILENAME
    if isinstance(startup_fingerprint, _StartupFingerprintError):
        return SpecializationResult(
            status="error",
            reason=(
                f"{reason}; failed to read {SPECIALIZED_OUTPUT_FILENAME} fingerprint "
                f"at setup startup: {startup_fingerprint.error}"
            ),
        )
    if startup_fingerprint is _NOT_PROVIDED:
        try:
            fingerprint: tuple[int, int, int] | None = _output_fingerprint(output_path)
        except OSError as exc:
            return SpecializationResult(
                status="error",
                reason=f"{reason}; failed to read {SPECIALIZED_OUTPUT_FILENAME} fingerprint: {exc}",
            )
    else:
        fingerprint = startup_fingerprint  # type: ignore[assignment]
    return _finalize_non_success(output_path, fingerprint, status=status, reason=reason)


def _output_fingerprint(output_path: Path) -> tuple[int, int, int] | None:
    """Return a stable fingerprint for *output_path*, or ``None`` when absent."""
    try:
        stat_result = output_path.stat()
    except FileNotFoundError:
        return None
    return (stat_result.st_ino, stat_result.st_size, stat_result.st_mtime_ns)


def _finalize_non_success(
    output_path: Path,
    initial_output_fingerprint: tuple[int, int, int] | None,
    *,
    status: Literal["skipped", "error"],
    reason: str,
) -> SpecializationResult:
    """Return a non-success result, removing only startup-owned stale output."""
    if initial_output_fingerprint is None:
        return SpecializationResult(status=status, reason=reason)

    from agentic_devtools.file_locking import FileLockError, locked_file  # noqa: PLC0415

    lock_path = output_path.with_name(output_path.name + ".lock")
    try:
        with locked_file(lock_path, mode="a", exclusive=True):
            try:
                current_output_fingerprint = _output_fingerprint(output_path)
            except OSError as exc:
                return SpecializationResult(
                    status="error",
                    reason=f"{reason}; failed to inspect stale {SPECIALIZED_OUTPUT_FILENAME}: {exc}",
                )

            if current_output_fingerprint != initial_output_fingerprint:
                return SpecializationResult(status=status, reason=reason)

            try:
                output_path.unlink()
            except FileNotFoundError:
                return SpecializationResult(status=status, reason=reason)
            except OSError as exc:
                return SpecializationResult(
                    status="error",
                    reason=f"{reason}; failed to remove stale {SPECIALIZED_OUTPUT_FILENAME}: {exc}",
                )
    except (OSError, FileLockError) as exc:
        return SpecializationResult(
            status="error",
            reason=f"{reason}; failed to acquire lock for {SPECIALIZED_OUTPUT_FILENAME}: {exc}",
        )
    return SpecializationResult(status=status, reason=reason)


def run_specialization(
    config: RepositoryConfiguration,
    state_dir: str | Path,
    general_doc_path: Path | None,
    *,
    startup_fingerprint: (
        tuple[int, int, int] | None | _StartupFingerprintError | _StartupFingerprintState | object
    ) = _NOT_PROVIDED,
) -> SpecializationResult:
    """Run specialization end-to-end, owning all filesystem access.

    Args:
        config: The target repository's configuration descriptor.
        state_dir: Directory into which the specialized document is written.
        general_doc_path: Path to the general expectations document, or ``None``.
        startup_fingerprint: Pre-captured fingerprint from
            :func:`capture_startup_fingerprint` taken at setup startup.  When
            supplied, it is used for every non-success cleanup path so that a
            stale run whose specialization fails mid-flight cannot delete an
            artifact published by a concurrent newer run after startup.  Omit
            (or pass :data:`_NOT_PROVIDED`) to capture the fingerprint at call
            time — the legacy behaviour, which is subject to the race described
            above.

    Returns:
        A :class:`SpecializationResult`:

        - ``status="skipped"`` when *general_doc_path* is ``None`` or absent and
          stale-output cleanup succeeds, or when a newer concurrent publish is
          detected under the output lock.
        - ``status="error"`` when stale-output cleanup, document resolution,
          reading, specializing, or writing fails.
        - ``status="success"`` with the specialized content otherwise.

    A stale ``setup-expectations-specialized.md`` left over from a previous
    successful run is removed on ``"skipped"`` or ``"error"`` outcomes when
    cleanup succeeds; locking, inspection, or deletion failures return
    ``status="error"`` while leaving the old artifact in place.  Consumers
    must therefore always honour the returned *status* rather than treating
    file presence as proof that it belongs to this run.
    The new document is published atomically inside the sidecar lock (write to
    a temp file, then replace), so a write failure never leaves a partially
    written file at the final path.
    """
    if isinstance(startup_fingerprint, _StartupFingerprintState):
        state_dir = startup_fingerprint.state_dir
        startup_fingerprint = startup_fingerprint.fingerprint

    output_path = Path(state_dir) / SPECIALIZED_OUTPUT_FILENAME
    if isinstance(startup_fingerprint, _StartupFingerprintError):
        return SpecializationResult(
            status="error",
            reason=(
                f"failed to read {SPECIALIZED_OUTPUT_FILENAME} fingerprint "
                f"at setup startup: {startup_fingerprint.error}"
            ),
        )
    if startup_fingerprint is _NOT_PROVIDED:
        try:
            initial_output_fingerprint: tuple[int, int, int] | None = _output_fingerprint(output_path)
        except OSError as exc:
            return SpecializationResult(
                status="error",
                reason=f"failed to inspect stale {SPECIALIZED_OUTPUT_FILENAME}: {exc}",
            )
    else:
        initial_output_fingerprint = startup_fingerprint  # type: ignore[assignment]

    if general_doc_path is None:
        return _finalize_non_success(
            output_path,
            initial_output_fingerprint,
            status="skipped",
            reason=f"General expectations document not found: {general_doc_path}",
        )

    try:
        general_doc_exists = general_doc_path.exists()
    except OSError as exc:
        return _finalize_non_success(output_path, initial_output_fingerprint, status="error", reason=str(exc))

    if not general_doc_exists:
        return _finalize_non_success(
            output_path,
            initial_output_fingerprint,
            status="skipped",
            reason=f"General expectations document not found: {general_doc_path}",
        )

    try:
        content = general_doc_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return _finalize_non_success(output_path, initial_output_fingerprint, status="error", reason=str(exc))

    try:
        specialized = specialize_expectations(content, config)
    except ValueError as exc:
        return _finalize_non_success(output_path, initial_output_fingerprint, status="error", reason=str(exc))

    from agentic_devtools.file_locking import FileLockError, locked_file  # noqa: PLC0415

    lock_path = output_path.with_name(output_path.name + ".lock")
    tmp_path = output_path.with_name(f"{output_path.name}.{uuid.uuid4().hex[:8]}.tmp")
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(specialized, encoding="utf-8")
        with locked_file(lock_path, mode="a", exclusive=True):
            current_fingerprint = _output_fingerprint(output_path)
            if current_fingerprint is not None and current_fingerprint != initial_output_fingerprint:
                # A newer run already published under this lock; yield to it.
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
                return SpecializationResult(
                    status="skipped",
                    reason="Skipped publish because a newer specialization result was already written",
                )
            tmp_path.replace(output_path)
    except (OSError, FileLockError) as exc:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        return _finalize_non_success(output_path, initial_output_fingerprint, status="error", reason=str(exc))

    return SpecializationResult(status="success", content=specialized)
