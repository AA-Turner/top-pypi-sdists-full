#include "dd_wrapper/include/sample_manager.hpp"
#include "pyroscope_ffi.h"
#include "sampler.hpp"
#include "span_links.hpp"

#include "echion/echion_sampler.h"
#include "echion/vm.h"

#include <cstdint>
#include <mutex>

extern "C" void
pyroscope_stack_configure(double interval_s,
                          bool fast_copy,
                          double fast_copy_warmup_s,
                          uint32_t max_nframes,
                          uint32_t max_threads,
                          bool oncpu,
                          bool adaptive_sampling,
                          double target_overhead,
                          uint64_t max_sampling_period_us,
                          double baseline_core_pct,
                          uint32_t p_stable_window_s,
                          double p_stable_percentile)
{
    static std::once_flag safe_copy_once;
    std::call_once(safe_copy_once, init_safe_copy, fast_copy);
    set_fast_copy_enabled(safe_memcpy_initialized);
    Datadog::SampleManager::set_max_nframes(max_nframes);
    auto& sampler = Datadog::Sampler::get();
    sampler.set_max_frames(max_nframes);
    sampler.set_max_threads_per_sample(max_threads);
    sampler.set_adaptive_sampling(adaptive_sampling);
    sampler.set_target_overhead(target_overhead);
    sampler.set_max_sampling_period(static_cast<microsecond_t>(max_sampling_period_us));
    sampler.set_baseline_core_pct(baseline_core_pct);
    sampler.set_p_stable_window_s(p_stable_window_s);
    sampler.set_p_stable_percentile(p_stable_percentile);
    sampler.set_interval(interval_s);
    sampler.get_echion().set_oncpu(oncpu);
    sampler.set_fast_copy_warmup_seconds(fast_copy_warmup_s);
}

extern "C" uint64_t
pyroscope_stack_interval_us()
{
    return Datadog::Sampler::get().get_interval_us();
}

extern "C" bool
pyroscope_stack_is_safe_copy_failed()
{
#if defined PL_LINUX
    return failed_safe_copy;
#else
    return false;
#endif
}

extern "C" bool
pyroscope_stack_fast_copy_initialized()
{
    return safe_memcpy_initialized;
}

extern "C" bool
pyroscope_stack_start()
{
    auto& sampler = Datadog::Sampler::get();
    {
        auto& echion = sampler.get_echion();
        const std::lock_guard<std::mutex> guard{ echion.thread_info_map_lock() };
        for (auto& [id, info] : echion.thread_info_map()) {
            (void)info->update_cpu_time();
        }
    }
    return sampler.start();
}

extern "C" void
pyroscope_stack_stop()
{
    auto& sampler = Datadog::Sampler::get();
    sampler.stop();
    sampler.get_echion().renderer().reset_string_cache(); // after the join, before stop_profilers clears the string table
}

extern "C" bool
pyroscope_stack_take_sampling_thread_error() noexcept
{
    return Datadog::Sampler::get().take_sampling_thread_error().has_value();
}

extern "C" uint8_t
pyroscope_stack_pause_sampling()
{
    return static_cast<uint8_t>(Datadog::Sampler::get().pause());
}

extern "C" void
pyroscope_stack_resume_sampling()
{
    Datadog::Sampler::get().resume();
}

extern "C" void
pyroscope_stack_uninstall_segv_handler()
{
    if (fast_copy_active) {
        uninstall_segv_handler();
    }
}

extern "C" void
pyroscope_stack_reinstall_segv_handler()
{
    if (fast_copy_active) {
        init_segv_catcher();
    }
}

extern "C" void
pyroscope_stack_register_thread(uint64_t id, uint64_t native_id)
{
    Datadog::Sampler::get().register_thread(id, native_id, "");
}

extern "C" void
pyroscope_stack_unregister_thread(uint64_t id)
{
    Datadog::Sampler::get().unregister_thread(id);
    Datadog::SpanLinks::get_instance().unlink_span(id);
}
