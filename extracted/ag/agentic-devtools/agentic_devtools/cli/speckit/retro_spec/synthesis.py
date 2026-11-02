"""LLM-based spec synthesis and file writing for the retro-spec command.

Assembles structured context from collected artifacts, invokes the LLM
for spec generation, and writes the output with retroactive metadata markers.
"""

from __future__ import annotations

import re as _re
import subprocess
from datetime import date
from pathlib import Path

from .artifact_collector import IssueArtifact, PRArtifact

_MAX_CONTEXT_CHARS = 100_000  # Context window budget for artifacts
_MAX_OUTPUT_CHARS = 10_000  # Maximum total spec size (header + body)
_MIN_BODY_CHARS = 2_000  # Minimum body reservation so metadata cannot consume the entire budget

_RETROACTIVE_HEADER = """\
# Feature Specification: Retroactive Implementation

**Feature Branch**: `unavailable`
**Created**: {created}
**Status**: Implemented
**Generated**: retroactive
{source_issue}{labels}{milestone}

> ⚠️ **Retroactive Spec**: This specification was generated from available
> delivery evidence (issue history, PR metadata, and implementation artifacts
> when available) rather than written as a forward-looking design document. It
> documents what was actually built.

"""

# Body-only budget: the header is prepended unconditionally, so reserve its length.
_MAX_BODY_CHARS = _MAX_OUTPUT_CHARS - len(
    _RETROACTIVE_HEADER.format(created="0000-00-00", source_issue="", labels="", milestone="")
)
_REQUIRED_SYNTHESIS_MARKERS = (
    "## User Scenarios & Testing",
    "### User Story ",
    "**Why this priority**",
    "**Independent Test**",
    "**Acceptance Scenarios**",
    "### Edge Cases",
    "## Requirements",
    "### Functional Requirements",
    "### Non-Functional Requirements",
    "## Success Criteria",
    "**Summary**",
    "**PR References**",
    "**Key Changes**",
)

# Markers that are prepended by the tool layer (not by the LLM) but must also
# be preserved when the combined body is capped during format_retroactive_spec.
_TOOL_INJECTED_REQUIRED_MARKERS = ("## Artifact Availability",)


def assemble_context(
    issue: IssueArtifact,
    prs: list[PRArtifact],
    diffs: list[str],
    commits: list[str],
) -> str:
    """Assemble structured context from collected artifacts.

    Combines issue body, comments, PR bodies, diffs, and commit messages
    into a single structured context string for LLM synthesis.
    Manages size by truncating large diffs to fit the context window.

    Args:
        issue: The collected issue artifact.
        prs: List of related PR artifacts.
        diffs: List of PR diff strings.
        commits: List of commit message strings.

    Returns:
        Structured context string.
    """
    sections: list[str] = []

    # Issue section
    sections.append(f"## Issue #{issue.number}: {issue.title}")
    sections.append(f"State: {issue.state}")
    if issue.labels:
        sections.append(f"Labels: {', '.join(issue.labels)}")
    if issue.milestone:
        sections.append(f"Milestone: {issue.milestone}")
    sections.append("")
    sections.append("### Issue Body")
    sections.append(issue.body or "(empty)")
    sections.append("")

    if issue.comments:
        sections.append("### Issue Comments")
        for i, comment in enumerate(issue.comments[:10], 1):  # Max 10 comments
            sections.append(f"**Comment {i}:**")
            sections.append(comment[:2000])  # Truncate long comments
            sections.append("")

    # PRs section
    if prs:
        sections.append("## Related Pull Requests")
        for pr in prs:
            sections.append(f"### PR #{pr.number}: {pr.title}")
            if pr.body:
                sections.append(pr.body[:3000])  # Truncate long PR bodies
            sections.append("")

    # Commit messages
    if commits:
        sections.append("## Commit Messages")
        for msg in commits[:50]:  # Max 50 commits
            sections.append(f"- {msg}")
        sections.append("")

    # Diffs section (size-managed)
    if diffs:
        sections.append("## Code Changes (Diffs)")
        remaining_budget = _MAX_CONTEXT_CHARS - len("\n".join(sections))
        for diff in diffs:
            if remaining_budget <= 0:
                sections.append("[Remaining diffs truncated due to size limits]")
                break
            truncated = diff[:remaining_budget]
            sections.append(truncated)
            sections.append("")
            remaining_budget -= len(truncated)

    context = "\n".join(sections)
    # Final truncation safety
    if len(context) > _MAX_CONTEXT_CHARS:
        context = context[:_MAX_CONTEXT_CHARS] + "\n[TRUNCATED]"

    return context


