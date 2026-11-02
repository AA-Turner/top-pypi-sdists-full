use crate::anthropic::convert::ctx::ConversionCtx;
use crate::anthropic::convert::helpers::*;
use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::types::*;
use crate::config::ConversionConfig;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::tool_namespace::flatten_tool_name;
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::types::*;
use crate::traits::FromOpenResponses;

impl FromOpenResponses for AnthropicResponse {
    type Source = OpenResponsesResponse;

    fn from_open_responses(
        source: OpenResponsesResponse,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self>, ConversionError> {
        match source.status {
            ResponseStatus::Failed => {
                return Err(ConversionError::InvalidInput(
                    "failed Open Responses response cannot be converted to a non-streaming Anthropic response"
                        .into(),
                ));
            }
            ResponseStatus::Queued => {
                return Err(ConversionError::InvalidInput(
                    "queued Open Responses response cannot be converted to a non-streaming Anthropic response"
                        .into(),
                ));
            }
            ResponseStatus::InProgress => {
                return Err(ConversionError::InvalidInput(
                    "in-progress Open Responses response cannot be converted to a non-streaming Anthropic response"
                        .into(),
                ));
            }
            ResponseStatus::Completed | ResponseStatus::Incomplete => {}
        }

        if source.error.is_some() {
            return Err(ConversionError::InvalidInput(
                "Open Responses response error cannot be converted to a non-streaming Anthropic response"
                    .into(),
            ));
        }

        let mut ctx = ConversionCtx::new();

        let stop_reason = convert_open_responses_status_to_anthropic_messages_stop_reason(
            source.status,
            &source.output,
            source.incomplete_details.as_ref(),
        );
        let content = convert_output_items(source.output, &mut ctx);
        let service_tier = source
            .service_tier
            .and_then(|tier| AnthropicServiceTier::lossy_try_from(tier, &mut ctx, "service_tier"));
        // Anthropic has service_tier both at response level and inside usage;
        // OR only has it at response level, so we copy it back into usage.
        let mut usage = if let Some(usage) = source.usage {
            AnthropicUsage::from(usage)
        } else {
            ctx.warn(
                "usage",
                WarningAction::Added,
                "Anthropic response requires usage; synthesized default usage",
            );
            AnthropicUsage::default()
        };
        usage.service_tier = service_tier.clone();

        let mut result = ConversionResult::with_warnings(
            AnthropicResponse {
                id: source.id,
                kind: "message".into(),
                role: AnthropicRole::Assistant,
                model: source.model,
                content,
                stop_reason,
                stop_sequence: None,
                usage,
                container: None,
                service_tier,
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Anthropic",
            &[
                ("incomplete_details", source.incomplete_details.is_some()),
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
            ],
        );

        Ok(result)
    }
}

fn convert_output_items(
    items: Vec<OutputItem>,
    ctx: &mut ConversionCtx,
) -> Vec<AnthropicOutputContentBlock> {
    let mut blocks = Vec::new();

    for (i, item) in items.into_iter().enumerate() {
        ctx.push(format!("output[{i}]"));
        match item {
            OutputItem::Message { role, content, .. } => {
                if role != MessageRole::Assistant {
                    ctx.warn(
                        "role",
                        WarningAction::Dropped,
                        "non-assistant output message role is not valid in Anthropic response",
                    );
                } else {
                    for (j, part) in content.into_iter().enumerate() {
                        ctx.push(format!("content[{j}]"));
                        if let Some(block) = convert_content_part_to_anthropic_messages(part, ctx) {
                            blocks.push(AnthropicOutputContentBlock::Known(block));
                        }
                        ctx.pop();
                    }
                }
            }
            OutputItem::FunctionCall {
                call_id,
                name,
                namespace,
                arguments,
                ..
            } => {
                let name = flatten_tool_name(namespace.as_deref(), name);
                let input = serde_json::from_str(&arguments).unwrap_or_else(|_| {
                    ctx.warn(
                        "arguments",
                        WarningAction::Changed,
                        "malformed JSON arguments, replaced with empty object",
                    );
                    serde_json::Value::Object(Default::default())
                });
                blocks.push(AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::ToolUse {
                        id: call_id,
                        name,
                        input,
                    },
                ));
            }
            OutputItem::Reasoning {
                summary,
                encrypted_content,
                ..
            } => {
                if let Some(block) =
                    convert_reasoning_to_anthropic_messages_block(summary, encrypted_content, ctx)
                {
                    blocks.push(AnthropicOutputContentBlock::Known(block));
                }
            }
            OutputItem::CustomToolCall { .. } => {
                ctx.warn(
                    "custom_tool_call",
                    WarningAction::Dropped,
                    "custom tool calls are not supported in Anthropic",
                );
            }
            OutputItem::FunctionCallOutput { .. } => {
                ctx.warn(
                    "function_call_output",
                    WarningAction::Dropped,
                    "not valid in Anthropic response output",
                );
            }
            OutputItem::CustomToolCallOutput { .. } => {
                ctx.warn(
                    "custom_tool_call_output",
                    WarningAction::Dropped,
                    "not valid in Anthropic response output",
                );
            }
            OutputItem::ToolSearchCall { .. } => {
                ctx.warn(
                    "tool_search_call",
                    WarningAction::Dropped,
                    "tool_search_call is not supported in Anthropic response",
                );
            }
            OutputItem::ToolSearchOutput { .. } => {
                ctx.warn(
                    "tool_search_output",
                    WarningAction::Dropped,
                    "tool_search_output is not supported in Anthropic response",
                );
            }
            OutputItem::WebSearchCall { id, status, action } => {
                let query = action
                    .as_ref()
                    .and_then(|a| match a {
                        WebSearchAction::Search { query, .. } => query.clone(),
                        _ => None,
                    })
                    .unwrap_or_default();

                blocks.push(AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::ServerToolUse {
                        id: id.clone(),
                        name: ctx.config.web_search_name.into(),
                        input: serde_json::json!({ "query": query }),
                        caller: None,
                    },
                ));

                let content = if matches!(status, WebSearchCallStatus::Failed) {
                    vec![AnthropicWebSearchToolResultItem::Error {
                        error_code: "unavailable".into(),
                    }]
                } else {
                    match action {
                        Some(WebSearchAction::Search { sources, .. }) => sources
                            .into_iter()
                            .map(|s| AnthropicWebSearchToolResultItem::WebSearchResult {
                                url: s.url,
                                title: String::new(),
                                encrypted_content: String::new(),
                                page_age: None,
                            })
                            .collect(),
                        _ => vec![],
                    }
                };
                blocks.push(AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::WebSearchToolResult {
                        tool_use_id: id,
                        content,
                    },
                ));
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

    blocks
}

fn convert_content_part_to_anthropic_messages(
    part: ContentPart,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicKnownOutputContentBlock> {
    match part {
        ContentPart::OutputText {
            text, annotations, ..
        } => {
            let citations = annotations
                .into_iter()
                .map(convert_open_responses_annotation_to_anthropic_messages)
                .collect();
            Some(AnthropicKnownOutputContentBlock::Text { text, citations })
        }
        ContentPart::Refusal { refusal } => Some(AnthropicKnownOutputContentBlock::Text {
            text: refusal,
            citations: vec![],
        }),
        ContentPart::InputText { text }
        | ContentPart::Text { text }
        | ContentPart::SummaryText { text }
        | ContentPart::ReasoningText { text } => Some(AnthropicKnownOutputContentBlock::Text {
            text,
            citations: vec![],
        }),
        ContentPart::InputImage { .. } | ContentPart::InputFile { .. } => {
            ctx.warn(
                "content_part",
                WarningAction::Dropped,
                "input-type content in output",
            );
            None
        }
    }
}

/// Non-empty summary → Thinking (signature restored from encrypted_content).
/// Empty summary + encrypted_content → RedactedThinking.
fn convert_reasoning_to_anthropic_messages_block(
    summary: Vec<ContentPart>,
    encrypted_content: Option<String>,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicKnownOutputContentBlock> {
    if !summary.is_empty() {
        let text = summary
            .into_iter()
            .filter_map(|s| match s {
                ContentPart::SummaryText { text } => Some(text),
                ContentPart::Text { text } => Some(text),
                _ => None,
            })
            .collect::<Vec<_>>()
            .join("\n");
        Some(AnthropicKnownOutputContentBlock::Thinking {
            thinking: text,
            signature: encrypted_content.unwrap_or_default(),
        })
    } else if let Some(data) = encrypted_content {
        Some(AnthropicKnownOutputContentBlock::RedactedThinking { data })
    } else {
        ctx.warn("reasoning", WarningAction::Dropped, "empty reasoning item");
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn completed_with_function_call_last_gives_tool_use() {
        let output = vec![OutputItem::FunctionCall {
            id: "fc_0".into(),
            call_id: "call_1".into(),
            name: "f".into(),
            namespace: None,
            arguments: "{}".into(),
            status: ItemStatus::Completed,
        }];
        let reason = convert_open_responses_status_to_anthropic_messages_stop_reason(
            ResponseStatus::Completed,
            &output,
            None,
        );
        assert_eq!(reason, Some(AnthropicStopReason::ToolUse));
    }

    #[test]
    fn completed_without_function_call_gives_end_turn() {
        let output = vec![OutputItem::Message {
            id: "msg_0".into(),
            status: ItemStatus::Completed,
            role: MessageRole::Assistant,
            content: vec![],
        }];
        let reason = convert_open_responses_status_to_anthropic_messages_stop_reason(
            ResponseStatus::Completed,
            &output,
            None,
        );
        assert_eq!(reason, Some(AnthropicStopReason::EndTurn));
    }

    #[test]
    fn failed_open_responses_response_is_rejected() {
        let result = AnthropicResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                status: ResponseStatus::Failed,
                model: "gpt-5".into(),
                ..Default::default()
            },
            None,
        );

        assert!(matches!(
            result,
            Err(ConversionError::InvalidInput(message))
                if message.contains("failed Open Responses response")
        ));
    }

    #[test]
    fn queued_open_responses_response_is_rejected() {
        let result = AnthropicResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                status: ResponseStatus::Queued,
                model: "gpt-5".into(),
                ..Default::default()
            },
            None,
        );

        assert!(matches!(
            result,
            Err(ConversionError::InvalidInput(message))
                if message.contains("queued Open Responses response")
        ));
    }

    #[test]
    fn in_progress_open_responses_response_is_rejected() {
        let result = AnthropicResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                status: ResponseStatus::InProgress,
                model: "gpt-5".into(),
                ..Default::default()
            },
            None,
        );

