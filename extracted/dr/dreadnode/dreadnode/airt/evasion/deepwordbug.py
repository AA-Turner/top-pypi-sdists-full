"""DeepWordBug (Gao et al. 2018): character-level text evasion.

Rank words by importance, then apply minimal character edits (adjacent swap /
substitute / delete / insert) to the most important words until the label flips.
Character perturbations produce human-readable typos rather than semantic word
swaps, so they probe a different weakness than :mod:`text` / :mod:`textfooler`.
"""

import typing as t

import numpy as np

from dreadnode.airt.evasion._base import ModelEvasionAttack
from dreadnode.airt.evasion._text_common import (
    greedy_substitute,
    importance_scan,
    text_setup,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput

_ALPHABET = "qwertyuiopasdfghjklzxcvbnm"


def char_perturbations(word: str, rng: np.random.Generator) -> list[str]:
    """DeepWordBug character transforms applied near the middle of the word so
    the first/last letters stay intact (readable typos): adjacent-swap,
    substitute, delete, insert. Returns variants that actually differ."""
    if len(word) < 2:
        return []
    m = len(word) // 2
    variants: list[str] = []
    if m + 1 < len(word):  # swap two adjacent characters
        s = list(word)
        s[m], s[m + 1] = s[m + 1], s[m]
        variants.append("".join(s))
    sub = _ALPHABET[int(rng.integers(0, len(_ALPHABET)))]
    variants.append(word[:m] + sub + word[m + 1 :])  # substitute
    variants.append(word[:m] + word[m + 1 :])  # delete
    ins = _ALPHABET[int(rng.integers(0, len(_ALPHABET)))]
    variants.append(word[:m] + ins + word[m:])  # insert
    return [v for v in variants if v and v != word]


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
        candidates=lambda word: char_perturbations(word, attack.rng),
    )


def deepwordbug_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """DeepWordBug black-box evasion for text inputs (Gao et al. 2018). Ranks
    words by importance, then applies minimal character-level typos (swap /
    substitute / delete / insert) to the most important words until the label
    flips - a readable, character-level counterpart to :func:`text_evasion`."""
    return ModelEvasionAttack(strategy="deepwordbug", target=target, original=original, **kwargs)
