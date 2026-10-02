//! Injectable millisecond clock, mirroring `java.time.Clock` as used by the
//! cgroup CPU worker metrics (only `Clock.millis()` is used).
//!
//! Java tests mock `Clock.millis()` to return a fixed sequence
//! (`when(clock.millis()).thenReturn(1000L, 2000L)`). [`Clock::mock`] reproduces
//! that: successive calls pop from a queue.

use std::sync::Arc;
use std::sync::Mutex;

/// A clock returning epoch milliseconds. Cheap to clone (shares the backing
/// closure).
#[derive(Clone)]
pub struct Clock {
    now_millis: Arc<dyn Fn() -> i64 + Send + Sync>,
}

impl Clock {
    /// System UTC clock (Java `Clock.systemUTC()`).
    pub fn system_utc() -> Self {
        Self {
            now_millis: Arc::new(|| {
                use std::time::{SystemTime, UNIX_EPOCH};
                SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .map(|d| d.as_millis() as i64)
                    .unwrap_or(0)
            }),
        }
    }

    /// A clock backed by an arbitrary closure.
    pub fn from_fn(f: impl Fn() -> i64 + Send + Sync + 'static) -> Self {
        Self {
            now_millis: Arc::new(f),
        }
    }

    /// A mock clock returning the given sequence of millis on successive calls.
    /// After the sequence is exhausted, the last value repeats (matching
    /// Mockito's `thenReturn(a, b)` "stick on last" behavior).
    pub fn mock(values: Vec<i64>) -> Self {
        let state = Mutex::new((values, 0usize));
        Self {
            now_millis: Arc::new(move || {
                let mut guard = state.lock().unwrap();
                let (ref vals, ref mut idx) = *guard;
                if vals.is_empty() {
                    return 0;
                }
                let i = (*idx).min(vals.len() - 1);
                let v = vals[i];
                *idx += 1;
                v
            }),
        }
    }

    /// Current epoch millis (Java `Clock.millis()`).
    pub fn millis(&self) -> i64 {
        (self.now_millis)()
    }
}

impl std::fmt::Debug for Clock {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("Clock")
    }
}
