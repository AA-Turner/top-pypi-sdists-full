use super::accum::OpenResponsesToAnthropicMessagesAccum;
use crate::anthropic::convert::helpers::*;
use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::stream::*;
use crate::anthropic::types::*;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::tool_namespace::flatten_tool_name;
use crate::error::{ConversionError, ConversionWarning, WarningAction};
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;
use crate::stream::StreamTransform;

/// Converts Open Responses stream events to Anthropic Messages stream events, one at a time.
pub struct OpenResponsesToAnthropicMessagesStream {
    accum: OpenResponsesToAnthropicMessagesAccum,
}

impl Default for OpenResponsesToAnthropicMessagesStream {
    fn default() -> Self {
        Self::new()
    }
}

impl OpenResponsesToAnthropicMessagesStream {
    pub fn new() -> Self {
        Self {
            accum: OpenResponsesToAnthropicMessagesAccum::new(),
        }
    }
}

impl StreamTransform for OpenResponsesToAnthropicMessagesStream {
    type Input = OpenResponsesStreamEvent;
    type Output = AnthropicStreamEvent;

    fn transform(
        &mut self,
        input: OpenResponsesStreamEvent,
    ) -> Result<Vec<AnthropicStreamEvent>, ConversionError> {
        let accum = &mut self.accum;
        match input {
            OpenResponsesStreamEvent::ResponseCreated { response, .. } => {
                Ok(handle_response_created(accum, response))
            }
            OpenResponsesStreamEvent::ContentPartAdded { part, .. } => {
                Ok(handle_content_part_added(accum, part))
            }
            OpenResponsesStreamEvent::OutputTextDelta { delta, .. } => {
                Ok(vec![AnthropicStreamEvent::ContentBlockDelta {
                    index: accum.block_index.saturating_sub(1),
                    delta: AnthropicStreamDelta::TextDelta { text: delta },
                }])
            }
            OpenResponsesStreamEvent::OutputTextDone { .. } => {
                let index = accum.block_index.saturating_sub(1);
                Ok(vec![AnthropicStreamEvent::ContentBlockStop { index }])
            }
            OpenResponsesStreamEvent::OutputItemAdded { item, .. } => {
                Ok(handle_output_item_added(accum, item))
            }
            OpenResponsesStreamEvent::FunctionCallArgumentsDelta { delta, .. } => {
                Ok(vec![AnthropicStreamEvent::ContentBlockDelta {
                    index: accum.block_index.saturating_sub(1),
                    delta: AnthropicStreamDelta::InputJsonDelta {
                        partial_json: delta,
                    },
                }])
            }
            OpenResponsesStreamEvent::FunctionCallArgumentsDone { .. } => {
                let index = accum.block_index.saturating_sub(1);
                Ok(vec![AnthropicStreamEvent::ContentBlockStop { index }])
            }
            OpenResponsesStreamEvent::CustomToolCallInputDelta { .. }
            | OpenResponsesStreamEvent::CustomToolCallInputDone { .. } => Ok(vec![]),
            OpenResponsesStreamEvent::ReasoningSummaryTextDelta { delta, .. } => {
                Ok(handle_reasoning_delta(accum, delta))
            }
            OpenResponsesStreamEvent::ReasoningDelta { delta, .. } => {
                Ok(handle_reasoning_delta(accum, delta))
            }
            OpenResponsesStreamEvent::OutputItemDone { item, .. } => {
                Ok(handle_output_item_done(accum, item))
            }
            OpenResponsesStreamEvent::RefusalDelta { delta, .. } => {
                Ok(vec![AnthropicStreamEvent::ContentBlockDelta {
                    index: accum.block_index.saturating_sub(1),
                    delta: AnthropicStreamDelta::TextDelta { text: delta },
                }])
            }
            OpenResponsesStreamEvent::RefusalDone { .. } => {
                let index = accum.block_index.saturating_sub(1);
                Ok(vec![AnthropicStreamEvent::ContentBlockStop { index }])
            }
            OpenResponsesStreamEvent::ResponseCompleted { response, .. }
            | OpenResponsesStreamEvent::ResponseFailed { response, .. }
            | OpenResponsesStreamEvent::ResponseIncomplete { response, .. } => {
                Ok(handle_response_terminal(response))
            }
            OpenResponsesStreamEvent::OutputTextAnnotationAdded { annotation, .. } => {
                let Some(annotation) = annotation else {
                    return Ok(vec![]);
                };
                Ok(vec![AnthropicStreamEvent::ContentBlockDelta {
                    index: accum.block_index.saturating_sub(1),
                    delta: AnthropicStreamDelta::CitationsDelta {
                        citation: convert_open_responses_annotation_to_anthropic_messages(
                            annotation,
                        ),
                    },
                }])
            }
            OpenResponsesStreamEvent::WebSearchCallInProgress { .. }
            | OpenResponsesStreamEvent::WebSearchCallSearching { .. }
            | OpenResponsesStreamEvent::WebSearchCallCompleted { .. } => Ok(vec![]),
            OpenResponsesStreamEvent::Error {
                code,
                message,
                param,
                ..
            } => Ok(handle_error(accum, code, message, param)),
            // Heartbeat: preserve the wire keepalive across the rewrite (ENG-1250).
            OpenResponsesStreamEvent::Keepalive { .. } => Ok(vec![AnthropicStreamEvent::Ping]),
            // Events with no Anthropic Messages equivalent
            OpenResponsesStreamEvent::ResponseInProgress { .. }
            | OpenResponsesStreamEvent::ResponseQueued { .. }
            | OpenResponsesStreamEvent::ContentPartDone { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryPartAdded { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryPartDone { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryTextDone { .. }
            | OpenResponsesStreamEvent::ReasoningDone { .. } => Ok(vec![]),
            OpenResponsesStreamEvent::Unknown => {
                accum.ctx.warn(
                    "type",
                    WarningAction::Dropped,
                    "unknown Open Responses stream event dropped",
                );
                Ok(vec![])
            }
        }
    }

    fn flush(&mut self) -> Result<Vec<AnthropicStreamEvent>, ConversionError> {
        Ok(vec![])
    }

    fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        self.accum.ctx.take_warnings()
    }
}

fn handle_response_created(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    response: crate::open_responses::response::OpenResponsesResponse,
) -> Vec<AnthropicStreamEvent> {
    let usage = if let Some(usage) = response.usage {
        AnthropicUsage::from(usage)
    } else {
        accum.ctx.warn(
            "usage",
            WarningAction::Added,
            "Anthropic response requires usage; synthesized default usage",
        );
        AnthropicUsage::default()
    };
    let service_tier = response.service_tier.and_then(|tier| {
        AnthropicServiceTier::lossy_try_from(tier, &mut accum.ctx, "service_tier")
    });
    vec![AnthropicStreamEvent::MessageStart {
        message: AnthropicResponse {
            id: response.id,
            kind: "message".into(),
            role: AnthropicRole::Assistant,
            model: response.model,
            content: vec![],
            stop_reason: None,
            stop_sequence: None,
            usage,
            container: None,
            service_tier,
        },
    }]
}

fn handle_content_part_added(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    part: ContentPart,
) -> Vec<AnthropicStreamEvent> {
    match part {
        ContentPart::OutputText { .. } | ContentPart::Refusal { .. } => {
            let index = accum.next_block_index();
            vec![AnthropicStreamEvent::ContentBlockStart {
                index,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::Text {
                        text: String::new(),
                        citations: vec![],
                    },
                ),
            }]
        }
        _ => vec![],
    }
}

fn handle_output_item_added(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    item: OutputItem,
) -> Vec<AnthropicStreamEvent> {
    match item {
        OutputItem::FunctionCall {
            call_id,
            name,
            namespace,
            ..
        } => {
            let index = accum.next_block_index();
            vec![AnthropicStreamEvent::ContentBlockStart {
                index,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::ToolUse {
                        id: call_id,
                        name: flatten_tool_name(namespace.as_deref(), name),
                        input: serde_json::json!({}),
                    },
                ),
            }]
        }
        OutputItem::Reasoning { summary, .. } => {
            accum.pending_reasoning_item = true;
            accum.thinking_block_open = false;
            accum.thinking_block_index = None;
            accum.thinking_block_started = false;

            if summary.is_empty() {
                // Buffer empty reasoning items until the first
                // ReasoningSummaryTextDelta/ReasoningDelta. At Added time we cannot tell
                // whether this will become normal thinking text, remain redacted,
                // or end up being dropped.
                vec![]
            } else {
                let index = accum.next_block_index();
                accum.thinking_block_open = true;
                accum.thinking_block_index = Some(index);
                accum.thinking_block_started = true;
                vec![AnthropicStreamEvent::ContentBlockStart {
                    index,
                    content_block: AnthropicOutputContentBlock::Known(
                        AnthropicKnownOutputContentBlock::Thinking {
                            thinking: String::new(),
                            signature: String::new(),
                        },
                    ),
                }]
            }
        }
        OutputItem::CustomToolCall { .. } => {
            accum.ctx.warn(
                "custom_tool_call",
                WarningAction::Dropped,
                "custom tool calls are not supported in Anthropic",
            );
            vec![]
        }
        // Message items don't map to Anthropic Messages content block starts
        OutputItem::Message { .. }
        | OutputItem::FunctionCallOutput { .. }
        | OutputItem::CustomToolCallOutput { .. } => vec![],
        OutputItem::WebSearchCall { id, .. } => {
            let index = accum.next_block_index();
            accum.pending_web_search_block_index = Some(index);
            vec![AnthropicStreamEvent::ContentBlockStart {
                index,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::ServerToolUse {
                        id,
                        name: accum.ctx.config.web_search_name.into(),
                        input: serde_json::json!({}),
                        caller: None,
                    },
                ),
            }]
        }
        OutputItem::ToolSearchCall { .. } => {
            accum.ctx.warn(
                "tool_search_call",
                WarningAction::Dropped,
                "tool_search_call is not supported in Anthropic streaming",
            );
            vec![]
        }
        OutputItem::ToolSearchOutput { .. } => {
            accum.ctx.warn(
                "tool_search_output",
                WarningAction::Dropped,
                "tool_search_output is not supported in Anthropic streaming",
            );
            vec![]
        }
        OutputItem::Unknown => {
            accum.ctx.warn(
                "output_item.type",
                WarningAction::Dropped,
                "unknown Open Responses output item dropped",
            );
            vec![]
        }
    }
}

