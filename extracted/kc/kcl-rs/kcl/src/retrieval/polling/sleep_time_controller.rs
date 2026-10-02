//! Port of `software.amazon.kinesis.retrieval.polling.SleepTimeController`,
//! `SleepTimeControllerConfig`, and `KinesisSleepTimeController`.
//!
//! These three tightly-coupled Java files are grouped into one Rust module: the
//! [`SleepTimeController`] trait (the pluggable strategy), the
//! [`SleepTimeControllerConfig`] value object it consumes, and the default
//! [`KinesisSleepTimeController`] implementation.

use std::time::Instant;

/// Immutable snapshot of the state needed to compute the next inter-`GetRecords`
/// sleep duration.
///
/// Port of the Lombok `@Data @Builder @Accessors(fluent=true)` value object.
/// Nullable Java fields (`Instant`, `Integer`, `Long`) map to `Option`;
/// `idleMillisBetweenCalls` is a primitive `long` (never null) → `i64`.
///
/// `last_records_count` is populated by the publisher but unused by
/// [`KinesisSleepTimeController`]'s algorithm; it is preserved for API/plugin
/// parity (a custom controller may consult it).
#[derive(Debug, Clone, Default, bon::Builder)]
pub struct SleepTimeControllerConfig {
    /// The wall-clock time of the last successful `GetRecords` call, if any.
    last_successful_call: Option<Instant>,
    /// The configured idle interval between calls (millis).
    #[builder(default)]
    idle_millis_between_calls: i64,
    /// The record count returned by the last call (unused by the default controller).
    last_records_count: Option<i32>,
    /// The `millisBehindLatest` of the last call, if any.
    last_millis_behind_latest: Option<i64>,
    /// The `millisBehindLatest` threshold that triggers reduced TPS near the tip.
    millis_behind_latest_threshold_for_reduced_tps: Option<i64>,
}

impl SleepTimeControllerConfig {
    /// The wall-clock time of the last successful `GetRecords` call.
    pub fn last_successful_call(&self) -> Option<Instant> {
        self.last_successful_call
    }

    /// The configured idle interval between calls (millis).
    pub fn idle_millis_between_calls(&self) -> i64 {
        self.idle_millis_between_calls
    }

    /// The record count returned by the last call.
    pub fn last_records_count(&self) -> Option<i32> {
        self.last_records_count
    }

    /// The `millisBehindLatest` of the last call.
    pub fn last_millis_behind_latest(&self) -> Option<i64> {
        self.last_millis_behind_latest
    }

    /// The `millisBehindLatest` threshold that triggers reduced TPS.
    pub fn millis_behind_latest_threshold_for_reduced_tps(&self) -> Option<i64> {
        self.millis_behind_latest_threshold_for_reduced_tps
    }
}

/// Strategy for computing the sleep duration before the next `GetRecords` call.
///
/// Port of the Java interface. Pluggable via `PollingConfig::sleep_time_controller`
/// (default [`KinesisSleepTimeController`]).
pub trait SleepTimeController: Send + Sync {
    /// Compute the sleep time (millis) before the next `GetRecords` call.
    ///
    /// Takes an explicit `now` so callers/tests can control the clock; the
    /// production caller passes [`Instant::now`].
    fn get_sleep_time_millis(&self, config: &SleepTimeControllerConfig, now: Instant) -> i64;
}

/// Default [`SleepTimeController`]: a fixed idle interval plus an additional
/// "reduced TPS near the tip of the stream" backoff.
///
/// Port of `KinesisSleepTimeController`. The Java code reads `Instant.now()`
/// internally; the Rust port threads an explicit `now` through
/// [`SleepTimeController::get_sleep_time_millis`] for deterministic testing
/// (the production caller passes the real clock).
#[derive(Debug, Clone, Copy, Default)]
pub struct KinesisSleepTimeController;

