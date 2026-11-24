"""What one picture costs in input tokens, by the provider's own rule (CGU-10 IMG5 finding 2/10).

The prompt estimate (``config/context_preflight.estimate_prompt_tokens``) measured an image by its
storage form with the bytes stripped — a few dozen characters — so a chat with a 2,048² picture was
estimated at 2,356 tokens and Anthropic counted 10,671. An under-count promises a fit the provider
then refuses. Each picture is now counted the way its provider counts it, after the resize its
vision class (``vision_classes.py``, the one place that knows each family's long edge) applies:

* Anthropic: 28 px PATCHES — ``ceil(w/28) * ceil(h/28)`` plus a per-picture overhead, after the fit to the
  class's long edge and then to the model's own long edge and patch cap (``claude_image_sizing``: the catalog
  row's ``capabilities.image_sizing``, else the name's tier). Measured with ``count_tokens`` on every current
  Claude (CGU-10 AND-IMG18 N2): the high-resolution tier (Opus 4.7+, Sonnet 5+, Haiku 5+, Fable) 2,576 px /
  4,784 patches +3; the earlier tier (Sonnet 4.6, Opus 4.6, Haiku 4.5) 1,568 px / 1,568 patches +4.
* Every other wire's fallback: ``ceil(width * height / 750)`` after the fit to the long edge.
* OpenAI (CGU-10 IMG7 #1, spec §4.1): the MEASURED per-model rule (``_PATCH_RULES``) at the ``detail``
  the wire really sends (``openai_image_detail`` — the translator sends the same value).
* Every other OpenAI-compatible wire: tiles — fit inside 2,048², shortest side down to 768, then 170
  per 512² tile + 85. ``low``: 85.
* Gemini 2.x and a picture/video-MAKING Gemini: a flat 258 (measured, CGU-10 IMG8).
* Gemini 3: by media resolution — the picture's own ``media_resolution`` first, else the class's:
  280 (low) / 560 (medium) / 1,120 (high) / 2,240 (ultra high).

A picture with no known size (a URL only, or bytes that do not decode) is counted as the
largest picture its class sends — an over-count is a smaller error than the refusal.

PDF pages (CGU-10 IMG6 #4, spec §8c): Anthropic and OpenAI read each page as its text AND a picture
of the page — ``PAGE_TEXT_TOKENS`` plus a letter-size page picture by the picture rule above; Gemini
2.5 counts 258 a page, Gemini 3 560 (its default PDF media resolution). A PDF of unknown length counts
as one page.
"""

from __future__ import annotations

import base64
import hashlib
import math
import re
import struct
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any

from matrx_ai.processing.vision.vision_classes import (
    VISION_API_CLASSES,
    VisionApiClass,
    resolve_vision_class,
)

_OPENAI_TILE = 170
_OPENAI_BASE = 85
_GEMINI_TILE = 258
# The TILING Gemini (2.x computer use; ``_gemini_tiled_tokens``), every figure measured with ``countTokens``.
_GEMINI_TILED_MIN_SIDE = 256
_GEMINI_TILED_SMALL = 384
_GEMINI_TILED_MAX_UNIT = 768
_GEMINI_TILED_MAX_TILES = 12
# Gemini 3 per media resolution (Google's published budgets; ``countTokens`` reads 24-31 lower, measured
# 2026-11-11: 256 / 529 / 1,089 / 2,209 — the published figure is the safer side).
_GEMINI3 = {
    "MEDIA_RESOLUTION_LOW": 280,
    "MEDIA_RESOLUTION_MEDIUM": 560,
    "MEDIA_RESOLUTION_HIGH": 1_120,
    "MEDIA_RESOLUTION_ULTRA_HIGH": 2_240,
}
# A NUMBERED Gemini 3.x lays its published budget out as a grid of the picture's shape (``gemini3_grid_tokens``);
# Gemini 4 (gemini-4-argon: 1,120) and an un-numbered ``*-latest`` (it moves to a new generation without a name
# change) keep the published budget, the safe side. A picture of unknown size counts the budget itself (no shape
# counts more).
_GEMINI3_NUMBERED = re.compile(r"^gemini-3(\.\d+)?-")


