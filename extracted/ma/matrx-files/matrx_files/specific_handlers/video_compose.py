"""Video composition — stitch images + videos into one crossfaded slideshow.

A standalone, dependency-light platform primitive: given an ordered list of
media segments (image bytes or video bytes), produce a single MP4 that plays
each segment in turn with smooth crossfade transitions. Every segment is
normalized onto a common wide canvas (16:9 by default); square / portrait
sources are centered over a scaled-and-blurred copy of themselves so the
canvas is filled edge-to-edge instead of black-barred.

This is intentionally transport-agnostic and host-agnostic — it takes bytes
and returns bytes. It is the engine behind the podcast "official video" but
is reusable for any slideshow / sizzle-reel / story-loop feature.

Implementation: a single ``ffmpeg`` ``filter_complex`` invocation. The ffmpeg
binary comes from ``imageio-ffmpeg`` (a bundled static build, so no system
``ffmpeg`` is required on the server), falling back to ``$FFMPEG_BINARY`` or a
``ffmpeg`` on ``PATH``. Video durations are probed with OpenCV (already a core
dependency), so no ``ffprobe`` is needed.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class SlideSegment:
    """One segment in a composed slideshow.

    Parameters
    ----------
    data:
        Raw bytes of the source — an image (PNG/JPEG/WebP/…) or a video
        (MP4/MOV/WebM/…).
    kind:
        ``"image"`` or ``"video"``. Drives how duration is resolved and how
        the source is fed to ffmpeg.
    duration:
        Seconds this segment is on screen. For images this is required
        behavior (falls back to the composer's ``image_duration`` when None).
        For videos, None means "use the video's native duration" (optionally
        capped by the composer's ``max_video_duration``).
    """

    data: bytes
    kind: Literal["image", "video"]
    duration: float | None = None


# Sentinel for "no usable ffmpeg found" so the error is raised lazily at call
# time (keeps `import matrx_utils` working in minimal environments).
class FfmpegNotAvailableError(RuntimeError):
    pass


def _resolve_ffmpeg_binary() -> str:
    """Locate an ffmpeg executable.

    Order: imageio-ffmpeg's bundled static build (most portable — works in a
    bare Docker image), then ``$FFMPEG_BINARY``, then ``ffmpeg`` on PATH.
    """
    try:
        import imageio_ffmpeg

        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except Exception:
        pass

    env_bin = os.environ.get("FFMPEG_BINARY")
    if env_bin and (os.path.exists(env_bin) or shutil.which(env_bin)):
        return env_bin

    which = shutil.which("ffmpeg")
    if which:
        return which

    raise FfmpegNotAvailableError(
        "No ffmpeg binary found. Install the bundled build with the matrx-files[media] extra "
        "(pip install 'matrx-files[media]'), set $FFMPEG_BINARY, or put ffmpeg on PATH."
    )


def _probe_video_duration(path: str) -> float | None:
    """Return a video's duration in seconds via OpenCV, or None if unknown."""
    try:
        import cv2
    except Exception:
        return None

    cap = cv2.VideoCapture(path)
    try:
        if not cap.isOpened():
            return None
        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
        if fps > 0 and frames > 0:
            return float(frames) / float(fps)
    finally:
        cap.release()
    return None


def _normalize_filter(
    idx: int,
    dur: float,
    width: int,
    height: int,
    fps: int,
    blur_sigma: float,
) -> str:
    """Build the per-input filter chain that fits source ``idx`` onto the
    canvas with a blurred fill background, trims to ``dur`` and pins fps/SAR.

    Produces a labeled output ``[v{idx}]``.
    """
    # bg: scale to COVER the canvas (may overflow), crop to exact, blur.
    # fg: scale to FIT inside the canvas (letterbox dims), centered via overlay.
    # Preserve the final frame through scheduled duration and fps/xfade buffering.
    # trim still caps the output; short sources hold their final frame.
    return (
        f"[{idx}:v]split=2[bg{idx}][fg{idx}];"
        f"[bg{idx}]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},gblur=sigma={blur_sigma}[bgb{idx}];"
        f"[fg{idx}]scale={width}:{height}:force_original_aspect_ratio=decrease[fgs{idx}];"
        f"[bgb{idx}][fgs{idx}]overlay=(W-w)/2:(H-h)/2,"
        f"tpad=stop_mode=clone:stop_duration={dur:.3f},"
        f"trim=0:{dur:.3f},setpts=PTS-STARTPTS,fps={fps},setsar=1,"
        f"format=yuv420p[v{idx}]"
    )


def _build_xfade_chain(
    durations: list[float],
    crossfade: float,
    transition: str,
) -> tuple[str, str]:
    """Build the xfade chain that crossfades [v0]..[vN-1] into one stream.

    Returns ``(filter_segment, final_label)``. With a single segment there is
    no transition and the final label is simply ``[v0]``.
    """
    n = len(durations)
    if n == 1:
        return "", "[v0]"

    parts: list[str] = []
    prev_label = "[v0]"
    # Cumulative length of the chain built so far (with overlaps removed).
    elapsed = durations[0]
    for i in range(1, n):
        out_label = "[outv]" if i == n - 1 else f"[x{i}]"
        offset = elapsed - crossfade
        parts.append(
            f"{prev_label}[v{i}]xfade=transition={transition}:"
            f"duration={crossfade:.3f}:offset={offset:.3f}{out_label}"
        )
        elapsed = elapsed + durations[i] - crossfade
        prev_label = out_label

    return ";".join(parts), "[outv]"


def compose_slideshow(
    segments: list[SlideSegment],
    *,
    width: int = 1280,
    height: int = 720,
    fps: int = 30,
    image_duration: float = 3.5,
    max_video_duration: float | None = 8.0,
    crossfade: float = 0.8,
    background_blur: float = 20.0,
    transition: str = "fade",
    audio_bytes: bytes | None = None,
    loop_audio: bool = True,
    crf: int = 20,
    preset: str = "medium",
) -> bytes:
    """Stitch ``segments`` into a single crossfaded MP4 and return its bytes.

    Each segment is normalized onto a ``width``x``height`` canvas with a
    blurred fill behind it, trimmed to its duration, and crossfaded into the
    next with a ``crossfade``-second transition. Total runtime is
    ``sum(durations) - crossfade * (len(segments) - 1)``.

    Parameters
    ----------
    width, height, fps:
        Output canvas geometry and frame rate. Defaults to 1280x720 (16:9).
    image_duration:
        On-screen seconds for image segments without an explicit duration.
    max_video_duration:
        Cap applied to a video segment's native duration (None = no cap).
    crossfade:
        Transition length in seconds. Automatically clamped below half the
        shortest segment so xfade offsets stay valid.
    background_blur:
        Gaussian sigma for the fill background. Higher = blurrier.
    transition:
        Any ffmpeg ``xfade`` transition name (``fade``, ``dissolve``,
        ``smoothleft``, ``circleopen``, …).
    audio_bytes:
        Optional soundtrack. When provided it is mapped onto the video and
        (if ``loop_audio``) looped to cover the full runtime; the output is
        cut to the video length.

    Raises
    ------
    ValueError
        If ``segments`` is empty.
    FfmpegNotAvailableError
        If no ffmpeg binary can be located.
    RuntimeError
        If ffmpeg exits non-zero (stderr tail included).
    """
    if not segments:
        raise ValueError("compose_slideshow requires at least one segment")

    ffmpeg = _resolve_ffmpeg_binary()
    tmpdir = tempfile.mkdtemp(prefix="matrx_slideshow_")
    try:
        # 1) Write every segment to disk and resolve its on-screen duration.
        durations: list[float] = []
        input_args: list[str] = []
        for i, seg in enumerate(segments):
            ext = ".mp4" if seg.kind == "video" else ".img"
            path = os.path.join(tmpdir, f"seg_{i}{ext}")
            with open(path, "wb") as fh:
                fh.write(seg.data)

            if seg.kind == "video":
                dur = seg.duration or _probe_video_duration(path) or image_duration
                if max_video_duration is not None:
                    dur = min(dur, max_video_duration)
                # A video is fed as a normal input; the filter trims it.
                input_args += ["-i", path]
            else:
                dur = seg.duration or image_duration
                # An image is looped for `dur` seconds at the target fps.
                input_args += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur:.3f}", "-i", path]

            durations.append(max(0.5, float(dur)))

        # 2) Clamp crossfade so every xfade offset is strictly inside its clip.
        if len(durations) > 1:
            eff_crossfade = min(crossfade, min(durations) * 0.5)
        else:
            eff_crossfade = 0.0
        eff_crossfade = max(0.0, eff_crossfade)

        # 3) Build the filter graph: per-input normalization + xfade chain.
        filters = [
            _normalize_filter(i, durations[i], width, height, fps, background_blur)
            for i in range(len(segments))
        ]
        xfade_filter, video_label = _build_xfade_chain(durations, eff_crossfade, transition)
        if xfade_filter:
            filters.append(xfade_filter)

        total_duration = sum(durations) - eff_crossfade * (len(durations) - 1)

        # 4) Optional audio input (looped + trimmed to the video length).
        audio_input_index: int | None = None
        if audio_bytes:
            audio_path = os.path.join(tmpdir, "audio.bin")
            with open(audio_path, "wb") as fh:
                fh.write(audio_bytes)
            audio_input_index = len(segments)
            if loop_audio:
                input_args += ["-stream_loop", "-1", "-i", audio_path]
            else:
                input_args += ["-i", audio_path]

        out_path = os.path.join(tmpdir, "out.mp4")
        cmd = [ffmpeg, "-y", *input_args, "-filter_complex", ";".join(filters)]
        cmd += ["-map", video_label]
        if audio_input_index is not None:
            cmd += ["-map", f"{audio_input_index}:a:0", "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += [
            "-t",
            f"{total_duration:.3f}",
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-r",
            str(fps),
            out_path,
        ]

        proc = subprocess.run(cmd, capture_output=True)
        if proc.returncode != 0:
            stderr_tail = proc.stderr.decode("utf-8", "replace")[-2000:]
            raise RuntimeError(
                f"ffmpeg slideshow composition failed (exit {proc.returncode}):\n{stderr_tail}"
            )

        with open(out_path, "rb") as fh:
            return fh.read()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


async def compose_slideshow_async(
    segments: list[SlideSegment],
    **kwargs,
) -> bytes:
    """Async wrapper around :func:`compose_slideshow` — runs the (blocking,
    CPU/ffmpeg-bound) composition in a thread executor so the event loop is
    never blocked. Use this in FastAPI routes / async pipelines."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: compose_slideshow(segments, **kwargs))
