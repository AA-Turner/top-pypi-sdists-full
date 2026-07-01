"""
cvc.core.learning_extractor — Cognitive Commit Learning Extractor (CCLE).

Analyzes the cognitive diff between consecutive commits to extract:
  - Skills learned (reusable patterns the agent discovered)
  - Mistakes made (errors and corrections)
  - Patterns discovered (recurring approaches)
  - User preferences observed (style, conventions, priorities)

Every extraction is stored as a structured ``LearningExtract`` and persisted
to ``.cvc/learnings/`` with Merkle hash linkage back to the source commits.
The extracts are also embedded in ChromaDB for semantic search.

This is the foundation of CVC's self-improvement loop — all other
learning features (skill auto-extraction, user modeling, dreaming)
build on top of CCLE outputs.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("cvc.learning")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class LearnedSkill(BaseModel):
    """A reusable pattern discovered from commit analysis."""

    name: str
    description: str
    trigger_pattern: str = ""  # Regex for auto-invocation
    confidence: float = 0.0  # 0.0–1.0 how confident the extraction is
    source_commits: list[str] = Field(default_factory=list)


class MistakeLearned(BaseModel):
    """An error pattern and the correction that fixed it."""

    description: str
    error_pattern: str  # What went wrong
    correction: str  # What fixed it
    severity: str = "low"  # low | medium | high
    source_commits: list[str] = Field(default_factory=list)


class UserPreference(BaseModel):
    """An observed user preference or convention."""

    category: str  # "code_style" | "communication" | "workflow" | "tooling"
    observation: str  # What was observed
    confidence: float = 0.0
    evidence: str = ""  # Supporting context


class LearningExtract(BaseModel):
    """Structured output of a CCLE analysis pass."""

    extract_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: float = Field(default_factory=time.time)
    source_commit: str = ""  # The newer commit analyzed
    parent_commit: str = ""  # The older commit compared against
    branch: str = ""
    skills: list[LearnedSkill] = Field(default_factory=list)
    mistakes: list[MistakeLearned] = Field(default_factory=list)
    preferences: list[UserPreference] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)  # Free-form pattern descriptions
    summary: str = ""  # One-paragraph summary of what was learned
    token_cost: float = 0.0  # Cost of the extraction LLM call


# ---------------------------------------------------------------------------
# Prompt template for the LLM extraction call
# ---------------------------------------------------------------------------

EXTRACTION_PROMPT = """\
You are a cognitive learning extractor. Analyze the diff between two consecutive \
agent cognitive states (commits) and extract structured learning.

## Previous Cognitive State (Parent Commit: {parent_hash})
Messages: {parent_msg_count}
Reasoning trace: {parent_trace_preview}
Tools used: {parent_tools}

## Current Cognitive State (Commit: {current_hash})
Messages: {current_msg_count}
Reasoning trace: {current_trace_preview}
Tools used: {current_tools}
Files affected: {files_affected}

## New Messages Since Parent (the cognitive diff):
{diff_messages}

## Instructions
Analyze the cognitive evolution between these two states. Extract:

1. **skills**: Reusable patterns (name, description, trigger_pattern regex)
2. **mistakes**: Errors and corrections (description, error_pattern, correction)
3. **preferences**: User preferences (category, observation, confidence 0-1)
4. **patterns**: Recurring approaches or strategies (free text list)
5. **summary**: One paragraph summarizing what was learned

Respond with ONLY valid JSON matching this schema:
{{
  "skills": [{{"name": "", "description": "", "trigger_pattern": "", "confidence": 0.0}}],
  "mistakes": [{{"description": "", "error_pattern": "", "correction": "", "severity": "low"}}],
  "preferences": [{{"category": "", "observation": "", "confidence": 0.0, "evidence": ""}}],
  "patterns": [""],
  "summary": ""
}}

