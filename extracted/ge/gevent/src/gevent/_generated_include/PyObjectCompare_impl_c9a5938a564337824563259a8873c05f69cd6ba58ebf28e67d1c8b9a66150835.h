#ifndef __Pyx_DEFINED_PyObject_CompareIntFloatBoolGt
#define __Pyx_DEFINED_PyObject_CompareIntFloatBoolGt
static int __Pyx_PyObject_CompareIntFloatBoolGt(PyObject *op1, PyObject *op2) {
    double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op2 == -1. && PyErr_Occurred())) return -1;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op1)) {
        Py_ssize_t iop1 = __Pyx_PyLong_CompactValue(op1);
        if (((double)iop1) > float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 > float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int sign1 = __Pyx_PyLong_Sign(op1);
        if (float_op2 >= 0.) {
            if (sign1 < 0) goto __pyx_return_false;
            if (float_op2 < (double) (1L << PyLong_SHIFT)) goto __pyx_return_true;
        } else {
            if (sign1 > 0) goto __pyx_return_true;
            if (float_op2 > -(double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        }
    }
    #else
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 > float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow1;
        long iop1 = PyLong_AsLongAndOverflow(op1, &overflow1);
        if (likely(!overflow1)) {
            if ((long long) iop1 >= (1LL << 53)) {
                overflow1 = 1;
            } else if ((long long) iop1 <= - (1LL << 53)) {
                overflow1 = -1;
            } else {
                if (((double) iop1) > float_op2) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow1 < 0) {
            if (float_op2 > ((double) (1LL << 53))) goto __pyx_return_false;
        } else {
            if (float_op2 < - ((double) (1LL << 53))) goto __pyx_return_true;
        }
    }
    #endif
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_GT);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
static CYTHON_INLINE int __Pyx_PyObject_CompareBoolGt_object_float(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (unlikely(op2 == Py_None)) {
        goto __pyx_richcmp;
    }
    if (likely(PyFloat_CheckExact(op1))) {
        if (likely(op2 != Py_None)) {
            double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op1 == -1. && PyErr_Occurred())) return -1;
            #endif
            double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op2 == -1. && PyErr_Occurred())) return -1;
            #endif
            if (float_op1 > float_op2) goto __pyx_return_true; else goto __pyx_return_false;
        }
        goto __pyx_richcmp;
    }
    if (PyLong_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_false;
        if (likely(op2 != Py_None)) {
            return __Pyx_PyObject_CompareIntFloatBoolGt(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if ((0)) goto __pyx_richcmp;
    if ((0)) goto __pyx_return_true;
    if ((0)) goto __pyx_return_false;
__pyx_richcmp:
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_GT);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}

