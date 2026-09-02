"""Counting commits should cost one request, not five.

`get_commits` pages a window a hundred at a time, up to five times. A caller
that only wants a number was pulling as many as five hundred commit objects per
repository to call `len()` on them — and on a seven-repository release that was
most of a seventeen-second wait, all of it silent.

With `per_page=1`, GitHub's `Link` header names the last page, and one commit per
page means the last page number *is* the count.
"""

from __future__ import annotations

import pytest

from src.api.github_api import GitHubAPI, _last_page


class TestTheLinkHeader:
    def test_it_reads_the_last_page(self):
        header = (
            '<https://api.github.com/repositories/1/commits?per_page=1&page=2>; rel="next", '
            '<https://api.github.com/repositories/1/commits?per_page=1&page=37>; rel="last"'
        )
        assert _last_page(header) == 37

    def test_a_missing_header_is_not_zero(self):
        """GitHub omits it entirely on a single page, so the caller has to fall
        back to the body. Reading absence as zero would report every quiet
        repository as having no commits — and one commit as none."""
        assert _last_page(None) is None
        assert _last_page("") is None

    def test_a_header_without_a_last_link_is_none(self):
        assert _last_page('<https://api.github.com/x?page=2>; rel="next"') is None


class TestCountCommits:
    @staticmethod
    def _api(monkeypatch, *, status=200, headers=None, body=None):
        import httpx

        class _Resp:
            status_code = status
            text = "boom"

            def __init__(self):
                self.headers = headers or {}

            def json(self):
                return body if body is not None else []

        class _Client:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def get(self, url, headers=None, params=None):
                _Client.seen = params
                return _Resp()

        monkeypatch.setattr(httpx, "AsyncClient", lambda *a, **k: _Client())
        return GitHubAPI("tok"), _Client

    @pytest.mark.asyncio
    async def test_the_count_comes_from_the_last_page(self, monkeypatch):
        api, client = self._api(
            monkeypatch,
            headers={
                "Link": '<https://api.github.com/x?per_page=1&page=39>; rel="last"'
            },
        )
        assert await api.count_commits("o", "r") == 39

    @pytest.mark.asyncio
    async def test_it_asks_for_one_per_page(self, monkeypatch):
        """The whole saving. `per_page=100` here would fetch a hundred commit
        bodies and still need the header."""
        api, client = self._api(monkeypatch, headers={"Link": '<x?page=9>; rel="last"'})
        await api.count_commits("o", "r")
        assert client.seen["per_page"] == 1

    @pytest.mark.asyncio
    async def test_a_single_page_falls_back_to_the_body(self, monkeypatch):
        api, _ = self._api(monkeypatch, headers={}, body=[{"sha": "abc"}])
        assert await api.count_commits("o", "r") == 1

    @pytest.mark.asyncio
    async def test_an_empty_repository_is_zero_not_an_error(self, monkeypatch):
        """404/409 mean an empty repo or a missing branch. A release must not
        fail because one repository in the project is a stub."""
        api, _ = self._api(monkeypatch, status=409)
        assert await api.count_commits("o", "r") == 0
