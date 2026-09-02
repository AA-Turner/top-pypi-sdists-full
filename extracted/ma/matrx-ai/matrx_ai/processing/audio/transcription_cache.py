"""
Transcription Cache

Simple in-memory cache for audio transcriptions to avoid re-transcribing
the same audio files across different requests.

Cache is keyed by (audio_source, model, language) to ensure we only reuse
transcriptions that used the same settings.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass
class CachedTranscription:
    """Cached transcription result"""
    
    text: str
    """The transcribed text"""
    
    metadata: dict[str, Any]
    """Metadata from the transcription (usage, quality metrics, etc.)"""

class TranscriptionCache:
    """
    Simple in-memory cache for transcriptions.
    
    Caches transcriptions by (audio_source, model, language) to avoid
    re-transcribing the same audio with the same settings.
    """
    
    def __init__(self):
        self._cache: dict[str, CachedTranscription] = {}
    
    def _generate_key(
        self, 
        audio_source: str, 
        model: str, 
        language: str | None
    ) -> str:
        """
        Generate cache key from audio source, model, and language.
        
        Uses hash of the audio source for reasonable key length.
        """
        # Hash the audio source to create a reasonable key
        source_hash = hashlib.md5(audio_source.encode()).hexdigest()[:16]
        
        # Combine with model and language
        lang_str = language or "auto"
        return f"{source_hash}:{model}:{lang_str}"
    
    def get(
        self, 
        audio_source: str, 
        model: str, 
        language: str | None
    ) -> CachedTranscription | None:
        """
        Get cached transcription if available.
        
        Args:
            audio_source: URL, file path, or base64 data
            model: Whisper model name
            language: Language code (or None for auto-detect)
        
        Returns:
            CachedTranscription if found, None otherwise
        """
        key = self._generate_key(audio_source, model, language)
        return self._cache.get(key)
    
    def set(
        self,
        audio_source: str,
        model: str,
        language: str | None,
        text: str,
        metadata: dict[str, Any]
    ) -> None:
        """
        Cache a transcription result.
        
        Args:
            audio_source: URL, file path, or base64 data
            model: Whisper model name
            language: Language code (or None for auto-detect)
            text: Transcribed text
            metadata: Transcription metadata (usage, quality metrics, etc.)
        """
        key = self._generate_key(audio_source, model, language)
        self._cache[key] = CachedTranscription(text=text, metadata=metadata)
    
    def clear(self) -> None:
        """Clear all cached transcriptions"""
        self._cache.clear()
    
    def size(self) -> int:
        """Get number of cached transcriptions"""
        return len(self._cache)

# Global cache instance
_global_cache = TranscriptionCache()

def get_cache() -> TranscriptionCache:
    """Get the global transcription cache instance"""
    return _global_cache

def clear_cache() -> None:
    """Clear the global transcription cache"""
    _global_cache.clear()
