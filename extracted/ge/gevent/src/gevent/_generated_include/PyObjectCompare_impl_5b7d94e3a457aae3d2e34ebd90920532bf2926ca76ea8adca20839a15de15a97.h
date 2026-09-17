#ifndef __Pyx_DEFINED_PyObject_CompareStrStrBoolGe
#define __Pyx_DEFINED_PyObject_CompareStrStrBoolGe
static CYTHON_INLINE int __Pyx_PyObject_CompareStrStrBoolGe(PyObject* s1, PyObject* s2) {
    int result = PyUnicode_Compare(s1, s2);
    if (unlikely((result == -1) && PyErr_Occurred())) return -1;
    if (result >= 0) goto __pyx_return_true; else goto __pyx_return_false;
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyBytesPyBytesBoolGe
#define __Pyx_DEFINED_PyObject_ComparePyBytesPyBytesBoolGe
static CYTHON_INLINE int __Pyx_PyObject_ComparePyBytesPyBytesBoolGe(PyObject* s1, PyObject* s2) {
    Py_ssize_t cmp;
    Py_ssize_t length1, length2, short_length;
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    length1 = __Pyx_PyBytes_GET_SIZE(s1);
    length2 = __Pyx_PyBytes_GET_SIZE(s2);
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    ps1 = PyBytes_AS_STRING(s1);
    ps2 = PyBytes_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    if (unlikely(PyBytes_AsStringAndSize(s1, &ps1, &length1) == -1)) return -1;
    if (unlikely(PyBytes_AsStringAndSize(s2, &ps2, &length2) == -1)) return -1;
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    #endif
    cmp = (Py_ssize_t) ((const unsigned char*) ps1)[0] - (Py_ssize_t) ((const unsigned char*) ps2)[0];
    if (cmp == 0 && short_length > 1) {
        cmp = memcmp(ps1, ps2, (size_t)short_length);
    }
    if (cmp == 0) cmp = (length1 - length2);
    if (cmp >= 0) goto __pyx_return_true; else goto __pyx_return_false;
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyBytesPyByteArrayBoolGe
#define __Pyx_DEFINED_PyObject_ComparePyBytesPyByteArrayBoolGe
static CYTHON_INLINE int __Pyx_PyObject_ComparePyBytesPyByteArrayBoolGe(PyObject* s1, PyObject* s2) {
    Py_ssize_t cmp;
    Py_ssize_t length1, length2, short_length;
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    length1 = __Pyx_PyBytes_GET_SIZE(s1);
    length2 = __Pyx_PyByteArray_GET_SIZE(s2);
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    ps1 = PyBytes_AS_STRING(s1);
    ps2 = PyByteArray_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    if (unlikely(PyBytes_AsStringAndSize(s1, &ps1, &length1) == -1)) return -1;
    ps2 = __Pyx_PyByteArray_AsString(s2); if (unlikely(!ps2)) return -1;
    length2 = __Pyx_PyByteArray_GET_SIZE(s2); if (unlikely(length2 == -1)) return -1;
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    #endif
    cmp = (Py_ssize_t) ((const unsigned char*) ps1)[0] - (Py_ssize_t) ((const unsigned char*) ps2)[0];
    if (cmp == 0 && short_length > 1) {
        cmp = memcmp(ps1, ps2, (size_t)short_length);
    }
    if (cmp == 0) cmp = (length1 - length2);
    if (cmp >= 0) goto __pyx_return_true; else goto __pyx_return_false;
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyByteArrayPyBytesBoolGe
#define __Pyx_DEFINED_PyObject_ComparePyByteArrayPyBytesBoolGe
static CYTHON_INLINE int __Pyx_PyObject_ComparePyByteArrayPyBytesBoolGe(PyObject* s1, PyObject* s2) {
    Py_ssize_t cmp;
    Py_ssize_t length1, length2, short_length;
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    length1 = __Pyx_PyByteArray_GET_SIZE(s1);
    length2 = __Pyx_PyBytes_GET_SIZE(s2);
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    ps1 = PyByteArray_AS_STRING(s1);
    ps2 = PyBytes_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    ps1 = __Pyx_PyByteArray_AsString(s1); if (unlikely(!ps1)) return -1;
    length1 = __Pyx_PyByteArray_GET_SIZE(s1); if (unlikely(length1 == -1)) return -1;
    if (unlikely(PyBytes_AsStringAndSize(s2, &ps2, &length2) == -1)) return -1;
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    #endif
    cmp = (Py_ssize_t) ((const unsigned char*) ps1)[0] - (Py_ssize_t) ((const unsigned char*) ps2)[0];
    if (cmp == 0 && short_length > 1) {
        cmp = memcmp(ps1, ps2, (size_t)short_length);
    }
    if (cmp == 0) cmp = (length1 - length2);
    if (cmp >= 0) goto __pyx_return_true; else goto __pyx_return_false;
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyByteArrayPyByteArrayBoolGe
#define __Pyx_DEFINED_PyObject_ComparePyByteArrayPyByteArrayBoolGe
static CYTHON_INLINE int __Pyx_PyObject_ComparePyByteArrayPyByteArrayBoolGe(PyObject* s1, PyObject* s2) {
    Py_ssize_t cmp;
    Py_ssize_t length1, length2, short_length;
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    length1 = __Pyx_PyByteArray_GET_SIZE(s1);
    length2 = __Pyx_PyByteArray_GET_SIZE(s2);
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    ps1 = PyByteArray_AS_STRING(s1);
    ps2 = PyByteArray_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    ps1 = __Pyx_PyByteArray_AsString(s1); if (unlikely(!ps1)) return -1;
    length1 = __Pyx_PyByteArray_GET_SIZE(s1); if (unlikely(length1 == -1)) return -1;
    ps2 = __Pyx_PyByteArray_AsString(s2); if (unlikely(!ps2)) return -1;
    length2 = __Pyx_PyByteArray_GET_SIZE(s2); if (unlikely(length2 == -1)) return -1;
    short_length = (length1 < length2) ? length1 : length2;
    if (short_length == 0) {
        if (length1 == 0) goto __pyx_return_false; else goto __pyx_return_true;
    }
    #endif
    cmp = (Py_ssize_t) ((const unsigned char*) ps1)[0] - (Py_ssize_t) ((const unsigned char*) ps2)[0];
    if (cmp == 0 && short_length > 1) {
        cmp = memcmp(ps1, ps2, (size_t)short_length);
    }
    if (cmp == 0) cmp = (length1 - length2);
    if (cmp >= 0) goto __pyx_return_true; else goto __pyx_return_false;
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
#endif
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
#ifndef __Pyx_DEFINED_PyObject_CompareIntFloatBoolGe
#define __Pyx_DEFINED_PyObject_CompareIntFloatBoolGe
static int __Pyx_PyObject_CompareIntFloatBoolGe(PyObject *op1, PyObject *op2) {
    double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op2 == -1. && PyErr_Occurred())) return -1;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op1)) {
        Py_ssize_t iop1 = __Pyx_PyLong_CompactValue(op1);
        if (((double)iop1) >= float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 >= float_op2) goto __pyx_return_true; else goto __pyx_return_false;
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
        if (0.0 >= float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow1;
        long iop1 = PyLong_AsLongAndOverflow(op1, &overflow1);
        if (likely(!overflow1)) {
            if ((long long) iop1 >= (1LL << 53)) {
                overflow1 = 1;
            } else if ((long long) iop1 <= - (1LL << 53)) {
                overflow1 = -1;
            } else {
                if (((double) iop1) >= float_op2) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow1 < 0) {
            if (float_op2 > ((double) (1LL << 53))) goto __pyx_return_false;
        } else {
            if (float_op2 < - ((double) (1LL << 53))) goto __pyx_return_true;
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
static CYTHON_INLINE int __Pyx_PyObject_CompareBoolGe_object_object(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (PyFloat_CheckExact(op1)) {
        if (PyFloat_CheckExact(op2)) {
            double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op1 == -1. && PyErr_Occurred())) return -1;
            #endif
            double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op2 == -1. && PyErr_Occurred())) return -1;
            #endif
            if (float_op1 >= float_op2) goto __pyx_return_true; else goto __pyx_return_false;
        }
        if (PyLong_CheckExact(op2)) {
            return __Pyx_PyObject_CompareFloatIntBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if (PyLong_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyLong_CheckExact(op2)) {
            return __Pyx_PyObject_CompareIntIntBoolGe(op1, op2);
        }
        if (PyFloat_CheckExact(op2)) {
            return __Pyx_PyObject_CompareIntFloatBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    
    if (PyUnicode_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyUnicode_CheckExact(op2)) {
            return __Pyx_PyObject_CompareStrStrBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    
    #if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
    if (PyBytes_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyBytes_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyBytesPyBytesBoolGe(op1, op2);
        }
        if (PyByteArray_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyBytesPyByteArrayBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    #endif
    #if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
    if (PyByteArray_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyByteArray_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyByteArrayPyByteArrayBoolGe(op1, op2);
        }
        if (PyBytes_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyByteArrayPyBytesBoolGe(op1, op2);
        }
        goto __pyx_richcmp;
    }
    #endif
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

