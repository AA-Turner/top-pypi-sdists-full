"""Auto streaming module for camera and streaming gateway management."""

from .auto_streaming import AutoStreaming
from .auto_streaming_utils import AutoStreamingUtils
from matrice.deploy.client.streaming_gateway import ModelInputType, OutputConfig, InputConfig, InputType

__all__ = [
    "AutoStreaming",
    "AutoStreamingUtils",
    "ModelInputType",
    "OutputConfig",
    "InputConfig",
    "InputType"
] 