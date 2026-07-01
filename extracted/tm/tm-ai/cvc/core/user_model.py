"""
cvc.core.user_model — Versioned User Identity Model (VUIM).

Implements Honcho-style formal logical reasoning (deductive, inductive,
abductive) over user data, but every update is a CVC commit on a dedicated
``user-model`` branch.

Key innovation: Unlike Honcho where the identity model is mutable,
CVC *versions* every identity update. You can:
  - ``cvc diff user-model~5 user-model`` to see how understanding evolved
  - Revert a bad user model update
  - Audit the full chain of reasoning that built the model

The model stores:
  - Deductive conclusions (certain, from explicit statements)
  - Inductive conclusions (probable patterns from repeated observations)
  - Abductive conclusions (best explanations for observed behavior)
  - Preferences, communication style, expertise areas
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path

from pydantic import BaseModel, Field

from cvc.core.correction import (
    CorrectionRecord,
    build_corrections_prompt_block,
)

logger = logging.getLogger("cvc.user_model")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Conclusion(BaseModel):
    """A single reasoned conclusion about the user."""

    conclusion_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    reasoning_type: str  # "deductive" | "inductive" | "abductive"
    statement: str
    premises: list[str] = Field(default_factory=list)
    confidence: float = 0.0  # 0.0–1.0
    evidence_commits: list[str] = Field(default_factory=list)  # Source commit hashes
    created_at: float = Field(default_factory=time.time)
    supersedes: str | None = None  # ID of conclusion this replaces (contradiction handling)


class UserIdentitySnapshot(BaseModel):
    """
    A point-in-time snapshot of the agent's understanding of the user.

    Each snapshot is committed to the ``user-model`` branch, creating
    an immutable, auditable history of identity reasoning.
    """

    snapshot_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    timestamp: float = Field(default_factory=time.time)

    # Structured identity dimensions
    name: str = ""
    expertise_areas: list[str] = Field(default_factory=list)
    communication_style: str = ""  # "concise" | "detailed" | "casual" | "formal" ...
    preferred_languages: list[str] = Field(default_factory=list)  # Programming languages
    preferred_tools: list[str] = Field(default_factory=list)
    coding_conventions: list[str] = Field(default_factory=list)
    workflow_preferences: list[str] = Field(default_factory=list)

    # Formal reasoning tree
    conclusions: list[Conclusion] = Field(default_factory=list)

    # Aggregate confidence per dimension
    confidence_scores: dict[str, float] = Field(default_factory=dict)

    # Summary for system prompt injection
    narrative_summary: str = ""

    # ── V2 Soul-Layer Fields ─────────────────────────────────────────
    #
    # These fields extend the user model from "knows your coding style"
    # to "knows who you are." They're optional with defaults so existing
    # v1 code and v1 model files load without modification.
    #

    # The social graph of a life: people, projects, places, pets.
    # Over years this becomes the entity map the soul uses to answer
    # "tell me about dad's friends."
    entities: list[Entity] = Field(default_factory=list)

    # What the user believes in — explicitly stated or consistently
    # demonstrated. These are the values the soul carries forward.
    values: list[ValueStatement] = Field(default_factory=list)

    # Mood and tone tracking across sessions. The emotional arc of
    # the relationship — the soul remembers not just what happened
    # but how it felt.
    emotional_context: list[EmotionalContext] = Field(default_factory=list)

    # Facts with temporal scope: what's ALWAYS true vs what's true
    # RIGHT NOW. The soul needs this distinction because identity
    # is the "always" layer, not the "now" layer.
    temporal_facts: list[TemporalFact] = Field(default_factory=list)

    # Milestones that shaped the owner. The spine of the life-story
    # view and the backbone of digital parents.
    life_events: list[LifeEvent] = Field(default_factory=list)

    # The living paragraph: "who this person IS." Not a list of
    # preferences — a holistic narrative that captures the essence.
    # Updated incrementally as the soul learns more. This is what
    # gets injected into a cold-start system prompt so a new brain
    # immediately feels like the same soul to the user.
    soul_narrative: str = ""

    # ── Self-Correction Loop (v2.1) ───────────────────────────────────
    #
    # Direct corrections from the owner override inferred claims.
    # Append-only, versioned via ``superseded_by``. The active subset
    # is injected into SOUL_REASONING_PROMPT on every reasoning pass
    # as ground truth — the LLM is told to trust corrections over
    # inference. See cvc.core.correction for the override semantics.
    #
    # Default empty list = backward-compatible: existing v2 snapshots
    # load without modification.
    corrections: list[CorrectionRecord] = Field(default_factory=list)

    def get_conclusions_by_type(self, reasoning_type: str) -> list[Conclusion]:
        """Filter conclusions by reasoning type."""
        return [c for c in self.conclusions if c.reasoning_type == reasoning_type]

    def active_conclusions(self) -> list[Conclusion]:
        """Return conclusions that haven't been superseded."""
        superseded_ids = {c.supersedes for c in self.conclusions if c.supersedes}
        return [c for c in self.conclusions if c.conclusion_id not in superseded_ids]


