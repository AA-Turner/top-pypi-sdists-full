"""Tests for microsoft_demangle(), non_microsoft_demangle(),
get_arm64ec_insertion_point(), MSDF_* constants, and LLVM_VERSION.

No direct LLVM C++ unit test counterpart for most of these — the C++ tests
for Microsoft demangling live in a separate large corpus. These tests verify
the Python API contract and flag behavior.
"""

import pytest


class TestMicrosoftDemangle:
    """Tests for microsoft_demangle()."""

    def test_basic(self, llvm):
        result = llvm.microsoft_demangle("?foo@@YAHH@Z")
        assert result is not None
        name, n_read = result
        assert name == "int __cdecl foo(int)"
        assert n_read == 12

    def test_void_function(self, llvm):
        result = llvm.microsoft_demangle("?foo@@YAXH@Z")
        assert result is not None
        assert result[0] == "void __cdecl foo(int)"

    def test_invalid(self, llvm):
        assert llvm.microsoft_demangle("not_msvc") is None

    def test_invalid_itanium(self, llvm):
        assert llvm.microsoft_demangle("_Z3fooi") is None

    def test_flag_no_calling_convention(self, llvm):
        result = llvm.microsoft_demangle(
            "?foo@@YAHH@Z", flags=llvm.MSDF_NO_CALLING_CONVENTION)
        assert result is not None
        assert result[0] == "int foo(int)"

    def test_flag_no_return_type(self, llvm):
        result = llvm.microsoft_demangle(
            "?foo@@YAHH@Z", flags=llvm.MSDF_NO_RETURN_TYPE)
        assert result is not None
        assert "__cdecl" in result[0]
        assert not result[0].startswith("int")

    def test_flag_combined(self, llvm):
        flags = (llvm.MSDF_NO_CALLING_CONVENTION |
                 llvm.MSDF_NO_RETURN_TYPE)
        result = llvm.microsoft_demangle("?foo@@YAHH@Z", flags=flags)
        assert result is not None
        assert result[0] == "foo(int)"

    def test_n_read_matches_input_length(self, llvm):
        mangled = "?foo@@YAHH@Z"
        result = llvm.microsoft_demangle(mangled)
        assert result is not None
        assert result[1] == len(mangled)


class TestMSDFConstants:
    """Verify MSDF_* flag constants have correct values."""

    def test_msdf_none(self, llvm):
        assert llvm.MSDF_NONE == 0

    def test_msdf_dump_backrefs(self, llvm):
        assert llvm.MSDF_DUMP_BACKREFS == 1

    def test_msdf_no_access_specifier(self, llvm):
        assert llvm.MSDF_NO_ACCESS_SPECIFIER == 2

    def test_msdf_no_calling_convention(self, llvm):
        assert llvm.MSDF_NO_CALLING_CONVENTION == 4

    def test_msdf_no_return_type(self, llvm):
        assert llvm.MSDF_NO_RETURN_TYPE == 8

    def test_msdf_no_member_type(self, llvm):
        assert llvm.MSDF_NO_MEMBER_TYPE == 16

    def test_msdf_no_variable_type(self, llvm):
        assert llvm.MSDF_NO_VARIABLE_TYPE == 32


class TestNonMicrosoftDemangle:
    """Tests for non_microsoft_demangle()."""

    def test_itanium(self, llvm):
        if llvm.LLVM_VERSION < 14:
            pytest.skip("requires LLVM >= 14")
        assert llvm.non_microsoft_demangle("_Z3fooi") == "foo(int)"

    def test_rejects_microsoft(self, llvm):
        if llvm.LLVM_VERSION < 14:
            pytest.skip("requires LLVM >= 14")
        assert llvm.non_microsoft_demangle("?foo@@YAHH@Z") is None

    def test_invalid(self, llvm):
        if llvm.LLVM_VERSION < 14:
            pytest.skip("requires LLVM >= 14")
        assert llvm.non_microsoft_demangle("not_mangled") is None

    def test_raises_not_implemented(self, llvm):
        if llvm.LLVM_VERSION >= 14:
            pytest.skip("Only test on LLVM < 14")
        with pytest.raises(NotImplementedError):
            llvm.non_microsoft_demangle("_Z3fooi")


class TestGetArm64ECInsertionPoint:
    """Tests for get_arm64ec_insertion_point()."""

    def test_non_applicable(self, llvm):
        if llvm.LLVM_VERSION < 19:
            pytest.skip("requires LLVM >= 19")
        result = llvm.get_arm64ec_insertion_point("_Z3fooi")
        assert result is None

    def test_raises_not_implemented(self, llvm):
        if llvm.LLVM_VERSION >= 19:
            pytest.skip("Only test on LLVM < 19")
        with pytest.raises(NotImplementedError):
            llvm.get_arm64ec_insertion_point("_Z3fooi")


class TestLLVMVersion:
    """Tests for the LLVM_VERSION constant."""

    def test_is_int(self, llvm):
        assert isinstance(llvm.LLVM_VERSION, int)

    def test_in_range(self, llvm):
        assert 11 <= llvm.LLVM_VERSION <= 99
