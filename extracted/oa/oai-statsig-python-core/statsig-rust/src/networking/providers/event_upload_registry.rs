use super::net_provider_reqwest::EventUploadTransport;
use crate::statsig_global::StatsigGlobal;
use arc_swap::ArcSwapOption;
use std::sync::{Arc, OnceLock, Weak};

static REGISTRY: ArcSwapOption<RegistryState> = ArcSwapOption::const_empty();

struct RegistryState {
    global: Weak<StatsigGlobal>,
    pid: u32,
    transport: OnceLock<Arc<EventUploadTransport>>,
}

impl RegistryState {
    fn new(global: &Arc<StatsigGlobal>) -> Self {
        Self {
            global: Arc::downgrade(global),
            pid: global.pid,
            transport: OnceLock::new(),
        }
    }

    fn belongs_to(&self, global: &Arc<StatsigGlobal>) -> bool {
        std::ptr::eq(self.global.as_ptr(), Arc::as_ptr(global))
    }
}

pub(super) fn get() -> Arc<EventUploadTransport> {
    loop {
        let current = REGISTRY.load_full();
        let global = StatsigGlobal::get();
        if let Some(state) = current.as_ref().filter(|state| state.belongs_to(&global)) {
            return state
                .transport
                .get_or_init(|| Arc::new(EventUploadTransport::new()))
                .clone();
        }

        let replacement = Some(Arc::new(RegistryState::new(&global)));
        let previous = REGISTRY.compare_and_swap(&current, replacement);
        if let (Some(state), Some(previous)) = (current, previous.as_ref()) {
            if Arc::ptr_eq(&state, previous) && state.pid != global.pid {
                // As with StatsigGlobal's runtime, do not destroy a reqwest client
                // copied from the parent process. Its runtime and locks are inherited.
                std::mem::forget(state);
            }
        }
    }
}

pub(super) fn reset(previous_global: &Arc<StatsigGlobal>) {
    let current = REGISTRY.load_full();
    if current
        .as_ref()
        .is_some_and(|state| state.belongs_to(previous_global))
    {
        REGISTRY.compare_and_swap(&current, None);
    }
}
