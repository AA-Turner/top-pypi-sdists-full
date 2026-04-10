#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_TRASHCAN_BEGIN Py_TRASHCAN_BEGIN
#define __Pyx_TRASHCAN_END Py_TRASHCAN_END
#elif CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_TRASHCAN_BEGIN_CONDITION(op, cond)\
    do {\
        PyThreadState *_tstate = NULL;\
        if (cond) {\
            _tstate = PyThreadState_GET();\
            if (_tstate->trash_delete_nesting >= PyTrash_UNWIND_LEVEL) {\
                _PyTrash_thread_deposit_object((PyObject*)(op));\
                break;\
            }\
            ++_tstate->trash_delete_nesting;\
        }
#define __Pyx_TRASHCAN_END\
        if (_tstate) {\
            --_tstate->trash_delete_nesting;\
            if (_tstate->trash_delete_later && _tstate->trash_delete_nesting <= 0)\
                _PyTrash_thread_destroy_chain();\
        }\
    } while (0);
#define __Pyx_TRASHCAN_BEGIN(op, dealloc) __Pyx_TRASHCAN_BEGIN_CONDITION(op,\
        __Pyx_PyObject_GetSlot(op, tp_dealloc, destructor) == (destructor)(dealloc))
#else
#define __Pyx_TRASHCAN_BEGIN(op, dealloc)
#define __Pyx_TRASHCAN_END
#endif

