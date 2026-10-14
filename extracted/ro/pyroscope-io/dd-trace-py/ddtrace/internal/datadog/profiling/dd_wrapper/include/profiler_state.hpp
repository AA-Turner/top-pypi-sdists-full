#pragma once

#include "constants.hpp"
#include "native_call_tracker.hpp"

#include <atomic>

namespace Datadog {

// ProfilerState is a singleton class that holds all Profiler "global" state.
// Consolidating it here makes lifecycle management (init, cleanup, fork handling) clearer.
// Note: this class does not start or stop threads. However, it installs fork handlers that
//   may stop threads through libdatadog helpers (abstracted away / out of our control).
//
// This class owns all shared mutable state for the profiler.
// When adding new state, consider whether it belongs here or in a specific component.
class ProfilerState
{
  public:
    // Singleton access
    static ProfilerState& get();

    // ========================================================================
    // Native call tracking state
    // ========================================================================
    NativeCallRegistry native_call_registry{};

    // ========================================================================
    // Sample configuration
    // ========================================================================
    std::atomic<unsigned int> max_nframes{ g_default_max_nframes };

  private:
    ProfilerState() = default;
    ~ProfilerState() = default;

    // Non-copyable, non-movable
    ProfilerState(const ProfilerState&) = delete;
    ProfilerState& operator=(const ProfilerState&) = delete;
    ProfilerState(ProfilerState&&) = delete;
    ProfilerState& operator=(ProfilerState&&) = delete;
};

} // namespace Datadog
