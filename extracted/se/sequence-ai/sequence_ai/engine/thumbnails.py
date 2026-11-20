# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
What a server shows of a robot's episode now, for a page that watches it: each camera's newest frame as a small JPEG -
made only while someone looks at the robot, never on an act's path. A deployment's worker and a policy server of your
own alike.

In one sentence: an episode's newest observation, decoded as it came (engine.obs_format), off the act's path → frames():
each image in it shrunk to THUMB pixels a side and encoded as a JPEG, or a robot-arm Observation's own JPEGs as they
came → with the episode's latest answers and its seq.plans, the view its server hands the page
(RegisteredAdapter.robot_view).
"""
from __future__ import annotations

import base64
import io
from typing import Any

import numpy as np

THUMB = 320                  # the longest side of a frame on the page, in pixels
_CAMERAS = 8                 # the most frames one view carries
_JPEG_CHARS = 700_000        # a robot's own JPEG past this is left out (the gateway keeps no more)


def frames(observation: Any) -> list[dict]:
    """Each image of an observation as {"name": where it is in the observation, "jpeg": base64, "width", "height"}: an
    array of 8-bit pixels (HxW or HxWx1/3/4) shrunk and encoded, or a robot-arm Observation's frames as they came."""
    out: list[dict] = []
    _walk(observation, "", out)
    return out[:_CAMERAS]


def _walk(value: Any, path: str, out: list[dict]) -> None:
    if len(out) >= _CAMERAS:
        return
    if isinstance(value, np.ndarray):
        if _image(value):
            jpeg, w, h = _jpeg(value)
            out.append({"name": path or "image", "jpeg": jpeg, "width": w, "height": h})
        return
    if isinstance(value, dict):
        own = value.get("images")
        if path == "" and isinstance(own, list) and all(isinstance(f, dict) and isinstance(f.get("data"), str)
                                                        for f in own):
            for i, f in enumerate(own):           # a robot-arm Observation: its frames are JPEGs already
                if len(f["data"]) <= _JPEG_CHARS:
                    out.append({"name": str(f.get("view") or f"images[{i}]"), "jpeg": f["data"],
                                "width": f.get("width"), "height": f.get("height")})
            return
        for k, v in value.items():
            _walk(v, f"{path}.{k}" if path else str(k), out)
        return
    if isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            _walk(v, f"{path}[{i}]", out)


def _image(a: np.ndarray) -> bool:
    return a.dtype == np.uint8 and (a.ndim == 2 or (a.ndim == 3 and a.shape[-1] in (1, 3, 4))) and min(a.shape[:2]) > 1


def _jpeg(a: np.ndarray) -> tuple[str, int, int]:
    from PIL import Image

    img = Image.fromarray(a[..., 0] if a.ndim == 3 and a.shape[-1] == 1 else a)
    img = img.convert("RGB") if img.mode not in ("RGB", "L") else img
    img.thumbnail((THUMB, THUMB))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode("ascii"), img.width, img.height
