#ifndef __Pyx_DEFINED_PyObject_CompareStrStrBoolEq
#define __Pyx_DEFINED_PyObject_CompareStrStrBoolEq
static CYTHON_INLINE int __Pyx_PyObject_CompareStrStrBoolEq(PyObject* s1, PyObject* s2) {
    #if __PYX_LIMITED_VERSION_HEX >= 0x030e0000
    int result = PyUnicode_Equal(s1, s2);
    #if !CYTHON_COMPILING_IN_CPYTHON
    if (unlikely(result == -1)) return -1;
    #endif
    if (result == 0) goto __pyx_return_false; else goto __pyx_return_true;
    #else
    int result = PyUnicode_Compare(s1, s2);
    if (unlikely((result == -1) && PyErr_Occurred())) return -1;
    if (result == 0) goto __pyx_return_true; else goto __pyx_return_false;
    #endif
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}
#endif
static CYTHON_INLINE int __Pyx_PyObject_CompareBoolEq_object_str(PyObject *op1, PyObject *op2, int pyop) {
    CYTHON_UNUSED_VAR(pyop);
    if (unlikely(op2 == Py_None)) {
        if (op1 == Py_None) goto __pyx_return_true; else goto __pyx_richcmp;
    }
    if (PyFloat_CheckExact(op1)) {
        goto __pyx_richcmp;
    }
    if (PyLong_CheckExact(op1)) {
        if (op1 == op2) goto __pyx_return_true;
        goto __pyx_richcmp;
    }
    
    if (likely(PyUnicode_CheckExact(op1))) {
        if (op1 == op2) goto __pyx_return_true;
        if (likely(op2 != Py_None)) {
            return __Pyx_PyObject_CompareStrStrBoolEq(op1, op2);
        }
        goto __pyx_richcmp;
    }
    
    if ((0)) goto __pyx_richcmp;
    if ((0)) goto __pyx_return_true;
    if ((0)) goto __pyx_return_false;
__pyx_richcmp:
    return __Pyx_PyObject_RichCompareBool(op1, op2, Py_EQ);
__pyx_return_true:
    return 1;
__pyx_return_false:
    return 0;
}

