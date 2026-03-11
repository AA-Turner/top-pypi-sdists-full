"""Tests for parse_package_string."""

from plato.cli.chronos.registry import parse_package_string


def test_package_with_version():
    assert parse_package_string("plato-world-foo:0.1.0") == ("plato-world-foo", "0.1.0")


def test_package_without_version():
    assert parse_package_string("plato-world-foo") == ("plato-world-foo", None)


def test_package_with_latest():
    assert parse_package_string("plato-world-foo:latest") == ("plato-world-foo", None)


def test_package_with_empty_version():
    assert parse_package_string("plato-world-foo:") == ("plato-world-foo", None)


def test_agent_with_latest():
    assert parse_package_string("claude-code:latest") == ("claude-code", None)


def test_prerelease_version():
    assert parse_package_string("plato-world-foo:0.1.0.dev1") == ("plato-world-foo", "0.1.0.dev1")
