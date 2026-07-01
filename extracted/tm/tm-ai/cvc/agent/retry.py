"""
cvc.agent.retry — Agentic Auto-Retry System (Intelligent Redo).

Implements the 3-step automatic retry workflow:
  1. Diagnose: Analyze what went wrong and classify severity
  2. Revert: Selectively undo file changes (non-git, human-in-the-loop for big issues)
  3. Re-execute: Replay the original task with lessons-learned context

This converts the manual "undo → edit prompt → resend" cycle into a single
agentic action triggered by a short user complaint.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger("cvc.agent.retry")

# ---------------------------------------------------------------------------
# Severity threshold: 3+ files = "big" issue requiring revert + permission
# ---------------------------------------------------------------------------
BIG_ISSUE_FILE_THRESHOLD = 3

# Max number of lessons to keep in .cvc/lessons.md
MAX_LESSONS = 50

# Patterns that indicate a user wants to retry/redo
RETRY_INTENT_PATTERNS = [
    r"(?:this|that|it)\s+(?:is|was|looks?)\s+(?:wrong|bad|incorrect|broken)",
    r"(?:that'?s?\s+)?not\s+(?:what\s+I\s+(?:wanted|asked|meant)|right|correct)",
    r"\b(?:redo|undo|retry|revert|rollback|start\s*over|try\s*again)\b",
    r"(?:do|try)\s+(?:it|this|that)\s+(?:again|over)",
    r"you\s+(?:did|got)\s+(?:it|this|that)\s+wrong",
    r"(?:this|that|it)\s+(?:doesn'?t|does\s*not)\s+(?:work|look\s+right)",
    r"(?:go|take)\s+(?:it\s+)?back",
    r"(?:scrap|scratch)\s+(?:this|that|it)",
    r"wrong\s+(?:approach|implementation|way)",
    r"completely\s+(?:wrong|off|different)",
]

_RETRY_RE = re.compile("|".join(RETRY_INTENT_PATTERNS), re.IGNORECASE)


@dataclass
class DiagnosisResult:
    """Result of analyzing what went wrong with the previous attempt."""
    severity: Literal["small", "big"]
    files_affected: list[str]
    what_went_wrong: str
    lessons_learned: list[str]
    original_prompt: str
    original_turn_id: int
    recommended_action: Literal["fix_in_place", "revert_and_retry"]
    user_complaint: str = ""


# ---------------------------------------------------------------------------
# Retry Intent Detection
# ---------------------------------------------------------------------------

def detect_retry_intent(user_input: str) -> bool:
    """
    Check if user input expresses dissatisfaction and retry intent.

    Returns True for short negative feedback that suggests the user wants
    the AI to redo its work. Returns False for longer messages that are
    likely follow-up instructions.
    """
    # Only trigger on short messages (< 200 chars) — longer messages are
    # likely detailed follow-up instructions, not retry triggers
    if len(user_input) > 200:
        return False

    return bool(_RETRY_RE.search(user_input))


# ---------------------------------------------------------------------------
# Diagnosis Engine
# ---------------------------------------------------------------------------

DIAGNOSIS_PROMPT = """\
You are analyzing a failed AI coding attempt to extract lessons learned.

## Original User Task
{original_prompt}

## Files Changed ({num_files} files)
{file_changes_summary}

## User Complaint
{user_complaint}

## Assistant's Last Response (excerpt)
{assistant_response}

---

Analyze what went wrong and respond with ONLY a JSON object (no markdown, no explanation):

{{
  "severity": "small" or "big",
  "what_went_wrong": "Clear 1-2 sentence description of the core issue",
  "lessons_learned": ["Specific actionable lesson 1", "Specific actionable lesson 2", ...]
}}

Rules for severity classification:
- "small": The issue affects 1-2 files AND is a minor correction (typo, wrong value, missing import, style issue)
- "big": The issue affects 3+ files OR the fundamental approach/architecture is wrong OR the user explicitly says to redo/start over

