"""`/tour` — interactive walkthrough for new users.

Walks through the canonical pipeline (`init → scan → agent gap →
agent document → poam`) one step at a time, explaining what each
step does before running it and pausing for Enter at every gate.
Ctrl+C exits the tour cleanly without leaving the shell.

Design intent: beginner-friendly without being patronizing. Each
step explains WHAT it does and WHY it matters in two short
paragraphs, then waits for the user to opt in before running. Steps
that have already run (e.g. `.efterlev/` already exists when the
user starts the tour) are skipped with a one-line note.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from prompt_toolkit import prompt as ptk_prompt
from rich.text import Text

if TYPE_CHECKING:
    from efterlev.shell.commands import ShellContext

ACCENT = "color(73)"
MUTED = "color(244)"
HEADER = "bold"


@dataclass(frozen=True)
class TourStep:
    """One step in the walkthrough."""

    number: int
    """1-based position in the sequence; used in the step header."""
    title: str
    """Short headline, e.g. `/init — create the workspace`."""
    what: str
    """One paragraph: WHAT the step does, in plain English."""
    why: str
    """One paragraph: WHY this matters and what the output is."""
    handler_args: list[str]
    """Args passed to the corresponding handler when the user confirms."""
    handler_name: str
    """Lookup key in the shell command registry, e.g. `/init`."""
    is_already_done: Callable[[Path], bool]
    """Returns True when the workspace state makes this step unnecessary."""


def _init_done(root: Path) -> bool:
    return (root / ".efterlev").is_dir()


def _scan_done(root: Path) -> bool:
    """Heuristic: scan has run if any scan_* primitive record exists in the store."""
    store = root / ".efterlev" / "store.db"
    if not store.is_file():
        return False
    import sqlite3

    try:
        conn = sqlite3.connect(f"file:{store}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM records WHERE primitive LIKE 'scan_%' LIMIT 1")
            return cur.fetchone() is not None
        finally:
            conn.close()
    except sqlite3.Error:
        return False


def _gap_done(root: Path) -> bool:
    """Heuristic: gap agent has run if any claim records exist."""
    store = root / ".efterlev" / "store.db"
    if not store.is_file():
        return False
    import sqlite3

    try:
        conn = sqlite3.connect(f"file:{store}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM records WHERE record_type = 'claim' LIMIT 1")
            return cur.fetchone() is not None
        finally:
            conn.close()
    except sqlite3.Error:
        return False


def _document_done(root: Path) -> bool:
    """Heuristic: documentation agent has run if attestation-*.json exists."""
    return any((root / ".efterlev").glob("attestation-*.json"))


def _poam_done(root: Path) -> bool:
    """Heuristic: poam has been emitted if any poam-*.md exists."""
    return (
        any((root / ".efterlev" / "poam").glob("poam-*.md"))
        if ((root / ".efterlev" / "poam").is_dir())
        else False
    )


TOUR_STEPS: tuple[TourStep, ...] = (
    TourStep(
        number=1,
        title="/init — create the workspace",
        what=(
            "Creates a `.efterlev/` directory under the current target. This holds "
            "your workspace config, scan results, evidence records, drafts, and "
            "receipts. You only do this once per repo."
        ),
        why=(
            "Every subsequent command reads from / writes to this directory. "
            "Without it, the rest of the pipeline has nowhere to land."
        ),
        handler_args=[],
        handler_name="/init",
        is_already_done=_init_done,
    ),
    TourStep(
        number=2,
        title="/scan — find evidence in your IaC",
        what=(
            "Walks your Terraform `.tf` files, AWS CloudFormation templates, "
            "GitHub workflow YAML, and any Evidence Manifests under "
            "`.efterlev/manifests/`. Runs the deterministic detector library "
            "against everything it finds."
        ),
        why=(
            "Detectors emit one Evidence record per pattern they recognize. "
            "Each record is content-addressed (sha256) and stays in the "
            "provenance store; the Gap Agent will cite these IDs by name."
        ),
        handler_args=[],
        handler_name="/scan",
        is_already_done=_scan_done,
    ),
    TourStep(
        number=3,
        title="/agent gap — classify each KSI against the evidence",
        what=(
            "Sends the evidence to the Gap Agent (Claude Opus 4.7 by default). "
            "The agent classifies all 60 FedRAMP 20x KSIs as implemented / "
            "partial / not_implemented / not_applicable, citing specific "
            "evidence records for each judgment."
        ),
        why=(
            "This is the core compliance assessment. Takes ~60-90 seconds and "
            "spends ~$1-2 on Opus (less on Haiku). Output is a Claim record "
            "per KSI, all linked back to the cited evidence — auditable."
        ),
        handler_args=["gap"],
        handler_name="/agent",
        is_already_done=_gap_done,
    ),
    TourStep(
        number=4,
        title="/agent document — draft FRMR attestation narratives",
        what=(
            "Sends the classifications to the Documentation Agent (Sonnet 4.6). "
            "Drafts FRMR-compatible JSON attestations + a color-coded HTML report "
            "summarizing the assessment."
        ),
        why=(
            "FRMR is the machine-readable format FedRAMP 20x is standardizing on. "
            "The HTML report is the artifact you'd share with a 3PAO for review."
        ),
        handler_args=["document"],
        handler_name="/agent",
        is_already_done=_document_done,
    ),
    TourStep(
        number=5,
        title="/poam — emit the POA&M for 3PAO review",
        what=(
            "Generates a Plan-of-Action-and-Milestones markdown listing every "
            "open KSI gap, with severity heuristics and reviewer-ready formatting."
        ),
        why=(
            "POA&M is what 3PAOs actually read first. It's the punch list of "
            "what's broken and what severity each item carries. Everything in "
            "it is DRAFT — humans confirm severities and add remediation plans."
        ),
        handler_args=[],
        handler_name="/poam",
        is_already_done=_poam_done,
    ),
)


def run_tour(ctx: ShellContext) -> bool:
    """Execute the walkthrough. Returns True if any step changed workspace state.

    Does NOT abort the shell on Ctrl+C — tour exits early, shell continues.
    """
    from efterlev.shell.commands import find_command

    console = ctx.console

    # Intro
    console.print()
    console.print(Text("  Efterlev walkthrough", style=HEADER))
    console.print()
    console.print(
        Text(
            "  Five steps from empty repo to 3PAO-ready POA&M. Each step\n"
            "  explains what it does and why, then waits for you to press\n"
            "  Enter before running. Ctrl+C at any prompt exits the tour\n"
            "  without leaving the shell.",
            style=MUTED,
        )
    )
    console.print()

    state_changed_overall = False

    for step in TOUR_STEPS:
        if step.is_already_done(ctx.root):
            console.print(
                Text(f"  Step {step.number} of {len(TOUR_STEPS)} ", style=MUTED)
                + Text(step.title, style=ACCENT)
                + Text("  (already done, skipping)", style=MUTED)
            )
            console.print()
            continue

        # Show step header + explanation
        console.print(
            Text(f"  Step {step.number} of {len(TOUR_STEPS)}  ", style=MUTED)
            + Text(step.title, style=ACCENT)
        )
        console.print()
        for line in step.what.split("\n"):
            console.print(Text("  " + line, style=""))
        console.print()
        for line in step.why.split("\n"):
            console.print(Text("  " + line, style=MUTED))
        console.print()

        # Pause for Enter
        try:
            ptk_prompt(
                f"  Press Enter to run {step.handler_name} "
                f"{' '.join(step.handler_args)} (Ctrl+C to leave the tour)  "
            )
        except (KeyboardInterrupt, EOFError):
            console.print()
            console.print(Text("  tour exited; shell continues", style=MUTED))
            console.print()
            return state_changed_overall

        # Run the handler
        cmd = find_command(step.handler_name)
        if cmd is None:
            console.print(
                Text(
                    f"  internal error: handler {step.handler_name} not found",
                    style="bold red",
                )
            )
            return state_changed_overall

        console.print()
        try:
            step_changed = cmd.handler(ctx, step.handler_args)
        except KeyboardInterrupt:
            console.print()
            console.print(Text("  command interrupted; tour exited", style=MUTED))
            return state_changed_overall

        if step_changed:
            state_changed_overall = True
        console.print()

    # All done
    console.print(Text("  ✓ Walkthrough complete.", style=ACCENT))
    console.print()
    console.print(
        Text("  Try ", style=MUTED)
        + Text("/status", style=ACCENT)
        + Text(" to see the final workspace state, ", style=MUTED)
        + Text("/cost", style=ACCENT)
        + Text(" for the LLM spend\n  breakdown, or ", style=MUTED)
        + Text("/report", style=ACCENT)
        + Text(" to re-run the whole pipeline.", style=MUTED)
    )
    console.print()
    return state_changed_overall
