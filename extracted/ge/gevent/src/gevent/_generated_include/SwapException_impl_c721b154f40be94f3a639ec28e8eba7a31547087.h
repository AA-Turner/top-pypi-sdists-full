#if CYTHON_FAST_THREAD_STATE
static CYTHON_INLINE void __Pyx__ExceptionSwap(PyThreadState *tstate, PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
  #if CYTHON_USE_EXC_INFO_STACK && PY_VERSION_HEX >= 0x030B00a4
    _PyErr_StackItem *exc_info = tstate->exc_info;
    tmp_value = exc_info->exc_value;
    exc_info->exc_value = *value;
    if (tmp_value == NULL || tmp_value == Py_None) {
        Py_XDECREF(tmp_value);
        tmp_value = NULL;
        tmp_type = NULL;
        tmp_tb = NULL;
    } else {
        tmp_type = (PyObject*) Py_TYPE(tmp_value);
        Py_INCREF(tmp_type);
        #if CYTHON_COMPILING_IN_CPYTHON
        tmp_tb = ((PyBaseExceptionObject*) tmp_value)->traceback;
        Py_XINCREF(tmp_tb);
        #else
        tmp_tb = PyException_GetTraceback(tmp_value);
        #endif
    }
  #elif CYTHON_USE_EXC_INFO_STACK
    _PyErr_StackItem *exc_info = tstate->exc_info;
    tmp_type = exc_info->exc_type;
    tmp_value = exc_info->exc_value;
    tmp_tb = exc_info->exc_traceback;
    exc_info->exc_type = *type;
    exc_info->exc_value = *value;
    exc_info->exc_traceback = *tb;
  #else
    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;
    tstate->exc_type = *type;
    tstate->exc_value = *value;
    tstate->exc_traceback = *tb;
  #endif
    *type = tmp_type;
    *value = tmp_value;
    *tb = tmp_tb;
}
#else
static CYTHON_INLINE void __Pyx_ExceptionSwap(PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyErr_GetExcInfo(&tmp_type, &tmp_value, &tmp_tb);
    PyErr_SetExcInfo(*type, *value, *tb);
    *type = tmp_type;
    *value = tmp_value;
    *tb = tmp_tb;
}
#endif

