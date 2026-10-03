"""THE DECLARED DEFAULT TRANSLATION TABLES — the one home of every number /
scale / map the engine falls back to when a translation cell (K3) does not
carry its own.

Settings-translation item C5 (CONTRACTS.md K6): translation tables are DATA a
processor reads from its rule — ``rule.from_number`` (number -> scale),
``rule.to_number`` (scale -> number), ``rule.processor_config[...]`` (maps) —
and the values below are what applies when the rule is silent. They are
today's live behaviour, verbatim from the processors / canonicalizer they were
lifted out of (the chat param golden and the wire snapshot freeze them), so a
rule that carries nothing translates exactly as before.

Changing a value HERE changes the wire for every offering whose cell does not
override it. The right place for a per-model fact is the cell, never this file.
Nothing outside ``matrx_ai.catalog`` should import it except tests.
"""

from __future__ import annotations

from typing import Any

# ── vocabulary postures (ai_041) ─────────────────────────────────────────────
# "auto" = leave unset; "none" = send nothing. Postures, never degrees.
HOUSE_VALUES: frozenset[str] = frozenset({"auto", "none"})
# The postures that canonically MEAN UNSET (settings-translation C3c, the
# chair's ruling: "a posture that means 'not set' is never a surprise"). With
# setting families loaded the engine treats such a value exactly like an absent
# key wherever the target cannot speak it — never a drop, never a warning.
UNSET_POSTURES: frozenset[str] = frozenset({"auto"})


def is_unset_posture(value: Any) -> bool:
    """Does ``value`` canonically mean "not set" (``auto``)?"""
    return isinstance(value, str) and value in UNSET_POSTURES


# ── OFF (K6 ``off``) ─────────────────────────────────────────────────────────
# Which canonical value MEANS off for a key. A rule's ``off`` acts only when the
# incoming value is one of these. ``disable_reasoning=True`` reaches the engine
# as reasoning_effort="none" (canonicalize).
OFF_VALUES: dict[str, tuple[Any, ...]] = {
    "reasoning_effort": ("none",),
    "thinking_level": ("none",),
    "include_thoughts": (False,),  # the off of the visibility family
    # Visibility offs spelled as values (C6): a degree never converts INTO one
    # (families._accepted_pool) and one converts only to a sibling's off.
    "reasoning_summary": ("never",),
    "reasoning_format": ("hidden",),
}
# Numeric keys whose off is "at or below" a number (a budget of 0 or -1 is off).
OFF_AT_OR_BELOW: dict[str, float] = {
    "thinking_budget": 0,
}

# ── number -> scale bridges (target-aware; replaces canonicalize's global tier) ─
# A numeric canonical key that, when its scale sibling is unset, converts to
# that sibling through the TARGET rule's ``from_number`` (else the default
# steps below). Done by ``CompiledControlsMap.bridge_numbers`` at the outbound
# seam, never in canonicalize.
NUMBER_TO_SCALE_BRIDGES: dict[str, str] = {
    "thinking_budget": "reasoning_effort",
}

# Default ``from_number`` per scale key. reasoning_effort = the OpenAI tiers the
# retired ``canonicalize._effort_from_budget`` applied to every target
# (tokens < 1 none / < 2000 low / < 10000 medium / < 20000 high / else xhigh).
DEFAULT_FROM_NUMBER: dict[str, list[dict[str, Any]]] = {
    "reasoning_effort": [
        {"lte": 0, "to": "none"},
        {"lte": 1999, "to": "low"},
        {"lte": 9999, "to": "medium"},
        {"lte": 19999, "to": "high"},
        {"lte": None, "to": "xhigh"},
    ],
}

# ── anthropic_thinking ───────────────────────────────────────────────────────
ANTHROPIC_MIN_BUDGET_TOKENS = 1024  # Anthropic rejects budget_tokens < 1024
# Headroom added to max_tokens above budget_tokens (max_tokens > budget rule).
ANTHROPIC_MAX_TOKENS_HEADROOM = 2048
# LAST RESORT ONLY — the offering's own ``default_max_tokens`` is the answer and
# must BE the model's real maximum. Never raise this to chase a new model
# (guard: scripts/check_output_ceiling_defaults.py).
ANTHROPIC_DEFAULT_MAX_TOKENS = 32768

