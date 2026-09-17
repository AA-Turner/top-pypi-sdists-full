#ifndef __Pyx_DEFINED_PyObject_CompareIntFloatBoolLt
#define __Pyx_DEFINED_PyObject_CompareIntFloatBoolLt
static int __Pyx_PyObject_CompareIntFloatBoolLt(PyObject *op1, PyObject *op2) {
    double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op2 == -1. && PyErr_Occurred())) return -1;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op1)) {
        Py_ssize_t iop1 = __Pyx_PyLong_CompactValue(op1);
        if (((double)iop1) < float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 < float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int sign1 = __Pyx_PyLong_Sign(op1);
        if (float_op2 >= 0.) {
            if (sign1 < 0) goto __pyx_return_true;
            if (float_op2 < (double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        } else {
            if (sign1 > 0) goto __pyx_return_false;
            if (float_op2 > -(double) (1L << PyLong_SHIFT)) goto __pyx_return_true;
        }
    }
    #else
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 < float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow1;
        long iop1 = PyLong_AsLongAndOverflow(op1, &overflow1);
        if (likely(!overflow1)) {
            if ((long long) iop1 >= (1LL << 53)) {
                overflow1 = 1;
            } else if ((long long) iop1 <= - (1LL << 53)) {
                overflow1 = -1;
            } else {
                if (((double) iop1) < float_op2) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow1 < 0) {
            if (float_op2 > ((double) (1LL << 53))) goto __pyx_return_true;
        } else {
            if (float_op2 < - ((double) (1LL << 53))) goto __pyx_return_false;
        }
    }
    #endif
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_LT);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#ifndef __Pyx_DEFINED_PyObject_CompareIntIntBoolLt
#define __Pyx_DEFINED_PyObject_CompareIntIntBoolLt
static int __Pyx_PyObject_CompareIntIntBoolLt(PyObject *op1, PyObject *op2) {
#if CYTHON_USE_PYLONG_INTERNALS
    Py_ssize_t cmp = __Pyx_PyLong_CompareSignAndSize(op1, op2);
    if (cmp == 0) {
        Py_ssize_t size = __Pyx_PyLong_DigitCount(op1);
        if (size > 0) {
            const digit* digits1 = __Pyx_PyLong_Digits(op1);
            const digit* digits2 = __Pyx_PyLong_Digits(op2);
            if (size == 1) {
                cmp = (Py_ssize_t) digits1[0] - (Py_ssize_t) digits2[0];
            } else if ((size == 2) && (8 * sizeof(Py_ssize_t) >= 2 * PyLong_SHIFT)) {
                cmp = (Py_ssize_t) (((((size_t)digits1[1]) << PyLong_SHIFT) | (size_t)digits1[0])) - (Py_ssize_t) (((((size_t)digits2[1]) << PyLong_SHIFT) | (size_t)digits2[0]));
            } else {
                for (Py_ssize_t i=size-1; i >= 0 && !cmp; --i) {
                    cmp = (Py_ssize_t) digits1[i] - (Py_ssize_t) digits2[i];
                }
            }
        }
        if (cmp == 0) goto __pyx_return_false;
        if (__Pyx_PyLong_IsNeg(op1)) cmp = -cmp;
    }
    if (cmp < 0) goto __pyx_return_true; else goto __pyx_return_false;
#else
    int overflow1, overflow2;
    long long iop1 = PyLong_AsLongLongAndOverflow(op1, &overflow1);
    long long iop2 = PyLong_AsLongLongAndOverflow(op2, &overflow2);
    if (likely(!(overflow1 | overflow2))) {
        if (iop1 < iop2) goto __pyx_return_true; else goto __pyx_return_false;
    } else if (overflow1 != overflow2) {
        if (overflow1 < overflow2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        return __Pyx_PyObject_RichCompareBool(op1, op2, Py_LT);
    }
#endif
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
static CYTHON_INLINE int __Pyx_PyObject_CompareBoolLt_int_object(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (unlikely(op1 == Py_None)) {
        goto __pyx_richcmp;
    }
    if (op1 == op2) goto __pyx_return_false;
    if (likely(op1 != Py_None)) {
        if (op1 == op2) goto __pyx_return_false;
        if (likely(PyLong_CheckExact(op2))) {
            return __Pyx_PyObject_CompareIntIntBoolLt(op1, op2);
        }
        if (PyFloat_CheckExact(op2)) {
            return __Pyx_PyObject_CompareIntFloatBoolLt(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if ((0)) goto __pyx_richcmp;
    if ((0)) goto __pyx_return_true;
    if ((0)) goto __pyx_return_false;
__pyx_richcmp:
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_LT);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}

