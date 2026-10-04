"""NOT SET means not set (settings translation, owner's words): a media processor
puts nothing on the wire for a key the person left empty unless its cell DECLARES
the value (processor_config ``default``) — never a hidden engine default.

Provider facts: OpenAI images ``n`` is optional (default 1,
platform.openai.com/docs/api-reference/images/create); Veo ``numberOfVideos`` is
optional (ai.google.dev/gemini-api/docs/video); Sora ``size`` is optional
(platform.openai.com/docs/api-reference/videos/create). Pure fixtures, no DB."""

from __future__ import annotations

from matrx_ai.catalog.controls import CompiledControlsMap
from matrx_ai.catalog.models import ControlRule


def _compiled(rules: dict[str, dict]) -> CompiledControlsMap:
    return CompiledControlsMap(
        rules={k: ControlRule.model_validate(v) for k, v in rules.items()},
        value_orders={},
    )


COUNT = {"count": {"processor": "media_count", "processor_config": {"max": 10, "target": "n"}}}
SORA = {
    "aspect_ratio": {
        "processor": "media_dims",
        "processor_config": {
            "mode": "sora_size",
            "target": "size",
            "consumes": ["width", "height", "resolution"],
        },
    }
}
FLUX = {"disable_safety_checker": {"processor": "flux_safety_tolerance"}}


def test_count_unset_sends_nothing():
    out, _ = _compiled(COUNT).outbound({})
    assert "n" not in out


def test_count_set_is_sent_and_clamped():
    assert _compiled(COUNT).outbound({"count": 2})[0]["n"] == 2
    assert _compiled(COUNT).outbound({"count": 40})[0]["n"] == 10


def test_count_declared_default_is_sent():
    rules = {"count": {**COUNT["count"], "processor_config": {"max": 10, "target": "n", "default": 1}}}
    assert _compiled(rules).outbound({})[0]["n"] == 1


def test_sora_size_unset_sends_nothing():
    out, _ = _compiled(SORA).outbound({})
    assert "size" not in out


def test_sora_size_set_is_sent():
    out, _ = _compiled(SORA).outbound({"aspect_ratio": "16:9"})
    width, height = (int(x) for x in out["size"].split("x"))
    assert width > height


def test_flux_tolerance_reads_declared_default():
    rules = {
        "disable_safety_checker": {
            "processor": "flux_safety_tolerance",
            "processor_config": {"default": 4},
        }
    }
    assert _compiled(rules).outbound({})[0]["safety_tolerance"] == 4
    assert _compiled(FLUX).outbound({})[0]["safety_tolerance"] == 5
