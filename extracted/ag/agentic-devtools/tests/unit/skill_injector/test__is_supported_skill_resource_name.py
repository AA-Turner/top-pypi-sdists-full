"""Unit tests for :func:`agentic_devtools.skill_injector._is_supported_skill_resource_name`."""

import pytest

from agentic_devtools.skill_injector import _is_supported_skill_resource_name


@pytest.mark.parametrize(
    "name",
    [
        "SKILL.md",
        "commit-types.md",
        "guide.txt",
        "resource_file.md",
        "RESOURCE.MD",
    ],
)
def test_valid_names_are_accepted(name: str) -> None:
    assert _is_supported_skill_resource_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "",
        ".hidden",
        ".hidden.md",
    ],
)
def test_empty_or_hidden_names_are_rejected(name: str) -> None:
    assert _is_supported_skill_resource_name(name) is False


@pytest.mark.parametrize(
    "name",
    [
        "sub/resource.md",
        "dir/file.md",
    ],
)
def test_forward_slash_is_rejected(name: str) -> None:
    assert _is_supported_skill_resource_name(name) is False


def test_backslash_is_rejected() -> None:
    assert _is_supported_skill_resource_name("dir\\file.md") is False


def test_backtick_is_rejected() -> None:
    # A backtick in a resource name would corrupt the backtick-delimited
    # Markdown manifest row, causing _read_managed_skill_manifest to parse
    # a truncated path and potentially schedule deletion of unmanaged files.
    assert _is_supported_skill_resource_name("foo`bar.md") is False


def test_newline_is_rejected() -> None:
    # A newline would forge an additional manifest row, enabling the same
    # stale-cleanup confusion as a backtick.
    assert _is_supported_skill_resource_name("foo\nbar.md") is False


def test_carriage_return_is_rejected() -> None:
    assert _is_supported_skill_resource_name("foo\rbar.md") is False
