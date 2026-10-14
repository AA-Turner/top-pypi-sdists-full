#pragma once

#include "constants.hpp"
#include "profiler_state.hpp"
#include "sample.hpp"

namespace Datadog {

class SampleManager
{
  public:
    static Sample* start_sample()
    {
        static thread_local Sample sample{ ProfilerState::get().max_nframes.load(),
                                           PprofBuilderType_CpuWall };
        sample.clear();
        return &sample;
    }

    static void set_max_nframes(unsigned int _max_nframes)
    {
        auto& state = ProfilerState::get();
        if (_max_nframes > 0) {
            state.max_nframes = _max_nframes;
        }
        if (state.max_nframes > g_backend_max_nframes) {
            state.max_nframes = g_backend_max_nframes;
        }
    }

    static void drop_sample([[maybe_unused]] Sample* sample) {}
};

} // namespace Datadog
