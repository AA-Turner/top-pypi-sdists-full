use crate::{ObservabilityClient, OpsStatsEventObserver};
use std::collections::HashMap;
use std::sync::Arc;

// Unit tests inspect the OpsStats queue directly; binding tests verify callbacks.
pub(crate) fn observer() -> Arc<dyn ObservabilityClient> {
    Arc::new(TestObserver)
}

struct TestObserver;

impl ObservabilityClient for TestObserver {
    fn init(&self) {}
    fn increment(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn gauge(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn dist(&self, _: String, _: f64, _: Option<HashMap<String, String>>) {}
    fn error(&self, _: String, _: String) {}
    fn should_enable_high_cardinality_for_this_tag(&self, _: String) -> Option<bool> {
        Some(false)
    }
    fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
        self
    }
}