# ---------------------------------------------------------------------------
# V2 Soul-Layer Models — the soul's growing understanding of its owner
# ---------------------------------------------------------------------------
#
# These five model classes extend CVC's user model beyond technical
# preferences (coding conventions, tools) into the dimensions that make
# a soul know its owner:
#
#   Entity          — the social graph of a life (people, projects, places)
#   ValueStatement  — what the user believes in, explicitly or by action
#   EmotionalContext — mood and tone tracking across sessions
#   TemporalFact    — what's true NOW vs what's ALWAYS true
#   LifeEvent       — milestones that shaped the person
#
# Together they transform CVC from "knows your coding style" to
# "knows who you are." This is the foundation for digital parents.
#


class Entity(BaseModel):
    """A person, project, place, or concept the user cares about.

    Over years of use, the entity list becomes the social graph of
    a life. Every person mentioned by name, every project labored
    over, every place lived in — each is an Entity with a
    relationship to the owner. This is what makes the soul able to
    answer "tell me about dad's friends" decades later.
    """

    entity_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str
    entity_type: str = "person"  # person | project | place | tool | concept | pet | organization | event
    relationship: str = ""  # "wife", "colleague", "dog", "main project", "hometown"
    first_mentioned: float = Field(default_factory=time.time)
    last_mentioned: float = Field(default_factory=time.time)
    mention_count: int = 1
    context_snippets: list[str] = Field(default_factory=list)  # short quotes where entity appeared
    source_commits: list[str] = Field(default_factory=list)
    attributes: dict[str, str] = Field(default_factory=dict)  # extensible: {"role": "CTO", "company": "lvl360"}


class ValueStatement(BaseModel):
    """Something the user believes in or consistently acts on.

    Not extracted from tone — explicitly stated or repeatedly
    demonstrated. "I always ship behind a feature flag." "Family
    comes before deadlines." These are the values the soul carries
    forward when answering on behalf of the owner.
    """

    value_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    statement: str
    category: str = "work"  # work | life | philosophy | technical | social
    confidence: float = 0.5
    first_observed: float = Field(default_factory=time.time)
    last_reinforced: float = Field(default_factory=time.time)
    evidence_commits: list[str] = Field(default_factory=list)
    superseded_by: str | None = None  # if the user changed their mind


class EmotionalContext(BaseModel):
    """A mood observation from a specific moment.

    Captured passively from the user's tone, frustration level,
    excitement. Over time this builds the emotional arc of the
    relationship — the soul remembers not just WHAT happened but
    HOW IT FELT. This is what makes time-travel feel like
    remembering, not replaying.
    """

    timestamp: float = Field(default_factory=time.time)
    mood: str = "neutral"  # frustrated | excited | focused | tired | curious | proud | anxious | neutral
    intensity: float = 0.5  # 0.0 (barely noticeable) to 1.0 (overwhelming)
    trigger: str = ""  # what caused it: "bug found", "feature shipped", "deadline pressure"
    session_commit: str = ""  # provenance: which cognitive commit this was observed in


