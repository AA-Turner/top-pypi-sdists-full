"""ActiveThief extraction (Pal et al. 2020).

Instead of querying the pool blindly, query in rounds and pick the next batch by
surrogate uncertainty (highest prediction entropy), refitting each round so the
query budget is spent on the most informative inputs. Each round emits a trace
step so the query-selection trajectory is visible in the Traces tab.
"""

import typing as t

import numpy as np

from dreadnode.airt.extraction._base import (
    ExtractionResult,
    ModelExtractionAttack,
    QueryPool,
    _Surrogate,
    top1_fidelity,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec


async def run(attack: ModelExtractionAttack) -> ExtractionResult:
    campaign = await attack._prepare_campaign()
    with attack._phase(
        "query + fit surrogate", queries=campaign.train_budget, strategy=attack.strategy
    ):
        surrogate, budget_curve = await _run_activethief(
            attack,
            campaign.pool,
            campaign.eval_feat,
            campaign.target_eval_labels,
            campaign.classes,
            campaign.train_budget,
        )
    return await attack._finalize(campaign, surrogate, budget_curve)


async def _run_activethief(
    attack: ModelExtractionAttack,
    pool: list[t.Any],
    eval_feat: np.ndarray,
    target_eval_labels: np.ndarray,
    classes: np.ndarray,
    budget: int,
) -> tuple[_Surrogate, list[tuple[int, float]]]:
    """ActiveThief (Pal et al. 2020): instead of querying the pool blindly,
    query in rounds and pick the next batch by surrogate uncertainty (highest
    prediction entropy), refitting each round. Each round emits a trace step so
    the query-selection trajectory is visible."""
    candidates = list(pool)
    n_query = min(budget, len(candidates))
    rounds = 5
    per_round = max(2, n_query // rounds)
    order: list[int] = [int(i) for i in attack.rng.permutation(len(candidates))]
    feat = proba = labels = None
    n_queried = 0
    surrogate: _Surrogate | None = None
    budget_curve: list[tuple[int, float]] = []
    while order and n_queried < n_query and not attack._over_budget():
        if surrogate is None:
            batch_idx, order = order[:per_round], order[per_round:]
        else:
            rem_feat = attack._feat([candidates[i] for i in order])
            p = surrogate.predict_proba(rem_feat)
            entropy = -np.sum(p * np.log(np.clip(p, 1e-9, 1.0)), axis=1)
            top = np.argsort(-entropy)[:per_round]
            batch_idx = [order[j] for j in top]
            chosen = set(batch_idx)
            order = [i for i in order if i not in chosen]
        batch_raw = [candidates[i] for i in batch_idx]
        if not batch_raw:
            break
        bp, bl = await attack._query_soft(batch_raw)
        bf = attack._feat(batch_raw)
        feat = bf if feat is None else np.vstack([feat, bf])
        proba = bp if proba is None else np.vstack([proba, bp])
        labels = bl if labels is None else np.concatenate([labels, bl])
        n_queried += len(batch_raw)
        surrogate = attack._build_surrogate(feat, proba, labels, classes)
        fid = top1_fidelity(surrogate.predict_label(eval_feat), target_eval_labels)
        budget_curve.append((attack._query_count, round(fid, 4)))
        attack._trace_step(
            len(budget_curve),
            input={"batch_size": len(batch_raw), "queried": n_queried},
            output={"fidelity": round(fid, 4)},
            metrics={"fidelity": round(fid, 4), "queries": attack._query_count},
        )
    if surrogate is None:
        # Degenerate case (budget exhausted before any round ran): force a
        # single seed batch so we always return a fitted surrogate.
        seed = [candidates[i] for i in order[: max(2, per_round)]] or candidates[
            : max(2, per_round)
        ]
        bp, bl = await attack._query_soft(seed)
        surrogate = attack._build_surrogate(attack._feat(seed), bp, bl, classes)
    return surrogate, budget_curve


def activethief_extraction(
    target: PredictionTargetSpec, query_pool: QueryPool, **kwargs: t.Any
) -> ModelExtractionAttack:
    """ActiveThief extraction (Pal et al. 2020). Queries the pool in rounds,
    selecting each next batch by surrogate uncertainty (highest prediction
    entropy) so the query budget is spent on the most informative inputs."""
    return ModelExtractionAttack(
        strategy="activethief", target=target, query_pool=query_pool, **kwargs
    )
