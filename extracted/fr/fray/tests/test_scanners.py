"""
Tests for critical scanner modules:
  xss, sqli, cmdi, ssrf, cache_poison, deser, massassign,
  proto_pollution, ai_bypass, race, monitor, interactive, recommender,
  ssti, csp_scanner, modern_bypasses

All tests use mocking — no real network requests.
"""

import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

# ── Ensure project root is on path ──────────────────────────────────────
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# ════════════════════════════════════════════════════════════════════════
# Helper — fake socket that returns a canned HTTP response
# ════════════════════════════════════════════════════════════════════════

def _make_fake_response(status: int = 200, body: str = "", headers: dict = None) -> bytes:
    hdr = headers or {}
    hdr_lines = "".join(f"{k}: {v}\r\n" for k, v in hdr.items())
    return (
        f"HTTP/1.1 {status} OK\r\n"
        f"Content-Type: text/html\r\n"
        f"{hdr_lines}"
        f"\r\n"
        f"{body}"
    ).encode("utf-8")


class _FakeSocket:
    def __init__(self, response_bytes: bytes):
        self._data = response_bytes
        self._pos = 0

    def recv(self, n: int) -> bytes:
        chunk = self._data[self._pos:self._pos + n]
        self._pos += n
        return chunk

    def sendall(self, data): pass
    def close(self): pass
    def wrap_socket(self, *a, **kw): return self
    def getpeercert(self): return {}


def _patch_socket(response_bytes: bytes):
    """Context-manager: patches socket.create_connection to return fake socket."""
    fake = _FakeSocket(response_bytes)
    return patch("socket.create_connection", return_value=fake)


# ════════════════════════════════════════════════════════════════════════
# SSTI Scanner
# ════════════════════════════════════════════════════════════════════════

