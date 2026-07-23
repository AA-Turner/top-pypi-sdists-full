"""Greedy word-substitution evasion for text inputs.

A trigger pre-phase (append strong opposite-polarity words) is tried first -
cheap and very effective against bag-of-words / TF-IDF sentiment models - then a
leave-one-out importance scan followed by greedy word replacement.
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack
from dreadnode.airt.evasion._text_common import (
    greedy_substitute,
    importance_scan,
    make_flipped,
    text_setup,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput

# Sentiment-flipping substitution candidates (both polarities + negation +
# deletion). The greedy search picks whichever drives the original-class
# confidence down fastest, so it works whichever way the label needs to flip.
WORD_CANDIDATES = (
    "",
    "not",
    "terrible",
    "awful",
    "boring",
    "worst",
    "disappointing",
    "great",
    "excellent",
    "amazing",
    "wonderful",
    "best",
)


async def run(attack: ModelEvasionAttack) -> t.Any:
    text, orig_label, orig_cls, words, cur_conf = await text_setup(attack)
    current = list(words)
    curve: list[tuple[int, float]] = []

    # 0. Trigger phase: append strong opposite-polarity words. A few tokens often
    # flip the label without touching the original text.
    neg = ["terrible", "awful", "boring", "worst", "disappointing", "horrible", "waste"]
    pos = ["great", "excellent", "amazing", "wonderful", "masterpiece", "brilliant", "perfect"]
    for trigger in (neg, pos):
        for k in range(1, 13):
            if attack._over_budget():
                break
            added = trigger * k
            cand = text + " " + " ".join(added)
            p = (await attack._predict([cand]))[0]
            curve.append((attack._query_count, len(added) / max(len(words) + len(added), 1)))
            if attack._label(p) != orig_label:
                return make_flipped(
                    attack,
                    text,
                    cand,
                    orig_label,
                    attack._label(p),
                    len(added),
                    words + added,
                    curve,
                )

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


def text_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """Greedy word-substitution black-box evasion for text inputs. Flips the
    label with the fewest token edits; distance is the fraction of tokens
    changed."""
    return ModelEvasionAttack(strategy="text", target=target, original=original, **kwargs)
