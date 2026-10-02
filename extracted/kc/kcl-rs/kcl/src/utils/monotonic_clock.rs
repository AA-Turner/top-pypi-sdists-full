//! The process-wide monotonic nanosecond clock — the port of Java's global
//! `System.nanoTime()`.
//!
//! Java code freely compares `nanoTime()` values captured by *different*
//! components (the lease taker stamps `lastCounterIncrementNanos`, the renewer
//! checks lease expiry against it, the discoverer stamps freshly discovered
//! leases). Those comparisons are only meaningful against a single time base,
//! so every component MUST read this one clock. Do NOT re-create a file-local
//! `OnceLock<Instant>` epoch: each such static anchors to whenever that file's
//! clock is *first called*, and two components whose clocks warm up minutes
//! apart will disagree by minutes — e.g. a lease stamped on one epoch looks
//! instantly expired on the other.

use std::sync::OnceLock;
use std::time::Instant;

/// Monotonic "now" in nanoseconds since one process-wide arbitrary epoch
/// (first use). Values are comparable across all callers in the process,
/// mirroring Java `System.nanoTime()`.
pub(crate) fn monotonic_nanos() -> i64 {
    static EPOCH: OnceLock<Instant> = OnceLock::new();
    let epoch = EPOCH.get_or_init(Instant::now);
    Instant::now().duration_since(*epoch).as_nanos() as i64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn is_monotonic_and_shared() {
        let a = monotonic_nanos();
        let b = monotonic_nanos();
        assert!(b >= a);
        // Two readings moments apart must be on the same epoch (a fresh
        // per-call epoch would reset toward 0 instead of advancing).
        let c = monotonic_nanos();
        assert!(c >= b);
    }
}
