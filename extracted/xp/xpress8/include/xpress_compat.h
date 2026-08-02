/* Portability shim for building Microsoft's ESE xpress8 sources outside MSVC.
 * Provides empty macros for SAL annotations and MSVC-only keywords.
 * Included from xprs.h before anything else. */
#ifndef XPRESS_COMPAT_H
#define XPRESS_COMPAT_H

#if defined(_MSC_VER)

/* MSVC: pull in the SAL annotation macros (__in_opt, __in_bcount, etc.).
 * These are not implicitly included by the CRT when consumers include only
 * <stdlib.h>/<memory.h>, so xpress.h's signatures fail to parse without it. */
#include <sal.h>

#else /* !_MSC_VER */

#ifndef UNIX
#define UNIX 1
#endif

/* No __stdcall outside Windows */
#define XPRESS_CALL

/* __unaligned is MSVC-only. Compilers we target tolerate unaligned access
 * for the small types xdecode reads. */
#define __unaligned

/* MSVC SAL annotations */
#define __in
#define __in_opt
#define __out
#define __out_opt
#define __inout
#define __inout_opt
#define __in_bcount(x)
#define __in_ecount(x)
#define __out_bcount(x)
#define __out_ecount(x)
#define __analysis_assume(x)

/* __declspec(align(N)) — drop on non-MSVC. Signature buffers are read as
 * pointers only, so alignment is not load-bearing here. */
#define __declspec(x)

#endif /* !_MSC_VER */

#endif /* XPRESS_COMPAT_H */
