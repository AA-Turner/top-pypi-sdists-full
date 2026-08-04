"""Web IDE surface: auth gate, path safety, per-folder history, i18n, wiring."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from bingo.config import BingoConfig
from bingo.web import security
from bingo.web.session import WebSession


def _cfg(lang="en"):
    c = BingoConfig()
    c.lang = lang
    return c


# ── token auth ────────────────────────────────────────────────────
def test_token_verify_constant_time():
    assert security.verify_token(security.SESSION_TOKEN) is True
    assert security.verify_token("") is False
    assert security.verify_token(None) is False
    assert security.verify_token("wrong") is False


# ── path traversal guard ──────────────────────────────────────────
def test_safe_resolve_blocks_escape():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "ok.txt").write_text("x")
        assert security.safe_resolve(root, "ok.txt") is not None
        assert security.safe_resolve(root, "../../etc/passwd") is None
        assert security.safe_resolve(root, "/etc/passwd") is None
        assert security.safe_resolve(root, "sub/../ok.txt") is not None


# ── file tree ──────────────────────────────────────────────────────
def test_list_tree_hides_noise_and_sorts_dirs_first():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "z.py").write_text("")
        (root / "a_dir").mkdir()
        (root / ".git").mkdir()
        (root / "__pycache__").mkdir()
        ws = WebSession(root, _cfg())
        names = [e["name"] for e in ws.list_tree()]
        assert names == ["a_dir", "z.py"]  # dir first, no .git/__pycache__


def test_list_tree_rejects_escape():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        assert ws.list_tree("../..") == []


# ── per-folder history isolation ───────────────────────────────────
def test_history_is_per_folder_and_persists(monkeypatch):
    with tempfile.TemporaryDirectory() as base:
        # Point workspace state at a temp dir so folders map to distinct files.
        import bingo.core.local_state as ls
        monkeypatch.setattr(ls, "state_dir", lambda: Path(base) / "state")

        fa, fb = Path(base) / "proj_a", Path(base) / "proj_b"
        fa.mkdir(); fb.mkdir()
        wa = WebSession(fa, _cfg())
        wa.history.add("user", "hello from A")
        wb = WebSession(fb, _cfg())
        wb.history.add("user", "hello from B")

        # Reload A from disk: its turn persists and B's does not leak in.
        wa2 = WebSession(fa, _cfg())
        texts = [t["content"] for t in wa2.history.context()]
        assert "hello from A" in texts
        assert "hello from B" not in texts


# ── DEV history + reply recording ──────────────────────────────────
def test_dev_ask_records_user_then_reply(monkeypatch):
    with tempfile.TemporaryDirectory() as base:
        import bingo.core.local_state as ls
        monkeypatch.setattr(ls, "state_dir", lambda: Path(base) / "state")
        ws = WebSession(Path(base), _cfg())

        captured = {}
        monkeypatch.setattr(ws._dev, "ask",
                            lambda m, fn, ft, history=None: captured.update(
                                msg=m, hist=history))
        ws.dev_ask("fix the bug")
        assert captured["msg"] == "fix the bug"
        # user turn is in history before the model runs
        assert any(t["content"] == "fix the bug" for t in ws.history.context())

        # simulate the streamed reply completing
        ws._on_dev_event("dev_done", {"full": "done, here is the fix"})
        roles = [t["role"] for t in ws.history.context()]
        assert roles[-2:] == ["user", "assistant"]


def test_dev_extract_file_from_reply():
    full = "Here you go.\nFILE: hello.py\n```python\nprint('hi')\n```"
    got = WebSession._dev_extract_file(full)
    assert got is not None
    assert got["name"] == "hello.py"
    assert "print('hi')" in got["text"]
    assert WebSession._dev_extract_file("no code here") is None


# ── pentest wiring (no live engine) ────────────────────────────────
def test_pentest_start_needs_target():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        events = []
        ws.set_loop(_FakeLoop())
        ws._clients.add(_Q(events))
        # no URL → error, engine not started
        assert ws.pentest_start("just some text") == ""


def test_finding_and_stats_cached_for_replay():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        ws.set_loop(_FakeLoop())
        ws._on_pentest_event("finding", {"title": "SQLi"})
        ws._on_pentest_event("stats", {"loops": 3})
        assert ws.findings == [{"title": "SQLi"}]
        assert ws.stats == {"loops": 3}


# ── app assembly + token/origin middleware ─────────────────────────
def test_app_registers_all_routes_and_serves_token():
    from bingo.web import server
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        ws.config_port = 17890
        app = server._make_app(ws)
        paths = {getattr(r, "path", "") for r in app.routes}
        for p in ("/", "/api/config", "/api/file", "/api/dev/ask",
                  "/api/pentest/start", "/api/scan", "/ws"):
            assert p in paths
        html = server._serve_index(17890, "en")
        assert "window.__BINGO__" in html
        assert security.SESSION_TOKEN in html


# ── request body is not mis-bound as a query param (422 regression) ─
def test_post_routes_bind_request_body_not_query():
    """`from __future__ import annotations` + function-local ``Request``
    import made FastAPI treat ``request`` as a required query param, so every
    POST returned 422. Guard: no route may declare a ``request`` query field."""
    from bingo.web import server
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        ws.config_port = 17890
        app = server._make_app(ws)
        for route in app.routes:
            dep = getattr(route, "dependant", None)
            if dep is None:
                continue
            names = {q.name for q in dep.query_params}
            assert "request" not in names, f"{route.path} mis-binds request"


# ── slash command palette ──────────────────────────────────────────
def test_slash_client_actions_return_action():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        assert ws.run_command("/clear")["action"] == "clear"
        assert ws.run_command("/help")["action"] == "help"
        assert ws.run_command("/model")["action"] == "settings"
        assert ws.run_command("/lang")["action"] == "settings"


def test_slash_unknown_command_is_flagged():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        r = ws.run_command("/definitely-not-a-command")
        assert r["ok"] is False


def test_slash_crack_and_report_run_server_side():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        # empty report → no findings message, never crashes
        assert ws.run_command("/report")["ok"] is True
        # crack with no arg → usage, not an exception
        assert ws.run_command("/crack")["ok"] is False


def test_slash_creds_never_echo_plaintext_password():
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        ws.run_command("/cred", "admin s3cr3tPASS")
        listing = ws.run_command("/cred", "list")["text"]
        assert "s3cr3tPASS" not in listing  # secret masked
        assert "admin" in listing
        assert "*" in listing


def test_all_cli_commands_present_in_web_catalog():
    """Every classic slash command must still be offered in the web palette."""
    from bingo.lang.strings import get_slash_commands
    cmds = {c for c, _ in get_slash_commands("en")}
    expected = {"/help", "/clear", "/model", "/config", "/history", "/export",
                "/lang", "/login", "/cred", "/session", "/retry", "/hint",
                "/crack", "/stop", "/report", "/load", "/quit"}
    assert expected <= cmds


# ── DEV chat replies must follow the UI language (config.lang) ──────
def test_dev_reply_language_follows_config_not_user_input():
    from bingo.web import dev
    # ambiguous "user's language" removed → deterministic per config.lang
    assert "user's language" not in dev._DEV_SYSTEM
    assert "中文" in dev._lang_directive("zh")
    assert "한국어" in dev._lang_directive("ko")
    assert "English" in dev._lang_directive("en")
    assert "English" in dev._lang_directive("")  # unknown → English


def test_dev_ask_injects_config_lang_into_system_prompt(monkeypatch):
    from bingo.web import dev as devmod
    captured = {}

    class _FakeModel:
        def chat_stream(self, messages):
            captured["system"] = messages[0].content
            return iter(())

    monkeypatch.setattr("bingo.models.registry.ModelRegistry.build",
                        lambda cfg: _FakeModel())
    with tempfile.TemporaryDirectory() as d:
        from bingo.models.base import ModelConfig
        c = _cfg("zh")
        c.add_model(ModelConfig(provider="deepseek", model="m",
                                api_key="k", base_url="u", alias="a"))
        ws = WebSession(Path(d), c)
        ws.dev_ask("파이썬으로 짜줘", "", "")  # user types Korean
        ws._dev._thread.join(timeout=2)
        assert "中文" in captured["system"]  # reply forced to zh, not ko


# ── model add / delete (web settings parity with CLI /model) ────────
def test_config_add_and_remove_model():
    from bingo.models.base import ModelConfig
    c = BingoConfig()
    c.add_model(ModelConfig(provider="deepseek", model="deepseek-v4-pro",
                            api_key="k1", base_url="u", alias="ds"))
    c.add_model(ModelConfig(provider="claude", model="claude-fable-5",
                            api_key="k2", base_url="u", alias="cl"))
    assert c.active_model == "ds"
    assert {m.display_name() for m in c.models} == {"ds", "cl"}
    # deleting the active model switches to the first remaining one
    assert c.remove_model("ds") is True
    assert c.active_model == "cl"
    assert len(c.models) == 1
    # deleting the last clears active_model
    assert c.remove_model("cl") is True
    assert c.active_model == ""
    assert c.models == []
    # unknown name is a no-op failure
    assert c.remove_model("nope") is False


def test_model_add_delete_routes_registered_and_bind_body():
    from bingo.web import server
    with tempfile.TemporaryDirectory() as d:
        ws = WebSession(Path(d), _cfg())
        ws.config_port = 17890
        app = server._make_app(ws)
        paths = {getattr(r, "path", "") for r in app.routes}
        assert "/api/model/add" in paths
        assert "/api/model/delete" in paths
        for route in app.routes:
            dep = getattr(route, "dependant", None)
            if dep is None:
                continue
            names = {q.name for q in dep.query_params}
            assert "request" not in names


# ── i18n leak guard (backend catalog) ──────────────────────────────
def test_index_lang_is_wired():
    from bingo.web import server
    html_zh = server._serve_index(17890, "zh")
    assert '"lang": "zh"' in html_zh


def test_chat_layout_pins_composer_and_scrolls_messages():
    """Chat column must stay height-bounded so the composer never scrolls
    off-screen and only #messages scrolls when the transcript grows."""
    css = (Path("bingo/web/static/css/app.css")).read_text(encoding="utf-8")

    def rule(sel: str) -> str:
        i = css.index(sel + "{")
        return css[i:css.index("}", i)]

    # the grid row must be capped so columns cannot grow past the viewport
    assert "grid-template-rows:minmax(0,1fr)" in rule("#app")
    chat = rule("#chat")
    assert "min-height:0" in chat and "height:100%" in chat
    msgs = rule("#messages")
    assert "min-height:0" in msgs and "overflow-y:auto" in msgs
    assert "flex:none" in rule("#composer")
    assert "flex:none" in rule("#findings")


