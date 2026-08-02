"""Assistant vocabulary for a skill's ``assistants:`` frontmatter.

The canonical set of assistant ids a skill may target, the lenient frontmatter
reader, and the validator used by ``internal scan-skill``. Lives in ``common/``
so both ``install/`` (skill deployment) and ``internal/`` (skill scan) depend on
it downward, never the reverse.

The set is the single source of truth: ``install/``'s skill converters must stay
within it (guarded by a unit test), so a new converter cannot silently introduce
an assistant id the scanner would reject.
"""

from typing import Any

import yaml

VALID_ASSISTANTS = ("claude", "codex")

_DELIMITER = "---"


def _frontmatter_mapping(md_text: str) -> dict[str, Any]:
    """Return the parsed YAML frontmatter mapping, or ``{}`` when absent/malformed.

    Lenient by design: reading the ``assistants`` target of many skills must not crash on
    one odd file. Strict validation of the field lives in :func:`invalid_assistants`.
    """
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != _DELIMITER:
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == _DELIMITER), None)
    if end is None:
        return {}
    try:
        parsed = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def read_assistants(md_text: str) -> list[str] | None:
    """Return the ``assistants:`` list from a SKILL.md, or ``None`` when the field is
    absent (deploy to every assistant). A scalar value is wrapped in a single-item list.
    """
    value = _frontmatter_mapping(md_text).get("assistants")
    if value is None:
        return None
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return None


def invalid_assistants(md_text: str) -> list[str]:
    """Return the ``assistants:`` values that are not in :data:`VALID_ASSISTANTS`
    (empty when the field is absent or every value is known). Used by ``scan_skill``.
    """
    assistants = read_assistants(md_text)
    if assistants is None:
        return []
    return [a for a in assistants if a not in VALID_ASSISTANTS]
