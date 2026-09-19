"""Bounded, non-executing launcher identity inspection."""

from __future__ import annotations

import os
import struct
import time
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Literal

import structlog

from runlayer_cli.scan import symlink_identity
from runlayer_cli.scan.cli_binaries import windows_bin_roots
from runlayer_cli.scan.hidden_space_sweep import HiddenLauncherDirectory
from runlayer_cli.scan.scanner_primitives import (
    MAX_PATH_COMPONENTS,
    is_link_or_reparse,
    is_real_directory,
    is_regular_file,
    read_bounded,
)

logger = structlog.get_logger(__name__)

MAX_INSPECTION_ENTRIES = 16_384
MAX_RETAINED_FINDINGS = 256
MAX_CMD_BYTES = 8 * 1024
MAX_LNK_BYTES = 64 * 1024
MAX_AGGREGATE_BYTES = 1024 * 1024
MAX_INSPECTION_SECONDS = 5.0
SHELL_LINK_MAX_PATH_CODE_UNITS = 260

_SHELL_LINK_HEADER_SIZE = 0x4C
_SHELL_LINK_CLSID = bytes.fromhex("0114020000000000c000000000000046")
_SHELL_LINK_HAS_RELATIVE_PATH = 0x00000008
_SHELL_LINK_IS_UNICODE = 0x00000080
_SUPPORTED_SHELL_LINK_FLAGS = _SHELL_LINK_HAS_RELATIVE_PATH | _SHELL_LINK_IS_UNICODE
_UTF8_BOM = b"\xef\xbb\xbf"
_WINDOWS_RESERVED_DEVICE_STEMS = frozenset(
    {
        "aux",
        "con",
        "nul",
        "prn",
        *(f"com{number}" for number in range(1, 10)),
        *(f"lpt{number}" for number in range(1, 10)),
    }
)

LauncherKind = Literal["hidden_symlink", "windows_cmd", "windows_lnk"]
TruncationReason = Literal[
    "deadline",
    "directories",
    "entries",
    "entries_per_directory",
    "launchers",
    "findings",
    "aggregate_bytes",
    "version_roots",
    "directory_error",
]


@dataclass(frozen=True)
class LauncherFinding:
    """One validated identity without attacker-controlled path data."""

    basename: str
    kind: LauncherKind


@dataclass
class LauncherInspectionResult:
    """Bounded findings and path-free completion telemetry."""

    findings: list[LauncherFinding] = field(default_factory=list)
    truncated: bool = False
    truncation_reason: TruncationReason | None = None
    directories: int = 0
    entries: int = 0
    launchers: int = 0
    bytes_read: int = 0
    cmd_bytes_read: int = 0
    lnk_bytes_read: int = 0
    malformed_or_unsafe: int = 0
    # Sweep-admitted bin directories this inspection refused (outside the
    # profile, reparse-bearing, or gone). Not a budget truncation, but the
    # launchers inside were never looked at, so absence there is unproven.
    hidden_directories_skipped: int = 0


@dataclass
class _InspectionBudget:
    result: LauncherInspectionResult
    checkpoint_callback: Callable[[], None] | None
    deadline: float
    identity: symlink_identity.SymlinkIdentityScanBudget = field(init=False)

    def __post_init__(self) -> None:
        self.identity = symlink_identity.SymlinkIdentityScanBudget(
            on_limit=self._identity_limit,
        )

    def _identity_limit(self, reason: symlink_identity.IdentityLimit) -> None:
        if reason == "candidates":
            self.truncate("launchers")
        else:
            self.truncate(reason)

    def checkpoint(self) -> bool:
        if self.checkpoint_callback is not None:
            self.checkpoint_callback()
        if time.monotonic() >= self.deadline:
            self.truncate("deadline")
            return False
        return True

    def truncate(self, reason: TruncationReason) -> None:
        self.result.truncated = True
        if self.result.truncation_reason is None:
            self.result.truncation_reason = reason

    def claim_directory(self, directory: Path) -> bool:
        if not self.identity.claim_directory(
            symlink_identity.logical_path_key(directory)
        ):
            return False
        self.result.directories += 1
        return True

    def claim_entry(self, *, directory_entries: int) -> bool:
        if not self.identity.claim_entry(directory_entries=directory_entries):
            return False
        if self.result.entries >= MAX_INSPECTION_ENTRIES:
            self.truncate("entries")
            return False
        self.result.entries += 1
        return True

    def claim_launcher(self) -> bool:
        if not self.identity.claim_candidate():
            return False
        self.result.launchers += 1
        return True

    def retain(self, finding: LauncherFinding) -> None:
        if finding in self.result.findings:
            return
        if len(self.result.findings) >= MAX_RETAINED_FINDINGS:
            self.truncate("findings")
            return
        self.result.findings.append(finding)


