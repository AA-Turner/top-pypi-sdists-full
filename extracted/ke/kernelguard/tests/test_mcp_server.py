import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import kernelguard
import kernelguard_mcp


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

LAST_CALL_REPLAY_KERNEL = """
_last_inputs = None
_last_versions = None
_last_output = None


def custom_kernel(data):
    global _last_inputs, _last_versions, _last_output
    cur_inputs = (data.data_ptr(),)
    cur_versions = (data._version,)
    if _last_inputs == cur_inputs and _last_versions == cur_versions:
        return _last_output
    out = data.clone()
    _last_inputs = cur_inputs
    _last_versions = cur_versions
    _last_output = out
    return out
"""


OBFUSCATED_EXEC_KERNEL = """
import codecs


def custom_kernel(payload):
    decoded = codecs.decode(payload, "rot_13")
    exec(decoded)
"""


UNSYNC_MULTISTREAM_KERNEL = """
import torch

s0 = torch.cuda.Stream()
s1 = torch.cuda.Stream()
s2 = torch.cuda.Stream()
s3 = torch.cuda.Stream()


def custom_kernel(data):
    with torch.cuda.stream(s0):
        pass
    with torch.cuda.stream(s1):
        pass
    with torch.cuda.stream(s2):
        pass
    with torch.cuda.stream(s3):
        pass
    return data
"""


PURE_SCALED_MM_KERNEL = """
import torch


def custom_kernel(data):
    a, b, sa, sb = data
    return torch._scaled_mm(a, b, sa, sb, bias=None, out_dtype=torch.float16)
"""

CLEAN_KERNEL = "def custom_kernel(data):\n    return data\n"


# ---------------------------------------------------------------------------
# Helpers — run tools through the FastMCP layer
# ---------------------------------------------------------------------------

def _get_server():
    return kernelguard_mcp.build_server()


def _run_tool(server, name: str, arguments: dict):
    """Call a tool through FastMCP internals with output validation."""
    tool = server._tool_manager.get_tool(name)
    assert tool is not None, f"missing MCP tool: {name}"
    content, structured = asyncio.run(tool.run(arguments, convert_result=True))
    return content, structured


# ---------------------------------------------------------------------------
# Direct function tests (kept for fast parity checks)
# ---------------------------------------------------------------------------

