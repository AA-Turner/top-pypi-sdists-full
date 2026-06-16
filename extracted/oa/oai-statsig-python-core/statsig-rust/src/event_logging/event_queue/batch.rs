use crate::event_logging::statsig_event_internal::StatsigEventInternal;
use crate::log_event_payload::{LogEventPayload, LogEventRequest};
use crate::statsig_metadata::StatsigMetadataWithLogEventExtras;
use serde_json::json;

pub struct EventBatch {
    pub attempts: u8,
    pub events: Vec<StatsigEventInternal>,
    first_event_time_ms: Option<u64>,
}

impl EventBatch {
    pub fn new(events: Vec<StatsigEventInternal>) -> Self {
        let first_event_time_ms = events.first().map(|event| event.time);
        Self {
            events,
            attempts: 0,
            first_event_time_ms,
        }
    }

    pub fn get_max_event_queue_time_ms(&self, now_ms: u64) -> u64 {
        self.first_event_time_ms
            .map(|first_event_time_ms| now_ms.saturating_sub(first_event_time_ms))
            .unwrap_or_default()
    }

    pub fn get_log_event_request(
        &self,
        statsig_metadata: StatsigMetadataWithLogEventExtras,
    ) -> LogEventRequest {
        let payload = LogEventPayload {
            events: json!(self.events),
            statsig_metadata: json!(statsig_metadata),
        };

        LogEventRequest {
            payload,
            event_count: self.events.len() as u64,
            retries: self.attempts as u32,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{event_logging::statsig_event::StatsigEvent, user::StatsigUserLoggable};

    fn make_event(time: u64) -> StatsigEventInternal {
        StatsigEventInternal::new(
            time,
            StatsigUserLoggable::null(),
            StatsigEvent {
                event_name: "test_event".to_string(),
                value: None,
                metadata: None,
                statsig_metadata: None,
            },
            None,
        )
    }

    #[test]
    fn max_event_queue_time_uses_cached_first_event_time() {
        let batch = EventBatch::new(vec![make_event(100), make_event(200)]);

        assert_eq!(batch.get_max_event_queue_time_ms(350), 250);
    }

    #[test]
    fn max_event_queue_time_saturates_at_zero() {
        let batch = EventBatch::new(vec![make_event(200)]);

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }

    #[test]
    fn max_event_queue_time_defaults_for_empty_batch() {
        let batch = EventBatch::new(Vec::new());

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }
}
