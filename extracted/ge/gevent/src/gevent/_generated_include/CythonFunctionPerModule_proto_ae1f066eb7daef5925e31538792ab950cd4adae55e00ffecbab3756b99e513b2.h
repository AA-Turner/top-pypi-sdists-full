#define __Pyx_CyFunction_USED
#if CYTHON_OPAQUE_SHARED_TYPES
#define __Pyx_as_CyFunctionObject(o) ((__pyx_CyFunctionObject *)PyObject_GetTypeData((o), __pyx_mstate_global->__pyx_CyFunctionType))
#else
#define __Pyx_as_CyFunctionObject(o) ((__pyx_CyFunctionObject *)o)
#endif
#define __Pyx_CYFUNCTION_STATICMETHOD  0x01
#define __Pyx_CYFUNCTION_CLASSMETHOD   0x02
#define __Pyx_CYFUNCTION_CCLASS        0x04
#define __Pyx_CYFUNCTION_COROUTINE     0x08
#define __Pyx_CyFunction_GetClosure(f)\
    ((__Pyx_as_CyFunctionObject(f))->func_closure)
#if CYTHON_COMPILING_IN_LIMITED_API
  #define __Pyx__CyFunction_GetClassObj(f)\
      ((f)->func_classobj)
#else
  #define __Pyx__CyFunction_GetClassObj(f)\
      ((PyObject*) ((PyCMethodObject *) (f))->mm_class)
#endif
#define __Pyx_CyFunction_GetClassObj(f)\
    __Pyx__CyFunction_GetClassObj(__Pyx_as_CyFunctionObject(f))
#define __Pyx_CyFunction_SetClassObj(f, classobj)\
    __Pyx__CyFunction_SetClassObj(__Pyx_as_CyFunctionObject(f), (classobj))
#define __Pyx_CyFunction_Defaults(type, f)\
    ((type *)((__Pyx_as_CyFunctionObject(f))->defaults))
#define __Pyx_CyFunction_SetDefaultsGetter(f, g)\
    (__Pyx_as_CyFunctionObject(f))->defaults_getter = (g)
typedef struct {
#if CYTHON_COMPILING_IN_LIMITED_API
#if !CYTHON_OPAQUE_OBJECTS
    PyObject_HEAD
#endif
    PyMethodDef *func_methoddef;
    PyObject *func_module;
#else
    PyCMethodObject func;
#endif
#if (CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY) && CYTHON_VECTORCALL
    __pyx_vectorcallfunc func_vectorcall;
#endif
#if CYTHON_COMPILING_IN_LIMITED_API
    PyObject *func_weakreflist;
#endif
#if PY_VERSION_HEX < 0x030C0000 || CYTHON_COMPILING_IN_LIMITED_API
    PyObject *func_dict;
#endif
    PyObject *func_name;
    PyObject *func_qualname;
    PyObject *func_doc;
    PyObject *func_globals;
    PyObject *func_code;
    PyObject *func_closure;
#if CYTHON_COMPILING_IN_LIMITED_API
    PyObject *func_classobj;
#endif
    PyObject *defaults;
    int flags;
    PyObject *defaults_tuple;
    PyObject *defaults_kwdict;
    PyObject *(*defaults_getter)(PyObject *);
    PyObject *func_annotations;
#if __PYX_LIMITED_VERSION_HEX < 0x030B0000
    PyObject *func_is_coroutine;
#endif
} __pyx_CyFunctionObject;
#undef __Pyx_CyOrPyCFunction_Check
#define __Pyx_CyFunction_Check(obj)  __Pyx_TypeCheck(obj, __pyx_mstate_global->__pyx_CyFunctionType)
#define __Pyx_CyOrPyCFunction_Check(obj)  __Pyx_TypeCheck2(obj, __pyx_mstate_global->__pyx_CyFunctionType, &PyCFunction_Type)
#define __Pyx_CyFunction_CheckExact(obj)  Py_IS_TYPE(obj, __pyx_mstate_global->__pyx_CyFunctionType)
static CYTHON_INLINE int __Pyx__IsSameCyOrCFunction(PyObject *func, void (*cfunc)(void));
#undef __Pyx_IsSameCFunction
#define __Pyx_IsSameCFunction(func, cfunc)   __Pyx__IsSameCyOrCFunction(func, cfunc)
static CYTHON_INLINE void __Pyx__CyFunction_SetClassObj(__pyx_CyFunctionObject* f, PyObject* classobj);
static CYTHON_INLINE PyObject *__Pyx_CyFunction_InitDefaults(PyObject *func,
                                                         PyTypeObject *defaults_type);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsTuple(PyObject *m,
                                                            PyObject *tuple);
static CYTHON_INLINE void __Pyx_CyFunction_SetDefaultsKwDict(PyObject *m,
                                                             PyObject *dict);
static CYTHON_INLINE void __Pyx_CyFunction_SetAnnotationsDict(PyObject *m,
                                                              PyObject *dict);
static int __pyx_CyFunction_init(PyObject *module);
#if CYTHON_VECTORCALL
#if CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY
#define __Pyx_CyFunction_func_vectorcall(f) ((f)->func_vectorcall)
#else
#define __Pyx_CyFunction_func_vectorcall(f) (((PyCFunctionObject*)f)->vectorcall)
#endif
#endif

