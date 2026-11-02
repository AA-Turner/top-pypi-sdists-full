use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult, ConversionWarning, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;

/// Stateful collector that accumulates Open Responses stream events
/// into a single [`OpenResponsesResponse`].
///
/// Feed events one at a time via [`ResponseCollector::feed`], then call
/// [`ResponseCollector::finalize`] to obtain the response.
///
/// Implements [`DynResponseCollector`](crate::collect::DynResponseCollector)
/// via the blanket impl, so it can be used type-erased at the Python boundary.
pub struct OpenResponsesCollector {
    fallback: Option<OpenResponsesResponse>,
    terminal: Option<OpenResponsesResponse>,
    saw_any_event: bool,
    saw_multiple_terminals: bool,
    warnings: Vec<ConversionWarning>,
    finalized: bool,
}

impl Default for OpenResponsesCollector {
    fn default() -> Self {
        Self::new()
    }
}

impl OpenResponsesCollector {
    pub fn new() -> Self {
        Self {
            fallback: None,
            terminal: None,
            saw_any_event: false,
            saw_multiple_terminals: false,
            warnings: Vec::new(),
            finalized: false,
        }
    }
}

impl ResponseCollector for OpenResponsesCollector {
    type Event = OpenResponsesStreamEvent;
    type Response = OpenResponsesResponse;

    fn feed(&mut self, event: OpenResponsesStreamEvent) -> Result<(), ConversionError> {
        if self.finalized {
            return Err(ConversionError::InvalidInput(
                "cannot feed events after finalize".into(),
            ));
        }
        self.saw_any_event = true;
        match event {
            OpenResponsesStreamEvent::ResponseCreated { response, .. }
            | OpenResponsesStreamEvent::ResponseQueued { response, .. }
            | OpenResponsesStreamEvent::ResponseInProgress { response, .. } => {
                self.fallback = Some(response);
            }
            OpenResponsesStreamEvent::ResponseCompleted { response, .. }
            | OpenResponsesStreamEvent::ResponseIncomplete { response, .. }
            | OpenResponsesStreamEvent::ResponseFailed { response, .. } => {
                if self.terminal.is_some() {
                    self.saw_multiple_terminals = true;
                }
                self.terminal = Some(response);
            }
            OpenResponsesStreamEvent::Unknown => {
                self.warnings.push(ConversionWarning {
                    field: "type".into(),
                    action: WarningAction::Dropped,
                    message: "unknown Open Responses stream event dropped".into(),
                });
            }
            _ => {}
        }
        Ok(())
    }

    fn finalize(&mut self) -> Result<ConversionResult<OpenResponsesResponse>, ConversionError> {
        if self.finalized {
            return Err(ConversionError::InvalidInput(
                "collector has already been finalized".into(),
            ));
        }
        self.finalized = true;

        if !self.saw_any_event {
            return Err(ConversionError::InvalidInput(
                "cannot collect stream: no events received".into(),
            ));
        }

        if let Some(response) = self.terminal.take() {
            let mut result =
                ConversionResult::with_warnings(response, std::mem::take(&mut self.warnings));
            if self.saw_multiple_terminals {
                result.warn(
                    "response",
                    WarningAction::Changed,
                    "multiple terminal events in stream; used the last one",
                );
            }
            Ok(result)
        } else {
            let response = match self.fallback.take() {
                Some(mut response) => {
                    response.status = ResponseStatus::Incomplete;
                    if response.incomplete_details.is_none() {
                        response.incomplete_details = Some(IncompleteDetails {
                            reason: "stream_ended_without_terminal_event".into(),
                        });
                    }
                    response
                }
                None => {
                    return Err(ConversionError::InvalidInput(
                        "cannot collect stream: no response header or terminal event found".into(),
                    ));
                }
            };

            let mut result =
                ConversionResult::with_warnings(response, std::mem::take(&mut self.warnings));
            result.warn(
                "response",
                WarningAction::Changed,
                "stream ended without a terminal event (response.completed / response.incomplete / response.failed); \
                 response was reconstructed from the last header event and marked incomplete",
            );
            Ok(result)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

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
    fn collector_double_finalize_returns_error() {
        let mut collector = OpenResponsesCollector::new();
        collector
            .feed(OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: 0,
                response: make_response(ResponseStatus::Completed),
            })
            .unwrap();

        assert!(collector.finalize().is_ok());
        let err = collector.finalize().unwrap_err();
        assert!(matches!(err, ConversionError::InvalidInput(_)));
        assert!(err.to_string().contains("already been finalized"));
    }

    #[test]
    fn collector_feed_after_finalize_returns_error() {
        let mut collector = OpenResponsesCollector::new();
        collector
            .feed(OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: 0,
                response: make_response(ResponseStatus::Completed),
            })
            .unwrap();

        collector.finalize().unwrap();
        let err = collector
            .feed(OpenResponsesStreamEvent::Keepalive { sequence_number: 1 })
            .unwrap_err();
        assert!(err.to_string().contains("after finalize"));
    }

    #[test]
    fn collector_no_events_returns_error() {
        let mut collector = OpenResponsesCollector::new();
        assert!(matches!(
            collector.finalize(),
            Err(ConversionError::InvalidInput(_))
        ));
    }

    #[test]
    fn collector_unknown_event_warns_and_continues() {
        let mut collector = OpenResponsesCollector::new();
        collector.feed(OpenResponsesStreamEvent::Unknown).unwrap();
        collector
            .feed(OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: 1,
                response: make_response(ResponseStatus::Completed),
            })
            .unwrap();

        let result = collector.finalize().expect("finalize");
        assert_eq!(result.warnings.len(), 1);
        assert_eq!(result.warnings[0].field, "type");
        assert_eq!(result.warnings[0].action, WarningAction::Dropped);
        assert_eq!(
            result.warnings[0].message,
            "unknown Open Responses stream event dropped"
        );
    }

    #[test]
    fn collector_fallback_uses_latest_header() {
        let mut collector = OpenResponsesCollector::new();
        collector
            .feed(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: OpenResponsesResponse {
                    service_tier: Some(ServiceTier::Auto),
                    ..make_response(ResponseStatus::InProgress)
                },
            })
            .unwrap();
        collector
            .feed(OpenResponsesStreamEvent::ResponseInProgress {
                sequence_number: 1,
                response: OpenResponsesResponse {
                    service_tier: Some(ServiceTier::Default),
                    ..make_response(ResponseStatus::InProgress)
                },
            })
            .unwrap();

        let result = collector.finalize().expect("finalize");
        assert_eq!(result.value.service_tier, Some(ServiceTier::Default));
    }
}
