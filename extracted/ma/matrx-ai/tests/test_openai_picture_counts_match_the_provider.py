"""WHAT IS COUNTED IS WHAT IS SENT, AND WHAT OPENAI COUNTS (CGU-10 IMG7 #1, 2026-11-11).

Live, one 2,048² picture: gpt-5-nano was estimated at ~124 tokens and OpenAI counted 6,169 (50x under:
a picture-heavy chat passes the fit, then the provider refuses it); gpt-5.4-nano ~10,116 against 3,026
(3.3x over: compaction or a refusal for nothing). Two causes: the wire sent no ``detail`` (OpenAI applied
``auto``) while the estimate assumed the class's hint, and the per-model rules were wrong.

``PROVIDER`` below is OpenAI's OWN count (``POST /v1/responses/input_tokens``: a prompt with the picture
minus its text-only twin), measured 2026-11-11 for every size and detail. Each must be reproduced to the
token. The three checker figures are inside it: gpt-5.5 auto 2,048² = 4,916 (live 4,946 with the gpt-5.5
text twin), gpt-5.4-nano auto = 3,001 (live 3,026), gpt-5-nano = 6,144 (live 6,169).

What each test is FOR:
* a rule drifts from the provider (multiplier, cap, box, tile price) → ``test_every_measured_count``;
* the translator stops sending ``detail`` → ``test_the_wire_sends_the_detail_the_estimate_counts``;
* the estimate stops reading the sent detail or the picture's own encoding class →
  ``test_the_estimate_counts_the_sent_detail`` / ``test_a_picture_encoded_upstream_is_counted_as_sent``.
"""

from __future__ import annotations

import pytest

from matrx_ai.knobs import configure_package_knobs
from matrx_ai.processing.vision import image_tokens as it

# (model, width, height) -> {detail ("none" = not sent): OpenAI's own count}
PROVIDER: dict[tuple[str, int, int], dict[str, int]] = {
    ("gpt-5.5", 2048, 2048): {"none": 4916, "auto": 4916, "low": 308, "high": 3001, "original": 4916},
    ("gpt-5.4", 2048, 2048): {"none": 3001, "auto": 3001, "low": 4916, "high": 3001, "original": 4916},
    ("gpt-5.4-mini", 2048, 2048): {"none": 3001, "low": 4916, "high": 3001, "original": 4916},
    ("gpt-5.4-nano", 2048, 2048): {"none": 3001, "auto": 3001, "low": 4916, "high": 3001, "original": 4916},
    ("gpt-5.2", 2048, 2048): {"none": 4916, "low": 4916, "high": 4916, "original": 4916},
    ("gpt-5", 2048, 2048): {"none": 630, "auto": 630, "low": 70, "high": 630, "original": 630},
    ("gpt-5-mini", 2048, 2048): {"none": 4916, "auto": 4916, "low": 4916, "high": 4916, "original": 4916},
    ("gpt-5-nano", 2048, 2048): {"none": 6144, "auto": 6144, "low": 6144, "high": 6144, "original": 6144},
    ("gpt-4o", 2048, 2048): {"none": 765, "auto": 765, "low": 85, "high": 765, "original": 765},
    ("gpt-4.1", 2048, 2048): {"none": 765, "low": 85, "high": 765, "original": 765},
    ("gpt-4.1-mini", 2048, 2048): {"none": 6636, "low": 6636, "high": 6636, "original": 6636},
    ("o3", 2048, 2048): {"none": 675, "low": 75, "high": 675, "original": 675},
    ("gpt-5.5", 512, 512): {"none": 308, "low": 308, "high": 308, "original": 308},
    ("gpt-5.4", 512, 512): {"none": 308, "low": 308, "high": 308, "original": 308},
    ("gpt-5", 512, 512): {"none": 210, "low": 70, "high": 210, "original": 210},
    ("gpt-5-mini", 512, 512): {"none": 308, "low": 308, "high": 308, "original": 308},
    ("gpt-5-nano", 512, 512): {"none": 384, "low": 384, "high": 384, "original": 384},
    ("gpt-5.5", 1024, 768): {"none": 922, "low": 231, "high": 922, "original": 922},
    ("gpt-5.4", 1024, 768): {"none": 922, "low": 922, "high": 922, "original": 922},
    ("gpt-5", 1024, 768): {"none": 630, "low": 70, "high": 630, "original": 630},
    ("gpt-5-nano", 1024, 768): {"none": 1152, "low": 1152, "high": 1152, "original": 1152},
    ("gpt-5.5", 1568, 1568): {"none": 2882, "low": 308, "high": 2882, "original": 2882},
    ("gpt-5.4-nano", 1568, 1568): {"none": 2882, "low": 2882, "high": 2882, "original": 2882},
    ("gpt-5-nano", 1568, 1568): {"none": 3602, "low": 3602, "high": 3602, "original": 3602},
    ("gpt-5.5", 3000, 3000): {"none": 10604, "low": 308, "high": 3001, "original": 10604},
    ("gpt-5.4", 3000, 3000): {"none": 3001, "low": 4916, "high": 3001, "original": 10604},
    ("gpt-5-mini", 3000, 3000): {"none": 4916, "low": 4916, "high": 4916, "original": 4916},
    ("gpt-5-nano", 3000, 3000): {"none": 6144, "low": 6144, "high": 6144, "original": 6144},
    ("gpt-5.5", 4000, 1000): {"none": 4801, "low": 77, "high": 1229, "original": 4801},
    ("gpt-5.4", 4000, 1000): {"none": 1229, "low": 1229, "high": 1229, "original": 4801},
    ("gpt-5.4-mini", 4000, 1000): {"none": 1229, "low": 1229, "high": 1229, "original": 4801},
    ("gpt-5.2", 4000, 1000): {"none": 1229, "low": 1229, "high": 1229, "original": 1229},
    ("gpt-5", 4000, 1000): {"none": 630, "low": 70, "high": 630, "original": 630},
    ("gpt-5-nano", 4000, 1000): {"none": 1536, "low": 1536, "high": 1536, "original": 1536},
    ("gpt-4.1", 4000, 1000): {"none": 765, "low": 85, "high": 765, "original": 765},
    ("gpt-4.1-mini", 4000, 1000): {"none": 1659, "low": 1659, "high": 1659, "original": 1659},
    ("o3", 4000, 1000): {"none": 675, "low": 75, "high": 675, "original": 675},
    ("gpt-5.5", 64, 64): {"none": 5, "low": 5, "high": 5, "original": 5},
    ("gpt-5", 64, 64): {"none": 210, "low": 70, "high": 210, "original": 210},
    ("gpt-5-nano", 64, 64): {"none": 6, "low": 6, "high": 6, "original": 6},
}