impl SleepTimeController for KinesisSleepTimeController {
    fn get_sleep_time_millis(&self, config: &SleepTimeControllerConfig, now: Instant) -> i64 {
        let idle_millis_between_calls = config.idle_millis_between_calls();
        let last_successful_call = match config.last_successful_call() {
            None => return idle_millis_between_calls,
            Some(t) => t,
        };

        // abs(Duration.between(lastSuccessfulCall, now)).toMillis(): guard against
        // clock skew making the duration negative.
        let time_since_last_call = if now >= last_successful_call {
            now.duration_since(last_successful_call).as_millis() as i64
        } else {
            last_successful_call.duration_since(now).as_millis() as i64
        };

        let mut idle_sleep_time = 0i64;
        if time_since_last_call < idle_millis_between_calls {
            idle_sleep_time = idle_millis_between_calls - time_since_last_call;
        }

        let mut reduced_tps_sleep_time = 0i64;
        let last_millis_behind_latest = config.last_millis_behind_latest();
        let millis_behind_threshold = config.millis_behind_latest_threshold_for_reduced_tps();
        if let (Some(last_behind), Some(threshold)) =
            (last_millis_behind_latest, millis_behind_threshold)
        {
            if last_behind < threshold {
                // NOTE: not clamped to >= 0 inline; the final Math.max floors it.
                reduced_tps_sleep_time = threshold - time_since_last_call;
            }
        }

        idle_sleep_time.max(reduced_tps_sleep_time)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::Duration;

    #[test]
    fn null_last_call_returns_idle() {
        let cfg = SleepTimeControllerConfig::builder()
            .idle_millis_between_calls(1500)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, Instant::now()),
            1500
        );
    }

    #[test]
    fn idle_sleep_is_remaining_interval() {
        let now = Instant::now();
        let last = now - Duration::from_millis(500);
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1500)
            .build();
        // 1500 - 500 = 1000
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            1000
        );
    }

    #[test]
    fn no_sleep_when_interval_elapsed() {
        let now = Instant::now();
        let last = now - Duration::from_millis(2000);
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1500)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            0
        );
    }

    #[test]
    fn reduced_tps_backoff_when_near_tip() {
        let now = Instant::now();
        let last = now - Duration::from_millis(100);
        // near-tip: lastMillisBehindLatest(50) < threshold(3000)
        // idleSleepTime = 1500 - 100 = 1400; reducedTps = 3000 - 100 = 2900; max = 2900
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1500)
            .last_millis_behind_latest(50)
            .millis_behind_latest_threshold_for_reduced_tps(3000)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            2900
        );
    }

    #[test]
    fn reduced_tps_not_triggered_when_far_from_tip() {
        let now = Instant::now();
        let last = now - Duration::from_millis(100);
        // far from tip: lastMillisBehindLatest(5000) >= threshold(3000) -> no reduced tps
        // idleSleepTime = 1500 - 100 = 1400
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1500)
            .last_millis_behind_latest(5000)
            .millis_behind_latest_threshold_for_reduced_tps(3000)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            1400
        );
    }

    /// Port of `testGetSleepTimeMillisWithFutureLastSuccessfulCall`. When the
    /// last-successful-call time is in the future, `Duration.abs()` treats it the
    /// same as the equivalent gap in the past. The Rust port threads `now`
    /// explicitly, so the result is exact rather than approximate.
    #[test]
    fn future_last_call_treated_as_abs_gap() {
        let now = Instant::now();
        let future_call = now + Duration::from_millis(500); // 500ms in the future
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(future_call)
            .idle_millis_between_calls(1000)
            .last_records_count(10)
            .last_millis_behind_latest(5000)
            .build();
        // abs(500) elapsed -> 1000 - 500 = 500
        let sleep_time = KinesisSleepTimeController.get_sleep_time_millis(&cfg, now);
        assert!(sleep_time > 0 && sleep_time <= 1000);
        assert_eq!(sleep_time, 500);
    }

    /// Port of `testGetSleepTimeMillisWithDifferentIdleTimes`.
    #[test]
    fn different_idle_times() {
        let now = Instant::now();
        let last = now - Duration::from_millis(300);

        // shorter idle time: 500 - 300 = 200
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(500)
            .last_records_count(10)
            .last_millis_behind_latest(5000)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            200
        );

        // longer idle time: 2000 - 300 = 1700
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(2000)
            .last_records_count(10)
            .last_millis_behind_latest(5000)
            .build();
        assert_eq!(
            KinesisSleepTimeController.get_sleep_time_millis(&cfg, now),
            1700
        );
    }

    /// Port of `testGetSleepTimeMillisIgnoresRecordCountAndMillisBehindLatest`.
    /// The default controller ignores `lastRecordsCount`; and
    /// `lastMillisBehindLatest` only matters when the reduced-TPS threshold is
    /// set (which it is not here), so the two configs yield identical sleep times.
    #[test]
    fn ignores_record_count_and_millis_behind_latest() {
        let now = Instant::now();
        let last = now - Duration::from_millis(500);

        let cfg1 = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1000)
            .last_records_count(0)
            .last_millis_behind_latest(0)
            .build();
        let sleep_time_1 = KinesisSleepTimeController.get_sleep_time_millis(&cfg1, now);

        let cfg2 = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1000)
            .last_records_count(100)
            .last_millis_behind_latest(10000)
            .build();
        let sleep_time_2 = KinesisSleepTimeController.get_sleep_time_millis(&cfg2, now);

        assert_eq!(sleep_time_1, sleep_time_2);
    }

    /// Port of `testGetSleepTimeMillisWithReducedTpsThresholdHigherIdleMillisWait`.
    /// At the tip (`lastMillisBehindLatest` < threshold) but the idle-interval
    /// wait dominates the reduced-TPS wait, so `max` picks the idle wait.
    #[test]
    fn reduced_tps_but_idle_wait_dominates() {
        let now = Instant::now();
        let last = now - Duration::from_millis(300);
        // idleSleepTime = 1000 - 300 = 700; reducedTps = 200 - 300 = -100; max = 700
        let cfg = SleepTimeControllerConfig::builder()
            .last_successful_call(last)
            .idle_millis_between_calls(1000)
            .last_records_count(10)
            .last_millis_behind_latest(0)
            .millis_behind_latest_threshold_for_reduced_tps(200)
            .build();
        let sleep_time = KinesisSleepTimeController.get_sleep_time_millis(&cfg, now);
        assert!(sleep_time > 0 && sleep_time <= 1000);
        assert_eq!(sleep_time, 700);
    }
}
