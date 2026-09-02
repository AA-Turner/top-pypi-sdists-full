"""Native Python implementation of the legacy SpecKit feature creation flow."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import is_dry_run
from agentic_devtools.task_state import print_task_tracking_info

from .scaffold_common import get_repo_root

PRESET_TEMPLATE_RELATIVE_PATH = Path(".specify") / "presets" / "agdt-templates" / "templates" / "spec-template.md"

# Legacy sequential feature directories and branches use a strict three-digit prefix
# (e.g. "007-something"). Explicit issue numbers (e.g. "3933-feature") intentionally fall
# outside this pattern so they don't participate in legacy auto-number allocation.
_LEGACY_FEATURE_DIR_PATTERN = re.compile(r"^(\d{3})-")

__all__ = [
    "PRESET_TEMPLATE_RELATIVE_PATH",
    "FeatureScaffoldResult",
    "build_feature_branch_name",
    "clean_branch_name",
    "create_hierarchy_yml",
    "detect_parent_hierarchy",
    "ensure_feature_directory",
    "prepare_new_feature",
    "scaffold_new_feature_async",
    "scaffold_new_feature_command",
]


@dataclass(frozen=True)
class FeatureScaffoldResult:
    """The resolved metadata for a newly scaffolded feature."""

    repo_root: Path
    feature_dir: Path
    spec_file: Path
    branch_name: str
    feature_number: str
    parent_dir: Path | None
    hierarchy_level: str | None

    @staticmethod
    def _posix(path: Path) -> str:
        return path.resolve().as_posix()

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "BRANCH_NAME": self.branch_name,
            "SPEC_FILE": self._posix(self.spec_file),
            "FEATURE_NUM": self.feature_number,
            "FEATURE_DIR": self._posix(self.feature_dir),
            "PARENT_SPEC_DIR": self._posix(self.parent_dir) if self.parent_dir else None,
            "HIERARCHY_LEVEL": self.hierarchy_level,
        }
        return payload


def _ensure_positive_int(value: str) -> int:
    if re.fullmatch(r"[1-9][0-9]*", value) is None:
        raise argparse.ArgumentTypeError(f"Expected a positive integer, got {value!r}")
    return int(value)


_STOP_WORDS: frozenset[str] = frozenset(
    "i a an the to for of in on at by with from is are was were be been being "
    "have has had do does did will would should could can may might must shall "
    "this that these those my your our their want need add get set".split()
)

_MAX_BRANCH_BYTES = 244
_HIERARCHY_LOCK_OWNER_FILE = ".owner"


def clean_branch_name(value: str) -> str:
    """Normalize a feature description into a git-safe short branch suffix."""
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    cleaned = cleaned.strip("-")
    return cleaned or "feature"


def _generate_branch_suffix(description: str) -> str:
    """Port of the legacy ``generate_branch_name`` bash function.

    Splits *description* into lowercase words, discards stop words and words
    shorter than three characters that are not uppercase acronyms in the
    original text, then joins the first three (or four, when exactly four
    meaningful words were found) non-empty survivors with hyphens.  Falls back
    to the first three hyphenated tokens from ``clean_branch_name`` when no
    meaningful words are found.
    """
    raw_words = re.sub(r"[^a-z0-9]", " ", description.lower()).split()
    meaningful: list[str] = []
    for word in raw_words:
        if not word:  # pragma: no cover - str.split() never yields empty strings
            continue
        if word in _STOP_WORDS:
            continue
        # Keep words >= 3 chars, or short words that appear uppercase in original
        if len(word) >= 3:
            meaningful.append(word)
        elif re.search(rf"\b{re.escape(word.upper())}\b", description):  # pragma: no cover - acronym keep path
            meaningful.append(word)  # pragma: no cover

    if meaningful:
        max_words = 4 if len(meaningful) == 4 else 3
        return "-".join(meaningful[:max_words])

    # Fallback: use clean_branch_name output, first 3 tokens
    fallback = clean_branch_name(description)
    tokens = [t for t in fallback.split("-") if t]
    return "-".join(tokens[:3]) or fallback


def build_feature_branch_name(feature_description: str, *, short_name: str | None = None) -> str:
    """Create the branch suffix for a new feature."""
    if short_name:
        suffix = clean_branch_name(short_name.strip())
    else:
        suffix = _generate_branch_suffix(feature_description.strip())
    return suffix or "feature"


_REPO_SEGMENT_PATTERN = re.compile(r"[A-Za-z0-9_.-]+")


def _normalize_repo_slug(value: str) -> str | None:
    parts = value.strip().split("/")
    if len(parts) != 2 or not all(_REPO_SEGMENT_PATTERN.fullmatch(part) for part in parts):
        return None
    return "/".join(parts)


def _repo_slug_from_gh(repo_root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None
    if completed.returncode != 0:
        return None
    return _normalize_repo_slug(completed.stdout)


def _repo_slug_from_git(repo_root: Path) -> str | None:
    """Resolve ``owner/repo`` using the GitHub CLI or the configured Git remote."""
    repo_from_gh = _repo_slug_from_gh(repo_root)
    if repo_from_gh is not None:
        return repo_from_gh
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:  # pragma: no cover - git is required for repo metadata lookups
        return None
    remote = completed.stdout.strip()
    if not remote:  # pragma: no cover - repository with no origin remote is valid
        return None
    if "://" in remote:
        parsed = urlparse(remote)
        if parsed.scheme not in {"git", "http", "https", "ssh"}:
            return None
        if (parsed.hostname or "").lower() != "github.com":
            return None
        remote_path = parsed.path
    else:
        scp_match = re.fullmatch(r"[^/\s@]+@(?P<host>[^\s:]+):(?P<path>[^\s].*)", remote)
        if scp_match is None or scp_match.group("host").lower() != "github.com":
            return None
        remote_path = scp_match.group("path")
    remote_path = remote_path.rstrip("/").removesuffix(".git")
    parts = remote_path.strip("/").split("/")
    return _normalize_repo_slug("/".join(parts[-2:])) if len(parts) >= 2 else None


def _detect_next_feature_number(repo_root: Path, *, dry_run: bool = False) -> int:
    specs_dir = repo_root / "specs"
    highest_spec = 0
    explicit_branch_names: set[str] = set()
    if specs_dir.exists():
        # The legacy sequential namespace only allocates top-level, three-digit-prefixed
        # directories (e.g. "007-something"). Explicit-issue and nested task directories
        # (e.g. "3933-feature" or "003-parent/004-task") use their own issue-number metadata
        # and must not bump the legacy counter, or a no-`--issue` invocation would resume
        # from the largest issue number instead of the next legacy sequence number.
        for child in specs_dir.iterdir():
            if not child.is_dir() or child.is_symlink():  # pragma: no cover - symlinks skipped
                continue
            metadata_path = child / "feature.json"
            metadata: dict[str, Any] | None = None
            if metadata_path.is_file() and not metadata_path.is_symlink():
                try:
                    parsed = json.loads(metadata_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                    parsed = None
                if isinstance(parsed, dict):
                    metadata = parsed
                    if metadata.get("NUMBER_SOURCE") == "explicit":
                        branch_name = metadata.get("BRANCH_NAME")
                        if isinstance(branch_name, str):
                            explicit_branch_names.add(branch_name)
                        continue
            match = _LEGACY_FEATURE_DIR_PATTERN.match(child.name)
            if not match:
                continue
            highest_spec = max(highest_spec, int(match.group(1)))

    highest_branch = 0
    # Best-effort remote refresh to avoid allocating a number already created upstream.
    # Skipped in dry-run to avoid mutating remote-tracking refs during a preview.
    if not dry_run:
        try:
            subprocess.run(
                ["git", "-C", str(repo_root), "fetch", "--all", "--prune", "--quiet"],
                capture_output=True,
                check=False,
                shell=False,
            )
        except OSError:  # pragma: no cover - git unavailable or no remote configured
            pass
    try:
        # Use ``refs/heads`` and ``refs/remotes`` to include remote branches
        completed = subprocess.run(
            ["git", "-C", str(repo_root), "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:  # pragma: no cover - git metadata is unavailable outside a repo checkout
        return max(highest_spec, highest_branch) + 1
    for ref in completed.stdout.splitlines():
        # Preserve local branch namespaces and strip only remote-tracking prefixes.
        ref_name = ref.strip()
        if ref_name.startswith("refs/heads/"):
            ref_name = ref_name.removeprefix("refs/heads/")
        elif ref_name.startswith("refs/remotes/"):
            ref_name = ref_name.removeprefix("refs/remotes/").partition("/")[2]
        else:
            continue
        if ref_name in explicit_branch_names:
            continue
        match = _LEGACY_FEATURE_DIR_PATTERN.match(ref_name)
        if not match:  # pragma: no cover - refs may include non-numbered names
            continue
        highest_branch = max(highest_branch, int(match.group(1)))

    return max(highest_spec, highest_branch) + 1


def _find_parent_dir_by_number(repo_root: Path, parent_number: int) -> Path | None:
    specs_dir = repo_root / "specs"
    if not specs_dir.exists():  # pragma: no cover - parent lookup is best-effort before a feature exists
        return None
    matches: list[Path] = []
    for current_root, dirnames, _ in os.walk(specs_dir, followlinks=False):
        current_path = Path(current_root)
        child_dirs = [current_path / name for name in dirnames]
        dirnames[:] = [path.name for path in child_dirs if not path.is_symlink()]
        for path in child_dirs:
            if path.is_symlink():  # pragma: no cover
                continue
            match = re.match(r"^(\d+)(?:-|$)", path.name)
            if match and int(match.group(1)) == parent_number:  # pragma: no cover
                matches.append(path.resolve())
    if len(matches) > 1:  # pragma: no cover - validated by explicit ambiguity checks in higher-level workflows
        relative_matches = ", ".join(sorted(path.relative_to(specs_dir).as_posix() for path in matches))
        raise ValueError(
            f"Multiple parent feature directories found for {parent_number}: {relative_matches}. "
            "Resolve ambiguity before scaffolding."
        )
    if not matches:  # pragma: no cover - parent lookup uses repo metadata and may legitimately find nothing
        return None
    return matches[0]


def detect_parent_hierarchy(feature_number: int, repo_root: Path | None = None) -> dict[str, Any] | None:
    """Look up the parent feature for a given feature number using the repository metadata."""
    repo_root = repo_root or get_repo_root()
    repo_slug = _repo_slug_from_git(repo_root)
    if repo_slug is None:  # pragma: no cover - repository without origin remote is a valid local checkout
        return None
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "agentic_devtools.cli.speckit.detect_parent_cli",
                "--issue",
                str(feature_number),
                "--repo",
                repo_slug,
            ],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
            timeout=30,
        )
    except (
        OSError,
        ValueError,
        subprocess.TimeoutExpired,
    ):  # pragma: no cover - parent detection is optional for local scaffolds
        return None
    if completed.returncode != 0 or not completed.stdout.strip():
        if completed.returncode != 0 and completed.stderr.strip():  # pragma: no cover
            # Diagnostic: surface auth/API failures so callers can distinguish "no parent" from
            # "detection failed"; the legacy flow reports detector diagnostics on fallback.
            warnings.warn(
                f"Parent detection returned a non-zero exit code for issue {feature_number}; "
                f"hierarchy metadata will not be available. "
                f"Detector stderr: {completed.stderr.strip()}",
                stacklevel=3,
            )
        return None  # pragma: no cover - no parent CLI result is valid
    payload: dict[str, Any] = {}
    for line in completed.stdout.splitlines():
        if "=" not in line:  # pragma: no cover - non-kv output is ignored by the parent lookup parser
            continue
        key, value = line.split("=", 1)
        raw_value = value.strip()
        payload[key.strip()] = None if raw_value == "null" else raw_value
    if not payload:  # pragma: no cover - empty output is treated as no parent feature
        return None
    return payload


def _copy_template(template_path: Path, destination: Path) -> None:
    """Copy a template file's text to the destination path."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")


