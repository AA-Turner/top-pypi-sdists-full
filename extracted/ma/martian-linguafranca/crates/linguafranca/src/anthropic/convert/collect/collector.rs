use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::stream::*;
use crate::anthropic::types::*;
use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult, WarningAction};

/// Stateful collector that accumulates Anthropic Messages stream events
/// into a single [`AnthropicResponse`].
///
/// Feed events one at a time via [`ResponseCollector::feed`], then call
/// [`ResponseCollector::finalize`] to obtain the response.
///
/// Implements [`DynResponseCollector`](crate::collect::DynResponseCollector)
/// via the blanket impl, so it can be used type-erased at the Python boundary.
pub struct AnthropicCollector {
    /// The response header from `MessageStart`.
    response_header: Option<AnthropicResponse>,

    /// Accumulated content blocks.
    content: Vec<AnthropicOutputContentBlock>,

    /// The block currently being built from delta events.
    current_block: Option<BlockInProgress>,

    /// Stop reason from `MessageDelta`.
    stop_reason: Option<AnthropicStopReason>,

    /// Stop sequence from `MessageDelta`.
    stop_sequence: Option<String>,

    /// Final usage from `MessageDelta` (overrides initial usage from `MessageStart`).
    final_usage: Option<AnthropicUsage>,

    warnings: Vec<crate::error::ConversionWarning>,
    saw_any_event: bool,
    saw_message_stop: bool,
    finalized: bool,
}

enum BlockInProgress {
    Text {
        text: String,
        citations: Vec<AnthropicCitation>,
    },
    ToolUse {
        id: String,
        name: String,
        input_json: String,
    },
    Thinking {
        thinking: String,
        signature: String,
    },
    ServerToolUse {
        id: String,
        name: String,
        input_json: String,
        caller: Option<serde_json::Value>,
    },
}

impl Default for AnthropicCollector {
    fn default() -> Self {
        Self::new()
    }
}

impl AnthropicCollector {
    pub fn new() -> Self {
        Self {
            response_header: None,
            content: Vec::new(),
            current_block: None,
            stop_reason: None,
            stop_sequence: None,
            final_usage: None,
            warnings: Vec::new(),
            saw_any_event: false,
            saw_message_stop: false,
            finalized: false,
        }
    }