# budget mode: effort -> budget_tokens (the rule's ``to_number`` overrides).
ANTHROPIC_EFFORT_TO_BUDGET: dict[str, int] = {
    "none": 0,
    "minimal": 1024,
    "low": 1024,
    "medium": 4096,
    "high": 8192,
    "xhigh": 24576,
}

# adaptive mode: canonical effort -> output_config.effort
# (processor_config["effort_map"] overrides). "auto" never reaches it (ai_041).
ANTHROPIC_ADAPTIVE_EFFORT: dict[str, str | None] = {
    "none": None,
    "minimal": "low",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
    "max": "max",
}

# adaptive mode: thinking_budget -> effort (the rule's ``from_number``
# overrides). A budget <= 0 is OFF and never reaches these steps.
ANTHROPIC_ADAPTIVE_FROM_NUMBER: list[dict[str, Any]] = [
    {"lte": 1024, "to": "low"},
    {"lte": 8192, "to": "medium"},
    {"lte": None, "to": "high"},
]

# adaptive mode: thinking_level -> effort
# (processor_config["thinking_level_map"] overrides).
ANTHROPIC_ADAPTIVE_THINKING_LEVEL: dict[str, str] = {
    "minimal": "low",
    "low": "low",
    "medium": "medium",
    "high": "high",
}

# Order of adaptive tiers — the ``effort_ceiling`` gate compares in it.
ANTHROPIC_ADAPTIVE_EFFORT_ORDER: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")

# anthropic_temp_topp_exclusion: with a thinking block Anthropic accepts only
# this temperature and top_p at or above this floor.
ANTHROPIC_THINKING_TEMPERATURE = 1
ANTHROPIC_THINKING_MIN_TOP_P = 0.95

# thinking_always_on models: the nearest honest "off" is adaptive at this effort.
ANTHROPIC_ALWAYS_ON_FLOOR_EFFORT = "low"

# ── google_thinking ──────────────────────────────────────────────────────────
GOOGLE_THINKING_BUDGET_FIELD_MAX = 65535  # thinking_config.thinking_budget range [-1, 65535]

# legacy (Gemini 2.5): effort -> thinking_budget (the rule's ``to_number``
# overrides); an effort missing from the table gets the unknown budget.
GOOGLE_LEGACY_EFFORT_TO_BUDGET: dict[str, int] = {
    "none": 0,
    "minimal": 512,
    "low": 1024,
    "medium": 4096,
    "high": 8192,
    "xhigh": 24576,
}
GOOGLE_LEGACY_UNKNOWN_EFFORT_BUDGET = 1024
# include_thoughts=False on legacy sends this budget (Google's dynamic thinking).
GOOGLE_LEGACY_HIDDEN_THOUGHTS_BUDGET = -1

# gemini_3: effort -> thinking_level per family
# (processor_config["level_map"] overrides the family's table).
GOOGLE_3_EFFORT_TO_LEVEL: dict[str, dict[str, str | None]] = {
    "flash": {
        "minimal": "minimal",
        "low": "low",
        "medium": "medium",
        "high": "high",
        "xhigh": "high",
    },
    "pro": {
        "minimal": "low",
        "low": "low",
        "medium": "low",
        "high": "high",
        "xhigh": "high",
    },
}
GOOGLE_3_DEFAULT_FAMILY = "pro"

# gemini_3: reasoning_summary -> include_thoughts
# (processor_config["summary_to_include"] overrides).
GOOGLE_3_SUMMARY_TO_INCLUDE: dict[str, bool | None] = {
    "concise": True,
    "always": True,
    "detailed": True,
    "never": False,
    "auto": None,
}

# gemini_3: thinking_budget -> thinking_level (the rule's ``from_number``
# overrides). ``to: None`` = no level.
GOOGLE_3_FROM_NUMBER: list[dict[str, Any]] = [
    {"lte": 0, "to": None},
    {"lte": 512, "to": "minimal"},
    {"lte": 1024, "to": "low"},
    {"lte": 4096, "to": "medium"},
    {"lte": None, "to": "high"},
]

