//! Port of `software.amazon.kinesis.retrieval.ThrottlingReporter`.
//!
//! Tracks consecutive throttle events per shard and logs at WARN until a
//! configurable threshold, then escalates to ERROR. Not thread-safety-annotated
//! in Java (called only from a single daemon thread's retrieval attempt); the
//! Rust equivalent keeps the same single-writer assumption (`&mut self`).

use std::sync::Arc;

/// The severity of a throttling log line, extracted so tests can observe which
/// level a `throttled()` call would emit (the Java tests verify `warn` vs
/// `error` counts by mocking `getLog()`).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ThrottleLogLevel {
    /// Below-or-at the consecutive-throttle threshold: logged at WARN.
    Warn,
    /// Above the threshold: escalated to ERROR.
    Error,
}

/// Sink for throttling log lines. The production sink emits via `tracing`; tests
/// inject a recording sink (the analog of the Java test's mocked `getLog()`).
pub trait ThrottleLogSink: Send + Sync {
    /// Emit a throttling message at the given level.
    fn log(&self, level: ThrottleLogLevel, message: &str);
}

/// Default sink: emits to `tracing` at WARN/ERROR (matching Java's SLF4J levels).
struct TracingSink;

impl ThrottleLogSink for TracingSink {
    fn log(&self, level: ThrottleLogLevel, message: &str) {
        match level {
            ThrottleLogLevel::Warn => {
                tracing::warn!(target: "kcl::retrieval::throttling", "{message}")
            }
            ThrottleLogLevel::Error => {
                tracing::error!(target: "kcl::retrieval::throttling", "{message}")
            }
        }
    }
}

/// Reports consecutive throttling events for a shard, escalating from WARN to
/// ERROR once `max_consecutive_warn_throttles` is exceeded.
///
/// Port of the Java `@RequiredArgsConstructor` class. The Java `getLog()` seam
/// is replaced by the injectable [`ThrottleLogSink`].
pub struct ThrottlingReporter {
    max_consecutive_warn_throttles: i32,
    shard_id: String,
    consecutive_throttles: i32,
    log: Arc<dyn ThrottleLogSink>,
}

impl ThrottlingReporter {
    /// Construct with the WARN→ERROR threshold and the shard id, logging via
    /// `tracing`.
    pub fn new(max_consecutive_warn_throttles: i32, shard_id: impl Into<String>) -> Self {
        Self::with_log(
            max_consecutive_warn_throttles,
            shard_id,
            Arc::new(TracingSink),
        )
    }

    /// Construct with an explicit log sink (test seam for the Java overridden
    /// `getLog()`).
    pub fn with_log(
        max_consecutive_warn_throttles: i32,
        shard_id: impl Into<String>,
        log: Arc<dyn ThrottleLogSink>,
    ) -> Self {
        Self {
            max_consecutive_warn_throttles,
            shard_id: shard_id.into(),
            consecutive_throttles: 0,
            log,
        }
    }

    /// Record a throttle event: increment the counter, then log at WARN, or at
    /// ERROR once the count exceeds the threshold.
    pub fn throttled(&mut self) {
        self.consecutive_throttles += 1;
        let message = format!(
            "Shard '{}' has been throttled {} consecutively",
            self.shard_id, self.consecutive_throttles
        );

        let level = if self.consecutive_throttles > self.max_consecutive_warn_throttles {
            ThrottleLogLevel::Error
        } else {
            ThrottleLogLevel::Warn
        };
        self.log.log(level, &message);
    }

    /// Reset the consecutive-throttle counter to zero (a successful retrieval).
    pub fn success(&mut self) {
        self.consecutive_throttles = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Mutex;

    /// Recording sink standing in for the Java mocked `Logger`.
    #[derive(Default)]
    struct RecordingSink {
        warns: Mutex<usize>,
        errors: Mutex<usize>,
    }

    impl ThrottleLogSink for RecordingSink {
        fn log(&self, level: ThrottleLogLevel, _message: &str) {
            match level {
                ThrottleLogLevel::Warn => *self.warns.lock().unwrap() += 1,
                ThrottleLogLevel::Error => *self.errors.lock().unwrap() += 1,
            }
        }
    }

    const SHARD_ID: &str = "Shard-001";

    #[test]
    fn test_less_than_max_throttles() {
        let sink = Arc::new(RecordingSink::default());
        let mut reporter = ThrottlingReporter::with_log(5, SHARD_ID, sink.clone());
        reporter.throttled();
        assert_eq!(*sink.warns.lock().unwrap(), 1);
        assert_eq!(*sink.errors.lock().unwrap(), 0);
    }

    #[test]
    fn test_more_than_max_throttles() {
        let sink = Arc::new(RecordingSink::default());
        let mut reporter = ThrottlingReporter::with_log(1, SHARD_ID, sink.clone());
        reporter.throttled();
        reporter.throttled();
        assert_eq!(*sink.warns.lock().unwrap(), 1);
        assert_eq!(*sink.errors.lock().unwrap(), 1);
    }

    #[test]
    fn test_success_resets_errors() {
        let sink = Arc::new(RecordingSink::default());
        let mut reporter = ThrottlingReporter::with_log(1, SHARD_ID, sink.clone());
        reporter.throttled();
        reporter.throttled();
        reporter.throttled();
        reporter.throttled();
        reporter.success();
        reporter.throttled();
        assert_eq!(*sink.warns.lock().unwrap(), 2);
        assert_eq!(*sink.errors.lock().unwrap(), 3);
    }
}
