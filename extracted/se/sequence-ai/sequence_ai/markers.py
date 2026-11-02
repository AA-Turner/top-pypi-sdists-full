"""
The observation format's markers: wrap an item of what the robot observes to say what it is, and observe() sends it
in the form made for it; the worker turns it back into the array it was, so the policy's observe function reads the
data the robot built, item for item. Anything not wrapped travels as it is.

    policy.observe({"head": sequence_ai.Video(frame),            # an RGB camera frame, HxWx3 uint8: low-latency video
                    "wrist_depth": sequence_ai.Depth(depth),    # a depth map, any integer or float dtype: lossless
                    "finger": sequence_ai.Tactile(touch),       # a tactile reading: an image's as high-quality video,
                    "joints": joints})                          #   any other array as it is; unwrapped: as it is

A wrapped item must be the same kind every step, under the same key: each key has an encoder of its own for the
episode. Wrapping is plain Python; sending one needs Python 3.10 or later and `pip install 'sequence-ai[observe]'`
(the encoders: sequence_base.codec.marked, PyAV, zstandard). Markers go in observe(), never in act().


"""
from __future__ import annotations

from typing import Any

__all__ = ["Depth", "Tactile", "Video"]


class _Marked:
    """An item of the observe data and what it is (`kind`, one of sequence_base.codec.marked.KINDS)."""

    kind = ""
    __slots__ = ("value",)

    def __init__(self, value: Any) -> None:
        if isinstance(value, _Marked):
            raise TypeError(f"{type(self).__name__}({type(value).__name__}(...)): an item is marked once")
        self.value = value

    def __repr__(self) -> str:
        shape, dtype = getattr(self.value, "shape", None), getattr(self.value, "dtype", None)
        what = f"{dtype} {tuple(shape)}" if shape is not None else type(self.value).__name__
        return f"{type(self).__name__}({what})"


class Video(_Marked):
    """An RGB camera frame, HxWx3 uint8: sent as low-latency video (H.264), lossy, a keyframe every second."""

    kind = "video"
    __slots__ = ()


class Depth(_Marked):
    """A depth map of any integer or float dtype, in the robot's own unit: sent losslessly, every value as it is."""

    kind = "depth"
    __slots__ = ()


class Tactile(_Marked):
    """A tactile reading: an image's (HxWx3 uint8) as high-quality video, any other array as it is."""

    kind = "tactile"
    __slots__ = ()
