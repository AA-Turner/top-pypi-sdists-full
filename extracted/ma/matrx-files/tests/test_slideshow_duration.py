"""Actual encoded media must retain every segment's scheduled duration."""

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from matrx_files.specific_handlers.video_compose import SlideSegment, compose_slideshow


cv2 = pytest.importorskip("cv2")
pytest.importorskip("imageio_ffmpeg")


def _png(color: str) -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (96, 96), color).save(buffer, "PNG")
    return buffer.getvalue()


def _assert_duration(data: bytes, target: Path, expected: float, fps: int) -> None:
    target.write_bytes(data)
    cap = cv2.VideoCapture(str(target))
    try:
        assert cap.isOpened()
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        assert actual_fps == fps
        # One encoded frame of tolerance, never an arbitrary percentage.
        assert abs(frames - round(expected * fps)) <= 1
        assert cap.get(cv2.CAP_PROP_FRAME_WIDTH) == 128
        assert cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == 96
        cap.set(cv2.CAP_PROP_POS_FRAMES, frames - 1)
        ok, frame = cap.read()
        assert ok and frame.shape[:2] == (96, 128)
    finally:
        cap.release()


@pytest.mark.parametrize("fps,duration,crossfade", [(10, 0.5, 0.1), (30, 3.5, 0.8)])
def test_two_image_transitions_preserve_scheduled_duration(tmp_path, fps, duration, crossfade):
    segments = [SlideSegment(_png(color), "image", duration) for color in ["red", "blue"]]
    data = compose_slideshow(
        segments, width=128, height=96, fps=fps, crossfade=crossfade, preset="ultrafast"
    )
    _assert_duration(data, tmp_path / "slides.mp4", 2 * duration - crossfade, fps)


def test_single_image_preserves_scheduled_duration(tmp_path):
    data = compose_slideshow(
        [SlideSegment(_png("red"), "image", 0.5)], width=128, height=96, fps=10, preset="ultrafast"
    )
    _assert_duration(data, tmp_path / "single.mp4", 0.5, 10)


def test_short_video_holds_last_frame_for_explicit_duration(tmp_path):
    video = compose_slideshow(
        [SlideSegment(_png("red"), "image", 0.5)], width=128, height=96, fps=10, preset="ultrafast"
    )
    data = compose_slideshow(
        [SlideSegment(video, "video", 1.5)], width=128, height=96, fps=10, preset="ultrafast"
    )
    _assert_duration(data, tmp_path / "held.mp4", 1.5, 10)
