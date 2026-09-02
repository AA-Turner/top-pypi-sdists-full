#!/usr/bin/env python3
"""Generate the "AI PR Loop — Epic Progress Report".

Aggregates GitHub issue status across three granularity levels wired together by
GitHub *sub-issues*:

    Epic (discovered via ``Epic`` label)  ->  Feature (depth 1 sub-issue)  ->  Task (depth 2 sub-issue)

Root epics are discovered by querying issues labelled ``Epic``; the Feature and Task
levels are determined by sub-issue traversal depth, not by label filtering.

Status is derived from each issue's state, its ``speckit:*`` labels, and whether the
Copilot agent is assigned. The result is written as a dated Markdown file under the chosen output directory
(default ``.agdt-temp/``).

Requires the GitHub CLI (``gh``) authenticated with ``repo`` scope on the target repo.

Usage:
    python scripts/generate_epic_progress_report.py
    python scripts/generate_epic_progress_report.py --owner swai-factory --repo agentic-devtools
    python scripts/generate_epic_progress_report.py --output-dir .agdt-temp --stdout
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------------------


@dataclass
class Node:
    """A single issue (epic, feature, or task) plus its children."""

    number: int
    title: str
    state: str  # "OPEN" | "CLOSED"
    updated_at: str
    labels: list[str] = field(default_factory=list)
    assignees: list[str] = field(default_factory=list)
    children: list[Node] = field(default_factory=list)
    child_total: int = 0  # totalCount reported by the API (to detect truncation)

    @property
    def is_closed(self) -> bool:
        return self.state == "CLOSED"

    @property
    def has_failed(self) -> bool:
        return "speckit:failed" in self.labels

    @property
    def is_blocked(self) -> bool:
        return "speckit:blocked" in self.labels

    @property
    def has_bot(self) -> bool:
        return any("copilot-swe-agent" in a for a in self.assignees)

    @property
    def closed_children(self) -> int:
        return sum(1 for c in self.children if c.is_closed)


# --------------------------------------------------------------------------------------
# GitHub data retrieval
# --------------------------------------------------------------------------------------

_GRAPHQL_QUERY = """
query($owner:String!, $repo:String!, $number:Int!) {
  repository(owner:$owner, name:$repo) {
    issue(number:$number) {
      number title state updatedAt
      labels(first:20){nodes{name}}
      assignees(first:10){nodes{login}}
      subIssues(first:40){
        totalCount
        nodes {
          number title state updatedAt
          labels(first:20){nodes{name}}
          assignees(first:10){nodes{login}}
          subIssues(first:80){
            totalCount
            nodes {
              number title state updatedAt
              labels(first:20){nodes{name}}
              assignees(first:10){nodes{login}}
            }
          }
        }
      }
    }
  }
}
"""


def _run_gh(args: list[str]) -> str:
    """Run a ``gh`` command and return stdout, raising on failure."""
    try:
        result = subprocess.run(  # noqa: S603 - shell=False, args passed as list (safe even with user-supplied values)
            ["gh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            shell=False,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment guard
        raise RuntimeError("GitHub CLI 'gh' not found on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or f"exit code {exc.returncode}"
        raise RuntimeError(f"gh command failed: {detail}") from exc
    return result.stdout


def _labels_of(raw: dict) -> list[str]:
    return [n["name"] for n in raw.get("labels", {}).get("nodes", [])]


def _assignees_of(raw: dict) -> list[str]:
    return [n["login"] for n in raw.get("assignees", {}).get("nodes", [])]


def _node_from_raw(raw: dict, child_key: str = "subIssues") -> Node:
    sub = raw.get(child_key) or {}
    children = [_node_from_raw(c, child_key=child_key) for c in sub.get("nodes", [])]
    return Node(
        number=raw["number"],
        title=raw["title"],
        state=raw["state"],
        updated_at=raw["updatedAt"],
        labels=_labels_of(raw),
        assignees=_assignees_of(raw),
        children=children,
        child_total=sub.get("totalCount", len(children)),
    )


_EPIC_LIMIT = 200


def list_epics(owner: str, repo: str) -> list[int]:
    out = _run_gh(
        [
            "issue",
            "list",
            "--repo",
            f"{owner}/{repo}",
            "--label",
            "Epic",
            "--state",
            "all",
            "--limit",
            str(_EPIC_LIMIT),
            "--json",
            "number",
        ]
    )
    try:
        items = json.loads(out)
    except json.JSONDecodeError as exc:
        snippet = out[:200].replace("\n", " ")
        raise RuntimeError(f"gh returned non-JSON for {owner}/{repo} epic list (truncated): {snippet!r}") from exc
    numbers = [item["number"] for item in items]
    if len(numbers) >= _EPIC_LIMIT:
        print(
            f"⚠️  Warning: {len(numbers)} epics returned — the {_EPIC_LIMIT}-item limit was hit; "
            "the report may be incomplete.",
            file=sys.stderr,
        )
    return numbers


def fetch_epic_tree(owner: str, repo: str, number: int) -> Node:
    out = _run_gh(
        [
            "api",
            "graphql",
            "-f",
            f"query={_GRAPHQL_QUERY}",
            "-F",
            f"owner={owner}",
            "-F",
            f"repo={repo}",
            "-F",
            f"number={number}",
        ]
    )
    try:
        issue_raw = json.loads(out)
    except json.JSONDecodeError as exc:
        snippet = out[:200].replace("\n", " ")
        raise RuntimeError(f"gh returned non-JSON for {owner}/{repo}#{number} (truncated): {snippet!r}") from exc
    errors = issue_raw.get("errors")
    if errors:
        msgs = "; ".join(e.get("message", str(e)) for e in errors)
        raise RuntimeError(f"GraphQL errors for {owner}/{repo}#{number}: {msgs}")
    repo_data = (issue_raw.get("data") or {}).get("repository") or {}
    issue = repo_data.get("issue")
    if issue is None:
        raise RuntimeError(f"GraphQL response missing issue for {owner}/{repo}#{number}; response: {issue_raw!r}")
    return _node_from_raw(issue)


# --------------------------------------------------------------------------------------
# Status derivation & metrics
# --------------------------------------------------------------------------------------

_WIP_LABELS = ("speckit:processing", "speckit:implementing")


def _recently_active(node: Node, now: _dt.datetime, hours: int = 48) -> bool:
    try:
        updated = _dt.datetime.fromisoformat(node.updated_at.replace("Z", "+00:00"))
    except ValueError:  # pragma: no cover - defensive
        return False
    return (now - updated).total_seconds() < hours * 3600


def base_glyph(node: Node, now: _dt.datetime) -> str:
    """Return the base status emoji for a node (before modifiers)."""
    if node.is_closed:
        return "✅"
    if node.is_blocked:
        return "🚧"
    has_phase = any(lbl.startswith("speckit:phase-") for lbl in node.labels)
    active = (
        node.closed_children > 0
        or any(lbl in node.labels for lbl in _WIP_LABELS)
        or has_phase
        or _recently_active(node, now)
    )
    return "🟡" if active else "⚪"


def glyph_with_mods(node: Node, now: _dt.datetime) -> str:
    """Base glyph with 🔴 (failed) prefix and/or 🤖 (bot) suffix modifiers.

    A node that is both failed and blocked renders as 🔴🚧 so neither signal
    is hidden.
    """
    prefix = "🔴" if node.has_failed else ""
    suffix = "🤖" if node.has_bot else ""
    return f"{prefix}{base_glyph(node, now)}{suffix}"


@dataclass
class EpicMetrics:
    node: Node
    features_done: int
    features_total: int
    tasks_closed: int
    tasks_total: int

    @property
    def pct(self) -> int:
        total = self.tasks_total + self.features_total
        if total == 0:
            return 0
        return round((self.tasks_closed + self.features_done) / total * 100)

    @property
    def bar(self) -> str:
        fill = min(round(self.pct / 10), 10)
        return "▓" * fill + "░" * (10 - fill)


def compute_metrics(epic: Node) -> EpicMetrics:
    features = epic.children
    tasks_closed = sum(f.closed_children for f in features)
    tasks_total = sum(f.child_total for f in features)
    return EpicMetrics(
        node=epic,
        features_done=sum(1 for f in features if f.is_closed),
        features_total=epic.child_total,
        tasks_closed=tasks_closed,
        tasks_total=tasks_total,
    )


# --------------------------------------------------------------------------------------
# Movement / stall detection (compare against the previous run)
# --------------------------------------------------------------------------------------

STATE_FILENAME = ".epic-report-state.json"


def _iter_subtree(epic: Node):
    yield epic
    for feature in epic.children:
        yield feature
        yield from feature.children


def subtree_max_updated(epic: Node) -> _dt.datetime | None:
    """Most recent ``updatedAt`` anywhere in the epic's subtree."""
    times: list[_dt.datetime] = []
    for node in _iter_subtree(epic):
        try:
            times.append(_dt.datetime.fromisoformat(node.updated_at.replace("Z", "+00:00")))
        except ValueError:  # pragma: no cover - defensive
            continue
    return max(times) if times else None


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):  # pragma: no cover - defensive
        return {}


