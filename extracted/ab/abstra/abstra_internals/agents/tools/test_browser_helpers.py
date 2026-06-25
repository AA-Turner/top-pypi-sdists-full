import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any, cast

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from abstra_internals.agents.tools.browser import (
    BrowserTools,
    ElementExtractor,
    _choose_select_option,
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
        self.set_input_files_calls: list[tuple[str, str, int]] = []

    def query_selector(self, selector: str):
        return object()

    def expect_download(self, timeout: int):
        self.download_timeout = timeout
        return FakeDownloadInfo()

    def click(self, selector: str, timeout: int):
        self.clicked_selector = selector

    def set_input_files(self, selector: str, files: str, timeout: int):
        self.set_input_files_calls.append((selector, files, timeout))


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


class _WaitPage:
    url = "https://example.com/app/"

    def __init__(self):
        self.waited = None

    def wait_for_timeout(self, milliseconds):
        self.waited = milliseconds


def _tools_with_pages(pages):
    tools = object.__new__(BrowserTools)
    tools.pages = cast(Any, pages)
    tools.debug_mode = False
    tools._extracted_elements = {}
    return tools


class TestWait:
    def test_clamps_milliseconds_above_max(self):
        page = _WaitPage()
        tools = _tools_with_pages({"tab-1": page})
        tools.wait("tab-1", 45000)
        assert page.waited == 30000

    def test_clamps_negative_milliseconds(self):
        page = _WaitPage()
        tools = _tools_with_pages({"tab-1": page})
        tools.wait("tab-1", -5)
        assert page.waited == 0

    def test_defaults_to_active_page_when_tab_id_omitted(self):
        page = _WaitPage()
        tools = _tools_with_pages({"tab-1": page})
        tools.wait(None, 100)
        assert page.waited == 100

    def test_unknown_tab_id_falls_back_to_active_page(self):
        # The model often invents a tab_id (e.g. "dummy-wait"); wait on the most
        # recently opened page instead of erroring out.
        page = _WaitPage()
        tools = _tools_with_pages({"tab-1": page})
        tools.wait("dummy-wait", 100)
        assert page.waited == 100

    def test_no_open_pages_raises_clear_error(self):
        tools = _tools_with_pages({})
        with pytest.raises(ValueError, match="No open browser pages"):
            tools.wait(None, 100)


class _SelectPage:
    url = "https://example.com/app/"

    def __init__(self):
        self.select_calls: list[dict] = []

    def query_selector(self, selector):
        return object()

    def select_option(self, selector, value=None, label=None, timeout=None):
        self.select_calls.append({"selector": selector, "value": value, "label": label})


class TestFillElementSelect:
    def test_select_dropdown_uses_select_option(self):
        page = _SelectPage()
        tools = object.__new__(BrowserTools)
        tools.pages = cast(Any, {"tab-1": page})
        tools.debug_mode = False
        tools._extracted_elements = {
            "tab-1": [{"index": 0, "selector": "#filtroMes", "tag": "select"}]
        }
        tools.extractor = ElementExtractor()

        result = tools.fill_element("tab-1", 0, "2026-04")

        assert page.select_calls == [
            {"selector": "#filtroMes", "value": "2026-04", "label": None}
        ]
        assert result["tag"] == "select"


class _FakeSelectTarget:
    """Stands in for a Playwright Page or Frame for select_option tests."""

    def __init__(self, fail_value: bool = False):
        self._fail_value = fail_value
        self.calls: list[dict] = []

    def select_option(self, selector, value=None, label=None, timeout=None):
        self.calls.append({"value": value, "label": label})
        if value is not None and self._fail_value:
            raise PlaywrightTimeoutError("no option matched by value")


class TestChooseSelectOption:
    # Shared by both the page path (BrowserTools.fill_element) and the iframe
    # path (_handle_iframe) used when testing Page stages.
    def test_selects_by_value(self):
        target = _FakeSelectTarget()
        _choose_select_option(target, "#sel", "2026-04")
        assert target.calls == [{"value": "2026-04", "label": None}]

    def test_falls_back_to_label_when_value_misses(self):
        target = _FakeSelectTarget(fail_value=True)
        _choose_select_option(target, "#sel", "April 2026")
        assert target.calls == [
            {"value": "April 2026", "label": None},
            {"value": None, "label": "April 2026"},
        ]


class _ListPage:
    def __init__(self, title_ok):
        self._title_ok = title_ok
        self.url = "https://example.com/app/"

    def title(self):
        if not self._title_ok:
            raise Exception("Target page, context or browser has been closed")
        return "OK"


class TestListPagesResilience:
    def test_skips_and_drops_stale_pages(self):
        tools = object.__new__(BrowserTools)
        tools.pages = cast(Any, {"good": _ListPage(True), "bad": _ListPage(False)})
        tools.debug_mode = False
        tools._extracted_elements = {}

        result = list(tools.list_pages())

        assert [r["tab_id"] for r in result] == ["good"]
        assert "bad" not in tools.pages  # stale handle dropped


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


class TestResolveDefaultDownloadPath:
    def test_default_uses_helper_and_creates_parent(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir) / "browser_tools" / "downloads" / "exec-abc123"
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser._default_download_dir",
                lambda: target_dir,
            )

            path = _resolve_download_path(None, "report.csv", overwrite=False)

            assert path == target_dir / "report.csv"
            assert path.parent.exists()

    def test_default_path_rejects_existing_file_without_overwrite(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir)
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser._default_download_dir",
                lambda: target_dir,
            )

            first = _resolve_download_path(None, "report.csv", overwrite=False)
            first.write_text("already here")

            with pytest.raises(FileExistsError):
                _resolve_download_path(None, "report.csv", overwrite=False)

    def test_default_path_allows_overwrite(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            target_dir = Path(tmpdir)
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser._default_download_dir",
                lambda: target_dir,
            )

            first = _resolve_download_path(None, "report.csv", overwrite=False)
            first.write_text("already here")

            second = _resolve_download_path(None, "report.csv", overwrite=True)
            assert second == first


