"""Slash command registry + dispatcher for the shell.

Each command is a `SlashCommand` carrying its canonical name, aliases,
one-line description, and a callable that takes (Console, args, state_ctx)
and returns whether the workspace state changed (so the caller knows
whether to re-print the status block).

Most dispatchers delegate to the existing Typer commands by direct
function call — there is no `efterlev` subprocess. Streaming agent
output reaches the user because the underlying commands write to
stderr directly; rich's `Console` doesn't interfere with that.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from efterlev.shell.layout import (
    render_error,
    render_ok,
    render_status_only,
)
from efterlev.shell.state import read_snapshot, suggest_next


@dataclass
class ShellContext:
    """Mutable per-session state. Held by the session loop; passed to handlers."""

    root: Path
    console: Console
    should_exit: bool = False


@dataclass(frozen=True)
class SlashCommand:
    """One slash command registered with the shell."""

    name: str
    """Canonical name with leading slash, e.g. `/scan`."""
    aliases: tuple[str, ...]
    """Short forms accepted as equivalent, e.g. `('/s',)` for `/scan`."""
    summary: str
    """One-line description shown in /help."""
    handler: Callable[[ShellContext, list[str]], bool]
    """Returns True if workspace state changed (caller re-prints status)."""
    arg_hint: str = ""
    """Optional argument hint shown in /help, e.g. `<findings.json>`."""
    phase: str = "inspect"
    """Phase grouping for /help and /map (v0.1.145 / #350).

    One of: `setup`, `workspace`, `ingest`, `inspect`, `help`. The
    `workspace` phase commands form the pipeline ladder that /map
    visualizes; the others are cross-cutting.
    """


# Phase metadata for /help and /map. Order is the display order in /help;
# `workspace` is the pipeline ladder /map visualizes top-to-bottom.
PHASES: list[tuple[str, str]] = [
    ("plan", "Plan (Stage 0 — orient before you scan; no workspace needed)"),
    ("setup", "Setup (one-time per machine / workspace)"),
    ("workspace", "Pipeline (run in order; /map shows where you are)"),
    ("ingest", "Ingest (alternative evidence sources, optional)"),
    ("inspect", "Inspect (read-only, anytime)"),
    ("help", "Help and navigation"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Handlers
# ─────────────────────────────────────────────────────────────────────────────


def _dispatch_efterlev(ctx: ShellContext, args: list[str]) -> int:
    """Run an `efterlev` subcommand as a subprocess from the workspace root.

    Subprocess (not direct function call) on purpose: Typer commands
    call `sys.exit` on errors, which would tear down the shell. The
    process boundary contains that. Streaming stays intact because
    we don't capture stdout/stderr — the child writes straight to
    our terminal.

    Safety: `cmd` is a fixed-shape list — `[sys.executable, "-m",
    "efterlev", *args]`. Shell expansion is impossible (no
    `shell=True`, list form passed straight to execve). User-supplied
    `args` reach Typer's argument parser, not a shell — Typer rejects
    unknown options. The semgrep audit rule for `subprocess.run` with
    non-static input doesn't apply: the threat model it warns about
    (shell injection via concatenated strings) is structurally
    excluded by the list+no-shell form.
    """
    cmd = [sys.executable, "-m", "efterlev", *args]
    # v0.1.146 / #351: signal "called from shell" so subcommands can swap
    # `efterlev <verb>` suggestion text for `/<verb>` slash commands the
    # shell user actually types. Inherited via the env passed to the child.
    import os

    env = {**os.environ, "EFTERLEV_SHELL": "1"}
    try:
        result = subprocess.run(cmd, cwd=ctx.root, check=False, env=env)  # nosemgrep
        return result.returncode
    except FileNotFoundError:
        render_error(
            ctx.console,
            f"could not invoke {sys.executable} -m efterlev",
            hint="is efterlev installed in the active Python env?",
        )
        return 1


def _handle_plan(ctx: ShellContext, args: list[str]) -> bool:
    # Stage 0: workspace-free, reads bundled catalog data only — no --target.
    _dispatch_efterlev(ctx, ["plan", *args])
    return False  # read-only


def _handle_catalog(ctx: ShellContext, args: list[str]) -> bool:
    # Stage 0: workspace-free KSI reference — no --target.
    _dispatch_efterlev(ctx, ["catalog", *args])
    return False  # read-only


def _handle_init(ctx: ShellContext, args: list[str]) -> bool:
    rc = _dispatch_efterlev(ctx, ["init", *args, "--target", str(ctx.root)])
    if rc == 0:
        render_ok(ctx.console, "workspace initialized")
        return True
    return False


def _handle_doctor(ctx: ShellContext, args: list[str]) -> bool:
    _dispatch_efterlev(ctx, ["doctor", *args, "--target", str(ctx.root)])
    return False  # read-only


def _handle_scan(ctx: ShellContext, args: list[str]) -> bool:
    rc = _dispatch_efterlev(ctx, ["scan", "--target", str(ctx.root), *args])
    return rc == 0


def _handle_agent(ctx: ShellContext, args: list[str]) -> bool:
    # `/agent` requires a sub-command (gap/document/remediate).
    if not args:
        render_error(
            ctx.console,
            "missing subcommand",
            hint="try /agent gap, /agent document, or /agent remediate",
        )
        return False
    rc = _dispatch_efterlev(ctx, ["agent", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_report(ctx: ShellContext, args: list[str]) -> bool:
    rc = _dispatch_efterlev(ctx, ["report", "run", "--target", str(ctx.root), *args])
    return rc == 0


def _handle_poam(ctx: ShellContext, args: list[str]) -> bool:
    # The CLI command is just `efterlev poam` — no `emit` subcommand exists.
    rc = _dispatch_efterlev(ctx, ["poam", "--target", str(ctx.root), *args])
    return rc == 0


def _handle_oscal(ctx: ShellContext, args: list[str]) -> bool:
    if not args:
        render_error(
            ctx.console,
            "missing subcommand",
            hint="try /oscal export --kind poam (or component-definition)",
        )
        return False
    rc = _dispatch_efterlev(ctx, ["oscal", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_import_security_hub(ctx: ShellContext, args: list[str]) -> bool:
    if not args:
        render_error(
            ctx.console,
            "missing path",
            hint="usage: /import security-hub <findings.json>",
        )
        return False
    rc = _dispatch_efterlev(ctx, ["import-security-hub", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_import_config(ctx: ShellContext, args: list[str]) -> bool:
    if not args:
        render_error(
            ctx.console,
            "missing path",
            hint="usage: /import config <evaluations.json>",
        )
        return False
    rc = _dispatch_efterlev(ctx, ["import-config", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_import_prowler(ctx: ShellContext, args: list[str]) -> bool:
    if not args:
        render_error(
            ctx.console,
            "missing path",
            hint="usage: /import prowler <findings.json>",
        )
        return False
    rc = _dispatch_efterlev(ctx, ["import-prowler", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_boundary(ctx: ShellContext, args: list[str]) -> bool:
    rc = _dispatch_efterlev(ctx, ["boundary", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_provenance(ctx: ShellContext, args: list[str]) -> bool:
    _dispatch_efterlev(ctx, ["provenance", *args, "--target", str(ctx.root)])
    return False  # read-only


def _handle_manifests(ctx: ShellContext, args: list[str]) -> bool:
    _dispatch_efterlev(ctx, ["manifests", *args])
    return False  # validation is read-only


def _handle_detectors(ctx: ShellContext, args: list[str]) -> bool:
    _dispatch_efterlev(ctx, ["detectors", *args])
    return False


# ── Built-in commands (don't shell out) ─────────────────────────────────────


def _handle_status(ctx: ShellContext, args: list[str]) -> bool:
    snapshot = read_snapshot(ctx.root)
    render_status_only(ctx.console, snapshot, suggest_next(snapshot))
    return False


def _handle_tour(ctx: ShellContext, args: list[str]) -> bool:
    """Interactive walkthrough for new users (see efterlev.shell.tour)."""
    from efterlev.shell.tour import run_tour

    return run_tour(ctx)


def _handle_setup(ctx: ShellContext, args: list[str]) -> bool:
    """Interactive LLM API setup wizard (see efterlev.shell.setup)."""
    from efterlev.shell.setup import run_setup

    return run_setup(ctx)


def _handle_ai(ctx: ShellContext, args: list[str]) -> bool:
    """Single-shot AI Q&A with workspace context (see efterlev.shell.ai)."""
    from efterlev.shell.ai import run_ai_query

    question = " ".join(args)
    return run_ai_query(ctx, question)


def _handle_readiness(ctx: ShellContext, args: list[str]) -> bool:
    """Score how close this workspace is to 3PAO engagement."""
    _dispatch_efterlev(ctx, ["readiness", *args, "--target", str(ctx.root)])
    return False  # read-only


def _handle_package(ctx: ShellContext, args: list[str]) -> bool:
    """Bundle the workspace's artifacts into a 3PAO-ready submission package."""
    rc = _dispatch_efterlev(ctx, ["submission", "package", *args, "--target", str(ctx.root)])
    return rc == 0


def _handle_help(ctx: ShellContext, args: list[str]) -> bool:
    from rich.text import Text

    from efterlev.shell.layout import ACCENT, MUTED

    if args:
        # /help <command> — detailed view (TODO: pull from underlying Typer help)
        target = args[0] if args[0].startswith("/") else "/" + args[0]
        match = _COMMANDS_BY_NAME.get(target)
        if match is None:
            render_error(ctx.console, f"unknown command {target!r}")
            return False
        ctx.console.print()
        ctx.console.print(
            Text("  " + match.name, style=ACCENT)
            + (Text(" " + match.arg_hint, style=MUTED) if match.arg_hint else Text(""))
        )
        ctx.console.print(Text("    " + match.summary))
        if match.aliases:
            ctx.console.print(
                Text("    aliases: ", style=MUTED) + Text(", ".join(match.aliases), style=ACCENT)
            )
        ctx.console.print()
        return False

    # No-arg /help — phase-grouped, with state markers on pipeline commands
    # (v0.1.145 / #350). Customers were missing the natural pipeline order
    # in the flat list.
    snapshot = read_snapshot(ctx.root)
    next_command = suggest_next(snapshot)
    next_name = next_command.command.split()[0] if next_command else None
    pipeline_state = _pipeline_state_for_commands(snapshot, next_name)

    ctx.console.print()
    for phase_id, phase_label in PHASES:
        cmds = [c for c in COMMANDS if c.phase == phase_id]
        if not cmds:
            continue
        ctx.console.print(Text("  " + phase_label, style=ACCENT))
        label_w = max(len(c.name + (" " + c.arg_hint if c.arg_hint else "")) for c in cmds)
        for c in cmds:
            head = c.name + (" " + c.arg_hint if c.arg_hint else "")
            marker = pipeline_state.get(c.name, "  ")
            ctx.console.print(
                Text(f"    {marker} ", style=ACCENT)
                + Text(head.ljust(label_w) + "  ", style=ACCENT)
                + Text(c.summary, style=MUTED)
            )
        ctx.console.print()
    ctx.console.print(
        Text("  Markers: ", style=MUTED)
        + Text("✓ done", style=ACCENT)
        + Text("  ", style=MUTED)
        + Text("→ next", style=ACCENT)
        + Text("  ", style=MUTED)
        + Text("○ pending", style=ACCENT)
    )
    ctx.console.print(
        Text("  Try ", style=MUTED)
        + Text("/map", style=ACCENT)
        + Text(" for the pipeline diagram, or ", style=MUTED)
        + Text("/help <command>", style=ACCENT)
        + Text(" for detail on one.", style=MUTED)
    )
    ctx.console.print()
    return False


# Pipeline commands in display order — used by /map and by `_pipeline_state_for_commands`
# to compute per-command markers (✓ / → / ○).
_PIPELINE_ORDER: list[tuple[str, str]] = [
    ("/init", "create the .efterlev/ workspace"),
    ("/scan", "find evidence in your IaC"),
    ("/agent", "classify (gap), narrate (document), or fix (remediate)"),
    ("/report", "all of the above + POA&M + OSCAL in one shot"),
    ("/readiness", "scorecard for 3PAO scoping"),
    ("/package", "ZIP everything for 3PAO handoff"),
]


def _pipeline_state_for_commands(snapshot, next_name: str | None) -> dict[str, str]:
    """Compute the ✓/→/○ marker for each pipeline command from workspace state.

    Mirrors the artifact-aware ladder in `suggest_next` (v0.1.144) but
    expressed per-command rather than as a single Next. Non-pipeline
    commands (in `setup`, `ingest`, `inspect`, `help` phases) get a blank
    marker — they're cross-cutting, not stage-gated.

    `next_name` is the command name `suggest_next` would propose right
    now (e.g. `/scan`) — used to mark exactly one command as → next.
    """
    from efterlev.shell.state import _report_artifacts_present, _submission_package_exists

    efterlev_dir = snapshot.root / ".efterlev"
    scan_epoch = snapshot.last_scan_at.timestamp() if snapshot.last_scan_at else 0.0
    has_init = snapshot.initialized
    has_scan = snapshot.last_scan_at is not None
    has_evidence = (snapshot.evidence_count or 0) > 0
    has_claims = (snapshot.claim_count or 0) > 0
    has_report = has_claims and _report_artifacts_present(efterlev_dir, scan_epoch)
    has_package = has_report and _submission_package_exists(efterlev_dir, scan_epoch)

    done_set: set[str] = set()
    if has_init:
        done_set.add("/init")
    if has_scan and has_evidence:
        done_set.add("/scan")
    if has_claims:
        done_set.add("/agent")
    if has_report:
        done_set.add("/report")
    if has_package:
        done_set.add("/package")
    # /readiness has no good "done" indicator — leave unmarked unless next

    out: dict[str, str] = {}
    for name, _ in _PIPELINE_ORDER:
        if name in done_set:
            out[name] = "✓"
        elif next_name == name:
            out[name] = "→"
        else:
            out[name] = "○"
    return out


def _handle_map(ctx: ShellContext, args: list[str]) -> bool:
    """Pretty pipeline diagram with progress markers (v0.1.145 / #350).

    A picture worth a hundred commands. Shows the linear pipeline
    (init → scan → agent gap → report → readiness → package) plus the
    two side-branches off `/agent` (document + remediate), each
    annotated with ✓/→/○ based on workspace state.
    """
    from rich.text import Text

    from efterlev.shell.layout import ACCENT, MUTED

    snapshot = read_snapshot(ctx.root)
    next_command = suggest_next(snapshot)
    next_name = next_command.command.split()[0] if next_command else None
    state = _pipeline_state_for_commands(snapshot, next_name)

    ctx.console.print()
    ctx.console.print(Text("  Pipeline", style=ACCENT))
    if next_command:
        ctx.console.print(
            Text("    where you are: ", style=MUTED) + Text(next_command.command, style=ACCENT)
        )
    else:
        ctx.console.print(Text("    pipeline complete — submission package built", style=MUTED))
    ctx.console.print()
    label_w = max(len(name) for name, _ in _PIPELINE_ORDER)
    for name, why in _PIPELINE_ORDER:
        marker = state.get(name, "○")
        ctx.console.print(
            Text(f"    {marker} ", style=ACCENT)
            + Text(name.ljust(label_w) + "  ", style=ACCENT)
            + Text(why, style=MUTED)
        )
        if name == "/agent":
            ctx.console.print(
                Text("        " + " " * label_w + "  ", style=ACCENT)
                + Text(
                    "subcommands: gap (classify) | document (narrate) | remediate (fix)",
                    style=MUTED,
                )
            )
    ctx.console.print()
    ctx.console.print(
        Text("  Tip: ", style=MUTED)
        + Text("/report", style=ACCENT)
        + Text(
            " runs the whole pipeline (scan + gap + document + POA&M + OSCAL) in one shot.",
            style=MUTED,
        )
    )
    ctx.console.print()
    return False


# `/open` targets → (kind, glob pattern). `kind` is resolved to a list
# of candidate directories at lookup time via `_open_target_dirs` so
# the v0.1.160 / #365 visible-output split (`efterlev-out/` for new
# writes; `.efterlev/` for legacy) is transparent to the user.
# `None` for the glob means open the directory itself.
_OPEN_TARGETS: dict[str, tuple[str, str | None]] = {
    "reports": ("reports", None),
    "gap": ("reports", "gap-*.html"),
    "docs": ("reports", "documentation-*.html"),
    "documentation": ("reports", "documentation-*.html"),
    "attestation": ("reports", "attestation-*.json"),
    "poam": ("poam", "poam-*.md"),
    "oscal": ("oscal", None),
    "package": ("submissions", None),
    "workspace": ("workspace", None),
    "config": ("config", None),
}


def _open_target_dirs(kind: str, workspace_root: Path) -> list[Path]:
    """Resolve a `/open` target kind into a list of candidate directories,
    NEW first (`efterlev-out/...`) then LEGACY (`.efterlev/...`).

    The caller picks the first existing dir for directory-open targets,
    or globs across all of them for file-pattern targets. This is what
    keeps the v0.1.160 / #365 visible-output transition transparent.
    """
    from efterlev.paths import (
        internal_root,
        oscal_dir,
        poam_dir,
        reports_dir,
        submissions_dir,
    )

    if kind == "reports":
        return [reports_dir(workspace_root), internal_root(workspace_root) / "reports"]
    if kind == "poam":
        return [poam_dir(workspace_root), internal_root(workspace_root) / "reports" / "poam"]
    if kind == "oscal":
        return [oscal_dir(workspace_root), internal_root(workspace_root) / "reports" / "oscal"]
    if kind == "submissions":
        return [submissions_dir(workspace_root), internal_root(workspace_root) / "submissions"]
    if kind == "workspace":
        return [workspace_root]
    if kind == "config":
        return [internal_root(workspace_root)]
    return []


def _handle_open(ctx: ShellContext, args: list[str]) -> bool:
    """Open a workspace artifact (or its directory) in the OS default app.

    Customer pain (v0.1.136 + v0.1.144): outputs land in `.efterlev/`
    which is hidden in Finder. Users see paths in the artifact summary
    but can't easily click through. `/open <target>` jumps straight
    there (v0.1.145 / #350).

    Targets:
      reports / gap / docs / documentation / attestation / poam / oscal
      / package / workspace / config

    No arg → show the target list.
    """
    from rich.text import Text

    from efterlev.shell.layout import ACCENT, MUTED

    if not args:
        ctx.console.print()
        ctx.console.print(Text("  /open <target>", style=ACCENT))
        ctx.console.print(
            Text("    opens an artifact or its directory in your OS default app.", style=MUTED)
        )
        ctx.console.print()
        ctx.console.print(Text("  Targets:", style=ACCENT))
        for target in sorted(_OPEN_TARGETS):
            ctx.console.print(Text(f"    {target}", style=ACCENT))
        ctx.console.print()
        return False

    target = args[0].lower()
    if target not in _OPEN_TARGETS:
        render_error(
            ctx.console,
            f"unknown /open target {target!r}",
            hint=f"valid: {', '.join(sorted(_OPEN_TARGETS))}",
        )
        return False

    kind, glob = _OPEN_TARGETS[target]
    # v0.1.160 / #365: resolve to NEW first then LEGACY, walk both for
    # file-pattern targets so customers in mid-upgrade still find their
    # historical artifacts.
    candidate_dirs = _open_target_dirs(kind, ctx.root)
    if glob is None:
        # Directory-open target: pick the first existing dir (preferring NEW).
        path_to_open = next((d for d in candidate_dirs if d.exists()), None)
        if path_to_open is None:
            shown = candidate_dirs[0] if candidate_dirs else ctx.root
            render_error(
                ctx.console,
                f"nothing to open — {shown} does not exist",
                hint="run /scan, /agent gap, /report, or /package first",
            )
            return False
    else:
        # File-pattern target: glob across all candidate dirs, pick newest.
        matches: list[Path] = []
        for d in candidate_dirs:
            if d.is_dir():
                matches.extend(d.glob(glob))
        if not matches:
            shown = candidate_dirs[0] if candidate_dirs else ctx.root
            render_error(
                ctx.console,
                f"no {glob} files under {shown}",
                hint="run /report (or the specific stage) first",
            )
            return False
        path_to_open = max(matches, key=lambda p: p.stat().st_mtime)

    opener = _os_opener_command()
    if opener is None:
        render_error(
            ctx.console,
            "no OS opener detected (mac: 'open', linux: 'xdg-open', windows: 'start')",
            hint=f"open manually: {path_to_open}",
        )
        return False

    try:
        # nosemgrep: subprocess audit — opener is a fixed binary name, path is
        # a resolved Path under the workspace; no shell=True.
        subprocess.run([opener, str(path_to_open)], check=False)  # nosemgrep
    except OSError as e:
        render_error(ctx.console, f"failed to open {path_to_open}: {e}")
        return False

    render_ok(ctx.console, f"opened {path_to_open}")
    return False


def _os_opener_command() -> str | None:
    """Return the OS-default file opener binary, or None if none is available.

    macOS: `open` (always present). Linux: `xdg-open` (usually present
    on desktops; absent on headless). Windows: `start` via cmd (handled
    by the OS shell, but we don't ship Windows support yet — return
    None gracefully).
    """
    import shutil

    if sys.platform == "darwin":
        return "open"
    if sys.platform.startswith("linux"):
        return shutil.which("xdg-open")
    return None


def _handle_cost(ctx: ShellContext, args: list[str]) -> bool:
    """Show the per-model cost breakdown without re-printing the full snapshot."""
    from rich.text import Text

    from efterlev.shell.layout import ACCENT, MUTED
    from efterlev.shell.state import format_cost_summary

    snapshot = read_snapshot(ctx.root)
    line = format_cost_summary(snapshot)
    ctx.console.print()
    if line:
        ctx.console.print(Text("  Cost  ", style=MUTED) + Text(line))
    else:
        ctx.console.print(Text("  no LLM spend recorded in .efterlev/receipts.log", style=MUTED))
    ctx.console.print()
    _ = ACCENT  # used for future detail formatting
    return False


def _handle_cd(ctx: ShellContext, args: list[str]) -> bool:
    if not args:
        render_error(ctx.console, "missing path", hint="usage: /cd <path>")
        return False
    target = Path(args[0]).expanduser().resolve()
    if not target.is_dir():
        render_error(ctx.console, f"not a directory: {target}")
        return False
    ctx.root = target
    return True  # workspace changed → re-print snapshot


def _handle_clear(ctx: ShellContext, args: list[str]) -> bool:
    # ANSI clear-screen + cursor home. prompt_toolkit's `clear` does the same.
    ctx.console.clear()
    return False


def _handle_exit(ctx: ShellContext, args: list[str]) -> bool:
    ctx.should_exit = True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Registry
# ─────────────────────────────────────────────────────────────────────────────


COMMANDS: list[SlashCommand] = [
    # ── plan (Stage 0 — orient before you scan; no workspace needed) ──────────
    SlashCommand(
        "/plan",
        ("/pl",),
        "map the KSI work breakdown before you scan",
        _handle_plan,
        arg_hint="[--architecture serverless]",
        phase="plan",
    ),
    SlashCommand(
        "/catalog",
        ("/cat",),
        "browse every KSI by theme + its mapped 800-53 controls",
        _handle_catalog,
        arg_hint="[--theme AFR]",
        phase="plan",
    ),
    # ── setup (one-time per machine / workspace) ─────────────────────────────
    SlashCommand(
        "/setup",
        (),
        "configure the LLM (Anthropic API or AWS Bedrock)",
        _handle_setup,
        phase="setup",
    ),
    SlashCommand(
        "/doctor",
        ("/dx",),
        "run the 7 environment checks",
        _handle_doctor,
        phase="setup",
    ),
    SlashCommand(
        "/cd",
        (),
        "change workspace root for this session",
        _handle_cd,
        arg_hint="<path>",
        phase="setup",
    ),
    SlashCommand(
        "/init",
        (),
        "initialize a workspace under the current target",
        _handle_init,
        phase="setup",
    ),
    # ── workspace pipeline (run in order) ────────────────────────────────────
    SlashCommand(
        "/scan",
        ("/s",),
        "find evidence in IaC and workflows",
        _handle_scan,
        phase="workspace",
    ),
    SlashCommand(
        "/agent",
        ("/g",),
        "run gap / document / remediate agent",
        _handle_agent,
        arg_hint="<gap | document | remediate>",
        phase="workspace",
    ),
    SlashCommand(
        "/report",
        (),
        "scan + gap + document + POA&M + OSCAL in one shot",
        _handle_report,
        phase="workspace",
    ),
    SlashCommand(
        "/poam",
        (),
        "emit POA&M markdown",
        _handle_poam,
        phase="workspace",
    ),
    SlashCommand(
        "/oscal",
        (),
        "export OSCAL POA&M or Component-Definition",
        _handle_oscal,
        arg_hint="<poam | component-definition>",
        phase="workspace",
    ),
    SlashCommand(
        "/readiness",
        ("/ready",),
        "score how close you are to a 3PAO scoping conversation",
        _handle_readiness,
        phase="workspace",
    ),
    SlashCommand(
        "/package",
        (),
        "bundle artifacts into a 3PAO-ready submission package",
        _handle_package,
        phase="workspace",
    ),
    # ── ingest (alternative evidence sources, optional) ──────────────────────
    SlashCommand(
        "/import-security-hub",
        ("/imp-sh",),
        "ingest AWS Security Hub ASFF findings",
        _handle_import_security_hub,
        arg_hint="<findings.json>",
        phase="ingest",
    ),
    SlashCommand(
        "/import-config",
        ("/imp-cfg",),
        "ingest AWS Config evaluations",
        _handle_import_config,
        arg_hint="<evaluations.json>",
        phase="ingest",
    ),
    SlashCommand(
        "/import-prowler",
        ("/imp-p",),
        "ingest Prowler native JSON findings",
        _handle_import_prowler,
        arg_hint="<findings.json>",
        phase="ingest",
    ),
    SlashCommand(
        "/manifests",
        (),
        "validate Evidence Manifests",
        _handle_manifests,
        phase="ingest",
    ),
    # ── inspect (read-only, anytime) ─────────────────────────────────────────
    SlashCommand(
        "/status",
        ("/st",),
        "re-print workspace state",
        _handle_status,
        phase="inspect",
    ),
    SlashCommand(
        "/cost",
        (),
        "show LLM cost breakdown by model",
        _handle_cost,
        phase="inspect",
    ),
    SlashCommand(
        "/map",
        (),
        "show the pipeline diagram with progress markers",
        _handle_map,
        phase="inspect",
    ),
    SlashCommand(
        "/open",
        (),
        "open a workspace artifact (or its directory) in the OS default app",
        _handle_open,
        arg_hint="<reports|gap|docs|poam|oscal|package|workspace>",
        phase="inspect",
    ),
    SlashCommand(
        "/provenance",
        ("/p",),
        "inspect a provenance record by id",
        _handle_provenance,
        phase="inspect",
    ),
    SlashCommand(
        "/detectors",
        ("/det",),
        "list registered detectors",
        _handle_detectors,
        phase="inspect",
    ),
    SlashCommand(
        "/boundary",
        ("/b",),
        "view / edit the FedRAMP boundary config",
        _handle_boundary,
        phase="inspect",
    ),
    # ── help and navigation ──────────────────────────────────────────────────
    SlashCommand(
        "/help",
        ("?",),
        "list commands; /help <name> for detail",
        _handle_help,
        arg_hint="[command]",
        phase="help",
    ),
    SlashCommand(
        "/tour",
        ("/walk",),
        "guided walkthrough: init → scan → gap → document → poam",
        _handle_tour,
        phase="help",
    ),
    SlashCommand(
        "/ai",
        ("/ask",),
        "ask the AI a question about Efterlev / your workspace",
        _handle_ai,
        arg_hint="<question>",
        phase="help",
    ),
    SlashCommand(
        "/clear",
        (),
        "clear the screen (history stays)",
        _handle_clear,
        phase="help",
    ),
    SlashCommand(
        "/exit",
        ("/quit", ":q"),
        "leave the shell",
        _handle_exit,
        phase="help",
    ),
]


_COMMANDS_BY_NAME: dict[str, SlashCommand] = {}
for _c in COMMANDS:
    _COMMANDS_BY_NAME[_c.name] = _c
    for _alias in _c.aliases:
        _COMMANDS_BY_NAME[_alias] = _c


def find_command(name: str) -> SlashCommand | None:
    """Look up by canonical name OR alias. None when no match."""
    return _COMMANDS_BY_NAME.get(name)


def parse_input(line: str) -> tuple[str, list[str]] | None:
    """Split user input into (command, args). None when input is blank.

    Returns the command exactly as typed (including leading slash). Args
    follow shell-style quoting so `/cd "path with spaces"` works.
    """
    line = line.strip()
    if not line:
        return None
    try:
        tokens = shlex.split(line)
    except ValueError:
        # Mismatched quotes — pass through with naive split; the
        # handler can complain about a malformed argument.
        tokens = line.split()
    if not tokens:
        return None
    return tokens[0], tokens[1:]