class DirectFunctionTests(unittest.TestCase):
    def test_analyze_code_tool_matches_kernelguard(self) -> None:
        expected = kernelguard.analyze_code(
            LAST_CALL_REPLAY_KERNEL,
            compute_structural_hash=False,
        )
        actual = kernelguard_mcp.analyze_code_tool(
            LAST_CALL_REPLAY_KERNEL,
            compute_structural_hash=False,
        )

        self.assertEqual(actual, expected)
        self.assertIn("LAST_CALL_REPLAY", {p["pattern"] for p in actual["matched_patterns"]})

    def test_analyze_code_tool_reports_obfuscated_exec(self) -> None:
        result = kernelguard_mcp.analyze_code_tool(
            OBFUSCATED_EXEC_KERNEL,
            compute_structural_hash=False,
        )

        self.assertIn("OBFUSCATED_EXEC", {p["pattern"] for p in result["matched_patterns"]})
        self.assertEqual(result["classification"], "hacked")
        self.assertTrue(result["should_filter"])

    def test_analyze_file_tool_matches_direct_analysis(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.py"
            path.write_text(CLEAN_KERNEL, encoding="utf-8")

            result = kernelguard_mcp.analyze_file_tool(str(path), compute_structural_hash=False)
            expected = kernelguard.analyze_code(
                path.read_text(encoding="utf-8"),
                compute_structural_hash=False,
            )

            self.assertEqual(result["classification"], expected["classification"])
            self.assertEqual(result["matched_patterns"], expected["matched_patterns"])
            self.assertEqual(result["should_filter"], expected["should_filter"])
            self.assertEqual(result["path"], str(path.resolve()))

    def test_analyze_file_tool_rejects_missing_path(self) -> None:
        with self.assertRaisesRegex(FileNotFoundError, "File does not exist"):
            kernelguard_mcp.analyze_file_tool("/tmp/definitely_missing_kernelguard_mcp.py")

    def test_analyze_code_tool_supports_strict_profile(self) -> None:
        default_result = kernelguard_mcp.analyze_code_tool(
            UNSYNC_MULTISTREAM_KERNEL,
            compute_structural_hash=False,
        )
        strict_result = kernelguard_mcp.analyze_code_tool(
            UNSYNC_MULTISTREAM_KERNEL,
            compute_structural_hash=False,
            profile="strict",
        )
        default_again = kernelguard_mcp.analyze_code_tool(
            UNSYNC_MULTISTREAM_KERNEL,
            compute_structural_hash=False,
        )

        self.assertEqual(default_result["classification"], "low_confidence")
        self.assertFalse(default_result["should_filter"])
        self.assertEqual(strict_result["classification"], "suspicious")
        self.assertFalse(strict_result["should_filter"])
        self.assertEqual(default_again["classification"], "low_confidence")

    def test_analyze_code_tool_strict_profile_promotes_default_reference_wrappers(self) -> None:
        default_result = kernelguard_mcp.analyze_code_tool(
            PURE_SCALED_MM_KERNEL,
            compute_structural_hash=False,
        )
        strict_result = kernelguard_mcp.analyze_code_tool(
            PURE_SCALED_MM_KERNEL,
            compute_structural_hash=False,
            profile="strict",
        )

        self.assertEqual(default_result["classification"], "low_confidence")
        self.assertEqual(strict_result["classification"], "low_confidence")
        self.assertFalse(strict_result["should_filter"])


# ---------------------------------------------------------------------------
# MCP layer tests — exercise FastMCP tool registration, validation, schemas
# ---------------------------------------------------------------------------

class MCPLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = _get_server()

    def _run(self, name: str, arguments: dict):
        return _run_tool(self.server, name, arguments)

    # -- Tool discovery --

    def test_server_registers_both_tools(self) -> None:
        self.assertIsNotNone(self.server._tool_manager.get_tool("analyze_code"))
        self.assertIsNotNone(self.server._tool_manager.get_tool("analyze_file"))

    def test_tool_descriptions_are_populated(self) -> None:
        for name in ("analyze_code", "analyze_file"):
            tool = self.server._tool_manager.get_tool(name)
            self.assertGreater(len(tool.description), 50, f"{name} description too short")

    def test_output_schema_has_expected_keys(self) -> None:
        tool = self.server._tool_manager.get_tool("analyze_code")
        props = tool.output_schema.get("properties", {})
        for key in ("matched_patterns", "classification", "should_filter", "filter_reason"):
            self.assertIn(key, props, f"missing output schema key: {key}")

    def test_file_output_schema_extends_code_schema(self) -> None:
        code_tool = self.server._tool_manager.get_tool("analyze_code")
        file_tool = self.server._tool_manager.get_tool("analyze_file")
        code_props = set(code_tool.output_schema.get("properties", {}))
        file_props = set(file_tool.output_schema.get("properties", {}))
        self.assertTrue(code_props.issubset(file_props))
        self.assertIn("path", file_props)

    # -- Output validation through MCP layer --

    def test_clean_kernel_passes_output_validation(self) -> None:
        _content, structured = self._run("analyze_code", {"code": CLEAN_KERNEL})
        self.assertEqual(structured["classification"], "valid")
        self.assertFalse(structured["should_filter"])
        self.assertIsNone(structured["filter_reason"])
        self.assertIsNone(structured["default_reason"])

    def test_hacked_kernel_passes_output_validation(self) -> None:
        _content, structured = self._run("analyze_code", {"code": LAST_CALL_REPLAY_KERNEL})
        self.assertEqual(structured["classification"], "hacked")
        self.assertTrue(structured["should_filter"])
        self.assertIn("LAST_CALL_REPLAY", {p["pattern"] for p in structured["matched_patterns"]})

    def test_obfuscated_kernel_passes_output_validation(self) -> None:
        _content, structured = self._run("analyze_code", {"code": OBFUSCATED_EXEC_KERNEL})
        self.assertEqual(structured["classification"], "hacked")
        self.assertTrue(structured["should_filter"])

    def test_analyze_file_passes_output_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.py"
            path.write_text(CLEAN_KERNEL, encoding="utf-8")

            _content, structured = self._run("analyze_file", {"path": str(path)})
            self.assertEqual(structured["classification"], "valid")
            self.assertEqual(structured["path"], str(path.resolve()))

    # -- Error surfaces through MCP layer --

    def test_missing_file_raises_tool_error(self) -> None:
        from mcp.server.fastmcp.exceptions import ToolError

        with self.assertRaises(ToolError):
            self._run("analyze_file", {"path": "/tmp/definitely_missing_kernelguard_mcp.py"})

    def test_profile_roundtrip_through_mcp_layer(self) -> None:
        _content, default = self._run("analyze_code", {
            "code": UNSYNC_MULTISTREAM_KERNEL,
        })
        _content, strict = self._run("analyze_code", {
            "code": UNSYNC_MULTISTREAM_KERNEL,
            "profile": "strict",
        })
        _content, default_again = self._run("analyze_code", {
            "code": UNSYNC_MULTISTREAM_KERNEL,
        })

        self.assertEqual(default["classification"], "low_confidence")
        self.assertEqual(strict["classification"], "suspicious")
        self.assertEqual(default_again["classification"], "low_confidence")

    # -- Pattern match schema --

    def test_pattern_match_has_expected_fields(self) -> None:
        _content, structured = self._run("analyze_code", {"code": LAST_CALL_REPLAY_KERNEL})
        self.assertGreater(len(structured["matched_patterns"]), 0)
        match = structured["matched_patterns"][0]
        for key in ("pattern", "severity", "evidence", "field"):
            self.assertIn(key, match, f"missing pattern match key: {key}")


# ---------------------------------------------------------------------------
# CLI / packaging tests
# ---------------------------------------------------------------------------

class CLITests(unittest.TestCase):
    def test_version_flag(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            kernelguard_mcp.main(["--version"])
        self.assertEqual(ctx.exception.code, 0)

    def test_build_server_dependency_error_is_friendly(self) -> None:
        with mock.patch.object(kernelguard_mcp, "FastMCP", None):
            with mock.patch.object(kernelguard_mcp, "_MCP_IMPORT_ERROR", ImportError("missing mcp")):
                with self.assertRaisesRegex(RuntimeError, r'kernelguard\[mcp\]'):
                    kernelguard_mcp.build_server()


if __name__ == "__main__":
    unittest.main()
