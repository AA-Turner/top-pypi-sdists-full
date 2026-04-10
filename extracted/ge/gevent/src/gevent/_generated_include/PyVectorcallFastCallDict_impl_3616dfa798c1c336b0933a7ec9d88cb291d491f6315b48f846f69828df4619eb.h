#if CYTHON_METH_FASTCALL && CYTHON_VECTORCALL
static PyObject *__Pyx_PyVectorcall_FastCallDict_kw(PyObject *func, __pyx_vectorcallfunc vc, PyObject *const *args, size_t nargs, PyObject *kw)
{
    PyObject *res = NULL;
    PyObject *kwnames;
    PyObject **newargs;
    PyObject **kwvalues;
    Py_ssize_t i;
    #if CYTHON_AVOID_BORROWED_REFS
    PyObject *pos;
    #else
    Py_ssize_t pos;
    #endif
    size_t j;
    PyObject *key, *value;
    unsigned long keys_are_strings;
    #if !CYTHON_ASSUME_SAFE_SIZE
    Py_ssize_t nkw = PyDict_Size(kw);
    if (unlikely(nkw == -1)) return NULL;
    #else
    Py_ssize_t nkw = PyDict_GET_SIZE(kw);
    #endif
    newargs = (PyObject **)PyMem_Malloc((nargs + (size_t)nkw) * sizeof(args[0]));
    if (unlikely(newargs == NULL)) {
        PyErr_NoMemory();
        return NULL;
    }
    for (j = 0; j < nargs; j++) newargs[j] = args[j];
    kwnames = PyTuple_New(nkw);
    if (unlikely(kwnames == NULL)) {
        PyMem_Free(newargs);
        return NULL;
    }
    kwvalues = newargs + nargs;
    pos = 0;
    i = 0;
    keys_are_strings = Py_TPFLAGS_UNICODE_SUBCLASS;
    while (__Pyx_PyDict_NextRef(kw, &pos, &key, &value)) {
        keys_are_strings &=
        #if CYTHON_COMPILING_IN_LIMITED_API
            PyType_GetFlags(Py_TYPE(key));
        #else
            Py_TYPE(key)->tp_flags;
        #endif
        #if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(PyTuple_SetItem(kwnames, i, key) < 0)) goto cleanup;
        #else
        PyTuple_SET_ITEM(kwnames, i, key);
        #endif
        kwvalues[i] = value;
        i++;
    }
    if (unlikely(!keys_are_strings)) {
        PyErr_SetString(PyExc_TypeError, "keywords must be strings");
        goto cleanup;
    }
    res = vc(func, newargs, nargs, kwnames);
cleanup:
    #if CYTHON_AVOID_BORROWED_REFS
    Py_DECREF(pos);
    #endif
    Py_DECREF(kwnames);
    for (i = 0; i < nkw; i++)
        Py_DECREF(kwvalues[i]);
    PyMem_Free(newargs);
    return res;
}
static CYTHON_INLINE PyObject *__Pyx_PyVectorcall_FastCallDict(PyObject *func, __pyx_vectorcallfunc vc, PyObject *const *args, size_t nargs, PyObject *kw)
{
    Py_ssize_t kw_size =
        likely(kw == NULL) ?
        0 :
#if !CYTHON_ASSUME_SAFE_SIZE
        PyDict_Size(kw);
#else
        PyDict_GET_SIZE(kw);
#endif
    if (kw_size == 0) {
        return vc(func, args, nargs, NULL);
    }
#if !CYTHON_ASSUME_SAFE_SIZE
    else if (unlikely(kw_size == -1)) {
        return NULL;
    }
#endif
    return __Pyx_PyVectorcall_FastCallDict_kw(func, vc, args, nargs, kw);
}
#endif

