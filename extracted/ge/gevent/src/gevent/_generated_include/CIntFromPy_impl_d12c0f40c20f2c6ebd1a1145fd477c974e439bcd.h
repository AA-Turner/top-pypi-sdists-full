static CYTHON_INLINE long __Pyx_PyInt_As_long(PyObject *x) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const long neg_one = (long) -1, const_zero = (long) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
#if PY_MAJOR_VERSION < 3
    if (likely(PyInt_Check(x))) {
        if ((sizeof(long) < sizeof(long))) {
            __PYX_VERIFY_RETURN_INT(long, long, PyInt_AS_LONG(x))
        } else {
            long val = PyInt_AS_LONG(x);
            if (is_unsigned && unlikely(val < 0)) {
                goto raise_neg_overflow;
            }
            return (long) val;
        }
    }
#endif
    if (unlikely(!PyLong_Check(x))) {
        long val;
        PyObject *tmp = __Pyx_PyNumber_IntOrLong(x);
        if (!tmp) return (long) -1;
        val = __Pyx_PyInt_As_long(tmp);
        Py_DECREF(tmp);
        return val;
    }
    if (is_unsigned) {
#if CYTHON_USE_PYLONG_INTERNALS
        if (unlikely(__Pyx_PyLong_IsNeg(x))) {
            goto raise_neg_overflow;
        } else if (__Pyx_PyLong_IsCompact(x)) {
            __PYX_VERIFY_RETURN_INT(long, __Pyx_compact_upylong, __Pyx_PyLong_CompactValueUnsigned(x))
        } else {
            const digit* digits = __Pyx_PyLong_Digits(x);
            assert(__Pyx_PyLong_DigitCount(x) > 1);
            switch (__Pyx_PyLong_DigitCount(x)) {
                case 2:
                    if ((8 * sizeof(long) > 1 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 2 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) >= 2 * PyLong_SHIFT)) {
                            return (long) (((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
                case 3:
                    if ((8 * sizeof(long) > 2 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 3 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) >= 3 * PyLong_SHIFT)) {
                            return (long) (((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
                case 4:
                    if ((8 * sizeof(long) > 3 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 4 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) >= 4 * PyLong_SHIFT)) {
                            return (long) (((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0]));
                        }
                    }
                    break;
            }
        }
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030C00A7
        if (unlikely(Py_SIZE(x) < 0)) {
            goto raise_neg_overflow;
        }
#else
        {
            int result = PyObject_RichCompareBool(x, Py_False, Py_LT);
            if (unlikely(result < 0))
                return (long) -1;
            if (unlikely(result == 1))
                goto raise_neg_overflow;
        }
#endif
        if ((sizeof(long) <= sizeof(unsigned long))) {
            __PYX_VERIFY_RETURN_INT_EXC(long, unsigned long, PyLong_AsUnsignedLong(x))
#ifdef HAVE_LONG_LONG
        } else if ((sizeof(long) <= sizeof(unsigned PY_LONG_LONG))) {
            __PYX_VERIFY_RETURN_INT_EXC(long, unsigned PY_LONG_LONG, PyLong_AsUnsignedLongLong(x))
#endif
        }
    } else {
#if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsCompact(x)) {
            __PYX_VERIFY_RETURN_INT(long, __Pyx_compact_pylong, __Pyx_PyLong_CompactValue(x))
        } else {
            const digit* digits = __Pyx_PyLong_Digits(x);
            assert(__Pyx_PyLong_DigitCount(x) > 1);
            switch (__Pyx_PyLong_SignedDigitCount(x)) {
                case -2:
                    if ((8 * sizeof(long) - 1 > 1 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 2 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 2 * PyLong_SHIFT)) {
                            return (long) (((long)-1)*(((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 2:
                    if ((8 * sizeof(long) > 1 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 2 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 2 * PyLong_SHIFT)) {
                            return (long) ((((((long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case -3:
                    if ((8 * sizeof(long) - 1 > 2 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 3 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 3 * PyLong_SHIFT)) {
                            return (long) (((long)-1)*(((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 3:
                    if ((8 * sizeof(long) > 2 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 3 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 3 * PyLong_SHIFT)) {
                            return (long) ((((((((long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case -4:
                    if ((8 * sizeof(long) - 1 > 3 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 4 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, long, -(long) (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 4 * PyLong_SHIFT)) {
                            return (long) (((long)-1)*(((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
                case 4:
                    if ((8 * sizeof(long) > 3 * PyLong_SHIFT)) {
                        if ((8 * sizeof(unsigned long) > 4 * PyLong_SHIFT)) {
                            __PYX_VERIFY_RETURN_INT(long, unsigned long, (((((((((unsigned long)digits[3]) << PyLong_SHIFT) | (unsigned long)digits[2]) << PyLong_SHIFT) | (unsigned long)digits[1]) << PyLong_SHIFT) | (unsigned long)digits[0])))
                        } else if ((8 * sizeof(long) - 1 > 4 * PyLong_SHIFT)) {
                            return (long) ((((((((((long)digits[3]) << PyLong_SHIFT) | (long)digits[2]) << PyLong_SHIFT) | (long)digits[1]) << PyLong_SHIFT) | (long)digits[0])));
                        }
                    }
                    break;
            }
        }
#endif
        if ((sizeof(long) <= sizeof(long))) {
            __PYX_VERIFY_RETURN_INT_EXC(long, long, PyLong_AsLong(x))
#ifdef HAVE_LONG_LONG
        } else if ((sizeof(long) <= sizeof(PY_LONG_LONG))) {
            __PYX_VERIFY_RETURN_INT_EXC(long, PY_LONG_LONG, PyLong_AsLongLong(x))
#endif
        }
    }
    {
        long val;
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
#else
        PyObject *v;
        PyObject *stepval = NULL, *mask = NULL, *shift = NULL;
        int bits, remaining_bits, is_negative = 0;
        int chunk_size = (sizeof(long) < 8) ? 30 : 62;
        if (likely(PyLong_CheckExact(x))) {
            v = __Pyx_NewRef(x);
        } else {
            v = PyNumber_Long(x);
            if (unlikely(!v)) return (long) -1;
            assert(PyLong_CheckExact(v));
        }
        {
            int result = PyObject_RichCompareBool(v, Py_False, Py_LT);
            if (unlikely(result < 0)) {
                Py_DECREF(v);
                return (long) -1;
            }
            is_negative = result == 1;
        }
        if (is_unsigned && unlikely(is_negative)) {
            Py_DECREF(v);
            goto raise_neg_overflow;
        } else if (is_negative) {
            stepval = PyNumber_Invert(v);
            Py_DECREF(v);
            if (unlikely(!stepval))
                return (long) -1;
        } else {
            stepval = v;
        }
        v = NULL;
        val = (long) 0;
        mask = PyLong_FromLong((1L << chunk_size) - 1); if (unlikely(!mask)) goto done;
        shift = PyLong_FromLong(chunk_size); if (unlikely(!shift)) goto done;
        for (bits = 0; bits < (int) sizeof(long) * 8 - chunk_size; bits += chunk_size) {
            PyObject *tmp, *digit;
            long idigit;
            digit = PyNumber_And(stepval, mask);
            if (unlikely(!digit)) goto done;
            idigit = PyLong_AsLong(digit);
            Py_DECREF(digit);
            if (unlikely(idigit < 0)) goto done;
            val |= ((long) idigit) << bits;
            tmp = PyNumber_Rshift(stepval, shift);
            if (unlikely(!tmp)) goto done;
            Py_DECREF(stepval); stepval = tmp;
        }
        Py_DECREF(shift); shift = NULL;
        Py_DECREF(mask); mask = NULL;
        {
            long idigit = PyLong_AsLong(stepval);
            if (unlikely(idigit < 0)) goto done;
            remaining_bits = ((int) sizeof(long) * 8) - bits - (is_unsigned ? 0 : 1);
            if (unlikely(idigit >= (1L << remaining_bits)))
                goto raise_overflow;
            val |= ((long) idigit) << bits;
        }
        if (!is_unsigned) {
            if (unlikely(val & (((long) 1) << (sizeof(long) * 8 - 1))))
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
            return (long) -1;
        return val;
    }
raise_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "value too large to convert to long");
    return (long) -1;
raise_neg_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "can't convert negative value to long");
    return (long) -1;
}

