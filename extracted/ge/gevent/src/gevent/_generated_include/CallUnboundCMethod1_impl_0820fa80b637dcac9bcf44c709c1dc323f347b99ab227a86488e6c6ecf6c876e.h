#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg) {
    int was_initialized =  __Pyx_CachedCFunction_GetAndSetInitializing(cfunc);
    if (likely(was_initialized == 2 && cfunc->func)) {
        int flag = cfunc->flag;
        if (flag == METH_O) {
            return __Pyx_CallCFunction(cfunc, self, arg);
        } else if (flag == METH_FASTCALL) {
            return __Pyx_CallCFunctionFast(cfunc, self, &arg, 1);
        } else if (flag == (METH_FASTCALL | METH_KEYWORDS)) {
            return __Pyx_CallCFunctionFastWithKeywords(cfunc, self, &arg, 1, NULL);
        }
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
        return __Pyx__CallUnboundCMethod1(&tmp_cfunc, self, arg);
    }
#endif
    PyObject* result = __Pyx__CallUnboundCMethod1(cfunc, self, arg);
    __Pyx_CachedCFunction_SetFinishedInitializing(cfunc);
    return result;
}
#endif
static PyObject* __Pyx__CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg){
    PyObject *result = NULL;
    if (unlikely(!cfunc->func && !cfunc->method) && unlikely(__Pyx_TryUnpackUnboundCMethod(cfunc) < 0)) return NULL;
#if CYTHON_COMPILING_IN_CPYTHON
    if (cfunc->func && (cfunc->flag & METH_VARARGS)) {
        PyObject *args = PyTuple_New(1);
        if (unlikely(!args)) return NULL;
        Py_INCREF(arg);
        PyTuple_SET_ITEM(args, 0, arg);
        if (cfunc->flag & METH_KEYWORDS)
            result = __Pyx_CallCFunctionWithKeywords(cfunc, self, args, NULL);
        else
            result = __Pyx_CallCFunction(cfunc, self, args);
        Py_DECREF(args);
    } else
#endif
    {
        result = __Pyx_PyObject_Call2Args(cfunc->method, self, arg);
    }
    return result;
}

