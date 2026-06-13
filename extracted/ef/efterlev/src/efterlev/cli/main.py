"""Efterlev CLI entry point.

The `app` Typer instance is the package's script entry (declared in
`pyproject.toml` as `efterlev = "efterlev.cli.main:app"`). Every subcommand
is a stub that raises `NotImplementedError` naming which build phase will
implement it. The CLI's *shape* is stable from Phase 0 onward; callers and
downstream scripts can depend on command and option names without waiting
for behavior to land.

Implementation phases (see `docs/dual_horizon_plan.md` §2.3):

  Phase 0  scaffold this CLI (done)
  Phase 1  models + primitives + provenance store/walker
  Phase 2  catalog loaders (FRMR + 800-53), `init`, first detector, `scan`
  Phase 3  Gap / Documentation / Remediation agents, FRMR generator
  Phase 4  MCP server wiring, demo polish
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# v0.1.150 / #355: macOS TCC (Transparency / Consent / Control) blocks
# Terminal from reading ~/Documents, ~/Desktop, ~/Downloads, and a few
# other protected dirs unless the user has explicitly granted Full Disk
# Access. The first thing typer/click does on a `efterlev <cmd>` invocation
# is call os.access(cwd) for any `Path("." )` option — that raises
# `click.BadParameter: Path '.' is not readable`. Then typer tries to
# pretty-print the error by importing rich, whose __init__.py calls
# `os.getcwd()`, which raises PermissionError, which then crashes the
# excepthook itself.
#
# We guard at module load (before typer / rich import in this file's
# downstream import chain) so the user gets one clear actionable
# message instead of two stacked tracebacks.
try:
    os.getcwd()
except (FileNotFoundError, PermissionError) as _cwd_err:
    sys.stderr.write(
        "efterlev: cannot read the current directory.\n"
        f"  raw error: {_cwd_err!s}\n"
        "\n"
        "On macOS this is usually a TCC permission issue: Terminal lacks\n"
        "access to one of the protected dirs (~/Documents, ~/Desktop,\n"
        "~/Downloads, etc.). Fix one of:\n"
        "\n"
        "  1. Grant Terminal Full Disk Access:\n"
        "       System Settings → Privacy & Security → Full Disk Access\n"
        "       → toggle on for Terminal (or iTerm2 / Warp / your shell app).\n"
        "       Restart the terminal.\n"
        "\n"
        "  2. Or move your workspace outside the protected dirs:\n"
        "       mv ~/Documents/<workspace> ~/<workspace>\n"
        "       cd ~/<workspace> && efterlev shell\n"
    )
    sys.exit(2)
from typing import Any

import typer

from efterlev import __version__
from efterlev.cli.friendly_errors import friendly_llm_error_handler
from efterlev.paths import iter_report_dirs as _iter_report_dirs
from efterlev.paths import poam_dir as _poam_dir
from efterlev.paths import reports_dir as _reports_dir

# Force stdout/stderr to UTF-8 on Windows. The default Windows console
# encoding is cp1252, which can't encode characters like ⚠ (U+26A0)
# that the CLI uses in user-facing scan-result messages. Without this,
# `efterlev scan` against any workspace that triggers a warning path
# raises `UnicodeEncodeError: 'charmap' codec can't encode character`
# and the whole command crashes.
#
# v0.1.26's release-smoke matrix Windows-2022 cell hit this when scan
# emitted "module calls detected" or "files skipped due to parse
# error" warnings. v0.1.27 fixes it for real by reconfiguring stdio
# at CLI import time. POSIX is unaffected (default is already utf-8).
#
# `reconfigure(encoding="utf-8")` is supported on TextIOWrapper since
# Python 3.7. The hasattr guard handles the case where stdout/stderr
# have been redirected to a non-TextIOWrapper (e.g., a custom pipe in
# subprocess capture); in that case the redirector is responsible for
# its own encoding.
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

app = typer.Typer(
    name="efterlev",
    help="Repo-native, agent-first compliance scanner for FedRAMP 20x and DoD IL.",
    add_completion=False,
)

agent_app = typer.Typer(
    name="agent",
    help="Run a reasoning agent (Gap, Documentation, or Remediation).",
    no_args_is_help=True,
)
app.add_typer(agent_app, name="agent")

provenance_app = typer.Typer(
    name="provenance",
    help="Inspect the local provenance graph.",
    no_args_is_help=True,
)
app.add_typer(provenance_app, name="provenance")

mcp_app = typer.Typer(
    name="mcp",
    help="Expose Efterlev's primitives over an MCP stdio server.",
    no_args_is_help=True,
)
app.add_typer(mcp_app, name="mcp")

redaction_app = typer.Typer(
    name="redaction",
    help="Inspect the LLM-prompt redaction audit log.",
    no_args_is_help=True,
)
app.add_typer(redaction_app, name="redaction")

detectors_app = typer.Typer(
    name="detectors",
    help="Inspect the registered detector library.",
    no_args_is_help=True,
)
app.add_typer(detectors_app, name="detectors")

boundary_app = typer.Typer(
    name="boundary",
    help="Declare and inspect the FedRAMP authorization boundary scope.",
    no_args_is_help=True,
)
app.add_typer(boundary_app, name="boundary")

report_app = typer.Typer(
    name="report",
    help="Operate on prior gap-report artifacts (diff, etc.).",
    no_args_is_help=True,
)
app.add_typer(report_app, name="report")

# v0.1.171 / #377: `scope` subcommand for shared-responsibility /
# inherited-control declaration (declare / show / clear / apply).
scope_app = typer.Typer(
    name="scope",
    help="Declare CSP-inherited controls (shared responsibility).",
    no_args_is_help=True,
)
app.add_typer(scope_app, name="scope")


@scope_app.command("declare")
def scope_declare(
    profile: str | None = typer.Option(
        None,
        "--profile",
        help="Built-in inheritance profile (e.g. aws-serverless). A STARTER list to review.",
    ),
    ksi: list[str] = typer.Option(
        [],
        "--ksi",
        help="Declare a specific KSI id as inherited (repeatable; with or without --profile).",
    ),
    target: Path = typer.Option(Path("."), "--target", help="Workspace root."),
) -> None:
    """Declare KSIs as CSP-inherited under the shared-responsibility model.

    Writes `[scope] inherited = [...]` to config. This is a declaration
    only — run `efterlev scan` then `efterlev scope apply` to cross-check
    against evidence and record the inherited status.
    """
    from efterlev.cli.scope_cli import run_scope_declare

    raise typer.Exit(code=run_scope_declare(target, profile=profile, ksis=list(ksi)))


@scope_app.command("show")
def scope_show(
    target: Path = typer.Option(Path("."), "--target", help="Workspace root."),
) -> None:
    """Show the current inherited-control declaration + per-KSI rationale."""
    from efterlev.cli.scope_cli import run_scope_show

    raise typer.Exit(code=run_scope_show(target))


@scope_app.command("clear")
def scope_clear(
    target: Path = typer.Option(Path("."), "--target", help="Workspace root."),
) -> None:
    """Remove the inherited-control declaration from config."""
    from efterlev.cli.scope_cli import run_scope_clear

    raise typer.Exit(code=run_scope_clear(target))


@scope_app.command("apply")
def scope_apply(
    target: Path = typer.Option(Path("."), "--target", help="Workspace root."),
) -> None:
    """Cross-check declared inherited KSIs against evidence + record status.

    Deterministic. For each declared KSI with no contradicting scanner
    evidence, writes an `implemented (inherited)` claim + an
    inheritance-basis evidence record (both DRAFT-marked). KSIs the
    scanner found customer-side evidence for are flagged, not marked.
    Requires a prior `efterlev scan`.
    """
    from efterlev.cli.scope_cli import run_scope_apply

    raise typer.Exit(code=run_scope_apply(target))


# OSCAL output arc step 1 (v0.1.105): subcommand for `oscal export --kind poam`.
# Future kinds (component-definition, partial-ssp) ship behind the same
# `--kind` flag.
from efterlev.cli.oscal import oscal_app  # noqa: E402

app.add_typer(oscal_app, name="oscal")

manifests_app = typer.Typer(
    name="manifests",
    help="Operate on Evidence Manifests (init starter-pack, validate, list).",
    no_args_is_help=True,
)
app.add_typer(manifests_app, name="manifests")


def _stub(phase: str, command: str) -> None:
    """Raise a stub error with a clear phase pointer.

    Used by every Phase-0 subcommand callback so the CLI shape is real but
    behavior is deferred to the phase that will implement it. See the module
    docstring for the phase map.
    """
    raise NotImplementedError(
        f"`efterlev {command}` is a stub in v{__version__}; "
        f"scheduled for Phase {phase}. See docs/dual_horizon_plan.md §2.3."
    )


def _probe_bedrock_default_model(region: str | None) -> str | None:
    """Discover the latest Anthropic Opus US cross-region inference profile.

    Thin wrapper over `_probe_bedrock_for_family` filtered to Opus —
    used at `init` time when the Bedrock backend is selected without
    an explicit `--llm-model`. Caller falls back to the hardcoded
    DEFAULT_BEDROCK_MODEL on None.

    Why probe at init time: Efterlev's hardcoded default
    (`us.anthropic.claude-opus-4-7-v1:0`) is unavailable in many AWS
    accounts/regions. Probing picks whatever the user actually has
    access to right now; first-run failure mode avoided. (Surfaced in
    a real first-run Bedrock report on 2026-04-30.)

    Why Opus: matches the per-agent default for Gap and Remediation
    (best classification quality). Sonnet/Haiku users override via
    `--llm-model`. The underlying helper supports all three families
    (`opus`, `sonnet`, `haiku`) for future per-agent Bedrock-default
    work — see CLAUDE.md "Path forward" Tier 2.
    """
    return _probe_bedrock_for_family(region, "opus")


# Match Anthropic-on-Bedrock inference profile IDs and capture a
# version tuple. Three legacy/current naming patterns are in production:
#
#   1. claude-{family}-{major}-{minor}(-{date})?(-v{rev})?
#      e.g. `claude-opus-4-7-v1:0`, `claude-opus-4-1-20250805-v1:0`,
#           `claude-haiku-4-5-20251001-v1:0`
#
#   2. claude-{family}-{major}(-{date})?(-v{rev})?
#      e.g. `claude-opus-4-20250514-v1:0`, `claude-sonnet-4-20250514-v1:0`
#
#   3. claude-{N}(-{minor})?-{family}(-{date})?(-v{rev})?
#      e.g. `claude-3-opus-20240229-v1:0`, `claude-3-5-sonnet-20241022-v2:0`,
#           `claude-3-7-sonnet-20250219-v1:0`
#
# The lexical sort the v0.1.0-v0.1.35 implementation used got the
# `4-1-20250805` vs `4-20250514` ordering wrong (picks Opus 4.0 over
# Opus 4.1 because `4-2…` lexically outranks `4-1…`). v0.1.36 parses
# a (major, minor, date_int, rev) tuple per profile and sorts by that.
_BEDROCK_VERSION_NEW_RE = re.compile(
    r"claude-(?:opus|sonnet|haiku)-"
    r"(?P<major>\d+)"
    # Minor is 1-2 digits but MUST NOT be the leading digits of a date.
    # `-(\d{1,2})(?=-|$)` requires either `-` or end-of-string after the
    # minor, which fails on `claude-opus-4-20250514` (the `2` of `20250514`
    # is followed by more digits, not `-`). v0.1.36 fix: pre-v0.1.36 the
    # greedy lexical-sort path picked Opus 4.0 (which had minor=20 parsed
    # off the date) over the actual Opus 4.1.
    r"(?:-(?P<minor>\d{1,2})(?=-|$))?"
    r"(?:-(?P<date>\d{8}))?"
    r"(?:-v(?P<rev>\d+))?"
)
_BEDROCK_VERSION_LEGACY_RE = re.compile(
    # Legacy `claude-{N}-{M}-{family}` shape: minor MUST be 1-2 digits
    # and MUST NOT be the leading digits of a date (same fix as above).
    r"claude-(?P<major>\d+)(?:-(?P<minor>\d{1,2})(?=-|$))?-(?:opus|sonnet|haiku)"
    r"(?:-(?P<date>\d{8}))?"
    r"(?:-v(?P<rev>\d+))?"
)


def _parse_bedrock_anthropic_version(profile_id: str) -> tuple[int, int, int, int] | None:
    """Parse a (major, minor, date_int, rev) version tuple from a Bedrock
    inference profile ID. Returns None if the ID matches no known shape.

    Sorting these tuples descending puts the LATEST model first regardless
    of digit-count quirks (e.g. `opus-4-1-20250805` beats `opus-4-20250514`
    even though lexically the second outranks the first).
    """
    pid = profile_id.lower()
    # Try the new (`-{family}-{N}-{M}`) shape first; v0.1.36+ Anthropic IDs
    # are predominantly this form.
    m = _BEDROCK_VERSION_NEW_RE.search(pid)
    if m:
        return _parsed_version_tuple(m)
    # Fall back to the legacy (`-{N}-{family}`) shape — Claude 3 / 3.5 / 3.7.
    m = _BEDROCK_VERSION_LEGACY_RE.search(pid)
    if m:
        return _parsed_version_tuple(m)
    return None


def _parsed_version_tuple(m: re.Match[str]) -> tuple[int, int, int, int]:
    major = int(m.group("major"))
    minor = int(m.group("minor")) if m.group("minor") else 0
    date = int(m.group("date")) if m.group("date") else 0
    rev = int(m.group("rev")) if m.group("rev") else 1
    return (major, minor, date, rev)


def _probe_bedrock_for_family(region: str | None, family: str) -> str | None:
    """Discover the best Anthropic model ID for the requested family.

    v0.1.39 behavior: probes BOTH inference profiles AND foundation models,
    consults each candidate's lifecycle status, and falls back to direct
    foundation-model invocation when no usable cross-region profile exists.

    Selection logic:

    1. List `SYSTEM_DEFINED` inference profiles. Filter to `us.*` (excludes
       `eu.*` / `apac.*` / `global.*` for FedRAMP boundary conservatism)
       + Anthropic + family.
    2. List Anthropic foundation models. Build a lifecycle map.
    3. For each `us.*` profile candidate, look up its underlying foundation
       model in the lifecycle map. SKIP if `lifecycle=LEGACY` — calls to
       these succeed-then-fail at agent runtime with AccessDenied. Surfaced
       by a real first-run fixture in v0.1.38 deep-test where the only
       `us.*` Opus profile in the account pointed at the Legacy
       Opus 4 (20250514) and the auto-pick blew up the gap call.
    4. For each ACTIVE foundation model not already covered by a kept
       profile, ALSO add it as a direct-invocation candidate. This closes
       the gap where AWS hasn't yet shipped a `us.*` cross-region profile
       for newer models in the account's region.
    5. Sort candidates by `(version_tuple, prefers_profile, id)` reverse —
       cross-region profile beats direct foundation model when the version
       ties. Cross-region routing has better availability characteristics
       than direct invocation.

    Why `us.*` only — exclude `eu.*`, `apac.*`, AND `global.*`:
    `eu.` / `apac.` route to non-US regions; `global.*` forfeits
    US-region geographic guarantees that FedRAMP boundary documentation
    may depend on. Users who explicitly want `global.*` can pass
    `--llm-model=global.anthropic.claude-...` directly.

    Returns None on any failure (boto3 missing, both API calls denied,
    no matching ACTIVE candidates). Caller falls back to the hardcoded
    DEFAULT_BEDROCK_MODEL on None.
    """
    if not region:
        return None
    if family not in {"opus", "sonnet", "haiku"}:
        return None
    try:
        import boto3
    except ImportError:
        return None
    try:
        client = boto3.Session().client("bedrock", region_name=region)
        profiles_resp = client.list_inference_profiles(typeEquals="SYSTEM_DEFINED", maxResults=200)
    except Exception:
        return None

    # Foundation models are best-effort: if listing fails (e.g. permission
    # missing on bedrock:ListFoundationModels but not ListInferenceProfiles),
    # continue without lifecycle data. Profiles still get probed; we just
    # can't filter LEGACY-backed ones. Better degraded behavior than total
    # failure.
    try:
        models_resp = client.list_foundation_models(byProvider="anthropic")
    except Exception:
        models_resp = {"modelSummaries": []}

    lifecycle_by_model_id: dict[str, str] = {}
    for m in models_resp.get("modelSummaries", []):
        mid = m.get("modelId") or ""
        status = (m.get("modelLifecycle") or {}).get("status") or ""
        if mid:
            lifecycle_by_model_id[mid] = status

    def _underlying_model_ids(profile: dict[str, Any]) -> list[str]:
        ids: list[str] = []
        for m in profile.get("models", []) or []:
            arn = m.get("modelArn") or ""
            # arn = `arn:aws:bedrock:<region>::foundation-model/<model_id>`
            if "/" in arn:
                ids.append(arn.split("/", 1)[-1])
        return ids

    # Profile preference encoded as 1 (profile) > 0 (foundation model) so a
    # reverse sort puts profiles ahead of equally-versioned direct-invocation
    # candidates.
    candidates: list[tuple[tuple[int, int, int, int], int, str]] = []
    profile_covered_models: set[str] = set()

    for p in profiles_resp.get("inferenceProfileSummaries", []):
        pid = p.get("inferenceProfileId") or ""
        if not pid.startswith("us."):
            continue
        pid_lower = pid.lower()
        if "anthropic" not in pid_lower:
            continue
        if family not in pid_lower:
            continue
        models = p.get("models", []) or []
        if models and not any("anthropic" in (m.get("modelArn") or "").lower() for m in models):
            continue
        underlying = _underlying_model_ids(p)
        # v0.1.39: skip profiles backed by a LEGACY foundation model.
        if any(lifecycle_by_model_id.get(mid) == "LEGACY" for mid in underlying):
            continue
        version = _parse_bedrock_anthropic_version(pid)
        if version is None:
            continue
        candidates.append((version, 1, pid))
        profile_covered_models.update(underlying)

    # v0.1.39: foundation-model fallback. Add ACTIVE foundation models that
    # aren't already represented by a kept profile. This rescues accounts
    # where AWS hasn't yet stood up a `us.*` cross-region profile for a
    # newer model.
    #
    # v0.1.40: ALSO require `inferenceTypesSupported` to contain `ON_DEMAND`.
    # `lifecycle=ACTIVE` does NOT imply directly invokable — newer Anthropic
    # models on Bedrock (Opus 4.x family) are inference-profile-only, and
    # AWS rejects direct invocation with `ValidationException: Invocation of
    # model ID X with on-demand throughput isn't supported. Retry your
    # request with the ID or ARN of an inference profile that contains this
    # model.` Surfaced by the v0.1.39 deep-test re-validation against a real
    # account where the probe correctly skipped the LEGACY profile, fell
    # back to anthropic.claude-opus-4-7, and then the gap call died on
    # this contract. The `inferenceTypesSupported` field is the documented
    # signal AWS publishes for this; foundation models requiring an
    # inference profile have it set to `['INFERENCE_PROFILE']` (no
    # `ON_DEMAND`).
    for m in models_resp.get("modelSummaries", []):
        mid = m.get("modelId") or ""
        if not mid.startswith("anthropic."):
            continue
        if family not in mid.lower():
            continue
        if (m.get("modelLifecycle") or {}).get("status") != "ACTIVE":
            continue
        if "ON_DEMAND" not in (m.get("inferenceTypesSupported") or []):
            continue
        if mid in profile_covered_models:
            continue
        version = _parse_bedrock_anthropic_version(mid)
        if version is None:
            continue
        candidates.append((version, 0, mid))

    if not candidates:
        return None
    candidates.sort(reverse=True)

    # v0.1.41: test-call closure. AWS's enumerable signals (lifecycle,
    # inferenceTypesSupported) miss real failure modes — we've shipped
    # three iterations of "another filter" (v0.1.36 lexical sort,
    # v0.1.39 LEGACY skip, v0.1.40 ON_DEMAND require) and STILL hit a
    # new class on the v0.1.40 deep-test re-validation: a profile whose
    # underlying foundation model is EOL'd from `list_foundation_models`
    # entirely but whose cross-region inference profile lingers as
    # `status=ACTIVE`. AWS reports `ResourceNotFoundException: This
    # model version has reached the end of its life` only at Converse
    # time. Each AWS misalignment class we discover is a flag we add;
    # the test-call is the closure — it catches everything Bedrock can
    # invent because it's the same call path the agent will actually
    # use.
    #
    # Cost: one Converse 1-token ping per candidate tried (in version-
    # priority order, stop at first success). Worst case ~5 calls @
    # ~$0.0001 each + ~200ms each. Best case 1 call. Negligible vs
    # the cost of "init succeeds, gap fails 30 min later."
    try:
        runtime = boto3.Session().client("bedrock-runtime", region_name=region)
    except Exception:
        # Couldn't construct the runtime client — fall back to v0.1.40
        # behavior (return highest-version candidate untested, let the
        # eventual agent call surface the failure). Better degraded
        # than total failure on credential edge cases.
        return candidates[0][2]

    for _version, _priority, model_id in candidates:
        if _is_invokable(runtime, model_id):
            return model_id

    # All candidates failed test-call. Return None so caller surfaces
    # the actionable error rather than writing a doomed config.
    return None


def _is_invokable(runtime_client: Any, model_id: str) -> bool:
    """1-token Converse ping. Returns True if the model accepts the call.

    Used by `_probe_bedrock_for_family` (v0.1.41+) to verify that an
    auto-pick candidate is ACTUALLY callable, not just listable. Catches:
      - EOL models still surfaced via lingering inference profiles
      - Invalid model IDs (typos, region mismatches)
      - Inference-profile-only models that slipped past the
        ON_DEMAND filter
      - Future AWS misalignment classes we haven't enumerated yet

    Returns False on any exception. We don't try to classify the
    error — anything that isn't a successful Converse means the model
    isn't usable for our agents. Quota/throttling errors at probe time
    would also return False, which is the right call: if Bedrock is
    throttling the smallest possible request, agent-time calls will
    fare worse.
    """
    try:
        runtime_client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": "hi"}]}],
            inferenceConfig={"maxTokens": 1},
        )
        return True
    except Exception:
        return False


def _ancestor_with_github_workflows(target: Path) -> Path | None:
    """Nearest strict ancestor of `target` containing `.github/workflows/`, or None.

    Used to warn when `efterlev scan --target infra/terraform` sits below
    a `.github/workflows/` directory the GitHub-source detectors would
    otherwise see — silent under-coverage is a documented v0.1.x footgun
    real customer repos hit. The walk stops at the git repo root (first
    parent containing a `.git/` entry) or at the filesystem root,
    whichever comes first.
    """
    for parent in target.resolve().parents:
        if (parent / ".github" / "workflows").is_dir():
            return parent
        if (parent / ".git").exists():
            return None
    return None


def _display_path(p: Path, target: Path) -> str:
    # On macOS, `/tmp` is a symlink to `/private/tmp`. We resolve target
    # paths internally so provenance records carry canonical paths, but
    # users typing `--target /tmp/X` then hunting for `/private/tmp/...`
    # in their finder is a real paper-cut. Re-stitch the path under the
    # un-resolved target form for display only. Falls back to the
    # canonical path if `p` isn't actually under `target.resolve()`.
    try:
        return str(target / p.relative_to(target.resolve()))
    except ValueError:
        return str(p)


@app.callback(invoke_without_command=True)
def _root(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Print the Efterlev version and exit.",
        is_eager=True,
    ),
) -> None:
    """Efterlev root callback. Handles --version and the no-subcommand case."""
    # `studio --live` spawns this CLI as a subprocess with EFTERLEV_STUDIO_EVENT_LOG
    # set; bind a process-global recorder bus so the scan + gap agent stream their
    # typed events to that file. No-op in every normal invocation (env unset).
    _event_log = os.environ.get("EFTERLEV_STUDIO_EVENT_LOG")
    if _event_log:
        from efterlev.events.recorder import record_events_to

        record_events_to(Path(_event_log))
    if version:
        typer.echo(f"efterlev {__version__}")
        # v0.1.38: when --version runs, also detect and warn about
        # parallel installs (uv-tool ↔ pipx shadowing) on stderr. The
        # doctor command catches this too, but users hit `--version`
        # first to confirm what they upgraded to — and the silent
        # symlink-shadow case (S1 from v0.1.35 deep-test: user ran
        # `pipx upgrade efterlev` to v0.1.35 but uv-tool's symlink
        # kept routing PATH to v0.1.15) is exactly the case they
        # need warned about at version-check time.
        try:
            from efterlev.cli.doctor import _efterlev_manager_installs
        except ImportError:  # pragma: no cover
            raise typer.Exit() from None
        managers = _efterlev_manager_installs()
        if len(managers) > 1:
            mgr_names = ", ".join(sorted({m for m, _, _ in managers}))
            typer.echo(
                f"warning: {len(managers)} parallel installs detected ({mgr_names}). "
                f"`{mgr_names.split(',')[0].strip()} upgrade` may silently leave you on the older "
                f"version because PATH symlinks belong to whichever manager won the race. "
                f"Run `efterlev doctor` for uninstall guidance.",
                err=True,
            )
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        # Cold open (DECISIONS 2026-05-22): on a real terminal, a bare
        # `efterlev` opens Studio — the visual front door. Off a TTY (piped,
        # CI, `efterlev | cat`) it prints help as before, so scripted use is
        # unchanged. `efterlev --help` always shows help.
        from efterlev.cli.first_run_wizard import is_interactive

        if is_interactive():
            from efterlev.studio.server import run_studio_web

            run_studio_web(Path(".").resolve())
            raise typer.Exit()
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command()
def shell(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root the shell session starts in. Defaults to the current directory.",
    ),
) -> None:
    """Start the interactive Efterlev shell.

    Persistent session with workspace state always visible, tab
    completion against the slash-command registry, command history,
    and state-aware next-step hints. Slash commands dispatch to the
    same primitives the bare CLI uses; no command logic is duplicated.

    Exit with `/exit`, `/quit`, or Ctrl+D. See `/help` for the full
    command list once inside.
    """
    from efterlev.shell import run_shell

    raise typer.Exit(code=run_shell(target))


@app.command()
def start(
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Prompt for each answer interactively (the default on a TTY when no flags are given).",
    ),
    cloud: str | None = typer.Option(
        None,
        "--cloud",
        help="Cloud provider: aws / azure / gcp / other. Default aws.",
    ),
    partition: str | None = typer.Option(
        None,
        "--partition",
        help="AWS partition: commercial / govcloud. Default commercial (AWS only).",
    ),
    impact_level: str | None = typer.Option(
        None,
        "--impact-level",
        help="Target impact level: low / moderate / high. Default moderate.",
    ),
    architecture: str | None = typer.Option(
        None,
        "--architecture",
        help="Architecture: serverless / containers / vms / hybrid. Default serverless.",
    ),
    posture: str | None = typer.Option(
        None,
        "--posture",
        help="Existing compliance: none / soc2 / iso27001 / fedramp-rev5 / other. Default none.",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        help="Also write the report to this path; always printed to stdout too.",
    ),
) -> None:
    """Pre-scan strategic walkthrough for FedRAMP 20x (Stage 0).

    Runs before a workspace exists. Asks about your cloud, impact level,
    architecture, and existing posture, then prints a personalized "your
    FedRAMP 20x path" report — which KSI families matter for your
    architecture, the seven-stage journey, and your next three commands.

    On a TTY with no flags it prompts interactively; pass flags (or run
    in CI) to use defaults non-interactively. Pure orientation — no
    workspace, no scan, no LLM call.
    """
    from efterlev.cli.start_cli import run_start

    raise typer.Exit(
        code=run_start(
            interactive=interactive,
            cloud=cloud,
            partition=partition,
            impact_level=impact_level,
            architecture=architecture,
            posture=posture,
            out=out,
        )
    )


@app.command()
def studio(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root to reflect. A scanned workspace shows its real "
        "verdicts; elsewhere Studio shows a labeled sample.",
    ),
    sample: bool = typer.Option(
        False,
        "--sample",
        help="Use the bundled govnotes sample instead of --target. Alone: instant, "
        "keyless real posture. With --live: runs the real pipeline on the sample.",
    ),
    live: bool = typer.Option(
        False,
        "--live",
        help="Run a real scan + gap classification on --target and stream it into "
        "the flow as it happens (needs an LLM backend configured for verdicts).",
    ),
    watch: Path | None = typer.Option(
        None,
        "--watch",
        help="Attach mode: stream events from an externally-driven `report run` by "
        "tailing the given JSONL event log. The driver sets "
        "`EFTERLEV_STUDIO_EVENT_LOG=<path>` for its `report run` and opens Studio "
        "in this mode — use when the AI install prompt or CI drives the pipeline.",
    ),
    no_open: bool = typer.Option(
        False,
        "--no-open",
        help="Start the server but don't open a browser (prints the localhost URL).",
    ),
    port: int = typer.Option(0, "--port", help="Localhost port (0 = pick a free one)."),
    poster: Path | None = typer.Option(
        None,
        "--poster",
        help="Write a shareable poster SVG of your posture to this path and exit "
        "(no server). e.g. --poster posture.svg",
    ),
) -> None:
    """Launch Efterlev Studio — the visual compliance map.

    Opens a local browser app: the 60 Key Security Indicators resolve out of
    the "fog" as evidence flows in and settles into a live dashboard — a
    theme-grouped grid of verdict-colored tiles alongside the readiness ring
    and the gap-agent feed. A scanned workspace shows your real verdicts;
    elsewhere a clearly-labeled sample.

    `--live` runs the real pipeline (scan + gap) on --target and streams the
    event flow into the page as it happens — evidence rushes in, then each KSI
    blooms to its verdict as the agent classifies it. `--sample` uses the
    bundled govnotes sample (instant + keyless on its own; a real run with
    --live) — the easiest way to see it before pointing it at your own repo.
    Local-first: the server runs on 127.0.0.1, the scan/agents run on your
    machine, nothing phones home. `--poster <path>` exports a shareable image
    instead of launching.
    """
    root = target.resolve()

    # Mutual exclusion: --watch is a third top-level mode beside --live and --sample.
    if watch is not None and (live or sample or poster is not None):
        typer.echo(
            "error: --watch is mutually exclusive with --live, --sample, and --poster.",
            err=True,
        )
        raise typer.Exit(code=2)

    if poster is not None:
        from efterlev.studio.poster import write_poster

        written = write_poster(root, poster.resolve())
        typer.echo(f"Wrote poster → {written}")
        return

    if watch is not None:
        from efterlev.studio.server import run_studio_watch

        run_studio_watch(root, watch.resolve(), open_browser=not no_open, port=port)
        return

    if sample and live:
        from efterlev.studio.server import materialize_sample, run_studio_live

        typer.echo("Running the live pipeline on the bundled govnotes sample…")
        run_studio_live(materialize_sample(), open_browser=not no_open, port=port)
        return

    if sample:
        from efterlev.studio.server import run_studio_web

        run_studio_web(None, open_browser=not no_open, port=port, sample=True)
        return

    if live:
        from efterlev.studio.server import run_studio_live

        run_studio_live(root, open_browser=not no_open, port=port)
        return

    from efterlev.studio.server import run_studio_web

    run_studio_web(root, open_browser=not no_open, port=port)


@app.command()
def catalog(
    theme: str | None = typer.Option(
        None,
        "--theme",
        help="Filter to one theme by id (e.g. AFR, SVC, CNA). Case-insensitive.",
    ),
    baseline: str = typer.Option(
        "fedramp-20x-moderate",
        "--baseline",
        help="FedRAMP 20x baseline to browse. Default: fedramp-20x-moderate.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit the catalog as JSON instead of the human-readable listing.",
    ),
) -> None:
    """Browse the KSI catalog for a baseline (Stage 0 reference).

    Lists every Key Security Indicator, grouped by theme, with how Efterlev
    evidences it ([scanner] from your IaC/runtime · [manifest] an Evidence
    Manifest you author · [hybrid] both) and its mapped NIST 800-53
    controls. The detailed companion to `efterlev plan`'s aggregate work
    breakdown — answers "show me exactly what I'll be measured against".

    Runs with no workspace, no IaC, no API key (bundled catalog data only).
    Deterministic; no LLM, no network, no files written.
    """
    from efterlev.cli.catalog import run_catalog

    raise typer.Exit(code=run_catalog(baseline=baseline, theme=theme, json_output=json_output))


@app.command()
def plan(
    architecture: str | None = typer.Option(
        None,
        "--architecture",
        "-a",
        help=(
            "Primary architecture (serverless / containers / ec2 / hybrid). "
            "Overlays which KSIs you may inherit from your CSP. Prompts "
            "interactively if omitted on a terminal."
        ),
    ),
    baseline: str = typer.Option(
        "fedramp-20x-moderate",
        "--baseline",
        help="FedRAMP 20x baseline to map. Default: fedramp-20x-moderate.",
    ),
) -> None:
    """Map the KSI landscape for a baseline before you scan (Stage 0).

    The pre-scan strategic-orientation command: with no workspace, no IaC,
    and no API key, it shows what FedRAMP 20x will measure you against —
    how many KSIs Efterlev evidences automatically from your
    infrastructure, how many need a human-authored Evidence Manifest (the
    procedural ones: personnel, training, incident response), where the
    human work concentrates by theme, and — for a chosen architecture —
    which KSIs are commonly CSP-inherited under shared responsibility.

    Deterministic; no LLM, no network, no files written. It's a map, not a
    scan. Run it before `efterlev init` to scope the work.
    """
    from efterlev.cli.plan import run_plan

    raise typer.Exit(code=run_plan(baseline=baseline, architecture=architecture))


@app.command()
def readiness(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root to score. Defaults to the current directory.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit the report as JSON instead of the human-readable view.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help=(
            "RFC-0017 per-KSI gate instead of the heuristic score. Exits "
            "2 on gate fail (any KSI missing any of the 5 PVA items). "
            "This is the check to wire into pre-submission CI."
        ),
    ),
) -> None:
    """Score how close this workspace is to a 3PAO scoping conversation.

    Default: heuristic 0-100% score combining KSI classification coverage,
    procedural-manifest coverage, and severity penalty for open HIGH-severity
    POA&M items. Ranks the top 3 blockers + suggests the next command for
    each. Exit 0 always.

    With `--strict`: RFC-0017 per-KSI gate. Every baseline KSI is checked
    against the 5 PVA items (implementation goal, consolidated inventory,
    automated cadence, human cadence, current status). Exit 2 if any KSI
    fails any item. Use this for pre-submission CI.

    Pure deterministic; reads the provenance store + manifests. Zero LLM
    spend. Safe to call as often as you like.
    """
    from efterlev.cli.readiness_cli import run_readiness

    raise typer.Exit(code=run_readiness(target, json_output=json_output, strict=strict))


submission_app = typer.Typer(
    name="submission",
    help="Build a 3PAO-ready submission package from this workspace's artifacts.",
    no_args_is_help=True,
)
app.add_typer(submission_app)


@submission_app.command("package")
def submission_package(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root containing `.efterlev/`. Defaults to the current directory.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Where to write the package. Defaults to "
            "`efterlev-out/submissions/submission-<ts>.zip` (v0.1.160+ visible-"
            "output split; was `.efterlev/submissions/`). Pass `--no-archive` "
            "to write a directory instead of a zip."
        ),
    ),
    no_archive: bool = typer.Option(
        False,
        "--no-archive",
        help="Write a directory tree instead of a .zip archive.",
    ),
    package_version: str | None = typer.Option(
        None,
        "--version",
        help=(
            "Version string embedded in the README + index.json. "
            "Defaults to a timestamp-based string."
        ),
    ),
) -> None:
    """Bundle the artifacts a 3PAO needs into a single deliverable.

    Picks the LATEST of each artifact type from `efterlev-out/reports/`
    (v0.1.160+ visible-output split; also reads legacy `.efterlev/reports/`
    for backward compat) and `.efterlev/manifests/` (customer-authored,
    unchanged location) and bundles them with a README + machine-readable
    index. Hands directly to a 3PAO; re-runnable as the customer closes
    more gaps.

    Pure deterministic; reads existing artifacts. Zero LLM spend.
    """
    from efterlev.cli.submission_cli import run_submission_package

    raise typer.Exit(
        code=run_submission_package(
            target,
            output=output,
            archive=not no_archive,
            package_version=package_version,
        )
    )


@app.command()
def init(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo to initialize. Defaults to the current directory.",
    ),
    baseline: str = typer.Option(
        "fedramp-20x-moderate",
        "--baseline",
        help="Compliance baseline to load. v0 supports `fedramp-20x-moderate` only.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing `.efterlev/` directory.",
    ),
    llm_backend: str = typer.Option(
        "anthropic",
        "--llm-backend",
        help=(
            "LLM backend: 'anthropic' (direct API), 'bedrock' (AWS Bedrock), "
            "or 'claude_code' (local `claude` subprocess; Claude Pro/Max "
            "subscription, zero per-call billing)."
        ),
    ),
    llm_region: str | None = typer.Option(
        None,
        "--llm-region",
        help=(
            "AWS region for Bedrock backend (e.g. 'us-gov-west-1'). "
            "Required when --llm-backend=bedrock."
        ),
    ),
    llm_model: str | None = typer.Option(
        None,
        "--llm-model",
        help=(
            "LLM model ID. When omitted, each agent uses its per-task "
            "default (Opus 4.7 for Gap and Remediation; Sonnet 4.6 for "
            "Documentation, ~5x cheaper for narrative drafting). When "
            "set, every agent uses this model uniformly. Bedrock backend "
            "always populates a Bedrock-shaped ID (e.g. "
            "'us.anthropic.claude-opus-4-7-v1:0')."
        ),
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Run the interactive setup wizard (the default for a bare `init` on a TTY).",
    ),
    no_interactive: bool = typer.Option(
        False,
        "--no-interactive",
        help="Force non-interactive init even on a TTY (use flags + defaults).",
    ),
) -> None:
    """Initialize `.efterlev/` in the target repo with a provenance store and config.

    On a TTY, a bare `efterlev init` (no config flags) runs an interactive
    wizard — cloud, LLM backend, boundary scope — and pre-fills from a
    prior `efterlev start`. Pass flags, pipe input, or `--no-interactive`
    for the scripted path. v0.1.172 / #378.
    """
    # v0.1.172 / #378: decide whether to run the interactive wizard. Opt-in
    # by design — a scripted `init` (any config flag, or non-TTY) keeps the
    # exact prior behavior. A bare `init` on a TTY is guided.
    from efterlev.cli.first_run_wizard import is_interactive as _is_tty
    from efterlev.config import (
        DEFAULT_BEDROCK_OPENAI_MODEL,
        DEFAULT_FALLBACK_MODEL,
        DEFAULT_OPENAI_MODEL,
        BoundaryConfig,
        LLMConfig,
    )
    from efterlev.errors import CatalogLoadError, ConfigError
    from efterlev.workspace import init_workspace

    _passed_config_flag = (
        baseline != "fedramp-20x-moderate"
        or llm_backend != "anthropic"
        or llm_region is not None
        or llm_model is not None
    )
    run_wizard = interactive or (not no_interactive and not _passed_config_flag and _is_tty())
    boundary_config: BoundaryConfig | None = None
    if run_wizard:
        from efterlev.cli.init_wizard import run_init_wizard

        wiz = run_init_wizard(target.resolve())
        baseline = wiz.baseline
        llm_backend = wiz.llm_backend
        llm_region = wiz.llm_region
        if wiz.boundary_include or wiz.boundary_exclude:
            boundary_config = BoundaryConfig(
                include=wiz.boundary_include, exclude=wiz.boundary_exclude
            )

    # Typer-level validation: fail fast on obvious CLI mistakes before
    # Pydantic's model_validator catches the same thing at config construction.
    if llm_backend not in ("anthropic", "bedrock", "claude_code", "openai", "bedrock_openai"):
        typer.echo(
            f"error: --llm-backend must be 'anthropic', 'bedrock', "
            f"'claude_code', 'openai', or 'bedrock_openai', got {llm_backend!r}",
            err=True,
        )
        raise typer.Exit(code=2)
    if llm_backend in ("bedrock", "bedrock_openai") and not llm_region:
        hint = (
            "'us-gov-west-1' or 'us-east-1'"
            if llm_backend == "bedrock"
            else "'us-east-2' or 'us-west-2' (commercial only at launch)"
        )
        typer.echo(
            f"error: --llm-region is required when --llm-backend={llm_backend} (e.g. {hint})",
            err=True,
        )
        raise typer.Exit(code=2)
    if llm_backend in ("anthropic", "claude_code", "openai") and llm_region:
        typer.echo(
            f"error: --llm-region is only valid with --llm-backend=bedrock "
            f"(got --llm-backend={llm_backend!r})",
            err=True,
        )
        raise typer.Exit(code=2)

    # Build LLMConfig explicitly so the Pydantic validator enforces the
    # invariants one more time (defense in depth).
    #
    # Anthropic backend: when --llm-model is not passed, store None so the
    # per-agent default_model values (Sonnet for Documentation, Opus for
    # Gap and Remediation) stay live at agent runtime. Passing --llm-model
    # at init overrides every agent's default uniformly.
    #
    # Bedrock backend: always populate model with a Bedrock-shaped ID
    # because the per-agent default_model values use Anthropic short-form
    # IDs that Bedrock does not accept. The LLMConfig validator rejects
    # `backend=bedrock, model=None` to enforce this.
    #
    # When --llm-model isn't passed and the backend is bedrock, probe
    # the user's account for available Anthropic inference profiles and
    # pick the latest Opus. Falls back to the hardcoded
    # DEFAULT_BEDROCK_MODEL only if the probe fails (no boto, no perms,
    # no profiles enabled). This avoids the v0.1.0-v0.1.2 first-run
    # failure mode where the hardcoded default doesn't exist in the
    # user's account.
    if llm_backend == "bedrock":
        if llm_model:
            configured_model: str | None = llm_model
        else:
            probed = _probe_bedrock_default_model(llm_region)
            if probed is None:
                # v0.1.40: when probe finds zero usable candidates after
                # the lifecycle + on-demand filtering, the hardcoded
                # DEFAULT_BEDROCK_MODEL almost certainly won't work either
                # — same account state that hid usable profiles from the
                # probe will reject the default at agent-call time. Surface
                # a clear error with the three real remediations instead
                # of silently writing a doomed config. Surfaced by the
                # v0.1.39 deep-test re-validation S2 finding.
                typer.echo(
                    f"error: no usable Anthropic {llm_model or 'Opus'} model "
                    f"auto-discovered in {llm_region}.\n"
                    f"\n"
                    f"  Either:\n"
                    f"    (a) Opt into a `us.*` cross-region inference profile for a\n"
                    f"        newer Opus model in the AWS Bedrock Model Access page\n"
                    f"        (https://console.aws.amazon.com/bedrock/home#/modelaccess),\n"
                    f"        then re-run init.\n"
                    f"    (b) Override with `--llm-model global.anthropic.claude-opus-4-7-v1:0`\n"
                    f"        (or another `global.*` profile). NOTE: `global.*` forfeits\n"
                    f"        the US-region geographic guarantee — review with your\n"
                    f"        FedRAMP boundary documentation before using.\n"
                    f"    (c) Override with `--llm-model us.anthropic.claude-sonnet-4-6-v1:0`\n"
                    f"        (or any other directly-invokable Sonnet/Haiku profile in\n"
                    f"        your account).\n"
                    f"\n"
                    f"  Diagnose what your account exposes:\n"
                    f"    aws bedrock list-foundation-models --by-provider anthropic \\\n"
                    f"      --region {llm_region} --query \\\n"
                    f"      'modelSummaries[].[modelId,modelLifecycle.status,"
                    f"inferenceTypesSupported]'",
                    err=True,
                )
                raise typer.Exit(code=1)
            configured_model = probed
            typer.echo(
                f"info: discovered Bedrock model {configured_model!r} "
                f"in {llm_region}; using it as the default model. Override with "
                f"--llm-model=<arn> if you want a different one.",
            )
    elif llm_backend == "claude_code" and not llm_model:
        # v0.1.175 / #381: pin claude_code agents to Sonnet 4.6, NOT the gap
        # agent's Opus default. Large Opus-4.7 (1M-context) calls via
        # `claude --print` are pathologically slow on the subscription —
        # observed 7.7-min time-to-first-token and intermittent fast-fails
        # (exit 1), so the gap stage couldn't finish under the client
        # timeout. base.py resolves an explicit config model OVER each
        # agent's `default_model`, so setting Sonnet HERE is what actually
        # overrides gap's Opus pin (leaving model=None would let gap fall
        # back to Opus and re-break). Sonnet is "indistinguishable from
        # Opus on the 60-KSI sweep" and returns in seconds; still $0 on
        # subscription. Pass --llm-model explicitly to force Opus (and
        # accept the latency) or Haiku.
        configured_model = "claude-sonnet-4-6"
    elif llm_backend == "openai" and not llm_model:
        # OpenAI launch readiness: the openai backend has no valid per-agent
        # default — gap/remediation default_model is the Claude short-form
        # 'claude-opus-4-7', which OpenAI 404s — and the interactive init
        # wizard never asks for a model. Pin the validated recommended
        # production model so a bare wizard pick (or `--llm-backend=openai`
        # without --llm-model) works out of the box. gpt-5.4-mini: 95.8%
        # precision + 100% recall on csp-starter-cfn, cheapest of the
        # validated set (v0.1.213). Pass --llm-model to override (e.g. gpt-5
        # for the safer under-classification failure mode).
        configured_model = DEFAULT_OPENAI_MODEL
    elif llm_backend == "bedrock_openai" and not llm_model:
        # Same rationale as openai: the per-agent Claude defaults are invalid
        # on the Mantle endpoint, so pin the validated default (gpt-5.5; see
        # config.DEFAULT_BEDROCK_OPENAI_MODEL). Pass --llm-model openai.gpt-5.4
        # for the alternative.
        configured_model = DEFAULT_BEDROCK_OPENAI_MODEL
    else:
        configured_model = llm_model
    # v0.1.175 / #381: the prior "Opus is free upside on subscription"
    # default was a latency trap (see above) — and moot anyway, because the
    # claude_code client does not use fallback_model (no fallback path in
    # `--print` mode). Keep the workspace fallback at Sonnet on Anthropic /
    # Bedrock (the cost/quality sweet spot); inert on claude_code. On openai
    # a Claude fallback would 404, so disable it — the client's 3-attempt
    # within-provider retry covers transients, and the factory drops any
    # non-OpenAI fallback as a backstop.
    fallback_model_for_backend = (
        "" if llm_backend in ("openai", "bedrock_openai") else DEFAULT_FALLBACK_MODEL
    )
    llm_config = LLMConfig(
        backend=llm_backend,  # type: ignore[arg-type]
        model=configured_model,
        region=llm_region,
        fallback_model=fallback_model_for_backend,
    )

    # Priority 3.4 (2026-04-28): show the first-run wizard before init
    # touches disk. Auto-skips on non-TTY (CI-safe) and when credentials
    # are already configured. The wizard only prints; it never blocks
    # init, so CI and scripted-init flows behave identically.
    from efterlev.cli.first_run_wizard import maybe_show_first_run_intro

    maybe_show_first_run_intro(llm_backend=llm_backend)

    try:
        result = init_workspace(
            target.resolve(),
            baseline,
            force=force,
            llm_config=llm_config,
            boundary_config=boundary_config,
        )
    except (ConfigError, CatalogLoadError) as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"Initialized {result.efterlev_dir}")
    typer.echo(f"  baseline:              {result.baseline}")
    typer.echo(
        f"  FRMR:                  v{result.frmr_version} "
        f"({result.frmr_last_updated}, {result.num_themes} themes, "
        f"{result.num_indicators} indicators)"
    )
    typer.echo(
        f"  NIST SP 800-53 Rev 5:  "
        f"{result.num_controls} controls "
        f"(+{result.num_enhancements} enhancements)"
    )
    typer.echo(f"  load receipt:          {result.receipt_record_id}")

    # Catalog-freshness nudges go to stderr after the success block so they
    # don't get lost in the init banner. Non-blocking: init has already
    # succeeded by this point.
    for warning in result.freshness_warnings:
        typer.echo("")
        typer.echo(warning, err=True)

    # Next-steps suggestion (v0.1.84 UX-polish bundle): the post-init
    # moment is the highest-leverage spot to point first-time users at
    # the natural next commands. Without this, a user might hit init
    # success and not know whether to run `scan` directly, `doctor`
    # first, or `report run` for the full pipeline. Three lines, no
    # cost, big first-impression payoff.
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        "  efterlev doctor       pre-flight check (Python, FRMR cache, API key, "
        "Bedrock creds, LLM ping)"
    )
    typer.echo(
        "  efterlev report run   full pipeline: scan → agent gap → agent document "
        "→ poam → oscal (LLM cost scales with repo size — cents on a small boundary, "
        "a few dollars on a large one; OSCAL emit is deterministic + free)"
    )
    typer.echo("  efterlev scan         deterministic detector evidence only (no LLM, no API key)")
    typer.echo("")
    typer.echo(
        "New to FedRAMP 20x? `efterlev plan` maps the work before you scan; docs/choosing-20x.md"
    )
    typer.echo("  covers the 20x-vs-Rev 5 decision.")


@app.command()
def scan(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo to scan. Defaults to the current directory.",
    ),
    plan: Path | None = typer.Option(
        None,
        "--plan",
        help=(
            "Path to a `terraform show -json <plan>` output file. When supplied, "
            "resources are read from the resolved plan instead of parsed from .tf "
            "files — exposes module `for_each` expansion and resolved values. "
            "Mutually exclusive with HCL-directory scanning (both modes still "
            "load manifests from `--target`)."
        ),
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help=(
            "Print full SHA256 record IDs for every emitted Evidence record. "
            "By default the per-detector record-id list is suppressed — record "
            "IDs are persisted in the provenance store (`.efterlev/store.db`) "
            "and surfaced by `efterlev provenance show <id>` when needed. "
            "First-time users find the SHA256 dump overwhelming."
        ),
    ),
    allow_subdir_target: bool = typer.Option(
        False,
        "--allow-subdir-target",
        help=(
            "Acknowledge that `--target` sits below a `.github/workflows/` "
            "ancestor and proceed without GitHub-source detector coverage. "
            "Without this flag, scan refuses to run when the situation is "
            "detected — silent under-coverage is a documented funnel-killer "
            "(a first-run user sees `20 evidence records` and concludes "
            "the tool covered their repo, when actually github-source "
            "detectors contributed zero). Pass this flag only when you "
            "deliberately want subdir-only Terraform scope (e.g. monorepo "
            "with multiple Terraform roots, or a quick re-scan of one "
            "subdir)."
        ),
    ),
) -> None:
    """Run all applicable detectors and load Evidence Manifests under the target.

    By default scans `.tf` files under `--target` via HCL parsing. Supply
    `--plan FILE` to instead scan a pre-generated Terraform plan JSON —
    the recommended mode for CI because module expansion and resolved
    values (jsonencode, variable references, for_each) are fully visible.
    See DECISIONS 2026-04-22 "Design: Terraform Plan JSON support" for
    the trust-posture call.
    """
    from efterlev.boundary import active_boundary_config
    from efterlev.config import load_config
    from efterlev.errors import ConfigError, DetectorError, ManifestError
    from efterlev.events import (
        EvidenceFound,
        KsiEvidenced,
        ScanFinished,
        ScanStarted,
        emit,
        get_active_bus,
    )
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.primitives.evidence import (
        LoadEvidenceManifestsInput,
        load_evidence_manifests,
    )
    from efterlev.primitives.scan import (
        ScanCdkPythonInput,
        ScanCloudFormationInput,
        ScanGithubWorkflowsInput,
        ScanTerraformInput,
        ScanTerraformPlanInput,
        scan_cdk_python,
        scan_cloudformation,
        scan_github_workflows,
        scan_terraform,
        scan_terraform_plan,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        # v0.1.174 / #380: a common first-run miss is pointing --target at a
        # subdirectory (e.g. `scan --target infra/terraform`). --target is
        # the workspace root where `init` ran; scan recurses into subdirs on
        # its own. Hint both possibilities rather than only "run init".
        typer.echo(
            f"error: no `.efterlev/` directory under {root}.\n"
            "  --target must be the workspace ROOT (where you ran `efterlev "
            "init`); scan recurses into subdirectories on its own, so don't "
            "point it at a subdir.\n"
            "  If you haven't initialized yet, run `efterlev init` at the repo root first.",
            err=True,
        )
        raise typer.Exit(code=1)

    # Pre-flight: catch the `--target <subdir>` + `.github/workflows/` ancestor
    # case before scan runs. Previously we warned AFTER scan completed; that
    # left first-run users seeing a "20 evidence records" success line and
    # concluding the tool covered their repo, when github-source detectors
    # had silently contributed zero. The warning was easy to miss in CI logs.
    # Hard-error by default; --allow-subdir-target opts into the prior behavior
    # for the legitimate monorepo-with-multiple-Terraform-roots case.
    wf_ancestor = _ancestor_with_github_workflows(root)
    if wf_ancestor is not None and not allow_subdir_target:
        typer.echo(
            f"error: `--target {target}` resolves to {root}, which sits below a "
            f"`.github/workflows/` directory at {wf_ancestor}.",
            err=True,
        )
        typer.echo(
            "  Scanning a subdir means GitHub-source detectors (workflow YAML) "
            "find nothing — under-coverage that's silent in the output.",
            err=True,
        )
        typer.echo("  Two ways forward:", err=True)
        typer.echo(
            f"    1. Re-run from the repo root for full coverage: "
            f"`efterlev scan --target {wf_ancestor}` "
            f"(`.tf` files under that root are still found via rglob)",
            err=True,
        )
        typer.echo(
            "    2. Pass `--allow-subdir-target` to acknowledge the trade-off "
            "and proceed with Terraform-only scope (the legitimate "
            "monorepo-with-multiple-Terraform-roots case).",
            err=True,
        )
        raise typer.Exit(code=2)

    # --plan is a dedicated mode; we don't try to scan both HCL + plan in
    # the same invocation (would double-emit evidence).
    plan_path = plan.resolve() if plan is not None else None
    if plan_path is not None and not plan_path.is_file():
        typer.echo(f"error: --plan file not found: {plan_path}", err=True)
        raise typer.Exit(code=1)

    # KSI→controls mapping, derived from the cached FRMR document the workspace
    # wrote at `init` time. Required for manifest loading (we don't invent
    # control lists; we resolve them from FRMR as the single source of truth).
    # Hard-error on missing cache rather than silently skipping every manifest
    # as "unknown KSI" — the latter masked broken init states as configuration
    # mistakes. Match the error style of `agent gap`/`agent document`.
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)
    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    ksi_to_controls: dict[str, list[str]] = {
        k: list(ind.controls) for k, ind in frmr_doc.indicators.items()
    }

    manifest_dir = root / ".efterlev" / "manifests"

    # Priority 4 (2026-04-27): activate the workspace's `[boundary]` config so
    # detectors emit Evidence with the correct `boundary_state`. Empty boundary
    # is the default ("boundary_undeclared") — the user hasn't told us their
    # FedRAMP scope, so every Evidence flows through unfiltered.
    try:
        workspace_config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    # Studio event spine (DECISIONS 2026-05-22): emit a typed event stream
    # alongside the scan. No-op in the normal CLI path (no active bus); a
    # bus is bound only by Studio or a test, so this changes nothing here.
    emit(ScanStarted(mode="plan" if plan_path is not None else "hcl", target=str(root)))

    try:
        with (
            ProvenanceStore(root) as store,
            active_store(store),
            active_boundary_config(workspace_config.boundary),
        ):
            if plan_path is not None:
                scan_result = scan_terraform_plan(
                    ScanTerraformPlanInput(plan_file=plan_path, target_root=root)
                )
            else:
                scan_result = scan_terraform(ScanTerraformInput(target_dir=root))
            # Priority 1.2 (2026-04-27): also scan `.github/workflows/*.yml`
            # for repo-metadata detectors (currently github.ci_validation_gates
            # for KSI-CMT-VTD). Empty result when the target has no
            # `.github/workflows/` directory — typical for non-GitHub-Actions
            # repos. Both terraform and github-workflows results merge into
            # the user-facing scan summary.
            workflow_result = scan_github_workflows(ScanGithubWorkflowsInput(target_dir=root))
            # CFN scan runs unconditionally as of v0.1.102 (CFN graduation
            # arc step 4). Walks YAML/JSON under --target, content-sniffs
            # for CFN templates, runs the SAME terraform-source detectors
            # over CFN-adapter-shaped resources. Type-coverage 100% (60/60
            # detectors at v0.1.96); maintainer-validation 44/44 = 100/100
            # across 2 fixtures (csp-starter-cfn v0.1.81 + aws-vpc-cfn
            # v0.1.98). The `--allow-cfn` opt-in flag (v0.1.72-v0.1.98)
            # was deprecated at v0.1.99 and removed at v0.1.102.
            cfn_result = scan_cloudformation(ScanCloudFormationInput(target_dir=root))
            # CDK Python source-mode runs unconditionally at v0.1.131
            # (graduated; mirrors v0.1.102 removal of --allow-cfn). Walks
            # `.py` files for supported `aws_cdk.*` construct invocations
            # (27 constructs at v0.1.129); preserves file:line citations
            # back to the source. Composes with synth-mode (`cdk synth →
            # CFN → scan`, default-on since v0.1.99) — source-mode for
            # code-review/inventory artifacts, synth-mode for property
            # depth. See DECISIONS 2026-05-15 amendment 1 for rationale.
            cdk_py_result = scan_cdk_python(ScanCdkPythonInput(target_dir=root))
            manifest_result = load_evidence_manifests(
                LoadEvidenceManifestsInput(
                    manifest_dir=manifest_dir,
                    ksi_to_controls=ksi_to_controls,
                    scan_root=root,
                )
            )
    except (DetectorError, ManifestError) as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    cfn_evidence_count = cfn_result.evidence_count if cfn_result is not None else 0
    cdk_py_evidence_count = cdk_py_result.evidence_count if cdk_py_result is not None else 0
    total_evidence = (
        scan_result.evidence_count
        + workflow_result.evidence_count
        + cfn_evidence_count
        + cdk_py_evidence_count
        + manifest_result.evidence_count
    )

    # Studio event spine: replay the scan's evidence as a typed stream so a
    # renderer can ignite the right stars. Guarded on an active bus so the
    # normal CLI path pays nothing (no bus → skip the walk entirely).
    if get_active_bus() is not None:
        by_source = {
            "terraform": scan_result.evidence_count,
            "github": workflow_result.evidence_count,
            "cloudformation": cfn_evidence_count,
            "cdk_python": cdk_py_evidence_count,
            "manifest": manifest_result.evidence_count,
        }
        ksi_counts: dict[str, int] = {}
        all_evidence = [
            *scan_result.evidence,
            *workflow_result.evidence,
            *(cfn_result.evidence if cfn_result is not None else []),
            *(cdk_py_result.evidence if cdk_py_result is not None else []),
            *manifest_result.evidence,
        ]
        for ev in all_evidence:
            emit(
                EvidenceFound(
                    detector_id=ev.detector_id,
                    ksis=list(ev.ksis_evidenced),
                    source_file=str(ev.source_ref.file),
                    line_start=ev.source_ref.line_start,
                    boundary_state=ev.boundary_state,
                )
            )
            for ksi in ev.ksis_evidenced:
                ksi_counts[ksi] = ksi_counts.get(ksi, 0) + 1
        for ksi, count in ksi_counts.items():
            emit(KsiEvidenced(ksi=ksi, evidence_count=count))
        emit(
            ScanFinished(
                evidence_total=total_evidence,
                by_source=by_source,
                ksis_with_evidence=len(ksi_counts),
            )
        )

    scan_mode = f"plan {plan_path}" if plan_path is not None else str(root)
    typer.echo(f"Scanned {scan_mode}")
    typer.echo(f"  resources parsed:    {scan_result.resources_parsed}")
    if scan_result.module_calls > 0:
        # Surfaced alongside resources so the imbalance (5 resources / 11
        # module calls) is visible at the top of the summary, not buried.
        typer.echo(f"  module calls:        {scan_result.module_calls}")
    if workflow_result.workflows_parsed > 0:
        typer.echo(f"  workflows parsed:    {workflow_result.workflows_parsed}")
    if cfn_result is not None:
        typer.echo(
            f"  cfn templates:       {cfn_result.cfn_templates_parsed} "
            f"({cfn_result.resources_parsed} resources adapted)"
        )
        # Surface parse failures explicitly — silent failures hide bugs.
        # Surfaced v0.1.103 after the aws-quickstart/quickstart-aws-aurora-
        # postgresql QA scan revealed a 1091-line template silently dropped
        # because the parser didn't handle the `!ValueOf` Rules-section
        # intrinsic.
        if cfn_result.parse_failures:
            typer.echo(
                f"  cfn parse failures:  {len(cfn_result.parse_failures)} — "
                f"see scan-<ts>.json sidecar for per-file reasons"
            )
        # Surface AWS::CloudFormation::Stack count as a known limitation.
        # Nested-stack expansion (following TemplateURL to fetch + parse
        # child templates) is a v0.x followup; today efterlev sees the
        # nested-stack reference as a single resource and stops there.
        # Surfaced v0.1.103 after the aurora-postgresql QA scan turned out
        # to be ~all nested-stack references.
        if cfn_result.nested_stack_refs:
            typer.echo(
                f"  cfn nested stacks:   {cfn_result.nested_stack_refs} (TemplateURL not "
                f"followed; scan child templates directly to reach nested resources)"
            )
    if cdk_py_result is not None:
        typer.echo(
            f"  cdk-py constructs:   {cdk_py_result.constructs_parsed} "
            f"(across {cdk_py_result.files_scanned} `.py` files; Stage 1 = `s3.Bucket` only)"
        )
        if cdk_py_result.parse_failures:
            typer.echo(
                f"  cdk-py parse failures: {len(cdk_py_result.parse_failures)} — "
                f"see scan-<ts>.json sidecar for per-file reasons"
            )
    typer.echo(
        f"  detectors run:       {scan_result.detectors_run + workflow_result.detectors_run}"
    )
    typer.echo(f"  manifest files:      {manifest_result.files_found}")
    typer.echo(f"  manifests loaded:    {manifest_result.manifests_loaded}")
    typer.echo(f"  evidence records:    {total_evidence}")
    detector_total = (
        scan_result.evidence_count
        + workflow_result.evidence_count
        + cfn_evidence_count
        + cdk_py_evidence_count
    )
    typer.echo(f"    from detectors:    {detector_total}")
    typer.echo(f"    from manifests:    {manifest_result.evidence_count}")
    for det in scan_result.per_detector:
        typer.echo(f"    {det.detector_id}@{det.version:<7}  +{det.evidence_count}")
    for det in workflow_result.per_detector:
        typer.echo(f"    {det.detector_id}@{det.version:<7}  +{det.evidence_count}")
    if cfn_result is not None:
        for cfn_det in cfn_result.per_detector:
            if cfn_det.evidence_count > 0:
                typer.echo(
                    f"    {cfn_det.detector_id}@{cfn_det.version:<7}  "
                    f"+{cfn_det.evidence_count} (cfn)"
                )
    if cdk_py_result is not None:
        for cdk_det in cdk_py_result.per_detector:
            if cdk_det.evidence_count > 0:
                typer.echo(
                    f"    {cdk_det.detector_id}@{cdk_det.version:<7}  "
                    f"+{cdk_det.evidence_count} (cdk-py)"
                )
    for m in manifest_result.per_manifest:
        rel = m.file.relative_to(root) if m.file.is_absolute() else m.file
        typer.echo(f"    manifest {rel}  ksi={m.ksi}  +{m.attestation_count}")
    if manifest_result.skipped_unknown_ksi:
        # Primitive already deduplicates; join for display.
        skipped = ", ".join(manifest_result.skipped_unknown_ksi)
        typer.echo(f"  skipped manifest(s) for unknown KSI(s): {skipped}")

    # Priority 0 (2026-04-27): warn the user when an HCL-mode scan is hitting
    # a module-composed codebase. Detectors look at root-level resource blocks
    # only; resources defined inside upstream modules (the dominant ICP-A
    # pattern) are invisible without plan-JSON expansion. The 2026-04-27
    # dogfood pass against `aws-ia/terraform-aws-eks-blueprints/patterns/
    # blue-green-upgrade` is the worked example: 11 module calls, 9 resources,
    # 30 detectors, 1 firing. Plan-mode scans never trigger this warning
    # because module_calls defaults to 0 there (modules are already expanded).
    if plan_path is None and scan_result.should_recommend_plan_json:
        typer.echo("")
        typer.echo(
            f"  ⚠ {scan_result.module_calls} module calls detected; "
            f"detector coverage is limited in HCL mode."
        )
        typer.echo(
            "    Detectors look at root-level `resource` declarations only. Resources defined"
        )
        typer.echo("    inside upstream modules (the dominant ICP-A pattern) are invisible without")
        typer.echo("    plan-JSON expansion. For full coverage:")
        typer.echo("      terraform init")
        typer.echo("      terraform plan -out plan.bin")
        typer.echo("      terraform show -json plan.bin > plan.json")
        typer.echo("      efterlev scan --plan plan.json")
        typer.echo("    Trade-off: plan-JSON gives full module coverage but `terraform show -json`")
        typer.echo("    output doesn't preserve HCL line numbers, so citations land at file-level")
        typer.echo("    only (source_lines: null in JSON sidecars). Line recovery is on the")
        typer.echo("    v0.2.0 roadmap.")
    elif plan_path is not None:
        # Plan-JSON mode in use — surface the same trade-off so the user
        # understands why citations carry no line numbers. v0.1.5 only
        # printed this when RECOMMENDING plan-JSON, leaving plan-JSON
        # users without any explanation for the file-level-only citations.
        typer.echo("")
        typer.echo(
            "  note: plan-JSON mode — full module coverage, but `terraform show -json` doesn't"
        )
        typer.echo("    preserve HCL line numbers, so citations land at file-level only")
        typer.echo("    (source_lines: null in JSON sidecars). Line recovery is on the v0.2.0")
        typer.echo("    roadmap.")

    # F2 (v0.1.12): when `--target` sits below a `.github/workflows/` ancestor
    # and no workflows were parsed in this run, GitHub-source detectors silently
    # contributed zero evidence. Surface the ancestor + recommended re-scan so
    # the under-coverage doesn't hide. Documented v0.1.x footgun; affected real
    # repos with `infra/terraform/`-style layouts.
    if workflow_result.workflows_parsed == 0:
        wf_ancestor = _ancestor_with_github_workflows(root)
        if wf_ancestor is not None:
            typer.echo("")
            typer.echo(
                f"  ⚠ found `.github/workflows/` at {wf_ancestor} but `--target {root}` "
                f"sits below it; GitHub-source detectors skipped this scan."
            )
            typer.echo(
                f"    For full coverage, scan from the repo root: "
                f"`efterlev scan --target {wf_ancestor}` "
                f"(`.tf` files under `--target` are still found via rglob)."
            )

    # F4 (v0.1.12): files parsed successfully but specific attribute
    # expressions couldn't be evaluated (the dominant case is
    # `jsonencode(...)` and `${...}` interpolations — python-hcl2 doesn't
    # evaluate Terraform expressions). Surface the plan-JSON hint at the
    # CLI layer rather than burying the `present="unparseable"` value in
    # individual Evidence records. Independent of parse_failures (which
    # is file-level), so emit even when no files failed outright. Skip
    # when already in plan-JSON mode — there nothing further to recommend.
    if plan_path is None:
        unparseable_records = sum(
            1 for ev in scan_result.evidence if any(v == "unparseable" for v in ev.content.values())
        )
        if unparseable_records > 0:
            typer.echo("")
            typer.echo(
                f"  ⚠ {unparseable_records} evidence record(s) contain unparseable "
                f"attribute values (e.g., `jsonencode(...)`, `${{...}}` interpolations)."
            )
            typer.echo("    python-hcl2 doesn't evaluate Terraform expressions; for accurate")
            typer.echo("    evaluation, use plan-JSON mode:")
            typer.echo(
                "      terraform plan -out plan.bin && terraform show -json plan.bin > plan.json"
            )
            typer.echo("      efterlev scan --plan plan.json")

    if scan_result.parse_failures:
        # Surface unparseable files structurally so the user knows what was
        # skipped without grepping logs. Truncate the list at 10 to keep the
        # CLI output skimmable; the structured output (JSON, MCP) carries the
        # full list. python-hcl2 lags upstream Terraform syntax — for codebases
        # with persistent failures, plan-JSON mode (`--plan plan.json`) is the
        # workaround since plan-JSON is HashiCorp-emitted.
        typer.echo("")
        typer.echo(
            f"  ⚠ files skipped due to parse error: {scan_result.files_failed} "
            f"(scan continued with the {scan_result.resources_parsed} resources "
            f"that did parse)"
        )
        for fail in scan_result.parse_failures[:10]:
            typer.echo(f"    {fail.file}: {fail.reason}")
        if scan_result.files_failed > 10:
            typer.echo(f"    … and {scan_result.files_failed - 10} more")
        typer.echo("    For codebases with persistent failures, try plan-JSON mode:")
        typer.echo(
            "      terraform plan -out plan.bin && terraform show -json plan.bin > plan.json"
        )
        typer.echo("      efterlev scan --plan plan.json")

    # Hard-fail only if EVERY .tf file failed to parse — partial success is
    # the design (see ScanTerraformOutput.parse_failures). Zero resources +
    # zero failures = empty repo (legitimate; not a failure).
    if scan_result.parse_failures and scan_result.resources_parsed == 0:
        typer.echo("", err=True)
        typer.echo("error: every .tf file failed to parse; nothing to scan.", err=True)
        raise typer.Exit(code=1)
    # v0.1.155 / #360: write-time evidence dedupe means `evidence_record_ids`
    # (records actually inserted into SQLite this scan) may be empty even
    # when detectors emitted evidence — re-scans of unchanged source skip
    # the insert and the dedupe path returns the existing record. Surface
    # the dedupe explicitly so the user sees the scan ran and how it lined
    # up with what's already in the store.
    if scan_result.evidence_record_ids or scan_result.evidence:
        typer.echo("")
        if verbose:
            typer.echo("Detector record IDs (pass to `efterlev provenance show`):")
            for rid, ev in zip(scan_result.evidence_record_ids, scan_result.evidence, strict=False):
                # Include the short detector id so records with identical
                # resource_name across detectors (e.g. "cloudtrail" = trail,
                # bucket, SSE, backup-retention) are distinguishable in the
                # listing.
                short_det = (
                    ev.detector_id.split(".", 1)[1] if "." in ev.detector_id else ev.detector_id
                )
                resource_name = ev.content.get("resource_name", "—")
                typer.echo(f"  {rid}  {short_det:<38}  {resource_name}")
        else:
            new_count = len(scan_result.evidence_record_ids)
            total_count = len(scan_result.evidence)
            deduped = total_count - new_count
            if new_count == total_count and new_count > 0:
                typer.echo(
                    f"{new_count} record(s) written to "
                    f"`.efterlev/store.db` — pass `--verbose` to print each ID, or "
                    f"feed any to `efterlev provenance show <id>`."
                )
            elif new_count == 0 and total_count > 0:
                typer.echo(
                    f"{total_count} evidence record(s) re-emitted by detectors; "
                    f"all match records already in `.efterlev/store.db` "
                    f"(nothing new to write)."
                )
            else:
                typer.echo(
                    f"{new_count} new record(s) written to `.efterlev/store.db`; "
                    f"{deduped} re-emitted record(s) matched existing entries (deduped)."
                )

    # ConMon Lite v0 (DECISIONS 2026-05-11 PR #237): emit a JSON sidecar
    # of this scan's evidence records so `efterlev scan-diff` can compare
    # two scans across branches. Mirrors the gap/documentation/remediation
    # sidecar pattern. The sidecar is the input format the PR-delta
    # workflow uses; the provenance store remains the source of truth for
    # within-workspace queries.
    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    scan_timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    scan_sidecar_path = reports_dir / f"scan-{scan_timestamp}.json"
    scan_sidecar_payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now().astimezone().isoformat(),
        "scan_root": str(root),
        "scan_mode": "plan" if plan_path is not None else "hcl",
        "summary": {
            "detectors_run": scan_result.detectors_run + workflow_result.detectors_run,
            "evidence_count": total_evidence,
            "manifests_loaded": manifest_result.manifests_loaded,
        },
        "evidence": [
            {
                "evidence_id": ev.evidence_id,
                "detector_id": ev.detector_id,
                "ksis_evidenced": list(ev.ksis_evidenced),
                "controls_evidenced": list(ev.controls_evidenced),
                "source_ref": ev.source_ref.model_dump(mode="json"),
                "content": ev.content,
            }
            for ev in (list(scan_result.evidence) + list(workflow_result.evidence))
        ],
    }
    scan_sidecar_path.write_text(
        json.dumps(scan_sidecar_payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    typer.echo(f"  JSON sidecar:        {scan_sidecar_path}")


@app.command("import-security-hub")
def import_security_hub(
    findings: Path = typer.Argument(
        ...,
        help=(
            "Path to an AWS Security Hub ASFF JSON file. Typically produced by "
            "`aws securityhub get-findings --output json > findings.json`. The "
            "tool does NOT call AWS APIs directly — local-first posture intact."
        ),
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose `.efterlev/` store receives the Evidence records.",
    ),
) -> None:
    """Ingest AWS Security Hub ASFF findings as Evidence records.

    Parses the ASFF JSON, looks up each finding's GeneratorId in the
    vendored mapping table, and writes one Evidence record per mapped
    finding into the workspace's provenance store.

    Findings whose GeneratorId is unmapped are reported but not emitted
    (no fabrication, same posture as `generate_poam_oscal`'s
    `skipped_unknown_ksi`).

    Honest scope:
    - File-based ingestion only. No AWS API calls. Customer runs
      `aws securityhub get-findings`; Efterlev consumes the JSON.
    - PASSED + FAILED findings both emit Evidence; NOT_AVAILABLE
      skipped (no signal).
    """
    if not findings.is_file():
        typer.echo(f"error: ASFF findings file not found: {findings}", err=True)
        raise typer.Exit(code=1)

    from efterlev.imports.security_hub import (
        IngestSecurityHubInput,
        ingest_security_hub,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    with ProvenanceStore(root) as store, active_store(store):
        result = ingest_security_hub(IngestSecurityHubInput(asff_path=findings))
        for ev in result.evidence:
            store.write_record(
                payload=ev.model_dump(mode="json"),
                record_type="evidence",
                primitive="ingest_security_hub@0.1.0",
            )

    typer.echo(f"Imported Security Hub ASFF findings from {findings}")
    typer.echo(f"  findings total:    {result.findings_total}")
    typer.echo(f"  evidence emitted:  {result.findings_emitted}")
    if result.skipped_status_not_available:
        typer.echo(
            f"  skipped (NOT_AVAILABLE): {result.skipped_status_not_available}",
            err=True,
        )
    if result.skipped_unmapped_generator_ids:
        typer.echo(
            "  skipped (unmapped generator-id):",
            err=True,
        )
        for gid in result.skipped_unmapped_generator_ids:
            typer.echo(f"    - {gid}", err=True)
        typer.echo(
            "  to expand coverage: see src/efterlev/imports/security_hub/mapping.yaml",
            err=True,
        )


@app.command("import-prowler")
def import_prowler_cli(
    findings: Path = typer.Argument(
        ...,
        help=(
            "Path to a Prowler native JSON output file (the default of "
            "`prowler aws -M json`). The tool does NOT call AWS APIs "
            "directly — local-first posture intact."
        ),
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose `.efterlev/` store receives the Evidence records.",
    ),
) -> None:
    """Ingest Prowler native JSON findings as Evidence records.

    Sibling to `efterlev import-security-hub` and `efterlev import-config`.
    Consumes Prowler's native JSON shape (CheckID + Status PASS/FAIL/MANUAL)
    rather than its ASFF translation — Prowler-specific fields like
    Risk and Remediation come through, and customers running Prowler
    in multi-tool aggregation workflows skip the ASFF translation step.

    Honest scope:
    - File-based ingestion only. No Prowler invocation. Customer runs
      `prowler aws -M json -o findings.json`; Efterlev consumes the JSON.
    - 8 mappings ship; expand via `src/efterlev/imports/prowler/mapping.yaml`.
    """
    if not findings.is_file():
        typer.echo(f"error: Prowler findings file not found: {findings}", err=True)
        raise typer.Exit(code=1)

    from efterlev.imports.prowler import (
        IngestProwlerInput,
        ingest_prowler,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    with ProvenanceStore(root) as store, active_store(store):
        result = ingest_prowler(IngestProwlerInput(prowler_path=findings))
        for ev in result.evidence:
            store.write_record(
                payload=ev.model_dump(mode="json"),
                record_type="evidence",
                primitive="ingest_prowler@0.1.0",
            )

    typer.echo(f"Imported Prowler findings from {findings}")
    typer.echo(f"  findings total:    {result.findings_total}")
    typer.echo(f"  evidence emitted:  {result.findings_emitted}")
    if result.skipped_manual_status:
        typer.echo(
            f"  skipped (MANUAL status): {result.skipped_manual_status}",
            err=True,
        )
    if result.skipped_unmapped_check_ids:
        typer.echo("  skipped (unmapped CheckID):", err=True)
        for cid in result.skipped_unmapped_check_ids:
            typer.echo(f"    - {cid}", err=True)
        typer.echo(
            "  to expand coverage: see src/efterlev/imports/prowler/mapping.yaml",
            err=True,
        )


@app.command("import-config")
def import_config_cli(
    evaluations: Path = typer.Argument(
        ...,
        help=(
            "Path to an AWS Config evaluations JSON file. Typically "
            "produced by `aws configservice get-compliance-details-by-config-rule "
            "--config-rule-name <name> --output json > evaluations.json`. The tool "
            "does NOT call AWS APIs directly — local-first posture intact."
        ),
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose `.efterlev/` store receives the Evidence records.",
    ),
) -> None:
    """Ingest AWS Config evaluations as Evidence records.

    Sibling to `efterlev import-security-hub`. Both ingest paths
    write into the same provenance store; the Gap Agent reasons
    over IaC + runtime evidence uniformly.

    Honest scope:
    - File-based ingestion only. No AWS API calls.
    """
    if not evaluations.is_file():
        typer.echo(f"error: AWS Config evaluations file not found: {evaluations}", err=True)
        raise typer.Exit(code=1)

    from efterlev.imports.config import (
        IngestConfigInput,
        ingest_config,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    with ProvenanceStore(root) as store, active_store(store):
        result = ingest_config(IngestConfigInput(config_path=evaluations))
        for ev in result.evidence:
            store.write_record(
                payload=ev.model_dump(mode="json"),
                record_type="evidence",
                primitive="ingest_config@0.1.0",
            )

    typer.echo(f"Imported AWS Config evaluations from {evaluations}")
    typer.echo(f"  evaluations total:  {result.evaluations_total}")
    typer.echo(f"  evidence emitted:   {result.evaluations_emitted}")
    if result.skipped_insufficient_data:
        typer.echo(
            f"  skipped (INSUFFICIENT_DATA): {result.skipped_insufficient_data}",
            err=True,
        )
    if result.skipped_unmapped_config_rule_names:
        typer.echo("  skipped (unmapped Config rule):", err=True)
        for name in result.skipped_unmapped_config_rule_names:
            typer.echo(f"    - {name}", err=True)
        typer.echo(
            "  to expand coverage: see src/efterlev/imports/config/mapping.yaml",
            err=True,
        )


@app.command("scan-diff")
def scan_diff(
    prior: Path = typer.Argument(
        ...,
        help=(
            "Path to a prior scan-result JSON sidecar (e.g. "
            "efterlev-out/reports/scan-<ts>.json on v0.1.160+; "
            ".efterlev/reports/scan-<ts>.json on pre-v0.1.160 stores)."
        ),
    ),
    current: Path = typer.Argument(
        ...,
        help="Path to the current scan-result JSON sidecar.",
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help=(
            "Path to the workspace whose efterlev-out/reports/ will receive "
            "the diff outputs (v0.1.160+ visible-output split)."
        ),
    ),
    base_branch: str = typer.Option(
        "",
        "--base-branch",
        help=(
            "Optional base-branch label for the markdown PR-comment header (e.g. `main`). "
            "Empty defaults to the generic 'base branch' phrase."
        ),
    ),
    print_markdown: bool = typer.Option(
        False,
        "--print-markdown",
        help="Print the markdown PR-comment to stdout (in addition to writing files).",
    ),
) -> None:
    """Diff two scan-result JSON sidecars at the per-detector gap-emission layer.

    Per DECISIONS 2026-05-11 "Tier 4 #1 design: ConMon Lite", surfaces
    new gaps + modified gaps + resolved gaps between two scans (typically
    base-branch vs PR-branch). Resolved gaps appear in the JSON sidecar
    and HTML report but are excluded from the markdown PR-comment view
    (regression focus per Decision #3).

    Outputs (v0.1.160+ visible-output split):
      - efterlev-out/reports/scan-diff-<ts>.html
      - efterlev-out/reports/scan-diff-<ts>.json
      - markdown PR-comment to stdout if --print-markdown

    Exit code: 0 if no new or modified gaps; 2 if either is non-empty
    (CI-friendly soft-fail signal — gating policy is a v1 follow-up).
    """
    from efterlev.reports import (
        compute_scan_diff,
        render_scan_diff_html,
        render_scan_diff_markdown,
    )

    if not prior.is_file():
        typer.echo(f"error: prior file not found: {prior}", err=True)
        raise typer.Exit(code=1)
    if not current.is_file():
        typer.echo(f"error: current file not found: {current}", err=True)
        raise typer.Exit(code=1)

    try:
        prior_data = json.loads(prior.read_text(encoding="utf-8"))
        current_data = json.loads(current.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        typer.echo(f"error: invalid JSON: {e}", err=True)
        raise typer.Exit(code=1) from e

    diff = compute_scan_diff(prior_data, current_data)

    typer.echo(f"Comparing {prior.name} → {current.name}")
    typer.echo(f"  new gaps:        {len(diff.new_gaps)}")
    typer.echo(f"  modified gaps:   {len(diff.modified_gaps)}")
    typer.echo(f"  resolved gaps:   {len(diff.resolved_gaps)}")

    root = target.resolve()
    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    generated_at = datetime.now().astimezone()

    html_path = reports_dir / f"scan-diff-{timestamp}.html"
    html_path.write_text(render_scan_diff_html(diff, generated_at=generated_at), encoding="utf-8")

    json_path = reports_dir / f"scan-diff-{timestamp}.json"
    json_path.write_text(json.dumps(diff.model_dump(), indent=2, sort_keys=True), encoding="utf-8")

    typer.echo("")
    typer.echo(f"HTML report:  {html_path}")
    typer.echo(f"JSON sidecar: {json_path}")

    if print_markdown:
        markdown = render_scan_diff_markdown(diff, base_branch=base_branch or None)
        typer.echo("")
        typer.echo(markdown)

    if diff.new_gaps or diff.modified_gaps:
        raise typer.Exit(code=2)


@app.command()
def poam(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Write the POA&M markdown to this file. "
            "Defaults to `efterlev-out/reports/poam/poam-<timestamp>.md` "
            "(v0.1.160+ visible-output split; was `.efterlev/reports/poam/`)."
        ),
    ),
    sort: str = typer.Option(
        "severity",
        "--sort",
        help=(
            "How to order POA&M items. `severity` (default): not_implemented "
            "(HIGH) first, then partial (MEDIUM); alphabetical within tier. "
            "`csx-ord`: order by KSI-CSX-ORD's prescribed initial-authorization "
            "sequence (MAS, ADS, UCM, …); items outside the prescribed sequence "
            "appear after, alphabetically."
        ),
    ),
) -> None:
    """Emit a POA&M markdown for every open (partial / not_implemented) KSI.

    Reads the latest Gap Agent classifications from the provenance store,
    resolves each KSI against the loaded FRMR, and renders a POA&M
    document with a summary table and per-item detail blocks. The output
    is deterministic — same inputs produce byte-identical markdown, so
    re-running is safe and diffable.

    DRAFT — every Reviewer field in each item is emitted as a
    `DRAFT — SET BEFORE SUBMISSION` placeholder. Severity is a
    starting-point heuristic (not_implemented → HIGH, partial →
    MEDIUM); reviewer confirms per internal risk framework before
    submission.

    Suitable for paste into Jira/Linear (their markdown-paste flows
    accept tables and per-item sections) or handing to a 3PAO alongside
    the FRMR attestation JSON.
    """
    from efterlev.agents import (
        count_duplicate_classification_runs,
        reconstruct_classifications_from_store,
    )
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.primitives.generate import (
        GeneratePoamMarkdownInput,
        PoamClassificationInput,
        generate_poam_markdown,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))

    with ProvenanceStore(root) as store, active_store(store):
        rows = store.iter_claims_by_metadata_kind("ksi_classification")
        duplicate_count = count_duplicate_classification_runs(rows)
        # v0.1.147 / #352: filter out stale classifications for KSI ids not
        # in the current baseline. Pre-v0.1.146 the gap agent could persist
        # malformed ids (e.g. KSI-SUS instead of KSI-IAM-SUS); old records
        # remain in the store and would otherwise leak through dedup.
        classifications = reconstruct_classifications_from_store(
            rows, baseline_ksi_ids=set(frmr_doc.indicators.keys())
        )
        if duplicate_count > 0:
            typer.echo(
                f"note: deduped {duplicate_count} duplicate classification(s) "
                f"from prior `agent gap` runs (latest-wins). "
                f"To see every run pass `--include-duplicate-runs`.",
                err=True,
            )
        if not classifications:
            typer.echo(
                "error: 0 Gap Agent classifications in the store. The Gap Agent "
                "either hasn't run yet, or ran with no evidence to classify "
                "(check `efterlev scan` first if you skipped that stage).",
                err=True,
            )
            raise typer.Exit(code=1)

        # Priority 4.2 (2026-04-27): build a {evidence_id -> boundary_state}
        # map from the store so we can drop POA&M items whose cited evidence
        # is entirely `out_of_boundary`. Out-of-scope findings are not in
        # the customer's FedRAMP boundary and don't belong in the POA&M.
        # `boundary_undeclared` and classifications with no cited evidence
        # (typical for `not_implemented` against a procedural KSI) flow
        # through — undeclared means "we don't know your scope" and an
        # uncited not_implemented is a real gap that needs tracking.
        evidence_boundary_state: dict[str, str] = {}
        for _rid, payload in store.iter_evidence():
            ev_id = payload.get("evidence_id")
            state = payload.get("boundary_state", "boundary_undeclared")
            if isinstance(ev_id, str):
                evidence_boundary_state[ev_id] = state

        kept_classifications = []
        skipped_out_of_boundary = 0
        for c in classifications:
            if not c.evidence_ids:
                # Uncited — keep. Real gap, not boundary-filterable.
                kept_classifications.append(c)
                continue
            states = [evidence_boundary_state.get(e, "boundary_undeclared") for e in c.evidence_ids]
            if all(s == "out_of_boundary" for s in states):
                skipped_out_of_boundary += 1
                continue
            kept_classifications.append(c)

        poam_inputs = [
            PoamClassificationInput(
                ksi_id=c.ksi_id,
                status=c.status,
                rationale=c.rationale,
                evidence_ids=list(c.evidence_ids),
                claim_record_id=None,  # the reconstructed shape doesn't carry record_id
            )
            for c in kept_classifications
        ]
        if sort not in ("severity", "csx-ord"):
            typer.echo(
                f"error: --sort must be 'severity' or 'csx-ord' (got '{sort}').",
                err=True,
            )
            raise typer.Exit(code=2)
        if sort == "csx-ord" and not frmr_doc.csx_ord_sequence:
            typer.echo(
                "warning: workspace's FRMR cache predates CSX-ORD support; "
                "the prescribed-sequence sort will fall back to alphabetical. "
                "Run `efterlev init --force` to refresh the cache.",
                err=True,
            )
        result = generate_poam_markdown(
            GeneratePoamMarkdownInput(
                classifications=poam_inputs,
                indicators=frmr_doc.indicators,
                baseline_id="fedramp-20x-moderate",
                frmr_version=frmr_doc.version,
                sort_mode=sort,  # type: ignore[arg-type]
                csx_ord_sequence=list(frmr_doc.csx_ord_sequence),
                out_of_boundary_excluded_count=skipped_out_of_boundary,
            )
        )

    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    # POA&M outputs land under `reports/poam/` (subdirectory) so the file
    # tree matches the runbook docs and so per-report-type artifacts cluster
    # cleanly. Pre-v0.1.6 wrote flat `reports/poam-<ts>.md`; the runbook
    # already pointed at the subdir form, leaving consumers chasing a path
    # that didn't exist.
    output_path = output or (_poam_dir(root) / f"poam-{timestamp}.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result.markdown, encoding="utf-8")

    typer.echo(f"POA&M: {output_path.resolve()}")
    typer.echo(f"  open items:       {result.item_count}")
    # v0.1.8: always print the out-of-boundary count, even when 0. A "0"
    # is itself a useful signal — it says either no boundary is declared
    # OR the boundary doesn't drop any open findings. Pre-v0.1.8 this
    # line was conditional, so users couldn't tell the difference between
    # "we considered the boundary and it didn't matter" and "we never
    # checked." Negative space is informative.
    typer.echo(
        f"  out-of-boundary:  {skipped_out_of_boundary} item(s) excluded "
        "(their cited evidence is entirely out_of_boundary)"
    )
    if result.skipped_unknown_ksi:
        skipped = ", ".join(result.skipped_unknown_ksi)
        typer.echo(f"  skipped unknown:  {skipped}")


@app.command()
def vdr(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    output_format: str = typer.Option(
        "both",
        "--format",
        help=(
            "Output format. `json` (machine-readable, RFC-0012-shaped), "
            "`markdown` (3PAO-readable), or `both` (default — emits both side "
            "by side, same content). v0.1.162 / #367."
        ),
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Write VDR to this file (single-format only; pass `--format json` "
            "or `--format markdown`). Default location is "
            "`efterlev-out/reports/vdr/vdr-<timestamp>.{json,md}`."
        ),
    ),
) -> None:
    """Emit a Vulnerability Detection & Response (VDR) report.

    VDR is the artifact FedRAMP 20x is moving toward as a replacement for
    the traditional POA&M, per RFC-0012 (Continuous Vulnerability
    Management Standard; closed for public comment 2025-08-21). v0.1.162
    ships an AHEAD-OF-FINALIZATION shape so customers can preview the
    output before the RFC lands; the JSON pins `vdr_schema_version` so
    consumers can detect breaking changes when the RFC standardizes.

    Each entry corresponds to a `partial` or `not_implemented` KSI
    classification and carries the RFC-0012 required fields: internal
    identifier, CVE IDs, detection timestamp, mitigation/remediation
    deadlines (heuristic — reviewer adjusts), internet-reachability
    status (defaults to "REVIEW" since IaC scanners can't reliably
    infer this), exploitability/impact, mitigation/remediation plans,
    and actions taken.

    Output is deterministic — same inputs produce byte-identical JSON
    and markdown, so re-running is safe and diffable.

    Mirrors the `efterlev poam` command's posture. Both can coexist in
    a submission package today; once RFC-0012 finalizes and the
    program migrates, this becomes the primary artifact.
    """
    from efterlev.agents import (
        count_duplicate_classification_runs,
        reconstruct_classifications_from_store,
    )
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.primitives.generate import (
        GenerateVdrReportInput,
        VdrClassificationInput,
        generate_vdr_report,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    if output_format not in ("json", "markdown", "both"):
        typer.echo(
            f"error: --format must be 'json', 'markdown', or 'both' (got '{output_format}').",
            err=True,
        )
        raise typer.Exit(code=2)
    if output is not None and output_format == "both":
        typer.echo(
            "error: --output is only valid with --format json or --format markdown "
            "(not 'both' — pick one explicit format when overriding the path).",
            err=True,
        )
        raise typer.Exit(code=2)

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))

    with ProvenanceStore(root) as store, active_store(store):
        rows = store.iter_claims_by_metadata_kind("ksi_classification")
        duplicate_count = count_duplicate_classification_runs(rows)
        classifications = reconstruct_classifications_from_store(
            rows, baseline_ksi_ids=set(frmr_doc.indicators.keys())
        )
        if duplicate_count > 0:
            typer.echo(
                f"note: deduped {duplicate_count} duplicate classification(s) "
                f"from prior `agent gap` runs (latest-wins).",
                err=True,
            )
        if not classifications:
            typer.echo(
                "error: 0 Gap Agent classifications in the store. The Gap Agent "
                "either hasn't run yet, or ran with no evidence to classify "
                "(check `efterlev scan` first if you skipped that stage).",
                err=True,
            )
            raise typer.Exit(code=1)

        # Same boundary filter as POA&M — out_of_boundary findings don't
        # belong in the VDR (they're out of the FedRAMP boundary scope).
        evidence_boundary_state: dict[str, str] = {}
        for _rid, payload in store.iter_evidence():
            ev_id = payload.get("evidence_id")
            state = payload.get("boundary_state", "boundary_undeclared")
            if isinstance(ev_id, str):
                evidence_boundary_state[ev_id] = state

        kept_classifications = []
        skipped_out_of_boundary = 0
        for c in classifications:
            if not c.evidence_ids:
                kept_classifications.append(c)
                continue
            states = [evidence_boundary_state.get(e, "boundary_undeclared") for e in c.evidence_ids]
            if all(s == "out_of_boundary" for s in states):
                skipped_out_of_boundary += 1
                continue
            kept_classifications.append(c)

        # v0.1.163 / #368: harvest CVE IDs from cited evidence so they
        # populate the VDR entry's RFC-0012 `cve_ids` field. Runtime-
        # evidence imports (Security Hub ASFF Vulnerabilities[]) carry
        # CVEs in `Evidence.content["cve_ids"]`. IaC detectors don't —
        # they emit empty lists by default, harmless.
        evidence_cves: dict[str, list[str]] = {}
        for _rid, payload in store.iter_evidence():
            ev_id = payload.get("evidence_id")
            content = payload.get("content", {})
            cves = content.get("cve_ids") if isinstance(content, dict) else None
            if isinstance(ev_id, str) and isinstance(cves, list):
                evidence_cves[ev_id] = [c for c in cves if isinstance(c, str)]

        def _harvest_cves(evidence_ids: list[str]) -> list[str]:
            """Collect deduped CVE IDs from every cited evidence record."""
            seen: set[str] = set()
            result: list[str] = []
            for eid in evidence_ids:
                for cve in evidence_cves.get(eid, []):
                    if cve not in seen:
                        seen.add(cve)
                        result.append(cve)
            return result

        vdr_inputs = [
            VdrClassificationInput(
                ksi_id=c.ksi_id,
                status=c.status,
                rationale=c.rationale,
                evidence_ids=list(c.evidence_ids),
                cve_ids=_harvest_cves(list(c.evidence_ids)),
            )
            for c in kept_classifications
        ]

        # Render inside the active_store block so the @primitive wrapper
        # can persist its invocation record (same pattern as POA&M).
        # JSON + markdown are deterministic and cheap; emit both when
        # --format=both.
        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        written: list[Path] = []
        entry_count = 0

        formats_to_emit: list[str] = (
            ["json", "markdown"] if output_format == "both" else [output_format]
        )
        for fmt in formats_to_emit:
            result = generate_vdr_report(
                GenerateVdrReportInput(
                    classifications=vdr_inputs,
                    indicators=frmr_doc.indicators,
                    baseline_id="fedramp-20x-moderate",
                    frmr_version=frmr_doc.version,
                    output_format=fmt,  # type: ignore[arg-type]
                    out_of_boundary_excluded_count=skipped_out_of_boundary,
                )
            )
            entry_count = result.entry_count
            ext = "json" if fmt == "json" else "md"
            if output is not None:
                target_path = output
            else:
                from efterlev.paths import vdr_dir as _vdr_dir

                target_path = _vdr_dir(root) / f"vdr-{timestamp}.{ext}"
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(result.rendered, encoding="utf-8")
            written.append(target_path)
            skipped_msg = (
                f"  skipped unknown: {', '.join(result.skipped_unknown_ksi)}"
                if result.skipped_unknown_ksi
                else ""
            )
            if skipped_msg:
                typer.echo(skipped_msg, err=True)

    for w in written:
        typer.echo(f"VDR ({w.suffix.lstrip('.')}): {w.resolve()}")
    typer.echo(f"  entries:          {entry_count}")
    typer.echo(
        f"  out-of-boundary:  {skipped_out_of_boundary} item(s) excluded "
        "(their cited evidence is entirely out_of_boundary)"
    )
    typer.echo(
        "  note: this is the RFC-0012-shaped (Vulnerability Detection & Response) "
        "artifact, emitted AHEAD of finalization. Schema version is pinned "
        "in the JSON output via `vdr_schema_version` so consumers can detect "
        "breaking changes when the RFC standardizes."
    )


@app.command()
def inventory(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    output_format: str = typer.Option(
        "both",
        "--format",
        help=(
            "Output format. `json` (machine-readable, RFC-0017-shaped), "
            "`html` (one-page table, 3PAO-readable), or `both` (default — "
            "emits both side by side, same content). v0.1.164 / #369."
        ),
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help=(
            "Write the inventory to this file (single-format only; pass "
            "`--format json` or `--format html`). Default location is "
            "`efterlev-out/reports/inventory/inventory-<timestamp>.{json,html}`."
        ),
    ),
) -> None:
    """Emit a consolidated resource inventory.

    RFC-0017 (Persistent Validation and Assessment Standard) names
    "consolidated resource inventory being validated" as one of the
    5 required items per Key Security Indicator. v0.1.164 promotes
    this data — already captured in every Evidence record's
    `source_ref` + `content.resource_type` + `content.resource_name`
    — to a first-class artifact a 3PAO can read.

    One row per (resource_type, resource_name) pair: aggregates
    evidence_count, ksi_coverage, controls_coverage, boundary_state,
    and every source file:line range that emitted evidence about the
    resource. Deterministic; no LLM call.

    Two outputs by default:
      - efterlev-out/reports/inventory/inventory-<ts>.json (machine)
      - efterlev-out/reports/inventory/inventory-<ts>.html (one-page)

    Hand the HTML to a 3PAO scoping meeting; feed the JSON to any
    OSCAL importer.
    """
    from efterlev.primitives.generate import (
        GenerateInventoryInput,
        generate_inventory,
    )
    from efterlev.provenance import ProvenanceStore, active_store

    if output_format not in ("json", "html", "both"):
        typer.echo(
            f"error: --format must be 'json', 'html', or 'both' (got '{output_format}').",
            err=True,
        )
        raise typer.Exit(code=2)
    if output is not None and output_format == "both":
        typer.echo(
            "error: --output is only valid with --format json or --format html "
            "(not 'both' — pick one explicit format when overriding the path).",
            err=True,
        )
        raise typer.Exit(code=2)

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    with ProvenanceStore(root) as store, active_store(store):
        # Pull every evidence payload — the primitive does the aggregation.
        payloads = [payload for _rid, payload in store.iter_evidence()]

        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        written: list[Path] = []
        entry_count = 0
        skipped = 0
        skipped_manifest = 0

        formats_to_emit: list[str] = (
            ["json", "html"] if output_format == "both" else [output_format]
        )
        for fmt in formats_to_emit:
            result = generate_inventory(
                GenerateInventoryInput(
                    evidence_payloads=payloads,
                    output_format=fmt,  # type: ignore[arg-type]
                )
            )
            entry_count = result.entry_count
            skipped = result.skipped_no_resource
            skipped_manifest = result.skipped_manifest
            ext = "json" if fmt == "json" else "html"
            if output is not None:
                target_path = output
            else:
                from efterlev.paths import inventory_dir as _inv_dir

                target_path = _inv_dir(root) / f"inventory-{timestamp}.{ext}"
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(result.rendered, encoding="utf-8")
            written.append(target_path)

    for w in written:
        typer.echo(f"Inventory ({w.suffix.lstrip('.')}): {w.resolve()}")
    typer.echo(f"  resources:        {entry_count}")
    if skipped_manifest:
        # Expected, not drift: procedural manifest attestations have no resource.
        typer.echo(
            f"  manifests:        {skipped_manifest} procedural attestation(s) "
            f"(no resource — counted toward KSI coverage, not the resource inventory)"
        )
    if skipped:
        typer.echo(
            f"  skipped:          {skipped} detector evidence record(s) had no "
            f"resource_type/resource_name in content (possible detector shape drift)"
        )
    typer.echo(
        "  note: consolidated resource inventory per RFC-0017 "
        "(Persistent Validation and Assessment Standard) — "
        "one of the 5 required items per KSI."
    )


def _new_scan_id() -> str:
    """UTC-timestamped scan identifier. Used to tag redaction-ledger entries
    so a user can later run `efterlev redaction review --scan-id <ts>` to see
    what got redacted on a specific run. Filesystem-safe, second-resolution
    (race-safe for typical operator cadence).
    """
    return datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")


def _write_scan_redaction_log(ledger_obj: Any, root: Path, scan_id: str) -> None:
    """Dump a RedactionLedger to `.efterlev/redacted.log` and echo a summary.

    The log is opened with 0600 perms at create time and re-chmodded to
    0600 on every append. An empty ledger is a no-op. See DECISIONS
    2026-04-23 "Redaction audit log + review CLI" for the full design.
    """
    from efterlev.llm.scrubber import write_redaction_log

    count = write_redaction_log(ledger_obj, root / ".efterlev" / "redacted.log", scan_id=scan_id)
    if count > 0:
        pattern_counts = ledger_obj.pattern_counts()
        summary = ", ".join(f"{n}x{name}" for name, n in sorted(pattern_counts.items()))
        typer.echo(
            f"Redacted {count} secret(s) from prompt content ({summary}); "
            f"audit: `efterlev redaction review --scan-id {scan_id}`."
        )


def _validate_dry_run_args(dump_prompt: Path | None, force: bool) -> None:
    """Pre-flight check for the dry-run flag combinations across agent commands.
    `--force` requires `--dump-prompt`; otherwise it has nothing to overwrite."""
    if force and dump_prompt is None:
        typer.echo("error: --force requires --dump-prompt PATH", err=True)
        raise typer.Exit(code=2)


def _dump_dry_run_session(
    session: Any,
    dump_prompt_path: Path | None,
    force: bool,
) -> None:
    """Serialize a DryRunSession's captured prompts to stdout or a file.

    Stdout when `dump_prompt_path is None`. File otherwise — refusing
    to overwrite an existing file unless `force=True`. The file write
    prints a one-line "wrote N prompts" summary to stderr (so stdout
    stays clean for piping when `--dry-run` alone is used).

    See DECISIONS 2026-05-06 "Tier 1 #2b design" for the rationale on
    --force-required-for-overwrite (clobbering an audit packet is real
    harm in the regulated context this command targets).
    """
    payload = json.dumps(session.to_json_array(), indent=2)
    if dump_prompt_path is None:
        typer.echo(payload)
        return
    if dump_prompt_path.exists() and not force:
        typer.echo(
            f"error: {dump_prompt_path} exists; pass --force to overwrite",
            err=True,
        )
        raise typer.Exit(code=2)
    dump_prompt_path.parent.mkdir(parents=True, exist_ok=True)
    dump_prompt_path.write_text(payload, encoding="utf-8")
    typer.echo(
        f"wrote {len(session.prompts)} dry-run prompt(s) to {dump_prompt_path} "
        f"(~${session.total_cost_estimate_usd:.2f} estimated)",
        err=True,
    )


def _format_elapsed(seconds: float) -> str:
    """Render a wall-clock duration the way `report run` displays per-stage
    timings (v0.1.154 / #359). Sub-second → `0.4s`; sub-minute → `47.3s`;
    longer → `1m12s`. Keeps two-digit precision below a minute so the user
    can see the cache-hit speed-up clearly (~0.1s vs ~50s).
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, sec = divmod(int(seconds), 60)
    return f"{minutes}m{sec:02d}s"


def _format_gap_agent_summary(
    report: Any,  # GapReport — typed loosely to avoid a heavy import at module scope
    *,
    verbose: bool,
) -> list[str]:
    """Render `/agent gap` post-run output. v0.1.152 / #357 collapses the
    pre-v0.1.152 per-KSI dump (60 rows x 5+ lines each) into a status-count
    summary by default; `--verbose` restores the full rationale dump.

    Customer reported "don't show the detailed of all the classified KSI's,
    no one will read them in the terminal, it's too long" 2026-05-17. The
    HTML report and JSON sidecar still carry the full detail.
    """
    from collections import Counter

    lines: list[str] = [f"Gap Agent classified {len(report.ksi_classifications)} KSI(s):"]
    status_counts = Counter(clf.status for clf in report.ksi_classifications)
    # Severity order — partial + not_implemented (actionable) appear first.
    status_order = [
        "implemented",
        "partial",
        "not_implemented",
        "not_applicable",
        "evidence_layer_inapplicable",
    ]
    label_w = max((len(s) for s in status_counts), default=0)
    for status in status_order:
        n = status_counts.get(status, 0)
        if n == 0:
            continue
        lines.append(f"  {status.ljust(label_w)}  {n}")
    for status, n in status_counts.items():
        if status in status_order:
            continue
        lines.append(f"  {status.ljust(label_w)}  {n}")
    if verbose:
        lines.append("")
        for clf in report.ksi_classifications:
            lines.append(f"  {clf.ksi_id:<14}  {clf.status}")
            lines.append(f"                  {clf.rationale}")
    else:
        lines.append(
            "  (full per-KSI rationales in the HTML and JSON sidecar below; "
            "pass --verbose to print here)"
        )
    return lines


@agent_app.command("gap")
def agent_gap(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help=(
            "Print full SHA256 record IDs to the terminal. By default the "
            "per-claim record IDs are written to the JSON sidecar only — "
            "they're useful for `efterlev provenance show <id>` walks but "
            "overwhelming for first-time users skimming a gap run."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help=(
            "Build the assembled prompt(s) and exit without invoking the LLM. "
            "Prints a JSON array of literal Anthropic API request envelopes "
            "(one per LLM call the agent would have made), each augmented with "
            "an `_efterlev` metadata sub-object holding iteration index, label, "
            "and pre-run token + dollar-cost estimates. Audit-credibility primitive: "
            "a 3PAO can verify exactly what was sent to the LLM. No network call, "
            "no Claim writes to the store."
        ),
    ),
    dump_prompt: Path | None = typer.Option(
        None,
        "--dump-prompt",
        help=(
            "Write the dry-run JSON to PATH instead of stdout. Implies --dry-run. "
            "Refuses to overwrite an existing file unless --force also passed."
        ),
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing --dump-prompt PATH.",
    ),
    runs: int = typer.Option(
        1,
        "--runs",
        min=1,
        max=9,
        help=(
            "Run the Gap Agent this many times and reduce to a per-KSI "
            "majority verdict (ConMon Lite v1, DECISIONS 2026-05-11 "
            "PR #241). Default 1 (single-run, existing behavior). When "
            ">1, KSIs whose top vote count is below ceil(runs/2) are "
            "recorded as `flickering_ksis` in the JSON sidecar. Cost "
            "scales linearly: 3 runs = 3x Anthropic spend per branch."
        ),
    ),
) -> None:
    """Classify each KSI as implemented / partial / not implemented / NA."""
    from datetime import UTC
    from datetime import datetime as _dt

    from efterlev.agents import (
        GapAgent,
        GapAgentInput,
        detector_covered_ksis,
        in_scope_evidence,
    )
    from efterlev.agents.cost_summary import summarize_run_cost
    from efterlev.agents.dry_run import DryRunSession, active_dry_run
    from efterlev.config import load_config
    from efterlev.errors import AgentError, ConfigError
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.llm.scrubber import RedactionLedger, active_redaction_ledger
    from efterlev.models import Evidence
    from efterlev.provenance import ProvenanceStore, active_store

    _validate_dry_run_args(dump_prompt, force)
    is_dry_run = dry_run or dump_prompt is not None

    started_at = _dt.now(UTC)
    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    indicators = list(frmr_doc.indicators.values())

    # v0.1.171 / #377: skip KSIs already recorded CSP-inherited via
    # `efterlev scope apply`. The agent must not reclassify them — a
    # newer evidence-based claim would clobber the deterministic
    # inherited declaration in the store's latest-claim-per-KSI view.
    from efterlev.cli.scope_cli import inherited_ksis_in_store

    inherited = inherited_ksis_in_store(root)
    if inherited:
        before = len(indicators)
        indicators = [ind for ind in indicators if ind.id not in inherited]
        skipped = before - len(indicators)
        if skipped:
            typer.echo(
                f"Skipping {skipped} KSI(s) recorded CSP-inherited via "
                "`efterlev scope` (see `efterlev scope show`)."
            )

    try:
        config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    scan_id = _new_scan_id()
    ledger = RedactionLedger()

    try:
        with ProvenanceStore(root) as store:
            # Boundary enforcement at the agent-input layer (v0.1.219): drop
            # out_of_boundary evidence so the Gap Agent never reasons over or
            # cites out-of-scope resources (govnotes-demo gap #27 regression).
            # No-op when no boundary is declared. See gap.in_scope_evidence.
            evidence = in_scope_evidence(
                [Evidence.model_validate(p) for _rid, p in store.iter_evidence()]
            )
            if not evidence:
                typer.echo(
                    "error: 0 evidence records in the store. The scan either hasn't run "
                    "yet or ran and matched no resources — your target may have no "
                    "Terraform/.github-workflows files in scope, or the 45 detectors "
                    "may not apply to its resources. Run `efterlev scan --target <path>` "
                    "to verify.",
                    err=True,
                )
                raise typer.Exit(code=1)

            # Priority 0 (2026-04-27): when the scan was HCL-mode against a
            # module-composed codebase, pass the summary so narratives reflect
            # the coverage limitation. None when no scan_terraform* primitive
            # invocation exists (already guarded by the `not evidence` check
            # above, but kept defensive).
            from efterlev.primitives.scan import latest_scan_summary

            scan_summary = latest_scan_summary(store)

            dry_run_session = DryRunSession() if is_dry_run else None
            # ConMon Lite v1 (DECISIONS 2026-05-11 PR #241): when
            # --runs > 1, invoke the Gap Agent N times and aggregate
            # via per-KSI majority voting. Each run persists its own
            # Claims to the provenance store; the synthesized report
            # uses the LAST run's claim_record_ids (most-recently
            # persisted) and the FIRST run that voted majority for the
            # rationale + evidence_ids per KSI.
            with active_store(store), active_redaction_ledger(ledger):
                # v0.1.116: construct LLM client from workspace config so
                # `[llm].backend = "bedrock"` is actually honored. Prior
                # versions only read `config.llm.model` and let the agent
                # fall back to `get_default_client()` — which walks up from
                # cwd, finds no `.efterlev/config.toml` (CLI runs in the
                # caller's cwd, not the workspace), and defaults to Anthropic.
                # Bug surfaced by the v0.1.115 Bedrock+Nemotron benchmark.
                from efterlev.llm.factory import get_client_from_config

                # v0.1.151 / #356: pass workspace_root + cache_mode so the
                # LLM cache actually applies. Pre-v0.1.151 this callsite
                # silently bypassed the cache wrapper entirely.
                agent = GapAgent(
                    model=config.llm.model,
                    client=get_client_from_config(
                        config.llm, workspace_root=root, cache_mode=config.cache.mode
                    ),
                )
                # v0.1.86: install streaming-progress reporter when stderr
                # is a TTY. Surfaces "[gap] classifying KSI X/N: KSI-AAA-BBB"
                # lines during the ~60-90s LLM call. None in CI / piped
                # output so logs stay clean.
                from efterlev.agents.gap_progress import make_reporter_if_tty

                progress = make_reporter_if_tty(total_ksis=len(indicators))
                gap_input = GapAgentInput(
                    indicators=indicators,
                    evidence=evidence,
                    scan_summary=scan_summary,
                    progress_callback=progress,
                    # Deterministic detector-coverage signal so the agent
                    # classifies a covered-but-zero-evidence KSI as
                    # not_implemented, not evidence_layer_inapplicable
                    # (DECISIONS 2026-06-08).
                    detector_covered_ksis=detector_covered_ksis(),
                )
                run_reports: list = []
                with friendly_llm_error_handler():
                    if dry_run_session is not None:
                        # Dry-run path: a single prompt-dump pass is
                        # enough; multi-run dry-run would just print
                        # N copies of the same envelope.
                        with active_dry_run(dry_run_session):
                            run_reports.append(agent.run(gap_input))
                    else:
                        for _ in range(runs):
                            run_reports.append(agent.run(gap_input))

                # v0.1.86: print final progress-summary line if a reporter
                # was installed. Silent in CI (progress is None there).
                if progress is not None:
                    progress.finish()

            per_run_verdicts: dict[str, list[str]] = {}
            flickering_ksis: list[str] = []
            if runs > 1 and not is_dry_run:
                from efterlev.agents.multi_run import aggregate_gap_reports

                report, per_run_verdicts, flickering_ksis = aggregate_gap_reports(run_reports)
            else:
                report = run_reports[0]
                # Single-run path: per_run_verdicts is the trivial
                # one-entry-per-KSI map; flickering is empty.
                per_run_verdicts = {clf.ksi_id: [clf.status] for clf in report.ksi_classifications}
    except AgentError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    if is_dry_run:
        # Bail before any of the normal post-run output (HTML, JSON sidecar,
        # cost summary, "Next steps") — the dry-run dump IS the output.
        assert dry_run_session is not None  # for type narrowing
        _dump_dry_run_session(dry_run_session, dump_prompt, force)
        return

    for line in _format_gap_agent_summary(report, verbose=verbose):
        typer.echo(line)
    if report.unmapped_findings:
        typer.echo("")
        total = len(report.unmapped_findings)
        # v0.1.144 / #349: collapse the per-record dump that drowned the user
        # into a per-detector summary. Each unmapped record has structurally
        # the same note ("controls don't map to any KSI in the baseline"); the
        # actionable info is which detectors are emitting orphan evidence and
        # which controls. Group + count; show full list only with --verbose.
        by_detector: dict[str, dict[str, int]] = {}
        for um in report.unmapped_findings:
            # The deterministic note template begins "Detector <id> produced...";
            # extract <id> from the note. Robust to the few-token offset because
            # the format is fixed (see compute_unmapped_findings in gap_batching.py).
            words = um.note.split(" ", 2)
            detector_id = words[1] if len(words) > 1 and words[0] == "Detector" else "(unknown)"
            controls_key = ",".join(um.controls) or "(none)"
            by_detector.setdefault(detector_id, {}).setdefault(controls_key, 0)
            by_detector[detector_id][controls_key] += 1
        typer.echo(
            f"Unmapped findings: {total} record(s) from {len(by_detector)} "
            f"detector(s) whose controls don't map to any KSI in the baseline."
        )
        if verbose:
            for detector_id in sorted(by_detector):
                for controls_key, count in sorted(by_detector[detector_id].items()):
                    typer.echo(
                        f"  {detector_id:<40}  controls={controls_key:<20}  ({count} record(s))"
                    )
        else:
            top = sorted(
                ((d, sum(c.values())) for d, c in by_detector.items()),
                key=lambda x: x[1],
                reverse=True,
            )[:5]
            for detector_id, count in top:
                ctrls = sorted(by_detector[detector_id].keys())
                ctrls_str = ", ".join(ctrls[:3]) + (
                    f", +{len(ctrls) - 3}" if len(ctrls) > 3 else ""
                )
                typer.echo(f"  {detector_id:<40}  controls=[{ctrls_str}]  ({count} record(s))")
            if len(by_detector) > 5:
                remaining = len(by_detector) - 5
                typer.echo(f"  ... and {remaining} more detector(s); pass --verbose for full list")
    if report.claim_record_ids:
        typer.echo("")
        if verbose:
            typer.echo("Claim record IDs (pass to `efterlev provenance show`):")
            for cid in report.claim_record_ids:
                typer.echo(f"  {cid}")
        else:
            typer.echo(
                f"{len(report.claim_record_ids)} claim record(s) written to the JSON "
                f"sidecar — pass `--verbose` to print each ID, or read them from "
                f"`gap-<ts>.json` and feed any to `efterlev provenance show <id>`."
            )

    from efterlev.reports import render_gap_report_html, render_gap_report_json

    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    generated_at = datetime.now().astimezone()

    html_body = render_gap_report_html(
        report,
        baseline_id="fedramp-20x-moderate",
        frmr_version=frmr_doc.version,
        evidence=evidence,
        generated_at=generated_at,
        themes=frmr_doc.themes,
        indicators=frmr_doc.indicators,
    )
    html_path = reports_dir / f"gap-{timestamp}.html"
    html_path.write_text(html_body, encoding="utf-8")

    json_data = render_gap_report_json(
        report,
        baseline_id="fedramp-20x-moderate",
        frmr_version=frmr_doc.version,
        evidence=evidence,
        generated_at=generated_at,
        themes=frmr_doc.themes,
        indicators=frmr_doc.indicators,
        runs_aggregated=runs,
        per_run_verdicts=per_run_verdicts,
        flickering_ksis=flickering_ksis,
    )
    json_path = reports_dir / f"gap-{timestamp}.json"
    json_path.write_text(json.dumps(json_data, indent=2, sort_keys=True), encoding="utf-8")

    typer.echo("")
    typer.echo(f"HTML report:  {html_path}")
    typer.echo(f"JSON sidecar: {json_path}")
    if runs > 1:
        stable = len(report.ksi_classifications) - len(flickering_ksis)
        typer.echo(
            f"  multi-run aggregation: {runs} runs, {stable} stable verdicts, "
            f"{len(flickering_ksis)} flickering KSI(s)"
        )
        if flickering_ksis:
            typer.echo(
                f"  flickering: {', '.join(flickering_ksis)} -- per_run_verdicts in "
                f"the JSON sidecar"
            )

    cost_line = summarize_run_cost(root, started_at)
    if cost_line:
        typer.echo(cost_line)

    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        "  efterlev agent document   draft per-KSI narratives + FRMR attestation (~$1-2 on Sonnet)"
    )
    typer.echo(
        "  efterlev poam             POA&M markdown for every open KSI (deterministic, free)"
    )
    typer.echo(
        "  efterlev agent remediate --ksi <KSI-ID>   propose a Terraform diff that "
        "closes one gap (~$0.30 on Opus)"
    )

    _write_scan_redaction_log(ledger, root, scan_id)


@agent_app.command("document")
def agent_document(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    ksi: str = typer.Option(
        None,
        "--ksi",
        help="KSI ID to draft an attestation for. Defaults to every classified KSI.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help=(
            "Print per-KSI summary blocks (citation count, narrative preview, "
            "claim record id) to the terminal. By default the agent prints a "
            "compact one-line-per-KSI summary; full per-KSI blocks live in the "
            "HTML and JSON outputs."
        ),
    ),
    include_inapplicable_narratives: bool = typer.Option(
        False,
        "--include-inapplicable-narratives",
        help=(
            "Generate full LLM narratives for `evidence_layer_inapplicable` KSIs. "
            "By default these get a deterministic narrative (no LLM call) since "
            "the agent has already classified them as 'scanner cannot evidence' "
            "and per-KSI prose is essentially boilerplate. Pass this flag if you "
            "want richer Sonnet-drafted procedural-reviewer prose for those KSIs "
            "— the FRMR attestation entries are still generated either way."
        ),
    ),
    llm_model: str = typer.Option(
        None,
        "--llm-model",
        help=(
            "Override the workspace-configured model for THIS documentation run "
            "only — config.toml is NOT modified, and the cached gap report is "
            "untouched (the gap and documentation stages cache independently). "
            "Use case (v0.1.227): the gap stage ran on Haiku but a stronger "
            "model is wanted for narratives — e.g. after a "
            "deterministic_guard_fallback warning. Examples: claude-sonnet-4-6, "
            "claude-haiku-4-5."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help=(
            "Build the assembled prompt(s) and exit without invoking the LLM. "
            "Prints a JSON array of literal Anthropic API request envelopes — "
            "one per per-KSI narrative request the agent would have made. See "
            "`efterlev agent gap --help` for the full --dry-run contract."
        ),
    ),
    dump_prompt: Path | None = typer.Option(
        None,
        "--dump-prompt",
        help="Write the dry-run JSON to PATH instead of stdout. Implies --dry-run.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing --dump-prompt PATH.",
    ),
) -> None:
    """Draft an FRMR-compatible attestation for a KSI, grounded in its evidence."""
    from datetime import UTC
    from datetime import datetime as _dt

    _validate_dry_run_args(dump_prompt, force)
    is_dry_run = dry_run or dump_prompt is not None

    from efterlev.agents import (
        DocumentationAgent,
        DocumentationAgentInput,
        count_duplicate_classification_runs,
        reconstruct_classifications_from_store,
    )
    from efterlev.agents.cost_summary import summarize_run_cost
    from efterlev.agents.dry_run import DryRunSession, active_dry_run
    from efterlev.config import load_config
    from efterlev.errors import AgentError, ConfigError
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.llm.scrubber import RedactionLedger, active_redaction_ledger
    from efterlev.models import Evidence
    from efterlev.primitives.generate import (
        GenerateFrmrAttestationInput,
        generate_frmr_attestation,
    )
    from efterlev.provenance import ProvenanceStore, active_store
    from efterlev.reports import (
        render_documentation_report_html,
        render_documentation_report_json,
    )

    started_at = _dt.now(UTC)
    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    try:
        config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    # Single ProvenanceStore context for the whole command: agent invocation
    # and FRMR-attestation generation both write records, and both belong to
    # the same logical "documentation run" in the provenance graph. Opening
    # the store twice (as this command did before Phase 2 polish) would put
    # the two primitives' records in different active-store contexts, which
    # is observable through the provenance walker and wasted SQLite opens.
    scan_id = _new_scan_id()
    ledger = RedactionLedger()

    try:
        with (
            ProvenanceStore(root) as store,
            active_store(store),
            active_redaction_ledger(ledger),
        ):
            evidence = [Evidence.model_validate(p) for _rid, p in store.iter_evidence()]
            classification_rows = store.iter_claims_by_metadata_kind("ksi_classification")
            duplicate_count = count_duplicate_classification_runs(classification_rows)
            # v0.1.147 / #352: drop pre-v0.1.146 stale unknown-KSI records.
            classifications = reconstruct_classifications_from_store(
                classification_rows, baseline_ksi_ids=set(frmr_doc.indicators.keys())
            )
            if duplicate_count > 0:
                typer.echo(
                    f"note: deduped {duplicate_count} duplicate classification(s) "
                    f"from prior `agent gap` runs (latest-wins). "
                    f"Doc-agent narratives reflect the latest run only.",
                    err=True,
                )

            if not classifications:
                typer.echo(
                    "error: 0 Gap Agent classifications in the store. The Gap Agent "
                    "either hasn't run yet, or ran with no evidence to classify "
                    "(check `efterlev scan` first if you skipped that stage).",
                    err=True,
                )
                raise typer.Exit(code=1)

            # Priority 0 (2026-04-27): scan_summary surfaces coverage
            # limitations to per-KSI narratives (HCL-mode against module
            # composition makes `not_implemented` ambiguous between "real
            # gap" and "scanner couldn't see it"). Same source as `agent gap`.
            from efterlev.primitives.scan import latest_scan_summary

            scan_summary = latest_scan_summary(store)

            from efterlev.cli.progress import TerminalProgressCallback

            # v0.1.116: see GapAgent comment above re: client= passthrough.
            # v0.1.151 / #356: pass workspace_root + cache_mode so the cache wrapper applies.
            from efterlev.llm.factory import get_client_from_config

            dry_run_session = DryRunSession() if is_dry_run else None
            # v0.1.227: --llm-model overrides for this run only. model_copy on
            # the frozen LLMConfig — config.toml on disk is never touched.
            llm_config = (
                config.llm
                if llm_model is None
                else config.llm.model_copy(update={"model": llm_model})
            )
            agent = DocumentationAgent(
                model=llm_config.model,
                client=get_client_from_config(
                    llm_config, workspace_root=root, cache_mode=config.cache.mode
                ),
            )
            with friendly_llm_error_handler():
                doc_input = DocumentationAgentInput(
                    indicators=frmr_doc.indicators,
                    evidence=evidence,
                    classifications=classifications,
                    baseline_id="fedramp-20x-moderate",
                    frmr_version=frmr_doc.version,
                    only_ksi=ksi,
                    include_inapplicable_narratives=include_inapplicable_narratives,
                    scan_summary=scan_summary,
                )
                if dry_run_session is not None:
                    with active_dry_run(dry_run_session):
                        report = agent.run(
                            doc_input,
                            progress_callback=TerminalProgressCallback(stage="documentation"),
                        )
                else:
                    report = agent.run(
                        doc_input,
                        progress_callback=TerminalProgressCallback(stage="documentation"),
                    )

            if is_dry_run:
                assert dry_run_session is not None
                _dump_dry_run_session(dry_run_session, dump_prompt, force)
                return

            attestation_drafts = [att.draft for att in report.attestations]
            claim_record_ids = {
                att.draft.ksi_id: att.claim_record_id
                for att in report.attestations
                if att.claim_record_id is not None
            }
            attestation_result = generate_frmr_attestation(
                GenerateFrmrAttestationInput(
                    drafts=attestation_drafts,
                    indicators=frmr_doc.indicators,
                    baseline_id="fedramp-20x-moderate",
                    frmr_version=frmr_doc.version,
                    frmr_last_updated=frmr_doc.last_updated,
                    claim_record_ids=claim_record_ids,
                    machine_validation_cadence=config.cadence.machine_validation_cadence,
                    non_machine_validation_cadence=config.cadence.non_machine_validation_cadence,
                )
            )
    except AgentError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"Documentation Agent drafted {len(report.attestations)} attestation(s).")
    if verbose:
        for att in report.attestations:
            draft = att.draft
            typer.echo("")
            typer.echo(f"  === {draft.ksi_id} ({draft.status or 'no status'}) ===")
            typer.echo(f"  citations: {len(draft.citations)}")
            if draft.narrative:
                preview = draft.narrative.strip().replace("\n", " ")
                ellipsis = "…" if len(preview) > 160 else ""
                typer.echo(f"  DRAFT — requires human review: {preview[:160]}{ellipsis}")
            if att.claim_record_id is not None:
                typer.echo(f"  record id: {att.claim_record_id}")
    else:
        # Compact one-line summary per KSI by status — first-time users skim
        # this; full per-KSI prose lives in the HTML/JSON output.
        from collections import Counter

        status_counts = Counter((att.draft.status or "no_status") for att in report.attestations)
        for status, count in sorted(status_counts.items()):
            typer.echo(f"  {status:<35} {count}")
    if report.skipped_ksi_ids:
        typer.echo("")
        skipped = ", ".join(report.skipped_ksi_ids)
        typer.echo(f"Skipped {len(report.skipped_ksi_ids)} KSI(s): {skipped}")

    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    generated_at = datetime.now().astimezone()

    html_body = render_documentation_report_html(
        report,
        baseline_id="fedramp-20x-moderate",
        frmr_version=frmr_doc.version,
        generated_at=generated_at,
    )
    html_path = reports_dir / f"documentation-{timestamp}.html"
    html_path.write_text(html_body, encoding="utf-8")

    json_data = render_documentation_report_json(
        report,
        baseline_id="fedramp-20x-moderate",
        frmr_version=frmr_doc.version,
        generated_at=generated_at,
    )
    json_path = reports_dir / f"documentation-{timestamp}.json"
    json_path.write_text(json.dumps(json_data, indent=2, sort_keys=True), encoding="utf-8")

    typer.echo("")
    typer.echo(f"HTML report:      {html_path}")
    typer.echo(f"JSON sidecar:     {json_path}")

    # FRMR-compatible attestation JSON alongside the HTML — one CLI run, two
    # artifacts. The human-readable HTML is for review; the machine-readable
    # JSON is the v1 primary production output fed to 3PAOs and downstream.
    attestation_path = reports_dir / f"attestation-{timestamp}.json"
    attestation_path.write_text(attestation_result.artifact_json, encoding="utf-8")
    typer.echo(f"FRMR attestation: {attestation_path}")
    typer.echo(f"  indicators:       {attestation_result.indicator_count}")
    if attestation_result.skipped_unknown_ksi:
        # Primitive already deduplicates; just format for display.
        skipped = ", ".join(attestation_result.skipped_unknown_ksi)
        typer.echo(f"  skipped unknown:  {skipped}")

    cost_line = summarize_run_cost(root, started_at)
    if cost_line:
        typer.echo(cost_line)

    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(
        "  efterlev poam             POA&M markdown for every open KSI (deterministic, free)"
    )
    typer.echo(
        "  efterlev agent remediate --ksi <KSI-ID>   propose a Terraform diff that "
        "closes one gap (~$0.30 on Opus)"
    )

    _write_scan_redaction_log(ledger, root, scan_id)


