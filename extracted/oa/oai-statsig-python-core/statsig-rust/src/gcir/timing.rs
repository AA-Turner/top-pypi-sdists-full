#[cfg(feature = "gcir-bench-timings")]
use std::{
    collections::HashMap,
    sync::{
        atomic::{AtomicBool, Ordering},
        Mutex, OnceLock,
    },
    time::{Duration, Instant},
};

#[cfg(feature = "gcir-bench-timings")]
static ENABLED: AtomicBool = AtomicBool::new(false);
#[cfg(feature = "gcir-bench-timings")]
static TIMINGS: OnceLock<Mutex<HashMap<&'static str, TimingAggregate>>> = OnceLock::new();

#[derive(Clone, Debug)]
pub struct TimingEntry {
    pub label: &'static str,
    pub total_ns: u128,
    pub count: u64,
}

#[cfg(feature = "gcir-bench-timings")]
#[derive(Clone, Copy, Debug, Default)]
struct TimingAggregate {
    total_ns: u128,
    count: u64,
}

#[doc(hidden)]
#[cfg(feature = "gcir-bench-timings")]
pub fn enable(enabled: bool) {
    ENABLED.store(enabled, Ordering::Relaxed);
}

#[doc(hidden)]
#[cfg(not(feature = "gcir-bench-timings"))]
pub fn enable(_: bool) {}

#[doc(hidden)]
#[cfg(feature = "gcir-bench-timings")]
pub fn reset() {
    let mut timings = timings().lock().expect("gcir timing mutex poisoned");
    timings.clear();
}

#[doc(hidden)]
#[cfg(not(feature = "gcir-bench-timings"))]
pub fn reset() {}

#[doc(hidden)]
#[cfg(feature = "gcir-bench-timings")]
pub fn take() -> Vec<TimingEntry> {
    let mut timings = timings().lock().expect("gcir timing mutex poisoned");
    let mut entries = timings
        .drain()
        .map(|(label, aggregate)| TimingEntry {
            label,
            total_ns: aggregate.total_ns,
            count: aggregate.count,
        })
        .collect::<Vec<_>>();
    entries.sort_by(|a, b| {
        b.total_ns
            .cmp(&a.total_ns)
            .then_with(|| a.label.cmp(b.label))
    });
    entries
}

#[doc(hidden)]
#[cfg(not(feature = "gcir-bench-timings"))]
pub fn take() -> Vec<TimingEntry> {
    Vec::new()
}

#[cfg(feature = "gcir-bench-timings")]
pub(crate) fn is_enabled() -> bool {
    ENABLED.load(Ordering::Relaxed)
}

#[cfg(feature = "gcir-bench-timings")]
pub(crate) struct Timer {
    enabled: bool,
}

#[cfg(feature = "gcir-bench-timings")]
impl Timer {
    #[inline(always)]
    pub(crate) fn current() -> Self {
        Self {
            enabled: is_enabled(),
        }
    }

    #[inline(always)]
    pub(crate) fn time<T>(&self, label: &'static str, f: impl FnOnce() -> T) -> T {
        if !self.enabled {
            return f();
        }

        let start = Instant::now();
        let result = f();
        record_elapsed(label, start.elapsed());
        result
    }
}

#[cfg(feature = "gcir-bench-timings")]
pub(crate) fn time<T>(label: &'static str, f: impl FnOnce() -> T) -> T {
    Timer::current().time(label, f)
}

#[cfg(feature = "gcir-bench-timings")]
fn record_elapsed(label: &'static str, elapsed: Duration) {
    let mut timings = timings().lock().expect("gcir timing mutex poisoned");
    let entry = timings.entry(label).or_default();
    entry.total_ns += elapsed.as_nanos();
    entry.count += 1;
}

#[cfg(feature = "gcir-bench-timings")]
fn timings() -> &'static Mutex<HashMap<&'static str, TimingAggregate>> {
    TIMINGS.get_or_init(|| Mutex::new(HashMap::new()))
}
