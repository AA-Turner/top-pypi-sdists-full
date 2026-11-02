use crate::chat_completions_openai::convert::mapping::open_responses_status_to_chat_completions_finish_reason;
use crate::chat_completions_openai::stream::{
    ChatCompletionsStreamChoice, ChatCompletionsStreamChunk, ChatCompletionsStreamCustomDelta,
    ChatCompletionsStreamDelta, ChatCompletionsStreamFunctionDelta, ChatCompletionsStreamToolCall,
};
use crate::convert::tool_namespace::flatten_tool_name;
use crate::error::{ConversionError, ConversionWarning, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;
use crate::stream::StreamTransform;

use super::accum::OpenResponsesToChatCompletionsAccum;

/// Converts Open Responses stream events to Chat Completions stream chunks.
pub struct OpenResponsesToChatCompletionsStream {
    accum: OpenResponsesToChatCompletionsAccum,
}

impl Default for OpenResponsesToChatCompletionsStream {
    fn default() -> Self {
        Self::new()
    }
}

impl OpenResponsesToChatCompletionsStream {
    pub fn new() -> Self {
        Self {
            accum: OpenResponsesToChatCompletionsAccum::new(),
        }
    }
}

impl StreamTransform for OpenResponsesToChatCompletionsStream {
    type Input = OpenResponsesStreamEvent;
    type Output = ChatCompletionsStreamChunk;

    fn transform(
        &mut self,
        input: OpenResponsesStreamEvent,
    ) -> Result<Vec<ChatCompletionsStreamChunk>, ConversionError> {
        let accum = &mut self.accum;
        if matches!(input, OpenResponsesStreamEvent::Unknown) {
            accum.ctx.warn(
                "type",
                WarningAction::Dropped,
                "unknown Open Responses stream event dropped",
            );
            return Ok(vec![]);
        }
        accum.saw_any_event = true;

        match input {
            OpenResponsesStreamEvent::ResponseCreated { response, .. }
            | OpenResponsesStreamEvent::ResponseQueued { response, .. }
            | OpenResponsesStreamEvent::ResponseInProgress { response, .. } => {
                let OpenResponsesResponse {
                    id,
                    model,
                    created_at,
                    service_tier,
                    ..
                } = response;
                accum.remember_response_header(id, model, created_at, service_tier);
                Ok(vec![])
            }
            OpenResponsesStreamEvent::OutputTextDelta {
                delta,
                logprobs,
                obfuscation,
                ..
            } => {
                if !logprobs.is_empty() {
                    accum.ctx.warn(
                        "output_text.logprobs",
                        WarningAction::Dropped,
                        "not supported in Chat Completions streaming",
                    );
                }
                Ok(emit_delta_chunk(
                    accum,
                    ChatCompletionsStreamDelta {
                        role: None,
                        content: Some(delta),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    None,
                    obfuscation,
                ))
            }
            OpenResponsesStreamEvent::RefusalDelta { delta, .. } => Ok(emit_delta_chunk(
                accum,
                ChatCompletionsStreamDelta {
                    role: None,
                    content: None,
                    tool_calls: None,
                    refusal: Some(delta),
                    reasoning_content: None,
                    reasoning_details: None,
                },
                None,
                None,
            )),
            OpenResponsesStreamEvent::ReasoningDelta {
                delta, obfuscation, ..
            }
            | OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                delta, obfuscation, ..
            } => Ok(emit_delta_chunk(
                accum,
                ChatCompletionsStreamDelta {
                    role: None,
                    content: None,
                    tool_calls: None,
                    refusal: None,
                    reasoning_content: Some(delta),
                    reasoning_details: None,
                },
                None,
                obfuscation,
            )),
            OpenResponsesStreamEvent::OutputItemAdded { item, .. } => {
                handle_output_item_added(accum, item)
            }
            OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
                item_id,
                delta,
                obfuscation,
                ..
            } => {
                if !accum.tool_call_indexes.contains_key(&item_id) {
                    accum.ctx.warn(
                        "function_call_arguments.item_id",
                        WarningAction::Added,
                        "function call arguments delta arrived before tool-call prelude; synthesized tool-call index",
                    );
                }
                accum.record_emitted_tool_call_arguments(&item_id, &delta);
                let index = accum.get_or_create_tool_call_index(&item_id);
                Ok(emit_delta_chunk(
                    accum,
                    ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index,
                            id: None,
                            kind: None,
                            function: Some(ChatCompletionsStreamFunctionDelta {
                                name: None,
                                arguments: Some(delta),
                            }),
                            custom: None,
                        }]),
                    },
                    None,
                    obfuscation,
                ))
            }
            OpenResponsesStreamEvent::CustomToolCallInputDelta {
                item_id,
                delta,
                obfuscation,
                ..
            } => {
                if !accum.tool_call_indexes.contains_key(&item_id) {
                    accum.ctx.warn(
                        "custom_tool_call_input.item_id",
                        WarningAction::Added,
                        "custom tool call input delta arrived before tool-call prelude; synthesized tool-call index",
                    );
                }
                accum.record_emitted_tool_call_arguments(&item_id, &delta);
                let index = accum.get_or_create_tool_call_index(&item_id);
                Ok(emit_delta_chunk(
                    accum,
                    ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index,
                            id: None,
                            kind: None,
                            function: None,
                            custom: Some(ChatCompletionsStreamCustomDelta {
                                name: None,
                                input: Some(delta),
                            }),
                        }]),
                    },
                    None,
                    obfuscation,
                ))
            }
            OpenResponsesStreamEvent::OutputTextAnnotationAdded { annotation, .. } => {
                if annotation.is_some() {
                    accum.ctx.warn(
                        "annotation",
                        WarningAction::Dropped,
                        "not supported in Chat Completions streaming",
                    );
                }
                Ok(vec![])
            }
            OpenResponsesStreamEvent::ResponseCompleted { response, .. }
            | OpenResponsesStreamEvent::ResponseIncomplete { response, .. }
            | OpenResponsesStreamEvent::ResponseFailed { response, .. } => {
                let OpenResponsesResponse {
                    id,
                    model,
                    created_at,
                    status,
                    output,
                    usage,
                    error,
                    service_tier,
                    ..
                } = response;
                accum.remember_response_header(id, model, created_at, service_tier);
                accum.saw_terminal_event = true;
                Ok(handle_terminal(accum, status, output, usage, error))
            }
            OpenResponsesStreamEvent::ContentPartAdded { part, .. } => {
                match part {
                    ContentPart::OutputText { .. } | ContentPart::Refusal { .. } => {}
                    ContentPart::InputText { .. }
                    | ContentPart::InputImage { .. }
                    | ContentPart::InputFile { .. } => {
                        accum.ctx.warn(
                            "content_part",
                            WarningAction::Dropped,
                            "input-type content in output",
                        );
                    }
                    ContentPart::Text { .. }
                    | ContentPart::SummaryText { .. }
                    | ContentPart::ReasoningText { .. } => {
                        accum.ctx.warn(
                            "content_part",
                            WarningAction::Dropped,
                            "non-output content part in output message is not representable in Chat Completions streaming",
                        );
                    }
                }
                Ok(vec![])
            }
            OpenResponsesStreamEvent::OutputItemDone {
                item:
                    OutputItem::Reasoning {
                        encrypted_content: Some(data),
                        ..
                    },
                ..
            } => Ok(emit_delta_chunk(
                accum,
                ChatCompletionsStreamDelta {
                    role: None,
                    content: None,
                    tool_calls: None,
                    refusal: None,
                    reasoning_content: None,
                    reasoning_details: Some(vec![serde_json::json!({
                        "type": "reasoning.encrypted",
                        "data": data,
                        "format": "unknown",
                        "index": 0,
                    })]),
                },
                None,
                None,
            )),
            OpenResponsesStreamEvent::OutputItemDone { .. } => Ok(vec![]),
            OpenResponsesStreamEvent::OutputTextDone { logprobs, .. } => {
                if !logprobs.is_empty() {
                    accum.ctx.warn(
                        "output_text.logprobs",
                        WarningAction::Dropped,
                        "not supported in Chat Completions streaming",
                    );
                }
                Ok(vec![])
            }
            OpenResponsesStreamEvent::Error { code, message, .. } => {
                // Chat Completions streaming has no native error *event* — but it
                // does have a terminal `finish_reason: "error"`. Emit one final
                // empty-delta chunk so clients see a clean termination instead of
                // a silently-truncated stream. The code/message goes into the
                // warning channel for operator-facing logging.
                accum.ctx.warn(
                    "error",
                    WarningAction::Changed,
                    format!(
                        "Open Responses error event ({}) surfaced as finish_reason=\"error\": {message}",
                        code.as_deref().unwrap_or("unknown"),
                    ),
                );
                accum.saw_terminal_event = true;
                Ok(emit_delta_chunk(
                    accum,
                    ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    Some(crate::chat_completions_openai::types::ChatCompletionsFinishReason::Error),
                    None,
                ))
            }
            OpenResponsesStreamEvent::ContentPartDone { .. }
            | OpenResponsesStreamEvent::RefusalDone { .. }
            | OpenResponsesStreamEvent::ReasoningDone { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryPartAdded { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryPartDone { .. }
            | OpenResponsesStreamEvent::ReasoningSummaryTextDone { .. }
            | OpenResponsesStreamEvent::FunctionCallArgumentsDone { .. }
            | OpenResponsesStreamEvent::CustomToolCallInputDone { .. }
            | OpenResponsesStreamEvent::WebSearchCallInProgress { .. }
            | OpenResponsesStreamEvent::WebSearchCallSearching { .. }
            | OpenResponsesStreamEvent::WebSearchCallCompleted { .. }
            | OpenResponsesStreamEvent::Keepalive { .. } => Ok(vec![]),
            OpenResponsesStreamEvent::Unknown => unreachable!("handled before match"),
        }
    }

    fn flush(&mut self) -> Result<Vec<ChatCompletionsStreamChunk>, ConversionError> {
        if self.accum.saw_any_event && !self.accum.saw_terminal_event {
            self.accum.ctx.warn(
                "response",
                WarningAction::Dropped,
                "stream ended without terminal Open Responses event; final Chat Completions finish_reason was not emitted",
            );
        }

        // We do not synthesize terminal chunks on flush. OR->CC requires an
        // explicit terminal Open Responses event to emit finish_reason.
        Ok(vec![])
    }

    fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        self.accum.ctx.take_warnings()
    }
}

