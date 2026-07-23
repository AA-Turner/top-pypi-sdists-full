"""Equation-solving extraction (Tramer et al., USENIX'16).

Recover a (near-)linear model by inverting its softmax outputs. Queries the pool
once for soft labels, then solves ``[X | 1] . W = log(p)`` per class - exact when
the target is linear. No iterative surrogate training.
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


def equation_solving_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """Recover a (near-)linear model by inverting its softmax outputs (Tramer'16).
    Exact for logistic/linear targets; needs soft outputs. No surrogate training."""
    return ModelExtractionAttack(
        strategy="equation_solving", target=target, query_pool=query_pool, **kwargs
    )
