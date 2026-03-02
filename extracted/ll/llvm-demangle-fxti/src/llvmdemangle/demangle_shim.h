// demangle_shim.h — Normalize LLVM Demangle API across versions 11-21.
// Included by demangle.pyx; requires -DLLVM_MAJOR=<N> from the build system.

#ifndef DEMANGLE_SHIM_H
#define DEMANGLE_SHIM_H

#include "llvm/Demangle/Demangle.h"
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <string>

#ifndef LLVM_MAJOR
#error "LLVM_MAJOR must be defined (e.g. -DLLVM_MAJOR=18)"
#endif

// Feature availability flags
static const bool SHIM_HAS_RUST  = (LLVM_MAJOR >= 13);
static const bool SHIM_HAS_DLANG = (LLVM_MAJOR >= 14);
static const bool SHIM_HAS_NON_MICROSOFT = (LLVM_MAJOR >= 14);
static const bool SHIM_HAS_PARSE_PARAMS  = (LLVM_MAJOR >= 18);
static const bool SHIM_HAS_NO_VARIABLE_TYPE = (LLVM_MAJOR >= 14);
static const bool SHIM_HAS_ARM64EC = (LLVM_MAJOR >= 19);

// --- demangle() ---
inline std::string shim_demangle(const char *name) {
#if LLVM_MAJOR >= 17
    return llvm::demangle(std::string_view(name));
#else
    return llvm::demangle(std::string(name));
#endif
}

// --- itaniumDemangle() ---
// Returns malloc'd string or nullptr. Caller must free().
inline char *shim_itanium_demangle(const char *name, bool parse_params) {
#if LLVM_MAJOR >= 18
    return llvm::itaniumDemangle(name, parse_params);
#elif LLVM_MAJOR >= 17
    (void)parse_params;
    return llvm::itaniumDemangle(name);
#else
    (void)parse_params;
    return llvm::itaniumDemangle(name, nullptr, nullptr, nullptr);
#endif
}

// --- microsoftDemangle() ---
// Returns malloc'd string or nullptr. Caller must free().
// n_read receives bytes consumed on success.
inline char *shim_microsoft_demangle(const char *name, int flags,
                                     size_t *n_read) {
    int status = 0;
#if LLVM_MAJOR >= 17
    return llvm::microsoftDemangle(name, n_read, &status,
                                   static_cast<llvm::MSDemangleFlags>(flags));
#else
    return llvm::microsoftDemangle(name, n_read, nullptr, nullptr, &status,
                                   static_cast<llvm::MSDemangleFlags>(flags));
#endif
}

// --- rustDemangle() ---
// Returns malloc'd string or nullptr. Caller must free().
// Returns (char*)-1 sentinel when feature is unavailable.
inline char *shim_rust_demangle(const char *name) {
#if LLVM_MAJOR >= 15
    return llvm::rustDemangle(name);
#elif LLVM_MAJOR >= 13
    return llvm::rustDemangle(name, nullptr, nullptr, nullptr);
#else
    (void)name;
    return reinterpret_cast<char *>(-1); // sentinel: not available
#endif
}

// --- dlangDemangle() ---
// Returns malloc'd string or nullptr. Caller must free().
// Returns (char*)-1 sentinel when feature is unavailable.
inline char *shim_dlang_demangle(const char *name) {
#if LLVM_MAJOR >= 17
    return llvm::dlangDemangle(name);
#elif LLVM_MAJOR >= 14
    return llvm::dlangDemangle(name);
#else
    (void)name;
    return reinterpret_cast<char *>(-1); // sentinel: not available
#endif
}

// --- nonMicrosoftDemangle() ---
// Returns success flag. Result written to out_result.
// Returns -1 when feature is unavailable.
inline int shim_non_microsoft_demangle(const char *name,
                                       bool can_have_leading_dot,
                                       bool parse_params,
                                       std::string *out_result) {
#if LLVM_MAJOR >= 18
    bool ok = llvm::nonMicrosoftDemangle(name, *out_result,
                                         can_have_leading_dot, parse_params);
    return ok ? 1 : 0;
#elif LLVM_MAJOR >= 17
    (void)parse_params;
    (void)can_have_leading_dot;
    bool ok = llvm::nonMicrosoftDemangle(name, *out_result);
    return ok ? 1 : 0;
#elif LLVM_MAJOR >= 14
    (void)parse_params;
    (void)can_have_leading_dot;
    bool ok = llvm::nonMicrosoftDemangle(name, *out_result);
    return ok ? 1 : 0;
#else
    (void)name;
    (void)can_have_leading_dot;
    (void)parse_params;
    (void)out_result;
    return -1; // not available
#endif
}

// --- getArm64ECInsertionPointInMangledName() ---
// Returns insertion point index, or -1 if not applicable / unavailable.
inline long long shim_get_arm64ec_insertion_point(const char *name) {
#if LLVM_MAJOR >= 19
    auto result = llvm::getArm64ECInsertionPointInMangledName(name);
    if (result.has_value())
        return static_cast<long long>(*result);
    return -1;
#else
    (void)name;
    return -2; // sentinel: not available
#endif
}

// ---------------------------------------------------------------------------
// ItaniumPartialDemangler shim: batch extraction
// Extract ALL string properties in a single C++ call to avoid cross-call
// buffer corruption observed when LLVM's OutputBuffer is used from within
// Python extension modules.
// ---------------------------------------------------------------------------

// Helper: extract one property using nullptr (LLVM allocates).
// Returns empty string on failure, sets *ok = false.
static inline std::string _ipd_extract(char *ret) {
    if (!ret) return std::string();
    std::string s(ret);
    std::free(ret);
    return s;
}

struct ShimIPDResult {
    std::string full_name;
    std::string base_name;
    std::string decl_context;
    std::string func_name;
    std::string params;
    std::string return_type;
    bool has_full_name;
    bool has_base_name;
    bool has_decl_context;
    bool has_func_name;
    bool has_params;
    bool has_return_type;
};

inline void shim_ipd_extract_all(llvm::ItaniumPartialDemangler *d,
                                  ShimIPDResult *r) {
    // Extract all string properties in one go.
    // Use nullptr buffers so LLVM allocates fresh memory each time.
    char *p;

    p = d->finishDemangle(nullptr, nullptr);
    r->has_full_name = (p != nullptr);
    if (p) { r->full_name.assign(p); std::free(p); }

    p = d->getFunctionBaseName(nullptr, nullptr);
    r->has_base_name = (p != nullptr);
    if (p) { r->base_name.assign(p); std::free(p); }

    p = d->getFunctionDeclContextName(nullptr, nullptr);
    r->has_decl_context = (p != nullptr);
    if (p) { r->decl_context.assign(p); std::free(p); }

    p = d->getFunctionName(nullptr, nullptr);
    r->has_func_name = (p != nullptr);
    if (p) { r->func_name.assign(p); std::free(p); }

    p = d->getFunctionParameters(nullptr, nullptr);
    r->has_params = (p != nullptr);
    if (p) { r->params.assign(p); std::free(p); }

    p = d->getFunctionReturnType(nullptr, nullptr);
    r->has_return_type = (p != nullptr);
    if (p) { r->return_type.assign(p); std::free(p); }
}

#endif // DEMANGLE_SHIM_H
