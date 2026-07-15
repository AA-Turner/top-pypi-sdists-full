#ifndef RUST_LEGACY_DEMANGLE_H
#define RUST_LEGACY_DEMANGLE_H

#include <string_view>

// Demangle a Rust legacy mangled symbol (pre-v0, using _ZN prefix).
// Returns a malloc'd NUL-terminated string on success, or nullptr.
char* rustLegacyDemangle(std::string_view MangledName);

#endif
