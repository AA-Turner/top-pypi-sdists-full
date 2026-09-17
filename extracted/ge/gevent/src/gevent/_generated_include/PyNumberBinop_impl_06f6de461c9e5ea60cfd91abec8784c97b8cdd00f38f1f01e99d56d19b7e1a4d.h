#if !(CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_GRAAL || CYTHON_COMPILING_IN_LIMITED_API)
#if CYTHON_USE_TYPE_SLOTS || __PYX_LIMITED_VERSION_HEX >= 0x030A0000
#ifndef __Pyx_DEFINED_BinopTypeError
#define __Pyx_DEFINED_BinopTypeError
static void __Pyx_BinopTypeError(PyObject *op1, PyObject *op2, const char* op, int inplace) {
    char opname[4] = {op[0], op[1], 0, 0};
    if (inplace) {
        opname[op[1] ? 2 : 1] = '=';
    }
    __Pyx_RaiseErrorWithObjectTypes1(
        PyExc_TypeError,
        "unsupported operand type(s) for %.3s: '" __Pyx_FMT_TYPENAME "' and '" __Pyx_FMT_TYPENAME "'",
        opname, op1, op2);
}
#endif
#endif
#ifndef __Pyx_DEFINED_PyNumber_Subtract_xfloat_object
#define __Pyx_DEFINED_PyNumber_Subtract_xfloat_object
static PyObject* __Pyx_PyNumber_Subtract_xfloat_object(PyObject *op1, PyObject *op2, int inplace) {
    if (PyLong_CheckExact(op2)) {
        double int_op2;
        #if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsCompact(op2)) {
            Py_ssize_t compact_op2 = __Pyx_PyLong_CompactValue(op2);
            if (compact_op2 == 0) return __Pyx_NewRef(op1);
            int_op2 = (double) compact_op2;
        } else
        #endif
        {
            int_op2 = PyLong_AsDouble(op2);
            if (unlikely((int_op2 == -1.) && PyErr_Occurred())) return NULL;
            #if !CYTHON_USE_PYLONG_INTERNALS
            if (int_op2 == 0.) return __Pyx_NewRef(op1);
            #endif
        }
        double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
        #if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely((float_op1 == -1.) && PyErr_Occurred())) return NULL;
        #endif
        return PyFloat_FromDouble(float_op1 - int_op2);
    }
    if (PyLong_Check(op2)) {
        binaryfunc slot_func = __Pyx_PyType_GetSubSlot(&PyFloat_Type, tp_as_number, nb_subtract, binaryfunc);
        if (likely(slot_func)) {
            return slot_func(op1, op2);
        }
    }
    #if CYTHON_USE_TYPE_SLOTS || __PYX_LIMITED_VERSION_HEX >= 0x030A0000
    {
        PyTypeObject *type_op2 = Py_TYPE(op2);
        binaryfunc slot_func = __Pyx_PyType_GetSubSlot(type_op2, tp_as_number, nb_subtract, binaryfunc);
        if (likely(slot_func)) {
            PyObject *result = slot_func(op1, op2);
            if (likely(result != Py_NotImplemented)) {
                return result;
            }
            Py_DECREF(result);
        }
        __Pyx_BinopTypeError(op1, op2, "-", inplace);
        return NULL;
    }
    #else
    return (inplace) ? PyNumber_InPlaceSubtract(op1, op2) : PyNumber_Subtract(op1, op2);
    #endif
}
#endif
#ifndef __Pyx_DEFINED_PyNumber_Subtract_xint_object
#define __Pyx_DEFINED_PyNumber_Subtract_xint_object
static PyObject* __Pyx_PyNumber_Subtract_xint_object(PyObject *op1, PyObject *op2, int inplace) {
    if (PyFloat_CheckExact(op2)) {
        double int_op1;
        #if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsCompact(op1)) {
            Py_ssize_t compact_op1 = __Pyx_PyLong_CompactValue(op1);
            int_op1 = (double) compact_op1;
        } else
        #endif
        {
            int_op1 = PyLong_AsDouble(op1);
            if (unlikely((int_op1 == -1.) && PyErr_Occurred())) return NULL;
        }
        double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
        #if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely((float_op2 == -1.) && PyErr_Occurred())) return NULL;
        #endif
        return PyFloat_FromDouble(int_op1 - float_op2);
    }
    #if CYTHON_USE_TYPE_SLOTS || __PYX_LIMITED_VERSION_HEX >= 0x030A0000
    {
        PyTypeObject *type_op2 = Py_TYPE(op2);
        binaryfunc slot_func = __Pyx_PyType_GetSubSlot(type_op2, tp_as_number, nb_subtract, binaryfunc);
        if (likely(slot_func)) {
            PyObject *result = slot_func(op1, op2);
            if (likely(result != Py_NotImplemented)) {
                return result;
            }
            Py_DECREF(result);
        }
        __Pyx_BinopTypeError(op1, op2, "-", inplace);
        return NULL;
    }
    #else
    return (inplace) ? PyNumber_InPlaceSubtract(op1, op2) : PyNumber_Subtract(op1, op2);
    #endif
}
#endif
static CYTHON_INLINE PyObject* __Pyx__PyNumber_Subtract_object_object(PyObject *op1, PyObject *op2, int inplace) {
    if (PyFloat_CheckExact(op1)) {
        if (PyFloat_CheckExact(op2)) {
            double float_op2 = __Pyx_PyFloat_AS_DOUBLE(op2);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely((float_op2 == -1.) && PyErr_Occurred())) return NULL;
            #endif
            double float_op1 = __Pyx_PyFloat_AS_DOUBLE(op1);
            #if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely((float_op1 == -1.) && PyErr_Occurred())) return NULL;
            #endif
            return PyFloat_FromDouble(float_op1 - float_op2);
        }
        return __Pyx_PyNumber_Subtract_xfloat_object(op1, op2, inplace);
    }
    if (PyLong_CheckExact(op1)) {
        if (PyLong_CheckExact(op2)) {
            #if CYTHON_USE_PYLONG_INTERNALS
            if (__Pyx_PyLong_IsCompact(op1)) {
                Py_ssize_t int_op1 = __Pyx_PyLong_CompactValue(op1);
                if (__Pyx_PyLong_IsCompact(op2)) {
                    Py_ssize_t int_op2 = __Pyx_PyLong_CompactValue(op2);
                    if (int_op2 == 0) return __Pyx_NewRef(op1);
                    return PyLong_FromSsize_t(int_op1 - int_op2);
                }
            }
            else if (__Pyx_PyLong_IsZero(op2)) return __Pyx_NewRef(op1);
            #endif
            binaryfunc slot_func = __Pyx_PyType_GetSubSlot(&PyLong_Type, tp_as_number, nb_subtract, binaryfunc);
            if (likely(slot_func)) {
                return slot_func(op1, op2);
            }
        }
        return __Pyx_PyNumber_Subtract_xint_object(op1, op2, inplace);
    }
    return (inplace) ? PyNumber_InPlaceSubtract(op1, op2) : PyNumber_Subtract(op1, op2);
}
#endif

