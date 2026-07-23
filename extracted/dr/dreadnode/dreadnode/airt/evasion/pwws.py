"""PWWS - Probability Weighted Word Saliency (Ren et al. 2019).

PWWS orders substitutions by a combined score: each word's *saliency* (how much
the original-class confidence drops when the word is removed) multiplied by the
*confidence gain* of its best synonym replacement. Words that are both salient
and have a high-impact synonym are perturbed first, which flips the label with
fewer edits than plain importance ordering. Our black-box version estimates
saliency and gain from the target's confidence scores over a bounded synonym set.
"""

import typing as t

import numpy as np

from dreadnode.airt.evasion._base import ModelEvasionAttack
from dreadnode.airt.evasion._text_common import (
    importance_scan,
    join,
    make_failed,
    make_flipped,
    text_setup,
)
from dreadnode.airt.evasion.text import WORD_CANDIDATES
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput

#: How many of the most-salient words to score for synonym gain (bounds queries
#: on long documents while covering the words that matter).
_TOP_K = 40


async def run(attack: ModelEvasionAttack) -> t.Any:
    text, orig_label, orig_cls, words, cur_conf = await text_setup(attack)
    current = list(words)
    curve: list[tuple[int, float]] = []

    ranked = await importance_scan(attack, current, orig_label, orig_cls, words, curve, text)
    if not isinstance(ranked, list):
        return ranked

    # saliency = 1 - residual_confidence when the word is removed; softmax it.
    salient = ranked[:_TOP_K]
    sal = np.array([max(0.0, 1.0 - conf) for conf, _ in salient])
    weights = np.exp(sal - sal.max()) if sal.size else sal
    weights = weights / (weights.sum() + 1e-12)

    # Score each salient word's best synonym gain, then order by saliency*gain.
    scored: list[tuple[float, int, str, t.Any]] = []
    for w, (_base_conf, i) in zip(weights, salient, strict=False):
        if attack._over_budget():
            break
        best_repl, best_conf, best_pred = None, cur_conf, None
        for repl in WORD_CANDIDATES:
            if attack._over_budget():
                break
            trial = current.copy()
            trial[i] = repl
            p = (await attack._predict([join(trial)]))[0]
            if attack._label(p) != orig_label:
                current[i] = repl
                curve.append((attack._query_count, 1 / max(len(words), 1)))
                return make_flipped(
                    attack, text, join(current), orig_label, attack._label(p), 1, words, curve
                )
            conf = attack._orig_confidence(p, orig_cls)
            if conf < best_conf:
                best_repl, best_conf, best_pred = repl, conf, p
        if best_repl is not None:
            gain = max(0.0, cur_conf - best_conf)
            scored.append((float(w) * gain, i, best_repl, best_pred))

    # Apply in descending PWWS order until the label flips.
    scored.sort(key=lambda s: s[0], reverse=True)
    changed: set[int] = set()
    for _, i, repl, _pred in scored:
        if attack._over_budget():
            break
        current[i] = repl
        changed.add(i)
        p = (await attack._predict([join(current)]))[0]
        cur_conf = attack._orig_confidence(p, orig_cls)
        curve.append((attack._query_count, cur_conf))
        attack._trace_step(
            len(changed),
            input=join(current),
            output=attack._pred_summary(p),
            metrics={
                "confidence": round(cur_conf, 4),
                "tokens_changed": len(changed),
                "queries": attack._query_count,
            },
        )
        if attack._label(p) != orig_label:
            return make_flipped(
                attack,
                text,
                join(current),
                orig_label,
                attack._label(p),
                len(changed),
                words,
                curve,
            )
    return make_failed(attack, text, current, changed, cur_conf, words, curve)


def pwws_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """PWWS (Ren et al. 2019): probability-weighted word-saliency text evasion.
    Orders synonym substitutions by word saliency times synonym gain, flipping the
    label with fewer edits than plain importance ordering."""
    return ModelEvasionAttack(strategy="pwws", target=target, original=original, **kwargs)