    /// Finalize the current in-progress block and push it to `content`.
    fn flush_current_block(&mut self) {
        let Some(block) = self.current_block.take() else {
            return;
        };

        let output = match block {
            BlockInProgress::Text { text, citations } => {
                AnthropicKnownOutputContentBlock::Text { text, citations }
            }
            BlockInProgress::ToolUse {
                id,
                name,
                input_json,
            } => {
                let input = serde_json::from_str(&input_json).unwrap_or_else(|e| {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "tool_use.input".into(),
                        action: WarningAction::Changed,
                        message: format!(
                            "failed to parse tool_use input JSON ({e}), replaced with empty object; \
                             input_json: {input_json}"
                        ),
                    });
                    serde_json::Value::Object(Default::default())
                });
                AnthropicKnownOutputContentBlock::ToolUse { id, name, input }
            }
            BlockInProgress::Thinking {
                thinking,
                signature,
            } => AnthropicKnownOutputContentBlock::Thinking {
                thinking,
                signature,
            },
            BlockInProgress::ServerToolUse {
                id,
                name,
                input_json,
                caller,
            } => {
                let input = serde_json::from_str(&input_json).unwrap_or_else(|e| {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "server_tool_use.input".into(),
                        action: WarningAction::Changed,
                        message: format!(
                            "failed to parse server_tool_use input JSON ({e}), replaced with empty object; \
                             input_json: {input_json}"
                        ),
                    });
                    serde_json::Value::Object(Default::default())
                });
                AnthropicKnownOutputContentBlock::ServerToolUse {
                    id,
                    name,
                    input,
                    caller,
                }
            }
        };

        self.content
            .push(AnthropicOutputContentBlock::Known(output));
    }

    fn handle_content_block_start(&mut self, content_block: AnthropicOutputContentBlock) {
        // Flush any previous in-progress block.
        self.flush_current_block();

        match content_block {
            AnthropicOutputContentBlock::Known(known) => match known {
                AnthropicKnownOutputContentBlock::Text { citations, .. } => {
                    self.current_block = Some(BlockInProgress::Text {
                        text: String::new(),
                        citations,
                    });
                }
                AnthropicKnownOutputContentBlock::ToolUse { id, name, .. } => {
                    self.current_block = Some(BlockInProgress::ToolUse {
                        id,
                        name,
                        input_json: String::new(),
                    });
                }
                AnthropicKnownOutputContentBlock::Thinking { .. } => {
                    self.current_block = Some(BlockInProgress::Thinking {
                        thinking: String::new(),
                        signature: String::new(),
                    });
                }
                AnthropicKnownOutputContentBlock::ServerToolUse {
                    id, name, caller, ..
                } => {
                    self.current_block = Some(BlockInProgress::ServerToolUse {
                        id,
                        name,
                        input_json: String::new(),
                        caller,
                    });
                }
                // These block types arrive fully formed — push directly to content.
                AnthropicKnownOutputContentBlock::RedactedThinking { .. }
                | AnthropicKnownOutputContentBlock::WebSearchToolResult { .. }
                | AnthropicKnownOutputContentBlock::ToolSearchToolResult { .. } => {
                    self.content.push(AnthropicOutputContentBlock::Known(known));
                }
            },
            AnthropicOutputContentBlock::Other(value) => {
                // Unknown block types — preserve as-is.
                self.content.push(AnthropicOutputContentBlock::Other(value));
            }
        }
    }

    fn handle_content_block_delta(&mut self, delta: AnthropicStreamDelta) {
        let Some(block) = &mut self.current_block else {
            let delta_kind = match &delta {
                AnthropicStreamDelta::TextDelta { .. } => "text_delta",
                AnthropicStreamDelta::InputJsonDelta { .. } => "input_json_delta",
                AnthropicStreamDelta::CitationsDelta { .. } => "citations_delta",
                AnthropicStreamDelta::ThinkingDelta { .. } => "thinking_delta",
                AnthropicStreamDelta::SignatureDelta { .. } => "signature_delta",
                AnthropicStreamDelta::Unknown => "unknown_delta",
            };
            self.warnings.push(crate::error::ConversionWarning {
                field: "content_block_delta".into(),
                action: WarningAction::Dropped,
                message: format!("{delta_kind} received without an active content block, dropped"),
            });
            return;
        };

        match delta {
            AnthropicStreamDelta::TextDelta { text } => {
                if let BlockInProgress::Text { text: buf, .. } = block {
                    buf.push_str(&text);
                } else {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "content_block_delta".into(),
                        action: WarningAction::Dropped,
                        message: "text_delta received for non-text block, dropped".into(),
                    });
                }
            }
            AnthropicStreamDelta::InputJsonDelta { partial_json } => match block {
                BlockInProgress::ToolUse { input_json, .. }
                | BlockInProgress::ServerToolUse { input_json, .. } => {
                    input_json.push_str(&partial_json);
                }
                _ => {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "content_block_delta".into(),
                        action: WarningAction::Dropped,
                        message: "input_json_delta received for non-tool block, dropped".into(),
                    });
                }
            },
            AnthropicStreamDelta::CitationsDelta { citation } => {
                if let BlockInProgress::Text { citations, .. } = block {
                    citations.push(citation);
                } else {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "content_block_delta".into(),
                        action: WarningAction::Dropped,
                        message: "citations_delta received for non-text block, dropped".into(),
                    });
                }
            }
            AnthropicStreamDelta::ThinkingDelta { thinking } => {
                if let BlockInProgress::Thinking { thinking: buf, .. } = block {
                    buf.push_str(&thinking);
                } else {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "content_block_delta".into(),
                        action: WarningAction::Dropped,
                        message: "thinking_delta received for non-thinking block, dropped".into(),
                    });
                }
            }
            AnthropicStreamDelta::SignatureDelta { signature } => {
                if let BlockInProgress::Thinking { signature: buf, .. } = block {
                    buf.push_str(&signature);
                } else {
                    self.warnings.push(crate::error::ConversionWarning {
                        field: "content_block_delta".into(),
                        action: WarningAction::Dropped,
                        message: "signature_delta received for non-thinking block, dropped".into(),
                    });
                }
            }
            AnthropicStreamDelta::Unknown => {
                self.warnings.push(crate::error::ConversionWarning {
                    field: "content_block_delta.delta.type".into(),
                    action: WarningAction::Dropped,
                    message: "unknown Anthropic Messages stream delta dropped".into(),
                });
            }
        }
    }
}

