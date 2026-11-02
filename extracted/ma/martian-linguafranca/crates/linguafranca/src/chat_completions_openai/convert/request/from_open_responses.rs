use serde_json::{Map, Value};

use crate::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use crate::chat_completions_openai::types::*;
use crate::config::ConversionConfig;
use crate::convert::ctx::ConversionCtx;
use crate::convert::mapping::map_non_empty_vec_with_ctx_path;
use crate::convert::tool_namespace::{flatten_namespace_tools, flatten_tool_name};
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::request::{OpenResponsesInput, OpenResponsesRequest};
use crate::open_responses::types::*;
use crate::traits::FromOpenResponses;

use super::accum::ChatCompletionsMessageAccum;

type Ctx = ConversionCtx<()>;

impl FromOpenResponses for ChatCompletionsOpenAiRequest {
    type Source = OpenResponsesRequest;

    fn from_open_responses(
        source: OpenResponsesRequest,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self>, ConversionError> {
        let mut ctx = Ctx::new();

        let messages = convert_open_responses_input_to_messages(source.input, &mut ctx);
        let (user, metadata) = convert_open_responses_metadata_to_chat_completions(source.metadata);
        let (logprobs, top_logprobs) = convert_open_responses_include_to_chat_completions_logprobs(
            source.include,
            source.top_logprobs,
            &mut ctx,
        );
        let (response_format, verbosity) =
            convert_open_responses_text_to_chat_completions(source.text, &mut ctx);
        let (reasoning_effort, reasoning) = source.reasoning.map_or((None, None), |r| {
            convert_open_responses_reasoning_to_chat_completions(r)
        });
        let stream_options =
            convert_open_responses_stream_options(source.stream, source.stream_options);
        let mut all_messages = messages;

        if let Some(instructions) = source.instructions {
            all_messages.insert(
                0,
                ChatCompletionsMessage::System {
                    content: ChatCompletionsContent::Text(instructions),
                    name: None,
                },
            );
        }

        let had_tools = source.tools.is_some();
        let had_tool_choice = source.tool_choice.is_some();
        let tools = match source.tools {
            Some(tools) => {
                let v: Vec<_> = flatten_namespace_tools(tools, &mut ctx)?
                    .into_iter()
                    .filter_map(|(field, tool)| {
                        convert_open_responses_tool_to_chat_completions(tool, &mut ctx, &field)
                    })
                    .collect();
                if v.is_empty() { None } else { Some(v) }
            }
            None => None,
        };
        let tool_choice = if had_tools && tools.is_none() {
            // No representable tools remain (e.g. unsupported-only or explicit empty tools)
            if had_tool_choice {
                ctx.warn(
                    "tool_choice",
                    WarningAction::Dropped,
                    "dropped because no representable tools remain after conversion",
                );
            }
            None
        } else {
            source
                .tool_choice
                .and_then(|tc| convert_open_responses_tool_choice_to_chat_completions(tc, &mut ctx))
        };

        let mut result = ConversionResult::with_warnings(
            ChatCompletionsOpenAiRequest {
                model: source.model,
                messages: all_messages,
                temperature: source.temperature,
                top_p: source.top_p,
                frequency_penalty: source.frequency_penalty,
                presence_penalty: source.presence_penalty,
                max_completion_tokens: source.max_output_tokens,
                max_tokens: None,
                stop: None,
                n: None,
                seed: None,
                logit_bias: None,
                logprobs,
                top_logprobs,
                stream: source.stream,
                stream_options,
                tools,
                tool_choice,
                parallel_tool_calls: source.parallel_tool_calls,
                response_format,
                reasoning_effort,
                reasoning,
                user,
                service_tier: source.service_tier.map(convert_open_responses_service_tier),
                store: source.store,
                modalities: None,
                audio: None,
                prediction: None,
                web_search_options: None,
                metadata,
                cache_control: None,
                safety_identifier: source.safety_identifier,
                prompt_cache_key: source.prompt_cache_key,
                prompt_cache_retention: source.prompt_cache_retention,
                verbosity,
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Chat Completions",
            &[
                (
                    "previous_response_id",
                    source.previous_response_id.is_some(),
                ),
                ("max_tool_calls", source.max_tool_calls.is_some()),
                ("truncation", source.truncation.is_some()),
                ("background", source.background.is_some()),
            ],
        );

        Ok(result)
    }
}

fn convert_open_responses_stream_options(
    stream: Option<bool>,
    stream_options: Option<StreamOptions>,
) -> Option<ChatCompletionsStreamOptions> {
    if let Some(options) = stream_options {
        return Some(ChatCompletionsStreamOptions {
            include_usage: Some(true), // Open Responses stream always includes usage.
            include_obfuscation: options.include_obfuscation,
        });
    }
    if matches!(stream, Some(true)) {
        return Some(ChatCompletionsStreamOptions {
            include_usage: Some(true), // Open Responses stream always includes usage.
            include_obfuscation: None,
        });
    }
    None
}

fn convert_open_responses_metadata_to_chat_completions(
    metadata: Option<Metadata>,
) -> (Option<String>, Option<Value>) {
    let Some(mut metadata) = metadata else {
        return (None, None);
    };
    let user = metadata.remove("user");
    if metadata.is_empty() {
        (user, None)
    } else {
        let object = metadata
            .into_iter()
            .map(|(k, v)| (k, Value::String(v)))
            .collect::<Map<String, Value>>();
        (user, Some(Value::Object(object)))
    }
}

fn convert_open_responses_include_to_chat_completions_logprobs(
    include: Option<Vec<Include>>,
    top_logprobs: Option<u64>,
    ctx: &mut Ctx,
) -> (Option<bool>, Option<u8>) {
    let Some(include) = include else {
        if top_logprobs.is_some() {
            ctx.warn(
                "top_logprobs",
                WarningAction::Dropped,
                "top_logprobs requires include=message.output_text.logprobs in Open Responses; dropped",
            );
        }
        return (None, None);
    };
    let mut has_logprobs_include = false;
    for include_entry in include {
        match include_entry {
            Include::Known(known) => match known {
                KnownInclude::MessageOutputTextLogprobs => {
                    has_logprobs_include = true;
                }
                KnownInclude::ReasoningEncryptedContent => {
                    ctx.warn(
                        "include",
                        WarningAction::Dropped,
                        "include value 'reasoning.encrypted_content' is not supported in Chat Completions request",
                    );
                }
            },
            Include::Other(value) => {
                ctx.warn(
                    "include",
                    WarningAction::Dropped,
                    format!("include value '{value}' is not supported in Chat Completions request"),
                );
            }
        }
    }
    if !has_logprobs_include {
        if top_logprobs.is_some() {
            ctx.warn(
                "top_logprobs",
                WarningAction::Dropped,
                "top_logprobs requires include=message.output_text.logprobs in Open Responses; dropped",
            );
        }
        return (None, None);
    }

    let top_logprobs = top_logprobs.map(|n| {
        if n > u8::MAX as u64 {
            ctx.warn(
                "top_logprobs",
                WarningAction::Changed,
                "top_logprobs exceeds Chat Completions type range and was clamped",
            );
            u8::MAX
        } else {
            n as u8
        }
    });
    (Some(true), top_logprobs)
}

fn convert_open_responses_reasoning_to_chat_completions(
    reasoning: ReasoningConfig,
) -> (
    Option<ChatCompletionsReasoningEffort>,
    Option<ChatCompletionsReasoning>,
) {
    let effort = reasoning
        .effort
        .map(convert_open_responses_reasoning_effort);
    let summary = reasoning
        .summary
        .map(convert_open_responses_reasoning_summary);
    if summary.is_none() {
        return (effort, None);
    }
    (
        None,
        Some(ChatCompletionsReasoning::Config(
            ChatCompletionsReasoningConfig { effort, summary },
        )),
    )
}

fn convert_open_responses_reasoning_effort(
    effort: ReasoningEffort,
) -> ChatCompletionsReasoningEffort {
    match effort {
        ReasoningEffort::None => ChatCompletionsReasoningEffort::None,
        ReasoningEffort::Minimal => ChatCompletionsReasoningEffort::Minimal,
        ReasoningEffort::Low => ChatCompletionsReasoningEffort::Low,
        ReasoningEffort::Medium => ChatCompletionsReasoningEffort::Medium,
        ReasoningEffort::High => ChatCompletionsReasoningEffort::High,
        ReasoningEffort::Xhigh => ChatCompletionsReasoningEffort::Xhigh,
        ReasoningEffort::Max => ChatCompletionsReasoningEffort::Max,
    }
}

fn convert_open_responses_reasoning_summary(
    summary: ReasoningSummary,
) -> ChatCompletionsReasoningSummary {
    match summary {
        ReasoningSummary::Auto => ChatCompletionsReasoningSummary::Auto,
        ReasoningSummary::Concise => ChatCompletionsReasoningSummary::Concise,
        ReasoningSummary::Detailed => ChatCompletionsReasoningSummary::Detailed,
    }
}

fn convert_open_responses_text_to_chat_completions(
    text: Option<TextConfig>,
    ctx: &mut Ctx,
) -> (
    Option<ChatCompletionsResponseFormat>,
    Option<ChatCompletionsVerbosity>,
) {
    let Some(text) = text else {
        return (None, None);
    };
    let response_format = text.format.map(|format| match format {
        TextFormat::Text => ChatCompletionsResponseFormat::Text,
        TextFormat::JsonObject => ChatCompletionsResponseFormat::JsonObject,
        TextFormat::JsonSchema {
            name,
            description,
            schema,
            strict,
        } => ChatCompletionsResponseFormat::JsonSchema {
            json_schema: ChatCompletionsJsonSchemaConfig {
                name,
                description,
                schema,
                strict,
            },
        },
    });
    let verbosity = text.verbosity.map(Into::into);
    if response_format.is_none() && verbosity.is_none() {
        ctx.warn("text", WarningAction::Dropped, "empty text config");
    }
    (response_format, verbosity)
}

fn convert_open_responses_service_tier(tier: ServiceTier) -> ChatCompletionsServiceTier {
    tier.into()
}

fn convert_open_responses_tool_to_chat_completions(
    tool: Tool,
    ctx: &mut Ctx,
    field: &str,
) -> Option<ChatCompletionsTool> {
    match tool {
        Tool::Function {
            name,
            description,
            parameters,
            strict,
            ..
        } => Some(ChatCompletionsTool::Function {
            function: ChatCompletionsFunctionDef {
                name,
                description,
                parameters,
                strict,
            },
        }),
        Tool::WebSearch { .. } => {
            ctx.warn(
                field,
                WarningAction::Dropped,
                "web_search is not supported in Chat Completions request",
            );
            None
        }
        Tool::ToolSearch { .. } => {
            ctx.warn(
                field,
                WarningAction::Dropped,
                "tool_search is not supported in Chat Completions request",
            );
            None
        }
        Tool::Namespace { .. } => unreachable!("namespace tools are flattened before conversion"),
        Tool::Custom {
            name,
            description,
            format,
            ..
        } => Some(ChatCompletionsTool::Custom {
            custom: ChatCompletionsCustomToolDef {
                name,
                description,
                format,
            },
        }),
    }
}

fn convert_open_responses_tool_choice_to_chat_completions(
    tc: ToolChoice,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsToolChoice> {
    match tc {
        ToolChoice::Mode(mode) => Some(ChatCompletionsToolChoice::Mode(match mode {
            ToolChoiceMode::None => "none".to_string(),
            ToolChoiceMode::Auto => "auto".to_string(),
            ToolChoiceMode::Required => "required".to_string(),
        })),
        ToolChoice::Specific(SpecificToolChoice::Function { name }) => match name {
            Some(name) => Some(ChatCompletionsToolChoice::Function(
                ChatCompletionsNamedToolChoice {
                    kind: "function".to_string(),
                    function: ChatCompletionsNamedToolChoiceFunction { name },
                },
            )),
            None => {
                ctx.warn(
                    "tool_choice",
                    WarningAction::Dropped,
                    "specific function tool choice is missing name; tool_choice dropped",
                );
                None
            }
        },
        ToolChoice::Specific(SpecificToolChoice::Custom { name }) => Some(
            ChatCompletionsToolChoice::Custom(ChatCompletionsNamedToolChoiceCustom {
                kind: "custom".to_string(),
                custom: ChatCompletionsNamedToolChoiceCustomData { name },
            }),
        ),
        ToolChoice::AllowedTools(allowed) => {
            let tools: Vec<_> = allowed
                .tools
                .into_iter()
                .enumerate()
                .filter_map(|(i, tool)| match tool {
                    SpecificToolChoice::Function { name: Some(name) } => Some(serde_json::json!({
                        "type": "function",
                        "function": { "name": name }
                    })),
                    SpecificToolChoice::Function { name: None } => {
                        let field = format!("tool_choice.allowed_tools[{i}]");
                        ctx.warn(
                            &field,
                            WarningAction::Dropped,
                            "function tool is missing name",
                        );
                        None
                    }
                    SpecificToolChoice::Custom { name } => Some(serde_json::json!({
                        "type": "custom",
                        "custom": { "name": name }
                    })),
                })
                .collect();

            if tools.is_empty() {
                ctx.warn(
                    "tool_choice.allowed_tools",
                    WarningAction::Dropped,
                    "no representable tools remain; tool_choice dropped",
                );
                None
            } else {
                let mode = match allowed.mode {
                    Some(ToolChoiceMode::Required) => "required".to_string(),
                    Some(ToolChoiceMode::Auto) | None => "auto".to_string(),
                    Some(ToolChoiceMode::None) => {
                        ctx.warn(
                            "tool_choice.allowed_tools.mode",
                            WarningAction::Changed,
                            "mode=none is not valid for Chat Completions allowed_tools; defaulted to auto",
                        );
                        "auto".to_string()
                    }
                };

                Some(ChatCompletionsToolChoice::AllowedTools(
                    ChatCompletionsAllowedToolChoice {
                        kind: "allowed_tools".to_string(),
                        allowed_tools: ChatCompletionsAllowedTools { mode, tools },
                    },
                ))
            }
        }
    }
}

fn convert_open_responses_input_to_messages(
    input: OpenResponsesInput,
    ctx: &mut Ctx,
) -> Vec<ChatCompletionsMessage> {
    match input {
        OpenResponsesInput::Text(text) => vec![ChatCompletionsMessage::User {
            content: ChatCompletionsContent::Text(text),
            name: None,
        }],
        OpenResponsesInput::Items(items) => convert_open_responses_items_to_messages(items, ctx),
    }
}

fn warn_if_present_dropped<T>(value: &Option<T>, field: &str, ctx: &mut Ctx) {
    if value.is_some() {
        ctx.warn(
            field,
            WarningAction::Dropped,
            "not supported in Chat Completions request",
        );
    }
}

fn convert_open_responses_items_to_messages(
    items: Vec<InputItem>,
    ctx: &mut Ctx,
) -> Vec<ChatCompletionsMessage> {
    let mut accum = ChatCompletionsMessageAccum::new();

    for (i, item) in items.into_iter().enumerate() {
        ctx.push(format!("input[{i}]"));
        match item {
            InputItem::Message {
                role,
                content,
                id,
                status,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                warn_if_present_dropped(&status, "status", ctx);
                if let Some(message) =
                    convert_open_responses_message_item_to_chat_completions(role, content, ctx)
                {
                    accum.push_message(message);
                }
            }
            InputItem::FunctionCall {
                call_id,
                name,
                namespace,
                arguments,
                id,
                status,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                warn_if_present_dropped(&status, "status", ctx);
                accum.push_function_call(ChatCompletionsToolCall::Function {
                    id: call_id,
                    function: ChatCompletionsFunctionCallData {
                        name: flatten_tool_name(namespace.as_deref(), name),
                        arguments,
                    },
                });
            }
            InputItem::FunctionCallOutput {
                call_id,
                output,
                id,
                status,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                warn_if_present_dropped(&status, "status", ctx);
                if let Some(content) =
                    convert_open_responses_function_call_output_to_chat_completions(output, ctx)
                {
                    accum.push_tool_output(ChatCompletionsMessage::Tool {
                        content,
                        tool_call_id: call_id,
                    });
                }
            }
            InputItem::Reasoning {
                summary,
                id,
                encrypted_content,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                let reasoning_details = encrypted_content.map(|data| {
                    vec![serde_json::json!({
                        "type": "reasoning.encrypted",
                        "data": data,
                        "format": "unknown",
                        "index": 0,
                    })]
                });
                let reasoning_content = summary
                    .into_iter()
                    .map(|s| s.text)
                    .collect::<Vec<_>>()
                    .join("\n");
                if reasoning_content.is_empty() && reasoning_details.is_none() {
                    ctx.warn("reasoning", WarningAction::Dropped, "empty reasoning item");
                } else {
                    accum.push_reasoning(ChatCompletionsMessage::Assistant {
                        content: Some(ChatCompletionsContent::Text(String::new())),
                        name: None,
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: (!reasoning_content.is_empty())
                            .then_some(reasoning_content),
                        reasoning_details,
                    });
                }
            }
            InputItem::CustomToolCall {
                call_id,
                name,
                namespace,
                input,
                id,
                status,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                warn_if_present_dropped(&status, "status", ctx);
                accum.push_function_call(ChatCompletionsToolCall::Custom {
                    id: call_id,
                    custom: ChatCompletionsCustomCallData {
                        name: flatten_tool_name(namespace.as_deref(), name),
                        input,
                    },
                });
            }
            InputItem::CustomToolCallOutput {
                call_id,
                output,
                id,
                status,
            } => {
                warn_if_present_dropped(&id, "id", ctx);
                warn_if_present_dropped(&status, "status", ctx);
                if let Some(content) =
                    convert_open_responses_function_call_output_to_chat_completions(output, ctx)
                {
                    accum.push_tool_output(ChatCompletionsMessage::Tool {
                        content,
                        tool_call_id: call_id,
                    });
                }
            }
            InputItem::WebSearchCall { .. } => {
                ctx.warn(
                    "web_search_call",
                    WarningAction::Dropped,
                    "web_search_call is not supported in Chat Completions request",
                );
            }
            InputItem::ToolSearchCall { .. } => {
                ctx.warn(
                    "tool_search_call",
                    WarningAction::Dropped,
                    "tool_search_call is not supported in Chat Completions request",
                );
            }
            InputItem::ToolSearchOutput { .. } => {
                ctx.warn(
                    "tool_search_output",
                    WarningAction::Dropped,
                    "tool_search_output is not supported in Chat Completions request",
                );
            }
            InputItem::ItemReference { .. } => {
                accum.flush_pending_tool_calls();
                ctx.warn(
                    "item_reference",
                    WarningAction::Dropped,
                    "item_reference is not supported in Chat Completions request",
                );
            }
        }
        ctx.pop();
    }

    accum.finish()
}
fn convert_open_responses_message_item_to_chat_completions(
    role: MessageRole,
    content: InputContent,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsMessage> {
    let content = convert_open_responses_content_to_chat_completions(content, ctx, "content")?;
    match role {
        MessageRole::System => Some(ChatCompletionsMessage::System {
            content,
            name: None,
        }),
        MessageRole::Developer => Some(ChatCompletionsMessage::Developer {
            content,
            name: None,
        }),
        MessageRole::User => Some(ChatCompletionsMessage::User {
            content,
            name: None,
        }),
        MessageRole::Assistant => Some(ChatCompletionsMessage::Assistant {
            content: Some(content),
            name: None,
            tool_calls: None,
            refusal: None,
            reasoning_content: None,
            reasoning_details: None,
        }),
    }
}

fn convert_open_responses_function_call_output_to_chat_completions(
    output: FunctionCallOutputValue,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsContent> {
    match output {
        FunctionCallOutputValue::Text(text) => Some(ChatCompletionsContent::Text(text)),
        FunctionCallOutputValue::Parts(parts) => {
            map_non_empty_vec_with_ctx_path(ctx, "output", parts, convert_or_input_part_to_cc)
                .map(ChatCompletionsContent::Parts)
        }
    }
}

fn convert_open_responses_content_to_chat_completions(
    content: InputContent,
    ctx: &mut Ctx,
    parts_base: &str,
) -> Option<ChatCompletionsContent> {
    match content {
        InputContent::Text(text) => Some(ChatCompletionsContent::Text(text)),
        InputContent::Parts(parts) => {
            map_non_empty_vec_with_ctx_path(ctx, parts_base, parts, convert_or_input_part_to_cc)
                .map(ChatCompletionsContent::Parts)
        }
    }
}

fn convert_or_input_part_to_cc(
    part: InputContentPart,
    ctx: &mut Ctx,
) -> Option<ChatCompletionsContentPart> {
    match part {
        InputContentPart::Text { text } => Some(ChatCompletionsContentPart::Text {
            text,
            cache_control: None,
        }),
        InputContentPart::Image { image_url, detail } => {
            let Some(url) = image_url else {
                ctx.warn(
                    "image_url",
                    WarningAction::Dropped,
                    "missing image_url, content part dropped",
                );
                return None;
            };
            Some(ChatCompletionsContentPart::ImageUrl {
                image_url: ChatCompletionsImageUrl {
                    url,
                    detail: detail.map(Into::into),
                },
            })
        }
        InputContentPart::OutputText {
            text,
            annotations,
            logprobs,
        } => {
            if !annotations.is_empty() {
                ctx.warn(
                    "output_text.annotations",
                    WarningAction::Dropped,
                    "annotations are not representable in Chat Completions",
                );
            }
            if !logprobs.is_empty() {
                ctx.warn(
                    "output_text.logprobs",
                    WarningAction::Dropped,
                    "logprobs are not representable in Chat Completions",
                );
            }
            Some(ChatCompletionsContentPart::Text {
                text,
                cache_control: None,
            })
        }
        InputContentPart::File {
            filename,
            file_data,
            file_url,
        } => {
            if file_url.is_some() {
                ctx.warn(
                    "file_url",
                    WarningAction::Dropped,
                    "file_url is not representable in Chat Completions file content part",
                );
            }
            if file_data.is_none() && file_url.is_some() {
                return None;
            }
            Some(ChatCompletionsContentPart::File {
                file: ChatCompletionsFileData {
                    file_data,
                    file_id: None,
                    filename,
                },
            })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stream_true_without_stream_options_sets_include_usage() {
        let converted = convert_open_responses_stream_options(Some(true), None);
        assert!(matches!(
            converted,
            Some(ChatCompletionsStreamOptions {
                include_usage: Some(true),
                include_obfuscation: None
            })
        ));
    }

    #[test]
    fn stream_options_preserves_include_obfuscation() {
        let converted = convert_open_responses_stream_options(
            Some(true),
            Some(StreamOptions {
                include_obfuscation: Some(true),
            }),
        );
        assert!(matches!(
            converted,
            Some(ChatCompletionsStreamOptions {
                include_usage: Some(true),
                include_obfuscation: Some(true)
            })
        ));
    }

    #[test]
    fn unsupported_tools_warn_and_drop_tool_choice_when_none_remain() {
        let converted = ChatCompletionsOpenAiRequest::from_open_responses(
            OpenResponsesRequest {
                model: "gpt-4o".into(),
                input: OpenResponsesInput::Text("hello".into()),
                tools: Some(vec![
                    Tool::WebSearch {
                        search_context_size: None,
                        user_location: None,
                        filters: None,
                    },
                    Tool::ToolSearch {
                        description: None,
                        execution: None,
                        parameters: None,
                    },
                ]),
                tool_choice: Some(ToolChoice::Mode(ToolChoiceMode::Required)),
                ..Default::default()
            },
            None,
        )
        .expect("conversion should succeed");

        assert!(converted.value.tools.is_none());
        assert!(converted.value.tool_choice.is_none());
        assert_eq!(converted.warnings.len(), 3);
        assert_eq!(converted.warnings[0].field, "tools[0]");
        assert_eq!(converted.warnings[0].action, WarningAction::Dropped);
        assert_eq!(converted.warnings[1].field, "tools[1]");
        assert_eq!(converted.warnings[1].action, WarningAction::Dropped);
        assert_eq!(converted.warnings[2].field, "tool_choice");
        assert_eq!(converted.warnings[2].action, WarningAction::Dropped);
    }

    #[test]
    fn explicit_empty_tools_warn_and_drop_tool_choice() {
        let converted = ChatCompletionsOpenAiRequest::from_open_responses(
            OpenResponsesRequest {
                model: "gpt-4o".into(),
                input: OpenResponsesInput::Text("hello".into()),
                tools: Some(vec![]),
                tool_choice: Some(ToolChoice::Mode(ToolChoiceMode::Auto)),
                ..Default::default()
            },
            None,
        )
        .expect("conversion should succeed");

        assert!(converted.value.tools.is_none());
        assert!(converted.value.tool_choice.is_none());
        assert_eq!(converted.warnings.len(), 1);
        assert_eq!(converted.warnings[0].field, "tool_choice");
        assert_eq!(converted.warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn allowed_tools_without_representable_entries_is_dropped_with_warnings() {
        let mut ctx = Ctx::new();
        let converted = convert_open_responses_tool_choice_to_chat_completions(
            ToolChoice::AllowedTools(AllowedToolChoice {
                kind: "allowed_tools".into(),
                tools: vec![SpecificToolChoice::Function { name: None }],
                mode: Some(ToolChoiceMode::Required),
            }),
            &mut ctx,
        );

        assert!(converted.is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 2);
        assert_eq!(warnings[0].field, "tool_choice.allowed_tools[0]");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
        assert_eq!(warnings[1].field, "tool_choice.allowed_tools");
        assert_eq!(warnings[1].action, WarningAction::Dropped);
    }

    #[test]
    fn allowed_tools_warn_for_invalid_entries_but_keep_valid_ones() {
        let mut ctx = Ctx::new();
        let converted = convert_open_responses_tool_choice_to_chat_completions(
            ToolChoice::AllowedTools(AllowedToolChoice {
                kind: "allowed_tools".into(),
                tools: vec![
                    SpecificToolChoice::Function { name: None },
                    SpecificToolChoice::Custom {
                        name: "custom_lookup".into(),
                    },
                ],
                mode: Some(ToolChoiceMode::Auto),
            }),
            &mut ctx,
        )
        .expect("tool_choice should be preserved");

        let ChatCompletionsToolChoice::AllowedTools(allowed) = converted else {
            panic!("expected allowed_tools tool_choice");
        };
        assert_eq!(allowed.allowed_tools.tools.len(), 1);
        assert_eq!(
            allowed.allowed_tools.tools[0]
                .get("type")
                .and_then(serde_json::Value::as_str),
            Some("custom")
        );
        assert_eq!(
            allowed.allowed_tools.tools[0]
                .get("custom")
                .and_then(|value| value.get("name"))
                .and_then(serde_json::Value::as_str),
            Some("custom_lookup")
        );

        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tool_choice.allowed_tools[0]");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn specific_tool_choice_without_name_is_dropped() {
        let mut ctx = Ctx::new();
        let converted = convert_open_responses_tool_choice_to_chat_completions(
            ToolChoice::Specific(SpecificToolChoice::Function { name: None }),
            &mut ctx,
        );
        assert!(converted.is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tool_choice");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn input_item_id_and_status_are_warned_when_dropped() {
        let mut ctx = Ctx::new();
        let messages = convert_open_responses_items_to_messages(
            vec![
                InputItem::Message {
                    role: MessageRole::User,
                    content: InputContent::Text("hello".into()),
                    id: Some("msg_1".into()),
                    status: Some(ItemStatus::Completed),
                },
                InputItem::FunctionCall {
                    call_id: "call_1".into(),
                    name: "lookup".into(),
                    namespace: None,
                    arguments: "{}".into(),
                    id: Some("fc_1".into()),
                    status: Some(ItemStatus::Completed),
                },
                InputItem::FunctionCallOutput {
                    call_id: "call_1".into(),
                    output: FunctionCallOutputValue::Text("ok".into()),
                    id: Some("fco_1".into()),
                    status: Some(ItemStatus::Completed),
                },
                InputItem::CustomToolCall {
                    call_id: "call_2".into(),
                    name: "custom_lookup".into(),
                    namespace: None,
                    input: "{}".into(),
                    id: Some("ctc_1".into()),
                    status: Some(ItemStatus::Completed),
                },
                InputItem::CustomToolCallOutput {
                    call_id: "call_2".into(),
                    output: FunctionCallOutputValue::Text("done".into()),
                    id: Some("ctco_1".into()),
                    status: Some(ItemStatus::Completed),
                },
            ],
            &mut ctx,
        );

        assert_eq!(messages.len(), 5);
        let warnings = ctx.into_warnings();
        let warning_fields: Vec<_> = warnings
            .iter()
            .map(|warning| warning.field.clone())
            .collect();
        assert!(warnings.iter().all(|w| w.action == WarningAction::Dropped));
        assert_eq!(
            warning_fields,
            vec![
                "input[0].id",
                "input[0].status",
                "input[1].id",
                "input[1].status",
                "input[2].id",
                "input[2].status",
                "input[3].id",
                "input[3].status",
                "input[4].id",
                "input[4].status",
            ]
        );
    }

    #[test]
    fn reasoning_encrypted_content_is_preserved() {
        let mut ctx = Ctx::new();
        let messages = convert_open_responses_items_to_messages(
            vec![InputItem::Reasoning {
                summary: vec![SummaryContent {
                    kind: SummaryContentType::SummaryText,
                    text: "Need intermediate reasoning".into(),
                }],
                id: Some("rs_1".into()),
                encrypted_content: Some("opaque-token".into()),
            }],
            &mut ctx,
        );

        assert!(matches!(
            &messages[0],
            ChatCompletionsMessage::Assistant {
                reasoning_content: Some(text),
                reasoning_details: Some(details),
                ..
            } if text == "Need intermediate reasoning"
                && details == &vec![serde_json::json!({
                    "type": "reasoning.encrypted",
                    "data": "opaque-token",
                    "format": "unknown",
                    "index": 0,
                })]
        ));
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "input[0].id");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn top_logprobs_without_include_is_dropped() {
        let mut ctx = Ctx::new();
        let (logprobs, top_logprobs) =
            convert_open_responses_include_to_chat_completions_logprobs(None, Some(5), &mut ctx);
        assert_eq!(logprobs, None);
        assert_eq!(top_logprobs, None);
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "top_logprobs");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn reasoning_summary_is_preserved_in_top_level_reasoning() {
        let (effort, reasoning) =
            convert_open_responses_reasoning_to_chat_completions(ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Detailed),
            });
        assert_eq!(effort, None);
        assert_eq!(
            reasoning,
            Some(ChatCompletionsReasoning::Config(
                ChatCompletionsReasoningConfig {
                    effort: Some(ChatCompletionsReasoningEffort::Low),
                    summary: Some(ChatCompletionsReasoningSummary::Detailed),
                },
            )),
        );
    }

    #[test]
    fn image_without_url_is_dropped_with_warning() {
        let mut ctx = Ctx::new();
        let out = convert_or_input_part_to_cc(
            InputContentPart::Image {
                image_url: None,
                detail: Some(ImageDetail::Low),
            },
            &mut ctx,
        );
        assert!(out.is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "image_url");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn file_url_without_file_data_is_dropped_with_warning() {
        let mut ctx = Ctx::new();
        let out = convert_or_input_part_to_cc(
            InputContentPart::File {
                filename: Some("a.txt".into()),
                file_data: None,
                file_url: Some("https://example.com/a.txt".into()),
            },
            &mut ctx,
        );
        assert!(out.is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "file_url");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }
}
