"""Read workspace state for the shell snapshot.

Pure-read helpers: never mutate the workspace. Each function returns a
small dataclass the layout module can render. Failures (missing files,
malformed receipts) degrade to "unknown" rather than raising — the
shell should keep going even when the workspace is partially broken.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from efterlev.agents.cost_summary import _aggregate_by_model, _short_model_name
from efterlev.llm.pricing import estimate_cost_usd, is_bedrock_model
from efterlev.provenance.receipts import ReceiptLog


@dataclass(frozen=True)
class WorkspaceSnapshot:
    """A read-only view of workspace state for shell rendering.

    Each field is best-effort: `None` means "couldn't determine"
    rather than "explicitly zero/empty." The layout layer uses that
    distinction (e.g. evidence_count=0 prints "0 evidence", while
    evidence_count=None prints nothing).
    """

    root: Path
    initialized: bool
    baseline: str | None
    evidence_count: int | None
    claim_count: int | None
    last_scan_at: datetime | None
    cost_by_model: dict[str, tuple[int, int, float | None]]
    """Maps model_id → (input_tokens, output_tokens, est_cost_usd). Empty when no receipts."""
    llm_backend: str | None = None
    """Backend from `.efterlev/config.toml` `[llm]` section, e.g.
    "anthropic", "bedrock", "claude_code". None when unread/unconfigured.
    v0.1.150 / #355: surfaced in the banner so users can tell at a glance
    which backend their LLM calls route through."""
    llm_model: str | None = None
    """Configured model id (or None to use per-agent defaults)."""

    @property
    def total_cost_usd(self) -> float | None:
        """Sum of priced models. None when nothing is priced; 0.0 when zero spend."""
        priced = [c for _, _, c in self.cost_by_model.values() if c is not None]
        if not priced and self.cost_by_model:
            return None
        return sum(priced) if priced else 0.0

    @property
    def any_bedrock(self) -> bool:
        return any(is_bedrock_model(m) for m in self.cost_by_model)


def read_snapshot(root: Path) -> WorkspaceSnapshot:
    """Build a snapshot from the workspace at `root`.

    Cheap: opens the SQLite store read-only, reads receipts.log once,
    no LLM calls, no detector runs. Safe to call on every shell action.
    """
    efterlev_dir = root / ".efterlev"
    if not efterlev_dir.is_dir():
        return WorkspaceSnapshot(
            root=root,
            initialized=False,
            baseline=None,
            evidence_count=None,
            claim_count=None,
            last_scan_at=None,
            cost_by_model={},
        )

    baseline = _read_baseline(efterlev_dir / "config.toml")
    llm_backend, llm_model = _read_llm_backend(efterlev_dir / "config.toml")
    evidence_count, claim_count = _read_record_counts(efterlev_dir / "store.db")
    last_scan_at = _read_last_scan_at(efterlev_dir / "store.db")
    cost_by_model = _read_cumulative_cost(efterlev_dir / "receipts.log")

    return WorkspaceSnapshot(
        root=root,
        initialized=True,
        baseline=baseline,
        evidence_count=evidence_count,
        claim_count=claim_count,
        last_scan_at=last_scan_at,
        cost_by_model=cost_by_model,
        llm_backend=llm_backend,
        llm_model=llm_model,
    )


def _read_llm_backend(config_path: Path) -> tuple[str | None, str | None]:
    """Read `[llm].backend` and `[llm].model` from the workspace config.

    Returns (None, None) on parse error or missing keys — banner shows
    "(backend unknown)" rather than crashing. v0.1.150 / #355.
    """
    if not config_path.is_file():
        return (None, None)
    try:
        import tomllib

        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
        llm = data.get("llm")
        if not isinstance(llm, dict):
            return (None, None)
        backend = llm.get("backend")
        model = llm.get("model")
        return (
            backend if isinstance(backend, str) else None,
            model if isinstance(model, str) else None,
        )
    except (OSError, ValueError, tomllib.TOMLDecodeError):
        return (None, None)


def _read_baseline(config_path: Path) -> str | None:
    """Pull the baseline from .efterlev/config.toml without invoking the full loader.

    Tolerant: returns None on any parse error. The shell doesn't want
    to crash because the user's config.toml has a typo — just degrades
    to "baseline unknown" until they fix it.
    """
    if not config_path.is_file():
        return None
    try:
        import tomllib

        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
        baseline = data.get("baseline")
        return baseline if isinstance(baseline, str) else None
    except (OSError, ValueError, tomllib.TOMLDecodeError):
        return None


def _read_record_counts(store_path: Path) -> tuple[int | None, int | None]:
    """Return (evidence_count, claim_count). (None, None) if store is unreadable.

    Uses the `provenance_records` table (per `efterlev/provenance/store.py`).
    """
    if not store_path.is_file():
        return (None, None)
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute("SELECT record_type, COUNT(*) FROM provenance_records GROUP BY record_type")
            counts = dict(cur.fetchall())
            return (counts.get("evidence", 0), counts.get("claim", 0))
        finally:
            conn.close()
    except sqlite3.Error:
        return (None, None)


def _read_last_scan_at(store_path: Path) -> datetime | None:
    """Most recent scan_* primitive timestamp, or None when no scan has run."""
    if not store_path.is_file():
        return None
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT MAX(timestamp) FROM provenance_records WHERE primitive LIKE 'scan_%'"
            )
            (ts_str,) = cur.fetchone()
            if not ts_str:
                return None
            return datetime.fromisoformat(ts_str)
        finally:
            conn.close()
    except (sqlite3.Error, ValueError):
        return None


def _read_cumulative_cost(
    receipts_path: Path,
) -> dict[str, tuple[int, int, float | None]]:
    """Aggregate all receipts.log entries by model, with cost estimates.

    Returns model_id → (input_tokens, output_tokens, estimated_cost_usd or None).
    Empty dict when receipts.log is missing or has no LLM entries.
    """
    if not receipts_path.is_file():
        return {}
    try:
        entries = ReceiptLog(receipts_path).read_all()
    except Exception:
        return {}
    # _aggregate_by_model gates entries past `started_at`; epoch start = all entries.
    by_model_tokens = _aggregate_by_model(entries, datetime.fromtimestamp(0, tz=UTC))
    out: dict[str, tuple[int, int, float | None]] = {}
    for model, (in_tok, out_tok) in by_model_tokens.items():
        cost = estimate_cost_usd(model, in_tok, out_tok)
        out[model] = (in_tok, out_tok, cost)
    return out


@dataclass(frozen=True)
class NextSuggestion:
    """One next-step hint the shell can render. command is the literal user types."""

    command: str
    why: str


def _has_iac_files(root: Path) -> bool:
    """Detect whether `root` contains the kinds of files efterlev scans.

    Looks for `.tf`, `.yaml`/`.yml`, and `.py` (with aws_cdk imports
    inferred by the cdk-py parser). Cheap rglob with early exit.
    Excludes the same dirs `scan_*` excludes (`.venv`, `.git`,
    `__pycache__`, `node_modules`, `cdk.out`, `.efterlev`).
    """
    excluded = {".venv", ".git", "__pycache__", "node_modules", "cdk.out", ".efterlev"}
    for pattern in ("*.tf", "*.yaml", "*.yml", "*.json"):
        for p in root.rglob(pattern):
            if any(part in excluded for part in p.parts):
                continue
            return True
    # `.py` files are common; only count as IaC if they import aws_cdk.
    for p in root.rglob("*.py"):
        if any(part in excluded for part in p.parts):
            continue
        try:
            with p.open(encoding="utf-8", errors="ignore") as f:
                head = f.read(2048)
                if "aws_cdk" in head:
                    return True
        except OSError:
            continue
    return False


def _latest_artifact_mtime(directory: Path, pattern: str) -> float | None:
    """Return the mtime of the most recent file matching `pattern` in
    `directory`, or None if none exist. Used to detect "have I run X?"
    by checking whether X's artifact exists and is newer than upstream
    work.

    The shell pipeline ladder uses this to advance the "Next" hint past
    earlier stages once their artifacts have landed (v0.1.144 / #349).
    """
    if not directory.is_dir():
        return None
    latest_mtime: float | None = None
    for path in directory.glob(pattern):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if latest_mtime is None or mtime > latest_mtime:
            latest_mtime = mtime
    return latest_mtime


def _report_artifacts_present(workspace_root: Path, since_epoch: float) -> bool:
    """Return True when ALL four `/report` outputs exist and are newer
    than `since_epoch`. Mirrors the artifacts the `/report` pipeline
    produces (DocAgent attestation + POA&M markdown + OSCAL POA&M JSON
    + OSCAL Component-Definition JSON).

    v0.1.160 / #365: looks across both the new `efterlev-out/reports/`
    location and the legacy `.efterlev/reports/` location so the shell's
    Next-step ladder works correctly on workspaces that pre-date the
    visible-output split.
    """
    from efterlev.paths import iter_report_dirs

    report_dirs = iter_report_dirs(workspace_root)
    poam_subdirs = [d / "poam" for d in report_dirs]
    oscal_subdirs = [d / "oscal" for d in report_dirs]
    artifact_groups: list[tuple[list[Path], str]] = [
        (report_dirs, "attestation-*.json"),
        (poam_subdirs, "poam-*.md"),
        (oscal_subdirs, "poam-*.json"),
        (oscal_subdirs, "component-definition-*.json"),
    ]
    for directories, pattern in artifact_groups:
        # An artifact group "exists" if ANY of its candidate directories
        # has a match newer than `since_epoch`.
        any_fresh = False
        for d in directories:
            mtime = _latest_artifact_mtime(d, pattern)
            if mtime is not None and mtime >= since_epoch:
                any_fresh = True
                break
        if not any_fresh:
            return False
    return True


def _submission_package_exists(workspace_root: Path, since_epoch: float) -> bool:
    """Return True when a submission package zip exists newer than
    `since_epoch`. v0.1.160 / #365: checks both new and legacy locations.
    """
    from efterlev.paths import iter_submission_dirs

    for d in iter_submission_dirs(workspace_root):
        mtime = _latest_artifact_mtime(d, "*.zip")
        if mtime is not None and mtime >= since_epoch:
            return True
    return False


def suggest_next(snapshot: WorkspaceSnapshot) -> NextSuggestion | None:
    """Pick the most useful next command based on workspace state.

    Returns None when the pipeline is "complete enough" — at that
    point the shell drops the Next line entirely rather than nag.

    The pipeline ladder (v0.1.144 / #349) advances by detecting
    *artifact presence + recency* rather than just inferring from the
    SQLite store. Each downstream stage is gated on its upstream
    artifact existing and being newer than the most recent upstream
    action; this prevents the "you ran /report, now run /report again"
    loop the prior heuristic produced.
    """
    if not snapshot.initialized:
        # Differentiate "wrong directory" from "ready to init."
        if not _has_iac_files(snapshot.root):
            return NextSuggestion(
                command="/cd <repo-root>",
                why=(
                    "no .tf / .yaml / aws_cdk .py files found here. "
                    "Efterlev scans the directory it runs from — cd into your "
                    "repo root first (NOT a subdir)"
                ),
            )
        return NextSuggestion(
            command="/init",
            why="found IaC files here; create a workspace to scan them",
        )
    if snapshot.last_scan_at is None:
        return NextSuggestion(
            command="/scan",
            why="find evidence in your IaC",
        )
    # All-zero workspace (init + scan ran but no detectors fired and no
    # manifests authored). Pipeline complete in the trivial sense.
    if (snapshot.evidence_count or 0) == 0:
        return NextSuggestion(
            command="/scan",
            why=(
                "re-scan; no evidence yet "
                "(consider adding manifests or running a detector-firing fixture)"
            ),
        )
    # Heuristic: if evidence exists but no classification claims, gap hasn't run.
    if (snapshot.claim_count or 0) == 0:
        return NextSuggestion(
            command="/agent gap",
            why="classify evidence against KSIs",
        )

    # Has classifications. Now consult the artifact ladder. v0.1.160 / #365:
    # artifact-presence helpers take workspace_root and walk both the new
    # efterlev-out/ and legacy .efterlev/ locations under the hood.
    scan_epoch = snapshot.last_scan_at.timestamp() if snapshot.last_scan_at else 0.0

    # If the full /report bundle hasn't produced fresh artifacts, run it.
    if not _report_artifacts_present(snapshot.root, scan_epoch):
        return NextSuggestion(
            command="/report",
            why="bundle scan + gap + document + POA&M + OSCAL",
        )

    # /report artifacts exist and are recent. Next milestone is the
    # readiness scorecard so the user knows what's blocking 3PAO submission.
    # Then the submission package zips everything up.
    if not _submission_package_exists(snapshot.root, scan_epoch):
        return NextSuggestion(
            command="/readiness",
            why="see your scorecard and top blockers; then /package for the 3PAO bundle",
        )

    # Submission package is fresh. The user has everything they need;
    # drop the Next line entirely rather than nag.
    return None


def humanize_relative_time(ts: datetime) -> str:
    """Render `ts` as `2m ago`, `5h ago`, `3d ago` for the status line."""
    delta = datetime.now(UTC) - ts.astimezone(UTC)
    secs = int(delta.total_seconds())
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def format_cost_summary(snapshot: WorkspaceSnapshot) -> str | None:
    """Build the Cost line for the snapshot block, or None when no spend.

    Single-model: `$1.23 Opus`
    Multi-model:  `$1.23 Opus · $0.04 Haiku · ($1.27 total)`
    Mixed registered/unregistered: total marked as "(partial)"

    v0.1.151 / #356: when the active backend is `claude_code`
    (subscription), suppress misleading dollar figures. Per-call billing
    is $0 on a Pro/Max subscription; ClaudeCodeClient writes tokens=0 to
    receipts.log so cost rolls up to $0 anyway, but we also want to tell
    the user explicitly that they're on subscription rather than show
    "$0.00 sonnet-4-6" which reads as "this run was free" when the user
    might wonder whether the run happened at all.
    """
    if not snapshot.cost_by_model:
        # No receipts at all. Show subscription marker if configured.
        if snapshot.llm_backend == "claude_code":
            return "subscription (no per-call billing)"
        return None

    # Subscription mode: replace the $ figure with a subscription marker.
    # Historical receipts (from API/Bedrock calls before the user switched)
    # still get shown — those WERE billed — but a `· subscription, new
    # calls bill $0` tag clarifies the going-forward billing.
    is_subscription = snapshot.llm_backend == "claude_code"

    parts = []
    unpriced: list[str] = []
    for model, (_in_tok, _out_tok, cost) in sorted(snapshot.cost_by_model.items()):
        short = _short_model_name(model)
        if cost is None:
            unpriced.append(short)
        else:
            parts.append(f"${cost:.2f} {short}")
    if not parts and unpriced:
        return f"pricing for {', '.join(unpriced)} not registered"
    if len(snapshot.cost_by_model) == 1:
        line = parts[0] if parts else ""
    else:
        total = snapshot.total_cost_usd
        if total is None:
            line = " · ".join(parts) + " · (partial — some models unregistered)"
        elif unpriced:
            line = (
                " · ".join(parts)
                + f" · (~${total:.2f} total, partial; {', '.join(unpriced)} unpriced)"
            )
        else:
            line = " · ".join(parts) + f" · (${total:.2f} total)"
    if snapshot.any_bedrock:
        line += "  (bedrock estimates use Anthropic-API rates)"
    if is_subscription:
        # On subscription, the historical $ figure (if any) reflects calls
        # made on a prior backend; new calls bill $0.
        total = snapshot.total_cost_usd or 0.0
        if total > 0:
            line += "  (subscription active — new calls bill $0)"
        else:
            # All $0 — collapse to subscription-only line.
            line = "subscription (no per-call billing)"
    return line


def format_status_summary(snapshot: WorkspaceSnapshot) -> str:
    """Build the Status line: 'initialized · 23 evidence · 60 claims · last scan 2m ago'."""
    if not snapshot.initialized:
        return "no .efterlev/ directory here"
    parts = ["initialized"]
    if snapshot.evidence_count is not None:
        suffix = "s" if snapshot.evidence_count != 1 else ""
        parts.append(f"{snapshot.evidence_count} evidence record{suffix}")
    if snapshot.claim_count is not None and snapshot.claim_count > 0:
        parts.append(f"{snapshot.claim_count} claim{'s' if snapshot.claim_count != 1 else ''}")
    if snapshot.last_scan_at is not None:
        parts.append(f"last scan {humanize_relative_time(snapshot.last_scan_at)}")
    elif snapshot.initialized and snapshot.evidence_count == 0:
        parts.append("no scan yet")
    return " · ".join(parts)
