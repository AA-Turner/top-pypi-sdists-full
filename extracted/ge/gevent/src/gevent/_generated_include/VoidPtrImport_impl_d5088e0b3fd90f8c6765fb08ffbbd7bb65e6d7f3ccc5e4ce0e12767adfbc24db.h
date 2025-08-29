#ifndef __PYX_HAVE_RT_ImportVoidPtr_3_1_2
#define __PYX_HAVE_RT_ImportVoidPtr_3_1_2
static int __Pyx_ImportVoidPtr_3_1_2(PyObject *module, const char *name, void **p, const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    d = PyObject_GetAttrString(module, "__pyx_capi__");
    if (!d)
        goto bad;
#if (defined(Py_LIMITED_API) && Py_LIMITED_API >= 0x030d0000) || (!defined(Py_LIMITED_API) && PY_VERSION_HEX >= 0x030d0000)
    PyDict_GetItemStringRef(d, name, &cobj);
#else
    cobj = PyDict_GetItemString(d, name);
    Py_XINCREF(cobj);
#endif
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C variable %.200s",
                PyModule_GetName(module), name);
        goto bad;
    }
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C variable %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), name, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    *p = PyCapsule_GetPointer(cobj, sig);
    if (!(*p))
        goto bad;
    Py_DECREF(d);
    Py_DECREF(cobj);
    return 0;
bad:
    Py_XDECREF(d);
    Py_XDECREF(cobj);
    return -1;
}
#endif