@dataclass
class EpicRow:
    metrics: EpicMetrics
    max_updated: _dt.datetime | None
    prev: dict | None
    prev_run_at: _dt.datetime | None
    open_failed: list[Node]
    blocked: list[Node]
    anomalies: list[Node]

    @property
    def epic(self) -> Node:
        return self.metrics.node

    @property
    def delta_tasks(self) -> int | None:
        if not self.prev:
            return None
        return self.metrics.tasks_closed - int(self.prev.get("closed_tasks", 0))

    @property
    def active_since_prev(self) -> bool:
        if not self.max_updated or not self.prev_run_at:
            return False
        return self.max_updated > self.prev_run_at

    @property
    def truncated(self) -> bool:
        """True when the epic or any feature has a truncated child list (API page limit).

        When truncated, delta counts and activity timestamps are derived from
        incomplete data, making stall detection unreliable.
        """
        epic = self.metrics.node
        if epic.child_total > len(epic.children):
            return True
        return any(f.child_total > len(f.children) for f in epic.children)

    @property
    def stalled(self) -> bool:
        # Only meaningful once we have a baseline, the epic isn't finished, and
        # none of the child lists are truncated (truncated data makes delta/activity
        # unreliable, so we skip stall detection to avoid false positives).
        if self.prev is None or self.metrics.pct >= 100 or self.truncated:
            return False
        return (self.delta_tasks == 0) and not self.active_since_prev