_CASES = [
    pytest.param(model, w, h, detail, count, id=f"{model}-{w}x{h}-{detail}")
    for (model, w, h), row in PROVIDER.items()
    for detail, count in row.items()
]


@pytest.fixture(autouse=True)
def _no_host_knobs():
    configure_package_knobs(None)
    yield
    configure_package_knobs(None)


@pytest.mark.parametrize(("model", "width", "height", "detail", "count"), _CASES)
def test_every_measured_count(model: str, width: int, height: int, detail: str, count: int) -> None:
    sent = None if detail == "none" else detail
    assert it.openai_picture_tokens(width, height, model, sent) == count


def test_the_wire_sends_the_detail_the_estimate_counts() -> None:
    from matrx_ai.providers.openai.translator import _stamp_image_detail

    for model, expected in (("gpt-5.5", "original"), ("gpt-5.4-nano", "original"), ("gpt-5", "high"),
                            ("gpt-5-nano", "low"), ("gpt-4o", "high")):
        items = [
            {"role": "user", "content": [{"type": "input_text", "text": "x"},
                                          {"type": "input_image", "image_url": "data:image/jpeg;base64,AA"}]},
            {"type": "function_call_output", "output": [{"type": "input_image", "image_url": "https://x/y.png"}]},
            {"role": "user", "content": [{"type": "input_image", "image_url": "u", "detail": "low"}]},
        ]
        _stamp_image_detail(items, model, "openai_chat")
        assert items[0]["content"][1]["detail"] == expected == it.openai_image_detail(model, "openai_chat")
        assert items[1]["output"][0]["detail"] == expected, "a tool output's picture went without detail"
        assert items[2]["content"][0]["detail"] == "low", "an explicit detail was overwritten"


def test_a_non_openai_wire_gets_no_detail() -> None:
    from matrx_ai.providers.openai.translator import _stamp_image_detail

    items = [{"type": "input_image", "image_url": "u"}]
    _stamp_image_detail(items, "claude-haiku-5-5", "anthropic_chat")
    assert "detail" not in items[0]
    assert it.openai_image_detail("gemini-3-flash", "google_chat") is None


def test_the_detail_is_a_knob() -> None:
    configure_package_knobs(lambda feature, key: {"gpt-5.4": "high"} if (feature, key) == (
        it.OPENAI_DETAIL_FEATURE, it.OPENAI_DETAIL_KEY) else None)
    assert it.openai_image_detail("gpt-5.4-nano", "openai_chat") == "high"
    assert it.openai_image_detail("gpt-5.5", "openai_chat") == "original"
    content = _picture(2048, 2048)
    assert it.image_content_tokens(content, model="gpt-5.4-nano", wire_format="openai_chat") == 3001


