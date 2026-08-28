"""Runtime seam for inference workers.

Exposes :class:`PostProcRunner`, the single per-frame post-processing
entrypoint the ml-codebases inference workers call, plus the pure
:func:`build_stream_info` and :func:`normalize_detections` helpers.
"""

from .post_proc_runner import (
    PostProcRunner,
    build_stream_info,
    normalize_detections,
)

__all__ = [
    "PostProcRunner",
    "build_stream_info",
    "normalize_detections",
]
