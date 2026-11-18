use crate::id_lists_adapter::id_list_load_timing::{Phase, measure, time_list_load};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};
use crate::{ObservabilityClient, OpsStatsEventObserver};
use parking_lot::Mutex;
use std::{collections::HashMap, sync::Arc};

#[derive(Default)]
struct Observer {
    metrics: Mutex<Vec<ObservabilityEvent>>,
    cardinality_checks: Mutex<Vec<String>>,
}

impl ObservabilityClient for Observer {
    fn init(&self) {}
    fn increment(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn gauge(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn error(&self, _: String, _: String) {}
    fn dist(&self, metric_name: String, value: f64, tags: Option<HashMap<String, String>>) {
        self.metrics.lock().push(ObservabilityEvent {
            metric_type: MetricType::Dist,
            metric_name,
            value,
            tags,
        });
    }
    fn should_enable_high_cardinality_for_this_tag(&self, tag: String) -> Option<bool> {
        self.cardinality_checks.lock().push(tag.clone());
        Some(tag == "lcut")
    }
    fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
        self
    }
}

#[tokio::test]
async fn retained_tags_preserve_filter_policy_and_default_metadata() {
    let observer = Observer::default();
    observer
        .handle_event(OpsStatsEvent::Observability(ObservabilityEvent {
            metric_type: MetricType::Dist,
            metric_name: "example".into(),
            value: 1.25,
            tags: Some(HashMap::from([
                ("lcut".into(), "123".into()),
                ("prev_lcut".into(), "122".into()),
                ("outcome".into(), "success".into()),
                ("sdk_type".into(), "incorrect".into()),
                ("sdk_version".into(), "incorrect".into()),
            ])),
        }))
        .await;
    let metrics = observer.metrics.lock();
    assert_eq!(metrics.len(), 1);
    assert_eq!(metrics[0].metric_name, "statsig.sdk.example");
    assert_eq!(metrics[0].value, 1.25);
    let tags = metrics[0].tags.as_ref().unwrap();
    assert_eq!(tags["lcut"], "123");
    assert!(!tags.contains_key("prev_lcut"));
    assert_eq!(tags["outcome"], "success");
    let metadata = crate::statsig_metadata::StatsigMetadata::get_metadata();
    assert_eq!(tags["sdk_type"], metadata.sdk_type);
    assert_eq!(tags["sdk_version"], metadata.sdk_version);
    let mut checked = observer.cardinality_checks.lock().clone();
    checked.sort();
    assert_eq!(checked, ["lcut", "prev_lcut"]);
}

#[tokio::test]
async fn id_list_summary_exports_both_metric_families_with_independent_tags() {
    let ops = OpsStatsForInstance::new();
    let mut events = ops.subscribe_for_test();
    time_list_load(&ops, "members", true, async {
        measure(Phase::HttpBody, || {});
        measure(Phase::ParsePublish, || measure(Phase::Processing, || {}));
        Ok(true)
    })
    .await
    .unwrap();
    let observer = Observer::default();
    observer.handle_event(events.try_recv().unwrap()).await;
    let metrics = observer.metrics.lock();
    assert_eq!(metrics.len(), 5); // three measured phases, other, total
    let metadata = crate::statsig_metadata::StatsigMetadata::get_metadata();
    let mut phases = Vec::new();
    for metric in metrics.iter() {
        assert!(metric.value >= 0.0);
        let tags = metric.tags.as_ref().unwrap();
        assert_eq!(tags["sdk_type"], metadata.sdk_type);
        assert_eq!(tags["sdk_version"], metadata.sdk_version);
        assert_eq!(tags["mode"], "lazy");
        assert_eq!(tags["outcome"], "success");
        assert_eq!(tags["list_name"], "members");
        let phase = tags["phase"].as_str();
        assert_eq!(
            metric.metric_name,
            if phase == "processing" {
                "statsig.sdk.lazy_id_list_load.store_phase_ms"
            } else {
                "statsig.sdk.lazy_id_list_load.list_phase_ms"
            }
        );
        phases.push(phase);
    }
    phases.sort();
    assert_eq!(
        phases,
        ["http_body", "other", "parse_publish", "processing", "total"]
    );
    assert!(observer.cardinality_checks.lock().is_empty());
}
