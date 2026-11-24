"""FORCING GUARD — the three text spans the live residual check reported (2026-11-15) are registered.

Each case builds the text with its REAL producer and runs the residual check with NOTHING known
(no config text): a registered block's frame is the only thing that can account for it. Red before
the frames were registered, green after. Self-test: a planted sentence in the same part is the
whole residual, so the frames do not swallow what they do not own.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers import residual_check
from matrx_ai.config.platform_parts import BLOCKS, PLATFORM_PARTS

HELPERS_TEXT = "\n".join(
    [
        '<your_helpers source="platform">',
        "The helper agents you started in this conversation, as of when this list was written "
        "(2 in all, 1 running). A later copy of this list replaces this one: trust the latest copy "
        "over anything you remember.",
        "- h1 (running) researcher: reading the docs",
        "  - (its own helpers could not be read just now)",
        "</your_helpers>",
    ]
)


def _grounded() -> str:
    from matrx_ai.providers.google.translator import GoogleTranslator

    return GoogleTranslator._grounded_json_text_contract({"type": "object", "properties": {"a": {"type": "string"}}})


def _label(name: str | None, *, file_id: str = "5414f980-aaaa-bbbb-cccc-111122223333") -> str:
    from matrx_ai.config.message_config import _media_identity_label
    from matrx_ai.config.unified_content import ImageContent

    part = ImageContent(url="https://x.invalid/a.jpg", file_id=file_id, metadata={"file_name": name} if name else {})
    label = _media_identity_label(part, "user")
    assert label and label.startswith("<attachment kind=")
    return label


def _anthropic(system: list[str], user: list[str]) -> dict[str, Any]:
    return {
        "system": [{"type": "text", "text": t} for t in system],
        "messages": [{"role": "user", "content": [{"type": "text", "text": t} for t in user]}],
    }


TYPED = "Please look at this picture."


def _residual(shape: str, body: dict[str, Any], *, via_worker_patterns: bool) -> list[tuple[str, str]]:
    patterns = residual_check.platform_patterns() if via_worker_patterns else None
    return residual_check.residual_of(shape, body, [TYPED], patterns=patterns)


@pytest.mark.parametrize("via_worker_patterns", [False, True], ids=["server", "worker"])
def test_the_helper_roster_block_is_accounted_for(via_worker_patterns: bool) -> None:
    body = _anthropic(["x"], [HELPERS_TEXT])
    assert _residual(fos.SHAPE_ANTHROPIC, body, via_worker_patterns=via_worker_patterns) == []
    assert "helpers" in BLOCKS and "helpers" in PLATFORM_PARTS


@pytest.mark.parametrize("via_worker_patterns", [False, True], ids=["server", "worker"])
def test_the_grounded_json_contract_is_accounted_for(via_worker_patterns: bool) -> None:
    text = _grounded()
    assert len(text) > 500
    body = {"contents": [{"role": "user", "parts": [{"text": "hi"}]}], "systemInstruction": {"parts": [{"text": text}]}}
    got = _residual(fos.SHAPE_GOOGLE, body, via_worker_patterns=via_worker_patterns)
    assert [g for g in got if g[0].startswith("system")] == []
    assert "grounded_json_contract" in PLATFORM_PARTS


@pytest.mark.parametrize("via_worker_patterns", [False, True], ids=["server", "worker"])
@pytest.mark.parametrize(
    "name",
    [
        "2026, 07:33.jpg",  # the live name: a comma and a colon
        'say "hi" & <b>.png',  # every character html-escape rewrites
        "it's a 'quoted' name.png",
        "line break and ünïcode 日本語.jpg",
        None,  # no name: the label says name_unavailable
    ],
)
def test_every_attachment_label_form_is_accounted_for(name: str | None, via_worker_patterns: bool) -> None:
    label = _label(name)
    body = _anthropic(["x"], [TYPED, label])
    assert _residual(fos.SHAPE_ANTHROPIC, body, via_worker_patterns=via_worker_patterns) == [], label


def test_the_not_resent_and_document_label_forms_are_accounted_for() -> None:
    for text in (
        '<attachment kind="image" name="2026, 07:33.jpg" not_resent="assistant turn"/>',
        '<attachment kind="document" name="a, b: c.pdf" id="abc" sent="in the next user turn"/>',
    ):
        assert _residual(fos.SHAPE_ANTHROPIC, _anthropic(["x"], [text]), via_worker_patterns=True) == [], text


def test_the_frames_do_not_swallow_text_they_do_not_own() -> None:
    plant = "Planted platform sentence that no registered block accounts for."
    for texts in (
        [HELPERS_TEXT + "\n" + plant],
        [_label("2026, 07:33.jpg") + " " + plant],
        [plant + " " + _label("a.jpg")],
        [_label("a.jpg")[:-2] + "/> " + plant + " " + _label("b.jpg")],
        [_label("a.jpg") + " " + plant + " />"],
    ):
        got = _residual(fos.SHAPE_ANTHROPIC, _anthropic(["x"], texts), via_worker_patterns=True)
        assert got and plant in got[0][1], got
    got = residual_check.residual_of(
        fos.SHAPE_GOOGLE,
        {"contents": [{"role": "user", "parts": [{"text": "hi"}]}], "systemInstruction": {"parts": [{"text": _grounded() + "\n" + plant}]}},
        [],
    )
    assert got and plant in got[0][1]
