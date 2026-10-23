use std::sync::Arc;

use tokio::sync::broadcast::{Receiver, error::TryRecvError};

use crate::networking::NetworkClient;
use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};

use super::*;

fn observed_hydrator() -> (RemoteConfigValueHydrator, Receiver<OpsStatsEvent>) {
    let ops_stats = Arc::new(OpsStatsForInstance::new());
    let events = ops_stats.subscribe_for_test();
    let hydrator = RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(NetworkClient::new("telemetry-context-test", None, None)),
        ops_stats,
    );
    (hydrator, events)
}

fn collect_metrics(events: &mut Receiver<OpsStatsEvent>) -> Vec<ObservabilityEvent> {
    let mut metrics = Vec::new();
    loop {
        match events.try_recv() {
            Ok(OpsStatsEvent::Observability(event)) => metrics.push(event),
            Ok(_) => panic!("unexpected non-metric hydration event"),
            Err(TryRecvError::Empty) => return metrics,
            Err(error) => panic!("hydration metric subscription failed: {error}"),
        }
    }
}

fn tags(trigger: &str, response_type: &str, extra: &[(&str, &str)]) -> HashMap<String, String> {
    let mut tags = HashMap::from([
        ("config_sync_trigger".into(), trigger.into()),
        ("config_payload_type".into(), response_type.into()),
    ]);
    tags.extend(
        extra
            .iter()
            .map(|(key, value)| (key.to_string(), value.to_string())),
    );
    tags
}

fn metric<'a>(metrics: &'a [ObservabilityEvent], name: &str) -> &'a ObservabilityEvent {
    let matching = metrics
        .iter()
        .filter(|event| event.metric_name == name)
        .collect::<Vec<_>>();
    assert_eq!(matching.len(), 1, "expected exactly one {name} event");
    matching[0]
}

#[test]
fn success_session_metrics_keep_the_same_explicit_or_unknown_context() {
    for (trigger, is_delta, expected_trigger, expected_response_type) in [
        (None, None, "unknown", "unknown"),
        (
            Some(SpecsSyncTrigger::Initial),
            Some(false),
            "http_adapter_start",
            "full_snapshot",
        ),
        (
            Some(SpecsSyncTrigger::Background),
            Some(true),
            "background_sync",
            "delta_update",
        ),
        (
            Some(SpecsSyncTrigger::Manual),
            Some(false),
            "explicit_fetch",
            "full_snapshot",
        ),
    ] {
        let (hydrator, mut events) = observed_hydrator();
        {
            let mut result = HydrationResult::new_with_trigger(&hydrator, trigger);
            if let Some(is_delta) = is_delta {
                result.set_response_type(is_delta);
            }
            result.mark_remote_metadata();
            result.finish(Ok(()));
            result.log_hydration_outcome(
                Instant::now() - Duration::from_millis(7),
                HydrationOutcome::Success,
            );
            result.log_hydration_success(2, 1234);
        }

        let metrics = collect_metrics(&mut events);
        assert_eq!(metrics.len(), 4);
        let result = metric(&metrics, HYDRATION_RESULT_METRIC);
        assert!(matches!(result.metric_type, MetricType::Increment));
        assert_eq!(result.value, 1.0);
        assert_eq!(
            result.tags.as_ref().unwrap(),
            &tags(
                expected_trigger,
                expected_response_type,
                &[("outcome", "success"), ("failure_reason", "none")],
            )
        );

        let expected_outcome_tags = tags(
            expected_trigger,
            expected_response_type,
            &[("outcome", "success")],
        );
        let count = metric(&metrics, HYDRATION_COUNT_METRIC);
        assert!(matches!(count.metric_type, MetricType::Increment));
        assert_eq!(count.value, 1.0);
        assert_eq!(count.tags.as_ref().unwrap(), &expected_outcome_tags);

        let latency = metric(&metrics, HYDRATION_LATENCY_METRIC);
        assert!(matches!(latency.metric_type, MetricType::Dist));
        assert!(latency.value >= 7.0);
        assert_eq!(latency.tags.as_ref().unwrap(), &expected_outcome_tags);

        let bytes = metric(&metrics, HYDRATION_BYTES_METRIC);
        assert!(matches!(bytes.metric_type, MetricType::Dist));
        assert_eq!(bytes.value, 1234.0);
        assert_eq!(
            bytes.tags.as_ref().unwrap(),
            &tags(expected_trigger, expected_response_type, &[])
        );
    }
}