@agent_app.command("remediate")
def agent_remediate(
    ksi: str = typer.Option(
        ...,
        "--ksi",
        help="KSI ID to propose a remediation for.",
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` store will be read. Defaults to cwd.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help=(
            "Build the assembled prompt and exit without invoking the LLM. "
            "Prints a JSON array of one Anthropic API request envelope (the "
            "single LLM call the remediation agent would have made for this KSI). "
            "See `efterlev agent gap --help` for the full --dry-run contract."
        ),
    ),
    dump_prompt: Path | None = typer.Option(
        None,
        "--dump-prompt",
        help="Write the dry-run JSON to PATH instead of stdout. Implies --dry-run.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing --dump-prompt PATH.",
    ),
) -> None:
    """Propose a Terraform diff fixing a selected KSI gap."""
    from datetime import UTC
    from datetime import datetime as _dt

    _validate_dry_run_args(dump_prompt, force)
    is_dry_run = dry_run or dump_prompt is not None

    from efterlev.agents import (
        RemediationAgent,
        RemediationAgentInput,
        count_duplicate_classification_runs,
        in_scope_evidence,
        reconstruct_classifications_from_store,
    )
    from efterlev.agents.cost_summary import summarize_run_cost
    from efterlev.agents.dry_run import DryRunSession, active_dry_run
    from efterlev.config import load_config
    from efterlev.errors import AgentError, ConfigError
    from efterlev.frmr.loader import FrmrDocument
    from efterlev.llm.scrubber import RedactionLedger, active_redaction_ledger
    from efterlev.models import Evidence
    from efterlev.provenance import ProvenanceStore, active_store

    started_at = _dt.now(UTC)
    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Re-run `efterlev init`.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    indicator = frmr_doc.indicators.get(ksi)
    if indicator is None:
        typer.echo(
            f"error: KSI {ksi!r} is not in the loaded baseline (FRMR {frmr_doc.version}).",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    scan_id = _new_scan_id()
    ledger = RedactionLedger()

    try:
        with ProvenanceStore(root) as store:
            classification_rows = store.iter_claims_by_metadata_kind("ksi_classification")
            duplicate_count = count_duplicate_classification_runs(classification_rows)
            # v0.1.147 / #352: drop pre-v0.1.146 stale unknown-KSI records.
            classifications = reconstruct_classifications_from_store(
                classification_rows, baseline_ksi_ids=set(frmr_doc.indicators.keys())
            )
            if duplicate_count > 0:
                typer.echo(
                    f"note: deduped {duplicate_count} duplicate classification(s) "
                    f"from prior `agent gap` runs (latest-wins).",
                    err=True,
                )
            clf = next((c for c in classifications if c.ksi_id == ksi), None)
            if clf is None:
                typer.echo(
                    f"error: no Gap Agent classification for {ksi} in the store. "
                    "Run `efterlev agent gap` first.",
                    err=True,
                )
                raise typer.Exit(code=1)
            if clf.status == "implemented":
                typer.echo(f"{ksi} is classified as `implemented`. No remediation needed.")
                raise typer.Exit(code=0)
            if clf.status == "not_applicable":
                typer.echo(f"{ksi} is classified as `not_applicable`. No remediation needed.")
                raise typer.Exit(code=0)

            # Boundary enforcement at the agent-input layer (v0.1.222): same
            # filter as `agent gap` (v0.1.219). Without it, out-of-boundary
            # evidence attributed to the target KSI flows into the prompt AND
            # the excluded `.tf` source files below get read and diffed — the
            # agent could propose a remediation against a file the user
            # explicitly scoped out. No-op when no boundary is declared.
            all_evidence = in_scope_evidence(
                [Evidence.model_validate(p) for _rid, p in store.iter_evidence()]
            )
            ksi_evidence = [ev for ev in all_evidence if ksi in ev.ksis_evidenced]

            # Manifest-sourced Evidence is human-signed procedural attestation;
            # a manifest YAML is NOT Terraform source, so reading it as source
            # for the Remediation Agent would produce nonsense diffs. The
            # agent still sees the manifest evidence in its prompt (so it can
            # reason "this KSI has attestations plus a Terraform gap"); we
            # just don't load the YAML contents as `.tf` source.
            from efterlev.primitives.evidence import MANIFEST_DETECTOR_ID

            terraform_evidence = [
                ev for ev in ksi_evidence if ev.detector_id != MANIFEST_DETECTOR_ID
            ]

            # If every Evidence for this KSI is manifest-sourced, there is no
            # Terraform surface for the agent to remediate. That's not an
            # error — the customer has attested procedurally, but the scanner
            # found no infra-layer gap to fix. Exit cleanly with a clear
            # message. This is the common case when a KSI is `partial` and
            # the gap is purely procedural (documentation, process, or SOP).
            if not terraform_evidence:
                typer.echo(
                    f"{ksi} has only manifest-sourced evidence ({len(ksi_evidence)} "
                    f"attestation(s)); no Terraform surface to remediate. The "
                    f"procedural gap — if any — is addressed by updating the "
                    f"manifest(s) under .efterlev/manifests/, not by a .tf diff."
                )
                raise typer.Exit(code=0)

            # Read the .tf files every Terraform-sourced evidence record
            # points at, keyed by the path as stored in the evidence.
            # `resolve_within_root` joins against `root` and rejects any
            # resolved path that escapes containment, so a hostile evidence
            # record cannot exfiltrate arbitrary files.
            from efterlev.paths import resolve_within_root

            source_files: dict[str, str] = {}
            for ev in terraform_evidence:
                rel_path = Path(str(ev.source_ref.file))
                # Non-.tf files (e.g. the plan JSON in plan-mode scans where
                # root-module resources land with `source_ref.file` pointing
                # at the plan file itself) are skipped here — a diff against
                # generated JSON doesn't change infrastructure. Fallback
                # below loads the .tf tree under target_root so the agent
                # still has source to reason about. Dogfood-2026-04-22
                # plan-mode finding.
                if rel_path.suffix != ".tf":
                    continue
                full = resolve_within_root(rel_path, root)
                if full is None or not full.is_file():
                    continue
                key = str(ev.source_ref.file)
                if key not in source_files:
                    source_files[key] = full.read_text(encoding="utf-8")

            # Plan-mode fallback: root-module resources' source_refs point
            # at the plan JSON, not the owning .tf file, because plan JSON
            # doesn't carry per-resource file info (only module-call
            # `source` hints). When evidence-walk produced no loadable .tf
            # content, sweep target_root for .tf files so the agent sees
            # the actual infrastructure source rather than refusing with
            # "no terraform surface to remediate" on a file that IS there.
            if not source_files:
                for tf_path in sorted(root.rglob("*.tf")):
                    # Skip anything inside .efterlev/ (tool state) or
                    # vendor-y hidden dirs. `relative_to(root)` preserves
                    # the repo-relative-path contract.
                    if any(part.startswith(".") for part in tf_path.relative_to(root).parts):
                        continue
                    rel = str(tf_path.relative_to(root))
                    source_files[rel] = tf_path.read_text(encoding="utf-8")

            dry_run_session = DryRunSession() if is_dry_run else None
            with active_store(store), active_redaction_ledger(ledger):
                # v0.1.116: see GapAgent comment above re: client= passthrough.
                from efterlev.llm.factory import get_client_from_config

                # v0.1.151 / #356: pass workspace_root + cache_mode so the cache wrapper applies.
                agent = RemediationAgent(
                    model=config.llm.model,
                    client=get_client_from_config(
                        config.llm, workspace_root=root, cache_mode=config.cache.mode
                    ),
                )
                with friendly_llm_error_handler():
                    rem_input = RemediationAgentInput(
                        indicator=indicator,
                        classification=clf,
                        evidence=ksi_evidence,
                        source_files=source_files,
                        baseline_id="fedramp-20x-moderate",
                        frmr_version=frmr_doc.version,
                    )
                    if dry_run_session is not None:
                        with active_dry_run(dry_run_session):
                            proposal = agent.run(rem_input)
                    else:
                        proposal = agent.run(rem_input)
    except AgentError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    if is_dry_run:
        assert dry_run_session is not None
        _dump_dry_run_session(dry_run_session, dump_prompt, force)
        return

    typer.echo(f"Remediation Agent draft for {proposal.ksi_id} ({proposal.status}):")
    typer.echo("")
    typer.echo("DRAFT — requires human review. Efterlev does not apply diffs.")
    typer.echo("")
    typer.echo(proposal.explanation)
    if proposal.diff:
        typer.echo("")
        typer.echo("--- diff ---")
        typer.echo(proposal.diff)
    if proposal.cited_source_files:
        typer.echo("")
        typer.echo(f"Files touched: {', '.join(proposal.cited_source_files)}")
    if proposal.claim_record_id is not None:
        typer.echo("")
        typer.echo(f"record id: {proposal.claim_record_id}")

    from efterlev.reports import (
        render_remediation_proposal_html,
        render_remediation_proposal_json,
    )

    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    generated_at = datetime.now().astimezone()

    html_body = render_remediation_proposal_html(
        proposal, evidence=ksi_evidence, generated_at=generated_at
    )
    # Include the KSI in the filename so running remediate for multiple KSIs
    # doesn't produce files that can only be distinguished by timestamp.
    html_path = reports_dir / f"remediation-{ksi}-{timestamp}.html"
    html_path.write_text(html_body, encoding="utf-8")

    json_data = render_remediation_proposal_json(proposal, generated_at=generated_at)
    json_path = reports_dir / f"remediation-{ksi}-{timestamp}.json"
    json_path.write_text(json.dumps(json_data, indent=2, sort_keys=True), encoding="utf-8")

    typer.echo("")
    typer.echo(f"HTML report:  {html_path}")
    typer.echo(f"JSON sidecar: {json_path}")

    cost_line = summarize_run_cost(root, started_at)
    if cost_line:
        typer.echo(cost_line)

    _write_scan_redaction_log(ledger, root, scan_id)


@provenance_app.command("show")
def provenance_show(
    record_id: str = typer.Argument(..., help="SHA-256 record ID to walk."),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Repo containing the `.efterlev/` store. Defaults to the current directory.",
    ),
) -> None:
    """Walk the provenance chain from a record back to its source lines."""
    from efterlev.errors import ProvenanceError
    from efterlev.provenance import ProvenanceStore, render_chain_text, walk_chain

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    try:
        with ProvenanceStore(root) as store:
            # Rationales / POA&Ms print 8-char prefixes for readability; resolve
            # the prefix back to a full record_id so users can paste either.
            resolved = store.resolve_record_id_prefix(record_id)
            if resolved is None:
                typer.echo(
                    f"error: no record matches {record_id!r}. "
                    f"Pass a full `sha256:<64hex>` id or a unique hex prefix "
                    f"(≥4 chars).",
                    err=True,
                )
                raise typer.Exit(code=1)
            if resolved != record_id and resolved != f"sha256:{record_id}":
                typer.echo(f"resolved {record_id} → {resolved}")
            # v0.1.11 (3PAO finding): make the dual-key reality explicit.
            # When the resolved record is an Evidence record, its payload
            # carries an `evidence_id` that may differ from the envelope's
            # `record_id` (Evidence content hash vs. ProvenanceRecord
            # envelope hash). Surfacing both lets reviewers verify that
            # the citation in a gap report (which uses `evidence_id`)
            # matches what the store walker walked (keyed by `record_id`).
            record = store.get_record(resolved)
            if record is not None and record.record_type == "evidence":
                try:
                    payload = store.read_payload(record)
                    evidence_id = payload.get("evidence_id") if isinstance(payload, dict) else None
                    if isinstance(evidence_id, str) and evidence_id != resolved:
                        typer.echo(
                            f"  record_id:    {resolved}  (envelope hash — what the store walks)"
                        )
                        typer.echo(
                            f"  evidence_id:  {evidence_id}  (content hash — what reports cite)"
                        )
                except ProvenanceError:
                    pass
            tree = walk_chain(store, resolved)
            typer.echo(render_chain_text(tree))
    except ProvenanceError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e


@provenance_app.command("verify")
def provenance_verify(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Repo containing the `.efterlev/` store. Defaults to the current directory.",
    ),
) -> None:
    """Detect tampering in the local provenance store.

    Backs the THREAT_MODEL.md T4 claim: "the provenance DB stores record
    hashes; `efterlev provenance verify` detects mismatches." The store
    is content-addressed (SHA-256 of canonical bytes), so any modification
    to a blob changes its hash and breaks the `(record_id → content_ref →
    file)` chain. This command walks every record, recomputes the
    blob's SHA-256, and compares it to the hash embedded in the
    sharded `content_ref` path (`xx/yy/xxyy<rest>.json`).

    Exit 0 = every blob matches its declared hash. Exit 1 = at least
    one mismatch (tampering, disk corruption, partial-write, etc.) or
    a missing blob. Output names each affected record explicitly.
    """
    import hashlib

    from efterlev.errors import ProvenanceError
    from efterlev.provenance import ProvenanceStore

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    findings: list[str] = []
    record_count = 0
    try:
        with ProvenanceStore(root) as store:
            for record_id, content_ref in store.iter_record_refs():
                record_count += 1
                blob_path = store.blob_dir / content_ref
                if not blob_path.exists():
                    findings.append(f"  ✗ {record_id}: blob missing at {content_ref}")
                    continue
                actual = hashlib.sha256(blob_path.read_bytes()).hexdigest()
                # Sharded content_ref shape: 9a/20/9a205d96…json. Pull
                # the embedded hash out of the filename stem.
                expected = blob_path.stem
                if actual != expected:
                    findings.append(
                        f"  ✗ {record_id}: blob hash {actual[:12]}… does not match "
                        f"declared {expected[:12]}… (path: {content_ref})"
                    )

            # v0.1.6: post-hoc referential-integrity sweep. The write-time
            # validator (`_validate_claim_derived_from`) is the primary
            # defense, but if it ever has a hole — or if a record was
            # written by a future tool that bypassed the validator — this
            # post-hoc check surfaces the problem at audit time. Walks
            # every record's envelope `derived_from` and confirms each
            # cited id resolves via the dual-key path.
            unresolvable: list[tuple[str, str]] = []
            for record_id in store.iter_records():
                rec = store.get_record(record_id)
                if rec is None or not rec.derived_from:
                    continue
                for cited in rec.derived_from:
                    if store.resolve_to_record(cited) is None:
                        unresolvable.append((record_id, cited))
            for record_id, cited in unresolvable:
                findings.append(
                    f"  ✗ {record_id}: derived_from cites {cited!r} which does not "
                    f"resolve as record_id or evidence_id"
                )
    except ProvenanceError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"verified {record_count} record(s)")
    if findings:
        typer.echo("")
        typer.echo("MISMATCHES (tamper-evidence):")
        for f in findings:
            typer.echo(f)
        typer.echo("")
        typer.echo("  Each mismatch indicates either tampering, disk corruption, a partial write,")
        typer.echo("  or a referential-integrity break in a record's `derived_from` chain.")
        raise typer.Exit(code=1)
    typer.echo(
        "RESULT: clean. Every blob matches its content-addressed hash, and every "
        "`derived_from` citation resolves."
    )


@app.command()
def quickstart() -> None:
    """One-command activation demo.

    Lays down a bundled synthetic Terraform + Evidence Manifest fixture
    in a temp workspace under the platform-appropriate cache dir, runs
    init → scan → agent gap → agent document end-to-end against it,
    prints a 5-line summary, and points the user at their own repo for
    the next step.

    Realistic wall time: 60-180 seconds with a valid `ANTHROPIC_API_KEY`
    on Sonnet (default), ~$0.30. Without a key, runs init + scan only
    and skips the agent stages with a hint.

    See DECISIONS 2026-05-06 "Tier 1 #1 design: efterlev quickstart"
    for the design rationale.
    """
    from efterlev.quickstart import run_quickstart

    raise typer.Exit(code=run_quickstart())


@mcp_app.command("serve")
def mcp_serve() -> None:
    """Run the MCP stdio server exposing every registered tool.

    Blocks on stdin/stdout for the MCP protocol. Intended to be launched
    as a subprocess by an MCP client (Claude Code, etc.); not interactive.
    Per DECISIONS design call #4: stdio-only, stateless, every tool call
    logged to the target repo's provenance store for audit.
    """
    import asyncio

    from efterlev.mcp_server import run_stdio_server

    try:
        asyncio.run(run_stdio_server())
    except KeyboardInterrupt:
        # Clean shutdown on Ctrl-C; Typer already swallows but be explicit.
        raise typer.Exit(code=0) from None


@redaction_app.command("review")
def redaction_review(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/redacted.log` to read. Defaults to cwd.",
    ),
    scan_id: str | None = typer.Option(
        None,
        "--scan-id",
        help="Show only redactions from a specific scan-id (e.g. 20260423T163045).",
    ),
    limit: int = typer.Option(
        20,
        "--limit",
        help="Maximum number of recent scans to summarize. Only applies when --scan-id is not set.",
    ),
) -> None:
    """Summarize the redaction audit log written during agent runs.

    Every agent invocation (`efterlev agent gap`, `document`, `remediate`)
    opens a `RedactionLedger` context that captures every secret the
    scrubber removed from a prompt. The ledger is appended to
    `.efterlev/redacted.log` (JSONL, 0600 perms). This command reads the
    log and prints a per-scan summary: how many secrets of which kinds
    were redacted in each scan, in field-location terms (NOT the secrets
    themselves — the log is audit-safe and never writes secret material).

    Without `--scan-id`, shows the most recent `limit` scans. With
    `--scan-id`, drills into one scan's events.
    """
    import json

    root = target.resolve()
    log_path = root / ".efterlev" / "redacted.log"
    if not log_path.is_file():
        typer.echo(
            f"No redaction log at {log_path}. "
            f"This means either no agent has run under this target, or no "
            f"redactions have occurred during any run.",
        )
        raise typer.Exit(code=0)

    # Load events, grouped by scan_id, in the order they appear.
    by_scan: dict[str, list[dict]] = {}
    scan_order: list[str] = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                # Skip malformed lines rather than abort — audit log integrity
                # isn't cryptographically enforced, only perm-enforced.
                continue
            sid = record.get("scan_id", "<unknown>")
            if sid not in by_scan:
                by_scan[sid] = []
                scan_order.append(sid)
            by_scan[sid].append(record)

    if scan_id is not None:
        events = by_scan.get(scan_id)
        if events is None:
            typer.echo(f"No redactions recorded for scan-id {scan_id!r}.")
            raise typer.Exit(code=1)
        typer.echo(f"Scan {scan_id} — {len(events)} redactions:")
        for ev in events:
            typer.echo(
                f"  {ev['timestamp']}  {ev['pattern_name']:<28}  "
                f"sha256:{ev['sha256_prefix']}  @ {ev['context_hint']}"
            )
        return

    # Default: per-scan summary, most recent `limit` scans.
    recent = scan_order[-limit:]
    typer.echo(f"Redaction audit log: {log_path} ({len(scan_order)} scan(s) total)")
    typer.echo("")
    typer.echo(f"{'scan_id':<18}  {'n':>4}  pattern counts")
    for sid in recent:
        events = by_scan[sid]
        counts: dict[str, int] = {}
        for ev in events:
            counts[ev["pattern_name"]] = counts.get(ev["pattern_name"], 0) + 1
        summary = ", ".join(f"{n}x{name}" for name, n in sorted(counts.items()))
        typer.echo(f"{sid:<18}  {len(events):>4}  {summary}")
    if len(scan_order) > limit:
        typer.echo(f"... {len(scan_order) - limit} earlier scan(s) not shown (--limit).")
    typer.echo("")
    typer.echo("Run `efterlev redaction review --scan-id <id>` for per-event detail.")


