"""Tests for OAuth browser lockfile mechanism."""

import tempfile

from freezegun import freeze_time

from runlayer_cli.oauth import (
    get_browser_lockfile_path,
    should_open_browser,
)


def test_get_browser_lockfile_path_deterministic():
    """Test that lockfile path is deterministic for the same server URL."""
    server_url = "https://example.com"
    path1 = get_browser_lockfile_path(server_url)
    path2 = get_browser_lockfile_path(server_url)

    assert path1 == path2
    # Verify it's in the system temp directory
    assert str(path1.parent) == tempfile.gettempdir()
    # Verify the filename format
    assert path1.name.startswith("runlayer_oauth_browser_")
    assert path1.name.endswith(".lock")


def test_get_browser_lockfile_path_different_servers():
    """Test that different servers get different lockfile paths."""
    path1 = get_browser_lockfile_path("https://server1.com")
    path2 = get_browser_lockfile_path("https://server2.com")

    assert path1 != path2


def test_should_open_browser_first_time():
    """Test that browser opens on first call."""
    server_url = "https://test-first-time.example.com"
    lockfile = get_browser_lockfile_path(server_url)

    # Clean up any existing lockfile
    if lockfile.exists():
        lockfile.unlink()

    try:
        assert should_open_browser(server_url) is True
        assert lockfile.exists()
    finally:
        # Clean up
        if lockfile.exists():
            lockfile.unlink()


def test_should_open_browser_within_window():
    """Test that browser doesn't open within the time window."""
    server_url = "https://test-within-window.example.com"
    lockfile = get_browser_lockfile_path(server_url)

    # Clean up any existing lockfile
    if lockfile.exists():
        lockfile.unlink()

    try:
        with freeze_time("2025-01-01 12:00:00") as frozen_time:
            # First call should open browser
            assert should_open_browser(server_url, window_seconds=3.0) is True

            # Immediate second call should NOT open browser
            assert should_open_browser(server_url, window_seconds=3.0) is False

            # Move time forward by 0.5 seconds (still within 3s window)
            frozen_time.tick(delta=0.5)

            # Third call within window should also NOT open browser
            assert should_open_browser(server_url, window_seconds=3.0) is False
    finally:
        # Clean up
        if lockfile.exists():
            lockfile.unlink()


def test_should_open_browser_after_window():
    """Test that browser opens after the time window expires."""
    server_url = "https://test-after-window.example.com"
    lockfile = get_browser_lockfile_path(server_url)

    # Clean up any existing lockfile
    if lockfile.exists():
        lockfile.unlink()

    try:
        with freeze_time("2025-01-01 12:00:00") as frozen_time:
            # First call should open browser
            assert should_open_browser(server_url, window_seconds=0.5) is True

            # Immediate second call should NOT open browser
            assert should_open_browser(server_url, window_seconds=0.5) is False

            # Move time forward by 0.6 seconds (past the 0.5s window)
            frozen_time.tick(delta=0.6)

            # Third call after window should open browser
            assert should_open_browser(server_url, window_seconds=0.5) is True
    finally:
        # Clean up
        if lockfile.exists():
            lockfile.unlink()


def test_should_open_browser_corrupted_lockfile():
    """Test that corrupted lockfile doesn't prevent browser from opening."""
    server_url = "https://test-corrupted.example.com"
    lockfile = get_browser_lockfile_path(server_url)

    try:
        # Create corrupted lockfile with invalid timestamp
        lockfile.write_text("not-a-timestamp")

        # Should still open browser (fail safe)
        result = should_open_browser(server_url)
        assert result is True

        # Note: The implementation prioritizes availability over fixing corrupted files,
        # so the lockfile may remain corrupted. This is acceptable behavior.
    finally:
        # Clean up
        if lockfile.exists():
            lockfile.unlink()


def test_should_open_browser_different_servers_independent():
    """Test that different servers have independent lockfiles."""
    server_url1 = "https://test-server1.example.com"
    server_url2 = "https://test-server2.example.com"
    lockfile1 = get_browser_lockfile_path(server_url1)
    lockfile2 = get_browser_lockfile_path(server_url2)

    # Clean up any existing lockfiles
    if lockfile1.exists():
        lockfile1.unlink()
    if lockfile2.exists():
        lockfile2.unlink()

    try:
        # Both servers should be able to open browser
        assert should_open_browser(server_url1, window_seconds=3.0) is True
        assert should_open_browser(server_url2, window_seconds=3.0) is True

        # Both should be blocked within their respective windows
        assert should_open_browser(server_url1, window_seconds=3.0) is False
        assert should_open_browser(server_url2, window_seconds=3.0) is False
    finally:
        # Clean up
        if lockfile1.exists():
            lockfile1.unlink()
        if lockfile2.exists():
            lockfile2.unlink()
