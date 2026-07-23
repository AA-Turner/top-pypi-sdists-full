"""TextBugger (Li et al. 2019): hybrid character + word text evasion.

TextBugger generates five "bug" types on the important words - four character
edits (insert a space, delete, swap, substitute-with-visually-similar) plus a
word-level semantic substitution - and keeps whichever most lowers the
original-class confidence. Mixing sub-word typos with word swaps evades both
character-robust and word-robust defenses.
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

#: Visually-similar substitutions (homoglyph-style) for the substitute-C bug.
_HOMOGLYPH = {"o": "0", "l": "1", "e": "3", "a": "@", "s": "$", "i": "1"}


def _textbugger_bugs(word: str) -> list[str]:
    bugs: list[str] = []
    if len(word) >= 2:
        m = len(word) // 2
        bugs.append(word[:m] + " " + word[m:])  # insert: split with a space
        bugs.append(word[:m] + word[m + 1 :])  # delete a middle char
        if m + 1 < len(word):  # swap two adjacent chars
            s = list(word)
            s[m], s[m + 1] = s[m + 1], s[m]
            bugs.append("".join(s))
        for ch, sub in _HOMOGLYPH.items():  # substitute with a look-alike
            if ch in word:
                bugs.append(word.replace(ch, sub, 1))
                break
    bugs.extend(c for c in WORD_CANDIDATES if c)  # word-level semantic swap
    return [b for b in bugs if b and b != word]


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
        candidates=_textbugger_bugs,
    )


def textbugger_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """TextBugger (Li et al. 2019): hybrid character + word text evasion that
    mixes visual/typo bugs with semantic word swaps on the important words."""
    return ModelEvasionAttack(strategy="textbugger", target=target, original=original, **kwargs)
