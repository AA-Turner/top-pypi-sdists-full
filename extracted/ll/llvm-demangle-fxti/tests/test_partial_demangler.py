"""Tests ported from LLVM 21.1.0 llvm/unittests/Demangle/PartialDemangleTest.cpp

Tests the ItaniumPartialDemangler class and itanium_demangle() function.
"""

import pytest


# ---------------------------------------------------------------------------
# From PartialDemangleTest.cpp: NamesToTest[] (TestNameChopping)
# Each entry: (mangled, context, base_name, return_type, params)
# ---------------------------------------------------------------------------
NAME_CHOPPING_DATA = [
    ("_Z1fv", "", "f", "", "()"),
    ("_ZN1a1b1cIiiiEEvm", "a::b", "c", "void", "(unsigned long)"),
    ("_ZZ5OuterIiEivEN5Inner12inner_memberEv",
     "int Outer<int>()::Inner", "inner_member", "", "()"),
    ("_Z1fIiEPFvvEv", "", "f", "void (*)()", "()"),
    ("_ZN1S1fIiEEvv", "S", "f", "void", "()"),
    # Call operator for a lambda in f().
    ("_ZZ1fvENK3$_0clEi", "f()::$_0", "operator()", "", "(int)"),
    # A call operator for a lambda in a lambda in f().
    ("_ZZZ1fvENK3$_0clEvENKUlvE_clEv",
     "f()::$_0::operator()() const::'lambda'()", "operator()", "", "()"),
    ("_ZZN1S1fEiiEd0_NKUlvE_clEv",
     "S::f(int, int)::'lambda'()", "operator()", "", "()"),
    ("_ZN1Scv7MuncherIJDpPT_EEIJFivEA_iEEEv",
     "S", "operator Muncher<int (*)(), int (*) []>", "", "()"),
    # Attributes.
    ("_ZN5test4IdE1fEUa9enable_ifIXeqfL0p_Li1EEXeqfL0p0_Li2EEEi",
     "test4<double>", "f", "", "(int)"),
    ("_ZN1SC2B8ctor_tagEv", "S", "S", "", "()"),
    ("_ZN1S1fB4MERPIiEEvv", "S", "f", "void", "()"),
    # _ZNSsC1EmcRKSaIcE: context differs between LLVM < 15 and >= 15
    # ("> >" vs ">>"). Handled in test_name_chopping() below.
    ("_ZNSsC1EmcRKSaIcE",
     "std::basic_string<char, std::char_traits<char>, std::allocator<char>>",
     "basic_string", "",
     "(unsigned long, char, std::allocator<char> const&)"),
    ("_ZNSsixEm", "std::string", "operator[]", "", "(unsigned long)"),
    ("_ZSt17__throw_bad_allocv", "std", "__throw_bad_alloc", "", "()"),
    ("_ZN1AI1BEC2Ev", "A<B>", "A", "", "()"),
    ("_ZN1AI1BED2Ev", "A<B>", "~A", "", "()"),
    ("_ZN1AI1BECI24BaseEi", "A<B>", "A", "", "(int)"),
    ("_ZNKR1AI1BE1fIiEEiv", "A<B>", "f", "int", "()"),
    ("_ZN1SIJicfEE3mfnIJjcdEEEvicfDpT_",
     "S<int, char, float>", "mfn", "void",
     "(int, char, float, unsigned int, char, double)"),
    # Fixed-point types (LLVM >= 20 only)
]

