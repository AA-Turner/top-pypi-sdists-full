"""One-shot script to tag all agdt.* skill files with platform classification frontmatter.

Reads each .github/agents/agdt.*.agent.md and .github/prompts/agdt.*.prompt.md file,
parses existing YAML frontmatter, inserts the appropriate `agdt` block based on a
hardcoded classification map, and writes back valid YAML.

Usage:
    python scripts/tag_skill_files.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Classification map: skill_name → classification bucket
# ---------------------------------------------------------------------------

# Jira-specific: requires: { issue_adapter: jira }
JIRA_SKILLS: frozenset[str] = frozenset(
    {
        "add-jira-comment",
        "add-users-to-project-role",
        "add-users-to-project-role-batch",
        "break-down-issue-into-subtasks.initiate",
        "check-user-exists",
        "check-users-exist",
        "create-epic",
        "create-issue",
        "create-jira-epic.initiate",
        "create-jira-issue.initiate",
        "create-jira-subtask.initiate",
        "create-subtask",
        "find-role-id-by-name",
        "get-jira-issue",
        "get-project-role-details",
        "list-project-roles",
        "optimize-issue-for-ai-agent.initiate",
        "parse-jira-error-report",
        "update-jira-issue",
        "update-jira-issue.initiate",
        "work-on-jira-issue.checklist-creation",
        "work-on-jira-issue.commit",
        "work-on-jira-issue.completion",
        "work-on-jira-issue.implementation",
        "work-on-jira-issue.implementation-review",
        "work-on-jira-issue.initiate",
        "work-on-jira-issue.planning",
        "work-on-jira-issue.pull-request",
        "work-on-jira-issue.retrieve",
        "work-on-jira-issue.setup",
        "work-on-jira-issue.verification",
    }
)

# Azure DevOps-specific: requires: { code_hosting: azure_devops }
AZURE_DEVOPS_SKILLS: frozenset[str] = frozenset(
    {
        "apply-pr-suggestions.initiate",
        "approve-pull-request",
        "confirm-suggestion-addressed",
        "create-pipeline",
        "create-pull-request",
        "get-pipeline-id",
        "get-pull-request-details",
        "get-pull-request-threads",
        "get-run-details",
        "list-pipelines",
        "mark-pull-request-draft",
        "publish-pull-request",
        "pull-request-review.completion",
        "pull-request-review.decision",
        "pull-request-review.file-reviewer",
        "pull-request-review.initiate",
        "pull-request-review.orchestrator",
        "reject-suggestion-resolution",
        "reply-to-pull-request-thread",
        "run-e2e-tests-fabric",
        "run-e2e-tests-synapse",
        "run-wb-patch",
        "update-pipeline",
        "wait-for-run",
    }
)

# GitHub-specific: requires: { code_hosting: github }
GITHUB_SKILLS: frozenset[str] = frozenset(
    {
        "address-copilot-review",
        "address-copilot-review.ci-repair",
        "address-copilot-review.evaluate-and-respond",
        "pr-merge-execute",
        "pr-merge-manager",
    }
)

# Always-inject: always: true
ALWAYS_SKILLS: frozenset[str] = frozenset(
    {
        "create-agdt-bug-issue",
        "create-agdt-documentation-issue",
        "create-agdt-feature-issue",
        "create-agdt-issue",
        "create-agdt-task-issue",
    }
)


def _build_agdt_block(skill: str) -> dict[str, object] | None:
    """Return the agdt block dict for a skill, or None if universal."""
    if skill in JIRA_SKILLS:
        return {"requires": {"issue_adapter": "jira"}}
    if skill in AZURE_DEVOPS_SKILLS:
        return {"requires": {"code_hosting": "azure_devops"}}
    if skill in GITHUB_SKILLS:
        return {"requires": {"code_hosting": "github"}}
    if skill in ALWAYS_SKILLS:
        return {"always": True}
    return None


def _parse_frontmatter(content: str) -> tuple[dict[str, object] | None, str, str]:
    """Parse YAML frontmatter from markdown content.

    Returns (frontmatter_dict, frontmatter_raw, body).
    If the file does not start with ``---``, returns (None, '', content).
    Raises ``ValueError`` if the file starts with ``---`` but has no closing
    ``---`` delimiter — writing to such a file would corrupt it by producing
    nested frontmatter; ``main()`` catches this and reports the file as an error.

    Uses ``splitlines()`` for defensive closing-delimiter detection (handles
    CRLF checkouts), then falls back to string-slice offsets so that
    ``fm_raw`` and ``body`` preserve the exact bytes from the source file.
    """
    if not content.startswith("---"):
        return None, "", content

    # Defensive detection: splitlines() strips line endings so CRLF and LF
    # lines both compare equal to "---".
    lines = content.splitlines()
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line == "---"),
        None,
    )
    if close_idx is None:
        raise ValueError(
            "File starts with '---' but is missing a closing '---' delimiter; "
            "this is a partially-edited file that would be corrupted by prepending "
            "a new frontmatter block. Fix the file manually before re-running."
        )

    # String-slice the raw content using the same offsets as before, now safe
    # because we know the closing delimiter exists.
    first_newline = content.index("\n")
    end_idx = content.index("\n---", first_newline)
    fm_raw = content[first_newline + 1 : end_idx + 1]
    body = content[end_idx + 4 :]

    fm_dict = yaml.safe_load(fm_raw)
    if fm_dict is None:
        fm_dict = {}
    return fm_dict, fm_raw, body


def tag_file(filepath: Path, skill: str, *, dry_run: bool = False) -> bool:
    """Tag a single file with the appropriate agdt block.

    Returns True if the file was modified (or would be in dry-run).
    """
    agdt_block = _build_agdt_block(skill)
    if agdt_block is None:
        return False

    content = filepath.read_text(encoding="utf-8")
    fm_dict, _, body = _parse_frontmatter(content)

    if fm_dict is None:
        # No frontmatter — create one with just the agdt block
        agdt_yaml = yaml.dump({"agdt": agdt_block}, default_flow_style=False).strip()
        new_content = f"---\n{agdt_yaml}\n---\n{content}"
        # Validate
        parsed = yaml.safe_load(agdt_yaml)
        assert parsed is not None, f"YAML parse failed for {filepath}"
        if dry_run:
            print(f"[DRY RUN] Would add frontmatter to: {filepath}")
            return True
        filepath.write_text(new_content, encoding="utf-8")
        print(f"Added frontmatter: {filepath}")
        return True

    # Check if agdt block already exists and matches
    if "agdt" in fm_dict:
        existing = fm_dict["agdt"]
        if existing == agdt_block:
            return False
        print(
            f"WARNING: Overwriting existing agdt block in {filepath}: {existing} → {agdt_block}",
            file=sys.stderr,
        )

    # Treat frontmatter as a mapping and re-dump the entire block so there is
    # exactly one agdt key (no duplicate keys from naive string insertion) and
    # the output uses consistent YAML style/newlines regardless of the file's
    # original line endings.  agdt is placed after `description` (if present);
    # if the key already exists it stays in its current position; otherwise it
    # falls through to the end.
    updated: dict[str, object] = {}
    agdt_inserted = False
    for k, v in fm_dict.items():
        if k == "agdt":
            # Discard the stale agdt value and write the new classification at
            # this position (preserving key order); `continue` prevents copying v.
            updated["agdt"] = agdt_block
            agdt_inserted = True
            continue
        updated[k] = v
        if k == "description" and not agdt_inserted:
            # Insert agdt immediately after description when no earlier agdt key existed.
            updated["agdt"] = agdt_block
            agdt_inserted = True

    if not agdt_inserted:
        updated["agdt"] = agdt_block

    new_fm_raw = yaml.dump(updated, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{new_fm_raw}---{body}"

    # Validate YAML
    parsed = yaml.safe_load(new_fm_raw)
    assert parsed is not None, f"YAML parse failed for {filepath}"
    assert "agdt" in parsed, f"agdt block missing after injection in {filepath}"

    if dry_run:
        print(f"[DRY RUN] Would modify: {filepath}")
        return True

    filepath.write_text(new_content, encoding="utf-8")
    print(f"Tagged: {filepath}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag agdt skill files with classification frontmatter")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    agents_dir = repo_root / ".github" / "agents"
    prompts_dir = repo_root / ".github" / "prompts"

    modified = 0
    errors = 0

    for directory, prefix, suffix in [
        (agents_dir, "agdt.", ".agent.md"),
        (prompts_dir, "agdt.", ".prompt.md"),
    ]:
        for filepath in sorted(directory.glob(f"{prefix}*{suffix}")):
            skill = filepath.name[len(prefix) : -len(suffix)]
            try:
                if tag_file(filepath, skill, dry_run=args.dry_run):
                    modified += 1
            except Exception as exc:
                print(f"ERROR processing {filepath}: {exc}", file=sys.stderr)
                errors += 1

    print(f"\nSummary: {modified} files {'would be ' if args.dry_run else ''}modified, {errors} errors")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