class TestDefaultDownloadDir:
    def _inject_fake_execution_module(self, monkeypatch, get_execution_id):
        import sys
        import types

        fake_module = types.ModuleType("abstra_internals.execution")
        fake_module.get_execution_id = get_execution_id  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, "abstra_internals.execution", fake_module)

    def test_uses_persisted_dir_with_exec_id_subdir(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir)
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            self._inject_fake_execution_module(monkeypatch, lambda: "exec-abc123")

            from abstra_internals.agents.tools.browser import _default_download_dir

            assert (
                _default_download_dir()
                == persisted / "browser_tools" / "downloads" / "exec-abc123"
            )

    def test_falls_back_without_exec_id_when_sdk_raises(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir)
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )

            def _raise():
                raise RuntimeError("no SDK context")

            self._inject_fake_execution_module(monkeypatch, _raise)

            from abstra_internals.agents.tools.browser import _default_download_dir

            assert _default_download_dir() == persisted / "browser_tools" / "downloads"

    def test_falls_back_without_exec_id_when_empty(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir)
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            self._inject_fake_execution_module(monkeypatch, lambda: "")

            from abstra_internals.agents.tools.browser import _default_download_dir

            assert _default_download_dir() == persisted / "browser_tools" / "downloads"


def _browser_tools_for_upload_tests(page: FakePage):
    tools = object.__new__(BrowserTools)
    tools.pages = cast(Any, {"page-1": page})
    tools.debug_mode = False
    tools._extracted_elements = {}
    tools.urls = None
    return tools


class TestUploadFile:
    def test_accepts_file_inside_persisted_dir(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir).resolve()
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            file_path = persisted / "data" / "foo.csv"
            file_path.parent.mkdir(parents=True)
            file_path.write_bytes(b"hello\n")

            page = FakePage()
            tools = _browser_tools_for_upload_tests(page)

            result = tools.upload_file(
                "page-1",
                file_path=str(file_path),
                selector="input[type=file]",
                timeout_ms=4321,
            )

            assert result == {
                "path": str(file_path),
                "size_bytes": 6,
                "selector": "input[type=file]",
            }
            assert page.set_input_files_calls == [
                ("input[type=file]", str(file_path), 4321)
            ]

    def test_rejects_file_outside_persisted_dir(self, monkeypatch):
        with (
            tempfile.TemporaryDirectory() as persisted_tmp,
            tempfile.TemporaryDirectory() as outside_tmp,
        ):
            persisted = Path(persisted_tmp).resolve()
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            outside = Path(outside_tmp) / "leak.csv"
            outside.write_bytes(b"")

            page = FakePage()
            tools = _browser_tools_for_upload_tests(page)

            with pytest.raises(PermissionError):
                tools.upload_file(
                    "page-1",
                    file_path=str(outside),
                    selector="input[type=file]",
                )

            assert page.set_input_files_calls == []

    def test_rejects_symlink_escape(self, monkeypatch):
        with (
            tempfile.TemporaryDirectory() as persisted_tmp,
            tempfile.TemporaryDirectory() as outside_tmp,
        ):
            persisted = Path(persisted_tmp).resolve()
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            real_target = Path(outside_tmp) / "secret.csv"
            real_target.write_bytes(b"top secret")
            link_inside = persisted / "decoy.csv"
            link_inside.symlink_to(real_target)

            page = FakePage()
            tools = _browser_tools_for_upload_tests(page)

            with pytest.raises(PermissionError):
                tools.upload_file(
                    "page-1",
                    file_path=str(link_inside),
                    selector="input[type=file]",
                )

            assert page.set_input_files_calls == []

    def test_raises_when_file_missing(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir).resolve()
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )

            page = FakePage()
            tools = _browser_tools_for_upload_tests(page)

            with pytest.raises(FileNotFoundError):
                tools.upload_file(
                    "page-1",
                    file_path=str(persisted / "nope.csv"),
                    selector="input[type=file]",
                )

            assert page.set_input_files_calls == []

    def test_rejects_selector_and_index_together(self, monkeypatch):
        with tempfile.TemporaryDirectory() as tmpdir:
            persisted = Path(tmpdir).resolve()
            monkeypatch.setattr(
                "abstra_internals.agents.tools.browser.get_persistent_dir",
                lambda: persisted,
            )
            file_path = persisted / "foo.csv"
            file_path.write_bytes(b"")

            page = FakePage()
            tools = _browser_tools_for_upload_tests(page)

            with pytest.raises(ValueError):
                tools.upload_file(
                    "page-1",
                    file_path=str(file_path),
                    selector="input",
                    index=0,
                )

    def test_upload_file_exposed_in_tools(self):
        tools = object.__new__(BrowserTools)
        tools.allow_close_page = False
        tools.listen_network = False
        tools.listen_console = False
        tools.listen_websocket = False
        assert "upload_file" in tools.__tools__()