@manifests_app.command("init")
def manifests_init(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo whose `.efterlev/` will receive the templates. Defaults to cwd.",
    ),
    starter_pack: bool = typer.Option(
        False,
        "--starter-pack",
        help=(
            "Copy the bundled starter-pack templates (26 KSIs covering the "
            "commonly-procedural FRMR baseline) into "
            "`.efterlev/manifests/starter-pack/`. Required flag — `init` does "
            "nothing useful without it today."
        ),
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing `.efterlev/manifests/starter-pack/` subdir.",
    ),
) -> None:
    """Initialize Evidence Manifest content (currently: copy starter pack).

    See DECISIONS 2026-05-06 "Tier 1 #3 design: Evidence Manifest starter
    pack" for the rationale on landing templates in a subdir (outside
    the manifest loader's pickup glob) and the `.template.yml` extension
    + loader skip filter.
    """
    import importlib.resources
    import shutil

    if not starter_pack:
        typer.echo(
            "error: `efterlev manifests init` currently requires --starter-pack. "
            "Other init modes will land in future releases.",
            err=True,
        )
        raise typer.Exit(code=2)

    root = target.resolve()
    if not (root / ".efterlev").is_dir():
        typer.echo(
            f"error: no `.efterlev/` directory under {root}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    dest = root / ".efterlev" / "manifests" / "starter-pack"
    if dest.exists():
        if not force:
            typer.echo(
                f"error: {dest} exists; pass --force to overwrite",
                err=True,
            )
            raise typer.Exit(code=2)
        # `--force` REPLACES the subdir wholesale; per DECISIONS this is
        # acceptable because templates are version-pinned to the wheel.
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Bundled templates live at `efterlev.manifest_templates`.
    template_pkg = importlib.resources.files("efterlev.manifest_templates")
    written = 0
    for entry in template_pkg.iterdir():
        if not entry.is_file():
            continue
        name = entry.name
        # Skip the package marker + script artifacts.
        if name.startswith("_") or name.startswith("."):
            continue
        body = entry.read_text(encoding="utf-8")
        (dest / name).write_text(body, encoding="utf-8")
        if name.endswith(".template.yml"):
            written += 1

    typer.echo(
        f"wrote {written} starter-pack templates to {dest}",
        err=True,
    )
    typer.echo(
        f"read {dest}/README.md for the workflow, then copy templates to "
        f"{root}/.efterlev/manifests/ as you fill them in.",
        err=True,
    )


@manifests_app.command("draft")
def manifests_draft(
    ksi: str = typer.Argument(
        ...,
        help="The procedural KSI to draft a manifest for, e.g. KSI-AFR-ADS.",
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root containing `.efterlev/`. Defaults to the current directory.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite an existing manifest for this KSI.",
    ),
) -> None:
    """Interactively draft an Evidence Manifest for a procedural KSI.

    Walks the KSI's attestation questions (from the bundled starter
    template) as prompts, then writes a clean, schema-valid
    `.efterlev/manifests/<ksi>.yml` ready for the next `efterlev scan`
    to load — no hand-editing of YAML, no DRAFT placeholders to clear.

    Deterministic; no LLM. The helper provides structure + guidance; the
    attestation wording is yours (it's a compliance claim you own —
    the tool will never fabricate it). Run on a terminal — it's
    interactive; `manifests init --starter-pack` is the hand-edit path.
    """
    from efterlev.cli.manifest_draft import run_manifest_draft

    raise typer.Exit(code=run_manifest_draft(target, ksi, force=force))


@manifests_app.command("validate")
def manifests_validate(
    path: Path = typer.Argument(
        ...,
        help=(
            "Manifest YAML file OR directory. A directory is walked via the "
            "same glob as scan-time manifest discovery (`*.yml` + `*.yaml`, "
            "`*.template.yml` skipped)."
        ),
    ),
) -> None:
    """Validate manifest YAML(s) against the EvidenceManifest schema offline.

    No FRMR / baseline load required — pure schema check. Catches the
    high-leverage mistakes a contributor makes while authoring a manifest:
    typo'd field names (`extra="forbid"` rejects them; e.g. `attester:`
    instead of `attested_by:` is silently swallowed in YAML but rejected
    here), malformed dates, missing required fields, top-level not-a-mapping.

    Does NOT cross-check the `ksi:` value against any baseline — a manifest
    can declare a KSI not in the loaded FedRAMP 20x baseline (the loader
    warns at scan time and skips). The cross-baseline check is what
    `efterlev scan` does after `init` loads the FRMR; the offline
    `validate` is the pre-commit / pre-PR gate that catches schema
    mistakes before scan time.

    Exit codes: 0 if every manifest validates; 1 if any manifest fails;
    2 if the path doesn't exist or is otherwise unusable.
    """
    from efterlev.errors import ManifestError
    from efterlev.manifests.loader import discover_manifest_files, load_manifest_file
    from efterlev.manifests.substantiveness import manifest_issues

    if not path.exists():
        typer.echo(f"error: path does not exist: {path}", err=True)
        raise typer.Exit(code=2)

    if path.is_file():
        files = [path]
    else:
        files = discover_manifest_files(path)
        if not files:
            typer.echo(
                f"error: no manifest files found under {path} "
                f"(looked for `*.yml` / `*.yaml`, excluding `*.template.yml`)",
                err=True,
            )
            raise typer.Exit(code=2)

    failures = 0
    for manifest_path in files:
        try:
            manifest = load_manifest_file(manifest_path)
        except ManifestError as e:
            typer.echo(f"  ✗ {manifest_path}", err=True)
            typer.echo(f"      {e}", err=True)
            failures += 1
            continue
        attestation_count = len(manifest.evidence)
        typer.echo(f"  ✓ {manifest_path}  ksi={manifest.ksi}  attestations={attestation_count}")
        # Schema-valid is not the same as filled-in: surface substantiveness gaps
        # (placeholder attester, no review cadence, no supporting docs) as warnings.
        for issue in manifest_issues(manifest):
            typer.echo(f"      ~ {issue}")

    typer.echo("")
    if failures:
        typer.echo(
            f"validation: {len(files) - failures}/{len(files)} valid; {failures} failed",
            err=True,
        )
        raise typer.Exit(code=1)
    typer.echo(f"validation: {len(files)}/{len(files)} valid")


_PROCEDURAL_PREFIXES = ("KSI-AFR-", "KSI-CED-", "KSI-INR-")


@manifests_app.command("scaffold")
def manifests_scaffold(
    target: Path = typer.Option(Path("."), "--target", help="Workspace path."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing <ksi>.yml stubs."),
) -> None:
    """Scaffold a fillable Evidence Manifest for every procedural KSI that lacks one.

    Procedural KSIs (AFR / CED / INR themes) can't be evidenced by any scanner —
    they need a human attestation. This lays down a schema-valid, fillable stub
    per missing procedural KSI under `.efterlev/manifests/<ksi>.yml`, with the
    starter-pack questions inline. Stubs are deliberately non-substantive (TODO
    placeholders) so `manifests status` / `efterlev next` keep flagging them
    until you fill them in. Never fabricates the claim you must own.
    """
    root = target.resolve()
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Run `efterlev init` first.", err=True
        )
        raise typer.Exit(code=1)

    from efterlev.frmr import FrmrDocument
    from efterlev.manifests.loader import discover_manifest_files, load_manifest_file
    from efterlev.manifests.scaffold import stub_yaml

    doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    procedural = [k for k in doc.indicators if k.startswith(_PROCEDURAL_PREFIXES)]
    manifests_dir = root / ".efterlev" / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    covered: set[str] = set()
    for f in discover_manifest_files(manifests_dir):
        try:
            covered.add(load_manifest_file(f).ksi)
        except Exception:
            continue

    written: list[str] = []
    skipped: list[str] = []
    for ksi in procedural:
        dest = manifests_dir / f"{ksi}.yml"
        if (ksi in covered or dest.exists()) and not force:
            skipped.append(ksi)
            continue
        dest.write_text(stub_yaml(ksi), encoding="utf-8")
        written.append(ksi)

    if written:
        typer.echo(f"Scaffolded {len(written)} manifest stub(s) under {manifests_dir}:")
        for ksi in written:
            typer.echo(f"  + {ksi}.yml")
        typer.echo("")
        typer.echo(
            "Fill in the TODO fields (attester, statement, review cadence, supporting docs);"
        )
        typer.echo("track progress with `efterlev manifests status`. Fill them BEFORE `efterlev")
        typer.echo("agent gap` so the agent reasons over real attestations, not placeholders.")
    if skipped:
        typer.echo(f"Skipped {len(skipped)} already present (pass --force to re-stub).")
    if not written and not skipped:
        typer.echo("No procedural KSIs found for this baseline.")


@manifests_app.command("status")
def manifests_status(
    target: Path = typer.Option(Path("."), "--target", help="Workspace path."),
    as_json: bool = typer.Option(False, "--json", help="Emit the status as JSON."),
) -> None:
    """Show which procedural KSIs have a substantive manifest, which are thin, which are missing.

    The completion tracker for the procedural wall: `ready` = a real statement +
    named attester + review cadence; `thin` = present but still has placeholders
    or gaps; `missing` = no manifest yet.
    """
    root = target.resolve()
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Run `efterlev init` first.", err=True
        )
        raise typer.Exit(code=1)

    import json as _json

    from efterlev.frmr import FrmrDocument
    from efterlev.manifests.loader import discover_manifest_files, load_manifest_file
    from efterlev.manifests.substantiveness import is_substantive, manifest_issues

    doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    procedural = [k for k in doc.indicators if k.startswith(_PROCEDURAL_PREFIXES)]

    by_ksi = {}
    for f in discover_manifest_files(root / ".efterlev" / "manifests"):
        try:
            manifest = load_manifest_file(f)
        except Exception:
            continue
        by_ksi[manifest.ksi] = manifest

    rows: list[tuple[str, str, list[str]]] = []
    for ksi in procedural:
        m = by_ksi.get(ksi)
        if m is None:
            rows.append((ksi, "missing", []))
        elif is_substantive(m):
            rows.append((ksi, "ready", []))
        else:
            rows.append((ksi, "thin", manifest_issues(m)))

    ready = sum(1 for _, s, _ in rows if s == "ready")
    thin = sum(1 for _, s, _ in rows if s == "thin")
    missing = sum(1 for _, s, _ in rows if s == "missing")

    if as_json:
        typer.echo(
            _json.dumps(
                {
                    "total": len(rows),
                    "ready": ready,
                    "thin": thin,
                    "missing": missing,
                    "ksis": [{"ksi": k, "status": s, "issues": iss} for k, s, iss in rows],
                },
                indent=2,
            )
        )
        return

    badge = {"ready": "✓", "thin": "~", "missing": "✗"}
    typer.echo("")
    typer.echo(
        f"  Procedural Evidence Manifests — {ready}/{len(rows)} ready · "
        f"{thin} thin · {missing} missing"
    )
    typer.echo("")
    for ksi, status, issues in rows:
        typer.echo(f"  {badge[status]} {ksi}  ({status})")
        for issue in issues[:2]:
            typer.echo(f"      ~ {issue}")
    typer.echo("")
    if missing:
        typer.echo("  Scaffold the missing ones:      efterlev manifests scaffold")
    if thin:
        typer.echo("  Fill one in interactively:      efterlev manifests draft <KSI>")


