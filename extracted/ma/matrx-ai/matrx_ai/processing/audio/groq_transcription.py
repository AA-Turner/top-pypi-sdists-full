"""Deprecated import path for the Groq STT provider adapter.

Use ``matrx_ai.processing.audio.execute_stt`` for catalog dispatch. This
re-export keeps direct package consumers source-compatible while provider SDK
access stays under ``matrx_ai.providers``.
"""

from matrx_ai.processing.audio.stt import STTResult, STTUsage
from matrx_ai.providers.groq.stt import GroqSTT

# Compatibility result names; the old synchronous, model-owning client is gone.
TranscriptionResult = STTResult
TranscriptionUsage = STTUsage

__all__ = ["GroqSTT", "TranscriptionResult", "TranscriptionUsage"]