FIXED_POINT_DATA = [
    ("_Z1fDAs", "", "f", "", "(short _Accum)"),
    ("_Z1fDAt", "", "f", "", "(unsigned short _Accum)"),
    ("_Z1fDAi", "", "f", "", "(_Accum)"),
    ("_Z1fDAj", "", "f", "", "(unsigned _Accum)"),
    ("_Z1fDAl", "", "f", "", "(long _Accum)"),
    ("_Z1fDAm", "", "f", "", "(unsigned long _Accum)"),
    ("_Z1fDRs", "", "f", "", "(short _Fract)"),
    ("_Z1fDRt", "", "f", "", "(unsigned short _Fract)"),
    ("_Z1fDRi", "", "f", "", "(_Fract)"),
    ("_Z1fDRj", "", "f", "", "(unsigned _Fract)"),
    ("_Z1fDRl", "", "f", "", "(long _Fract)"),
    ("_Z1fDRm", "", "f", "", "(unsigned long _Fract)"),
    ("_Z1fDSDAs", "", "f", "", "(_Sat short _Accum)"),
    ("_Z1fDSDAt", "", "f", "", "(_Sat unsigned short _Accum)"),
    ("_Z1fDSDAi", "", "f", "", "(_Sat _Accum)"),
    ("_Z1fDSDAj", "", "f", "", "(_Sat unsigned _Accum)"),
    ("_Z1fDSDAl", "", "f", "", "(_Sat long _Accum)"),
    ("_Z1fDSDAm", "", "f", "", "(_Sat unsigned long _Accum)"),
    ("_Z1fDSDRs", "", "f", "", "(_Sat short _Fract)"),
    ("_Z1fDSDRt", "", "f", "", "(_Sat unsigned short _Fract)"),
    ("_Z1fDSDRi", "", "f", "", "(_Sat _Fract)"),
    ("_Z1fDSDRj", "", "f", "", "(_Sat unsigned _Fract)"),
    ("_Z1fDSDRl", "", "f", "", "(_Sat long _Fract)"),
    ("_Z1fDSDRm", "", "f", "", "(_Sat unsigned long _Fract)"),
]


class TestPartialDemangleNameChopping:
    """Ported from TEST(PartialDemanglerTest, TestNameChopping)."""

    @pytest.mark.parametrize(
        "mangled,context,base_name,return_type,params",
        NAME_CHOPPING_DATA,
        ids=[t[0] for t in NAME_CHOPPING_DATA],
    )
    def test_name_chopping(self, llvm, mangled, context, base_name, return_type, params):
        d = llvm.ItaniumPartialDemangler(mangled)
        assert d.is_function is True
        assert d.is_data is False
        assert d.is_special_name is False
        # LLVM < 15 outputs "> >" instead of ">>" for nested templates
        if mangled == "_ZNSsC1EmcRKSaIcE" and llvm.LLVM_VERSION < 15:
            context = context.replace(">>", "> >")
        assert d.function_decl_context == context
        assert d.function_base_name == base_name
        assert d.function_return_type == return_type
        assert d.function_parameters == params

    @pytest.mark.parametrize(
        "mangled,context,base_name,return_type,params",
        FIXED_POINT_DATA,
        ids=[t[0] for t in FIXED_POINT_DATA],
    )
    def test_name_chopping_fixed_point(self, llvm, mangled, context, base_name, return_type, params):
        if llvm.LLVM_VERSION < 20:
            pytest.skip("Fixed-point types require LLVM >= 20")
        d = llvm.ItaniumPartialDemangler(mangled)
        assert d.is_function is True
        assert d.is_data is False
        assert d.is_special_name is False
        assert d.function_decl_context == context
        assert d.function_base_name == base_name
        assert d.function_return_type == return_type
        assert d.function_parameters == params


class TestPartialDemangleNameMeta:
    """Ported from TEST(PartialDemanglerTest, TestNameMeta)."""

    def test_const_member_function(self, llvm):
        d = llvm.ItaniumPartialDemangler("_ZNK1f1gEv")
        assert d.is_function is True
        assert d.has_function_qualifiers is True
        assert d.is_special_name is False
        assert d.is_data is False

    def test_no_qualifiers(self, llvm):
        d = llvm.ItaniumPartialDemangler("_Z1fv")
        assert d.has_function_qualifiers is False

    def test_vtable_special_name(self, llvm):
        d = llvm.ItaniumPartialDemangler("_ZTV1S")
        assert d.is_special_name is True
        assert d.is_data is False
        assert d.is_function is False

    def test_structured_binding_data(self, llvm):
        d = llvm.ItaniumPartialDemangler("_ZN1aDC1a1b1cEE")
        assert d.is_function is False
        assert d.is_special_name is False
        assert d.is_data is True


