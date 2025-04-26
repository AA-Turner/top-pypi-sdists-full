#if CYTHON_COMPILING_IN_PYPY && PY_VERSION_HEX < 0x02070600 && !defined(Py_OptimizeFlag)
  #define __Pyx_init_assertions_enabled()  (0)
  #define __pyx_assertions_enabled()  (1)
#elif CYTHON_COMPILING_IN_LIMITED_API  ||  (CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030C0000)
  static int __pyx_assertions_enabled_flag;
  #define __pyx_assertions_enabled() (__pyx_assertions_enabled_flag)
  static int __Pyx_init_assertions_enabled(void) {
    PyObject *builtins, *debug, *debug_str;
    int flag;
    builtins = PyEval_GetBuiltins();
    if (!builtins) goto bad;
    debug_str = PyUnicode_FromStringAndSize("__debug__", 9);
    if (!debug_str) goto bad;
    debug = PyObject_GetItem(builtins, debug_str);
    Py_DECREF(debug_str);
    if (!debug) goto bad;
    flag = PyObject_IsTrue(debug);
    Py_DECREF(debug);
    if (flag == -1) goto bad;
    __pyx_assertions_enabled_flag = flag;
    return 0;
  bad:
    __pyx_assertions_enabled_flag = 1;
    return -1;
  }
#else
  #define __Pyx_init_assertions_enabled()  (0)
  #define __pyx_assertions_enabled()  (!Py_OptimizeFlag)
#endif