def gemini3_grid_tokens(width: int, height: int, budget: int) -> int:
    """What a NUMBERED Gemini 3.x counts for one picture: its published budget laid out as a grid of the
    picture's shape — ``floor(sqrt(budget * a)) * floor(sqrt(budget / a))`` for aspect ``a = w / h``, whatever
    the pixel size (a 400² and a 1536² picture both count 33 x 33 = 1,089 at HIGH). ``countTokens`` on
    gemini-3.8-flash, 2026-11-12, 20 shapes, every one exact (CGU-10 AND-IMG18): 4:3 1,064 · 16:9 1,100 ·
    2:1 1,081 · 1000x700 1,120 · 1000x100 1,050 · 4000x1000 1,056. The flat 1,089 (the square's figure)
    over-counted a 4:3 photo by 25 — +2.6% against its bill with the label."""
    a = (width / height) if width and height and width > 0 and height > 0 else 1.0
    return max(1, math.floor(math.sqrt(budget * a))) * max(1, math.floor(math.sqrt(budget / a)))


def _resolution_level(value: Any) -> str | None:
    """``"low"`` / ``"media_resolution_low"`` / ``"MEDIA_RESOLUTION_LOW"`` → ``"MEDIA_RESOLUTION_LOW"``."""
    if not isinstance(value, str) or not value.strip():
        return None
    level = value.strip().upper()
    return level if level.startswith("MEDIA_RESOLUTION_") else f"MEDIA_RESOLUTION_{level}"

# PDF pages (spec §8c).
PAGE_TEXT_TOKENS = 1_500  # Anthropic's own lower bound for a page's text (1,500–3,000)
_LETTER_PAGE = (1_700, 2_200)  # 8.5 x 11 in at 200 dpi: the page picture before the class's resize
_GEMINI25_PAGE = 258
_GEMINI3_PAGE = 560

# Keyed by a digest of the WHOLE payload: two pictures of one length and one header (a JPEG's size
# sits past any short prefix) must never share a size (CGU-10 IMG6 F9 / plant N8).
_DIMENSIONS: OrderedDict[tuple[int, bytes], tuple[int | None, int | None]] = OrderedDict()
_PAGES: OrderedDict[tuple[int, bytes], int | None] = OrderedDict()
_MAX_REMEMBERED = 256


def _payload_key(data: str) -> tuple[int, bytes]:
    return len(data), hashlib.blake2b(data.encode("ascii", "ignore"), digest_size=16).digest()


