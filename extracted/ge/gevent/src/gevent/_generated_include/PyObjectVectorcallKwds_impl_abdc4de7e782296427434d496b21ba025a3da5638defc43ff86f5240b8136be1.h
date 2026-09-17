#if CYTHON_VECTORCALL
CYTHON_UNUSED static int __Pyx_CheckVectorcallKwarg(PyObject *kwnames, Py_ssize_t i) {
    PyObject *key = __Pyx_PyTuple_GET_ITEM(kwnames, i);
#if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(!key)) return -1;
#endif
    if (unlikely(!PyUnicode_Check(key))) {
        PyErr_SetString(PyExc_TypeError, "keywords must be strings");
        return -1;
    }
    return 0;
}
#else
CYTHON_UNUSED static PyObject *__Pyx_MakeKwargDict(PyObject **keys, PyObject **values, Py_ssize_t n) {
    PyObject *out = PyDict_New();
    if (unlikely(!out)) return NULL;
    for (Py_ssize_t i=0; i<n; ++i) {
        if (unlikely(PyDict_SetItem(out, keys[i], values[i]) < 0)) {
            Py_DECREF(out);
            return NULL;
        }
    }
    return out;
}
CYTHON_UNUSED static int __Pyx_CheckVectorcallKwarg(PyObject **kwnames, Py_ssize_t i) {
    PyObject *key = kwnames[i];
    if (unlikely(!PyUnicode_Check(key))) {
        PyErr_SetString(PyExc_TypeError, "keywords must be strings");
        return -1;
    }
    return 0;
}
#endif