#[test]
fn failed_delta_retains_context_and_repeated_finish_does_not_duplicate_the_result() {
    let (hydrator, mut events) = observed_hydrator();
    let error = hydration_error(HydrationFailureReason::ChecksumMismatch, "test mismatch");
    {
        let mut result =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Background));
        result.set_response_type(true);
        result.mark_remote_metadata();
        result.finish(Err(&error));
        result.finish(Err(&error));
        result.log_hydration_outcome(
            Instant::now() - Duration::from_millis(7),
            HydrationOutcome::Failure,
        );
    }

    let metrics = collect_metrics(&mut events);
    assert_eq!(metrics.len(), 3);
    assert_eq!(
        metric(&metrics, HYDRATION_RESULT_METRIC)
            .tags
            .as_ref()
            .unwrap(),
        &tags(
            "background_sync",
            "delta_update",
            &[
                ("outcome", "failure"),
                ("failure_reason", "checksum_mismatch")
            ],
        )
    );
    for name in [HYDRATION_COUNT_METRIC, HYDRATION_LATENCY_METRIC] {
        assert_eq!(
            metric(&metrics, name).tags.as_ref().unwrap(),
            &tags("background_sync", "delta_update", &[("outcome", "failure")])
        );
    }
}

#[test]
fn cancellation_retains_the_known_context_and_emits_only_one_result() {
    let (hydrator, mut events) = observed_hydrator();
    {
        let mut result =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Manual));
        result.set_response_type(false);
        result.mark_remote_metadata();
    }

    let metrics = collect_metrics(&mut events);
    assert_eq!(metrics.len(), 1);
    assert_eq!(
        metric(&metrics, HYDRATION_RESULT_METRIC)
            .tags
            .as_ref()
            .unwrap(),
        &tags(
            "explicit_fetch",
            "full_snapshot",
            &[("outcome", "aborted"), ("failure_reason", "cancelled")],
        )
    );
}

#[test]
fn unclassified_failure_preserves_unknown_response_type() {
    let (hydrator, mut events) = observed_hydrator();
    let error = StatsigErr::SerializationError("body read failed".into());
    {
        let mut result =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Initial));
        result.mark_remote_metadata();
        result.record_download_error(&error);
        result.finish(Err(&error));
    }

    let metrics = collect_metrics(&mut events);
    assert_eq!(metrics.len(), 1);
    assert_eq!(
        metric(&metrics, HYDRATION_RESULT_METRIC)
            .tags
            .as_ref()
            .unwrap(),
        &tags(
            "http_adapter_start",
            "unknown",
            &[
                ("outcome", "failure"),
                ("failure_reason", "body_read_failed")
            ],
        )
    );
}

#[test]
fn no_remote_metadata_does_not_create_a_result_for_success_failure_or_cancellation() {
    let (hydrator, mut events) = observed_hydrator();
    let error = hydration_error(HydrationFailureReason::InvalidMetadata, "test metadata");
    for completion in [Some(Ok(())), Some(Err(&error)), None] {
        let mut result =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Background));
        result.set_response_type(false);
        if let Some(completion) = completion {
            result.finish(completion);
        }
    }
    assert!(collect_metrics(&mut events).is_empty());
}

#[test]
fn interleaved_sessions_do_not_share_response_context() {
    let (hydrator, mut events) = observed_hydrator();
    {
        let mut initial =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Initial));
        initial.set_response_type(false);
        initial.mark_remote_metadata();
        let mut background =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Background));
        background.set_response_type(true);
        background.mark_remote_metadata();
        background.finish(Ok(()));
        initial.finish(Ok(()));
    }

    let metrics = collect_metrics(&mut events);
    assert_eq!(metrics.len(), 2);
    let metrics = metrics
        .iter()
        .filter(|event| event.metric_name == HYDRATION_RESULT_METRIC)
        .collect::<Vec<_>>();
    for (event, trigger, response_type) in [
        (&metrics[0], "background_sync", "delta_update"),
        (&metrics[1], "http_adapter_start", "full_snapshot"),
    ] {
        assert_eq!(event.metric_name, HYDRATION_RESULT_METRIC);
        assert_eq!(
            event.tags.as_ref().unwrap(),
            &tags(
                trigger,
                response_type,
                &[("outcome", "success"), ("failure_reason", "none")],
            )
        );
    }
}

#[test]
fn phase_metrics_do_not_gain_session_cohort_tags() {
    let (hydrator, mut events) = observed_hydrator();
    {
        let mut result =
            HydrationResult::new_with_trigger(&hydrator, Some(SpecsSyncTrigger::Background));
        result.set_response_type(true);
        result.mark_remote_metadata();
        hydrator.log_phase_latency(Duration::from_millis(7), HydrationPhase::Verify);
        result.finish(Ok(()));
    }

    let metrics = collect_metrics(&mut events);
    assert_eq!(metrics.len(), 2);
    let phase = metric(&metrics, "remote_config_hydration.phase_latency");
    assert!(matches!(phase.metric_type, MetricType::Dist));
    assert_eq!(phase.value, 7.0);
    assert_eq!(
        phase.tags.as_ref().unwrap(),
        &HashMap::from([("phase".into(), "verify".into())])
    );
}
