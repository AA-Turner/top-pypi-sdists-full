# if CYTHON_COMPILING_IN_CPYTHON
    #if CYTHON_REFNANNY
        #define __Pyx_PyUnicode_ConcatInPlace(left, right, unsafe_shared) __Pyx_PyUnicode_ConcatInPlaceImpl(&left, right, unsafe_shared, __pyx_refnanny)
    #else
        #define __Pyx_PyUnicode_ConcatInPlace(left, right, unsafe_shared) __Pyx_PyUnicode_ConcatInPlaceImpl(&left, right, unsafe_shared)
    #endif
    #define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_DefinitelyUniqueInPlace(left, right) __Pyx_PyUnicode_ConcatInPlace(left, right, __Pyx_ReferenceSharing_DefinitelyUnique)
    #define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_OwnStrongReferenceInPlace(left, right) __Pyx_PyUnicode_ConcatInPlace(left, right, __Pyx_ReferenceSharing_OwnStrongReference)
    #define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_FunctionArgumentInPlace(left, right) __Pyx_PyUnicode_ConcatInPlace(left, right, __Pyx_ReferenceSharing_FunctionArgument)
    #define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_SharedReferenceInPlace(left, right) __Pyx_PyUnicode_ConcatInPlace(left, right, __Pyx_ReferenceSharing_SharedReference)
    static CYTHON_INLINE PyObject *__Pyx_PyUnicode_ConcatInPlaceImpl(PyObject **p_left, PyObject *right, int unsafe_shared
        #if CYTHON_REFNANNY
        , void* __pyx_refnanny
        #endif
    );
#else
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_DefinitelyUniqueInPlace __Pyx_PyUnicode_Concat
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_OwnStrongReferenceInPlace __Pyx_PyUnicode_Concat
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_FunctionArgumentInPlace __Pyx_PyUnicode_Concat
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_SharedReferenceInPlace __Pyx_PyUnicode_Concat
#endif
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_DefinitelyUniqueInPlaceSafe(left, right)\
    ((unlikely((left) == Py_None) || unlikely((right) == Py_None)) ?\
    PyNumber_InPlaceAdd(left, right) : __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_DefinitelyUniqueInPlace(left, right))
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_OwnStrongReferenceInPlaceSafe(left, right)\
    ((unlikely((left) == Py_None) || unlikely((right) == Py_None)) ?\
    PyNumber_InPlaceAdd(left, right) : __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_OwnStrongReferenceInPlace(left, right))
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_FunctionArgumentInPlaceSafe(left, right)\
    ((unlikely((left) == Py_None) || unlikely((right) == Py_None)) ?\
    PyNumber_InPlaceAdd(left, right) : __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_FunctionArgumentInPlace(left, right))
#define __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_SharedReferenceInPlaceSafe(left, right)\
    ((unlikely((left) == Py_None) || unlikely((right) == Py_None)) ?\
    PyNumber_InPlaceAdd(left, right) : __Pyx_PyUnicode_Concat__Pyx_ReferenceSharing_SharedReferenceInPlace(left, right))