def synthesize_spec(
    context: str,
    system_prompt: str,
    *,
    has_implementation_artifacts: bool = True,
    pr_artifacts: list[PRArtifact] | None = None,
    diff_entries: list[str] | None = None,
    commit_messages: list[str] | None = None,
) -> str:
    """Synthesize a spec document via LLM.

    Calls the LLM with the structured context and system prompt.
    Falls back to a template-based approach if LLM is unavailable.
    Enforces a 10,000 character output cap.

    Args:
        context: Structured context string from assemble_context().
        system_prompt: System prompt enforcing tone and structure.
        has_implementation_artifacts: Passed through to the fallback generator
            to control whether SC-001 claims merged artifacts exist.
        pr_artifacts: Structured related-PR metadata used by fallback synthesis.
        diff_entries: Structured per-file diff entries used by fallback synthesis.
        commit_messages: Structured commit messages used by fallback synthesis.

    Returns:
        Generated spec content string (capped at 10,000 chars).
    """
    user_prompt = (
        "Based on the following implementation artifacts, generate a retroactive "
        "specification document following the output structure defined in your instructions.\n\n" + context
    )

    def _fallback_content() -> str:
        return _generate_fallback_spec(
            context,
            has_implementation_artifacts=has_implementation_artifacts,
            pr_artifacts=pr_artifacts,
            diff_entries=diff_entries,
            commit_messages=commit_messages,
        )

    try:
        result = subprocess.run(
            [
                "gh",
                "api",
                "/copilot/chat/completions",
                "-X",
                "POST",
                "--input",
                "-",
            ],
            input=f'{{"messages":[{{"role":"system","content":{_json_escape(system_prompt)}}},{{"role":"user","content":{_json_escape(user_prompt)}}}],"model":"gpt-4o"}}',
            capture_output=True,
            text=True,
            shell=False,
        )
    except OSError:
        return _apply_output_cap(_fallback_content())

    if result.returncode == 0 and result.stdout.strip():
        try:
            import json

            response = json.loads(result.stdout)
            choices = response.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if content.strip() and _has_required_synthesis_structure(content):
                    capped = _apply_output_cap(content)
                    if _has_required_synthesis_structure(capped):
                        return capped
        except Exception:
            pass

    return _apply_output_cap(_fallback_content())


def _apply_output_cap(content: str) -> str:
    """Enforce output body cap so that header + body stays within 10,000 characters.

    The cap is applied to the *body* content only; ``format_retroactive_spec``
    prepends ``_RETROACTIVE_HEADER`` afterwards, so the effective body budget is
    ``_MAX_OUTPUT_CHARS - len(_RETROACTIVE_HEADER)`` rather than the full 10k.
    """
    capped = _cap_content(content, _MAX_BODY_CHARS)
    if _required_sections_intact(content, capped):
        return capped
    return _cap_with_required_sections(content, _MAX_BODY_CHARS)


def _has_required_synthesis_structure(content: str) -> bool:
    """Return True when generated content contains required template markers."""
    return all(marker in content for marker in _REQUIRED_SYNTHESIS_MARKERS)


def _cap_content(content: str, limit: int) -> str:
    """Cap *content* to *limit* chars with a best-effort line-boundary truncation note."""
    if len(content) <= limit:
        return content

    note = "\n\n> **Note**: This spec was summarized due to extensive artifacts.\n"
    if limit <= len(note):
        return content[:limit]

    truncated = content[: limit - len(note)]
    # Try to end at a line boundary
    last_newline = truncated.rfind("\n")
    if last_newline > len(truncated) - 400:
        truncated = truncated[:last_newline]
    return truncated + note


def _required_sections_intact(original: str, candidate: str) -> bool:
    """Return True when every required section in *original* still exists in *candidate*."""
    required_headings = ("## User Scenarios & Testing", "## Requirements", "## Success Criteria")
    for heading in required_headings:
        if heading in original and heading not in candidate:
            return False
    return True