# ── together_reasoning ───────────────────────────────────────────────────────
# Omission means the provider's "max", so an effort is ALWAYS sent: these map
# (processor_config["effort_map"] overrides), anything else -> the default.
TOGETHER_EFFORT_MAP: dict[str, str] = {"xhigh": "max", "max": "max"}
TOGETHER_DEFAULT_EFFORT = "high"

# ── media_dims ───────────────────────────────────────────────────────────────
# aspect -> (w, h) (processor_config["aspect_table"] overrides).
MEDIA_ASPECT_TO_WH: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1536, 1024),
    "9:16": (1024, 1536),
    "4:3": (1408, 1024),
    "3:4": (1024, 1408),
    "21:9": (1920, 832),
    "9:21": (832, 1920),
    "3:2": (1536, 1024),
    "2:3": (1024, 1536),
}
MEDIA_ANCHOR_SHORT_EDGE = 1024  # computed ratios anchor on this short edge
MEDIA_DIMENSION_MULTIPLE = 16  # and round the long edge to this multiple
MEDIA_ANCHOR_FALLBACK_RATIO = (1, 1)

# sora_size: aspect + resolution -> "WxH" (landscape, portrait).
SORA_DEFAULT_ASPECT = "16:9"
SORA_DEFAULT_RESOLUTION = "720p"
SORA_LANDSCAPE_ASPECTS: tuple[str, ...] = ("16:9", "21:9", "3:2", "4:3", "1:1")
SORA_SIZES: dict[str, tuple[str, str]] = {
    "1080p": ("1920x1080", "1080x1920"),
    "1024p": ("1792x1024", "1024x1792"),
    "720p": ("1280x720", "720x1280"),
}

# ── xai_image_resolution ─────────────────────────────────────────────────────
XAI_NATIVE_RESOLUTIONS: tuple[str, ...] = ("1k", "2k")
XAI_WIDTH_THRESHOLD = 2048  # width >= this -> high tier
XAI_HIGH_RESOLUTION = "2k"
XAI_LOW_RESOLUTION = "1k"

# ── google_imagen_size ───────────────────────────────────────────────────────
IMAGEN_RESOLUTION_TO_SIZE: dict[str, str] = {
    "1k": "1K",
    "2k": "2K",
    "720p": "1K",
    "1080p": "1K",
    "4k": "2K",
    "1080": "1K",
}
IMAGEN_WIDTH_THRESHOLD = 2048
IMAGEN_HIGH_SIZE = "2K"
IMAGEN_LOW_SIZE = "1K"

# ── flux_safety_tolerance / openai_image_gen_only ────────────────────────────
FLUX_SAFETY_TOLERANCE = 5
FLUX_SAFETY_TOLERANCE_WITH_IMAGE_INPUT = 2
OPENAI_IMAGE_DEFAULT_MODERATION = "low"


def is_off_value(key: str, value: Any) -> bool:
    """Does ``value`` mean OFF for ``key``? (K6 ``off`` acts only then.)"""
    if value is None:
        return False
    threshold = OFF_AT_OR_BELOW.get(key)
    if threshold is not None:
        return isinstance(value, int | float) and not isinstance(value, bool) and value <= threshold
    for off in OFF_VALUES.get(key, ()):
        if isinstance(off, bool):
            if value is off:
                return True
        elif not isinstance(value, bool) and value == off:
            return True
    return False


_NO_STEP = object()


def step_lookup(steps: Any, number: float) -> Any:
    """Resolve ``number`` through ``from_number`` steps (ascending ``lte``;
    ``lte: None`` = everything above). Accepts FromNumberStep models or dicts.
    A number above every finite cut-off with no open-ended last step takes the
    LAST step's ``to`` (the highest declared tier)."""
    last: Any = _NO_STEP
    for step in steps or ():
        lte = step.get("lte") if isinstance(step, dict) else step.lte
        to = step.get("to") if isinstance(step, dict) else step.to
        last = to
        if lte is None or number <= lte:
            return to
    return None if last is _NO_STEP else last


__all__ = [name for name in dir() if name.isupper()] + [
    "is_off_value",
    "is_unset_posture",
    "step_lookup",
]
