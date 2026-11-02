"""THE ALL-ZERO ANSWER — schema-valid, semantically empty, and never a success.

WHY THIS EXISTS
---------------
Live 2026-09-12, run ``9347de24…`` of the Watson Parenting Adviser: the
prescriber step received a complete, correct input (the parent's whole
account, the age band, the cause in the handling, the governing rules with
real ids, the routine faults) and answered, in 93 output tokens, with this::

    {"stop_doing": [], "not_covered": [], "instructions": [],
     "physician_note": null, "expected_course": "", "physician_first": false,
     "headline_finding": "", "all_cited_rule_ids": [],
     "methods_that_will_not_work": []}

Every field at its zero value. The provider-enforced schema was satisfied,
so the contract check passed, the step SUCCEEDED, the run COMPLETED, and the
parent was shown that object beside a full letter. Nothing screamed. The
letter-writing agent downstream even wrote around the hole ("Where the
regime I have set down for you does not speak, I have left it silent").

A schema says what SHAPE an answer has. It cannot say that the answer has
CONTENT. ``{"instructions": []}`` is a perfectly valid regimen with no
regimen in it, and handing that to a person as a completed answer is the
"nothing fails silently / a screen never lies" defect in its purest form.

WHAT COUNTS AS ZERO
-------------------
``None``, ``""`` (and all-whitespace), ``[]``, ``{}``, ``False``, and ``0``
— the value a field has when the model declined to fill it. ``__kind`` is
never counted: a marker is identity, not content.

WHAT THIS IS NOT
----------------
It is not a content-quality judge. ONE field carrying anything at all makes
the object non-empty; this only names the answer that carries NOTHING. And
some steps are legitimately empty ("no issues found") — which is why the
verdict is a fact the caller acts on under its own knob, never a raise from
here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: The marker key is identity, not content — an object carrying only its
#: ``__kind`` is still an empty object.
_IDENTITY_KEYS: frozenset[str] = frozenset({"__kind"})


def is_zero_value(value: Any) -> bool:
    """Whether one field's value is the value it has when nothing was said."""
    if value is None or value is False:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list | tuple | set | dict):
        return len(value) == 0
    if isinstance(value, int | float):
        return value == 0
    return False


@dataclass(frozen=True, slots=True)
class EmptyVerdict:
    """An answer whose every considered field is at its zero value.

    ``fields`` are the field names that were considered (all of them zero);
    ``considered`` says whether the declared schema's ``required`` list chose
    them or the object's own keys did — the sentence a human reads says which.
    """

    fields: tuple[str, ...]
    considered: str  # "required" | "present"

    def sentence(self, *, what: str = "object") -> str:
        return (
            f"the model returned an empty but valid {what}; nothing to deliver — "
            f"every {'required ' if self.considered == 'required' else ''}field "
            f"came back at its zero value (empty, null, false or blank): "
            f"{', '.join(self.fields)}"
        )


def _required_field_names(schema: Any) -> tuple[str, ...]:
    """The declared schema's ``required`` names, unwrapping the wire envelopes.

    Accepts the bare JSON Schema object, the OpenAI ``json_schema`` inner
    envelope (``{"name": …, "schema": {...}}``), and the full
    ``response_format`` (``{"type": "json_schema", "json_schema": {...}}``) —
    the three shapes a step's declared contract actually travels in.
    """
    if not isinstance(schema, dict):
        return ()
    inner = schema.get("json_schema")
    if isinstance(inner, dict):
        return _required_field_names(inner)
    body = schema.get("schema")
    if isinstance(body, dict):
        return _required_field_names(body)
    required = schema.get("required")
    if not isinstance(required, list):
        return ()
    return tuple(str(name) for name in required if isinstance(name, str) and name)


def empty_structured_output(value: Any, *, schema: Any = None) -> EmptyVerdict | None:
    """The verdict on one structured answer: ``EmptyVerdict`` or ``None``.

    ``None`` means "this carries something", and is ALSO the answer whenever
    the question does not apply — a scalar, a shape with no field to consider,
    anything this cannot read. A detector that guesses is worse than one that
    stays quiet: only an object (or list) whose every considered field is zero
    is ever named.

    The declared ``schema``'s ``required`` fields are the fields considered
    when it has any — those are the ones the step PROMISED — falling back to
    the object's own keys otherwise. An empty root list is empty by itself.
    """
    if isinstance(value, list):
        return EmptyVerdict(fields=(), considered="present") if not value else None
    if not isinstance(value, dict):
        return None

    names = tuple(n for n in _required_field_names(schema) if n in value)
    considered = "required"
    if not names:
        names = tuple(k for k in value if k not in _IDENTITY_KEYS)
        considered = "present"
    if not names:
        # Nothing to judge (an object with only its marker, or none at all).
        # Deliberately NOT a verdict: see the module docstring.
        return None

    if all(is_zero_value(value[name]) for name in names):
        return EmptyVerdict(fields=names, considered=considered)
    return None


def zero_valued_keys(payload: Any) -> tuple[str, ...]:
    """Top-level keys of ``payload`` whose value is an ALL-ZERO structure.

    What a delivery step needs to know: not "is the whole envelope empty" but
    "which of the things I am about to show a person is a hollow shell". In
    the live incident the envelope carried a real letter under
    ``watsons_words`` and an all-zero object under ``the_regimen`` — an
    envelope-level check would have called that fine.
    """
    if not isinstance(payload, dict):
        return ()
    return tuple(
        key
        for key, value in payload.items()
        if key not in _IDENTITY_KEYS
        and isinstance(value, dict | list)
        and empty_structured_output(value) is not None
    )
