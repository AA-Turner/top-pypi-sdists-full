static int __Pyx_CheckKeywordStrings(
    PyObject *kw,
    const char* function_name,
    int kw_allowed)
{
    PyObject* key = 0;
    Py_ssize_t pos = 0;
#if CYTHON_COMPILING_IN_PYPY
    if (!kw_allowed && PyDict_Next(kw, &pos, &key, 0))
        goto invalid_keyword;
    return 1;
#else
    if (CYTHON_METH_FASTCALL && likely(PyTuple_Check(kw))) {
        Py_ssize_t kwsize;
#if CYTHON_ASSUME_SAFE_MACROS
        kwsize = PyTuple_GET_SIZE(kw);
#else
        kwsize = PyTuple_Size(kw);
        if (kwsize < 0) return 0;
#endif
        if (unlikely(kwsize == 0))
            return 1;
        if (!kw_allowed) {
#if CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kw, 0);
#else
            key = PyTuple_GetItem(kw, pos);
            if (!key) return 0;
#endif
            goto invalid_keyword;
        }
#if PY_VERSION_HEX < 0x03090000
        for (pos = 0; pos < kwsize; pos++) {
#if CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kw, pos);
#else
            key = PyTuple_GetItem(kw, pos);
            if (!key) return 0;
#endif
            if (unlikely(!PyUnicode_Check(key)))
                goto invalid_keyword_type;
        }
#endif
        return 1;
    }
    while (PyDict_Next(kw, &pos, &key, 0)) {
        #if PY_MAJOR_VERSION < 3
        if (unlikely(!PyString_Check(key)))
        #endif
            if (unlikely(!PyUnicode_Check(key)))
                goto invalid_keyword_type;
    }
    if (!kw_allowed && unlikely(key))
        goto invalid_keyword;
    return 1;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%.200s() keywords must be strings", function_name);
    return 0;
#endif
invalid_keyword:
    #if PY_MAJOR_VERSION < 3
    PyErr_Format(PyExc_TypeError,
        "%.200s() got an unexpected keyword argument '%.200s'",
        function_name, PyString_AsString(key));
    #else
    PyErr_Format(PyExc_TypeError,
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
    return 0;
}

