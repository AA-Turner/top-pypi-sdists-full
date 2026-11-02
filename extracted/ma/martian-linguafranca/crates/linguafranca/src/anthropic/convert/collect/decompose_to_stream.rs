use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::stream::*;
use crate::anthropic::types::*;
use crate::error::{ConversionError, ConversionResult};
use crate::traits::DecomposeToStream;

impl DecomposeToStream for AnthropicResponse {
    type Event = AnthropicStreamEvent;

    fn decompose_to_stream(
        self,
    ) -> Result<ConversionResult<Vec<AnthropicStreamEvent>>, ConversionError> {
        let mut events = Vec::new();

        // MessageStart — response with empty content, no stop reason, seed usage.
        let start_usage = AnthropicUsage {
            output_tokens: self.usage.output_tokens.min(1),
            ..self.usage.clone()
        };
        events.push(AnthropicStreamEvent::MessageStart {
            message: AnthropicResponse {
                content: vec![],
                stop_reason: None,
                stop_sequence: None,
                usage: start_usage,
                ..self.clone()
            },
        });

        // Content blocks.
        for (i, block) in self.content.iter().enumerate() {
            let index = i as u64;

            events.push(AnthropicStreamEvent::ContentBlockStart {
                index,
                content_block: empty_content_block(block),
            });

            emit_content_block_deltas(&mut events, index, block);

            events.push(AnthropicStreamEvent::ContentBlockStop { index });
        }

        // MessageDelta with final usage and stop reason.
        events.push(AnthropicStreamEvent::MessageDelta {
            delta: AnthropicMessageDelta {
                stop_reason: self.stop_reason,
                stop_sequence: self.stop_sequence,
            },
            usage: Some(self.usage),
        });

        // MessageStop.
        events.push(AnthropicStreamEvent::MessageStop);

        Ok(ConversionResult::new(events))
    }
}

/// Creates the "start" version of a content block with text/input/thinking cleared.
///
/// Block types that arrive fully formed (`RedactedThinking`, `WebSearchToolResult`,
/// `ToolSearchToolResult`, `Other`) are cloned as-is.
fn empty_content_block(block: &AnthropicOutputContentBlock) -> AnthropicOutputContentBlock {
    match block {
        AnthropicOutputContentBlock::Known(known) => {
            AnthropicOutputContentBlock::Known(match known {
                AnthropicKnownOutputContentBlock::Text { citations, .. } => {
                    AnthropicKnownOutputContentBlock::Text {
                        text: String::new(),
                        citations: citations.clone(),
                    }
                }
                AnthropicKnownOutputContentBlock::ToolUse { id, name, .. } => {
                    AnthropicKnownOutputContentBlock::ToolUse {
                        id: id.clone(),
                        name: name.clone(),
                        input: serde_json::json!({}),
                    }
                }
                AnthropicKnownOutputContentBlock::Thinking { .. } => {
                    AnthropicKnownOutputContentBlock::Thinking {
                        thinking: String::new(),
                        signature: String::new(),
                    }
                }
                AnthropicKnownOutputContentBlock::ServerToolUse {
                    id, name, caller, ..
                } => AnthropicKnownOutputContentBlock::ServerToolUse {
                    id: id.clone(),
                    name: name.clone(),
                    input: serde_json::json!({}),
                    caller: caller.clone(),
                },
                // These block types arrive fully formed — preserve as-is.
                AnthropicKnownOutputContentBlock::RedactedThinking { .. }
                | AnthropicKnownOutputContentBlock::WebSearchToolResult { .. }
                | AnthropicKnownOutputContentBlock::ToolSearchToolResult { .. } => known.clone(),
            })
        }
        AnthropicOutputContentBlock::Other(value) => {
            AnthropicOutputContentBlock::Other(value.clone())
        }
    }
}

