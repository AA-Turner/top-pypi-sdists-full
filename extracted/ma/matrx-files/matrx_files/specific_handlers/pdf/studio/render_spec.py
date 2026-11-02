"""``PdfRenderSpec`` + preset-driven render dispatcher.

Mirrors the shape of ``image_handler.StudioRenderSpec``: one TypedDict per
render target, dispatched through ``render_studio_variant`` to the right
``ops/*`` function based on the preset's operation field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

from ..concurrency import run_in_cpu_executor
from ..ops.render import (
    PdfPageRender,
    render_all_pages_to_image_bytes,
    render_page_to_image_bytes,
    render_thumbnail_bytes,
)
from .presets import PdfStudioPreset, get_pdf_preset_by_id


class PdfRenderSpec(TypedDict, total=False):
    """One Studio render target.

    Mirrors the per-variant spec the FE composes for the Image Studio. Either
    supply *preset_id* to look up params from the catalog, or fill *operation*
    + *params* directly for a one-off render.
    """

    preset_id: str
    operation: Literal["render_page", "render_all", "render_thumbnail"]
    params: dict[str, Any]
    overrides: dict[str, Any]


@dataclass(frozen=True)
class PdfStudioRenderResult:
    """Output of ``render_studio_variant``."""

    preset_id: str | None
    operation: str
    pages: list[PdfPageRender]
    notes: list[str]


_DEFAULT_PARAMS: dict[str, dict[str, Any]] = {
    "render_page": {"page": 1, "dpi": 150, "fmt": "png", "jpeg_quality": 85},
    "render_all": {"dpi": 150, "fmt": "png", "jpeg_quality": 85},
    "render_thumbnail": {"page": 1, "max_side": 256, "fmt": "jpeg", "jpeg_quality": 80},
}


def _resolve_spec(spec: PdfRenderSpec) -> tuple[str, dict[str, Any], PdfStudioPreset | None]:
    preset: PdfStudioPreset | None = None
    operation: str | None = spec.get("operation")  # type: ignore[assignment]
    params: dict[str, Any] = dict(spec.get("params") or {})

    preset_id = spec.get("preset_id")
    if preset_id:
        preset = get_pdf_preset_by_id(preset_id)
        if preset is None:
            raise ValueError(f"Unknown PDF preset id: {preset_id!r}.")
        operation = operation or preset.get("operation")
        merged: dict[str, Any] = dict(preset.get("params") or {})
        merged.update(params)
        params = merged

    if not operation:
        raise ValueError(
            "PdfRenderSpec must include either preset_id or operation."
        )

    overrides = spec.get("overrides") or {}
    params.update(overrides)

    defaults = _DEFAULT_PARAMS.get(operation, {})
    for key, value in defaults.items():
        params.setdefault(key, value)

    return operation, params, preset


def render_studio_variant(
    pdf_bytes: bytes,
    spec: PdfRenderSpec,
) -> PdfStudioRenderResult:
    """Resolve *spec* against the preset catalog and dispatch to the matching op.

    Today supports the render-family operations (``render_page``,
    ``render_all``, ``render_thumbnail``). Future Phase 2/3 work will extend
    this dispatcher to non-render presets without breaking the contract.
    """
    operation, params, preset = _resolve_spec(spec)
    notes: list[str] = []

    if operation == "render_page":
        result = render_page_to_image_bytes(
            pdf_bytes,
            page=int(params.get("page", 1)),
            dpi=int(params.get("dpi", 150)),
            fmt=params.get("fmt", "png"),
            colorspace=params.get("colorspace", "rgb"),
            alpha=bool(params.get("alpha", False)),
            annotations=bool(params.get("annotations", True)),
            jpeg_quality=int(params.get("jpeg_quality", 85)),
            clip=params.get("clip"),
        )
        return PdfStudioRenderResult(
            preset_id=preset["id"] if preset else None,
            operation=operation,
            pages=[result],
            notes=notes,
        )

    if operation == "render_all":
        results = render_all_pages_to_image_bytes(
            pdf_bytes,
            dpi=int(params.get("dpi", 150)),
            fmt=params.get("fmt", "png"),
            colorspace=params.get("colorspace", "rgb"),
            alpha=bool(params.get("alpha", False)),
            annotations=bool(params.get("annotations", True)),
            jpeg_quality=int(params.get("jpeg_quality", 85)),
            pages=params.get("pages"),
        )
        return PdfStudioRenderResult(
            preset_id=preset["id"] if preset else None,
            operation=operation,
            pages=results,
            notes=notes,
        )

    if operation == "render_thumbnail":
        result = render_thumbnail_bytes(
            pdf_bytes,
            page=int(params.get("page", 1)),
            max_side=int(params.get("max_side", 256)),
            fmt=params.get("fmt", "jpeg"),
            jpeg_quality=int(params.get("jpeg_quality", 80)),
        )
        return PdfStudioRenderResult(
            preset_id=preset["id"] if preset else None,
            operation=operation,
            pages=[result],
            notes=notes,
        )

    raise ValueError(
        f"Operation {operation!r} is not supported by render_studio_variant "
        f"in Phase 2. Supported: render_page, render_all, render_thumbnail."
    )


async def render_studio_variant_async(
    pdf_bytes: bytes,
    spec: PdfRenderSpec,
) -> PdfStudioRenderResult:
    return await run_in_cpu_executor(render_studio_variant, pdf_bytes, spec)


__all__ = [
    "PdfRenderSpec",
    "PdfStudioRenderResult",
    "render_studio_variant",
    "render_studio_variant_async",
]
