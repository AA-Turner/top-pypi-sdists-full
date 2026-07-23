"""BAE - BERT-based Adversarial Examples (Garg & Ramakrishnan 2020).

BAE perturbs the most important tokens with a masked language model using two
operations: REPLACE (swap a token for a context-fit alternative) and INSERT (add
a token adjacent to it). Its hallmark versus word-only attacks is that insertion
grows the text rather than only replacing. Without a hosted MLM in the black-box
setting, our version draws replacements/insertions from a curated candidate set
and keeps whichever operation most reduces the original-class confidence.
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


def _bae_candidates(word: str) -> list[str]:
    """BAE-R (replace ``word`` with a candidate) and BAE-I (insert a candidate
    before ``word``). Insertion is realised as a two-token string so the shared
    substitution machinery applies it without index bookkeeping."""
    out: list[str] = []
    for c in WORD_CANDIDATES:
        if not c:
            continue
        out.append(c)  # replace
        out.append(f"{c} {word}")  # insert-before
    return out


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
        candidates=_bae_candidates,
    )


def bae_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """BAE (Garg & Ramakrishnan 2020): masked-LM-style text evasion using replace
    and insert operations on the most important tokens."""
    return ModelEvasionAttack(strategy="bae", target=target, original=original, **kwargs)
