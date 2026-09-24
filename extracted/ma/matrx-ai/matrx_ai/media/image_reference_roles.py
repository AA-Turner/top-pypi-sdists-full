"""Image-generation reference roles — the ONE vocabulary and the ONE gate.

A reference image in an image-generation request is never an unlabeled pile:
each image says what it controls (``common-docs/systems/agents/typed-messages/
FEATURE.md``, the Image generation row; research in
``common-docs/operations/for-arman/2026-09-20/typed-message-system-design.md``).

    subject              keep this object/product recognisable
    character            keep this person/character consistent
    style                transfer look (palette, medium, lighting), not content
    mask                 which region of the edit target may change
    edit_target          the base image being edited
    composition_control  geometry/layout to follow (depth, edge, sketch)

Video generation reads an image as a frame or a reference (the Video
generation row; the video-side gate is ``media/video_reference_roles.py``):

    first_frame          the clip starts on this exact image
    last_frame           the clip ends on this exact image
    asset                keep this subject/object/character in the clip
    style                (shared) take its look only

The role rides on the image part itself (``ImageContent.role`` /
``ImageMediaPart.role``). Absent role = today's behaviour: a plain image the
model sees.

Three facts decide whether a request goes out:

1. The MODEL's limits — ``capabilities.image_reference_roles`` on the catalog
   (``{role: max_count, ..., "total": n}``), resolved into
   ``ResolvedModelCapabilities.image_reference_limits``. A role absent from the
   map, or mapped to 0, is a role the model cannot take.
2. The ROUTE's transport — the roles this provider adapter can actually put on
   the wire (``BaseMediaGeneration.image_role_transport``).
3. The COUNTS in the request.

Any miss is an :class:`ImageRoleCompatibilityError` naming the role and the
model, raised BEFORE the paid call. Never a silent drop.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal, get_args

ImageReferenceRole = Literal[
    "subject",
    "character",
    "style",
    "mask",
    "edit_target",
    "composition_control",
    # Video-generation image roles (``style`` is shared with image generation).
    "first_frame",
    "last_frame",
    "asset",
]

IMAGE_REFERENCE_ROLES: tuple[str, ...] = get_args(ImageReferenceRole)

#: The roles an IMAGE-generating model can take (the image gate's order).
IMAGE_GENERATION_ROLES: tuple[str, ...] = (
    "subject",
    "character",
    "style",
    "mask",
    "edit_target",
    "composition_control",
)

#: The image roles a VIDEO-generating model can take.
VIDEO_IMAGE_ROLES: tuple[str, ...] = ("first_frame", "last_frame", "asset", "style")

#: Reserved key in ``capabilities.image_reference_roles`` for the combined cap.
TOTAL_KEY = "total"

#: Plain names, used in refusals and prompt legends. Keep in lockstep with the
#: frontend labels (features/agents/image-roles/roles.ts).
ROLE_LABELS: dict[str, str] = {
    "subject": "Subject",
    "character": "Character",
    "style": "Style",
    "mask": "Mask",
    "edit_target": "Edit this",
    "composition_control": "Composition",
    "first_frame": "First frame",
    "last_frame": "Last frame",
    "asset": "Asset",
}

#: What the model is told each role means when the transport is a flat image
#: list (Gemini native, FLUX 2, gpt-image edits, nano-banana): the doctrine is
#: "give every reference one role", so the prompt carries the legend.
ROLE_INSTRUCTIONS: dict[str, str] = {
    "subject": (
        "subject reference — keep this exact object or product recognisable: "
        "shape, materials, colours, labels and proportions"
    ),
    "character": (
        "character reference — keep this person or character's identity, face, "
        "build and outfit consistent"
    ),
    "style": (
        "style reference — take only its look (palette, medium, texture, "
        "lighting, mood); do not copy its subjects or layout"
    ),
    "mask": "mask — only the marked region of the image being edited may change",
    "edit_target": (
        "image to edit — change only what the prompt asks and preserve "
        "everything else exactly"
    ),
    "composition_control": (
        "composition reference — follow its layout, pose and geometry; do not "
        "copy its appearance"
    ),
    "first_frame": "first frame — the video starts on exactly this image",
    "last_frame": "last frame — the video ends on exactly this image",
    "asset": (
        "asset reference — keep this subject, object or character recognisable "
        "and consistent throughout the video"
    ),
}


class ImageRoleCompatibilityError(ValueError):
    """A reference-image role the selected model or route cannot take."""

    def __init__(self, message: str, *, role: str | None, model: str) -> None:
        super().__init__(message)
        self.role = role
        self.model = model


def validate_role(value: Any) -> str | None:
    """Canonical role or None. An unknown non-empty value RAISES — a typo'd
    role must never degrade into an unlabeled image."""
    if value is None or value == "":
        return None
    if isinstance(value, str) and value in IMAGE_REFERENCE_ROLES:
        return value
    raise ValueError(
        f"Unknown image reference role {value!r}. Allowed: "
        + ", ".join(IMAGE_REFERENCE_ROLES)
        + ". Leave it empty for a plain image."
    )


def role_of(content: Any) -> str | None:
    """The typed role on an image content block (dataclass, model or dict)."""
    value = getattr(content, "role", None)
    if value is None and isinstance(content, dict):
        value = content.get("role")
    return value if isinstance(value, str) and value in IMAGE_REFERENCE_ROLES else None


def collect_role_images(messages: Any) -> dict[str, list[Any]]:
    """User image blocks that carry a typed role, grouped by role, in message
    order (oldest first) so "Image 1, Image 2" legends are stable."""
    from matrx_ai.config.media_config import ImageContent

    grouped: dict[str, list[Any]] = {}
    for msg in messages or []:
        if getattr(msg, "role", None) != "user":
            continue
        for content in getattr(msg, "content", None) or []:
            if not isinstance(content, ImageContent):
                continue
            role = role_of(content)
            if role is not None:
                grouped.setdefault(role, []).append(content)
    return grouped


def collect_plain_images(messages: Any) -> list[Any]:
    """User image blocks with NO typed role (and no legacy metadata role) —
    the plain images the model simply sees."""
    from matrx_ai.config.media_config import ImageContent

    out: list[Any] = []
    for msg in messages or []:
        if getattr(msg, "role", None) != "user":
            continue
        for content in getattr(msg, "content", None) or []:
            if not isinstance(content, ImageContent) or role_of(content) is not None:
                continue
            meta = getattr(content, "metadata", None)
            if isinstance(meta, dict) and isinstance(meta.get("role"), str) and meta["role"]:
                continue
            out.append(content)
    return out


def normalize_limits(raw: Any) -> dict[str, int]:
    """``capabilities.image_reference_roles`` -> ``{role|total: int}``.

    Unknown keys and non-integer counts are dropped here; the WRITE path
    (``capability_vocabulary.normalize_capabilities``) rejects them loudly."""
    if not isinstance(raw, Mapping):
        return {}
    out: dict[str, int] = {}
    for key, value in raw.items():
        if key not in IMAGE_REFERENCE_ROLES and key != TOTAL_KEY:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            continue
        out[key] = value
    return out


def enforce_image_roles(
    role_images: Mapping[str, list[Any]],
    *,
    limits: Mapping[str, int],
    transport: Iterable[str],
    model: str,
) -> None:
    """Refuse (raise) unless every role, every count and the total fit.

    Order of checks is the order a person fixes them: can the model take this
    role at all, can this route carry it, is there room for this many."""
    transport_set = frozenset(transport)
    total = 0
    for role in IMAGE_REFERENCE_ROLES:
        images = role_images.get(role) or []
        if not images:
            continue
        label = ROLE_LABELS[role]
        allowed = limits.get(role, 0)
        if allowed <= 0:
            raise ImageRoleCompatibilityError(
                f"{model} cannot take a {label} reference image. Remove the "
                f"{label} role from the image, or pick a model that accepts it.",
                role=role,
                model=model,
            )
        if role not in transport_set:
            raise ImageRoleCompatibilityError(
                f"{model} accepts a {label} reference image, but the route this "
                f"request is served through cannot send one. Pick the model's "
                f"direct offering, or remove the {label} role.",
                role=role,
                model=model,
            )
        if len(images) > allowed:
            raise ImageRoleCompatibilityError(
                f"{model} takes at most {allowed} {label} reference image"
                f"{'' if allowed == 1 else 's'}; this request has {len(images)}.",
                role=role,
                model=model,
            )
        total += len(images)
    cap = limits.get(TOTAL_KEY)
    if cap is not None and total > cap:
        raise ImageRoleCompatibilityError(
            f"{model} takes at most {cap} reference images in total; this request "
            f"has {total}.",
            role=None,
            model=model,
        )
    if role_images.get("mask") and not role_images.get("edit_target"):
        raise ImageRoleCompatibilityError(
            "A Mask image needs an 'Edit this' image to mask. Add the image being "
            "edited, or remove the Mask role.",
            role="mask",
            model=model,
        )


def ordered_role_images(
    role_images: Mapping[str, list[Any]], roles: Iterable[str]
) -> list[tuple[str, Any]]:
    """Flatten the named roles into one ordered list: the edit target first
    (providers treat image 1 as the base), then the rest in vocabulary order."""
    wanted = list(roles)
    order = ["edit_target"] + [r for r in IMAGE_REFERENCE_ROLES if r != "edit_target"]
    out: list[tuple[str, Any]] = []
    for role in order:
        if role not in wanted:
            continue
        for image in role_images.get(role) or []:
            out.append((role, image))
    return out


def role_legend(ordered: list[tuple[str, Any]], *, offset: int = 0) -> str:
    """"Image 1 is the ... ." lines for a flat image-list transport."""
    lines = [
        f"Image {offset + index + 1} is the {ROLE_INSTRUCTIONS[role]}."
        for index, (role, _image) in enumerate(ordered)
    ]
    return "\n".join(lines)


def with_legend(prompt: str, ordered: list[tuple[str, Any]], *, offset: int = 0) -> str:
    """Prompt plus the role legend (unchanged when no roled image exists)."""
    if not ordered:
        return prompt
    legend = role_legend(ordered, offset=offset)
    return f"{prompt}\n\nReference images:\n{legend}" if prompt else legend


def resolve_roled(
    ordered: list[tuple[str, Any]], resolve: Any
) -> list[tuple[str, Any]]:
    """Map each (role, image) through ``resolve`` (image -> wire value). An
    image that resolves to nothing RAISES naming its position and role — a
    reference the person attached is never dropped on the way out."""
    out: list[tuple[str, Any]] = []
    for index, (role, content) in enumerate(ordered, start=1):
        value = resolve(content)
        if not value:
            raise ValueError(
                f"Reference image {index} ({ROLE_LABELS[role]}) could not be read. "
                "Re-upload it and run again."
            )
        out.append((role, value))
    return out


__all__ = [
    "resolve_roled",
    "IMAGE_GENERATION_ROLES",
    "IMAGE_REFERENCE_ROLES",
    "ROLE_INSTRUCTIONS",
    "VIDEO_IMAGE_ROLES",
    "ROLE_LABELS",
    "TOTAL_KEY",
    "ImageReferenceRole",
    "ImageRoleCompatibilityError",
    "collect_plain_images",
    "collect_role_images",
    "enforce_image_roles",
    "normalize_limits",
    "ordered_role_images",
    "role_legend",
    "role_of",
    "validate_role",
    "with_legend",
]