@detectors_app.command("list")
def detectors_list() -> None:
    """List every detector registered with the runtime registry.

    Promised by THREAT_MODEL.md as the path to inspect what's loaded —
    "shows all loaded detectors, including third-party, before any scan
    runs." Useful as a defense-in-depth check (detect a registration
    regression like the 16-of-30 bug found 2026-04-25 dogfooding) and
    as introspection for users adding third-party detectors.

    Output is `<id>@<version>  <source>  ksis: ...  controls: ...`
    sorted by detector id. Stable output shape; safe to grep / pipe.
    """
    import efterlev.detectors  # noqa: F401  (registration side-effect)
    from efterlev.detectors.base import get_registry

    specs = sorted(get_registry().values(), key=lambda s: s.id)
    if not specs:
        typer.echo("(no detectors registered)")
        return
    for spec in specs:
        # Priority 6 (2026-04-27): visually distinguish KSI-mapped detectors
        # from supplementary 800-53-only ones. The latter still emit valid
        # evidence; they just don't contribute to KSI roll-ups because their
        # underlying controls (SC-28, IA-5, AC-3) are not in any FRMR
        # 0.9.43-beta KSI's `controls` array. Tracked upstream.
        if spec.ksis:
            tag = ""
            ksis = ", ".join(spec.ksis)
        else:
            tag = "  [800-53 only]"
            ksis = "—"
        controls = ", ".join(spec.controls) if spec.controls else "—"
        typer.echo(f"  {spec.id}@{spec.version}  source={spec.source}{tag}")
        typer.echo(f"      ksis:     {ksis}")
        typer.echo(f"      controls: {controls}")
    typer.echo("")
    ksi_mapped_count = sum(1 for s in specs if s.ksis)
    only_800_53_count = len(specs) - ksi_mapped_count
    typer.echo(
        f"  total: {len(specs)} detectors  "
        f"({ksi_mapped_count} KSI-mapped, {only_800_53_count} 800-53 only)"
    )


