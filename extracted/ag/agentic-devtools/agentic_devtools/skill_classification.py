"""Classification reader for context-aware conditional skill injection.

Provides a ``Classification`` dataclass and three public functions:

- ``parse_classification(frontmatter)`` — defensively reads the ``agdt`` block
  from a frontmatter mapping and returns a ``Classification``.  Never raises,
  never mutates the input.
- ``should_inject(classification, *, issue_adapter, code_hosting)`` — pure
  predicate deciding whether a skill should be injected given resolved platform
  values.
- ``resolve_platform_context(platform)`` — maps a raw ``platform`` config
  section to the filter-capable ``(issue_adapter, code_hosting)`` axes to
  forward to injection.  Never raises, never mutates the input.
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from agentic_devtools.config import VALID_CODE_HOSTING, VALID_ISSUE_ADAPTERS

__all__ = ["Classification", "parse_classification", "resolve_platform_context", "should_inject"]


@dataclass(frozen=True)
class Classification:
    """Immutable classification extracted from skill frontmatter."""

    requires_issue_adapter: str | None = None
    requires_code_hosting: str | None = None
    always: bool = False


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

_TRUE_TOKENS: frozenset[str] = frozenset({"true", "yes", "on", "1"})
_FALSE_TOKENS: frozenset[str] = frozenset({"false", "no", "off", "0"})

# Filter-capable platform values.  Only these confidently-resolved values
# activate an injection axis; every other value — the non-filter-capable
# catch-alls (``markdown`` for issue_adapter, ``other`` for code_hosting), an
# absent key, a non-string value, or a non-mapping ``platform`` section — leaves
# that axis unrestricted (``None``), yielding legacy inject-all for that axis.
_FILTER_CAPABLE_ISSUE_ADAPTERS: frozenset[str] = frozenset({"jira", "github"})
_FILTER_CAPABLE_CODE_HOSTING: frozenset[str] = frozenset({"github", "azure_devops"})


def _coerce_always(value: Any) -> bool:
    """Coerce an ``always`` field value to bool using an explicit allowlist.

    Accepts native bools, integers 0/1, and case-insensitive string tokens.
    Unrecognized values emit a warning and resolve to ``False``.
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        warnings.warn(
            f"Unrecognized 'always' value {value!r}; defaulting to False.",
            stacklevel=3,
        )
        return False

    if isinstance(value, str):
        lower = value.lower()
        if lower in _TRUE_TOKENS:
            return True
        if lower in _FALSE_TOKENS:
            return False
        warnings.warn(
            f"Unrecognized 'always' value {value!r}; defaulting to False.",
            stacklevel=3,
        )
        return False

    warnings.warn(
        f"Unrecognized 'always' value {value!r}; defaulting to False.",
        stacklevel=3,
    )
    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_classification(frontmatter: Any) -> Classification:
    """Parse a ``Classification`` from a frontmatter mapping.

    This function is fully defensive:

    - Non-mapping *frontmatter* → universal, no warning.
    - Absent/None/empty ``agdt`` → universal, no warning.
    - Non-mapping ``agdt`` → universal, with warning.
    - Non-mapping ``requires`` → axes=None with warning, ``always`` preserved.
    - Invalid enum axis values → dropped per-axis with warning.

    The function never raises and never mutates *frontmatter*.
    """
    # Guard: non-mapping frontmatter (including None) → universal, no warning.
    if not isinstance(frontmatter, Mapping):
        return Classification()

    agdt = frontmatter.get("agdt")

    # Absent or None agdt → universal, no warning.
    if agdt is None:
        return Classification()

    # Empty mapping agdt → universal, no warning.
    if isinstance(agdt, Mapping) and not agdt:
        return Classification()

    # Non-mapping agdt → universal, with warning.
    if not isinstance(agdt, Mapping):
        warnings.warn(
            f"Expected 'agdt' to be a mapping, got {type(agdt).__name__!r}; returning universal classification.",
            stacklevel=2,
        )
        return Classification()

    # Parse 'always' (before requires, so it's preserved even if requires is bad).
    always = _coerce_always(agdt.get("always", False))

    # Parse 'requires' block.
    requires = agdt.get("requires")

    # Absent or None requires → axes unrestricted, no warning.
    if requires is None:
        return Classification(always=always)

    # Empty mapping requires → axes unrestricted, no warning.
    if isinstance(requires, Mapping) and not requires:
        return Classification(always=always)

    # Non-mapping requires → warning, axes=None, preserve always.
    if not isinstance(requires, Mapping):
        warnings.warn(
            f"Expected 'agdt.requires' to be a mapping, got {type(requires).__name__!r}; ignoring requires block.",
            stacklevel=2,
        )
        return Classification(always=always)

    # Validate each axis.
    issue_adapter: str | None = None
    raw_ia = requires.get("issue_adapter")
    if raw_ia is not None:
        if not isinstance(raw_ia, str) or raw_ia not in VALID_ISSUE_ADAPTERS:
            warnings.warn(
                f"Invalid issue_adapter value {raw_ia!r}; "
                f"valid options are {sorted(VALID_ISSUE_ADAPTERS)}. "
                "Dropping to unrestricted.",
                stacklevel=2,
            )
        else:
            issue_adapter = raw_ia

    code_hosting: str | None = None
    raw_ch = requires.get("code_hosting")
    if raw_ch is not None:
        if not isinstance(raw_ch, str) or raw_ch not in VALID_CODE_HOSTING:
            warnings.warn(
                f"Invalid code_hosting value {raw_ch!r}; "
                f"valid options are {sorted(VALID_CODE_HOSTING)}. "
                "Dropping to unrestricted.",
                stacklevel=2,
            )
        else:
            code_hosting = raw_ch

    return Classification(
        requires_issue_adapter=issue_adapter,
        requires_code_hosting=code_hosting,
        always=always,
    )