def _marker_excerpt_within_limit(body: str, markers: list[str], limit: int) -> str:
    """Return a compact marker-bearing excerpt that stays within ``limit`` chars."""
    if limit <= 0:
        return ""

    lines = body.splitlines(keepends=True)
    marker_indices: list[int] = []
    for marker in markers:
        for idx, line in enumerate(lines):
            if line.startswith(marker) and idx not in marker_indices:
                marker_indices.append(idx)
                break

    if not marker_indices:
        return _cap_content(body, limit)

    marker_indices.sort()
    excerpt = ""
    for idx in marker_indices:
        line = lines[idx]
        if not line.endswith("\n"):
            line += "\n"
        if len(excerpt) + len(line) <= limit:
            excerpt += line
        elif not excerpt:
            return line[:limit]
        else:
            break
    return excerpt


def _cap_with_required_sections(content: str, limit: int) -> str:
    """Cap content while preserving required terminal sections when possible.

    When a section body contains required sub-markers (e.g. ``### Functional
    Requirements``), the body is never truncated before those markers.  The
    minimum body prefix that still includes all required sub-markers in the
    original body is used as a floor for truncation, even when that floor
    slightly exceeds the ideal per-section budget.
    """
    sections = _extract_required_sections(content)
    if not sections:
        return _cap_content(content, limit)

    note = "\n\n> **Note**: This spec was summarized due to extensive artifacts.\n"
    preface = (
        "> **Note**: Earlier sections were condensed to preserve the required "
        "User Scenarios, Requirements, and Success Criteria sections.\n"
    )
    base = f"{preface}{note}"
    if len(base) >= limit:
        return _cap_content(content, limit)

    remaining = limit - len(base) - 1  # reserve 1 for the trailing '\n'
    rendered: list[str] = []
    for idx, section in enumerate(sections):
        heading, _, body = section.partition("\n")
        trailing_headings = [next_section.partition("\n")[0] for next_section in sections[idx + 1 :]]
        min_for_future = sum(len(h) + 2 for h in trailing_headings)
        sep_before = 2 if rendered else 0
        section_budget = max(0, remaining - sep_before - min_for_future)
        if section_budget < len(heading):
            break

        if section_budget <= len(heading) + 1:
            chunk = heading
        else:
            body_budget = section_budget - len(heading) - 1
            capped_body = _cap_content(body, body_budget)
            # If the body cap dropped required sub-markers, switch to a compact
            # marker-bearing excerpt that stays inside the same body budget.
            markers_in_body = [m for m in _REQUIRED_SYNTHESIS_MARKERS if m in body]
            if markers_in_body and not all(m in capped_body for m in markers_in_body):
                capped_body = _marker_excerpt_within_limit(body, markers_in_body, body_budget)
            chunk = heading + "\n" + capped_body
        normalized_chunk = chunk.rstrip()
        rendered.append(normalized_chunk)
        remaining -= len(normalized_chunk) + sep_before
        if remaining <= 0:
            break

    if not rendered:
        return _cap_content(content, limit)
    return base + "\n\n".join(rendered).rstrip() + "\n"


def _extract_required_sections(content: str) -> list[str]:
    """Extract required top-level sections from content in source order."""
    lines = content.splitlines()
    heading_indices: list[int] = []
    for index, line in enumerate(lines):
        if (
            line.startswith("## Artifact Availability")
            or line.startswith("## User Scenarios & Testing")
            or line.startswith("## Requirements")
            or line.startswith("## Success Criteria")
        ):
            heading_indices.append(index)
    if not heading_indices:
        return []

    sections: list[str] = []
    for start in heading_indices:
        end = len(lines)
        for next_line in range(start + 1, len(lines)):
            if lines[next_line].startswith("## "):
                end = next_line
                break
        body_lines = lines[start + 1 : end]
        if not body_lines or not any(line.strip() for line in body_lines):
            continue
        section_text = "\n".join(lines[start:end]).strip()
        sections.append(section_text)
    return sections


def _json_escape(text: str) -> str:
    """Escape text for JSON string embedding."""
    import json

    return json.dumps(text)


