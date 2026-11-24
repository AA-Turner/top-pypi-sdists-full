"""Forcing-function guards for images and Box questions on the decision routes.

THE BREAKS THESE CATCH (each names a production change that turns it red):

1. An image beside the questions of a model that READS images (Jev 1.14) is
   refused, dropped, or sent without its asset / its place in the state.
2. A Box question goes out without its presence check, or names no image, or
   its answer is not mapped back from the fitted image onto the source picture.
3. An image outside Jev's accepted bounds is sent as-is (TypeSafe rejects it,
   never resizes): too large, too small, a thin strip, sideways from EXIF,
   transparent.
4. A model that does NOT read images stops refusing one by name, or a Box with
   no image to look in is paid for.
5. A vision chat model asked the same Box question loses the picture or the
   schema that returns the same answer shape.

THE USE CASE: All Green Recycling's driver app. A driver photographs a curb at
a missed pickup; the decision asks whether a recycling bin is out and where it
is in the photo.
"""

from __future__ import annotations

import base64
from io import BytesIO
from types import SimpleNamespace

import pytest
from PIL import Image

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.decisions.kinds import DecisionAnswer, DecisionBox, DecisionQuestions
from matrx_ai.decisions.translate import (
    DecisionCompatibilityError,
    decision_answers_from_verbalized,
    prepare_verbalized_decision,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.processing.vision import VISION_API_CLASSES, fit_for_vision_class
from matrx_ai.providers.typesafe import SystemOneResult
from matrx_ai.providers.unified_client import UnifiedAIClient

JEV = VISION_API_CLASSES["typesafe_jev"]

CURB_QUESTIONS = [
    {"name": "bin_out", "type": "noul", "instructions": "Is a recycling bin out at the curb?"},
    {"name": "bin", "type": "box", "instructions": "the blue recycling bin"},
]


def _jpeg(width: int, height: int, color=(30, 90, 200), **save) -> bytes:
    out = BytesIO()
    Image.new("RGB", (width, height), color).save(out, format="JPEG", **save)
    return out.getvalue()


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _curb_message(*images: ImageContent) -> UnifiedMessage:
    return UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Missed pickup reported at 14 Oak Lane."),
            *images,
            DecisionQuestionsContent(questions=[dict(q) for q in CURB_QUESTIONS]),
        ],
    )


# --- 3. Fitting an image inside Jev's bounds -------------------------------


def test_a_large_photo_is_shrunk_to_the_long_edge_and_kept_whole():
    fitted = fit_for_vision_class(_jpeg(4032, 3024), JEV)
    assert (fitted.width, fitted.height) == (1568, 1176)
    assert fitted.content == (0, 0, 1568, 1176)
    assert fitted.format == "jpg"
    assert Image.open(BytesIO(fitted.data)).format == "JPEG"


def test_a_tiny_image_is_upscaled_to_the_minimum_side():
    fitted = fit_for_vision_class(_jpeg(140, 200), JEV)
    assert min(fitted.width, fitted.height) == 280
    assert max(fitted.width, fitted.height) <= 1568
    assert fitted.content == (0, 0, fitted.width, fitted.height)


def test_a_thin_strip_is_padded_and_a_box_maps_back_onto_the_source():
    """Upscaling 2000x100 to a 280 px short side would break 1568, so it pads."""
    fitted = fit_for_vision_class(_jpeg(2000, 100), JEV)
    assert fitted.width == 1568 and fitted.height == 280
    left, top, right, bottom = fitted.content
    assert (left, right) == (0, 1568) and top > 0 and bottom < 280
    # A box covering exactly the picture's band maps to the whole source.
    whole = fitted.to_source_fractions(
        {"left": 0.0, "right": 1.0, "top": top / 280, "bottom": bottom / 280}
    )
    assert whole == pytest.approx({"left": 0.0, "right": 1.0, "top": 0.0, "bottom": 1.0})
    # A box in the padding clamps to the edge it is nearest, never outside 0..1.
    edge = fitted.to_source_fractions({"left": 0.1, "right": 0.2, "top": 0.0, "bottom": 0.05})
    assert edge["top"] == 0.0 and edge["bottom"] == 0.0