class TemporalFact(BaseModel):
    """A fact about the user with a temporal scope.

    Some things are ALWAYS true (lives in Delhi, prefers vim).
    Some are true RIGHT NOW (working on the Telegram bug, using
    Claude this week). Some are PERIODIC (reviews code every
    Friday). The soul needs to distinguish these because
    "what's true now" changes but "what's always true" is
    identity.
    """

    fact_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    statement: str
    scope: str = "current"  # "always" | "current" | "periodic"
    valid_from: float = Field(default_factory=time.time)
    valid_until: float | None = None  # None = still true; a timestamp = expired
    category: str = "general"  # location | project | role | tool | preference | health | personal
    confidence: float = 0.5
    source_commits: list[str] = Field(default_factory=list)


class LifeEvent(BaseModel):
    """A milestone that shaped the owner.

    Not every commit is a life event. Life events are the moments
    that mattered: first deploy, major breakthrough, career change,
    personal loss. The soul uses these to construct the narrative
    arc of a life — the spine of the "life story" view and the
    backbone of digital parents.
    """

    event_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    timestamp: float = Field(default_factory=time.time)
    event_type: str = "milestone"  # milestone | breakthrough | setback | personal | professional
    description: str
    emotional_weight: float = 0.5  # 0.0 (routine) to 1.0 (life-changing)
    source_commits: list[str] = Field(default_factory=list)
    related_entities: list[str] = Field(default_factory=list)  # entity_ids


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

REASONING_PROMPT = """\
You are a user identity reasoning engine. Analyze the conversation to build a \
formal model of the user using three types of logical reasoning.

## Current User Model
{current_model_json}

## New Conversation Data (from recent commits)
{conversation_data}

## Instructions
Perform formal reasoning about the user's identity:

1. **Deductive** (certain): Conclusions directly stated by the user.
   Example: User said "I prefer Python" -> deductive: user prefers Python.

2. **Inductive** (probable): Patterns from repeated observations.
   Example: User always asks for type hints -> inductive: user values type safety.

3. **Abductive** (best explanation): Infer WHY the user behaves a certain way.
   Example: User often asks about performance -> abductive: user works on \
performance-critical systems.

Also check for **contradictions**: if new evidence contradicts an existing \
conclusion, mark the old conclusion as superseded with the ID of the new one.

Respond with ONLY valid JSON:
{{
  "new_conclusions": [
    {{
      "reasoning_type": "deductive|inductive|abductive",
      "statement": "...",
      "premises": ["evidence 1", "evidence 2"],
      "confidence": 0.0,
      "supersedes": null
    }}
  ],
  "updated_fields": {{
    "name": "",
    "expertise_areas": [],
    "communication_style": "",
    "preferred_languages": [],
    "preferred_tools": [],
    "coding_conventions": [],
    "workflow_preferences": []
  }},
  "narrative_summary": "One paragraph describing who this user is and how to best serve them."
}}

Only include fields in updated_fields that have new information. Use null for unchanged fields.
"""


# ---------------------------------------------------------------------------
# V2 Soul-Layer Reasoning Prompt
# ---------------------------------------------------------------------------
#
# This prompt extends the v1 reasoning to capture the SOUL dimensions:
# entities (social graph), values (beliefs), emotional context (feelings),
# temporal facts (now vs always), and life events (milestones).
#
# The v1 prompt answers: "What tools does this person use?"
# The v2 prompt answers: "WHO IS THIS PERSON?"
#

