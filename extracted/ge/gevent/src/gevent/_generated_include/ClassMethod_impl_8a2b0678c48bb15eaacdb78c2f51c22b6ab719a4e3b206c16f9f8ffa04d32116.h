static PyObject* __Pyx_Method_ClassMethod(PyObject *method) {
#if CYTHON_COMPILING_IN_PYPY && PYPY_VERSION_NUM <= 0x05080000
    if (PyObject_TypeCheck(method, &PyWrapperDescr_Type)) {
        return PyClassMethod_New(method);
    }
#else
#if CYTHON_COMPILING_IN_PYPY
    if (PyMethodDescr_Check(method))
#else
    if (__Pyx_TypeCheck(method, &PyMethodDescr_Type))
#endif
    {
#if CYTHON_COMPILING_IN_LIMITED_API
        return PyErr_Format(
            PyExc_SystemError,
            "Cython cannot yet handle classmethod on a MethodDescriptorType (%S) in limited API mode. "
            "This is most likely a classmethod in a cdef class method with binding=False. "
            "Try setting 'binding' to True.",
            method);
#elif CYTHON_COMPILING_IN_GRAAL && defined(GRAALPY_VERSION_NUM) && GRAALPY_VERSION_NUM > 0x19000000
        PyTypeObject *d_type = GraalPyDescrObject_GetType(method);
        return PyDescr_NewClassMethod(d_type, GraalPyMethodDescrObject_GetMethod(method));
#elif CYTHON_COMPILING_IN_GRAAL
        PyTypeObject *d_type = PyDescrObject_GetType(method);
        return PyDescr_NewClassMethod(d_type, PyMethodDescrObject_GetMethod(method));
#else
        PyMethodDescrObject *descr = (PyMethodDescrObject *)method;
        PyTypeObject *d_type = descr->d_common.d_type;
        return PyDescr_NewClassMethod(d_type, descr->d_method);
#endif
    }
#endif
#if !CYTHON_COMPILING_IN_LIMITED_API
    else if (PyMethod_Check(method)) {
        return PyClassMethod_New(PyMethod_GET_FUNCTION(method));
    }
    else {
        return PyClassMethod_New(method);
    }
#else
    {
        PyObject *func=NULL;
        PyObject *builtins, *classmethod, *classmethod_str, *result=NULL;
        if (__Pyx_TypeCheck(method, __pyx_mstate_global->__Pyx_CachedMethodType)) {
            func = PyObject_GetAttrString(method, "__func__");
            if (!func) goto bad;
        } else {
            func = method;
            Py_INCREF(func);
        }
        builtins = PyEval_GetBuiltins(); // borrowed
        if (unlikely(!builtins)) goto bad;
        classmethod_str = PyUnicode_FromString("classmethod");
        if (unlikely(!classmethod_str)) goto bad;
        classmethod = PyObject_GetItem(builtins, classmethod_str);
        Py_DECREF(classmethod_str);
        if (unlikely(!classmethod)) goto bad;
        result = PyObject_CallFunctionObjArgs(classmethod, func, NULL);
        Py_DECREF(classmethod);
        bad:
        Py_XDECREF(func);
        return result;
    }
#endif
}