def test_exif_orientation_is_applied_to_the_pixels():
    """Jev strips EXIF unapplied: a portrait phone photo would arrive sideways."""
    img = Image.new("RGB", (600, 400), (0, 0, 0))
    exif = img.getexif()
    exif[0x0112] = 6  # rotate 90° clockwise to display
    out = BytesIO()
    img.save(out, format="JPEG", exif=exif.tobytes())
    fitted = fit_for_vision_class(out.getvalue(), JEV)
    assert (fitted.width, fitted.height) == (400, 600)


def test_transparency_is_flattened_onto_white():
    img = Image.new("RGBA", (400, 400), (255, 0, 0, 0))
    out = BytesIO()
    img.save(out, format="PNG")
    fitted = fit_for_vision_class(out.getvalue(), JEV)
    pixel = Image.open(BytesIO(fitted.data)).convert("RGB").getpixel((200, 200))
    assert all(channel > 240 for channel in pixel)


def test_bytes_that_are_not_an_image_are_refused_with_the_reason():
    with pytest.raises(ValueError, match="not a readable image"):
        fit_for_vision_class(b"definitely not a picture", JEV)


# --- The native route --------------------------------------------------------


def _profile(*, reads_images: bool):
    return SimpleNamespace(
        wire_format="typesafe_systemone",
        client_attr="decision",
        capabilities=SimpleNamespace(interaction="decision", supports_vision=reads_images),
        byok_secret_key=None,
        provider_model_id="jev-1.14.0",
        base_url="https://api.typesafe.ai",
        model_name="jev-1.14.0",
        vendor="typesafe",
        endpoint_id="endpoint-typesafe",
        api_id="api-systemone",
        offering_id="offering-jev",
        resolution_route="pinned",
    )


class _Admission:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.fixture
def jev_wire(monkeypatch):
    from matrx_ai.catalog import resolve as resolve_mod
    from matrx_ai.decisions import runner

    state = SimpleNamespace(reads_images=True)

    async def _resolve(*_args, **_kwargs):
        return _profile(reads_images=state.reads_images)

    async def _pricing():
        return {"offering-jev": object()}

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    monkeypatch.setattr(runner, "ensure_pricing_lookup", _pricing)
    monkeypatch.setattr(runner.TokenUsage, "calculate_catalog_cost", lambda *_a: 0.00002)
    monkeypatch.setattr("matrx_ai.providers.admission.admit_provider_call", lambda _p: _Admission())
    captured: dict = {}

    def install(answers: dict) -> None:
        async def _caller(request, **kwargs):
            captured["request"] = request
            return SystemOneResult.model_validate(
                {"model": "jev-1.14.0", "answers": answers, "usage": {"input_tokens": 620, "output_tokens": 0}}
            )

        monkeypatch.setattr(runner, "call_system_one", _caller)

    return SimpleNamespace(install=install, captured=captured, state=state)


_BOX_CASES = [
    # Two different photos, two different answers: a constant cannot pass both.
    pytest.param((1200, 900), 0.94, {"top": 0.4, "bottom": 0.9, "left": 0.1, "right": 0.3}, 0.81, True, id="bin-out"),
    pytest.param((2000, 100), 0.08, {"top": 0.0, "bottom": 1.0, "left": 0.6, "right": 0.7}, None, False, id="strip-empty"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("size", "present", "edges", "confidence", "bin_out"), _BOX_CASES)
async def test_an_image_and_a_box_ride_the_native_wire_and_come_back_mapped(
    jev_wire, size, present, edges, confidence, bin_out
):
    jev_wire.install(
        {
            "bin_out": {"type": "noul", "noul": present},
            "bin": {"type": "box", "box": edges, "confidence": confidence},
            "bin:present": {"type": "noul", "noul": present},
        }
    )
    photo = ImageContent(base64_data=_b64(_jpeg(*size)), mime_type="image/jpeg", file_id="file-curb-1")
    config = UnifiedConfig(model="jev-1.14.0", messages=[_curb_message(photo)])
    response = await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="curb-1", config=config))

    sent = jev_wire.captured["request"]
    # The picture is in the state by an opaque reference, and that reference is an asset.
    [reference] = sent.state["images"]
    assert set(sent.assets) == {reference}
    assert sent.assets[reference].format == "jpg"
    fitted = Image.open(BytesIO(base64.b64decode(sent.assets[reference].data_base64)))
    assert 280 <= min(fitted.size) and max(fitted.size) <= 1568
    # The box names its image, and brings its presence check.
    assert sent.questions["bin"].type == "box"
    assert "`images[0]`" in sent.questions["bin"].instructions
    assert sent.questions["bin:present"].type == "noul"
    assert sent.uses_images

    answers = response.messages[0].content[0].answers
    assert answers.answers["bin_out"].answer is bin_out
    box = answers.answers["bin"]
    assert box.type == "box" and box.image == 0
    assert box.probability == present
    assert box.confidence == confidence
    # Mapped back onto the source picture (identity for a whole image).
    if size == (1200, 900):
        assert box.answer.model_dump() == pytest.approx(edges)
    else:
        assert box.answer.top == 0.0 and box.answer.bottom == 1.0
    # The picture the box is drawn on rides the answers, by durable handle.
    assert answers.images[0].file_id == "file-curb-1"
    assert (answers.images[0].width, answers.images[0].height) == size
    assert "bin:present" not in answers.answers


