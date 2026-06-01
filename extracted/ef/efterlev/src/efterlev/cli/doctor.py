"""`efterlev doctor` — self-diagnose pre-flight checks.

Priority 3 (2026-04-28). On a fresh install, the most-common failure
mode is "agent invocation explodes because ANTHROPIC_API_KEY is unset"
or "FRMR cache is missing because init wasn't run." Both produce
unfriendly tracebacks. `efterlev doctor` runs a series of cheap checks
and reports per-check pass/fail with remediation pointers, so users
catch the misconfiguration before the first agent run.

Checks are pure functions that return a `Check` dataclass. The
top-level `run_doctor_checks(target)` aggregates them. The CLI command
in `cli/main.py` wires it to typer and exits non-zero if any required
check fails.

Network reachability checks are intentionally NOT included — they're
flaky in CI sandboxes, add latency, and add a network dependency to a
diagnostic tool. The doctor inspects local state only.
"""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CheckStatus = Literal["pass", "warn", "fail"]


@dataclass(frozen=True)
class Check:
    """One diagnostic check's outcome.

    `severity`: a "fail" indicates the user can't run the agent
    pipeline — exit non-zero. A "warn" is a heads-up (e.g. Bedrock
    creds optional, FRMR cache slightly stale). A "pass" is the green
    case.
    """

    name: str
    status: CheckStatus
    detail: str
    hint: str | None = None


# Minimum supported Python — matches pyproject.toml's `requires-python`.
_MIN_PYTHON = (3, 10)


def check_python_version() -> Check:
    if sys.version_info[:2] >= _MIN_PYTHON:
        return Check(
            name="python_version",
            status="pass",
            detail=f"Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
        )
    cur_v = f"{sys.version_info[0]}.{sys.version_info[1]}"
    min_v = f"{_MIN_PYTHON[0]}.{_MIN_PYTHON[1]}"
    return Check(
        name="python_version",
        status="fail",
        detail=f"Python {cur_v} is below required {min_v}",
        hint="Upgrade Python to 3.10 or newer (we recommend 3.12).",
    )


def check_anthropic_api_key(*, configured_backend: str | None = None) -> Check:
    """Check ANTHROPIC_API_KEY presence and shape.

    Skipped when the workspace's configured backend is `bedrock` OR
    `claude_code` — the key is irrelevant on both paths and the warn was
    noise. (v0.1.175 / #381: claude_code added — the subscription path
    uses OAuth via `claude --print`, and efterlev actively STRIPS
    ANTHROPIC_API_KEY from that subprocess, so warning a subscription
    user about a missing/odd key read as "it still wants the API key
    even though I picked the subscription.") The shape check is
    conservative: real keys start with `sk-ant-` and are 100+ chars. We
    don't make a network call to validate the key here — that's the
    bedrock-side InvokeModel ping or the Anthropic-side first agent call.
    """
    if configured_backend in ("bedrock", "claude_code", "openai"):
        return Check(
            name="anthropic_api_key",
            status="pass",
            detail=f"skipped — workspace is configured for the {configured_backend} backend",
        )
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return Check(
            name="anthropic_api_key",
            status="warn",
            detail="ANTHROPIC_API_KEY is not set in the environment",
            hint=(
                "Set ANTHROPIC_API_KEY before running any `efterlev agent` "
                "command. Get a key at https://console.anthropic.com. "
                "Bedrock users can skip this — see `[bedrock]` in config.toml."
            ),
        )
    if not key.startswith("sk-ant-"):
        # Identify common confusables to give an actionable hint.
        if key.startswith("sk-proj-"):
            confusable = "an OpenAI project key (`sk-proj-...`)"
        elif key.startswith(("sk_live_", "sk_test_")):
            confusable = "a Stripe API key (`sk_live_*` / `sk_test_*`)"
        elif key.startswith("ghp_") or key.startswith("gho_"):
            confusable = "a GitHub token (`ghp_*` / `gho_*`)"
        else:
            confusable = "a different vendor's key or a leftover placeholder"
        # Escalate to fail when the workspace's configured backend is
        # `anthropic` — a wrong-shape key is essentially guaranteed to
        # 401 at LLM-call time. Pre-anthropic-config (or Bedrock-config),
        # stay at warn since the key is irrelevant or incidental.
        is_fail = configured_backend == "anthropic"
        return Check(
            name="anthropic_api_key",
            status="fail" if is_fail else "warn",
            detail=(
                f"ANTHROPIC_API_KEY is set but doesn't start with 'sk-ant-' "
                f"(length {len(key)}; looks like {confusable})"
            ),
            hint=(
                "Real Anthropic API keys start with `sk-ant-api03-`. "
                "Get one at https://console.anthropic.com, OR switch to "
                "the Bedrock backend in `.efterlev/config.toml`. "
                + (
                    "Workspace is configured for the Anthropic backend, so "
                    "this WILL 401 at agent-call time."
                    if is_fail
                    else "(Currently warn-only because the workspace backend "
                    "isn't anthropic-direct.)"
                )
            ),
        )
    return Check(
        name="anthropic_api_key",
        status="pass",
        detail=f"ANTHROPIC_API_KEY is set (sk-ant-…, length {len(key)})",
    )


