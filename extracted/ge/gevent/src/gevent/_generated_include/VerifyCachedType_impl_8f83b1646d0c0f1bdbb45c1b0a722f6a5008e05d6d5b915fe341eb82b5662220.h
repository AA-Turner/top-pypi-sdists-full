static int __Pyx_VerifyCachedType(PyObject *cached_type,
                               const char *name,
                               Py_ssize_t expected_basicsize) {
    Py_ssize_t basicsize;
    if (!PyType_Check(cached_type)) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s is not a type object", name);
        return -1;
    }
    if (expected_basicsize == 0) {
        return 0; // size is inherited, nothing useful to check
    }
#if CYTHON_COMPILING_IN_LIMITED_API && CYTHON_OPAQUE_OBJECTS
    if (expected_basicsize < 0) {
        basicsize = PyType_GetTypeDataSize((PyTypeObject*)cached_type);
    } else
#endif
    {
    #if CYTHON_COMPILING_IN_LIMITED_API
        PyObject *py_basicsize;
        py_basicsize = PyObject_GetAttrString(cached_type, "__basicsize__");
        if (unlikely(!py_basicsize)) return -1;
        basicsize = PyLong_AsSsize_t(py_basicsize);
        Py_DECREF(py_basicsize);
        py_basicsize = NULL;
        if (unlikely(basicsize == (Py_ssize_t)-1) && PyErr_Occurred()) return -1;
    #else
        basicsize = ((PyTypeObject*) cached_type)->tp_basicsize;
    #endif
    }
    if ((expected_basicsize >= 0) ?
            (basicsize != expected_basicsize) :
            (basicsize < -expected_basicsize)) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s has the wrong size, try recompiling",
            name);
        return -1;
    }
    return 0;
}

