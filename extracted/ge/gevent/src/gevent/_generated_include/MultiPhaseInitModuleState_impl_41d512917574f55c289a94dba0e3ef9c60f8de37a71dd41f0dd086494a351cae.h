#if CYTHON_PEP489_MULTI_PHASE_INIT && CYTHON_USE_MODULE_STATE
#ifndef CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
#if (CYTHON_COMPILING_IN_LIMITED_API || PY_VERSION_HEX >= 0x030C0000)
  #define CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE 1
#else
  #define CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE 0
#endif
#endif
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE && !CYTHON_ATOMICS
#error "Module state with PEP489 requires atomics. Currently that's one of\
 C11, C++11, gcc atomic intrinsics or MSVC atomic intrinsics"
#endif
#if !CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
#define __Pyx_ModuleStateLookup_Lock()
#define __Pyx_ModuleStateLookup_Unlock()
#elif !CYTHON_COMPILING_IN_LIMITED_API && PY_VERSION_HEX >= 0x030d0000
static PyMutex __Pyx_ModuleStateLookup_mutex = {0};
#define __Pyx_ModuleStateLookup_Lock() PyMutex_Lock(&__Pyx_ModuleStateLookup_mutex)
#define __Pyx_ModuleStateLookup_Unlock() PyMutex_Unlock(&__Pyx_ModuleStateLookup_mutex)
#elif defined(__cplusplus) && __cplusplus >= 201103L
#include <mutex>
static std::mutex __Pyx_ModuleStateLookup_mutex;
#define __Pyx_ModuleStateLookup_Lock() __Pyx_ModuleStateLookup_mutex.lock()
#define __Pyx_ModuleStateLookup_Unlock() __Pyx_ModuleStateLookup_mutex.unlock()
#elif defined(__STDC_VERSION__) && (__STDC_VERSION__ > 201112L) && !defined(__STDC_NO_THREADS__)
#include <threads.h>
static mtx_t __Pyx_ModuleStateLookup_mutex;
static once_flag __Pyx_ModuleStateLookup_mutex_once_flag = ONCE_FLAG_INIT;
static void __Pyx_ModuleStateLookup_initialize_mutex(void) {
    mtx_init(&__Pyx_ModuleStateLookup_mutex, mtx_plain);
}
#define __Pyx_ModuleStateLookup_Lock()\
  call_once(&__Pyx_ModuleStateLookup_mutex_once_flag, __Pyx_ModuleStateLookup_initialize_mutex);\
  mtx_lock(&__Pyx_ModuleStateLookup_mutex)
#define __Pyx_ModuleStateLookup_Unlock() mtx_unlock(&__Pyx_ModuleStateLookup_mutex)
#elif defined(HAVE_PTHREAD_H)
#include <pthread.h>
static pthread_mutex_t __Pyx_ModuleStateLookup_mutex = PTHREAD_MUTEX_INITIALIZER;
#define __Pyx_ModuleStateLookup_Lock() pthread_mutex_lock(&__Pyx_ModuleStateLookup_mutex)
#define __Pyx_ModuleStateLookup_Unlock() pthread_mutex_unlock(&__Pyx_ModuleStateLookup_mutex)
#elif defined(_WIN32)
#include <Windows.h>  // synchapi.h on its own doesn't work
static SRWLOCK __Pyx_ModuleStateLookup_mutex = SRWLOCK_INIT;
#define __Pyx_ModuleStateLookup_Lock() AcquireSRWLockExclusive(&__Pyx_ModuleStateLookup_mutex)
#define __Pyx_ModuleStateLookup_Unlock() ReleaseSRWLockExclusive(&__Pyx_ModuleStateLookup_mutex)
#else
#error "No suitable lock available for CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE.\
 Requires C standard >= C11, or C++ standard >= C++11,\
 or pthreads, or the Windows 32 API, or Python >= 3.13."