# Detector-id format: <cloud>.<snake_case_name>. The accepted clouds are
# the same set the detector library is currently organized under; new
# clouds need a corresponding `src/efterlev/detectors/<cloud>/` directory
# + a registration import in `src/efterlev/detectors/__init__.py` so the
# scaffolded detector actually loads.
_VALID_DETECTOR_CLOUDS: frozenset[str] = frozenset({"aws", "github", "gcp", "azure"})
_VALID_DETECTOR_SOURCES: frozenset[str] = frozenset({"terraform", "terraform-plan", "github"})


@detectors_app.command("new")
def detectors_new(
    detector_id: str = typer.Argument(
        ...,
        help=(
            "Detector id in `<cloud>.<snake_case_name>` form (e.g. "
            "`aws.foo_bar`). Cloud must be one of: aws, github, gcp, azure."
        ),
    ),
    ksi: list[str] = typer.Option(
        [],
        "--ksi",
        help=(
            "KSI(s) the detector evidences (repeatable, e.g. "
            "`--ksi KSI-CNA-RVP --ksi KSI-CNA-MAT`). Empty (default) "
            "means a supplementary 800-53-only detector."
        ),
    ),
    control: list[str] = typer.Option(
        [],
        "--control",
        help=(
            "800-53 control(s) the detector evidences (repeatable, e.g. "
            "`--control SC-7 --control AC-3`). Defaults to empty."
        ),
    ),
    source: str = typer.Option(
        "terraform",
        "--source",
        help=("Source the detector reads. One of: terraform (default), terraform-plan, github."),
    ),
) -> None:
    """Scaffold the 5-file detector folder skeleton + fixture directories.

    Generates `src/efterlev/detectors/<cloud>/<name>/` with the
    canonical 5-file shape (`__init__.py`, `detector.py`, `mapping.yaml`,
    `evidence.yaml`, `README.md`) plus `fixtures/should_match/.gitkeep`
    and `fixtures/should_not_match/.gitkeep`. The generated `detector.py`
    is a minimal stub: `@detector(...)` decorator + a `def detect()`
    that returns `[]` (the contributor fills in the matching logic).

    OSS-contribution friction reducer (held since v0.1.18+ per
    LIMITATIONS.md). After scaffolding, the contributor adds an import
    line to `src/efterlev/detectors/<cloud>/__init__.py` (or the
    top-level `src/efterlev/detectors/__init__.py`, depending on the
    cloud's convention) so the registry picks the new detector up.

    Refuses to overwrite an existing folder.
    """
    # Validate the detector id shape.
    if "." not in detector_id:
        typer.echo(
            f"error: detector id must be `<cloud>.<snake_case_name>`; got `{detector_id}`",
            err=True,
        )
        raise typer.Exit(code=2)
    cloud, _, name = detector_id.partition(".")
    if cloud not in _VALID_DETECTOR_CLOUDS:
        typer.echo(
            f"error: unsupported cloud `{cloud}`; expected one of: "
            f"{', '.join(sorted(_VALID_DETECTOR_CLOUDS))}",
            err=True,
        )
        raise typer.Exit(code=2)
    if not name or not name.replace("_", "").isalnum() or not name[0].isalpha():
        typer.echo(
            f"error: detector name `{name}` must be snake_case starting with a letter",
            err=True,
        )
        raise typer.Exit(code=2)
    if source not in _VALID_DETECTOR_SOURCES:
        typer.echo(
            f"error: unsupported source `{source}`; expected one of: "
            f"{', '.join(sorted(_VALID_DETECTOR_SOURCES))}",
            err=True,
        )
        raise typer.Exit(code=2)

    # Locate the detector library directory. The scaffolder writes into
    # the `efterlev` package's source tree; finding it via the package's
    # __file__ keeps the scaffolder usable from a checkout AND from a
    # site-packages install (if a contributor wants to scaffold inside
    # an installed wheel for some reason).
    import efterlev.detectors as _det_pkg

    detectors_root = Path(_det_pkg.__file__).resolve().parent
    folder = detectors_root / cloud / name
    if folder.exists():
        typer.echo(f"error: detector folder already exists: {folder}", err=True)
        raise typer.Exit(code=1)

    folder.mkdir(parents=True)
    (folder / "fixtures" / "should_match").mkdir(parents=True)
    (folder / "fixtures" / "should_not_match").mkdir(parents=True)
    (folder / "fixtures" / "should_match" / ".gitkeep").write_text("", encoding="utf-8")
    (folder / "fixtures" / "should_not_match" / ".gitkeep").write_text("", encoding="utf-8")

    ksi_list_repr = "[" + ", ".join(f'"{k}"' for k in ksi) + "]" if ksi else "[]"
    control_list_repr = "[" + ", ".join(f'"{c}"' for c in control) + "]" if control else "[]"

    init_body = f'''"""{cloud}.{name} detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.{cloud}.{name} import detector  # noqa: F401
'''
    (folder / "__init__.py").write_text(init_body, encoding="utf-8")

    detector_body = f'''"""{detector_id}: detector stub.

Generated by `efterlev detectors new {detector_id}`. Replace the
docstring with what the detector evidences, fill in the `detect`
function with the matching logic, and populate the fixtures under
`fixtures/should_match/` and `fixtures/should_not_match/`.
"""

from __future__ import annotations

from datetime import UTC, datetime

from efterlev.detectors.base import detector
from efterlev.models import Evidence, TerraformResource


@detector(
    id="{detector_id}",
    ksis={ksi_list_repr},
    controls={control_list_repr},
    source="{source}",
    version="0.1.0",
)
def detect(resources: list[TerraformResource]) -> list[Evidence]:
    """TODO: emit Evidence records for resources matching this detector."""
    out: list[Evidence] = []
    _now = datetime.now(UTC)
    for _r in resources:
        # TODO: filter by resource type, walk content, emit per-resource evidence.
        pass
    return out
'''
    (folder / "detector.py").write_text(detector_body, encoding="utf-8")

    ksi_yaml = (
        "\n".join(
            f"  - id: {k}\n"
            f'    name: "TODO"\n'
            f"    coverage: partial\n"
            f"    notes: >\n"
            f"      TODO: explain what this detector evidences for {k}.\n"
            for k in ksi
        )
        if ksi
        else "  []  # supplementary detector (no KSI mapping)\n"
    )
    control_yaml = (
        "\n".join(
            f"  - id: {c}\n"
            f"    evidence_type: infrastructure\n"
            f"    coverage: partial\n"
            f"    notes: >\n"
            f"      TODO: explain what this detector evidences for {c}.\n"
            for c in control
        )
        if control
        else "  []\n"
    )
    mapping_body = f"""detector_id: {detector_id}

ksis:
{ksi_yaml}
controls:
{control_yaml}"""
    (folder / "mapping.yaml").write_text(mapping_body, encoding="utf-8")

    evidence_body = f"""detector_id: {detector_id}

evidence_shape:
  resource_type: string         # TODO: e.g. "aws_..."
  resource_name: string         # the Terraform logical name
  pattern: enum                 # TODO: a stable per-detector pattern label
  detail: string?               # short positive-state description
  gap: string?                  # present only on negative-state evidence
"""
    (folder / "evidence.yaml").write_text(evidence_body, encoding="utf-8")

    ksi_table = (
        "\n".join(f"| {k} | partial | TODO |" for k in ksi)
        if ksi
        else "| — | — | supplementary 800-53-only detector |"
    )
    controls_table = (
        "\n".join(f"| {c} | infrastructure | partial |" for c in control)
        if control
        else "| — | — | — |"
    )
    readme_body = f"""# {detector_id}

TODO: one-paragraph description of what this detector evidences.

## What it proves

- TODO

## What it does NOT prove

- TODO

## KSI mapping

| KSI | Coverage | Notes |
|---|---|---|
{ksi_table}

## 800-53 controls

| Control | Evidence type | Coverage |
|---|---|---|
{controls_table}

## Fixtures

- `fixtures/should_match/<example>.tf` — positive-evidence cases.
- `fixtures/should_not_match/<example>.tf` — negative-evidence cases.

## Next steps

1. Fill in `detector.py`'s `detect` function.
2. Add Terraform fixtures under `fixtures/should_match/` and
   `fixtures/should_not_match/`.
3. Add `tests/detectors/test_{cloud}_{name}.py` mirroring the other
   detector test files.
4. Add an import line to
   `src/efterlev/detectors/{cloud}/__init__.py` (or the top-level
   `src/efterlev/detectors/__init__.py`, depending on the cloud's
   convention) so the registry picks this detector up.
5. Bump `EXPECTED_DETECTORS` in `scripts/triage.sh` and the count
   sites listed in the test_triage_constant_alignment / deep-smoke
   / test_cli tests.
"""
    (folder / "README.md").write_text(readme_body, encoding="utf-8")

    typer.echo(f"Scaffolded detector folder: {folder.relative_to(detectors_root.parent.parent)}")
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo(f"  1. Fill in {folder.name}/detector.py's detect() function.")
    typer.echo(f"  2. Add fixtures under {folder.name}/fixtures/should_{{match,not_match}}/.")
    typer.echo(f"  3. Add tests/detectors/test_{cloud}_{name}.py.")
    typer.echo(
        f"  4. Add `from efterlev.detectors.{cloud} import {name}` to "
        f"`src/efterlev/detectors/__init__.py` so the registry loads it."
    )
    typer.echo(
        "  5. Bump EXPECTED_DETECTORS in scripts/triage.sh + the test count "
        "sites; see the README's `Next steps` section for details."
    )


