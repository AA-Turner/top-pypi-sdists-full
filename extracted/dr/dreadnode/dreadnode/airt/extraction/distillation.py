"""Knowledge-distillation extraction.

Train the surrogate to match the target's full probability vectors (soft targets)
via KL divergence - a straightforward, strong distillation baseline. Queries the
pool once for soft labels, then fits a soft-label surrogate.
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


def distillation_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """Knowledge-distillation extraction. Trains the surrogate to match the
    target's full probability vectors (soft targets) via KL divergence - a
    straightforward, strong distillation baseline."""
    return ModelExtractionAttack(
        strategy="distillation", target=target, query_pool=query_pool, **kwargs
    )
