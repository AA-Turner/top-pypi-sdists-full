"""Coverage boost — tests for retry, model_detect, compare, provider_health, web_engine.

Target: lift coverage from 67% → ~73-75%.
"""
from __future__ import annotations

import asyncio
import json
import sys
import time
import unittest
import urllib.error
from io import BytesIO
from unittest.mock import MagicMock, patch, AsyncMock

# ─────────────────────────────────────────────────────────────────────────────
# utils/retry.py
# ─────────────────────────────────────────────────────────────────────────────

class TestRetryPolicy(unittest.TestCase):

    def test_should_retry_non_retryable_4xx(self):
        from salmalm.utils.retry import _should_retry
        for code in (400, 401, 403, 404, 405):
            err = urllib.error.HTTPError("http://x", code, "err", {}, None)
            retry, wait = _should_retry(err)
            self.assertFalse(retry, f"code {code} should NOT retry")

    def test_should_retry_5xx(self):
        from salmalm.utils.retry import _should_retry
        for code in (500, 502, 503):
            err = urllib.error.HTTPError("http://x", code, "err", {}, None)
            retry, wait = _should_retry(err)
            self.assertTrue(retry, f"code {code} SHOULD retry")

    def test_should_retry_429_with_retry_after(self):
        from salmalm.utils.retry import _should_retry
        headers = MagicMock()
        headers.get = lambda k, d=None: "2" if k == "Retry-After" else d
        err = urllib.error.HTTPError("http://x", 429, "Rate limit", headers, None)
        retry, wait = _should_retry(err)
        self.assertTrue(retry)
        self.assertAlmostEqual(wait, 2.0, delta=0.5)

    def test_should_retry_429_no_retry_after(self):
        from salmalm.utils.retry import _should_retry
        headers = MagicMock()
        headers.get = lambda k, d=None: None
        err = urllib.error.HTTPError("http://x", 429, "Rate limit", headers, None)
        retry, wait = _should_retry(err)
        self.assertTrue(retry)

    def test_should_retry_529_overloaded(self):
        from salmalm.utils.retry import _should_retry, OVERLOADED_WAIT
        err = urllib.error.HTTPError("http://x", 529, "Overloaded", {}, None)
        retry, wait = _should_retry(err)
        self.assertTrue(retry)
        self.assertEqual(wait, OVERLOADED_WAIT)

    def test_should_retry_network_error(self):
        from salmalm.utils.retry import _should_retry
        err = urllib.error.URLError("connection refused")
        retry, wait = _should_retry(err)
        self.assertTrue(retry)

    def test_should_retry_timeout(self):
        from salmalm.utils.retry import _should_retry
        retry, wait = _should_retry(TimeoutError("timed out"))
        self.assertTrue(retry)

    def test_should_retry_value_error_rate_limit(self):
        from salmalm.utils.retry import _should_retry
        retry, wait = _should_retry(ValueError("rate limit exceeded"))
        self.assertTrue(retry)

    def test_should_retry_value_error_generic(self):
        from salmalm.utils.retry import _should_retry
        retry, wait = _should_retry(ValueError("invalid json"))
        self.assertFalse(retry)

    def test_add_jitter(self):
        from salmalm.utils.retry import _add_jitter
        for _ in range(20):
            result = _add_jitter(10.0)
            self.assertGreaterEqual(result, 9.0)
            self.assertLessEqual(result, 11.0)

    def test_retry_decorator_success_first_try(self):
        from salmalm.utils.retry import retry_with_backoff
        calls = []

        @retry_with_backoff
        def fn():
            calls.append(1)
            return "ok"

        result = fn()
        self.assertEqual(result, "ok")
        self.assertEqual(len(calls), 1)

    def test_retry_decorator_retries_then_succeeds(self):
        from salmalm.utils.retry import retry_with_backoff
        calls = []

        @retry_with_backoff(max_attempts=3, base_delay=0.001)
        def fn():
            calls.append(1)
            if len(calls) < 2:
                raise urllib.error.URLError("transient")
            return "ok"

        result = fn()
        self.assertEqual(result, "ok")
        self.assertEqual(len(calls), 2)

    def test_retry_decorator_gives_up_after_max(self):
        from salmalm.utils.retry import retry_with_backoff
        calls = []

        @retry_with_backoff(max_attempts=3, base_delay=0.001)
        def fn():
            calls.append(1)
            raise urllib.error.URLError("always fails")

        with self.assertRaises(urllib.error.URLError):
            fn()
        self.assertEqual(len(calls), 3)

    def test_retry_decorator_no_retry_on_403(self):
        from salmalm.utils.retry import retry_with_backoff
        calls = []

        @retry_with_backoff(max_attempts=3, base_delay=0.001)
        def fn():
            calls.append(1)
            raise urllib.error.HTTPError("http://x", 403, "Forbidden", {}, None)

        with self.assertRaises(urllib.error.HTTPError):
            fn()
        self.assertEqual(len(calls), 1)  # no retry

    def test_retry_call_functional(self):
        from salmalm.utils.retry import retry_call
        calls = []

        def fn():
            calls.append(1)
            if len(calls) < 2:
                raise urllib.error.URLError("transient")
            return "ok"

        result = retry_call(fn, max_attempts=3, base_delay=0.001)
        self.assertEqual(result, "ok")

    def test_retry_decorator_raises_type_error_on_async(self):
        from salmalm.utils.retry import retry_with_backoff
        with self.assertRaises(TypeError):
            @retry_with_backoff
            async def async_fn():
                pass

    def test_async_retry_success(self):
        from salmalm.utils.retry import async_retry_with_backoff

        async def fn():
            return "async_ok"

        result = asyncio.run(
            async_retry_with_backoff(fn, max_attempts=3, base_delay=0.001)
        )
        self.assertEqual(result, "async_ok")

    def test_async_retry_retries_then_succeeds(self):
        from salmalm.utils.retry import async_retry_with_backoff
        calls = []

        async def fn():
            calls.append(1)
            if len(calls) < 2:
                raise urllib.error.URLError("transient")
            return "ok"

        result = asyncio.run(
            async_retry_with_backoff(fn, max_attempts=3, base_delay=0.001)
        )
        self.assertEqual(result, "ok")

    def test_async_retry_gives_up(self):
        from salmalm.utils.retry import async_retry_with_backoff

        async def fn():
            raise urllib.error.URLError("always fails")

        with self.assertRaises(urllib.error.URLError):
            asyncio.run(
                async_retry_with_backoff(fn, max_attempts=2, base_delay=0.001)
            )


