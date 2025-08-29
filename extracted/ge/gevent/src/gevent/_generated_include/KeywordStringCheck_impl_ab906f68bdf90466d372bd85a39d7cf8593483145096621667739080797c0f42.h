static int __Pyx_CheckKeywordStrings(
    const char* function_name,
    PyObject *kw)
{
#if CYTHON_COMPILING_IN_PYPY && !defined(PyArg_ValidateKeywordArguments)
    CYTHON_UNUSED_VAR(function_name);
    CYTHON_UNUSED_VAR(kw);
    return 0;
#else
    if (CYTHON_METH_FASTCALL && likely(PyTuple_Check(kw))) {
#if PY_VERSION_HEX >= 0x03090000
        CYTHON_UNUSED_VAR(function_name);
#else
        Py_ssize_t kwsize;
        #if CYTHON_ASSUME_SAFE_SIZE
        kwsize = PyTuple_GET_SIZE(kw);
        #else
        kwsize = PyTuple_Size(kw);
        if (unlikely(kwsize < 0)) return -1;
        #endif
        for (Py_ssize_t pos = 0; pos < kwsize; pos++) {
            PyObject* key = NULL;
            #if CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kw, pos);
            #else
            key = PyTuple_GetItem(kw, pos);
            if (unlikely(!key)) return -1;
            #endif
            if (unlikely(!PyUnicode_Check(key))) {
                PyErr_Format(PyExc_TypeError,
                    "%.200s() keywords must be strings", function_name);
                return -1;
            }
        }
#endif
    } else {
        if (unlikely(!PyArg_ValidateKeywordArguments(kw))) return -1;
    }
    return 0;
#endif
}

