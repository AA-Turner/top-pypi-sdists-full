"""Vision-class registry and image re-encoder.

Public surface:

- ``VisionApiClass`` — frozen dataclass describing one re-encoding bundle.
- ``VISION_API_CLASSES`` — the registry, keyed by class name.
- ``MODEL_TO_VISION_CLASS`` — model-name → class name.
- ``WIRE_FORMAT_DEFAULT_VISION_CLASS`` — wire route → class name.
- ``resolve_vision_class(model, wire_format)`` — resolution helper.
- ``is_known_vision_class(name)`` — registry membership check.
- ``reencode_for_vision_class(master_bytes, cls)`` — pure Pillow encoder.
- ``should_skip_reencode(meta, cls)`` — pass-through guard.

The ``configure()`` entrypoint in ``matrx_ai/__init__.py`` registers a
host-injected encoder with ``matrx_files.cloud_sync.variants``
so every ``MediaRef.vision_class`` resolves to a real cld_files variant
without matrx-utils ever importing matrx-ai at module top-level.
"""

from .image_processor import reencode_for_vision_class, should_skip_reencode
from .vision_classes import (
    MODEL_TO_VISION_CLASS,
    VISION_API_CLASSES,
    WIRE_FORMAT_DEFAULT_VISION_CLASS,
    VisionApiClass,
    is_known_vision_class,
    resolve_vision_class,
)

__all__ = [
    "VisionApiClass",
    "VISION_API_CLASSES",
    "MODEL_TO_VISION_CLASS",
    "WIRE_FORMAT_DEFAULT_VISION_CLASS",
    "resolve_vision_class",
    "is_known_vision_class",
    "reencode_for_vision_class",
    "should_skip_reencode",
]
