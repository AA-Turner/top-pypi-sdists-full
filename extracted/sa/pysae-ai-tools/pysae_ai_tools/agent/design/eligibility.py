"""Auto-eligibility gate for the design lane: deterministic prefilter + Haiku classifier.

Replaces the *mandatory* manual `design::eligible` label. Two tiers, cheapest first:

1. **Deterministic prefilter (free)** — reject tickets with no UI signal, or with a
   custom-interaction keyword (drag-drop, livemap, animation, real-time, dataviz...).
   These are never "commodity" and must not burn an LLM call.
2. **Haiku classifier** — on what survives, judge whether the feature is a *commodity*
   UI (standard CRUD list / form / detail / tabs / modal) and how confident it is.
   Only `commodity AND confidence >= threshold` is eligible.

Manual labels stay as optional human overrides (the classifier is correctable):
- ``design::skip``     → never eligible (wins over everything)
- ``design::eligible`` → always eligible
"""

import json
import os
import re
from typing import Literal

from pydantic import BaseModel, Field

from ..models import Ticket
from ..score import _llm_client, _log_llm_usage, _strip_code_fences

OVERRIDE_IN = "design::eligible"
OVERRIDE_OUT = "design::skip"

_ELIGIBILITY_MODEL = os.environ.get("ANTHROPIC_DESIGN_ELIGIBILITY_MODEL", "claude-haiku-4-5")

# Custom / non-commodity interaction signals → never auto-eligible.
_CUSTOM_INTERACTION = re.compile(
    r"\b(drag[- ]?(and[- ]?)?drop|glisser[- ]?d[ée]poser|livemap|live[- ]?map|"
    r"carte\s+(interactive|temps\s+r[ée]el)|timeline|frise\s+chrono|gantt|kanban|"
    r"canvas|webgl|three\.js|animations?|anim[ée]e?s?|temps\s+r[ée]el|real[- ]?time|"
    r"websockets?|multi[- ]?step|multi[- ]?[ée]tapes|wizard|stepper|data[- ]?viz|"
    r"visualisations?|graphes?|charts?|courbes?|diagrammes?|signature\s+pad|"
    r"gestures?|swipe|infinite\s+scroll|virtualis)",
    re.IGNORECASE,
)

# Minimal UI signal: the ticket is about a screen / page / component.
_UI_SIGNAL = re.compile(
    r"\b(UI|[ée]crans?|screens?|pages?|interface|formulaires?|forms?|listes?|lists?|"
    r"table(au)?x?|modal(e|es)?|onglets?|tabs?|d[ée]tail|vue|front(end)?|"
    r"composants?|components?|maquettes?|design|sidebar|dashboard)\b|\.tsx|\.jsx",
    re.IGNORECASE,
)

EligibilitySource = Literal[
    "override-skip",
    "override-eligible",
    "deterministic-no-ui",
    "deterministic-custom-interaction",
    "llm-commodity",
    "llm-not-commodity",
    "llm-low-confidence",
]


class EligibilityAssessment(BaseModel):
    """Haiku's raw judgement on whether a ticket is a commodity UI feature."""

    commodity: bool
    confidence: int = Field(ge=0, le=100)
    reason: str


class EligibilityVerdict(BaseModel):
    """Final decision combining overrides, deterministic prefilter, and the LLM."""

    eligible: bool
    source: EligibilitySource
    confidence: int = 0
    reason: str


def _text(ticket: Ticket) -> str:
    return f"{ticket.title}\n{ticket.description or ''}"


def has_ui_signal(ticket: Ticket) -> bool:
    return bool(_UI_SIGNAL.search(_text(ticket)))


def has_custom_interaction(ticket: Ticket) -> bool:
    return bool(_CUSTOM_INTERACTION.search(_text(ticket)))


_PROMPT = (
    "You decide whether a GitLab ticket is a COMMODITY UI feature that an automated"
    " HTML-prototyping agent can mock faithfully without a human designer.\n\n"
    "TICKET:\nTitle: {title}\nLabels: {labels}\nDescription:\n{description}\n\n"
    "COMMODITY = standard, well-understood screens built from known patterns:"
    " CRUD lists, tables, forms, detail/read views, tab strips, modals, filters,"
    " empty/loading/error states. The solution space is settled; thousands of"
    " products solve it the same way.\n\n"
    "NOT COMMODITY = novel or custom UX: drag-and-drop, live maps, timelines,"
    " canvas/animation/real-time, data-visualisation, multi-step wizards with"
    " complex state, anything needing user research or a bespoke interaction.\n\n"
    "Output a JSON object with EXACTLY these keys:\n"
    "- commodity (bool): true only if it clearly fits the COMMODITY definition\n"
    "- confidence (int 0-100): how sure you are of the commodity verdict\n"
    "- reason (string, max 200 chars): one sentence justifying the call\n\n"
    "Be conservative: if the ticket is vague about the UI or mixes commodity"
    " screens with a custom interaction, lower the confidence. Output ONLY the"
    " JSON object, no preamble, no markdown fences."
)


def classify_with_llm(ticket: Ticket) -> EligibilityAssessment:
    """Call Haiku to classify commodity-ness + confidence."""
    prompt = _PROMPT.format(
        title=ticket.title,
        labels=", ".join(ticket.labels) or "(none)",
        description=(ticket.description or "(empty)")[:4000],
    )
    response = _llm_client().complete(
        model=_ELIGIBILITY_MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    _log_llm_usage(response.usage, caller="haiku-design-eligibility", model=_ELIGIBILITY_MODEL, ticket=ticket)
    data = json.loads(_strip_code_fences(response.text))
    return EligibilityAssessment.model_validate(data)


def assess_eligibility(ticket: Ticket, *, threshold: int = 70, skip_llm: bool = False) -> EligibilityVerdict:
    """Decide whether a ticket enters the design fast-path.

    Order (short-circuits, cheapest first): manual overrides → deterministic
    prefilter → Haiku classifier with a confidence threshold. The LLM is only
    called when no override and the prefilter passes.
    """
    labels = ticket.labels
    if OVERRIDE_OUT in labels:
        return EligibilityVerdict(eligible=False, source="override-skip", reason=f"label {OVERRIDE_OUT}")
    if OVERRIDE_IN in labels:
        return EligibilityVerdict(
            eligible=True, source="override-eligible", confidence=100, reason=f"label {OVERRIDE_IN}"
        )
    if not has_ui_signal(ticket):
        return EligibilityVerdict(
            eligible=False, source="deterministic-no-ui", reason="aucun signal UI (écran/page/composant)"
        )
    if has_custom_interaction(ticket):
        return EligibilityVerdict(
            eligible=False,
            source="deterministic-custom-interaction",
            reason="interaction custom détectée (hors commodity)",
        )
    if skip_llm:
        return EligibilityVerdict(
            eligible=True, source="llm-commodity", confidence=0, reason="déterministe seul (LLM ignoré)"
        )
    a = classify_with_llm(ticket)
    if not a.commodity:
        return EligibilityVerdict(
            eligible=False, source="llm-not-commodity", confidence=a.confidence, reason=a.reason[:200]
        )
    if a.confidence < threshold:
        return EligibilityVerdict(
            eligible=False,
            source="llm-low-confidence",
            confidence=a.confidence,
            reason=f"commodity mais confiance {a.confidence} < {threshold}: {a.reason[:150]}",
        )
    return EligibilityVerdict(eligible=True, source="llm-commodity", confidence=a.confidence, reason=a.reason[:200])
