#if PY_VERSION_HEX < 0x03090000 || CYTHON_COMPILING_IN_LIMITED_API
static PyObject* __Pyx_PyObject_FastCall_fallback(PyObject *func, PyObject * const*args, size_t nargs, PyObject *kwargs) {
    PyObject *argstuple;
    PyObject *result = 0;
    size_t i;
    argstuple = PyTuple_New((Py_ssize_t)nargs);
    if (unlikely(!argstuple)) return NULL;
    for (i = 0; i < nargs; i++) {
        Py_INCREF(args[i]);
        if (__Pyx_PyTuple_SET_ITEM(argstuple, (Py_ssize_t)i, args[i]) != (0)) goto bad;
    }
    result = __Pyx_PyObject_Call(func, argstuple, kwargs);
  bad:
    Py_DECREF(argstuple);
    return result;
}
#endif
#if CYTHON_VECTORCALL && !CYTHON_COMPILING_IN_LIMITED_API
  #if PY_VERSION_HEX < 0x03090000
    #define __Pyx_PyVectorcall_Function(callable) _PyVectorcall_Function(callable)
  #elif CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE vectorcallfunc __Pyx_PyVectorcall_Function(PyObject *callable) {
    PyTypeObject *tp = Py_TYPE(callable);
    #if defined(__Pyx_CyFunction_USED)
    if (__Pyx_CyFunction_CheckExact(callable)) {
        return __Pyx_CyFunction_func_vectorcall(callable);
    }
    #endif
    if (!PyType_HasFeature(tp, Py_TPFLAGS_HAVE_VECTORCALL)) {
        return NULL;
    }
    assert(PyCallable_Check(callable));
    Py_ssize_t offset = tp->tp_vectorcall_offset;
    assert(offset > 0);
    vectorcallfunc ptr;
    memcpy(&ptr, (char *) callable + offset, sizeof(ptr));
    return ptr;
}
  #else
    #define __Pyx_PyVectorcall_Function(callable) PyVectorcall_Function(callable)
  #endif
#endif
static CYTHON_INLINE PyObject* __Pyx_PyObject_FastCallDict(PyObject *func, PyObject *const *args, size_t _nargs, PyObject *kwargs) {
    Py_ssize_t nargs = __Pyx_PyVectorcall_NARGS(_nargs);
#if CYTHON_COMPILING_IN_CPYTHON
    if (nargs == 0 && kwargs == NULL) {
        if (__Pyx_CyOrPyCFunction_Check(func) && likely( __Pyx_CyOrPyCFunction_GET_FLAGS(func) & METH_NOARGS))
            return __Pyx_PyObject_CallMethO(func, NULL);
    }
    else if (nargs == 1 && kwargs == NULL) {
        if (__Pyx_CyOrPyCFunction_Check(func) && likely( __Pyx_CyOrPyCFunction_GET_FLAGS(func) & METH_O))
            return __Pyx_PyObject_CallMethO(func, args[0]);
    }
#endif
    if (kwargs == NULL) {
        #if CYTHON_VECTORCALL
          #if CYTHON_COMPILING_IN_LIMITED_API
            return PyObject_Vectorcall(func, args, _nargs, NULL);
          #else
            vectorcallfunc f = __Pyx_PyVectorcall_Function(func);
            if (f) {
                return f(func, args, _nargs, NULL);
            }
          #endif
        #endif
    }
    if (nargs == 0) {
        return __Pyx_PyObject_Call(func, __pyx_mstate_global->__pyx_empty_tuple, kwargs);
    }
    #if PY_VERSION_HEX >= 0x03090000 && !CYTHON_COMPILING_IN_LIMITED_API
    return PyObject_VectorcallDict(func, args, (size_t)nargs, kwargs);
    #else
    return __Pyx_PyObject_FastCall_fallback(func, args, (size_t)nargs, kwargs);
    #endif
}

