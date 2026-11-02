use crate::chat_completions_openai::convert::mapping::open_responses_status_to_chat_completions_finish_reason;
use crate::chat_completions_openai::response::{
    ChatCompletionsAssistantMessage, ChatCompletionsChoice, ChatCompletionsOpenAiResponse,
};
use crate::chat_completions_openai::types::*;
use crate::config::ConversionConfig;
use crate::convert::ctx::ConversionCtx;
use crate::convert::tool_namespace::flatten_tool_name;
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::types::*;
use crate::traits::FromOpenResponses;

type Ctx = ConversionCtx<()>;

impl FromOpenResponses for ChatCompletionsOpenAiResponse {
    type Source = OpenResponsesResponse;

    fn from_open_responses(
        source: OpenResponsesResponse,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self>, ConversionError> {
        let mut ctx = Ctx::new();

        let finish_reason = convert_open_responses_status_to_chat_completions_finish_reason(
            source.status,
            &source.output,
            source.error.as_ref(),
            &mut ctx,
        );
        let message = convert_open_responses_output_to_assistant_message(source.output, &mut ctx);

        let usage = source.usage.map(Into::into);

        let mut result = ConversionResult::with_warnings(
            ChatCompletionsOpenAiResponse {
                id: source.id,
                object: "chat.completion".into(),
                created: source.created_at,
                model: source.model,
                choices: vec![ChatCompletionsChoice {
                    index: 0,
                    message,
                    finish_reason,
                    logprobs: None,
                }],
                usage,
                system_fingerprint: None,
                service_tier: source.service_tier.map(convert_open_responses_service_tier),
            },
            ctx.into_warnings(),
        );

        if source.object != "response" {
            result.warn(
                "object",
                WarningAction::Changed,
                format!("unexpected value '{}', expected 'response'", source.object),
            );
        }

        result.warn_unsupported(
            "Chat Completions",
            &[
                ("completed_at", source.completed_at.is_some()),
                ("incomplete_details", source.incomplete_details.is_some()),
                (
                    "previous_response_id",
                    source.previous_response_id.is_some(),
                ),
                ("instructions", source.instructions.is_some()),
            ],
        );
        warn_open_responses_error_dropped(&mut result, source.status, source.error.as_ref());
        result.warn_unsupported(
            "Chat Completions",
            &[
                ("tools", source.tools.is_some()),
                ("tool_choice", source.tool_choice.is_some()),
                ("truncation", source.truncation.is_some()),
                ("parallel_tool_calls", source.parallel_tool_calls.is_some()),
                ("text", source.text.is_some()),
                ("top_p", source.top_p.is_some()),
                ("presence_penalty", source.presence_penalty.is_some()),
                ("frequency_penalty", source.frequency_penalty.is_some()),
                ("top_logprobs", source.top_logprobs.is_some()),
                ("temperature", source.temperature.is_some()),
                ("reasoning", source.reasoning.is_some()),
                ("max_output_tokens", source.max_output_tokens.is_some()),
                ("max_tool_calls", source.max_tool_calls.is_some()),
                ("store", source.store.is_some()),
                ("background", source.background.is_some()),
                ("metadata", source.metadata.is_some()),
                ("safety_identifier", source.safety_identifier.is_some()),
                ("prompt_cache_key", source.prompt_cache_key.is_some()),
            ],
        );

        Ok(result)
    }
}

fn convert_open_responses_output_to_assistant_message(
    output: Vec<OutputItem>,
    ctx: &mut Ctx,
) -> ChatCompletionsAssistantMessage {
    let mut content = String::new();
    let mut refusal = String::new();
    let mut reasoning_content = String::new();
    let mut tool_calls = Vec::new();
    let mut annotations = Vec::new();

    for (i, item) in output.into_iter().enumerate() {
        ctx.push(format!("output[{i}]"));
        match item {
            OutputItem::Message {
                id: _,
                status: _,
                role,
                content: parts,
            } => {
                if role != MessageRole::Assistant {
                    ctx.warn(
                        "role",
                        WarningAction::Dropped,
                        "non-assistant output message role is not valid in Chat Completions response",
                    );
                    ctx.pop();
                    continue;
                }

                warn_dropped_chat_completions_response_field("id", ctx);
                warn_dropped_chat_completions_response_field("status", ctx);

                for (j, part) in parts.into_iter().enumerate() {
                    ctx.push(format!("content[{j}]"));
                    match part {
                        ContentPart::OutputText {
                            text,
                            annotations: part_annotations,
                            logprobs,
                        } => append_output_text_to_chat_completions_content(
                            text,
                            part_annotations,
                            logprobs,
                            &mut content,
                            &mut annotations,
                            ctx,
                        ),
                        ContentPart::Refusal {
                            refusal: refusal_text,
                        } => {
                            append_joined_text(&mut refusal, &refusal_text);
                        }
                        ContentPart::InputText { .. }
                        | ContentPart::InputImage { .. }
                        | ContentPart::InputFile { .. } => {
                            ctx.warn(
                                "content_part",
                                WarningAction::Dropped,
                                "input-type content in output",
                            );
                        }
                        ContentPart::Text { .. }
                        | ContentPart::SummaryText { .. }
                        | ContentPart::ReasoningText { .. } => {
                            ctx.warn(
                                "content_part",
                                WarningAction::Dropped,
                                "non-output content part in output message is not representable in Chat Completions response",
                            );
                        }
                    }
                    ctx.pop();
                }
            }
            OutputItem::FunctionCall {
                id: _,
                call_id,
                name,
                namespace,
                arguments,
                status: _,
            } => {
                warn_dropped_chat_completions_response_field("id", ctx);
                warn_dropped_chat_completions_response_field("status", ctx);
                tool_calls.push(ChatCompletionsToolCall::Function {
                    id: call_id,
                    function: ChatCompletionsFunctionCallData {
                        name: flatten_tool_name(namespace.as_deref(), name),
                        arguments,
                    },
                });
            }
            OutputItem::Reasoning {
                id: _,
                summary,
                content: reasoning_parts,
                encrypted_content,
            } => {
                warn_dropped_chat_completions_response_field("id", ctx);
                if encrypted_content.is_some() {
                    warn_dropped_chat_completions_response_field("encrypted_content", ctx);
                }
                for (j, part) in summary.into_iter().enumerate() {
                    ctx.push(format!("summary[{j}]"));
                    handle_reasoning_content_part(
                        part,
                        &mut reasoning_content,
                        &mut content,
                        &mut annotations,
                        &mut refusal,
                        ctx,
                    );
                    ctx.pop();
                }
                if let Some(content_parts) = reasoning_parts {
                    for (j, part) in content_parts.into_iter().enumerate() {
                        ctx.push(format!("content[{j}]"));
                        handle_reasoning_content_part(
                            part,
                            &mut reasoning_content,
                            &mut content,
                            &mut annotations,
                            &mut refusal,
                            ctx,
                        );
                        ctx.pop();
                    }
                }
            }
            OutputItem::CustomToolCall {
                id: _,
                call_id,
                name,
                namespace,
                input,
                status: _,
            } => {
                warn_dropped_chat_completions_response_field("id", ctx);
                warn_dropped_chat_completions_response_field("status", ctx);
                tool_calls.push(ChatCompletionsToolCall::Custom {
                    id: call_id,
                    custom: ChatCompletionsCustomCallData {
                        name: flatten_tool_name(namespace.as_deref(), name),
                        input,
                    },
                });
            }
            OutputItem::FunctionCallOutput { .. } => {
                ctx.warn(
                    "function_call_output",
                    WarningAction::Dropped,
                    "not valid in Chat Completions response output",
                );
            }
            OutputItem::CustomToolCallOutput { .. } => {
                ctx.warn(
                    "custom_tool_call_output",
                    WarningAction::Dropped,
                    "not valid in Chat Completions response output",
                );
            }
            OutputItem::WebSearchCall { .. } => {
                ctx.warn(
                    "web_search_call",
                    WarningAction::Dropped,
                    "not supported in Chat Completions response",
                );
            }
            OutputItem::ToolSearchCall { .. } => {
                ctx.warn(
                    "tool_search_call",
                    WarningAction::Dropped,
                    "not supported in Chat Completions response",
                );
            }
            OutputItem::ToolSearchOutput { .. } => {
                ctx.warn(
                    "tool_search_output",
                    WarningAction::Dropped,
                    "not supported in Chat Completions response",
                );
            }
            OutputItem::Unknown => {
                ctx.warn(
                    "type",
                    WarningAction::Dropped,
                    "unknown Open Responses output item dropped",
                );
            }
        }
        ctx.pop();
    }

    ChatCompletionsAssistantMessage {
        role: "assistant".into(),
        content: (!content.is_empty()).then_some(content),
        tool_calls: (!tool_calls.is_empty()).then_some(tool_calls),
        refusal: (!refusal.is_empty()).then_some(refusal),
        reasoning_content: (!reasoning_content.is_empty()).then_some(reasoning_content),
        reasoning_details: None,
        annotations,
        audio: None,
    }
}

fn warn_dropped_chat_completions_response_field(field: &str, ctx: &mut Ctx) {
    ctx.warn(
        field,
        WarningAction::Dropped,
        "not supported in Chat Completions response",
    );
}

fn append_joined_text(accum: &mut String, text: &str) -> u64 {
    if text.is_empty() {
        accum.len() as u64
    } else {
        if !accum.is_empty() {
            accum.push('\n');
        }
        let offset = accum.len() as u64;
        accum.push_str(text);
        offset
    }
}

fn append_output_text_to_chat_completions_content(
    text: String,
    part_annotations: Vec<Annotation>,
    logprobs: Vec<LogProb>,
    content: &mut String,
    annotations: &mut Vec<ChatCompletionsAnnotation>,
    ctx: &mut Ctx,
) {
    if !logprobs.is_empty() {
        ctx.warn(
            "logprobs",
            WarningAction::Dropped,
            "output_text.logprobs is not supported in Chat Completions response",
        );
    }
    let offset = append_joined_text(content, &text);
    for (k, annotation) in part_annotations.into_iter().enumerate() {
        let field = format!("annotations[{k}]");
        if let Some(annotation) =
            convert_open_responses_annotation_to_chat_completions(annotation, offset, &field, ctx)
        {
            annotations.push(annotation);
        }
    }
}

fn handle_reasoning_content_part(
    part: ContentPart,
    reasoning_content: &mut String,
    content: &mut String,
    annotations: &mut Vec<ChatCompletionsAnnotation>,
    refusal: &mut String,
    ctx: &mut Ctx,
) {
    match part {
        ContentPart::SummaryText { text } | ContentPart::ReasoningText { text } => {
            append_joined_text(reasoning_content, &text);
        }
        ContentPart::OutputText {
            text,
            annotations: part_annotations,
            logprobs,
        } => append_output_text_to_chat_completions_content(
            text,
            part_annotations,
            logprobs,
            content,
            annotations,
            ctx,
        ),
        ContentPart::Refusal {
            refusal: refusal_text,
        } => {
            append_joined_text(refusal, &refusal_text);
        }
        ContentPart::InputText { .. }
        | ContentPart::InputImage { .. }
        | ContentPart::InputFile { .. } => {
            ctx.warn(
                "content_part",
                WarningAction::Dropped,
                "input-type content in reasoning",
            );
        }
        ContentPart::Text { .. } => {
            ctx.warn(
                "content_part",
                WarningAction::Dropped,
                "reasoning part is not representable in Chat Completions response",
            );
        }
    }
}

fn warn_open_responses_error_dropped<T>(
    result: &mut ConversionResult<T>,
    status: ResponseStatus,
    error: Option<&OpenResponsesError>,
) {
    if let Some(error) = error {
        let code_mapped_to_finish_reason =
            matches!(status, ResponseStatus::Failed) && error.code == ERROR_CODE_CONTENT_FILTER;
        if !code_mapped_to_finish_reason {
            result.warn(
                "error.code",
                WarningAction::Dropped,
                "not supported in Chat Completions response",
            );
        }
        result.warn(
            "error.message",
            WarningAction::Dropped,
            "not supported in Chat Completions response",
        );
    }
}

fn convert_open_responses_status_to_chat_completions_finish_reason(
    status: ResponseStatus,
    output: &[OutputItem],
    error: Option<&OpenResponsesError>,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsFinishReason> {
    match status {
        ResponseStatus::Completed | ResponseStatus::Incomplete => {
            open_responses_status_to_chat_completions_finish_reason(status, output)
        }
        ResponseStatus::Failed => {
            if matches!(error, Some(error) if error.code == ERROR_CODE_CONTENT_FILTER) {
                Some(ChatCompletionsFinishReason::ContentFilter)
            } else {
                Some(ChatCompletionsFinishReason::Error)
            }
        }
        ResponseStatus::InProgress | ResponseStatus::Queued => {
            ctx.warn(
                "status",
                WarningAction::Dropped,
                "non-terminal Open Responses status in non-streaming response; finish_reason omitted",
            );
            None
        }
    }
}

fn convert_open_responses_annotation_to_chat_completions(
    ann: Annotation,
    offset: u64,
    field: &str,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsAnnotation> {
    match ann {
        Annotation::UrlCitation {
            url,
            title,
            start_index,
            end_index,
        } => {
            let Some(start_index) = start_index.checked_add(offset) else {
                ctx.warn(
                    field,
                    WarningAction::Dropped,
                    "annotation offset overflow after flattening",
                );
                return None;
            };
            let Some(end_index) = end_index.checked_add(offset) else {
                ctx.warn(
                    field,
                    WarningAction::Dropped,
                    "annotation offset overflow after flattening",
                );
                return None;
            };

            Some(ChatCompletionsAnnotation::UrlCitation {
                url_citation: ChatCompletionsUrlCitation {
                    url,
                    title,
                    start_index,
                    end_index,
                },
            })
        }
    }
}

fn convert_open_responses_service_tier(tier: ServiceTier) -> String {
    match tier {
        ServiceTier::Auto => "auto".into(),
        ServiceTier::Default => "default".into(),
        ServiceTier::Flex => "flex".into(),
        ServiceTier::Priority => "priority".into(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn assistant_message_annotations_are_rebased_when_text_parts_are_joined() {
        let mut ctx = Ctx::new();
        let message = convert_open_responses_output_to_assistant_message(
            vec![OutputItem::Message {
                id: "msg_0".into(),
                status: ItemStatus::Completed,
                role: MessageRole::Assistant,
                content: vec![
                    ContentPart::OutputText {
                        text: "first".into(),
                        annotations: vec![Annotation::UrlCitation {
                            url: "https://example.com/a".into(),
                            title: "A".into(),
                            start_index: 0,
                            end_index: 5,
                        }],
                        logprobs: vec![],
                    },
                    ContentPart::OutputText {
                        text: "second".into(),
                        annotations: vec![Annotation::UrlCitation {
                            url: "https://example.com/b".into(),
                            title: "B".into(),
                            start_index: 0,
                            end_index: 6,
                        }],
                        logprobs: vec![],
                    },
                ],
            }],
            &mut ctx,
        );

        assert_eq!(message.content.as_deref(), Some("first\nsecond"));
        assert_eq!(message.annotations.len(), 2);

        let url_citation = match &message.annotations[1] {
            ChatCompletionsAnnotation::UrlCitation { url_citation } => url_citation,
        };
        assert_eq!(url_citation.start_index, 6);
        assert_eq!(url_citation.end_index, 12);

        let warning_fields: Vec<_> = ctx
            .into_warnings()
            .into_iter()
            .map(|warning| warning.field)
            .collect();
        assert_eq!(warning_fields, vec!["output[0].id", "output[0].status"]);
    }

    #[test]
    fn reasoning_encrypted_content_is_warned_when_dropped() {
        let mut ctx = Ctx::new();
        let message = convert_open_responses_output_to_assistant_message(
            vec![OutputItem::Reasoning {
                id: "rs_0".into(),
                summary: vec![],
                content: None,
                encrypted_content: Some("opaque-state".into()),
            }],
            &mut ctx,
        );

        assert!(message.reasoning_content.is_none());
        let warning_fields: Vec<_> = ctx
            .into_warnings()
            .into_iter()
            .map(|warning| warning.field)
            .collect();
        assert_eq!(
            warning_fields,
            vec!["output[0].id", "output[0].encrypted_content"]
        );
    }

    #[test]
    fn failed_content_filter_maps_to_content_filter_finish_reason() {
        let converted = ChatCompletionsOpenAiResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                created_at: 1,
                status: ResponseStatus::Failed,
                model: "gpt-4o".into(),
                output: vec![],
                error: Some(OpenResponsesError {
                    code: "content_filter".into(),
                    message: "blocked".into(),
                }),
                ..Default::default()
            },
            None,
        )
        .expect("conversion should succeed");

        assert!(matches!(
            converted.value.choices[0].finish_reason,
            Some(ChatCompletionsFinishReason::ContentFilter)
        ));
        assert_eq!(converted.warnings.len(), 1);
        assert_eq!(converted.warnings[0].field, "error.message");
    }

    #[test]
    fn output_item_metadata_is_warned_when_dropped() {
        let mut ctx = Ctx::new();
        let message = convert_open_responses_output_to_assistant_message(
            vec![
                OutputItem::Message {
                    id: "msg_0".into(),
                    status: ItemStatus::Completed,
                    role: MessageRole::Assistant,
                    content: vec![ContentPart::OutputText {
                        text: "hello".into(),
                        annotations: vec![],
                        logprobs: vec![],
                    }],
                },
                OutputItem::FunctionCall {
                    id: "fc_item_0".into(),
                    call_id: "call_1".into(),
                    name: "lookup".into(),
                    namespace: None,
                    arguments: "{}".into(),
                    status: ItemStatus::Completed,
                },
                OutputItem::CustomToolCall {
                    id: "ctc_item_0".into(),
                    call_id: "call_2".into(),
                    name: "custom_lookup".into(),
                    namespace: None,
                    input: "{}".into(),
                    status: ItemStatus::Completed,
                },
                OutputItem::Reasoning {
                    id: "rs_0".into(),
                    summary: vec![ContentPart::SummaryText {
                        text: "thinking".into(),
                    }],
                    content: None,
                    encrypted_content: None,
                },
            ],
            &mut ctx,
        );

        assert_eq!(message.content.as_deref(), Some("hello"));
        assert_eq!(message.reasoning_content.as_deref(), Some("thinking"));
        assert_eq!(message.tool_calls.as_ref().map(Vec::len), Some(2));

        let warning_fields: Vec<_> = ctx
            .into_warnings()
            .into_iter()
            .map(|warning| warning.field)
            .collect();
        assert_eq!(
            warning_fields,
            vec![
                "output[0].id",
                "output[0].status",
                "output[1].id",
                "output[1].status",
                "output[2].id",
                "output[2].status",
                "output[3].id",
            ]
        );
    }
}