@pytest.mark.asyncio
async def test_a_model_that_does_not_read_images_still_refuses_one_by_name(jev_wire):
    jev_wire.state.reads_images = False
    jev_wire.install({"bin_out": {"type": "noul", "noul": 0.5}})
    photo = ImageContent(base64_data=_b64(_jpeg(600, 400)), mime_type="image/jpeg")
    config = UnifiedConfig(model="jev-1.14.0", messages=[_curb_message(photo)])
    with pytest.raises(DecisionCompatibilityError, match="an image"):
        await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="curb-2", config=config))
    assert "request" not in jev_wire.captured


@pytest.mark.asyncio
async def test_a_box_with_no_image_to_look_in_is_refused_before_paying(jev_wire):
    jev_wire.install({"bin_out": {"type": "noul", "noul": 0.5}})
    config = UnifiedConfig(model="jev-1.14.0", messages=[_curb_message()])
    with pytest.raises(DecisionCompatibilityError, match="carries no image"):
        await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="curb-3", config=config))
    assert "request" not in jev_wire.captured


# --- The kind contract -------------------------------------------------------


def test_a_box_question_takes_no_criteria():
    with pytest.raises(ValueError, match="takes no criteria"):
        DecisionQuestions(questions=[{"name": "bin", "type": "box", "instructions": "the bin", "criteria": ["a", "b"]}])


def test_a_box_answer_must_enclose_an_area_and_others_must_carry_confidence():
    with pytest.raises(ValueError):
        DecisionBox(top=0.5, bottom=0.5, left=0.1, right=0.2)
    with pytest.raises(ValueError, match="carries its confidence"):
        DecisionAnswer(type="noul", answer=True, probability=0.9)
    DecisionAnswer(type="box", answer={"top": 0.1, "bottom": 0.2, "left": 0.1, "right": 0.2}, probability=0.9)


# --- 5. A vision chat model asked the same questions --------------------------


def test_a_vision_chat_model_keeps_the_picture_and_gets_a_box_schema():
    photo = ImageContent(base64_data=_b64(_jpeg(600, 400)), mime_type="image/jpeg", file_id="file-curb-9")
    config = UnifiedConfig(model="gpt-5.2", messages=[_curb_message(photo)])
    overlay = prepare_verbalized_decision(
        config, model_name="gpt-5.2", supports_structured_output=True, supports_vision=True
    )
    assert overlay is not None
    content = config.messages[0].content
    assert any(isinstance(block, ImageContent) for block in content)
    prose = content[-1].text
    assert "1 image(s)" in prose and "image 0" in prose
    box_schema = config.response_format["json_schema"]["schema"]["properties"]["answers"]["properties"]["bin"]
    assert box_schema["required"] == ["present", "box", "confidence"]
    assert overlay.images[0].file_id == "file-curb-9"


def test_a_text_only_chat_model_refuses_the_picture():
    photo = ImageContent(base64_data=_b64(_jpeg(600, 400)), mime_type="image/jpeg")
    config = UnifiedConfig(model="text-only", messages=[_curb_message(photo)])
    with pytest.raises(DecisionCompatibilityError, match="an image"):
        prepare_verbalized_decision(config, model_name="text-only", supports_structured_output=True)