# ── OpenAI: what each model counts, MEASURED (CGU-10 IMG7 #1, 2026-11-11) ──────────────────────────────
# The rules below were fitted to OpenAI's own counts (``POST /v1/responses/input_tokens``, the difference
# between a prompt with one picture and its text-only twin) for 512², 1024x768, 1568², 2048², 3000²,
# 4000x1000 and 64² pictures under every ``detail`` value; each rule reproduces every measured count to the
# token (pinned in ``tests/test_openai_picture_counts_match_the_provider.py``). They differ from what the
# image spec (§4) once said: the patch models carry a x1.2 factor (gpt-5-nano x1.5), ``high`` caps at 2,500
# patches (not 1,536), several models ignore ``detail`` entirely, and gpt-5 base counts 70 + 140 per tile.
#
#   kind "patch": 32-px patches, ``ceil(patches * multiplier)``. Per detail: the box the picture is first
#                 fitted inside (long edge) and the patch cap (scaled down to fit, as OpenAI publishes).
#   kind "tile":  fitted inside 2,048², shortest side down to 768, ``base + tile * tiles``; ``low`` = base.
_FIT_2048 = (2_048, None)
_PATCH_RULES: dict[str, dict[str, Any]] = {
    # detail honored. auto = original.
    "gpt-5.5": {"kind": "patch", "multiplier": 1.2, "auto": "original",
                "detail": {"original": (None, 10_000), "high": (2_048, 2_500), "low": (512, None)}},
    # detail honored. auto = high; ``low`` is NOT low here (measured: fit to 2,048, no cap).
    "gpt-5.4": {"kind": "patch", "multiplier": 1.2, "auto": "high",
                "detail": {"original": (None, 10_000), "high": (2_048, 2_500), "low": _FIT_2048}},
    # detail ignored: fit to 2,048, no cap reached.
    "gpt-5.2": {"kind": "patch", "multiplier": 1.2, "ignores_detail": True},
    "gpt-5-mini": {"kind": "patch", "multiplier": 1.2, "ignores_detail": True},
    "gpt-5-nano": {"kind": "patch", "multiplier": 1.5, "ignores_detail": True},
    "gpt-4.1-mini": {"kind": "patch", "multiplier": 1.62, "ignores_detail": True},
    "gpt-4.1-nano": {"kind": "patch", "multiplier": 2.46, "ignores_detail": True},  # OpenAI docs; not measured
    "o4-mini": {"kind": "patch", "multiplier": 1.72, "ignores_detail": True},  # OpenAI docs; not measured
    "gpt-5": {"kind": "tile", "base": 70, "tile": 140},
    "o3": {"kind": "tile", "base": 75, "tile": 150},
    "o1": {"kind": "tile", "base": 75, "tile": 150},
    "gpt-4.1": {"kind": "tile", "base": _OPENAI_BASE, "tile": _OPENAI_TILE},
    "gpt-4o": {"kind": "tile", "base": _OPENAI_BASE, "tile": _OPENAI_TILE},
    # A later GPT generation counts like the newest measured one until it is measured.
    "gpt-6": {"kind": "patch", "multiplier": 1.2, "auto": "original",
              "detail": {"original": (None, 10_000), "high": (2_048, 2_500), "low": (512, None)}},
}
_DEFAULT_OPENAI_RULE: dict[str, Any] = {"kind": "tile", "base": _OPENAI_BASE, "tile": _OPENAI_TILE}
_OPENAI_PATCH = 32


def _openai_rule(model: str | None) -> dict[str, Any]:
    name = (model or "").lower().rsplit("/", 1)[-1]
    hits = [prefix for prefix in _PATCH_RULES if name.startswith(prefix)]
    return _PATCH_RULES[max(hits, key=len)] if hits else _DEFAULT_OPENAI_RULE


#: KNOB MIRROR ai.vision.openai_image_detail — ``{model prefix: detail}`` to send instead of the vision
#: class's hint. Empty: every model gets its class's detail (``vision_classes.py``, the spec's §4.1 column).
OPENAI_DETAIL_FEATURE = "ai.vision"
OPENAI_DETAIL_KEY = "openai_image_detail"
OPENAI_DETAIL_MIRROR: dict[str, str] = {}
_OPENAI_DETAILS = frozenset({"auto", "low", "high", "original"})