/// Emit delta events for a content block's payload.
///
/// Blocks that arrive fully formed (`RedactedThinking`, `WebSearchToolResult`,
/// `ToolSearchToolResult`, `Other`) produce no deltas.
fn emit_content_block_deltas(
    events: &mut Vec<AnthropicStreamEvent>,
    index: u64,
    block: &AnthropicOutputContentBlock,
) {
    let known = match block {
        AnthropicOutputContentBlock::Known(k) => k,
        AnthropicOutputContentBlock::Other(_) => return,
    };

    match known {
        AnthropicKnownOutputContentBlock::Text { text, .. } => {
            if !text.is_empty() {
                events.push(AnthropicStreamEvent::ContentBlockDelta {
                    index,
                    delta: AnthropicStreamDelta::TextDelta { text: text.clone() },
                });
            }
        }
        AnthropicKnownOutputContentBlock::ToolUse { input, .. } => {
            let json = serde_json::to_string(input).unwrap_or_default();
            if json != "{}" && !json.is_empty() {
                events.push(AnthropicStreamEvent::ContentBlockDelta {
                    index,
                    delta: AnthropicStreamDelta::InputJsonDelta { partial_json: json },
                });
            }
        }
        AnthropicKnownOutputContentBlock::Thinking {
            thinking,
            signature,
        } => {
            if !thinking.is_empty() {
                events.push(AnthropicStreamEvent::ContentBlockDelta {
                    index,
                    delta: AnthropicStreamDelta::ThinkingDelta {
                        thinking: thinking.clone(),
                    },
                });
            }
            if !signature.is_empty() {
                events.push(AnthropicStreamEvent::ContentBlockDelta {
                    index,
                    delta: AnthropicStreamDelta::SignatureDelta {
                        signature: signature.clone(),
                    },
                });
            }
        }
        AnthropicKnownOutputContentBlock::ServerToolUse { input, .. } => {
            let json = serde_json::to_string(input).unwrap_or_default();
            if json != "{}" && !json.is_empty() {
                events.push(AnthropicStreamEvent::ContentBlockDelta {
                    index,
                    delta: AnthropicStreamDelta::InputJsonDelta { partial_json: json },
                });
            }
        }
        // Fully-formed block types — no deltas.
        AnthropicKnownOutputContentBlock::RedactedThinking { .. }
        | AnthropicKnownOutputContentBlock::WebSearchToolResult { .. }
        | AnthropicKnownOutputContentBlock::ToolSearchToolResult { .. } => {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::traits::CollectStream;

    fn make_response(
        content: Vec<AnthropicOutputContentBlock>,
        stop_reason: Option<AnthropicStopReason>,
    ) -> AnthropicResponse {
        AnthropicResponse {
            id: "msg_01".into(),
            kind: "message".into(),
            role: AnthropicRole::Assistant,
            model: "claude-sonnet-4-20250514".into(),
            content,
            stop_reason,
            stop_sequence: None,
            usage: AnthropicUsage {
                input_tokens: 10,
                output_tokens: 20,
                ..Default::default()
            },
            container: None,
            service_tier: None,
        }
    }

    fn block(b: AnthropicKnownOutputContentBlock) -> AnthropicOutputContentBlock {
        AnthropicOutputContentBlock::Known(b)
    }

    fn text(s: &str) -> AnthropicOutputContentBlock {
        block(AnthropicKnownOutputContentBlock::Text {
            text: s.into(),
            citations: vec![],
        })
    }

    fn tool_use(id: &str, name: &str, input: serde_json::Value) -> AnthropicOutputContentBlock {
        block(AnthropicKnownOutputContentBlock::ToolUse {
            id: id.into(),
            name: name.into(),
            input,
        })
    }

    fn decompose(response: AnthropicResponse) -> Vec<AnthropicStreamEvent> {
        response.decompose_to_stream().expect("decompose").value
    }

    fn event_types(events: &[AnthropicStreamEvent]) -> Vec<String> {
        serde_json::to_value(events)
            .unwrap()
            .as_array()
            .unwrap()
            .iter()
            .map(|e| e["type"].as_str().unwrap().to_string())
            .collect()
    }

    fn has_delta(events: &[AnthropicStreamEvent]) -> bool {
        events
            .iter()
            .any(|e| matches!(e, AnthropicStreamEvent::ContentBlockDelta { .. }))
    }

    // ── Envelope structure ──

    #[test]
    fn message_start_has_empty_content_and_no_stop_reason() {
        let events = decompose(make_response(
            vec![text("hi")],
            Some(AnthropicStopReason::EndTurn),
        ));
        match &events[0] {
            AnthropicStreamEvent::MessageStart { message } => {
                assert!(message.content.is_empty());
                assert!(message.stop_reason.is_none());
            }
            other => panic!("expected MessageStart, got {other:?}"),
        }
    }

    #[test]
    fn message_start_has_seed_usage_and_delta_has_final() {
        let events = decompose(make_response(vec![], Some(AnthropicStopReason::EndTurn)));
        match &events[0] {
            AnthropicStreamEvent::MessageStart { message } => {
                assert_eq!(message.usage.output_tokens, 1);
                assert_eq!(message.usage.input_tokens, 10);
            }
            other => panic!("expected MessageStart, got {other:?}"),
        }
        match &events[1] {
            AnthropicStreamEvent::MessageDelta { usage, .. } => {
                assert_eq!(usage.as_ref().unwrap().output_tokens, 20);
            }
            other => panic!("expected MessageDelta, got {other:?}"),
        }
    }

    #[test]
    fn empty_content_produces_envelope_only() {
        let events = decompose(make_response(vec![], Some(AnthropicStopReason::EndTurn)));
        assert_eq!(
            event_types(&events),
            ["message_start", "message_delta", "message_stop"]
        );
    }

    #[test]
    fn multi_block_indexes_are_sequential() {
        let events = decompose(make_response(
            vec![
                block(AnthropicKnownOutputContentBlock::Thinking {
                    thinking: "h".into(),
                    signature: "s".into(),
                }),
                text("a"),
                tool_use("t", "f", serde_json::json!({"x": 1})),
            ],
            Some(AnthropicStopReason::ToolUse),
        ));
        let indexes: Vec<u64> = events
            .iter()
            .filter_map(|e| match e {
                AnthropicStreamEvent::ContentBlockStart { index, .. } => Some(*index),
                _ => None,
            })
            .collect();
        assert_eq!(indexes, [0, 1, 2]);
    }

    // ── Block-specific event sequences ──

    #[test]
    fn text_block_emits_text_delta() {
        let events = decompose(make_response(
            vec![text("Hello!")],
            Some(AnthropicStopReason::EndTurn),
        ));
        assert_eq!(
            event_types(&events),
            [
                "message_start",
                "content_block_start",
                "content_block_delta",
                "content_block_stop",
                "message_delta",
                "message_stop",
            ]
        );
        assert!(matches!(&events[2],
            AnthropicStreamEvent::ContentBlockDelta { delta: AnthropicStreamDelta::TextDelta { text }, .. } if text == "Hello!"
        ));
    }

    #[test]
    fn tool_use_block_emits_input_json_delta() {
        let events = decompose(make_response(
            vec![tool_use("t", "fn", serde_json::json!({"a": 1}))],
            Some(AnthropicStopReason::ToolUse),
        ));
        match &events[2] {
            AnthropicStreamEvent::ContentBlockDelta {
                delta: AnthropicStreamDelta::InputJsonDelta { partial_json },
                ..
            } => {
                assert_eq!(
                    serde_json::from_str::<serde_json::Value>(partial_json).unwrap(),
                    serde_json::json!({"a": 1})
                );
            }
            other => panic!("expected InputJsonDelta, got {other:?}"),
        }
    }

    #[test]
    fn thinking_block_emits_thinking_and_signature_deltas() {
        let events = decompose(make_response(
            vec![block(AnthropicKnownOutputContentBlock::Thinking {
                thinking: "hmm".into(),
                signature: "sig".into(),
            })],
            Some(AnthropicStopReason::EndTurn),
        ));
        assert_eq!(events.len(), 7); // start, block_start, thinking, signature, block_stop, delta, stop
        assert!(matches!(&events[2],
            AnthropicStreamEvent::ContentBlockDelta { delta: AnthropicStreamDelta::ThinkingDelta { thinking }, .. } if thinking == "hmm"
        ));
        assert!(matches!(&events[3],
            AnthropicStreamEvent::ContentBlockDelta { delta: AnthropicStreamDelta::SignatureDelta { signature }, .. } if signature == "sig"
        ));
    }

    #[test]
    fn redacted_thinking_emits_no_deltas_and_preserves_data() {
        let events = decompose(make_response(
            vec![block(AnthropicKnownOutputContentBlock::RedactedThinking {
                data: "opaque".into(),
            })],
            Some(AnthropicStopReason::EndTurn),
        ));
        assert_eq!(
            event_types(&events),
            [
                "message_start",
                "content_block_start",
                "content_block_stop",
                "message_delta",
                "message_stop",
            ]
        );
        match &events[1] {
            AnthropicStreamEvent::ContentBlockStart {
                content_block:
                    AnthropicOutputContentBlock::Known(
                        AnthropicKnownOutputContentBlock::RedactedThinking { data },
                    ),
                ..
            } => assert_eq!(data, "opaque"),
            other => panic!("expected RedactedThinking start, got {other:?}"),
        }
    }

    // ── Empty payloads skip deltas ──

    #[test]
    fn empty_text_skips_delta() {
        assert!(!has_delta(&decompose(make_response(
            vec![text("")],
            Some(AnthropicStopReason::EndTurn)
        ))));
    }

    #[test]
    fn empty_tool_input_skips_delta() {
        assert!(!has_delta(&decompose(make_response(
            vec![tool_use("t", "f", serde_json::json!({}))],
            Some(AnthropicStopReason::ToolUse),
        ))));
    }

    // ── Round-trips: decompose → collect recovers original ──

    fn assert_round_trip(response: AnthropicResponse) {
        let events = response
            .clone()
            .decompose_to_stream()
            .expect("decompose")
            .value;
        let collected = AnthropicResponse::collect_stream(events).expect("collect");
        assert_eq!(collected.value, response);
        assert!(collected.warnings.is_empty());
    }

    #[test]
    fn round_trip_mixed_content() {
        assert_round_trip(make_response(
            vec![
                block(AnthropicKnownOutputContentBlock::Thinking {
                    thinking: "think".into(),
                    signature: "sig".into(),
                }),
                text("answer"),
                tool_use("t1", "get_weather", serde_json::json!({"city": "Paris"})),
            ],
            Some(AnthropicStopReason::ToolUse),
        ));
    }

    #[test]
    fn round_trip_redacted_thinking() {
        assert_round_trip(make_response(
            vec![
                block(AnthropicKnownOutputContentBlock::RedactedThinking {
                    data: "opaque".into(),
                }),
                text("Answer."),
            ],
            Some(AnthropicStopReason::EndTurn),
        ));
    }

    #[test]
    fn round_trip_max_tokens() {
        assert_round_trip(make_response(
            vec![text("truncated...")],
            Some(AnthropicStopReason::MaxTokens),
        ));
    }

    #[test]
    fn round_trip_web_search() {
        assert_round_trip(make_response(
            vec![
                block(AnthropicKnownOutputContentBlock::ServerToolUse {
                    id: "ws".into(),
                    name: "web_search".into(),
                    input: serde_json::json!({"query": "rust"}),
                    caller: None,
                }),
                block(AnthropicKnownOutputContentBlock::WebSearchToolResult {
                    tool_use_id: "ws".into(),
                    content: vec![AnthropicWebSearchToolResultItem::WebSearchResult {
                        url: "https://rust-lang.org".into(),
                        title: "Rust".into(),
                        encrypted_content: "enc".into(),
                        page_age: None,
                    }],
                }),
            ],
            Some(AnthropicStopReason::EndTurn),
        ));
    }

    #[test]
    fn round_trip_server_tool_use_with_caller() {
        assert_round_trip(make_response(
            vec![block(AnthropicKnownOutputContentBlock::ServerToolUse {
                id: "ws".into(),
                name: "web_search".into(),
                input: serde_json::json!({"query": "rust"}),
                caller: Some(serde_json::json!({"type": "direct"})),
            })],
            Some(AnthropicStopReason::EndTurn),
        ));
    }

    #[test]
    fn round_trip_text_with_citations() {
        assert_round_trip(make_response(
            vec![block(AnthropicKnownOutputContentBlock::Text {
                text: "hello".into(),
                citations: vec![AnthropicCitation::WebSearchResultLocation {
                    cited_text: "hello".into(),
                    encrypted_index: "enc".into(),
                    title: "Example".into(),
                    url: "https://example.com".into(),
                }],
            })],
            Some(AnthropicStopReason::EndTurn),
        ));
    }

    #[test]
    fn citations_preserved_in_start_block() {
        let citation = AnthropicCitation::WebSearchResultLocation {
            cited_text: "hi".into(),
            encrypted_index: "e".into(),
            title: "T".into(),
            url: "https://t.com".into(),
        };
        let events = decompose(make_response(
            vec![block(AnthropicKnownOutputContentBlock::Text {
                text: "hi".into(),
                citations: vec![citation.clone()],
            })],
            Some(AnthropicStopReason::EndTurn),
        ));

        match &events[1] {
            AnthropicStreamEvent::ContentBlockStart {
                content_block:
                    AnthropicOutputContentBlock::Known(AnthropicKnownOutputContentBlock::Text {
                        text,
                        citations,
                    }),
                ..
            } => {
                assert!(text.is_empty());
                assert_eq!(*citations, vec![citation]);
            }
            other => panic!("expected Text start with citations, got {other:?}"),
        }
    }

    #[test]
    fn caller_preserved_in_start_block() {
        let caller = Some(serde_json::json!({"type": "tool"}));
        let events = decompose(make_response(
            vec![block(AnthropicKnownOutputContentBlock::ServerToolUse {
                id: "s".into(),
                name: "ws".into(),
                input: serde_json::json!({"q": "x"}),
                caller: caller.clone(),
            })],
            Some(AnthropicStopReason::EndTurn),
        ));

        match &events[1] {
            AnthropicStreamEvent::ContentBlockStart {
                content_block:
                    AnthropicOutputContentBlock::Known(
                        AnthropicKnownOutputContentBlock::ServerToolUse {
                            caller: c, input, ..
                        },
                    ),
                ..
            } => {
                assert_eq!(*c, caller);
                assert_eq!(*input, serde_json::json!({}));
            }
            other => panic!("expected ServerToolUse start with caller, got {other:?}"),
        }
    }
}
