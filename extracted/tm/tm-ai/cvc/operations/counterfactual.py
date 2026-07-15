"""
cvc.operations.counterfactual — The Counterfactual Self-Test Loop (Fable5 Phase 4).

The single most important accuracy mechanism for AGI-grade preservation
(FABLE5 directive §3.1): the soul periodically generates a NOVEL
hypothetical the owner never faced, predicts their answer from the world
model, and surfaces the prediction for correction.

Every correction is gold-standard training signal — weighted far above
passive observation, because it is the owner directly grading the soul's
generating-function accuracy.

Flow (piggybacks on the dream-cycle cadence):

  1. PROBE GENERATION — pick a target: either an unresolved
     UncertaintyFlag from the world model (preferred — probe where we
     KNOW we're weak) or a random value/style extrapolation.
  2. PREDICTION — the soul predicts the owner's response using the
     world-model injection + soul narrative. Prediction persisted BEFORE
     the owner sees it (append-only honesty: no post-hoc editing).
  3. SURFACING — probe queued to ``.cvc/probes/pending/``; the dashboard
     or chat surfaces at most one per session ("I think you'd say X here
     — is that right?").
  4. GRADING — owner confirms / corrects / skips. Result recorded, flag
     resolved on confirm, CorrectionRecord created on correct.
  5. SCORING — rolling calibration score = the soul's measurable
     world-model accuracy over time. THE metric for AGI-grade
     preservation progress.

Invariants: local-first (.cvc/probes/), append-only (probes and grades
never edited after write), provider-agnostic.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger("cvc.counterfactual")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CounterfactualProbe(BaseModel):
    """One self-test: a novel situation + the soul's prediction."""

    probe_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float = Field(default_factory=time.time)

    # What we're testing
    target_kind: str = "uncertainty_flag"  # uncertainty_flag | value_extrapolation | style_extrapolation
    target_id: str = ""  # flag_id / value_id when applicable
    scenario: str = ""  # the novel hypothetical, phrased to the owner

    # The soul's committed prediction (written BEFORE owner sees it)
    prediction: str = ""
    prediction_reasoning: str = ""
    confidence: float = 0.5

    # Grading
    status: str = "pending"  # pending | confirmed | corrected | skipped
    owner_response: str = ""
    graded_at: float | None = None


class CalibrationRecord(BaseModel):
    """Rolling accuracy ledger — the AGI-grade preservation metric."""

    total_probes: int = 0
    confirmed: int = 0
    corrected: int = 0
    skipped: int = 0
    # Brier-style: sum of (confidence - outcome)^2, lower = better calibrated
    brier_sum: float = 0.0

    @property
    def accuracy(self) -> float:
        graded = self.confirmed + self.corrected
        return (self.confirmed / graded) if graded else 0.0

    @property
    def brier_score(self) -> float:
        graded = self.confirmed + self.corrected
        return (self.brier_sum / graded) if graded else 0.0


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