@detectors_app.command("show")
def detectors_show(
    detector_id: str = typer.Argument(
        ...,
        help="Detector id to inspect (e.g. `aws.encryption_s3_at_rest`).",
    ),
) -> None:
    """Print a detector's metadata + mapping notes + evidence shape + README.

    The read/inspect counterpart to `detectors list` (registry summary)
    and `detectors new` (write/scaffold). Surfaces what `detectors list`
    elides: the mapping.yaml KSI/control coverage notes, the evidence.yaml
    shape, the README's "what it proves / does NOT prove" framing, and the
    fixture file counts. Useful for contributors choosing what to extend
    and for operators who want to understand what a scanned-evidence
    record means without opening the source tree.

    Sections degrade gracefully: if a detector folder is missing
    `mapping.yaml` / `evidence.yaml` / `README.md` / `fixtures/`, that
    section is skipped rather than erroring. Detectors registered from
    outside the source tree (e.g. third-party packages) print only the
    registry-level header.
    """
    import efterlev.detectors  # noqa: F401  (registration side-effect)
    from efterlev.detectors.base import get_registry

    registry = get_registry()
    if detector_id not in registry:
        typer.echo(f"error: detector `{detector_id}` is not registered.", err=True)
        # Helpful suggestions: substring overlap, then prefix match, then alpha-near.
        ids = sorted(registry)
        similar = [k for k in ids if detector_id in k or k in detector_id]
        if not similar and "." in detector_id:
            cloud_prefix = detector_id.split(".", 1)[0] + "."
            similar = [k for k in ids if k.startswith(cloud_prefix)][:5]
        if similar:
            typer.echo("  did you mean:", err=True)
            for s in similar[:5]:
                typer.echo(f"    - {s}", err=True)
        else:
            typer.echo("  list all detectors with `efterlev detectors list`.", err=True)
        raise typer.Exit(code=1)

    spec = registry[detector_id]
    tag = "" if spec.ksis else "  [800-53 only]"
    typer.echo(f"{spec.id}@{spec.version}  source={spec.source}{tag}")
    typer.echo(f"  KSIs:     {', '.join(spec.ksis) if spec.ksis else '—'}")
    typer.echo(f"  Controls: {', '.join(spec.controls) if spec.controls else '—'}")

    folder = _detector_folder(spec)
    if folder is None:
        return  # third-party / dynamically-registered: no source tree to read

    _print_detector_mapping_notes(folder / "mapping.yaml")
    _print_detector_evidence_shape(folder / "evidence.yaml")
    _print_detector_readme_excerpt(folder / "README.md")
    _print_detector_fixture_summary(folder / "fixtures")


