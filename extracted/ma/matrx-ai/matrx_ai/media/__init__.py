"""
AI Media — MIME detection and persistence for AI-generated content.

Usage:
    from matrx_ai.media import detect_mime_type, save_media, fetch_media
    from matrx_ai.media import AIMediaHandler, EXTENSION_MIME_MAP
"""

from .media_persistence import (
    AIMediaHandler,
    BORN_PUBLIC_FEATURES,
    MediaPersistResult,
    fetch_media,
    persist_media_blobs_async,
    public_media_scope,
    public_media_scope_active,
    resolve_default_visibility,
    save_media,
    save_media_envelope_async,
)
from .file_handles import (
    DegradedFinding,
    FileHandleError,
    HandleMap,
    InjectionResult,
    OrdinalError,
    ReconcileSpec,
    ReconciliationReport,
    UnknownHandleError,
    inject_file_handles,
    resolve_file_handles,
)
from .mime_utils import EXTENSION_MIME_MAP, detect_mime_type
from .naming import ai_filename_async, slugify_prompt

__all__ = [
    "AIMediaHandler",
    "BORN_PUBLIC_FEATURES",
    "MediaPersistResult",
    "resolve_default_visibility",
    "EXTENSION_MIME_MAP",
    "detect_mime_type",
    "fetch_media",
    "persist_media_blobs_async",
    "public_media_scope",
    "public_media_scope_active",
    "save_media",
    "save_media_envelope_async",
    "slugify_prompt",
    "ai_filename_async",
    # Agent file handles (platform primitive — see file_handles.py / FEATURE.md)
    "DegradedFinding",
    "FileHandleError",
    "HandleMap",
    "InjectionResult",
    "OrdinalError",
    "ReconcileSpec",
    "ReconciliationReport",
    "UnknownHandleError",
    "inject_file_handles",
    "resolve_file_handles",
]
