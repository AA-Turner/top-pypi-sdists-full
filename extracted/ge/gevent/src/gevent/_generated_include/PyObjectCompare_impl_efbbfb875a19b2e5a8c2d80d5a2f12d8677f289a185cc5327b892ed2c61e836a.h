#ifndef __Pyx_DEFINED_PyObject_CompareFloatIntBoolGe
#define __Pyx_DEFINED_PyObject_CompareFloatIntBoolGe
static int __Pyx_PyObject_CompareFloatIntBoolGe(PyObject *op1, PyObject *op2) {
    double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op1 == -1. && PyErr_Occurred())) return -1;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op2)) {
        Py_ssize_t iop2 = __Pyx_PyLong_CompactValue(op2);
        if (float_op1 >= ((double)iop2)) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op1))) {
        if (float_op1 >= 0.0) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int sign2 = __Pyx_PyLong_Sign(op2);
        if (float_op1 >= 0.) {
            if (sign2 < 0) goto __pyx_return_true;
            if (float_op1 < (double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        } else {
            if (sign2 > 0) goto __pyx_return_false;
            if (float_op1 > -(double) (1L << PyLong_SHIFT)) goto __pyx_return_true;
        }
    }
    #else
    if (unlikely(!isfinite(float_op1))) {
        if (float_op1 >= 0.0) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow2;
        long iop2 = PyLong_AsLongAndOverflow(op2, &overflow2);
        if (likely(!overflow2)) {
            if ((long long) iop2 >= (1LL << 53)) {
                overflow2 = 1;
            } else if ((long long) iop2 <= - (1LL << 53)) {
                overflow2 = -1;
            } else {
                if (float_op1 >= ((double) iop2)) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow2 > 0) {
            if (float_op1 < ((double) (1LL << 53))) goto __pyx_return_false;
        } else {
            if (float_op1 > - ((double) (1LL << 53))) goto __pyx_return_true;
        }
    }
    #endif
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_GE);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#ifndef __Pyx_DEFINED_PyObject_CompareIntIntBoolGe
#define __Pyx_DEFINED_PyObject_CompareIntIntBoolGe
static int __Pyx_PyObject_CompareIntIntBoolGe(PyObject *op1, PyObject *op2) {
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
        if (cmp == 0) goto __pyx_return_true;
        if (__Pyx_PyLong_IsNeg(op1)) cmp = -cmp;
    }
    if (cmp < 0) goto __pyx_return_false; else goto __pyx_return_true;
#else
    int overflow1, overflow2;
    long long iop1 = PyLong_AsLongLongAndOverflow(op1, &overflow1);
    long long iop2 = PyLong_AsLongLongAndOverflow(op2, &overflow2);
    if (likely(!(overflow1 | overflow2))) {
        if (iop1 >= iop2) goto __pyx_return_true; else goto __pyx_return_false;
    } else if (overflow1 != overflow2) {
        if (overflow1 >= overflow2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        return __Pyx_PyObject_RichCompareBool(op1, op2, Py_GE);
    }
#endif
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
static CYTHON_INLINE int __Pyx_PyObject_CompareBoolGe_object_int(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (unlikely(op2 == Py_None)) {
        goto __pyx_richcmp;
    }
    if (op1 == op2) goto __pyx_return_true;
    if (PyFloat_CheckExact(op1)) {
        if (likely(op2 != Py_None)) {
            return __Pyx_PyObject_CompareFloatIntBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if (likely(PyLong_CheckExact(op1))) {
        if (op1 == op2) goto __pyx_return_true;
        if (likely(op2 != Py_None)) {
            return __Pyx_PyObject_CompareIntIntBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if ((0)) goto __pyx_richcmp;
    if ((0)) goto __pyx_return_true;
    if ((0)) goto __pyx_return_false;
__pyx_richcmp:
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_GE);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}