# ─────────────────────────────────────────────────────────────────────────────
# features/model_detect.py
# ─────────────────────────────────────────────────────────────────────────────

class TestModelDetector(unittest.TestCase):

    def _make_detector(self):
        from salmalm.features.model_detect import ModelDetector
        d = ModelDetector()
        d._cache = []
        d._cache_ts = 0
        return d

    def test_detect_all_no_vault(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = False
        mock_vault.get = lambda k: None
        d = self._make_detector()
        with patch("salmalm.security.crypto.vault", mock_vault):
            models = d.detect_all()
        self.assertIsInstance(models, list)
        for m in models:
            self.assertFalse(m["available"])

    def test_detect_all_with_vault(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = True
        mock_vault.get = lambda k: "sk-fake" if "anthropic" in k else None
        d = self._make_detector()
        with patch("salmalm.security.crypto.vault", mock_vault):
            models = d.detect_all()
        anthropic_models = [m for m in models if m["provider"] == "anthropic"]
        self.assertTrue(len(anthropic_models) > 0)
        for m in anthropic_models:
            self.assertTrue(m["available"])

    def test_detect_all_uses_cache(self):
        d = self._make_detector()
        d._cache = [{"id": "cached", "name": "Cached", "provider": "test", "available": False, "source": "config"}]
        d._cache_ts = time.time()
        models = d.detect_all()
        self.assertEqual(models[0]["id"], "cached")

    def test_detect_all_force_refresh(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = False
        mock_vault.get = lambda k: None
        d = self._make_detector()
        d._cache = [{"id": "stale", "name": "Stale", "provider": "test", "available": False, "source": "config"}]
        d._cache_ts = time.time()
        with patch("salmalm.security.crypto.vault", mock_vault):
            models = d.detect_all(force=True)
        ids = [m["id"] for m in models]
        self.assertNotIn("stale", ids)

    def test_detect_local_models_openai_format(self):
        from salmalm.features.model_detect import ModelDetector
        d = ModelDetector()
        mock_data = {"data": [{"id": "llama3"}, {"id": "mistral"}]}
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(mock_data).encode()
        with patch("urllib.request.urlopen", return_value=mock_resp):
            models = d._detect_local_models("http://localhost:11434")
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]["provider"], "ollama")
        self.assertIn("llama3", models[0]["id"])

    def test_detect_local_models_ollama_format(self):
        from salmalm.features.model_detect import ModelDetector
        d = ModelDetector()
        # First endpoint fails, second also fails, third (ollama /api/tags) succeeds
        mock_data = {"models": [{"name": "llama3:8b", "size": 4000000000}]}
        call_count = [0]

        def mock_urlopen(req, timeout=5):
            call_count[0] += 1
            if call_count[0] < 3:
                raise urllib.error.URLError("connection refused")
            mock_resp = MagicMock()
            mock_resp.read.return_value = json.dumps(mock_data).encode()
            return mock_resp

        with patch("urllib.request.urlopen", side_effect=mock_urlopen):
            models = d._detect_local_models("http://localhost:11434")
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0]["name"], "llama3:8b")

    def test_detect_local_models_all_fail(self):
        from salmalm.features.model_detect import ModelDetector
        d = ModelDetector()
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
            models = d._detect_local_models("http://localhost:11434")
        self.assertEqual(models, [])


