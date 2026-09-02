"""The Selector — pick among N candidates, by comparison, never by score.

Engram VISION §3.6: speculative execution runs 2-3 plausible branches in
parallel and keeps the winner, and *"the selector is the ceiling"* — discarding
the losers requires exactly the "is this good" judgement models are mediocre at.
The resolution the vision names is this class: **the Selector is a first-class
specialist**, with its own contract, its own accuracy ledger, and — the part
that actually makes it work — it selects **by comparison**, never by grading
each candidate on an absolute scale.

So this is deliberately a *thin* specialization of :class:`Judge`, not a new
evaluator. It is a champion-challenger tournament over the candidate list:

    champion = candidates[0]
    for challenger in candidates[1:]:
        if judge.compare(challenger, champion) == 'better':
            champion = challenger

Every comparison is one ordinary comparative judgement and lands its own ledger
row, so a Selector's accuracy is measured by the same machinery as any judge's —
and a counterfactual replay of the losing branch can later stamp the agreement
bit on the exact comparison that discarded it (§4.2).

The constructor REFUSES a rubric-mode contract. There is no absolute-score path
into this class, by construction — that is the whole point of the specialization.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from matrx_ai.evaluators.judge import (
    Judge,
    JudgeContract,
    JudgeContractError,
    JudgeOutcome,
    JudgeSubject,
)

logger = logging.getLogger("matrx_ai.evaluators.selector")


class SelectionComparison(BaseModel):
    """One head-to-head in the tournament, kept so the choice is auditable."""

    model_config = ConfigDict(extra="forbid")

    challenger_index: int
    champion_index: int
    verdict: str
    confidence: float
    reasoning: str
    ledger_id: str | None = None


class Selection(BaseModel):
    """Which candidate won, and every comparison that decided it."""

    model_config = ConfigDict(extra="forbid")

    winner_index: int
    winner_label: str
    comparisons: list[SelectionComparison] = Field(default_factory=list)
    judge_key: str
    judge_version: int


class Selector:
    """Pick the best of N candidates by pairwise comparison."""

    def __init__(self, contract: JudgeContract, *, agent_cls: Any | None = None) -> None:
        if contract.mode != "comparative":
            raise JudgeContractError(
                f"Selector refuses judge {contract.key!r}: mode={contract.mode!r}. A selector "
                "picks by COMPARISON, never by absolute score (VISION §3.6) — declare the "
                "contract with mode='comparative'."
            )
        self.contract = contract
        self._judge = Judge(contract, agent_cls=agent_cls)

    async def select(
        self,
        candidates: list[JudgeSubject],
        *,
        context: dict[str, Any] | None = None,
        organization_id: str | None = None,
        user_id: str | None = None,
    ) -> Selection:
        if not candidates:
            raise JudgeContractError(
                f"Selector {self.contract.key!r}: the candidate list is empty — "
                "there is nothing to choose between."
            )
        candidate_refs = [
            {"index": i, "label": c.label, "ref_type": c.ref.ref_type, "ref_id": c.ref.ref_id}
            for i, c in enumerate(candidates)
        ]
        champion_index = 0
        comparisons: list[SelectionComparison] = []

        for index in range(1, len(candidates)):
            outcome: JudgeOutcome = await self._judge.compare(
                candidates[index],
                candidates[champion_index],
                context={
                    **(context or {}),
                    "selection": {
                        "candidate_count": len(candidates),
                        "challenger_index": index,
                        "champion_index": champion_index,
                    },
                },
                organization_id=organization_id,
                user_id=user_id,
                ledger=False,  # written below with the full candidate set attached
            )
            ledger_id = await self._record(
                candidates[index],
                candidates[champion_index],
                outcome,
                candidate_refs,
                organization_id,
                user_id,
            )
            comparisons.append(
                SelectionComparison(
                    challenger_index=index,
                    champion_index=champion_index,
                    verdict=outcome.verdict,
                    confidence=outcome.confidence,
                    reasoning=outcome.reasoning,
                    ledger_id=ledger_id,
                )
            )
            # Only a clear win unseats the champion. `same` keeps the incumbent —
            # a tie is not a reason to churn, and treating it as one would make
            # the result depend on candidate ORDER far more than on quality.
            if outcome.verdict == "better":
                champion_index = index

        return Selection(
            winner_index=champion_index,
            winner_label=candidates[champion_index].label,
            comparisons=comparisons,
            judge_key=self.contract.key,
            judge_version=self.contract.version,
        )

    async def _record(
        self,
        challenger: JudgeSubject,
        champion: JudgeSubject,
        outcome: JudgeOutcome,
        candidate_refs: list[dict[str, Any]],
        organization_id: str | None,
        user_id: str | None,
    ) -> str | None:
        from matrx_ai.evaluators.ledger import record_verdict

        return await record_verdict(
            contract=self.contract,
            subject=challenger,
            reference=champion,
            outcome=outcome,
            invocation={"runner": "selector", "model": self.contract.model},
            organization_id=organization_id,
            user_id=user_id,
            candidate_refs=candidate_refs,
        )


__all__ = ["Selection", "SelectionComparison", "Selector"]