def openai_image_detail(model: str | None, wire_format: str | None = None) -> str | None:
    """THE ``detail`` an OpenAI picture is sent with — the translator sends it, the estimate counts it.

    ``None`` when the model's vision class is not an OpenAI one (nothing is sent then). Before this, the
    class's hint was read only by the estimate and the wire sent no ``detail`` (OpenAI applied ``auto``):
    live, gpt-5-nano was estimated 50x under and gpt-5.4-nano 3.3x over (CGU-10 IMG7 #1)."""
    cls = resolve_vision_class(model, wire_format)
    if not cls.name.startswith("openai"):
        return None
    from matrx_ai.knobs import announce_malformed_knob, package_knob

    chosen: Any = None
    overrides = package_knob(OPENAI_DETAIL_FEATURE, OPENAI_DETAIL_KEY, OPENAI_DETAIL_MIRROR)
    class_detail = str(cls.provider_hint or "auto").lower()
    if isinstance(overrides, dict) and overrides:
        name = (model or "").lower().rsplit("/", 1)[-1]
        hits = [str(prefix) for prefix in overrides if name.startswith(str(prefix).lower())]
        if hits:
            chosen = overrides[max(hits, key=len)]
    elif overrides not in (None, {}, "", []):
        # Law 4 (CGU-10 IMG8 #8): a knob that is not a ``{model prefix: detail}`` map says so.
        announce_malformed_knob(
            OPENAI_DETAIL_FEATURE, OPENAI_DETAIL_KEY, overrides, using="each model's class detail",
            why="not a {model prefix: detail} map",
        )
    if chosen is not None:
        detail = str(chosen).strip().lower()
        if detail in _OPENAI_DETAILS:
            return detail
        # An unknown detail never silently becomes ``auto``: it is announced and the class's own
        # detail (what the estimate would count without the knob) is sent instead.
        announce_malformed_knob(
            OPENAI_DETAIL_FEATURE, OPENAI_DETAIL_KEY, overrides, using=class_detail,
            why=f"{chosen!r} is not one of {sorted(_OPENAI_DETAILS)}",
        )
    return class_detail if class_detail in _OPENAI_DETAILS else "auto"


def _patches(width: float, height: float) -> int:
    return math.ceil(width / _OPENAI_PATCH) * math.ceil(height / _OPENAI_PATCH)


def _openai_patch_tokens(width: int, height: int, rule: dict[str, Any], detail: str) -> int:
    if rule.get("ignores_detail"):
        box, cap = _FIT_2048
    else:
        detail = rule["auto"] if detail == "auto" else detail
        box, cap = rule["detail"].get(detail, rule["detail"][rule["auto"]])
    w, h = float(width), float(height)
    if box is not None and max(w, h) > box:
        scale = box / max(w, h)
        w, h = w * scale, h * scale
    if cap is not None and _patches(w, h) > cap:
        # OpenAI's published scale-down: shrink to the cap's area, then to whole patches.
        shrink = math.sqrt(cap * _OPENAI_PATCH * _OPENAI_PATCH / (w * h))
        w, h = w * shrink, h * shrink
        fit = min(math.floor(w / _OPENAI_PATCH) / (w / _OPENAI_PATCH), math.floor(h / _OPENAI_PATCH) / (h / _OPENAI_PATCH))
        w, h = w * fit, h * fit
    patches = _patches(w, h)
    if cap is not None:
        patches = min(cap, patches)
    # The provider multiplies in float32: 1.2 is 1.2000000477, so 2,500 patches count 3,001, not 3,000
    # (measured), while x1.5 is exact (4,096 patches count 6,144).
    return math.ceil(patches * _float32(rule["multiplier"]))


def _float32(value: float) -> float:
    return struct.unpack("f", struct.pack("f", value))[0]


def _openai_tile_tokens(width: int, height: int, rule: dict[str, Any], detail: str) -> int:
    if detail == "low":
        return rule["base"]
    w, h = _fit(width, height, 2048)
    short = min(w, h)
    if short > 768:
        w, h = round(w * 768 / short), round(h * 768 / short)
    return rule["tile"] * math.ceil(w / 512) * math.ceil(h / 512) + rule["base"]


def openai_picture_tokens(width: int, height: int, model: str | None, detail: str | None) -> int:
    """What OpenAI counts for one picture of ``width`` x ``height`` (as sent) on ``model`` at ``detail``."""
    rule = _openai_rule(model)
    detail = (detail or "auto").lower()
    if rule["kind"] == "patch":
        return _openai_patch_tokens(width, height, rule, detail)
    return _openai_tile_tokens(width, height, rule, detail)


