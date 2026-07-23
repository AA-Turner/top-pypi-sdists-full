"""Jacobian-based dataset-augmentation extraction (Papernot et al., arXiv 1602.02697).

Iteratively fit a surrogate, expand the query set along the surrogate's gradient
sign, query ONLY the new points, and refit - until the budget is spent. Only newly
synthesised points are queried each round (prior labels are cached), so the total
query count stays within ``query_budget``. Augmentation needs raw inputs to be the
feature space (numeric); text targets fall back to the batch campaign.
"""

import typing as t

import numpy as np

from dreadnode.airt.extraction._base import (
    ExtractionResult,
    ModelExtractionAttack,
    QueryPool,
    _numeric_gradient_sign,
    _Surrogate,
    top1_fidelity,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec


async def run(attack: ModelExtractionAttack) -> ExtractionResult:
    campaign = await attack._prepare_campaign()
    with attack._phase(
        "query + fit surrogate", queries=campaign.train_budget, strategy=attack.strategy
    ):
        if attack._numeric:
            seed_x = np.asarray(attack._feat(campaign.train_raw))
            surrogate = await _run_jacobian(attack, campaign, seed_x)
            budget_curve: list[tuple[int, float]] = []
        else:
            surrogate, budget_curve = await attack._run_batch_campaign(campaign)
    return await attack._finalize(campaign, surrogate, budget_curve)


async def _run_jacobian(
    attack: ModelExtractionAttack, campaign: t.Any, seed_x: np.ndarray
) -> _Surrogate:
    """Iterative Jacobian-based augmentation: fit, expand the query set along the
    surrogate's gradient sign, query ONLY the new points, refit - until budget.

    Only newly synthesised points are queried each round (prior labels are
    cached), so the total query count stays within ``query_budget``. Each round
    emits a trace step so the augmentation trajectory is visible in the Traces tab."""
    classes = campaign.classes
    x_all = seed_x
    proba, labels = await attack._query_soft(seed_x)
    surrogate = attack._build_surrogate(x_all, proba, labels, classes)
    for it in range(attack.jacobian_rounds):
        room = attack.query_budget - attack._query_count
        if room <= 0:
            break
        grad_sign = _numeric_gradient_sign(surrogate, x_all)
        new_x = (x_all + attack.jacobian_lambda * grad_sign)[:room]
        new_proba, new_labels = await attack._query_soft(new_x)
        x_all = np.vstack([x_all, new_x])
        proba = np.vstack([proba, new_proba])
        labels = np.concatenate([labels, new_labels])
        surrogate = attack._build_surrogate(x_all, proba, labels, classes)
        fid = top1_fidelity(
            surrogate.predict_label(campaign.eval_feat), campaign.target_eval_labels
        )
        attack._trace_step(
            it,
            input={"new_points": len(new_x), "pool_size": len(x_all)},
            output={"fidelity": round(fid, 4)},
            metrics={"fidelity": round(fid, 4), "queries": attack._query_count},
        )
    return surrogate


def jacobian_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """Jacobian-based dataset augmentation for query-efficient boundary cloning
    (Papernot'17). Grows the query set along the surrogate's gradient sign."""
    return ModelExtractionAttack(
        strategy="jacobian", target=target, query_pool=query_pool, **kwargs
    )
