static unsigned short __Pyx_LargePyLong___Pyx_PyLong_As_unsigned_short(PyObject *x);
static unsigned short __Pyx_raise_neg_overflow___Pyx_PyLong_As_unsigned_short(void) {
    const char* type_name = "unsigned short";
    PyErr_Format(PyExc_OverflowError,
        "can't convert negative value to %.200s", type_name);
    return (unsigned short) -1;
}
static unsigned short __Pyx_raise_overflow___Pyx_PyLong_As_unsigned_short(void) {
    const char* type_name = "unsigned short";
    PyErr_Format(PyExc_OverflowError,
        "value too large to convert to %.200s", type_name);
    return (unsigned short) -1;
}
static CYTHON_INLINE unsigned short __Pyx_PyULong___Pyx_PyLong_As_unsigned_short(PyObject *x) {
    const int is_unsigned = 1;
#if CYTHON_USE_PYLONG_INTERNALS
    {
        const digit* digits = __Pyx_PyLong_Digits(x);
        const Py_ssize_t size = __Pyx_PyLong_DigitCount(x);
        if (size == 2 && (8 * sizeof(unsigned short) > 1 * PyLong_SHIFT)) {
            if ((8 * sizeof(unsigned long) > 2 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) >= 2 * PyLong_SHIFT)) {
                return (unsigned short) (((((unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        if (size == 3 && (8 * sizeof(unsigned short) > 2 * PyLong_SHIFT)) {
            if ((8 * sizeof(unsigned long) > 3 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) >= 3 * PyLong_SHIFT)) {
                return (unsigned short) (((((((unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        if (size == 4 && (8 * sizeof(unsigned short) > 3 * PyLong_SHIFT)) {
            if ((8 * sizeof(unsigned long) > 4 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) >= 4 * PyLong_SHIFT)) {
                return (unsigned short) (((((((((unsigned short)digits[3]) << PyLong_SHIFT) | (unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        {}
    }
#elif CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030C00A7
    if (unlikely(Py_SIZE(x) < 0)) {
        goto raise_neg_overflow;
    }
#else
    {
        int result = PyObject_RichCompareBool(x, Py_False, Py_LT);
        if (unlikely(result < 0))
            return (unsigned short) -1;
        if (unlikely(result == 1))
            goto raise_neg_overflow;
    }
#endif
    if ((sizeof(unsigned short) <= sizeof(unsigned long))) {
        __PYX_VERIFY_RETURN_INT_EXC(unsigned short, unsigned long, PyLong_AsUnsignedLong(x))
    } else if ((sizeof(unsigned short) <= sizeof(unsigned PY_LONG_LONG))) {
        __PYX_VERIFY_RETURN_INT_EXC(unsigned short, unsigned PY_LONG_LONG, PyLong_AsUnsignedLongLong(x))
    }
    return __Pyx_LargePyLong___Pyx_PyLong_As_unsigned_short(x);
raise_neg_overflow:
    return __Pyx_raise_neg_overflow___Pyx_PyLong_As_unsigned_short();
raise_overflow:
    return __Pyx_raise_overflow___Pyx_PyLong_As_unsigned_short();
}
static CYTHON_INLINE unsigned short __Pyx_PySLong___Pyx_PyLong_As_unsigned_short(PyObject *x) {
    const int is_unsigned = 0;
#if CYTHON_USE_PYLONG_INTERNALS
    if (__Pyx_PyLong_IsNeg(x)) {
        const Py_ssize_t size = __Pyx_PyLong_DigitCount(x);
        const digit* digits = __Pyx_PyLong_Digits(x);
        if (size == 2 && (8 * sizeof(unsigned short) > 1 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 2 * PyLong_SHIFT)) {
                long ival = - (long) (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0]));
                __PYX_VERIFY_RETURN_INT(unsigned short, long, ival)
            } else if ((8 * sizeof(unsigned short) - 1 > 2 * PyLong_SHIFT)) {
                return (unsigned short) (((unsigned short) -1) * (((((unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0])));
            }
        } else
        if (size == 3 && (8 * sizeof(unsigned short) > 2 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 3 * PyLong_SHIFT)) {
                long ival = - (long) (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0]));
                __PYX_VERIFY_RETURN_INT(unsigned short, long, ival)
            } else if ((8 * sizeof(unsigned short) - 1 > 3 * PyLong_SHIFT)) {
                return (unsigned short) (((unsigned short) -1) * (((((((unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0])));
            }
        } else
        if (size == 4 && (8 * sizeof(unsigned short) > 3 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 4 * PyLong_SHIFT)) {
                long ival = - (long) (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0]));
                __PYX_VERIFY_RETURN_INT(unsigned short, long, ival)
            } else if ((8 * sizeof(unsigned short) - 1 > 4 * PyLong_SHIFT)) {
                return (unsigned short) (((unsigned short) -1) * (((((((((unsigned short)digits[3]) << PyLong_SHIFT) | (unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0])));
            }
        } else
        {}
    } else {
        const Py_ssize_t size = __Pyx_PyLong_DigitCount(x);
        const digit* digits = __Pyx_PyLong_Digits(x);
        if (size == 2 && (8 * sizeof(unsigned short) > 1 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 2 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) - 1 > 2 * PyLong_SHIFT)) {
                return (unsigned short) (((((unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        if (size == 3 && (8 * sizeof(unsigned short) > 2 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 3 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) - 1 > 3 * PyLong_SHIFT)) {
                return (unsigned short) (((((((unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        if (size == 4 && (8 * sizeof(unsigned short) > 3 * PyLong_SHIFT)) {
            if ((8 * sizeof(long) > 4 * PyLong_SHIFT)) {
                __PYX_VERIFY_RETURN_INT(unsigned short, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
            } else if ((8 * sizeof(unsigned short) - 1 > 4 * PyLong_SHIFT)) {
                return (unsigned short) (((((((((unsigned short)digits[3]) << PyLong_SHIFT) | (unsigned short)digits[2]) << PyLong_SHIFT) | (unsigned short)digits[1]) << PyLong_SHIFT) | (unsigned short)digits[0]));
            }
        } else
        {}
    }
#endif
    #if __PYX_LIMITED_VERSION_HEX >= 0x030d0000
    if ((sizeof(unsigned short) <= sizeof(int)) && (sizeof(int) < sizeof(long))) {
        __PYX_VERIFY_RETURN_INT_EXC(unsigned short, int, PyLong_AsInt(x))
    } else
    #endif
    if ((sizeof(unsigned short) <= sizeof(long))) {
        __PYX_VERIFY_RETURN_INT_EXC(unsigned short, long, PyLong_AsLong(x))
    } else if ((sizeof(unsigned short) <= sizeof(PY_LONG_LONG))) {
        __PYX_VERIFY_RETURN_INT_EXC(unsigned short, PY_LONG_LONG, PyLong_AsLongLong(x))
    }
    return __Pyx_LargePyLong___Pyx_PyLong_As_unsigned_short(x);
raise_neg_overflow:
    return __Pyx_raise_neg_overflow___Pyx_PyLong_As_unsigned_short();
raise_overflow:
    return __Pyx_raise_overflow___Pyx_PyLong_As_unsigned_short();
}
static unsigned short __Pyx_LargePyLong___Pyx_PyLong_As_unsigned_short(PyObject *x) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const unsigned short neg_one = (unsigned short) -1, const_zero = (unsigned short) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    unsigned short val;
    int ret = -1;
#if PY_VERSION_HEX >= 0x030d00A6 && !CYTHON_COMPILING_IN_LIMITED_API
    Py_ssize_t bytes_copied = PyLong_AsNativeBytes(
        x, &val, sizeof(val), Py_ASNATIVEBYTES_NATIVE_ENDIAN | (is_unsigned ? Py_ASNATIVEBYTES_UNSIGNED_BUFFER | Py_ASNATIVEBYTES_REJECT_NEGATIVE : 0));
    if (unlikely(bytes_copied == -1)) {
    } else if (unlikely(bytes_copied > (Py_ssize_t) sizeof(val))) {
        goto raise_overflow;
    } else {
        ret = 0;
    }
#elif PY_VERSION_HEX < 0x030d0000 && !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_LIMITED_API) || defined(_PyLong_AsByteArray)
    int one = 1; int is_little = (int)*(unsigned char *)&one;
    unsigned char *bytes = (unsigned char *)&val;
    ret = _PyLong_AsByteArray((PyLongObject *)x,
                                bytes, sizeof(val),
                                is_little, !is_unsigned);
    if ((0)) goto raise_overflow;
#else
    PyObject *v;
    PyObject *stepval = NULL, *mask = NULL, *shift = NULL;
    int bits, remaining_bits, is_negative = 0;
    int chunk_size = (sizeof(long) < 8) ? 30 : 62;
    if (likely(PyLong_CheckExact(x))) {
        v = __Pyx_NewRef(x);
    } else {
        v = PyNumber_Long(x);
        if (unlikely(!v)) return (unsigned short) -1;
        assert(PyLong_CheckExact(v));
    }
    {
        int result = PyObject_RichCompareBool(v, Py_False, Py_LT);
        if (unlikely(result < 0)) {
            Py_DECREF(v);
            return (unsigned short) -1;
        }
        is_negative = result == 1;
    }
    if (is_unsigned && unlikely(is_negative)) {
        Py_DECREF(v);
        PyErr_SetString(PyExc_OverflowError,
            "can't convert negative value to unsigned short");
        return (unsigned short) -1;
    } else if (is_negative) {
        stepval = PyNumber_Invert(v);
        Py_DECREF(v);
        if (unlikely(!stepval))
            return (unsigned short) -1;
    } else {
        stepval = v;
    }
    v = NULL;
    val = (unsigned short) 0;
    mask = PyLong_FromLong((1L << chunk_size) - 1); if (unlikely(!mask)) goto done;
    shift = PyLong_FromLong(chunk_size); if (unlikely(!shift)) goto done;
    for (bits = 0; bits < (int) sizeof(unsigned short) * 8 - chunk_size; bits += chunk_size) {
        PyObject *tmp, *digit;
        long idigit;
        digit = PyNumber_And(stepval, mask);
        if (unlikely(!digit)) goto done;
        idigit = PyLong_AsLong(digit);
        Py_DECREF(digit);
        if (unlikely(idigit < 0)) goto done;
        val |= ((unsigned short) idigit) << bits;
        tmp = PyNumber_Rshift(stepval, shift);
        if (unlikely(!tmp)) goto done;
        Py_DECREF(stepval); stepval = tmp;
    }
    Py_DECREF(shift); shift = NULL;
    Py_DECREF(mask); mask = NULL;
    {
        long idigit = PyLong_AsLong(stepval);
        if (unlikely(idigit < 0)) goto done;
        remaining_bits = ((int) sizeof(unsigned short) * 8) - bits - (is_unsigned ? 0 : 1);
        if (unlikely(idigit >= (1L << remaining_bits)))
            goto raise_overflow;
        val |= ((unsigned short) idigit) << bits;
    }
    if (!is_unsigned) {
        if (unlikely(val & (((unsigned short) 1) << (sizeof(unsigned short) * 8 - 1))))
            goto raise_overflow;
        if (is_negative)
            val = ~val;
    }
    ret = 0;
done:
    Py_XDECREF(shift);
    Py_XDECREF(mask);
    Py_XDECREF(stepval);
#endif
    if (unlikely(ret))
        return (unsigned short) -1;
    return val;
raise_overflow:
    return __Pyx_raise_overflow___Pyx_PyLong_As_unsigned_short();
}
static CYTHON_INLINE unsigned short __Pyx_PyLong___Pyx_PyLong_As_unsigned_short(PyObject *x) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const unsigned short neg_one = (unsigned short) -1, const_zero = (unsigned short) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    if (is_unsigned) {
        #if CYTHON_USE_PYLONG_INTERNALS
        if (unlikely(__Pyx_PyLong_IsNeg(x))) {
            goto raise_neg_overflow;
        } else if (__Pyx_PyLong_IsCompact(x)) {
            __PYX_VERIFY_RETURN_INT(unsigned short, __Pyx_compact_upylong, __Pyx_PyLong_CompactValueUnsigned(x))
        } else
        #endif
        {
            return __Pyx_PyULong___Pyx_PyLong_As_unsigned_short(x);
        }
    } else {
        #if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsCompact(x)) {
            __PYX_VERIFY_RETURN_INT(unsigned short, __Pyx_compact_pylong, __Pyx_PyLong_CompactValue(x))
        } else
        #endif
        {
            return __Pyx_PySLong___Pyx_PyLong_As_unsigned_short(x);
        }
    }
#if CYTHON_USE_PYLONG_INTERNALS
raise_neg_overflow:
    return __Pyx_raise_neg_overflow___Pyx_PyLong_As_unsigned_short();
raise_overflow:
    return __Pyx_raise_overflow___Pyx_PyLong_As_unsigned_short();
#endif
}
static unsigned short __Pyx_NonPyLong___Pyx_PyLong_As_unsigned_short(PyObject *x) {
    unsigned short val;
    PyObject *tmp = __Pyx_PyNumber_Long(x);
    if (!tmp) return (unsigned short) -1;
    val = __Pyx_PyLong_As_unsigned_short(tmp);
    Py_DECREF(tmp);
    return val;
}
static CYTHON_INLINE unsigned short __Pyx_PyLong_As_unsigned_short(PyObject *x) {
    if (likely(PyLong_Check(x))) {
        return __Pyx_PyLong___Pyx_PyLong_As_unsigned_short(x);
    } else {
        return __Pyx_NonPyLong___Pyx_PyLong_As_unsigned_short(x);
    }
}