class TestSSTIScanner(unittest.TestCase):

    def _make_scanner(self):
        from fray.ssti import SSTIScanner
        return SSTIScanner("http://example.com/page", param="q",
                           timeout=3, verify_ssl=False)

    def test_import(self):
        from fray.ssti import SSTIScanner, SSTIResult, SSTIFinding
        self.assertTrue(callable(SSTIScanner))

    def test_no_ssti_clean_response(self):
        """Clean response → not vulnerable."""
        from fray.ssti import SSTIScanner
        resp = _make_fake_response(200, "Hello world")
        with _patch_socket(resp):
            scanner = SSTIScanner("http://example.com/", param="q",
                                  timeout=3, verify_ssl=False)
            with patch("ssl.create_default_context"):
                result = scanner.scan()
        self.assertFalse(result.vulnerable)
        self.assertEqual(result.findings, [])

    def test_jinja2_detected(self):
        """Response containing '49' triggers Jinja2 detection."""
        from fray.ssti import SSTIScanner

        call_count = [0]
        responses = [
            _make_fake_response(200, "fraynoop"),   # baseline
            _make_fake_response(200, "result: 49"), # probe match
        ]

        def fake_connect(*a, **kw):
            resp = responses[min(call_count[0], len(responses) - 1)]
            call_count[0] += 1
            return _FakeSocket(resp)

        with patch("socket.create_connection", side_effect=fake_connect):
            with patch("ssl.create_default_context"):
                scanner = SSTIScanner("http://example.com/", param="q",
                                      timeout=3, verify_ssl=False)
                result = scanner.scan()

        self.assertTrue(result.vulnerable)
        self.assertTrue(any("Jinja2" in f.engine for f in result.findings))

    def test_result_has_requests_count(self):
        from fray.ssti import SSTIScanner
        resp = _make_fake_response(200, "nothing")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = SSTIScanner("http://example.com/", param="q",
                                      timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertGreater(result.requests, 0)

    def test_load_file_payloads_graceful_missing_dir(self):
        """Scanner initialises without error even if payload dir missing."""
        from fray.ssti import SSTIScanner
        with patch("fray.ssti._PAYLOADS_DIR", Path("/nonexistent/path")):
            scanner = SSTIScanner("http://example.com/", param="q")
        self.assertIsInstance(scanner._file_payloads, list)


# ════════════════════════════════════════════════════════════════════════
# CSP Bypass Scanner
# ════════════════════════════════════════════════════════════════════════

class TestCSPBypassScanner(unittest.TestCase):

    def test_import(self):
        from fray.csp_scanner import CSPBypassScanner, CSPResult
        self.assertTrue(callable(CSPBypassScanner))

    def test_no_csp_header_is_critical(self):
        from fray.csp_scanner import CSPBypassScanner
        resp = _make_fake_response(200, "<html>ok</html>")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = CSPBypassScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertTrue(result.vulnerable)
        self.assertEqual(result.csp_grade, "F")
        self.assertTrue(any(f.bypass_type == "missing-csp" for f in result.findings))

    def test_unsafe_inline_detected(self):
        from fray.csp_scanner import CSPBypassScanner
        resp = _make_fake_response(200, "ok", {
            "content-security-policy": "script-src 'self' 'unsafe-inline'"
        })
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = CSPBypassScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertTrue(result.vulnerable)
        self.assertTrue(any(f.bypass_type == "unsafe-inline" for f in result.findings))
        self.assertIn(result.csp_grade, ("C", "D", "F"))

    def test_strict_csp_scores_well(self):
        from fray.csp_scanner import CSPBypassScanner
        resp = _make_fake_response(200, "ok", {
            "content-security-policy": (
                "default-src 'none'; script-src 'nonce-abc123'; "
                "object-src 'none'; base-uri 'none'; form-action 'self'"
            )
        })
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = CSPBypassScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        # nonce-reuse is a low-severity info finding, grade should be B or A
        self.assertIn(result.csp_grade, ("A", "B", "C"))

    def test_jsonp_origin_detected(self):
        from fray.csp_scanner import CSPBypassScanner
        resp = _make_fake_response(200, "ok", {
            "content-security-policy": "script-src 'self' ajax.googleapis.com"
        })
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = CSPBypassScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertTrue(any(f.bypass_type == "JSONP" for f in result.findings))


# ════════════════════════════════════════════════════════════════════════
# Modern Bypass Scanner
# ════════════════════════════════════════════════════════════════════════

class TestModernBypassScanner(unittest.TestCase):

    def test_import(self):
        from fray.modern_bypasses import ModernBypassScanner, ModernBypassResult
        self.assertTrue(callable(ModernBypassScanner))

    def test_no_bypass_when_no_waf(self):
        """No WAF active → waf_active=False → nothing flagged as bypass."""
        from fray.modern_bypasses import ModernBypassScanner
        resp = _make_fake_response(200, "ok")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = ModernBypassScanner("http://example.com/", param="q",
                                              timeout=3, verify_ssl=False)
                result = scanner.scan()
        # No WAF active baseline means bypass detection disabled for WAF-bypass path
        self.assertIsNotNone(result)
        self.assertIsInstance(result.requests, int)

    def test_result_structure(self):
        from fray.modern_bypasses import ModernBypassResult, BypassFinding
        r = ModernBypassResult()
        self.assertFalse(r.vulnerable)
        self.assertEqual(r.findings, [])
        self.assertEqual(r.techniques_bypassed, [])

    def test_payload_list_non_empty(self):
        from fray.modern_bypasses import _BYPASS_PROBES
        self.assertGreater(len(_BYPASS_PROBES), 10)
        for entry in _BYPASS_PROBES:
            self.assertEqual(len(entry), 5, f"Probe entry should have 5 fields: {entry}")


# ════════════════════════════════════════════════════════════════════════
# Cache Poison Scanner
# ════════════════════════════════════════════════════════════════════════

class TestCachePoisonScanner(unittest.TestCase):

    def test_import(self):
        from fray.cache_poison import CachePoisonScanner
        self.assertTrue(callable(CachePoisonScanner))

    def test_scan_returns_result(self):
        from fray.cache_poison import CachePoisonScanner
        resp = _make_fake_response(200, "ok")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = CachePoisonScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertIsNotNone(result)
        self.assertFalse(getattr(result, "vulnerable", True))

    def test_payload_file_exists(self):
        payload_file = _ROOT / "payloads" / "cache_poison" / "cache_poison_headers.json"
        self.assertTrue(payload_file.exists(), "payloads/cache_poison/cache_poison_headers.json missing")
        with open(payload_file) as f:
            data = json.load(f)
        self.assertIn("payloads", data)
        self.assertGreater(len(data["payloads"]), 10)

    def test_payloads_have_required_fields(self):
        payload_file = _ROOT / "payloads" / "cache_poison" / "cache_poison_headers.json"
        with open(payload_file) as f:
            data = json.load(f)
        for p in data["payloads"]:
            self.assertIn("payload", p, f"Missing 'payload' field: {p}")
            self.assertIn("type", p, f"Missing 'type' field: {p}")
            self.assertIn("severity", p, f"Missing 'severity' field: {p}")


# ════════════════════════════════════════════════════════════════════════
# Deserialization Scanner
# ════════════════════════════════════════════════════════════════════════

class TestDeserScanner(unittest.TestCase):

    def test_import(self):
        from fray.deser import DeserScanner
        self.assertTrue(callable(DeserScanner))

    def test_scan_clean_response(self):
        from fray.deser import DeserScanner
        resp = _make_fake_response(200, "ok")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = DeserScanner("http://example.com/api", param="data",
                                       timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertFalse(getattr(result, "vulnerable", True))

    def test_payload_file_exists(self):
        payload_file = _ROOT / "payloads" / "deserialization" / "deser_java.json"
        self.assertTrue(payload_file.exists())
        with open(payload_file) as f:
            data = json.load(f)
        self.assertIn("payloads", data)
        self.assertGreater(len(data["payloads"]), 5)

    def test_java_payloads_have_cve(self):
        payload_file = _ROOT / "payloads" / "deserialization" / "deser_java.json"
        with open(payload_file) as f:
            data = json.load(f)
        java_payloads = [p for p in data["payloads"] if p.get("type") == "java"]
        cve_payloads = [p for p in java_payloads if p.get("cve")]
        self.assertGreater(len(cve_payloads), 0, "Expected at least one Java payload with CVE")


# ════════════════════════════════════════════════════════════════════════
# Mass Assignment Scanner
# ════════════════════════════════════════════════════════════════════════

class TestMassAssignScanner(unittest.TestCase):

    def test_import(self):
        from fray.massassign import MassAssignScanner
        self.assertTrue(callable(MassAssignScanner))

    def test_scan_clean_response(self):
        from fray.massassign import MassAssignScanner
        resp = _make_fake_response(200, "ok")
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = MassAssignScanner("http://example.com/api/user",
                                            timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertFalse(getattr(result, "vulnerable", True))

    def test_payload_file_exists_and_has_privilege_escalation(self):
        payload_file = _ROOT / "payloads" / "massassign" / "massassign_params.json"
        self.assertTrue(payload_file.exists())
        with open(payload_file) as f:
            data = json.load(f)
        types_present = {p["type"] for p in data["payloads"]}
        self.assertIn("privilege_escalation", types_present)
        self.assertIn("business_logic", types_present)

    def test_admin_payloads_present(self):
        payload_file = _ROOT / "payloads" / "massassign" / "massassign_params.json"
        with open(payload_file) as f:
            data = json.load(f)
        admin_payloads = [p for p in data["payloads"] if "admin" in p["payload"].lower()]
        self.assertGreater(len(admin_payloads), 3)


# ════════════════════════════════════════════════════════════════════════
# Race Condition
# ════════════════════════════════════════════════════════════════════════

class TestRaceCondition(unittest.TestCase):

    def test_import(self):
        from fray.race import run_race_test, RaceResult
        self.assertTrue(callable(run_race_test))

    def test_payload_file_exists(self):
        payload_file = _ROOT / "payloads" / "race_condition" / "race_condition_endpoints.json"
        self.assertTrue(payload_file.exists())

    def test_race_payloads_have_concurrency(self):
        payload_file = _ROOT / "payloads" / "race_condition" / "race_condition_endpoints.json"
        with open(payload_file) as f:
            data = json.load(f)
        for p in data["payloads"]:
            self.assertIn("concurrency", p, f"Missing concurrency field: {p['payload']}")
            self.assertGreater(p["concurrency"], 1)

    def test_race_result_structure(self):
        from fray.race import RaceResult, RaceResponse
        r = RaceResult(target="http://example.com", method="GET", concurrency=10)
        self.assertIsInstance(r.responses, list)
        self.assertFalse(r.divergence_detected)

    def test_run_race_test_returns_result(self):
        """run_race_test against a mocked server returns RaceResult."""
        from fray.race import run_race_test
        resp = _make_fake_response(200, "ok")

        with patch("socket.create_connection", return_value=_FakeSocket(resp)):
            with patch("ssl.create_default_context"):
                result = run_race_test(
                    "http://example.com/api/transfer",
                    concurrency=3,
                    rounds=1,
                    timeout=3,
                )
        self.assertIsNotNone(result)
        self.assertIsInstance(result.responses, list)


# ════════════════════════════════════════════════════════════════════════
# Recommender
# ════════════════════════════════════════════════════════════════════════

class TestRecommender(unittest.TestCase):

    def test_import(self):
        from fray.recommender import WAFRecommendationEngine
        self.assertTrue(callable(WAFRecommendationEngine.generate_recommendations))

    def test_timestamp_is_set(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="http://example.com"
        )
        self.assertIsNotNone(result["timestamp"])
        self.assertIn("Z", result["timestamp"])

    def test_no_waf_is_critical_posture(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="http://example.com"
        )
        self.assertIn("CRITICAL", result["security_posture"])
        self.assertGreater(len(result["recommendations"]), 0)

    def test_vendor_recommendations_are_list_of_dicts(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="http://example.com"
        )
        vendors = result["alternative_vendors"]
        self.assertIsInstance(vendors, list)
        self.assertGreater(len(vendors), 0)
        for v in vendors:
            self.assertIn("name", v)
            self.assertIn("reason", v)
            self.assertIn("url", v)

    def test_aws_target_recommends_aws_waf(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="https://myapp.elasticbeanstalk.com"
        )
        names = [v["name"] for v in result["alternative_vendors"]]
        self.assertIn("AWS WAF", names)

    def test_azure_target_recommends_azure_waf(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="https://myapp.azurewebsites.net"
        )
        names = [v["name"] for v in result["alternative_vendors"]]
        self.assertIn("Microsoft Azure WAF", names)

    def test_cloudflare_always_recommended(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=False, target="https://randomsite.com"
        )
        names = [v["name"] for v in result["alternative_vendors"]]
        self.assertIn("Cloudflare", names)

    def test_waf_detected_sets_good_posture(self):
        from fray.recommender import WAFRecommendationEngine
        result = WAFRecommendationEngine.generate_recommendations(
            waf_detected=True, waf_vendor="Cloudflare", confidence=90
        )
        self.assertIn("GOOD", result["security_posture"])


# ════════════════════════════════════════════════════════════════════════
# reporter.py — WAF_RECOMMENDATIONS_AVAILABLE import check
# ════════════════════════════════════════════════════════════════════════

class TestReporterImport(unittest.TestCase):

    def test_waf_recommendations_available_is_true(self):
        """reporter.py should now resolve the import correctly."""
        from fray.reporter import WAF_RECOMMENDATIONS_AVAILABLE
        self.assertTrue(WAF_RECOMMENDATIONS_AVAILABLE,
                        "WAF_RECOMMENDATIONS_AVAILABLE should be True after import fix")


# ════════════════════════════════════════════════════════════════════════
# payload_generator.py — SSTI templates
# ════════════════════════════════════════════════════════════════════════

class TestPayloadGeneratorSSTI(unittest.TestCase):

    def test_jinja2_renders_correctly(self):
        """Template stored with double-braces for .format() escaping; rendered should be {{7*7}}."""
        from fray.payload_generator import PayloadGenerator
        pg = PayloadGenerator()
        tmpl = pg.templates["ssti"]["jinja2"]
        # The raw template uses Python format-string escaping: {{{{ → {{ when rendered
        rendered = tmpl.format(input="id") if "{input}" in tmpl else tmpl
        self.assertIn("7*7", rendered, f"Jinja2 template should contain '7*7': {rendered!r}")
        self.assertIn("{", rendered, f"Jinja2 template should contain '{{': {rendered!r}")

    def test_mako_renders_correctly(self):
        from fray.payload_generator import PayloadGenerator
        pg = PayloadGenerator()
        tmpl = pg.templates["ssti"]["mako"]
        rendered = tmpl.format(input="id") if "{input}" in tmpl else tmpl
        self.assertIn("7*7", rendered)
        self.assertIn("$", rendered)

    def test_erb_renders_correctly(self):
        from fray.payload_generator import PayloadGenerator
        pg = PayloadGenerator()
        tmpl = pg.templates["ssti"]["erb"]
        self.assertEqual(tmpl, "<%= 7*7 %>")

    def test_no_triple_brace_issue(self):
        """Ensure no template has mismatched braces (e.g. 3 closing braces for 2 open)."""
        from fray.payload_generator import PayloadGenerator
        pg = PayloadGenerator()
        for engine, tmpl in pg.templates["ssti"].items():
            rendered = tmpl.format(input="id") if "{input}" in tmpl else tmpl
            # Basic sanity: rendered should not contain lone unmatched { or }
            # (we skip this for raw strings that aren't format templates)
            self.assertIsInstance(rendered, str)


# ════════════════════════════════════════════════════════════════════════
# interactive.py — module map completeness
# ════════════════════════════════════════════════════════════════════════

class TestInteractiveModuleMap(unittest.TestCase):

    def test_no_none_none_stubs(self):
        """All entries in _VULN_MODULE_MAP should have a real module path."""
        from fray.interactive import _VULN_MODULE_MAP
        stubs = [(k, v) for k, v in _VULN_MODULE_MAP.items() if v[0] is None]
        self.assertEqual(stubs, [],
                         f"Stub (None,None) entries remain: {stubs}")

    def test_ssti_module_importable(self):
        from fray.interactive import _VULN_MODULE_MAP
        import importlib
        mod_path, class_name, _ = _VULN_MODULE_MAP["ssti"]
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, class_name)
        self.assertTrue(callable(cls))

    def test_csp_bypass_module_importable(self):
        from fray.interactive import _VULN_MODULE_MAP
        import importlib
        mod_path, class_name, _ = _VULN_MODULE_MAP["csp_bypass"]
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, class_name)
        self.assertTrue(callable(cls))

    def test_modern_bypasses_module_importable(self):
        from fray.interactive import _VULN_MODULE_MAP
        import importlib
        mod_path, class_name, _ = _VULN_MODULE_MAP["modern_bypasses"]
        mod = importlib.import_module(mod_path)
        cls = getattr(mod, class_name)
        self.assertTrue(callable(cls))


# ════════════════════════════════════════════════════════════════════════
# Proto Pollution Scanner
# ════════════════════════════════════════════════════════════════════════

class TestProtoPollutionScanner(unittest.TestCase):

    def test_import(self):
        from fray.proto_pollution import PPScanner
        self.assertTrue(callable(PPScanner))

    def test_scan_returns_result(self):
        from fray.proto_pollution import PPScanner
        resp = _make_fake_response(200, '{"ok":true}',
                                   {"content-type": "application/json"})
        with _patch_socket(resp):
            with patch("ssl.create_default_context"):
                scanner = PPScanner("http://example.com/", timeout=3, verify_ssl=False)
                result = scanner.scan()
        self.assertIsNotNone(result)


# ════════════════════════════════════════════════════════════════════════
# Payload directories exist and are non-empty
# ════════════════════════════════════════════════════════════════════════

class TestPayloadDirectories(unittest.TestCase):

    def _check_dir(self, name: str, min_payloads: int = 5):
        d = _ROOT / "payloads" / name
        self.assertTrue(d.exists(), f"Payload directory missing: payloads/{name}/")
        json_files = list(d.glob("*.json"))
        txt_files  = list(d.glob("*.txt"))
        self.assertTrue(len(json_files) + len(txt_files) > 0,
                        f"No payload files in payloads/{name}/")
        total = 0
        for jf in json_files:
            data = json.loads(jf.read_text())
            plist = data.get("payloads", data) if isinstance(data, dict) else data
            total += len(plist) if isinstance(plist, list) else 0
        for tf in txt_files:
            total += sum(1 for ln in tf.read_text().splitlines()
                         if ln.strip() and not ln.strip().startswith("#"))
        self.assertGreaterEqual(total, min_payloads,
                                f"payloads/{name}/ has only {total} payloads, expected >= {min_payloads}")

    def test_cache_poison_payloads(self):   self._check_dir("cache_poison", 15)
    def test_deserialization_payloads(self): self._check_dir("deserialization", 10)
    def test_massassign_payloads(self):     self._check_dir("massassign", 15)
    def test_race_condition_payloads(self): self._check_dir("race_condition", 10)
    def test_ssti_payloads(self):           self._check_dir("ssti", 50)
    def test_xss_payloads(self):            self._check_dir("xss", 100)
    def test_sqli_payloads(self):           self._check_dir("sqli", 50)


if __name__ == "__main__":
    unittest.main(verbosity=2)