def build_rows(epics: list[Node], now: _dt.datetime, prev_state: dict) -> list[EpicRow]:
    prev_epics = prev_state.get("epics", {})
    prev_run_at: _dt.datetime | None = None
    if prev_state.get("generated_at"):
        try:
            prev_run_at = _dt.datetime.fromisoformat(prev_state["generated_at"])
        except ValueError:  # pragma: no cover - defensive
            prev_run_at = None

    rows: list[EpicRow] = []
    for epic in epics:
        open_failed: list[Node] = []
        blocked: list[Node] = []
        anomalies: list[Node] = []
        if epic.has_failed and not epic.is_closed:
            open_failed.append(epic)
        if epic.is_blocked and not epic.is_closed:
            blocked.append(epic)
        for feature in epic.children:
            if feature.is_blocked and not feature.is_closed:
                blocked.append(feature)
            if feature.has_failed and not feature.is_closed:
                open_failed.append(feature)
            has_full_child_set = feature.child_total == len(feature.children)
            if (
                feature.is_closed
                and feature.child_total > 0
                and has_full_child_set
                and feature.closed_children < feature.child_total
            ):
                anomalies.append(feature)
            for task in feature.children:
                if task.has_failed and not task.is_closed:
                    open_failed.append(task)
                if task.is_blocked and not task.is_closed:
                    blocked.append(task)
        rows.append(
            EpicRow(
                metrics=compute_metrics(epic),
                max_updated=subtree_max_updated(epic),
                prev=prev_epics.get(str(epic.number)),
                prev_run_at=prev_run_at,
                open_failed=open_failed,
                blocked=blocked,
                anomalies=anomalies,
            )
        )
    return sorted(rows, key=lambda r: r.metrics.pct, reverse=True)


