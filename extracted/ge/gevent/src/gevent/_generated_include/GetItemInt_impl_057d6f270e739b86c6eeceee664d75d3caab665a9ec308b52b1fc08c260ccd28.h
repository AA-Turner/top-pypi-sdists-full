static PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j) {
    PyObject *r;
    if (unlikely(!j)) return NULL;
    r = PyObject_GetItem(o, j);
    Py_DECREF(j);
    return r;
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_List_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_ASSUME_SAFE_SIZE
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += PyList_GET_SIZE(o);
    }
    if ((CYTHON_AVOID_BORROWED_REFS || CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS || !CYTHON_ASSUME_SAFE_MACROS)) {
        return __Pyx_PyList_GetItemRefFast(o, wrapped_i, unsafe_shared);
    } else
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, PyList_GET_SIZE(o)))) {
        return __Pyx_NewRef(PyList_GET_ITEM(o, wrapped_i));
    }
    return __Pyx_GetItemInt_Generic(o, PyLong_FromSsize_t(i));
#else
    (void)wraparound;
    (void)boundscheck;
    return PySequence_GetItem(o, i);
#endif
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Tuple_Fast(PyObject *o, Py_ssize_t i,
                                                              int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    Py_ssize_t wrapped_i = i;
    if (wraparound & unlikely(i < 0)) {
        wrapped_i += PyTuple_GET_SIZE(o);
    }
    if ((!boundscheck) || likely(__Pyx_is_valid_index(wrapped_i, PyTuple_GET_SIZE(o)))) {
        return __Pyx_NewRef(PyTuple_GET_ITEM(o, wrapped_i));
    }
    return __Pyx_GetItemInt_Generic(o, PyLong_FromSsize_t(i));
#else
    (void)wraparound;
    (void)boundscheck;
    return PySequence_GetItem(o, i);
#endif
}
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i, int is_list,
                                                     int wraparound, int boundscheck, int unsafe_shared) {
    CYTHON_MAYBE_UNUSED_VAR(unsafe_shared);
#if CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE
    if (is_list || PyList_CheckExact(o)) {
        Py_ssize_t n = ((!wraparound) | likely(i >= 0)) ? i : i + PyList_GET_SIZE(o);
        if ((CYTHON_AVOID_BORROWED_REFS || CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS)) {
            return __Pyx_PyList_GetItemRefFast(o, n, unsafe_shared);
        } else if ((!boundscheck) || (likely(__Pyx_is_valid_index(n, PyList_GET_SIZE(o))))) {
            return __Pyx_NewRef(PyList_GET_ITEM(o, n));
        }
    } else
    #if !CYTHON_AVOID_BORROWED_REFS
    if (PyTuple_CheckExact(o)) {
        Py_ssize_t n = ((!wraparound) | likely(i >= 0)) ? i : i + PyTuple_GET_SIZE(o);
        if ((!boundscheck) || likely(__Pyx_is_valid_index(n, PyTuple_GET_SIZE(o)))) {
            return __Pyx_NewRef(PyTuple_GET_ITEM(o, n));
        }
    } else
    #endif
#endif
#if CYTHON_USE_TYPE_SLOTS && !CYTHON_COMPILING_IN_PYPY
    {
        PyMappingMethods *mm = Py_TYPE(o)->tp_as_mapping;
        PySequenceMethods *sm = Py_TYPE(o)->tp_as_sequence;
        if (!is_list && mm && mm->mp_subscript) {
            PyObject *r, *key = PyLong_FromSsize_t(i);
            if (unlikely(!key)) return NULL;
            r = mm->mp_subscript(o, key);
            Py_DECREF(key);
            return r;
        }
        if (is_list || likely(sm && sm->sq_item)) {
            if (wraparound && unlikely(i < 0) && likely(sm->sq_length)) {
                Py_ssize_t l = sm->sq_length(o);
                if (likely(l >= 0)) {
                    i += l;
                } else {
                    if (!PyErr_ExceptionMatches(PyExc_OverflowError))
                        return NULL;
                    PyErr_Clear();
                }
            }
            return sm->sq_item(o, i);
        }
    }
#else
    if (is_list || !PyMapping_Check(o)) {
        return PySequence_GetItem(o, i);
    }
#endif
    (void)wraparound;
    (void)boundscheck;
    return __Pyx_GetItemInt_Generic(o, PyLong_FromSsize_t(i));
}

