#include "dd_wrapper/include/sample_manager.hpp"
#include "pyroscope_ffi.h"
#include "sampler.hpp"
#include "span_links.hpp"
#include "cpu_timer.hpp"

#include "echion/echion_sampler.h"
#include "echion/vm.h"

#include <cstdint>
#include <mutex>

extern "C" void
pyroscope_stack_configure(double interval_s,
                          uint32_t max_nframes,
                          uint32_t max_threads,
                          uint32_t max_tasks,
                          bool oncpu,
                          bool adaptive_sampling,
                          double target_overhead,
                          uint64_t max_sampling_period_us,
                          double baseline_core_pct,
                          uint32_t p_stable_window_s,
                          double p_stable_percentile,
                          bool cpu_timer_enabled,
                          uint64_t cpu_timer_interval_ms
                          )
{
    static std::once_flag safe_copy_once;
    std::call_once(safe_copy_once, init_safe_copy);
    Datadog::SampleManager::set_max_nframes(max_nframes);
    auto& sampler = Datadog::Sampler::get();
    sampler.set_max_frames(max_nframes);
    sampler.set_max_threads_per_sample(max_threads);
    sampler.set_max_tasks_per_sample(max_tasks);
    sampler.set_adaptive_sampling(adaptive_sampling);
    sampler.set_target_overhead(target_overhead);
    sampler.set_max_sampling_period(static_cast<microsecond_t>(max_sampling_period_us));
    sampler.set_baseline_core_pct(baseline_core_pct);
    sampler.set_p_stable_window_s(p_stable_window_s);
    sampler.set_p_stable_percentile(p_stable_percentile);
    sampler.set_interval(interval_s);
    sampler.get_echion().set_oncpu(oncpu);
    Datadog::CpuTimer::Engine::get().configure(cpu_timer_enabled, cpu_timer_interval_ms);

}

extern "C" uint64_t
pyroscope_stack_interval_us()
{
    return Datadog::Sampler::get().get_interval_us();
}

extern "C" bool
pyroscope_stack_is_safe_copy_failed()
{
    return failed_safe_copy;
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
pyroscope_stack_take_sampling_thread_error()
{
    return Datadog::Sampler::get().take_sampling_thread_error().has_value();
}

extern "C" void
pyroscope_stack_register_thread_gil(uint64_t id, uint64_t native_id)
{
    PyThreadState* tstate = PyThreadState_Get();
    // stack.register_thread may be called for already-active threads
    // from a different Python thread. Only pass a PyThreadState pointer when it
    // belongs to the registered thread; timer_create signal capture dereferences
    // this pointer on the target native thread.
    if (tstate != nullptr && tstate->thread_id != id) {
        tstate = nullptr;
    }
    Py_BEGIN_ALLOW_THREADS;
    Datadog::Sampler::get().register_thread(id, native_id, "", tstate);
    Py_END_ALLOW_THREADS;
}

extern "C" void
pyroscope_stack_unregister_thread_gil(uint64_t id)
{
    Py_BEGIN_ALLOW_THREADS;
    Datadog::Sampler::get().unregister_thread(id);
    Datadog::SpanLinks::get_instance().unlink_span(id);
    Py_END_ALLOW_THREADS;
}

extern "C" void
pyroscope_stack_init_asyncio(PyObject* scheduled_tasks, PyObject* eager_tasks)
{
    Datadog::Sampler::get().init_asyncio(scheduled_tasks, eager_tasks);
}

extern "C" void
pyroscope_stack_track_asyncio_loop(uint64_t thread_id, PyObject* loop)
{
    Datadog::Sampler::get().track_asyncio_loop(static_cast<uintptr_t>(thread_id), loop);
}

extern "C" void
pyroscope_stack_link_tasks(PyObject* parent, PyObject* child)
{
    Datadog::Sampler::get().link_tasks(parent, child);
}

extern "C" void
pyroscope_stack_weak_link_tasks(PyObject* parent, PyObject* child)
{
    Datadog::Sampler::get().weak_link_tasks(parent, child);
}

extern "C" bool
pyroscope_stack_set_uvloop_mode(uint64_t thread_id, bool value)
{
    auto& sampler = Datadog::Sampler::get();
    sampler.set_uvloop_mode(static_cast<uintptr_t>(thread_id), value);

    auto& echion = sampler.get_echion();
    const std::lock_guard<std::mutex> guard{ echion.thread_info_map_lock() };
    auto& map = echion.thread_info_map();
    auto it = map.find(static_cast<uintptr_t>(thread_id));
    return it != map.end() && it->second->using_uvloop == value;
}
