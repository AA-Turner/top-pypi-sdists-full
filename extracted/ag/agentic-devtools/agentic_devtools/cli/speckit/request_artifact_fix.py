"""Post the @copilot repair request for an advisory artifact-gate failure.

When the pre-PR artifact gate runs in advisory mode and exhausts its
regeneration budget, the phase still commits its artifacts and opens a draft
pull request.  This module posts the follow-up comment that asks ``@copilot``
to fix the remaining deterministic violations on that branch.

The orchestration lives here — not in the phase-progression workflow YAML — so
that parent-spec resolution and comment construction are unit-testable rather
than only assertable as YAML strings.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

from ..subprocess_utils import run_safe

#: ``parent:`` entry of a ``hierarchy.yml`` file, e.g. ``parent: "#1859"``.
_PARENT_LINE_RE = re.compile(r"^\s*parent:\s*(?P<value>.*?)\s*$")

#: Depth limit used when searching the spec base path for the parent directory,
#: matching the nested spec layout (``specs/<parent>/<child>/<grandchild>``).
_PARENT_SEARCH_MAX_DEPTH = 3

_GATE_SUMMARY = (
    "The gate enforces: only reference repository files that exist (or state "
    "explicitly that you are creating them); every `FR-NNN` cited downstream "
    "must be defined in `spec.md`; every test task must cite an `FR-NNN` or a "
    "`[USn]` label; only advertise artifacts you actually produce; every "
    "generated checklist must contain real checkbox items."
)

_NO_VIOLATION_DETAIL = "(no violation detail captured — see the workflow run logs)"

#: Internal generator sub-steps that run inside pipeline phase 3 (plan and tasks).
#: A failure in either sub-step means downstream artifacts may be stale, so the
#: verify command must be unscoped (covering all phase-3 checks) rather than
#: restricted to the single failing sub-step.
_PHASE3_INTERNAL_STEPS: frozenset[str] = frozenset({"3", "4"})

#: Downstream-artifact regeneration notes keyed by hierarchy level.
#: ``feature`` (default): plan feeds tasks, tasks feeds analysis.
#: ``epic``: plan feeds analysis only (epics skip tasks.md).
#: ``task``: task-level runs produce only tasks.md; no downstream artifacts.
_DOWNSTREAM_REGENERATION_NOTES: dict[str, str | None] = {
    "feature": (
        "If you changed `plan.md`, regenerate all downstream phase-3 artifacts "
        "(`tasks.md`, coverage diagnostics, and `analysis-report.md`) before verifying. "
        "If you changed only `tasks.md`, regenerate coverage diagnostics and `analysis-report.md`."
    ),
    "epic": (
        "If you changed `plan.md`, regenerate the downstream phase-3 artifact (`analysis-report.md`) before verifying."
    ),
    "task": None,  # task-level runs produce only tasks.md; no downstream artifacts exist
}

_SUPPORTED_HIERARCHY_LEVELS: tuple[str, str, str] = ("feature", "epic", "task")


def _parse_parent_number(hierarchy_file: Path) -> str | None:
    """Return the numeric parent issue id declared in *hierarchy_file*.

    Returns ``None`` when the file is unreadable, declares no ``parent:`` entry,
    or the declared value is not numeric once quotes, inline comments and a
    leading ``#`` are stripped.
    """
    try:
        content = hierarchy_file.read_text(encoding="utf-8")
    except OSError:
        return None

    for line in content.splitlines():
        match = _PARENT_LINE_RE.match(line)
        if match is None:
            continue
        value = match.group("value")
        if value.startswith(('"', "'")):
            quote = value[0]
            closing = value.find(quote, 1)
            value = value[1:closing] if closing != -1 else value[1:]
        else:
            value = re.sub(r"\s+#.*$", "", value)
        value = value.strip().lstrip("#").strip()
        return value if value.isdigit() else None
    return None


def _find_parent_dir(spec_base_path: Path, parent_number: str) -> Path | None:
    """Return the spec directory of *parent_number* under *spec_base_path*.

    Matches a directory named exactly ``<parent_number>`` or prefixed with
    ``<parent_number>-``, searching up to :data:`_PARENT_SEARCH_MAX_DEPTH`
    levels.  Returns ``None`` when zero or more than one match is found so
    that an ambiguous resolution never silently validates a task spec against
    an arbitrary parent (consistent with the ``generate-spec-from-issue.sh``
    shell resolver, which treats multiple matches as an error).
    """
    if not spec_base_path.is_dir():
        return None

    matches: list[Path] = []
    for candidate in spec_base_path.rglob("*"):
        if not candidate.is_dir():
            continue
        if len(candidate.relative_to(spec_base_path).parts) > _PARENT_SEARCH_MAX_DEPTH:
            continue
        name = candidate.name
        if name == parent_number or name.startswith(f"{parent_number}-"):
            matches.append(candidate)

    if len(matches) != 1:
        return None
    return matches[0]


def resolve_parent_spec_context(spec_dir: Path, spec_base_path: Path) -> Path | None:
    """Return the parent feature's ``spec.md`` for a task-level spec directory.

    Task-level specs have no local ``spec.md``, so the FR-reference and
    unmapped-test-task checks need the parent specification passed through
    ``--spec-context``.  Returns ``None`` when no parent is declared, the parent
    directory cannot be resolved, or it holds no ``spec.md``.
    """
    hierarchy_file = spec_dir / "hierarchy.yml"
    if not hierarchy_file.is_file():
        return None

    parent_number = _parse_parent_number(hierarchy_file)
    if parent_number is None:
        return None

    parent_dir = _find_parent_dir(spec_base_path, parent_number)
    if parent_dir is None:
        return None

    parent_spec = parent_dir / "spec.md"
    return parent_spec if parent_spec.is_file() else None


def _normalize_phase_scope(phase_number: str, phase_name: str) -> tuple[str, str, str]:
    """Return normalized phase display text and verify-command scope.

    Returns:
        tuple:
            - phase label for prose (``"Phase 3"`` or ``"Phases 3,4"``)
            - phase description for prose (``"(plan)"`` or ``"(plan,tasks)"``)
            - ``agdt-speckit-verify-artifacts`` phase argument (empty string for
              unscoped verification; ``" --phase 3"`` only for pipeline-level phases
              like 1 or 2 that have no downstream dependants within the same pipeline
              phase)

    Internal phase-3 sub-steps (keys ``3`` and ``4`` in
    :data:`verify_artifacts.PHASE_CHECKS`) always produce an **unscoped** verify
    command.  Scoping to a single sub-step would allow the gate to pass while
    downstream artifacts (``tasks.md`` or ``analysis-report.md``) remain stale
    relative to an upstream change.
    """
    phase_numbers = [item.strip() for item in phase_number.split(",") if item.strip()]
    phase_names = [item.strip() for item in phase_name.split(",") if item.strip()]

    if len(phase_numbers) <= 1:
        normalized_number = phase_numbers[0] if phase_numbers else phase_number.strip()
        normalized_name = phase_names[0] if phase_names else phase_name.strip()
        if not normalized_number:
            return ("Phase", f"({normalized_name})" if normalized_name else "", "")
        # Internal phase-3 sub-steps must use an unscoped verify command so that
        # all downstream phase-3 artifacts are validated end-to-end.
        if normalized_number in _PHASE3_INTERNAL_STEPS:
            return (
                f"Phase {normalized_number}",
                f"({normalized_name})" if normalized_name else "",
                "",
            )
        return (
            f"Phase {normalized_number}",
            f"({normalized_name})" if normalized_name else "",
            f" --phase {normalized_number}",
        )

    return (
        f"Phases {','.join(phase_numbers)}",
        f"({','.join(phase_names)})" if phase_names else "",
        "",
    )


def build_repair_comment(
    *,
    spec_dir: str,
    phase_number: str,
    phase_name: str,
    violations: str,
    spec_context: Path | None,
    hierarchy_level: str = "feature",
) -> str:
    """Return the Markdown body of the @copilot repair request.

    The body MUST begin with ``@copilot`` — agent sessions trigger unreliably
    when the mention is not the first token of the comment.

    *hierarchy_level* controls which downstream-artifact regeneration note is
    inserted when a phase-3 internal sub-step fails:

    - ``"feature"`` (default): plan feeds tasks, tasks feeds analysis.
    - ``"epic"``: plan feeds analysis only (epics skip ``tasks.md``).
    - ``"task"``: no downstream note (task-level runs produce only ``tasks.md``
      and skip plan + analysis entirely).
    """
    phase_label, phase_description, verify_phase_arg = _normalize_phase_scope(phase_number, phase_name)
    spec_context_arg = f" --spec-context {spec_context.as_posix()}" if spec_context is not None else ""
    detail = violations.strip() or _NO_VIOLATION_DETAIL
    verify_command = (
        f"agdt-speckit-verify-artifacts --spec-dir {spec_dir} --repo-root .{verify_phase_arg}{spec_context_arg}"
    )
    update_report_command = (
        f"agdt-speckit-verify-artifacts --spec-dir {spec_dir} --repo-root .{verify_phase_arg}{spec_context_arg}"
        f" --json > {spec_dir}/artifact-verification.json"
    )
    phase_descriptor = f" {phase_description}" if phase_description else ""
    # Determine whether downstream-artifact regeneration is required.  This applies
    # whenever a phase-3 internal sub-step is involved: fixing plan.md may invalidate
    # downstream artifacts.  The exact set of downstream artifacts depends on the
    # hierarchy level (feature: tasks + analysis; epic: analysis only; task: none).
    phase_numbers_set = {item.strip() for item in phase_number.split(",") if item.strip()}
    is_phase3_internal = bool(phase_numbers_set & _PHASE3_INTERNAL_STEPS)
    downstream_note: str | None = (
        _DOWNSTREAM_REGENERATION_NOTES.get(hierarchy_level, _DOWNSTREAM_REGENERATION_NOTES["feature"])
        if is_phase3_internal
        else None
    )
    what_to_do: list[str] = [
        f"1. Fix every violation above in `{spec_dir}`. Each one names the exact artifact and defect.",
    ]
    if downstream_note:
        what_to_do.append(f"2. {downstream_note}")
        what_to_do.append(f"3. Verify the gate passes: `{verify_command}`")
        what_to_do.append(f"4. Refresh the committed report: `{update_report_command}`")
        what_to_do.append("5. Push the fix to this branch and mark the PR ready for review.")
    else:
        what_to_do.append(f"2. Verify the gate passes: `{verify_command}`")
        what_to_do.append(f"3. Refresh the committed report: `{update_report_command}`")
        what_to_do.append("4. Push the fix to this branch and mark the PR ready for review.")
    return "\n".join(
        [
            "@copilot - the SpecKit artifact verification gate still reports "
            "violations on this PR. Please fix them on this branch.",
            "",
            f"{phase_label}{phase_descriptor} artifacts were generated and "
            "committed, but the deterministic pre-PR gate could not be satisfied "
            "within its regeneration budget. The PR was opened as a draft so no "
            "generation work is lost.",
            "",
            "### Remaining violations",
            "",
            "~~~text",
            detail,
            "~~~",
            "",
            "### What to do",
            "",
            *what_to_do,
            "",
            _GATE_SUMMARY,
            "",
            "---",
            "",
            "_Posted by the SpecKit artifact verification gate (advisory mode)._",
            "",
        ]
    )


def post_pr_comment(pr_number: str, repo: str, body: str) -> int:
    """Post *body* as a PR comment via ``gh``; return the ``gh`` exit code.

    The body is passed through a temporary file (``--body-file``) so that
    generated Markdown is never interpolated into an argument list.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(body)
        body_file = handle.name
    try:
        completed = run_safe(
            ["gh", "pr", "comment", pr_number, "--repo", repo, "--body-file", body_file],
            text=True,
            shell=False,
        )
        return completed.returncode
    finally:
        Path(body_file).unlink(missing_ok=True)


