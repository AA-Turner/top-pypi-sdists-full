#if CYTHON_COMPILING_IN_LIMITED_API
    #if CYTHON_METH_FASTCALL
        #define __PYX_FASTCALL_ABI_SUFFIX  "_fastcall"
    #else
        #define __PYX_FASTCALL_ABI_SUFFIX
    #endif
    #define __PYX_LIMITED_ABI_SUFFIX "limited" __PYX_FASTCALL_ABI_SUFFIX __PYX_AM_SEND_ABI_SUFFIX
#else
    #define __PYX_LIMITED_ABI_SUFFIX
#endif
#if __PYX_HAS_PY_AM_SEND == 1
    #define __PYX_AM_SEND_ABI_SUFFIX
#elif __PYX_HAS_PY_AM_SEND == 2
    #define __PYX_AM_SEND_ABI_SUFFIX "amsendbackport"
#else
    #define __PYX_AM_SEND_ABI_SUFFIX "noamsend"
#endif
#ifndef __PYX_MONITORING_ABI_SUFFIX
    #define __PYX_MONITORING_ABI_SUFFIX
#endif
#if CYTHON_USE_TP_FINALIZE
    #define __PYX_TP_FINALIZE_ABI_SUFFIX
#else
    #define __PYX_TP_FINALIZE_ABI_SUFFIX "nofinalize"
#endif
#if CYTHON_USE_FREELISTS || !defined(__Pyx_AsyncGen_USED)
    #define __PYX_FREELISTS_ABI_SUFFIX
#else
    #define __PYX_FREELISTS_ABI_SUFFIX "nofreelists"
#endif
#define CYTHON_ABI  __PYX_ABI_VERSION __PYX_LIMITED_ABI_SUFFIX __PYX_MONITORING_ABI_SUFFIX __PYX_TP_FINALIZE_ABI_SUFFIX __PYX_FREELISTS_ABI_SUFFIX __PYX_AM_SEND_ABI_SUFFIX
#define __PYX_ABI_MODULE_NAME "_cython_" CYTHON_ABI
#define __PYX_TYPE_MODULE_PREFIX __PYX_ABI_MODULE_NAME "."

