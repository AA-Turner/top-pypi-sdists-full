"""Tests for `_diagnose_llama_cpp_failure` — better error messages for
fix-llama-cpp.

Originally `sage fix-llama-cpp` failed with a generic "Rebuild failed. See
pip output above" hint, which is not actionable when the user is trying
to diagnose what broke. The diagnostic helper scans the captured pip /
cmake / ninja output for known error patterns and returns one or more
specific recovery hints.
"""

from __future__ import annotations

import pytest


class TestDiagnoseFailure:
    """`_diagnose_llama_cpp_failure(output: str) -> list[str]` should match
    known error patterns and return a list of actionable hint strings."""

    def test_returns_empty_for_unknown_output(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        # Random output that doesn't match any known pattern → empty list,
        # the caller falls back to the generic message.
        hints = _diagnose_llama_cpp_failure("nothing interesting here")
        assert hints == []

    def test_detects_ninja_build_stopped(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = (
            "      ninja: build stopped: subcommand failed.\n"
            "                  *** CMake build failed\n"
            "      [end of output]\n"
            "  ERROR: Failed building wheel for llama-cpp-python\n"
        )
        hints = _diagnose_llama_cpp_failure(output)
        # The combined ninja+CMake signature is the user's actual case.
        joined = " ".join(hints).lower()
        assert any(kw in joined for kw in ("xcode", "cmake", "compiler", "toolchain"))

    def test_detects_missing_xcode_clt(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = "xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools)"
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "xcode-select" in joined or "command line tools" in joined

    def test_detects_missing_cmake(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = "CMake Error: CMake was unable to find a build program"
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "cmake" in joined or "ninja" in joined

    def test_detects_missing_cuda(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = "No CMAKE_CUDA_COMPILER could be found."
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "cuda" in joined

    def test_detects_externally_managed_env(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = (
            "error: externally-managed-environment\n"
            "× This environment is externally managed\n"
        )
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "pipx" in joined or "venv" in joined or "break-system-packages" in joined

    def test_detects_metal_compilation_failure(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = "metal_library_compilation_failed: see logs above"
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "metal" in joined

    def test_detects_missing_compiler(self):
        from sage.cli_core import _diagnose_llama_cpp_failure
        output = "CMake Error: No CMAKE_C_COMPILER could be found."
        hints = _diagnose_llama_cpp_failure(output)
        joined = " ".join(hints).lower()
        assert "compiler" in joined or "xcode" in joined or "clang" in joined


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