Keep lessons_learned concrete and actionable (max 5 items). Each lesson should be a DO or DON'T instruction.
"""


async def diagnose_issue(
    llm: Any,
    original_prompt: str,
    user_complaint: str,
    file_changes: list[Any],  # list[FileChange]
    assistant_response: str,
    turn_id: int,
    workspace: Path,
) -> DiagnosisResult:
    """
    Use the LLM to analyze what went wrong and classify the issue.

    Parameters
    ----------
    llm : AgentLLM
        The LLM instance for making the diagnosis call.
    original_prompt : str
        The user's original task/query that started the failed attempt.
    user_complaint : str
        The user's complaint about the result.
    file_changes : list[FileChange]
        All file changes from the failed turn.
    assistant_response : str
        The assistant's response text from the failed turn.
    turn_id : int
        The turn ID of the failed attempt.
    workspace : Path
        Workspace root for relative path display.
    """
    # Build file changes summary
    changes_summary_parts = []
    for fc in file_changes:
        rel = fc.path.relative_to(workspace) if fc.path.is_relative_to(workspace) else fc.path
        action = "CREATED" if fc.old_content is None else "MODIFIED"
        changes_summary_parts.append(f"- {rel} ({action} by {fc.tool_name})")
    file_changes_summary = "\n".join(changes_summary_parts) if changes_summary_parts else "(no file changes)"

    files_affected = []
    for fc in file_changes:
        rel = str(fc.path.relative_to(workspace) if fc.path.is_relative_to(workspace) else fc.path)
        if rel not in files_affected:
            files_affected.append(rel)

    # Build the diagnosis prompt
    prompt_text = DIAGNOSIS_PROMPT.format(
        original_prompt=original_prompt[:2000],
        num_files=len(files_affected),
        file_changes_summary=file_changes_summary[:3000],
        user_complaint=user_complaint[:500],
        assistant_response=assistant_response[:2000],
    )

    try:
        response = await llm.chat(
            messages=[
                {"role": "system", "content": "You are a code review analyst. Respond with ONLY valid JSON."},
                {"role": "user", "content": prompt_text},
            ],
            tools=[],
            temperature=0.3,
            max_tokens=1024,
        )

        # Parse the JSON response
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*\n?", "", text)
            text = re.sub(r"\n?```\s*$", "", text)

        result = json.loads(text)

        severity = result.get("severity", "big")
        # Override severity based on file count threshold
        if len(files_affected) >= BIG_ISSUE_FILE_THRESHOLD and severity == "small":
            severity = "big"

        return DiagnosisResult(
            severity=severity,
            files_affected=files_affected,
            what_went_wrong=result.get("what_went_wrong", "Unknown issue"),
            lessons_learned=result.get("lessons_learned", [])[:5],
            original_prompt=original_prompt,
            original_turn_id=turn_id,
            recommended_action="fix_in_place" if severity == "small" else "revert_and_retry",
            user_complaint=user_complaint,
        )

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.warning("Failed to parse diagnosis response: %s", e)
        # Fallback: use heuristic-based diagnosis
        severity: Literal["small", "big"] = "big" if len(files_affected) >= BIG_ISSUE_FILE_THRESHOLD else "small"
        return DiagnosisResult(
            severity=severity,
            files_affected=files_affected,
            what_went_wrong=f"User reported issue: {user_complaint[:200]}",
            lessons_learned=[f"Address: {user_complaint[:100]}"],
            original_prompt=original_prompt,
            original_turn_id=turn_id,
            recommended_action="fix_in_place" if severity == "small" else "revert_and_retry",
            user_complaint=user_complaint,
        )


# ---------------------------------------------------------------------------
# Retry Prompt Builder
# ---------------------------------------------------------------------------

def build_retry_prompt(diagnosis: DiagnosisResult) -> str:
    """
    Build an enhanced prompt that includes the original task plus
    lessons learned from the failed attempt.
    """
    lessons_block = "\n".join(f"  - {lesson}" for lesson in diagnosis.lessons_learned)

    if diagnosis.severity == "small":
        # For small issues: targeted fix prompt
        return (
            f"The previous changes had an issue. Fix it without starting over.\n\n"
            f"**What went wrong:** {diagnosis.what_went_wrong}\n\n"
            f"**Lessons — apply these fixes:**\n{lessons_block}\n\n"
            f"**User feedback:** {diagnosis.user_complaint}\n\n"
            f"Make targeted corrections to fix the issue."
        )
    else:
        # For big issues: full redo prompt with lessons
        return (
            f"Re-implement the following task from scratch. "
            f"The previous attempt has been reverted.\n\n"
            f"## Original Task\n{diagnosis.original_prompt}\n\n"
            f"## Lessons from Previous Attempt — DO NOT repeat these mistakes\n"
            f"{lessons_block}\n\n"
            f"## What Went Wrong Last Time\n{diagnosis.what_went_wrong}\n\n"
            f"## User Feedback\n{diagnosis.user_complaint}\n\n"
            f"Re-implement the original task correctly, applying all lessons learned."
        )


# ---------------------------------------------------------------------------
# Lessons Persistence
# ---------------------------------------------------------------------------

def persist_lessons(workspace: Path, diagnosis: DiagnosisResult) -> None:
    """
    Append lessons learned to .cvc/lessons.md for future sessions.

    This file is automatically loaded by the system prompt builder
    and injected as context for all future LLM calls.
    """
    lessons_path = workspace / ".cvc" / "lessons.md"
    lessons_path.parent.mkdir(parents=True, exist_ok=True)

    # Format the new lessons entry
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    entry_lines = [
        f"\n### Lesson ({timestamp})",
        f"**Task:** {diagnosis.original_prompt[:150]}",
        f"**Issue:** {diagnosis.what_went_wrong}",
    ]
    for lesson in diagnosis.lessons_learned:
        entry_lines.append(f"- {lesson}")
    entry_lines.append("")
    new_entry = "\n".join(entry_lines)

    # Read existing content
    existing = ""
    if lessons_path.exists():
        try:
            existing = lessons_path.read_text(encoding="utf-8")
        except OSError:
            pass

    # Append new entry
    updated = existing + new_entry

    # Enforce rolling window: keep only ~MAX_LESSONS most recent entries
    sections = updated.split("\n### Lesson ")
    if len(sections) > MAX_LESSONS + 1:  # +1 for possible header before first ###
        # Keep header (sections[0]) and last MAX_LESSONS entries
        sections = [sections[0]] + sections[-(MAX_LESSONS):]
        updated = "\n### Lesson ".join(sections)

    try:
        lessons_path.write_text(updated, encoding="utf-8")
        logger.debug("Persisted %d lessons to %s", len(diagnosis.lessons_learned), lessons_path)
    except OSError as e:
        logger.warning("Failed to persist lessons: %s", e)


# ---------------------------------------------------------------------------
# Conversation Rewind (for big-issue revert)
# ---------------------------------------------------------------------------

def rewind_messages_to_turn(
    messages: list[dict[str, Any]],
    turn_id: int,
    turn_prompts: dict[int, str],
) -> list[dict[str, Any]]:
    """
    Truncate conversation messages to remove the failed turn's assistant
    response and tool calls, while keeping the original user prompt
    and all prior context.

    This leaves the conversation in a state as if the failed attempt
    never happened (from the LLM's perspective).

    Parameters
    ----------
    messages : list
        The full conversation message list.
    turn_id : int
        The turn to rewind (remove its assistant/tool messages).
    turn_prompts : dict
        Mapping of turn_id → user input text.

    Returns
    -------
    list
        The truncated message list.
    """
    original_prompt = turn_prompts.get(turn_id, "")
    if not original_prompt:
        return messages

    # Find the user message that started this turn
    # Walk backwards from the end to find the matching user message
    target_idx = -1
    for i in range(len(messages) - 1, -1, -1):
        msg = messages[i]
        if msg.get("role") == "user" and msg.get("content") == original_prompt:
            target_idx = i
            break

    if target_idx < 0:
        # Fallback: find the last user message
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                target_idx = i
                break

    if target_idx < 0:
        return messages

    # Truncate: keep everything up to (but not including) the user message
    # for this turn — so the LLM sees a clean slate
    return messages[:target_idx]


# ---------------------------------------------------------------------------
# Revert File Selection Menu
# ---------------------------------------------------------------------------

def show_revert_menu(
    files_affected: list[str],
) -> Literal["all", "select", "cancel"]:
    """
    Show interactive menu for selecting revert scope.

    Returns
    -------
    "all" : Revert all changed files
    "select" : User wants to select specific files
    "cancel" : User cancelled
    """
    from cvc.agent.menus import arrow_select

    options: list[tuple[str, str]] = [
        (f"Revert ALL changed files ({len(files_affected)} files)", "all"),
        ("Select specific files to revert", "select"),
        ("Cancel — don't revert anything", "cancel"),
    ]

    descriptions = [
        "Recommended — restores all files to pre-change state",
        "Choose which files to revert individually",
        "Keep current changes, skip retry",
    ]

    choice = arrow_select(
        "Revert Files",
        options,
        descriptions=descriptions,
        default=0,
    )

    return choice if choice is not None else "cancel"


def show_file_select_menu(files_affected: list[str]) -> list[str]:
    """
    Show per-file selection menu. Returns list of selected file paths.

    Uses multiple arrow_confirm calls for each file.
    """
    from cvc.agent.menus import arrow_confirm
    from cvc.agent.renderer import render_info

    selected: list[str] = []
    render_info("Select files to revert (Yes/No for each):")

    for filepath in files_affected:
        if arrow_confirm(f"  Revert {filepath}?", default_yes=True):
            selected.append(filepath)

    return selected
