"""Knockoff Nets extraction (Orekondy et al., arXiv 1812.02766).

Soft-label transfer-set extraction: query the pool once for the target's full
probability vectors, then fit a surrogate on those soft labels for the highest
fidelity. Uses ART's KnockoffNets when available, else a native soft-label fit.
"""

import typing as t

from dreadnode.airt.extraction._base import (
    ExtractionResult,
    ModelExtractionAttack,
    QueryPool,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec


async def run(attack: ModelExtractionAttack) -> ExtractionResult:
    campaign = await attack._prepare_campaign()
    with attack._phase(
        "query + fit surrogate", queries=campaign.train_budget, strategy=attack.strategy
    ):
        surrogate, budget_curve = await attack._run_batch_campaign(campaign)
    return await attack._finalize(campaign, surrogate, budget_curve)


def knockoff_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """Soft-label transfer-set extraction (Knockoff Nets). Trains the surrogate on the
    target's probability vectors for the highest fidelity."""
    return ModelExtractionAttack(
        strategy="knockoff", target=target, query_pool=query_pool, **kwargs
    )
