"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/RustDemangleTest.cpp

Tests the rust_demangle() function.
"""

import pytest


class TestRustDemangle:
    """Ported from TEST(RustDemangle, Success) and TEST(RustDemangle, Invalid)."""

    def test_success(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("_RNvC1a4main") == "a::main"

    def test_invalid_prefix(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("_ABCDEF") is None

    def test_correct_prefix_but_invalid(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("_RRR") is None

    def test_crate_function(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("_RNvC8my_crate3foo") == "my_crate::foo"

    def test_not_rust(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("_Z3fooi") is None

    def test_plain_string(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.rust_demangle("not_rust") is None


class TestRustDemangleVersionGuard:
    """Verify NotImplementedError on old LLVM versions."""

    def test_raises_not_implemented(self, llvm):
        if llvm.LLVM_VERSION >= 13:
            pytest.skip("Only test on LLVM < 13")
        with pytest.raises(NotImplementedError):
            llvm.rust_demangle("_RNvC1a4main")