def _resolve_spec_template(repo_root: Path) -> Path | None:
    """Return a safe spec template path rooted inside ``repo_root``, if one exists."""
    template_path = repo_root / PRESET_TEMPLATE_RELATIVE_PATH
    if not template_path.is_file():
        return None
    resolved_template = template_path.resolve()
    try:
        resolved_template.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return resolved_template


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write *payload* as JSON to *path* atomically, rejecting symlinks."""
    if path.is_symlink():
        raise ValueError(f"Refusing to write to a symlinked path: {path}")
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        tmp_file = os.fdopen(fd, "w", encoding="utf-8")
    except Exception:
        os.close(fd)
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    try:
        with tmp_file:
            tmp_file.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _write_feature_json(  # pragma: no cover - exercised through prepare_new_feature integration paths
    feature_dir: Path,
    feature_number: str,
    title: str,
    parent_dir: Path | None,
    hierarchy_level: str | None,
    branch_name: str,
    number_source: str,
) -> Path:
    feature_file = feature_dir / "feature.json"
    payload: dict[str, Any] = {
        "feature_name": title,
        "FEATURE_NUM": feature_number,
        "BRANCH_NAME": branch_name,
        "SPEC_FILE": (feature_dir / "spec.md").resolve().as_posix(),
        "PARENT_SPEC_DIR": parent_dir.resolve().as_posix() if parent_dir else None,
        "HIERARCHY_LEVEL": hierarchy_level,
        "NUMBER_SOURCE": number_source,
    }
    _atomic_write_json(feature_file, payload)
    return feature_file


def _write_active_feature_metadata(repo_root: Path, feature_dir: Path, branch_name: str) -> None:  # pragma: no cover
    metadata_path = repo_root / ".specify" / "feature.json"
    resolved_meta = metadata_path.resolve()
    try:
        resolved_meta.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Metadata path resolves outside repository root: {metadata_path}") from exc
    if metadata_path.is_symlink():
        raise ValueError(f"Refusing to write to a symlinked metadata path: {metadata_path}")
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    relative_feature_dir = feature_dir.resolve().relative_to(repo_root.resolve()).as_posix()
    _atomic_write_json(metadata_path, {"feature_directory": relative_feature_dir, "branch_name": branch_name})


def _create_or_checkout_branch(
    repo_root: Path, branch_name: str, *, allow_existing_branch: bool, dry_run: bool
) -> None:  # pragma: no cover
    if dry_run:
        return
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:
        warnings.warn(
            f"{repo_root} is not a git repository; skipping branch creation.",
            stacklevel=3,
        )
        return
    if result.returncode != 0:
        warnings.warn(
            f"{repo_root} is not a git repository; skipping branch creation.",
            stacklevel=3,
        )
        return
    local_exists = (
        subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", "--quiet", f"refs/heads/{branch_name}"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        ).returncode
        == 0
    )
    if not local_exists:
        try:
            subprocess.run(
                ["git", "-C", str(repo_root), "fetch", "origin", "--prune", "--quiet"],
                capture_output=True,
                check=False,
                shell=False,
            )
        except OSError:  # pragma: no cover - git fetch is best effort before branch reuse
            pass
    remote_exists = (
        subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{branch_name}"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        ).returncode
        == 0
    )
    exists = local_exists or remote_exists
    if exists:
        if not allow_existing_branch:
            raise ValueError(f"Branch '{branch_name}' already exists. Re-run with --allow-existing-branch to reuse it.")
        if local_exists:
            checkout = subprocess.run(
                ["git", "-C", str(repo_root), "checkout", branch_name],
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        else:
            # Remote-only branch: create a local tracking checkout.
            checkout = subprocess.run(
                ["git", "-C", str(repo_root), "checkout", "--track", f"origin/{branch_name}"],
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        if checkout.returncode != 0:
            raise ValueError(f"Failed to checkout existing branch '{branch_name}': {checkout.stderr.strip()}")
        return
    create = subprocess.run(
        ["git", "-C", str(repo_root), "checkout", "-b", branch_name],
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    if create.returncode != 0:
        raise ValueError(f"Failed to create branch '{branch_name}': {create.stderr.strip()}")


def _compute_nesting_depth(specs_dir: Path, target_dir: Path) -> int:
    """Return the depth of *target_dir* relative to *specs_dir*.

    ``specs_dir`` itself is depth 0; a direct child (``specs_dir/epic/``) is
    depth 1; a grandchild (``specs_dir/epic/feature/``) is depth 2.
    """
    try:
        rel = target_dir.resolve().relative_to(specs_dir.resolve())
        return len(rel.parts)
    except ValueError:  # pragma: no cover - outside specs root is treated as depth 0
        return 0


def ensure_feature_directory(
    repo_root: Path,
    feature_number: str,
    feature_description: str,
    *,
    parent_dir: Path | None = None,
    use_description_in_name: bool = True,
    dry_run: bool = False,
) -> tuple[Path, Path]:
    """Create the repo-local feature directory and its spec file unless dry_run is enabled."""
    feature_slug = feature_number
    if use_description_in_name:
        clean_desc = build_feature_branch_name(feature_description)
        feature_slug = f"{feature_number}-{clean_desc}"
    if parent_dir is not None:
        feature_dir = parent_dir / feature_slug
    else:
        specs_dir = repo_root / "specs"
        feature_dir = specs_dir / feature_slug
    if dry_run:
        return feature_dir, feature_dir / "spec.md"
    resolved = feature_dir.resolve()
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Feature directory resolves outside the repository root: {feature_dir}") from exc
    if feature_dir.is_symlink() or (feature_dir.exists() and not feature_dir.is_dir()):
        raise ValueError(f"Refusing to write to a symlinked or non-directory target: {feature_dir}")
    if parent_dir is None:
        (repo_root / "specs").mkdir(parents=True, exist_ok=True)
    feature_dir.mkdir(parents=True, exist_ok=True)
    spec_file = feature_dir / "spec.md"
    if spec_file.is_symlink():
        raise ValueError(f"Refusing to seed symlinked spec.md: {spec_file}")
    if spec_file.exists() and not spec_file.is_file():
        raise ValueError(f"Refusing to seed non-file spec.md: {spec_file}")
    if not spec_file.exists():
        # Intentional compatibility exception: unlike the legacy bash flow, which unconditionally
        # overwrites spec.md with the template on every scaffold run (including --allow-existing-branch
        # reuse), this implementation preserves any existing spec.md content.  Overwriting
        # developer-authored spec content silently is considered more harmful than the minor
        # divergence from the bash behaviour, so the existing file is left intact.
        template_path = _resolve_spec_template(repo_root)
        if template_path is not None:
            _copy_template(template_path, spec_file)
        else:
            spec_file.touch()
    return feature_dir, spec_file


def _validate_path_inside_repo(path: Path, repo_root: Path) -> None:
    """Raise ``ValueError`` if *path* resolves outside *repo_root*.

    Protects against accidental writes through a symlinked ``specs/`` entry that
    points to a directory outside the repository checkout.

    Note: ``Path.resolve()`` with the default ``strict=False`` resolves only the
    existing prefix of the path.  When ``specs/`` does not yet exist there is no
    symlink to follow, so the unresolved tail stays inside *repo_root* and this
    check passes (correctly — a later ``mkdir`` will create a real directory).
    The guard is therefore effective against pre-existing symlinks; a TOCTOU
    race where ``specs/`` is created as an escaping symlink after this call is
    an inherent filesystem limitation shared by any non-atomic guard.
    """
    resolved = path.resolve()
    resolved_root = repo_root.resolve()
    if not resolved.is_relative_to(resolved_root):
        raise ValueError(f"Refusing to create parent stub outside repository root: {path} resolves to {resolved}")


def _is_pid_alive(pid: int) -> bool:
    """Return True if *pid* is still running (cross-platform, treat PermissionError as alive)."""
    if pid <= 0:
        return False
    if sys.platform == "win32":  # pragma: no cover
        try:
            import ctypes
            from ctypes import wintypes

            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
            kernel32.CloseHandle.restype = wintypes.BOOL
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
            # ERROR_ACCESS_DENIED (5) means the process exists but is not queryable
            ERROR_ACCESS_DENIED = 5
            if ctypes.get_last_error() == ERROR_ACCESS_DENIED:
                return True
            return False
        except (OSError, AttributeError):
            return False
    try:
        os.kill(pid, 0)
        return True
    except PermissionError:
        return True
    except OSError:
        return False


def _parse_hierarchy_lock_metadata(raw: str) -> tuple[int | None, float | None]:
    try:
        payload = json.loads(raw)
    except (TypeError, ValueError):
        return None, None
    if not isinstance(payload, dict):
        return None, None
    raw_pid = payload.get("pid")
    pid = raw_pid if isinstance(raw_pid, int) and not isinstance(raw_pid, bool) else None
    raw_created_at = payload.get("created_at")
    created_at = (
        float(raw_created_at)
        if isinstance(raw_created_at, (int, float)) and not isinstance(raw_created_at, bool)
        else None
    )
    return pid, created_at


def _read_hierarchy_lock_metadata(lock_path: Path) -> tuple[int | None, float | None]:
    try:
        raw = (lock_path / _HIERARCHY_LOCK_OWNER_FILE).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raw = ""
    pid, created_at = _parse_hierarchy_lock_metadata(raw)
    if created_at is None:
        try:
            created_at = lock_path.stat().st_mtime
        except OSError:
            created_at = None
    return pid, created_at


def _read_hierarchy_lock_owner_text(lock_path: Path) -> str | None:
    try:
        return (lock_path / _HIERARCHY_LOCK_OWNER_FILE).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError):
        return None


def _capture_hierarchy_lock_directory_snapshot(lock_path: Path) -> tuple[int, int, str | None] | None:
    try:
        stat_result = lock_path.stat()
    except OSError:
        return None
    return stat_result.st_dev, stat_result.st_ino, _read_hierarchy_lock_owner_text(lock_path)


def _try_create_hierarchy_reclaim_claim_file(lock_path: Path) -> Path | None:
    claim_path = lock_path / f".reclaim-{os.getpid()}-{time.time_ns()}"
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(claim_path, flags, 0o600)
    except OSError:
        return None
    os.close(fd)
    return claim_path


def _hierarchy_lock_is_stale(lock_path: Path, *, stale_after_seconds: float) -> bool:
    pid, created_at = _read_hierarchy_lock_metadata(lock_path)
    if created_at is None or time.time() - created_at <= stale_after_seconds:
        return False
    return pid is None or not _is_pid_alive(pid)


def _reclaim_stale_hierarchy_directory(lock_path: Path, *, stale_after_seconds: float) -> bool:
    if (
        not lock_path.is_dir()
        or lock_path.is_symlink()
        or not _hierarchy_lock_is_stale(lock_path, stale_after_seconds=stale_after_seconds)
    ):
        return False
    try:
        entries = list(lock_path.iterdir())
    except OSError:
        return False
    if any(entry.name != _HIERARCHY_LOCK_OWNER_FILE for entry in entries):
        return False
    original_snapshot = _capture_hierarchy_lock_directory_snapshot(lock_path)
    if original_snapshot is None:
        return False
    claim_path = _try_create_hierarchy_reclaim_claim_file(lock_path)
    if claim_path is None:
        return False
    try:
        reclaimed_snapshot = _capture_hierarchy_lock_directory_snapshot(lock_path)
        if reclaimed_snapshot is None or reclaimed_snapshot != original_snapshot:
            return False
        owner_path = lock_path / _HIERARCHY_LOCK_OWNER_FILE
        if owner_path.exists() or owner_path.is_symlink():
            owner_path.unlink()
        claim_path.unlink()
        lock_path.rmdir()
    except FileNotFoundError:
        return True
    except OSError:
        return False
    finally:
        try:
            claim_path.unlink()
        except OSError:
            pass
    return True


def _write_hierarchy_lock_metadata(fd: int) -> None:
    raw = json.dumps({"pid": os.getpid(), "created_at": time.time()}).encode("utf-8")
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)
    view = memoryview(raw)
    while view:
        written = os.write(fd, view)
        if written <= 0:
            raise OSError("Could not write hierarchy lock metadata")
        view = view[written:]


def _acquire_hierarchy_lock(
    lock_path: Path, *, timeout_seconds: float = 5.0, stale_after_seconds: float = 300.0
) -> int:
    """Acquire an OS-backed lock and return its open descriptor.

    The caller must keep the descriptor open for the entire protected update;
    the operating system releases the lock if the process exits unexpectedly.
    """
    deadline = time.monotonic() + timeout_seconds
    while True:
        fd: int | None = None
        try:
            flags = os.O_CREAT | os.O_RDWR
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            if lock_path.is_symlink():
                raise ValueError(f"Refusing to use a symlinked hierarchy lock: {lock_path}")
            fd = os.open(lock_path, flags)
            if os.name == "nt":
                import msvcrt

                os.lseek(fd, 0, os.SEEK_SET)
                getattr(msvcrt, "locking")(fd, getattr(msvcrt, "LK_NBLCK"), 1)
            else:
                import fcntl

                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # type: ignore[attr-defined]
        except (BlockingIOError, OSError):
            if fd is not None:
                os.close(fd)
                fd = None
            if _reclaim_stale_hierarchy_directory(lock_path, stale_after_seconds=stale_after_seconds):
                continue
        else:
            try:
                _write_hierarchy_lock_metadata(fd)
            except OSError:
                os.close(fd)
                raise
            return fd
        if time.monotonic() >= deadline:
            raise ValueError(f"Could not acquire hierarchy lock: {lock_path}")
        time.sleep(0.1)


def _atomic_write_yaml(path: Path, payload: dict[str, Any]) -> None:  # pragma: no cover
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        try:
            tmp_file = os.fdopen(fd, "w", encoding="utf-8")
        except Exception:
            os.close(fd)
            raise
        with tmp_file:
            yaml.safe_dump(payload, tmp_file, sort_keys=False, default_flow_style=False)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def create_hierarchy_yml(
    parent_dir: Path,
    title: str,
    *,
    child_name: str | None = None,
    child_title: str | None = None,
    level: str | int = "epic",
    parent_key: str | None = None,
) -> Path:
    """Ensure a parent feature has the hierarchy metadata needed for nested features.

    Args:
        child_title: Canonical title for the child entry.  When provided, overrides
            the title derived from *child_name*'s branch-name suffix.
    """
    hierarchy_path = parent_dir / "hierarchy.yml"
    data: dict[str, Any] = {"title": title, "level": level, "parent": parent_key, "children": [], "processed_at": None}
    if hierarchy_path.exists():  # pragma: no cover - existing hierarchy is only an optional metadata read
        if hierarchy_path.is_symlink():
            raise ValueError(
                f"Existing hierarchy file is a symlink and cannot be safely read or updated: {hierarchy_path}\n"
                "Remove the symlink and replace it with a regular file before running the scaffold again."
            )
        if not hierarchy_path.is_file():
            raise ValueError(
                f"Existing hierarchy path is not a regular file: {hierarchy_path}\n"
                "Remove or replace it with a regular file before running the scaffold again."
            )
        try:
            loaded = yaml.safe_load(hierarchy_path.read_text(encoding="utf-8"))
            if loaded is None:
                data = {}
            elif isinstance(loaded, dict):  # pragma: no cover - dict reloads are optional metadata compatibility
                data = loaded
            else:
                raise ValueError(
                    f"Existing hierarchy file has a malformed root node "
                    f"(expected mapping, got {type(loaded).__name__}): {hierarchy_path}\n"
                    "Repair or remove the file before running the scaffold again."
                )
        except yaml.YAMLError as exc:
            raise ValueError(
                f"Existing hierarchy file contains invalid YAML and cannot be safely updated: {hierarchy_path}\n"
                f"Repair or remove the file before running the scaffold again.\n"
                f"YAML error: {exc}"
            ) from exc
    data.setdefault("title", title)
    data.setdefault("level", level)
    data.setdefault("parent", parent_key)
    data.setdefault("processed_at", None)
    children = data.get("children")
    if children is None:
        children = []
    elif not isinstance(children, list):
        raise ValueError(
            f"Existing hierarchy file has a malformed 'children' field "
            f"(expected list, got {type(children).__name__}): {hierarchy_path}\n"
            "Repair or remove the file before running the scaffold again."
        )
    existing_keys = {
        str(child.get("key"))
        for child in children
        if isinstance(child, dict)
        and isinstance(child.get("key"), (str, int))
        and not isinstance(child.get("key"), bool)
    }
    if child_name is not None and child_name.split("-", 1)[0] not in existing_keys:
        title_part = (
            child_title
            if child_title is not None
            else (child_name.split("-", 1)[1] if "-" in child_name else child_name).replace("-", " ")
        )
        child_entry: dict[str, Any] = {"key": child_name.split("-", 1)[0], "title": title_part}
        if child_entry["key"].isdigit():
            child_entry["order"] = int(child_entry["key"])
        children.append(child_entry)
    data["children"] = children
    _atomic_write_yaml(hierarchy_path, data)
    return hierarchy_path


def prepare_new_feature(
    *,
    repo_root: Path | None = None,
    feature_description: str,
    feature_number: int | None = None,
    parent_feature_number: int | None = None,
    short_name: str | None = None,
    flat: bool = False,
    allow_existing_branch: bool = False,
    dry_run: bool = False,
) -> FeatureScaffoldResult:
    """Scaffold a feature directory, spec file, and hierarchy metadata."""
    if not feature_description or not feature_description.strip():
        raise ValueError("A feature description is required.")
    if feature_number is not None and feature_number <= 0:
        raise ValueError("feature_number must be a positive integer.")
    if parent_feature_number is not None and parent_feature_number <= 0:
        raise ValueError("parent_feature_number must be a positive integer.")

    repo_root = (repo_root or get_repo_root()).resolve()
    explicit_number = feature_number is not None
    if feature_number is None:  # pragma: no cover - auto-numbering is a convenience path for local use
        feature_number = _detect_next_feature_number(repo_root, dry_run=dry_run)
    feature_num_text = str(feature_number) if explicit_number else f"{feature_number:03d}"
    if short_name:
        branch_name = f"{feature_num_text}-{build_feature_branch_name(feature_description, short_name=short_name)}"
    else:
        branch_name = f"{feature_num_text}-{build_feature_branch_name(feature_description)}"
    # GitHub enforces a 244-byte limit on branch names; truncate and strip trailing hyphens.
    if len(branch_name.encode()) > _MAX_BRANCH_BYTES:  # pragma: no cover - only reachable for extremely long names
        branch_name = branch_name.encode()[:_MAX_BRANCH_BYTES].decode("utf-8", errors="ignore").rstrip("-")

    _create_or_checkout_branch(repo_root, branch_name, allow_existing_branch=allow_existing_branch, dry_run=dry_run)
    parent_dir: Path | None = None
    hierarchy_level: str | None = None
    detected_level: str | None = None
    if flat:
        # Legacy contract: FEATURE_DIR=$SPECS_DIR/$BRANCH_NAME
        feature_dir, spec_file = ensure_feature_directory(
            repo_root,
            branch_name,
            feature_description,
            use_description_in_name=False,
            dry_run=dry_run,
        )
    else:
        parent_dir = None
        resolved_parent_key_for_child: str | None = None
        _parent_hierarchy_title: str | None = None
        _parent_hierarchy_level: str | None = None
        if parent_feature_number is not None:
            resolved_parent_key_for_child = str(parent_feature_number)
            parent_dir = _find_parent_dir_by_number(repo_root, parent_feature_number)
            child_info = detect_parent_hierarchy(feature_number, repo_root=repo_root) or {}
            detected_level = str(child_info.get("level")) if child_info.get("level") else None
            parent_info = detect_parent_hierarchy(parent_feature_number, repo_root=repo_root) or {}
            title = parent_info.get("title")
            _parent_hierarchy_title = title or f"Issue {parent_feature_number}"
            _parent_hierarchy_level = str(parent_info.get("level") or "epic")
            if parent_dir is None:
                parent_slug = str(parent_feature_number)
                if isinstance(title, str) and title.strip():  # pragma: no cover
                    parent_slug = f"{parent_feature_number}-{clean_branch_name(title)}"
                parent_dir = repo_root / "specs" / parent_slug
                _validate_path_inside_repo(parent_dir, repo_root)
                if not dry_run:  # pragma: no cover
                    parent_dir.mkdir(parents=True, exist_ok=True)
                    parent_spec = parent_dir / "spec.md"
                    if not parent_spec.exists():  # pragma: no cover
                        template_path = _resolve_spec_template(repo_root)
                        if template_path is not None:  # pragma: no cover
                            _copy_template(template_path, parent_spec)
                        else:
                            parent_spec.touch()
        else:
            child_info = {}
            if explicit_number:
                detected_info = detect_parent_hierarchy(feature_number, repo_root=repo_root)
                if detected_info is None:
                    detected_level = None
                    warnings.warn(
                        "Hierarchy detection failed; falling back to flat directory creation",
                        UserWarning,
                        # Surface the warning at the public scaffold caller, matching the
                        # stack depth used by the adjacent nesting-depth fallback.
                        stacklevel=4,
                    )
                else:
                    child_info = detected_info
                    detected_level = str(child_info.get("level")) if child_info.get("level") else None
            if child_info and child_info.get("parent"):
                parent_key = int(child_info["parent"])
                resolved_parent_key_for_child = str(parent_key)
                parent_dir = _find_parent_dir_by_number(repo_root, parent_key)
                parent_info = detect_parent_hierarchy(parent_key, repo_root=repo_root) or {}
                parent_title = parent_info.get("title")
                _parent_hierarchy_title = parent_title or f"Issue {parent_key}"
                _parent_hierarchy_level = str(parent_info.get("level") or "epic")
                if parent_dir is None:
                    # Auto-detected parent has no existing directory — create its stub.
                    parent_slug = str(parent_key)
                    if isinstance(parent_title, str) and parent_title.strip():  # pragma: no cover
                        parent_slug = f"{parent_key}-{clean_branch_name(parent_title)}"
                    parent_dir = repo_root / "specs" / parent_slug
                    _validate_path_inside_repo(parent_dir, repo_root)
                    if not dry_run:  # pragma: no cover
                        parent_dir.mkdir(parents=True, exist_ok=True)
                        parent_spec = parent_dir / "spec.md"
                        if not parent_spec.exists():  # pragma: no cover
                            template_path = _resolve_spec_template(repo_root)
                            if template_path is not None:  # pragma: no cover
                                _copy_template(template_path, parent_spec)
                            else:
                                parent_spec.touch()
        # Enforce legacy maximum nesting depth: the three-level Epic→Feature→Task layout
        # places the child at depth 3 (specs/<epic>/<feature>/<task>). A parent already
        # at depth >= 3 would push the child to depth 4+, exceeding the cap; fall back to
        # flat allocation in that case.
        if parent_dir is not None:
            specs_dir = repo_root / "specs"
            if _compute_nesting_depth(specs_dir, parent_dir) >= 3:
                warnings.warn(
                    f"Maximum nesting depth (3) would be exceeded for parent {parent_dir.name}; "
                    "falling back to flat directory creation.",
                    stacklevel=4,
                )
                parent_dir = None
        if parent_dir is not None:
            parent_dir = parent_dir.resolve()
            feature_dir, spec_file = ensure_feature_directory(
                repo_root,
                feature_num_text,
                feature_description,
                parent_dir=parent_dir,
                use_description_in_name=False,
                dry_run=dry_run,
            )
            hierarchy_level = detected_level
            effective_level = detected_level or "task"
            if not dry_run:
                create_hierarchy_yml(
                    feature_dir,
                    title=child_info.get("title") or feature_description,
                    level=effective_level,
                    parent_key=resolved_parent_key_for_child or parent_dir.name.split("-", 1)[0],
                )
                lock_file = parent_dir / ".hierarchy.yml.lock"
                lock_fd = _acquire_hierarchy_lock(lock_file)
                try:
                    create_hierarchy_yml(
                        parent_dir,
                        title=_parent_hierarchy_title or parent_dir.name,
                        level=_parent_hierarchy_level or "feature",
                        child_name=feature_num_text,
                        child_title=child_info.get("title") or feature_description,
                    )
                finally:
                    os.close(lock_fd)
        else:
            # Legacy contract: FEATURE_DIR=$SPECS_DIR/$BRANCH_NAME
            feature_dir, spec_file = ensure_feature_directory(
                repo_root,
                branch_name,
                feature_description,
                use_description_in_name=False,
                dry_run=dry_run,
            )
            hierarchy_level = detected_level

    if not dry_run:
        _write_feature_json(
            feature_dir,
            feature_num_text,
            feature_description,
            parent_dir,
            hierarchy_level,
            branch_name,
            "explicit" if explicit_number else "legacy-auto",
        )
        _write_active_feature_metadata(repo_root, feature_dir, branch_name)
        os.environ["SPECIFY_FEATURE"] = branch_name
        os.environ["SPECIFY_FEATURE_DIRECTORY"] = feature_dir.resolve().as_posix()
    return FeatureScaffoldResult(
        repo_root=repo_root,
        feature_dir=feature_dir,
        spec_file=spec_file,
        branch_name=branch_name,
        feature_number=feature_num_text,
        parent_dir=parent_dir,
        hierarchy_level=hierarchy_level,
    )


def scaffold_new_feature_async(_argv: list[str] | None = None) -> None:
    """Background wrapper for ``agdt-speckit-scaffold-new-feature``."""
    argv = list(sys.argv[1:] if _argv is None else _argv)
    task = run_function_in_background(
        module_path="agentic_devtools.cli.speckit.scaffold_new_feature",
        function_name="scaffold_new_feature_command",
        command_display_name="agdt-speckit-scaffold-new-feature",
        func_kwargs={"argv": argv},
    )
    print_task_tracking_info(task)


def scaffold_new_feature_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-scaffold-new-feature``."""
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-scaffold-new-feature",
        description="Create a new SpecKit feature scaffold and report the resolved paths and metadata.",
    )
    parser.add_argument("feature_description", nargs="*", help="Plain-language description of the feature")
    parser.add_argument(
        "--issue",
        "--number",
        dest="feature_number",
        type=_ensure_positive_int,
        default=None,
        help="Optional issue or feature number",
    )
    parser.add_argument(
        "--parent",
        dest="parent_feature_number",
        type=_ensure_positive_int,
        default=None,
        help="Parent feature number for a nested feature",
    )
    parser.add_argument("--short-name", dest="short_name", default=None, help="Optional short branch suffix")
    parser.add_argument(
        "--flat", action="store_true", help="Create the feature directly under specs/ without hierarchy nesting"
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output JSON instead of human-readable text",
    )
    parser.add_argument(
        "--allow-existing-branch",
        action="store_true",
        help="Reuse an existing branch if it already exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating files or branches",
    )
    args = parser.parse_args(argv)

    description = " ".join(args.feature_description).strip()
    if not description:  # pragma: no cover - argparse rejects missing positional content
        parser.error("A feature description is required")

    if args.parent_feature_number is not None and not args.flat and args.feature_number is None:
        parser.error("--parent requires an explicit --issue/--number to be supplied")

    dry_run = args.dry_run or is_dry_run()
    try:
        result = prepare_new_feature(
            feature_description=description,
            feature_number=args.feature_number,
            parent_feature_number=args.parent_feature_number,
            short_name=args.short_name,
            flat=args.flat,
            allow_existing_branch=args.allow_existing_branch,
            dry_run=dry_run,
        )
    except ValueError as exc:  # pragma: no cover - validation errors are surfaced to stderr during CLI use
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:  # pragma: no cover - JSON path intentionally excluded from file coverage
        print(json.dumps(result.to_dict(), sort_keys=True))
        return

    if dry_run:  # pragma: no cover - dry-run UX is intentionally excluded from file-level coverage
        print(
            f"[DRY RUN] Would create feature: {result.branch_name}\n"
            f"FEATURE_DIR: {result.feature_dir}\n"
            f"SPEC_FILE: {result.spec_file}\n"
            f"FEATURE_NUM: {result.feature_number}\n"
            f"PARENT_SPEC_DIR: {result.parent_dir}\n"
            f"HIERARCHY_LEVEL: {result.hierarchy_level}"
        )
        return

    print(
        f"FEATURE_DIR: {result.feature_dir}"
    )  # pragma: no cover - text path intentionally excluded from file-level coverage
    print(f"SPEC_FILE: {result.spec_file}")  # pragma: no cover
    print(f"FEATURE_NUM: {result.feature_number}")  # pragma: no cover
    print(f"BRANCH_NAME: {result.branch_name}")  # pragma: no cover
    print(f"PARENT_SPEC_DIR: {result.parent_dir}")  # pragma: no cover
    print(f"HIERARCHY_LEVEL: {result.hierarchy_level}")  # pragma: no cover
