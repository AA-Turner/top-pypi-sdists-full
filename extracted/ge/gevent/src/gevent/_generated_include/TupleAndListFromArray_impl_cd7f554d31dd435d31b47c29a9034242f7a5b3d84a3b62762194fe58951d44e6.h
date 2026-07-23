#if !CYTHON_COMPILING_IN_CPYTHON && CYTHON_METH_FASTCALL
static CYTHON_INLINE PyObject *
__Pyx_PyTuple_FromArray(PyObject *const *src, Py_ssize_t n)
{
    PyObject *res;
    Py_ssize_t i;
    if (n <= 0) {
        return __Pyx_NewRef(__pyx_mstate_global->__pyx_empty_tuple);
    }
    res = PyTuple_New(n);
    if (unlikely(res == NULL)) return NULL;
    for (i = 0; i < n; i++) {
        Py_INCREF(src[i]);
        if (unlikely(__Pyx_PyTuple_SET_ITEM(res, i, src[i]) < (0))) {
            Py_DECREF(res);
            return NULL;
        }
    }
    return res;
}
#elif CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE void __Pyx_copy_object_array(PyObject *const *CYTHON_RESTRICT src, PyObject** CYTHON_RESTRICT dest, Py_ssize_t length) {
    PyObject *v;
    Py_ssize_t i;
    for (i = 0; i < length; i++) {
        v = dest[i] = src[i];
        Py_INCREF(v);
    }
}
static CYTHON_INLINE PyObject *
__Pyx_PyTuple_FromArray(PyObject *const *src, Py_ssize_t n)
{
    PyObject *res;
    if (n <= 0) {
        return __Pyx_NewRef(__pyx_mstate_global->__pyx_empty_tuple);
    }
    res = PyTuple_New(n);
    if (unlikely(res == NULL)) return NULL;
    __Pyx_copy_object_array(src, ((PyTupleObject*)res)->ob_item, n);
    return res;
}
static CYTHON_INLINE PyObject *
__Pyx_PyList_FromArray(PyObject *const *src, Py_ssize_t n)
{
    PyObject *res;
    if (n <= 0) {
        return PyList_New(0);
    }
    res = PyList_New(n);
    if (unlikely(res == NULL)) return NULL;
    __Pyx_copy_object_array(src, ((PyListObject*)res)->ob_item, n);
    return res;
}
#endif

