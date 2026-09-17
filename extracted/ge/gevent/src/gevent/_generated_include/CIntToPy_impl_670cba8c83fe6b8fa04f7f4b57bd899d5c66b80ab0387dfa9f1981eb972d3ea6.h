static CYTHON_INLINE PyObject* __Pyx_PyLong_From_unsigned_int(unsigned int value) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const unsigned int neg_one = (unsigned int) -1, const_zero = (unsigned int) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    if (is_unsigned) {
        if (sizeof(unsigned int) < sizeof(long)) {
            return PyLong_FromLong((long) value);
        } else if (sizeof(unsigned int) <= sizeof(unsigned long)) {
            return PyLong_FromUnsignedLong((unsigned long) value);
#if !CYTHON_COMPILING_IN_PYPY
        } else if (sizeof(unsigned int) <= sizeof(unsigned PY_LONG_LONG)) {
            return PyLong_FromUnsignedLongLong((unsigned PY_LONG_LONG) value);
#endif
        }
    } else {
        if (sizeof(unsigned int) <= sizeof(long)) {
            return PyLong_FromLong((long) value);
        } else if (sizeof(unsigned int) <= sizeof(PY_LONG_LONG)) {
            return PyLong_FromLongLong((PY_LONG_LONG) value);
        }
    }
    {
        unsigned char *bytes = (unsigned char *)&value;
#if !CYTHON_COMPILING_IN_LIMITED_API && PY_VERSION_HEX >= 0x030d00A4
        if (is_unsigned) {
            return PyLong_FromUnsignedNativeBytes(bytes, sizeof(value), -1);
        } else {
            return PyLong_FromNativeBytes(bytes, sizeof(value), -1);
        }
#elif !CYTHON_COMPILING_IN_LIMITED_API && PY_VERSION_HEX < 0x030d0000
        int one = 1; int little = (int)*(unsigned char *)&one;
        return _PyLong_FromByteArray(bytes, sizeof(unsigned int),
                                     little, !is_unsigned);
#else
        int one = 1; int little = (int)*(unsigned char *)&one;
        PyObject *result = NULL, *kwds = NULL;
        PyObject *py_bytes = NULL, *order_str = NULL, *from_bytes_str = NULL;;
        py_bytes = PyBytes_FromStringAndSize((char*)bytes, sizeof(unsigned int));
        if (!py_bytes) goto limited_bad;
        from_bytes_str = PyUnicode_FromStringAndSize("from_bytes", 10);
        if (!from_bytes_str) goto limited_bad;
        order_str = PyUnicode_FromString(little ? "little" : "big");
        if (!order_str) goto limited_bad;
        {
            PyObject *args[] = { (PyObject*)&PyLong_Type, py_bytes, order_str, Py_True };
            if (!is_unsigned) {
                PyObject *signed_str = PyUnicode_FromStringAndSize("signed", 6);
                if (!signed_str) goto limited_bad;
#if CYTHON_VECTORCALL
                kwds = PyTuple_Pack(1, signed_str);
#else
                {
                    PyObject *keys[] = {signed_str};
                    PyObject *values[] = {Py_True};
                    kwds = __Pyx_MakeKwargDict(keys, values, 1);
                }
#endif
                Py_DECREF(signed_str);
                if (unlikely(!kwds)) goto limited_bad;
            }
            result = __Pyx_Object_VectorcallMethodKwds(from_bytes_str, args, 3 | __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET, kwds);
        }
        limited_bad:
        Py_XDECREF(kwds);
        Py_XDECREF(order_str);
        Py_XDECREF(py_bytes);
        Py_XDECREF(from_bytes_str);
        return result;
#endif
    }
}

