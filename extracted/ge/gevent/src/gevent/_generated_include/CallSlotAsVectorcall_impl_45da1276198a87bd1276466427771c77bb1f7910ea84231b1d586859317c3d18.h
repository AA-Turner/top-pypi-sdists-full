#if CYTHON_VECTORCALL_TPNEW
static int __Pyx_CallTpinitAsVectorcall(__Pyx_tpinitvectorcallfunc f, PyObject* o, PyObject *a, PyObject *k) {
    Py_ssize_t k_size = k ? __Pyx_PyDict_GET_SIZE(k) : 0;
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(k_size < 0)) return -1;
#endif
    Py_ssize_t a_size = __Pyx_PyTuple_GET_SIZE(a);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(a_size < 0)) return -1;
#endif
#if CYTHON_ASSUME_SAFE_MACROS
    if (k_size == 0) {
        return f(o, &PyTuple_GET_ITEM(a, 0), a_size, NULL);
    }
#else
    if (k_size == 0 && a_size == 0) {
        return f(o, NULL, 0, NULL);
    }
#endif
    PyObject *stack_args[5];
    PyObject **args = stack_args;
    Py_ssize_t maxnargs = PY_SSIZE_T_MAX / sizeof(PyObject*) - 1;
    if (a_size > maxnargs - k_size) {
        PyErr_NoMemory();
        return -1;
    }
    Py_ssize_t total_size = a_size + k_size;
    if (total_size > 5) {
        args = (PyObject**)PyMem_Malloc(((size_t)total_size)*sizeof(PyObject*));
        if (unlikely(!args)) {
            PyErr_NoMemory();
            return -1;
        }
    }
    int result = -1;
    PyObject *kwnames = NULL;
    int unpack_dict_result;
    Py_ssize_t i = 0;
    for (; i < a_size; ++i) {
        args[i] = __Pyx_PyTuple_GET_ITEM(a, i);
#if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!args[i])) goto cleanup;
#endif
    }
#if !CYTHON_ASSUME_SAFE_MACROS
    if (k)  // There's a specific shortcut earlier for ASSUME_SAFE_MACROS with no keywords
#endif
    {
        kwnames = PyTuple_New(k_size);
        if (unlikely(!kwnames)) goto cleanup;
        __Pyx_BEGIN_CRITICAL_SECTION(k);
        unpack_dict_result = __Pyx_CallSlotAsVectorcallUnpackDict(a_size, k, args, kwnames);
        __Pyx_END_CRITICAL_SECTION();
        if (unlikely(unpack_dict_result == -1)) goto cleanup;
    }
    result = f(o, args, a_size, kwnames);
  cleanup:
    Py_XDECREF(kwnames);
    for (i=a_size; i<total_size; ++i) {
        Py_XDECREF(args[i]);
    }
    if (args != stack_args) {
        PyMem_Free(args);
    }
    return result;
}
#endif

