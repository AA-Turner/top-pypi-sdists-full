static int __Pyx_SetNewInClass(PyObject *ns, PyObject *name, PyObject *value) {
#ifdef __Pyx_CyFunction_USED
    int ret;
    if (__Pyx_CyFunction_Check(value)) {
        PyObject *staticnew;
#if !CYTHON_COMPILING_IN_LIMITED_API
        staticnew = PyStaticMethod_New(value);
#else
        PyObject *builtins, *staticmethod_str, *staticmethod;
        builtins = PyEval_GetBuiltins(); // borrowed
        if (!builtins) return -1;
        staticmethod_str = PyUnicode_FromStringAndSize("staticmethod", 12);
        if (!staticmethod_str) return -1;
        staticmethod = PyObject_GetItem(builtins, staticmethod_str);
        Py_DECREF(staticmethod_str);
        if (!staticmethod) return -1;
        staticnew = PyObject_CallFunctionObjArgs(staticmethod, value, NULL);
        Py_DECREF(staticmethod);
#endif
        if (unlikely(!staticnew)) return -1;
        ret = __Pyx_SetNameInClass(ns, name, staticnew);
        Py_DECREF(staticnew);
        return ret;
    }
#endif
    return __Pyx_SetNameInClass(ns, name, value);
}

