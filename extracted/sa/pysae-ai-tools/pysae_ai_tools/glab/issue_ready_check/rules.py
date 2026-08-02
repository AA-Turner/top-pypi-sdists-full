"""Structural rules for the AC gate.

Per-type required sections + checkboxes. Reuses common.glab.templates for
section extraction so behaviour is consistent with glab issue-audit.
"""

import re
import unicodedata
from collections.abc import Iterable

from ...common.glab.templates import (
    Section,
    extract_sections,
    find_section,
    is_placeholder_only,
    strip_heading_emojis,
)
from .models import (
    CheckboxViolation,
    ReadyCheckResult,
    SectionViolation,
    TicketType,
    Violation,
)

_TYPE_LABEL_MAP: dict[str, TicketType] = {
    "type::feature": TicketType.FEATURE,
    "type::bug": TicketType.BUG,
    "type::technical": TicketType.TECHNICAL,
    "type::debt": TicketType.TECHNICAL,
}

_PREP_CHECKBOX_LABELS = (
    "Le **contexte** est clairement défini",
    "Les **spécifications** sont complètes et compréhensibles",
    "Les **critères d'acceptation** sont rédigés et validés",
)

_PREP_TECH_CHECKBOX_LABELS = (
    "Le **contexte** est clairement défini",
    "La **description technique** est complète et compréhensible",
    "Les **critères d'acceptation** sont rédigés et validés",
)

# Each slot is a tuple of accepted heading synonyms. A slot is satisfied
# if any synonym matches a heading, either by exact normalised equality or
# by token-prefix (so "Fix" matches "Fix 1 - persistance ..." and
# "Root Cause" matches "Root Cause - timeline lockup"). The first synonym
# in each tuple is the canonical FR name reported in violations.
_REQUIRED_SECTIONS: dict[TicketType, tuple[tuple[str, ...], ...]] = {
    TicketType.FEATURE: (
        ("Contexte", "Context", "Background", "Overview"),
        ("Spécifications", "Specifications", "Specs", "Scope", "Plan", "Approach", "Design", "Implementation", "Fix"),
        (
            "Critères d'acceptation",
            "Acceptance Criteria",
            "Acceptance",
            "Definition of Done",
            "DoD",
            "Tests",
            "Validation",
        ),
    ),
    TicketType.TECHNICAL: (
        ("Contexte", "Context", "Background", "Overview"),
        (
            "Description technique",
            "Technical Description",
            "Scope",
            "Plan",
            "Approach",
            "Design",
            "Implementation",
            "Fix",
        ),
        (
            "Critères d'acceptation",
            "Acceptance Criteria",
            "Acceptance",
            "Definition of Done",
            "DoD",
            "Tests",
            "Validation",
        ),
    ),
    TicketType.BUG: (
        ("Contexte", "Context", "Background", "Overview"),
        ("Étapes pour reproduire", "Steps to Reproduce", "Reproduction", "Root Cause"),
        ("Résultat attendu", "Expected", "Expected Result", "Fix"),
        ("Résultat observé", "Observed", "Actual", "Root Cause", "Bug"),
    ),
}


def _normalise_heading(text: str) -> str:
    no_accents = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", no_accents.lower()).strip()


def _find_required_section(description: str, synonyms: tuple[str, ...]) -> tuple[Section, str] | None:
    """Find a section matching any synonym; return it with its effective body.

    The effective body absorbs deeper subsections (e.g. H3 under an H2) so
    that a parent heading with empty body but rich subsection content isn't
    flagged as placeholder.
    """
    sections = extract_sections(description)
    for name in synonyms:
        target_tokens = _normalise_heading(strip_heading_emojis(name)).split()
        if not target_tokens:
            continue
        for idx, section in enumerate(sections):
            heading_tokens = section.normalised.split()
            if heading_tokens[: len(target_tokens)] == target_tokens:
                body_parts = [section.body]
                for sub in sections[idx + 1 :]:
                    if sub.level <= section.level:
                        break
                    body_parts.append(sub.body)
                return section, "\n".join(p for p in body_parts if p)
    return None


def detect_type(labels: Iterable[str]) -> TicketType:
    for label in labels:
        if label in _TYPE_LABEL_MAP:
            return _TYPE_LABEL_MAP[label]
    return TicketType.UNKNOWN


def _check_sections(description: str, ttype: TicketType) -> list[Violation]:
    violations: list[Violation] = []
    for synonyms in _REQUIRED_SECTIONS.get(ttype, ()):
        primary = synonyms[0]
        found = _find_required_section(description, synonyms)
        if found is None:
            violations.append(SectionViolation(section=primary, reason="section absente"))
            continue
        _, effective_body = found
        if is_placeholder_only(effective_body):
            violations.append(
                SectionViolation(
                    section=primary,
                    reason="ne contient que le texte de placeholder du template",
                )
            )
    return violations


def _check_prep_checkboxes(description: str, ttype: TicketType) -> list[Violation]:
    if ttype is TicketType.BUG:
        return []
    section = find_section(description, "Préparation au développement")
    if section is None:
        # Optional: trust the required Context/Spec/AC sections to cover quality
        return []
    labels: tuple[str, ...]
    if ttype is TicketType.TECHNICAL:
        labels = _PREP_TECH_CHECKBOX_LABELS
    else:
        labels = _PREP_CHECKBOX_LABELS
    violations: list[Violation] = []
    body = section.body
    for label in labels:
        pattern = re.compile(
            r"-\s*\[\s*[xX]\s*\]\s*" + re.escape(label),
        )
        if not pattern.search(body):
            violations.append(CheckboxViolation(checkbox=label, reason="non cochée ou absente"))
    return violations


def evaluate_ticket(
    description: str,
    labels: Iterable[str],
) -> ReadyCheckResult:
    ttype = detect_type(labels)
    if ttype is TicketType.UNKNOWN:
        return ReadyCheckResult(
            ready=False,
            type=ttype,
            violations=[
                SectionViolation(
                    section="type",
                    reason="aucun label type::* présent sur le ticket",
                )
            ],
        )

    violations: list[Violation] = []
    violations.extend(_check_sections(description, ttype))
    violations.extend(_check_prep_checkboxes(description, ttype))

    return ReadyCheckResult(
        ready=not violations,
        type=ttype,
        violations=violations,
    )
