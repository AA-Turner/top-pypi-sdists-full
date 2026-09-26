"""AGT-N-7's first case: an undeclared ``{{placeholder}}`` never survives silently.

THE DEFECT, IN ONE SENTENCE. ``{{name}}`` is substituted by a naive ``str.replace`` over
the declared variables, so a placeholder nobody declared is left in the prompt **exactly
as typed**, with no warning anywhere in the chain — the model reads two literal braces
and a word, and either echoes them at a person or quietly invents a value for them. A
declared variable with no value becomes ``""``, which is the same failure wearing
different clothes. DYNAMIC-VALUES §D names both, and CONTRACT.md `AGT-N-7` makes the
general law: *anything an agent could not deliver is named in its answer, never silently
omitted.*

WHAT THIS MODULE IS. The bookkeeping half — a per-turn record of every placeholder that
reached the end of substitution unresolved, written at the ONE choke point every
substituted string already passes through (``TextContent.replace_variables``), and read
once, at the top of the turn, by whoever assembles the prompt.

WHAT IT DELIBERATELY DOES NOT DO — and this is the part to read before "improving" it.
It does **not** rewrite the braces away. Substitution in this system is not one pass: a
picklist envelope, a staged reference-fence swap and the executor's send-clone each
resolve tokens at their own moment, and a pass that ate every unresolved brace on sight
would destroy the later ones and call the damage a fix. Naming is safe at any point;
erasing is not. So the placeholder stays, the turn learns its name, and the prompt
carries ONE sentence telling the model to say plainly that it was not delivered rather
than invent it.

The record is a :class:`contextvars.ContextVar`, so it follows the turn across
``asyncio`` tasks and two concurrent turns in one process never read each other's.
"""

from __future__ import annotations

import re
from contextvars import ContextVar

#: What a placeholder looks like after substitution has had its turn. Deliberately
#: NARROW: the identifier characters a variable name may carry and nothing else, so a
#: JSON object, a Jinja block or a Handlebars helper inside a prompt is not mistaken for
#: an undelivered value. A name with a dot is one (``assistant.email`` — declaring a
#: Reference merge field declares the whole record, DYNAMIC-VALUES §A).
PLACEHOLDER_RE = re.compile(r"\{\{\s*([A-Za-z0-9_][A-Za-z0-9_.\-]*)\s*\}\}")

_undelivered: ContextVar[dict[str, None] | None] = ContextVar(
    "matrx_ai_undelivered_placeholders", default=None
)


def begin_turn() -> None:
    """Start a fresh record for this turn. Safe to call more than once."""
    _undelivered.set({})


def note_unresolved(text: str, *, template: str | None = None) -> tuple[str, ...]:
    """Record every placeholder still standing in ``text`` and return their names.

    Called after substitution, with the substituted text. Returns the names it found so
    a caller that wants to act immediately can, without reading the whole record.

    ``template`` is the text BEFORE this substitution pass. When given, only a
    placeholder the template itself carried counts: braces that arrived INSIDE a
    substituted value are that value's content (a conversation about Handlebars, a
    case quoting ``{{name}}``), not something the prompt failed to deliver — naming
    them would tell the model to disclaim data it was handed in full.
    """
    if not text or "{{" not in text:
        return ()
    found = tuple(dict.fromkeys(m.group(1) for m in PLACEHOLDER_RE.finditer(text)))
    if template is not None:
        authored = {m.group(1) for m in PLACEHOLDER_RE.finditer(template)}
        found = tuple(name for name in found if name in authored)
    if not found:
        return ()
    record = _undelivered.get()
    if record is None:
        record = {}
        _undelivered.set(record)
    for name in found:
        record.setdefault(name, None)
    return found


def undelivered() -> tuple[str, ...]:
    """Every placeholder this turn could not deliver, in the order first seen."""
    record = _undelivered.get()
    return tuple(record) if record else ()


def omission_sentence(names: tuple[str, ...] | None = None) -> str | None:
    """The ONE sentence that goes into the prompt, or ``None`` when nothing is missing.

    It is written for the model to act on, not for a log: it says which names were not
    delivered, forbids inventing them, and tells the model to say so in its answer —
    which is `AGT-N-7` in the place where it can actually be obeyed.
    """
    names = undelivered() if names is None else names
    if not names:
        return None
    listed = ", ".join(f"{{{{{n}}}}}" for n in names)
    plural = "placeholders" if len(names) > 1 else "placeholder"
    return (
        f"NOT DELIVERED — the {plural} {listed} in the instructions above had no "
        "declared value, no resolved merge field and no fallback, so nothing was "
        "substituted for them and they are still written out literally. Do not guess "
        "what they were meant to contain and do not repeat them back as if they were "
        "content. If the answer depends on one of them, say plainly which one was not "
        "delivered and stop there."
    )


__all__ = [
    "PLACEHOLDER_RE",
    "begin_turn",
    "note_unresolved",
    "omission_sentence",
    "undelivered",
]