impl ResponseCollector for AnthropicCollector {
    type Event = AnthropicStreamEvent;
    type Response = AnthropicResponse;

    fn feed(&mut self, event: AnthropicStreamEvent) -> Result<(), ConversionError> {
        if self.finalized {
            return Err(ConversionError::InvalidInput(
                "cannot feed events after finalize".into(),
            ));
        }

        self.saw_any_event = true;

        match event {
            AnthropicStreamEvent::MessageStart { message } => {
                self.response_header = Some(message);
            }
            AnthropicStreamEvent::ContentBlockStart { content_block, .. } => {
                self.handle_content_block_start(content_block);
            }
            AnthropicStreamEvent::ContentBlockDelta { delta, .. } => {
                self.handle_content_block_delta(delta);
            }
            AnthropicStreamEvent::ContentBlockStop { .. } => {
                self.flush_current_block();
            }
            AnthropicStreamEvent::MessageDelta { delta, usage } => {
                self.stop_reason = delta.stop_reason;
                self.stop_sequence = delta.stop_sequence;
                if let Some(usage) = usage {
                    self.final_usage = Some(usage);
                }
            }
            AnthropicStreamEvent::MessageStop => {
                self.saw_message_stop = true;
            }
            AnthropicStreamEvent::Ping => {}
            AnthropicStreamEvent::Error { error } => {
                return Err(ConversionError::InvalidInput(format!(
                    "Anthropic stream error: {}: {}",
                    error.kind, error.message
                )));
            }
            AnthropicStreamEvent::Unknown => {
                self.warnings.push(crate::error::ConversionWarning {
                    field: "type".into(),
                    action: WarningAction::Dropped,
                    message: "unknown Anthropic Messages stream event dropped".into(),
                });
            }
        }

        Ok(())
    }

    fn finalize(&mut self) -> Result<ConversionResult<AnthropicResponse>, ConversionError> {
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

        // Flush any remaining in-progress block (defensive).
        self.flush_current_block();

        let header = self.response_header.take().ok_or_else(|| {
            ConversionError::InvalidInput(
                "cannot collect stream: no message_start event received".into(),
            )
        })?;

        let usage = self.final_usage.take().unwrap_or(header.usage);
        let content = std::mem::take(&mut self.content);

        let response = AnthropicResponse {
            id: header.id,
            kind: header.kind,
            role: header.role,
            model: header.model,
            content,
            stop_reason: self.stop_reason.take(),
            stop_sequence: self.stop_sequence.take(),
            usage,
            container: header.container,
            service_tier: header.service_tier,
        };

        let mut result =
            ConversionResult::with_warnings(response, std::mem::take(&mut self.warnings));

        if !self.saw_message_stop {
            result.warn(
                "message_stop",
                WarningAction::Changed,
                "stream ended without message_stop event",
            );
        }

        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn msg_start() -> AnthropicStreamEvent {
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
        }
    }

    fn block_start(index: u64, block: AnthropicKnownOutputContentBlock) -> AnthropicStreamEvent {
        AnthropicStreamEvent::ContentBlockStart {
            index,
            content_block: AnthropicOutputContentBlock::Known(block),
        }
    }

