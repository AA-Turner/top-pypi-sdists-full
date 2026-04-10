#if CYTHON_COMPILING_IN_PYPY
#include <string.h>
#endif
static CYTHON_INLINE PyObject* __Pyx_dict_iterator(PyObject* iterable, int is_dict, PyObject* method_name,
                                                   Py_ssize_t* p_orig_length, int* p_source_is_dict) {
    is_dict = is_dict || likely(PyDict_CheckExact(iterable));
    *p_source_is_dict = is_dict;
    if (is_dict) {
#if !CYTHON_COMPILING_IN_PYPY
        *p_orig_length = PyDict_Size(iterable);
        Py_INCREF(iterable);
        return iterable;
#else
        static PyObject *py_items = NULL, *py_keys = NULL, *py_values = NULL;
        PyObject **pp = NULL;
        if (method_name) {
            const char *name = PyUnicode_AsUTF8(method_name);
            if (strcmp(name, "iteritems") == 0) pp = &py_items;
            else if (strcmp(name, "iterkeys") == 0) pp = &py_keys;
            else if (strcmp(name, "itervalues") == 0) pp = &py_values;
            if (pp) {
                if (!*pp) {
                    *pp = PyUnicode_FromString(name + 4);
                    if (!*pp)
                        return NULL;
                }
                method_name = *pp;
            }
        }
#endif
    }
    *p_orig_length = 0;
    if (method_name) {
        PyObject* iter;
        iterable = __Pyx_PyObject_CallMethod0(iterable, method_name);
        if (!iterable)
            return NULL;
#if !CYTHON_COMPILING_IN_PYPY
        if (PyTuple_CheckExact(iterable) || PyList_CheckExact(iterable))
            return iterable;
#endif
        iter = PyObject_GetIter(iterable);
        Py_DECREF(iterable);
        return iter;
    }
    return PyObject_GetIter(iterable);
}
#if !CYTHON_AVOID_BORROWED_REFS
static CYTHON_INLINE int __Pyx_dict_iter_next_source_is_dict(
        PyObject* iter_obj, CYTHON_NCP_UNUSED Py_ssize_t orig_length, CYTHON_NCP_UNUSED Py_ssize_t* ppos,
        PyObject** pkey, PyObject** pvalue, PyObject** pitem) {
    PyObject *key, *value;
    if (unlikely(orig_length != PyDict_Size(iter_obj))) {
        PyErr_SetString(PyExc_RuntimeError, "dictionary changed size during iteration");
        return -1;
    }
    if (unlikely(!PyDict_Next(iter_obj, ppos, &key, &value))) {
        return 0;
    }
    if (pitem) {
        PyObject* tuple = PyTuple_New(2);
        if (unlikely(!tuple)) {
            return -1;
        }
        Py_INCREF(key);
        Py_INCREF(value);
        #if CYTHON_ASSUME_SAFE_MACROS
        PyTuple_SET_ITEM(tuple, 0, key);
        PyTuple_SET_ITEM(tuple, 1, value);
        #else
        if (unlikely(PyTuple_SetItem(tuple, 0, key) < 0)) {
            Py_DECREF(value);
            Py_DECREF(tuple);
            return -1;
        }
        if (unlikely(PyTuple_SetItem(tuple, 1, value) < 0)) {
            Py_DECREF(tuple);
            return -1;
        }
        #endif
        *pitem = tuple;
    } else {
        if (pkey) {
            Py_INCREF(key);
            *pkey = key;
        }
        if (pvalue) {
            Py_INCREF(value);
            *pvalue = value;
        }
    }
    return 1;
}
#endif
static CYTHON_INLINE int __Pyx_dict_iter_next(
        PyObject* iter_obj, CYTHON_NCP_UNUSED Py_ssize_t orig_length, CYTHON_NCP_UNUSED Py_ssize_t* ppos,
        PyObject** pkey, PyObject** pvalue, PyObject** pitem, int source_is_dict) {
    PyObject* next_item;
#if !CYTHON_AVOID_BORROWED_REFS
    if (source_is_dict) {
        int result;
#if PY_VERSION_HEX >= 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
        Py_BEGIN_CRITICAL_SECTION(iter_obj);
#endif
        result = __Pyx_dict_iter_next_source_is_dict(iter_obj, orig_length, ppos, pkey, pvalue, pitem);
#if PY_VERSION_HEX >= 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
        Py_END_CRITICAL_SECTION();
#endif
        return result;
    } else if (PyTuple_CheckExact(iter_obj)) {
        Py_ssize_t pos = *ppos;
        Py_ssize_t tuple_size = __Pyx_PyTuple_GET_SIZE(iter_obj);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(tuple_size < 0)) return -1;
        #endif
        if (unlikely(pos >= tuple_size)) return 0;
        *ppos = pos + 1;
        #if CYTHON_ASSUME_SAFE_MACROS
        next_item = PyTuple_GET_ITEM(iter_obj, pos);
        #else
        next_item = PyTuple_GetItem(iter_obj, pos);
        if (unlikely(!next_item)) return -1;
        #endif
        Py_INCREF(next_item);
    } else if (PyList_CheckExact(iter_obj)) {
        Py_ssize_t pos = *ppos;
        Py_ssize_t list_size = __Pyx_PyList_GET_SIZE(iter_obj);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(list_size < 0)) return -1;
        #endif
        if (unlikely(pos >= list_size)) return 0;
        *ppos = pos + 1;
        next_item = __Pyx_PyList_GetItemRef(iter_obj, pos);
        if (unlikely(!next_item)) return -1;
    } else
#endif
    {
        next_item = PyIter_Next(iter_obj);
        if (unlikely(!next_item)) {
            return __Pyx_IterFinish();
        }
    }
    if (pitem) {
        *pitem = next_item;
    } else if (pkey && pvalue) {
        if (__Pyx_unpack_tuple2(next_item, pkey, pvalue, source_is_dict, source_is_dict, 1))
            return -1;
    } else if (pkey) {
        *pkey = next_item;
    } else {
        *pvalue = next_item;
    }
    return 1;
}

