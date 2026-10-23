"""A kind value in a BARE fence (```, no language label) is corrected like a ```json one.

The durable-text corrector only matched fences labelled json, so a model that fenced
its kind value without a label kept its own arithmetic in the stored answer. A bare
fence is corrected only when its content parses as JSON for a registered kind; any
other fence (prose, code in another language) is left exactly as written.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.processing.blocks import kind_correctors as kc

SLUG = "test_bare_fence_kind"


def _fix_total(value):
    total = sum(value.get("parts", []))
    if value.get("total") == total:
        return value, []
    return {**value, "total": total}, [f"total was {value.get('total')!r}; the parts give {total}"]


@pytest.fixture(autouse=True)
def _registered():
    kc.register_kind_corrector(SLUG, _fix_total)
    yield
    kc.unregister_kind_corrector(SLUG)


def _value(text: str, fence: str) -> dict:
    body = text.split(fence, 1)[1].split("```", 1)[0]
    return json.loads(body)


def test_a_bare_fence_is_corrected() -> None:
    text = "Here it is.\n```\n" + json.dumps({"__kind": SLUG, "parts": [1, 2], "total": 7}) + "\n```\nDone."
    out, notes = kc.correct_kind_regions_in_text(text)
    assert notes == ["total was 7; the parts give 3"]
    assert _value(out, "```\n")["total"] == 3
    assert out.startswith("Here it is.\n```\n") and out.endswith("\n```\nDone.")


def test_a_json_fence_still_is() -> None:
    text = "```json\n" + json.dumps({"__kind": SLUG, "parts": [2, 2], "total": 1}) + "\n```"
    out, notes = kc.correct_kind_regions_in_text(text)
    assert notes and _value(out, "```json\n")["total"] == 4


def test_other_fences_are_left_alone() -> None:
    value = json.dumps({"__kind": SLUG, "parts": [1], "total": 9})
    text = "Code:\n```python\nx = " + value + "\n```\n```\nnot json\n```"
    assert kc.correct_kind_regions_in_text(text) == (text, [])