def check_openai_api_key(*, configured_backend: str | None = None) -> Check:
    """Check OPENAI_API_KEY presence and shape — v0.1.211 parallel to the
    Anthropic check. Skipped when the workspace isn't configured for the
    OpenAI backend (the key is irrelevant on every other path). Real OpenAI
    keys start with `sk-` (often `sk-proj-…` for project-scoped keys); this
    is a shape check, not a network ping (a 401 surfaces at first agent call)."""
    if configured_backend != "openai":
        return Check(
            name="openai_api_key",
            status="pass",
            detail=f"skipped — workspace backend is {configured_backend or 'anthropic (default)'}",
        )
    from efterlev.shell.credentials import resolve_openai_api_key

    key = resolve_openai_api_key() or ""
    if not key:
        return Check(
            name="openai_api_key",
            status="fail",
            detail="OPENAI_API_KEY is not set (env var or credentials file)",
            hint=(
                "Set OPENAI_API_KEY before running any `efterlev agent` "
                "command, or run /setup in the efterlev shell. Get a key at "
                "https://platform.openai.com/api-keys. Recommended model: "
                "gpt-5.4-mini — see LIMITATIONS.md “OpenAI backend”."
            ),
        )
    if not key.startswith("sk-"):
        # Identify common confusables, mirroring the Anthropic check's hints.
        if key.startswith("sk-ant-"):
            confusable = "an Anthropic API key (`sk-ant-...`)"
        elif key.startswith(("sk_live_", "sk_test_")):
            confusable = "a Stripe API key (`sk_live_*` / `sk_test_*`)"
        elif key.startswith(("ghp_", "gho_")):
            confusable = "a GitHub token (`ghp_*` / `gho_*`)"
        else:
            confusable = "a different vendor's key or a leftover placeholder"
        return Check(
            name="openai_api_key",
            status="fail",
            detail=(
                f"OPENAI_API_KEY is set but doesn't start with 'sk-' "
                f"(length {len(key)}; looks like {confusable})"
            ),
            hint=(
                "Real OpenAI API keys start with `sk-` (often `sk-proj-…`). "
                "Get one at https://platform.openai.com/api-keys."
            ),
        )
    return Check(
        name="openai_api_key",
        status="pass",
        detail=f"OPENAI_API_KEY is set (sk-…, length {len(key)})",
    )


def check_efterlev_dir(target: Path) -> Check:
    """Check whether `.efterlev/` exists in the target directory."""
    efterlev_dir = target / ".efterlev"
    if efterlev_dir.is_dir():
        return Check(
            name="efterlev_dir",
            status="pass",
            detail=f".efterlev/ found at {efterlev_dir}",
        )
    return Check(
        name="efterlev_dir",
        status="warn",
        detail=f"No .efterlev/ at {target} — workspace not initialized",
        hint="Run `efterlev init` in the workspace before scanning or invoking agents.",
    )


_FRMR_CACHE_REL = Path(".efterlev/cache/frmr_document.json")
# Stale threshold: 90 days. The FRMR catalog is vendored, so the cache
# is the canonical local copy — if it's older than this, the user is
# almost certainly running against an outdated FedRAMP standard.
_FRMR_STALE_SECONDS = 90 * 24 * 60 * 60


