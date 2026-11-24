"""AD296 — a ``mask`` reaches OpenAI's images.edit as a PNG WITH alpha at the edit target's size.

OpenAI changes the picture where the mask is transparent, so the mask must be a PNG with an
alpha channel, the exact size of image 1. The media pass in ``UnifiedAIClient`` used to give
every image-shaped item the model's vision class, which re-encodes to RGB JPEG at the class's
long edge: the mask's alpha was gone before the provider saw it. The roled ``mask`` and
``edit_target`` now keep their master bytes.

The fake file manager below renders a vision variant with the REAL production encoder
(``reencode_for_vision_class``), so these tests go red exactly when the media pass stamps a
class on the mask.
"""

from __future__ import annotations

import base64
from io import BytesIO
from types import SimpleNamespace
from typing import Any

import pytest
from PIL import Image

from matrx_ai import _ext
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.processing.vision import VISION_API_CLASSES, reencode_for_vision_class
from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration
from matrx_ai.providers.unified_client import UnifiedAIClient

TARGET_SIZE = (2048, 1536)  # larger than every vision class's long edge

#: gpt-image-2's offering as the live catalog declares it (ai.model_offering.effective_capabilities).
EDIT_MODEL_ROLES = {"mask": 1, "edit_target": 1, "style": 16, "subject": 16, "character": 16, "total": 17}


def _png(mode: str, color: Any) -> bytes:
    buf = BytesIO()
    Image.new(mode, TARGET_SIZE, color).save(buf, format="PNG")
    return buf.getvalue()


MASTERS = {
    "target-file": _png("RGB", (40, 120, 200)),
    # The platform convention: area to change transparent black, the rest opaque white.
    "mask-file": _png("RGBA", (255, 255, 255, 255)),
}


class _FakeFileManager:
    """Serves the master, or the vision variant rendered by the production encoder."""

    async def resolve_media_async(self, ref: Any, *, needs_bytes: bool = False) -> Any:
        master = MASTERS[ref.file_id]
        if ref.vision_class:
            data = reencode_for_vision_class(master, VISION_API_CLASSES[ref.vision_class])
            ref.mime_type = "image/jpeg"
        else:
            data = master
            ref.mime_type = "image/png"
        ref.base64_data = base64.b64encode(data).decode("ascii")
        ref.is_resolved = True
        return ref


def _boundary_resolved(file_id: str, role: str) -> ImageContent:
    """An image as the API boundary leaves it: resolved to master bytes, no vision class."""
    return ImageContent(
        file_id=file_id,
        base64_data=base64.b64encode(MASTERS[file_id]).decode("ascii"),
        mime_type="image/png",
        is_resolved=True,
        role=role,
    )


class _Messages:
    def __init__(self, messages: list[UnifiedMessage]) -> None:
        self._messages = messages

    def to_list(self) -> list[UnifiedMessage]:
        return self._messages

    def __iter__(self):
        return iter(self._messages)


def _config(messages: _Messages) -> Any:
    return SimpleNamespace(
        model="gpt-image-2",
        messages=messages,
        image_input=None,
        image_inputs=None,
        mask=None,
        reference_images=None,
        last_frame_image=None,
        system_instruction=None,
        partial_images=None,
        image_loras=None,
    )


def _profile() -> Any:
    return SimpleNamespace(
        model_name="gpt-image-2",
        controls=None,
        capabilities=SimpleNamespace(image_reference_limits={}),
    )


@pytest.mark.asyncio
async def test_the_mask_reaches_images_edit_as_png_with_alpha_at_the_targets_size(monkeypatch):
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    target = _boundary_resolved("target-file", "edit_target")
    mask = _boundary_resolved("mask-file", "mask")
    messages = _Messages(
        [UnifiedMessage(role="user", content=[TextContent(text="Add a red kite"), target, mask])]
    )

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages,
        model_name="gpt-image-2",
        wire_format="openai_image",
        supports_vision=True,
        role_limits=EDIT_MODEL_ROLES,
    )

    gen = OpenAIImageGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    kwargs = gen._build_kwargs(_config(messages), _profile())

    _name, mask_bytes, mask_mime = kwargs["mask"]
    _name, image_bytes, _mime = kwargs["image"]
    sent_mask = Image.open(BytesIO(mask_bytes))
    sent_image = Image.open(BytesIO(image_bytes))
    assert mask_mime == "image/png"
    assert sent_mask.format == "PNG"
    assert "A" in sent_mask.getbands(), f"mask lost its alpha channel (mode {sent_mask.mode})"
    assert sent_mask.size == sent_image.size == TARGET_SIZE
    # The saved parts keep their true type.
    assert mask.vision_class is None and mask.mime_type == "image/png"
    assert target.vision_class is None and target.mime_type == "image/png"