PROBE_GENERATION_PROMPT = """\
You are the self-testing engine of a digital soul. Generate ONE novel \
hypothetical situation to test whether the soul truly understands its \
owner — a situation the owner has NEVER actually faced (check the \
evidence: do not restate a past event).

## Soul narrative
{soul_narrative}

## World model (values hierarchy + reasoning style)
{world_model_block}

## Weak spot to probe (prefer this)
{probe_target}

## Rules
- The scenario must be NOVEL but PLAUSIBLE for this specific owner's life.
- It must force the weak spot: if two values have never collided, build
  the collision. If a style axis is uncertain, build a decision that
  reveals it.
- Keep it short (2-4 sentences), second person, concrete.
- Then PREDICT the owner's response, with reasoning, and an honest
  confidence (0-1). Do not inflate confidence on weak evidence.

Respond with ONLY valid JSON:
{{
  "scenario": "...",
  "prediction": "...",
  "prediction_reasoning": "...",
  "confidence": 0.0
}}
"""


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class CounterfactualEngine:
    """Generates, persists, surfaces, and grades counterfactual probes."""

    PROBES_DIR = "probes"

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = Path(cvc_root)
        self.probes_root = self.cvc_root / self.PROBES_DIR
        self.pending_dir = self.probes_root / "pending"
        self.graded_dir = self.probes_root / "graded"
        self.calibration_path = self.probes_root / "calibration.json"
        for d in (self.pending_dir, self.graded_dir):
            d.mkdir(parents=True, exist_ok=True)

    # -- generation -----------------------------------------------------------

    def build_probe_prompt(
        self,
        soul_narrative: str,
        world_model_block: str,
        probe_target: str,
    ) -> str:
        return PROBE_GENERATION_PROMPT.format(
            soul_narrative=soul_narrative[:4000] or "(no narrative yet)",
            world_model_block=world_model_block[:4000] or "(no world model yet)",
            probe_target=probe_target or "(no specific weak spot — extrapolate a value collision)",
        )

    @staticmethod
    def _extract_json(text: str) -> dict[str, Any] | None:
        text = text.strip()
        if text.startswith("```"):
            lines = [l for l in text.splitlines() if not l.strip().startswith("```")]
            text = "\n".join(lines)
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            return None
        try:
            return json.loads(text[start : end + 1], strict=False)
        except Exception:  # noqa: BLE001
            return None

    def parse_probe_response(
        self,
        response_text: str,
        target_kind: str = "uncertainty_flag",
        target_id: str = "",
    ) -> CounterfactualProbe | None:
        data = self._extract_json(response_text)
        if not data or not data.get("scenario") or not data.get("prediction"):
            logger.warning("counterfactual: probe response unparseable")
            return None
        try:
            conf = max(0.0, min(1.0, float(data.get("confidence", 0.5))))
        except Exception:  # noqa: BLE001
            conf = 0.5
        return CounterfactualProbe(
            target_kind=target_kind,
            target_id=target_id,
            scenario=str(data["scenario"]),
            prediction=str(data["prediction"]),
            prediction_reasoning=str(data.get("prediction_reasoning", "")),
            confidence=conf,
        )

    # -- persistence (append-only) ---------------------------------------------

    def persist_probe(self, probe: CounterfactualProbe) -> Path:
        """Write the probe BEFORE the owner sees it — committed prediction."""
        path = self.pending_dir / f"{probe.probe_id}.json"
        path.write_text(probe.model_dump_json(indent=2), encoding="utf-8")
        logger.info("counterfactual: probe %s persisted (pending)", probe.probe_id)
        return path

    def list_pending(self, limit: int = 10) -> list[CounterfactualProbe]:
        probes: list[CounterfactualProbe] = []
        for p in sorted(self.pending_dir.glob("*.json")):
            try:
                probes.append(
                    CounterfactualProbe.model_validate_json(p.read_text(encoding="utf-8"))
                )
            except Exception:  # noqa: BLE001
                continue
            if len(probes) >= limit:
                break
        return probes

    def next_probe_for_surfacing(self) -> CounterfactualProbe | None:
        """At most one probe per session — never spam the owner."""
        pending = self.list_pending(limit=1)
        return pending[0] if pending else None

    # -- grading ----------------------------------------------------------------

    def grade_probe(
        self,
        probe_id: str,
        status: str,
        owner_response: str = "",
    ) -> CounterfactualProbe | None:
        """Record the owner's grade. status: confirmed | corrected | skipped."""
        if status not in {"confirmed", "corrected", "skipped"}:
            raise ValueError(f"invalid grade status: {status}")

        src = self.pending_dir / f"{probe_id}.json"
        if not src.exists():
            logger.warning("counterfactual: probe %s not found in pending", probe_id)
            return None

        try:
            probe = CounterfactualProbe.model_validate_json(src.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            logger.warning("counterfactual: probe %s unreadable: %s", probe_id, e)
            return None

        probe.status = status
        probe.owner_response = owner_response
        probe.graded_at = time.time()

        # Append-only: graded copy written to graded/, pending copy removed
        # (the graded file preserves the full record including the original
        # prediction — nothing is lost, just moved through the lifecycle).
        dst = self.graded_dir / f"{probe.probe_id}.json"
        dst.write_text(probe.model_dump_json(indent=2), encoding="utf-8")
        src.unlink(missing_ok=True)

        # Update calibration ledger
        if status in {"confirmed", "corrected"}:
            cal = self.load_calibration()
            cal.total_probes += 1
            outcome = 1.0 if status == "confirmed" else 0.0
            if status == "confirmed":
                cal.confirmed += 1
            else:
                cal.corrected += 1
            cal.brier_sum += (probe.confidence - outcome) ** 2
            self._save_calibration(cal)
        elif status == "skipped":
            cal = self.load_calibration()
            cal.total_probes += 1
            cal.skipped += 1
            self._save_calibration(cal)

        logger.info("counterfactual: probe %s graded %s", probe_id, status)
        return probe

    # -- calibration --------------------------------------------------------------

    def load_calibration(self) -> CalibrationRecord:
        if self.calibration_path.exists():
            try:
                return CalibrationRecord.model_validate_json(
                    self.calibration_path.read_text(encoding="utf-8")
                )
            except Exception:  # noqa: BLE001
                pass
        return CalibrationRecord()

    def _save_calibration(self, cal: CalibrationRecord) -> None:
        self.calibration_path.write_text(cal.model_dump_json(indent=2), encoding="utf-8")

    def calibration_summary(self) -> str:
        cal = self.load_calibration()
        graded = cal.confirmed + cal.corrected
        if not graded:
            return "No graded probes yet — world-model accuracy unmeasured."
        return (
            f"World-model calibration: {cal.accuracy:.0%} accurate over "
            f"{graded} graded probes (Brier {cal.brier_score:.3f}, "
            f"{cal.skipped} skipped)."
        )


# ---------------------------------------------------------------------------
# Dream-cycle integration hook
# ---------------------------------------------------------------------------


async def run_counterfactual_cycle(
    cvc_root: Path,
    adapter: Any,
    model: str,
    soul_narrative: str = "",
    max_pending: int = 3,
) -> CounterfactualProbe | None:
    """Generate one probe if the pending queue has room.

    Called from the dream cycle (cognitive_hooks.trigger_dreaming) so the
    soul self-tests at the same cadence it dreams. Returns the new probe
    or None.
    """
    engine = CounterfactualEngine(cvc_root)

    if len(engine.list_pending(limit=max_pending)) >= max_pending:
        logger.info("counterfactual: pending queue full — skipping generation")
        return None

    if adapter is None:
        return None

    # Prefer probing a known weak spot
    probe_target = ""
    target_kind, target_id = "value_extrapolation", ""
    try:
        from cvc.core.world_model import WorldModelManager

        wm = WorldModelManager(cvc_root)
        flags = wm.get_probe_targets(limit=1)
        if flags:
            probe_target = flags[0].description
            target_kind, target_id = "uncertainty_flag", flags[0].flag_id
        world_block = wm.get_world_model_injection()
    except Exception as e:  # noqa: BLE001
        logger.debug("counterfactual: world model unavailable: %s", e)
        world_block = ""

    prompt = engine.build_probe_prompt(soul_narrative, world_block, probe_target)

    try:
        from cvc.core.models import ChatCompletionRequest, ChatMessage

        response = await adapter.complete(
            ChatCompletionRequest(
                model=model,
                messages=[ChatMessage(role="user", content=prompt)],
                max_tokens=800,
            )
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("counterfactual: LLM call failed: %s", e)
        return None

    if not response.choices:
        return None

    probe = engine.parse_probe_response(
        response.choices[0].message.content,
        target_kind=target_kind,
        target_id=target_id,
    )
    if probe is None:
        return None

    engine.persist_probe(probe)
    return probe