def _fit(width: int, height: int, long_edge: int) -> tuple[int, int]:
    scale = min(1.0, long_edge / max(width, height))
    return max(1, round(width * scale)), max(1, round(height * scale))


def image_tokens(
    width: int | None,
    height: int | None,
    vision_class: VisionApiClass,
    model: str | None = None,
    *,
    detail: str | None = None,
    media_resolution: str | None = None,
) -> int:
    """Input tokens for one picture of ``width`` x ``height`` encoded under ``vision_class`` and sent to
    ``model``. ``detail`` is the OpenAI ``detail`` the wire sends (``openai_image_detail``; the class's hint
    when not given); ``media_resolution`` the Gemini per-picture resolution the wire sends."""
    edge = vision_class.long_edge
    size_known = bool(width and height and width > 0 and height > 0)
    if not size_known:
        width = height = edge  # unknown size: the largest picture this class sends
    hint = vision_class.provider_hint
    name = vision_class.name
    if name.startswith("openai"):
        w, h = _fit(width, height, edge)
        return openai_picture_tokens(w, h, model, detail or hint)
    if name.startswith("gemini3"):
        # The picture's OWN resolution wins (it rides the wire as ``mediaResolution``; CGU-10 IMG7 #4).
        level = _resolution_level(media_resolution) or hint or ""
        if size_known and _GEMINI3_NUMBERED.match((model or "").lower().rsplit("/", 1)[-1]):
            return gemini3_grid_tokens(width, height, _GEMINI3.get(level, _GEMINI3["MEDIA_RESOLUTION_HIGH"]))
        return _GEMINI3.get(level, _GEMINI3["MEDIA_RESOLUTION_HIGH"])
    if name == "gemini25_tiled":
        w, h = _fit(width, height, edge)
        return _gemini_tiled_tokens(w, h)
    if name.startswith("gemini"):
        # Gemini 2.x and a picture/video-making Gemini: a FLAT 258 a picture, whatever its size
        # (CGU-10 IMG8 #6 — ``countTokens`` 258 for 300², 384², 800², 1536² and 1536x400 on 2.5 flash
        # and pro, 2.5-flash-image, 3.1-flash-image, 3-pro-image, nano-banana-2.1 and both omni, and a
        # billed 1536² call on 2.5 flash charged 258). The 768-tile rule counted up to 4x more. These
        # models refuse a per-picture ``mediaResolution``, so nothing makes it cheaper either.
        return _GEMINI_TILE
    w, h = _fit(width, height, edge)
    if name.startswith("anthropic"):
        return claude_picture_tokens(w, h, claude_image_sizing(model))
    return math.ceil(w * h / 750)


# Anthropic's picture sizing, measured (CGU-10 AND-IMG18 N2). Claude counts a picture in 28 px PATCHES:
# ``ceil(w / 28) * ceil(h / 28)`` plus a small per-picture overhead, after scaling it down until it fits the
# model's long edge AND its patch cap. ``messages/count_tokens`` on 2026-11-12, every size exact:
#   high-resolution tier (Opus 4.7+, Sonnet 5+, Haiku 5+, Fable): 2,576 px / 4,784 patches (92 x 52 — the
#   documented "~4,784 tokens at 3.75 MP"), +3: 1568x1176 2,355 · 1568² 3,139 · 1092² 1,524 · 2576x1456 4,787
#   · 1000² 1,299 · 3000x2250 4,743 (79 x 60) · 500x300 201; the picture's label counts 75.
#   earlier tier (Sonnet 4.6, Opus 4.6, Haiku 4.5): 1,568 px / 1,568 patches, +4: 1568x1176 1,568 (46 x 34)
#   · 1568² 1,525 · 2576x1456 1,564 · 1000² 1,300 · 500x300 202; the label counts 64.
# The old ``w*h/750`` over-counted every current Claude by ~3.6% (live AND-V IMG17: 2,517 estimated, 2,430
# billed = 2,355 + 75). Each model row carries its sizing in the catalog (``capabilities.image_sizing``);
# every Claude row carries it since 2026-11-12 (the three Claude 3 rows seeded, AND-IMG19 F6), so the name rule
# below answers only when no catalog does (a client host without one, a server before its catalog loads) — kept so
# that case never over-counts an earlier-tier model at the high-resolution tier.


