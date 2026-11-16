"""Serving-device observations attached to an exact sample."""

from .hardware import (
    GpuAttribution,
    GpuReading,
    GpuUnsupported,
    SampleHardware,
    SampleHardwarePoint,
)

__all__ = ["GpuAttribution", "GpuReading", "GpuUnsupported", "SampleHardware", "SampleHardwarePoint"]
