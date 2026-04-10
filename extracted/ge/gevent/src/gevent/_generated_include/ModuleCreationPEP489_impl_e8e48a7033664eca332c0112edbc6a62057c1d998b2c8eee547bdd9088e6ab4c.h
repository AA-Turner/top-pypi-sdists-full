#if CYTHON_COMPILING_IN_LIMITED_API && (__PYX_LIMITED_VERSION_HEX < 0x03090000\
      || ((defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)) && __PYX_LIMITED_VERSION_HEX < 0x030A0000))
static PY_INT64_T __Pyx_GetCurrentInterpreterId(void) {
    {
        PyObject *module = PyImport_ImportModule("_interpreters"); // 3.13+ I think
        if (!module) {
            PyErr_Clear(); // just try the 3.8-3.12 version
            module = PyImport_ImportModule("_xxsubinterpreters");
            if (!module) goto bad;
        }
        PyObject *current = PyObject_CallMethod(module, "get_current", NULL);
        Py_DECREF(module);
        if (!current) goto bad;
        if (PyTuple_Check(current)) {
            PyObject *new_current = PySequence_GetItem(current, 0);
            Py_DECREF(current);
            current = new_current;
            if (!new_current) goto bad;
        }
        long long as_c_int = PyLong_AsLongLong(current);
        Py_DECREF(current);
        return as_c_int;
    }
  bad:
    PySys_WriteStderr("__Pyx_GetCurrentInterpreterId failed. Try setting the C define CYTHON_PEP489_MULTI_PHASE_INIT=0\n");
    return -1;
}
#endif
#if !CYTHON_USE_MODULE_STATE
static CYTHON_SMALL_CODE int __Pyx_check_single_interpreter(void) {
    static PY_INT64_T main_interpreter_id = -1;
#if CYTHON_COMPILING_IN_GRAAL && defined(GRAALPY_VERSION_NUM) && GRAALPY_VERSION_NUM > 0x19000000
    PY_INT64_T current_id = GraalPyInterpreterState_GetIDFromThreadState(PyThreadState_Get());
#elif CYTHON_COMPILING_IN_GRAAL
    PY_INT64_T current_id = PyInterpreterState_GetIDFromThreadState(PyThreadState_Get());
#elif CYTHON_COMPILING_IN_LIMITED_API && (__PYX_LIMITED_VERSION_HEX < 0x03090000\
      || ((defined(_WIN32) || defined(WIN32) || defined(MS_WINDOWS)) && __PYX_LIMITED_VERSION_HEX < 0x030A0000))
    PY_INT64_T current_id = __Pyx_GetCurrentInterpreterId();
#elif CYTHON_COMPILING_IN_LIMITED_API
    PY_INT64_T current_id = PyInterpreterState_GetID(PyInterpreterState_Get());
#else
    PY_INT64_T current_id = PyInterpreterState_GetID(PyThreadState_Get()->interp);
#endif
    if (unlikely(current_id == -1)) {
        return -1;
    }
    if (main_interpreter_id == -1) {
        main_interpreter_id = current_id;
        return 0;
    } else if (unlikely(main_interpreter_id != current_id)) {
        PyErr_SetString(
            PyExc_ImportError,
            "Interpreter change detected - this module can only be loaded into one interpreter per process.");
        return -1;
    }
    return 0;
}
#endif
static CYTHON_SMALL_CODE int __Pyx_copy_spec_to_module(PyObject *spec, PyObject *moddict, const char* from_name, const char* to_name, int allow_none)
{
    PyObject *value = PyObject_GetAttrString(spec, from_name);
    int result = 0;
    if (likely(value)) {
        if (allow_none || value != Py_None) {
            result = PyDict_SetItemString(moddict, to_name, value);
        }
        Py_DECREF(value);
    } else if (PyErr_ExceptionMatches(PyExc_AttributeError)) {
        PyErr_Clear();
    } else {
        result = -1;
    }
    return result;
}
static CYTHON_SMALL_CODE PyObject* __pyx_pymod_create(PyObject *spec, PyModuleDef *def) {
    PyObject *module = NULL, *moddict, *modname;
    CYTHON_UNUSED_VAR(def);
    #if !CYTHON_USE_MODULE_STATE
    if (__Pyx_check_single_interpreter())
        return NULL;
    #endif
    if (__pyx_m)
        return __Pyx_NewRef(__pyx_m);
    modname = PyObject_GetAttrString(spec, "name");
    if (unlikely(!modname)) goto bad;
    module = PyModule_NewObject(modname);
    Py_DECREF(modname);
    if (unlikely(!module)) goto bad;
    moddict = PyModule_GetDict(module);
    if (unlikely(!moddict)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "loader", "__loader__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "origin", "__file__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "parent", "__package__", 1) < 0)) goto bad;
    if (unlikely(__Pyx_copy_spec_to_module(spec, moddict, "submodule_search_locations", "__path__", 0) < 0)) goto bad;
    return module;
bad:
    Py_XDECREF(module);
    return NULL;
}