@dataclass(frozen=True)
class ClaudeImageSizing:
    """How one Claude counts a picture: fit to ``long_edge`` px and ``max_patches`` patches of ``patch_px``,
    then patches + ``overhead``; ``label_scale`` is its tokenizer's count of a picture's label over the
    estimator's text ratio (rounded UP from the measured 75/58 and 64/58, so the label is never under)."""

    long_edge: int
    max_patches: int
    patch_px: int = 28
    overhead: int = 0
    label_scale: float = 1.0


_CLAUDE_STANDARD = ClaudeImageSizing(long_edge=1_568, max_patches=1_568, overhead=4, label_scale=1.15)
_CLAUDE_HIRES = ClaudeImageSizing(long_edge=2_576, max_patches=4_784, overhead=3, label_scale=1.35)
_CLAUDE_STANDARD_PREFIXES = (
    "claude-3", "claude-sonnet-4", "claude-haiku-4", "claude-opus-4-0", "claude-opus-4-1",
    "claude-opus-4-5", "claude-opus-4-6", "claude-opus-4-2", "claude-opus-4-3", "claude-opus-4-4",
    "claude-opus-4-20", "claude-sonnet-3", "claude-instant",
)


def _sizing_from_fact(fact: Any) -> ClaudeImageSizing | None:
    if not isinstance(fact, dict):
        return None
    try:
        return ClaudeImageSizing(
            long_edge=int(fact["long_edge"]),
            max_patches=int(fact["max_patches"]),
            patch_px=int(fact.get("patch_px") or 28),
            overhead=int(fact.get("overhead") or 0),
            label_scale=float(fact.get("label_scale") or 1.0),
        )
    except (KeyError, TypeError, ValueError):
        return None


def claude_image_sizing(model: str | None) -> ClaudeImageSizing:
    """How ``model`` counts a picture: its catalog row's ``capabilities.image_sizing`` when the catalog
    answers, else the tier its name belongs to (an unknown Claude counts high-resolution, the safe side)."""
    from matrx_ai.processing.vision.vision_classes import _catalog

    catalog = _catalog()
    reader = getattr(catalog, "model_image_sizing", None) if catalog is not None else None
    if reader is not None and model:
        try:
            sizing = _sizing_from_fact(reader(model))
        except Exception:  # noqa: BLE001 — the catalog must never break a send
            sizing = None
        if sizing is not None:
            return sizing
    name = (model or "").lower().rsplit("/", 1)[-1].removeprefix("anthropic.")
    if name == "claude-opus-4" or name.startswith(_CLAUDE_STANDARD_PREFIXES):
        return _CLAUDE_STANDARD
    return _CLAUDE_HIRES


def claude_pixel_budget(model: str | None) -> tuple[int, int]:
    """``(long edge, max pixels)`` Claude counts for ``model`` after its own rescale."""
    sizing = claude_image_sizing(model)
    return sizing.long_edge, sizing.max_patches * sizing.patch_px * sizing.patch_px


def claude_picture_tokens(width: int, height: int, sizing: ClaudeImageSizing) -> int:
    """What Claude counts for one ``width`` x ``height`` picture: scaled to the long edge, then down until its
    patches fit the cap (the first width from the top that fits, its height kept to the picture's shape)."""
    w, h = _fit(width, height, sizing.long_edge)
    p = sizing.patch_px

    def patches(x: int, y: int) -> int:
        return math.ceil(x / p) * math.ceil(y / p)

    if patches(w, h) > sizing.max_patches:
        aspect = h / w
        x = max(1, math.floor(w * math.sqrt(sizing.max_patches * p * p / (w * h))))
        while x > 1 and patches(x, max(1, round(x * aspect))) > sizing.max_patches:
            x -= 1
        w, h = x, max(1, round(x * aspect))
    return patches(w, h) + sizing.overhead