    fn delta(index: u64, d: AnthropicStreamDelta) -> AnthropicStreamEvent {
        AnthropicStreamEvent::ContentBlockDelta { index, delta: d }
    }

    fn block_stop(index: u64) -> AnthropicStreamEvent {
        AnthropicStreamEvent::ContentBlockStop { index }
    }

    fn msg_delta(
        stop_reason: Option<AnthropicStopReason>,
        usage: Option<AnthropicUsage>,
    ) -> AnthropicStreamEvent {
        AnthropicStreamEvent::MessageDelta {
            delta: AnthropicMessageDelta {
                stop_reason,
                stop_sequence: None,
            },
            usage,
        }
    }

    fn msg_stop() -> AnthropicStreamEvent {
        AnthropicStreamEvent::MessageStop
    }

    /// Feed all events, finalize, and return the result.
    fn collect(events: Vec<AnthropicStreamEvent>) -> ConversionResult<AnthropicResponse> {
        let mut c = AnthropicCollector::new();
        for e in events {
            c.feed(e).unwrap();
        }
        c.finalize().unwrap()
    }

    fn end_turn() -> Option<AnthropicStopReason> {
        Some(AnthropicStopReason::EndTurn)
    }

    fn usage(output_tokens: u64) -> Option<AnthropicUsage> {
        Some(AnthropicUsage {
            input_tokens: 10,
            output_tokens,
            ..Default::default()
        })
    }

    // ── Content block collection ──