If nothing meaningful was learned (e.g., trivial commit), return empty arrays and \
a summary stating "No significant learning detected."
"""


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class CognitiveLearnExtractor:
    """
    Extracts structured learning from cognitive commit diffs.

    Operates on the CVC engine's commit history, comparing consecutive
    commits to identify what changed in the agent's reasoning and what
    can be learned from those changes.
    """

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self.learnings_dir = cvc_root / "learnings"
        self.learnings_dir.mkdir(parents=True, exist_ok=True)

    def build_extraction_prompt(
        self,
        parent_blob: Any,  # ContentBlob
        current_blob: Any,  # ContentBlob
        parent_hash: str,
        current_hash: str,
    ) -> str:
        """Build the LLM prompt for a commit-pair analysis."""
        # Compute the diff: messages in current that aren't in parent
        parent_msg_count = len(parent_blob.messages) if parent_blob else 0
        current_msg_count = len(current_blob.messages)

        diff_messages = ""
        start_idx = parent_msg_count if parent_blob else 0
        for msg in current_blob.messages[start_idx:]:
            role = msg.role
            content = msg.content[:500] if len(msg.content) > 500 else msg.content
            diff_messages += f"[{role}]: {content}\n\n"

        if not diff_messages.strip():
            diff_messages = "(No new messages)"

        # Gather tool info
        parent_tools = ", ".join(parent_blob.tool_outputs.keys()) if parent_blob else "none"
        current_tools = ", ".join(current_blob.tool_outputs.keys()) or "none"

        # Files affected
        files = list(current_blob.source_files.keys()) + list(current_blob.files_written.keys())
        files_str = ", ".join(files[:20]) or "none"

        return EXTRACTION_PROMPT.format(
            parent_hash=parent_hash[:12],
            parent_msg_count=parent_msg_count,
            parent_trace_preview=(parent_blob.reasoning_trace[:200] if parent_blob else "none"),
            parent_tools=parent_tools,
            current_hash=current_hash[:12],
            current_msg_count=current_msg_count,
            current_trace_preview=current_blob.reasoning_trace[:200] or "none",
            current_tools=current_tools,
            files_affected=files_str,
            diff_messages=diff_messages[:3000],  # Cap to avoid token overflow
        )

    def parse_llm_response(self, response_text: str) -> LearningExtract:
        """Parse the LLM's JSON response into a LearningExtract."""
        # Strip markdown code fences if present
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse LLM learning extraction response")
            return LearningExtract(summary="Extraction failed: invalid JSON response")

        extract = LearningExtract(summary=data.get("summary", ""))

        for sk in data.get("skills", []):
            if sk.get("name"):
                extract.skills.append(
                    LearnedSkill(
                        name=sk["name"],
                        description=sk.get("description", ""),
                        trigger_pattern=sk.get("trigger_pattern", ""),
                        confidence=float(sk.get("confidence", 0.5)),
                    )
                )

        for mk in data.get("mistakes", []):
            if mk.get("description"):
                extract.mistakes.append(
                    MistakeLearned(
                        description=mk["description"],
                        error_pattern=mk.get("error_pattern", ""),
                        correction=mk.get("correction", ""),
                        severity=mk.get("severity", "low"),
                    )
                )

        for pref in data.get("preferences", []):
            if pref.get("observation"):
                extract.preferences.append(
                    UserPreference(
                        category=pref.get("category", "workflow"),
                        observation=pref["observation"],
                        confidence=float(pref.get("confidence", 0.5)),
                        evidence=pref.get("evidence", ""),
                    )
                )

        extract.patterns = [p for p in data.get("patterns", []) if p]

        return extract

    def persist_extract(
        self,
        extract: LearningExtract,
        parent_hash: str,
        current_hash: str,
        branch: str,
    ) -> Path:
        """Save a learning extract to disk as JSON."""
        extract.source_commit = current_hash
        extract.parent_commit = parent_hash
        extract.branch = branch

        # Tag skills with source commits
        for skill in extract.skills:
            skill.source_commits = [parent_hash, current_hash]
        for mistake in extract.mistakes:
            mistake.source_commits = [parent_hash, current_hash]

        filename = f"{extract.extract_id}_{current_hash[:8]}.json"
        path = self.learnings_dir / filename
        path.write_text(
            extract.model_dump_json(indent=2),
            encoding="utf-8",
        )
        logger.info(
            "Persisted learning extract %s: %d skills, %d mistakes, %d preferences",
            extract.extract_id,
            len(extract.skills),
            len(extract.mistakes),
            len(extract.preferences),
        )
        return path

    def load_all_extracts(self) -> list[LearningExtract]:
        """Load all persisted learning extracts."""
        extracts = []
        if not self.learnings_dir.exists():
            return extracts
        for f in sorted(self.learnings_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                extracts.append(LearningExtract.model_validate(data))
            except Exception as e:
                logger.warning("Failed to load extract %s: %s", f.name, e)
        return extracts

    def update_lessons_file(self, extract: LearningExtract) -> None:
        """Append significant learnings to .cvc/lessons.md for session loading."""
        if not extract.mistakes and not extract.skills:
            return  # Nothing significant to persist

        lessons_path = self.cvc_root / "lessons.md"
        existing = ""
        if lessons_path.exists():
            existing = lessons_path.read_text(encoding="utf-8")

        new_entries = []
        for mistake in extract.mistakes:
            rule = (
                f"- **[{mistake.severity.upper()}]** {mistake.description}\n"
                f"  - Error: {mistake.error_pattern}\n"
                f"  - Fix: {mistake.correction}\n"
                f"  - Source: commits {', '.join(h[:8] for h in mistake.source_commits)}\n"
            )
            # Avoid duplicates (simple substring check)
            if mistake.error_pattern and mistake.error_pattern not in existing:
                new_entries.append(rule)

        for skill in extract.skills:
            if skill.confidence >= 0.7:
                entry = (
                    f"- **[SKILL]** {skill.name}: {skill.description}\n"
                    f"  - Trigger: `{skill.trigger_pattern}`\n"
                    f"  - Source: commits {', '.join(h[:8] for h in skill.source_commits)}\n"
                )
                if skill.name not in existing:
                    new_entries.append(entry)

        if new_entries:
            if not existing:
                existing = "# CVC Learned Lessons\n\nAuto-extracted from diffs.\n\n"
            existing += "\n".join(new_entries) + "\n"
            lessons_path.write_text(existing, encoding="utf-8")
            logger.info("Updated lessons.md with %d new entries", len(new_entries))

    def get_recent_extract_count(self, since_timestamp: float) -> int:
        """Count extracts since a given timestamp (for rate limiting)."""
        count = 0
        for f in self.learnings_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("timestamp", 0) >= since_timestamp:
                    count += 1
            except Exception:
                pass
        return count
