#if CYTHON_COMPILING_IN_LIMITED_API
static Py_ssize_t __Pyx_GetTypeDictOffset(void) {
    PyObject *tp_dictoffset_o;
    Py_ssize_t tp_dictoffset;
    tp_dictoffset_o = PyObject_GetAttrString((PyObject*)(&PyType_Type), "__dictoffset__");
    if (unlikely(!tp_dictoffset_o)) return -1;
    tp_dictoffset = PyLong_AsSsize_t(tp_dictoffset_o);
    Py_DECREF(tp_dictoffset_o);
    if (unlikely(tp_dictoffset == 0)) {
        PyErr_SetString(
            PyExc_TypeError,
            "'type' doesn't have a dictoffset");
        return -1;
    } else if (unlikely(tp_dictoffset < 0)) {
        PyErr_SetString(
            PyExc_TypeError,
            "'type' has an unexpected negative dictoffset. "
            "Please report this as Cython bug");
        return -1;
    }
    return tp_dictoffset;
}
static PyObject *__Pyx_GetTypeDict(PyTypeObject *tp) {
    static Py_ssize_t tp_dictoffset = 0;
    if (unlikely(tp_dictoffset == 0)) {
        tp_dictoffset = __Pyx_GetTypeDictOffset();
        if (unlikely(tp_dictoffset == -1 && PyErr_Occurred())) {
            tp_dictoffset = 0; // try again next time?
            return NULL;
        }
    }
    return *(PyObject**)((char*)tp + tp_dictoffset);
}
#endif