fn handle_output_item_added(
    accum: &mut OpenResponsesToChatCompletionsAccum,
    item: OutputItem,
) -> Result<Vec<ChatCompletionsStreamChunk>, ConversionError> {
    match item {
        OutputItem::FunctionCall {
            id,
            call_id,
            name,
            namespace,
            arguments,
            ..
        } => {
            let name = flatten_tool_name(namespace.as_deref(), name);
            accum.saw_function_call = true;
            let emitted_arguments =
                accum.inline_tool_call_arguments_to_emit(&id, arguments, "function_call.arguments");
            if let Some(arguments) = emitted_arguments.as_deref() {
                accum.record_emitted_tool_call_arguments(&id, arguments);
            }
            let index = accum.get_or_create_tool_call_index(&id);
            Ok(emit_delta_chunk(
                accum,
                ChatCompletionsStreamDelta {
                    role: None,
                    content: None,
                    tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                        index,
                        id: (!call_id.is_empty()).then_some(call_id),
                        kind: Some("function".into()),
                        function: Some(ChatCompletionsStreamFunctionDelta {
                            name: (!name.is_empty()).then_some(name),
                            arguments: emitted_arguments,
                        }),
                        custom: None,
                    }]),
                    refusal: None,
                    reasoning_content: None,
                    reasoning_details: None,
                },
                None,
                None,
            ))
        }
        OutputItem::Message { role, .. } => {
            if role != MessageRole::Assistant {
                accum.ctx.warn(
                    "role",
                    WarningAction::Dropped,
                    "non-assistant output message role is not valid in Chat Completions streaming",
                );
            }
            Ok(vec![])
        }
        OutputItem::CustomToolCall {
            id,
            call_id,
            name,
            namespace,
            input,
            ..
        } => {
            let name = flatten_tool_name(namespace.as_deref(), name);
            accum.saw_function_call = true;
            let emitted_input =
                accum.inline_tool_call_arguments_to_emit(&id, input, "custom_tool_call.input");
            if let Some(input) = emitted_input.as_deref() {
                accum.record_emitted_tool_call_arguments(&id, input);
            }
            let index = accum.get_or_create_tool_call_index(&id);
            Ok(emit_delta_chunk(
                accum,
                ChatCompletionsStreamDelta {
                    role: None,
                    content: None,
                    tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                        index,
                        id: (!call_id.is_empty()).then_some(call_id),
                        kind: Some("custom".into()),
                        function: None,
                        custom: Some(ChatCompletionsStreamCustomDelta {
                            name: (!name.is_empty()).then_some(name),
                            input: emitted_input,
                        }),
                    }]),
                    refusal: None,
                    reasoning_content: None,
                    reasoning_details: None,
                },
                None,
                None,
            ))
        }
        OutputItem::FunctionCallOutput { .. } => {
            accum.ctx.warn(
                "function_call_output",
                WarningAction::Dropped,
                "not valid in Chat Completions streaming output",
            );
            Ok(vec![])
        }
        OutputItem::CustomToolCallOutput { .. } => {
            accum.ctx.warn(
                "custom_tool_call_output",
                WarningAction::Dropped,
                "not valid in Chat Completions streaming output",
            );
            Ok(vec![])
        }
        OutputItem::Reasoning { .. } => Ok(vec![]),
        OutputItem::WebSearchCall { .. } => {
            accum.ctx.warn(
                "web_search_call",
                WarningAction::Dropped,
                "not supported in Chat Completions streaming",
            );
            Ok(vec![])
        }
        OutputItem::ToolSearchCall { .. } => {
            accum.ctx.warn(
                "tool_search_call",
                WarningAction::Dropped,
                "not supported in Chat Completions streaming",
            );
            Ok(vec![])
        }
        OutputItem::ToolSearchOutput { .. } => {
            accum.ctx.warn(
                "tool_search_output",
                WarningAction::Dropped,
                "not supported in Chat Completions streaming",
            );
            Ok(vec![])
        }
        OutputItem::Unknown => {
            accum.ctx.warn(
                "output_item.type",
                WarningAction::Dropped,
                "unknown Open Responses output item dropped",
            );
            Ok(vec![])
        }
    }
}