def _generate_fallback_spec(
    context: str,
    *,
    has_implementation_artifacts: bool = True,
    pr_artifacts: list[PRArtifact] | None = None,
    diff_entries: list[str] | None = None,
    commit_messages: list[str] | None = None,
) -> str:
    """Generate a basic spec when LLM synthesis is unavailable.

    Derives key information from structured artifacts when available, falling
    back to bounded context parsing when those structured inputs are absent.

    Args:
        context: The assembled artifact context string.
        has_implementation_artifacts: True when at least one related PR was found
            and diffs or commits are available.  When False, success criteria that
            claim merged artifacts exist are replaced with artifact-neutral wording.
        pr_artifacts: Optional structured PR artifacts. When provided, PR references
            are derived from these artifacts instead of context parsing.
        diff_entries: Optional structured diff entries. When provided, key-change
            paths are derived from these entries instead of context parsing.
        commit_messages: Optional structured commit messages. When provided, commit
            summaries are derived from these messages instead of context parsing.
    """
    context_lines = context.splitlines()
    _pr_cap = 5
    all_pr_refs: list[str] = (
        [_format_pr_reference(pr.number, pr.title) for pr in pr_artifacts] if pr_artifacts is not None else []
    )
    pr_references: list[str] = all_pr_refs[:_pr_cap]
    if len(all_pr_refs) > _pr_cap:
        pr_references.append(f"_({len(all_pr_refs) - _pr_cap} additional related PRs omitted)_")
    key_change_paths: list[str] = []
    commit_summaries: list[str] = (
        [message.strip() for message in commit_messages if message.strip()][:5] if commit_messages is not None else []
    )

    if diff_entries is not None:
        for entry in diff_entries:
            header = entry.splitlines()[0] if entry else ""
            if not (header.startswith("--- ") and header.endswith(" ---")):
                continue
            path = header.removeprefix("--- ").removesuffix(" ---").strip()
            if path and path not in key_change_paths:
                key_change_paths.append(path)
                if len(key_change_paths) >= 5:
                    break

    # Parse PR references only within the bounded "## Related Pull Requests"
    # section to prevent issue bodies or PR descriptions from impersonating
    # the structural markers used by assemble_context.
    in_pr_section = False
    in_diff_section = False
    in_commit_section = False

    for line in context_lines:
        # Track which top-level section we are in.
        if line.startswith("## "):
            in_pr_section = line == "## Related Pull Requests"
            in_diff_section = line == "## Code Changes (Diffs)"
            in_commit_section = line == "## Commit Messages"
            continue

        if pr_artifacts is None and in_pr_section and line.startswith("### PR #"):
            pr_references.append(line.removeprefix("### ").strip())

        if diff_entries is None and in_diff_section and line.startswith("--- ") and line.endswith(" ---"):
            path = line.removeprefix("--- ").removesuffix(" ---").strip()
            if path and path not in key_change_paths:
                key_change_paths.append(path)
                if len(key_change_paths) >= 5:
                    in_diff_section = False  # collected enough; stop scanning
            continue

        if commit_messages is None and in_commit_section and line.startswith("- "):
            commit_summaries.append(line[2:].strip())
            if len(commit_summaries) >= 5:
                in_commit_section = False  # collected enough; stop scanning

    issue_title = _extract_issue_title(context_lines)
    user_stories = _derive_user_stories(
        issue_title=issue_title,
        pr_references=pr_references,
        key_change_paths=key_change_paths,
        commit_summaries=commit_summaries,
    )
    acceptance_scenarios = _derive_acceptance_scenarios(
        issue_title=issue_title,
        pr_references=pr_references,
        key_change_paths=key_change_paths,
        commit_summaries=commit_summaries,
    )

    lines: list[str] = []
    lines.append("## Summary")
    lines.append("")
    has_related_pr_metadata = bool(pr_references)

    if has_implementation_artifacts:
        lines.append("The implementation artifacts below record the delivered behavior.")
    elif has_related_pr_metadata:
        lines.append(
            "The issue evidence and related pull-request metadata below record the available context; "
            "diff and commit artifacts were unavailable."
        )
    else:
        lines.append(
            "The issue evidence below records the available context; no merged pull request artifacts were found."
        )
    lines.append("")
    lines.append("## User Scenarios & Testing")
    lines.append("")
    if has_implementation_artifacts:
        scenario_basis = "issue evidence, related pull requests, and implementation artifacts."
    elif has_related_pr_metadata:
        scenario_basis = "issue evidence and related pull-request metadata (diff/commit artifacts were unavailable)."
    else:
        scenario_basis = "issue evidence only; no related pull requests were available."
    lines.append("")
    story_body = (
        user_stories[0] if user_stories else "A factual user story could not be established from the artifacts."
    )
    scenario_body = (
        acceptance_scenarios[0]
        if acceptance_scenarios
        else "A factual acceptance scenario could not be established from the available artifacts."
    )
    lines.append("### User Story 1 - Retroactive Implementation Evidence (Priority: P1)")
    lines.append("")
    lines.append(story_body)
    lines.append("")
    lines.append(
        f"**Why this priority**: This story is prioritized first because it is the primary "
        f"artifact-backed account of delivered behavior drawn from {scenario_basis}"
    )
    lines.append("")
    lines.append(
        "**Independent Test**: This story can be independently validated by reviewing the "
        "referenced issue and pull-request artifacts to confirm the documented behavior."
    )
    lines.append("")
    lines.append("**Acceptance Scenarios**:")
    lines.append("")
    lines.append(f"1. {scenario_body}")
    lines.append("")
    lines.append("### PR References")
    lines.append("")
    if pr_references:
        for pr_reference in pr_references:
            lines.append(f"- {pr_reference}")
    elif has_implementation_artifacts:
        lines.append("- Related pull request metadata was unavailable in the assembled context.")
    else:
        lines.append("- No related pull requests were available.")
    lines.append("")
    lines.append("### Key Changes")
    lines.append("")
    if key_change_paths:
        lines.append("The available diffs touched the following implementation areas:")
        for path in key_change_paths:
            lines.append(f"- `{path}`")
    elif commit_summaries:
        lines.append("The available commit history recorded these implementation changes:")
        for summary in commit_summaries:
            lines.append(f"- {summary}")
    elif has_implementation_artifacts:
        lines.append(
            "The available implementation artifacts did not preserve enough diff detail to summarize the "
            "principal code changes."
        )
    else:
        lines.append(
            "Merged implementation artifacts were unavailable, so the principal code changes could not be "
            "established from this source."
        )
    lines.append("")
    lines.append("### Edge Cases")
    lines.append("")
    if has_implementation_artifacts:
        lines.append("The available implementation artifacts do not establish additional edge cases.")
    else:
        lines.append("The available issue evidence does not establish additional edge cases.")
    lines.append("")
    lines.append("## Requirements")
    lines.append("")
    lines.append("### Functional Requirements")
    lines.append("")
    functional_requirements = _derive_functional_requirements(
        key_change_paths=key_change_paths,
        commit_summaries=commit_summaries,
        has_implementation_artifacts=has_implementation_artifacts,
    )
    for requirement in functional_requirements:
        lines.append(requirement)
    lines.append("")
    lines.append("### Non-Functional Requirements")
    lines.append("")
    lines.append(_derive_non_functional_requirement(has_implementation_artifacts=has_implementation_artifacts))
    lines.append("")
    lines.append("## Success Criteria")
    lines.append("")
    lines.append("### Measurable Outcomes")
    lines.append("")
    if has_implementation_artifacts:
        lines.append("- **SC-001**: The merged implementation artifacts document the delivered behavior.")
    else:
        lines.append(
            "- **SC-001**: No merged implementation artifacts were available; "
            "the delivered behavior could not be established from this source."
        )
    lines.append("")
    lines.append("## Implementation Summary")
    lines.append("")
    if has_implementation_artifacts:
        lines.append(
            "This specification was generated retroactively from implementation "
            "artifacts. LLM synthesis was unavailable; the content below is a "
            "structured extraction from the source artifacts."
        )
    else:
        lines.append(
            "This specification was generated retroactively from the issue evidence. "
            "LLM synthesis was unavailable; no merged implementation artifacts were "
            "available to extract from."
        )
    lines.append("")
    lines.append("## Implementation Artifacts")
    lines.append("")
    # Include first portion of context as reference
    lines.append(context[:5000])
    return "\n".join(lines)