fn handle_reasoning_delta(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    delta: String,
) -> Vec<AnthropicStreamEvent> {
    if accum.pending_reasoning_item && !accum.thinking_block_started {
        let index = accum.next_block_index();
        accum.thinking_block_open = true;
        accum.thinking_block_index = Some(index);
        accum.thinking_block_started = true;
        return vec![
            AnthropicStreamEvent::ContentBlockStart {
                index,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::Thinking {
                        thinking: String::new(),
                        signature: String::new(),
                    },
                ),
            },
            AnthropicStreamEvent::ContentBlockDelta {
                index,
                delta: AnthropicStreamDelta::ThinkingDelta { thinking: delta },
            },
        ];
    }

    let Some(index) = accum
        .thinking_block_open
        .then_some(accum.thinking_block_index)
        .flatten()
    else {
        return vec![];
    };

    vec![AnthropicStreamEvent::ContentBlockDelta {
        index,
        delta: AnthropicStreamDelta::ThinkingDelta { thinking: delta },
    }]
}

fn handle_output_item_done(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    item: OutputItem,
) -> Vec<AnthropicStreamEvent> {
    match item {
        OutputItem::Reasoning {
            encrypted_content, ..
        } if accum.pending_reasoning_item => {
            accum.pending_reasoning_item = false;
            let started = accum.thinking_block_started;
            let index = accum.thinking_block_index;
            accum.thinking_block_open = false;
            accum.thinking_block_started = false;
            accum.thinking_block_index = None;

            if !started {
                match encrypted_content {
                    Some(data) if !data.is_empty() => {
                        let index = accum.next_block_index();
                        vec![
                            AnthropicStreamEvent::ContentBlockStart {
                                index,
                                content_block: AnthropicOutputContentBlock::Known(
                                    AnthropicKnownOutputContentBlock::RedactedThinking { data },
                                ),
                            },
                            AnthropicStreamEvent::ContentBlockStop { index },
                        ]
                    }
                    Some(_) => {
                        accum.ctx.warn(
                            "reasoning.encrypted_content",
                            WarningAction::Dropped,
                            "redacted reasoning is missing encrypted_content",
                        );
                        vec![]
                    }
                    None => {
                        accum
                            .ctx
                            .warn("reasoning", WarningAction::Dropped, "empty reasoning item");
                        vec![]
                    }
                }
            } else {
                let index = index.expect("started thinking block must have an index");
                let mut events = Vec::new();
                if let Some(signature) = encrypted_content.filter(|s| !s.is_empty()) {
                    events.push(AnthropicStreamEvent::ContentBlockDelta {
                        index,
                        delta: AnthropicStreamDelta::SignatureDelta { signature },
                    });
                }
                events.push(AnthropicStreamEvent::ContentBlockStop { index });
                events
            }
        }
        OutputItem::WebSearchCall { id, action, .. }
            if accum.pending_web_search_block_index.is_some() =>
        {
            let server_tool_use_index = accum.pending_web_search_block_index.take().unwrap();
            let result_index = accum.next_block_index();
            let mut events = Vec::new();

            let (query, content) = match action {
                Some(WebSearchAction::Search { query, sources, .. }) => {
                    let q = query.unwrap_or_default();
                    let content: Vec<AnthropicWebSearchToolResultItem> = sources
                        .into_iter()
                        .map(|s| AnthropicWebSearchToolResultItem::WebSearchResult {
                            url: s.url,
                            title: String::new(),
                            encrypted_content: String::new(),
                            page_age: None,
                        })
                        .collect();
                    (q, content)
                }
                _ => (String::new(), vec![]),
            };

            let query_json = serde_json::json!({ "query": query }).to_string();
            events.push(AnthropicStreamEvent::ContentBlockDelta {
                index: server_tool_use_index,
                delta: AnthropicStreamDelta::InputJsonDelta {
                    partial_json: query_json,
                },
            });
            events.push(AnthropicStreamEvent::ContentBlockStop {
                index: server_tool_use_index,
            });
            events.push(AnthropicStreamEvent::ContentBlockStart {
                index: result_index,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::WebSearchToolResult {
                        tool_use_id: id,
                        content,
                    },
                ),
            });
            events.push(AnthropicStreamEvent::ContentBlockStop {
                index: result_index,
            });
            events
        }
        _ => vec![],
    }
}

