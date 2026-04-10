static CYTHON_INLINE PyObject* __Pyx_PyFrozenSet_New(PyObject* it) {
    if (it) {
        PyObject* result;
#if CYTHON_COMPILING_IN_PYPY
        PyObject* args;
        args = PyTuple_Pack(1, it);
        if (unlikely(!args))
            return NULL;
        result = PyObject_Call((PyObject*)&PyFrozenSet_Type, args, NULL);
        Py_DECREF(args);
        return result;
#else
        if (PyFrozenSet_CheckExact(it)) {
            Py_INCREF(it);
            return it;
        }
        result = PyFrozenSet_New(it);
        if (unlikely(!result))
            return NULL;
        if ((__PYX_LIMITED_VERSION_HEX >= 0x030A0000)
#if CYTHON_COMPILING_IN_LIMITED_API
            || __Pyx_get_runtime_version() >= 0x030A0000
#endif
            )
            return result;
        {
            Py_ssize_t size = __Pyx_PySet_GET_SIZE(result);
            if (likely(size > 0))
                return result;
#if !CYTHON_ASSUME_SAFE_SIZE
            if (unlikely(size < 0)) {
                Py_DECREF(result);
                return NULL;
            }
#endif
        }
        Py_DECREF(result);
#endif
    }
    return __Pyx_PyObject_CallNoArg((PyObject*) &PyFrozenSet_Type);
}

