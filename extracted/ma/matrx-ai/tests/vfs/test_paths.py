from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.paths import (
    basename,
    dirname,
    is_absolute,
    join,
    normalize,
    split_components,
)


class TestNormalize:
    @pytest.mark.parametrize(
        ("inp", "expected"),
        [
            ("", "/"),
            ("/", "/"),
            ("/a", "/a"),
            ("/a/", "/a"),
            ("/a//b", "/a/b"),
            ("/a/./b", "/a/b"),
            ("/a/../b", "/b"),
            ("/a/b/../../c", "/c"),
            ("/../a", "/a"),
            ("/a/b/c/", "/a/b/c"),
            ("///", "/"),
            ("/a/b/.", "/a/b"),
            ("/./", "/"),
        ],
    )
    def test_absolute(self, inp: str, expected: str) -> None:
        assert normalize(inp) == expected

    def test_relative_paths(self) -> None:
        # Relative inputs are normalised but kept relative.
        assert normalize("a/b") == "a/b"
        assert normalize("a/./b") == "a/b"
        assert normalize("a/../b") == "b"
        assert normalize(".") == "."
        assert normalize("./a") == "a"


class TestJoin:
    def test_simple(self) -> None:
        assert join("/a", "b") == "/a/b"

    def test_absolute_overrides(self) -> None:
        assert join("/a", "/b") == "/b"

    def test_empty_parts(self) -> None:
        assert join("/a", "", "b") == "/a/b"

    def test_trailing_slash(self) -> None:
        assert join("/a/", "b") == "/a/b"

    def test_no_args(self) -> None:
        assert join() == "/"

    def test_collapses_dotdot(self) -> None:
        assert join("/a/b", "..", "c") == "/a/c"


class TestDirnameBasename:
    @pytest.mark.parametrize(
        ("path", "d", "b"),
        [
            ("/a/b/c", "/a/b", "c"),
            ("/a", "/", "a"),
            ("/", "/", ""),
            ("/a/b/", "/a", "b"),
        ],
    )
    def test_dirname_basename(self, path: str, d: str, b: str) -> None:
        assert dirname(path) == d
        assert basename(path) == b


class TestSplitComponents:
    @pytest.mark.parametrize(
        ("path", "expected"),
        [
            ("/", []),
            ("/a", ["a"]),
            ("/a/b/c", ["a", "b", "c"]),
            ("/a//b", ["a", "b"]),
            ("/a/../b", ["b"]),
        ],
    )
    def test_split(self, path: str, expected: list[str]) -> None:
        assert split_components(path) == expected


class TestIsAbsolute:
    def test_absolute(self) -> None:
        assert is_absolute("/a")
        assert is_absolute("/")

    def test_relative(self) -> None:
        assert not is_absolute("a/b")
        assert not is_absolute("")
