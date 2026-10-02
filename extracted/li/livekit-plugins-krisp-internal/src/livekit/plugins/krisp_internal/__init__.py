# Copyright (c) 2025 LiveKit, Inc. All rights reserved.
# Proprietary and confidential.

from importlib.metadata import PackageNotFoundError, version

from .plugin import VivaMode, KrispVivaFilterFrameProcessor

try:
    __version__ = version("livekit-plugins-krisp-internal")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["VivaMode", "KrispVivaFilterFrameProcessor", "__version__"]
