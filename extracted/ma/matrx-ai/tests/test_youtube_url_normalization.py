import pytest

from matrx_ai.config.media_config import YouTubeVideoContent, normalize_youtube_url

CANONICAL = "https://www.youtube.com/watch?v=5WY8Gv_QCDU"


@pytest.mark.parametrize(
    "value",
    [
        "5WY8Gv_QCDU",
        "https://youtu.be/5WY8Gv_QCDU",
        "https://youtu.be/5WY8Gv_QCDU?si=J3rCB17pq7PTEtgX",
        "https://www.youtube.com/watch?v=5WY8Gv_QCDU",
        "https://www.youtube.com/watch?v=5WY8Gv_QCDU&t=42s",
        "https://m.youtube.com/watch?v=5WY8Gv_QCDU",
        "https://www.youtube.com/shorts/5WY8Gv_QCDU",
        "https://www.youtube.com/embed/5WY8Gv_QCDU",
        "https://www.youtube.com/live/5WY8Gv_QCDU",
        "youtu.be/5WY8Gv_QCDU",
        "youtube.com/watch?v=5WY8Gv_QCDU",
    ],
)
def test_normalizes_to_canonical_watch_url(value):
    assert normalize_youtube_url(value) == CANONICAL


def test_to_google_uses_canonical_url():
    content = YouTubeVideoContent(url="5WY8Gv_QCDU")
    part = content.to_google()
    assert part is not None
    assert part["fileData"]["fileUri"] == CANONICAL


def test_non_youtube_input_passes_through():
    url = "https://generativelanguage.googleapis.com/files/abc123"
    assert normalize_youtube_url(url) == url


def test_empty_passes_through():
    assert normalize_youtube_url("") == ""