class TestPartialDemangleCtorOrDtor:
    """Ported from TEST(PartialDemanglerTest, TestCtorOrDtor)."""

    @pytest.mark.parametrize("mangled", [
        "_ZN1AC1Ev",         # A::A()
        "_ZN1AC1IiEET_",     # A::A<int>(int)
        "_ZN1AD2Ev",         # A::~A()
        "_ZN1BIiEC1IcEET_",  # B<int>::B<char>(char)
        "_ZN1AC1B1TEv",      # A::A[abi:T]()
        "_ZNSt1AD2Ev",       # std::A::~A()
        "_ZN2ns1AD1Ev",      # ns::A::~A()
    ])
    def test_is_ctor_or_dtor(self, llvm, mangled):
        d = llvm.ItaniumPartialDemangler(mangled)
        assert d.is_ctor_or_dtor is True

    @pytest.mark.parametrize("mangled", [
        "_Z1fv",
        "_ZN1A1gIiEEvT_",  # void A::g<int>(int)
    ])
    def test_is_not_ctor_or_dtor(self, llvm, mangled):
        d = llvm.ItaniumPartialDemangler(mangled)
        assert d.is_ctor_or_dtor is False


class TestPartialDemangleMisc:
    """Ported from TEST(PartialDemanglerTest, TestMisc)."""

    def test_invalid_mangling(self, llvm):
        with pytest.raises(ValueError):
            llvm.ItaniumPartialDemangler("Not a mangled name!")

    def test_different_symbols(self, llvm):
        """Verify parsing different symbols produces correct results."""
        d1 = llvm.ItaniumPartialDemangler("_Z1fv")
        assert d1.is_function is True
        d2 = llvm.ItaniumPartialDemangler("_Z1g")
        assert d2.is_function is False  # _Z1g is data, not a function

    def test_data_not_function(self, llvm):
        d = llvm.ItaniumPartialDemangler("_Z1g")
        assert d.is_function is False
        assert d.function_name is None


class TestPartialDemanglePrintCases:
    """Ported from TEST(PartialDemanglerTest, TestPrintCases)."""

    def test_short_context_name(self, llvm):
        d = llvm.ItaniumPartialDemangler("_ZN1a1bEv")
        assert d.function_decl_context == "a"

    def test_full_demangle(self, llvm):
        d = llvm.ItaniumPartialDemangler("_ZN1a1b1cIiiiEEvm")
        assert d.full_name == "void a::b::c<int, int, int>(unsigned long)"

    def test_non_function_returns_none(self, llvm):
        """a::c is data, not a function -- function_name should be None."""
        d = llvm.ItaniumPartialDemangler("_ZN1a1cE")
        assert d.function_name is None


class TestItaniumDemangle:
    """Tests for the itanium_demangle() function."""

    def test_basic(self, llvm):
        assert llvm.itanium_demangle("_Z3fooi") == "foo(int)"

    def test_invalid(self, llvm):
        assert llvm.itanium_demangle("not_itanium") is None

    def test_namespace(self, llvm):
        assert llvm.itanium_demangle("_ZN3Foo3barEid") == \
            "Foo::bar(int, double)"

    def test_template(self, llvm):
        assert llvm.itanium_demangle("_ZN3Foo3barIiEEvi") == \
            "void Foo::bar<int>(int)"

    def test_parse_params_false(self, llvm):
        if llvm.LLVM_VERSION < 18:
            pytest.skip("parse_params requires LLVM >= 18")
        assert llvm.itanium_demangle("_Z3fooi", parse_params=False) == "foo"

    def test_parse_params_true(self, llvm):
        if llvm.LLVM_VERSION < 18:
            pytest.skip("parse_params requires LLVM >= 18")
        assert llvm.itanium_demangle("_Z3fooi", parse_params=True) == "foo(int)"
