#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_CallUnboundCMethod0(__Pyx_CachedCFunction* cfunc, PyObject* self) {
    int was_initialized = __Pyx_CachedCFunction_GetAndSetInitializing(cfunc);
    if (likely(was_initialized == 2 && cfunc->func)) {
        if (likely(cfunc->flag == METH_NOARGS))
            return __Pyx_CallCFunction(cfunc, self, NULL);
        if (likely(cfunc->flag == METH_FASTCALL))
            return __Pyx_CallCFunctionFast(cfunc, self, NULL, 0);
        if (cfunc->flag == (METH_FASTCALL | METH_KEYWORDS))
            return __Pyx_CallCFunctionFastWithKeywords(cfunc, self, NULL, 0, NULL);
        if (likely(cfunc->flag == (METH_VARARGS | METH_KEYWORDS)))
            return __Pyx_CallCFunctionWithKeywords(cfunc, self, __pyx_mstate_global->__pyx_empty_tuple, NULL);
        if (cfunc->flag == METH_VARARGS)
            return __Pyx_CallCFunction(cfunc, self, __pyx_mstate_global->__pyx_empty_tuple);
        return __Pyx__CallUnboundCMethod0(cfunc, self);
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
        return __Pyx__CallUnboundCMethod0(&tmp_cfunc, self);
    }
#endif
    PyObject *result = __Pyx__CallUnboundCMethod0(cfunc, self);
    __Pyx_CachedCFunction_SetFinishedInitializing(cfunc);
    return result;
}
#endif
static PyObject* __Pyx__CallUnboundCMethod0(__Pyx_CachedCFunction* cfunc, PyObject* self) {
    PyObject *result;
    if (unlikely(!cfunc->method) && unlikely(__Pyx_TryUnpackUnboundCMethod(cfunc) < 0)) return NULL;
    result = __Pyx_PyObject_CallOneArg(cfunc->method, self);
    return result;
}

