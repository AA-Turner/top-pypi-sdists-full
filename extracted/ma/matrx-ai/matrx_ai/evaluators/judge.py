"""The Judge primitive — a declared contract, two modes, one accuracy ledger.

Why this exists
---------------
Engram VISION §3.3 makes a Judge a **first-class specialist**: a cheap, narrow
agent whose only job is one semantic assessment, "with its own contract and its
own Hindsight accuracy tracking." §3.6 makes the Selector its sibling. Before
this module the platform had three independent judges — :class:`AIJudge` (the
strict-JSON test evaluator), Hindsight's mandated replay judge, and Growth Loop's
per-stage quality Mandates — each with its own verdict vocabulary, its own prompt
shape, and NO accuracy record at all. Nobody could answer "is this judge any
good?", which is the only question that makes a judge worth trusting.

The contract
------------
A :class:`JudgeContract` declares, up front and in one place:

* **who** it is — ``key`` + ``version`` (the accuracy-ledger identity),
* **the question** it answers, in plain language,
* **the input shape** it expects — ``subject_kind`` plus the fields of
  :class:`JudgeSubject`,
* **the verdict schema** — the exact allowed verdict values,
* **the rubric**, when it has one, with its H/V/A provenance and its author.

Two modes, and the asymmetry is deliberate (D-14, research #7)
--------------------------------------------------------------
* ``comparative`` — rank a subject against a **reference** (the original output,
  a human correction, a champion arm). Preferred WHENEVER a reference exists:
  "which of these is better" is a measurably easier task than "how good is this."
* ``rubric`` — absolute assessment, allowed **only with a named rubric**. A
  contract in rubric mode with no ``rubric_name``/``rubric`` is refused at
  construction, not at call time. This is the line that stops "score it 0-100"
  from creeping back in as an unnamed vibe.

Both modes run on :class:`AIJudge`'s funnel — the same
``llm_messages_to_pydantic`` strict-JSON path, so routing, retries, usage and
durable cost capture are identical to product calls. A judge is a platform agent
under the hood: declare ``mandate`` and a :class:`NamedAgent` class and the
judge runs as that DB-managed, user-swappable agent instead (the Hindsight
replay judge is exactly this); declare neither and it runs on the funnel with
``model``.

The guardrail — D-15, and it is structural
------------------------------------------
**The judged agent never authors and never sees its judge's rubric.** Rubrics
live on the judge contract, nowhere else. Three layers enforce it, each
sufficient alone and each loud when it fires:

1. ``rubric_author_ref`` may not equal the subject being judged
   (:meth:`JudgeContract.assert_not_self_authored`) — refused before any paid call.
2. The rubric text may not appear in the subject or reference content
   (:func:`_assert_rubric_isolation`) — catches a caller that helpfully "gave the
   agent its grading criteria," which is the realistic way this rule dies.
3. Every ledger row records ``rubric_fingerprint`` + ``rubric_provenance`` +
   ``rubric_author``, so a violation that somehow lands is visible afterwards.

Anti-patterns
-------------
* Asking a judge for a 0-100 number. Verdicts are enumerated; nuance rides
  ``confidence``.
* Grading absolutely when a reference exists. Use ``compare``.
* Writing a judge that scores its own author's work.
* Bumping a rubric without bumping ``version`` — that silently merges two
  different judges into one accuracy record.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_ai.evaluators.ai_judge import JudgeError, _format_output
from matrx_ai.graph_nodes._strict_json import StrictJsonError, llm_messages_to_pydantic
from matrx_ai.providers.keys import resolve_api_key

logger = logging.getLogger("matrx_ai.evaluators.judge")

DEFAULT_JUDGE_MODEL = "claude-opus-4-5-20250929"

#: The default comparative vocabulary. A contract may narrow or rename it, but
#: the values are always an enumeration — never a scale.
COMPARATIVE_VERDICTS: tuple[str, ...] = ("better", "same", "worse", "regressed")
RUBRIC_VERDICTS: tuple[str, ...] = ("pass", "fail")

JudgeMode = Literal["comparative", "rubric"]
Provenance = Literal["H", "V", "A"]
AuthorityKind = Literal["human_feedback", "replay_outcome", "gate_result"]


class JudgeContractError(Exception):
    """The contract is invalid, or running it would violate D-15."""


class EntityRef(BaseModel):
    """A pointer at something in the platform. ``ref_id`` is optional because
    plenty of judged artifacts (a turn's answer text) have no row of their own."""

    model_config = ConfigDict(extra="forbid")

    ref_type: str | None = None
    ref_id: str | None = None


class JudgeSubject(BaseModel):
    """One thing to judge. ``content`` is what the judge reads; ``ref`` is how
    the ledger points back at it; ``metrics`` are measured facts (cost, tokens,
    latency) the judge may weigh but never has to take on faith."""

    model_config = ConfigDict(extra="forbid")

    label: str = Field(default="", description="Short human label, e.g. 'candidate' / 'original'.")
    content: Any = None
    ref: EntityRef = Field(default_factory=EntityRef)
    metrics: dict[str, Any] = Field(default_factory=dict)


class JudgeInputs(BaseModel):
    """The GRANULAR input shape every Judge-harness mandated agent receives.

    One field per value the harness has in scope — the contract's question,
    rubric and verdict vocabulary, the subject, the optional reference, and
    the caller's context — each delivered as its own named variable. Dicts and
    lists ride RAW (``metrics`` / ``context`` / ``verdict_values``): the prompt
    door (``to_template_value`` / ``prompt_safe_value``) canonicalizes them at
    substitution, so the harness never ``json.dumps`` anything itself.

    History: until 2026-08-22 the harness fused all of this into ONE
    ``payload_json`` blob variable (the census row in
    ``aidream/docs/mandates/INPUT_CHANNEL_VIOLATIONS.md`` § Patterns #4). A
    judge agent that rides the harness declares exactly these names in its
    ``variable_definitions`` and renders them as named sections in its user
    message; a host ``NamedAgent`` sets ``Inputs = JudgeInputs`` (or a subclass
    that adds nothing the harness does not send).
    """

    model_config = ConfigDict(extra="forbid")

    question: str
    rubric_name: str | None = None
    rubric: str | None = None
    verdict_values: list[str]
    subject_label: str | None = None
    subject_content: str
    subject_metrics: dict[str, Any] | None = None
    reference_label: str | None = None
    reference_content: str | None = None
    reference_metrics: dict[str, Any] | None = None
    context: dict[str, Any] | None = None


class JudgeContract(BaseModel):
    """The declared contract of one judge. Immutable; a change means a new
    ``version`` (see the module docstring)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    key: str = Field(min_length=1, description="Stable judge id, e.g. 'hindsight.replay_judge'.")
    version: int = Field(default=1, ge=1)
    question: str = Field(
        min_length=1,
        description="What this judge decides, in one plain-language sentence.",
    )
    mode: JudgeMode
    subject_kind: str = Field(
        min_length=1,
        description="The CLASS of thing judged — the per-class axis of accuracy tracking.",
    )
    verdict_values: tuple[str, ...] = Field(default=COMPARATIVE_VERDICTS)

    # ── The rubric. Rubric mode REQUIRES it; comparative mode may carry one as
    # ranking guidance. Either way it lives HERE and only here (D-15).
    rubric_name: str | None = None
    rubric: str | None = None
    rubric_provenance: Provenance = "A"
    rubric_author: str | None = Field(
        default=None,
        description="Who wrote the rubric — an email for H/V, an agent key for A.",
    )
    rubric_author_ref: EntityRef = Field(
        default_factory=EntityRef,
        description="The authoring entity, when it is one we can compare against the subject.",
    )

    # ── How it runs. A Mandate wins over the funnel when both are set.
    mandate: str | None = None
    model: str = DEFAULT_JUDGE_MODEL
    web_access: bool = False
    max_tokens: int = 4096
    consumer: str = Field(default="unknown", description="Which feature invoked it.")

    @model_validator(mode="after")
    def _check(self) -> JudgeContract:
        if not self.verdict_values:
            raise JudgeContractError(f"judge {self.key!r}: verdict_values may not be empty")
        if self.mode == "rubric":
            # THE LINE. An absolute verdict without a named rubric is an
            # unaccountable opinion, and D-14 does not permit one.
            if not self.rubric_name or not (self.rubric or "").strip():
                raise JudgeContractError(
                    f"judge {self.key!r}: rubric mode requires BOTH rubric_name and rubric text. "
                    "Absolute scoring is only allowed against a named rubric (D-14); "
                    "if you have a reference to rank against, use mode='comparative' instead."
                )
        return self

    @property
    def rubric_fingerprint(self) -> str | None:
        """sha256 of the exact rubric text — proves which rubric produced a verdict."""
        if not self.rubric:
            return None
        return hashlib.sha256(self.rubric.encode("utf-8")).hexdigest()

    def assert_not_self_authored(self, subject_ref: EntityRef) -> None:
        """D-15 layer 1 — the judged agent may not have authored this rubric."""
        author = self.rubric_author_ref
        if author.ref_id and subject_ref.ref_id and author.ref_id == subject_ref.ref_id:
            raise JudgeContractError(
                f"judge {self.key!r} REFUSED: the subject being judged "
                f"({subject_ref.ref_type}:{subject_ref.ref_id}) is also the author of this "
                "judge's rubric. A unit may never author or see the rubric it is judged "
                "against (D-15) — move the rubric onto the judge contract, authored "
                "independently."
            )


class JudgeAssessment(BaseModel):
    """What a judge returns. One enumerated verdict, a confidence, and the
    evidence that makes the verdict checkable by a human."""

    model_config = ConfigDict(extra="forbid")

    verdict: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    reasoning: str = Field(min_length=1)
    evidence: list[str] = Field(default_factory=list)


class JudgeOutcome(BaseModel):
    """A verdict plus its ledger identity — what a caller persists and shows."""

    model_config = ConfigDict(extra="forbid")

    verdict: str
    confidence: float
    reasoning: str
    evidence: list[str] = Field(default_factory=list)
    judge_key: str
    judge_version: int
    mode: JudgeMode
    ledger_id: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
    #: How it ran — runner, model, and (Mandate path) the judge agent's own output
    #: dict, so a consumer keeps access to fields its agent returns beyond the
    #: contract's four (Hindsight's `quality_delta` / `regression_risk`).
    invocation: dict[str, Any] = Field(default_factory=dict)


def _assert_rubric_isolation(contract: JudgeContract, *subjects: JudgeSubject | None) -> None:
    """D-15 layer 2 — the rubric text may not be inside what is being judged.

    A caller that pastes the grading criteria into the agent's own prompt (or
    into the artifact) hands the judged unit its answer key. That is the
    realistic way this rule dies, and a string check is enough to stop it.
    """
    rubric = (contract.rubric or "").strip()
    if len(rubric) < 40:  # too short to fingerprint by containment without false hits
        return
    probe = rubric[:200]
    for subject in subjects:
        if subject is None:
            continue
        rendered = _format_output(subject.content)
        if probe in rendered:
            raise JudgeContractError(
                f"judge {contract.key!r} REFUSED: this judge's rubric text appears inside the "
                f"{subject.label or 'subject'} being judged. The judged unit must never see "
                "the rubric it is graded against (D-15). Remove the rubric from the subject's "
                "prompt/content — it belongs on the judge contract and nowhere else."
            )


def _verdict_model(contract: JudgeContract) -> type[JudgeAssessment]:
    """A per-contract strict model whose `verdict` is the contract's enumeration.

    Built here rather than validated afterwards so the PROVIDER enforces the
    vocabulary — an out-of-vocabulary verdict is impossible, not corrected.
    """
    values = contract.verdict_values

    class _Contracted(JudgeAssessment):
        model_config = ConfigDict(extra="forbid")
        verdict: Literal[values]  # type: ignore[valid-type]

    _Contracted.__name__ = "JudgeAssessment"
    return _Contracted


def _system_prompt(contract: JudgeContract) -> str:
    if contract.mode == "comparative":
        body = (
            "You are an impartial specialist judge. You are given a SUBJECT and a "
            "REFERENCE, and you decide how the subject compares to the reference.\n\n"
            "Rules:\n"
            "1. You are RANKING, not scoring. Never invent a numeric grade.\n"
            "2. Judge the subject only against the reference in front of you.\n"
            "3. Cite specific evidence — quotes or concrete observations — for your verdict.\n"
            "4. `confidence` is your certainty in the verdict, never the subject's quality.\n"
            "5. When the two are genuinely indistinguishable in the ways that matter, "
            "say so rather than manufacturing a difference.\n"
        )
    else:
        body = (
            "You are an impartial specialist judge. You assess ONE artifact against a "
            "NAMED RUBRIC and return a single enumerated verdict.\n\n"
            "Rules:\n"
            "1. Judge against the rubric as written — not against your own preferences.\n"
            "2. Cite specific evidence from the artifact (or its absence).\n"
            "3. Prefer the stricter verdict at low confidence over the lenient one "
            "with reservations.\n"
            "4. `confidence` is your certainty in the verdict, never the artifact's quality.\n"
        )
    allowed = ", ".join(repr(v) for v in contract.verdict_values)
    web = (
        " You may use web_search to check facts the question depends on; use it sparingly."
        if contract.web_access
        else ""
    )
    return f"{body}\nThe only permitted verdict values are: {allowed}.{web}"


def _user_message(
    contract: JudgeContract,
    subject: JudgeSubject,
    reference: JudgeSubject | None,
    context: dict[str, Any] | None,
) -> str:
    parts = [f"## The question\n{contract.question}"]
    if contract.rubric:
        parts.append(f"## Rubric — {contract.rubric_name}\n{contract.rubric}")
    if reference is not None:
        parts.append(
            f"## Reference ({reference.label or 'reference'})\n```\n"
            f"{_format_output(reference.content)}\n```"
        )
        if reference.metrics:
            parts.append(
                "### Reference measured metrics\n```json\n"
                f"{json.dumps(reference.metrics, indent=2, default=str)}\n```"
            )
    parts.append(
        f"## Subject ({subject.label or 'subject'})\n```\n{_format_output(subject.content)}\n```"
    )
    if subject.metrics:
        parts.append(
            "### Subject measured metrics\n```json\n"
            f"{json.dumps(subject.metrics, indent=2, default=str)}\n```"
        )
    if context:
        parts.append(f"## Context\n```json\n{json.dumps(context, indent=2, default=str)}\n```")
    parts.append("Return your verdict in the required structured shape.")
    return "\n\n".join(parts)


class Judge:
    """Runs one :class:`JudgeContract`, then writes the accuracy ledger.

    ``agent_cls`` is an optional :class:`~matrx_ai.agents.named.NamedAgent`
    subclass; pass it together with ``contract.mandate`` to run the judge as
    the DB-managed platform agent behind that Mandate (user-swappable, versioned,
    provenance-stamped) instead of on the raw funnel.
    """

    def __init__(
        self,
        contract: JudgeContract,
        *,
        agent_cls: Any | None = None,
        mandate_runner: Any | None = None,
        api_key: str | None = None,
    ) -> None:
        self.contract = contract
        self._agent_cls = agent_cls
        # There are deliberately TWO `run_mandated` twins — `matrx_ai.mandates`
        # (package-internal, injected resolver) and aidream's host-side one that
        # adds ambient-AppContext principal defaulting. A host judge must pass
        # its own, or it silently loses that defaulting.
        self._mandate_runner = mandate_runner
        self._api_key = api_key

    # ── The two modes ───────────────────────────────────────────────────────

    async def compare(
        self,
        subject: JudgeSubject,
        reference: JudgeSubject,
        *,
        context: dict[str, Any] | None = None,
        organization_id: str | None = None,
        user_id: str | None = None,
        ledger: bool = True,
    ) -> JudgeOutcome:
        """Rank ``subject`` against ``reference``. The preferred mode (D-14)."""
        if self.contract.mode != "comparative":
            raise JudgeContractError(
                f"judge {self.contract.key!r} is declared mode={self.contract.mode!r}; "
                "compare() requires mode='comparative'."
            )
        return await self._run(
            subject,
            reference,
            context=context,
            organization_id=organization_id,
            user_id=user_id,
            ledger=ledger,
        )

    async def score(
        self,
        subject: JudgeSubject,
        *,
        context: dict[str, Any] | None = None,
        organization_id: str | None = None,
        user_id: str | None = None,
        ledger: bool = True,
    ) -> JudgeOutcome:
        """Assess ``subject`` absolutely — only ever against a named rubric."""
        if self.contract.mode != "rubric":
            raise JudgeContractError(
                f"judge {self.contract.key!r} is declared mode={self.contract.mode!r}; "
                "score() requires mode='rubric'. If a reference exists, rank against it "
                "with compare() — ranking beats absolute scoring whenever both are possible."
            )
        return await self._run(
            subject,
            None,
            context=context,
            organization_id=organization_id,
            user_id=user_id,
            ledger=ledger,
        )

    # ── Execution ───────────────────────────────────────────────────────────

    async def _run(
        self,
        subject: JudgeSubject,
        reference: JudgeSubject | None,
        *,
        context: dict[str, Any] | None,
        organization_id: str | None,
        user_id: str | None,
        ledger: bool,
    ) -> JudgeOutcome:
        contract = self.contract
        # D-15, before anything is paid for.
        contract.assert_not_self_authored(subject.ref)
        _assert_rubric_isolation(contract, subject, reference)

        if self._agent_cls is not None and contract.mandate:
            verdict, invocation = await self._run_mandated(
                subject, reference, context=context, user_id=user_id
            )
        else:
            verdict, invocation = await self._run_funnel(subject, reference, context=context)

        outcome = JudgeOutcome(
            verdict=verdict.verdict,
            confidence=verdict.confidence,
            reasoning=verdict.reasoning,
            evidence=list(verdict.evidence),
            judge_key=contract.key,
            judge_version=contract.version,
            mode=contract.mode,
            raw=verdict.model_dump(),
            invocation=invocation,
        )
        if ledger:
            from matrx_ai.evaluators.ledger import record_verdict

            outcome.ledger_id = await record_verdict(
                contract=contract,
                subject=subject,
                reference=reference,
                outcome=outcome,
                invocation=invocation,
                organization_id=organization_id,
                user_id=user_id,
            )
        return outcome

    async def _run_funnel(
        self,
        subject: JudgeSubject,
        reference: JudgeSubject | None,
        *,
        context: dict[str, Any] | None,
    ) -> tuple[JudgeAssessment, dict[str, Any]]:
        contract = self.contract
        api_key = self._api_key or resolve_api_key("ANTHROPIC_API_KEY")
        if not api_key:
            raise JudgeError(
                f"judge {contract.key!r}: ANTHROPIC_API_KEY not set and no api_key passed."
            )
        try:
            verdict = await llm_messages_to_pydantic(
                model=contract.model,
                system=_system_prompt(contract),
                messages=[
                    {
                        "role": "user",
                        "content": _user_message(contract, subject, reference, context),
                    }
                ],
                output_cls=_verdict_model(contract),
                max_tokens=contract.max_tokens,
                internal_web_search=contract.web_access,
                api_keys={"ANTHROPIC_API_KEY": api_key},
                system_run=True,
                store=True,
                metadata={
                    "source_app": "matrx-ai",
                    "source_feature": "judge",
                    "judge_key": contract.key,
                    "judge_version": contract.version,
                },
            )
        except (StrictJsonError, RuntimeError) as exc:
            raise JudgeError(f"judge {contract.key!r} failed through the funnel: {exc}") from exc
        return verdict, {"runner": "funnel", "model": contract.model}

    async def _run_mandated(
        self,
        subject: JudgeSubject,
        reference: JudgeSubject | None,
        *,
        context: dict[str, Any] | None,
        user_id: str | None,
    ) -> tuple[JudgeAssessment, dict[str, Any]]:
        """Run the judge as the DB agent behind its Mandate.

        The mandated agent owns its own output schema (it is authored in the
        product, versioned, swappable). We map that output onto the contract's
        verdict vocabulary here rather than forcing every judge agent to be
        rewritten — the contract stays the authority on what a verdict may be.
        """
        if self._mandate_runner is not None:
            run_mandated = self._mandate_runner
        else:
            from matrx_ai.mandates import run_mandated

        contract = self.contract
        agent_cls = self._agent_cls
        # Granular delivery (2026-08-22): every value the harness has in scope is
        # its own named variable — dicts/lists raw, the prompt door canonicalizes.
        # Never a fused `payload_json` blob again (THE USER-INPUT LAW / Provision
        # model: the agent's variables ARE the offer, name for name).
        inputs = agent_cls.Inputs(
            question=contract.question,
            rubric_name=contract.rubric_name,
            rubric=contract.rubric,
            verdict_values=list(contract.verdict_values),
            subject_label=subject.label,
            subject_content=_format_output(subject.content),
            subject_metrics=dict(subject.metrics) if subject.metrics else None,
            reference_label=reference.label if reference is not None else None,
            reference_content=_format_output(reference.content) if reference is not None else None,
            reference_metrics=(
                dict(reference.metrics) if reference is not None and reference.metrics else None
            ),
            context=dict(context) if context else None,
        )
        res = await run_mandated(
            agent_cls,
            inputs=inputs,
            user_id=user_id,
            label=f"Judge · {contract.key}",
            request_metadata={
                "feature": "judge",
                "judge_key": contract.key,
                "judge_version": contract.version,
            },
        )
        parsed = res.parsed
        if parsed is None:
            raise JudgeError(f"judge {contract.key!r}: mandated agent returned no parsed output")
        raw = parsed.model_dump() if isinstance(parsed, BaseModel) else dict(parsed)
        value = str(raw.get("verdict") or "").strip()
        if value not in contract.verdict_values:
            # LOUD, and it does not become a fake verdict. The contract owns the
            # vocabulary; a mandated agent that drifts off it is a real defect.
            raise JudgeError(
                f"judge {contract.key!r}: mandated agent returned verdict {value!r}, which is "
                f"not in the contract's vocabulary {contract.verdict_values}. Either the "
                "agent's output schema drifted from the contract, or the contract needs a "
                "new version — never silently coerce a verdict."
            )
        confidence = raw.get("confidence")
        verdict = JudgeAssessment(
            verdict=value,
            confidence=float(confidence) if isinstance(confidence, int | float) else 0.5,
            reasoning=str(raw.get("reasoning") or "").strip() or "(no reasoning returned)",
            evidence=[str(x) for x in (raw.get("evidence") or []) if str(x).strip()],
        )
        return verdict, {
            # 🚨 RETIRED WORD, DELIBERATELY STILL WRITTEN. This is a persisted
            # value (`platform.judge_verdict.invocation`), not prose — 5 live
            # rows already say "slot". Flipping the writer alone would fork the
            # column's vocabulary, which is worse than the stale word. Law 4
            # makes this a data migration: UPDATE the 5 rows to "mandate" and
            # change this literal in the SAME change. Ledgered in FOUND_DEFECTS.md.
            "runner": "slot",
            "mandate": contract.mandate,
            "model": getattr(res, "model_id", None),
            "agent_output": raw,
        }


__all__ = [
    "COMPARATIVE_VERDICTS",
    "RUBRIC_VERDICTS",
    "AuthorityKind",
    "EntityRef",
    "Judge",
    "JudgeContract",
    "JudgeContractError",
    "JudgeInputs",
    "JudgeMode",
    "JudgeOutcome",
    "JudgeSubject",
    "JudgeAssessment",
    "Provenance",
]
