use crate::anthropic::convert::collect::collector::AnthropicCollector;
use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::stream::AnthropicStreamEvent;
use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult};
use crate::traits::CollectStream;

impl CollectStream for AnthropicResponse {
    type Event = AnthropicStreamEvent;
    type Response = AnthropicResponse;

    fn collect_stream(
        events: impl IntoIterator<Item = AnthropicStreamEvent>,
    ) -> Result<ConversionResult<AnthropicResponse>, ConversionError> {
        let mut collector = AnthropicCollector::new();
        for event in events {
            collector.feed(event)?;
        }
        collector.finalize()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::anthropic::stream::*;
    use crate::anthropic::types::*;

    fn minimal_stream() -> Vec<AnthropicStreamEvent> {
        vec![
            AnthropicStreamEvent::MessageStart {
                message: AnthropicResponse {
                    id: "msg_1".into(),
                    kind: "message".into(),
                    role: AnthropicRole::Assistant,
                    model: "claude".into(),
                    content: vec![],
                    stop_reason: None,
                    stop_sequence: None,
                    usage: AnthropicUsage {
                        input_tokens: 10,
                        output_tokens: 1,
                        ..Default::default()
                    },
                    container: None,
                    service_tier: None,
                },
            },
            AnthropicStreamEvent::MessageDelta {
                delta: AnthropicMessageDelta {
                    stop_reason: Some(AnthropicStopReason::EndTurn),
                    stop_sequence: None,
                },
                usage: Some(AnthropicUsage {
                    input_tokens: 10,
                    output_tokens: 5,
                    ..Default::default()
                }),
            },
            AnthropicStreamEvent::MessageStop,
        ]
    }

    #[test]
    fn delegates_to_collector() {
        let r = AnthropicResponse::collect_stream(minimal_stream()).expect("ok");
        assert_eq!(r.value.id, "msg_1");
        assert_eq!(r.value.stop_reason, Some(AnthropicStopReason::EndTurn));
        assert_eq!(r.value.usage.output_tokens, 5);
        assert!(r.warnings.is_empty());
    }

    #[test]
    fn empty_stream_returns_error() {
        assert!(matches!(
            AnthropicResponse::collect_stream(vec![]),
            Err(ConversionError::InvalidInput(_))
        ));
    }
}
