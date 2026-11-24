"""git_ingest reads a repository on any git host, not only gitingest's six known ones.

Live failure (system_error 62740547, 2026-11-13): a public gitee.com repository failed with
``Unknown domain 'gitee.com' in URL`` before the host was ever asked. gitingest's host allow-list
is replaced inside ``_ingest``; this proves the replacement is what the parser actually runs.
"""

from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("gitingest")


def _normalise(source: str):
    import gitingest.utils.query_parser_utils as parse

    return asyncio.run(parse._normalise_source(source, token=None))


def _install_override(monkeypatch) -> None:
    """Run ``_ingest`` far enough to install its overrides, without cloning anything."""
    import gitingest
    from matrx_ai.tools.implementations import code_ingest

    monkeypatch.setattr(gitingest, "ingest", lambda *a, **k: ("s", "t", "c"))
    assert code_ingest._ingest("https://gitee.com/owner/repo") == ("s", "t", "c")


def test_upstream_refuses_gitee_before_the_override(monkeypatch) -> None:
    import gitingest.utils.query_parser_utils as parse

    original = parse._validate_host
    monkeypatch.setattr(parse, "_validate_host", original)
    if original.__module__ != parse.__name__:
        pytest.skip("another test already installed the override in this process")
    with pytest.raises(ValueError, match="Unknown domain 'gitee.com'"):
        _normalise("https://gitee.com/owner/repo")


@pytest.mark.parametrize(
    "source",
    [
        "https://gitee.com/owner/repo",
        "gitee.com/owner/repo",
        "https://sourceforge.net/p/project/code",
        "https://framagit.org/owner/repo",
    ],
)
def test_any_named_host_parses_after_the_override(monkeypatch, source: str) -> None:
    import gitingest.utils.query_parser_utils as parse

    monkeypatch.setattr(parse, "_validate_host", parse._validate_host)
    _install_override(monkeypatch)
    parsed = _normalise(source)
    assert parsed.netloc in source


def test_a_dotless_host_is_still_refused(monkeypatch) -> None:
    import gitingest.utils.query_parser_utils as parse

    monkeypatch.setattr(parse, "_validate_host", parse._validate_host)
    _install_override(monkeypatch)
    with pytest.raises(ValueError, match="Unknown domain"):
        _normalise("https://localhost/owner/repo")
