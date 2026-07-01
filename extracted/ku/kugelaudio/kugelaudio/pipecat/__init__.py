# Copyright 2024 KugelAudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
KugelAudio Pipecat TTS Service.

This module provides integration between KugelAudio TTS and the Pipecat framework.

Example usage:
    from kugelaudio.pipecat import KugelAudioTTSService

    tts = KugelAudioTTSService(
        api_key="your-api-key",
        voice_id=280,
        model="kugel-1-turbo",
    )

    # Use in a Pipecat pipeline
    pipeline = Pipeline([..., tts, ...])
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kugelaudio.pipecat.tts import KugelAudioTTSService as KugelAudioTTSService
    from kugelaudio.pipecat.models import TTSModels as TTSModels

try:
    from pipecat.services.tts_service import TTSService

    _PIPECAT_AVAILABLE = True
except ImportError:
    _PIPECAT_AVAILABLE = False


def _check_pipecat_installed() -> None:
    """Check if pipecat-ai is installed."""
    if not _PIPECAT_AVAILABLE:
        raise ImportError(
            "pipecat-ai is required for Pipecat integration. "
            "Install with: pip install kugelaudio[pipecat]"
        )


# Lazy imports to avoid requiring pipecat-ai when just importing the SDK
def __getattr__(name: str):
    """Lazy import KugelAudioTTSService and related classes."""
    if name == "KugelAudioTTSService":
        _check_pipecat_installed()
        from kugelaudio.pipecat.tts import KugelAudioTTSService

        return KugelAudioTTSService

    if name == "TTSModels":
        from kugelaudio.pipecat.models import TTSModels

        return TTSModels

    if name in (
        "DEFAULT_MODEL",
        "DEFAULT_SAMPLE_RATE",
        "DEFAULT_VOICE_ID",
        "DEFAULT_CFG_SCALE",
        "DEFAULT_MAX_NEW_TOKENS",
        "SUPPORTED_SAMPLE_RATES",
    ):
        from kugelaudio.pipecat import models

        return getattr(models, name)

    if name == "__version__":
        from kugelaudio import __version__

        return __version__

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "KugelAudioTTSService",
    "TTSModels",
    "DEFAULT_MODEL",
    "DEFAULT_SAMPLE_RATE",
    "DEFAULT_VOICE_ID",
    "DEFAULT_CFG_SCALE",
    "DEFAULT_MAX_NEW_TOKENS",
    "SUPPORTED_SAMPLE_RATES",
    "__version__",
]