@pytest.mark.parametrize(
    ("raw", "answered"),
    [
        ({"present": 0.9, "box": {"top": 0.2, "bottom": 0.6, "left": 0.3, "right": 0.5}, "confidence": 0.7}, True),
        ({"present": 0.9, "box": {"top": 0.6, "bottom": 0.2, "left": 0.3, "right": 0.5}, "confidence": 0.7}, False),
    ],
)
def test_a_verbalized_box_is_the_same_answer_or_an_honest_refusal(raw, answered):
    batch = DecisionQuestions(questions=[dict(q) for q in CURB_QUESTIONS])
    answers = decision_answers_from_verbalized(
        {"answers": {"bin_out": {"answer": True, "probability": 0.9, "confidence": 0.9}, "bin": raw}},
        batch,
        model="gpt-5.2",
        input_tokens=1,
        output_tokens=1,
        cost_usd=0.0,
    )
    if answered:
        assert answers.answers["bin"].answer.top == 0.2
        assert answers.answers["bin"].probability == 0.9
    else:
        assert "bin" in answers.unanswerable


@pytest.mark.asyncio
async def test_a_photo_attached_on_the_persons_turn_after_the_template_is_judged(jev_wire):
    """An agent's template carries the questions; the person's photo arrives in the
    NEXT message when the agent runs. It must reach the wire, never be ignored."""
    jev_wire.install(
        {
            "bin_out": {"type": "noul", "noul": 0.9},
            "bin": {"type": "box", "box": {"top": 0.1, "bottom": 0.5, "left": 0.1, "right": 0.5}, "confidence": 0.6},
            "bin:present": {"type": "noul", "noul": 0.9},
        }
    )
    template = _curb_message()
    turn = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Driver note: gate was open."),
            ImageContent(base64_data=_b64(_jpeg(800, 600)), mime_type="image/jpeg", file_id="file-turn-1"),
        ],
    )
    config = UnifiedConfig(model="jev-1.14.0", messages=[template, turn])
    response = await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="curb-4", config=config))
    sent = jev_wire.captured["request"]
    assert len(sent.state["images"]) == 1
    assert "Driver note: gate was open." in sent.state["subject"]
    assert "14 Oak Lane" in sent.state["subject"]
    assert response.messages[0].content[0].answers.images[0].file_id == "file-turn-1"


@pytest.mark.asyncio
async def test_pictures_earlier_in_the_conversation_ride_as_history_not_dropped(jev_wire):
    jev_wire.install(
        {
            "bin_out": {"type": "noul", "noul": 0.9},
            "bin": {"type": "box", "box": {"top": 0.1, "bottom": 0.5, "left": 0.1, "right": 0.5}, "confidence": 0.6},
            "bin:present": {"type": "noul", "noul": 0.9},
        }
    )
    earlier = UnifiedMessage(
        role="user",
        content=[TextContent(text="Yesterday's photo."), ImageContent(base64_data=_b64(_jpeg(500, 400)), mime_type="image/jpeg")],
    )
    photo = ImageContent(base64_data=_b64(_jpeg(600, 400)), mime_type="image/jpeg", file_id="file-today")
    config = UnifiedConfig(model="jev-1.14.0", messages=[earlier, _curb_message(photo)])
    response = await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="curb-5", config=config))
    sent = jev_wire.captured["request"]
    assert len(sent.state["images"]) == 1 and len(sent.state["earlier_images"]) == 1
    assert set(sent.assets) == {*sent.state["images"], *sent.state["earlier_images"]}
    # Image 0 is still TODAY's picture: history is never numbered into the turn.
    assert [image.file_id for image in response.messages[0].content[0].answers.images] == ["file-today"]


def test_too_many_image_bytes_for_one_request_is_refused_by_name():
    from matrx_ai.decisions.images import (
        DecisionImageError,
        PreparedDecisionImage,
        require_images_fit_one_request,
    )
    from matrx_ai.decisions.kinds import DecisionImage
    from matrx_ai.processing.vision import FittedImage

    big = FittedImage(data=b"x" * (12 * 1024 * 1024), format="jpg", width=1568, height=1568,
                      content=(0, 0, 1568, 1568), source_width=1568, source_height=1568)
    images = [PreparedDecisionImage(index=i, reference=f"r{i}", fitted=big, identity=DecisionImage()) for i in range(2)]
    with pytest.raises(DecisionImageError, match="Send fewer images"):
        require_images_fit_one_request(images)
    require_images_fit_one_request(images[:1])


def test_only_a_box_answer_names_an_image():
    with pytest.raises(ValueError, match="only a box"):
        DecisionAnswer(type="noul", answer=True, probability=0.9, confidence=0.9, image=0)
