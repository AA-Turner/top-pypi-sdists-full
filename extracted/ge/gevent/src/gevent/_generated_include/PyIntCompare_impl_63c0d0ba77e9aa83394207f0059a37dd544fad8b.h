static CYTHON_INLINE int __Pyx_PyInt_BoolNeObjC(PyObject *op1, PyObject *op2, long intval, long inplace) {
    CYTHON_MAYBE_UNUSED_VAR(intval);
    CYTHON_UNUSED_VAR(inplace);
    if (op1 == op2) {
        return 0;
    }
    #if PY_MAJOR_VERSION < 3
    if (likely(PyInt_CheckExact(op1))) {
        const long b = intval;
        long a = PyInt_AS_LONG(op1);
        return (a != b);
    }
    #endif
    #if CYTHON_USE_PYLONG_INTERNALS
    if (likely(PyLong_CheckExact(op1))) {
        int unequal;
        unsigned long uintval;
        Py_ssize_t size = __Pyx_PyLong_DigitCount(op1);
        const digit* digits = __Pyx_PyLong_Digits(op1);
        if (intval == 0) {
            return (__Pyx_PyLong_IsZero(op1) != 1);
        } else if (intval < 0) {
            if (__Pyx_PyLong_IsNonNeg(op1))
                return 1;
            intval = -intval;
        } else {
            if (__Pyx_PyLong_IsNeg(op1))
                return 1;
        }
        uintval = (unsigned long) intval;
#if PyLong_SHIFT * 4 < SIZEOF_LONG*8
        if (uintval >> (PyLong_SHIFT * 4)) {
            unequal = (size != 5) || (digits[0] != (uintval & (unsigned long) PyLong_MASK))
                 | (digits[1] != ((uintval >> (1 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[2] != ((uintval >> (2 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[3] != ((uintval >> (3 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[4] != ((uintval >> (4 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK));
        } else
#endif
#if PyLong_SHIFT * 3 < SIZEOF_LONG*8
        if (uintval >> (PyLong_SHIFT * 3)) {
            unequal = (size != 4) || (digits[0] != (uintval & (unsigned long) PyLong_MASK))
                 | (digits[1] != ((uintval >> (1 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[2] != ((uintval >> (2 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[3] != ((uintval >> (3 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK));
        } else
#endif
#if PyLong_SHIFT * 2 < SIZEOF_LONG*8
        if (uintval >> (PyLong_SHIFT * 2)) {
            unequal = (size != 3) || (digits[0] != (uintval & (unsigned long) PyLong_MASK))
                 | (digits[1] != ((uintval >> (1 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)) | (digits[2] != ((uintval >> (2 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK));
        } else
#endif
#if PyLong_SHIFT * 1 < SIZEOF_LONG*8
        if (uintval >> (PyLong_SHIFT * 1)) {
            unequal = (size != 2) || (digits[0] != (uintval & (unsigned long) PyLong_MASK))
                 | (digits[1] != ((uintval >> (1 * PyLong_SHIFT)) & (unsigned long) PyLong_MASK));
        } else
#endif
            unequal = (size != 1) || (((unsigned long) digits[0]) != (uintval & (unsigned long) PyLong_MASK));
        return (unequal != 0);
    }
    #endif
    if (PyFloat_CheckExact(op1)) {
        const long b = intval;
#if CYTHON_COMPILING_IN_LIMITED_API
        double a = __pyx_PyFloat_AsDouble(op1);
#else
        double a = PyFloat_AS_DOUBLE(op1);
#endif
        return ((double)a != (double)b);
    }
    return __Pyx_PyObject_IsTrueAndDecref(
        PyObject_RichCompare(op1, op2, Py_NE));
}

