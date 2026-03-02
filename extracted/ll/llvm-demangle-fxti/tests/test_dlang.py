"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/DLangDemangleTest.cpp

Tests the dlang_demangle() function.
"""

import pytest

# From DLangDemangleTest.cpp: INSTANTIATE_TEST_SUITE_P values
# Each entry: (mangled, expected)  — expected=None means demangling should fail
DLANG_TEST_DATA = [
    ("_Dmain", "D main"),
    ("_Z", None),
    ("_DDD", None),
    ("_D88", None),
    ("_D8demangleZ", "demangle"),
    ("_D8demangle4testZ", "demangle.test"),
    ("_D8demangle4test5test2Z", "demangle.test.test2"),
    ("_D8demangle4test0Z", "demangle.test"),
    ("_D8demangle4test03fooZ", "demangle.test.foo"),
    ("_D8demangle4test6__initZ", "initializer for demangle.test"),
    ("_D8demangle4test6__vtblZ", "vtable for demangle.test"),
    ("_D8demangle4test7__ClassZ", "ClassInfo for demangle.test"),
    ("_D8demangle4test11__InterfaceZ", "Interface for demangle.test"),
    ("_D8demangle4test12__ModuleInfoZ", "ModuleInfo for demangle.test"),
    ("_D8demangle4__S14testZ", "demangle.test"),
    ("_D8demangle4__Sd4testZ", "demangle.__Sd.test"),
    ("_D8demangle3fooi", "demangle.foo"),
    # Symbol without a type sequence.
    ("_D8demangle3foo", None),
    # Invalid type sequence.
    ("_D8demangle3fooinvalidtypeseq", None),
    # Symbol back reference: `Qe` is a back reference for position 5.
    ("_D8demangle3ABCQe1ai", "demangle.ABC.ABC.a"),
    # Invalid symbol back reference (recursive).
    ("_D8demangle3ABCQa1ai", None),
    # Overflow back reference position.
    ("_D8demangleQDXXXXXXXXXXXXx", None),
    # Type back reference: `Qd` is a back reference for position 4.
    ("_D8demangle4ABCi1aQd", "demangle.ABCi.a"),
    # Invalid type back reference position.
    ("_D8demangle3fooQXXXx", None),
    # Invalid type back reference (recursive).
    ("_D8demangle5recurQa", None),
]


class TestDlangDemangle:
    """Ported from DLangDemangleTestFixture."""

    @pytest.mark.parametrize(
        "mangled,expected",
        DLANG_TEST_DATA,
        ids=[t[0] for t in DLANG_TEST_DATA],
    )
    def test_dlang_demangle(self, llvm, mangled, expected):
        if llvm.LLVM_VERSION < 14:
            pytest.skip("dlang_demangle requires LLVM >= 14")
        result = llvm.dlang_demangle(mangled)
        assert result == expected


class TestDlangDemangleVersionGuard:
    """Verify NotImplementedError on old LLVM versions."""

    def test_raises_not_implemented(self, llvm):
        if llvm.LLVM_VERSION >= 14:
            pytest.skip("Only test on LLVM < 14")
        with pytest.raises(NotImplementedError):
            llvm.dlang_demangle("_Dmain")
