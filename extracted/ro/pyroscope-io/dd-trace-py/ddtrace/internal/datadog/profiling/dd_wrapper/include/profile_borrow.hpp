#pragma once

#include "profiler_stats.hpp"

namespace Datadog {

// RAII wrapper for borrowing both profile and stats under a single lock
class ProfileBorrow
{
  public:
    ProfileBorrow() = default;

    // Disable copy
    ProfileBorrow(const ProfileBorrow&) = delete;
    ProfileBorrow& operator=(const ProfileBorrow&) = delete;

    // Enable move
    ProfileBorrow(ProfileBorrow&& other) noexcept = default;
    ProfileBorrow& operator=(ProfileBorrow&& other) noexcept = default;

    // Accessors
    ProfilerStats& stats()
    {
        static ProfilerStats stats;
        return stats;
    }
};

} // namespace Datadog