def _picture(width: int, height: int, vision_class: str | None = None):
    from matrx_ai.config.media_config import ImageContent

    picture = ImageContent(url="https://example.invalid/p.jpg", mime_type="image/jpeg")
    picture.width, picture.height = width, height  # type: ignore[attr-defined]
    if vision_class:
        picture.vision_class = vision_class  # type: ignore[attr-defined]
    return picture


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        ("gpt-5.5", 4916),  # original (the class's detail), 2,048 edge
        ("gpt-5.4-nano", 4916),  # original, sent explicitly now
        ("gpt-5", 630),  # tiles 70 / 140
        ("gpt-5-nano", 384),  # its class re-encodes to 512²; detail ignored, x1.5
    ],
)
def test_the_estimate_counts_the_sent_detail(model: str, expected: int) -> None:
    content = _picture(2048, 2048)
    assert it.image_content_tokens(content, model=model, wire_format="openai_chat") == expected


def test_a_picture_encoded_upstream_is_counted_as_sent() -> None:
    """The media pass keeps a class a picture already carries, so its bytes go at THAT class's size —
    the live gpt-5-nano picture went at 2,048² and OpenAI counted 6,144 (+ framing)."""
    content = _picture(2048, 2048, vision_class="openai_original")
    assert it.image_content_tokens(content, model="gpt-5-nano", wire_format="openai_chat") == 6144


@pytest.mark.parametrize(
    ("model", "live_estimate", "provider"),
    [("gpt-5.5", 4916, 4946), ("gpt-5.4-nano", 3001, 3026), ("gpt-5-nano", 6144, 6169)],
)
def test_the_checkers_three_live_figures_are_within_two_percent(model: str, live_estimate: int, provider: int) -> None:
    """IMG7's live figures (auto on the wire, a 2,048² picture encoded at 2,048): each within 2%."""
    assert it.openai_picture_tokens(2048, 2048, model, "auto") == live_estimate
    assert abs(live_estimate - provider) / provider < 0.02


# ── CGU-10 IMG8 #4: the stamp is guarded THROUGH THE REAL TRANSLATOR (plant P9 was green suite-wide) ──
@pytest.mark.parametrize("model", ["gpt-5.5", "gpt-5", "gpt-5-nano", "gpt-4o"])
def test_the_translators_request_carries_the_detail_the_estimate_counts(model: str) -> None:
    """``OpenAITranslator.to_openai`` — not the helper — must put the counted ``detail`` on every picture.
    Red when the ``_stamp_image_detail`` call is dropped from ``to_openai`` (the wire falls back to
    ``auto`` while the estimate counts the class's detail: the IMG7 #1 defect)."""
    from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.providers.openai.translator import OpenAITranslator
    from matrx_ai.testing.profile_factory import make_profile

    picture = ImageContent(base64_data="AAAA", mime_type="image/jpeg")
    config = UnifiedConfig(
        model=model,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="what is this?"), picture])],
    )
    request = OpenAITranslator().to_openai(config, make_profile(model_name=model, wire_format="openai_chat"))
    images = [
        part
        for item in request["input"]
        if isinstance(item, dict)
        for part in (item.get("content") or [])
        if isinstance(part, dict) and part.get("type") == "input_image"
    ]
    assert images, f"no picture reached the request: {request['input']!r}"
    expected = it.openai_image_detail(model, "openai_chat")
    assert [part.get("detail") for part in images] == [expected], images


def test_a_malformed_detail_knob_announces_itself_and_sends_the_class_detail(capsys) -> None:
    """CGU-10 IMG8 #8: a typo in ``ai.vision.openai_image_detail`` silently became ``auto``. It is now
    announced (stderr + a ``feature_knob_malformed`` system error) and the class's own detail is sent
    (what the estimate counts with no knob). A value with stray case/space is simply read."""
    import matrx_ai.knobs as knobs

    knobs._malformed.clear()
    configure_package_knobs(lambda feature, key: {"gpt-5.5": "HIGH "} if (feature, key) == (
        it.OPENAI_DETAIL_FEATURE, it.OPENAI_DETAIL_KEY) else None)
    assert it.openai_image_detail("gpt-5.5", "openai_chat") == "high"
    assert "malformed" not in capsys.readouterr().err

    configure_package_knobs(lambda feature, key: {"gpt-5.5": "hgih"} if (feature, key) == (
        it.OPENAI_DETAIL_FEATURE, it.OPENAI_DETAIL_KEY) else None)
    assert it.openai_image_detail("gpt-5.5", "openai_chat") == "original"  # the class's, not auto
    err = capsys.readouterr().err
    assert "ai.vision.openai_image_detail" in err and "hgih" in err and "malformed" in err

    configure_package_knobs(lambda feature, key: "high" if (feature, key) == (
        it.OPENAI_DETAIL_FEATURE, it.OPENAI_DETAIL_KEY) else None)
    assert it.openai_image_detail("gpt-5", "openai_chat") == "high"
    assert "not a {model prefix: detail} map" in capsys.readouterr().err


def test_a_malformed_number_knob_announces_itself(capsys) -> None:
    import matrx_ai.knobs as knobs

    knobs._malformed.clear()
    configure_package_knobs(lambda feature, key: "ten" if (feature, key) == ("f.x", "k") else None)
    assert knobs.package_knob_number("f.x", "k", 5, low=1, high=9) == 5
    assert "f.x.k" in capsys.readouterr().err
