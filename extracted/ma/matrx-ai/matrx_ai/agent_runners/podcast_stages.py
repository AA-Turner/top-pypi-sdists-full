"""Which parts of a podcast are the PODCAST, and which are decoration.

🚨 THE DESIGN RULE (Arman, 2026-08-11): *"The finalization of a podcast cannot
rely on all of those little parts."*

A podcast IS its script, its audio, and its published episode. The cover images,
the individual clip videos, the transcript-derived feature image and the composed
"official" promo video are ANCILLARY — nice to have, frequently flaky (a content
filter, a provider hiccup, a slow render), and individually replaceable through
`POST /podcast/runs/{id}/assets/regenerate`.

So they are modelled apart, and the split is load-bearing in three places:

1. **Completion.** Essential stages gate the run's terminal state. Ancillary
   stages never do. A run whose audio is finished is a FINISHED PODCAST even if
   two covers failed and the promo video never composed — and it must be stamped
   complete, published, and costed on that basis alone.
2. **Presentation.** An ancillary failure is reported as one addressable item
   ("this cover needs a redo"), never as a failed or incomplete run. The user
   gets their episode plus a fix-it chip; they never get a run held hostage by
   one image.
3. **Recovery.** The reconcile path resumes only PENDING ESSENTIAL work. It never
   re-buys an ancillary asset on its own initiative — that is the user's call,
   one click away, and a recovery path that silently re-buys paid renders turns
   one stuck run into a recurring bill.

Ancillary membership is decided by SHAPE, not by an enumerated list: anything
that is a numbered image/video slot, a feature-image step, or the official-video
composition. Everything else — including any stage added later — is ESSENTIAL by
default. That default is deliberate: a new stage that genuinely gates the podcast
is protected automatically, and one that doesn't is a one-line addition here.
"""

from __future__ import annotations

import re

#: Numbered media slots (`image_0`, `video_1`), the feature-image steps
#: (`feature_image_prompt`, `feature_image_4`), and the promo-video composition.
_ANCILLARY_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^image_\d+$"),
    re.compile(r"^video_\d+$"),
    re.compile(r"^feature_image(_.*)?$"),
    re.compile(r"^compose_official_video$"),
)

#: The stage that produces the podcast itself. Its completion — with a real URL —
#: is what "this run delivered" means, everywhere in the platform.
AUDIO_STAGE = "create_audio"

#: The stage that produces the script. Essential, and the audio's input.
SCRIPT_STAGE = "create_script"

#: Slot-bearing ancillary kinds, mapped to the `asset_kind` the regenerate
#: endpoint expects, so a reported problem is directly actionable.
_MANDATE_KINDS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"^image_(\d+)$"), "image"),
    (re.compile(r"^video_(\d+)$"), "video"),
)


def is_ancillary_stage(stage_key: str) -> bool:
    """True when this stage may fail without the podcast failing."""
    key = (stage_key or "").strip()
    return any(pattern.match(key) for pattern in _ANCILLARY_PATTERNS)


def is_essential_stage(stage_key: str) -> bool:
    """True when this stage gates the run's terminal state. The default."""
    return not is_ancillary_stage(stage_key)


def expected_ancillary_stages(request: dict[str, object]) -> list[str]:
    """Every ancillary stage this run's REQUEST asked for, whether or not a row
    for it exists yet.

    Needed because a checkpoint row is written only when a stage FINISHES. A
    cover that is still rendering therefore has no row at all — so reporting only
    on rows makes in-flight ancillary work invisible, and a client that shows the
    finished episode has no way to say "two covers are still coming". Absence is
    not the same as nothing to do.

    Resolved from the same caps the pipeline resolves (`max_images` / `max_videos`
    → the pinned agent counts, `include_feature_image`), so the expectation and
    the work can't drift apart.
    """
    from matrx_ai.agent_runners.podcast_generator import (
        _TARGET_IMAGE_COUNT,
        _TARGET_VIDEO_COUNT,
        _effective_media_count,
    )

    def _cap(value: object) -> int | None:
        if isinstance(value, bool) or not isinstance(value, int | float):
            return None
        return int(value)

    images = _effective_media_count(_cap(request.get("max_images")), _TARGET_IMAGE_COUNT)
    videos = _effective_media_count(_cap(request.get("max_videos")), _TARGET_VIDEO_COUNT)
    expected = [f"image_{i}" for i in range(images)] + [f"video_{i}" for i in range(videos)]
    # The feature image is opt-out and lands in the slot AFTER the numbered ones.
    if request.get("include_feature_image", True):
        expected.append("feature_image_prompt")
    # Composition only happens with at least two pieces of media to stitch.
    if images + videos >= 2:
        expected.append("compose_official_video")
    return expected


def mandate_for_stage(stage_key: str) -> tuple[str, int] | None:
    """`("image", 3)` for `image_3` — the coordinates the regenerate endpoint
    takes. `None` for ancillary stages that aren't a numbered slot (the composed
    official video, the feature-image prompt)."""
    key = (stage_key or "").strip()
    for pattern, kind in _MANDATE_KINDS:
        match = pattern.match(key)
        if match:
            return kind, int(match.group(1))
    return None


__all__ = [
    "AUDIO_STAGE",
    "SCRIPT_STAGE",
    "expected_ancillary_stages",
    "is_ancillary_stage",
    "is_essential_stage",
    "mandate_for_stage",
]
