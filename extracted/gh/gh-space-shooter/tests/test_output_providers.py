"""Tests for output providers."""

from PIL import Image
import pytest
from gh_space_shooter.output import GifOutputProvider, WebPOutputProvider, resolve_output_provider



def create_test_frame(color="red"):
    """Helper to create a test frame."""
    img = Image.new("RGB", (10, 10), color)
    return img


def test_gif_provider_encodes_frames():
    """GifOutputProvider should encode frames to GIF format."""
    provider = GifOutputProvider("test_output.gif")
    frames = [create_test_frame("red"), create_test_frame("blue")]

    result = provider.encode(iter(frames), frame_duration=100)

    assert result.startswith(b"GIF89")
    assert len(result) > 0


def test_gif_provider_empty_frames():
    """GifOutputProvider should handle empty frame list."""
    provider = GifOutputProvider("test_output.gif")
    result = provider.encode(iter([]), frame_duration=100)

    # Empty result for empty frames
    assert result == b""


def test_webp_provider_encodes_frames():
    """WebPOutputProvider should encode frames to WebP format."""
    provider = WebPOutputProvider("test_output.webp")
    frames = [create_test_frame("red"), create_test_frame("blue")]

    result = provider.encode(iter(frames), frame_duration=100)

    # WebP files start with RIFF....WEBP
    assert result.startswith(b"RIFF")
    assert b"WEBP" in result
    assert len(result) > 0


def test_webp_provider_empty_frames():
    """WebPOutputProvider should handle empty frame list."""
    provider = WebPOutputProvider("test_output.webp")
    result = provider.encode(iter([]), frame_duration=100)

    assert result == b""


def test_resolve_gif_provider():
    """resolve_output_provider should return GifOutputProvider for .gif files."""
    provider = resolve_output_provider("output.gif")

    assert isinstance(provider, GifOutputProvider)



def test_resolve_webp_provider():
    """resolve_output_provider should return WebPOutputProvider for .webp files."""
    provider = resolve_output_provider("output.webp")

    assert isinstance(provider, WebPOutputProvider)


def test_resolve_unsupported_format():
    """resolve_output_provider should raise ValueError for unsupported formats."""
    with pytest.raises(ValueError, match="Unsupported output format"):
        resolve_output_provider("output.mp4")


def test_resolve_case_insensitive():
    """resolve_output_provider should handle uppercase extensions."""
    provider = resolve_output_provider("output.GIF", )
    assert isinstance(provider, GifOutputProvider)

    provider = resolve_output_provider("output.WEBP", )
    assert isinstance(provider, WebPOutputProvider)
