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

"""Models and type definitions for KugelAudio LiveKit TTS plugin."""

from typing import Literal

# Available TTS models
TTSModels = Literal["kugel-2-turbo", "kugel-2.5", "kugel-1-turbo", "kugel-1"]

# Default model (premium 7B; matches public API default)
DEFAULT_MODEL: TTSModels = "kugel-2.5"

# Supported sample rates
# The model generates audio at 24kHz natively; other rates use server-side resampling
SUPPORTED_SAMPLE_RATES = (24000, 22050, 16000, 8000)
DEFAULT_SAMPLE_RATE = 24000

# Default voice ID (None means use server default)
DEFAULT_VOICE_ID = None

# Default CFG scale for generation
DEFAULT_CFG_SCALE = 2.0

# Default max tokens
DEFAULT_MAX_NEW_TOKENS = 2048