    #[test]
    fn text_deltas_are_concatenated() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::Text {
                    text: String::new(),
                    citations: vec![],
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::TextDelta {
                    text: "hello ".into(),
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::TextDelta {
                    text: "world".into(),
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), usage(20)),
            msg_stop(),
        ]);

        assert_eq!(r.value.content.len(), 1);
        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(AnthropicKnownOutputContentBlock::Text {
                text,
                ..
            }) => {
                assert_eq!(text, "hello world");
            }
            other => panic!("expected Text, got {other:?}"),
        }
        assert_eq!(r.value.stop_reason, end_turn());
        assert_eq!(r.value.usage.output_tokens, 20);
        assert!(r.warnings.is_empty());
    }

    #[test]
    fn tool_use_json_chunks_are_reassembled() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::ToolUse {
                    id: "t1".into(),
                    name: "fn".into(),
                    input: serde_json::json!({}),
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::InputJsonDelta {
                    partial_json: "{\"a\":".into(),
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::InputJsonDelta {
                    partial_json: "1}".into(),
                },
            ),
            block_stop(0),
            msg_delta(Some(AnthropicStopReason::ToolUse), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(AnthropicKnownOutputContentBlock::ToolUse {
                id,
                name,
                input,
            }) => {
                assert_eq!(id, "t1");
                assert_eq!(name, "fn");
                assert_eq!(input, &serde_json::json!({"a": 1}));
            }
            other => panic!("expected ToolUse, got {other:?}"),
        }
    }

    #[test]
    fn thinking_and_signature_are_reassembled() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::Thinking {
                    thinking: String::new(),
                    signature: String::new(),
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::ThinkingDelta {
                    thinking: "hmm".into(),
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::SignatureDelta {
                    signature: "sig".into(),
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(AnthropicKnownOutputContentBlock::Thinking {
                thinking,
                signature,
            }) => {
                assert_eq!(thinking, "hmm");
                assert_eq!(signature, "sig");
            }
            other => panic!("expected Thinking, got {other:?}"),
        }
    }

    #[test]
    fn redacted_thinking_passed_through_from_start() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::RedactedThinking {
                    data: "opaque".into(),
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(
                AnthropicKnownOutputContentBlock::RedactedThinking { data },
            ) => {
                assert_eq!(data, "opaque");
            }
            other => panic!("expected RedactedThinking, got {other:?}"),
        }
    }

    #[test]
    fn server_tool_use_json_is_reassembled() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::ServerToolUse {
                    id: "ws".into(),
                    name: "web_search".into(),
                    input: serde_json::json!({}),
                    caller: None,
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::InputJsonDelta {
                    partial_json: "{\"q\":\"r\"}".into(),
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(
                AnthropicKnownOutputContentBlock::ServerToolUse { input, .. },
            ) => {
                assert_eq!(input, &serde_json::json!({"q": "r"}));
            }
            other => panic!("expected ServerToolUse, got {other:?}"),
        }
    }

    #[test]
    fn web_search_tool_result_passed_through_from_start() {
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::WebSearchToolResult {
                    tool_use_id: "ws".into(),
                    content: vec![AnthropicWebSearchToolResultItem::WebSearchResult {
                        url: "https://x.com".into(),
                        title: "X".into(),
                        encrypted_content: "e".into(),
                        page_age: None,
                    }],
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(
                AnthropicKnownOutputContentBlock::WebSearchToolResult {
                    tool_use_id,
                    content,
                },
            ) => {
                assert_eq!(tool_use_id, "ws");
                assert_eq!(content.len(), 1);
            }
            other => panic!("expected WebSearchToolResult, got {other:?}"),
        }
    }

    // ── Usage precedence ──

    #[test]
    fn message_delta_usage_overrides_initial() {
        let r = collect(vec![
            msg_start(),
            msg_delta(end_turn(), usage(99)),
            msg_stop(),
        ]);
        assert_eq!(r.value.usage.output_tokens, 99);
    }

    #[test]
    fn falls_back_to_initial_usage_when_delta_has_none() {
        let r = collect(vec![msg_start(), msg_delta(end_turn(), None), msg_stop()]);
        assert_eq!(r.value.usage.output_tokens, 1); // from msg_start
    }

    // ── Edge cases / errors ──

    #[test]
    fn ping_is_ignored() {
        let r = collect(vec![msg_start(), AnthropicStreamEvent::Ping, msg_stop()]);
        assert_eq!(r.value.id, "msg_1");
    }

    #[test]
    fn unknown_event_warns_and_continues() {
        let r = collect(vec![msg_start(), AnthropicStreamEvent::Unknown, msg_stop()]);
        assert_eq!(r.value.id, "msg_1");
        assert_eq!(r.warnings.len(), 1);
        assert_eq!(r.warnings[0].field, "type");
        assert_eq!(r.warnings[0].action, WarningAction::Dropped);
        assert_eq!(
            r.warnings[0].message,
            "unknown Anthropic Messages stream event dropped"
        );
    }

    #[test]
    fn missing_message_stop_warns() {
        let r = collect(vec![msg_start(), msg_delta(end_turn(), None)]);
        assert_eq!(r.warnings.len(), 1);
        assert_eq!(r.warnings[0].field, "message_stop");
    }

    #[test]
    fn error_event_returns_error() {
        let mut c = AnthropicCollector::new();
        c.feed(msg_start()).unwrap();
        let err = c
            .feed(AnthropicStreamEvent::Error {
                error: AnthropicStreamError {
                    kind: "overloaded_error".into(),
                    message: "Overloaded".into(),
                },
            })
            .unwrap_err();
        assert!(err.to_string().contains("overloaded_error"));
        assert!(err.to_string().contains("Overloaded"));
    }

    #[test]
    fn no_events_returns_error() {
        assert!(
            AnthropicCollector::new()
                .finalize()
                .unwrap_err()
                .to_string()
                .contains("no events")
        );
    }

    #[test]
    fn no_message_start_returns_error() {
        let mut c = AnthropicCollector::new();
        c.feed(AnthropicStreamEvent::Ping).unwrap();
        assert!(
            c.finalize()
                .unwrap_err()
                .to_string()
                .contains("no message_start")
        );
    }

    #[test]
    fn double_finalize_returns_error() {
        let mut c = AnthropicCollector::new();
        c.feed(msg_start()).unwrap();
        c.feed(msg_stop()).unwrap();
        assert!(c.finalize().is_ok());
        assert!(
            c.finalize()
                .unwrap_err()
                .to_string()
                .contains("already been finalized")
        );
    }

    #[test]
    fn feed_after_finalize_returns_error() {
        let mut c = AnthropicCollector::new();
        c.feed(msg_start()).unwrap();
        c.feed(msg_stop()).unwrap();
        c.finalize().unwrap();
        assert!(
            c.feed(AnthropicStreamEvent::Ping)
                .unwrap_err()
                .to_string()
                .contains("after finalize")
        );
    }

    // ── Citations preservation ──

    #[test]
    fn text_citations_preserved_from_start_block() {
        let citation = AnthropicCitation::WebSearchResultLocation {
            cited_text: "hello".into(),
            encrypted_index: "enc".into(),
            title: "Example".into(),
            url: "https://example.com".into(),
        };
        let r = collect(vec![
            msg_start(),
            block_start(
                0,
                AnthropicKnownOutputContentBlock::Text {
                    text: String::new(),
                    citations: vec![citation.clone()],
                },
            ),
            delta(
                0,
                AnthropicStreamDelta::TextDelta {
                    text: "hello".into(),
                },
            ),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        match &r.value.content[0] {
            AnthropicOutputContentBlock::Known(AnthropicKnownOutputContentBlock::Text {
                text,
                citations,
            }) => {
                assert_eq!(text, "hello");
                assert_eq!(*citations, vec![citation]);
            }
            other => panic!("expected Text, got {other:?}"),
        }
    }

    // ── Mismatched delta warnings ──

    fn assert_mismatched_delta_warns(
        start_block: AnthropicKnownOutputContentBlock,
        wrong_delta: AnthropicStreamDelta,
        expected_substring: &str,
    ) {
        let r = collect(vec![
            msg_start(),
            block_start(0, start_block),
            delta(0, wrong_delta),
            block_stop(0),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);
        assert!(
            r.warnings.iter().any(|w| w.field == "content_block_delta"
                && w.message.contains(expected_substring)),
            "expected warning containing '{expected_substring}', got: {:?}",
            r.warnings,
        );
    }

    fn text_block() -> AnthropicKnownOutputContentBlock {
        AnthropicKnownOutputContentBlock::Text {
            text: String::new(),
            citations: vec![],
        }
    }

    fn tool_block() -> AnthropicKnownOutputContentBlock {
        AnthropicKnownOutputContentBlock::ToolUse {
            id: "t".into(),
            name: "f".into(),
            input: serde_json::json!({}),
        }
    }

    #[test]
    fn text_delta_on_tool_block_warns() {
        assert_mismatched_delta_warns(
            tool_block(),
            AnthropicStreamDelta::TextDelta { text: "x".into() },
            "text_delta",
        );
    }

    #[test]
    fn input_json_delta_on_text_block_warns() {
        assert_mismatched_delta_warns(
            text_block(),
            AnthropicStreamDelta::InputJsonDelta {
                partial_json: "{}".into(),
            },
            "input_json_delta",
        );
    }

    #[test]
    fn thinking_delta_on_text_block_warns() {
        assert_mismatched_delta_warns(
            text_block(),
            AnthropicStreamDelta::ThinkingDelta {
                thinking: "x".into(),
            },
            "thinking_delta",
        );
    }

    #[test]
    fn signature_delta_on_tool_block_warns() {
        assert_mismatched_delta_warns(
            tool_block(),
            AnthropicStreamDelta::SignatureDelta {
                signature: "x".into(),
            },
            "signature_delta",
        );
    }

    #[test]
    fn delta_without_active_block_warns() {
        let r = collect(vec![
            msg_start(),
            // No ContentBlockStart — delta arrives orphaned.
            delta(
                0,
                AnthropicStreamDelta::TextDelta {
                    text: "orphan".into(),
                },
            ),
            msg_delta(end_turn(), None),
            msg_stop(),
        ]);

        assert!(r.warnings.iter().any(|w| w.field == "content_block_delta"
            && w.message.contains("text_delta")
            && w.message.contains("without an active content block")));
    }
}
