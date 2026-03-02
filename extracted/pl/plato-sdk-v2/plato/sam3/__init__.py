"""SAM3 (Segment Anything Model 3) client.

Usage:
    from plato.sam3 import Sam3, AsyncSam3

    sam3 = Sam3(base_url="http://localhost:8100")
    result = sam3.predict("path/to/image.jpg", "truck")
    print(result.boxes, result.scores)

    # Iterate detections
    for det in result:
        print(det.score, det.box)
        det.extract(image).save(f"det_{det.index}.png")

    # Visualization
    from plato.sam3.visualization import render_overlay, save_extractions
    render_overlay(image, result).save("overlay.png")
    save_extractions(image, result, "segments/")

    # Batch
    results = sam3.predict_batch([
        {"image": "a.jpg", "prompt": "car"},
        {"image": "b.jpg", "prompt": "person"},
    ])
"""

from plato.sam3.models import BatchResult, Detection, MaskRLE, PredictionResult
from plato.sam3.sdk import AsyncSam3, Sam3, Sam3ServerError
from plato.sam3.visualization import render_overlay, save_extractions

__all__ = [
    "Sam3",
    "AsyncSam3",
    "Sam3ServerError",
    "PredictionResult",
    "BatchResult",
    "Detection",
    "MaskRLE",
    "render_overlay",
    "save_extractions",
]
