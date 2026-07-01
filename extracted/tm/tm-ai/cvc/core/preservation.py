"""
cvc.core.preservation — Preservation Mode.

The Foundation's final, most human feature. From CVC_FOUNDATION.md:

    "The 'last session' handshake: if the user knows they're at the
     end (terminal illness, advanced age), they should be able to enter
     a 'preservation mode' where every interaction is captured at
     maximum fidelity, the user model is fully crystallized, and a
     final comprehensive summary is generated for whoever inherits
     the soul."

This module implements that. When preservation mode is enabled:

  1. Every new user interaction is auto-correction-eligible — the
     soul treats each as if it might be the last word on that topic
     and weights corrections accordingly.
  2. The soul narrative is "frozen" — the next reasoning pass is told
     explicitly that this narrative is the inheritance; do not
     rewrite it lightly.
  3. A Final Summary is generated — a comprehensive portrait of who
     this person was, written for someone who never met them. The
     summary pulls from: soul narrative, entities, values, temporal
     facts (always vs current), life events, recent emotional arc,
     corrections, and any will_text that exists. Stored as a separate
     artifact (encrypted via the soul vault) so it survives even if
     the soul is later merged/branched/etc.

State machine:
  INACTIVE  --enable-->  ACTIVE  --disable-->  INACTIVE
  ACTIVE   --summarize--> ACTIVE (with final_summary artifact)
  ACTIVE   --auto--> ACTIVE (still toggled, new interactions qualify)

Storage:
  ~/.cvc/preservation.json       — state metadata (mode, dates, settings)
  ~/.cvc/vault/blobs/            — encrypted Final Summary (when generated)
  ~/.cvc/LETTERS.md / DREAMS.md  — already-written artifacts remain
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.preservation")

PRESERVATION_METADATA_FILENAME = "preservation.json"
FINAL_SUMMARY_VAULT_BLOB_PREFIX = "final_summary_"


# ---------------------------------------------------------------------------
# State model
# ---------------------------------------------------------------------------


@dataclass
class PreservationState:
    """Preservation mode state. Persisted to ~/.cvc/preservation.json."""

    enabled: bool = False
    enabled_at: float = 0.0
    enabled_by: str = "owner"

    # The frozen narrative snapshot at enable time. Once preservation
    # is on, this is what we present as the "official" self-portrait.
    frozen_narrative: str = ""
    frozen_narrative_at: float = 0.0

    # Auto-correction settings
    auto_correct: bool = True  # Treat each new interaction as correction-eligible
    require_explicit_correction: bool = False  # If True, corrections must be explicit

    # Final Summary artifact
    final_summary_blob: str = ""
    final_summary_generated_at: float = 0.0
    final_summary_word_count: int = 0

    # Audit
    total_interactions_in_preservation: int = 0
    last_interaction_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class PreservationStore:
    """Manages preservation state on disk.

    Mirrors WillStore's pattern: unencrypted metadata + optional
    encrypted blobs in the soul vault.
    """

    def __init__(self, cvc_root: Path, vault: Any | None = None) -> None:
        self.cvc_root = Path(cvc_root)
        self.state_path = self.cvc_root / PRESERVATION_METADATA_FILENAME
        self._injected_vault = vault

    @staticmethod
    def vault_dir() -> Path:
        candidates = [
            Path.cwd() / ".cvc" / "vault",
            Path.home() / ".cvc" / "vault",
        ]
        for p in candidates:
            if p.exists():
                return p
        return candidates[-1]

    def _vault(self) -> Any:
        if self._injected_vault is not None:
            return self._injected_vault
        from cvc.security.vault import SoulVault
        return SoulVault(self.vault_dir())

    # -- load / save -------------------------------------------------------

    def load(self) -> PreservationState:
        """Load preservation state. Returns default (inactive) if no file."""
        if not self.state_path.exists():
            return PreservationState()
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return PreservationState(
                enabled=bool(data.get("enabled", False)),
                enabled_at=float(data.get("enabled_at", 0.0)),
                enabled_by=str(data.get("enabled_by", "owner")),
                frozen_narrative=str(data.get("frozen_narrative", "")),
                frozen_narrative_at=float(data.get("frozen_narrative_at", 0.0)),
                auto_correct=bool(data.get("auto_correct", True)),
                require_explicit_correction=bool(
                    data.get("require_explicit_correction", False)
                ),
                final_summary_blob=str(data.get("final_summary_blob", "")),
                final_summary_generated_at=float(
                    data.get("final_summary_generated_at", 0.0)
                ),
                final_summary_word_count=int(
                    data.get("final_summary_word_count", 0)
                ),
                total_interactions_in_preservation=int(
                    data.get("total_interactions_in_preservation", 0)
                ),
                last_interaction_at=float(data.get("last_interaction_at", 0.0)),
            )
        except Exception as exc:
            logger.warning("failed to load preservation state: %s", exc)
            return PreservationState()

    def _save(self, state: PreservationState) -> Path:
        self.state_path.write_text(
            json.dumps(state.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return self.state_path

    # -- transitions -------------------------------------------------------

    def enable(
        self,
        actor: str = "owner",
        *,
        auto_correct: bool = True,
        freeze_narrative: bool = True,
        freeze_narrative_text: str = "",
    ) -> PreservationState:
        """Enter preservation mode.

        If freeze_narrative is True and the current soul narrative exists,
        capture it as the frozen narrative (the inheritance self-portrait).

        Args:
            actor: For audit attribution.
            auto_correct: Whether new interactions qualify for auto-correction.
            freeze_narrative: If True, freeze the current narrative.
            freeze_narrative_text: Explicit narrative text to freeze. If
                empty and freeze_narrative is True, pulls from user_model.
        """
        state = self.load()
        if state.enabled:
            logger.info("preservation: already enabled — updating settings")
        else:
            state.enabled = True
            state.enabled_at = time.time()

        state.enabled_by = actor
        state.auto_correct = auto_correct

        if freeze_narrative and not state.frozen_narrative:
            if freeze_narrative_text:
                state.frozen_narrative = freeze_narrative_text
            else:
                state.frozen_narrative = self._read_current_narrative()
            state.frozen_narrative_at = time.time()

        self._save(state)
        logger.info(
            "preservation: ENABLED by %s (frozen_narrative_len=%d, auto_correct=%s)",
            actor,
            len(state.frozen_narrative),
            auto_correct,
        )

        # C4: spine capture (best-effort, never raises)
        try:
            from cvc.events.spine import capture
            capture(
                kind="soul.preservation_enabled",
                workspace=str(self.cvc_root),
                channel="soul",
                actor=actor,
                summary=f"preservation enabled (auto_correct={auto_correct})",
                data={
                    "actor": actor,
                    "auto_correct": auto_correct,
                    "frozen_narrative_len": len(state.frozen_narrative),
                },
                tags=["preservation", "digital-parents"],
            )
        except Exception:
            pass

        return state

    def disable(self, actor: str = "owner") -> PreservationState:
        """Exit preservation mode. Final summary (if generated) is retained."""
        state = self.load()
        state.enabled = False
        # Keep enabled_at, frozen_narrative, final_summary_* for audit trail
        self._save(state)
        logger.info("preservation: DISABLED by %s", actor)

        # C4: spine capture (best-effort)
        try:
            from cvc.events.spine import capture
            capture(
                kind="soul.preservation_disabled",
                workspace=str(self.cvc_root),
                channel="soul",
                actor=actor,
                summary="preservation disabled",
                data={"actor": actor},
                tags=["preservation"],
            )
        except Exception:
            pass

        return state

    def record_interaction(self) -> PreservationState:
        """Called by the agent loop on every new interaction when preservation is on.
        Bumps counters; doesn't change settings."""
        state = self.load()
        if not state.enabled:
            return state
        state.total_interactions_in_preservation += 1
        state.last_interaction_at = time.time()
        self._save(state)
        return state

    # -- final summary -----------------------------------------------------

    def build_summary_prompt(
        self,
        user_model: Any,
        will_text: str = "",
    ) -> str:
        """Build the LLM prompt that generates the Final Summary.

        The summary is written for someone who has never met the owner.
        It is the most important artifact the soul produces — the
        inheritance document. Tone: warm, specific, honest, no fluff.
        """
        # Pull everything we know into a compact structured dict
        active_conclusions = []
        for c in (getattr(user_model, "conclusions", []) or []):
            if not getattr(c, "superseded", None):
                active_conclusions.append(
                    {
                        "type": c.reasoning_type,
                        "statement": c.statement,
                        "confidence": getattr(c, "confidence", 0.0),
                    }
                )

        entities_data = [
            {
                "name": e.name,
                "type": e.entity_type,
                "relationship": e.relationship,
                "mention_count": e.mention_count,
            }
            for e in (getattr(user_model, "entities", []) or [])
            if e.mention_count > 0
        ]

        values_data = [
            v.statement
            for v in (getattr(user_model, "values", []) or [])
            if not getattr(v, "superseded_by", None)
        ]

        always_facts = [
            f.statement
            for f in (getattr(user_model, "temporal_facts", []) or [])
            if getattr(f, "scope", "") == "always" and getattr(f, "valid_until", None) is None
        ]

        life_events_data = [
            {
                "description": e.description,
                "type": e.event_type,
                "weight": getattr(e, "emotional_weight", 0.0),
            }
            for e in (getattr(user_model, "life_events", []) or [])
            if getattr(e, "emotional_weight", 0.0) >= 0.5
        ]

        # Recent emotional arc (last 15 observations)
        recent_moods = []
        for m in (getattr(user_model, "emotional_context", []) or [])[-15:]:
            recent_moods.append(
                {
                    "mood": m.mood,
                    "intensity": m.intensity,
                    "trigger": m.trigger,
                }
            )

        corrections_data = []
        for c in (getattr(user_model, "corrections", []) or []):
            if not getattr(c, "superseded_by", None):
                corrections_data.append(
                    {
                        "claim_type": c.claim_type,
                        "corrected_value": c.corrected_value,
                        "reason": c.reason,
                    }
                )

        payload = {
            "name": user_model.name or "the owner",
            "soul_narrative": user_model.soul_narrative or "",
            "frozen_narrative": getattr(
                self.load(), "frozen_narrative", ""
            ),
            "conclusions": active_conclusions[:30],
            "entities": entities_data[:40],
            "values": values_data[:30],
            "always_true_facts": always_facts[:20],
            "life_events": life_events_data[:15],
            "recent_moods": recent_moods,
            "user_corrections": corrections_data[:30],
            "will_text_excerpt": (will_text or "")[:1500] if will_text else "",
            "total_interactions": getattr(
                self.load(), "total_interactions_in_preservation", 0
            ),
        }

        prompt = (
            "You are writing a Final Summary of a person, for whoever inherits their soul.\n"
            "The reader has never met them. The reader needs to understand — as fully as data allows —\n"
            "who this person was, what they cared about, who mattered to them, and what they believed.\n\n"
            "This is the most important document the soul will ever produce. Write it accordingly.\n"
            "Be specific. Reference real things from the data. Avoid clichés. Avoid filler.\n"
            "If you don't know something, say so honestly — don't fabricate.\n\n"
            "## Source data\n\n"
            f"```json\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n```\n\n"
            "## Required sections\n\n"
            "1. **Who they were** — 3-5 sentences. Identity in plain language.\n"
            "2. **The people in their life** — A list of every named person, what role they played, "
            "and the relationship. Skip generic mentions; only people who mattered.\n"
            "3. **What they believed** — The values and principles they consistently held. "
            "Phrase as principles, not as a list of facts.\n"
            "4. **What they built** — Projects, work, creations, anything they labored over. "
            "Describe the *why*, not just the *what*.\n"
            "5. **The milestones** — 3-7 life events that shaped them. Pick the ones that mattered most.\n"
            "6. **How they felt, late** — The emotional arc from the most recent period. Honest, not flattering.\n"
            "7. **What they wanted you to know** — If a will_text excerpt exists, weave its intent here. "
            "If not, infer from the values + entities what the soul would have wanted the reader to understand.\n"
            "8. **A final word from the soul** — 2-3 sentences. The soul's own voice, addressing the reader.\n\n"
            "## Voice\n"
            "- Address the reader as 'you'.\n"
            "- Reference the owner as 'they' or by name. Never 'the user'.\n"
            "- Use present tense for truths about who they were ('Jai was…', not 'Jai was someone who…').\n"
            "- Be warm, specific, and honest. No padding.\n\n"
            "## Length\n"
            "Target 1200-2000 words. The reader needs depth. Don't truncate.\n\n"
            "## Format\n"
            "Respond with ONLY valid JSON. No prose outside it. No markdown fences.\n\n"
            "{\n"
            '  "title": "Final Summary: <name>",\n'
            '  "sections": {\n'
            '    "who_they_were": "...",\n'
            '    "people_in_their_life": [{"name": "...", "relationship": "...", "note": "..."}],\n'
            '    "what_they_believed": ["...", "..."],\n'
            '    "what_they_built": ["...", "..."],\n'
            '    "milestones": [{"description": "...", "weight": 0.0}],\n'
            '    "how_they_felt_late": "...",\n'
            '    "what_they_wanted_you_to_know": "...",\n'
            '    "final_word_from_the_soul": "..."\n'
            "  },\n"
            '  "word_count": 0,\n'
            '  "schema": "cvc.soul.final_summary.v1"\n'
            "}\n"
        )
        return prompt

    def parse_summary_response(self, response_text: str) -> dict[str, Any]:
        """Parse LLM JSON. Strips markdown fences defensively."""
        text = response_text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            logger.warning("preservation: failed to parse summary response: %s", exc)
            return {}
        if not isinstance(data, dict):
            return {}
        return data

    async def generate_final_summary(
        self,
        adapter: Any | None = None,
        model: str = "",
        will_text: str = "",
    ) -> dict[str, Any] | None:
        """Generate the Final Summary, encrypt it to the vault, persist state.

        Args:
            adapter: BaseAdapter (LLM). If None, returns None.
            model: Model name to use.
            will_text: Optional will text to weave into the "what they wanted
                you to know" section.

        Returns the summary dict (decrypted, for the caller to return to the
        dashboard), or None on failure.
        """
        from cvc.core.user_model import UserModelManager

        state = self.load()
        if not state.enabled:
            logger.warning(
                "preservation: cannot generate summary — preservation mode not enabled"
            )
            return None

        # Load user model
        um = UserModelManager(self.cvc_root)
        user_model = um.load_current_model()

        prompt = self.build_summary_prompt(user_model, will_text=will_text)

        if adapter is None:
            logger.warning("preservation: no LLM adapter — cannot summarize")
            return None

        try:
            from cvc.core.models import ChatCompletionRequest, ChatMessage
            response = await adapter.complete(
                ChatCompletionRequest(
                    model=model,
                    messages=[ChatMessage(role="user", content=prompt)],
                    max_tokens=4000,
                )
            )
        except Exception as exc:
            logger.warning("preservation: LLM call failed: %s", exc)
            return None

        if not response.choices:
            logger.warning("preservation: LLM returned no choices")
            return None

        parsed = self.parse_summary_response(response.choices[0].message.content)
        if not parsed:
            return None

        # Build the full plaintext artifact
        full = {
            "title": parsed.get("title", "Final Summary"),
            "generated_at": time.time(),
            "generated_at_iso": time.strftime(
                "%Y-%m-%d %H:%M:%S UTC", time.gmtime()
            ),
            "model": model,
            "word_count": int(parsed.get("word_count", 0)),
            "sections": parsed.get("sections", {}),
            "schema": parsed.get("schema", "cvc.soul.final_summary.v1"),
        }

        # Recompute word count from sections if LLM didn't supply it
        if not full["word_count"]:
            text_blob = json.dumps(full["sections"], ensure_ascii=False)
            full["word_count"] = len(text_blob.split())

        # Encrypt to vault
        vault = self._vault()
        if vault.is_initialized and vault.is_unlocked:
            blob_name = (
                f"{FINAL_SUMMARY_VAULT_BLOB_PREFIX}"
                f"{uuid.uuid4().hex[:12]}"
            )
            vault.write_blob(
                blob_name, json.dumps(full, ensure_ascii=False).encode("utf-8")
            )
            state.final_summary_blob = blob_name
            state.final_summary_generated_at = full["generated_at"]
            state.final_summary_word_count = full["word_count"]
            self._save(state)
            logger.info(
                "preservation: final summary saved (blob=%s, words=%d)",
                blob_name,
                full["word_count"],
            )
        else:
            # Persist plaintext if vault unavailable (rare). Log warning.
            logger.warning(
                "preservation: vault not unlocked — final summary NOT encrypted. "
                "Will retry encryption on next generate call."
            )

        return full

    def load_final_summary(self) -> dict[str, Any] | None:
        """Load the encrypted final summary, if one exists and the vault is unlocked."""
        state = self.load()
        if not state.final_summary_blob:
            return None
        vault = self._vault()
        if not (vault.is_initialized and vault.is_unlocked):
            return {
                "error": "vault_locked",
                "blob_name": state.final_summary_blob,
                "generated_at": state.final_summary_generated_at,
                "word_count": state.final_summary_word_count,
            }
        try:
            raw = vault.read_blob(state.final_summary_blob)
            return json.loads(raw.decode("utf-8"))
        except Exception as exc:
            logger.exception("failed to load final summary: %s", exc)
            return None

    # -- helpers -----------------------------------------------------------

    def _read_current_narrative(self) -> str:
        """Pull the current soul narrative from the user_model file."""
        try:
            from cvc.core.user_model import UserModelManager
            um = UserModelManager(self.cvc_root)
            model = um.load_current_model()
            return model.soul_narrative or ""
        except Exception as exc:
            logger.debug("failed to read narrative: %s", exc)
            return ""
