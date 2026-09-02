// FPS Safety Valve (T-042 to T-045)
//
// Caps the maximum frame rate across all graphical protocol handlers by
// enforcing a minimum inter-frame interval. When the interval is zero,
// the valve is disabled (no cap). When enabled, a frame is allowed only
// if at least `min_interval` has elapsed since the previous frame.
//
// Design note: wait_for_slot() does NOT call tokio::time::sleep internally.
// On Windows, tokio::time::sleep has 15-16ms timer granularity — sleeping for
// a 10ms interval would cap at ~60 FPS instead of 100 FPS.
//
// Instead, callers use the returned `Instant` deadline:
//   if let Some(until) = valve.next_slot() {
//       tokio::time::sleep_until(until.into()).await;
//   }
// tokio::time::sleep_until with a non-zero interval is also affected by Windows
// timer granularity, so for sub-15ms intervals the effective cap is ~67 FPS
// on Windows. This is a hardware limitation, not a code bug.
//
// AC-1: At default 10ms interval no handler exceeds 100 FPS sustained.
// AC-2: The interval is configurable at startup via FpsValve::new(interval).
// AC-3: Applied to all 9 graphical handlers by using FpsValve::next_slot().
// AC-4: interval == 0 disables the valve (next_slot returns None).
// AC-5: Frames already below the cap return None immediately (no added latency).

use std::time::{Duration, Instant};

/// Configurable FPS cap enforced via minimum inter-frame interval.
///
/// Usage (per handler, in the frame-send loop):
/// ```ignore
/// let mut valve = FpsValve::new(Duration::from_millis(10)); // 100 FPS cap
/// loop {
///     if let Some(until) = valve.next_slot() {
///         tokio::time::sleep_until(until.into()).await;
///     }
///     valve.record_frame();
///     send_frame().await?;
/// }
/// ```
pub struct FpsValve {
    /// Minimum time between successive frames.
    /// Zero = disabled (no cap).
    min_interval: Duration,
    /// Instant of the most recently sent frame.
    last_frame: Option<Instant>,
}

impl FpsValve {
    /// Create a new valve with the given minimum inter-frame interval.
    ///
    /// Pass `Duration::ZERO` to disable the valve (AC-4).
    pub fn new(min_interval: Duration) -> Self {
        Self {
            min_interval,
            last_frame: None,
        }
    }

    /// Create a valve with the default 10ms interval (100 FPS cap, AC-1).
    pub fn default_cap() -> Self {
        Self::new(Duration::from_millis(10))
    }

    /// Create a disabled valve (no cap, AC-4).
    pub fn disabled() -> Self {
        Self::new(Duration::ZERO)
    }

    /// Return the `Instant` at which the next frame may be sent, or `None` if
    /// the frame can be sent immediately.
    ///
    /// - `None` when the valve is disabled (interval == 0, AC-4).
    /// - `None` when enough time has elapsed since the last frame (AC-5).
    /// - `Some(deadline)` when the caller should wait until `deadline`.
    ///
    /// The caller awaits if needed:
    /// ```ignore
    /// if let Some(until) = valve.next_slot() {
    ///     tokio::time::sleep_until(until.into()).await;
    /// }
    /// valve.record_frame();
    /// ```
    pub fn next_slot(&self) -> Option<Instant> {
        if self.min_interval.is_zero() {
            return None; // AC-4: disabled
        }
        self.last_frame.and_then(|last| {
            let elapsed = last.elapsed();
            if elapsed >= self.min_interval {
                None // AC-5: already past the interval, no wait needed
            } else {
                Some(last + self.min_interval)
            }
        })
    }

    /// Record that a frame was just sent. Must be called after each send.
    pub fn record_frame(&mut self) {
        self.last_frame = Some(Instant::now());
    }

    /// Backward-compatible async helper.
    ///
    /// Awaits `sleep_until` if a delay is needed, then records the frame.
    /// Prefer the `next_slot()` + `record_frame()` pattern for clarity.
    ///
    /// NOTE: On Windows tokio::time::sleep_until rounds up to ~15ms. For
    /// intervals < 15ms this means effective cap is ~67 FPS, not 100 FPS.
    /// This is the OS timer limit — not a code defect.
    pub async fn wait_for_slot(&mut self) {
        if let Some(until) = self.next_slot() {
            tokio::time::sleep_until(tokio::time::Instant::from_std(until)).await;
        }
        self.record_frame();
    }

    /// Synchronous check: returns `Some(Duration)` to wait, or `None` if ready.
    /// Used in non-async contexts or for metrics.
    pub fn check(&self) -> Option<Duration> {
        if self.min_interval.is_zero() {
            return None;
        }
        self.last_frame.and_then(|last| {
            let elapsed = last.elapsed();
            if elapsed < self.min_interval {
                Some(self.min_interval - elapsed)
            } else {
                None
            }
        })
    }

    /// Return the configured minimum inter-frame interval.
    pub fn min_interval(&self) -> Duration {
        self.min_interval
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Instant;

    // AC-4: disabled valve always returns None.
    #[test]
    fn test_disabled_valve_no_wait() {
        let valve = FpsValve::disabled();
        assert_eq!(
            valve.next_slot(),
            None,
            "disabled valve must never request wait"
        );
        assert_eq!(valve.check(), None);
    }

    // AC-5: first frame after valve creation is always allowed immediately.
    #[test]
    fn test_first_frame_no_wait() {
        let valve = FpsValve::new(Duration::from_millis(10));
        assert_eq!(
            valve.next_slot(),
            None,
            "first frame has no prior timestamp"
        );
    }

    // AC-5: frame sent after interval elapsed requires no wait.
    #[test]
    fn test_frame_after_interval_no_wait() {
        let mut valve = FpsValve::new(Duration::from_millis(1));
        valve.record_frame();
        std::thread::sleep(Duration::from_millis(5)); // wait > interval
        assert_eq!(
            valve.next_slot(),
            None,
            "post-interval frame must not add latency"
        );
    }

    // AC-1: frame sent before interval returns a deadline.
    #[test]
    fn test_frame_before_interval_returns_deadline() {
        let mut valve = FpsValve::new(Duration::from_millis(100));
        valve.record_frame();
        let slot = valve.next_slot();
        assert!(
            slot.is_some(),
            "frame sent immediately after previous needs deadline"
        );
        assert!(
            slot.unwrap() > Instant::now(),
            "deadline must be in the future"
        );
    }

    // AC-2: min_interval is configurable.
    #[test]
    fn test_configurable_interval() {
        let v50 = FpsValve::new(Duration::from_millis(50));
        assert_eq!(v50.min_interval(), Duration::from_millis(50));
    }

    // AC-1: default_cap is 10ms.
    #[test]
    fn test_default_cap_is_10ms() {
        assert_eq!(
            FpsValve::default_cap().min_interval(),
            Duration::from_millis(10)
        );
    }

    // wait_for_slot records the frame after sleeping.
    #[tokio::test]
    async fn test_async_wait_for_slot_records_frame() {
        let mut valve = FpsValve::new(Duration::from_millis(1));
        valve.wait_for_slot().await; // first — no wait
        assert!(
            valve.last_frame.is_some(),
            "frame must be recorded after wait_for_slot"
        );
    }
}