def check_frmr_cache(target: Path) -> Check:
    """Check the FRMR-cache file is present and not impossibly stale."""
    cache = target / _FRMR_CACHE_REL
    if not cache.is_file():
        return Check(
            name="frmr_cache",
            status="warn",
            detail=f"FRMR cache missing at {cache}",
            hint=(
                "Run `efterlev init` to populate the FRMR cache. The "
                "cache contains the vendored FedRAMP catalog; agents "
                "and `efterlev scan` need it."
            ),
        )
    age_seconds = time.time() - cache.stat().st_mtime
    if age_seconds > _FRMR_STALE_SECONDS:
        days = int(age_seconds / 86400)
        return Check(
            name="frmr_cache",
            status="warn",
            detail=f"FRMR cache at {cache} is {days} days old",
            hint=(
                "Re-run `efterlev init --force` to refresh the FRMR "
                "cache from the vendored catalog (which itself ships "
                "with the installed efterlev package)."
            ),
        )
    return Check(
        name="frmr_cache",
        status="pass",
        detail=f"FRMR cache at {cache}",
    )


def _detect_installer() -> str:
    """Return 'uv' / 'pipx' / 'pip' / 'unknown' based on the install path.

    v0.1.9: doctor's Bedrock-extras hint pointed at `pipx inject efterlev
    boto3`, which is wrong for users who installed via `uv tool install
    efterlev`. The two installers manage isolated venvs at different
    locations, so the wrong installer's commands silently fail to find
    the package. This helper reads `sys.executable` and infers the
    installer from the venv path layout, then surfaces the correct
    fix-up command in the hint string.

    Detection rules (path substring match against `sys.executable`):
      - `/uv/tools/efterlev/` or `.local/share/uv/tools/efterlev/` → uv
      - `/pipx/venvs/efterlev/` or `.local/pipx/venvs/efterlev/` → pipx
      - everything else → 'pip' (or system, or container) — generic hint.
    """
    import sys

    exe = sys.executable.replace("\\", "/")
    if "/uv/tools/efterlev/" in exe or "/uv/tool/efterlev/" in exe:
        return "uv"
    if "/pipx/venvs/efterlev/" in exe:
        return "pipx"
    return "pip"


def _bedrock_install_hint() -> str:
    """Return the right install-fix command for the detected installer."""
    installer = _detect_installer()
    if installer == "uv":
        return (
            "If you don't use Bedrock, ignore this check. To install the "
            "Bedrock backend (you appear to have used `uv tool install`): "
            "`uv tool install --reinstall 'efterlev[bedrock]'`."
        )
    if installer == "pipx":
        return (
            "If you don't use Bedrock, ignore this check. To install the "
            "Bedrock backend: `pipx install 'efterlev[bedrock]'` (or "
            "`pipx inject efterlev boto3` if efterlev is already installed)."
        )
    return (
        "If you don't use Bedrock, ignore this check. To install the "
        "Bedrock backend: `pip install 'efterlev[bedrock]'` (or use "
        "the container image / your installer's equivalent)."
    )


