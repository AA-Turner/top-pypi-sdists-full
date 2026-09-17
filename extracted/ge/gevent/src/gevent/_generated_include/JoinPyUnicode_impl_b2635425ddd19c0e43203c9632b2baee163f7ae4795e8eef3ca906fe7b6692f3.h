static PyObject* __Pyx_PyUnicode_Join(PyObject** values, Py_ssize_t value_count, Py_ssize_t result_ulength, int kind) {
#if __Pyx_PyUnicode_Join_CAN_USE_KIND_AND_LENGTH && CYTHON_USE_UNICODE_INTERNALS
    PyObject *result_uval;
    int result_ukind, kind_shift;
    Py_ssize_t i, char_pos;
    void *result_udata;
    static const Py_UCS4 max_char[5] = {0x7fU, 0xffU, 0xffffU, 0xffffU, 0x10ffffU};
    assert (kind >= 0);
    if (kind > PyUnicode_4BYTE_KIND) kind = PyUnicode_4BYTE_KIND;
    result_uval = PyUnicode_New(result_ulength, max_char[kind]);
    if (unlikely(!result_uval)) return NULL;
    kind_shift = kind >> 1;  // 0, 1, 2
    result_ukind = 1 << kind_shift;  // 1, 2, 4
    result_udata = PyUnicode_DATA(result_uval);
    assert(kind_shift == 2 || kind_shift == 1 || kind_shift == 0);
    if (unlikely((PY_SSIZE_T_MAX >> kind_shift) - result_ulength < 0))
        goto overflow;
    char_pos = 0;
    for (i=0; i < value_count; i++) {
        int ukind;
        Py_ssize_t ulength;
        void *udata;
        PyObject *uval = values[i];
        if (__Pyx_PyUnicode_READY(uval) == (-1))
            goto bad;
        ulength = __Pyx_PyUnicode_GET_LENGTH(uval);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(ulength < 0)) goto bad;
        #endif
        if (unlikely(!ulength))
            continue;
        if (unlikely((PY_SSIZE_T_MAX >> kind_shift) - ulength < char_pos))
            goto overflow;
        ukind = __Pyx_PyUnicode_KIND(uval);
        udata = __Pyx_PyUnicode_DATA(uval);
        if (ukind == result_ukind) {
            memcpy((char *)result_udata + (char_pos << kind_shift), udata, (size_t) (ulength << kind_shift));
        } else {
            #if PY_VERSION_HEX >= 0x030d0000
            if (unlikely(PyUnicode_CopyCharacters(result_uval, char_pos, uval, 0, ulength) < 0)) goto bad;
            #elif CYTHON_COMPILING_IN_CPYTHON || defined(_PyUnicode_FastCopyCharacters)
            _PyUnicode_FastCopyCharacters(result_uval, char_pos, uval, 0, ulength);
            #else
            Py_ssize_t j;
            for (j=0; j < ulength; j++) {
                Py_UCS4 uchar = __Pyx_PyUnicode_READ(ukind, udata, j);
                __Pyx_PyUnicode_WRITE(result_ukind, result_udata, char_pos+j, uchar);
            }
            #endif
        }
        char_pos += ulength;
    }
    return result_uval;
overflow:
    PyErr_SetString(PyExc_OverflowError, "join() result is too long for a Python string");
bad:
    Py_DECREF(result_uval);
    return NULL;
#else
    Py_ssize_t i;
    PyObject *result = NULL;
    PyObject *value_tuple = PyTuple_New(value_count);
    if (unlikely(!value_tuple)) return NULL;
    CYTHON_UNUSED_VAR(kind);
    CYTHON_UNUSED_VAR(result_ulength);
    for (i=0; i<value_count; i++) {
        Py_INCREF(values[i]);
        if (__Pyx_PyTuple_SET_ITEM(value_tuple, i, values[i]) != (0)) goto bad;
    }
    result = PyUnicode_Join(__pyx_mstate_global->__pyx_empty_unicode, value_tuple);
bad:
    Py_DECREF(value_tuple);
    return result;
#endif
}

