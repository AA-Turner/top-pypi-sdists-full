static double __Pyx_SlowPyString_AsDouble(PyObject *obj);
static double __Pyx__PyBytes_AsDouble(PyObject *obj, const char* start, Py_ssize_t length);
static CYTHON_INLINE double __Pyx_PyBytes_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE
    as_c_string = PyBytes_AS_STRING(obj);
    size = PyBytes_GET_SIZE(obj);
#else
    if (PyBytes_AsStringAndSize(obj, &as_c_string, &size) < 0) {
        return (double)-1;
    }
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}
static CYTHON_INLINE double __Pyx_PyByteArray_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE
    as_c_string = PyByteArray_AS_STRING(obj);
    size = PyByteArray_GET_SIZE(obj);
#else
    as_c_string = PyByteArray_AsString(obj);
    if (as_c_string == NULL) {
        return (double)-1;
    }
    size = PyByteArray_Size(obj);
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}