def should_inject(
    classification: Classification,
    *,
    issue_adapter: str | None = None,
    code_hosting: str | None = None,
) -> bool:
    """Decide whether a skill should be injected given resolved platform values.

    Rules (evaluated in order):

    1. ``always=True`` → always inject.
    2. Both platform args ``None`` → legacy inject-all.
    3. Per-axis: ``None`` platform arg = unrestricted for that axis.
    4. AND-combine non-None axes.
    """
    # Rule 1: always override.
    if classification.always:
        return True

    # Rule 2: legacy inject-all when platform is unresolved.
    if issue_adapter is None and code_hosting is None:
        return True

    # Rule 3 & 4: AND-combine axis checks.
    # A None platform arg means unrestricted (always passes for that axis).
    # A None requires_* means no constraint on that axis (always passes).
    if issue_adapter is not None and classification.requires_issue_adapter is not None:
        if issue_adapter != classification.requires_issue_adapter:
            return False

    if code_hosting is not None and classification.requires_code_hosting is not None:
        if code_hosting != classification.requires_code_hosting:
            return False

    return True


def resolve_platform_context(platform: Any) -> tuple[str | None, str | None]:
    """Resolve filter-capable ``(issue_adapter, code_hosting)`` from a platform config.

    Reads a *raw* ``platform`` config section (the value of the ``platform`` key
    in ``.github/agdt-config.json``) and returns the pair of resolved injection
    axes suitable for forwarding to :func:`inject_skills`.  Only
    *confidently-resolved, filter-capable* values activate an axis:

    - ``issue_adapter`` ∈ {``jira``, ``github``}
    - ``code_hosting`` ∈ {``github``, ``azure_devops``}

    Every other input leaves that axis unrestricted (``None``):

    - non-filter-capable catch-all values (``markdown`` for the adapter axis,
      ``other`` for the hosting axis),
    - absent keys,
    - non-string values, and
    - a non-mapping ``platform`` argument (including ``None``).

    A ``None`` axis means "inject-all for that axis"; when *both* axes are
    ``None`` injection is byte-identical to the legacy inject-all behavior.

    The function is pure: it never raises and never mutates *platform*.
    """
    if not isinstance(platform, Mapping):
        return None, None

    raw_adapter = platform.get("issue_adapter")
    issue_adapter = (
        raw_adapter if isinstance(raw_adapter, str) and raw_adapter in _FILTER_CAPABLE_ISSUE_ADAPTERS else None
    )

    raw_hosting = platform.get("code_hosting")
    code_hosting = raw_hosting if isinstance(raw_hosting, str) and raw_hosting in _FILTER_CAPABLE_CODE_HOSTING else None

    return issue_adapter, code_hosting
