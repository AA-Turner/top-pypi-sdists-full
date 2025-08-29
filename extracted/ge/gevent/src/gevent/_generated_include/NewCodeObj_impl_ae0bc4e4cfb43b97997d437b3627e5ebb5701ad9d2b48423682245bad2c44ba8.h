#if CYTHON_COMPILING_IN_LIMITED_API
    static PyObject* __Pyx__PyCode_New(int a, int p, int k, int l, int s, int f,
                                       PyObject *code, PyObject *c, PyObject* n, PyObject *v,
                                       PyObject *fv, PyObject *cell, PyObject* fn,
                                       PyObject *name, int fline, PyObject *lnos) {
        PyObject *exception_table = NULL;
        PyObject *types_module=NULL, *code_type=NULL, *result=NULL;
        #if __PYX_LIMITED_VERSION_HEX < 0x030b0000
        PyObject *version_info;
        PyObject *py_minor_version = NULL;
        #endif
        long minor_version = 0;
        PyObject *type, *value, *traceback;
        PyErr_Fetch(&type, &value, &traceback);
        #if __PYX_LIMITED_VERSION_HEX >= 0x030b0000
        minor_version = 11;
        #else
        if (!(version_info = PySys_GetObject("version_info"))) goto end;
        if (!(py_minor_version = PySequence_GetItem(version_info, 1))) goto end;
        minor_version = PyLong_AsLong(py_minor_version);
        Py_DECREF(py_minor_version);
        if (minor_version == -1 && PyErr_Occurred()) goto end;
        #endif
        if (!(types_module = PyImport_ImportModule("types"))) goto end;
        if (!(code_type = PyObject_GetAttrString(types_module, "CodeType"))) goto end;
        if (minor_version <= 7) {
            (void)p;
            result = PyObject_CallFunction(code_type, "iiiiiOOOOOOiOOO", a, k, l, s, f, code,
                          c, n, v, fn, name, fline, lnos, fv, cell);
        } else if (minor_version <= 10) {
            result = PyObject_CallFunction(code_type, "iiiiiiOOOOOOiOOO", a,p, k, l, s, f, code,
                          c, n, v, fn, name, fline, lnos, fv, cell);
        } else {
            if (!(exception_table = PyBytes_FromStringAndSize(NULL, 0))) goto end;
            result = PyObject_CallFunction(code_type, "iiiiiiOOOOOOOiOOOO", a,p, k, l, s, f, code,
                          c, n, v, fn, name, name, fline, lnos, exception_table, fv, cell);
        }
    end:
        Py_XDECREF(code_type);
        Py_XDECREF(exception_table);
        Py_XDECREF(types_module);
        if (type) {
            PyErr_Restore(type, value, traceback);
        }
        return result;
    }
#elif PY_VERSION_HEX >= 0x030B0000
  static PyCodeObject* __Pyx__PyCode_New(int a, int p, int k, int l, int s, int f,
                                         PyObject *code, PyObject *c, PyObject* n, PyObject *v,
                                         PyObject *fv, PyObject *cell, PyObject* fn,
                                         PyObject *name, int fline, PyObject *lnos) {
    PyCodeObject *result;
    result =
      #if PY_VERSION_HEX >= 0x030C0000
        PyUnstable_Code_NewWithPosOnlyArgs
      #else
        PyCode_NewWithPosOnlyArgs
      #endif
        (a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, name, fline, lnos, __pyx_mstate_global->__pyx_empty_bytes);
    return result;
  }
#elif PY_VERSION_HEX >= 0x030800B2 && !CYTHON_COMPILING_IN_PYPY
  #define __Pyx__PyCode_New(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_NewWithPosOnlyArgs(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#else
  #define __Pyx__PyCode_New(a, p, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)\
          PyCode_New(a, k, l, s, f, code, c, n, v, fv, cell, fn, name, fline, lnos)
#endif
static PyObject* __Pyx_PyCode_New(
        const __Pyx_PyCode_New_function_description descr,
        PyObject * const *varnames,
        PyObject *filename,
        PyObject *funcname,
        const char *line_table,
        PyObject *tuple_dedup_map
) {
    PyObject *code_obj = NULL, *varnames_tuple_dedup = NULL, *code_bytes = NULL, *line_table_bytes = NULL;
    Py_ssize_t var_count = (Py_ssize_t) descr.nlocals;
    PyObject *varnames_tuple = PyTuple_New(var_count);
    if (unlikely(!varnames_tuple)) return NULL;
    for (Py_ssize_t i=0; i < var_count; i++) {
        Py_INCREF(varnames[i]);
        if (__Pyx_PyTuple_SET_ITEM(varnames_tuple, i, varnames[i]) != (0)) goto done;
    }
    #if CYTHON_COMPILING_IN_LIMITED_API
    varnames_tuple_dedup = PyDict_GetItem(tuple_dedup_map, varnames_tuple);
    if (!varnames_tuple_dedup) {
        if (unlikely(PyDict_SetItem(tuple_dedup_map, varnames_tuple, varnames_tuple) < 0)) goto done;
        varnames_tuple_dedup = varnames_tuple;
    }
    #else
    varnames_tuple_dedup = PyDict_SetDefault(tuple_dedup_map, varnames_tuple, varnames_tuple);
    if (unlikely(!varnames_tuple_dedup)) goto done;
    #endif
    #if CYTHON_AVOID_BORROWED_REFS
    Py_INCREF(varnames_tuple_dedup);
    #endif
    if (__PYX_LIMITED_VERSION_HEX >= (0x030b0000) && line_table != NULL
        && !CYTHON_COMPILING_IN_GRAAL) {
        line_table_bytes = PyBytes_FromStringAndSize(line_table, descr.line_table_length);
        if (unlikely(!line_table_bytes)) goto done;
        Py_ssize_t code_len = (descr.line_table_length * 2 + 4) & ~3;
        code_bytes = PyBytes_FromStringAndSize(NULL, code_len);
        if (unlikely(!code_bytes)) goto done;
        char* c_code_bytes = PyBytes_AsString(code_bytes);
        if (unlikely(!c_code_bytes)) goto done;
        memset(c_code_bytes, 0, (size_t) code_len);
    }
    code_obj = (PyObject*) __Pyx__PyCode_New(
        (int) descr.argcount,
        (int) descr.num_posonly_args,
        (int) descr.num_kwonly_args,
        (int) descr.nlocals,
        0,
        (int) descr.flags,
        code_bytes ? code_bytes : __pyx_mstate_global->__pyx_empty_bytes,
        __pyx_mstate_global->__pyx_empty_tuple,
        __pyx_mstate_global->__pyx_empty_tuple,
        varnames_tuple_dedup,
        __pyx_mstate_global->__pyx_empty_tuple,
        __pyx_mstate_global->__pyx_empty_tuple,
        filename,
        funcname,
        (int) descr.first_line,
        (__PYX_LIMITED_VERSION_HEX >= (0x030b0000) && line_table_bytes) ? line_table_bytes : __pyx_mstate_global->__pyx_empty_bytes
    );
done:
    Py_XDECREF(code_bytes);
    Py_XDECREF(line_table_bytes);
    #if CYTHON_AVOID_BORROWED_REFS
    Py_XDECREF(varnames_tuple_dedup);
    #endif
    Py_DECREF(varnames_tuple);
    return code_obj;
}

