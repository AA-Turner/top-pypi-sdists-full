"""Exception-complete decoding of untrusted text.

``json5.loads``, ``json.loads``, ``yaml.safe_load`` and ``tomllib.loads`` are
all recursive and raise ``RecursionError`` (a ``RuntimeError``, not a
``ValueError``) on deeply nested input. A reader that catches only the
documented decode errors lets that escape and takes its whole scan phase down
with it, so one crafted file on disk empties every sibling finding. Every scan
reader of untrusted text decodes through this module so the failure set is
owned in one place. The same hazard applies to hook-path decoders (transcript
lines, MCP config files, the flow spool, the hook payload itself), which
decode through here too.

``plistlib.loads`` is worse: its failure set cannot be enumerated. The binary
reader wraps every malformed input in ``InvalidFileException``, but the XML
reader's element handlers leak whatever they trip over: a non-numeric
``<integer>`` raises bare ``ValueError``, ``<date>invalid</date>`` raises
``AttributeError`` from ``_date_from_string``, a ``<key>`` outside any
``<dict>`` raises ``IndexError``, and malformed markup raises
``xml.parsers.expat.ExpatError``. Each new shape found is another class, so
``parse_plist`` treats every ``Exception`` as a decode failure and re-raises
only ``MemoryError``.

Module top is stdlib-only (``json`` + typing). ``json5``, ``yaml``,
``tomllib``/``tomli`` and ``plistlib`` are imported inside the ``parse_*``
that needs them: this module sits in the ``aiwatch hook`` hot path and in the
stdlib-only ``flow_*`` closure (cli/AGENTS.md import-budget rules, guarded by
``tests/test_aiwatch_imports.py``), so an eager ``yaml`` import here would be
paid by every hook fire and would break the flow-spool closure.

Lives at the package root, not under ``runlayer_cli.scan``: ``scan/__init__``
imports the whole scan graph, and leaf modules the graph depends on (such as
``runlayer_cli.plugins.claude_manifest``) also decode untrusted text, so a
``scan``-rooted home would make them import their own importer.
"""

from __future__ import annotations

import json
import sys
from typing import Any, TypedDict

# Every exception a decoder may raise on hostile-but-not-catastrophic input.
# ``MemoryError`` is deliberately absent: bounded reads guard input size and a
# true allocation failure should surface, not be logged away.
#
# ``json.JSONDecodeError``, ``tomllib.TOMLDecodeError`` (stdlib and ``tomli``),
# ``plistlib.InvalidFileException`` and ``UnicodeDecodeError`` are all
# ``ValueError`` subclasses. ``yaml.YAMLError`` is not; ``parse_yaml`` adds it
# locally so the module top stays free of the ``yaml`` import.
PARSE_ERRORS: tuple[type[Exception], ...] = (
    ValueError,
    TypeError,
    RecursionError,
)


class ParseOutcome(TypedDict):
    """Decoded document (``None`` on failure), or the reason decoding failed.

    ``value`` is ``Any`` because a decoded document has whatever shape the
    file had; callers narrow with ``isinstance`` exactly as they did against
    the raw decoders.
    """

    value: Any
    error: str | None


def _outcome(value: Any) -> ParseOutcome:
    return {"value": value, "error": None}


def _failure(exc: Exception) -> ParseOutcome:
    return {"value": None, "error": f"{type(exc).__name__}: {exc}"}


def parse_json5(text: str) -> ParseOutcome:
    """Decode JSON/JSONC/JSON5 text without raising."""
    import json5

    try:
        return _outcome(json5.loads(text))
    except PARSE_ERRORS as exc:
        return _failure(exc)


def parse_json(text: str | bytes) -> ParseOutcome:
    """Decode strict JSON text without raising."""
    try:
        return _outcome(json.loads(text))
    except PARSE_ERRORS as exc:
        return _failure(exc)


def parse_yaml(text: str) -> ParseOutcome:
    """Decode a YAML document with the safe loader without raising."""
    import yaml

    try:
        return _outcome(yaml.safe_load(text))
    except (*PARSE_ERRORS, yaml.YAMLError) as exc:
        return _failure(exc)


def parse_toml(text: str) -> ParseOutcome:
    """Decode TOML text without raising."""
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib

    try:
        return _outcome(tomllib.loads(text))
    except PARSE_ERRORS as exc:
        return _failure(exc)


def parse_plist(raw: bytes) -> ParseOutcome:
    """Decode an XML or binary property list without raising.

    Broader than the other decoders on purpose: see the module docstring for
    why plistlib's XML handlers have no enumerable failure set.
    """
    import plistlib

    try:
        return _outcome(plistlib.loads(raw))
    except MemoryError:
        raise
    except Exception as exc:
        return _failure(exc)