def test_scan_log_localizer_leaves_no_hangul_and_keeps_dynamic():
    """Progress logs must follow config.lang (zh/en) with no Korean leaking,
    while dynamic values (URLs, counts) and Rich markup stay intact."""
    import re
    from bingo.redteam.log_i18n import localize_log

    ko = "[yellow]🛡 WAF 감지: cloudflare — 우회 기법 자동 활성화[/yellow]"
    zh = localize_log(ko, "zh")
    en = localize_log(ko, "en")
    assert not re.search(r"[가-힣]", zh)
    assert not re.search(r"[가-힣]", en)
    assert "cloudflare" in zh and "cloudflare" in en   # dynamic preserved
    assert "[yellow]" in zh and "[/yellow]" in en       # markup preserved
    # ko / unknown lang must pass through unchanged
    assert localize_log(ko, "ko") == ko
    assert localize_log(ko, "ja") == ko


def test_scan_log_localizer_covers_every_pipeline_string():
    """Every Korean progress string emitted by the redteam pipeline must
    fully localize with zero residual Hangul for zh and en."""
    import glob
    import re
    from bingo.redteam.log_i18n import localize_log

    call = re.compile(r'(?:self\.log|on_progress|\blog)\(\s*f?["\']')
    hangul = re.compile(r"[가-힣]")
    lit = re.compile(r'''f?(["\'])(.*?)\1''')
    ph = re.compile(r"\{[^}]*\}")
    residual = []
    for f in glob.glob("bingo/redteam/**/*.py", recursive=True):
        for ln in open(f, encoding="utf-8"):
            if not (call.search(ln) and hangul.search(ln)):
                continue
            m = lit.search(ln)
            if not m:
                continue
            fixed = ph.sub("§", m.group(2)).replace("\\n", "")
            for lang in ("zh", "en"):
                if hangul.search(localize_log(fixed, lang)):
                    residual.append((lang, fixed))
    assert not residual, f"unlocalized: {residual[:5]}"


# ── test doubles ───────────────────────────────────────────────────
class _FakeLoop:
    def call_soon_threadsafe(self, fn, *a):
        fn(*a)


class _Q:
    def __init__(self, sink):
        self._sink = sink

    def put_nowait(self, msg):
        self._sink.append(msg)