def _detector_folder(spec: Any) -> Path | None:
    """Return the source folder of a detector, or None if not introspectable.

    Uses the registered callable's module __file__ — works for both
    editable installs and pip-installed wheels (the .py source ships
    inside the wheel; site-packages is just a different parent dir).
    """
    import inspect as _inspect

    module = _inspect.getmodule(spec.callable)
    module_file = getattr(module, "__file__", None) if module is not None else None
    if module_file is None:
        return None
    return Path(module_file).resolve().parent


def _print_detector_mapping_notes(path: Path) -> None:
    """Print KSI + control notes from mapping.yaml (if present + parseable)."""
    if not path.is_file():
        return
    import yaml

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return  # malformed mapping.yaml: skip the section silently

    ksis = data.get("ksis") or []
    controls = data.get("controls") or []
    if not ksis and not controls:
        return

    typer.echo("")
    typer.echo("Mapping notes:")
    for ksi in ksis if isinstance(ksis, list) else []:
        if not isinstance(ksi, dict):
            continue
        coverage = ksi.get("coverage") or "—"
        typer.echo(f"  {ksi.get('id', '?')} ({coverage}): {ksi.get('name', '')}")
        notes = (ksi.get("notes") or "").strip()
        if notes:
            for line in _wrap_paragraph(notes, indent="    "):
                typer.echo(line)
    for ctrl in controls if isinstance(controls, list) else []:
        if not isinstance(ctrl, dict):
            continue
        coverage = ctrl.get("coverage") or "—"
        evidence_type = ctrl.get("evidence_type") or "—"
        typer.echo(f"  {ctrl.get('id', '?')} ({coverage}, {evidence_type})")
        notes = (ctrl.get("notes") or "").strip()
        if notes:
            for line in _wrap_paragraph(notes, indent="    "):
                typer.echo(line)


def _print_detector_evidence_shape(path: Path) -> None:
    """Print evidence-shape keys + types from evidence.yaml (if present)."""
    if not path.is_file():
        return
    import yaml

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return

    shape = data.get("evidence_shape")
    if not isinstance(shape, dict) or not shape:
        return

    typer.echo("")
    typer.echo("Evidence shape (per-record `content` keys):")
    for key, type_decl in shape.items():
        type_str = str(type_decl).split("#", 1)[0].strip()
        typer.echo(f"  {key}: {type_str}")


def _print_detector_readme_excerpt(path: Path) -> None:
    """Print the first paragraph of README.md (excluding the H1 title)."""
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    excerpt: list[str] = []
    seen_body = False
    for line in lines:
        stripped = line.strip()
        if not seen_body:
            if stripped.startswith("# ") or not stripped:
                continue
            seen_body = True
        # Stop at the first H2/H3 (the README's section structure starts).
        if stripped.startswith("## ") or stripped.startswith("### "):
            break
        if stripped:
            excerpt.append(stripped)
        elif excerpt:
            break  # paragraph break terminates the lead

    if not excerpt:
        return
    typer.echo("")
    typer.echo("README:")
    for line in _wrap_paragraph(" ".join(excerpt), indent="  "):
        typer.echo(line)


def _print_detector_fixture_summary(fixtures_dir: Path) -> None:
    """Print fixture file counts from should_match/ + should_not_match/."""
    if not fixtures_dir.is_dir():
        return
    sm = fixtures_dir / "should_match"
    snm = fixtures_dir / "should_not_match"
    sm_files = (
        [p for p in sm.iterdir() if p.is_file() and p.name != ".gitkeep"] if sm.is_dir() else []
    )
    snm_files = (
        [p for p in snm.iterdir() if p.is_file() and p.name != ".gitkeep"] if snm.is_dir() else []
    )
    if not sm.is_dir() and not snm.is_dir():
        return
    typer.echo("")
    typer.echo("Fixtures:")
    typer.echo(f"  should_match:     {len(sm_files)} file(s)")
    for p in sorted(sm_files):
        typer.echo(f"    - {p.name}")
    typer.echo(f"  should_not_match: {len(snm_files)} file(s)")
    for p in sorted(snm_files):
        typer.echo(f"    - {p.name}")


def _wrap_paragraph(text: str, *, indent: str, width: int = 76) -> list[str]:
    """Wrap a paragraph for terminal printing. Honors hard newlines as breaks."""
    import textwrap

    out: list[str] = []
    for para in text.split("\n\n"):
        normalized = " ".join(para.split())
        if not normalized:
            continue
        wrapped = textwrap.wrap(
            normalized, width=width, initial_indent=indent, subsequent_indent=indent
        )
        out.extend(wrapped)
    return out


# --- boundary CLI (Priority 4.2, 2026-04-27) ------------------------------

# A FedRAMP customer typically has GovCloud Terraform in scope and commercial
# Terraform out of scope. These verbs let them declare scope and inspect it.
# `set` writes the workspace's `[boundary]` config; `show` reads it; `check`
# tests one path against the current rules. Acts on `.efterlev/config.toml`
# under `--target` (default: cwd), the same convention as every other
# workspace-touching command.


@boundary_app.command("set")
def boundary_set(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose `.efterlev/config.toml` will be modified.",
    ),
    include: list[str] = typer.Option(
        [],
        "--include",
        help=(
            "Glob pattern (gitignore-style) for paths IN the boundary. "
            "Pass multiple times for multiple patterns."
        ),
    ),
    exclude: list[str] = typer.Option(
        [],
        "--exclude",
        help=(
            "Glob pattern (gitignore-style) for paths OUT of the boundary. "
            "Pass multiple times. Exclude takes precedence over include."
        ),
    ),
    append: bool = typer.Option(
        False,
        "--append",
        help=(
            "Append the supplied patterns to the existing config instead of "
            "replacing them (the v0.1.9+ default is replace). Use this when "
            "you want to add patterns without re-stating the existing ones."
        ),
    ),
    replace: bool = typer.Option(
        False,
        "--replace",
        help=(
            "Deprecated: replace is now the default. Kept as a no-op for "
            "backwards-compat with pre-v0.1.9 scripts that passed it explicitly."
        ),
        hidden=True,
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help=(
            "Prompt for include / exclude globs interactively instead of "
            "passing them via --include / --exclude flags. Useful for "
            "first-time setup -- the prompt explains what each glob does. "
            "Mutually exclusive with --include / --exclude."
        ),
    ),
) -> None:
    """Declare which paths are inside the FedRAMP authorization boundary.

    Patterns are gitignore-style: `boundary/**` matches anything under
    `boundary/`, `**/main.tf` matches all `main.tf` anywhere. Exclude
    takes precedence over include — a path matching both is `out_of_boundary`.

    Default behavior REPLACES the existing config (matches the verb's
    intuition — "set" reads as "set this, replacing what was there").
    Pass `--append` to add patterns to the existing config without
    restating it. Pre-v0.1.9 the default was append; that surprised
    users running `boundary set` expecting clean replace semantics.

    Without an explicit declaration, every Evidence is `boundary_undeclared`
    and the workspace cannot produce a defensible scope statement to a 3PAO.
    """
    from efterlev.config import BoundaryConfig, load_config, save_config
    from efterlev.errors import ConfigError

    # `--replace` is now a no-op (kept for backwards-compat); reading it
    # silently is fine since replace is the default. Surface a one-line
    # deprecation note so scripts notice and can drop the flag.
    if replace and not append:
        typer.echo(
            "note: --replace is now the default and a no-op; you can drop it from your invocation.",
            err=True,
        )

    # --interactive is mutually exclusive with --include / --exclude. Held
    # in LIMITATIONS.md "Future ideas" since v0.1.18+; OSS-friction
    # reducer for first-time boundary setup. Default behavior unchanged
    # (the existing --include/--exclude flags work as they always did).
    if interactive and (include or exclude):
        typer.echo(
            "error: --interactive is mutually exclusive with --include / --exclude. "
            "Either supply globs via flags OR pass --interactive and answer the "
            "prompts; not both.",
            err=True,
        )
        raise typer.Exit(code=2)

    if interactive:
        include, exclude = _boundary_set_interactive_prompt(append)
        if not include and not exclude:
            typer.echo(
                "error: no include or exclude globs supplied; aborting without writing config.",
                err=True,
            )
            raise typer.Exit(code=2)
    elif not include and not exclude:
        typer.echo(
            "error: pass at least one --include or --exclude pattern (or "
            "--interactive to be prompted). Use `efterlev boundary show` to "
            "view current rules.",
            err=True,
        )
        raise typer.Exit(code=2)

    root = target.resolve()
    config_path = root / ".efterlev" / "config.toml"
    try:
        config = load_config(config_path)
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    if append:
        new_include = list(config.boundary.include) + list(include)
        new_exclude = list(config.boundary.exclude) + list(exclude)
    else:
        # v0.1.9 default: replace. Pre-v0.1.9 default was append, which
        # made `boundary set` accumulate patterns silently.
        new_include = list(include)
        new_exclude = list(exclude)

    new_boundary = BoundaryConfig(include=new_include, exclude=new_exclude)
    new_config = config.model_copy(update={"boundary": new_boundary})
    save_config(new_config, config_path)

    typer.echo(f"Updated {config_path}")
    if new_include:
        typer.echo(f"  include ({len(new_include)}): {', '.join(new_include)}")
    if new_exclude:
        typer.echo(f"  exclude ({len(new_exclude)}): {', '.join(new_exclude)}")


def _boundary_set_interactive_prompt(append: bool) -> tuple[list[str], list[str]]:
    """Prompt the user for include + exclude globs interactively.

    Returns `(include_globs, exclude_globs)`. Either or both may be
    empty -- the caller decides whether that's an error (the CLI
    refuses to write an all-empty config to avoid wiping the existing
    one accidentally).

    Held in LIMITATIONS.md "Future ideas" since v0.1.18+; OSS-friction
    reducer for first-time boundary setup. The prompt walks through
    what each glob does so a user who's never run `boundary set`
    before doesn't have to read the man-page-equivalent first.
    """
    typer.echo("")
    typer.echo("Interactive boundary setup. Glob patterns are gitignore-style:")
    typer.echo("  - `boundary/**` matches anything under `boundary/`.")
    typer.echo("  - `**/main.tf` matches all `main.tf` files anywhere.")
    typer.echo("  - exclude patterns take precedence over include patterns.")
    if append:
        typer.echo("  (--append: patterns will be ADDED to the existing config.)")
    else:
        typer.echo("  (default: patterns will REPLACE the existing config.)")
    typer.echo("")

    include: list[str] = []
    typer.echo("Include globs (paths IN the boundary). Empty input ends the list.")
    while True:
        glob = typer.prompt(
            f"  include #{len(include) + 1}",
            default="",
            show_default=False,
        ).strip()
        if not glob:
            break
        include.append(glob)

    exclude: list[str] = []
    typer.echo("")
    typer.echo("Exclude globs (paths OUT of the boundary). Empty input ends the list.")
    while True:
        glob = typer.prompt(
            f"  exclude #{len(exclude) + 1}",
            default="",
            show_default=False,
        ).strip()
        if not glob:
            break
        exclude.append(glob)

    # Bail BEFORE the confirm prompt if both lists are empty -- that's
    # not a user choice the confirm prompt should mediate; the caller
    # refuses with a clear "no globs supplied" error.
    if not include and not exclude:
        return include, exclude

    typer.echo("")
    typer.echo("Will write the following to .efterlev/config.toml:")
    if include:
        typer.echo(f"  include ({len(include)}): {', '.join(include)}")
    else:
        typer.echo("  include: (none)")
    if exclude:
        typer.echo(f"  exclude ({len(exclude)}): {', '.join(exclude)}")
    else:
        typer.echo("  exclude: (none)")

    if not typer.confirm("Confirm?", default=True):
        typer.echo("Aborted; no config changes written.")
        raise typer.Exit(code=0)

    return include, exclude


@boundary_app.command("show")
def boundary_show(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose boundary will be displayed.",
    ),
) -> None:
    """Show the workspace's current boundary declaration.

    When no patterns are configured, the workspace is `boundary_undeclared`
    and Evidence flows through unfiltered — agents cannot tell a 3PAO which
    findings represent the in-scope boundary.
    """
    from efterlev.config import load_config
    from efterlev.errors import ConfigError

    root = target.resolve()
    try:
        config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    boundary = config.boundary
    if not boundary.include and not boundary.exclude:
        typer.echo("No boundary declared (status: boundary_undeclared).")
        typer.echo("")
        typer.echo("Run `efterlev boundary set --include 'boundary/**'` to declare scope.")
        return

    typer.echo("Boundary patterns (gitignore-style):")
    if boundary.include:
        typer.echo(f"  include ({len(boundary.include)}):")
        for p in boundary.include:
            typer.echo(f"    {p}")
    if boundary.exclude:
        typer.echo(f"  exclude ({len(boundary.exclude)}):")
        for p in boundary.exclude:
            typer.echo(f"    {p}")
    typer.echo("")
    typer.echo("Decision precedence: exclude wins over include.")


@boundary_app.command("check")
def boundary_check(
    path: str = typer.Argument(
        ...,
        help="Repo-relative path to test against the boundary patterns.",
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose boundary patterns will be applied.",
    ),
) -> None:
    """Test whether a repo-relative path is in/out of the declared boundary.

    Useful when adjusting boundary patterns to verify the rules behave
    as expected before re-running a scan.
    """
    from efterlev.boundary import compute_boundary_state
    from efterlev.config import load_config
    from efterlev.errors import ConfigError

    root = target.resolve()
    try:
        config = load_config(root / ".efterlev" / "config.toml")
    except ConfigError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    state = compute_boundary_state(path, config.boundary)
    typer.echo(f"{path}  →  {state}")


@boundary_app.command("discover")
def boundary_discover(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo to scan for boundary signals.",
    ),
    as_json: bool = typer.Option(
        False,
        "--json",
        help="Emit the signals as JSON instead of the human-readable report.",
    ),
) -> None:
    """Surface candidate in-boundary dependencies from your Terraform.

    Answers the first question every FedRAMP 20x customer asks — "what's my
    boundary?" — by walking the IaC for external touchpoints: non-AWS provider
    integrations, cross-account references, remote state, hardcoded third-party
    SaaS endpoints, and external data sources.

    This is reconnaissance, not a decision: Efterlev surfaces candidates and
    explains why each matters; you (and your 3PAO) decide what is in vs out of
    the authorization boundary. Deterministic — no LLM, no network, no writes.
    No workspace required.
    """
    import json as _json
    from dataclasses import asdict

    from efterlev.boundary_discovery import CATEGORY_LABELS, discover_boundary_signals

    root = target.resolve()
    if not root.is_dir():
        typer.echo(f"error: target is not a directory: {target}", err=True)
        raise typer.Exit(code=1)

    signals = discover_boundary_signals(root)
    tf_count = sum(1 for _ in root.rglob("*.tf"))

    if as_json:
        typer.echo(_json.dumps([asdict(s) for s in signals], indent=2))
        return

    if not signals:
        typer.echo(
            f"Boundary reconnaissance — no external-dependency signals in {tf_count} .tf file(s)."
        )
        typer.echo("")
        typer.echo(
            "That can mean a self-contained boundary, or that dependencies live "
            "outside your IaC (SaaS wired up by hand). Review manually, then declare "
            "scope with `efterlev boundary set`."
        )
        return

    typer.echo("Boundary reconnaissance — candidate in-boundary dependencies")
    typer.echo(f"{len(signals)} signal(s) across {tf_count} .tf file(s)")
    last_category = None
    for s in signals:
        if s.category != last_category:
            typer.echo("")
            typer.echo(CATEGORY_LABELS.get(s.category, s.category))
            last_category = s.category
        where = ", ".join(s.locations[:4]) + (" …" if len(s.locations) > 4 else "")
        typer.echo(f"  • {s.title}  ({where})")
        typer.echo(f"    {s.detail}")
    typer.echo("")
    typer.echo(
        "These are candidates, not a boundary. You and your 3PAO decide what is in "
        "vs out of the authorization boundary. When you've decided, declare it:"
    )
    typer.echo("  efterlev boundary set --include 'infra/**' --include '.github/workflows/**'")


@app.command("next")
def next_steps(
    target: Path = typer.Option(Path("."), "--target", help="Path to the workspace."),
    as_json: bool = typer.Option(False, "--json", help="Emit the worklist as JSON."),
    limit: int = typer.Option(8, "--limit", help="Max items to show before summarizing the rest."),
) -> None:
    """Your ranked next steps — what to do next, in impact order, with the command to run.

    A companion, not a scanner: given the current state of your workspace it
    surfaces the single most important next step plus an impact-ranked worklist
    (each item carries the exact command), and re-ranks every time you run it as
    you close items. Deterministic — no LLM, no network, no writes.
    """
    import json as _json
    from dataclasses import asdict

    from efterlev.worklist import build_worklist

    root = target.resolve()
    wl = build_worklist(root)

    if as_json:
        typer.echo(
            _json.dumps(
                {
                    "stage": wl.stage,
                    "headline": wl.headline,
                    "overall_pct": wl.overall_pct,
                    "activity": [{"stage": s, "when": w} for s, w in wl.activity],
                    "items": [asdict(i) for i in wl.items],
                },
                indent=2,
            )
        )
        return

    typer.echo("")
    if wl.overall_pct is not None:
        typer.echo(f"  Readiness {wl.overall_pct:.0f}%  ·  {wl.stage}")
    typer.echo(f"  → {wl.headline}")
    typer.echo("")
    shown = wl.items[:limit]
    for n, item in enumerate(shown, start=1):
        typer.echo(f"  {n}. {item.title}   [{item.impact} impact · {item.effort}]")
        typer.echo(f"     {item.why}")
        typer.echo(f"     $ {item.command}")
    remaining = len(wl.items) - len(shown)
    if remaining > 0:
        typer.echo("")
        typer.echo(
            f"  … and {remaining} more. Close these, then re-run `efterlev next` — it re-ranks."
        )
    if wl.activity:
        typer.echo("")
        typer.echo("  Activity — " + " · ".join(f"{s}: {w}" for s, w in wl.activity))
    typer.echo("")


@app.command()
def doctor(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the workspace whose .efterlev/ state will be inspected.",
    ),
) -> None:
    """Run pre-flight diagnostic checks.

    Verifies Python version, ANTHROPIC_API_KEY shape, .efterlev/
    initialization, FRMR cache freshness, and Bedrock credentials.
    Prints per-check pass/warn/fail with remediation hints. Exits
    non-zero only on `fail`-status checks (warnings are informational).

    No network calls — strictly local introspection.
    """
    from efterlev.cli.doctor import has_failures, run_doctor_checks

    root = target.resolve()
    checks = run_doctor_checks(root)

    badge = {"pass": "✓", "warn": "!", "fail": "✗"}
    typer.echo("Efterlev doctor — pre-flight checks")
    typer.echo("")
    for c in checks:
        line = f"  {badge[c.status]} {c.status:5}  {c.name:24}  {c.detail}"
        typer.echo(line)
        if c.hint:
            typer.echo(f"           hint: {c.hint}")
    typer.echo("")
    fail_count = sum(1 for c in checks if c.status == "fail")
    warn_count = sum(1 for c in checks if c.status == "warn")
    pass_count = sum(1 for c in checks if c.status == "pass")
    typer.echo(f"summary: {pass_count} pass, {warn_count} warn, {fail_count} fail")

    if has_failures(checks):
        raise typer.Exit(code=1)


def _latest_glob(directory: Path, pattern: str) -> Path | None:
    """Return the most recent file matching `pattern` in `directory`, or None."""
    if not directory.is_dir():
        return None
    matches = list(directory.glob(pattern))
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def _has_inherited_declaration(root: Path) -> bool:
    """True iff the workspace config declares CSP-inherited controls.

    Used by `report run` to conditionally insert the `scope apply` stage.
    Tolerant of a missing/unparseable config (fresh workspace before
    init) — returns False rather than raising.
    """
    config_path = root / ".efterlev" / "config.toml"
    if not config_path.is_file():
        return False
    try:
        from efterlev.config import load_config

        return bool(load_config(config_path).scope.inherited)
    except Exception:
        return False


