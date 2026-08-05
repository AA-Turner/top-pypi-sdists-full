use crate::event_logging::statsig_event_internal::StatsigEventInternal;
use crate::log_event_payload::{LogEventPayload, LogEventRequest};
use crate::statsig_metadata::StatsigMetadataWithLogEventExtras;
use serde_json::json;

pub(crate) struct EnqueuedEvent<T> {
    event: T,
    enqueued_at_ms: u64,
}

impl<T> EnqueuedEvent<T> {
    pub(crate) fn new(event: T, enqueued_at_ms: u64) -> Self {
        Self {
            event,
            enqueued_at_ms,
        }
    }

    pub(crate) fn map<U>(self, map_event: impl FnOnce(T) -> U) -> EnqueuedEvent<U> {
        EnqueuedEvent {
            event: map_event(self.event),
            enqueued_at_ms: self.enqueued_at_ms,
        }
    }
}

pub(crate) struct EventBatch {
    attempts: u8,
    events: Vec<EnqueuedEvent<StatsigEventInternal>>,
}

impl EventBatch {
    pub(crate) fn new(events: Vec<EnqueuedEvent<StatsigEventInternal>>) -> Self {
        Self {
            events,
            attempts: 0,
        }
    }

    pub(crate) fn len(&self) -> usize {
        self.events.len()
    }

    pub(crate) fn attempts(&self) -> u8 {
        self.attempts
    }

    pub(crate) fn increment_attempts(&mut self) {
        self.attempts += 1;
    }

    pub(crate) fn iter_events(&self) -> impl Iterator<Item = &StatsigEventInternal> {
        self.events.iter().map(|event| &event.event)
    }

    pub(crate) fn into_events(self) -> impl Iterator<Item = EnqueuedEvent<StatsigEventInternal>> {
        self.events.into_iter()
    }

    pub(crate) fn get_max_event_queue_time_ms(&self, now_ms: u64) -> u64 {
        self.events
            .iter()
            .map(|event| event.enqueued_at_ms)
            .min()
            .map(|enqueued_at_ms| now_ms.saturating_sub(enqueued_at_ms))
            .unwrap_or_default()
    }

    pub(crate) fn get_log_event_request(
        &self,
        statsig_metadata: StatsigMetadataWithLogEventExtras,
    ) -> LogEventRequest {
        let events = self.iter_events().collect::<Vec<_>>();
        let payload = LogEventPayload {
            events: json!(events),
            statsig_metadata: json!(statsig_metadata),
        };

        LogEventRequest {
            payload,
            event_count: self.len() as u64,
            retries: self.attempts as u32,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        event_logging::statsig_event::StatsigEvent, statsig_metadata::StatsigMetadata,
        user::StatsigUserLoggable,
    };

    fn make_event(time: u64, enqueued_at_ms: u64) -> EnqueuedEvent<StatsigEventInternal> {
        EnqueuedEvent::new(
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
            ),
            enqueued_at_ms,
        )
    }

    #[test]
    fn max_event_queue_time_uses_oldest_enqueue_time() {
        let batch = EventBatch::new(vec![make_event(100, 300), make_event(200, 250)]);

        assert_eq!(batch.get_max_event_queue_time_ms(350), 100);
    }

    #[test]
    fn max_event_queue_time_saturates_at_zero() {
        let batch = EventBatch::new(vec![make_event(500, 200)]);

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }

    #[test]
    fn max_event_queue_time_defaults_for_empty_batch() {
        let batch = EventBatch::new(Vec::new());

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }

    #[test]
    fn enqueue_metadata_is_not_serialized() {
        let batch = EventBatch::new(vec![make_event(100, 250)]);
        let request = batch.get_log_event_request(StatsigMetadata::get_with_log_event_extras(
            10,
            500,
            100,
            "test".to_string(),
        ));

        let events = request.payload.events.as_array().unwrap();
        assert_eq!(events.len(), 1);
        assert_eq!(events[0]["time"], 100);
        assert!(events[0].get("enqueued_at_ms").is_none());
        assert!(events[0].get("enqueuedAtMs").is_none());
    }
}
