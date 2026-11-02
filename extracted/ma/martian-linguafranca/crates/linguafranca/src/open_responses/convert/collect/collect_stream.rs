use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult};
use crate::open_responses::convert::collect::collector::OpenResponsesCollector;
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::traits::CollectStream;

impl CollectStream for OpenResponsesResponse {
    type Event = OpenResponsesStreamEvent;
    type Response = OpenResponsesResponse;

    fn collect_stream(
        events: impl IntoIterator<Item = OpenResponsesStreamEvent>,
    ) -> Result<ConversionResult<OpenResponsesResponse>, ConversionError> {
        let mut collector = OpenResponsesCollector::new();
        for event in events {
            collector.feed(event)?;
        }
        collector.finalize()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::open_responses::types::*;

    fn make_response(status: ResponseStatus) -> OpenResponsesResponse {
        OpenResponsesResponse {
            id: "resp_1".into(),
            object: "response".into(),
            created_at: 100,
            status,
            model: "gpt-5".into(),
            output: vec![],
            ..Default::default()
        }
    }

    #[test]
    fn collect_no_events_returns_error() {
        let result = OpenResponsesResponse::collect_stream(vec![]);
        assert!(matches!(result, Err(ConversionError::InvalidInput(_))));
    }

    #[test]
    fn collect_only_keepalives_returns_error() {
        let events = vec![
            OpenResponsesStreamEvent::Keepalive { sequence_number: 0 },
            OpenResponsesStreamEvent::Keepalive { sequence_number: 1 },
        ];
        assert!(OpenResponsesResponse::collect_stream(events).is_err());
    }

    #[test]
    fn collect_multiple_terminals_uses_last_and_warns() {
        let events = vec![
            OpenResponsesStreamEvent::ResponseIncomplete {
                sequence_number: 0,
                response: make_response(ResponseStatus::Incomplete),
            },
            OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: 1,
                response: make_response(ResponseStatus::Completed),
            },
        ];

        let result = OpenResponsesResponse::collect_stream(events).expect("ok");
        assert_eq!(result.value.status, ResponseStatus::Completed);
        assert_eq!(result.warnings.len(), 1);
        assert!(
            result.warnings[0]
                .message
                .contains("multiple terminal events")
        );
    }

    #[test]
    fn collect_fallback_preserves_existing_incomplete_details() {
        let events = vec![OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: 0,
            response: OpenResponsesResponse {
                incomplete_details: Some(IncompleteDetails {
                    reason: "custom_reason".into(),
                }),
                ..make_response(ResponseStatus::InProgress)
            },
        }];

        let result = OpenResponsesResponse::collect_stream(events).expect("ok");
        assert_eq!(result.value.status, ResponseStatus::Incomplete);
        assert_eq!(
            result.value.incomplete_details.as_ref().unwrap().reason,
            "custom_reason"
        );
    }

    #[test]
    fn collect_fallback_uses_latest_header_event() {
        let events = vec![
            OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: OpenResponsesResponse {
                    service_tier: Some(ServiceTier::Auto),
                    ..make_response(ResponseStatus::InProgress)
                },
            },
            OpenResponsesStreamEvent::ResponseInProgress {
                sequence_number: 1,
                response: OpenResponsesResponse {
                    service_tier: Some(ServiceTier::Default),
                    ..make_response(ResponseStatus::InProgress)
                },
            },
        ];

        let result = OpenResponsesResponse::collect_stream(events).expect("ok");
        assert_eq!(result.value.service_tier, Some(ServiceTier::Default));
    }
}