@pytest.mark.asyncio
async def test_a_plain_image_still_gets_its_vision_variant(monkeypatch):
    """The exemption is the mask and its target only; a plain picture is still re-encoded."""
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    plain = _boundary_resolved("target-file", "style")
    plain.role = None
    messages = _Messages([UnifiedMessage(role="user", content=[plain])])

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages, model_name="gpt-image-2", wire_format="openai_image", supports_vision=True
    )

    assert plain.vision_class == "unknown_default"
    assert plain.mime_type == "image/jpeg"


def test_an_unreadable_mask_is_refused_never_turned_into_a_whole_picture_edit(monkeypatch):
    target = _boundary_resolved("target-file", "edit_target")
    # A mask the boundary failed to fetch: a URL and no bytes.
    mask = ImageContent(url="https://cdn.example.com/mask.png", mime_type="image/png", role="mask")
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="x"), target, mask])])

    gen = OpenAIImageGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    with pytest.raises(ValueError, match="mask"):
        gen._build_kwargs(_config(messages), _profile())


@pytest.mark.asyncio
async def test_a_replayed_area_edit_on_a_chat_model_is_downsized_like_any_picture(monkeypatch):
    """CGU-10 IMG2 finding 4: the exemption is for a model that TAKES the mask / edit_target role.

    After an area edit the saved user message keeps both roled parts. The next ordinary turn on a
    vision chat model (no image roles) must get the class's downsized JPEG, never the master PNG
    (a 4096² edit target is ~50 MB against Anthropic's 5 MB limit)."""
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    target = _boundary_resolved("target-file", "edit_target")
    mask = _boundary_resolved("mask-file", "mask")
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="x"), target, mask])])

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages,
        model_name="claude-sonnet-4-5",
        wire_format="anthropic",
        supports_vision=True,
        role_limits={},  # a chat model: no image reference roles
    )

    for part in (target, mask):
        assert part.vision_class == "anthropic_sonnet_default", part.role
        assert part.mime_type == "image/jpeg"
        data = base64.b64decode(part.base64_data)
        assert len(data) <= VISION_API_CLASSES["anthropic_sonnet_default"].max_bytes
        assert max(Image.open(BytesIO(data)).size) <= 1568


@pytest.mark.asyncio
async def test_a_pre_stamped_mask_on_an_edit_model_is_cleared_and_re_resolved_to_master(monkeypatch):
    """IMG2 S3: replayed history carries a ``vision_class`` already set (and its JPEG bytes). On a
    model that takes the roles, that class is cleared and the master PNG re-resolved."""
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    fm = _FakeFileManager()
    parts = []
    for file_id, role in (("target-file", "edit_target"), ("mask-file", "mask")):
        part = ImageContent(file_id=file_id, role=role, vision_class="unknown_default")
        await fm.resolve_media_async(part, needs_bytes=True)  # the stale JPEG variant
        assert part.mime_type == "image/jpeg"
        parts.append(part)
    target, mask = parts
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="x"), target, mask])])

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages,
        model_name="gpt-image-2",
        wire_format="openai_image",
        supports_vision=True,
        role_limits=EDIT_MODEL_ROLES,
    )

    for part in (target, mask):
        assert part.vision_class is None, part.role
        assert part.mime_type == "image/png"
        assert base64.b64decode(part.base64_data) == MASTERS[part.file_id]
    assert "A" in Image.open(BytesIO(base64.b64decode(mask.base64_data))).getbands()


#: An edit-target-only offering as the live catalog declares it (gemini-3-pro-image, CGU-10 IMG3 #1).
EDIT_TARGET_ONLY_ROLES = {"edit_target": 1, "style": 14}