fn handle_terminal(
    accum: &mut OpenResponsesToChatCompletionsAccum,
    status: ResponseStatus,
    output: Vec<OutputItem>,
    usage: Option<Usage>,
    error: Option<OpenResponsesError>,
) -> Vec<ChatCompletionsStreamChunk> {
    let finish_reason = if accum.saw_function_call && matches!(status, ResponseStatus::Completed) {
        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ToolCalls
    } else if matches!(status, ResponseStatus::Failed)
        && matches!(error.as_ref(), Some(error) if error.code == ERROR_CODE_CONTENT_FILTER)
    {
        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ContentFilter
    } else {
        open_responses_status_to_chat_completions_finish_reason(status, &output)
            .unwrap_or(crate::chat_completions_openai::types::ChatCompletionsFinishReason::Stop)
    };

    let mut chunks = emit_delta_chunk(
        accum,
        ChatCompletionsStreamDelta {
            role: None,
            content: None,
            tool_calls: None,
            refusal: None,
            reasoning_content: None,
            reasoning_details: None,
        },
        Some(finish_reason),
        None,
    );

    if let Some(usage) = usage {
        chunks.push(ChatCompletionsStreamChunk {
            id: accum.response_id.clone(),
            object: "chat.completion.chunk".into(),
            created: accum.created,
            model: accum.model.clone(),
            choices: vec![],
            usage: Some(usage.into()),
            system_fingerprint: None,
            service_tier: accum.service_tier.clone(),
            obfuscation: None,
        });
    }

    chunks
}