def _format_pr_reference(number: int, title: str) -> str:
    """Return a stable PR reference, retaining the number even without a title."""
    return f"PR #{number}" if not title else f"PR #{number}: {title}"


_NON_BEHAVIORAL_COMMIT_RE = _re.compile(
    r"^(?:merge\b|revert\b|wip\b|bump\b|chore\b|style\b|docs\b|test\b|ci\b|build\b|refactor\b|"
    r"fix typo\b|formatting\b|cleanup\b|clean up\b|update changelog\b|auto[- ]?generated\b)",
    _re.IGNORECASE,
)


def _is_behavioral_commit(summary: str) -> bool:
    """Return True when a commit subject likely describes an observable behavior change."""
    return not _NON_BEHAVIORAL_COMMIT_RE.match(summary.strip())


def _derive_functional_requirements(
    *,
    key_change_paths: list[str],
    commit_summaries: list[str],
    has_implementation_artifacts: bool,
) -> list[str]:
    """Derive factual functional requirements from available implementation evidence."""
    behavioral = [s for s in commit_summaries if _is_behavioral_commit(s)]
    if behavioral:
        return [
            f"- **FR-{idx:03d}**: The implementation delivers: {summary}."
            for idx, summary in enumerate(behavioral[:3], 1)
        ]

    if commit_summaries:
        # Commits exist but none describe observable behavioral changes
        return [
            "- **FR-001**: The available commit history does not establish observable functional requirements "
            "(commits describe non-behavioral changes such as merges, tests, or housekeeping)."
        ]

    if key_change_paths:
        return [
            "- **FR-001**: The available implementation artifacts identify changed files, "
            "but do not establish observable functional requirements."
        ]

    if has_implementation_artifacts:
        return [
            "- **FR-001**: No factual functional requirement could be established from the available merged "
            "implementation artifacts."
        ]

    return ["- **FR-001**: No merged implementation artifacts were available to establish functional requirements."]


