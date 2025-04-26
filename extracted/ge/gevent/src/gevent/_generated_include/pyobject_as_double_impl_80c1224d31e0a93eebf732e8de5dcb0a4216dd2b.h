static double __Pyx__PyObject_AsDouble(PyObject* obj) {
    if (PyUnicode_CheckExact(obj)) {
        return __Pyx_PyUnicode_AsDouble(obj);
    } else if (PyBytes_CheckExact(obj)) {
        return __Pyx_PyBytes_AsDouble(obj);
    } else if (PyByteArray_CheckExact(obj)) {
        return __Pyx_PyByteArray_AsDouble(obj);
    } else {
        PyObject* float_value;
#if !CYTHON_USE_TYPE_SLOTS
        float_value = PyNumber_Float(obj);  if ((0)) goto bad;
        (void)__Pyx_PyObject_CallOneArg;
#else
        PyNumberMethods *nb = Py_TYPE(obj)->tp_as_number;
        if (likely(nb) && likely(nb->nb_float)) {
            float_value = nb->nb_float(obj);
            if (likely(float_value) && unlikely(!PyFloat_Check(float_value))) {
                __Pyx_TypeName float_value_type_name = __Pyx_PyType_GetName(Py_TYPE(float_value));
                PyErr_Format(PyExc_TypeError,
                    "__float__ returned non-float (type " __Pyx_FMT_TYPENAME ")",
                    float_value_type_name);
                __Pyx_DECREF_TypeName(float_value_type_name);
                Py_DECREF(float_value);
                goto bad;
            }
        } else {
            float_value = __Pyx_PyObject_CallOneArg((PyObject*)&PyFloat_Type, obj);
        }
#endif
        if (likely(float_value)) {
            double value = PyFloat_AS_DOUBLE(float_value);
            Py_DECREF(float_value);
            return value;
        }
    }
bad:
    return (double)-1;
}