@pytest.mark.asyncio
async def test_an_edit_target_only_model_gets_the_vision_variant(monkeypatch):
    """CGU-10 IMG3 #1: master bytes exist so a mask lines up with its picture. A model that takes
    ``edit_target`` but no ``mask`` (Gemini image, Grok Imagine, FLUX.2) gets the downsized
    variant: a 4096² master PNG is ~50 MB, over Gemini's inline request limit."""
    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    target = _boundary_resolved("target-file", "edit_target")
    mask = _boundary_resolved("mask-file", "mask")
    messages = _Messages([UnifiedMessage(role="user", content=[TextContent(text="x"), target, mask])])

    await UnifiedAIClient()._annotate_and_resolve_image_refs(
        messages,
        model_name="gemini-3-pro-image",
        wire_format="google",
        supports_vision=True,
        role_limits=EDIT_TARGET_ONLY_ROLES,
    )

    for part in (target, mask):
        assert part.vision_class is not None, part.role
        assert part.mime_type == "image/jpeg", part.role
        cls = VISION_API_CLASSES[part.vision_class]
        assert max(Image.open(BytesIO(base64.b64decode(part.base64_data))).size) <= cls.long_edge


async def _dispatch_media_pass(monkeypatch, capabilities: dict[str, Any]) -> ImageContent:
    """Drive the REAL ``_execute_dispatch`` with a fake catalog profile; return the edit target
    as the provider receives it."""
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import _app_context, set_app_context

    import matrx_ai.catalog.resolve as resolve_mod
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.testing.profile_factory import make_profile

    monkeypatch.setitem(_ext._registry, "get_cloud_file_manager", lambda: _FakeFileManager())
    profile = make_profile(
        model_name="fake-image-model", wire_format="google_image", capabilities=capabilities
    )
    sent: dict[str, Any] = {}

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    class _Provider:
        async def execute(self, wire_config: Any, _profile: Any, _debug: bool) -> Any:
            sent["messages"] = list(wire_config.messages)
            return SimpleNamespace(usage=None, messages=[])

    async def _client(_self: Any, _name: str) -> Any:
        return _Provider()

    async def _net(thunk: Any, **_k: Any) -> Any:
        return await thunk()

    class _Emitter:
        async def send_warning(self, payload: Any) -> None:  # pragma: no cover
            pass

        async def send_info(self, payload: Any) -> None:  # pragma: no cover
            pass

        async def send_data(self, payload: Any) -> None:  # pragma: no cover
            pass

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    monkeypatch.setattr(UnifiedAIClient, "_get_provider_client", _client)
    monkeypatch.setattr(UnifiedAIClient, "_dispatch_with_billing_net", staticmethod(_net))

    config = UnifiedConfig.from_dict(
        {"model": "fake-image-model", "messages": [{"role": "user", "content": [{"type": "text", "text": "x"}]}]}
    )
    config.messages[0].content.append(_boundary_resolved("target-file", "edit_target"))
    token = set_app_context(AppContext(emitter=_Emitter(), metadata={}))
    try:
        request = SimpleNamespace(config=config, debug=False, add_usage=lambda _u: None)
        await UnifiedAIClient()._execute_dispatch(request)
    finally:
        _app_context.reset(token)
    return next(c for m in sent["messages"] for c in m.content if isinstance(c, ImageContent))


_VISION_CAPS = {"input": ["text", "image"], "output": ["text", "image"], "interaction": "turn"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "roles",
    [{}, EDIT_TARGET_ONLY_ROLES, {**EDIT_TARGET_ONLY_ROLES, "mask": 0}],
    # ``mask: 0`` is a model that takes NO mask (IMG4 S4): a zero limit is never a taken role.
    ids=["no-image-roles", "edit-target-without-mask", "mask-limit-zero"],
)
async def test_the_real_dispatch_downsizes_an_edit_target_the_model_cannot_mask(monkeypatch, roles):
    """The real call site hands the media pass this model's role limits (SP6), and a model with
    no ``mask`` role gets the downsized edit target (SP5) — driven through ``_execute_dispatch``,
    never read off the source text."""
    target = await _dispatch_media_pass(monkeypatch, {**_VISION_CAPS, "image_reference_roles": roles})
    assert target.vision_class is not None
    assert target.mime_type == "image/jpeg"
    size = Image.open(BytesIO(base64.b64decode(target.base64_data))).size
    assert max(size) < max(TARGET_SIZE)


@pytest.mark.asyncio
async def test_the_real_dispatch_keeps_the_master_for_a_mask_model(monkeypatch):
    """The other direction: a mask-edit model's limits reach the pass and keep the master."""
    target = await _dispatch_media_pass(
        monkeypatch, {**_VISION_CAPS, "image_reference_roles": EDIT_MODEL_ROLES}
    )
    assert target.vision_class is None
    assert base64.b64decode(target.base64_data) == MASTERS["target-file"]
