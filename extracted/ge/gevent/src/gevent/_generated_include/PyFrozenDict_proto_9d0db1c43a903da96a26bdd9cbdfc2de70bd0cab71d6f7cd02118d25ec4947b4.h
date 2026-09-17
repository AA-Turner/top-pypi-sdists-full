#if CYTHON_COMPILING_IN_LIMITED_API
#define __Pyx_PyFrozenDict_TypePtr  ((PyTypeObject*) __pyx_mstate_global->__Pyx_PyFrozenDictType)
#define __Pyx_PyFrozenDict_New(it)  __Pyx__PyFrozenDict_New(__pyx_mstate_global->__Pyx_PyFrozenDictType, it)
static CYTHON_INLINE PyObject* __Pyx__PyFrozenDict_New(PyObject* frozendict_type, PyObject* it);
#define __Pyx_PyFrozenDict_NewEmpty()  __Pyx_PyFrozenDict_New(NULL)
#define __Pyx_PyFrozenDict_Check(obj)  PyObject_TypeCheck((obj), __Pyx_PyFrozenDict_TypePtr)
#define __Pyx_PyFrozenDict_CheckExact(obj)  Py_IS_TYPE((obj), __Pyx_PyFrozenDict_TypePtr)
#define __Pyx_PyAnyDict_Check(obj)   __Pyx__PyAnyDict_Check(obj, __Pyx_PyFrozenDict_TypePtr)
static CYTHON_INLINE int __Pyx__PyAnyDict_Check(PyObject *obj, PyTypeObject* frozendict_type) {
    return PyObject_TypeCheck(obj, &PyDict_Type) || PyObject_TypeCheck(obj, frozendict_type);
}
#define __Pyx_PyAnyDict_CheckExact(obj)  __Pyx__PyAnyDict_CheckExact(obj, __Pyx_PyFrozenDict_TypePtr)
static CYTHON_INLINE int __Pyx__PyAnyDict_CheckExact(PyObject *obj, PyTypeObject* frozendict_type) {
    return Py_IS_TYPE(obj, &PyDict_Type) || Py_IS_TYPE(obj, frozendict_type);
}
#elif PY_VERSION_HEX >= 0x030f00a6 ||\
    (defined(PyFrozenDict_Check) && defined(PyAnyDict_Check) && defined(PyFrozenDict_New))
#define __Pyx_PyFrozenDict_TypePtr  (&PyFrozenDict_Type)
#define __Pyx_PyFrozenDict_New(it)  PyFrozenDict_New(it)
#define __Pyx_PyFrozenDict_NewEmpty()  PyFrozenDict_New(NULL)
#define __Pyx_PyFrozenDict_Check(obj)  PyFrozenDict_Check(obj)
#define __Pyx_PyFrozenDict_CheckExact(obj)  PyFrozenDict_CheckExact(obj)
#define __Pyx_PyAnyDict_Check(obj)  PyAnyDict_Check(obj)
#define __Pyx_PyAnyDict_CheckExact(obj)  PyAnyDict_CheckExact(obj)
#else
#define __Pyx_PyFrozenDict_TypePtr  (&PyDict_Type)
static CYTHON_INLINE PyObject* __Pyx_PyFrozenDict_New(PyObject* it) {
    if (!it) {
        return PyDict_New();
    } else if (PyDict_Check(it)) {
        return PyDict_Copy(it);
    } else {
        PyObject *dict = PyDict_New();
        if (!dict) return NULL;
        PyObject *result = PyNumber_InPlaceOr(dict, it);
        Py_DECREF(dict);
        return result;
    }
}
#define __Pyx_PyFrozenDict_NewEmpty()  PyDict_New()
#define __Pyx_PyFrozenDict_Check(obj)  PyDict_Check(obj)
#define __Pyx_PyFrozenDict_CheckExact(obj)  PyDict_CheckExact(obj)
#define __Pyx_PyAnyDict_Check(obj)  PyDict_Check(obj)
#define __Pyx_PyAnyDict_CheckExact(obj)  PyDict_CheckExact(obj)
#endif