fn emit_delta_chunk(
    accum: &mut OpenResponsesToChatCompletionsAccum,
    delta: ChatCompletionsStreamDelta,
    finish_reason: Option<crate::chat_completions_openai::types::ChatCompletionsFinishReason>,
    obfuscation: Option<String>,
) -> Vec<ChatCompletionsStreamChunk> {
    warn_if_response_header_missing(accum);

    let mut chunks = Vec::new();

    if !accum.role_prelude_emitted {
        accum.role_prelude_emitted = true;
        chunks.push(ChatCompletionsStreamChunk {
            id: accum.response_id.clone(),
            object: "chat.completion.chunk".into(),
            created: accum.created,
            model: accum.model.clone(),
            choices: vec![ChatCompletionsStreamChoice {
                index: 0,
                delta: ChatCompletionsStreamDelta {
                    role: Some("assistant".into()),
                    content: None,
                    tool_calls: None,
                    refusal: None,
                    reasoning_content: None,
                    reasoning_details: None,
                },
                finish_reason: None,
                logprobs: None,
            }],
            usage: None,
            system_fingerprint: None,
            service_tier: accum.service_tier.clone(),
            obfuscation: None,
        });
    }

    chunks.push(ChatCompletionsStreamChunk {
        id: accum.response_id.clone(),
        object: "chat.completion.chunk".into(),
        created: accum.created,
        model: accum.model.clone(),
        choices: vec![ChatCompletionsStreamChoice {
            index: 0,
            delta,
            finish_reason,
            logprobs: None,
        }],
        usage: None,
        system_fingerprint: None,
        service_tier: accum.service_tier.clone(),
        obfuscation,
    });

    chunks
}

