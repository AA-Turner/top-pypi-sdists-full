use crate::anthropic::convert::ctx::ConversionCtx;
use crate::anthropic::convert::helpers::*;
use crate::anthropic::request::AnthropicRequest;
use crate::anthropic::types::*;
use crate::config::ConversionConfig;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::open_responses_input_accum::OpenResponsesInputAccum;
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::request::{OpenResponsesInput, OpenResponsesRequest};
use crate::open_responses::types::*;
use crate::traits::IntoOpenResponses;

impl IntoOpenResponses for AnthropicRequest {
    type Target = OpenResponsesRequest;

    fn into_open_responses(
        self,
        config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<OpenResponsesRequest>, ConversionError> {
        let strip = config.as_ref().is_some_and(|c| c.strip_encrypted_reasoning);
        let mut ctx = if strip {
            ConversionCtx::with_config(crate::anthropic::convert::config::AnthropicConvertConfig {
                strip_encrypted_reasoning: true,
                ..Default::default()
            })
        } else {
            ConversionCtx::new()
        };
        let mut accum = OpenResponsesInputAccum::new();
        if let Some(system) = self.system {
            append_anthropic_system_to_open_responses(&mut accum, system, &mut ctx);
        }
        convert_anthropic_messages(&mut accum, self.messages, &mut ctx);

        // Derive effort from output_config.effort (preferred) or thinking (legacy).
        let output_effort = self
            .output_config
            .as_ref()
            .and_then(|c| c.effort.clone())
            .and_then(|e| ReasoningEffort::lossy_try_from(e, &mut ctx, "output_config.effort"));

        let thinking_reasoning = self.thinking.and_then(|t| {
            convert_anthropic_messages_thinking_to_open_responses_reasoning(
                t,
                self.max_tokens,
                &mut ctx,
            )
        });

        let reasoning =
            merge_effort_and_thinking_reasoning(output_effort, thinking_reasoning, &mut ctx);

        let mut result = ConversionResult::with_warnings(
            OpenResponsesRequest {
                model: self.model,
                input: OpenResponsesInput::Items(accum.into_items()),
                max_output_tokens: Some(self.max_tokens),
                temperature: self.temperature,
                top_p: self.top_p,
                stream: self.stream,
                tools: self.tools.map(|tools| {
                    tools
                        .into_iter()
                        .filter_map(|t| {
                            convert_anthropic_messages_tool_to_open_responses(t, &mut ctx)
                        })
                        .collect()
                }),
                tool_choice: self
                    .tool_choice
                    .map(convert_anthropic_messages_tool_choice_to_open_responses),
                reasoning,
                service_tier: self
                    .service_tier
                    .and_then(|tier| ServiceTier::lossy_try_from(tier, &mut ctx, "service_tier")),
                text: convert_anthropic_output_config_to_open_responses_text(
                    self.output_config,
                    &mut ctx,
                ),
                prompt_cache_retention:
                    convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(
                        self.cache_control,
                    ),
                ..Default::default()
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Open Responses",
            &[
                ("top_k", self.top_k.is_some()),
                ("stop_sequences", self.stop_sequences.is_some()),
                ("container", self.container.is_some()),
                ("inference_geo", self.inference_geo.is_some()),
            ],
        );
        if self.metadata.is_some() {
            result.warn(
                "metadata",
                WarningAction::Dropped,
                "Anthropic metadata structure differs",
            );
        }

        Ok(result)
    }
}

fn append_anthropic_system_to_open_responses(
    accum: &mut OpenResponsesInputAccum,
    system: AnthropicSystem,
    ctx: &mut ConversionCtx,
) {
    match system {
        AnthropicSystem::Text(text) => {
            accum.push_item(
                MessageRole::Developer,
                InputItem::Message {
                    role: MessageRole::Developer,
                    content: InputContent::Text(text),
                    id: None,
                    status: None,
                },
            );
        }
        AnthropicSystem::Blocks(blocks) => {
            for (i, block) in blocks.into_iter().enumerate() {
                if block.kind != "text" {
                    ctx.push(format!("system[{i}]"));
                    ctx.warn(
                        "type",
                        WarningAction::Changed,
                        format!(
                            "unknown Anthropic system block type '{}' treated as developer text",
                            block.kind
                        ),
                    );
                    ctx.pop();
                }
                accum.push_item(
                    MessageRole::Developer,
                    InputItem::Message {
                        role: MessageRole::Developer,
                        content: InputContent::Text(block.text),
                        id: None,
                        status: None,
                    },
                );
            }
        }
    }
}

fn convert_anthropic_messages(
    accum: &mut OpenResponsesInputAccum,
    messages: Vec<AnthropicMessage>,
    ctx: &mut ConversionCtx,
) {
    // Tracks server_tool_use web_search blocks across messages so the query
    // is available when the matching web_search_tool_result arrives in the
    // next (user) message.
    let mut pending_web_search: Option<(String, Option<String>)> = None;
    // Tracks server_tool_use tool_search blocks across messages.
    // (id, input_json)
    let mut pending_tool_search: Option<(String, serde_json::Value)> = None;

    for (i, msg) in messages.into_iter().enumerate() {
        ctx.push(format!("messages[{i}]"));

        let blocks = match msg.content {
            AnthropicMessageContent::Text(t) => {
                vec![AnthropicInputContentBlock::Text {
                    text: t,
                    cache_control: None,
                    citations: None,
                }]
            }
            AnthropicMessageContent::Blocks(b) => b,
        };

        let role = match msg.role {
            AnthropicRole::User => MessageRole::User,
            AnthropicRole::Assistant => MessageRole::Assistant,
            AnthropicRole::System => MessageRole::System,
        };

        convert_blocks(
            accum,
            blocks,
            role,
            ctx,
            &mut pending_web_search,
            &mut pending_tool_search,
        );
        ctx.pop();
    }

    // Flush any unmatched server_tool_use
    if let Some((id, query)) = pending_web_search {
        accum.push_item(
            MessageRole::Assistant,
            InputItem::WebSearchCall {
                id: Some(id),
                status: Some(WebSearchCallStatus::InProgress),
                action: Some(WebSearchAction::Search {
                    query,
                    queries: vec![],
                    sources: vec![],
                }),
            },
        );
    }
    if let Some((id, input)) = pending_tool_search {
        accum.push_item(
            MessageRole::Assistant,
            InputItem::ToolSearchCall {
                id: Some(id),
                call_id: None,
                arguments: input,
                execution: Some(ToolSearchExecution::Server),
                status: Some(ToolSearchCallStatus::InProgress),
            },
        );
    }
}

fn convert_blocks(
    accum: &mut OpenResponsesInputAccum,
    blocks: Vec<AnthropicInputContentBlock>,
    role: MessageRole,
    ctx: &mut ConversionCtx,
    pending_web_search: &mut Option<(String, Option<String>)>,
    pending_tool_search: &mut Option<(String, serde_json::Value)>,
) {
    for block in blocks {
        match block {
            AnthropicInputContentBlock::Text { text, .. } => {
                if role == MessageRole::Assistant {
                    accum.push_part(InputContentPart::OutputText {
                        text,
                        annotations: vec![],
                        logprobs: vec![],
                    });
                } else {
                    accum.push_part(InputContentPart::Text { text });
                }
            }
            AnthropicInputContentBlock::Image { source, .. } => {
                accum.push_part(InputContentPart::Image {
                    image_url: Some(image_source_to_url(source)),
                    detail: None,
                });
            }
            AnthropicInputContentBlock::Document { source, title, .. } => {
                accum.push_part(document_source_to_open_responses_file(source, title));
            }
            AnthropicInputContentBlock::SearchResult { content, title, .. } => {
                accum.push_part(search_result_to_text(title, content));
            }
            AnthropicInputContentBlock::ToolResult {
                tool_use_id,
                content,
                ..
            } => {
                let (output, tool_refs) = tool_result_content_to_output_and_refs(content);
                accum.push_item(
                    role,
                    InputItem::FunctionCallOutput {
                        call_id: tool_use_id.clone(),
                        output,
                        id: None,
                        status: None,
                    },
                );
                if !tool_refs.is_empty() {
                    let tools = tool_refs
                        .into_iter()
                        .map(|name| Tool::Function {
                            name,
                            description: None,
                            parameters: None,
                            strict: None,
                            defer_loading: None,
                        })
                        .collect();
                    accum.push_item(
                        role,
                        InputItem::ToolSearchOutput {
                            id: None,
                            call_id: Some(tool_use_id),
                            tools,
                            execution: Some(ToolSearchExecution::Client),
                            status: Some(ToolSearchCallStatus::Completed),
                        },
                    );
                }
            }
            AnthropicInputContentBlock::ToolUse {
                id, name, input, ..
            } => {
                let arguments = serde_json::to_string(&input).unwrap_or_else(|_| {
                    ctx.warn(
                        "tool_use.input",
                        WarningAction::Changed,
                        "failed to serialize tool input, replaced with empty string",
                    );
                    String::new()
                });
                accum.push_item(
                    role,
                    InputItem::FunctionCall {
                        call_id: id,
                        name,
                        namespace: None,
                        arguments,
                        id: None,
                        status: None,
                    },
                );
            }
            // Signature is stored in encrypted_content to preserve it for
            // round-trips. On the way back (OR→AM), we distinguish from
            // RedactedThinking by checking whether summary is non-empty.
            AnthropicInputContentBlock::Thinking {
                thinking,
                signature,
            } => {
                let encrypted_content = if ctx.config.strip_encrypted_reasoning {
                    None
                } else {
                    Some(signature)
                };
                accum.push_item(
                    role,
                    InputItem::Reasoning {
                        summary: vec![SummaryContent {
                            kind: SummaryContentType::SummaryText,
                            text: thinking,
                        }],
                        id: None,
                        encrypted_content,
                    },
                );
            }
            AnthropicInputContentBlock::RedactedThinking { data } => {
                if ctx.config.strip_encrypted_reasoning {
                    // No summary to preserve — drop entirely
                } else {
                    accum.push_item(
                        role,
                        InputItem::Reasoning {
                            summary: Vec::new(),
                            id: None,
                            encrypted_content: Some(data),
                        },
                    );
                }
            }
            AnthropicInputContentBlock::ServerToolUse {
                id, name, input, ..
            } => {
                if name == "web_search" {
                    let query = input
                        .get("query")
                        .and_then(|v| v.as_str())
                        .map(String::from);
                    *pending_web_search = Some((id, query));
                } else if name.starts_with("tool_search_tool") {
                    *pending_tool_search = Some((id, input));
                } else {
                    ctx.warn(
                        "server_tool_use",
                        WarningAction::Dropped,
                        format!("unsupported server tool '{name}'"),
                    );
                }
            }
            AnthropicInputContentBlock::WebSearchToolResult {
                tool_use_id,
                content,
            } => {
                let query = pending_web_search
                    .take()
                    .filter(|(id, _)| *id == tool_use_id)
                    .and_then(|(_, q)| q);

                let (status, sources) = convert_web_search_results(content, ctx);
                accum.push_item(
                    role,
                    InputItem::WebSearchCall {
                        id: Some(tool_use_id),
                        status: Some(status),
                        action: Some(WebSearchAction::Search {
                            query,
                            queries: vec![],
                            sources,
                        }),
                    },
                );
            }
            AnthropicInputContentBlock::ToolSearchToolResult {
                tool_use_id,
                content,
                ..
            } => {
                let arguments = pending_tool_search
                    .take()
                    .filter(|(id, _)| *id == tool_use_id)
                    .map(|(_, input)| input)
                    .unwrap_or(serde_json::Value::Null);

                match content {
                    AnthropicToolSearchToolResultContent::Error { error_code, .. } => {
                        ctx.warn(
                            "tool_search_tool_result",
                            WarningAction::Changed,
                            format!("tool search failed with error: {error_code}"),
                        );
                        accum.push_item(
                            role,
                            InputItem::ToolSearchCall {
                                id: Some(tool_use_id),
                                call_id: None,
                                arguments,
                                execution: Some(ToolSearchExecution::Server),
                                status: Some(ToolSearchCallStatus::Incomplete),
                            },
                        );
                    }
                    AnthropicToolSearchToolResultContent::SearchResult { tool_references } => {
                        accum.push_item(
                            role,
                            InputItem::ToolSearchCall {
                                id: Some(tool_use_id.clone()),
                                call_id: None,
                                arguments,
                                execution: Some(ToolSearchExecution::Server),
                                status: Some(ToolSearchCallStatus::Completed),
                            },
                        );
                        let tools: Vec<Tool> = tool_references
                            .into_iter()
                            .map(|tr| Tool::Function {
                                name: tr.tool_name,
                                description: None,
                                parameters: None,
                                strict: None,
                                defer_loading: None,
                            })
                            .collect();
                        accum.push_item(
                            role,
                            InputItem::ToolSearchOutput {
                                id: None,
                                call_id: Some(tool_use_id),
                                tools,
                                execution: Some(ToolSearchExecution::Server),
                                status: Some(ToolSearchCallStatus::Completed),
                            },
                        );
                    }
                }
            }
        }
    }

    accum.flush_parts(role);
}

/// Splits tool_result content into (output_value, tool_reference_names).
/// Tool references are extracted separately so they can be emitted as
/// ToolSearchOutput items for client-side tool search.
fn tool_result_content_to_output_and_refs(
    content: Option<AnthropicToolResultContent>,
) -> (FunctionCallOutputValue, Vec<String>) {
    match content {
        None => (FunctionCallOutputValue::Text(String::new()), vec![]),
        Some(AnthropicToolResultContent::Text(t)) => (FunctionCallOutputValue::Text(t), vec![]),
        Some(AnthropicToolResultContent::Blocks(blocks)) => {
            let mut parts: Vec<InputContentPart> = Vec::new();
            let mut tool_refs: Vec<String> = Vec::new();
            for b in blocks {
                match b {
                    AnthropicToolResultBlock::Text { text } => {
                        parts.push(InputContentPart::Text { text });
                    }
                    AnthropicToolResultBlock::Image { source } => {
                        parts.push(InputContentPart::Image {
                            image_url: Some(image_source_to_url(source)),
                            detail: None,
                        });
                    }
                    AnthropicToolResultBlock::Document { source, title, .. } => {
                        parts.push(document_source_to_open_responses_file(source, title));
                    }
                    AnthropicToolResultBlock::SearchResult { content, title, .. } => {
                        parts.push(search_result_to_text(title, content));
                    }
                    AnthropicToolResultBlock::ToolReference { tool_name } => {
                        tool_refs.push(tool_name);
                    }
                }
            }
            let output = if parts.is_empty() {
                FunctionCallOutputValue::Text(String::new())
            } else {
                FunctionCallOutputValue::Parts(parts)
            };
            (output, tool_refs)
        }
    }
}

fn convert_anthropic_messages_tool_to_open_responses(
    tool: AnthropicToolUnion,
    ctx: &mut ConversionCtx,
) -> Option<Tool> {
    match tool {
        AnthropicToolUnion::Known(am) => Some(Tool::Function {
            name: am.name,
            description: am.description,
            parameters: Some(am.input_schema),
            strict: am.strict,
            defer_loading: am.defer_loading,
        }),
        AnthropicToolUnion::Other(value) => {
            let type_str = value.get("type").and_then(|v| v.as_str()).unwrap_or("");
            if type_str.starts_with("web_search") {
                let user_location = value
                    .get("user_location")
                    .and_then(|loc| loc.as_object())
                    .map(|obj| UserLocation {
                        kind: obj
                            .get("type")
                            .and_then(|v| v.as_str())
                            .unwrap_or("approximate")
                            .to_string(),
                        city: obj.get("city").and_then(|v| v.as_str()).map(String::from),
                        country: obj
                            .get("country")
                            .and_then(|v| v.as_str())
                            .map(String::from),
                        region: obj.get("region").and_then(|v| v.as_str()).map(String::from),
                        timezone: obj
                            .get("timezone")
                            .and_then(|v| v.as_str())
                            .map(String::from),
                    });
                let allowed_domains = value
                    .get("allowed_domains")
                    .and_then(|v| v.as_array())
                    .map(|arr| {
                        arr.iter()
                            .filter_map(|v| v.as_str().map(String::from))
                            .collect::<Vec<_>>()
                    })
                    .unwrap_or_default();

                if value
                    .get("blocked_domains")
                    .and_then(|v| v.as_array())
                    .is_some_and(|a| !a.is_empty())
                {
                    ctx.warn(
                        "blocked_domains",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                if value.get("allowed_callers").is_some() {
                    ctx.warn(
                        "allowed_callers",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                if value.get("cache_control").is_some() {
                    ctx.warn(
                        "cache_control",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                if value.get("max_uses").is_some() {
                    ctx.warn(
                        "max_uses",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }

                let filters = if allowed_domains.is_empty() {
                    None
                } else {
                    Some(WebSearchFilters { allowed_domains })
                };

                Some(Tool::WebSearch {
                    search_context_size: None,
                    user_location,
                    filters,
                })
            } else if type_str.starts_with("tool_search_tool") {
                Some(Tool::ToolSearch {
                    description: None,
                    execution: Some(ToolSearchExecution::Server),
                    parameters: None,
                })
            } else {
                None
            }
        }
    }
}

fn convert_anthropic_messages_tool_choice_to_open_responses(tc: AnthropicToolChoice) -> ToolChoice {
    match tc {
        AnthropicToolChoice::Auto { .. } => ToolChoice::Mode(ToolChoiceMode::Auto),
        AnthropicToolChoice::Any { .. } => ToolChoice::Mode(ToolChoiceMode::Required),
        AnthropicToolChoice::None => ToolChoice::Mode(ToolChoiceMode::None),
        AnthropicToolChoice::Tool { name, .. } => {
            ToolChoice::Specific(SpecificToolChoice::Function { name: Some(name) })
        }
    }
}

fn convert_anthropic_messages_thinking_to_open_responses_reasoning(
    thinking: AnthropicThinkingConfig,
    max_tokens: u64,
    ctx: &mut ConversionCtx,
) -> Option<ReasoningConfig> {
    match thinking {
        AnthropicThinkingConfig::Enabled {
            budget_tokens,
            display,
        } => {
            let effort = ctx
                .config
                .budget_to_effort(budget_tokens, max_tokens)
                .unwrap_or_else(|_| {
                    ctx.warn(
                        "max_tokens",
                        WarningAction::Changed,
                        "max_tokens is too small for reasoning; defaulting effort to medium",
                    );
                    ReasoningEffort::Medium
                });
            let summary = convert_thinking_display_to_reasoning_summary(display);
            Some(ReasoningConfig {
                effort: Some(effort),
                summary,
            })
        }
        AnthropicThinkingConfig::Adaptive { display } => {
            let summary = convert_thinking_display_to_reasoning_summary(display);
            Some(ReasoningConfig {
                effort: None,
                summary,
            })
        }
        AnthropicThinkingConfig::Disabled => None,
    }
}

/// Maps the Anthropic top-level `cache_control` to an Open Responses
/// `prompt_cache_retention` value:
///
/// - AM `cache_control: None` → OR `None`
/// - AM `ttl: None` or `"5m"` → OR `None` (OR default is equivalent)
/// - AM `ttl: "1h"` → OR `Some("24h")`
fn convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(
    cache_control: Option<CacheControl>,
) -> Option<String> {
    let cc = cache_control?;
    match cc.ttl.as_deref() {
        Some("1h") => Some("24h".to_string()),
        _ => None, // None | "5m" → OR default
    }
}

/// Maps Anthropic `thinking.display` to Open Responses `reasoning.summary`.
///
/// On [Anthropic's side](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking),
/// an absent `display` and `display: "summarized"` are semantically identical:
/// both produce the full visible thinking stream. They must map to the same OR
/// value, otherwise spelling out the default silently downgrades reasoning
/// visibility (see ENG-1249).
///
/// [`Auto`](https://platform.openai.com/docs/api-reference/responses/create) is
/// OR's "best summarizer available for this model" — typically equivalent to
/// `detailed` on modern reasoning models, with room for finer tiers in the
/// future. It's the closest analogue to Anthropic's default.
///
/// - `None` / `Summarized` → `Auto`: visible thinking.
/// - `Omitted` → no summary: user explicitly opted out.
fn convert_thinking_display_to_reasoning_summary(
    display: Option<AnthropicThinkingDisplay>,
) -> Option<ReasoningSummary> {
    match display {
        None | Some(AnthropicThinkingDisplay::Summarized) => Some(ReasoningSummary::Auto),
        Some(AnthropicThinkingDisplay::Omitted) => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn enabled_thinking_no_display_sets_summary_auto() {
        let mut ctx = ConversionCtx::new();
        let reasoning = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Enabled {
                budget_tokens: 2048,
                display: None,
            },
            32_768,
            &mut ctx,
        );

        assert_eq!(
            reasoning,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Auto),
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn enabled_thinking_display_summarized_maps_to_auto() {
        // ENG-1249: `display:"summarized"` is Anthropic's documented explicit
        // form of the default and is semantically identical to omitting
        // `display`. Both must map to `summary:auto` so that an explicit
        // request for visible thinking is not silently downgraded relative to
        // an implicit one.
        let mut ctx = ConversionCtx::new();
        let reasoning = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Enabled {
                budget_tokens: 2048,
                display: Some(AnthropicThinkingDisplay::Summarized),
            },
            32_768,
            &mut ctx,
        );

        assert_eq!(
            reasoning,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Auto),
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn enabled_thinking_display_summarized_matches_no_display() {
        // ENG-1249 regression guard: explicit `display:"summarized"` and an
        // omitted `display` must produce identical OR `reasoning` output.
        let mut ctx_summarized = ConversionCtx::new();
        let summarized = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Enabled {
                budget_tokens: 2048,
                display: Some(AnthropicThinkingDisplay::Summarized),
            },
            32_768,
            &mut ctx_summarized,
        );

        let mut ctx_none = ConversionCtx::new();
        let none = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Enabled {
                budget_tokens: 2048,
                display: None,
            },
            32_768,
            &mut ctx_none,
        );

        assert_eq!(summarized, none);
        assert!(ctx_summarized.into_warnings().is_empty());
        assert!(ctx_none.into_warnings().is_empty());
    }

    #[test]
    fn adaptive_thinking_display_summarized_matches_no_display() {
        // ENG-1249 regression guard for adaptive thinking variant.
        let mut ctx_summarized = ConversionCtx::new();
        let summarized = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            },
            32_768,
            &mut ctx_summarized,
        );

        let mut ctx_none = ConversionCtx::new();
        let none = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Adaptive { display: None },
            32_768,
            &mut ctx_none,
        );

        assert_eq!(summarized, none);
        assert!(ctx_summarized.into_warnings().is_empty());
        assert!(ctx_none.into_warnings().is_empty());
    }

    #[test]
    fn enabled_thinking_display_omitted_maps_to_no_summary() {
        let mut ctx = ConversionCtx::new();
        let reasoning = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Enabled {
                budget_tokens: 2048,
                display: Some(AnthropicThinkingDisplay::Omitted),
            },
            32_768,
            &mut ctx,
        );

        assert_eq!(
            reasoning,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: None,
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn adaptive_thinking_no_display_sets_summary_auto() {
        let mut ctx = ConversionCtx::new();
        let reasoning = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Adaptive { display: None },
            32_768,
            &mut ctx,
        );

        assert_eq!(
            reasoning,
            Some(ReasoningConfig {
                effort: None,
                summary: Some(ReasoningSummary::Auto),
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn adaptive_thinking_display_omitted_maps_to_no_summary() {
        let mut ctx = ConversionCtx::new();
        let reasoning = convert_anthropic_messages_thinking_to_open_responses_reasoning(
            AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Omitted),
            },
            32_768,
            &mut ctx,
        );

        assert_eq!(
            reasoning,
            Some(ReasoningConfig {
                effort: None,
                summary: None,
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    // ── merge_effort_and_thinking_reasoning ──

    #[test]
    fn merge_output_effort_overrides_thinking_effort_with_warning() {
        let mut ctx = ConversionCtx::new();
        let result = merge_effort_and_thinking_reasoning(
            Some(ReasoningEffort::High),
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Concise),
            }),
            &mut ctx,
        );
        assert_eq!(
            result,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::High),
                summary: Some(ReasoningSummary::Concise),
            })
        );
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert!(warnings[0].message.contains("using output_config.effort"));
    }

    #[test]
    fn merge_output_effort_with_adaptive_thinking_no_warning() {
        let mut ctx = ConversionCtx::new();
        let result = merge_effort_and_thinking_reasoning(
            Some(ReasoningEffort::Xhigh),
            Some(ReasoningConfig {
                effort: None,
                summary: Some(ReasoningSummary::Auto),
            }),
            &mut ctx,
        );
        assert_eq!(
            result,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Xhigh),
                summary: Some(ReasoningSummary::Auto),
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn merge_output_effort_only_no_thinking() {
        let mut ctx = ConversionCtx::new();
        let result =
            merge_effort_and_thinking_reasoning(Some(ReasoningEffort::Medium), None, &mut ctx);
        assert_eq!(
            result,
            Some(ReasoningConfig {
                effort: Some(ReasoningEffort::Medium),
                summary: None,
            })
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn merge_thinking_only_no_output_effort() {
        let mut ctx = ConversionCtx::new();
        let thinking = Some(ReasoningConfig {
            effort: Some(ReasoningEffort::Low),
            summary: Some(ReasoningSummary::Auto),
        });
        let result = merge_effort_and_thinking_reasoning(None, thinking.clone(), &mut ctx);
        assert_eq!(result, thinking);
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn merge_neither_returns_none() {
        let mut ctx = ConversionCtx::new();
        let result = merge_effort_and_thinking_reasoning(None, None, &mut ctx);
        assert_eq!(result, None);
        assert!(ctx.into_warnings().is_empty());
    }

    // ── cache_control ──

    #[test]
    fn cache_control_none_maps_to_no_retention() {
        let retention =
            convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(None);
        assert_eq!(retention, None);
    }

    #[test]
    fn cache_control_ephemeral_no_ttl_maps_to_no_retention() {
        let retention = convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(
            Some(CacheControl {
                kind: "ephemeral".to_string(),
                ttl: None,
            }),
        );
        assert_eq!(retention, None);
    }

    #[test]
    fn cache_control_ephemeral_5m_maps_to_no_retention() {
        let retention = convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(
            Some(CacheControl {
                kind: "ephemeral".to_string(),
                ttl: Some("5m".to_string()),
            }),
        );
        assert_eq!(retention, None);
    }

    #[test]
    fn cache_control_ephemeral_1h_maps_to_24h_retention() {
        let retention = convert_anthropic_cache_control_to_open_responses_prompt_cache_retention(
            Some(CacheControl {
                kind: "ephemeral".to_string(),
                ttl: Some("1h".to_string()),
            }),
        );
        assert_eq!(retention, Some("24h".to_string()));
    }
}

fn convert_anthropic_output_config_to_open_responses_text(
    config: Option<AnthropicOutputConfig>,
    _ctx: &mut ConversionCtx,
) -> Option<TextConfig> {
    let config = config?;

    // effort is handled separately via merge_effort_and_thinking_reasoning

    let format =
        config.format.map(
            |AnthropicOutputFormat::JsonSchema { schema }| TextFormat::JsonSchema {
                name: "json_schema".to_string(),
                description: None,
                schema: Some(schema),
                strict: None,
            },
        );

    format.as_ref()?;

    Some(TextConfig {
        format,
        verbosity: None,
    })
}

/// Merges effort from `output_config.effort` with reasoning derived from `thinking`.
///
/// `output_config.effort` is the newer/recommended mechanism and takes precedence
/// over `thinking.budget_tokens`-derived effort when both are present.
fn merge_effort_and_thinking_reasoning(
    output_effort: Option<ReasoningEffort>,
    thinking_reasoning: Option<ReasoningConfig>,
    ctx: &mut ConversionCtx,
) -> Option<ReasoningConfig> {
    match (output_effort, thinking_reasoning) {
        // Both present: output_config.effort wins, summary from thinking.
        (
            Some(effort),
            Some(ReasoningConfig {
                effort: Some(_),
                summary,
            }),
        ) => {
            ctx.warn(
                "output_config.effort",
                WarningAction::Changed,
                "both output_config.effort and thinking are present; using output_config.effort",
            );
            Some(ReasoningConfig {
                effort: Some(effort),
                summary,
            })
        }
        // output_config.effort + adaptive thinking (no derived effort override)
        (
            Some(effort),
            Some(ReasoningConfig {
                effort: None,
                summary,
            }),
        ) => Some(ReasoningConfig {
            effort: Some(effort),
            summary,
        }),
        // Only output_config.effort, no thinking at all
        (Some(effort), None) => Some(ReasoningConfig {
            effort: Some(effort),
            summary: None,
        }),
        // Only thinking, no output_config.effort
        (None, some_reasoning) => some_reasoning,
    }
}
