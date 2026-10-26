"""THE ESCAPE ROUND TRIP (Arman, 2026-10-25): rule 6 turns ``{{!…}}`` back into exactly the token for
every sample the UI offers Escape on (rich-content ``canEscapeToken``), and leaves the rest as written.
One table for both: apps/shared/rich-content/src/editor/core/__fixtures__/escape-roundtrip.json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.config.template_substitution import substitute_authored

TABLE = Path(__file__).resolve().parents[3] / "apps/shared/rich-content/src/editor/core/__fixtures__/escape-roundtrip.json"
# Standalone (the package outside this monorepo): the UI's table is not there, so nothing to agree with.
SAMPLES = json.loads(TABLE.read_text())["samples"] if TABLE.exists() else []
pytestmark = pytest.mark.skipif(not TABLE.exists(), reason="the UI's escape table lives in the aidream monorepo")


@pytest.mark.parametrize(("token", "escapable"), SAMPLES)
def test_escape_roundtrip_matches_the_ui(token: str, escapable: bool) -> None:
    escaped = "{{!" + token[2:]
    out = substitute_authored(escaped, escaped, {}, str, unescape=True)
    assert out == (token if escapable else escaped)
