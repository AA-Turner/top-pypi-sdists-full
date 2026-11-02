use crate::chat_completions_openai::convert::mapping::{
    chat_completions_finish_reason_to_open_responses_status,
    warn_dropped_chat_completions_usage_details,
};
use crate::chat_completions_openai::response::{
    ChatCompletionsChoice, ChatCompletionsOpenAiResponse,
};
use crate::chat_completions_openai::types::*;
use crate::config::ConversionConfig;
use crate::convert::ctx::ConversionCtx;
use crate::convert::open_responses_id::{OpenResponsesOutputItemKind, output_item_id};
use crate::convert::tool_namespace::split_tool_name;
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::types::*;
use crate::traits::IntoOpenResponses;

type Ctx = ConversionCtx<()>;

impl IntoOpenResponses for ChatCompletionsOpenAiResponse {
    type Target = OpenResponsesResponse;

    fn into_open_responses(
        self,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<OpenResponsesResponse>, ConversionError> {
        let mut ctx = Ctx::new();

        let mut choices = self.choices;
        if choices.is_empty() {
            return Err(ConversionError::InvalidInput(
                "chat completions response has no choices".into(),
            ));
        }
        if choices.len() > 1 {
            ctx.warn(
                "choices",
                WarningAction::Dropped,
                "multiple choices are not representable in Open Responses response; only the first choice was used",
            );
        }

        let choice = choices.swap_remove(0);
        if choice.logprobs.is_some() {
            ctx.warn(
                "choices[0].logprobs",
                WarningAction::Dropped,
                "choice-level logprobs are not supported in Open Responses response",
            );
        }

        let (status, incomplete_details) = if choice.finish_reason.is_none() {
            ctx.warn(
                "choices[0].finish_reason",
                WarningAction::Dropped,
                "missing in non-streaming Chat Completions response; emitted response as incomplete",
            );
            (
                ResponseStatus::Incomplete,
                Some(IncompleteDetails {
                    reason: "missing_finish_reason".into(),
                }),
            )
        } else {
            chat_completions_finish_reason_to_open_responses_status(choice.finish_reason.clone())
        };
        let output = convert_choice_to_open_responses_output(&self.id, choice, &mut ctx);
        let usage = self.usage.map(|usage| {
            warn_dropped_chat_completions_usage_details(&usage, &mut ctx, "usage");
            usage.into()
        });

        let mut result = ConversionResult::with_warnings(
            OpenResponsesResponse {
                id: self.id,
                object: "response".into(),
                created_at: self.created,
                status,
                model: self.model,
                output,
                incomplete_details,
                usage,
                service_tier: self
                    .service_tier
                    .and_then(|tier| convert_service_tier_to_open_responses(tier, &mut ctx)),
                ..Default::default()
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Open Responses",
            &[("system_fingerprint", self.system_fingerprint.is_some())],
        );

        Ok(result)
    }
}

fn convert_choice_to_open_responses_output(
    response_id: &str,
    choice: ChatCompletionsChoice,
    ctx: &mut Ctx,
) -> Vec<OutputItem> {
    let mut output = Vec::new();

    let ChatCompletionsChoice { message, .. } = choice;

    let encrypted_content = message.reasoning_details.as_ref().and_then(|details| {
        details
            .iter()
            .filter(|detail| detail["type"] == "reasoning.encrypted")
            .find_map(|detail| {
                detail["data"]
                    .as_str()
                    .or_else(|| detail["encrypted_content"].as_str())
            })
            .map(str::to_owned)
    });
    if encrypted_content.is_none()
        && message
            .reasoning_details
            .as_ref()
            .is_some_and(|details| !details.is_empty())
    {
        ctx.warn(
            "choices[0].message.reasoning_details",
            WarningAction::Dropped,
            "reasoning_details without a supported reasoning.encrypted carrier are not representable in Open Responses",
        );
    }
    let reasoning_content = message.reasoning_content.filter(|text| !text.is_empty());
    if reasoning_content.is_some() || encrypted_content.is_some() {
        let id = output_item_id(
            response_id,
            OpenResponsesOutputItemKind::Reasoning,
            u64::try_from(output.len()).expect("output item count fits in u64"),
            None,
        );
        output.push(OutputItem::Reasoning {
            id,
            summary: reasoning_content
                .map(|text| ContentPart::SummaryText { text })
                .into_iter()
                .collect(),
            content: None,
            encrypted_content,
        });
    }

    let mut message_parts = Vec::new();

    if message.role != "assistant" {
        ctx.warn(
            "choices[0].message.role",
            WarningAction::Changed,
            "non-assistant response role is not valid for Open Responses output and was coerced to assistant",
        );
    }

    if let Some(content) = message.content {
        message_parts.push(ContentPart::OutputText {
            text: content,
            annotations: message
                .annotations
                .into_iter()
                .map(convert_chat_completions_annotation_to_open_responses)
                .collect(),
            logprobs: vec![],
        });
    } else if !message.annotations.is_empty() {
        ctx.warn(
            "choices[0].message.annotations",
            WarningAction::Dropped,
            "annotations without message content are not representable in Open Responses response",
        );
    }

    if let Some(refusal) = message.refusal {
        message_parts.push(ContentPart::Refusal { refusal });
    }

    if !message_parts.is_empty() {
        let id = output_item_id(
            response_id,
            OpenResponsesOutputItemKind::Message,
            u64::try_from(output.len()).expect("output item count fits in u64"),
            None,
        );
        output.push(OutputItem::Message {
            id,
            status: ItemStatus::Completed,
            role: MessageRole::Assistant,
            content: message_parts,
        });
    }

    if let Some(tool_calls) = message.tool_calls {
        for (i, tool_call) in tool_calls.into_iter().enumerate() {
            ctx.push(format!("choices[0].message.tool_calls[{i}]"));
            if let Some(item) = convert_chat_completions_tool_call_to_open_responses(
                response_id,
                tool_call,
                output.len(),
                ctx,
            ) {
                output.push(item);
            }
            ctx.pop();
        }
    }

    if message.audio.is_some() {
        ctx.warn(
            "choices[0].message.audio",
            WarningAction::Dropped,
            "audio output is not supported in Open Responses response",
        );
    }

    output
}

fn convert_chat_completions_tool_call_to_open_responses(
    response_id: &str,
    tool_call: ChatCompletionsToolCall,
    output_index: usize,
    _ctx: &mut Ctx,
) -> Option<OutputItem> {
    match tool_call {
        ChatCompletionsToolCall::Function { id, function } => {
            let source_hint = (!id.is_empty()).then_some(id.as_str());
            let (namespace, name) = split_tool_name(function.name);
            Some(OutputItem::FunctionCall {
                id: output_item_id(
                    response_id,
                    OpenResponsesOutputItemKind::FunctionCall,
                    u64::try_from(output_index).expect("output index fits in u64"),
                    source_hint,
                ),
                call_id: id,
                name,
                namespace,
                arguments: function.arguments,
                status: ItemStatus::Completed,
            })
        }
        ChatCompletionsToolCall::Custom { id, custom } => {
            let source_hint = (!id.is_empty()).then_some(id.as_str());
            let (namespace, name) = split_tool_name(custom.name);
            Some(OutputItem::CustomToolCall {
                id: output_item_id(
                    response_id,
                    OpenResponsesOutputItemKind::CustomToolCall,
                    u64::try_from(output_index).expect("output index fits in u64"),
                    source_hint,
                ),
                call_id: id,
                name,
                namespace,
                input: custom.input,
                status: ItemStatus::Completed,
            })
        }
    }
}

fn convert_chat_completions_annotation_to_open_responses(
    ann: ChatCompletionsAnnotation,
) -> Annotation {
    match ann {
        ChatCompletionsAnnotation::UrlCitation { url_citation } => Annotation::UrlCitation {
            url: url_citation.url,
            title: url_citation.title,
            start_index: url_citation.start_index,
            end_index: url_citation.end_index,
        },
    }
}

fn convert_service_tier_to_open_responses(tier: String, ctx: &mut Ctx) -> Option<ServiceTier> {
    match tier.as_str() {
        "auto" => Some(ServiceTier::Auto),
        "default" => Some(ServiceTier::Default),
        "flex" => Some(ServiceTier::Flex),
        "priority" => Some(ServiceTier::Priority),
        "scale" => {
            ctx.warn(
                "service_tier",
                WarningAction::Changed,
                "service_tier=scale is not available in Open Responses and was mapped to priority",
            );
            Some(ServiceTier::Priority)
        }
        _ => {
            ctx.warn(
                "service_tier",
                WarningAction::Dropped,
                format!("unknown service_tier '{tier}'"),
            );
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn missing_finish_reason_maps_to_incomplete_with_warning() {
        let converted = ChatCompletionsOpenAiResponse {
            id: "chatcmpl_1".into(),
            object: "chat.completion".into(),
            created: 1,
            model: "gpt-4o".into(),
            choices: vec![ChatCompletionsChoice {
                index: 0,
                message:
                    crate::chat_completions_openai::response::ChatCompletionsAssistantMessage {
                        role: "assistant".into(),
                        content: Some("still generating".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                        annotations: vec![],
                        audio: None,
                    },
                finish_reason: None,
                logprobs: None,
            }],
            usage: None,
            system_fingerprint: None,
            service_tier: None,
        }
        .into_open_responses(None)
        .expect("conversion should succeed");

        assert_eq!(converted.value.status, ResponseStatus::Incomplete);
        assert_eq!(
            converted
                .value
                .incomplete_details
                .as_ref()
                .map(|details| details.reason.as_str()),
            Some("missing_finish_reason")
        );
        assert_eq!(converted.warnings.len(), 1);
        assert_eq!(converted.warnings[0].field, "choices[0].finish_reason");
    }

    #[test]
    fn synthesized_open_responses_serializes_nullable_required_fields() {
        let converted = ChatCompletionsOpenAiResponse {
            id: "chatcmpl_1".into(),
            object: "chat.completion".into(),
            created: 1,
            model: "gpt-4o".into(),
            choices: vec![ChatCompletionsChoice {
                index: 0,
                message:
                    crate::chat_completions_openai::response::ChatCompletionsAssistantMessage {
                        role: "assistant".into(),
                        content: Some("ok".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                        annotations: vec![],
                        audio: None,
                    },
                finish_reason: Some(ChatCompletionsFinishReason::Stop),
                logprobs: None,
            }],
            usage: Some(ChatCompletionsUsage {
                prompt_tokens: 1,
                completion_tokens: 2,
                total_tokens: 3,
                prompt_tokens_details: None,
                completion_tokens_details: None,
            }),
            system_fingerprint: None,
            service_tier: None,
        }
        .into_open_responses(None)
        .expect("conversion should succeed");

        let json = serde_json::to_value(&converted.value).expect("serialize response");
        for key in [
            "error",
            "incomplete_details",
            "instructions",
            "metadata",
            "previous_response_id",
            "temperature",
            "top_p",
        ] {
            assert_eq!(json.get(key), Some(&serde_json::Value::Null), "{key}");
        }
        assert_eq!(
            json.pointer("/usage/input_tokens_details"),
            Some(&serde_json::json!({"cached_tokens": 0}))
        );
        assert_eq!(
            json.pointer("/usage/output_tokens_details"),
            Some(&serde_json::json!({"reasoning_tokens": 0}))
        );
        assert_eq!(
            json.pointer("/output/0/content/0/logprobs"),
            Some(&serde_json::json!([]))
        );
        assert!(json.get("tools").is_none());
        assert!(json.get("tool_choice").is_none());
        assert!(json.get("parallel_tool_calls").is_none());
    }
}