def _gemini_tiled_tokens(width: int, height: int) -> int:
    """What a TILING Gemini (2.x computer use) counts for one picture of ``width`` x ``height``.

    Fitted to Google's ``countTokens`` on gemini-2.5-computer-use-preview-10-2025 (CGU-10 AND-IMG11,
    2026-11-11), 25 sizes, every one exact: a short side under 256 is first scaled up to 256; a picture
    then within 384² is 258; otherwise it is cut into tiles of ``clamp(int(short / 1.5), 256, 768)`` px —
    a WHOLE number of pixels, so an exact 2:1 picture gets one more column (AND-IMG12: 1,000×500 is 2,322,
    not 1,806; 85 measured sizes in ``TILED_MEASURED``) — at most 12 count, and the picture costs 258 x (tiles + 1). 385² 1,290 · 1,920×1,080 1,806 ·
    2,304² 2,580 · 300×100 1,032 · 4,000² 3,354 (the 12-tile ceiling).
    """
    short = min(width, height)
    if short < _GEMINI_TILED_MIN_SIDE:
        scale = _GEMINI_TILED_MIN_SIDE / short
        width, height = round(width * scale), round(height * scale)
        short = min(width, height)
    if width <= _GEMINI_TILED_SMALL and height <= _GEMINI_TILED_SMALL:
        return _GEMINI_TILE
    unit = min(_GEMINI_TILED_MAX_UNIT, max(_GEMINI_TILED_MIN_SIDE, int(short / 1.5)))
    tiles = math.ceil(width / unit) * math.ceil(height / unit)
    return _GEMINI_TILE * (min(tiles, _GEMINI_TILED_MAX_TILES) + 1)


def _dimensions(content: Any) -> tuple[int | None, int | None]:
    width, height = getattr(content, "width", None), getattr(content, "height", None)
    if width and height:
        return int(width), int(height)
    data = getattr(content, "base64_data", None)
    if not isinstance(data, str) or not data:
        return None, None
    key = _payload_key(data)
    if key in _DIMENSIONS:
        return _DIMENSIONS[key]
    try:
        from matrx_files.asset_builder import image_dimensions

        found = image_dimensions(base64.b64decode(data, validate=False))
    except Exception:  # noqa: BLE001 — unknown size is counted at the class's largest
        found = (None, None)
    _DIMENSIONS[key] = found
    while len(_DIMENSIONS) > _MAX_REMEMBERED:
        _DIMENSIONS.popitem(last=False)
    return found


def is_image(content: Any) -> bool:
    from matrx_ai.config.media_config import ImageContent

    return isinstance(content, ImageContent)


def image_content_tokens(content: Any, *, model: str | None, wire_format: str | None) -> int:
    """Input tokens for one ``ImageContent`` on this model's wire."""
    width, height = _dimensions(content)
    model_class = resolve_vision_class(model, wire_format)
    # The bytes are re-encoded under the picture's OWN class when it already carries one (the media pass
    # keeps a class set upstream); otherwise under the model's.
    own = getattr(content, "vision_class", None)
    size_class = VISION_API_CLASSES.get(own, model_class) if isinstance(own, str) else model_class
    if size_class.name.startswith("openai") != model_class.name.startswith("openai"):
        size_class = model_class
    detail = openai_image_detail(model, wire_format) if model_class.name.startswith("openai") else None
    return image_tokens(
        width, height, size_class, model, detail=detail, media_resolution=getattr(content, "media_resolution", None)
    )


