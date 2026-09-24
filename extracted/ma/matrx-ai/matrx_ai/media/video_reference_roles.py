"""Video-generation reference roles — the ONE vocabulary and the ONE gate.

A video model reads every input it is given AS something
(``common-docs/systems/agents/typed-messages/FEATURE.md``, the Video generation
row; research in ``common-docs/operations/for-arman/2026-09-20/
typed-message-system-design.md`` §2 Video):

    image  first_frame   the clip starts on this exact image
           last_frame    the clip ends on this exact image
           asset         keep this subject/object/character in the clip
           style         take its look only
    video  extend        continue this clip
           restyle       re-render this clip (new look, same motion)
    audio  lip_sync      the speech the on-screen face mouths

A reference may also carry a ``name`` (Kling elements, Pika storyboards): the
prompt addresses it as ``@name``. A name is a TAG on an asset/style image or a
reference video, never a role of its own.

The image roles live in ``image_reference_roles`` (one image vocabulary); the
video/audio roles and the named-reference cap live here. Limits are catalog
data on the offering (``ai.offering.capabilities_override``):

    image_reference_roles  {first_frame: 1, last_frame: 1, asset: 3, style: 0, total: 3}
    video_reference_roles  {extend: 1, restyle: 1, lip_sync: 1, named: 4}

A role absent from the map, or mapped to 0, is one the model cannot take. Each
video adapter declares what its route can carry
(``BaseMediaGeneration.video_role_transport``). Any miss is an
:class:`ImageRoleCompatibilityError` naming the role and the model, raised
BEFORE the paid call. Never a silent drop.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any, Literal, get_args

from matrx_ai.media.image_reference_roles import (
    ROLE_LABELS as IMAGE_ROLE_LABELS,
)
from matrx_ai.media.image_reference_roles import (
    TOTAL_KEY,
    VIDEO_IMAGE_ROLES,
    ImageRoleCompatibilityError,
)

VideoReferenceRole = Literal["extend", "restyle"]
AudioReferenceRole = Literal["lip_sync"]

VIDEO_REFERENCE_ROLES: tuple[str, ...] = get_args(VideoReferenceRole)
AUDIO_REFERENCE_ROLES: tuple[str, ...] = get_args(AudioReferenceRole)

#: Key in ``capabilities.video_reference_roles`` for the named-reference cap.
NAMED_KEY = "named"

#: Transport token an adapter returns when it can carry named references.
NAMED_TRANSPORT = "named"

#: Transport token an adapter returns when it can carry ``camera_control``.
CAMERA_TRANSPORT = "camera_control"

VIDEO_ROLE_LABELS: dict[str, str] = {
    "extend": "Extend",
    "restyle": "Restyle",
    "lip_sync": "Lip sync",
}

#: Every video-side label, image roles included — keep in lockstep with the
#: frontend (features/agents/image-roles/roles.ts).
ALL_LABELS: dict[str, str] = {
    **{r: IMAGE_ROLE_LABELS[r] for r in VIDEO_IMAGE_ROLES},
    **VIDEO_ROLE_LABELS,
}

#: Legacy ``metadata.role`` tags agent templates already carry. A typed role
#: wins; these still work so no existing template breaks.
LEGACY_ALIASES: dict[str, tuple[str, ...]] = {
    "first_frame": ("start_image",),
    "last_frame": ("end_image", "last_frame_image"),
    "asset": ("reference",),
}

_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,31}$")


def validate_video_role(value: Any) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, str) and value in VIDEO_REFERENCE_ROLES:
        return value
    raise ValueError(
        f"Unknown video reference role {value!r}. Allowed: "
        + ", ".join(VIDEO_REFERENCE_ROLES)
        + ". Leave it empty for a plain video."
    )


def validate_audio_role(value: Any) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, str) and value in AUDIO_REFERENCE_ROLES:
        return value
    raise ValueError(
        f"Unknown audio reference role {value!r}. Allowed: "
        + ", ".join(AUDIO_REFERENCE_ROLES)
        + ". Leave it empty for a plain audio clip."
    )


def validate_reference_name(value: Any) -> str | None:
    """A tag the prompt addresses as ``@name``: a letter, then letters,
    digits, ``_`` or ``-`` (max 32). A leading ``@`` is accepted and dropped."""
    if value is None or value == "":
        return None
    if isinstance(value, str):
        candidate = value.strip().lstrip("@")
        if _NAME_RE.match(candidate):
            return candidate
    raise ValueError(
        f"Reference name {value!r} is not a usable tag. Use a short word the "
        "prompt can address as @name: start with a letter, then letters, "
        "digits, '_' or '-'."
    )


def normalize_video_limits(raw: Any) -> dict[str, int]:
    if not isinstance(raw, Mapping):
        return {}
    allowed = set(VIDEO_REFERENCE_ROLES) | set(AUDIO_REFERENCE_ROLES) | {NAMED_KEY}
    out: dict[str, int] = {}
    for key, value in raw.items():
        if key not in allowed:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            continue
        out[key] = value
    return out


def _typed_role(content: Any) -> str | None:
    value = getattr(content, "role", None)
    if value is None and isinstance(content, dict):
        value = content.get("role")
    return value if isinstance(value, str) and value else None


def _legacy_role(content: Any) -> str | None:
    meta = getattr(content, "metadata", None)
    if isinstance(meta, dict):
        value = meta.get("role")
        if isinstance(value, str) and value:
            return value
    return None


def reference_name(content: Any) -> str | None:
    value = getattr(content, "name", None)
    if value is None and isinstance(content, dict):
        value = content.get("name")
    return value if isinstance(value, str) and value else None


def collect_video_references(messages: Any) -> dict[str, list[Any]]:
    """User media blocks that carry a video-side role, grouped by role, in
    message order (oldest first). Legacy ``metadata.role`` tags fold into
    their typed role (``start_image`` -> ``first_frame`` ...)."""
    from matrx_ai.config.media_config import AudioContent, ImageContent, VideoContent

    legacy_to_typed = {old: new for new, olds in LEGACY_ALIASES.items() for old in olds}
    grouped: dict[str, list[Any]] = {}
    for msg in messages or []:
        if getattr(msg, "role", None) != "user":
            continue
        for content in getattr(msg, "content", None) or []:
            role: str | None = None
            if isinstance(content, ImageContent):
                role = _typed_role(content)
                if role is None:
                    role = legacy_to_typed.get(_legacy_role(content) or "")
            elif isinstance(content, (VideoContent, AudioContent)):
                role = _typed_role(content)
            if role is not None:
                grouped.setdefault(role, []).append(content)
    return grouped


def first_of(references: Mapping[str, list[Any]], role: str) -> Any:
    """The LAST-authored block of a single-slot role (most recent intent wins)."""
    items = references.get(role) or []
    return items[-1] if items else None


def named_references(references: Mapping[str, list[Any]]) -> list[tuple[str, str, Any]]:
    """``(name, role, content)`` for every tagged reference, in role order."""
    out: list[tuple[str, str, Any]] = []
    for role in (*VIDEO_IMAGE_ROLES, *VIDEO_REFERENCE_ROLES, *AUDIO_REFERENCE_ROLES):
        for content in references.get(role) or []:
            name = reference_name(content)
            if name:
                out.append((name, role, content))
    return out


def enforce_video_roles(
    references: Mapping[str, list[Any]],
    *,
    image_limits: Mapping[str, int],
    video_limits: Mapping[str, int],
    transport: Iterable[str],
    model: str,
    camera_control: Any = None,
) -> None:
    """Refuse (raise) unless every role, count, name and control fits.

    Order is the order a person fixes them: can the model take this role at
    all, can this route carry it, is there room for this many."""
    transport_set = frozenset(transport)

    for role, items in references.items():
        if not items:
            continue
        if role not in ALL_LABELS:
            label = IMAGE_ROLE_LABELS.get(role, role)
            raise ImageRoleCompatibilityError(
                f"{model} generates video; a {label} image is an image-generation "
                f"role. Use First frame, Last frame, Asset or Style, or pick an "
                f"image model.",
                role=role,
                model=model,
            )

    image_total = 0
    for role in (*VIDEO_IMAGE_ROLES, *VIDEO_REFERENCE_ROLES, *AUDIO_REFERENCE_ROLES):
        items = references.get(role) or []
        if not items:
            continue
        label = ALL_LABELS[role]
        noun = "image" if role in VIDEO_IMAGE_ROLES else (
            "audio clip" if role in AUDIO_REFERENCE_ROLES else "video"
        )
        limits = image_limits if role in VIDEO_IMAGE_ROLES else video_limits
        allowed = limits.get(role, 0)
        if allowed <= 0:
            raise ImageRoleCompatibilityError(
                f"{model} cannot take a {label} {noun}. Remove the {label} role, "
                f"or pick a video model that accepts it.",
                role=role,
                model=model,
            )
        if role not in transport_set:
            raise ImageRoleCompatibilityError(
                f"{model} accepts a {label} {noun}, but the route this request is "
                f"served through cannot send one. Pick the model's direct "
                f"offering, or remove the {label} role.",
                role=role,
                model=model,
            )
        if len(items) > allowed:
            raise ImageRoleCompatibilityError(
                f"{model} takes at most {allowed} {label} {noun}"
                f"{'' if allowed == 1 else 's'}; this request has {len(items)}.",
                role=role,
                model=model,
            )
        if role in VIDEO_IMAGE_ROLES:
            image_total += len(items)

    cap = image_limits.get(TOTAL_KEY)
    if cap is not None and image_total > cap:
        raise ImageRoleCompatibilityError(
            f"{model} takes at most {cap} reference images in total; this request "
            f"has {image_total}.",
            role=None,
            model=model,
        )

    if references.get("last_frame") and not references.get("first_frame"):
        raise ImageRoleCompatibilityError(
            "A Last frame needs a First frame to travel from. Add the first "
            "frame, or remove the Last frame role.",
            role="last_frame",
            model=model,
        )

    named = named_references(references)
    if named:
        seen: set[str] = set()
        for name, _role, _content in named:
            if name.lower() in seen:
                raise ImageRoleCompatibilityError(
                    f"Two references are named @{name}. Give each one its own name.",
                    role=None,
                    model=model,
                )
            seen.add(name.lower())
        for name, role, _content in named:
            if role in ("first_frame", "last_frame", "lip_sync"):
                raise ImageRoleCompatibilityError(
                    f"@{name} is a {ALL_LABELS[role]}; only Asset and Style images "
                    "and reference videos can carry a name the prompt addresses.",
                    role=role,
                    model=model,
                )
        allowed_named = video_limits.get(NAMED_KEY, 0)
        if allowed_named <= 0 or NAMED_TRANSPORT not in transport_set:
            raise ImageRoleCompatibilityError(
                f"{model} cannot take named references (@{named[0][0]}). Remove "
                "the names, or pick a model with named elements.",
                role=None,
                model=model,
            )
        if len(named) > allowed_named:
            raise ImageRoleCompatibilityError(
                f"{model} takes at most {allowed_named} named references; this "
                f"request has {len(named)}.",
                role=None,
                model=model,
            )

    if camera_control and CAMERA_TRANSPORT not in transport_set:
        raise ImageRoleCompatibilityError(
            f"{model} takes no structured camera control on this route. Clear "
            "Camera control, or pick a model that takes camera moves.",
            role=None,
            model=model,
        )


def named_legend(
    named: list[tuple[str, str, Any]], position_of: Mapping[int, int] | None = None
) -> str:
    """"@hero is reference image 1." lines: how a list transport tells the
    model which reference each ``@name`` in the prompt addresses. ``position_of``
    maps ``id(content)`` -> 1-based position in the wire list."""
    lines: list[str] = []
    for index, (name, role, content) in enumerate(named, start=1):
        pos = (position_of or {}).get(id(content), index)
        noun = "reference video" if role in VIDEO_REFERENCE_ROLES else (
            "style reference image" if role == "style" else "reference image"
        )
        lines.append(f"@{name} is {noun} {pos}.")
    return "\n".join(lines)


def with_named_legend(prompt: str, legend: str) -> str:
    if not legend:
        return prompt
    return f"{prompt}\n\n{legend}" if prompt else legend


# ---------------------------------------------------------------------------
# Structured camera control — ONE canonical shape, vendor-scoped mappings.
# ---------------------------------------------------------------------------

#: Canonical moves (Luma's concept vocabulary is the richest public set; the
#: axis moves are the ones Kling's camera_control can express).
CAMERA_MOVES: tuple[str, ...] = (
    "static", "pan_left", "pan_right", "tilt_up", "tilt_down", "zoom_in",
    "zoom_out", "push_in", "pull_out", "truck_left", "truck_right",
    "pedestal_up", "pedestal_down", "roll_left", "roll_right", "orbit_left",
    "orbit_right", "crane_up", "crane_down", "dolly_zoom", "handheld",
    "aerial", "aerial_drone", "overhead", "low_angle", "high_angle",
    "eye_level", "ground_level", "over_the_shoulder", "pov", "selfie",
    "bolt_cam", "tiny_planet", "elevator_doors",
)


def validate_camera_control(value: Any) -> dict[str, Any] | None:
    """``{"moves": [move, ...], "strength": 0..1?}`` or None."""
    if value is None or value == {} or value == "":
        return None
    if not isinstance(value, Mapping):
        raise ValueError("camera_control must be an object: {moves: [...], strength?}")
    moves = value.get("moves")
    if not isinstance(moves, list) or not moves:
        raise ValueError("camera_control.moves must list at least one camera move")
    bad = [m for m in moves if m not in CAMERA_MOVES]
    if bad:
        raise ValueError(
            f"Unknown camera move(s) {bad}. Allowed: " + ", ".join(CAMERA_MOVES)
        )
    out: dict[str, Any] = {"moves": list(dict.fromkeys(moves))}
    strength = value.get("strength")
    if strength is not None:
        if isinstance(strength, bool) or not isinstance(strength, (int, float)) or not (
            0 <= float(strength) <= 1
        ):
            raise ValueError("camera_control.strength must be a number from 0 to 1")
        out["strength"] = float(strength)
    return out


def camera_to_luma_concepts(camera: Mapping[str, Any]) -> list[str]:
    """Luma Ray ``concepts``: the moves, verbatim (same vocabulary)."""
    return list(camera.get("moves") or [])


_KLING_AXES: dict[str, tuple[str, int]] = {
    "truck_left": ("horizontal", -1), "truck_right": ("horizontal", 1),
    "pedestal_down": ("vertical", -1), "pedestal_up": ("vertical", 1),
    "pan_left": ("pan", -1), "pan_right": ("pan", 1),
    "tilt_down": ("tilt", -1), "tilt_up": ("tilt", 1),
    "roll_left": ("roll", -1), "roll_right": ("roll", 1),
    "zoom_out": ("zoom", -1), "zoom_in": ("zoom", 1),
    "pull_out": ("zoom", -1), "push_in": ("zoom", 1),
}


def camera_to_kling(camera: Mapping[str, Any]) -> dict[str, Any]:
    """Kling ``camera_control``: ONE axis move of -10..10 (Kling takes exactly
    one non-zero axis). Several moves, or a move with no axis, RAISE."""
    moves = list(camera.get("moves") or [])
    if moves == ["static"]:
        return {"type": "simple", "config": {k: 0 for k in (
            "horizontal", "vertical", "pan", "tilt", "roll", "zoom")}}
    axis_moves = [m for m in moves if m in _KLING_AXES]
    if len(axis_moves) != 1 or len(moves) != 1:
        raise ValueError(
            "Kling takes exactly one axis camera move (pan, tilt, roll, zoom, "
            f"truck or pedestal); this request asks for {moves}."
        )
    axis, sign = _KLING_AXES[axis_moves[0]]
    magnitude = max(1, round(10 * float(camera.get("strength", 0.5))))
    config = {k: 0 for k in ("horizontal", "vertical", "pan", "tilt", "roll", "zoom")}
    config[axis] = sign * magnitude
    return {"type": "simple", "config": config}


__all__ = [
    "ALL_LABELS",
    "AUDIO_REFERENCE_ROLES",
    "CAMERA_MOVES",
    "CAMERA_TRANSPORT",
    "LEGACY_ALIASES",
    "NAMED_KEY",
    "NAMED_TRANSPORT",
    "VIDEO_REFERENCE_ROLES",
    "VIDEO_ROLE_LABELS",
    "AudioReferenceRole",
    "VideoReferenceRole",
    "camera_to_kling",
    "camera_to_luma_concepts",
    "collect_video_references",
    "enforce_video_roles",
    "first_of",
    "named_legend",
    "named_references",
    "normalize_video_limits",
    "reference_name",
    "validate_audio_role",
    "validate_camera_control",
    "validate_reference_name",
    "validate_video_role",
    "with_named_legend",
]
