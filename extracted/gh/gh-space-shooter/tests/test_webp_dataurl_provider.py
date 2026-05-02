"""Tests for WebP data URL output provider."""

from PIL import Image
import pytest
from gh_space_shooter.output.webp_dataurl_provider import (
    WebpDataUrlOutputProvider,
    _SECTION_START_MARKER,
    _SECTION_END_MARKER,
)
import tempfile
import os


def create_test_frame(color="red"):
    """Helper to create a test frame."""
    img = Image.new("RGB", (10, 10), color)
    return img


def test_creates_new_file_with_wrapping_markers():
    """Provider should create file with content wrapped in section markers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")
        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red"), create_test_frame("blue")]

        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # File should exist and contain HTML img tag wrapped in markers
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            content = f.read()

        lines = content.splitlines()
        assert len(lines) == 3
        assert lines[0] == _SECTION_START_MARKER
        assert lines[1].startswith('<img src="data:image/webp;base64,')
        assert lines[1].endswith('" />')
        assert lines[2] == _SECTION_END_MARKER


def test_section_based_injection_replaces_content_between_markers():
    """Provider should replace content between section markers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with section markers and existing content
        with open(output_path, "w") as f:
            f.write("# My Contribution Graph\n")
            f.write(f"{_SECTION_START_MARKER}\n")
            f.write("old content here\n")
            f.write(f"{_SECTION_END_MARKER}\n")
            f.write("## Other content\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # Verify injection worked - content between markers replaced
        with open(output_path, "r") as f:
            content = f.read()

        lines = content.splitlines()
        assert len(lines) == 5
        assert lines[0] == "# My Contribution Graph"
        assert lines[1] == _SECTION_START_MARKER
        assert lines[2].startswith('<img src="data:image/webp;base64,')
        assert lines[2].endswith('" />')
        assert lines[3] == _SECTION_END_MARKER
        assert lines[4] == "## Other content"


def test_preserves_content_around_markers():
    """Provider should preserve content outside the section markers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with content before and after markers
        header_content = "# Header\nSome introductory text\n"
        footer_content = "\n## Footer\nMore footer content\n"

        with open(output_path, "w") as f:
            f.write(header_content)
            f.write(f"{_SECTION_START_MARKER}\n")
            f.write("old content\n")
            f.write(f"{_SECTION_END_MARKER}\n")
            f.write(footer_content)

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # Verify outer content preserved
        with open(output_path, "r") as f:
            content = f.read()

        assert content.startswith(header_content)
        assert content.endswith(footer_content)


def test_empty_section():
    """Provider should handle empty sections (no content between markers)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with empty section
        with open(output_path, "w") as f:
            f.write("# Header\n")
            f.write(f"{_SECTION_START_MARKER}\n")
            f.write(f"{_SECTION_END_MARKER}\n")
            f.write("## Footer\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # Verify content inserted
        with open(output_path, "r") as f:
            content = f.read()

        lines = content.splitlines()
        assert len(lines) == 5
        assert lines[0] == "# Header"
        assert lines[1] == _SECTION_START_MARKER
        assert lines[2].startswith('<img src="data:image/webp;base64,')


def test_error_when_start_marker_missing():
    """Provider should raise ValueError when start marker is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with only end marker
        with open(output_path, "w") as f:
            f.write("# Header\n")
            f.write(f"{_SECTION_END_MARKER}\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)

        with pytest.raises(ValueError) as exc_info:
            provider.write(data)

        assert "Start marker" in str(exc_info.value)
        assert _SECTION_START_MARKER in str(exc_info.value)


def test_error_when_end_marker_missing():
    """Provider should raise ValueError when end marker is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with only start marker
        with open(output_path, "w") as f:
            f.write("# Header\n")
            f.write(f"{_SECTION_START_MARKER}\n")
            f.write("some content\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)

        with pytest.raises(ValueError) as exc_info:
            provider.write(data)

        assert "End marker" in str(exc_info.value)
        assert _SECTION_END_MARKER in str(exc_info.value)


def test_error_when_markers_wrong_order():
    """Provider should raise ValueError when markers are in wrong order."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with end marker before start marker
        with open(output_path, "w") as f:
            f.write("# Header\n")
            f.write(f"{_SECTION_END_MARKER}\n")
            f.write("some content\n")
            f.write(f"{_SECTION_START_MARKER}\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)

        with pytest.raises(ValueError) as exc_info:
            provider.write(data)

        assert "must appear before" in str(exc_info.value)


def test_error_when_no_markers_at_all():
    """Provider should raise ValueError when file has no markers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file without any markers
        with open(output_path, "w") as f:
            f.write("# My Contribution Graph\n")
            f.write("Some content here\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)

        with pytest.raises(ValueError) as exc_info:
            provider.write(data)

        assert "Start marker" in str(exc_info.value)


def test_section_markers_on_same_line_with_content():
    """Provider should handle markers on different lines with content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with multiline content between markers
        with open(output_path, "w") as f:
            f.write(f"{_SECTION_START_MARKER}\n")
            f.write("line 1\n")
            f.write("line 2\n")
            f.write("line 3\n")
            f.write(f"{_SECTION_END_MARKER}\n")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # Verify all lines between markers replaced with single img tag
        with open(output_path, "r") as f:
            content = f.read()

        lines = content.splitlines()
        assert len(lines) == 3
        assert lines[0] == _SECTION_START_MARKER
        assert lines[1].startswith('<img src="data:image/webp;base64,')
        assert lines[2] == _SECTION_END_MARKER


def test_section_markers_without_trailing_newlines():
    """Provider should handle markers without proper newlines."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")

        # Create file with markers but no newlines
        with open(output_path, "w") as f:
            f.write(f"{_SECTION_START_MARKER}")
            f.write("content")
            f.write(f"{_SECTION_END_MARKER}")

        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red")]
        data = provider.encode(iter(frames), frame_duration=100)
        provider.write(data)

        # Verify content replaced and proper formatting maintained
        with open(output_path, "r") as f:
            content = f.read()

        assert _SECTION_START_MARKER in content
        assert _SECTION_END_MARKER in content
        assert '<img src="data:image/webp;base64,' in content
