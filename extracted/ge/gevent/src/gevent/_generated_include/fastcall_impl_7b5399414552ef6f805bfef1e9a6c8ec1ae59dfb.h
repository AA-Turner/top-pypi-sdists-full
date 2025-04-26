#if CYTHON_METH_FASTCALL
static CYTHON_INLINE PyObject * __Pyx_GetKwValue_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues, PyObject *s)
{
    Py_ssize_t i, n = PyTuple_GET_SIZE(kwnames);
    for (i = 0; i < n; i++)
    {
        if (s == PyTuple_GET_ITEM(kwnames, i)) return kwvalues[i];
    }
    for (i = 0; i < n; i++)
    {
        int eq = __Pyx_PyUnicode_Equals(s, PyTuple_GET_ITEM(kwnames, i), Py_EQ);
        if (unlikely(eq != 0)) {
            if (unlikely(eq < 0)) return NULL;
            return kwvalues[i];
        }
    }
    return NULL;
}
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
CYTHON_UNUSED static PyObject *__Pyx_KwargsAsDict_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues) {
    Py_ssize_t i, nkwargs = PyTuple_GET_SIZE(kwnames);
    PyObject *dict;
    dict = PyDict_New();
    if (unlikely(!dict))
        return NULL;
    for (i=0; i<nkwargs; i++) {
        PyObject *key = PyTuple_GET_ITEM(kwnames, i);
        if (unlikely(PyDict_SetItem(dict, key, kwvalues[i]) < 0))
            goto bad;
    }
    return dict;
bad:
    Py_DECREF(dict);
    return NULL;
}
#endif
#endif