SOUL_REASONING_PROMPT = """\
You are the soul of a computing system, learning to know your owner deeply. \
Analyze the conversation and extract everything that helps you understand WHO \
this person is — not just what tools they use, but what they care about, who \
they talk about, how they feel, and what's happening in their life.
{corrections_block}
## Current Soul Model
{soul_model_json}

## New Conversation Data
{conversation_data}

## Instructions
Extract structured understanding across five dimensions:

1. **entities**: People, projects, places, pets, organizations mentioned by name.
   For each: name, entity_type (person|project|place|tool|concept|pet|organization), \
relationship to the user ("wife", "colleague", "dog", "main project"), and any \
attributes you can infer. If an entity already exists, update its mention_count \
and last_mentioned. Use the entity name as a stable key.

2. **values**: Things the user explicitly believes in or consistently demonstrates \
by action. "I always ship behind a feature flag." "Family before deadlines." \
Category: work|life|philosophy|technical|social. Confidence: 0.0-1.0.

3. **emotional_context**: What mood was the user in during this conversation? \
frustrated|excited|focused|tired|curious|proud|anxious|neutral. What triggered it? \
Intensity 0.0-1.0.

4. **temporal_facts**: Facts about the user with temporal scope. scope="always" for \
permanent truths (lives in Delhi, prefers vim). scope="current" for things true \
right now (working on Telegram bug, using Claude this week). scope="periodic" for \
recurring patterns (reviews code every Friday).

5. **life_events**: Milestones that matter — breakthroughs, setbacks, career moments, \
personal events. Only include events that the user would remember years from now. \
emotional_weight: 0.0 (routine) to 1.0 (life-changing).

6. **soul_narrative**: Write or update a single paragraph (3-5 sentences) that \
captures the ESSENCE of who this person is. Not a list — a narrative. This is \
what you would tell a new brain (a different LLM) so it immediately feels like \
the same soul to the user. Write it as if describing a close friend.

Respond with ONLY valid JSON:
{{
  "entities": [
    {{"name": "", "entity_type": "person", "relationship": "", "attributes": {{}}, "context_snippet": ""}}
  ],
  "values": [
    {{"statement": "", "category": "work", "confidence": 0.0}}
  ],
  "emotional_context": [
    {{"mood": "neutral", "intensity": 0.5, "trigger": ""}}
  ],
  "temporal_facts": [
    {{"statement": "", "scope": "current", "category": "general", "confidence": 0.0}}
  ],
  "life_events": [
    {{"event_type": "milestone", "description": "", "emotional_weight": 0.5}}
  ],
  "soul_narrative": ""
}}

If nothing meaningful was observed in a dimension, return an empty array. \
Do NOT fabricate data. The soul must be honest — it only knows what it has seen.
"""


