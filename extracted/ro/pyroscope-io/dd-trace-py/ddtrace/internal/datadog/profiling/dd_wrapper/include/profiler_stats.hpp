#pragma once

#include <cstddef>
#include <optional>
#include <string>

namespace Datadog {

/*
ProfilerStats holds statistics around Profiling to be sent along
with the actual Profiles.

None of its methods are thread-safe and it should typically used with
a mutex to protect access to the data.
*/
class ProfilerStats
{
  public:
    ProfilerStats() = default;
    ~ProfilerStats() = default;

    void increment_sample_count([[maybe_unused]] size_t k_sample_count = 1) {}
    size_t get_sample_count() const;

    void increment_sampling_event_count([[maybe_unused]] size_t k_sampling_event_count = 1) {}
    size_t get_sampling_event_count() const;

    void set_sampling_interval_us([[maybe_unused]] size_t interval_us) {}
    std::optional<size_t> get_sampling_interval_us() const;

    void set_string_table_count([[maybe_unused]] size_t count) {}
    std::optional<size_t> get_string_table_count() const;

    void set_fast_copy_memory_enabled([[maybe_unused]] bool enabled) {}
    std::optional<bool> get_fast_copy_memory_enabled() const;

    void set_fast_copy_memory_user_disabled([[maybe_unused]] bool disabled) {}
    std::optional<bool> get_fast_copy_memory_user_disabled() const;

    void set_fast_copy_memory_capable([[maybe_unused]] bool capable) {}
    std::optional<bool> get_fast_copy_memory_capable() const;

    void set_fast_copy_memory_syscall_fallback([[maybe_unused]] bool fallback) {}
    std::optional<bool> get_fast_copy_memory_syscall_fallback() const;

    // fast_copy_memory_* are process-static; carry them across ProfilerStats swaps.
    void copy_fast_copy_metadata_from(const ProfilerStats& other);

    void add_copy_memory_error_count([[maybe_unused]] size_t count) {}
    size_t get_copy_memory_error_count() const;

    void set_heap_tracker_size([[maybe_unused]] size_t count) {}
    std::optional<size_t> get_heap_tracker_size() const;

    void set_heap_tracker_cap_drops(size_t count);
    std::optional<size_t> get_heap_tracker_cap_drops() const;

    void set_asyncio_task_count([[maybe_unused]] size_t count) {}
    std::optional<size_t> get_asyncio_task_count() const;

    void set_greenlet_count([[maybe_unused]] size_t count) {}
    std::optional<size_t> get_greenlet_count() const;

    void add_sample_capture_cpu_time_us([[maybe_unused]] size_t cpu_time_us) {}
    size_t get_sample_capture_cpu_time_us() const;

    // Returns a JSON string containing relevant Profiler Stats to be included
    // in the libdatadog payload.
    std::string get_internal_metadata_json();

    void reset_state();
};

} // namespace Datadog