"""Shared helpers used by more than one ecosystem parser.

Kept tiny and dependency-free (standard library plus the RE2 ``regex_safe``
wrapper) so each ecosystem module
can import it without pulling in the others.
"""

from __future__ import annotations

from runlayer_cli import regex_safe

_PEP508_NAME = regex_safe.compile(r"^[A-Za-z0-9._-]+")


def pep508_name(spec: str) -> str | None:
    """Extract the bare package name from a PEP 508 requirement string."""
    spec = spec.strip()
    if not spec or spec.startswith("#"):
        return None
    match = _PEP508_NAME.match(spec)
    return match.group(0) if match else None


def local_tag(tag: str) -> str:
    """Strip an XML namespace from a tag, e.g. ``{ns}dependency`` -> ``dependency``."""
    return tag.rsplit("}", 1)[-1]
