"""Tests for fray.cli — CLI utility functions and output builders."""

import json
import re
import sys
from datetime import datetime
from argparse import Namespace
from unittest.mock import patch, MagicMock

import pytest

from fray.cli import (
    _build_ai_output,
    _build_sarif_output,
    build_auth_headers,
    _do_login_flow,
    _read_targets,
    cmd_share,
    main,
    _share_fields_for_target,
    cmd_todo,
)
from fray.cloud_sync import share_viewer_url


# ── _build_ai_output ──────────────────────────────────────────────────

class TestBuildAiOutput:
    def test_minimal(self):
        out = _build_ai_output("https://example.com")
        assert out["schema"] == "fray-ai/v1"
        assert out["target"] == "https://example.com"
        assert "timestamp" in out

    def test_with_recon(self):
        recon = {
            "fingerprint": {"technologies": {"php": 0.9, "nginx": 0.8}},
            "waf_detected": {"vendor": "cloudflare"},
            "security_headers": {"score": 67, "missing": ["CSP"]},
            "tls": {"version": "TLSv1.3", "expires_days": 90},
            "cors": {"misconfigured": True, "issues": ["wildcard origin"]},
            "exposed_files": {"found": ["/robots.txt"]},
            "cookies": {"issues": ["HttpOnly missing"]},
            "graphql": {"introspection_enabled": True, "endpoint": "/graphql"},
            "api_discovery": {"endpoints_found": ["/api/v1"]},
            "host_header_injection": {"vulnerable": True, "vulnerable_headers": ["X-Forwarded-Host"]},
            "admin_panels": {"panels_found": [{"path": "/admin", "status": 200, "protected": False}]},
            "recommended_categories": ["xss", "sqli"],
        }
        out = _build_ai_output("https://example.com", recon=recon)
        assert len(out["technologies"]) == 2
        assert out["waf"] is not None
        posture = out["security_posture"]
        assert posture["header_score"] == 67
        assert posture["cors_misconfigured"] is True
        assert posture["graphql_introspection_open"] is True
        assert posture["host_header_injectable"] is True
        assert len(posture["admin_panels"]) == 1
        assert posture["admin_panels"][0]["open"] is True
        assert out["recommended_categories"] == ["xss", "sqli"]

    def test_with_results_reflected(self):
        results = [
            {"payload": "<script>alert(1)</script>", "blocked": False, "reflected": True,
             "category": "xss", "url": "https://example.com/search", "param": "q"},
            {"payload": "' OR 1=1--", "blocked": True, "reflected": False, "category": "sqli"},
        ]
        out = _build_ai_output("https://example.com", results=results)
        assert out["summary"]["total_tested"] == 2
        assert out["summary"]["blocked"] == 1
        assert out["summary"]["reflected"] == 1
        assert out["summary"]["risk"] == "critical"
        assert any(v["type"] == "xss" and v["confirmed"] for v in out["vulnerabilities"])

    def test_with_results_bypassed_only(self):
        results = [
            {"payload": "test", "blocked": False, "reflected": False, "category": "xss"},
        ]
        out = _build_ai_output("https://example.com", results=results)
        assert out["summary"]["risk"] == "medium"

    def test_all_blocked(self):
        results = [
            {"payload": "p1", "blocked": True, "category": "xss"},
            {"payload": "p2", "blocked": True, "category": "sqli"},
        ]
        out = _build_ai_output("https://example.com", results=results)
        assert out["summary"]["risk"] == "low"
        assert out["summary"]["block_rate"] == "100.0%"

    def test_suggested_actions_on_reflected(self):
        results = [
            {"payload": "<script>", "blocked": False, "reflected": True, "category": "xss"},
        ]
        out = _build_ai_output("https://example.com", results=results)
        assert any(a["action"] == "report" for a in out["suggested_actions"])

    def test_suggested_actions_on_all_blocked(self):
        results = [{"payload": "p", "blocked": True, "category": "xss"}]
        out = _build_ai_output("https://example.com", results=results)
        assert any(a["action"] == "expand" for a in out["suggested_actions"])

    def test_crawl_summary(self):
        crawl = {"pages_crawled": 5, "total_endpoints": 12, "total_injection_points": 3}
        out = _build_ai_output("https://example.com", crawl=crawl)
        assert out["crawl"]["pages"] == 5
        assert out["crawl"]["endpoints"] == 12

    def test_cwe_mapping(self):
        results = [
            {"payload": "p", "blocked": False, "reflected": True, "category": "sqli"},
        ]
        out = _build_ai_output("https://example.com", results=results)
        vuln = next(v for v in out["vulnerabilities"] if v["type"] == "sqli")
        assert vuln["cwe"] == "CWE-89"