def _safe_relative_windows_path(value: str) -> PureWindowsPath | None:
    if not value or "\0" in value or "%" in value:
        return None
    raw_parts = value.replace("/", "\\").split("\\")
    if any(not part or part == "." for part in raw_parts):
        return None
    path = PureWindowsPath(value)
    if path.drive or path.root or path.is_absolute() or not path.parts:
        return None
    for part in path.parts:
        if part in {".", ".."}:
            continue
        if (
            ":" in part
            or part.endswith((" ", "."))
            or part.casefold().endswith(".exe.exe")
            or part.partition(".")[0].casefold() in _WINDOWS_RESERVED_DEVICE_STEMS
        ):
            return None
    if path.name.casefold().endswith(".exe.exe") or path.suffix.casefold() != ".exe":
        return None
    return path


def parse_windows_cmd_target(raw: bytes) -> PureWindowsPath | None:
    """Parse the phase-1 exact static ``%~dp0`` forwarding grammar."""
    if len(raw) > MAX_CMD_BYTES:
        return None
    try:
        if raw.startswith(_UTF8_BOM):
            text = raw[len(_UTF8_BOM) :].decode("utf-8", errors="strict")
        else:
            if any(value > 0x7F for value in raw):
                return None
            text = raw.decode("ascii", errors="strict")
    except UnicodeError:
        return None
    if "\0" in text:
        return None

    normalized = text.replace("\r\n", "\n")
    if "\r" in normalized or any(
        separator in normalized for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e")
    ):
        return None
    if normalized.endswith("\n"):
        normalized = normalized[:-1]
    lines = normalized.split("\n")
    if lines and lines[0].casefold() == "@echo off":
        lines = lines[1:]
    if len(lines) != 1:
        return None
    line = lines[0]
    prefix = '@"%~dp0'
    suffix = '" %*'
    if (
        len(line) <= len(prefix) + len(suffix)
        or line[: len(prefix)].casefold() != prefix
        or not line.endswith(suffix)
    ):
        return None
    target = line[len(prefix) : -len(suffix)]
    if '"' in target or any(character in target for character in "!^&|<>"):
        return None
    return _safe_relative_windows_path(target)


def parse_windows_shell_link_target(raw: bytes) -> PureWindowsPath | None:
    """Parse the phase-1 Unicode RelativePath-only MS-SHLLINK subset."""
    try:
        if len(raw) < _SHELL_LINK_HEADER_SIZE + 2 + 4 or len(raw) > MAX_LNK_BYTES:
            return None
        header_size = struct.unpack_from("<I", raw, 0)[0]
        flags = struct.unpack_from("<I", raw, 20)[0]
        if (
            header_size != _SHELL_LINK_HEADER_SIZE
            or raw[4:20] != _SHELL_LINK_CLSID
            or flags != _SUPPORTED_SHELL_LINK_FLAGS
        ):
            return None
        code_units = struct.unpack_from("<H", raw, _SHELL_LINK_HEADER_SIZE)[0]
        if not 0 < code_units <= SHELL_LINK_MAX_PATH_CODE_UNITS:
            return None
        start = _SHELL_LINK_HEADER_SIZE + 2
        end = start + code_units * 2
        if end + 4 != len(raw) or raw[end:] != b"\0\0\0\0":
            return None
        value = raw[start:end].decode("utf-16le", errors="strict")
        return _safe_relative_windows_path(value)
    except (UnicodeError, struct.error, ValueError):
        return None


def _safe_user_path(path: Path, home: Path) -> bool:
    absolute_path = path.absolute()
    absolute_home = home.absolute()
    try:
        relative = absolute_path.relative_to(absolute_home)
    except ValueError:
        return False
    if len(relative.parts) + 1 > MAX_PATH_COMPONENTS:
        return False
    current = absolute_home
    for part in relative.parts:
        current /= part
        if is_link_or_reparse(current):
            return False
    return True


