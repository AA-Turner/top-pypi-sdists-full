"""Browser-level coverage for chat attachment size validation (#1551)."""

from __future__ import annotations

from importlib.util import find_spec

import pytest

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(find_spec("pytest_playwright") is None, reason="pytest-playwright not installed"),
]


def test_chat_attachment_over_50_mb_shows_matching_rejection(authenticated_page, tmp_path) -> None:
    page = authenticated_page
    oversized = tmp_path / "too-big.txt"
    with oversized.open("wb") as fh:
        fh.truncate((50 * 1024 * 1024) + 1)

    dialog_messages: list[str] = []
    page.once("dialog", lambda dialog: (dialog_messages.append(dialog.message), dialog.accept()))

    page.locator("#file-input").set_input_files(str(oversized))

    assert dialog_messages, "Expected browser alert for oversized attachment"
    message = dialog_messages[0]
    assert "File too large: too-big.txt" in message
    assert "Maximum size: 50 MB" in message
    assert page.locator("#attachment-previews .attachment-preview").count() == 0
