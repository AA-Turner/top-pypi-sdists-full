"""Copycat extraction (Correia-Silva et al., arXiv 1806.05476 / CopycatCNN).

Hard-label distillation on natural or random queries: query the pool once, then
fit a classifier on the target's top-1 labels. Works even when the target returns
only a label. Uses ART's CopycatCNN when available, else a native sklearn fit.
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


def copycat_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """Hard-label distillation on natural/random queries (CopycatCNN). Works even
    when the target returns only a label."""
    return ModelExtractionAttack(strategy="copycat", target=target, query_pool=query_pool, **kwargs)
