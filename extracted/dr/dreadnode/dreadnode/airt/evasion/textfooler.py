"""TextFooler (Jin et al. 2020): word-level synonym-substitution text evasion.

Rank words by importance (leave-one-out confidence drop), then greedily replace
the most important words with the candidate that most reduces the original-class
confidence, until the label flips. Word-level substitution only (no appended
triggers, no typos).
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack
from dreadnode.airt.evasion._text_common import (
    greedy_substitute,
    importance_scan,
    text_setup,
)
from dreadnode.airt.evasion.text import WORD_CANDIDATES
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    text, orig_label, orig_cls, words, cur_conf = await text_setup(attack)
    current = list(words)
    curve: list[tuple[int, float]] = []
    ranked = await importance_scan(attack, current, orig_label, orig_cls, words, curve, text)
    if not isinstance(ranked, list):
        return ranked
    return await greedy_substitute(
        attack,
        text=text,
        current=current,
        importance=ranked,
        orig_label=orig_label,
        orig_cls=orig_cls,
        words=words,
        curve=curve,
        cur_conf=cur_conf,
        candidates=lambda _word: WORD_CANDIDATES,
    )


def textfooler_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """TextFooler (Jin et al. 2020): ranks words by importance, then greedily
    substitutes the most important words with the candidate that most reduces the
    original-class confidence until the label flips (word-level, no appending)."""
    return ModelEvasionAttack(strategy="textfooler", target=target, original=original, **kwargs)
