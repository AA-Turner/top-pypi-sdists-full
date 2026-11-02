"""Output format generation for audit batch data.

Generates structured Markdown files consumed by the evaluation agent.
Includes category assignment heuristics for review observations.
"""

from __future__ import annotations

import re
from pathlib import Path

from agentic_devtools.cli.audit.models import (
    BatchOutput,
    ClosedPRInfo,
    ReviewObservation,
)

# 13-category taxonomy for review feedback classification
CATEGORIES = (
    "input_validation",
    "error_handling",
    "cross_platform",
    "type_safety",
    "concurrency",
    "documentation",
    "test_reliability",
    "performance",
    "security",
    "naming",
    "api_interface",
    "dependencies",
    "other",
)

# Keyword-to-category mapping for heuristic assignment
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "input_validation": [
        "validation",
        "validate",
        "invalid",
        "bounds",
        "range check",
        "negative",
        "zero",
        "null check",
        "empty",
        "sanitize",
        "constraint",
    ],
    "error_handling": [
        "error",
        "exception",
        "try",
        "catch",
        "raise",
        "handle",
        "failure",
        "fallback",
        "recovery",
        "retry",
        "timeout",
    ],
    "cross_platform": [
        "platform",
        "windows",
        "linux",
        "macos",
        "os-specific",
        "portable",
        "cross-platform",
        "path separator",
    ],
    "type_safety": [
        "type",
        "typing",
        "annotation",
        "cast",
        "isinstance",
        "typevar",
        "generic",
        "union",
        "optional",
        "none check",
    ],
    "concurrency": [
        "concurrent",
        "thread",
        "async",
        "await",
        "lock",
        "race condition",
        "deadlock",
        "mutex",
        "parallel",
        "atomic",
    ],
    "documentation": [
        "docstring",
        "documentation",
        "comment",
        "readme",
        "doc",
        "jsdoc",
        "sphinx",
        "type hint",
        "describe",
    ],
    "test_reliability": [
        "test",
        "flaky",
        "assertion",
        "mock",
        "fixture",
        "coverage",
        "deterministic",
        "reproducible",
        "test isolation",
    ],
    "performance": [
        "performance",
        "slow",
        "optimize",
        "cache",
        "memory",
        "allocation",
        "complexity",
        "o(n",
        "bottleneck",
        "efficient",
    ],
    "security": [
        "security",
        "vulnerability",
        "injection",
        "xss",
        "csrf",
        "auth",
        "credential",
        "secret",
        "encrypt",
        "sanitize input",
    ],
    "naming": [
        "naming",
        "rename",
        "name",
        "variable name",
        "misleading",
        "clarity",
        "descriptive",
        "convention",
    ],
    "api_interface": [
        "api",
        "interface",
        "contract",
        "signature",
        "parameter",
        "return type",
        "breaking change",
        "backward compat",
    ],
    "dependencies": [
        "dependency",
        "package",
        "version",
        "upgrade",
        "deprecated",
        "import",
        "library",
        "third-party",
    ],
}


def assign_category(body: str) -> tuple[str, str]:
    """Assign primary and secondary categories based on comment body text.

    Uses keyword-based heuristic matching. Searches for category keywords
    in the comment body (case-insensitive) and returns the best match.

    Args:
        body: Full review comment body text.

    Returns:
        Tuple of (primary_category, secondary_category). Secondary may be
        empty string if no second category is found.
    """
    if not body:
        return ("other", "")

    body_lower = body.lower()
    scores: dict[str, int] = {}

    for category, keywords in _CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in body_lower)
        if score > 0:
            scores[category] = score

    if not scores:
        return ("other", "")

    sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_categories[0][0]
    secondary = sorted_categories[1][0] if len(sorted_categories) > 1 else ""

    return (primary, secondary)