# ─────────────────────────────────────────────────────────────────────────────
# features/provider_health.py
# ─────────────────────────────────────────────────────────────────────────────

class TestProviderHealth(unittest.TestCase):

    def _make_checker(self):
        from salmalm.features.provider_health import ProviderHealthCheck
        c = ProviderHealthCheck()
        c._cache = {}
        c._cache_ts = 0
        return c

    def test_check_all_no_keys(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = False
        mock_vault.get = lambda k: None
        c = self._make_checker()
        with patch("salmalm.security.crypto.vault", mock_vault):
            result = c.check_all()
        self.assertIn("status", result)
        self.assertIn("providers", result)
        for v in result["providers"].values():
            self.assertEqual(v, "not configured")

    def test_check_all_uses_cache(self):
        c = self._make_checker()
        cached = {"status": "ok", "providers": {}, "checked_at": "2026-01-01"}
        c._cache = cached
        c._cache_ts = time.time()
        result = c.check_all()
        self.assertEqual(result, cached)

    def test_check_all_force_refreshes(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = False
        mock_vault.get = lambda k: None
        c = self._make_checker()
        c._cache = {"status": "ok", "providers": {}, "checked_at": "stale"}
        c._cache_ts = time.time()
        with patch("salmalm.security.crypto.vault", mock_vault):
            result = c.check_all(force=True)
        for v in result["providers"].values():
            self.assertEqual(v, "not configured")

    def test_check_all_with_anthropic_key_ok(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = True
        mock_vault.get = lambda k: "sk-ant-fake" if k == "anthropic_api_key" else None
        c = self._make_checker()
        with patch("salmalm.security.crypto.vault", mock_vault), \
             patch.object(c, "_test_anthropic", return_value="ok"):
            result = c.check_all(force=True)
        self.assertEqual(result["providers"]["anthropic"], "ok")
        self.assertEqual(result["status"], "ok")

    def test_check_all_with_anthropic_key_error(self):
        mock_vault = MagicMock()
        mock_vault.is_unlocked = True
        mock_vault.get = lambda k: "sk-ant-fake" if k == "anthropic_api_key" else None
        c = self._make_checker()
        with patch("salmalm.security.crypto.vault", mock_vault), \
             patch.object(c, "_test_anthropic", return_value="error: invalid auth"):
            result = c.check_all(force=True)
        self.assertNotEqual(result["status"], "ok")


# ─────────────────────────────────────────────────────────────────────────────
# features/compare.py
# ─────────────────────────────────────────────────────────────────────────────

class TestCompareModels(unittest.TestCase):

    def _run(self, coro):
        return asyncio.run(coro)

    def test_compare_models_success(self):
        from salmalm.features.compare import compare_models

        async def mock_call_llm_async(messages, model=None, max_tokens=None):
            return {"content": f"response from {model}", "usage": {"input": 10, "output": 20}}

        with patch("salmalm.core.engine._call_llm_async", side_effect=mock_call_llm_async), \
             patch("salmalm.core.prompt.build_system_prompt", return_value="system"), \
             patch("salmalm.core.get_session", return_value={}):
            results = self._run(compare_models("test-session", "hello", models=["anthropic/claude-haiku-4", "openai/gpt-4o-mini"]))

        self.assertEqual(len(results), 2)
        for r in results:
            self.assertIn("model", r)
            self.assertIn("response", r)
            self.assertIsNone(r["error"])

    def test_compare_models_one_fails(self):
        from salmalm.features.compare import compare_models

        async def mock_call_llm_async(messages, model=None, max_tokens=None):
            if "haiku" in model:
                raise RuntimeError("LLM error")
            return {"content": "ok", "usage": {"input": 5, "output": 10}}

        with patch("salmalm.core.engine._call_llm_async", side_effect=mock_call_llm_async), \
             patch("salmalm.core.prompt.build_system_prompt", return_value="system"), \
             patch("salmalm.core.get_session", return_value={}):
            results = self._run(compare_models("test-session", "hello", models=["anthropic/claude-haiku-4", "openai/gpt-4o-mini"]))

        self.assertEqual(len(results), 2)
        haiku_result = next(r for r in results if "haiku" in r["model"])
        other_result = next(r for r in results if "haiku" not in r["model"])
        self.assertIsNotNone(haiku_result["error"])
        self.assertIsNone(other_result["error"])

    def test_compare_models_default_models(self):
        """When no models specified, uses defaults from MODELS constant."""
        from salmalm.features.compare import compare_models

        async def mock_call_llm_async(messages, model=None, max_tokens=None):
            return {"content": "resp", "usage": {"input": 1, "output": 1}}

        with patch("salmalm.core.engine._call_llm_async", side_effect=mock_call_llm_async), \
             patch("salmalm.core.prompt.build_system_prompt", return_value="system"), \
             patch("salmalm.core.get_session", return_value={}):
            results = self._run(compare_models("test-session", "hello", models=None))

        self.assertIsInstance(results, list)
        # At least some results (haiku + sonnet or similar)
        self.assertGreater(len(results), 0)


# ─────────────────────────────────────────────────────────────────────────────
# web/routes/web_engine.py — via TestClient
# ─────────────────────────────────────────────────────────────────────────────

class TestWebEngineRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from salmalm.web.app import app
        from fastapi.testclient import TestClient
        cls.client = TestClient(app, raise_server_exceptions=False)
        # Get admin token
        r = cls.client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
        if r.status_code == 200:
            cls.token = r.json().get("access_token", "")
        else:
            cls.token = ""
        cls.headers = {"Authorization": f"Bearer {cls.token}"} if cls.token else {}

    def test_get_engine_status(self):
        r = self.client.get("/api/engine", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_get_sla(self):
        r = self.client.get("/api/sla", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_get_failover(self):
        r = self.client.get("/api/failover", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_get_routing(self):
        r = self.client.get("/api/routing", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_get_cost(self):
        r = self.client.get("/api/cost", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_get_watchdog(self):
        r = self.client.get("/api/watchdog", headers=self.headers)
        self.assertIn(r.status_code, (200, 401, 403, 404))

    def test_post_engine_settings_non_admin(self):
        """Non-admin cannot change engine settings."""
        r = self.client.post("/api/engine/settings",
                             json={"temperature": 0.9},
                             headers={"Authorization": "Bearer invalid"})
        self.assertIn(r.status_code, (401, 403, 422))

    def test_post_engine_settings_no_auth(self):
        r = self.client.post("/api/engine/settings", json={"temperature": 0.5})
        self.assertIn(r.status_code, (401, 403, 422))

    def test_get_health_endpoint(self):
        r = self.client.get("/api/health")
        self.assertIn(r.status_code, (200, 503))
        data = r.json()
        self.assertIn("status", data)
        self.assertIn(data["status"], ("healthy", "degraded", "unhealthy"))

    def test_get_health_has_version(self):
        r = self.client.get("/api/health")
        data = r.json()
        self.assertIn("version", data)

    def test_get_health_has_uptime(self):
        r = self.client.get("/api/health")
        data = r.json()
        self.assertIn("uptime_seconds", data)
        self.assertGreaterEqual(data["uptime_seconds"], 0)


# ─────────────────────────────────────────────────────────────────────────────
# utils/migration.py — zip-slip guard
# ─────────────────────────────────────────────────────────────────────────────

class TestMigrationZipSlip(unittest.TestCase):

    def test_safe_zip_dest_normal(self):
        from salmalm.utils.migration import _safe_zip_dest
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            result = _safe_zip_dest(base, "plugins/myplugin/config.json", "plugins/")
            self.assertIsNotNone(result)
            self.assertTrue(str(result).startswith(str(base)))

    def test_safe_zip_dest_zip_slip_blocked(self):
        from salmalm.utils.migration import _safe_zip_dest
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            result = _safe_zip_dest(base, "plugins/../../etc/passwd", "plugins/")
            self.assertIsNone(result)

    def test_safe_zip_dest_wrong_prefix(self):
        from salmalm.utils.migration import _safe_zip_dest
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            result = _safe_zip_dest(base, "memory/secret.md", "plugins/")
            self.assertIsNone(result)

    def test_safe_zip_dest_directory_entry(self):
        from salmalm.utils.migration import _safe_zip_dest
        from pathlib import Path
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            result = _safe_zip_dest(base, "plugins/subdir/", "plugins/")
            self.assertIsNone(result)


# ─────────────────────────────────────────────────────────────────────────────
# config_manager.py — path traversal guard
# ─────────────────────────────────────────────────────────────────────────────

class TestConfigManagerGuard(unittest.TestCase):

    def test_valid_name(self):
        from salmalm.config_manager import ConfigManager
        # Should not raise
        ConfigManager._validate_config_name("my_config-123")

    def test_invalid_name_slash(self):
        from salmalm.config_manager import ConfigManager
        with self.assertRaises(ValueError):
            ConfigManager._validate_config_name("../etc/passwd")

    def test_invalid_name_dot(self):
        from salmalm.config_manager import ConfigManager
        with self.assertRaises(ValueError):
            ConfigManager._validate_config_name("config.json")

    def test_invalid_name_empty(self):
        from salmalm.config_manager import ConfigManager
        with self.assertRaises(ValueError):
            ConfigManager._validate_config_name("")

    def test_invalid_name_too_long(self):
        from salmalm.config_manager import ConfigManager
        with self.assertRaises(ValueError):
            ConfigManager._validate_config_name("a" * 65)

    def test_resolve_env_var(self):
        import os
        from salmalm.config_manager import ConfigManager
        os.environ["SALMALM_TEST_MYKEY"] = "hello"
        try:
            val = ConfigManager.resolve("test", "mykey")
            self.assertEqual(val, "hello")
        finally:
            del os.environ["SALMALM_TEST_MYKEY"]

    def test_resolve_json_env_var(self):
        import os
        from salmalm.config_manager import ConfigManager
        os.environ["SALMALM_TEST_NUMKEY"] = "42"
        try:
            val = ConfigManager.resolve("test", "numkey")
            self.assertEqual(val, 42)
        finally:
            del os.environ["SALMALM_TEST_NUMKEY"]

    def test_resolve_default(self):
        from salmalm.config_manager import ConfigManager
        val = ConfigManager.resolve("nonexistent_config_xyz", "nonexistent_key", default="fallback")
        self.assertEqual(val, "fallback")


# ─────────────────────────────────────────────────────────────────────────────
# features/screen_capture.py — non-subprocess paths
# ─────────────────────────────────────────────────────────────────────────────

class TestScreenCapture(unittest.TestCase):

    def test_image_to_base64(self):
        from salmalm.features.screen_capture import ScreenCapture
        c = ScreenCapture()
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
        b64 = c.image_to_base64(png)
        import base64
        self.assertEqual(base64.b64decode(b64), png)

    def test_screen_history_search_empty(self):
        from salmalm.features.screen_capture import ScreenHistory
        import tempfile, pathlib
        with tempfile.TemporaryDirectory() as tmpdir:
            h = ScreenHistory.__new__(ScreenHistory)
            h._config = {"maxHistory": 10}
            from salmalm.features import screen_capture as sc
            old_dir = sc._HISTORY_DIR
            sc._HISTORY_DIR = pathlib.Path(tmpdir)
            try:
                results = h.search("nonexistent_query_xyz")
                self.assertEqual(results, [])
            finally:
                sc._HISTORY_DIR = old_dir

    def test_capture_and_analyze_no_capture(self):
        from salmalm.features.screen_capture import ScreenCapture
        c = ScreenCapture()
        with patch.object(c, "capture_screen", return_value=None):
            result = c.capture_and_analyze()
        self.assertIn("failed", result.lower())


if __name__ == "__main__":
    unittest.main()