def _derive_non_functional_requirement(*, has_implementation_artifacts: bool) -> str:
    """Derive a factual non-functional requirement statement from artifact availability."""
    if has_implementation_artifacts:
        return (
            "- **NFR-001**: Requirements in this retroactive specification are limited to behaviors observable in "
            "the retained merged artifacts."
        )
    return (
        "- **NFR-001**: Requirements in this retroactive specification are limited to issue and PR metadata because "
        "merged implementation artifacts were unavailable."
    )


def _extract_issue_title(context_lines: list[str]) -> str:
    """Extract the issue title from the assembled context heading, if present."""
    for line in context_lines:
        if not line.startswith("## Issue #"):
            continue
        _, _, title = line.partition(":")
        return title.strip()
    return ""


def _derive_user_stories(
    *,
    issue_title: str,
    pr_references: list[str],
    key_change_paths: list[str],
    commit_summaries: list[str],
) -> list[str]:
    """Derive factual user-story style bullets from available artifacts."""
    if issue_title:
        return [f"The delivered scope described by the source issue title: {issue_title}."]
    if pr_references:
        return [f"The related pull request evidence documents delivered behavior in {pr_references[0]}."]
    if key_change_paths:
        return [f"The available implementation evidence records delivered changes in `{key_change_paths[0]}`."]
    if commit_summaries:
        return [f"The available commit history records delivered work summarized as: {commit_summaries[0]}."]
    return ["A factual user story could not be established from the available artifacts."]


def _derive_acceptance_scenarios(
    *,
    issue_title: str,
    pr_references: list[str],
    key_change_paths: list[str],
    commit_summaries: list[str],
) -> list[str]:
    """Derive factual acceptance-scenario style bullets from available artifacts."""
    if key_change_paths:
        basis = f"changes to `{key_change_paths[0]}`"
    elif commit_summaries:
        basis = f"the recorded commit summary `{commit_summaries[0]}`"
    elif pr_references:
        basis = pr_references[0]
    elif issue_title:
        basis = f"the source issue title `{issue_title}`"
    else:
        return ["A factual acceptance scenario could not be established from the available artifacts."]

    prefix = (
        f"Given the delivered scope captured by {issue_title}, "
        if issue_title
        else "Given the available delivery artifacts, "
    )
    return [f"{prefix}when the implementation evidence is reviewed, then it traces the change through {basis}."]


