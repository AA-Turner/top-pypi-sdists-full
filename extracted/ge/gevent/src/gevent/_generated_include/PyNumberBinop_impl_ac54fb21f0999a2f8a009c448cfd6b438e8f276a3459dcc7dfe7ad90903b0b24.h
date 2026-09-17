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
#ifndef __Pyx_DEFINED_PyNumber_Subtract_xfloat_float
#define __Pyx_DEFINED_PyNumber_Subtract_xfloat_float
static PyObject* __Pyx_PyNumber_Subtract_xfloat_float(PyObject *op1, PyObject *op2, int inplace) {
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
#ifndef __Pyx_DEFINED_PyNumber_Subtract_xint_float
#define __Pyx_DEFINED_PyNumber_Subtract_xint_float
static PyObject* __Pyx_PyNumber_Subtract_xint_float(PyObject *op1, PyObject *op2, int inplace) {
    if (likely(op2 != Py_None)) {
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
static CYTHON_INLINE PyObject* __Pyx__PyNumber_Subtract_object_float(PyObject *op1, PyObject *op2, int inplace) {
    if (likely(PyFloat_CheckExact(op1))) {
        if (likely(op2 != Py_None)) {
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
        return __Pyx_PyNumber_Subtract_xfloat_float(op1, op2, inplace);
    }
    if (PyLong_CheckExact(op1)) {
        return __Pyx_PyNumber_Subtract_xint_float(op1, op2, inplace);
    }
    return (inplace) ? PyNumber_InPlaceSubtract(op1, op2) : PyNumber_Subtract(op1, op2);
}
#endif

