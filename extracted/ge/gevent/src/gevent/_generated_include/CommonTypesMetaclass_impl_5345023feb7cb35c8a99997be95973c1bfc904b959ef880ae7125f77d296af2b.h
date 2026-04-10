static PyObject* __pyx_CommonTypesMetaclass_get_module(CYTHON_UNUSED PyObject *self, CYTHON_UNUSED void* context) {
    return PyUnicode_FromString(__PYX_ABI_MODULE_NAME);
}
#if __PYX_LIMITED_VERSION_HEX < 0x030A0000
static PyObject* __pyx_CommonTypesMetaclass_call(CYTHON_UNUSED PyObject *self, CYTHON_UNUSED PyObject *args, CYTHON_UNUSED PyObject *kwds) {
    PyErr_SetString(PyExc_TypeError, "Cannot instantiate Cython internal types");
    return NULL;
}
static int __pyx_CommonTypesMetaclass_setattr(CYTHON_UNUSED PyObject *self, CYTHON_UNUSED PyObject *attr, CYTHON_UNUSED PyObject *value) {
    PyErr_SetString(PyExc_TypeError, "Cython internal types are immutable");
    return -1;
}
#endif
static PyGetSetDef __pyx_CommonTypesMetaclass_getset[] = {
    {"__module__", __pyx_CommonTypesMetaclass_get_module, NULL, NULL, NULL},
    {0, 0, 0, 0, 0}
};
static PyType_Slot __pyx_CommonTypesMetaclass_slots[] = {
    {Py_tp_getset, (void *)__pyx_CommonTypesMetaclass_getset},
    #if __PYX_LIMITED_VERSION_HEX < 0x030A0000
    {Py_tp_call, (void*)__pyx_CommonTypesMetaclass_call},
    {Py_tp_new, (void*)__pyx_CommonTypesMetaclass_call},
    {Py_tp_setattro, (void*)__pyx_CommonTypesMetaclass_setattr},
    #endif
    {0, 0}
};
static PyType_Spec __pyx_CommonTypesMetaclass_spec = {
    __PYX_TYPE_MODULE_PREFIX "_common_types_metatype",
    0,
    0,
    Py_TPFLAGS_IMMUTABLETYPE |
    Py_TPFLAGS_DISALLOW_INSTANTIATION |
    Py_TPFLAGS_DEFAULT,
    __pyx_CommonTypesMetaclass_slots
};
static int __pyx_CommonTypesMetaclass_init(PyObject *module) {
    __pyx_mstatetype *mstate = __Pyx_PyModule_GetState(module);
    PyObject *bases = PyTuple_Pack(1, &PyType_Type);
    if (unlikely(!bases)) {
        return -1;
    }
    mstate->__pyx_CommonTypesMetaclassType = __Pyx_FetchCommonTypeFromSpec(NULL, module, &__pyx_CommonTypesMetaclass_spec, bases);
    Py_DECREF(bases);
    if (unlikely(mstate->__pyx_CommonTypesMetaclassType == NULL)) {
        return -1;
    }
    return 0;
}