#endif
typedef struct {
    int64_t id;
    PyObject *module;
} __Pyx_InterpreterIdAndModule;
typedef struct {
    char interpreter_id_as_index;
    Py_ssize_t count;
    Py_ssize_t allocated;
    __Pyx_InterpreterIdAndModule table[1];
} __Pyx_ModuleStateLookupData;
#define __PYX_MODULE_STATE_LOOKUP_SMALL_SIZE 32
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
static __pyx_atomic_int_type __Pyx_ModuleStateLookup_read_counter = 0;
#endif
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
static __pyx_atomic_ptr_type __Pyx_ModuleStateLookup_data = 0;
#else
static __Pyx_ModuleStateLookupData* __Pyx_ModuleStateLookup_data = NULL;
#endif
static __Pyx_InterpreterIdAndModule* __Pyx_State_FindModuleStateLookupTableLowerBound(
        __Pyx_InterpreterIdAndModule* table,
        Py_ssize_t count,
        int64_t interpreterId) {
    __Pyx_InterpreterIdAndModule* begin = table;
    __Pyx_InterpreterIdAndModule* end = begin + count;
    if (begin->id == interpreterId) {
        return begin;
    }
    while ((end - begin) > __PYX_MODULE_STATE_LOOKUP_SMALL_SIZE) {
        __Pyx_InterpreterIdAndModule* halfway = begin + (end - begin)/2;
        if (halfway->id == interpreterId) {
            return halfway;
        }
        if (halfway->id < interpreterId) {
            begin = halfway;
        } else {
            end = halfway;
        }
    }
    for (; begin < end; ++begin) {
        if (begin->id >= interpreterId) return begin;
    }
    return begin;
}
static PyObject *__Pyx_State_FindModule(CYTHON_UNUSED void* dummy) {
    int64_t interpreter_id = PyInterpreterState_GetID(__Pyx_PyInterpreterState_Get());
    if (interpreter_id == -1) return NULL;
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
    __Pyx_ModuleStateLookupData* data = (__Pyx_ModuleStateLookupData*)__pyx_atomic_pointer_load_relaxed(&__Pyx_ModuleStateLookup_data);
    {
        __pyx_atomic_incr_acq_rel(&__Pyx_ModuleStateLookup_read_counter);
        if (likely(data)) {
            __Pyx_ModuleStateLookupData* new_data = (__Pyx_ModuleStateLookupData*)__pyx_atomic_pointer_load_acquire(&__Pyx_ModuleStateLookup_data);
            if (likely(data == new_data)) {
                goto read_finished;
            }
        }
        __pyx_atomic_decr_acq_rel(&__Pyx_ModuleStateLookup_read_counter);
        __Pyx_ModuleStateLookup_Lock();
        __pyx_atomic_incr_relaxed(&__Pyx_ModuleStateLookup_read_counter);
        data = (__Pyx_ModuleStateLookupData*)__pyx_atomic_pointer_load_relaxed(&__Pyx_ModuleStateLookup_data);
        __Pyx_ModuleStateLookup_Unlock();
    }
  read_finished:;
#else
    __Pyx_ModuleStateLookupData* data = __Pyx_ModuleStateLookup_data;
#endif
    __Pyx_InterpreterIdAndModule* found = NULL;
    if (unlikely(!data)) goto end;
    if (data->interpreter_id_as_index) {
        if (interpreter_id < data->count) {
            found = data->table+interpreter_id;
        }
    } else {
        found = __Pyx_State_FindModuleStateLookupTableLowerBound(
            data->table, data->count, interpreter_id);
    }
  end:
    {
        PyObject *result=NULL;
        if (found && found->id == interpreter_id) {
            result = found->module;
        }
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
        __pyx_atomic_decr_acq_rel(&__Pyx_ModuleStateLookup_read_counter);
#endif
        return result;
    }
}
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
static void __Pyx_ModuleStateLookup_wait_until_no_readers(void) {
    while (__pyx_atomic_load(&__Pyx_ModuleStateLookup_read_counter) != 0);
}
#else
#define __Pyx_ModuleStateLookup_wait_until_no_readers()
#endif
static int __Pyx_State_AddModuleInterpIdAsIndex(__Pyx_ModuleStateLookupData **old_data, PyObject* module, int64_t interpreter_id) {
    Py_ssize_t to_allocate = (*old_data)->allocated;
    while (to_allocate <= interpreter_id) {
        if (to_allocate == 0) to_allocate = 1;
        else to_allocate *= 2;
    }
    __Pyx_ModuleStateLookupData *new_data = *old_data;
    if (to_allocate != (*old_data)->allocated) {
         new_data = (__Pyx_ModuleStateLookupData *)realloc(
            *old_data,
            sizeof(__Pyx_ModuleStateLookupData)+(to_allocate-1)*sizeof(__Pyx_InterpreterIdAndModule));
        if (!new_data) {
            PyErr_NoMemory();
            return -1;
        }
        for (Py_ssize_t i = new_data->allocated; i < to_allocate; ++i) {
            new_data->table[i].id = i;
            new_data->table[i].module = NULL;
        }
        new_data->allocated = to_allocate;
    }
    new_data->table[interpreter_id].module = module;
    if (new_data->count < interpreter_id+1) {
        new_data->count = interpreter_id+1;
    }
    *old_data = new_data;
    return 0;
}
static void __Pyx_State_ConvertFromInterpIdAsIndex(__Pyx_ModuleStateLookupData *data) {
    __Pyx_InterpreterIdAndModule *read = data->table;
    __Pyx_InterpreterIdAndModule *write = data->table;
    __Pyx_InterpreterIdAndModule *end = read + data->count;
    for (; read<end; ++read) {
        if (read->module) {
            write->id = read->id;
            write->module = read->module;
            ++write;
        }
    }
    data->count = write - data->table;
    for (; write<end; ++write) {
        write->id = 0;
        write->module = NULL;
    }
    data->interpreter_id_as_index = 0;
}
static int __Pyx_State_AddModule(PyObject* module, CYTHON_UNUSED void* dummy) {
    int64_t interpreter_id = PyInterpreterState_GetID(__Pyx_PyInterpreterState_Get());
    if (interpreter_id == -1) return -1;
    int result = 0;
    __Pyx_ModuleStateLookup_Lock();
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
    __Pyx_ModuleStateLookupData *old_data = (__Pyx_ModuleStateLookupData *)
            __pyx_atomic_pointer_exchange(&__Pyx_ModuleStateLookup_data, 0);
#else
    __Pyx_ModuleStateLookupData *old_data = __Pyx_ModuleStateLookup_data;
#endif
    __Pyx_ModuleStateLookupData *new_data = old_data;
    if (!new_data) {
        new_data = (__Pyx_ModuleStateLookupData *)calloc(1, sizeof(__Pyx_ModuleStateLookupData));
        if (!new_data) {
            result = -1;
            PyErr_NoMemory();
            goto end;
        }
        new_data->allocated = 1;
        new_data->interpreter_id_as_index = 1;
    }
    __Pyx_ModuleStateLookup_wait_until_no_readers();
    if (new_data->interpreter_id_as_index) {
        if (interpreter_id < __PYX_MODULE_STATE_LOOKUP_SMALL_SIZE) {
            result = __Pyx_State_AddModuleInterpIdAsIndex(&new_data, module, interpreter_id);
            goto end;
        }
        __Pyx_State_ConvertFromInterpIdAsIndex(new_data);
    }
    {
        Py_ssize_t insert_at = 0;
        {
            __Pyx_InterpreterIdAndModule* lower_bound = __Pyx_State_FindModuleStateLookupTableLowerBound(
                new_data->table, new_data->count, interpreter_id);
            assert(lower_bound);
            insert_at = lower_bound - new_data->table;
            if (unlikely(insert_at < new_data->count && lower_bound->id == interpreter_id)) {
                lower_bound->module = module;
                goto end;  // already in table, nothing more to do
            }
        }
        if (new_data->count+1 >= new_data->allocated) {
            Py_ssize_t to_allocate = (new_data->count+1)*2;
            new_data =
                (__Pyx_ModuleStateLookupData*)realloc(
                    new_data,
                    sizeof(__Pyx_ModuleStateLookupData) +
                    (to_allocate-1)*sizeof(__Pyx_InterpreterIdAndModule));
            if (!new_data) {
                result = -1;
                new_data = old_data;
                PyErr_NoMemory();
                goto end;
            }
            new_data->allocated = to_allocate;
        }
        ++new_data->count;
        int64_t last_id = interpreter_id;
        PyObject *last_module = module;
        for (Py_ssize_t i=insert_at; i<new_data->count; ++i) {
            int64_t current_id = new_data->table[i].id;
            new_data->table[i].id = last_id;
            last_id = current_id;
            PyObject *current_module = new_data->table[i].module;
            new_data->table[i].module = last_module;
            last_module = current_module;
        }
    }
  end:
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
    __pyx_atomic_pointer_exchange(&__Pyx_ModuleStateLookup_data, new_data);
#else
    __Pyx_ModuleStateLookup_data = new_data;
#endif
    __Pyx_ModuleStateLookup_Unlock();
    return result;
}
static int __Pyx_State_RemoveModule(CYTHON_UNUSED void* dummy) {
    int64_t interpreter_id = PyInterpreterState_GetID(__Pyx_PyInterpreterState_Get());
    if (interpreter_id == -1) return -1;
    __Pyx_ModuleStateLookup_Lock();
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
    __Pyx_ModuleStateLookupData *data = (__Pyx_ModuleStateLookupData *)
            __pyx_atomic_pointer_exchange(&__Pyx_ModuleStateLookup_data, 0);
#else
    __Pyx_ModuleStateLookupData *data = __Pyx_ModuleStateLookup_data;
#endif
    if (data->interpreter_id_as_index) {
        if (interpreter_id < data->count) {
            data->table[interpreter_id].module = NULL;
        }
        goto done;
    }
    {
        __Pyx_ModuleStateLookup_wait_until_no_readers();
        __Pyx_InterpreterIdAndModule* lower_bound = __Pyx_State_FindModuleStateLookupTableLowerBound(
            data->table, data->count, interpreter_id);
        if (!lower_bound) goto done;
        if (lower_bound->id != interpreter_id) goto done;
        __Pyx_InterpreterIdAndModule *end = data->table+data->count;
        for (;lower_bound<end-1; ++lower_bound) {
            lower_bound->id = (lower_bound+1)->id;
            lower_bound->module = (lower_bound+1)->module;
        }
    }
    --data->count;
    if (data->count == 0) {
        free(data);
        data = NULL;
    }
  done:
#if CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE
    __pyx_atomic_pointer_exchange(&__Pyx_ModuleStateLookup_data, data);
#else
    __Pyx_ModuleStateLookup_data = data;
#endif
    __Pyx_ModuleStateLookup_Unlock();
    return 0;
}
#endif

