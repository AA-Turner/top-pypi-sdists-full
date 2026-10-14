#pragma once

#include <cstdint>
#include <functional>
#include <optional>
#include <string>

namespace Datadog {

struct CallSiteKey
{
    uintptr_t code_ptr;
    int offset_bytes;
    int first_lineno; // Guards against code object address reuse after GC
    bool operator==(const CallSiteKey& other) const
    {
        return code_ptr == other.code_ptr && offset_bytes == other.offset_bytes && first_lineno == other.first_lineno;
    }
};

struct CallSiteKeyHash
{
    size_t operator()(const CallSiteKey& k) const
    {
        // Boost-style hash combine for better collision resistance
        size_t h = std::hash<uintptr_t>()(k.code_ptr);
        h ^= std::hash<int>()(k.offset_bytes) + 0x9e3779b9 + (h << 6) + (h >> 2);
        h ^= std::hash<int>()(k.first_lineno) + 0x9e3779b9 + (h << 6) + (h >> 2);
        return h;
    }
};

struct NativeCallEntry
{
    std::string name;
    std::string module;
};

// Pyroscope patch: always-empty stub; nothing registers call sites without upstream's stack.cpp.
class NativeCallRegistry
{
  public:
    std::optional<std::reference_wrapper<NativeCallEntry>> lookup(uintptr_t, int, int) { return std::nullopt; }
};

} // namespace Datadog