fn handle_response_terminal(
    response: crate::open_responses::response::OpenResponsesResponse,
) -> Vec<AnthropicStreamEvent> {
    if let Some(error) = response.error {
        return vec![AnthropicStreamEvent::Error {
            error: AnthropicStreamError {
                kind: error.code,
                message: error.message,
            },
        }];
    }

    let stop_reason = convert_open_responses_status_to_anthropic_messages_stop_reason(
        response.status,
        &response.output,
        response.incomplete_details.as_ref(),
    );
    let usage = response.usage.map(AnthropicUsage::from);
    vec![
        AnthropicStreamEvent::MessageDelta {
            delta: AnthropicMessageDelta {
                stop_reason,
                stop_sequence: None,
            },
            usage,
        },
        AnthropicStreamEvent::MessageStop,
    ]
}

/// Map an Open Responses [error event][or-docs] to an Anthropic Messages
/// [error event][am-docs].
///
/// OpenAI's payload is `{ code, message, param, sequence_number }` and Anthropic's
/// is `{ error: { type, message } }`, so we put `code` into Anthropic's `type`
/// (defaulting to `"api_error"` when missing) and drop `param` with a warning.
///
/// [or-docs]: https://developers.openai.com/api/reference/resources/responses/streaming-events
/// [am-docs]: https://docs.anthropic.com/en/api/messages-streaming#error-events
fn handle_error(
    accum: &mut OpenResponsesToAnthropicMessagesAccum,
    code: Option<String>,
    message: String,
    param: Option<String>,
) -> Vec<AnthropicStreamEvent> {
    if param.is_some() {
        accum.ctx.warn(
            "error.param",
            WarningAction::Dropped,
            "Anthropic error events have no `param` field",
        );
    }
    vec![AnthropicStreamEvent::Error {
        error: AnthropicStreamError {
            kind: code.unwrap_or_else(|| "api_error".into()),
            message,
        },
    }]
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::open_responses::response::OpenResponsesResponse;
    use crate::stream::StreamTransform;

    fn make_response_created() -> OpenResponsesStreamEvent {
        OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: 0,
            response: OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                model: "gpt-5".into(),
                status: ResponseStatus::InProgress,
                ..Default::default()
            },
        }
    }

    fn make_response_created_with_usage() -> OpenResponsesStreamEvent {
        OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: 0,
            response: OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                model: "gpt-5".into(),
                status: ResponseStatus::InProgress,
                usage: Some(Usage {
                    input_tokens: 1,
                    output_tokens: 2,
                    total_tokens: 3,
                    input_tokens_details: None,
                    output_tokens_details: None,
                }),
                ..Default::default()
            },
        }
    }

    #[test]
    fn unknown_event_is_dropped_with_warning() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let events = stream.transform(OpenResponsesStreamEvent::Unknown).unwrap();
        assert!(events.is_empty());

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "type");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
        assert_eq!(
            warnings[0].message,
            "unknown Open Responses stream event dropped"
        );
    }

    #[test]
    fn response_created_emits_message_start() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let events = stream.transform(make_response_created()).unwrap();
        assert_eq!(events.len(), 1);
        assert!(matches!(
            &events[0],
            AnthropicStreamEvent::MessageStart { .. }
        ));
    }

    #[test]
    fn response_created_without_usage_warns_and_synthesizes_default_usage() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let events = stream.transform(make_response_created()).unwrap();

        match &events[0] {
            AnthropicStreamEvent::MessageStart { message } => {
                assert_eq!(message.usage, AnthropicUsage::default());
            }
            other => panic!("expected MessageStart, got {other:?}"),
        }

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "usage");
        assert_eq!(
            warnings[0].message,
            "Anthropic response requires usage; synthesized default usage"
        );
    }

    #[test]
    fn text_delta_passes_through() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream.transform(make_response_created()).unwrap();
        stream
            .transform(OpenResponsesStreamEvent::ContentPartAdded {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                part: ContentPart::OutputText {
                    text: String::new(),
                    annotations: vec![],
                    logprobs: vec![],
                },
            })
            .unwrap();
        let events = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 2,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: "hello".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .unwrap();
        assert_eq!(events.len(), 1);
        match &events[0] {
            AnthropicStreamEvent::ContentBlockDelta {
                delta: AnthropicStreamDelta::TextDelta { text },
                ..
            } => assert_eq!(text, "hello"),
            other => panic!("expected TextDelta, got {other:?}"),
        }
    }

    #[test]
    fn response_completed_emits_message_delta_and_stop() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream.transform(make_response_created()).unwrap();
        let events = stream
            .transform(OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: 10,
                response: OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    model: "gpt-5".into(),
                    status: ResponseStatus::Completed,
                    ..Default::default()
                },
            })
            .unwrap();
        assert_eq!(events.len(), 2);
        assert!(matches!(
            &events[0],
            AnthropicStreamEvent::MessageDelta { .. }
        ));
        assert!(matches!(&events[1], AnthropicStreamEvent::MessageStop));
    }

    #[test]
    fn redacted_reasoning_without_encrypted_content_warns_and_is_dropped() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(make_response_created_with_usage())
            .unwrap();

        let added_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: Some(String::new()),
                },
            })
            .unwrap();
        assert!(added_events.is_empty());

        let done_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: 2,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: Some(String::new()),
                },
            })
            .unwrap();
        assert!(done_events.is_empty());

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "reasoning.encrypted_content");
        assert_eq!(
            warnings[0].message,
            "redacted reasoning is missing encrypted_content"
        );
    }

    #[test]
    fn empty_reasoning_is_buffered_until_first_reasoning_delta() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(make_response_created_with_usage())
            .unwrap();

        let added_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: None,
                },
            })
            .unwrap();
        assert!(added_events.is_empty());

        let delta_events = stream
            .transform(OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                sequence_number: 2,
                item_id: "rs_1".into(),
                output_index: 0,
                summary_index: 0,
                delta: "hello".into(),
                obfuscation: None,
            })
            .unwrap();
        assert_eq!(delta_events.len(), 2);
        assert!(matches!(
            &delta_events[0],
            AnthropicStreamEvent::ContentBlockStart { .. }
        ));
        assert!(matches!(
            &delta_events[1],
            AnthropicStreamEvent::ContentBlockDelta {
                delta: AnthropicStreamDelta::ThinkingDelta { thinking },
                ..
            } if thinking == "hello"
        ));
    }

    #[test]
    fn reasoning_added_without_encrypted_content_can_still_finish_as_redacted() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(make_response_created_with_usage())
            .unwrap();

        let added_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: None,
                },
            })
            .unwrap();
        assert!(added_events.is_empty());

        let done_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: 2,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: Some("secret".into()),
                },
            })
            .unwrap();
        assert_eq!(done_events.len(), 2);
        assert!(matches!(
            &done_events[0],
            AnthropicStreamEvent::ContentBlockStart {
                index: 0,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::RedactedThinking { data }
                ),
            } if data == "secret"
        ));
        assert!(matches!(
            &done_events[1],
            AnthropicStreamEvent::ContentBlockStop { index: 0 }
        ));
    }

    #[test]
    fn dropped_reasoning_does_not_create_a_block_index_gap() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(make_response_created_with_usage())
            .unwrap();

        stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: None,
                },
            })
            .unwrap();
        let dropped_events = stream
            .transform(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: 2,
                output_index: 0,
                item: OutputItem::Reasoning {
                    id: "rs_1".into(),
                    summary: vec![],
                    content: None,
                    encrypted_content: None,
                },
            })
            .unwrap();
        assert!(dropped_events.is_empty());

        let text_events = stream
            .transform(OpenResponsesStreamEvent::ContentPartAdded {
                sequence_number: 3,
                item_id: "msg_0".into(),
                output_index: 1,
                content_index: 0,
                part: ContentPart::OutputText {
                    text: String::new(),
                    annotations: vec![],
                    logprobs: vec![],
                },
            })
            .unwrap();
        assert!(matches!(
            &text_events[0],
            AnthropicStreamEvent::ContentBlockStart { index: 0, .. }
        ));
    }

    #[test]
    fn orphan_reasoning_delta_is_dropped_instead_of_attaching_to_previous_block() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(make_response_created_with_usage())
            .unwrap();

        let text_events = stream
            .transform(OpenResponsesStreamEvent::ContentPartAdded {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                part: ContentPart::OutputText {
                    text: String::new(),
                    annotations: vec![],
                    logprobs: vec![],
                },
            })
            .unwrap();
        assert!(matches!(
            &text_events[0],
            AnthropicStreamEvent::ContentBlockStart { index: 0, .. }
        ));

        let delta_events = stream
            .transform(OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                sequence_number: 2,
                item_id: "rs_orphan".into(),
                output_index: 1,
                summary_index: 0,
                delta: "orphan".into(),
                obfuscation: None,
            })
            .unwrap();
        assert!(delta_events.is_empty());
    }

    #[test]
    fn keepalive_maps_to_ping() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let out = stream
            .transform(OpenResponsesStreamEvent::Keepalive {
                sequence_number: 42,
            })
            .unwrap();
        assert_eq!(out.len(), 1);
        assert!(matches!(&out[0], AnthropicStreamEvent::Ping));
    }

    #[test]
    fn error_event_emits_anthropic_error() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let out = stream
            .transform(OpenResponsesStreamEvent::Error {
                sequence_number: 7,
                code: Some("server_error".into()),
                message: "boom".into(),
                param: None,
            })
            .unwrap();
        assert_eq!(out.len(), 1);
        match &out[0] {
            AnthropicStreamEvent::Error { error } => {
                assert_eq!(error.kind, "server_error");
                assert_eq!(error.message, "boom");
            }
            other => panic!("expected Error event, got {other:?}"),
        }
        assert!(stream.take_warnings().is_empty());
    }

    #[test]
    fn error_event_without_code_uses_fallback() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        let out = stream
            .transform(OpenResponsesStreamEvent::Error {
                sequence_number: 7,
                code: None,
                message: "boom".into(),
                param: None,
            })
            .unwrap();
        match &out[0] {
            AnthropicStreamEvent::Error { error } => {
                assert_eq!(error.kind, "api_error");
            }
            other => panic!("expected Error event, got {other:?}"),
        }
    }

    #[test]
    fn error_event_param_emits_warning() {
        let mut stream = OpenResponsesToAnthropicMessagesStream::new();
        stream
            .transform(OpenResponsesStreamEvent::Error {
                sequence_number: 7,
                code: Some("invalid_prompt".into()),
                message: "bad input".into(),
                param: Some("input.text".into()),
            })
            .unwrap();
        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "error.param");
    }
}