def is_document(content: Any) -> bool:
    from matrx_ai.config.media_config import DocumentContent

    return isinstance(content, DocumentContent)


_PAGE_MARK = re.compile(rb"/Type\s*/Page(?![a-zA-Z])")


def _page_count(content: Any) -> int | None:
    stored = getattr(content, "page_count", None)
    if isinstance(stored, int) and stored > 0:
        return stored
    data = getattr(content, "base64_data", None)
    if not isinstance(data, str) or not data:
        return None
    key = _payload_key(data)
    if key in _PAGES:
        return _PAGES[key]
    try:
        found = len(_PAGE_MARK.findall(base64.b64decode(data, validate=False))) or None
    except Exception:  # noqa: BLE001 — unknown length counts as one page
        found = None
    _PAGES[key] = found
    while len(_PAGES) > _MAX_REMEMBERED:
        _PAGES.popitem(last=False)
    return found


def page_tokens(vision_class: VisionApiClass, model: str | None = None) -> int:
    """Input tokens for one PDF page sent under ``vision_class`` to ``model`` (spec §8c)."""
    name = vision_class.name
    if name.startswith("gemini3"):
        return _GEMINI3_PAGE
    if name.startswith("gemini"):
        return _GEMINI25_PAGE
    detail = openai_image_detail(model) if name.startswith("openai") else None
    return PAGE_TEXT_TOKENS + image_tokens(*_LETTER_PAGE, vision_class, model, detail=detail)


def document_content_tokens(content: Any, *, model: str | None, wire_format: str | None) -> int:
    """Input tokens for one ``DocumentContent`` (every page) on this model's wire. A non-PDF document
    (sent as text) adds nothing here: its text is measured with the prose."""
    if "pdf" not in str(getattr(content, "mime_type", None) or "").lower():
        return 0
    pages = _page_count(content) or 1
    return pages * page_tokens(resolve_vision_class(model, wire_format), model)


def text_only_document_tokens(content: Any) -> int:
    """What a PDF costs a model that reads no images (CGU-10 IMG7 #3): the media fallback puts the PDF's
    EXTRACTED TEXT on the wire (never the one-line attachment it sends for a picture), so every page is
    counted at ``PAGE_TEXT_TOKENS``. A non-PDF document is text already, measured with the prose."""
    if "pdf" not in str(getattr(content, "mime_type", None) or "").lower():
        return 0
    return min((_page_count(content) or 1) * PAGE_TEXT_TOKENS, extracted_text_ceiling_tokens())


def extracted_text_ceiling_tokens() -> int:
    """The most a PDF's extracted text can put on the wire (CGU-10 IMG8 #7): the media fallback cuts it
    at ``MAX_EXTRACTED_DOCUMENT_CHARS``, measured by the one budget estimator. Before, a 100-page PDF on
    a text-only model was estimated 150,000 tokens while at most ~34,000 could reach the wire, so a
    small-window model was wrongly refused a fit."""
    from matrx_ai.config.context_trim import estimate_budget_tokens
    from matrx_ai.processing.media_fallback.resolvers import MAX_EXTRACTED_DOCUMENT_CHARS

    return estimate_budget_tokens(MAX_EXTRACTED_DOCUMENT_CHARS, "prose")


__all__ = [
    "OPENAI_DETAIL_FEATURE",
    "OPENAI_DETAIL_KEY",
    "OPENAI_DETAIL_MIRROR",
    "PAGE_TEXT_TOKENS",
    "ClaudeImageSizing",
    "claude_image_sizing",
    "claude_picture_tokens",
    "gemini3_grid_tokens",
    "claude_pixel_budget",
    "openai_image_detail",
    "openai_picture_tokens",
    "document_content_tokens",
    "image_content_tokens",
    "image_tokens",
    "is_document",
    "is_image",
    "page_tokens",
    "text_only_document_tokens",
    "extracted_text_ceiling_tokens",
]