        assert!(matches!(
            result,
            Err(ConversionError::InvalidInput(message))
                if message.contains("in-progress Open Responses response")
        ));
    }

    #[test]
    fn open_responses_response_error_is_rejected() {
        let result = AnthropicResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                status: ResponseStatus::Completed,
                model: "gpt-5".into(),
                error: Some(OpenResponsesError {
                    code: "server_error".into(),
                    message: "boom".into(),
                }),
                ..Default::default()
            },
            None,
        );

        assert!(matches!(
            result,
            Err(ConversionError::InvalidInput(message))
                if message.contains("response error")
        ));
    }

    #[test]
    fn non_assistant_output_message_is_dropped_with_warning() {
        let mut ctx = ConversionCtx::new();
        let blocks = convert_output_items(
            vec![OutputItem::Message {
                id: "msg_0".into(),
                status: ItemStatus::Completed,
                role: MessageRole::User,
                content: vec![ContentPart::OutputText {
                    text: "hello".into(),
                    annotations: vec![],
                    logprobs: vec![],
                }],
            }],
            &mut ctx,
        );

        assert!(blocks.is_empty());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "output[0].role");
        assert_eq!(
            warnings[0].message,
            "non-assistant output message role is not valid in Anthropic response"
        );
    }

    #[test]
    fn missing_usage_warns_and_synthesizes_default_usage() {
        let result = AnthropicResponse::from_open_responses(
            OpenResponsesResponse {
                id: "resp_1".into(),
                object: "response".into(),
                status: ResponseStatus::Completed,
                model: "gpt-5".into(),
                output: vec![],
                usage: None,
                ..Default::default()
            },
            None,
        )
        .unwrap();

        assert_eq!(result.value.usage, AnthropicUsage::default());
        assert_eq!(result.warnings.len(), 1);
        assert_eq!(result.warnings[0].field, "usage");
        assert_eq!(
            result.warnings[0].message,
            "Anthropic response requires usage; synthesized default usage"
        );
    }
}
