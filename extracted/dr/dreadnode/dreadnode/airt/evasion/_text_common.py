"""Shared plumbing for the text-evasion attacks.

Every text attack follows the same skeleton: predict the clean text, rank words
by a leave-one-out importance scan, then greedily perturb the most important
words (each attack supplying its own candidate generator) until the label flips.
This module factors out the common steps so each attack module only owns the
part that makes it distinct (the candidate generator and any pre-phase), and so
the per-step trajectory tracing is emitted identically everywhere.
"""

import typing as t

import numpy as np

from dreadnode.airt.evasion._base import (
    EvasionResult,
    ModelEvasionAttack,
    _trunc,
    levenshtein,
)


def _edit(orig: str, pert: str) -> tuple[int, float]:
    """Levenshtein distance and its length-normalised form for a text edit."""
    lev = levenshtein(orig, pert)
    return lev, round(lev / max(len(orig), 1), 4)


def join(ws: list[str]) -> str:
    return " ".join(w for w in ws if w)


async def text_setup(
    attack: ModelEvasionAttack,
) -> tuple[str, t.Any, int, list[str], float]:
    """Predict the clean text and return (text, orig_label, orig_cls, words,
    clean_confidence)."""
    text = str(attack.original)
    base = await attack._predict([text])
    orig_label = attack._label(base[0])
    orig_cls = int(orig_label) if isinstance(orig_label, (int, np.integer)) else 0
    words = text.split()
    cur_conf = attack._orig_confidence(base[0], orig_cls)
    return text, orig_label, orig_cls, words, cur_conf


def make_flipped(
    attack: ModelEvasionAttack,
    orig: str,
    pert: str,
    orig_label: t.Any,
    adv_label: t.Any,
    n_changed: int,
    words: list[str],
    curve: list[tuple[int, float]],
) -> EvasionResult:
    frac = n_changed / max(len(words), 1)
    lev, lev_norm = _edit(orig, pert)
    return EvasionResult(
        strategy=attack.strategy,
        success=True,
        original_class=orig_label,
        adversarial_class=adv_label,
        distance_norm="tokens",
        distance_value=frac,
        residual_confidence=0.0,
        query_count=attack._query_count,
        distance_curve=curve or [(attack._query_count, frac)],
        original_preview=_trunc(orig),
        perturbed_preview=_trunc(pert),
        tokens_changed=n_changed,
        tokens_total=len(orig.split()),
        l0_changed=n_changed,
        levenshtein=lev,
        levenshtein_normalized=lev_norm,
    )


def make_failed(
    attack: ModelEvasionAttack,
    orig: str,
    current: list[str],
    changed: set[int],
    cur_conf: float,
    words: list[str],
    curve: list[tuple[int, float]],
) -> EvasionResult:
    pert = join(current)
    lev, lev_norm = _edit(orig, pert)
    return EvasionResult(
        strategy=attack.strategy,
        success=False,
        original_class=None,
        adversarial_class=None,
        distance_norm="tokens",
        distance_value=len(changed) / max(len(words), 1),
        residual_confidence=float(cur_conf),
        query_count=attack._query_count,
        distance_curve=curve or [(attack._query_count, 0.0)],
        original_preview=_trunc(orig),
        perturbed_preview=_trunc(pert),
        tokens_changed=len(changed),
        tokens_total=len(words),
        levenshtein=lev,
        levenshtein_normalized=lev_norm,
    )


async def importance_scan(
    attack: ModelEvasionAttack,
    current: list[str],
    orig_label: t.Any,
    orig_cls: int,
    words: list[str],
    curve: list[tuple[int, float]],
    text: str,
) -> "list[tuple[float, int]] | EvasionResult":
    """Rank words by the confidence drop when each is deleted (leave-one-out).
    A plain deletion that already flips the label short-circuits to a success
    result; otherwise returns the ranking (lowest residual confidence first)."""
    importance: list[tuple[float, int]] = []
    for i in range(len(current)):
        if attack._over_budget():
            break
        trial = current.copy()
        trial[i] = ""
        p = (await attack._predict([join(trial)]))[0]
        if attack._label(p) != orig_label:
            curve.append((attack._query_count, 1 / max(len(words), 1)))
            return make_flipped(
                attack, text, join(trial), orig_label, attack._label(p), 1, words, curve
            )
        importance.append((attack._orig_confidence(p, orig_cls), i))
    importance.sort()  # lowest residual confidence first = most impactful
    return importance


async def greedy_substitute(
    attack: ModelEvasionAttack,
    *,
    text: str,
    current: list[str],
    importance: list[tuple[float, int]],
    orig_label: t.Any,
    orig_cls: int,
    words: list[str],
    curve: list[tuple[int, float]],
    cur_conf: float,
    candidates: t.Callable[[str], t.Iterable[str]],
) -> EvasionResult:
    """Greedily replace the most important words with the candidate (from the
    attack-specific ``candidates`` generator) that most reduces the original-class
    confidence, until the label flips or the budget is spent. Emits an enriched
    per-step trace (current text + target verdict) on each accepted substitution."""
    changed: set[int] = set()
    for _, i in importance:
        if attack._over_budget():
            break
        best_repl, best_conf, best_pred = None, cur_conf, None
        for repl in candidates(current[i]):
            if attack._over_budget():
                break
            trial = current.copy()
            trial[i] = repl
            p = (await attack._predict([join(trial)]))[0]
            if attack._label(p) != orig_label:
                current[i] = repl
                changed.add(i)
                curve.append((attack._query_count, len(changed) / max(len(words), 1)))
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
            conf = attack._orig_confidence(p, orig_cls)
            if conf < best_conf:
                best_repl, best_conf, best_pred = repl, conf, p
        if best_repl is not None:
            current[i] = best_repl
            changed.add(i)
            cur_conf = best_conf
            curve.append((attack._query_count, cur_conf))
            attack._trace_step(
                len(changed),
                input=join(current),
                output=attack._pred_summary(best_pred) if best_pred is not None else None,
                metrics={
                    "confidence": round(cur_conf, 4),
                    "tokens_changed": len(changed),
                    "queries": attack._query_count,
                },
            )
    return make_failed(attack, text, current, changed, cur_conf, words, curve)