fn warn_if_response_header_missing(accum: &mut OpenResponsesToChatCompletionsAccum) {
    if accum.warned_missing_response_header || accum.saw_response_header {
        return;
    }

    accum.warned_missing_response_header = true;
    accum.ctx.warn(
        "response",
        WarningAction::Dropped,
        "emitting Chat Completions stream chunk before response header was observed; id/model/created may be unset",
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unknown_event_is_dropped_with_warning() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        let events = stream
            .transform(OpenResponsesStreamEvent::Unknown)
            .expect("ok");
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
    fn role_prelude_emitted_once() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let first = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: "hello".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(first.len(), 2);

        let second = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 2,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: " world".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(second.len(), 1);
    }

    #[test]
    fn function_call_added_preserves_inline_arguments() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::FunctionCall {
                    id: "fc_1".into(),
                    call_id: "call_1".into(),
                    name: "lookup".into(),
                    namespace: None,
                    arguments: "{\"q\":\"x\"}".into(),
                    status: ItemStatus::InProgress,
                },
            })
            .expect("ok");

        let tool_calls = out
            .last()
            .expect("delta chunk")
            .choices
            .first()
            .expect("choice")
            .delta
            .tool_calls
            .as_ref()
            .expect("tool_calls");
        let function = tool_calls[0].function.as_ref().expect("function");
        assert_eq!(function.arguments.as_deref(), Some("{\"q\":\"x\"}"));
    }

    #[test]
    fn function_call_added_preserves_empty_inline_arguments() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 1,
                output_index: 0,
                item: OutputItem::FunctionCall {
                    id: "fc_1".into(),
                    call_id: "call_1".into(),
                    name: "lookup".into(),
                    namespace: None,
                    arguments: String::new(),
                    status: ItemStatus::InProgress,
                },
            })
            .expect("ok");

        let tool_calls = out
            .last()
            .expect("delta chunk")
            .choices
            .first()
            .expect("choice")
            .delta
            .tool_calls
            .as_ref()
            .expect("tool_calls");
        let function = tool_calls[0].function.as_ref().expect("function");
        assert_eq!(function.arguments.as_deref(), Some(""));
    }

    #[test]
    fn failed_content_filter_response_maps_to_content_filter_finish_reason() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        let chunks = stream
            .transform(OpenResponsesStreamEvent::ResponseFailed {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::Failed,
                    model: "gpt-5".into(),
                    output: vec![],
                    error: Some(OpenResponsesError {
                        code: "content_filter".into(),
                        message: "blocked".into(),
                    }),
                    ..Default::default()
                },
            })
            .expect("ok");

        assert_eq!(chunks.len(), 2);
        assert!(matches!(
            chunks[1].choices[0].finish_reason,
            Some(crate::chat_completions_openai::types::ChatCompletionsFinishReason::ContentFilter)
        ));
    }

    #[test]
    fn flush_without_terminal_event_emits_no_synthetic_chunk_and_warns() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let flushed = stream.flush().expect("ok");
        assert!(flushed.is_empty());

        let warnings = stream.take_warnings();
        assert!(warnings.iter().any(|warning| {
            warning.field == "response"
                && warning
                    .message
                    .contains("stream ended without terminal Open Responses event")
        }));
    }

    #[test]
    fn function_call_arguments_delta_without_prelude_warns() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
                sequence_number: 1,
                item_id: "fc_1".into(),
                output_index: 0,
                delta: "{\"q\":\"x\"}".into(),
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(out.len(), 2);

        let warnings = stream.take_warnings();
        assert!(warnings.iter().any(|warning| {
            warning.field == "function_call_arguments.item_id"
                && warning.message.contains("arrived before tool-call prelude")
        }));
    }

    #[test]
    fn function_call_added_after_arguments_delta_does_not_duplicate_inline_arguments() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let delta_out = stream
            .transform(OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
                sequence_number: 1,
                item_id: "fc_1".into(),
                output_index: 0,
                delta: "{\"q\":\"x\"}".into(),
                obfuscation: None,
            })
            .expect("ok");
        let delta_function = delta_out
            .last()
            .expect("delta chunk")
            .choices
            .first()
            .expect("choice")
            .delta
            .tool_calls
            .as_ref()
            .expect("tool_calls")[0]
            .function
            .as_ref()
            .expect("function")
            .clone();
        assert_eq!(delta_function.arguments.as_deref(), Some("{\"q\":\"x\"}"));

        let added_out = stream
            .transform(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: 2,
                output_index: 0,
                item: OutputItem::FunctionCall {
                    id: "fc_1".into(),
                    call_id: "call_1".into(),
                    name: "lookup".into(),
                    namespace: None,
                    arguments: "{\"q\":\"x\"}".into(),
                    status: ItemStatus::InProgress,
                },
            })
            .expect("ok");

        let added_function = added_out
            .last()
            .expect("delta chunk")
            .choices
            .first()
            .expect("choice")
            .delta
            .tool_calls
            .as_ref()
            .expect("tool_calls")[0]
            .function
            .as_ref()
            .expect("function")
            .clone();
        assert_eq!(added_function.name.as_deref(), Some("lookup"));
        assert_eq!(added_function.arguments, None);
    }

    #[test]
    fn created_at_zero_in_response_header_does_not_trigger_missing_header_warning() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 0,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: "hello".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(out[0].created, 0);
        assert_eq!(out[1].created, 0);

        let warnings = stream.take_warnings();
        assert!(!warnings.iter().any(|warning| {
            warning.field == "response"
                && warning
                    .message
                    .contains("before response header was observed")
        }));
    }

    #[test]
    fn delta_before_response_header_warns_once() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();

        let first = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 0,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: "hello".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(first.len(), 2);

        let second = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: " world".into(),
                logprobs: vec![],
                obfuscation: None,
            })
            .expect("ok");
        assert_eq!(second.len(), 1);

        let warnings = stream.take_warnings();
        let header_warnings: Vec<_> = warnings
            .iter()
            .filter(|warning| warning.field == "response")
            .collect();
        assert_eq!(header_warnings.len(), 1);
        assert!(
            header_warnings[0]
                .message
                .contains("before response header was observed")
        );
    }

    #[test]
    fn service_tier_and_obfuscation_are_preserved_on_emitted_chunks() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 1,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    service_tier: Some(ServiceTier::Auto),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: 1,
                item_id: "msg_0".into(),
                output_index: 0,
                content_index: 0,
                delta: "hello".into(),
                logprobs: vec![],
                obfuscation: Some("abc123".into()),
            })
            .expect("ok");

        assert_eq!(out[0].service_tier.as_deref(), Some("auto"));
        assert_eq!(out[0].obfuscation, None);
        assert_eq!(out[1].service_tier.as_deref(), Some("auto"));
        assert_eq!(out[1].obfuscation.as_deref(), Some("abc123"));
    }

    #[test]
    fn keepalive_is_dropped() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        let out = stream
            .transform(OpenResponsesStreamEvent::Keepalive {
                sequence_number: 42,
            })
            .expect("ok");
        assert!(out.is_empty());
    }

    #[test]
    fn error_event_emits_finish_reason_error_and_warning() {
        let mut stream = OpenResponsesToChatCompletionsStream::new();
        // Seed a response header so the emitted chunk has a stable id/model.
        stream
            .transform(OpenResponsesStreamEvent::ResponseCreated {
                sequence_number: 0,
                response: crate::open_responses::response::OpenResponsesResponse {
                    id: "resp_1".into(),
                    object: "response".into(),
                    created_at: 42,
                    status: ResponseStatus::InProgress,
                    model: "gpt-5".into(),
                    ..Default::default()
                },
            })
            .expect("ok");

        let out = stream
            .transform(OpenResponsesStreamEvent::Error {
                sequence_number: 5,
                code: Some("server_error".into()),
                message: "boom".into(),
                param: None,
            })
            .expect("ok");

        // Expect exactly one terminal chunk with finish_reason="error".
        let terminal = out
            .iter()
            .find(|c| {
                c.choices
                    .first()
                    .and_then(|choice| choice.finish_reason.clone())
                    .is_some()
            })
            .expect("terminal chunk emitted");
        assert_eq!(terminal.id, "resp_1");
        assert_eq!(terminal.model, "gpt-5");
        assert_eq!(
            terminal.choices[0].finish_reason,
            Some(crate::chat_completions_openai::types::ChatCompletionsFinishReason::Error),
        );

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "error");
        assert!(warnings[0].message.contains("server_error"));
        assert!(warnings[0].message.contains("boom"));
    }
}
