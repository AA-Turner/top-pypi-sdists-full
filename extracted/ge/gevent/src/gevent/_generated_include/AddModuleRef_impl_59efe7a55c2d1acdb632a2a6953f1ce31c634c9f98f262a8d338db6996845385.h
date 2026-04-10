#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
  static PyObject *__Pyx_PyImport_AddModuleObjectRef(PyObject *name) {
      PyObject *module_dict = PyImport_GetModuleDict();
      PyObject *m;
      if (PyMapping_GetOptionalItem(module_dict, name, &m) < 0) {
          return NULL;
      }
      if (m != NULL && PyModule_Check(m)) {
          return m;
      }
      Py_XDECREF(m);
      m = PyModule_NewObject(name);
      if (m == NULL)
          return NULL;
      if (PyDict_CheckExact(module_dict)) {
          PyObject *new_m;
          (void)PyDict_SetDefaultRef(module_dict, name, m, &new_m);
          Py_DECREF(m);
          return new_m;
      } else {
           if (PyObject_SetItem(module_dict, name, m) != 0) {
                Py_DECREF(m);
                return NULL;
            }
            return m;
      }
  }
  static PyObject *__Pyx_PyImport_AddModuleRef(const char *name) {
      PyObject *py_name = PyUnicode_FromString(name);
      if (!py_name) return NULL;
      PyObject *module = __Pyx_PyImport_AddModuleObjectRef(py_name);
      Py_DECREF(py_name);
      return module;
  }
#elif __PYX_LIMITED_VERSION_HEX >= 0x030d0000
  #define __Pyx_PyImport_AddModuleRef(name) PyImport_AddModuleRef(name)
#else
  static PyObject *__Pyx_PyImport_AddModuleRef(const char *name) {
      PyObject *module = PyImport_AddModule(name);
      Py_XINCREF(module);
      return module;
  }
#endif

