"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/DemangleTest.cpp

Tests the top-level demangle() function which auto-detects the mangling scheme.
"""

import pytest


class TestDemangle:
    """Ported from TEST(Demangle, demangleTest)."""

    def test_underscore(self, llvm):
        assert llvm.demangle("_") == "_"

    def test_itanium_basic(self, llvm):
        assert llvm.demangle("_Z3fooi") == "foo(int)"

    def test_itanium_double_underscore(self, llvm):
        assert llvm.demangle("__Z3fooi") == "foo(int)"

    def test_itanium_block_invoke_triple_underscore(self, llvm):
        assert llvm.demangle("___Z3fooi_block_invoke") == \
            "invocation function for block in foo(int)"

    def test_itanium_block_invoke_quad_underscore(self, llvm):
        assert llvm.demangle("____Z3fooi_block_invoke") == \
            "invocation function for block in foo(int)"

    def test_microsoft(self, llvm):
        assert llvm.demangle("?foo@@YAXH@Z") == "void __cdecl foo(int)"

    def test_plain_name(self, llvm):
        assert llvm.demangle("foo") == "foo"

    def test_rust(self, llvm):
        if llvm.LLVM_VERSION < 13:
            pytest.skip("rust_demangle requires LLVM >= 13")
        assert llvm.demangle("_RNvC3foo3bar") == "foo::bar"

    def test_rust_double_underscore(self, llvm):
        if llvm.LLVM_VERSION < 15:
            pytest.skip("__R prefix for Rust requires LLVM >= 15")
        assert llvm.demangle("__RNvC3foo3bar") == "foo::bar"

    def test_dlang(self, llvm):
        if llvm.LLVM_VERSION < 14:
            pytest.skip("dlang_demangle requires LLVM >= 14")
        assert llvm.demangle("_Dmain") == "D main"

    def test_vendor_extended_type_qualifier(self, llvm):
        """Regression test for https://bugs.llvm.org/show_bug.cgi?id=48009"""
        if llvm.LLVM_VERSION < 13:
            pytest.skip("_ExtInt demangling requires LLVM >= 13")
        assert llvm.demangle("_Z3fooILi79EEbU7_ExtIntIXT_EEi") == \
            "bool foo<79>(int _ExtInt<79>)"


class TestLlvmDemangleCompat:
    """Test backward-compatible llvm_demangle() alias."""

    def test_alias(self, llvm):
        assert llvm.llvm_demangle("_Z3fooi") == "foo(int)"

    def test_alias_matches_demangle(self, llvm):
        name = "_ZN3Foo3barEid"
        assert llvm.llvm_demangle(name) == llvm.demangle(name)
