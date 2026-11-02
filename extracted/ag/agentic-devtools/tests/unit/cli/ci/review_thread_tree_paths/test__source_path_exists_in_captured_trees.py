"""Tests for exact-path checks against captured Git trees."""

from collections.abc import Iterable

from agentic_devtools.cli.ci.review_thread_tree_paths import _source_path_exists_in_captured_trees


def test_normalized_path_without_alias_needs_no_tree_lookup() -> None:
    def unexpected_git_call(_args: Iterable[str]) -> str:
        raise AssertionError("unmodified paths do not need tree inspection")

    assert _source_path_exists_in_captured_trees("base", "head", unexpected_git_call, "src/a.py") is None


def test_returns_true_when_exact_path_exists_in_either_captured_tree() -> None:
    calls: list[list[str]] = []

    def run_git(args: Iterable[str]) -> str:
        argv = list(args)
        calls.append(argv)
        return "" if argv[5] == "base" else "src/\u200ba.py\0"

    assert _source_path_exists_in_captured_trees("base", "head", run_git, "src/\u200ba.py") is True
    assert calls == [
        ["ls-tree", "-r", "--full-tree", "-z", "--name-only", "base", "--", ":(literal)src/\u200ba.py"],
        ["ls-tree", "-r", "--full-tree", "-z", "--name-only", "head", "--", ":(literal)src/\u200ba.py"],
    ]


def test_returns_false_only_after_both_trees_confirm_path_absence() -> None:
    calls: list[list[str]] = []

    def run_git(args: Iterable[str]) -> str:
        calls.append(list(args))
        return ""

    assert _source_path_exists_in_captured_trees("base", "head", run_git, "src/\u200ba.py") is False
    assert len(calls) == 2


def test_returns_unknown_when_tree_inspection_is_unavailable() -> None:
    def run_git(_args: Iterable[str]) -> str:
        raise RuntimeError("captured commit is unavailable")

    assert _source_path_exists_in_captured_trees("base", "head", run_git, "src/\u200ba.py") is None


def test_returns_true_if_one_tree_is_unavailable_but_the_other_has_the_path() -> None:
    responses = iter((RuntimeError("base tree unavailable"), "src/\u200ba.py\0"))

    def run_git(_args: Iterable[str]) -> str:
        response = next(responses)
        if isinstance(response, Exception):
            raise response
        return response

    assert _source_path_exists_in_captured_trees("base", "head", run_git, "src/\u200ba.py") is True


def test_returns_unknown_when_source_path_cannot_be_encoded_as_utf8() -> None:
    def unexpected_git_call(_args: Iterable[str]) -> str:
        raise AssertionError("unencodable paths cannot be checked exactly")

    assert _source_path_exists_in_captured_trees("base", "head", unexpected_git_call, "src/\u200b\ud800.py") is None


def test_returns_true_for_carriage_return_path_in_binary_git_output() -> None:
    source_path = "src/\u200ba\rb.py"
    responses = iter(("", source_path + "\0"))

    def run_git(_args: Iterable[str]) -> str:
        return next(responses)

    assert _source_path_exists_in_captured_trees("base", "head", run_git, source_path) is True
