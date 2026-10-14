#include "profiler_state.hpp"

namespace Datadog {

ProfilerState&
ProfilerState::get()
{
    // Keep process-global profiler state alive until the OS reclaims it. Some embedders,
    // including uWSGI, run native atexit handlers before finalizing Python. Python
    // finalization can still invoke native sys.monitoring callbacks, so destroying this
    // state at native atexit would leave those callbacks accessing freed registries.
    static ProfilerState* const instance = new ProfilerState();
    return *instance;
}

} // namespace Datadog
