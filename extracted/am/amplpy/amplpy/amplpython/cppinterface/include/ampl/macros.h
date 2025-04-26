#ifndef AMPL_MACROS_H_
#define AMPL_MACROS_H_

#define AMPL_DISALLOW_COPY_AND_ASSIGN(TypeName) \
  TypeName(const TypeName &) = delete;         \
  TypeName &operator=(const TypeName &) = delete

#if defined(_WIN32) && !defined(__MINGW32__)
// Fix warnings about deprecated symbols.
#define AMPL_POSIX(call) _##call
#else
#define AMPL_POSIX(call) call
#endif

// Calls to system functions are wrapped in AMPL_SYSTEM for testability.
#ifdef AMPL_SYSTEM
#define AMPL_POSIX_CALL(call) AMPL_SYSTEM(call)
#else
#define AMPL_SYSTEM(call) call
#ifdef _WIN32
// Fix warnings about deprecated symbols.
#define AMPL_POSIX_CALL(call) ::_##call
#else
#define AMPL_POSIX_CALL(call) ::call
#endif
#endif


#endif  // AMPL_MACROS_H_