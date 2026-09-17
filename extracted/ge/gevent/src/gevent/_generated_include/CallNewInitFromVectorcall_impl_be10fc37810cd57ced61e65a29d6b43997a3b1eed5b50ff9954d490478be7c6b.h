#if CYTHON_VECTORCALL_TPNEW
static PyObject *__Pyx_CallNewInitFromVectorcall(PyTypeObject *t, PyObject *const *args, size_t nargsf, PyObject *kwnames) {
    newfunc tp_new = __Pyx_PyType_GetSlot(t, tp_new, newfunc);
    if (unlikely(!tp_new)) {
        __Pyx_RaiseErrorWithType(PyExc_TypeError, "cannot create " __Pyx_FMT_TYPENAME " instances", t);
        return NULL;
    }
    Py_ssize_t nargs = __Pyx_PyVectorcall_NARGS(nargsf);
    PyObject *result = NULL, *args_tuple = NULL, *kwds_dict = NULL;
    Py_ssize_t kw_size = kwnames ? __Pyx_PyTuple_GET_SIZE(kwnames) : 0;
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(kw_size == -1)) {
        return NULL;
    }
#endif
    if (kw_size) {
        kwds_dict = __Pyx_PyDict_NewPresized(kw_size);
        if (unlikely(!kwds_dict)) {
            return NULL;
        }
        for (Py_ssize_t i=0; i<kw_size; ++i) {
            PyObject *v = args[nargs + i];
            PyObject *k = __Pyx_PyTuple_GET_ITEM(kwnames, i);
#if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(!k)) {
                goto end;
            }
#endif
            if (unlikely(PyDict_SetItem(kwds_dict, k, v) < 0)) {
                goto end;
            }
        }
    }
    if (nargs) {
        args_tuple = __Pyx_PyTuple_FromArray(args, nargs);
        if (unlikely(!args_tuple)) {
            goto end;
        }
    } else {
        args_tuple = __Pyx_NewRef(__pyx_mstate_global->__pyx_empty_tuple);
    }
    result = tp_new(t, args_tuple, kwds_dict);
    if (unlikely(!result)) {
        goto end;
    }
    if (PyObject_TypeCheck(result, t)) {
        initproc tp_init = __Pyx_PyObject_GetSlot(result, tp_init, initproc);
        if (tp_init && unlikely(tp_init(result, args_tuple, kwds_dict) < 0)) {
            Py_CLEAR(result);
        }
    }
  end:
    Py_XDECREF(args_tuple);
    Py_XDECREF(kwds_dict);
    return result;
}
#endif

