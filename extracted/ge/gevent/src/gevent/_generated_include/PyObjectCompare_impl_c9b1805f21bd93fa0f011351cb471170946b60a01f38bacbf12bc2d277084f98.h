#ifndef __Pyx_DEFINED_PyObject_CompareStrStrEq
#define __Pyx_DEFINED_PyObject_CompareStrStrEq
static CYTHON_INLINE PyObject* __Pyx_PyObject_CompareStrStrEq(PyObject* s1, PyObject* s2) {
    #if __PYX_LIMITED_VERSION_HEX >= 0x030e0000
    int result = PyUnicode_Equal(s1, s2);
    #if !CYTHON_COMPILING_IN_CPYTHON
    if (unlikely(result == -1)) return NULL;
    #endif
    if (result == 0) goto __pyx_return_false; else goto __pyx_return_true;
    #else
    int result = PyUnicode_Compare(s1, s2);
    if (unlikely((result == -1) && PyErr_Occurred())) return NULL;
    if (result == 0) goto __pyx_return_true; else goto __pyx_return_false;
    #endif
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyBytesPyBytesEq
#define __Pyx_DEFINED_PyObject_ComparePyBytesPyBytesEq
static CYTHON_INLINE PyObject* __Pyx_PyObject_ComparePyBytesPyBytesEq(PyObject* s1, PyObject* s2) {
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    Py_ssize_t length = PyBytes_GET_SIZE(s1);
    if (length != PyBytes_GET_SIZE(s2)) goto __pyx_return_false;
    ps1 = PyBytes_AS_STRING(s1);
    ps2 = PyBytes_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    Py_ssize_t length, length2;
    if (unlikely(PyBytes_AsStringAndSize(s1, &ps1, &length) == -1)) return NULL;
    if (unlikely(PyBytes_AsStringAndSize(s2, &ps2, &length2) == -1)) return NULL;
    if (length != length2) goto __pyx_return_false;
    #endif
    if (ps1[0] != ps2[0]) goto __pyx_return_false;
    if (length == 1) goto __pyx_return_true;
    {
        int cmp;
#if CYTHON_USE_UNICODE_INTERNALS && (PY_VERSION_HEX < 0x030B0000)
        Py_hash_t hash1 = ((PyBytesObject*)s1)->ob_shash;
        Py_hash_t hash2 = ((PyBytesObject*)s2)->ob_shash;
        if (hash1 != hash2 && hash1 != -1 && hash2 != -1) goto __pyx_return_false;
#endif
        cmp = memcmp(ps1, ps2, (size_t)length);
        if (cmp == 0) goto __pyx_return_true; else goto __pyx_return_false;
    }
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyBytesPyByteArrayEq
#define __Pyx_DEFINED_PyObject_ComparePyBytesPyByteArrayEq
static CYTHON_INLINE PyObject* __Pyx_PyObject_ComparePyBytesPyByteArrayEq(PyObject* s1, PyObject* s2) {
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    Py_ssize_t length = PyBytes_GET_SIZE(s1);
    if (length != PyByteArray_GET_SIZE(s2)) goto __pyx_return_false;
    ps1 = PyBytes_AS_STRING(s1);
    ps2 = PyByteArray_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    Py_ssize_t length, length2;
    if (unlikely(PyBytes_AsStringAndSize(s1, &ps1, &length) == -1)) return NULL;
    ps2 = __Pyx_PyByteArray_AsString(s2); if (unlikely(!ps2)) return NULL;
    length2 = __Pyx_PyByteArray_GET_SIZE(s2); if (unlikely(length2 == -1)) return NULL;
    if (length != length2) goto __pyx_return_false;
    #endif
    if (ps1[0] != ps2[0]) goto __pyx_return_false;
    if (length == 1) goto __pyx_return_true;
    {
        int cmp;
        cmp = memcmp(ps1, ps2, (size_t)length);
        if (cmp == 0) goto __pyx_return_true; else goto __pyx_return_false;
    }
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyByteArrayPyBytesEq
#define __Pyx_DEFINED_PyObject_ComparePyByteArrayPyBytesEq
static CYTHON_INLINE PyObject* __Pyx_PyObject_ComparePyByteArrayPyBytesEq(PyObject* s1, PyObject* s2) {
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    Py_ssize_t length = PyByteArray_GET_SIZE(s1);
    if (length != PyBytes_GET_SIZE(s2)) goto __pyx_return_false;
    ps1 = PyByteArray_AS_STRING(s1);
    ps2 = PyBytes_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    Py_ssize_t length, length2;
    ps1 = __Pyx_PyByteArray_AsString(s1); if (unlikely(!ps1)) return NULL;
    length = __Pyx_PyByteArray_GET_SIZE(s1); if (unlikely(length == -1)) return NULL;
    if (unlikely(PyBytes_AsStringAndSize(s2, &ps2, &length2) == -1)) return NULL;
    if (length != length2) goto __pyx_return_false;
    #endif
    if (length == 0) goto __pyx_return_true;
    if (ps1[0] != ps2[0]) goto __pyx_return_false;
    if (length == 1) goto __pyx_return_true;
    {
        int cmp;
        cmp = memcmp(ps1, ps2, (size_t)length);
        if (cmp == 0) goto __pyx_return_true; else goto __pyx_return_false;
    }
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#endif
#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
#ifndef __Pyx_DEFINED_PyObject_ComparePyByteArrayPyByteArrayEq
#define __Pyx_DEFINED_PyObject_ComparePyByteArrayPyByteArrayEq
static CYTHON_INLINE PyObject* __Pyx_PyObject_ComparePyByteArrayPyByteArrayEq(PyObject* s1, PyObject* s2) {
    #if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS
    const char *ps1, *ps2;
    Py_ssize_t length = PyByteArray_GET_SIZE(s1);
    if (length != PyByteArray_GET_SIZE(s2)) goto __pyx_return_false;
    ps1 = PyByteArray_AS_STRING(s1);
    ps2 = PyByteArray_AS_STRING(s2);
    #else
    char *ps1, *ps2;
    Py_ssize_t length, length2;
    ps1 = __Pyx_PyByteArray_AsString(s1); if (unlikely(!ps1)) return NULL;
    length = __Pyx_PyByteArray_GET_SIZE(s1); if (unlikely(length == -1)) return NULL;
    ps2 = __Pyx_PyByteArray_AsString(s2); if (unlikely(!ps2)) return NULL;
    length2 = __Pyx_PyByteArray_GET_SIZE(s2); if (unlikely(length2 == -1)) return NULL;
    if (length != length2) goto __pyx_return_false;
    #endif
    if (length == 0) goto __pyx_return_true;
    if (ps1[0] != ps2[0]) goto __pyx_return_false;
    if (length == 1) goto __pyx_return_true;
    {
        int cmp;
        cmp = memcmp(ps1, ps2, (size_t)length);
        if (cmp == 0) goto __pyx_return_true; else goto __pyx_return_false;
    }
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#endif
#ifndef __Pyx_DEFINED_PyObject_CompareFloatIntEq
#define __Pyx_DEFINED_PyObject_CompareFloatIntEq
static PyObject* __Pyx_PyObject_CompareFloatIntEq(PyObject *op1, PyObject *op2) {
    double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op1 == -1. && PyErr_Occurred())) return NULL;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op2)) {
        Py_ssize_t iop2 = __Pyx_PyLong_CompactValue(op2);
        if (float_op1 == ((double)iop2)) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op1))) {
        if (float_op1 == 0.0) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int sign2 = __Pyx_PyLong_Sign(op2);
        if (float_op1 >= 0.) {
            if (sign2 < 0) goto __pyx_return_false;
            if (float_op1 < (double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        } else {
            if (sign2 > 0) goto __pyx_return_false;
            if (float_op1 > -(double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        }
    }
    #else
    if (unlikely(!isfinite(float_op1))) {
        if (float_op1 == 0.0) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow2;
        long iop2 = PyLong_AsLongAndOverflow(op2, &overflow2);
        if (likely(!overflow2)) {
            if ((long long) iop2 >= (1LL << 53)) {
                overflow2 = 1;
            } else if ((long long) iop2 <= - (1LL << 53)) {
                overflow2 = -1;
            } else {
                if (float_op1 == ((double) iop2)) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow2 > 0) {
            if (float_op1 < ((double) (1LL << 53))) goto __pyx_return_false;
        } else {
            if (float_op1 > - ((double) (1LL << 53))) goto __pyx_return_false;
        }
    }
    #endif
    return PyObject_RichCompare(op1, op2, Py_EQ);
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#ifndef __Pyx_DEFINED_PyObject_CompareIntFloatEq
#define __Pyx_DEFINED_PyObject_CompareIntFloatEq
static PyObject* __Pyx_PyObject_CompareIntFloatEq(PyObject *op1, PyObject *op2) {
    double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(float_op2 == -1. && PyErr_Occurred())) return NULL;
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsCompact(op1)) {
        Py_ssize_t iop1 = __Pyx_PyLong_CompactValue(op1);
        if (((double)iop1) == float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    }
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 == float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int sign1 = __Pyx_PyLong_Sign(op1);
        if (float_op2 >= 0.) {
            if (sign1 < 0) goto __pyx_return_false;
            if (float_op2 < (double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        } else {
            if (sign1 > 0) goto __pyx_return_false;
            if (float_op2 > -(double) (1L << PyLong_SHIFT)) goto __pyx_return_false;
        }
    }
    #else
    if (unlikely(!isfinite(float_op2))) {
        if (0.0 == float_op2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        int overflow1;
        long iop1 = PyLong_AsLongAndOverflow(op1, &overflow1);
        if (likely(!overflow1)) {
            if ((long long) iop1 >= (1LL << 53)) {
                overflow1 = 1;
            } else if ((long long) iop1 <= - (1LL << 53)) {
                overflow1 = -1;
            } else {
                if (((double) iop1) == float_op2) goto __pyx_return_true; else goto __pyx_return_false;
            }
        }
        if (overflow1 < 0) {
            if (float_op2 > ((double) (1LL << 53))) goto __pyx_return_false;
        } else {
            if (float_op2 < - ((double) (1LL << 53))) goto __pyx_return_false;
        }
    }
    #endif
    return PyObject_RichCompare(op1, op2, Py_EQ);
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
#ifndef __Pyx_DEFINED_PyObject_CompareIntIntEq
#define __Pyx_DEFINED_PyObject_CompareIntIntEq
static PyObject* __Pyx_PyObject_CompareIntIntEq(PyObject *op1, PyObject *op2) {
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
    goto __pyx_return_false;
#else
    int overflow1, overflow2;
    long long iop1 = PyLong_AsLongLongAndOverflow(op1, &overflow1);
    long long iop2 = PyLong_AsLongLongAndOverflow(op2, &overflow2);
    if (likely(!(overflow1 | overflow2))) {
        if (iop1 == iop2) goto __pyx_return_true; else goto __pyx_return_false;
    } else if (overflow1 != overflow2) {
        if (overflow1 == overflow2) goto __pyx_return_true; else goto __pyx_return_false;
    } else {
        return PyObject_RichCompare(op1, op2, Py_EQ);
    }
#endif
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}
#endif
static CYTHON_INLINE PyObject* __Pyx_PyObject_CompareEq_object_object(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (PyFloat_CheckExact(op1)) {
        if (PyFloat_CheckExact(op2)) {
            double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op1 == -1. && PyErr_Occurred())) return NULL;
            #endif
            double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(float_op2 == -1. && PyErr_Occurred())) return NULL;
            #endif
            if (float_op1 == float_op2) goto __pyx_return_true; else goto __pyx_return_false;
        }
        if (PyLong_CheckExact(op2)) {
            return __Pyx_PyObject_CompareFloatIntEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    if (PyLong_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyLong_CheckExact(op2)) {
            return __Pyx_PyObject_CompareIntIntEq(op1, op2);
        }
        if (PyFloat_CheckExact(op2)) {
            return __Pyx_PyObject_CompareIntFloatEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    
    if (PyUnicode_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyUnicode_CheckExact(op2)) {
            return __Pyx_PyObject_CompareStrStrEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    
    #if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
    if (PyBytes_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyBytes_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyBytesPyBytesEq(op1, op2);
        }
        if (PyByteArray_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyBytesPyByteArrayEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    #endif
    #if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL)
    if (PyByteArray_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        if (PyByteArray_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyByteArrayPyByteArrayEq(op1, op2);
        }
        if (PyBytes_CheckExact(op2)) {
            return __Pyx_PyObject_ComparePyByteArrayPyBytesEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    #endif
    if ((0)) goto __pyx_richcmp;
    if ((0)) goto __pyx_return_true;
    if ((0)) goto __pyx_return_false;
__pyx_richcmp:
    return PyObject_RichCompare(op1, op2, Py_EQ);
__pyx_return_true:
    Py_RETURN_TRUE;
__pyx_return_false:
    Py_RETURN_FALSE;
}