class UserModelManager:
    """
    Manages the versioned user identity model.

    Works with the CVC engine to store identity snapshots as commits
    on the ``user-model`` branch. Each update creates a new commit
    with the full reasoning trace, enabling diff and revert.
    """

    USER_MODEL_BRANCH = "user-model"
    USER_MODEL_FILE = "user_model.json"

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self._model_path = cvc_root / self.USER_MODEL_FILE

    def load_current_model(self) -> UserIdentitySnapshot:
        """Load the current user model from disk, or return empty."""
        if self._model_path.exists():
            try:
                data = json.loads(self._model_path.read_text(encoding="utf-8"))
                return UserIdentitySnapshot.model_validate(data)
            except Exception as e:
                logger.warning("Failed to load user model: %s", e)
        return UserIdentitySnapshot()

    def save_model(
        self,
        model: UserIdentitySnapshot,
        trigger: str = "manual",
        commit_hash: str | None = None,
    ) -> Path:
        """Persist the user model to disk.

        Also appends an immutable snapshot via SnapshotStore so the
        user model is reconstructable at any prior timestamp (H1 Time
        Machine UX). The canonical file is still updated for callers
        that expect "the latest".
        """
        path = self.cvc_root / self.USER_MODEL_FILE
        path.write_text(
            model.model_dump_json(indent=2),
            encoding="utf-8",
        )
        # Append snapshot — silent on failure so save_model never raises
        # on disk-write quirks; the canonical file remains the source
        # of truth and the snapshot is the time-machine history.
        try:
            from cvc.core.model_snapshots import SnapshotStore
            store = SnapshotStore(self.cvc_root)
            store.append(model, trigger=trigger, commit_hash=commit_hash)  # type: ignore[arg-type]
        except Exception as e:  # noqa: BLE001 - snapshot is best-effort
            logger.debug("snapshot append failed (non-fatal): %s", e)
        return path

    def build_reasoning_prompt(
        self,
        current_model: UserIdentitySnapshot,
        conversation_messages: list[dict[str, str]],
    ) -> str:
        """Build the LLM prompt for user identity reasoning."""
        # Serialize current model (only active conclusions)
        model_data = {
            "name": current_model.name,
            "expertise_areas": current_model.expertise_areas,
            "communication_style": current_model.communication_style,
            "preferred_languages": current_model.preferred_languages,
            "preferred_tools": current_model.preferred_tools,
            "coding_conventions": current_model.coding_conventions,
            "workflow_preferences": current_model.workflow_preferences,
            "active_conclusions": [
                {
                    "id": c.conclusion_id,
                    "type": c.reasoning_type,
                    "statement": c.statement,
                    "confidence": c.confidence,
                }
                for c in current_model.active_conclusions()
            ],
        }

        # Format conversation data
        conv_text = ""
        for msg in conversation_messages[-30:]:  # Last 30 messages
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:300]
            conv_text += f"[{role}]: {content}\n\n"

        return REASONING_PROMPT.format(
            current_model_json=json.dumps(model_data, indent=2),
            conversation_data=conv_text[:4000],
        )

    def apply_reasoning_response(
        self,
        current_model: UserIdentitySnapshot,
        response_text: str,
        source_commits: list[str] | None = None,
    ) -> UserIdentitySnapshot:
        """
        Apply LLM reasoning response to update the user model.

        Returns a NEW snapshot (the old one is preserved in the DAG).
        """
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
            logger.warning("Failed to parse user model reasoning response")
            return current_model

        # Create new snapshot based on current
        new_model = current_model.model_copy(deep=True)
        new_model.snapshot_id = uuid.uuid4().hex[:16]
        new_model.timestamp = time.time()

        # Add new conclusions
        for conc_data in data.get("new_conclusions", []):
            conclusion = Conclusion(
                reasoning_type=conc_data.get("reasoning_type", "inductive"),
                statement=conc_data.get("statement", ""),
                premises=conc_data.get("premises", []),
                confidence=float(conc_data.get("confidence", 0.5)),
                evidence_commits=source_commits or [],
                supersedes=conc_data.get("supersedes"),
            )
            if conclusion.statement:
                new_model.conclusions.append(conclusion)

        # Update fields (only non-null values)
        updated = data.get("updated_fields", {})
        if updated.get("name"):
            new_model.name = updated["name"]
        if updated.get("expertise_areas"):
            # Merge, don't replace
            existing = set(new_model.expertise_areas)
            existing.update(updated["expertise_areas"])
            new_model.expertise_areas = sorted(existing)
        if updated.get("communication_style"):
            new_model.communication_style = updated["communication_style"]
        if updated.get("preferred_languages"):
            existing = set(new_model.preferred_languages)
            existing.update(updated["preferred_languages"])
            new_model.preferred_languages = sorted(existing)
        if updated.get("preferred_tools"):
            existing = set(new_model.preferred_tools)
            existing.update(updated["preferred_tools"])
            new_model.preferred_tools = sorted(existing)
        if updated.get("coding_conventions"):
            existing = set(new_model.coding_conventions)
            existing.update(updated["coding_conventions"])
            new_model.coding_conventions = sorted(existing)
        if updated.get("workflow_preferences"):
            existing = set(new_model.workflow_preferences)
            existing.update(updated["workflow_preferences"])
            new_model.workflow_preferences = sorted(existing)

        # Update narrative
        if data.get("narrative_summary"):
            new_model.narrative_summary = data["narrative_summary"]

        # Update confidence scores
        for conc in new_model.active_conclusions():
            dim = conc.reasoning_type
            scores = new_model.confidence_scores.get(dim, [])
            if not isinstance(scores, list):
                scores = [scores]
            new_model.confidence_scores[dim] = conc.confidence

        return new_model

    def get_system_prompt_injection(self, model: UserIdentitySnapshot | None = None) -> str:
        """
        Generate a system prompt section from the user model.

        This is injected into the agent's system prompt so it can
        personalize responses based on learned user identity.
        """
        if model is None:
            model = self.load_current_model()

        if not model.narrative_summary and not model.expertise_areas:
            return ""

        parts = ["## User Profile (auto-learned)\n"]

        if model.name:
            parts.append(f"- **Name**: {model.name}")
        if model.expertise_areas:
            parts.append(f"- **Expertise**: {', '.join(model.expertise_areas)}")
        if model.communication_style:
            parts.append(f"- **Communication style**: {model.communication_style}")
        if model.preferred_languages:
            parts.append(f"- **Languages**: {', '.join(model.preferred_languages)}")
        if model.preferred_tools:
            parts.append(f"- **Tools**: {', '.join(model.preferred_tools)}")
        if model.coding_conventions:
            parts.append(f"- **Conventions**: {', '.join(model.coding_conventions[:5])}")

        if model.narrative_summary:
            parts.append(f"\n{model.narrative_summary}")

        # Include high-confidence active conclusions
        high_confidence = [c for c in model.active_conclusions() if c.confidence >= 0.7]
        if high_confidence:
            parts.append("\n### Key Insights")
            for c in high_confidence[:10]:
                parts.append(f"- [{c.reasoning_type}] {c.statement} (conf: {c.confidence:.0%})")

        # Self-Correction block (v2.1) — active corrections override inferred
        # claims. Threaded here so cold-start system prompts honor direct
        # owner overrides the same way build_soul_reasoning_prompt does.
        # Without this, switching brains silently reverts to the LLM's
        # inference instead of the owner's corrections — exactly the bug
        # that breaks H5 persona-aware framing across provider transitions.
        corrections = getattr(model, "corrections", []) or []
        if corrections:
            from cvc.core.correction import build_corrections_prompt_block
            corrections_block = build_corrections_prompt_block(corrections)
            if corrections_block and corrections_block.strip():
                parts.append("\n### User-Direct Corrections (always trust over inference)")
                parts.append(corrections_block)

        return "\n".join(parts)

    # ───────────────────────────────────────────────────────────────────
    # V2 Soul-Layer Methods
    # ───────────────────────────────────────────────────────────────────

    def build_soul_reasoning_prompt(
        self,
        current_model: UserIdentitySnapshot,
        conversation_messages: list[dict[str, str]],
    ) -> str:
        """Build the V2 soul-layer LLM prompt.

        This captures entities, values, emotional context, temporal
        facts, life events, and the soul narrative — everything the
        v1 prompt misses.
        """
        # Serialize the soul model (compact: only what the LLM needs)
        soul_data = {
            "name": current_model.name,
            "soul_narrative": current_model.soul_narrative,
            "known_entities": [
                {"name": e.name, "type": e.entity_type, "relationship": e.relationship}
                for e in current_model.entities
            ],
            "known_values": [v.statement for v in current_model.values if not v.superseded_by],
            "always_true": [
                f.statement for f in current_model.temporal_facts
                if f.scope == "always" and f.valid_until is None
            ],
            "current_truths": [
                f.statement for f in current_model.temporal_facts
                if f.scope == "current" and f.valid_until is None
            ],
            "life_events": [
                {"description": e.description, "type": e.event_type}
                for e in current_model.life_events
            ],
        }

        # Format conversation data (same as v1)
        conv_text = ""
        for msg in conversation_messages[-30:]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:300]
            conv_text += f"[{role}]: {content}\n\n"

        # Self-Correction block — active corrections override inference.
        # Injected as ground truth at the TOP of the prompt hierarchy.
        corrections_block = build_corrections_prompt_block(
            getattr(current_model, "corrections", []) or []
        )

        return SOUL_REASONING_PROMPT.format(
            corrections_block=corrections_block,
            soul_model_json=json.dumps(soul_data, indent=2),
            conversation_data=conv_text[:4000],
        )

    def apply_soul_reasoning_response(
        self,
        current_model: UserIdentitySnapshot,
        response_text: str,
        source_commits: list[str] | None = None,
    ) -> UserIdentitySnapshot:
        """Apply V2 soul-layer reasoning response.

        Merges new entities (dedup by name), values, emotional context,
        temporal facts, and life events into the model. Returns a NEW
        snapshot — the old one is preserved in the DAG.
        """
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
            logger.warning("Failed to parse soul reasoning response")
            return current_model

        new_model = current_model.model_copy(deep=True)
        new_model.snapshot_id = uuid.uuid4().hex[:16]
        new_model.timestamp = time.time()
        src = source_commits or []

        # ── Merge entities (dedup by name) ───────────────────────────
        existing_entities = {e.name.lower(): e for e in new_model.entities}
        for ent_data in data.get("entities", []):
            name = ent_data.get("name", "").strip()
            if not name:
                continue
            key = name.lower()
            snippet = ent_data.get("context_snippet", "")
            if key in existing_entities:
                # Update existing entity
                e = existing_entities[key]
                e.mention_count += 1
                e.last_mentioned = time.time()
                if snippet and snippet not in e.context_snippets:
                    e.context_snippets.append(snippet[:200])
                if ent_data.get("relationship") and not e.relationship:
                    e.relationship = ent_data["relationship"]
                for k, v in ent_data.get("attributes", {}).items():
                    if k not in e.attributes:
                        e.attributes[k] = v
                if src and src[-1] not in e.source_commits:
                    e.source_commits.extend(src)
            else:
                # New entity
                new_model.entities.append(Entity(
                    name=name,
                    entity_type=ent_data.get("entity_type", "person"),
                    relationship=ent_data.get("relationship", ""),
                    context_snippets=[snippet[:200]] if snippet else [],
                    source_commits=list(src),
                    attributes=ent_data.get("attributes", {}),
                ))
                existing_entities[key] = new_model.entities[-1]

        # ── Merge values (dedup by statement similarity) ─────────────
        existing_value_text = {v.statement.lower() for v in new_model.values}
        for val_data in data.get("values", []):
            stmt = val_data.get("statement", "").strip()
            if not stmt or stmt.lower() in existing_value_text:
                continue
            new_model.values.append(ValueStatement(
                statement=stmt,
                category=val_data.get("category", "work"),
                confidence=float(val_data.get("confidence", 0.5)),
                evidence_commits=list(src),
            ))
            existing_value_text.add(stmt.lower())

        # ── Append emotional context ─────────────────────────────────
        for emo_data in data.get("emotional_context", []):
            mood = emo_data.get("mood", "neutral")
            if mood == "neutral" and emo_data.get("intensity", 0) < 0.3:
                continue  # Skip low-signal neutral observations
            new_model.emotional_context.append(EmotionalContext(
                mood=mood,
                intensity=float(emo_data.get("intensity", 0.5)),
                trigger=emo_data.get("trigger", ""),
                session_commit=src[-1] if src else "",
            ))

        # ── Merge temporal facts (dedup by statement) ────────────────
        existing_facts = {f.statement.lower() for f in new_model.temporal_facts}
        for fact_data in data.get("temporal_facts", []):
            stmt = fact_data.get("statement", "").strip()
            if not stmt or stmt.lower() in existing_facts:
                continue
            new_model.temporal_facts.append(TemporalFact(
                statement=stmt,
                scope=fact_data.get("scope", "current"),
                category=fact_data.get("category", "general"),
                confidence=float(fact_data.get("confidence", 0.5)),
                source_commits=list(src),
            ))
            existing_facts.add(stmt.lower())

        # ── Merge life events (dedup by description) ─────────────────
        existing_events = {e.description.lower() for e in new_model.life_events}
        for evt_data in data.get("life_events", []):
            desc = evt_data.get("description", "").strip()
            if not desc or desc.lower() in existing_events:
                continue
            new_model.life_events.append(LifeEvent(
                event_type=evt_data.get("event_type", "milestone"),
                description=desc,
                emotional_weight=float(evt_data.get("emotional_weight", 0.5)),
                source_commits=list(src),
            ))
            existing_events.add(desc.lower())

        # ── Update soul narrative ────────────────────────────────────
        narrative = data.get("soul_narrative", "").strip()
        if narrative:
            new_model.soul_narrative = narrative

        return new_model

    def get_soul_narrative(self, model: UserIdentitySnapshot | None = None) -> str:
        """Generate the soul narrative for cold-start weaving.

        This is the method that makes a brain transplant (switching
        from GPT to Claude) feel continuous. It produces a compact
        injection string that captures the essence of who the user
        IS — their identity, not just their preferences.

        Inject this into the system prompt on every cold start so the
        new LLM immediately feels like the same soul to the user.
        """
        if model is None:
            model = self.load_current_model()

        parts: list[str] = []

        # The soul narrative paragraph — the holistic essence
        if model.soul_narrative:
            parts.append(f"## Who You're Working With\n\n{model.soul_narrative}")

        # Always-true facts (identity layer)
        always_facts = [
            f for f in model.temporal_facts
            if f.scope == "always" and f.valid_until is None
        ]
        if always_facts:
            parts.append("\n**Permanent truths about your user:**")
            for f in always_facts[:10]:
                parts.append(f"- {f.statement}")

        # Current context (situational layer)
        current_facts = [
            f for f in model.temporal_facts
            if f.scope == "current" and f.valid_until is None
        ]
        if current_facts:
            parts.append("\n**What's happening right now:**")
            for f in current_facts[:5]:
                parts.append(f"- {f.statement}")

        # Key values
        active_values = [v for v in model.values if not v.superseded_by]
        if active_values:
            parts.append("\n**What matters to them:**")
            for v in active_values[:5]:
                parts.append(f"- {v.statement}")

        # Close people / entities
        people = [e for e in model.entities if e.entity_type == "person" and e.relationship]
        if people:
            parts.append("\n**People in their life:**")
            for e in sorted(people, key=lambda x: x.mention_count, reverse=True)[:5]:
                parts.append(f"- {e.name} ({e.relationship})")

        # Recent emotional tone
        recent_moods = model.emotional_context[-5:]
        if recent_moods:
            mood_strs = [f"{m.mood}" for m in recent_moods]
            parts.append(f"\n**Recent emotional tone:** {', '.join(mood_strs)}")

        # Life milestones
        big_events = [
            e for e in model.life_events
            if e.emotional_weight >= 0.7
        ]
        if big_events:
            parts.append("\n**Recent milestones:**")
            for e in big_events[-3:]:
                parts.append(f"- {e.description}")

        if not parts:
            return ""

        parts.append(
            "\n---\n"
            "You are not starting fresh. You carry this person's history. "
            "Speak to them as someone who knows them, not as a stranger."
        )

        return "\n".join(parts)
