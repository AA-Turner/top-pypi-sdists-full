use super::accum::{AnthropicMessageAccum, append_blocks_to_content};
use crate::anthropic::convert::ctx::ConversionCtx;
use crate::anthropic::convert::helpers::*;
use crate::anthropic::request::AnthropicRequest;
use crate::anthropic::types::*;
use crate::config::ConversionConfig;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::tool_namespace::{
    flatten_namespace_tool_references, flatten_namespace_tools, flatten_tool_name,
};
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::request::{OpenResponsesInput, OpenResponsesRequest};
use crate::open_responses::types::*;
use crate::traits::FromOpenResponses;

impl FromOpenResponses for AnthropicRequest {
    type Source = OpenResponsesRequest;

    fn from_open_responses(
        source: OpenResponsesRequest,
        config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<Self>, ConversionError> {
        let strip = config.as_ref().is_some_and(|c| c.strip_encrypted_reasoning);
        let mut ctx = if strip {
            ConversionCtx::with_config(crate::anthropic::convert::config::AnthropicConvertConfig {
                strip_encrypted_reasoning: true,
                ..Default::default()
            })
        } else {
            ConversionCtx::new()
        };
        let had_instructions = source.instructions.is_some();
        let supports_mid_conv_system = model_supports_mid_conversation_system(&source.model);
        let (messages, system_from_input) = convert_open_responses_input_to_anthropic_messages(
            source.input,
            supports_mid_conv_system,
            &mut ctx,
        );

        let system = system_from_input;
        let tools = match source.tools {
            Some(tools) => Some(
                flatten_namespace_tools(tools, &mut ctx)?
                    .into_iter()
                    .filter_map(|(_, t)| {
                        convert_open_responses_tool_to_anthropic_messages(t, &mut ctx)
                    })
                    .collect(),
            ),
            None => None,
        };
        let mut tool_choice = source
            .tool_choice
            .and_then(|tc| convert_open_responses_tool_choice_to_anthropic_messages(tc, &mut ctx));
        let max_tokens = source
            .max_output_tokens
            .unwrap_or(ctx.config.default_max_tokens);
        if max_tokens == 0 {
            return Err(ConversionError::InvalidInput(
                "max_output_tokens must be at least 1".into(),
            ));
        }

        // Split reasoning into effort (→ output_config.effort) and thinking config.
        let (thinking, output_effort) = match source.reasoning {
            Some(reasoning) => convert_open_responses_reasoning_to_anthropic(reasoning, &mut ctx),
            None => (None, None),
        };
        normalize_thinking_tool_choice_compatibility(thinking.as_ref(), &mut tool_choice, &mut ctx);

        // Build output_config: merge effort from reasoning with format from text.
        let output_config =
            build_anthropic_output_config(output_effort, source.text.as_ref(), &mut ctx);

        let mut result = ConversionResult::with_warnings(
            AnthropicRequest {
                model: source.model,
                max_tokens,
                messages,
                system,
                temperature: source.temperature,
                top_p: source.top_p,
                top_k: None,
                stop_sequences: None,
                stream: source.stream,
                metadata: None,
                tools,
                tool_choice,
                thinking,
                service_tier: source.service_tier.and_then(|tier| {
                    AnthropicServiceTier::lossy_try_from(tier, &mut ctx, "service_tier")
                }),
                cache_control: Some(convert_open_responses_prompt_cache_retention_to_anthropic(
                    source.prompt_cache_retention.as_deref(),
                )),
                container: None,
                inference_geo: None,
                output_config,
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Anthropic",
            &[
                ("presence_penalty", source.presence_penalty.is_some()),
                ("frequency_penalty", source.frequency_penalty.is_some()),
                ("truncation", source.truncation.is_some()),
                ("store", source.store.is_some()),
                ("background", source.background.is_some()),
                (
                    "previous_response_id",
                    source.previous_response_id.is_some(),
                ),
                ("parallel_tool_calls", source.parallel_tool_calls.is_some()),
                ("top_logprobs", source.top_logprobs.is_some()),
            ],
        );
        if had_instructions {
            result.warn(
                "instructions",
                WarningAction::Dropped,
                "not supported in Anthropic",
            );
        }

        Ok(result)
    }
}

fn is_instruction_message(item: &InputItem) -> bool {
    matches!(
        item,
        InputItem::Message {
            role: MessageRole::System | MessageRole::Developer,
            ..
        }
    )
}

fn normalize_thinking_tool_choice_compatibility(
    thinking: Option<&AnthropicThinkingConfig>,
    tool_choice: &mut Option<AnthropicToolChoice>,
    ctx: &mut ConversionCtx,
) {
    let has_extended_thinking = matches!(
        thinking,
        Some(AnthropicThinkingConfig::Enabled { .. } | AnthropicThinkingConfig::Adaptive { .. })
    );
    if !has_extended_thinking {
        return;
    }

    let replacement = match tool_choice.as_ref() {
        Some(AnthropicToolChoice::Any {
            disable_parallel_tool_use,
        }) => Some(AnthropicToolChoice::Auto {
            disable_parallel_tool_use: *disable_parallel_tool_use,
        }),
        Some(AnthropicToolChoice::Tool {
            disable_parallel_tool_use,
            ..
        }) => Some(AnthropicToolChoice::Auto {
            disable_parallel_tool_use: *disable_parallel_tool_use,
        }),
        _ => None,
    };

    if let Some(replacement) = replacement {
        ctx.warn(
            "tool_choice",
            WarningAction::Changed,
            "Anthropic extended thinking is not compatible with tool_choice any/tool; mapped to auto",
        );
        *tool_choice = Some(replacement);
    }
}

fn convert_open_responses_input_to_anthropic_messages(
    input: OpenResponsesInput,
    supports_mid_conv_system: bool,
    ctx: &mut ConversionCtx,
) -> (Vec<AnthropicMessage>, Option<AnthropicSystem>) {
    match input {
        OpenResponsesInput::Text(t) => (
            vec![AnthropicMessage {
                role: AnthropicRole::User,
                content: AnthropicMessageContent::Text(t),
            }],
            None,
        ),
        OpenResponsesInput::Items(items) => {
            let mut accum = AnthropicMessageAccum::new();
            let mut system_blocks: Vec<AnthropicSystemBlock> = Vec::new();
            let mut in_conversation_phase = false;

            for (i, item) in items.into_iter().enumerate() {
                ctx.push(format!("input[{i}]"));

                let is_instruction = is_instruction_message(&item);
                let interleaved_instruction = is_instruction && in_conversation_phase;
                if !is_instruction {
                    in_conversation_phase = true;
                }

                match item {
                    InputItem::Message {
                        role: MessageRole::System | MessageRole::Developer,
                        content,
                        ..
                    } => {
                        if interleaved_instruction && supports_mid_conv_system {
                            // Opus 4.8 honors mid-conversation system messages:
                            // preserve position as a `{"role":"system"}` entry
                            // instead of hoisting into the top-level system field.
                            convert_open_responses_instruction_to_mid_conv_system(
                                &mut accum, content, ctx,
                            );
                        } else {
                            let appended = append_open_responses_content_to_anthropic_system_blocks(
                                &mut system_blocks,
                                content,
                                ctx,
                            );
                            if appended && interleaved_instruction {
                                ctx.warn(
                                    "role",
                                    WarningAction::Changed,
                                    "instruction message was hoisted to Anthropic system; original position not preserved (mid-conversation system messages require Claude Opus 4.8)",
                                );
                            }
                        }
                    }
                    InputItem::Message { role, content, .. } => {
                        convert_open_responses_message_to_anthropic_messages(
                            &mut accum, role, content, ctx,
                        );
                    }
                    InputItem::FunctionCall {
                        call_id,
                        name,
                        namespace,
                        arguments,
                        ..
                    } => {
                        let name = flatten_tool_name(namespace.as_deref(), name);
                        convert_open_responses_function_call_to_anthropic_messages(
                            &mut accum, call_id, name, arguments, ctx,
                        );
                    }
                    InputItem::FunctionCallOutput {
                        call_id, output, ..
                    } => {
                        convert_open_responses_function_call_output_to_anthropic_messages(
                            &mut accum, call_id, output, ctx,
                        );
                    }
                    InputItem::Reasoning {
                        summary,
                        encrypted_content,
                        ..
                    } => {
                        if !ctx.config.strip_encrypted_reasoning {
                            convert_open_responses_reasoning_to_anthropic_messages_block(
                                &mut accum,
                                summary,
                                encrypted_content,
                                ctx,
                            );
                        }
                    }
                    InputItem::CustomToolCall { .. } => {
                        ctx.warn(
                            "custom_tool_call",
                            WarningAction::Dropped,
                            "custom tool calls are not supported in Anthropic",
                        );
                    }
                    InputItem::CustomToolCallOutput { .. } => {
                        ctx.warn(
                            "custom_tool_call_output",
                            WarningAction::Dropped,
                            "custom tool call outputs are not supported in Anthropic",
                        );
                    }
                    InputItem::WebSearchCall { .. } => {
                        ctx.warn(
                            "web_search_call",
                            WarningAction::Dropped,
                            "web_search_call cannot be converted to Anthropic (missing encrypted_content)",
                        );
                    }
                    InputItem::ToolSearchCall { id, arguments, .. } => {
                        let block_id = id.unwrap_or_else(|| format!("ts_{i}"));
                        accum.push_blocks(
                            AnthropicRole::Assistant,
                            vec![AnthropicInputContentBlock::ServerToolUse {
                                id: block_id,
                                name: ctx.config.tool_search_name.to_string(),
                                input: arguments,
                                cache_control: None,
                            }],
                        );
                    }
                    InputItem::ToolSearchOutput {
                        call_id,
                        tools,
                        execution,
                        ..
                    } => {
                        let tool_use_id = call_id.unwrap_or_else(|| format!("ts_{i}"));
                        let tools = flatten_namespace_tool_references(tools);
                        if execution == Some(ToolSearchExecution::Client) {
                            // Client-side: emit tool_result with tool_reference blocks
                            let blocks: Vec<AnthropicToolResultBlock> = tools
                                .into_iter()
                                .filter_map(|t| match t {
                                    Tool::Function { name, .. } => {
                                        Some(AnthropicToolResultBlock::ToolReference {
                                            tool_name: name,
                                        })
                                    }
                                    other => {
                                        ctx.warn(
                                            "tool_search_output",
                                            WarningAction::Dropped,
                                            format!("only function tools can be referenced, dropped {:?}", std::mem::discriminant(&other)),
                                        );
                                        None
                                    }
                                })
                                .collect();
                            accum.push_blocks(
                                AnthropicRole::User,
                                vec![AnthropicInputContentBlock::ToolResult {
                                    tool_use_id,
                                    content: Some(AnthropicToolResultContent::Blocks(blocks)),
                                    is_error: None,
                                    cache_control: None,
                                }],
                            );
                        } else {
                            // Server-side: emit tool_search_tool_result
                            let tool_references = tools
                                .into_iter()
                                .filter_map(|t| match t {
                                    Tool::Function { name, .. } => {
                                        Some(AnthropicToolReference::new(name))
                                    }
                                    other => {
                                        ctx.warn(
                                            "tool_search_output",
                                            WarningAction::Dropped,
                                            format!("only function tools can be referenced, dropped {:?}", std::mem::discriminant(&other)),
                                        );
                                        None
                                    }
                                })
                                .collect();
                            accum.push_blocks(
                                AnthropicRole::User,
                                vec![AnthropicInputContentBlock::ToolSearchToolResult {
                                    tool_use_id,
                                    content: AnthropicToolSearchToolResultContent::SearchResult {
                                        tool_references,
                                    },
                                    cache_control: None,
                                }],
                            );
                        }
                    }
                    InputItem::ItemReference { .. } => {
                        ctx.warn(
                            "item_reference",
                            WarningAction::Dropped,
                            "not supported in Anthropic",
                        );
                    }
                }
                ctx.pop();
            }

            let mut messages = accum.into_messages();
            validate_and_repair_mid_conv_system_placement(&mut messages, &mut system_blocks, ctx);

            let system = match system_blocks.len() {
                0 => None,
                1 => Some(AnthropicSystem::Text(system_blocks.pop().unwrap().text)),
                _ => Some(AnthropicSystem::Blocks(system_blocks)),
            };
            (messages, system)
        }
    }
}

/// Emit an Open Responses instruction message as a positioned Anthropic
/// mid-conversation `{"role":"system"}` message. Consecutive system messages
/// are merged by the accumulator (Anthropic disallows consecutive ones).
fn convert_open_responses_instruction_to_mid_conv_system(
    accum: &mut AnthropicMessageAccum,
    content: InputContent,
    ctx: &mut ConversionCtx,
) {
    match content {
        InputContent::Text(text) => accum.push_text(AnthropicRole::System, text),
        InputContent::Parts(parts) => {
            let mut blocks = Vec::new();
            for (j, part) in parts.into_iter().enumerate() {
                ctx.push(format!("content[{j}]"));
                match part {
                    InputContentPart::Text { text } | InputContentPart::OutputText { text, .. } => {
                        blocks.push(AnthropicInputContentBlock::Text {
                            text,
                            cache_control: None,
                            citations: None,
                        });
                    }
                    InputContentPart::Image { .. } => {
                        ctx.warn(
                            "image",
                            WarningAction::Dropped,
                            "images are not representable in an Anthropic system message",
                        );
                    }
                    InputContentPart::File { .. } => {
                        ctx.warn(
                            "file",
                            WarningAction::Dropped,
                            "files are not representable in an Anthropic system message",
                        );
                    }
                }
                ctx.pop();
            }
            if blocks.is_empty() {
                ctx.warn(
                    "content",
                    WarningAction::Dropped,
                    "mid-conversation system message had no representable text",
                );
            } else {
                accum.push_blocks(AnthropicRole::System, blocks);
            }
        }
    }
}

/// Anthropic requires a mid-conversation `system` message to immediately follow
/// a `user` turn (or an `assistant` turn ending in server tool use) and to be
/// the last entry or be followed by an `assistant` turn. Any `system` message
/// that violates these rules is hoisted into the top-level `system` field to
/// avoid a 400, with a warning.
fn validate_and_repair_mid_conv_system_placement(
    messages: &mut Vec<AnthropicMessage>,
    system_blocks: &mut Vec<AnthropicSystemBlock>,
    ctx: &mut ConversionCtx,
) {
    let mut i = 0;
    while i < messages.len() {
        if messages[i].role != AnthropicRole::System {
            i += 1;
            continue;
        }

        let prev_ok = i > 0 && message_can_precede_mid_conv_system(&messages[i - 1]);
        let next_ok = i + 1 >= messages.len() || messages[i + 1].role == AnthropicRole::Assistant;

        if prev_ok && next_ok {
            i += 1;
            continue;
        }

        let removed = messages.remove(i);
        hoist_anthropic_system_message_to_blocks(removed, system_blocks, ctx);
        ctx.warn(
            "messages",
            WarningAction::Changed,
            "mid-conversation system message has invalid placement (must follow a user turn and be last or precede an assistant turn); hoisted to top-level system",
        );
        // Removing the separator can leave two same-role neighbors adjacent
        // (e.g. `user, system, user` -> `user, user`), which violates
        // Anthropic's turn alternation. Merge them back together, mirroring
        // what the accumulator does while building messages.
        if i > 0 && i < messages.len() && messages[i - 1].role == messages[i].role {
            let merged = messages.remove(i);
            append_blocks_to_content(&mut messages[i - 1].content, content_into_blocks(merged));
        }
        // Do not advance `i`: the slot now holds the following message, which
        // still needs to be checked (and a chain like `user, system, user,
        // system, user` thus fully collapses to a single `user`).
    }
}

/// A mid-conversation system message may follow a `user` turn, or an
/// `assistant` turn whose final block is a server tool use.
fn message_can_precede_mid_conv_system(prev: &AnthropicMessage) -> bool {
    match prev.role {
        AnthropicRole::User => true,
        AnthropicRole::System => false,
        AnthropicRole::Assistant => match &prev.content {
            AnthropicMessageContent::Text(_) => false,
            AnthropicMessageContent::Blocks(blocks) => matches!(
                blocks.last(),
                Some(AnthropicInputContentBlock::ServerToolUse { .. })
            ),
        },
    }
}

/// Move the text content of a (hoisted) system message into top-level system
/// blocks, appending after any existing leading instructions.
fn hoist_anthropic_system_message_to_blocks(
    message: AnthropicMessage,
    system_blocks: &mut Vec<AnthropicSystemBlock>,
    ctx: &mut ConversionCtx,
) {
    match message.content {
        AnthropicMessageContent::Text(text) => {
            system_blocks.push(AnthropicSystemBlock {
                kind: "text".into(),
                text,
                cache_control: None,
            });
        }
        AnthropicMessageContent::Blocks(blocks) => {
            for block in blocks {
                if let AnthropicInputContentBlock::Text { text, .. } = block {
                    system_blocks.push(AnthropicSystemBlock {
                        kind: "text".into(),
                        text,
                        cache_control: None,
                    });
                } else {
                    // System messages reaching this path are built only from
                    // text blocks today (non-text is dropped with a warning
                    // upstream), so this is defensive: warn rather than
                    // silently lose content if that ever changes.
                    ctx.warn(
                        "messages",
                        WarningAction::Dropped,
                        "non-text block in hoisted system message is not representable in Anthropic system",
                    );
                }
            }
        }
    }
}

/// Extract a message's content as a block list so it can be merged into an
/// adjacent same-role message via `append_blocks_to_content`.
fn content_into_blocks(message: AnthropicMessage) -> Vec<AnthropicInputContentBlock> {
    match message.content {
        AnthropicMessageContent::Blocks(blocks) => blocks,
        AnthropicMessageContent::Text(text) => vec![AnthropicInputContentBlock::Text {
            text,
            cache_control: None,
            citations: None,
        }],
    }
}

fn convert_open_responses_message_to_anthropic_messages(
    accum: &mut AnthropicMessageAccum,
    role: MessageRole,
    content: InputContent,
    ctx: &mut ConversionCtx,
) {
    let am_role = match role {
        MessageRole::User => AnthropicRole::User,
        MessageRole::Assistant => AnthropicRole::Assistant,
        MessageRole::System | MessageRole::Developer => {
            ctx.warn(
                "role",
                WarningAction::Changed,
                "instruction message was not hoisted before message conversion; coerced to user",
            );
            AnthropicRole::User
        }
    };

    match content {
        InputContent::Text(t) => accum.push_text(am_role, t),
        InputContent::Parts(parts) => {
            let blocks = parts
                .into_iter()
                .enumerate()
                .filter_map(|(j, part)| {
                    ctx.push(format!("content[{j}]"));
                    let result = convert_open_responses_part_to_anthropic_messages(part, ctx);
                    ctx.pop();
                    result
                })
                .collect();
            accum.push_blocks(am_role, blocks);
        }
    }
}

fn convert_open_responses_function_call_to_anthropic_messages(
    accum: &mut AnthropicMessageAccum,
    call_id: String,
    name: String,
    arguments: String,
    ctx: &mut ConversionCtx,
) {
    let input = serde_json::from_str(&arguments).unwrap_or_else(|_| {
        ctx.warn(
            "function_call.arguments",
            WarningAction::Changed,
            "malformed JSON arguments, replaced with empty object",
        );
        serde_json::Value::Object(Default::default())
    });
    let block = AnthropicInputContentBlock::ToolUse {
        id: call_id,
        name,
        input,
        cache_control: None,
    };
    accum.push_blocks(AnthropicRole::Assistant, vec![block]);
}

fn convert_open_responses_function_call_output_to_anthropic_messages(
    accum: &mut AnthropicMessageAccum,
    call_id: String,
    output: FunctionCallOutputValue,
    ctx: &mut ConversionCtx,
) {
    let content = match output {
        FunctionCallOutputValue::Text(t) => Some(AnthropicToolResultContent::Text(t)),
        FunctionCallOutputValue::Parts(parts) => {
            let blocks: Vec<AnthropicToolResultBlock> = parts
                .into_iter()
                .enumerate()
                .filter_map(|(j, p)| {
                    ctx.push(format!("output[{j}]"));
                    let result = match p {
                        InputContentPart::Text { text }
                        | InputContentPart::OutputText { text, .. } => {
                            Some(AnthropicToolResultBlock::Text { text })
                        }
                        InputContentPart::Image { image_url, .. } => {
                            let url = image_url?;
                            let (source, warn) = url_to_image_source(url);
                            if let Some(msg) = warn {
                                ctx.warn("image", WarningAction::Changed, msg);
                            }
                            Some(AnthropicToolResultBlock::Image { source })
                        }
                        InputContentPart::File {
                            filename,
                            file_data,
                            file_url,
                        } => {
                            let source = open_responses_file_to_document_source(
                                file_url,
                                file_data,
                                filename.as_deref(),
                            )?;
                            Some(AnthropicToolResultBlock::Document {
                                source,
                                citations: None,
                                context: None,
                                title: filename,
                            })
                        }
                    };
                    ctx.pop();
                    result
                })
                .collect();
            if blocks.is_empty() {
                None
            } else {
                Some(AnthropicToolResultContent::Blocks(blocks))
            }
        }
    };
    let block = AnthropicInputContentBlock::ToolResult {
        tool_use_id: call_id,
        content,
        is_error: None,
        cache_control: None,
    };
    accum.push_blocks(AnthropicRole::User, vec![block]);
}

/// Non-empty summary + signature → Thinking.
/// Empty summary + encrypted_content → RedactedThinking.
fn convert_open_responses_reasoning_to_anthropic_messages_block(
    accum: &mut AnthropicMessageAccum,
    summary: Vec<SummaryContent>,
    encrypted_content: Option<String>,
    ctx: &mut ConversionCtx,
) {
    let block = if !summary.is_empty() {
        let Some(signature) = encrypted_content.filter(|value| !value.is_empty()) else {
            ctx.warn(
                "reasoning",
                WarningAction::Dropped,
                "reasoning summary cannot be converted to Anthropic thinking without a signature",
            );
            return;
        };
        let text = summary
            .into_iter()
            .map(|s| s.text)
            .collect::<Vec<_>>()
            .join("\n");
        AnthropicInputContentBlock::Thinking {
            thinking: text,
            signature,
        }
    } else if let Some(data) = encrypted_content.filter(|value| !value.is_empty()) {
        AnthropicInputContentBlock::RedactedThinking { data }
    } else {
        ctx.warn("reasoning", WarningAction::Dropped, "empty reasoning item");
        return;
    };
    accum.push_blocks(AnthropicRole::Assistant, vec![block]);
}

fn append_open_responses_content_to_anthropic_system_blocks(
    system_blocks: &mut Vec<AnthropicSystemBlock>,
    content: InputContent,
    ctx: &mut ConversionCtx,
) -> bool {
    let before_len = system_blocks.len();

    match content {
        InputContent::Text(text) => {
            system_blocks.push(AnthropicSystemBlock {
                kind: "text".into(),
                text,
                cache_control: None,
            });
        }
        InputContent::Parts(parts) => {
            for (j, part) in parts.into_iter().enumerate() {
                ctx.push(format!("content[{j}]"));
                match part {
                    InputContentPart::Text { text } | InputContentPart::OutputText { text, .. } => {
                        system_blocks.push(AnthropicSystemBlock {
                            kind: "text".into(),
                            text,
                            cache_control: None,
                        });
                    }
                    InputContentPart::Image { .. } => {
                        ctx.warn(
                            "image",
                            WarningAction::Dropped,
                            "images are not representable in Anthropic system",
                        );
                    }
                    InputContentPart::File { .. } => {
                        ctx.warn(
                            "file",
                            WarningAction::Dropped,
                            "files are not representable in Anthropic system",
                        );
                    }
                }
                ctx.pop();
            }
        }
    }

    let appended = system_blocks.len() != before_len;
    if !appended {
        ctx.warn(
            "content",
            WarningAction::Dropped,
            "instruction message had no representable Anthropic system text",
        );
    }
    appended
}

fn convert_open_responses_part_to_anthropic_messages(
    part: InputContentPart,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicInputContentBlock> {
    match part {
        InputContentPart::Text { text } | InputContentPart::OutputText { text, .. } => {
            Some(AnthropicInputContentBlock::Text {
                text,
                cache_control: None,
                citations: None,
            })
        }
        InputContentPart::Image { image_url, .. } => {
            let url = image_url?;
            let (source, warn) = url_to_image_source(url);
            if let Some(msg) = warn {
                ctx.warn("image", WarningAction::Changed, msg);
            }
            Some(AnthropicInputContentBlock::Image {
                source,
                cache_control: None,
            })
        }
        InputContentPart::File {
            filename,
            file_data,
            file_url,
        } => {
            let source =
                open_responses_file_to_document_source(file_url, file_data, filename.as_deref())?;
            Some(AnthropicInputContentBlock::Document {
                source,
                cache_control: None,
                citations: None,
                context: None,
                title: filename,
            })
        }
    }
}

fn convert_open_responses_tool_to_anthropic_messages(
    tool: Tool,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicToolUnion> {
    match tool {
        Tool::Function {
            name,
            description,
            parameters,
            strict,
            defer_loading,
        } => Some(AnthropicToolUnion::Known(AnthropicTool {
            name,
            description,
            input_schema: parameters.unwrap_or(serde_json::json!({"type": "object"})),
            cache_control: None,
            strict,
            kind: None,
            defer_loading,
        })),
        Tool::WebSearch {
            search_context_size,
            user_location,
            filters,
        } => {
            if search_context_size.is_some() {
                ctx.warn(
                    "search_context_size",
                    WarningAction::Dropped,
                    "not supported in Anthropic",
                );
            }
            let mut obj = serde_json::json!({
                "type": ctx.config.web_search_type,
                "name": ctx.config.web_search_name
            });
            if let Some(loc) = user_location {
                obj["user_location"] = serde_json::json!({
                    "type": loc.kind,
                    "city": loc.city,
                    "country": loc.country,
                    "region": loc.region,
                    "timezone": loc.timezone,
                });
            }
            if let Some(f) = filters
                && !f.allowed_domains.is_empty()
            {
                obj["allowed_domains"] = serde_json::json!(f.allowed_domains);
            }
            Some(AnthropicToolUnion::Other(obj))
        }
        Tool::Custom { .. } => {
            ctx.warn(
                "custom_tool",
                WarningAction::Dropped,
                "custom tools are not supported in Anthropic",
            );
            None
        }
        Tool::Namespace { .. } => unreachable!("namespace tools are flattened before conversion"),
        Tool::ToolSearch { execution, .. } => {
            if execution == Some(ToolSearchExecution::Client) {
                // Client-side tool search uses a regular function tool on
                // the Anthropic side — no dedicated tool definition needed.
                None
            } else {
                // OR Tool::ToolSearch doesn't distinguish bm25/regex, so we
                // use the configured default. The variant is not preserved.
                Some(AnthropicToolUnion::Other(serde_json::json!({
                    "type": ctx.config.tool_search_type,
                    "name": ctx.config.tool_search_name
                })))
            }
        }
    }
}

fn convert_open_responses_tool_choice_to_anthropic_messages(
    tc: ToolChoice,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicToolChoice> {
    match tc {
        ToolChoice::Mode(ToolChoiceMode::Auto) => Some(AnthropicToolChoice::Auto {
            disable_parallel_tool_use: None,
        }),
        ToolChoice::Mode(ToolChoiceMode::Required) => Some(AnthropicToolChoice::Any {
            disable_parallel_tool_use: None,
        }),
        ToolChoice::Mode(ToolChoiceMode::None) => Some(AnthropicToolChoice::None),
        ToolChoice::Specific(SpecificToolChoice::Function { name }) => match name {
            Some(name) => Some(AnthropicToolChoice::Tool {
                name,
                disable_parallel_tool_use: None,
            }),
            None => {
                ctx.warn(
                    "tool_choice",
                    WarningAction::Dropped,
                    "specific function tool choice is missing name; tool_choice dropped",
                );
                None
            }
        },
        ToolChoice::Specific(SpecificToolChoice::Custom { name }) => {
            Some(AnthropicToolChoice::Tool {
                name,
                disable_parallel_tool_use: None,
            })
        }
        ToolChoice::AllowedTools(_) => {
            ctx.warn(
                "tool_choice.allowed_tools",
                WarningAction::Dropped,
                "not representable in Anthropic",
            );
            None
        }
    }
}

/// Builds the final `AnthropicOutputConfig` by merging effort from reasoning
/// with format from text config.
fn build_anthropic_output_config(
    output_effort: Option<AnthropicOutputEffort>,
    text: Option<&TextConfig>,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicOutputConfig> {
    let format = convert_open_responses_text_format_to_anthropic(text, ctx);

    if output_effort.is_none() && format.is_none() {
        return None;
    }

    Some(AnthropicOutputConfig {
        effort: output_effort,
        format,
    })
}

/// Extracts just the format portion of text config for Anthropic output_config.
fn convert_open_responses_text_format_to_anthropic(
    text: Option<&TextConfig>,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicOutputFormat> {
    let text = text?;

    if text.verbosity.is_some() {
        ctx.warn(
            "text.verbosity",
            WarningAction::Dropped,
            "not supported in Anthropic",
        );
    }

    match &text.format {
        Some(TextFormat::JsonSchema {
            schema,
            name,
            description,
            strict,
        }) => {
            if !name.is_empty() {
                ctx.warn(
                    "text.format.name",
                    WarningAction::Dropped,
                    "not supported in Anthropic",
                );
            }
            if description.is_some() {
                ctx.warn(
                    "text.format.description",
                    WarningAction::Dropped,
                    "not supported in Anthropic",
                );
            }
            if strict.is_some() {
                ctx.warn(
                    "text.format.strict",
                    WarningAction::Dropped,
                    "not supported in Anthropic",
                );
            }
            match schema {
                Some(s) => Some(AnthropicOutputFormat::JsonSchema { schema: s.clone() }),
                None => {
                    ctx.warn(
                        "text.format.schema",
                        WarningAction::Dropped,
                        "schema is missing, dropped json_schema format",
                    );
                    None
                }
            }
        }
        Some(TextFormat::Text) => None,
        Some(TextFormat::JsonObject) => {
            ctx.warn(
                "text.format",
                WarningAction::Dropped,
                "json_object format not supported in Anthropic",
            );
            None
        }
        None => None,
    }
}

/// Converts OR reasoning config into both an Anthropic thinking config and
/// an output effort level.
///
/// `output_config.effort` is the modern/recommended mechanism for controlling
/// effort on newer Anthropic models. The thinking config provides the
/// `display` (summary) setting and enables thinking when needed.
///
/// Returns `(thinking_config, output_effort)`.
fn convert_open_responses_reasoning_to_anthropic(
    reasoning: ReasoningConfig,
    ctx: &mut ConversionCtx,
) -> (
    Option<AnthropicThinkingConfig>,
    Option<AnthropicOutputEffort>,
) {
    let ReasoningConfig { effort, summary } = reasoning;

    let output_effort = effort
        .as_ref()
        .and_then(|e| AnthropicOutputEffort::lossy_try_from(e.clone(), ctx, "reasoning.effort"));

    let thinking = convert_open_responses_reasoning_to_anthropic_thinking(effort, summary, ctx);

    (thinking, output_effort)
}

fn convert_open_responses_reasoning_to_anthropic_thinking(
    effort: Option<ReasoningEffort>,
    summary: Option<ReasoningSummary>,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicThinkingConfig> {
    match (effort, summary) {
        (Some(ReasoningEffort::None), Some(_)) => {
            ctx.warn(
                "reasoning.summary",
                WarningAction::Dropped,
                "reasoning.summary is not representable when reasoning.effort is none; dropped",
            );
            Some(AnthropicThinkingConfig::Disabled)
        }
        (Some(ReasoningEffort::None), None) => Some(AnthropicThinkingConfig::Disabled),
        // With effort present, use Adaptive thinking — effort is communicated
        // via output_config.effort, and thinking.display carries the summary.
        (Some(_), summary) => {
            let display = convert_reasoning_summary_to_thinking_display(summary, ctx);
            Some(AnthropicThinkingConfig::Adaptive { display })
        }
        // No effort but summary present — adaptive thinking with display only.
        (None, Some(summary)) => {
            let display = convert_reasoning_summary_to_thinking_display(Some(summary), ctx);
            Some(AnthropicThinkingConfig::Adaptive { display })
        }
        (None, None) => None,
    }
}

fn convert_reasoning_summary_to_thinking_display(
    summary: Option<ReasoningSummary>,
    ctx: &mut ConversionCtx,
) -> Option<AnthropicThinkingDisplay> {
    match summary {
        None => Some(AnthropicThinkingDisplay::Omitted),
        Some(ReasoningSummary::Auto) => Some(AnthropicThinkingDisplay::Summarized),
        Some(ReasoningSummary::Concise) => Some(AnthropicThinkingDisplay::Summarized),
        Some(ReasoningSummary::Detailed) => {
            ctx.warn(
                "reasoning.summary",
                WarningAction::Changed,
                "Anthropic only supports summarized/omitted thinking display; mapped to summarized",
            );
            Some(AnthropicThinkingDisplay::Summarized)
        }
    }
}

/// Open Responses caches prompts by default; Anthropic requires explicit opt-in.
/// We always return a `CacheControl` with `type: "ephemeral"` and derive the
/// TTL from the Open Responses `prompt_cache_retention` value:
///
/// - `None` or `"in-memory"` → AM `ttl: None` (AM defaults to 5 min)
/// - `"24h"` → AM `ttl: Some("1h")` (AM's max extended tier)
fn convert_open_responses_prompt_cache_retention_to_anthropic(
    retention: Option<&str>,
) -> CacheControl {
    let ttl = match retention {
        Some("24h") => Some("1h".to_string()),
        _ => None, // None | "in-memory" → AM default (5m)
    };
    CacheControl {
        kind: "ephemeral".to_string(),
        ttl,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::traits::FromOpenResponses;

    #[test]
    fn max_output_tokens_zero_errors() {
        let result = AnthropicRequest::from_open_responses(
            OpenResponsesRequest {
                model: "test".to_string(),
                input: OpenResponsesInput::Text("hi".to_string()),
                max_output_tokens: Some(0),
                ..Default::default()
            },
            None,
        );
        assert!(result.is_err());
    }

    #[test]
    fn reasoning_summary_without_signature_is_dropped() {
        let mut accum = AnthropicMessageAccum::new();
        let mut ctx = ConversionCtx::new();

        convert_open_responses_reasoning_to_anthropic_messages_block(
            &mut accum,
            vec![SummaryContent {
                kind: SummaryContentType::SummaryText,
                text: "private reasoning".to_string(),
            }],
            None,
            &mut ctx,
        );

        assert!(accum.into_messages().is_empty());
        assert!(ctx.into_warnings().iter().any(|warning| {
            warning.field == "reasoning"
                && warning.action == WarningAction::Dropped
                && warning.message.contains("without a signature")
        }));
    }

    #[test]
    fn reasoning_summary_with_signature_maps_to_thinking_block() {
        let mut accum = AnthropicMessageAccum::new();
        let mut ctx = ConversionCtx::new();

        convert_open_responses_reasoning_to_anthropic_messages_block(
            &mut accum,
            vec![SummaryContent {
                kind: SummaryContentType::SummaryText,
                text: "private reasoning".to_string(),
            }],
            Some("sig_abc123".to_string()),
            &mut ctx,
        );

        let messages = accum.into_messages();
        assert_eq!(messages.len(), 1);
        match &messages[0].content {
            AnthropicMessageContent::Blocks(blocks) => assert!(matches!(
                &blocks[0],
                AnthropicInputContentBlock::Thinking { thinking, signature }
                    if thinking == "private reasoning" && signature == "sig_abc123"
            )),
            other => panic!("expected Blocks, got {other:?}"),
        }
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_is_dropped_when_effort_is_none() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::None),
                summary: Some(ReasoningSummary::Concise),
            },
            &mut ctx,
        );

        assert_eq!(thinking, Some(AnthropicThinkingConfig::Disabled));
        assert_eq!(output_effort, None); // None effort → no output_config.effort
        let warnings = ctx.into_warnings();
        assert!(
            warnings
                .iter()
                .any(|w| w.field == "reasoning.summary" && w.action == WarningAction::Dropped)
        );
    }

    #[test]
    fn reasoning_summary_auto_maps_to_adaptive_summarized_with_effort() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Auto),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Low));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_concise_maps_to_adaptive_summarized_with_effort() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Concise),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Low));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_detailed_maps_to_adaptive_summarized_with_warning() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: Some(ReasoningSummary::Detailed),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Low));
        let warnings = ctx.into_warnings();
        assert!(
            warnings
                .iter()
                .any(|w| w.field == "reasoning.summary" && w.action == WarningAction::Changed)
        );
    }

    #[test]
    fn reasoning_no_summary_maps_to_adaptive_omitted_with_effort() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Low),
                summary: None,
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Omitted),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Low));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_auto_maps_to_adaptive_summarized() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: None,
                summary: Some(ReasoningSummary::Auto),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, None);
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_concise_maps_to_adaptive_summarized() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: None,
                summary: Some(ReasoningSummary::Concise),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, None);
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_summary_detailed_maps_to_adaptive_summarized_no_effort_with_warning() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: None,
                summary: Some(ReasoningSummary::Detailed),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, None);
        let warnings = ctx.into_warnings();
        assert!(
            warnings
                .iter()
                .any(|w| w.field == "reasoning.summary" && w.action == WarningAction::Changed)
        );
    }

    #[test]
    fn reasoning_xhigh_effort_maps_to_output_config_xhigh() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Xhigh),
                summary: Some(ReasoningSummary::Auto),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Xhigh));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn reasoning_minimal_effort_maps_to_output_config_low_with_warning() {
        let mut ctx = ConversionCtx::new();
        let (thinking, output_effort) = convert_open_responses_reasoning_to_anthropic(
            ReasoningConfig {
                effort: Some(ReasoningEffort::Minimal),
                summary: Some(ReasoningSummary::Auto),
            },
            &mut ctx,
        );

        assert_eq!(
            thinking,
            Some(AnthropicThinkingConfig::Adaptive {
                display: Some(AnthropicThinkingDisplay::Summarized),
            })
        );
        assert_eq!(output_effort, Some(AnthropicOutputEffort::Low));
        let warnings = ctx.into_warnings();
        assert!(
            warnings
                .iter()
                .any(|w| w.message.contains("minimal") && w.action == WarningAction::Changed)
        );
    }

    #[test]
    fn required_tool_choice_with_extended_thinking_maps_to_auto_with_warning() {
        let result = AnthropicRequest::from_open_responses(
            OpenResponsesRequest {
                model: "gpt-5".to_string(),
                input: OpenResponsesInput::Text("hi".to_string()),
                tool_choice: Some(ToolChoice::Mode(ToolChoiceMode::Required)),
                reasoning: Some(ReasoningConfig {
                    effort: Some(ReasoningEffort::Low),
                    summary: None,
                }),
                ..Default::default()
            },
            None,
        )
        .unwrap();

        assert_eq!(
            result.value.tool_choice,
            Some(AnthropicToolChoice::Auto {
                disable_parallel_tool_use: None,
            })
        );
        assert!(result.warnings.iter().any(|warning| {
            warning.field == "tool_choice"
                && warning.action == WarningAction::Changed
                && warning.message
                    == "Anthropic extended thinking is not compatible with tool_choice any/tool; mapped to auto"
        }));
    }

    #[test]
    fn specific_tool_choice_with_adaptive_thinking_maps_to_auto_with_warning() {
        let result = AnthropicRequest::from_open_responses(
            OpenResponsesRequest {
                model: "gpt-5".to_string(),
                input: OpenResponsesInput::Text("hi".to_string()),
                tool_choice: Some(ToolChoice::Specific(SpecificToolChoice::Custom {
                    name: "lookup".to_string(),
                })),
                reasoning: Some(ReasoningConfig {
                    effort: None,
                    summary: Some(ReasoningSummary::Concise),
                }),
                ..Default::default()
            },
            None,
        )
        .unwrap();

        assert_eq!(
            result.value.tool_choice,
            Some(AnthropicToolChoice::Auto {
                disable_parallel_tool_use: None,
            })
        );
        assert!(result.warnings.iter().any(|warning| {
            warning.field == "tool_choice"
                && warning.action == WarningAction::Changed
                && warning.message
                    == "Anthropic extended thinking is not compatible with tool_choice any/tool; mapped to auto"
        }));
    }

    #[test]
    fn prompt_cache_retention_none_maps_to_ephemeral_no_ttl() {
        let cc = convert_open_responses_prompt_cache_retention_to_anthropic(None);
        assert_eq!(cc.kind, "ephemeral");
        assert_eq!(cc.ttl, None);
    }

    #[test]
    fn prompt_cache_retention_in_memory_maps_to_ephemeral_no_ttl() {
        let cc = convert_open_responses_prompt_cache_retention_to_anthropic(Some("in-memory"));
        assert_eq!(cc.kind, "ephemeral");
        assert_eq!(cc.ttl, None);
    }

    #[test]
    fn prompt_cache_retention_24h_maps_to_ephemeral_1h_ttl() {
        let cc = convert_open_responses_prompt_cache_retention_to_anthropic(Some("24h"));
        assert_eq!(cc.kind, "ephemeral");
        assert_eq!(cc.ttl, Some("1h".to_string()));
    }

    #[test]
    fn or_to_am_always_injects_cache_control() {
        let result = AnthropicRequest::from_open_responses(
            OpenResponsesRequest {
                model: "test".to_string(),
                input: OpenResponsesInput::Text("hi".to_string()),
                ..Default::default()
            },
            None,
        )
        .unwrap();

        assert_eq!(
            result.value.cache_control,
            Some(CacheControl {
                kind: "ephemeral".to_string(),
                ttl: None,
            })
        );
    }

    #[test]
    fn or_to_am_24h_retention_maps_to_1h_ttl() {
        let result = AnthropicRequest::from_open_responses(
            OpenResponsesRequest {
                model: "test".to_string(),
                input: OpenResponsesInput::Text("hi".to_string()),
                prompt_cache_retention: Some("24h".to_string()),
                ..Default::default()
            },
            None,
        )
        .unwrap();

        assert_eq!(
            result.value.cache_control,
            Some(CacheControl {
                kind: "ephemeral".to_string(),
                ttl: Some("1h".to_string()),
            })
        );
    }

    fn text_msg(role: AnthropicRole, text: &str) -> AnthropicMessage {
        AnthropicMessage {
            role,
            content: AnthropicMessageContent::Text(text.into()),
        }
    }

    #[test]
    fn placement_repair_keeps_valid_mid_conv_system() {
        // user, system, assistant -> all valid, unchanged.
        let mut messages = vec![
            text_msg(AnthropicRole::User, "q"),
            text_msg(AnthropicRole::System, "rule"),
            text_msg(AnthropicRole::Assistant, "a"),
        ];
        let mut system_blocks = Vec::new();
        let mut ctx = ConversionCtx::new();
        validate_and_repair_mid_conv_system_placement(&mut messages, &mut system_blocks, &mut ctx);
        assert_eq!(messages.len(), 3);
        assert_eq!(messages[1].role, AnthropicRole::System);
        assert!(system_blocks.is_empty());
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn placement_repair_hoists_and_merges_user_neighbors() {
        // user, system, user -> invalid (followed by user); hoist + merge.
        let mut messages = vec![
            text_msg(AnthropicRole::User, "first"),
            text_msg(AnthropicRole::System, "rule"),
            text_msg(AnthropicRole::User, "second"),
        ];
        let mut system_blocks = Vec::new();
        let mut ctx = ConversionCtx::new();
        validate_and_repair_mid_conv_system_placement(&mut messages, &mut system_blocks, &mut ctx);
        assert_eq!(messages.len(), 1);
        assert_eq!(messages[0].role, AnthropicRole::User);
        match &messages[0].content {
            AnthropicMessageContent::Blocks(blocks) => assert_eq!(blocks.len(), 2),
            other => panic!("expected merged blocks, got {other:?}"),
        }
        assert_eq!(system_blocks.len(), 1);
        assert_eq!(system_blocks[0].text, "rule");
    }

    #[test]
    fn placement_repair_collapses_chain_of_invalid_systems() {
        // user, system, user, system, user -> all systems invalid; collapses
        // to a single user message with all three user texts.
        let mut messages = vec![
            text_msg(AnthropicRole::User, "a"),
            text_msg(AnthropicRole::System, "r1"),
            text_msg(AnthropicRole::User, "b"),
            text_msg(AnthropicRole::System, "r2"),
            text_msg(AnthropicRole::User, "c"),
        ];
        let mut system_blocks = Vec::new();
        let mut ctx = ConversionCtx::new();
        validate_and_repair_mid_conv_system_placement(&mut messages, &mut system_blocks, &mut ctx);
        assert_eq!(messages.len(), 1);
        assert_eq!(messages[0].role, AnthropicRole::User);
        match &messages[0].content {
            AnthropicMessageContent::Blocks(blocks) => assert_eq!(blocks.len(), 3),
            other => panic!("expected three merged blocks, got {other:?}"),
        }
        assert_eq!(system_blocks.len(), 2);
    }

    #[test]
    fn placement_repair_hoists_when_not_preceded_by_user() {
        // assistant(text), system, assistant -> system does not follow a user
        // turn; hoist. The two assistant turns then merge.
        let mut messages = vec![
            text_msg(AnthropicRole::Assistant, "x"),
            text_msg(AnthropicRole::System, "rule"),
            text_msg(AnthropicRole::Assistant, "y"),
        ];
        let mut system_blocks = Vec::new();
        let mut ctx = ConversionCtx::new();
        validate_and_repair_mid_conv_system_placement(&mut messages, &mut system_blocks, &mut ctx);
        assert_eq!(messages.len(), 1);
        assert_eq!(messages[0].role, AnthropicRole::Assistant);
        assert_eq!(system_blocks.len(), 1);
    }
}
