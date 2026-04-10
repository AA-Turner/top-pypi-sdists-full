static int __Pyx__Import_GetModule(PyObject *qualname, PyObject **module) {
    PyObject *imported_module = PyImport_GetModule(qualname);
    if (unlikely(!imported_module)) {
        *module = NULL;
        if (PyErr_Occurred()) {
            return -1;
        }
        return 0;
    }
    *module = imported_module;
    return 1;
}
static int __Pyx__Import_Lookup(PyObject *qualname, PyObject *const *imported_names, Py_ssize_t len_imported_names, PyObject **module) {
    PyObject *imported_module;
    PyObject *top_level_package_name;
    Py_ssize_t i;
    int status, module_found;
    Py_ssize_t dot_index;
    module_found = __Pyx__Import_GetModule(qualname, &imported_module);
    if (unlikely(!module_found || module_found == -1)) {
        *module = NULL;
        return module_found;
    }
    if (imported_names) {
        for (i = 0; i < len_imported_names; i++) {
            PyObject *imported_name = imported_names[i];
#if __PYX_LIMITED_VERSION_HEX < 0x030d0000
            int has_imported_attribute = PyObject_HasAttr(imported_module, imported_name);
#else
            int has_imported_attribute = PyObject_HasAttrWithError(imported_module, imported_name);
            if (unlikely(has_imported_attribute == -1)) goto error;
#endif
            if (!has_imported_attribute) {
                goto not_found;
            }
        }
        *module = imported_module;
        return 1;
    }
    dot_index = PyUnicode_FindChar(qualname, '.', 0, PY_SSIZE_T_MAX, 1);
    if (dot_index == -1) {
        *module = imported_module;
        return 1;
    }
    if (unlikely(dot_index == -2)) goto error;
    top_level_package_name = PyUnicode_Substring(qualname, 0, dot_index);
    if (unlikely(!top_level_package_name)) goto error;
    Py_DECREF(imported_module);
    status = __Pyx__Import_GetModule(top_level_package_name, module);
    Py_DECREF(top_level_package_name);
    return status;
error:
    Py_DECREF(imported_module);
    *module = NULL;
    return -1;
not_found:
    Py_DECREF(imported_module);
    *module = NULL;
    return 0;
}
static PyObject *__Pyx__Import(PyObject *name, PyObject *const *imported_names, Py_ssize_t len_imported_names, PyObject *qualname, PyObject *moddict, int level) {
    PyObject *module = 0;
    PyObject *empty_dict = 0;
    PyObject *from_list = 0;
    int module_found;
    if (!qualname) {
        qualname = name;
    }
    module_found = __Pyx__Import_Lookup(qualname, imported_names, len_imported_names, &module);
    if (likely(module_found == 1)) {
        return module;
    } else if (unlikely(module_found == -1)) {
        return NULL;
    }
    empty_dict = PyDict_New();
    if (unlikely(!empty_dict))
        goto bad;
    if (imported_names) {
#if CYTHON_COMPILING_IN_CPYTHON
        from_list = __Pyx_PyList_FromArray(imported_names, len_imported_names);
        if (unlikely(!from_list))
            goto bad;
#else
        from_list = PyList_New(len_imported_names);
        if (unlikely(!from_list)) goto bad;
        for (Py_ssize_t i=0; i<len_imported_names; ++i) {
            if (PyList_SetItem(from_list, i, __Pyx_NewRef(imported_names[i])) < 0) goto bad;
        }
#endif
    }
    if (level == -1) {
        const char* package_sep = strchr(__Pyx_MODULE_NAME, '.');
        if (package_sep != (0)) {
            module = PyImport_ImportModuleLevelObject(
                name, moddict, empty_dict, from_list, 1);
            if (unlikely(!module)) {
                if (unlikely(!PyErr_ExceptionMatches(PyExc_ImportError)))
                    goto bad;
                PyErr_Clear();
            }
        }
        level = 0;
    }
    if (!module) {
        module = PyImport_ImportModuleLevelObject(
            name, moddict, empty_dict, from_list, level);
    }
bad:
    Py_XDECREF(from_list);
    Py_XDECREF(empty_dict);
    return module;
}

