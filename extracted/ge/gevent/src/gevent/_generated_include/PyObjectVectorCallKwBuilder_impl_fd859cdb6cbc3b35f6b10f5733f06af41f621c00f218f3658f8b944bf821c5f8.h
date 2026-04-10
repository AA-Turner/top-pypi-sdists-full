#if CYTHON_VECTORCALL
static int __Pyx_VectorcallBuilder_AddArg(PyObject *key, PyObject *value, PyObject *builder, PyObject **args, int n) {
    (void)__Pyx_PyObject_FastCallDict;
    if (__Pyx_PyTuple_SET_ITEM(builder, n, key) != (0)) return -1;
    Py_INCREF(key);
    args[n] = value;
    return 0;
}
CYTHON_UNUSED static int __Pyx_VectorcallBuilder_AddArg_Check(PyObject *key, PyObject *value, PyObject *builder, PyObject **args, int n) {
    (void)__Pyx_VectorcallBuilder_AddArgStr;
    if (unlikely(!PyUnicode_Check(key))) {
        PyErr_SetString(PyExc_TypeError, "keywords must be strings");
        return -1;
    }
    return __Pyx_VectorcallBuilder_AddArg(key, value, builder, args, n);
}
static int __Pyx_VectorcallBuilder_AddArgStr(const char *key, PyObject *value, PyObject *builder, PyObject **args, int n) {
    PyObject *pyKey = PyUnicode_FromString(key);
    if (!pyKey) return -1;
    return __Pyx_VectorcallBuilder_AddArg(pyKey, value, builder, args, n);
}
#else // CYTHON_VECTORCALL
CYTHON_UNUSED static int __Pyx_VectorcallBuilder_AddArg_Check(PyObject *key, PyObject *value, PyObject *builder, CYTHON_UNUSED PyObject **args, CYTHON_UNUSED int n) {
    if (unlikely(!PyUnicode_Check(key))) {
        PyErr_SetString(PyExc_TypeError, "keywords must be strings");
        return -1;
    }
    return PyDict_SetItem(builder, key, value);
}
#endif