def check_bedrock_credentials(
    *,
    configured_backend: str | None = None,
    configured_region: str | None = None,
    configured_model: str | None = None,
) -> Check:
    """Optional check: is the Bedrock LLM backend usable?

    Uses boto3's full credential resolution chain (env vars → shared
    credentials file → AWS_PROFILE → IMDS → SSO → container metadata),
    which is what the runtime actually consults. Earlier versions of
    this check only inspected env vars and false-warned on configs
    where `~/.aws/credentials` or an SSO session was already valid
    (real first-run report 2026-04-30).

    When `configured_backend == "bedrock"`, additionally validates the
    configured model end-to-end with a 1-token `InvokeModel` ping —
    catches stale defaults, missing inference profiles, expired creds,
    and access-denied scenarios in the diagnostic phase before users
    spend money on a doomed agent run. The ping is intentionally
    minimal (`max_tokens=1`, throwaway prompt) so the cost is fractions
    of a cent.
    """
    try:
        import boto3
        from botocore.exceptions import (  # type: ignore[import-untyped]
            BotoCoreError,
            ClientError,
            NoCredentialsError,
        )
    except ImportError:
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail="boto3 not installed (Bedrock backend unavailable)",
            hint=_bedrock_install_hint(),
        )

    # boto3's full credential chain — env, shared file, AWS_PROFILE,
    # IMDS, SSO, container creds. Matches what the runtime client uses.
    try:
        session = boto3.Session()
        creds = session.get_credentials()
    except Exception as e:  # pragma: no cover - boto3 setup edge cases
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail=f"boto3 session init failed: {e}",
            hint="Check `aws configure` or your AWS_PROFILE / SSO setup.",
        )

    # v0.1.8: region resolution mirrors boto3's own chain — workspace
    # config first, then env, then `~/.aws/config` profile region, then
    # AWS_DEFAULT_REGION. Pre-v0.1.8 only checked env vars and false-
    # warned on accounts where `aws configure set region us-east-1` was
    # the only place region was set; runtime worked but the doctor
    # screamed. boto3's `Session.region_name` resolves the full chain.
    region = (
        configured_region
        or os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or session.region_name
    )

    if creds is None:
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail="No AWS credentials resolvable from any source (Bedrock backend unavailable)",
            hint=(
                "If you don't use Bedrock, ignore this check. To enable "
                "Bedrock: run `aws configure` (writes to ~/.aws/credentials), "
                "or set AWS_PROFILE, or export AWS_ACCESS_KEY_ID + "
                "AWS_SECRET_ACCESS_KEY. Then set [llm].backend = 'bedrock' "
                "in .efterlev/config.toml."
            ),
        )

    if not region:
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail="AWS credentials resolved but no region configured",
            hint=(
                "Set AWS_REGION (or AWS_DEFAULT_REGION), or `aws configure "
                "set region us-east-1`, so Bedrock knows where to call. "
                "GovCloud customers: use `us-gov-west-1`."
            ),
        )

    # Skip the InvokeModel ping unless the workspace is actually configured
    # for Bedrock. On Anthropic-backend workspaces we just want to confirm
    # that Bedrock COULD be used without spending API budget.
    if configured_backend != "bedrock" or not configured_model:
        return Check(
            name="bedrock_credentials",
            status="pass",
            detail=(
                f"AWS credentials resolved + region {region} configured (Bedrock backend usable)"
            ),
        )

    # End-to-end ping: 1 token, throwaway prompt. Catches stale model
    # defaults, missing inference-profile access, and credential lifetimes
    # before the first agent run.
    try:
        from botocore.config import Config

        client = session.client(
            "bedrock-runtime",
            region_name=region,
            config=Config(read_timeout=30, connect_timeout=10, retries={"max_attempts": 1}),
        )
        client.converse(
            modelId=configured_model,
            messages=[{"role": "user", "content": [{"text": "ping"}]}],
            inferenceConfig={"maxTokens": 1},
        )
    except NoCredentialsError:
        return Check(
            name="bedrock_credentials",
            status="fail",
            detail="boto3 reported credentials, but Bedrock rejected them",
            hint="Refresh credentials (e.g. `aws sso login`) and re-run.",
        )
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "?")
        msg = e.response.get("Error", {}).get("Message", str(e))
        if code in ("AccessDeniedException", "UnauthorizedException"):
            return Check(
                name="bedrock_credentials",
                status="fail",
                detail=f"Bedrock denied access to {configured_model}: {msg}",
                hint=(
                    "Request access to the model in the Bedrock console "
                    "(console.aws.amazon.com/bedrock → Model access), or "
                    "pick a different `model` in .efterlev/config.toml."
                ),
            )
        if code in ("ResourceNotFoundException", "ValidationException"):
            return Check(
                name="bedrock_credentials",
                status="fail",
                detail=f"Configured model {configured_model!r} is not callable: {msg}",
                hint=(
                    "Run `aws bedrock list-inference-profiles --type-equals "
                    "SYSTEM_DEFINED --region <region>` and pick a current "
                    "Anthropic profile ARN. Update [llm].model in "
                    ".efterlev/config.toml."
                ),
            )
        # Throttling / 5xx — credentials and model are fine, just a transient
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail=f"Bedrock ping returned {code}: {msg}",
            hint="Retry in a moment; credentials and model look OK.",
        )
    except BotoCoreError as e:
        return Check(
            name="bedrock_credentials",
            status="warn",
            detail=f"Bedrock ping connection error: {e}",
            hint="Network reachability to Bedrock failed; check VPC endpoints / proxy config.",
        )

    return Check(
        name="bedrock_credentials",
        status="pass",
        detail=(
            f"InvokeModel ping succeeded against {configured_model} in {region} "
            "(creds + model verified end-to-end)"
        ),
    )