def _resolve_user_target(
    launcher: Path,
    relative_target: PureWindowsPath,
    *,
    home: Path,
) -> Path | None:
    try:
        parent_parts = list(
            launcher.parent.absolute().relative_to(home.absolute()).parts
        )
    except ValueError:
        return None
    for part in relative_target.parts:
        if part == "..":
            if not parent_parts:
                return None
            parent_parts.pop()
        elif part != ".":
            parent_parts.append(part)
    target = home.joinpath(*parent_parts)
    if (
        not _safe_user_path(target, home)
        or is_link_or_reparse(target)
        or not is_regular_file(target)
    ):
        return None
    return target


def _windows_identity(
    target: Path,
    known_basenames: dict[str, str],
) -> str | None:
    name = target.name
    folded = name.casefold()
    if (
        ":" in name
        or name.endswith((" ", "."))
        or folded.endswith(".exe.exe")
        or not folded.endswith(".exe")
    ):
        return None
    return known_basenames.get(folded[: -len(".exe")])


def _read_launcher(
    path: Path,
    *,
    max_bytes: int,
    budget: _InspectionBudget,
) -> bytes | None:
    if not budget.checkpoint():
        return None
    remaining = MAX_AGGREGATE_BYTES - budget.result.bytes_read
    if remaining <= 0:
        budget.truncate("aggregate_bytes")
        return None
    try:
        file_size = path.lstat().st_size
    except OSError:
        budget.result.malformed_or_unsafe += 1
        return None
    if not budget.checkpoint():
        return None
    if file_size > max_bytes:
        budget.result.malformed_or_unsafe += 1
        return None
    if file_size > remaining:
        budget.truncate("aggregate_bytes")
        return None
    raw = read_bounded(path, max_bytes=min(max_bytes, remaining))
    if not budget.checkpoint():
        return None
    if raw is None:
        budget.result.malformed_or_unsafe += 1
        return None
    if budget.result.bytes_read + len(raw) > MAX_AGGREGATE_BYTES:
        budget.truncate("aggregate_bytes")
        return None
    budget.result.bytes_read += len(raw)
    return raw


def _inspect_windows_candidate(
    path: Path,
    *,
    kind: Literal["cmd", "lnk"],
    home: Path,
    known_basenames: dict[str, str],
    budget: _InspectionBudget,
) -> None:
    if not budget.claim_launcher() or not budget.checkpoint():
        return
    path_is_safe = (
        _safe_user_path(path, home)
        and not is_link_or_reparse(path)
        and is_regular_file(path)
    )
    if not budget.checkpoint():
        return
    if not path_is_safe:
        budget.result.malformed_or_unsafe += 1
        return
    max_bytes = MAX_CMD_BYTES if kind == "cmd" else MAX_LNK_BYTES
    raw = _read_launcher(path, max_bytes=max_bytes, budget=budget)
    if raw is None:
        return
    if kind == "cmd":
        budget.result.cmd_bytes_read += len(raw)
    else:
        budget.result.lnk_bytes_read += len(raw)
    relative_target = (
        parse_windows_cmd_target(raw)
        if kind == "cmd"
        else parse_windows_shell_link_target(raw)
    )
    target = (
        _resolve_user_target(path, relative_target, home=home)
        if relative_target is not None
        else None
    )
    if not budget.checkpoint():
        return
    identity = (
        _windows_identity(target, known_basenames) if target is not None else None
    )
    if identity is None:
        budget.result.malformed_or_unsafe += 1
        return
    budget.retain(
        LauncherFinding(
            basename=identity,
            kind="windows_cmd" if kind == "cmd" else "windows_lnk",
        )
    )


def _inspect_posix_symlink(
    path: Path,
    *,
    known_posix_basenames: frozenset[str],
    budget: _InspectionBudget,
) -> None:
    if not path.is_symlink():
        return
    if not budget.claim_launcher() or not budget.checkpoint():
        return
    resolved = symlink_identity.resolve_posix_symlink_identity(
        path,
        known_basenames=known_posix_basenames,
        checkpoint=budget.checkpoint,
    )
    if resolved is None:
        if budget.result.truncation_reason != "deadline":
            budget.result.malformed_or_unsafe += 1
        return
    if resolved.executable_basename is None:
        budget.result.malformed_or_unsafe += 1
        return
    if not budget.checkpoint():
        return
    budget.retain(
        LauncherFinding(
            basename=resolved.executable_basename,
            kind="hidden_symlink",
        )
    )


