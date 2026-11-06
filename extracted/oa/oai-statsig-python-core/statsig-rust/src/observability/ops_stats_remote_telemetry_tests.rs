use super::*;
use crate::StatsigOptions;
use crate::sdk_diagnostics::marker::ActionType;

#[test]
fn diagnostics_are_dropped_before_queueing_but_local_metrics_and_errors_remain() {
    let registry = OpsStats::new();
    let suppressed_options = StatsigOptions {
        disable_remote_telemetry: Some(true),
        ..StatsigOptions::default()
    };
    let legacy_options = StatsigOptions {
        disable_remote_telemetry: Some(false),
        ..StatsigOptions::default()
    };
    let suppressed = registry.get_for_instance_with_options("shared-id", Some(&suppressed_options));
    let legacy = registry.get_for_instance_with_options("shared-id", Some(&legacy_options));
    assert!(Arc::ptr_eq(
        &registry.get_for_instance("shared-id"),
        &legacy
    ));
    let mut suppressed_events = suppressed.subscribe_for_test();
    let mut legacy_events = legacy.subscribe_for_test();

    suppressed.add_marker(Marker::new(KeyType::Overall, ActionType::Start, None), None);
    suppressed.set_diagnostics_context(ContextType::ConfigSync);
    suppressed.enqueue_diagnostics_event(Some(KeyType::DownloadConfigSpecs), None);
    suppressed.log(OpsStatsEvent::Diagnostics(DiagnosticsEvent {
        marker: None,
        context: Some(ContextType::Initialize),
        key: None,
        should_enqueue: true,
    }));
    assert!(matches!(
        suppressed_events.try_recv(),
        Err(broadcast::error::TryRecvError::Empty)
    ));
    suppressed.log_error(ErrorBoundaryEvent {
        tag: "test".into(),
        info: "local error".into(),
        exception: "TestError".into(),
        dedupe_key: None,
        bypass_dedupe: false,
        extra: None,
    });
    assert!(matches!(
        suppressed_events.try_recv(),
        Ok(OpsStatsEvent::SDKError(_))
    ));
    assert!(matches!(
        legacy_events.try_recv(),
        Err(broadcast::error::TryRecvError::Empty)
    ));
    suppressed.log(ObservabilityEvent::new_event(
        MetricType::Increment,
        "test_metric".into(),
        1.0,
        None,
    ));
    assert!(matches!(
        suppressed_events.try_recv(),
        Ok(OpsStatsEvent::Observability(_))
    ));
    legacy.add_marker(Marker::new(KeyType::Overall, ActionType::Start, None), None);
    assert!(matches!(
        legacy_events.try_recv(),
        Ok(OpsStatsEvent::Diagnostics(_))
    ));
}

#[test]
fn option_builder_preserves_explicit_false_and_unset() {
    for value in [None, Some(false), Some(true)] {
        let options = StatsigOptions::builder()
            .disable_remote_telemetry(value)
            .build();
        assert_eq!(options.disable_remote_telemetry, value);
        let json = serde_json::to_value(&options).unwrap();
        assert_eq!(
            json.get("disable_remote_telemetry")
                .and_then(serde_json::Value::as_bool),
            value
        );
    }
}
