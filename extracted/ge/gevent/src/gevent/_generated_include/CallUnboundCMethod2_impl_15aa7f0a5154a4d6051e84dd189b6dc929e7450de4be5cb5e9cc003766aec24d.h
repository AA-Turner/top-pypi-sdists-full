#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject *__Pyx_CallUnboundCMethod2(__Pyx_CachedCFunction *cfunc, PyObject *self, PyObject *arg1, PyObject *arg2) {
    int was_initialized = __Pyx_CachedCFunction_GetAndSetInitializing(cfunc);
    if (likely(was_initialized == 2 && cfunc->func)) {
        PyObject *args[2] = {arg1, arg2};
        if (cfunc->flag == METH_FASTCALL) {
            return __Pyx_CallCFunctionFast(cfunc, self, args, 2);
        }
        if (cfunc->flag == (METH_FASTCALL | METH_KEYWORDS))
            return __Pyx_CallCFunctionFastWithKeywords(cfunc, self, args, 2, NULL);
    }
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
    else if (unlikely(was_initialized == 1)) {
        __Pyx_CachedCFunction tmp_cfunc = {
#ifndef __cplusplus
            0
#endif
        };
        tmp_cfunc.type = cfunc->type;
        tmp_cfunc.method_name = cfunc->method_name;
        return __Pyx__CallUnboundCMethod2(&tmp_cfunc, self, arg1, arg2);
    }
#endif
    PyObject *result = __Pyx__CallUnboundCMethod2(cfunc, self, arg1, arg2);
    __Pyx_CachedCFunction_SetFinishedInitializing(cfunc);
    return result;
}
#endif
static PyObject* __Pyx__CallUnboundCMethod2(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg1, PyObject* arg2){
    if (unlikely(!cfunc->func && !cfunc->method) && unlikely(__Pyx_TryUnpackUnboundCMethod(cfunc) < 0)) return NULL;
#if CYTHON_COMPILING_IN_CPYTHON
    if (cfunc->func && (cfunc->flag & METH_VARARGS)) {
        PyObject *result = NULL;
        PyObject *args = PyTuple_New(2);
        if (unlikely(!args)) return NULL;
        Py_INCREF(arg1);
        PyTuple_SET_ITEM(args, 0, arg1);
        Py_INCREF(arg2);
        PyTuple_SET_ITEM(args, 1, arg2);
        if (cfunc->flag & METH_KEYWORDS)
            result = __Pyx_CallCFunctionWithKeywords(cfunc, self, args, NULL);
        else
            result = __Pyx_CallCFunction(cfunc, self, args);
        Py_DECREF(args);
        return result;
    }
#endif
    {
        PyObject *args[4] = {NULL, self, arg1, arg2};
        return __Pyx_PyObject_FastCall(cfunc->method, args+1, 3 | __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET);
    }
}

