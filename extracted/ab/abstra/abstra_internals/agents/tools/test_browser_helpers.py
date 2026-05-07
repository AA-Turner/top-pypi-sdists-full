import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any, cast

import pytest

from abstra_internals.agents.tools.browser import (
    BrowserTools,
    _resolve_download_path,
    _safe_download_filename,
    _same_origin,
    _wrap_for_safe_eval,
)


def _node_check(snippet: str) -> subprocess.CompletedProcess:
    """Ask Node to parse the snippet and return the result.

    We pipe through `--check` because that only validates syntax without
    running anything (so DOM globals don't need to exist).
    """
    return subprocess.run(
        ["node", "--check"],
        input=snippet,
        capture_output=True,
        text=True,
    )


_NODE_AVAILABLE = shutil.which("node") is not None
needs_node = pytest.mark.skipif(not _NODE_AVAILABLE, reason="node not installed")


class TestWrapForSafeEval:
    """The wrapper takes the user's script verbatim and injects it into an
    async IIFE inside the safe-eval helper. We don't try to be clever
    about expression-vs-statement — the agent is expected to use
    `return X;` to surface values."""

    def test_injects_script_verbatim(self):
        wrapped = _wrap_for_safe_eval("return 42;")
        assert "return 42;" in wrapped

    def test_wraps_in_async_iife(self):
        wrapped = _wrap_for_safe_eval("return 42;")
        assert wrapped.startswith("(") and wrapped.endswith(")()")
        assert "async () => { return 42; }" in wrapped

    def test_no_heuristic_for_pure_expression(self):
        # `42` is a valid expression but the wrapper does NOT insert an
        # implicit return — agents must write `return 42;` to get the value.
        wrapped = _wrap_for_safe_eval("42")
        assert "async () => { 42 }" in wrapped

    @needs_node
    def test_statements_with_trailing_semicolon_dont_syntax_error(self):
        # c09 regression: an earlier version produced `;);` at the boundary
        # and crashed every JS call with `SyntaxError: Unexpected token ';'`.
        wrapped = _wrap_for_safe_eval("setInterval(fn, 50);")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_multistatement_with_return_is_valid(self):
        wrapped = _wrap_for_safe_eval("const x = 1;\nreturn x;")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_pure_expression_is_valid_js(self):
        wrapped = _wrap_for_safe_eval("42")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_iife_input_does_not_double_wrap_unsafely(self):
        wrapped = _wrap_for_safe_eval("(async () => { return 42; })()")
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr

    @needs_node
    def test_script_with_window_open_is_valid(self):
        # c17 / circular-reference regression: window.open returns an object
        # full of cycles; the wrapper must keep producing valid JS for it.
        wrapped = _wrap_for_safe_eval(
            textwrap.dedent(
                """
                window.open('http://example.com/x', '_blank');
                """
            ).strip()
        )
        result = _node_check(wrapped)
        assert result.returncode == 0, result.stderr


class FakeDownload:
    suggested_filename = "report.csv"
    url = "https://example.com/report.csv"

    def save_as(self, path: str):
        Path(path).write_bytes(b"a,b\n1,2\n")


class FakeDownloadInfo:
    value = FakeDownload()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakePage:
    url = "https://example.com/app/"

    def __init__(self):
        self.clicked_selector = None
        self.download_timeout = None

    def query_selector(self, selector: str):
        return object()

    def expect_download(self, timeout: int):
        self.download_timeout = timeout
        return FakeDownloadInfo()

    def click(self, selector: str, timeout: int):
        self.clicked_selector = selector


class FakeResponse:
    ok = True
    status = 200
    status_text = "OK"
    headers = {"content-type": "text/csv"}

    def body(self):
        return b"x,y\n3,4\n"


class FakeRequestContext:
    def __init__(self):
        self.called_url = None
        self.called_timeout = None

    def get(self, url: str, timeout: int):
        self.called_url = url
        self.called_timeout = timeout
        return FakeResponse()


class FakeBrowserContext:
    def __init__(self):
        self.request = FakeRequestContext()


def _browser_tools_for_download_tests(
    page: FakePage,
    context: FakeBrowserContext,
    urls=None,
):
    tools = object.__new__(BrowserTools)
    # The fakes intentionally only implement the slice of the Playwright
    # surface these tests touch; cast through Any so pyright doesn't try
    # to match the full Page / BrowserContext protocols.
    tools.pages = cast(Any, {"page-1": page})
    tools._browser_context = cast(Any, context)
    tools.debug_mode = False
    tools._extracted_elements = {}
    tools.urls = urls
    return tools


class TestDownloadHelpers:
    def test_safe_download_filename_strips_paths(self):
        assert _safe_download_filename("../nested/report.csv") == "report.csv"
        assert _safe_download_filename("") == "download"

    def test_same_origin_normalizes_default_ports(self):
        assert _same_origin("https://example.com/app", "https://example.com:443/file")
        assert not _same_origin("https://example.com/app", "http://example.com/file")

    def test_resolve_download_path_uses_directory_and_suggested_filename(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = _resolve_download_path(tmpdir, "report.csv", overwrite=False)
            assert path == Path(tmpdir) / "report.csv"

    def test_resolve_download_path_rejects_existing_file_without_overwrite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            existing = Path(tmpdir) / "report.csv"
            existing.write_text("already here")

            with pytest.raises(FileExistsError):
                _resolve_download_path(str(existing), "ignored.csv", overwrite=False)

    def test_download_file_saves_click_triggered_download(self):
        page = FakePage()
        tools = _browser_tools_for_download_tests(page, FakeBrowserContext())

        with tempfile.TemporaryDirectory() as tmpdir:
            result = tools.download_file(
                "page-1",
                selector="a.download",
                output_path=tmpdir,
                timeout_ms=1234,
            )

            saved_path = Path(result["path"])
            assert saved_path == Path(tmpdir) / "report.csv"
            assert saved_path.read_bytes() == b"a,b\n1,2\n"
            assert result["suggested_filename"] == "report.csv"
            assert result["url"] == "https://example.com/report.csv"
            assert result["size_bytes"] == 8
            assert page.clicked_selector == "a.download"
            assert page.download_timeout == 1234

    def test_download_url_uses_browser_context_request_and_resolves_relative_url(self):
        page = FakePage()
        context = FakeBrowserContext()
        tools = _browser_tools_for_download_tests(
            page, context, urls=["https://example.com/app/"]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            result = tools.download_url(
                "page-1",
                "exports/data.csv",
                output_path=str(Path(tmpdir) / "data.csv"),
                timeout_ms=4321,
            )

            saved_path = Path(result["path"])
            assert saved_path.read_bytes() == b"x,y\n3,4\n"
            assert result["url"] == "https://example.com/app/exports/data.csv"
            assert result["status"] == 200
            assert result["headers"] == {"content-type": "text/csv"}
            assert result["size_bytes"] == 8
            assert (
                context.request.called_url == "https://example.com/app/exports/data.csv"
            )
            assert context.request.called_timeout == 4321

    def test_download_url_rejects_cross_origin_when_browser_is_scoped(self):
        page = FakePage()
        context = FakeBrowserContext()
        tools = _browser_tools_for_download_tests(
            page, context, urls=["https://example.com/app/"]
        )

        with pytest.raises(PermissionError):
            tools.download_url("page-1", "https://other.example.com/data.csv")

        assert context.request.called_url is None