def _inspect_entry(
    entry: os.DirEntry[str],
    *,
    system: str,
    home: Path,
    known_posix: frozenset[str],
    known_windows: dict[str, str],
    budget: _InspectionBudget,
) -> None:
    path = Path(entry.path)
    if system != "Windows":
        _inspect_posix_symlink(
            path,
            known_posix_basenames=known_posix,
            budget=budget,
        )
        return
    suffix = Path(entry.name).suffix.casefold()
    if suffix not in {".cmd", ".lnk"}:
        return
    _inspect_windows_candidate(
        path,
        kind="cmd" if suffix == ".cmd" else "lnk",
        home=home,
        known_basenames=known_windows,
        budget=budget,
    )


def inspect_launcher_identities(
    *,
    known_basenames: Sequence[str],
    home: Path,
    system: str,
    hidden_directories: Iterable[HiddenLauncherDirectory] = (),
    windows_system_profile: bool = False,
    checkpoint: Callable[[], None] | None = None,
) -> LauncherInspectionResult:
    """Inspect admitted launchers without executing or returning their paths."""
    started_at = time.monotonic()
    result = LauncherInspectionResult()
    budget = _InspectionBudget(
        result=result,
        checkpoint_callback=checkpoint,
        deadline=started_at + MAX_INSPECTION_SECONDS,
    )
    known_posix = frozenset(known_basenames)
    known_windows = {
        basename.casefold(): basename
        for basename in known_basenames
        if PureWindowsPath(basename).name == basename
        and not basename.casefold().endswith(".exe")
    }

    static_windows_directories: list[Path] = []
    if system == "Windows" and not windows_system_profile:
        static_windows_directories = windows_bin_roots(
            home=home,
            include_versioned=False,
        )

    def _inspection_directories() -> Iterable[tuple[Path, bool]]:
        yield from ((directory, False) for directory in static_windows_directories)
        yield from ((directory.path, True) for directory in hidden_directories)
        if system == "Windows" and not windows_system_profile and budget.checkpoint():
            for directory in windows_bin_roots(
                home=home,
                include_versioned=True,
                checkpoint=budget.checkpoint,
                on_versioned_truncated=lambda: budget.truncate("version_roots"),
            ):
                if directory not in static_windows_directories:
                    yield directory, False

    if system != "Windows" or not windows_system_profile:
        for directory, admitted_by_sweep in _inspection_directories():
            if not budget.checkpoint():
                break
            directory_is_safe = (
                system != "Windows" or _safe_user_path(directory, home)
            ) and is_real_directory(directory)
            if not directory_is_safe:
                if admitted_by_sweep:
                    result.hidden_directories_skipped += 1
                continue
            if not budget.checkpoint() or not budget.claim_directory(directory):
                continue
            directory_entries = 0
            try:
                with os.scandir(directory) as entries:
                    for entry in entries:
                        if not budget.checkpoint() or not budget.claim_entry(
                            directory_entries=directory_entries
                        ):
                            break
                        directory_entries += 1
                        # One unreadable entry is that entry's problem, not the
                        # directory's: count it and keep inspecting siblings.
                        try:
                            _inspect_entry(
                                entry,
                                system=system,
                                home=home,
                                known_posix=known_posix,
                                known_windows=known_windows,
                                budget=budget,
                            )
                        except OSError:
                            result.malformed_or_unsafe += 1
            except OSError:
                result.malformed_or_unsafe += 1
                budget.truncate("directory_error")
            budget.checkpoint()

    duration_ms = max(0, int((time.monotonic() - started_at) * 1000))
    matches_by_kind = {
        kind: sum(finding.kind == kind for finding in result.findings)
        for kind in ("hidden_symlink", "windows_cmd", "windows_lnk")
    }
    logger.info(
        "launcher_inspection_complete",
        directories=result.directories,
        entries=result.entries,
        launchers=result.launchers,
        bytes_read=result.bytes_read,
        cmd_bytes_read=result.cmd_bytes_read,
        lnk_bytes_read=result.lnk_bytes_read,
        findings=len(result.findings),
        matches_by_kind=matches_by_kind,
        malformed_or_unsafe=result.malformed_or_unsafe,
        hidden_directories_skipped=result.hidden_directories_skipped,
        truncated=result.truncated,
        truncation_reason=result.truncation_reason,
        duration_ms=duration_ms,
    )
    return result