def state_from_rows(now: _dt.datetime, rows: list[EpicRow]) -> dict:
    return {
        "generated_at": now.isoformat(),
        "epics": {
            str(r.epic.number): {
                "closed_tasks": r.metrics.tasks_closed,
                "total_tasks": r.metrics.tasks_total,
                "closed_features": r.metrics.features_done,
                "max_updated": r.max_updated.isoformat() if r.max_updated else None,
            }
            for r in rows
        },
    }


# --------------------------------------------------------------------------------------
# Rendering (concise overview)
# --------------------------------------------------------------------------------------


def _short(title: str, length: int = 48) -> str:
    title = title.removeprefix("[EPIC] ").removeprefix("[Epic] ")
    return title if len(title) <= length else title[: length - 1] + "…"


def _bar(pct: int) -> str:
    fill = min(round(pct / 10), 10)
    return "▓" * fill + "░" * (10 - fill)


def _clean_feature_name(title: str) -> str:
    for prefix in ("Feature: ", "Feature "):
        if title.startswith(prefix):
            return title[len(prefix) :]
    return title


def _fmt(nodes: list[Node], limit: int = 10) -> str:
    shown = nodes[:limit]
    rest = len(nodes) - len(shown)
    body = ", ".join(f"#{n.number}" for n in shown)
    return body + (f" (+{rest} more)" if rest > 0 else "")


