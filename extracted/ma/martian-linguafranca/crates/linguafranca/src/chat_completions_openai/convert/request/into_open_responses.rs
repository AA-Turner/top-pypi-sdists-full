use std::collections::HashMap;

use crate::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use crate::chat_completions_openai::types::*;
use crate::config::ConversionConfig;
use crate::convert::ctx::ConversionCtx;
use crate::convert::mapping::{
    LossyTryFromWithCtx, map_non_empty_vec_with_ctx_path, map_vec_with_ctx_path,
};
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::request::{OpenResponsesInput, OpenResponsesRequest};
use crate::open_responses::types::*;
use crate::traits::IntoOpenResponses;

use super::accum::OrInputItemAccum;
use super::web_search;

type Ctx = ConversionCtx<()>;

impl IntoOpenResponses for ChatCompletionsOpenAiRequest {
    type Target = OpenResponsesRequest;

    fn into_open_responses(
        self,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<OpenResponsesRequest>, ConversionError> {
        let mut ctx = Ctx::new();
        let stream_include_usage_present = self
            .stream_options
            .as_ref()
            .is_some_and(|options| options.include_usage.is_some());

        let input_items = convert_messages_to_open_responses_input_items(self.messages, &mut ctx);
        let metadata =
            convert_metadata_and_user_to_open_responses(self.metadata, self.user, &mut ctx);
        let include =
            convert_logprobs_to_open_responses_include(self.logprobs, self.top_logprobs, &mut ctx);

        let tools = convert_chat_completions_tools_to_open_responses(
            self.tools,
            self.web_search_options,
            &mut ctx,
        );

        let mut result = ConversionResult::with_warnings(
            OpenResponsesRequest {
                model: self.model,
                input: OpenResponsesInput::Items(input_items),
                tools,
                tool_choice: self
                    .tool_choice
                    .and_then(|tc| convert_tool_choice_to_open_responses(tc, &mut ctx)),
                temperature: self.temperature,
                top_p: self.top_p,
                frequency_penalty: self.frequency_penalty,
                presence_penalty: self.presence_penalty,
                stream: self.stream,
                stream_options: self.stream_options.map(|options| StreamOptions {
                    include_obfuscation: options.include_obfuscation,
                }),
                parallel_tool_calls: self.parallel_tool_calls,
                max_output_tokens: resolve_max_output_tokens(
                    self.max_completion_tokens,
                    self.max_tokens,
                    &mut ctx,
                ),
                reasoning: convert_reasoning_to_open_responses(
                    self.reasoning,
                    self.reasoning_effort,
                    &mut ctx,
                ),
                text: convert_response_format_and_verbosity_to_open_responses(
                    self.response_format,
                    self.verbosity,
                ),
                include,
                top_logprobs: self.top_logprobs.map(u64::from),
                metadata,
                service_tier: self
                    .service_tier
                    .and_then(|tier| convert_service_tier_to_open_responses(tier, &mut ctx)),
                store: self.store,
                safety_identifier: self.safety_identifier,
                prompt_cache_key: self.prompt_cache_key,
                prompt_cache_retention: self.prompt_cache_retention.clone(),
                ..Default::default()
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Open Responses",
            &[
                ("stop", self.stop.is_some()),
                ("n", self.n.is_some()),
                ("seed", self.seed.is_some()),
                ("logit_bias", self.logit_bias.is_some()),
                ("modalities", self.modalities.is_some()),
                ("audio", self.audio.is_some()),
                ("prediction", self.prediction.is_some()),
                ("cache_control", self.cache_control.is_some()),
            ],
        );
        if stream_include_usage_present {
            result.warn(
                "stream_options.include_usage",
                WarningAction::Dropped,
                "not supported in Open Responses request (usage included by default)",
            );
        }

        Ok(result)
    }
}

fn resolve_max_output_tokens(
    max_completion_tokens: Option<u64>,
    max_tokens: Option<u64>,
    ctx: &mut Ctx,
) -> Option<u64> {
    match (max_completion_tokens, max_tokens) {
        (Some(preferred), Some(deprecated)) => {
            if preferred != deprecated {
                ctx.warn(
                    "max_tokens",
                    WarningAction::Changed,
                    "both max_completion_tokens and max_tokens are set with different values; max_completion_tokens was used",
                );
            }
            Some(preferred)
        }
        (Some(preferred), None) => Some(preferred),
        (None, Some(deprecated)) => Some(deprecated),
        (None, None) => None,
    }
}

fn convert_reasoning_to_open_responses(
    reasoning: Option<ChatCompletionsReasoning>,
    reasoning_effort: Option<ChatCompletionsReasoningEffort>,
    ctx: &mut Ctx,
) -> Option<ReasoningConfig> {
    match reasoning {
        Some(ChatCompletionsReasoning::Config(mut config)) => {
            if let (Some(reasoning_effort), Some(config_effort)) =
                (&reasoning_effort, &config.effort)
                && reasoning_effort != config_effort
            {
                ctx.warn(
                    "reasoning_effort",
                    WarningAction::Changed,
                    "both reasoning.effort and reasoning_effort are set with different values; reasoning.effort was used",
                );
            }
            if config.effort.is_none() {
                config.effort = reasoning_effort;
            }
            convert_reasoning_config_to_open_responses(config, ctx)
        }
        Some(ChatCompletionsReasoning::Enabled(false)) => {
            convert_reasoning_effort_to_open_responses(ChatCompletionsReasoningEffort::None, ctx)
        }
        Some(ChatCompletionsReasoning::Enabled(true)) => {
            ctx.warn(
                "reasoning",
                WarningAction::Dropped,
                "boolean reasoning is not representable in Open Responses request",
            );
            reasoning_effort
                .and_then(|effort| convert_reasoning_effort_to_open_responses(effort, ctx))
        }
        None => reasoning_effort
            .and_then(|effort| convert_reasoning_effort_to_open_responses(effort, ctx)),
    }
}

fn convert_reasoning_config_to_open_responses(
    config: ChatCompletionsReasoningConfig,
    ctx: &mut Ctx,
) -> Option<ReasoningConfig> {
    let effort = config
        .effort
        .and_then(|effort| ReasoningEffort::lossy_try_from(effort, ctx, "reasoning.effort"));
    let summary = config
        .summary
        .map(convert_reasoning_summary_to_open_responses);
    if effort.is_none() && summary.is_none() {
        None
    } else {
        Some(ReasoningConfig { effort, summary })
    }
}

fn convert_reasoning_effort_to_open_responses(
    effort: ChatCompletionsReasoningEffort,
    ctx: &mut Ctx,
) -> Option<ReasoningConfig> {
    ReasoningEffort::lossy_try_from(effort, ctx, "reasoning_effort").map(|effort| ReasoningConfig {
        effort: Some(effort),
        summary: None,
    })
}

fn convert_reasoning_summary_to_open_responses(
    summary: ChatCompletionsReasoningSummary,
) -> ReasoningSummary {
    match summary {
        ChatCompletionsReasoningSummary::Auto => ReasoningSummary::Auto,
        ChatCompletionsReasoningSummary::Concise => ReasoningSummary::Concise,
        ChatCompletionsReasoningSummary::Detailed => ReasoningSummary::Detailed,
    }
}

fn convert_response_format_and_verbosity_to_open_responses(
    response_format: Option<ChatCompletionsResponseFormat>,
    verbosity: Option<ChatCompletionsVerbosity>,
) -> Option<TextConfig> {
    let format = response_format.map(|f| match f {
        ChatCompletionsResponseFormat::Text => TextFormat::Text,
        ChatCompletionsResponseFormat::JsonObject => TextFormat::JsonObject,
        ChatCompletionsResponseFormat::JsonSchema { json_schema } => TextFormat::JsonSchema {
            name: json_schema.name,
            description: json_schema.description,
            schema: json_schema.schema,
            strict: json_schema.strict,
        },
    });

    let verbosity = verbosity.map(Into::into);

    if format.is_none() && verbosity.is_none() {
        None
    } else {
        Some(TextConfig { format, verbosity })
    }
}

fn convert_logprobs_to_open_responses_include(
    logprobs: Option<bool>,
    top_logprobs: Option<u8>,
    ctx: &mut Ctx,
) -> Option<Vec<Include>> {
    let wants_logprobs = matches!(logprobs, Some(true)) || top_logprobs.is_some();
    if matches!(logprobs, Some(false)) && top_logprobs.is_some() {
        ctx.warn(
            "logprobs",
            WarningAction::Changed,
            "logprobs=false with top_logprobs set; normalized to include logprobs",
        );
    }
    if wants_logprobs {
        Some(vec![Include::Known(
            KnownInclude::MessageOutputTextLogprobs,
        )])
    } else {
        None
    }
}

fn convert_service_tier_to_open_responses(
    tier: ChatCompletionsServiceTier,
    ctx: &mut Ctx,
) -> Option<ServiceTier> {
    ServiceTier::lossy_try_from(tier, ctx, "service_tier")
}

fn convert_metadata_and_user_to_open_responses(
    metadata: Option<serde_json::Value>,
    user: Option<String>,
    ctx: &mut Ctx,
) -> Option<Metadata> {
    let mut out: HashMap<String, String> = HashMap::new();

    if let Some(value) = metadata {
        match value {
            serde_json::Value::Object(object) => {
                for (key, value) in object {
                    match value {
                        serde_json::Value::String(s) => {
                            out.insert(key, s);
                        }
                        _ => ctx.warn(
                            "metadata",
                            WarningAction::Dropped,
                            "non-string metadata value dropped (Open Responses metadata values must be strings)",
                        ),
                    }
                }
            }
            _ => ctx.warn(
                "metadata",
                WarningAction::Dropped,
                "metadata must be an object",
            ),
        }
    }

    if let Some(user) = user {
        if let Some(existing) = out.get("user")
            && existing != &user
        {
            ctx.warn(
                "user",
                WarningAction::Changed,
                "user conflicts with metadata.user; user field takes precedence",
            );
        }
        out.insert("user".into(), user);
    }

    if out.is_empty() { None } else { Some(out) }
}

fn convert_chat_completions_tools_to_open_responses(
    tools: Option<Vec<ChatCompletionsTool>>,
    web_search_options: Option<serde_json::Value>,
    ctx: &mut Ctx,
) -> Option<Vec<Tool>> {
    let mut out: Vec<Tool> = tools
        .unwrap_or_default()
        .into_iter()
        .enumerate()
        .filter_map(|(i, tool)| {
            ctx.push(format!("tools[{i}]"));
            let converted = convert_chat_completions_tool_to_open_responses(tool, ctx);
            ctx.pop();
            converted
        })
        .collect();

    if let Some(options) = web_search_options {
        out.push(web_search::convert_options(options, ctx));
    }

    if out.is_empty() { None } else { Some(out) }
}

fn convert_chat_completions_tool_to_open_responses(
    tool: ChatCompletionsTool,
    ctx: &mut Ctx,
) -> Option<Tool> {
    match tool {
        ChatCompletionsTool::Function { function } => Some(Tool::Function {
            name: function.name,
            description: function.description,
            parameters: function.parameters,
            strict: function.strict,
            defer_loading: None,
        }),
        ChatCompletionsTool::Custom { custom } => Some(Tool::Custom {
            name: custom.name,
            description: custom.description,
            format: custom.format,
            defer_loading: None,
        }),
        ChatCompletionsTool::WebSearch {
            search_context_size,
            user_location,
            filters,
            domains,
            search_content_types,
            extra,
        } => Some(web_search::convert_tool(
            web_search::WebSearchToolFields {
                search_context_size,
                user_location,
                filters,
                domains,
                search_content_types,
                extra,
            },
            ctx,
        )),
    }
}

fn convert_tool_choice_to_open_responses(
    tool_choice: ChatCompletionsToolChoice,
    ctx: &mut Ctx,
) -> Option<ToolChoice> {
    match tool_choice {
        ChatCompletionsToolChoice::Mode(mode) => match mode.as_str() {
            "none" => Some(ToolChoice::Mode(ToolChoiceMode::None)),
            "auto" => Some(ToolChoice::Mode(ToolChoiceMode::Auto)),
            "required" => Some(ToolChoice::Mode(ToolChoiceMode::Required)),
            _ => {
                ctx.warn(
                    "tool_choice",
                    WarningAction::Dropped,
                    "unknown tool_choice mode",
                );
                None
            }
        },
        ChatCompletionsToolChoice::Function(f) => {
            Some(ToolChoice::Specific(SpecificToolChoice::Function {
                name: Some(f.function.name),
            }))
        }
        ChatCompletionsToolChoice::Custom(c) => {
            Some(ToolChoice::Specific(SpecificToolChoice::Custom {
                name: c.custom.name,
            }))
        }
        ChatCompletionsToolChoice::AllowedTools(allowed) => {
            let tools: Vec<SpecificToolChoice> = allowed
                .allowed_tools
                .tools
                .into_iter()
                .enumerate()
                .filter_map(|(i, tool)| {
                    let kind = tool.get("type").and_then(|v| v.as_str());
                    match kind {
                        Some("function") => tool
                            .get("function")
                            .and_then(|f| f.get("name"))
                            .and_then(serde_json::Value::as_str)
                            .map(|name| SpecificToolChoice::Function {
                                name: Some(name.to_string()),
                            })
                            .or_else(|| {
                                ctx.warn(
                                    "tool_choice.allowed_tools",
                                    WarningAction::Dropped,
                                    format!("allowed_tools entry at index {i} is missing function name"),
                                );
                                None
                            }),
                        Some("custom") => tool
                            .get("custom")
                            .and_then(|c| c.get("name"))
                            .and_then(serde_json::Value::as_str)
                            .map(|name| SpecificToolChoice::Custom {
                                name: name.to_string(),
                            })
                            .or_else(|| {
                                ctx.warn(
                                    "tool_choice.allowed_tools",
                                    WarningAction::Dropped,
                                    format!("allowed_tools entry at index {i} is missing custom tool name"),
                                );
                                None
                            }),
                        _ => {
                            ctx.warn(
                                "tool_choice.allowed_tools",
                                WarningAction::Dropped,
                                format!("allowed_tools entry at index {i} has unsupported type"),
                            );
                            None
                        }
                    }
                })
                .collect();

            let mode = match allowed.allowed_tools.mode.as_str() {
                "auto" => Some(ToolChoiceMode::Auto),
                "required" => Some(ToolChoiceMode::Required),
                "none" => {
                    ctx.warn(
                        "tool_choice.allowed_tools.mode",
                        WarningAction::Changed,
                        "mode=none is not valid for allowed_tools in Open Responses; defaulted to auto",
                    );
                    Some(ToolChoiceMode::Auto)
                }
                _ => {
                    ctx.warn(
                        "tool_choice.allowed_tools.mode",
                        WarningAction::Changed,
                        "unknown allowed_tools.mode, defaulted to auto",
                    );
                    Some(ToolChoiceMode::Auto)
                }
            };

            Some(ToolChoice::AllowedTools(AllowedToolChoice {
                kind: "allowed_tools".into(),
                tools,
                mode,
            }))
        }
    }
}

fn convert_messages_to_open_responses_input_items(
    messages: Vec<ChatCompletionsMessage>,
    ctx: &mut Ctx,
) -> Vec<InputItem> {
    let mut accum = OrInputItemAccum::new();
    for (i, message) in messages.into_iter().enumerate() {
        ctx.push(format!("messages[{i}]"));
        append_message_to_open_responses_items(message, &mut accum, ctx);
        ctx.pop();
    }
    accum.finish()
}

fn append_message_to_open_responses_items(
    message: ChatCompletionsMessage,
    accum: &mut OrInputItemAccum,
    ctx: &mut Ctx,
) {
    match message {
        ChatCompletionsMessage::System { content, .. } => {
            if let Some(content) =
                convert_content_to_open_responses_input(content, ctx, "content", false)
            {
                accum.push_message(MessageRole::System, content);
            }
        }
        ChatCompletionsMessage::Developer { content, .. } => {
            if let Some(content) =
                convert_content_to_open_responses_input(content, ctx, "content", false)
            {
                accum.push_message(MessageRole::Developer, content);
            }
        }
        ChatCompletionsMessage::User { content, .. } => {
            if let Some(content) =
                convert_content_to_open_responses_input(content, ctx, "content", false)
            {
                accum.push_message(MessageRole::User, content);
            }
        }
        ChatCompletionsMessage::Assistant {
            content,
            tool_calls,
            refusal,
            reasoning_content,
            reasoning_details,
            ..
        } => {
            if let Some(content) = content.and_then(|content| {
                convert_content_to_open_responses_input(content, ctx, "content", true)
            }) {
                accum.push_message(MessageRole::Assistant, content);
            }

            if let Some(refusal) = refusal {
                accum.push_message(MessageRole::Assistant, InputContent::Text(refusal));
                ctx.warn(
                    "messages.assistant.refusal",
                    WarningAction::Changed,
                    "refusal has no dedicated Open Responses input type and was converted to assistant text",
                );
            }

            let encrypted_content = reasoning_details.as_ref().and_then(|details| {
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
                && reasoning_details
                    .as_ref()
                    .is_some_and(|details| !details.is_empty())
            {
                ctx.warn(
                    "reasoning_details",
                    WarningAction::Dropped,
                    "reasoning_details without a supported reasoning.encrypted carrier are not representable in Open Responses",
                );
            }
            if reasoning_content.is_some() || encrypted_content.is_some() {
                accum.push_reasoning(reasoning_content, encrypted_content);
            }

            if let Some(tool_calls) = tool_calls {
                let specs: Vec<ToolCallSpec> =
                    map_vec_with_ctx_path(ctx, "tool_calls", tool_calls, |call, _ctx| {
                        Some(convert_tool_call_to_open_responses(call))
                    });
                for spec in specs {
                    match spec {
                        ToolCallSpec::Function {
                            call_id,
                            name,
                            arguments,
                        } => accum.push_function_call(call_id, name, arguments),
                        ToolCallSpec::Custom {
                            call_id,
                            name,
                            input,
                        } => accum.push_custom_tool_call(call_id, name, input),
                    }
                }
            }
        }
        ChatCompletionsMessage::Tool {
            content,
            tool_call_id,
        } => {
            if let Some(output) = convert_content_to_function_call_output(content, ctx, "content") {
                accum.push_function_call_output(tool_call_id, output);
            } else {
                ctx.warn(
                    "tool",
                    WarningAction::Dropped,
                    "tool message had no representable output content",
                );
            }
        }
    }
}

fn convert_content_to_open_responses_input(
    content: ChatCompletionsContent,
    ctx: &mut Ctx,
    parts_base: &str,
    is_assistant: bool,
) -> Option<InputContent> {
    match content {
        ChatCompletionsContent::Text(text) => Some(InputContent::Text(text)),
        ChatCompletionsContent::Parts(parts) => {
            map_non_empty_vec_with_ctx_path(ctx, parts_base, parts, |part, ctx| {
                convert_cc_content_part_to_or_input(part, ctx, is_assistant)
            })
            .map(InputContent::Parts)
        }
    }
}

fn convert_content_to_function_call_output(
    content: ChatCompletionsContent,
    ctx: &mut Ctx,
    parts_base: &str,
) -> Option<FunctionCallOutputValue> {
    match content {
        ChatCompletionsContent::Text(text) => Some(FunctionCallOutputValue::Text(text)),
        ChatCompletionsContent::Parts(parts) => {
            map_non_empty_vec_with_ctx_path(ctx, parts_base, parts, |part, ctx| {
                convert_cc_content_part_to_or_input(part, ctx, false)
            })
            .map(FunctionCallOutputValue::Parts)
        }
    }
}

enum ToolCallSpec {
    Function {
        call_id: String,
        name: String,
        arguments: String,
    },
    Custom {
        call_id: String,
        name: String,
        input: String,
    },
}

fn convert_tool_call_to_open_responses(call: ChatCompletionsToolCall) -> ToolCallSpec {
    match call {
        ChatCompletionsToolCall::Function { id, function } => ToolCallSpec::Function {
            call_id: id,
            name: function.name,
            arguments: function.arguments,
        },
        ChatCompletionsToolCall::Custom { id, custom } => ToolCallSpec::Custom {
            call_id: id,
            name: custom.name,
            input: custom.input,
        },
    }
}

fn convert_cc_content_part_to_or_input(
    part: ChatCompletionsContentPart,
    ctx: &mut Ctx,
    is_assistant: bool,
) -> Option<InputContentPart> {
    match part {
        ChatCompletionsContentPart::Text { text, .. } => {
            if is_assistant {
                Some(InputContentPart::OutputText {
                    text,
                    annotations: vec![],
                    logprobs: vec![],
                })
            } else {
                Some(InputContentPart::Text { text })
            }
        }
        ChatCompletionsContentPart::ImageUrl { image_url } => {
            let detail = image_url
                .detail
                .and_then(|detail| ImageDetail::lossy_try_from(detail, ctx, "image_url.detail"));
            Some(InputContentPart::Image {
                image_url: Some(image_url.url),
                detail,
            })
        }
        ChatCompletionsContentPart::File { file } => {
            if file.file_id.is_some() {
                if file.file_data.is_none() {
                    ctx.warn(
                        "file.file_id",
                        WarningAction::Dropped,
                        "file_id has no Open Responses request equivalent; part dropped",
                    );
                    return None;
                }
                ctx.warn(
                    "file.file_id",
                    WarningAction::Dropped,
                    "file_id has no Open Responses request equivalent",
                );
            }
            Some(InputContentPart::File {
                filename: file.filename,
                file_data: file.file_data,
                file_url: None,
            })
        }
        ChatCompletionsContentPart::InputAudio { .. } => {
            ctx.warn(
                "input_audio",
                WarningAction::Dropped,
                "audio input content is not supported in Open Responses request",
            );
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn max_tokens_conflict_warns_and_prefers_max_completion_tokens() {
        let mut ctx = Ctx::new();
        let out = resolve_max_output_tokens(Some(100), Some(200), &mut ctx);
        assert_eq!(out, Some(100));
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "max_tokens");
        assert_eq!(warnings[0].action, WarningAction::Changed);
    }

    #[test]
    fn logprobs_false_with_top_logprobs_warns_and_enables_include() {
        let mut ctx = Ctx::new();
        let include = convert_logprobs_to_open_responses_include(Some(false), Some(3), &mut ctx);
        assert_eq!(
            include,
            Some(vec![Include::Known(
                KnownInclude::MessageOutputTextLogprobs
            )])
        );
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "logprobs");
        assert_eq!(warnings[0].action, WarningAction::Changed);
    }

    #[test]
    fn boolean_false_reasoning_maps_to_effort_none() {
        let mut ctx = Ctx::new();
        let out = convert_reasoning_to_open_responses(
            Some(ChatCompletionsReasoning::Enabled(false)),
            Some(ChatCompletionsReasoningEffort::High),
            &mut ctx,
        );

        assert_eq!(
            out,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::None),
                summary: None,
            }),
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn unknown_tool_choice_mode_is_dropped_with_warning() {
        let mut ctx = Ctx::new();
        let out = convert_tool_choice_to_open_responses(
            ChatCompletionsToolChoice::Mode("weird".into()),
            &mut ctx,
        );
        assert!(out.is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tool_choice");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn non_string_metadata_value_warns_and_is_dropped() {
        let mut ctx = Ctx::new();
        let out = convert_metadata_and_user_to_open_responses(
            Some(serde_json::json!({"a":"ok","b":123})),
            None,
            &mut ctx,
        );
        assert_eq!(
            out.as_ref().and_then(|m| m.get("a").map(String::as_str)),
            Some("ok")
        );
        assert!(out.as_ref().and_then(|m| m.get("b")).is_none());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "metadata");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn service_tier_scale_maps_to_priority_with_warning() {
        let mut ctx = Ctx::new();
        let out = convert_service_tier_to_open_responses(
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Scale),
            &mut ctx,
        );
        assert_eq!(out, Some(ServiceTier::Priority));
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "service_tier");
        assert_eq!(warnings[0].action, WarningAction::Changed);
    }

    #[test]
    fn file_id_with_file_data_warns_but_keeps_file_part() {
        let mut ctx = Ctx::new();
        let out = convert_cc_content_part_to_or_input(
            ChatCompletionsContentPart::File {
                file: ChatCompletionsFileData {
                    file_data: Some("ZGF0YQ==".into()),
                    file_id: Some("file_1".into()),
                    filename: Some("a.txt".into()),
                },
            },
            &mut ctx,
            false,
        );
        assert!(matches!(
            out,
            Some(InputContentPart::File {
                filename: Some(_),
                file_data: Some(_),
                file_url: None
            })
        ));
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "file.file_id");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
    }

    #[test]
    fn text_with_is_assistant_converts_to_output_text() {
        let mut ctx = Ctx::new();
        let out = convert_cc_content_part_to_or_input(
            ChatCompletionsContentPart::Text {
                text: "hello".into(),
                cache_control: None,
            },
            &mut ctx,
            true,
        );
        assert!(matches!(
            out,
            Some(InputContentPart::OutputText { text, .. }) if text == "hello"
        ));
        assert!(ctx.into_warnings().is_empty());
    }
}