def check_boundary_declared(target: Path) -> Check:
    """Warn when `.efterlev/config.toml` has both `[boundary].include` and
    `[boundary].exclude` empty.

    Boundary scope is the FedRAMP authorization-boundary declaration: which
    paths in this workspace are in-scope vs out-of-scope. With both lists
    empty, every Evidence record is marked `boundary_undeclared` and flows
    through every classification unfiltered. That's a real semantic gap for
    a 3PAO-shaped artifact — a defensible posture statement names which
    resources are inside the boundary. The gap-report header already shows
    `workspace_boundary_state: boundary_undeclared`, but earlier doctor
    versions reported 5 pass / 0 warn / 0 fail and never surfaced it.

    The check runs on every workspace; users explicitly running outside a
    formal authorization boundary (e.g. internal compliance dogfood) can
    safely ignore the warn — it's informational, not blocking.
    """
    config_path = target / ".efterlev" / "config.toml"
    if not config_path.is_file():
        # No config to read — `check_efterlev_dir` already warns about this.
        return Check(
            name="boundary_declared",
            status="pass",
            detail="skipped — no `.efterlev/config.toml` to read",
        )
    try:
        import tomllib

        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except Exception as e:
        return Check(
            name="boundary_declared",
            status="warn",
            detail=f"could not parse `.efterlev/config.toml`: {e}",
            hint="Re-run `efterlev init --force` to regenerate the config.",
        )
    boundary = data.get("boundary") if isinstance(data, dict) else None
    include: list[object] = []
    exclude: list[object] = []
    if isinstance(boundary, dict):
        raw_include = boundary.get("include")
        raw_exclude = boundary.get("exclude")
        if isinstance(raw_include, list):
            include = raw_include
        if isinstance(raw_exclude, list):
            exclude = raw_exclude
    if include or exclude:
        return Check(
            name="boundary_declared",
            status="pass",
            detail=(
                f"boundary scope declared "
                f"(include={len(include)} pattern(s), exclude={len(exclude)} pattern(s))"
            ),
        )
    return Check(
        name="boundary_declared",
        status="warn",
        detail="boundary scope is undeclared — every finding flows through unfiltered",
        hint=(
            "Declare scope with `efterlev boundary set` using gitignore-style "
            "patterns matching YOUR in-scope paths — e.g. "
            "`--include 'infra/**' --include '.github/workflows/**'` (workflows "
            "live outside infra/, so include them explicitly or their findings "
            "fall out_of_boundary). Until then, the gap report's "
            "`workspace_boundary_state` is `boundary_undeclared` — fine for "
            "internal review, not appropriate for a 3PAO-shaped artifact."
        ),
    )


def _read_configured_backend(target: Path) -> tuple[str | None, str | None, str | None]:
    """Best-effort read of `[llm]` settings from `.efterlev/config.toml`.

    Returns (backend, region, model) — any missing field is None. Failures
    parsing the file return all-None silently; the doctor checks fall back
    to env-var inspection in that case.
    """
    config_path = target / ".efterlev" / "config.toml"
    if not config_path.is_file():
        return (None, None, None)
    try:
        import tomllib

        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return (None, None, None)
    llm = data.get("llm", {}) if isinstance(data, dict) else {}
    if not isinstance(llm, dict):
        return (None, None, None)
    backend = llm.get("backend") if isinstance(llm.get("backend"), str) else None
    region = llm.get("region") if isinstance(llm.get("region"), str) else None
    model = llm.get("model") if isinstance(llm.get("model"), str) else None
    return (backend, region, model)


def _efterlev_path_binaries() -> list[str]:
    """Every `efterlev` binary discoverable on PATH, deduped by resolved target.

    Symlink dedup avoids the common false-positive where /usr/local/bin
    is itself a symlink to /opt/bin (or, on macOS, /tmp → /private/tmp).
    """
    seen: list[str] = []
    seen_resolved: set[str] = set()
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        candidate = Path(entry) / "efterlev"
        if not candidate.exists():
            continue
        try:
            resolved = str(candidate.resolve())
        except OSError:
            resolved = str(candidate)
        if resolved in seen_resolved:
            continue
        seen_resolved.add(resolved)
        seen.append(str(candidate))
    return seen