def format_retroactive_spec(
    content: str,
    *,
    issue_number: int | None = None,
    title: str | None = None,
    labels: list[str] | None = None,
    milestone: str = "",
) -> str:
    """Return the generated spec content with retroactive metadata markers.

    Prepends ``_RETROACTIVE_HEADER`` to *content*, capping both the title and
    the body so the total (header + body) always stays within ``_MAX_OUTPUT_CHARS``
    and the required retroactive markers (``**Generated**: retroactive``,
    the warning block) are never truncated.
    """
    raw_title = title if isinstance(title, str) else ""
    # Cap the title to prevent an excessively long title from consuming the
    # header budget and truncating required retroactive markers.
    safe_title = " ".join(raw_title.split())[:500]
    safe_labels = [label.replace("\n", " ").strip() for label in (labels or []) if isinstance(label, str)]
    milestone_text = milestone if isinstance(milestone, str) else ""
    safe_milestone = " ".join(milestone_text.split())
    source_issue = f"**Source Issue**: #{issue_number}" if issue_number is not None else ""
    if source_issue:
        source_issue += "\n"

    def _render_header(*, labels_text: str, milestone_text: str) -> str:
        rendered = _RETROACTIVE_HEADER.format(
            created=date.today().isoformat(),
            source_issue=source_issue,
            labels=labels_text,
            milestone=milestone_text,
        )
        if safe_title:
            rendered = rendered.replace(
                "# Feature Specification: Retroactive Implementation", f"# Feature Specification: {safe_title}"
            )
        return rendered

    base_header = _render_header(labels_text="", milestone_text="")
    metadata_budget = max(0, _MAX_OUTPUT_CHARS - len(base_header) - _MIN_BODY_CHARS)
    label_line = ""
    if safe_labels and metadata_budget > len("**Labels**: …\n"):
        labels_text = ", ".join(safe_labels)
        max_labels_chars = metadata_budget - len("**Labels**: …\n")
        if len(labels_text) > max_labels_chars:
            label_line = f"**Labels**: {labels_text[:max_labels_chars]}…\n"
        else:
            label_line = f"**Labels**: {labels_text}\n"
        metadata_budget -= len(label_line)

    milestone_line = ""
    if safe_milestone and metadata_budget > len("**Milestone**: …\n"):
        max_milestone_chars = metadata_budget - len("**Milestone**: …\n")
        if len(safe_milestone) > max_milestone_chars:
            milestone_line = f"**Milestone**: {safe_milestone[:max_milestone_chars]}…\n"
        else:
            milestone_line = f"**Milestone**: {safe_milestone}\n"

    header = _render_header(
        labels_text=label_line,
        milestone_text=milestone_line,
    )
    if len(header) > _MAX_OUTPUT_CHARS:
        header = _render_header(labels_text="", milestone_text="")
    if len(header) > _MAX_OUTPUT_CHARS:
        return header[:_MAX_OUTPUT_CHARS]
    available = _MAX_OUTPUT_CHARS - len(header)
    budget = max(0, available)
    capped = _cap_content(content, budget)
    all_required = (*_REQUIRED_SYNTHESIS_MARKERS, *_TOOL_INJECTED_REQUIRED_MARKERS)
    if not _required_sections_intact(content, capped) or not all(
        marker not in content or marker in capped for marker in all_required
    ):
        capped = _cap_with_required_sections(content, budget)
    # Post-validate: if required markers are still absent after section-preserving
    # capping, fall back to a compact marker-bearing excerpt that still honors
    # the total output cap.
    if not all(marker not in content or marker in capped for marker in all_required):
        markers_in_content = [m for m in all_required if m in content]
        capped = _marker_excerpt_within_limit(content, markers_in_content, budget)
    return header + capped


def write_spec_file(
    content: str,
    target_path: str | Path,
    output_file: str | Path | None = None,
    *,
    issue_number: int | None = None,
    title: str | None = None,
    labels: list[str] | None = None,
    milestone: str = "",
) -> None:
    """Write the generated spec.md with retroactive metadata markers.

    Creates the target directory if needed. Adds the retroactive metadata
    header before the generated content.

    Args:
        content: The generated spec content.
        target_path: Path to the target directory where the spec file will be written.
        output_file: Explicit path to the spec file. When provided, the spec is
            written to this exact path instead of ``target_path/spec.md``. This
            supports custom ``--output`` filenames (e.g. ``my-spec.md``).
        issue_number: Source issue number to include in retroactive metadata.
        title: Source issue title used for the document heading.
        labels: Source issue labels rendered in retroactive metadata.
        milestone: Source issue milestone rendered in retroactive metadata.
    """
    target = Path(target_path)
    target.mkdir(parents=True, exist_ok=True)
    spec_file = Path(output_file) if output_file is not None else target / "spec.md"
    spec_file.write_text(
        format_retroactive_spec(
            content,
            issue_number=issue_number,
            title=title,
            labels=labels,
            milestone=milestone,
        ),
        encoding="utf-8",
    )
