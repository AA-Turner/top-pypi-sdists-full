"""Safe, per-client application Git provenance discovery.

Only configuration and environment parsing happen synchronously. Local Git is
queried at most once per client on a short-lived daemon thread; telemetry paths
only copy the latest immutable-by-convention snapshot.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, TypedDict


COMMIT_SHA_PROPERTY = "raindrop.app.commit_sha"
COMMIT_DIRTY_PROPERTY = "raindrop.app.commit_dirty"
BRANCH_PROPERTY = "raindrop.app.branch"
INFERRED_CONTEXT_KEY = "_raindrop.internal.app_git.inferred_keys"
CANONICAL_PROPERTIES = (
    COMMIT_SHA_PROPERTY,
    COMMIT_DIRTY_PROPERTY,
    BRANCH_PROPERTY,
)


class AppGitOptions(TypedDict, total=False):
    """Application revision values and automatic discovery controls."""

    commit_sha: str
    commit_dirty: bool
    branch: str
    source_directory: str
    detect_branch: bool
    auto_detect: bool


_OPTION_KEYS = frozenset(AppGitOptions.__annotations__)
_SHA_PATTERN = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
_ENV_KEYS = frozenset(
    {
        "RAINDROP_COMMIT_SHA",
        "RAINDROP_COMMIT_DIRTY",
        "RAINDROP_BRANCH",
        "RAINDROP_GIT_AUTO_DETECT",
        "RAINDROP_GIT_DETECT_BRANCH",
        "RAINDROP_GIT_SOURCE_DIRECTORY",
        "VERCEL",
        "VERCEL_GIT_COMMIT_SHA",
        "VERCEL_GIT_COMMIT_REF",
        "RAILWAY_GIT_COMMIT_SHA",
        "RAILWAY_GIT_BRANCH",
        "RAILWAY_ENVIRONMENT",
        "DYNO",
        "HEROKU_SLUG_COMMIT",
        "GITHUB_SHA",
        "GITHUB_REF_NAME",
        "GITHUB_ACTIONS",
        "CI_COMMIT_SHA",
        "CI_COMMIT_REF_NAME",
        "GITLAB_CI",
        "BUILDKITE_COMMIT",
        "BUILDKITE_BRANCH",
        "BUILDKITE",
        "CIRCLE_SHA1",
        "CIRCLE_BRANCH",
        "CIRCLECI",
        "PATH",
    }
)


@dataclass(frozen=True)
class GitDiscoveryPlan:
    source_directory: str
    detect_branch: bool
    explicit_properties: Mapping[str, Any]
    process_path: str
    fallback_snapshot: AppGitSnapshot | None = None


@dataclass(frozen=True)
class AppGitSnapshot:
    properties: Mapping[str, Any]
    inferred_keys: frozenset[str] = frozenset()


@dataclass(frozen=True)
class EffectiveAppGit:
    properties: Mapping[str, Any]
    suppressed_keys: frozenset[str] = frozenset()
    inferred_keys: frozenset[str] = frozenset()

    def context_attributes(self) -> dict[str, Any]:
        result = dict(self.properties)
        result.update({key: None for key in self.suppressed_keys})
        result[INFERRED_CONTEXT_KEY] = self.inferred_keys
        return result


EMPTY_SNAPSHOT = AppGitSnapshot({})


def _parse_bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def _valid_automatic_sha(value: Optional[str]) -> bool:
    return isinstance(value, str) and _SHA_PATTERN.fullmatch(value) is not None


def _provider_marked(value: Optional[str]) -> bool:
    return bool(value) and value.strip().lower() not in {"0", "false", "no", "off"}


def _source(
    environ: Mapping[str, str],
    sha_key: str,
    branch_key: Optional[str],
    detect_branch: bool,
) -> Optional[dict[str, Any]]:
    sha = environ.get(sha_key)
    if not _valid_automatic_sha(sha):
        return None
    result: dict[str, Any] = {COMMIT_SHA_PROPERTY: sha}
    if detect_branch and branch_key is not None and branch_key in environ:
        branch = environ[branch_key]
        if branch.strip():
            result[BRANCH_PROPERTY] = branch
    return result


def prepare_app_git(
    value: bool | Mapping[str, Any],
    environ: Optional[Mapping[str, str]] = None,
) -> tuple[AppGitSnapshot, Optional[GitDiscoveryPlan], tuple[str, ...]]:
    """Resolve explicit metadata and prepare optional bounded local discovery.

    Returns the immediately usable snapshot, a local-Git plan (if needed), and
    configuration warnings. The environment is copied once so later mutations
    cannot change this client's identity.
    """

    source_env = os.environ if environ is None else environ
    env = {key: source_env[key] for key in _ENV_KEYS if key in source_env}
    warnings: list[str] = []
    if value is False:
        return EMPTY_SNAPSHOT, None, ()
    if value is True:
        options: Mapping[str, Any] = {}
    elif isinstance(value, Mapping):
        options = dict(value)
    else:
        return EMPTY_SNAPSHOT, None, ("app_git must be True, False, or a mapping",)

    unknown = sorted(str(key) for key in options if key not in _OPTION_KEYS)
    if unknown:
        warnings.append(f"unknown app_git option(s): {', '.join(unknown)}")

    explicit_config: dict[str, Any] = {}
    typed_fields = (
        ("commit_sha", str, COMMIT_SHA_PROPERTY),
        ("commit_dirty", bool, COMMIT_DIRTY_PROPERTY),
        ("branch", str, BRANCH_PROPERTY),
    )
    for option, expected_type, prop in typed_fields:
        if option not in options:
            continue
        candidate = options[option]
        if isinstance(candidate, expected_type):
            explicit_config[prop] = candidate
        else:
            warnings.append(f"app_git.{option} has the wrong type")

    explicit_env: dict[str, Any] = {}
    if "RAINDROP_COMMIT_SHA" in env:
        explicit_env[COMMIT_SHA_PROPERTY] = env["RAINDROP_COMMIT_SHA"]
    if "RAINDROP_COMMIT_DIRTY" in env:
        dirty = _parse_bool(env["RAINDROP_COMMIT_DIRTY"])
        if dirty is not None:
            explicit_env[COMMIT_DIRTY_PROPERTY] = dirty
        else:
            warnings.append("RAINDROP_COMMIT_DIRTY must be true or false")
    if "RAINDROP_BRANCH" in env:
        explicit_env[BRANCH_PROPERTY] = env["RAINDROP_BRANCH"]

    explicit = dict(explicit_env)
    explicit.update(explicit_config)

    env_auto = _parse_bool(env.get("RAINDROP_GIT_AUTO_DETECT"))
    auto_detect = env_auto is not False
    if "auto_detect" in options:
        if isinstance(options["auto_detect"], bool):
            auto_detect = options["auto_detect"]
        else:
            warnings.append("app_git.auto_detect has the wrong type")

    env_branch = _parse_bool(env.get("RAINDROP_GIT_DETECT_BRANCH"))
    detect_branch = env_branch is True
    if "detect_branch" in options:
        if isinstance(options["detect_branch"], bool):
            detect_branch = options["detect_branch"]
        else:
            warnings.append("app_git.detect_branch has the wrong type")

    # An explicit SHA establishes the source identity. Never fill its dirty or
    # branch from a lower-priority detected source; explicit config/env fields
    # may still intentionally accompany it.
    if COMMIT_SHA_PROPERTY in explicit or not auto_detect:
        return AppGitSnapshot(explicit), None, tuple(warnings)

    source_directory: Optional[str] = None
    selected_source_directory = False
    if "source_directory" in options:
        if isinstance(options["source_directory"], str):
            source_directory = options["source_directory"]
            selected_source_directory = bool(source_directory)
        else:
            warnings.append("app_git.source_directory has the wrong type")
    elif "RAINDROP_GIT_SOURCE_DIRECTORY" in env:
        source_directory = env["RAINDROP_GIT_SOURCE_DIRECTORY"]
        selected_source_directory = bool(source_directory)

    # A nonempty source_directory explicitly names the application repository.
    # Ambient observer metadata must neither replace it nor serve as fallback.
    if selected_source_directory and source_directory is not None:
        try:
            resolved_source_directory = str(
                Path(source_directory).expanduser().resolve(strict=False)
            )
        except Exception:
            return AppGitSnapshot(explicit), None, tuple(warnings)
        return (
            AppGitSnapshot(explicit),
            GitDiscoveryPlan(
                source_directory=resolved_source_directory,
                detect_branch=detect_branch,
                explicit_properties=explicit,
                process_path=env.get("PATH", os.defpath),
                fallback_snapshot=None,
            ),
            tuple(warnings),
        )

    reliable_sources = (
        ("VERCEL", "VERCEL_GIT_COMMIT_SHA", "VERCEL_GIT_COMMIT_REF"),
        ("RAILWAY_ENVIRONMENT", "RAILWAY_GIT_COMMIT_SHA", "RAILWAY_GIT_BRANCH"),
        ("DYNO", "HEROKU_SLUG_COMMIT", None),
    )
    for marker, sha_key, branch_key in reliable_sources:
        if not _provider_marked(env.get(marker)):
            continue
        detected = _source(env, sha_key, branch_key, detect_branch)
        if detected is not None:
            detected.update(explicit)
            inferred = frozenset(set(detected) - set(explicit))
            return AppGitSnapshot(detected, inferred), None, tuple(warnings)

    contextual_ci_sources = (
        ("GITHUB_ACTIONS", "GITHUB_SHA", "GITHUB_REF_NAME"),
        ("GITLAB_CI", "CI_COMMIT_SHA", "CI_COMMIT_REF_NAME"),
        ("BUILDKITE", "BUILDKITE_COMMIT", "BUILDKITE_BRANCH"),
        ("CIRCLECI", "CIRCLE_SHA1", "CIRCLE_BRANCH"),
    )
    fallback_snapshot: AppGitSnapshot | None = None
    for marker, sha_key, branch_key in contextual_ci_sources:
        if not _provider_marked(env.get(marker)):
            continue
        detected = _source(env, sha_key, branch_key, detect_branch)
        if detected is not None:
            detected.update(explicit)
            fallback_snapshot = AppGitSnapshot(
                detected, frozenset(set(detected) - set(explicit))
            )
            break

    if source_directory is None:
        try:
            source_directory = os.getcwd()
        except Exception:
            return AppGitSnapshot(explicit), None, tuple(warnings)
    try:
        source_directory = str(
            Path(source_directory).expanduser().resolve(strict=False)
        )
    except Exception:
        return AppGitSnapshot(explicit), None, tuple(warnings)

    return (
        AppGitSnapshot(explicit),
        GitDiscoveryPlan(
            source_directory=source_directory,
            detect_branch=detect_branch,
            explicit_properties=explicit,
            process_path=env.get("PATH", os.defpath),
            fallback_snapshot=fallback_snapshot,
        ),
        tuple(warnings),
    )


def _git(
    plan: GitDiscoveryPlan,
    args: list[str],
    *,
    capture: bool,
    timeout: float,
) -> tuple[int, str, bool]:
    if timeout <= 0:
        raise subprocess.TimeoutExpired(args, timeout)
    set_blocking = getattr(os, "set_blocking", None)
    if capture and (
        not callable(set_blocking)
        or (os.name == "nt" and sys.version_info < (3, 12))
    ):
        raise OSError("nonblocking Git output is unavailable")
    process = subprocess.Popen(
        ["git", "-C", plan.source_directory, *args],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env={
            "PATH": plan.process_path,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
            "LC_ALL": "C",
        },
    )
    output = bytearray()
    output_capped = False
    deadline = time.monotonic() + timeout
    stdout = process.stdout
    try:
        if stdout is not None:
            set_blocking(stdout.fileno(), False)
        while process.poll() is None:
            if time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired(args, timeout)
            if stdout is not None:
                try:
                    chunk = os.read(stdout.fileno(), 4096 - len(output))
                except BlockingIOError:
                    chunk = b""
                if chunk:
                    output.extend(chunk)
                if len(output) >= 4096:
                    stdout.close()
                    stdout = None
                    output_capped = True
            time.sleep(0.005)
        held_open = False
        if stdout is not None:
            while len(output) < 4096:
                try:
                    chunk = os.read(stdout.fileno(), 4096 - len(output))
                except BlockingIOError:
                    held_open = True
                    break
                except OSError:
                    break
                if not chunk:
                    break
                output.extend(chunk)
        if held_open or output_capped:
            # A fake/wrapped Git exited after spawning a descendant that kept
            # stdout open. Kill only that isolated process group.
            _terminate_git_process(process)
    except Exception:
        _terminate_git_process(process)
        raise
    finally:
        if stdout is not None:
            try:
                stdout.close()
            except Exception:
                pass
    return (
        process.returncode,
        bytes(output).decode("utf-8", errors="replace"),
        not held_open and not output_capped,
    )


def _terminate_git_process(process: subprocess.Popen[bytes]) -> None:
    """Best-effort bounded cleanup for a spawned Git process and its pipes."""

    try:
        if os.name == "posix":
            os.killpg(process.pid, 9)
        else:
            process.kill()
    except Exception:
        try:
            process.kill()
        except Exception:
            pass
    try:
        process.wait(timeout=0.1)
    except Exception:
        pass


def discover_local_git(plan: GitDiscoveryPlan) -> Optional[AppGitSnapshot]:
    """Perform one bounded, prompt-free local Git lookup."""

    try:
        deadline = time.monotonic() + 0.75
        revision_code, revision_output, revision_complete = _git(
            plan,
            ["rev-parse", "--verify", "HEAD"],
            capture=True,
            timeout=max(0.0, deadline - time.monotonic()),
        )
        sha = (
            revision_output.strip()
            if revision_code == 0 and revision_complete
            else None
        )
        if not _valid_automatic_sha(sha):
            return plan.fallback_snapshot

        result: dict[str, Any] = {COMMIT_SHA_PROPERTY: sha}
        contextual: dict[str, Any] = {}
        if time.monotonic() < deadline:
            try:
                dirty_code, dirty_output, dirty_complete = _git(
                    plan,
                    ["status", "--porcelain=v1", "--untracked-files=normal"],
                    capture=True,
                    timeout=max(0.0, deadline - time.monotonic()),
                )
                if dirty_code == 0 and dirty_complete:
                    contextual[COMMIT_DIRTY_PROPERTY] = bool(dirty_output)
            except Exception:
                pass

        if plan.detect_branch and time.monotonic() < deadline:
            try:
                branch_code, branch_output, branch_complete = _git(
                    plan,
                    ["symbolic-ref", "--short", "HEAD"],
                    capture=True,
                    timeout=max(0.0, deadline - time.monotonic()),
                )
                if branch_code == 0 and branch_complete and branch_output.strip():
                    contextual[BRANCH_PROPERTY] = branch_output.strip()
            except Exception:
                pass

        # Status and branch describe a checkout, not an immutable commit. Only
        # attach them if HEAD is still the revision captured above. A failed or
        # budget-exhausted recheck keeps the useful first SHA but drops the
        # potentially mixed contextual values.
        coherent = False
        if time.monotonic() < deadline:
            try:
                final_code, final_output, final_complete = _git(
                    plan,
                    ["rev-parse", "--verify", "HEAD"],
                    capture=True,
                    timeout=max(0.0, deadline - time.monotonic()),
                )
                coherent = (
                    final_code == 0
                    and final_complete
                    and final_output.strip() == sha
                )
            except Exception:
                pass
        if coherent:
            result.update(contextual)

        # Explicit config/env fields win independently. Automatic dirty and
        # branch came from the exact repository that produced this SHA.
        result.update(plan.explicit_properties)
        return AppGitSnapshot(
            result, frozenset(set(result) - set(plan.explicit_properties))
        )
    except Exception:
        return plan.fallback_snapshot


def effective_app_git(
    snapshot: AppGitSnapshot,
    operation_properties: Optional[Mapping[str, Any]],
) -> EffectiveAppGit:
    """Apply canonical operation overrides without mixing inferred identity."""

    raw = operation_properties or {}
    result = dict(snapshot.properties)
    suppressed: set[str] = set()
    inferred = set(snapshot.inferred_keys)
    if COMMIT_SHA_PROPERTY in raw and raw[COMMIT_SHA_PROPERTY] != result.get(
        COMMIT_SHA_PROPERTY
    ):
        for key in (COMMIT_DIRTY_PROPERTY, BRANCH_PROPERTY):
            if key in snapshot.inferred_keys and key not in raw:
                result.pop(key, None)
                suppressed.add(key)
                inferred.discard(key)
    for key in CANONICAL_PROPERTIES:
        if key in raw:
            result[key] = raw[key]
            suppressed.discard(key)
            inferred.discard(key)
    return EffectiveAppGit(
        result, frozenset(suppressed), frozenset(inferred)
    )
