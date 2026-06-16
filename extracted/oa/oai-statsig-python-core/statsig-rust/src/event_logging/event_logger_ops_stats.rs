use std::collections::HashMap;

use crate::{
    observability::{
        observability_client_adapter::{MetricType, ObservabilityEvent},
        ops_stats::{OpsStatsEvent, OpsStatsForInstance},
        ErrorBoundaryEvent,
    },
    StatsigErr,
};

use super::{event_queue::queue::EventQueue, flush_interval::FlushInterval, flush_type::FlushType};

impl OpsStatsForInstance {
    pub fn log_event_request_failure(&self, event_count: u64, flush_type: FlushType) {
        let error = StatsigErr::LogEventError("Log event failed".to_string());
        self.log_error(ErrorBoundaryEvent {
            exception: error.name().to_string(),
            info: serde_json::to_string(&error).unwrap_or_default(),
            tag: "statsig::log_event_failed".to_string(),
            bypass_dedupe: true,
            dedupe_key: None,
            extra: Some(HashMap::from([
                ("eventCount".to_string(), event_count.to_string()),
                ("flushType".to_string(), flush_type.to_string()),
            ])),
        });
    }

    pub fn log_event_request_batch_stats(
        &self,
        event_count: usize,
        max_event_queue_time_ms: u64,
        flush_type: FlushType,
        tags: Option<HashMap<String, String>>,
    ) {
        let tags = Some(get_event_request_tags(tags, flush_type));

        self.log(OpsStatsEvent::Observability(ObservabilityEvent {
            metric_type: MetricType::Dist,
            metric_name: "log_event_request_event_count".to_string(),
            value: event_count as f64,
            tags: tags.clone(),
        }));

        self.log(OpsStatsEvent::Observability(ObservabilityEvent {
            metric_type: MetricType::Dist,
            metric_name: "log_event_request_max_event_queue_time_ms".to_string(),
            value: max_event_queue_time_ms as f64,
            tags,
        }));
    }

    pub fn log_event_request_success(
        &self,
        event_count: usize,
        flush_type: FlushType,
        tags: Option<HashMap<String, String>>,
    ) {
        self.log(OpsStatsEvent::Observability(ObservabilityEvent {
            metric_type: MetricType::Increment,
            metric_name: "events_successfully_sent_count".to_string(),
            value: event_count as f64,
            tags: Some(get_event_request_tags(tags, flush_type)),
        }))
    }

    pub fn log_event_request_uncompressed_body_size_bytes(
        &self,
        uncompressed_body_size_bytes: usize,
        flush_type: String,
        tags: Option<HashMap<String, String>>,
    ) {
        self.log(OpsStatsEvent::Observability(ObservabilityEvent {
            metric_type: MetricType::Dist,
            metric_name: "log_event_request_uncompressed_body_size_bytes".to_string(),
            value: uncompressed_body_size_bytes as f64,
            tags: Some(get_event_request_tags(tags, flush_type)),
        }))
    }

    pub fn log_batching_dropped_events(
        &self,
        drop_error: StatsigErr,
        count: u64,
        flush_interval: &FlushInterval,
        queue: &EventQueue,
        flush_type: FlushType,
    ) {
        let curr_flush_interval = flush_interval.get_current_flush_interval_ms();
        let batch_size = queue.batch_size;
        let max_pending_batches_count = queue.max_pending_batches;

        self.log_error(ErrorBoundaryEvent {
            tag: "statsig::log_event_dropped_event_count".to_string(),
            exception: drop_error.name().to_string(),
            info: serde_json::to_string(&drop_error).unwrap_or_default(),
            bypass_dedupe: true,
            dedupe_key: None,
            extra: Some(HashMap::from([
                ("eventCount".to_string(), count.to_string()),
                (
                    "loggingInterval".to_string(),
                    curr_flush_interval.to_string(),
                ),
                ("batchSize".to_string(), batch_size.to_string()),
                (
                    "maxPendingBatches".to_string(),
                    max_pending_batches_count.to_string(),
                ),
                ("flushType".to_string(), flush_type.to_string()),
            ])),
        });
    }
}

fn get_event_request_tags(
    tags: Option<HashMap<String, String>>,
    flush_type: impl ToString,
) -> HashMap<String, String> {
    let mut tags = tags.unwrap_or_default();
    tags.insert("flush_type".to_string(), flush_type.to_string());
    tags
}