def _efterlev_manager_installs() -> list[tuple[str, str, str]]:
    """Detected parallel installs by package-manager metadata location.

    H1 (v0.1.15): the v0.1.14 install_uniqueness check walked PATH only,
    which missed the dominant footgun — pipx and uv tool both want to
    own the `~/.local/bin/efterlev` symlink, so only one of them ends
    up on PATH even though both have a venv. The user runs
    `pipx upgrade efterlev`, sees "upgraded", then `efterlev --version`
    returns the OLD version because the PATH symlink belongs to uv tool
    (or vice versa). To catch this, walk known manager-metadata dirs
    rather than (only) PATH.

    Returns a list of `(manager, install_path, uninstall_command)` tuples
    for each manager that has efterlev installed. Empty list = no
    detected manager-managed installs (the user may still have a
    custom path-based install — PATH walking covers that).
    """
    home = Path.home()
    detected: list[tuple[str, str, str]] = []

    pipx_venv = home / ".local" / "pipx" / "venvs" / "efterlev"
    if pipx_venv.is_dir():
        detected.append(("pipx", str(pipx_venv), "pipx uninstall efterlev"))

    uv_tool = home / ".local" / "share" / "uv" / "tools" / "efterlev"
    if uv_tool.is_dir():
        detected.append(("uv tool", str(uv_tool), "uv tool uninstall efterlev"))

    # User pip installs land in different paths per OS. Glob both shapes;
    # the package dir's name is `efterlev` (no version suffix), so we
    # look for `<site-packages>/efterlev/__init__.py` to confirm it's
    # actually installed there (not just an `efterlev-*.dist-info`).
    user_pip_globs = [
        home / "Library" / "Python",  # macOS user pip
        home / ".local" / "lib",  # linux user pip
    ]
    for base in user_pip_globs:
        if not base.is_dir():
            continue
        for sp in base.glob("*/lib/python*/site-packages/efterlev/__init__.py"):
            detected.append(("user pip", str(sp.parent), "pip uninstall efterlev"))
        for sp in base.glob("python*/site-packages/efterlev/__init__.py"):
            detected.append(("user pip", str(sp.parent), "pip uninstall efterlev"))

    return detected


def check_install_uniqueness() -> Check:
    """Detect multiple `efterlev` installations on the host.

    Combines two detection strategies:
      1. PATH walk — catches the `/usr/local/bin/efterlev` +
         `~/.local/bin/efterlev` parallel-install case (G2, v0.1.14).
      2. Manager-metadata walk — catches the dominant footgun where
         pipx and uv tool both install but only one wins the
         `~/.local/bin/efterlev` symlink, so PATH only sees one (H1,
         v0.1.15). Without this, `pipx upgrade efterlev` reports
         success while `efterlev --version` keeps returning the older
         install owned by uv tool (or vice versa).

    Warns when ≥2 distinct installations are detected by either
    strategy. PATH installs that overlap with a manager dir aren't
    double-counted (the manager dir is the canonical location).
    """
    path_binaries = _efterlev_path_binaries()
    manager_installs = _efterlev_manager_installs()

    # A PATH binary that resolves into a known manager dir is the same
    # install — don't double-count.
    manager_resolved = {Path(p).resolve() for _, p, _ in manager_installs}

    def _under_manager(binary: str) -> bool:
        try:
            resolved = Path(binary).resolve()
        except OSError:
            return False
        return any(str(resolved).startswith(str(mgr)) for mgr in manager_resolved)

    extra_path_binaries = [b for b in path_binaries if not _under_manager(b)]
    total = len(manager_installs) + len(extra_path_binaries)

    if total <= 1:
        # Describe what we found, even on the green case — useful diagnostic
        # for a user grepping for "where IS efterlev installed?".
        if manager_installs:
            mgr, _path, _uninst = manager_installs[0]
            detail = f"single install detected (managed by {mgr})"
        elif path_binaries:
            detail = f"single `efterlev` on PATH ({path_binaries[0]})"
        else:
            detail = "no `efterlev` install detected (running via `python -m`?)"
        return Check(name="install_uniqueness", status="pass", detail=detail)

    lines: list[str] = []
    for mgr, path, _uninst in manager_installs:
        lines.append(f"{mgr}: {path}")
    for b in extra_path_binaries:
        lines.append(f"PATH-only: {b}")
    listing = "; ".join(lines)
    winner = path_binaries[0] if path_binaries else "(no binary on PATH)"
    uninstall_hints = " / ".join(sorted({uninst for _, _, uninst in manager_installs}))
    return Check(
        name="install_uniqueness",
        status="warn",
        detail=f"{total} parallel `efterlev` installs detected: {listing}",
        hint=(
            f"PATH winner: {winner}. With multiple managers active, "
            f"`pipx upgrade` / `uv tool upgrade` against a non-winner "
            f"silently leaves you on the older install (the PATH symlink "
            f"is owned by whichever manager won the race). Prune the "
            f"unused install(s) with: {uninstall_hints or 'the matching uninstall command'}."
        ),
    )