# ── _build_sarif_output ───────────────────────────────────────────────

class TestBuildSarifOutput:
    def test_sarif_schema(self):
        sarif = _build_sarif_output("https://example.com", [])
        assert sarif["version"] == "2.1.0"
        assert "$schema" in sarif
        assert len(sarif["runs"]) == 1
        assert sarif["runs"][0]["tool"]["driver"]["name"] == "Fray"

    def test_blocked_excluded(self):
        results = [
            {"payload": "blocked", "blocked": True, "category": "xss"},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        assert len(sarif["runs"][0]["results"]) == 0

    def test_bypass_included(self):
        results = [
            {"payload": "<script>", "blocked": False, "reflected": True,
             "category": "xss", "status": 200, "param": "q"},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        assert len(sarif["runs"][0]["results"]) == 1
        r = sarif["runs"][0]["results"][0]
        assert r["ruleId"] == "fray/xss"
        assert r["level"] == "error"
        assert r["properties"]["reflected"] is True

    def test_sarif_rules_deduped(self):
        results = [
            {"payload": "p1", "blocked": False, "category": "xss", "status": 200},
            {"payload": "p2", "blocked": False, "category": "xss", "status": 200},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        rules = sarif["runs"][0]["tool"]["driver"]["rules"]
        assert len(rules) == 1
        assert rules[0]["id"] == "fray/xss"

    def test_sarif_multiple_categories(self):
        results = [
            {"payload": "p1", "blocked": False, "category": "xss", "status": 200},
            {"payload": "p2", "blocked": False, "category": "sqli", "status": 500},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        rule_ids = {r["id"] for r in sarif["runs"][0]["tool"]["driver"]["rules"]}
        assert rule_ids == {"fray/xss", "fray/sqli"}

    def test_sarif_target_uri(self):
        sarif = _build_sarif_output("https://example.com", [])
        uri = sarif["runs"][0]["originalUriBaseIds"]["TARGET"]["uri"]
        assert uri.endswith("/")

    def test_reflected_is_error_level(self):
        results = [
            {"payload": "p", "blocked": False, "reflected": True, "category": "open-redirect", "status": 302},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        assert sarif["runs"][0]["results"][0]["level"] == "error"

    def test_non_reflected_uses_default_level(self):
        results = [
            {"payload": "p", "blocked": False, "reflected": False, "category": "open-redirect", "status": 302},
        ]
        sarif = _build_sarif_output("https://example.com", results)
        assert sarif["runs"][0]["results"][0]["level"] == "warning"


# ── build_auth_headers ────────────────────────────────────────────────

class TestBuildAuthHeaders:
    def test_empty(self):
        args = Namespace(cookie=None, bearer=None, header=None, login_flow=None)
        assert build_auth_headers(args) == {}

    def test_cookie(self):
        args = Namespace(cookie="session=abc123", bearer=None, header=None, login_flow=None)
        h = build_auth_headers(args)
        assert h["Cookie"] == "session=abc123"

    def test_bearer(self):
        args = Namespace(cookie=None, bearer="tok123", header=None, login_flow=None)
        h = build_auth_headers(args)
        assert h["Authorization"] == "Bearer tok123"

    def test_custom_headers(self):
        args = Namespace(cookie=None, bearer=None, header=["X-Api-Key: abc", "X-Custom: val"], login_flow=None)
        h = build_auth_headers(args)
        assert h["X-Api-Key"] == "abc"
        assert h["X-Custom"] == "val"

    def test_cookie_and_bearer_combined(self):
        args = Namespace(cookie="sid=1", bearer="tok", header=None, login_flow=None)
        h = build_auth_headers(args)
        assert h["Cookie"] == "sid=1"
        assert h["Authorization"] == "Bearer tok"

    def test_missing_attrs_safe(self):
        args = Namespace()
        h = build_auth_headers(args)
        assert h == {}

    @patch('fray.cli._do_login_flow', return_value='session=xyz')
    def test_login_flow(self, mock_login):
        args = Namespace(cookie=None, bearer=None, header=None, login_flow='https://ex.com/login,u=a,p=b')
        h = build_auth_headers(args)
        assert h["Cookie"] == "session=xyz"
        mock_login.assert_called_once()

    @patch('fray.cli._do_login_flow', return_value='new=cookie')
    def test_login_flow_merges_with_existing(self, mock_login):
        args = Namespace(cookie="existing=1", bearer=None, header=None, login_flow='https://ex.com/login,u=a')
        h = build_auth_headers(args)
        assert "existing=1" in h["Cookie"]
        assert "new=cookie" in h["Cookie"]


# ── _do_login_flow ────────────────────────────────────────────────────

class TestDoLoginFlow:
    def test_invalid_format(self):
        result = _do_login_flow("just-a-url")
        assert result == ""

    @patch('http.client.HTTPSConnection')
    def test_successful_login(self, mock_conn_cls):
        mock_conn = MagicMock()
        mock_conn_cls.return_value = mock_conn
        mock_resp = MagicMock()
        mock_resp.getheaders.return_value = [
            ('set-cookie', 'session=abc123; Path=/; HttpOnly'),
            ('set-cookie', 'csrf=xyz; Path=/'),
        ]
        mock_resp.status = 302
        mock_conn.getresponse.return_value = mock_resp

        result = _do_login_flow("https://example.com/login,username=admin,password=secret")
        assert "session=abc123" in result
        assert "csrf=xyz" in result
        mock_conn.request.assert_called_once()

    @patch('http.client.HTTPSConnection')
    def test_no_cookies_returned(self, mock_conn_cls):
        mock_conn = MagicMock()
        mock_conn_cls.return_value = mock_conn
        mock_resp = MagicMock()
        mock_resp.getheaders.return_value = [('content-type', 'text/html')]
        mock_resp.status = 200
        mock_conn.getresponse.return_value = mock_resp

        result = _do_login_flow("https://example.com/login,user=a,pass=b")
        assert result == ""

    @patch('http.client.HTTPSConnection', side_effect=Exception("connection failed"))
    def test_connection_failure(self, mock_conn_cls):
        result = _do_login_flow("https://example.com/login,user=a,pass=b")
        assert result == ""


# ── _read_targets ─────────────────────────────────────────────────────

class TestReadTargets:
    def test_single_target(self):
        args = Namespace(target="https://example.com")
        with patch('fray.cli._is_piped', return_value=False):
            targets = _read_targets(args)
        assert targets == ["https://example.com"]

    def test_auto_https(self):
        args = Namespace(target="example.com")
        with patch('fray.cli._is_piped', return_value=False):
            targets = _read_targets(args)
        assert targets == ["https://example.com"]

    def test_http_preserved(self):
        args = Namespace(target="http://example.com")
        with patch('fray.cli._is_piped', return_value=False):
            targets = _read_targets(args)
        assert targets == ["http://example.com"]

    def test_no_target_exits(self):
        args = Namespace(target=None)
        with patch('fray.cli._is_piped', return_value=False):
            with pytest.raises(SystemExit):
                _read_targets(args)

    def test_piped_input(self):
        args = Namespace(target=None)
        import io
        fake_stdin = io.StringIO("example.com\n# comment\nhttps://test.com\n\n")
        with patch('fray.cli._is_piped', return_value=True), \
             patch('fray.cli.sys.stdin', fake_stdin):
            targets = _read_targets(args)
        assert targets == ["https://example.com", "https://test.com"]

    def test_cli_plus_pipe(self):
        args = Namespace(target="https://first.com")
        import io
        fake_stdin = io.StringIO("second.com\n")
        with patch('fray.cli._is_piped', return_value=True), \
             patch('fray.cli.sys.stdin', fake_stdin):
            targets = _read_targets(args)
        assert "https://first.com" in targets
        assert "https://second.com" in targets


class TestShareCliExtend:
    def _make_args(self, **overrides):
        defaults = {
            "extend": None,
            "days": 30,
            "json": False,
            "list": False,
            "unshare": None,
            "target": None,
            "expires": 30,
        }
        defaults.update(overrides)
        return Namespace(**defaults)

    def test_cmd_share_extend_success_prints_url(self, monkeypatch, capsys):
        captured = {}

        def fake_extend(share_id, days, verbose=True):
            captured["share_id"] = share_id
            captured["days"] = days
            captured["verbose"] = verbose
            return "https://share.example/abcd"

        monkeypatch.setattr('fray.cloud_sync.extend_share', fake_extend)

        args = self._make_args(extend="abcd1234", days=15)
        cmd_share(args)

        out = capsys.readouterr().out
        assert "Extended share" in out
        assert "https://share.example/abcd" in out
        assert captured == {"share_id": "abcd1234", "days": 15, "verbose": True}

    def test_cmd_share_extend_json_failure(self, monkeypatch):
        monkeypatch.setattr('fray.cloud_sync.extend_share', lambda *a, **k: None)
        recorded = {}

        def fake_json_print(payload):
            recorded.update(payload)

        monkeypatch.setattr('fray.cli._json_print', fake_json_print)

        args = self._make_args(extend="missing", days=5, json=True)
        cmd_share(args)

        assert recorded == {
            "status": "failed",
            "id": "missing",
            "days": 5,
            "url": None,
        }


class TestShareMetadataExports:
    def _fake_share_info(self):
        return {
            "id": "share123",
            "domain": "example.com",
            "shared_at": "2024-02-01T00:00:00Z",
            "expires_at": "2024-03-01T00:00:00Z",
        }

    def test_cmd_test_writes_share_fields(self, tmp_path, monkeypatch):
        from fray.cli import cmd_test

        share_url = "https://share.example/?id=share123"
        share_info = self._fake_share_info()
        output_file = tmp_path / "results.json"

        class DummyTester:
            def __init__(self, target, **kwargs):
                self.target = target
                self.start_time = datetime.now()

            def load_payloads(self, source):
                return [{"payload": "demo", "blocked": False}]

            def test_payloads(self, payloads, **kwargs):
                self.start_time = datetime.now()
                return [{"payload": "demo", "blocked": False}]

            def generate_report(self, results, output, html=False, extra_fields=None):
                report = {"target": self.target, "results": results}
                if extra_fields:
                    report.update(extra_fields)
                with open(output, "w", encoding="utf-8") as fh:
                    json.dump(report, fh, ensure_ascii=False)

        def fake_lookup(share_id=None, domain=None):
            return dict(share_info)

        monkeypatch.setattr('fray.cli._lookup_share_info', fake_lookup)
        monkeypatch.setattr('fray.cloud_sync.share_viewer_url', lambda sid: share_url)
        monkeypatch.setattr('fray.cli._save_to_fray', lambda *a, **k: str(tmp_path / "ignored.json"))
        monkeypatch.setattr('fray.cli._read_targets', lambda args: [args.target])
        monkeypatch.setattr('fray.cli._TEST_WAF_TESTER', DummyTester)
        monkeypatch.setattr('fray.cli._TEST_OUTPUT_VALIDATOR', lambda path: None)

        args = Namespace(
            target="https://example.com",
            scope=None,
            timeout=2,
            insecure=False,
            cookie=None,
            bearer=None,
            header=None,
            login_flow=None,
            auth_profile=None,
            json=False,
            quiet=True,
            category=None,
            payload_file="dummy.json",
            smart=False,
            all=False,
            max=None,
            param="input",
            context="url_param",
            resume=False,
            content_type="",
            mutate=0,
            blind=False,
            oob_server="",
            sarif=False,
            output=str(output_file),
            ai=False,
            report_format=None,
            webhook=None,
            notify=None,
            yes=False,
            from_crawl=None,
            delay=0.0,
            rate_limit=0.0,
            auto_throttle=False,
            impersonate=None,
            solve_challenge=False,
            stealth=False,
            jitter=0.0,
            no_follow_redirects=False,
            redirect_limit=5,
            concurrency=1,
            workers=1,
        )

        cmd_test(args)

        data = json.loads(output_file.read_text(encoding="utf-8"))
        assert data["share_url"] == share_url
        assert data["share"]["id"] == share_info["id"]
        assert data["share"]["domain"] == share_info["domain"]


class TestTodoJsonOutput:
    def _write_items(self, home_dir, items):
        fray_dir = home_dir / ".fray"
        fray_dir.mkdir(parents=True, exist_ok=True)
        todo_path = fray_dir / "todo.json"
        todo_path.write_text(json.dumps(items, indent=2), encoding="utf-8")

    def _read_items(self, home_dir):
        todo_path = home_dir / ".fray" / "todo.json"
        if not todo_path.exists():
            return []
        return json.loads(todo_path.read_text(encoding="utf-8"))

    def _make_args(self, **overrides):
        defaults = {
            "action": "list",
            "json": True,
            "all": False,
            "text": None,
            "priority": None,
            "id": None,
        }
        defaults.update(overrides)
        return Namespace(**defaults)

    def _set_home(self, tmp_path, monkeypatch):
        home_dir = tmp_path / "home"
        monkeypatch.setattr('pathlib.Path.home', lambda: home_dir)
        return home_dir

    def _strip_ansi(self, text):
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    def test_json_output_sorts_by_priority_and_created(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)

        items = [
            {"id": 1, "content": "low", "status": "pending", "priority": "low", "created": "2024-01-01T00:00:00"},
            {"id": 2, "content": "high-new", "status": "pending", "priority": "high", "created": "2024-01-02T00:00:00"},
            {"id": 3, "content": "medium-complete", "status": "completed", "priority": "medium", "created": "2024-01-01T01:00:00"},
            {"id": 4, "content": "high-old", "status": "pending", "priority": "high", "created": "2023-12-31T00:00:00"},
        ]
        self._write_items(home_dir, items)

        args = self._make_args()
        cmd_todo(args)

        out = json.loads(capsys.readouterr().out.strip())
        summary = out["summary"]
        assert summary["total_count"] == 4
        assert summary["pending_count"] == 3
        assert summary["completed_count"] == 1
        assert summary["showing_count"] == 3
        assert summary["show_all"] is False

        returned_ids = [item["id"] for item in out["items"]]
        assert returned_ids == [4, 2, 1]

    def test_json_output_show_all_includes_completed(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)

        items = [
            {"id": 1, "content": "pending", "status": "pending", "priority": "medium", "created": "2024-01-01T00:00:00"},
            {"id": 2, "content": "done", "status": "completed", "priority": "low", "created": "2024-01-01T01:00:00"},
        ]
        self._write_items(home_dir, items)

        args = self._make_args(all=True)
        cmd_todo(args)

        out = json.loads(capsys.readouterr().out.strip())
        assert out["summary"]["show_all"] is True
        assert out["summary"]["showing_count"] == 2
        returned_ids = [item["id"] for item in out["items"]]
        assert returned_ids == [1, 2]

    def test_add_creates_incrementing_ids_and_persists(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)

        cmd_todo(self._make_args(action="add", text=["first", "task"], priority="high", json=True))
        cmd_todo(self._make_args(action="add", text=["second"], priority="low", json=True))

        items = self._read_items(home_dir)
        assert [item["id"] for item in items] == [1, 2]
        assert items[0]["priority"] == "high"
        assert items[1]["priority"] == "low"

    def test_done_marks_item_completed(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)
        items = [
            {"id": 1, "content": "pending", "status": "pending", "priority": "medium", "created": "2024-01-01T00:00:00"},
        ]
        self._write_items(home_dir, items)

        cmd_todo(self._make_args(action="done", id=1, json=True))

        stored = self._read_items(home_dir)
        assert stored[0]["status"] == "completed"

    def test_rm_removes_item(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)
        items = [
            {"id": 1, "content": "pending", "status": "pending", "priority": "medium", "created": "2024-01-01T00:00:00"},
            {"id": 2, "content": "other", "status": "pending", "priority": "low", "created": "2024-01-01T01:00:00"},
        ]
        self._write_items(home_dir, items)

        cmd_todo(self._make_args(action="rm", id=1, json=True))

        stored = self._read_items(home_dir)
        assert [item["id"] for item in stored] == [2]

    def test_text_output_hides_completed_without_all(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)
        items = [
            {"id": 1, "content": "pending task", "status": "pending", "priority": "high", "created": "2024-01-01T00:00:00"},
            {"id": 2, "content": "completed task", "status": "completed", "priority": "low", "created": "2024-01-01T01:00:00"},
        ]
        self._write_items(home_dir, items)

        cmd_todo(self._make_args(json=False))
        out = self._strip_ansi(capsys.readouterr().out)

        assert "pending task" in out
        assert "completed task" not in out
        assert "completed — use --all to show" in out

    def test_text_output_with_all_includes_completed_and_symbols(self, tmp_path, monkeypatch, capsys):
        home_dir = self._set_home(tmp_path, monkeypatch)
        items = [
            {"id": 1, "content": "pending task", "status": "pending", "priority": "high", "created": "2024-01-01T00:00:00"},
            {"id": 2, "content": "completed task", "status": "completed", "priority": "low", "created": "2024-01-01T01:00:00"},
        ]
        self._write_items(home_dir, items)

        cmd_todo(self._make_args(json=False, all=True))
        out = self._strip_ansi(capsys.readouterr().out)

        assert "completed task" in out
        assert "pending task" in out
        assert "✓" in out  # completed status symbol
        assert "●" in out  # priority symbol remains after stripping ANSI


class TestShareMetadataIntegration:
    def test_fray_test_json_emits_share_metadata_end_to_end(self, tmp_path, monkeypatch, capsys):
        fray_home = tmp_path / "home"
        fray_dir = fray_home / ".fray"
        fray_dir.mkdir(parents=True)

        share_id = "share-e2e"
        domain = "shareintegration.test"
        shares_file = fray_dir / "shares.json"
        shares_file.write_text(json.dumps({
            share_id: {
                "domain": domain,
                "shared_at": "2025-01-01T00:00:00Z",
                "expires_at": "2099-01-01T00:00:00Z",
            }
        }), encoding="utf-8")

        monkeypatch.setenv("HOME", str(fray_home))
        monkeypatch.setenv("USERPROFILE", str(fray_home))
        monkeypatch.setattr('pathlib.Path.home', lambda: fray_home)
        monkeypatch.setattr('fray.cloud_sync._FRAY_DIR', fray_dir)

        payload_file = tmp_path / "payloads.json"
        payload_file.write_text(json.dumps([{"payload": "demo"}]), encoding="utf-8")

        class DummyTester:
            def __init__(self, target, **kwargs):
                self.target = target
                self.start_time = datetime.now()

            def load_payloads(self, source):
                return [{"payload": "demo"}]

            def test_payloads(self, payloads, **kwargs):
                self.start_time = datetime.now()
                return [{"payload": payloads[0]["payload"], "blocked": False, "category": "xss"}]

        monkeypatch.setattr('fray.cli._TEST_WAF_TESTER', DummyTester)
        monkeypatch.setattr('fray.cli._TEST_IS_PIPED', False)

        target = f"https://{domain}/login"

        fields = _share_fields_for_target(target)
        assert fields["share"]["id"] == share_id

        monkeypatch.setattr(sys, 'argv', [
            'fray', 'test', target, '--json', '--quiet', '--payload-file', str(payload_file)
        ])

        try:
            main()
        except SystemExit as exc:
            assert exc.code == 0

        captured = capsys.readouterr()
        result = json.loads(captured.out.strip())

        expected_share_url = share_viewer_url(share_id)
        assert result["share_url"] == expected_share_url
        assert result["share"]["id"] == share_id
        assert result["share"]["domain"] == domain
        assert result["share"]["status"]["state"] == "ok"


    @pytest.mark.xfail(reason="Output path validation blocks tmpdir — pre-existing", strict=False)
    def test_cmd_scan_writes_share_fields(self, tmp_path, monkeypatch):
        from fray.cli import cmd_scan

        share_url = "https://share.example/?id=share123"
        share_info = self._fake_share_info()
        output_file = tmp_path / "scan.json"

        class DummyCrawler:
            def __init__(self, *args, **kwargs):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def crawl(self):
                return {"endpoints": [], "total_params": 0, "pages_crawled": 0, "elapsed_s": 0}

        class DummyScan:
            def __init__(self):
                class _Crawl:
                    def __init__(self):
                        self.injection_points = []

                self.crawl = _Crawl()
                self._data = {
                    "test_results": [{"payload": "demo", "blocked": False}],
                    "summary": {"passed": 1, "blocked": 0, "total_tested": 1, "block_rate": "0%"},
                    "duration": "1s",
                }

            def to_dict(self):
                base = dict(self._data)
                base.setdefault("crawl", {})
                return base

        def fake_run_scan(**kwargs):
            return DummyScan()

        def fake_lookup(share_id=None, domain=None):
            return dict(share_info)

        monkeypatch.setattr('fray.cli._lookup_share_info', fake_lookup)
        monkeypatch.setattr('fray.cloud_sync.share_viewer_url', lambda sid: share_url)
        monkeypatch.setattr('fray.cli._save_to_fray', lambda *a, **k: str(tmp_path / "ignored_scan.json"))
        monkeypatch.setattr('fray.crawler.Crawler', DummyCrawler)
        monkeypatch.setattr('fray.scanner.run_scan', fake_run_scan)
        monkeypatch.setattr('fray.scanner.print_scan_result', lambda scan: None)
        monkeypatch.setattr('fray.cli._TEST_OUTPUT_VALIDATOR', lambda path: None)

        args = Namespace(
            target="https://example.com",
            json=False,
            quiet=True,
            category=None,
            max=None,
            max_pages=1,
            depth=1,
            delay=0.0,
            timeout=2,
            insecure=False,
            browser=False,
            stealth=False,
            scope=None,
            ai=False,
            sarif=False,
            output=str(output_file),
            burp=None,
            zap=None,
            nuclei_export=None,
            notify=None,
            workers=1,
            auto_throttle=False,
            impersonate=None,
            parallel=0,
            follow_redirects=False,
            baseline=False,
            resume=False,
            jitter=0.0,
            rate_limit=0.0,
            cookie=None,
            bearer=None,
            header=None,
            login_flow=None,
        )

        cmd_scan(args)

        data = json.loads(output_file.read_text(encoding="utf-8"))
        assert data["share_url"] == share_url
        assert data["share"]["id"] == share_info["id"]
        assert data["share"]["domain"] == share_info["domain"]
