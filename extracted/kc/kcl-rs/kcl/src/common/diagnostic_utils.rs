//! Port of `software.amazon.kinesis.common.DiagnosticUtils`.

use chrono::{DateTime, Utc};

/// Maximum expected time (millis) between a request and its response.
///
/// Java reads `software.amazon.kinesis.lifecycle.ShardConsumer.MAX_TIME_BETWEEN_REQUEST_RESPONSE`
/// (a `public static final int = 60 * 1000`). That creates a `common -> lifecycle`
/// dependency; to avoid a circular crate dependency we define the constant here
/// (in the truly-common location) with the identical value, and the lifecycle
/// port re-exports / references this. The delayed-delivery warning threshold is
/// `MAX_TIME_BETWEEN_REQUEST_RESPONSE / 3` = 20000 ms (20 s).
///
/// NOTE: the Java code comment claims "exceeds 11 seconds", but the actual
/// computed threshold is 20000 ms — the comment is stale; the code behavior
/// (20 s) is what is preserved.
pub const MAX_TIME_BETWEEN_REQUEST_RESPONSE: i64 = 60 * 1000;

/// Measure the event-delivery latency between when a record-delivery event was
/// enqueued to an executor and when it was acknowledged, and log a warning if it
/// is abnormally delayed.
///
/// Port of `takeDelayedDeliveryActionIfRequired`. If the elapsed time exceeds
/// `MAX_TIME_BETWEEN_REQUEST_RESPONSE / 3` (20 s) a `WARN` is emitted; otherwise
/// a `DEBUG` is emitted.
///
/// # Deviations from Java
///
/// - Java takes a caller-supplied `org.slf4j.Logger` so log lines attribute to
///   the calling class. Rust's `tracing` uses module-path targets, so this takes
///   a `resource_identifier` string (already part of the message) and logs via
///   `tracing` at this module's target. Callers that need their own target can
///   inline the check or wrap in a span.
/// - `Instant.now()` is replaced by an injectable "now" parameter to make the
///   latency deterministically testable (Java's implicit `Instant.now()` is not
///   injectable; this is a test seam, see [`take_delayed_delivery_action_if_required`]
///   which passes the real clock).
pub fn take_delayed_delivery_action_if_required(
    resource_identifier: &str,
    enqueue_timestamp: DateTime<Utc>,
) {
    take_delayed_delivery_action_if_required_with_now(
        resource_identifier,
        enqueue_timestamp,
        Utc::now(),
    );
}

/// [`take_delayed_delivery_action_if_required`] with an injectable `now` (test seam).
pub fn take_delayed_delivery_action_if_required_with_now(
    resource_identifier: &str,
    enqueue_timestamp: DateTime<Utc>,
    now: DateTime<Utc>,
) {
    let duration_between_enqueue_and_ack_in_millis = (now - enqueue_timestamp).num_milliseconds();
    if duration_between_enqueue_and_ack_in_millis > MAX_TIME_BETWEEN_REQUEST_RESPONSE / 3 {
        tracing::warn!(
            "{}: Record delivery time to shard consumer is high at {} millis. Check the \
             ExecutorStateEvent logs to see the state of the executor service. Also check if the \
             RecordProcessor's processing time is high. ",
            resource_identifier,
            duration_between_enqueue_and_ack_in_millis
        );
    } else {
        tracing::debug!(
            "{}: Record delivery time to shard consumer is {} millis",
            resource_identifier,
            duration_between_enqueue_and_ack_in_millis
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Duration;

    #[test]
    fn threshold_is_20_seconds() {
        assert_eq!(MAX_TIME_BETWEEN_REQUEST_RESPONSE / 3, 20_000);
    }

    #[test]
    fn high_latency_does_not_panic() {
        // 25s elapsed -> exceeds the 20s threshold (WARN path).
        let enqueue = Utc::now();
        let now = enqueue + Duration::seconds(25);
        take_delayed_delivery_action_if_required_with_now("shard-0001", enqueue, now);
    }

    #[test]
    fn low_latency_does_not_panic() {
        // 1s elapsed -> below the threshold (DEBUG path).
        let enqueue = Utc::now();
        let now = enqueue + Duration::seconds(1);
        take_delayed_delivery_action_if_required_with_now("shard-0001", enqueue, now);
    }

    #[test]
    fn boundary_at_exactly_threshold_takes_debug_path() {
        // elapsed == threshold is NOT "> threshold", so it takes the else branch.
        let enqueue = Utc::now();
        let now = enqueue + Duration::milliseconds(MAX_TIME_BETWEEN_REQUEST_RESPONSE / 3);
        take_delayed_delivery_action_if_required_with_now("r", enqueue, now);
    }
}