def check_cloudformation_templates(target: Path) -> Check:
    """Detect CloudFormation YAML/JSON templates and confirm scan reaches them.

    Scope: walk the target tree once, looking at .yaml/.yml/.json files
    under common IaC directory names (`infra/`, `cloudformation/`,
    `cfn/`, top level). Sniff the first 4KB for `AWSTemplateFormatVersion`
    or `Resources:` (the same heuristic the parser uses; matches
    `src/efterlev/cloudformation/parser.py:_looks_like_cfn`).

    As of v0.1.99 (CFN graduation arc step 3), CFN scanning is default-on.
    This check now just informs the user that CFN templates are detected
    and will be scanned by default. The `--allow-cfn` flag is deprecated
    (still functional with a warning, removed in v0.2.0).

    CFN coverage at v0.1.98: 60/60 detector type-coverage (v0.1.96) +
    44/44 = 100% precision/recall across 2 maintainer-validated fixtures
    (csp-starter-cfn v0.1.81 + aws-vpc-cfn v0.1.98).
    """
    candidate_dirs = [target, target / "infra", target / "cloudformation", target / "cfn"]
    found_templates: list[Path] = []
    for d in candidate_dirs:
        if not d.is_dir():
            continue
        for ext in ("*.yaml", "*.yml", "*.json"):
            for path in d.rglob(ext):
                # Skip noise dirs: .efterlev/, .git/, node_modules/, .venv/.
                if any(part.startswith(".") for part in path.relative_to(target).parts[:-1]):
                    continue
                if any(part in {"node_modules", "venv"} for part in path.parts):
                    continue
                try:
                    head = path.read_text(encoding="utf-8", errors="replace")[:4096]
                except OSError:
                    continue
                if "AWSTemplateFormatVersion" in head or "Resources:" in head:
                    found_templates.append(path)
                    if len(found_templates) >= 5:
                        break
            if len(found_templates) >= 5:
                break
        if len(found_templates) >= 5:
            break

    if not found_templates:
        return Check(
            name="cloudformation_templates",
            status="pass",
            detail="no CFN templates detected (TF-only or non-IaC repo)",
        )

    rel_paths = [str(p.relative_to(target)) for p in found_templates[:3]]
    sample = ", ".join(rel_paths)
    if len(found_templates) > 3:
        sample += f" (+{len(found_templates) - 3} more)"

    return Check(
        name="cloudformation_templates",
        status="pass",
        detail=(
            f"{len(found_templates)} CFN template(s) detected: {sample}; "
            f"will be scanned by default (CFN graduated v0.1.99)"
        ),
    )


def run_doctor_checks(target: Path) -> list[Check]:
    """Run every doctor check and return the results in display order.

    Order: Python (foundational), .efterlev workspace state, FRMR cache
    (init artifact), API keys (agent invocation), Bedrock (optional),
    boundary declared, CFN templates detected.

    The api-key and bedrock checks are config-aware: if `.efterlev/
    config.toml` declares `backend = "bedrock"`, the anthropic-key
    check skips, and the bedrock check additionally pings InvokeModel
    against the configured model (1-token round-trip).
    """
    backend, region, model = _read_configured_backend(target)
    return [
        check_python_version(),
        check_install_uniqueness(),
        check_efterlev_dir(target),
        check_frmr_cache(target),
        check_anthropic_api_key(configured_backend=backend),
        check_openai_api_key(configured_backend=backend),
        check_bedrock_credentials(
            configured_backend=backend,
            configured_region=region,
            configured_model=model,
        ),
        check_boundary_declared(target),
        check_cloudformation_templates(target),
    ]


def has_failures(checks: list[Check]) -> bool:
    """True if any check is `fail` (the gate for non-zero exit). Warns
    don't block — they're informational."""
    return any(c.status == "fail" for c in checks)