def render_report(
    owner: str,
    repo: str,
    rows: list[EpicRow],
    now: _dt.datetime,
    prev_state: dict,
    show_details: bool,
) -> str:
    lines: list[str] = []
    add = lines.append

    prev_date = "none (baseline)"
    if prev_state.get("generated_at"):
        try:
            prev_date = _dt.datetime.fromisoformat(prev_state["generated_at"]).date().isoformat()
        except ValueError:  # pragma: no cover - defensive
            prev_date = "unknown"

    add("# 📊 AI PR Loop — Epic Progress Report")
    add(f"**Repo:** {owner}/{repo} · **Snapshot:** {now.date().isoformat()} · **Compared to:** {prev_date}")
    add("")

    has_baseline = bool(prev_state.get("generated_at"))

    # --- Completed stats ---------------------------------------------------------
    tasks_closed = sum(r.metrics.tasks_closed for r in rows)
    tasks_total = sum(r.metrics.tasks_total for r in rows)
    feat_done = sum(r.metrics.features_done for r in rows)
    feat_total = sum(r.metrics.features_total for r in rows)
    overall_total = tasks_total + feat_total
    overall_pct = round((tasks_closed + feat_done) / overall_total * 100) if overall_total else 0

    prev_tasks_closed = sum(int(r.prev.get("closed_tasks", 0)) for r in rows if r.prev)
    prev_feat_done = sum(int(r.prev.get("closed_features", 0)) for r in rows if r.prev)
    delta_tasks_total = tasks_closed - prev_tasks_closed if has_baseline else None
    delta_feat_total = feat_done - prev_feat_done if has_baseline else None

    add("## ✅ Completed")
    add(
        f"- **Overall:** {_bar(overall_pct)} {overall_pct}% "
        f"— {tasks_closed}/{tasks_total} subtasks · {feat_done}/{feat_total} features"
    )
    if has_baseline:
        add(f"- **Since {prev_date}:** {delta_tasks_total:+d} subtasks, {delta_feat_total:+d} features")
    else:
        add("- **Since last run:** — (baseline; deltas start next run)")
    for r in rows:
        m = r.metrics
        if r.delta_tasks is None:
            d = ""
        else:
            d = f"  ({r.delta_tasks:+d})"
        stall = " 🛑" if r.stalled else ""
        add(
            f"  - {m.bar} {m.pct}% #{m.node.number} {_short(m.node.title, 38)} "
            f"— {m.tasks_closed}/{m.tasks_total} subtasks · {m.features_done}/{m.features_total} features{d}{stall}"
        )
    add("")

    # --- Errors / attention ------------------------------------------------------
    all_open_failed = [n for r in rows for n in r.open_failed]
    all_blocked = [n for r in rows for n in r.blocked]
    all_anomalies = [n for r in rows for n in r.anomalies]
    stalled_rows = [r for r in rows if r.stalled]

    # Deduplicate across categories: an issue may carry both speckit:failed and
    # speckit:blocked labels, so count unique issue numbers to avoid inflating the total.
    attention_numbers: set[int] = {n.number for n in all_open_failed}
    attention_numbers.update(n.number for n in all_blocked)
    attention_numbers.update(n.number for n in all_anomalies)
    stalled_epic_numbers: set[int] = {r.epic.number for r in stalled_rows}
    total_errors = len(attention_numbers | stalled_epic_numbers)

    add(f"## ⚠️ Errors & attention ({total_errors})")
    if total_errors == 0:
        add("✅ None — no failures, nothing blocked." + ("" if has_baseline else " (stall detection starts next run)"))
    else:
        if all_open_failed:
            add(f"- 🔴 **Open failures** (`speckit:failed`) — {len(all_open_failed)}: {_fmt(all_open_failed)}")
        if all_blocked:
            add(f"- 🚧 **Blocked** (`speckit:blocked`) — {len(all_blocked)}: {_fmt(all_blocked)}")
        if stalled_rows:
            stalled_desc = ", ".join(f"#{r.epic.number}" for r in stalled_rows[:10])
            rest = len(stalled_rows) - min(len(stalled_rows), 10)
            stalled_desc += f" (+{rest} more)" if rest > 0 else ""
            add(f"- 🛑 **No progress since {prev_date}** — {len(stalled_rows)}: {stalled_desc}")
        if all_anomalies:
            add(f"- ❓ **Closed but subtasks still open** — {len(all_anomalies)}: {_fmt(all_anomalies)}")
    add("")

    # --- Optional feature-level breakdown (--details) ---------------------------
    if show_details:
        add("## Feature breakdown")
        for r in rows:
            epic = r.epic
            add(f"\n**#{epic.number} {_short(epic.title, 60)}**")
            for feature in epic.children:
                fg = glyph_with_mods(feature, now)
                fname = _clean_feature_name(_short(feature.title, 52))
                add(f"- {fg} #{feature.number} {fname} — {feature.closed_children}/{feature.child_total}")
        add("")

    # --- Truncation warnings -----------------------------------------------------
    truncated = [n for r in rows for n in (r.epic, *r.epic.children) if n.child_total > len(n.children)]
    if truncated:
        add(
            "> ⚠️ Some issues have more children than were fetched (API page limit), "
            f"so counts may be underreported and percentages/deltas may be inaccurate for: {_fmt(truncated)}."
        )
        add("")

    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="swai-factory")
    parser.add_argument("--repo", default="agentic-devtools")
    parser.add_argument(
        "--output-dir",
        default=".agdt-temp",
        help="Directory for the generated report (default: .agdt-temp, which is gitignored).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Also print the report to stdout.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Include a compact feature-level breakdown under each epic.",
    )
    parser.add_argument(
        "--no-save-state",
        action="store_true",
        help="Do not update the stall-detection state file for this run.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    now = _dt.datetime.now(_dt.timezone.utc)

    print(f"Discovering epics in {args.owner}/{args.repo} …", file=sys.stderr)
    epic_numbers = list_epics(args.owner, args.repo)
    print(f"Found {len(epic_numbers)} epics; fetching trees …", file=sys.stderr)

    epics = [fetch_epic_tree(args.owner, args.repo, n) for n in epic_numbers]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    state_path = out_dir / STATE_FILENAME

    prev_state = load_state(state_path)
    rows = build_rows(epics, now, prev_state)
    report = render_report(args.owner, args.repo, rows, now, prev_state, args.details)

    out_path = out_dir / f"status-ai-pr-loop-{now.date().isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Report written to: {out_path}", file=sys.stderr)

    if not args.no_save_state:
        state_path.write_text(json.dumps(state_from_rows(now, rows), indent=2), encoding="utf-8")
        print(f"Stall-detection state updated: {state_path}", file=sys.stderr)

    if args.stdout:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