def _latest_glob_across_dirs(directories: list[Path], pattern: str) -> Path | None:
    """v0.1.160 / #365: find the most-recent match across multiple dirs.
    Used to surface artifacts that may live in either the new
    `efterlev-out/` location or the legacy `.efterlev/` location during
    the path transition. Returns the absolute newest across all dirs.
    """
    candidates: list[Path] = []
    for d in directories:
        if d.is_dir():
            candidates.extend(d.glob(pattern))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _print_report_artifact_summary(target_resolved: Path) -> None:
    """Print a single summary block listing every artifact `/report` just
    produced. Pulls the latest matching file from each artifact directory
    so the list reflects the run that just completed (not a stale prior run).

    Quiet on missing artifacts — if a stage was skipped or failed earlier,
    the row is simply absent from the table. v0.1.144 / #349.

    v0.1.160 / #365: looks across both the new `efterlev-out/` location
    (default for fresh writes) and the legacy `.efterlev/` location so
    upgraded workspaces continue to surface historical reports until
    they age out via natural rotation.
    """
    # New artifacts land here; legacy artifacts may exist in
    # `.efterlev/reports/` on workspaces that pre-date v0.1.160.
    report_dirs = _iter_report_dirs(target_resolved)
    poam_subdirs = [d / "poam" for d in report_dirs]
    oscal_subdirs = [d / "oscal" for d in report_dirs]
    vdr_subdirs = [d / "vdr" for d in report_dirs]
    inventory_subdirs = [d / "inventory" for d in report_dirs]
    if not any(d.is_dir() for d in report_dirs):
        return
    artifacts: list[tuple[str, Path | None]] = [
        ("Scan (JSON)", _latest_glob_across_dirs(report_dirs, "scan-*.json")),
        (
            "Inventory (HTML, open in browser)",
            _latest_glob_across_dirs(inventory_subdirs, "inventory-*.html"),
        ),
        (
            "Inventory (JSON sidecar)",
            _latest_glob_across_dirs(inventory_subdirs, "inventory-*.json"),
        ),
        (
            "Gap report (HTML, open in browser)",
            _latest_glob_across_dirs(report_dirs, "gap-*.html"),
        ),
        ("Gap report (JSON sidecar)", _latest_glob_across_dirs(report_dirs, "gap-*.json")),
        (
            "Documentation (HTML, open in browser)",
            _latest_glob_across_dirs(report_dirs, "documentation-*.html"),
        ),
        (
            "Documentation (JSON sidecar)",
            _latest_glob_across_dirs(report_dirs, "documentation-*.json"),
        ),
        ("FRMR attestation (JSON)", _latest_glob_across_dirs(report_dirs, "attestation-*.json")),
        ("POA&M (markdown)", _latest_glob_across_dirs(poam_subdirs, "poam-*.md")),
        (
            "VDR (RFC-0012, JSON)",
            _latest_glob_across_dirs(vdr_subdirs, "vdr-*.json"),
        ),
        (
            "VDR (RFC-0012, markdown)",
            _latest_glob_across_dirs(vdr_subdirs, "vdr-*.md"),
        ),
        ("OSCAL POA&M (JSON)", _latest_glob_across_dirs(oscal_subdirs, "poam-*.json")),
        (
            "OSCAL Component-Definition (JSON)",
            _latest_glob_across_dirs(oscal_subdirs, "component-definition-*.json"),
        ),
    ]
    typer.echo("")
    typer.echo("Artifacts produced by this run:")
    for label, path in artifacts:
        if path is None:
            continue
        typer.echo(f"  {label:<42}  {path}")
    typer.echo("")
    typer.echo("  Tip: HTML reports open in any browser; JSON/OSCAL files feed 3PAO tooling.")
    # v0.1.161 / #366: point at whichever reports dir actually has files.
    # New visible dir (v0.1.160+) is preferred; legacy hidden dir only
    # surfaces when an upgraded workspace still has pre-v0.1.160 history.
    open_target = next((d for d in report_dirs if d.is_dir()), report_dirs[0])
    typer.echo(f"  Open reports dir:  open {open_target}")
    typer.echo("  (Inside `efterlev shell`, use `/open reports` instead.)")


@report_app.command("run")
def report_run(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Path to the repo to run the full pipeline against.",
    ),
    skip_init: bool = typer.Option(
        False,
        "--skip-init",
        help="Skip the init step. Useful when re-running on a workspace already initialized.",
    ),
    skip_document: bool = typer.Option(
        False,
        "--skip-document",
        help=(
            "Skip the Documentation Agent stage. Useful for fast iteration "
            "loops where you only care about gap classification."
        ),
    ),
    skip_inventory: bool = typer.Option(
        False,
        "--skip-inventory",
        help=(
            "Skip the consolidated-resource-inventory stage (v0.1.164 / "
            "#369; RFC-0017 artifact). Deterministic + free; runs in "
            "well under a second. Pass this flag to opt out for fast "
            "iteration loops where the inventory artifact isn't needed."
        ),
    ),
    skip_poam: bool = typer.Option(
        False,
        "--skip-poam",
        help="Skip the POA&M generation stage.",
    ),
    skip_vdr: bool = typer.Option(
        False,
        "--skip-vdr",
        help=(
            "Skip the VDR (Vulnerability Detection & Response, RFC-0012-shaped) "
            "stage. VDR graduated to default-on in `report run` at v0.1.163 / "
            "#368 ahead of RFC-0012 finalization; pass this flag to opt out "
            "(e.g., for fast iteration loops where VDR output isn't needed). "
            "POA&M remains program-current until RFC-0012 standardizes."
        ),
    ),
    with_oscal: bool = typer.Option(
        False,
        "--with-oscal",
        help=(
            "Also emit OSCAL 1.0.4 POA&M + Component-Definition artifacts. "
            "OFF by default since v0.1.223: FedRAMP 20x does not require "
            "OSCAL (the ADS standard is format-agnostic; no 20x pilot "
            "participant used OSCAL; FedRAMP recommends implementing from "
            "the FRMR JSON, which Efterlev produces natively). OSCAL export "
            "remains available — here and via `efterlev oscal export` — for "
            "Rev5-ecosystem / GRC-tool interop."
        ),
    ),
    skip_oscal: bool = typer.Option(
        False,
        "--skip-oscal",
        hidden=True,
        help=(
            "Deprecated no-op (v0.1.223): OSCAL stages no longer run by "
            "default, so there is nothing to skip. Use --with-oscal to "
            "opt in. This flag will be removed in a future release."
        ),
    ),
    skip_inspector: bool = typer.Option(
        False,
        "--skip-inspector",
        help=(
            "Skip the 3PAO inspector report stage (v0.1.168 / #374). The "
            "inspector is a single-page HTML view designed for assessor "
            "review — per-KSI RFC-0017 checklist, statement + controls + "
            "cadence + citations + narrative. Deterministic, no LLM cost, "
            "runs in <1s. Opt out for fast iteration loops."
        ),
    ),
    skip_scan: bool = typer.Option(
        False,
        "--skip-scan",
        help=(
            "Skip the scan stage. Useful when you've already run "
            "`efterlev scan --plan plan.json` separately and want the "
            "pipeline to pick up from agent gap. v0.1.158 / #363."
        ),
    ),
    scan_plan: Path | None = typer.Option(
        None,
        "--scan-plan",
        help=(
            "Path to a terraform plan JSON. When set, the scan stage uses "
            "plan-JSON mode (`efterlev scan --plan PATH`) for full module "
            "coverage. Mutually exclusive with --skip-scan. v0.1.158 / #363."
        ),
    ),
    watch: bool = typer.Option(
        False,
        "--watch",
        help=(
            "After the initial run, watch --target for changes to .tf, "
            ".tfvars, .yml, .yaml, .json files and re-run the pipeline "
            "(debounced 2s). Ctrl-C exits."
        ),
    ),
    profile: str | None = typer.Option(
        None,
        "--profile",
        help=(
            "v0.1.166 / #371: select a named profile from "
            "`.efterlev/config.toml`'s `[profile.<name>]` section. "
            "Overrides boundary / baseline / scan-target for this run. "
            "Output lands under `efterlev-out/profile-<name>/` so "
            "profiles don't collide. Equivalent to setting "
            "`EFTERLEV_PROFILE=<name>` in the environment; the flag "
            "exports the env var for every subprocess the orchestrator "
            "launches. Omit for backward-compatible single-environment "
            "behavior."
        ),
    ),
) -> None:
    """Run the full pipeline: init → scan → agent gap → agent document → poam → oscal.

    Each stage runs in sequence; if any stage exits non-zero, the
    pipeline stops and propagates the exit code. Per-stage flags
    (--skip-init, --skip-document, --skip-poam, --skip-oscal) let you
    tailor the pipeline to your situation. Add --watch to stay running
    and re-execute the pipeline on file changes (debounced 2s).

    OSCAL graduated to default-on at v0.1.111: the pipeline emits both
    OSCAL POA&M and Component-Definition JSON alongside the existing
    markdown POA&M. Both OSCAL artifacts validate against NIST OSCAL
    1.0.4 schema (v0.1.106) + FedRAMP rule layer (v0.1.107) + NIST
    canonical oscal-cli (v0.1.110).
    """
    target_resolved = target.resolve()

    # v0.1.166 / #371: --profile sets EFTERLEV_PROFILE for the rest of
    # the run. Validate the name and export it so every subprocess the
    # orchestrator launches picks up the same profile. load_config()
    # reads the env var; the path helpers read it too.
    if profile is not None:
        from efterlev.profile import PROFILE_ENV_VAR, validate_profile_name

        try:
            validate_profile_name(profile)
        except ValueError as e:
            typer.echo(f"error: {e}", err=True)
            raise typer.Exit(code=2) from e
        os.environ[PROFILE_ENV_VAR] = profile

    # v0.1.158 / #363: --skip-scan and --scan-plan are mutually exclusive
    # — --skip-scan means "I'll scan separately"; --scan-plan means
    # "pipeline runs scan with --plan PATH". Validate up front.
    if skip_scan and scan_plan is not None:
        typer.echo(
            "error: --skip-scan and --scan-plan are mutually exclusive. "
            "Pick one: --skip-scan if you've already run scan separately, "
            "or --scan-plan PATH to have the pipeline scan in plan-JSON mode.",
            err=True,
        )
        raise typer.Exit(code=2)
    if scan_plan is not None and not scan_plan.is_file():
        typer.echo(
            f"error: --scan-plan path does not exist: {scan_plan}",
            err=True,
        )
        raise typer.Exit(code=2)

    def run_once() -> None:
        # Capture pipeline start INSIDE run_once so --watch iterations
        # roll only their own spend (v0.1.84 cost-rollup). datetime
        # imported lazily to avoid a top-of-module hit.
        from datetime import UTC, datetime

        pipeline_started_at = datetime.now(UTC)
        target_str = str(target_resolved)

        # Treat `.efterlev/` as initialized only when the FRMR cache is
        # actually present — that's what `scan` and the agents need. The
        # canonical pattern of `.efterlev/manifests/` committed to git +
        # `.efterlev/cache/` gitignored means a fresh clone has the
        # workspace dir present (the manifests) but the cache missing,
        # and any check that only looked at the dir would skip init and
        # then fail at scan time. (govnotes-demo CI hit this on
        # 2026-04-30.)
        frmr_cache = target_resolved / ".efterlev" / "cache" / "frmr_document.json"
        efterlev_initialized = frmr_cache.is_file()
        skip_init_effective = skip_init or efterlev_initialized

        stages: list[tuple[str, list[str]]] = []
        if not skip_init_effective:
            init_args = ["init", "--target", target_str]
            # If the workspace dir already exists (e.g. only `.efterlev/
            # manifests/` is committed) but the cache doesn't, init would
            # otherwise fail with "directory already exists". Pass
            # --force so init regenerates the cache + provenance store
            # while leaving customer-authored content (manifests/) intact.
            if (target_resolved / ".efterlev").is_dir():
                init_args.append("--force")
            stages.append(("init", init_args))
        # v0.1.158 / #363: --skip-scan / --scan-plan support.
        if not skip_scan:
            scan_args = ["scan", "--target", target_str]
            if scan_plan is not None:
                scan_args.extend(["--plan", str(scan_plan.resolve())])
            stages.append(("scan", scan_args))
        if not skip_inventory:
            # v0.1.164 / #369: consolidated resource inventory per RFC-0017.
            # Slotted between scan and agent gap — runs subsecond, free,
            # produces a one-page artifact the assistant can surface
            # ("here's what's in scope") before the long-running LLM
            # stages start.
            stages.append(("inventory", ["inventory", "--target", target_str]))
        # v0.1.171 / #377: apply CSP-inherited declarations (if any) after
        # scan so the deterministic cross-check sees the scan's evidence,
        # and before agent gap so gap skips the inherited KSIs. No-op +
        # omitted when nothing is declared.
        if _has_inherited_declaration(target.resolve()):
            stages.append(("scope apply", ["scope", "apply", "--target", target_str]))
        stages.append(("agent gap", ["agent", "gap", "--target", target_str]))
        # v0.1.226: the deterministic gap-derived emits (poam, vdr, oscal)
        # run BEFORE `agent document`. They derive from the gap
        # classifications, not the narratives, so a documentation-stage
        # failure must not take them down — the 2026-06-11 onboarding run
        # lost POA&M + VDR + OSCAL to a doc-agent guard rejection at KSI
        # 29/60 even though all three were already fully computable. Only
        # the inspector (which assembles the attestation narratives) stays
        # downstream of document.
        if not skip_poam:
            stages.append(("poam", ["poam", "--target", target_str]))
        if not skip_vdr:
            # v0.1.163 / #368: VDR (Vulnerability Detection & Response,
            # RFC-0012-shaped) is now a default `report run` stage.
            # Ahead of RFC-0012 finalization; ships alongside POA&M
            # which remains program-current until the RFC standardizes.
            # `--format both` (the command default) emits JSON + markdown.
            stages.append(("vdr", ["vdr", "--target", target_str]))
        if skip_oscal:
            # Deprecated at v0.1.223 (OSCAL flipped default-on -> opt-in,
            # so skipping is the default). Warn-and-ignore mirrors the
            # --allow-cfn deprecation pattern (v0.1.99 -> v0.1.102).
            typer.echo(
                "warning: --skip-oscal is deprecated and a no-op since "
                "v0.1.223 — OSCAL stages no longer run by default. Use "
                "--with-oscal to opt in. The flag will be removed in a "
                "future release.",
                err=True,
            )
        if with_oscal:
            # Opt-in since v0.1.223 (default-on v0.1.111 -> v0.1.222).
            # FedRAMP 20x does not require OSCAL: the ADS standard is
            # format-agnostic, no 20x pilot participant used OSCAL, and
            # FedRAMP recommends implementing from the FRMR JSON. The
            # export stays for Rev5-ecosystem / GRC interop. DECISIONS
            # 2026-06-09. Both stages are deterministic (no LLM cost).
            stages.append(
                ("oscal poam", ["oscal", "export", "--kind", "poam", "--target", target_str])
            )
            stages.append(
                (
                    "oscal component-definition",
                    [
                        "oscal",
                        "export",
                        "--kind",
                        "component-definition",
                        "--target",
                        target_str,
                    ],
                )
            )
        if not skip_document:
            # v0.1.226: document moved AFTER the deterministic emits (see
            # comment above the poam stage). It still precedes the
            # inspector, which assembles its narratives.
            stages.append(("agent document", ["agent", "document", "--target", target_str]))
        if not skip_inspector:
            # v0.1.168 / #374: 3PAO inspector — single-page HTML assembling
            # FRMR statements + attestation narratives + RFC-0017 gate into
            # one assessor-facing view. Runs last so it picks up the
            # attestation just generated by `agent document`.
            stages.append(("inspector", ["report", "inspector", "--target", target_str]))

        typer.echo(f"Pipeline: {' → '.join(name for name, _ in stages)}")
        # v0.1.157 / #362: upfront duration framing. Customer feedback:
        # a 24-min run on a real ~140-resource repo left the user
        # wondering whether the pipeline had hung. Print the rough
        # range BEFORE the first stage so the wait is grounded.
        # Sizing heuristic: gap is 60 KSIs x ~7-15s/KSI = 7-15 min on
        # Sonnet/Opus first run; document is 35-60 LLM calls x ~5-10s
        # = 3-10 min; deterministic stages add <1s combined. Cache
        # replays drop the LLM stages to <1s/stage.
        has_llm_stage = any(name in ("agent gap", "agent document") for name, _ in stages)
        if has_llm_stage:
            typer.echo(
                "Expected wall-clock: ~10-25 min on a fresh run "
                "(`agent gap` is 60 sequential LLM calls — the longest stretch); "
                "cache replays on unchanged source are near-instant per stage."
            )
        typer.echo("")

        # v0.1.154 / #359: per-stage wall-clock so users can compare runs
        # across models, fixture sizes, and cache states. List of
        # (stage_name, elapsed_seconds) — populated as each stage exits
        # successfully, rendered in the summary block at the end of the run.
        import time

        stage_timings: list[tuple[str, float]] = []

        for stage_idx, (name, args) in enumerate(stages, start=1):
            typer.echo("")
            typer.echo(f"━━━ [{stage_idx}/{len(stages)}] {name} ━━━")
            typer.echo("")
            stage_t0 = time.perf_counter()
            try:
                # `standalone_mode=False` makes Click RETURN an int exit code
                # on `typer.Exit` (rather than raising). We must check the
                # return value as well as the exception path; otherwise a
                # stage that raises `typer.Exit(code=1)` slips through and
                # the orchestrator falsely declares success.
                rv = app(args, standalone_mode=False)
            except typer.Exit as e:
                # Defensive — older click versions (or non-standalone wrappers)
                # may still raise here.
                if e.exit_code and e.exit_code != 0:
                    typer.echo(
                        f"\nerror: pipeline stopped — `{name}` exited with code {e.exit_code}",
                        err=True,
                    )
                    raise
            except SystemExit as e:
                code = e.code if isinstance(e.code, int) else 1
                if code != 0:
                    typer.echo(
                        f"\nerror: pipeline stopped — `{name}` raised SystemExit({code})",
                        err=True,
                    )
                    raise typer.Exit(code=code) from e
            else:
                # Returned-int-exit-code path. Click sets `rv` to the int
                # the stage raised via `typer.Exit(code=N)` when
                # standalone_mode=False; non-zero is failure.
                if isinstance(rv, int) and rv != 0:
                    typer.echo(
                        f"\nerror: pipeline stopped — `{name}` exited with code {rv}",
                        err=True,
                    )
                    raise typer.Exit(code=rv)
            stage_elapsed = time.perf_counter() - stage_t0
            stage_timings.append((name, stage_elapsed))
            typer.echo("")
            typer.echo(f"✓ [{name}] done in {_format_elapsed(stage_elapsed)}")

        typer.echo("")
        typer.echo("✓ Pipeline complete.")

        # v0.1.154 / #359: timing summary table — one row per stage in
        # execution order, plus a total. Useful for comparing runs across
        # different models (default Sonnet vs Haiku vs Bedrock) or fixture
        # sizes. Always printed (even on a single-stage run) so the format
        # is consistent and easy to grep.
        if stage_timings:
            typer.echo("")
            typer.echo("Pipeline timing:")
            label_w = max(len(name) for name, _ in stage_timings)
            for name, elapsed in stage_timings:
                typer.echo(f"  {name.ljust(label_w)}  {_format_elapsed(elapsed)}")
            total = sum(elapsed for _, elapsed in stage_timings)
            typer.echo(f"  {'total'.ljust(label_w)}  {_format_elapsed(total)}")

        # v0.1.144 / #349: one summary block listing every artifact the
        # pipeline just produced. Customer feedback: with 6 stages each
        # printing their own paths interleaved with progress, it was hard
        # to find the actual outputs at the end of a long run. This block
        # is the single "here's what to open" cheat sheet.
        _print_report_artifact_summary(target_resolved)

        # v0.1.84: total cost rollup across every agent stage in this
        # pipeline run.
        from efterlev.agents.cost_summary import summarize_run_cost

        total_cost_line = summarize_run_cost(target_resolved, pipeline_started_at)
        if total_cost_line:
            typer.echo("")
            typer.echo(f"Pipeline total: {total_cost_line.removeprefix('cost: ')}")

    # First run: always. (pipeline_started_at is captured inside
    # run_once so --watch iterations get a fresh window each time.)
    try:
        run_once()
    except typer.Exit:
        if not watch:
            raise
        # In watch mode, the initial pipeline failure shouldn't kill the
        # watcher — the user can fix the issue and re-trigger by saving.
        typer.echo("(initial run failed; continuing to watch — fix and save to retry)", err=True)

    if not watch:
        return

    # --watch: stay running, re-execute on file change.
    from efterlev.cli.watch import watch_loop

    typer.echo("")
    typer.echo(f"Watching {target_resolved} for changes (Ctrl-C to exit)...", err=True)

    def on_change() -> None:
        typer.echo("", err=True)
        typer.echo("━━━ change detected — re-running pipeline ━━━", err=True)
        typer.echo("")
        try:
            run_once()
        except typer.Exit as e:
            typer.echo(
                f"(re-run failed with exit {e.exit_code}; fix and save to retry)",
                err=True,
            )

    try:
        watch_loop(target_resolved, on_change=on_change)
    except KeyboardInterrupt:
        typer.echo("", err=True)
        typer.echo("Watch mode exited.", err=True)


@report_app.command("diff")
def report_diff(
    prior: Path = typer.Argument(
        ...,
        help=(
            "Path to a prior gap-report JSON sidecar (e.g. "
            "efterlev-out/reports/gap-<ts>.json on v0.1.160+; "
            ".efterlev/reports/gap-<ts>.json on pre-v0.1.160 stores)."
        ),
    ),
    current: Path = typer.Argument(
        ...,
        help="Path to the current gap-report JSON sidecar.",
    ),
    target: Path = typer.Option(
        Path("."),
        "--target",
        help=(
            "Path to the workspace whose efterlev-out/reports/ will receive "
            "the diff output (v0.1.160+ visible-output split)."
        ),
    ),
    base_branch: str = typer.Option(
        "",
        "--base-branch",
        help=(
            "Optional base-branch label for the markdown PR-comment header (e.g. `main`). "
            "Empty defaults to the generic 'base branch' phrase. Only used when "
            "--print-markdown is set."
        ),
    ),
    print_markdown: bool = typer.Option(
        False,
        "--print-markdown",
        help=(
            "Print the markdown PR-comment to stdout (in addition to writing files). "
            "ConMon Lite v1 (DECISIONS 2026-05-11 PR #241) uses this to capture the "
            "comment body for posting. Distinct sticky-comment marker "
            "<!-- efterlev-conmon-lite-v1 --> from the v0 marker."
        ),
    ),
) -> None:
    """Compute and render a diff between two gap-report JSON sidecars.

    Emits both `gap-diff-<ts>.html` (reviewer-friendly) and
    `gap-diff-<ts>.json` (machine-readable, schema-versioned) under
    `.efterlev/reports/` of the target workspace. Exits non-zero if the
    diff contains any regressed KSIs — useful in CI for blocking PRs
    that regress posture.
    """
    from efterlev.reports import (
        compute_gap_diff,
        render_gap_diff_html,
        render_gap_diff_markdown,
    )

    if not prior.is_file():
        typer.echo(f"error: prior file not found: {prior}", err=True)
        raise typer.Exit(code=1)
    if not current.is_file():
        typer.echo(f"error: current file not found: {current}", err=True)
        raise typer.Exit(code=1)

    try:
        prior_data = json.loads(prior.read_text(encoding="utf-8"))
        current_data = json.loads(current.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        typer.echo(f"error: invalid JSON: {e}", err=True)
        raise typer.Exit(code=1) from e

    try:
        diff = compute_gap_diff(prior_data, current_data)
    except ValueError as e:
        typer.echo(f"error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"Comparing {prior.name} → {current.name}")
    typer.echo(f"  added:      {len(diff.added)}")
    typer.echo(f"  removed:    {len(diff.removed)}")
    typer.echo(f"  improved:   {len(diff.improved)}")
    typer.echo(f"  regressed:  {len(diff.regressed)}")
    typer.echo(f"  unchanged:  {len(diff.unchanged)}")

    root = target.resolve()
    reports_dir = _reports_dir(root)
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    generated_at = datetime.now().astimezone()

    html_body = render_gap_diff_html(diff, generated_at=generated_at)
    html_path = reports_dir / f"gap-diff-{timestamp}.html"
    html_path.write_text(html_body, encoding="utf-8")

    json_path = reports_dir / f"gap-diff-{timestamp}.json"
    json_path.write_text(json.dumps(diff.model_dump(), indent=2, sort_keys=True), encoding="utf-8")

    typer.echo("")
    typer.echo(f"HTML report:  {html_path}")
    typer.echo(f"JSON sidecar: {json_path}")

    if print_markdown:
        markdown = render_gap_diff_markdown(diff, base_branch=base_branch or None)
        typer.echo("")
        typer.echo(markdown)

    if diff.regressed:
        typer.echo("")
        typer.echo(
            f"warning: {len(diff.regressed)} KSI(s) regressed since the prior scan.",
            err=True,
        )
        raise typer.Exit(code=2)


@report_app.command("inspector")
def report_inspector(
    target: Path = typer.Option(
        Path("."),
        "--target",
        help="Workspace root. Defaults to the current directory.",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        help=(
            "Explicit output path. Defaults to "
            "<workspace>/efterlev-out/reports/inspector-<ts>.html (profile-scoped "
            "if a profile is active)."
        ),
    ),
) -> None:
    """Render the 3PAO inspector HTML — single-page assessor view (v0.1.168+).

    Composes the FRMR catalog statements + the latest attestation artifact
    (if present) + the RFC-0017 readiness gate into one HTML page.
    Per-KSI rows collapse to id + status pill + 5-item RFC-0017 dots;
    click to expand for statement + controls + cadence + citations +
    narrative.

    Pure deterministic. No LLM call. Safe to call after any combination
    of `init` / `scan` / `agent gap` / `agent document` — rows
    gracefully render whatever data is present.
    """
    from efterlev import __version__ as efterlev_version
    from efterlev.frmr import FrmrDocument
    from efterlev.models.attestation_artifact import AttestationArtifact
    from efterlev.primitives.generate.generate_inspector_report import (
        GenerateInspectorReportInput,
        generate_inspector_report,
    )
    from efterlev.primitives.readiness import (
        compute_rfc_0017_gate,
        load_latest_claim_statuses,
    )

    root = target.resolve()
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Run `efterlev init` first.",
            err=True,
        )
        raise typer.Exit(code=1)

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    baseline_ksi_ids = list(frmr_doc.indicators.keys())

    # Catalog entries: pull statement + theme + controls per KSI.
    catalog_entries: list[dict[str, object]] = []
    for ksi_id, indicator in frmr_doc.indicators.items():
        catalog_entries.append(
            {
                "ksi_id": ksi_id,
                "theme": indicator.theme,
                "statement": indicator.statement or "",
                "controls_mapped": list(indicator.controls),
            }
        )

    # Workspace cadence config — items 3 + 4 of the gate.
    machine_cadence = ""
    human_cadence = ""
    config_path = root / ".efterlev" / "config.toml"
    profile_label: str | None = None
    try:
        from efterlev.config import load_config

        config = load_config(config_path)
        machine_cadence = config.cadence.machine_validation_cadence
        human_cadence = config.cadence.non_machine_validation_cadence
    except Exception as e:
        typer.echo(f"warning: could not load workspace config ({e})", err=True)

    from efterlev.profile import get_active_profile

    profile_label = get_active_profile()

    gate_report = compute_rfc_0017_gate(
        root,
        baseline_ksi_ids=baseline_ksi_ids,
        machine_validation_cadence=machine_cadence,
        human_validation_cadence=human_cadence,
    )

    # Latest attestation artifact (optional — fresh workspaces won't have one).
    from efterlev.paths import iter_report_dirs

    attestation_path = _latest_glob_across_dirs(iter_report_dirs(root), "attestation-*.json")
    attestation: AttestationArtifact | None = None
    if attestation_path is not None:
        try:
            attestation = AttestationArtifact.model_validate_json(
                attestation_path.read_text(encoding="utf-8")
            )
        except Exception as e:
            typer.echo(
                f"warning: could not parse attestation at {attestation_path} ({e})",
                err=True,
            )

    # v0.1.173 / #379: per-KSI status from the store (same source as the
    # gate) so the status pill stays consistent with the gate dots — fixes
    # inherited / gap-without-document KSIs showing "unclassified".
    store_statuses = load_latest_claim_statuses(root, baseline_ksi_ids=set(baseline_ksi_ids))

    # v0.1.174 / #380: run the generate under an active store so the
    # primitive records its provenance like every other generate command
    # (inventory, poam, oscal). Without this the @primitive decorator
    # warned "called with no active provenance store" straight to the
    # user's stdout on every inspector run.
    from efterlev.provenance import ProvenanceStore, active_store

    with ProvenanceStore(root) as store, active_store(store):
        result = generate_inspector_report(
            GenerateInspectorReportInput(
                catalog_entries=catalog_entries,
                attestation=attestation,
                store_statuses=store_statuses,
                gate_report=gate_report,
                workspace_label=root.name,
                profile_label=profile_label,
                baseline_id="fedramp-20x-moderate",
                tool_version=efterlev_version,
            )
        )

    # Resolve output path. --out wins; otherwise reports_dir/inspector-<ts>.html.
    if out is not None:
        out_path = out.resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        reports_dir = _reports_dir(root)
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        out_path = reports_dir / f"inspector-{timestamp}.html"

    out_path.write_text(result.rendered, encoding="utf-8")
    typer.echo(f"Inspector report: {out_path}")
    typer.echo(
        f"  Gate verdict: {'PASS' if gate_report.passed else 'FAIL'} "
        f"({result.passing_count}/{result.passing_count + result.failing_count} "
        "KSIs passing all 5 PVA items)"
    )


if __name__ == "__main__":
    app()
