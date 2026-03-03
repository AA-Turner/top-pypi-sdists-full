"""Segmentation client (SAM3 + OmniParser).

Usage:
    from plato.segmentation import Segmentation, AsyncSegmentation

    client = Segmentation(base_url="http://localhost:8100")
    result = client.predict("path/to/image.jpg", "truck")
    print(result.boxes, result.scores)

    # Iterate detections
    for det in result:
        print(det.score, det.box)
        det.extract(image).save(f"det_{det.index}.png")

    # UI parsing (OmniParser)
    ui = client.parse_ui("screenshot.png")
    for el in ui:
        print(el.element_type, el.content, el.bbox_pixels)

    # Visualization
    from plato.segmentation.visualization import render_overlay, save_extractions
    render_overlay(image, result).save("overlay.png")
    save_extractions(image, result, "segments/")

    # Batch
    results = client.predict_batch([
        {"image": "a.jpg", "prompt": "car"},
        {"image": "b.jpg", "prompt": "person"},
    ])
"""

from plato.segmentation.models import (
    BatchResult,
    Detection,
    MaskRLE,
    PredictionResult,
    UIElement,
    UIParseResult,
)
from plato.segmentation.sdk import AsyncSegmentation, Segmentation, SegmentationServerError


def __getattr__(name: str):  # noqa: N807
    """Lazy-load visualization helpers (requires numpy + Pillow from plato[segmentation])."""
    if name in ("render_overlay", "save_extractions"):
        from plato.segmentation import visualization

        return getattr(visualization, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Segmentation",
    "AsyncSegmentation",
    "SegmentationServerError",
    "PredictionResult",
    "BatchResult",
    "Detection",
    "MaskRLE",
    "UIElement",
    "UIParseResult",
    "render_overlay",
    "save_extractions",
]