def request_artifact_fix_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-request-artifact-fix``.

    Exit codes: ``0`` the comment was posted, ``1`` ``gh`` failed.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-request-artifact-fix",
        description=(
            "Ask @copilot to fix the artifact-gate violations that remain on a "
            "draft pull request opened in advisory mode."
        ),
    )
    parser.add_argument("--pr", required=True, help="Pull request number to comment on")
    parser.add_argument("--repo", required=True, help="Target repository as owner/repo")
    parser.add_argument("--spec-dir", required=True, help="Spec directory holding the artifacts")
    parser.add_argument("--phase-number", required=True, help="Pipeline phase number")
    parser.add_argument("--phase-name", required=True, help="Pipeline phase name")
    parser.add_argument("--violations", default="", help="Violation detail rendered by the gate")
    parser.add_argument(
        "--hierarchy-level",
        default="feature",
        choices=_SUPPORTED_HIERARCHY_LEVELS,
        help=(
            "Hierarchy level of the spec (feature, epic, task). "
            "Controls downstream-artifact regeneration note and parent spec.md resolution."
        ),
    )
    parser.add_argument(
        "--spec-base-path",
        default="specs",
        help="Root directory searched for the parent spec directory (default: specs)",
    )

    args = parser.parse_args(argv)

    spec_context: Path | None = None
    if args.hierarchy_level == "task":
        spec_context = resolve_parent_spec_context(Path(args.spec_dir), Path(args.spec_base_path))

    body = build_repair_comment(
        spec_dir=args.spec_dir,
        phase_number=args.phase_number,
        phase_name=args.phase_name,
        violations=args.violations,
        spec_context=spec_context,
        hierarchy_level=args.hierarchy_level,
    )

    returncode = post_pr_comment(args.pr, args.repo, body)
    if returncode != 0:
        print(
            f"Error: failed to post the artifact-gate repair comment (gh exit {returncode}).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"Requested @copilot artifact fix on PR #{args.pr}.")
