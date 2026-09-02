"""Tests for backwards compatibility functionality."""

import sys
from unittest.mock import patch

from runlayer_cli.main import _ensure_backwards_compatibility


def test_uuid_as_first_arg_inserts_run_command():
    """Test that a UUID as first argument gets 'run' inserted before it."""
    test_uuid = "550e8400-e29b-41d4-a716-446655440000"
    test_argv = ["runlayer", test_uuid, "--secret", "test-secret"]

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == ["runlayer", "run", test_uuid, "--secret", "test-secret"]


def test_run_command_already_present_no_modification():
    """Test that existing 'run' command is not modified."""
    test_uuid = "550e8400-e29b-41d4-a716-446655440000"
    test_argv = ["runlayer", "run", test_uuid, "--secret", "test-secret"]
    expected = test_argv.copy()

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == expected


def test_invalid_uuid_no_modification():
    """Test that invalid UUID strings are not modified."""
    test_argv = ["runlayer", "not-a-uuid", "--secret", "test-secret"]
    expected = test_argv.copy()

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == expected


def test_alias_as_first_arg_no_modification():
    """Test that bare aliases stay unsupported in v1."""
    test_argv = ["runlayer", "@runlayer/agent-terminal", "--secret", "test-secret"]
    expected = test_argv.copy()

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == expected


def test_help_flag_no_modification():
    """Test that help flags are not modified."""
    test_argv = ["runlayer", "--help"]
    expected = test_argv.copy()

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == expected


def test_version_flag_no_modification():
    """Test that version flags are not modified."""
    test_argv = ["runlayer", "--version"]
    expected = test_argv.copy()

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == expected


def test_uppercase_uuid_inserts_run_command():
    """Test that uppercase UUIDs also work."""
    test_uuid = "550E8400-E29B-41D4-A716-446655440000"
    test_argv = ["runlayer", test_uuid, "--secret", "test-secret"]

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
        assert sys.argv == ["runlayer", "run", test_uuid, "--secret", "test-secret"]


def test_empty_argv_no_crash():
    """Test that empty or minimal argv doesn't crash."""
    # Edge case: only program name
    test_argv = ["runlayer"]

    with patch.object(sys, "argv", test_argv):
        _ensure_backwards_compatibility()