def write_batch_output(batch_output: BatchOutput, output_dir: str) -> None:
    """Write structured Markdown files for the evaluation agent.

    Generates three files in the output directory:
    - ``batch-summary.md`` — metadata, PR list, statistics
    - ``batch-data.md`` — full structured data for evaluation
    - ``instruction-files.md`` — preloaded instruction file contents

    Args:
        batch_output: Complete batch output data.
        output_dir: Directory to write output files to.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    _write_batch_summary(batch_output, out_path)
    _write_batch_data(batch_output, out_path)
    _write_instruction_files(batch_output, out_path)


def _write_batch_summary(batch_output: BatchOutput, out_path: Path) -> None:
    """Write batch-summary.md with metadata and statistics."""
    total_observations = len(batch_output.observations)
    stale_count = sum(1 for o in batch_output.observations if o.is_stale)
    pr_numbers = [pr.number for pr in batch_output.prs]

    lines = [
        f"# Review Feedback Audit Batch — {len(batch_output.prs)} PRs",
        "",
        f"**Batch ID:** {batch_output.batch_id}",
        f"**PRs audited:** {len(batch_output.prs)}",
        f"**Total observations:** {total_observations}",
        f"**Stale observations:** {stale_count}",
        f"**PR numbers:** {', '.join(f'#{n}' for n in pr_numbers)}",
        "",
        "## PRs Included",
        "",
    ]

    for pr in batch_output.prs:
        merge_status = "merged" if pr.merged else "closed (not merged)"
        lines.append(f"- **#{pr.number}**: {pr.title} ({merge_status})")

    lines.append("")
    lines.append("## Category Distribution")
    lines.append("")

    # Count categories
    category_counts: dict[str, int] = {}
    for obs in batch_output.observations:
        if not obs.is_stale:
            category_counts[obs.primary_category] = category_counts.get(obs.primary_category, 0) + 1

    for cat in CATEGORIES:
        count = category_counts.get(cat, 0)
        if count > 0:
            lines.append(f"- **{cat}**: {count}")

    content = "\n".join(lines) + "\n"
    (out_path / "batch-summary.md").write_text(content, encoding="utf-8")


def _write_batch_data(batch_output: BatchOutput, out_path: Path) -> None:
    """Write batch-data.md with full structured review data."""
    lines = [
        f"# Batch Review Data — {batch_output.batch_id}",
        "",
    ]

    for pr in batch_output.prs:
        merge_status = "merged" if pr.merged else "closed (not merged)"
        lines.extend(
            [
                f"## PR #{pr.number}: {pr.title}",
                "",
                f"- **State:** {merge_status}",
                f"- **Closed at:** {pr.closed_at}",
                f"- **URL:** {pr.url}",
                "",
            ]
        )

        # Group observations by PR
        pr_observations = [o for o in batch_output.observations if _observation_belongs_to_pr(o, pr)]
        if not pr_observations:
            lines.append("*No review observations for this PR.*")
            lines.append("")
            continue

        for i, obs in enumerate(pr_observations, 1):
            stale_marker = " ⚠️ STALE" if obs.is_stale else ""
            body_fence = _choose_fence(obs.body)
            diff_content = obs.diff_hunk if obs.diff_hunk else "*(no diff hunk available)*"
            diff_fence = _choose_fence(diff_content)
            lines.extend(
                [
                    f"### Observation {i} — `{obs.file_path}` L{obs.line or '?'}{stale_marker}",
                    "",
                    f"- **Reviewer:** {obs.reviewer}",
                    f"- **Category:** {obs.primary_category}"
                    + (f" / {obs.secondary_category}" if obs.secondary_category else ""),
                    f"- **Resolved:** {'yes' if obs.resolved else 'no'}",
                    "- **Body:**",
                    f"{body_fence}text",
                    obs.body,
                    body_fence,
                    "",
                ]
            )
            lines.extend(
                [
                    "**Diff hunk:**",
                    f"{diff_fence}diff",
                    diff_content,
                    diff_fence,
                    "",
                ]
            )

        lines.append("---")
        lines.append("")

    content = "\n".join(lines) + "\n"
    (out_path / "batch-data.md").write_text(content, encoding="utf-8")


def _choose_fence(content: str) -> str:
    """Return a code-fence string that does not appear verbatim in *content*.

    Finds the longest consecutive run of backticks in the content and returns
    a string one backtick longer (minimum 3).  This prevents embedded
    triple-backtick fences inside instruction files from terminating the outer
    code block early, which would corrupt the generated Markdown and the
    evaluation agent input.
    """
    max_run = max(
        (len(m.group()) for m in re.finditer(r"`+", content)),
        default=0,
    )
    return "`" * max(3, max_run + 1)


def _write_instruction_files(batch_output: BatchOutput, out_path: Path) -> None:
    """Write instruction-files.md with preloaded instruction content."""
    lines = [
        "# Preloaded Instruction Files",
        "",
        "These are the existing instruction files relevant to the reviewed code.",
        "The evaluation agent may update writable files, create new writable files,",
        "and use read-only migration context files only as reference.",
        "",
    ]

    for ifile in batch_output.instruction_files:
        if ifile.exists:
            status = "exists (update allowed)" if ifile.can_update else "exists (read-only migration context)"
        else:
            status = (
                "does not exist (creation allowed)"
                if ifile.can_update
                else "does not exist (read-only migration context)"
            )
        lines.extend(
            [
                f"## File: `{ifile.path}`",
                "",
                f"**Path:** {ifile.path}",
                f"**Status:** {status}",
                "",
            ]
        )
        if ifile.exists and ifile.content:
            fence = _choose_fence(ifile.content)
            lines.extend(
                [
                    "**Content:**",
                    "",
                    f"{fence}markdown",
                    ifile.content,
                    fence,
                    "",
                ]
            )

    content = "\n".join(lines) + "\n"
    (out_path / "instruction-files.md").write_text(content, encoding="utf-8")


def _observation_belongs_to_pr(obs: ReviewObservation, pr: ClosedPRInfo) -> bool:
    """Check if an observation belongs to a specific PR."""
    return obs.pr_number == pr.number
