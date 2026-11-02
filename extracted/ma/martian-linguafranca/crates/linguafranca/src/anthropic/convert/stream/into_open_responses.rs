use super::accum::{
    AnthropicMessagesToOpenResponsesAccum, CurrentBlock, PendingTextCitation, PendingToolSearch,
};
use crate::anthropic::convert::helpers::*;
use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::stream::*;
use crate::anthropic::types::*;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::open_responses_id::OpenResponsesOutputItemKind;
use crate::convert::tool_namespace::{split_tool_name, tool_references_from_flat_names};
use crate::error::{ConversionError, ConversionWarning, WarningAction};
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;
use crate::stream::StreamTransform;

/// Converts Anthropic Messages stream events to Open Responses stream events, one at a time.
pub struct AnthropicMessagesToOpenResponsesStream {
    accum: AnthropicMessagesToOpenResponsesAccum,
}

impl Default for AnthropicMessagesToOpenResponsesStream {
    fn default() -> Self {
        Self::new()
    }
}

impl AnthropicMessagesToOpenResponsesStream {
    pub fn new() -> Self {
        Self {
            accum: AnthropicMessagesToOpenResponsesAccum::new(),
        }
    }
}

impl StreamTransform for AnthropicMessagesToOpenResponsesStream {
    type Input = AnthropicStreamEvent;
    type Output = OpenResponsesStreamEvent;

    fn transform(
        &mut self,
        input: AnthropicStreamEvent,
    ) -> Result<Vec<OpenResponsesStreamEvent>, ConversionError> {
        let accum = &mut self.accum;
        match input {
            AnthropicStreamEvent::MessageStart { message } => {
                Ok(handle_message_start(accum, message))
            }
            AnthropicStreamEvent::ContentBlockStart {
                content_block,
                index,
            } => Ok(handle_content_block_start(accum, content_block, index)),
            AnthropicStreamEvent::ContentBlockDelta { delta, .. } => {
                Ok(handle_content_block_delta(accum, delta))
            }
            AnthropicStreamEvent::ContentBlockStop { .. } => Ok(handle_content_block_stop(accum)),
            AnthropicStreamEvent::MessageDelta { delta, usage } => {
                accum.stop_reason = delta.stop_reason;
                if let Some(usage) = usage {
                    accum.usage = Some(usage);
                }
                Ok(vec![])
            }
            AnthropicStreamEvent::MessageStop => Ok(handle_message_stop(accum)),
            // Heartbeat: preserve the wire keepalive across the rewrite (ENG-1250).
            AnthropicStreamEvent::Ping => Ok(vec![OpenResponsesStreamEvent::Keepalive {
                sequence_number: accum.next_seq(),
            }]),
            AnthropicStreamEvent::Error { error } => handle_error(accum, error),
            AnthropicStreamEvent::Unknown => {
                accum.ctx.warn(
                    "type",
                    WarningAction::Dropped,
                    "unknown Anthropic Messages stream event dropped",
                );
                Ok(vec![])
            }
        }
    }

    fn flush(&mut self) -> Result<Vec<OpenResponsesStreamEvent>, ConversionError> {
        Ok(vec![])
    }

    fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        self.accum.ctx.take_warnings()
    }
}

fn handle_message_start(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
    message: AnthropicResponse,
) -> Vec<OpenResponsesStreamEvent> {
    accum.response_id = message.id.clone();
    accum.model = message.model.clone();
    accum.service_tier = message
        .service_tier
        .and_then(|tier| ServiceTier::lossy_try_from(tier, &mut accum.ctx, "service_tier"));

    let usage = Some(message.usage.into());
    let response = build_open_responses_response_snapshot(
        message.id,
        message.model,
        ResponseStatus::InProgress,
        vec![],
        usage,
        None,
        accum.service_tier.clone(),
    );
    let seq_created = accum.next_seq();
    let seq_in_progress = accum.next_seq();
    vec![
        OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: seq_created,
            response: response.clone(),
        },
        OpenResponsesStreamEvent::ResponseInProgress {
            sequence_number: seq_in_progress,
            response,
        },
    ]
}

fn handle_content_block_start(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
    content_block: AnthropicOutputContentBlock,
    _index: u64,
) -> Vec<OpenResponsesStreamEvent> {
    let mut events = Vec::new();

    let known = match content_block {
        AnthropicOutputContentBlock::Known(known) => known,
        AnthropicOutputContentBlock::Other(_) => {
            accum.ctx.warn(
                "content_block",
                WarningAction::Dropped,
                "unknown content block type",
            );
            return vec![];
        }
    };

    match known {
        AnthropicKnownOutputContentBlock::Text { citations, .. } => {
            accum.current_block = CurrentBlock::Text;
            accum.text_buf.clear();
            accum.text_citations = citations
                .into_iter()
                .map(|citation| PendingTextCitation {
                    citation,
                    fallback_start_index: None,
                })
                .collect();

            if !accum.message_open {
                open_message(accum, &mut events);
            }

            let content_index = accum.next_content_index();
            let seq = accum.next_seq();
            events.push(OpenResponsesStreamEvent::ContentPartAdded {
                sequence_number: seq,
                item_id: accum.message_item_id.clone(),
                output_index: accum.message_output_index,
                content_index,
                part: ContentPart::OutputText {
                    text: String::new(),
                    annotations: vec![],
                    logprobs: vec![],
                },
            });
        }
        AnthropicKnownOutputContentBlock::ToolUse { id, name, .. } => {
            events.extend(close_message(accum));

            let output_index = accum.next_output_index();
            let fc_id = accum.item_id(
                OpenResponsesOutputItemKind::FunctionCall,
                output_index,
                Some(&id),
            );
            accum.args_buf.clear();
            accum.current_block = CurrentBlock::ToolUse {
                id: id.clone(),
                name: name.clone(),
                fc_id: fc_id.clone(),
                output_index,
            };
            let seq = accum.next_seq();
            let (namespace, name) = split_tool_name(name);
            events.push(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: seq,
                output_index,
                item: OutputItem::FunctionCall {
                    id: fc_id,
                    call_id: id,
                    name,
                    namespace,
                    arguments: String::new(),
                    status: ItemStatus::InProgress,
                },
            });
        }
        AnthropicKnownOutputContentBlock::Thinking { .. } => {
            events.extend(close_message(accum));

            accum.thinking_buf.clear();
            accum.signature_buf.clear();

            let output_index = accum.next_output_index();
            let rs_id = accum.item_id(OpenResponsesOutputItemKind::Reasoning, output_index, None);
            accum.current_block = CurrentBlock::Thinking {
                rs_id: rs_id.clone(),
                output_index,
            };
            let seq_added = accum.next_seq();
            events.push(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: seq_added,
                output_index,
                item: OutputItem::Reasoning {
                    id: rs_id.clone(),
                    summary: vec![],
                    content: None,
                    encrypted_content: None,
                },
            });

            let seq_part = accum.next_seq();
            events.push(OpenResponsesStreamEvent::ReasoningSummaryPartAdded {
                sequence_number: seq_part,
                item_id: rs_id,
                output_index,
                summary_index: 0,
                part: ContentPart::SummaryText {
                    text: String::new(),
                },
            });
        }
        AnthropicKnownOutputContentBlock::RedactedThinking { data } => {
            events.extend(close_message(accum));

            accum.current_block = CurrentBlock::RedactedThinking;

            let output_index = accum.next_output_index();
            let rs_id = accum.item_id(OpenResponsesOutputItemKind::Reasoning, output_index, None);
            // Inline the immediate Added/Done emission here because the
            // hash-based item id is derived from the output_index.
            let item = OutputItem::Reasoning {
                id: rs_id,
                summary: vec![],
                content: None,
                encrypted_content: Some(data),
            };
            accum.output_items.push(item.clone());
            let seq_added = accum.next_seq();
            events.push(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: seq_added,
                output_index,
                item: item.clone(),
            });
            let seq_done = accum.next_seq();
            events.push(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: seq_done,
                output_index,
                item,
            });
        }
        AnthropicKnownOutputContentBlock::ToolSearchToolResult {
            tool_use_id,
            content,
            ..
        } => {
            let (pending_id, arguments) = accum
                .pending_tool_search
                .take()
                .map(|p| (p.id, p.arguments))
                .unwrap_or_else(|| {
                    (
                        tool_use_id.clone(),
                        serde_json::Value::Object(Default::default()),
                    )
                });

            match content {
                AnthropicToolSearchToolResultContent::Error { error_code, .. } => {
                    accum.ctx.warn(
                        "tool_search_tool_result",
                        WarningAction::Changed,
                        format!("tool_search_tool_result error: {error_code}"),
                    );
                    accum.emit_item_immediate(
                        OutputItem::ToolSearchCall {
                            id: pending_id,
                            call_id: None,
                            arguments,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Incomplete,
                        },
                        &mut events,
                    );
                }
                AnthropicToolSearchToolResultContent::SearchResult { tool_references } => {
                    let tools: Vec<Tool> = tool_references_from_flat_names(
                        tool_references.into_iter().map(|r| r.tool_name),
                    );

                    accum.emit_item_immediate(
                        OutputItem::ToolSearchCall {
                            id: pending_id,
                            call_id: None,
                            arguments,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Completed,
                        },
                        &mut events,
                    );
                    accum.emit_item_immediate(
                        OutputItem::ToolSearchOutput {
                            id: format!("{tool_use_id}_output"),
                            call_id: Some(tool_use_id),
                            tools,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Completed,
                        },
                        &mut events,
                    );
                }
            }

            accum.current_block = CurrentBlock::None;
        }
        AnthropicKnownOutputContentBlock::ServerToolUse {
            id, name, input, ..
        } => {
            if name == "web_search" {
                events.extend(close_message(accum));

                let ws_id = id;
                let output_index = accum.next_output_index();
                accum.args_buf.clear();

                accum.current_block = CurrentBlock::WebSearchServerToolUse {
                    id: ws_id.clone(),
                    output_index,
                };

                // Pre-populate args_buf if input already has content (non-streaming start)
                if let Some(q) = input.get("query").and_then(|v| v.as_str())
                    && !q.is_empty()
                {
                    accum.args_buf = serde_json::json!({ "query": q }).to_string();
                }

                let in_progress_item = OutputItem::WebSearchCall {
                    id: ws_id.clone(),
                    status: WebSearchCallStatus::InProgress,
                    action: None,
                };
                accum.output_items.push(in_progress_item.clone());

                let seq_added = accum.next_seq();
                events.push(OpenResponsesStreamEvent::OutputItemAdded {
                    sequence_number: seq_added,
                    output_index,
                    item: in_progress_item,
                });
                let seq_in_progress = accum.next_seq();
                events.push(OpenResponsesStreamEvent::WebSearchCallInProgress {
                    sequence_number: seq_in_progress,
                    output_index,
                    item_id: ws_id,
                });
            } else if name.starts_with("tool_search_tool") {
                accum.args_buf.clear();
                accum.current_block = CurrentBlock::ToolSearchServerToolUse;
                accum.pending_tool_search = Some(PendingToolSearch {
                    id,
                    arguments: input,
                });
            } else {
                accum.ctx.warn(
                    "server_tool_use",
                    WarningAction::Dropped,
                    format!("unsupported server tool '{name}'"),
                );
            }
        }
        AnthropicKnownOutputContentBlock::WebSearchToolResult {
            tool_use_id,
            content,
        } => {
            let pending = accum.pending_web_search.take();
            let (ws_id, query, output_index) = match pending {
                Some(pw) => (pw.id, pw.query, pw.output_index),
                None => {
                    // Orphan result block (no preceding server_tool_use): emit
                    // the missing preamble events so the OR stream stays valid.
                    let oi = accum.next_output_index();
                    let seq_added = accum.next_seq();
                    events.push(OpenResponsesStreamEvent::OutputItemAdded {
                        sequence_number: seq_added,
                        output_index: oi,
                        item: OutputItem::WebSearchCall {
                            id: tool_use_id.clone(),
                            status: WebSearchCallStatus::InProgress,
                            action: None,
                        },
                    });
                    let seq_ip = accum.next_seq();
                    events.push(OpenResponsesStreamEvent::WebSearchCallInProgress {
                        sequence_number: seq_ip,
                        output_index: oi,
                        item_id: tool_use_id.clone(),
                    });
                    let seq_searching = accum.next_seq();
                    events.push(OpenResponsesStreamEvent::WebSearchCallSearching {
                        sequence_number: seq_searching,
                        output_index: oi,
                        item_id: tool_use_id.clone(),
                    });
                    (tool_use_id, None, oi)
                }
            };

            accum.current_block = CurrentBlock::WebSearchToolResult;

            let (status, sources) = convert_web_search_results(content, &mut accum.ctx);

            let seq_completed = accum.next_seq();
            events.push(OpenResponsesStreamEvent::WebSearchCallCompleted {
                sequence_number: seq_completed,
                output_index,
                item_id: ws_id.clone(),
            });

            let item = OutputItem::WebSearchCall {
                id: ws_id,
                status,
                action: Some(WebSearchAction::Search {
                    query,
                    queries: vec![],
                    sources,
                }),
            };
            if let Ok(index) = usize::try_from(output_index)
                && let Some(slot) = accum.output_items.get_mut(index)
            {
                *slot = item.clone();
            } else {
                accum.output_items.push(item.clone());
            }

            let seq_done = accum.next_seq();
            events.push(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: seq_done,
                output_index,
                item,
            });
        }
    }

    events
}

fn citation_kind(citation: &AnthropicCitation) -> &'static str {
    match citation {
        AnthropicCitation::CharLocation { .. } => "char_location",
        AnthropicCitation::PageLocation { .. } => "page_location",
        AnthropicCitation::ContentBlockLocation { .. } => "content_block_location",
        AnthropicCitation::WebSearchResultLocation { .. } => "web_search_result_location",
        AnthropicCitation::SearchResultLocation { .. } => "search_result_location",
    }
}

fn current_block_kind(block: &CurrentBlock) -> &'static str {
    match block {
        CurrentBlock::None => "none",
        CurrentBlock::Text => "text",
        CurrentBlock::ToolUse { .. } => "tool_use",
        CurrentBlock::Thinking { .. } => "thinking",
        CurrentBlock::RedactedThinking => "redacted_thinking",
        CurrentBlock::WebSearchServerToolUse { .. } => "server_tool_use(web_search)",
        CurrentBlock::WebSearchToolResult => "web_search_tool_result",
        CurrentBlock::ToolSearchServerToolUse => "server_tool_use(tool_search)",
    }
}

fn handle_content_block_delta(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
    delta: AnthropicStreamDelta,
) -> Vec<OpenResponsesStreamEvent> {
    match delta {
        AnthropicStreamDelta::TextDelta { text } => {
            accum.text_buf.push_str(&text);
            let seq = accum.next_seq();
            vec![OpenResponsesStreamEvent::OutputTextDelta {
                sequence_number: seq,
                item_id: accum.message_item_id.clone(),
                output_index: accum.message_output_index,
                content_index: accum.content_index.saturating_sub(1),
                delta: text,
                logprobs: vec![],
                obfuscation: None,
            }]
        }
        AnthropicStreamDelta::InputJsonDelta { partial_json } => match &accum.current_block {
            CurrentBlock::ToolUse {
                fc_id,
                output_index,
                ..
            } => {
                let fc_id = fc_id.clone();
                let output_index = *output_index;
                accum.args_buf.push_str(&partial_json);
                let seq = accum.next_seq();
                vec![OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
                    sequence_number: seq,
                    item_id: fc_id,
                    output_index,
                    delta: partial_json,
                    obfuscation: None,
                }]
            }
            CurrentBlock::WebSearchServerToolUse { .. } | CurrentBlock::ToolSearchServerToolUse => {
                accum.args_buf.push_str(&partial_json);
                vec![]
            }
            _ => vec![],
        },
        AnthropicStreamDelta::CitationsDelta { citation } => {
            if !matches!(accum.current_block, CurrentBlock::Text) {
                accum.ctx.warn(
                    "content_block_delta",
                    WarningAction::Dropped,
                    format!(
                        "citations_delta ({}) received for non-text block ({}), dropped",
                        citation_kind(&citation),
                        current_block_kind(&accum.current_block)
                    ),
                );
                return vec![];
            }
            let start_index = accum.text_buf.chars().count() as u64;
            accum.text_citations.push(PendingTextCitation {
                citation,
                fallback_start_index: Some(start_index),
            });
            vec![]
        }
        AnthropicStreamDelta::ThinkingDelta { thinking } => {
            let (rs_id, output_index) = match &accum.current_block {
                CurrentBlock::Thinking {
                    rs_id,
                    output_index,
                } => (rs_id.clone(), *output_index),
                _ => return vec![],
            };
            accum.thinking_buf.push_str(&thinking);
            let seq = accum.next_seq();
            vec![OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                sequence_number: seq,
                item_id: rs_id,
                output_index,
                summary_index: 0,
                delta: thinking,
                obfuscation: None,
            }]
        }
        AnthropicStreamDelta::SignatureDelta { signature } => {
            accum.signature_buf.push_str(&signature);
            vec![]
        }
        AnthropicStreamDelta::Unknown => {
            accum.ctx.warn(
                "content_block_delta.delta.type",
                WarningAction::Dropped,
                "unknown Anthropic Messages stream delta dropped",
            );
            vec![]
        }
    }
}

fn handle_content_block_stop(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    let block = std::mem::take(&mut accum.current_block);
    match block {
        CurrentBlock::Text => {
            let text = std::mem::take(&mut accum.text_buf);
            let citations = std::mem::take(&mut accum.text_citations);
            let content_index = accum.content_index.saturating_sub(1);
            let annotations: Vec<Annotation> = citations
                .into_iter()
                .filter_map(|pending| {
                    let text_len = text.chars().count() as u64;
                    let result = convert_anthropic_messages_citation_to_open_responses(
                        pending.citation,
                        &text,
                        pending.fallback_start_index.map(|start| (start, text_len)),
                    );
                    if result.is_none() {
                        accum.ctx.warn(
                            "citation",
                            WarningAction::Dropped,
                            "non-URL citation type or no generated text span available",
                        );
                    }
                    result
                })
                .collect();

            let mut events = Vec::new();
            for (annotation_index, annotation) in annotations.iter().enumerate() {
                let seq = accum.next_seq();
                events.push(OpenResponsesStreamEvent::OutputTextAnnotationAdded {
                    sequence_number: seq,
                    item_id: accum.message_item_id.clone(),
                    output_index: accum.message_output_index,
                    content_index,
                    annotation_index: annotation_index as u64,
                    annotation: Some(annotation.clone()),
                });
            }

            accum.message_content_parts.push(ContentPart::OutputText {
                text: text.clone(),
                annotations: annotations.clone(),
                logprobs: vec![],
            });

            let seq_text_done = accum.next_seq();
            let seq_part_done = accum.next_seq();
            events.extend([
                OpenResponsesStreamEvent::OutputTextDone {
                    sequence_number: seq_text_done,
                    item_id: accum.message_item_id.clone(),
                    output_index: accum.message_output_index,
                    content_index,
                    text: text.clone(),
                    logprobs: vec![],
                },
                OpenResponsesStreamEvent::ContentPartDone {
                    sequence_number: seq_part_done,
                    item_id: accum.message_item_id.clone(),
                    output_index: accum.message_output_index,
                    content_index,
                    part: ContentPart::OutputText {
                        text,
                        annotations,
                        logprobs: vec![],
                    },
                },
            ]);
            events
        }
        CurrentBlock::ToolUse {
            id,
            name,
            fc_id,
            output_index,
        } => {
            let arguments = std::mem::take(&mut accum.args_buf);
            let (namespace, name) = split_tool_name(name);

            let item = OutputItem::FunctionCall {
                id: fc_id.clone(),
                call_id: id,
                name,
                namespace,
                arguments: arguments.clone(),
                status: ItemStatus::Completed,
            };
            accum.output_items.push(item.clone());

            let seq_args_done = accum.next_seq();
            let seq_item_done = accum.next_seq();
            vec![
                OpenResponsesStreamEvent::FunctionCallArgumentsDone {
                    sequence_number: seq_args_done,
                    item_id: fc_id.clone(),
                    output_index,
                    arguments,
                },
                OpenResponsesStreamEvent::OutputItemDone {
                    sequence_number: seq_item_done,
                    output_index,
                    item,
                },
            ]
        }
        CurrentBlock::Thinking {
            rs_id,
            output_index,
        } => {
            let thinking_text = std::mem::take(&mut accum.thinking_buf);
            let signature = std::mem::take(&mut accum.signature_buf);

            let item = OutputItem::Reasoning {
                id: rs_id.clone(),
                summary: vec![ContentPart::SummaryText {
                    text: thinking_text.clone(),
                }],
                content: None,
                encrypted_content: Some(signature),
            };
            accum.output_items.push(item.clone());

            let seq_summary_text_done = accum.next_seq();
            let seq_summary_part_done = accum.next_seq();
            let seq_item_done = accum.next_seq();
            vec![
                OpenResponsesStreamEvent::ReasoningSummaryTextDone {
                    sequence_number: seq_summary_text_done,
                    item_id: rs_id.clone(),
                    output_index,
                    summary_index: 0,
                    text: thinking_text.clone(),
                },
                OpenResponsesStreamEvent::ReasoningSummaryPartDone {
                    sequence_number: seq_summary_part_done,
                    item_id: rs_id,
                    output_index,
                    summary_index: 0,
                    part: ContentPart::SummaryText {
                        text: thinking_text,
                    },
                },
                OpenResponsesStreamEvent::OutputItemDone {
                    sequence_number: seq_item_done,
                    output_index,
                    item,
                },
            ]
        }
        CurrentBlock::WebSearchServerToolUse { id, output_index } => {
            let query_json = std::mem::take(&mut accum.args_buf);
            let query = serde_json::from_str::<serde_json::Value>(&query_json)
                .ok()
                .and_then(|v| v.get("query").and_then(|q| q.as_str()).map(String::from));

            accum.pending_web_search = Some(super::accum::PendingWebSearch {
                id: id.clone(),
                query,
                output_index,
            });

            let seq = accum.next_seq();
            vec![OpenResponsesStreamEvent::WebSearchCallSearching {
                sequence_number: seq,
                output_index,
                item_id: id,
            }]
        }
        CurrentBlock::ToolSearchServerToolUse => {
            let args_json = std::mem::take(&mut accum.args_buf);
            if let Some(pending) = &mut accum.pending_tool_search
                && let Ok(parsed) = serde_json::from_str::<serde_json::Value>(&args_json)
            {
                pending.arguments = parsed;
            }
            vec![]
        }
        CurrentBlock::RedactedThinking | CurrentBlock::WebSearchToolResult | CurrentBlock::None => {
            vec![]
        }
    }
}

fn handle_message_stop(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    let mut events = close_message(accum);

    let (status, incomplete_details) =
        convert_anthropic_messages_stop_reason_to_open_responses(accum.stop_reason.take());
    let usage = accum.usage.take().map(Usage::from);
    let output = std::mem::take(&mut accum.output_items);
    let response = build_open_responses_response_snapshot(
        accum.response_id.clone(),
        accum.model.clone(),
        status,
        output,
        usage,
        incomplete_details,
        accum.service_tier.clone(),
    );
    let seq = accum.next_seq();
    let terminal_event = match status {
        ResponseStatus::Completed => OpenResponsesStreamEvent::ResponseCompleted {
            sequence_number: seq,
            response,
        },
        ResponseStatus::Incomplete => OpenResponsesStreamEvent::ResponseIncomplete {
            sequence_number: seq,
            response,
        },
        ResponseStatus::Failed => OpenResponsesStreamEvent::ResponseFailed {
            sequence_number: seq,
            response,
        },
        _ => OpenResponsesStreamEvent::ResponseCompleted {
            sequence_number: seq,
            response,
        },
    };
    events.push(terminal_event);
    events
}

/// Opens a new Open Responses Message item.
fn open_message(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
    events: &mut Vec<OpenResponsesStreamEvent>,
) {
    let output_index = accum.next_output_index();
    accum.message_item_id = accum.item_id(OpenResponsesOutputItemKind::Message, output_index, None);
    accum.message_output_index = output_index;
    accum.content_index = 0;
    accum.message_open = true;
    accum.message_content_parts.clear();

    let seq = accum.next_seq();
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq,
        output_index: accum.message_output_index,
        item: OutputItem::Message {
            id: accum.message_item_id.clone(),
            status: ItemStatus::InProgress,
            role: MessageRole::Assistant,
            content: vec![],
        },
    });
}

fn close_message(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    if !accum.message_open {
        return vec![];
    }
    accum.message_open = false;

    let item_status = match accum.stop_reason {
        Some(AnthropicStopReason::MaxTokens) | Some(AnthropicStopReason::StopSequence) => {
            ItemStatus::Incomplete
        }
        _ => ItemStatus::Completed,
    };
    let content = std::mem::take(&mut accum.message_content_parts);
    let item = OutputItem::Message {
        id: accum.message_item_id.clone(),
        status: item_status,
        role: MessageRole::Assistant,
        content,
    };
    accum.output_items.push(item.clone());

    let seq = accum.next_seq();
    vec![OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq,
        output_index: accum.message_output_index,
        item,
    }]
}

fn handle_error(
    accum: &mut AnthropicMessagesToOpenResponsesAccum,
    error: AnthropicStreamError,
) -> Result<Vec<OpenResponsesStreamEvent>, ConversionError> {
    if accum.response_id.is_empty() {
        return Err(ConversionError::InvalidInput(format!(
            "Anthropic error before response started: {}",
            error.message
        )));
    }

    let mut events = close_message(accum);
    let output = std::mem::take(&mut accum.output_items);
    let usage = accum.usage.take().map(Usage::from);
    let mut response = build_open_responses_response_snapshot(
        accum.response_id.clone(),
        accum.model.clone(),
        ResponseStatus::Failed,
        output,
        usage,
        None,
        accum.service_tier.clone(),
    );
    response.error = Some(OpenResponsesError {
        code: error.kind,
        message: error.message,
    });
    let seq = accum.next_seq();
    events.push(OpenResponsesStreamEvent::ResponseFailed {
        sequence_number: seq,
        response,
    });
    Ok(events)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::stream::StreamTransform;

    fn make_message_start(id: &str, model: &str) -> AnthropicStreamEvent {
        AnthropicStreamEvent::MessageStart {
            message: AnthropicResponse {
                id: id.into(),
                kind: "message".into(),
                role: AnthropicRole::Assistant,
                model: model.into(),
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

    #[test]
    fn unknown_event_is_dropped_with_warning() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let events = stream.transform(AnthropicStreamEvent::Unknown).unwrap();
        assert!(events.is_empty());

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "type");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
        assert_eq!(
            warnings[0].message,
            "unknown Anthropic Messages stream event dropped"
        );
    }

    #[test]
    fn unknown_delta_is_dropped_with_warning() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let events = stream
            .transform(AnthropicStreamEvent::ContentBlockDelta {
                index: 0,
                delta: AnthropicStreamDelta::Unknown,
            })
            .unwrap();
        assert!(events.is_empty());

        let warnings = stream.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "content_block_delta.delta.type");
        assert_eq!(warnings[0].action, WarningAction::Dropped);
        assert_eq!(
            warnings[0].message,
            "unknown Anthropic Messages stream delta dropped"
        );
    }

    #[test]
    fn message_start_emits_created_and_in_progress() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let events = stream
            .transform(make_message_start("msg_1", "claude"))
            .unwrap();
        assert_eq!(events.len(), 2);
        assert!(matches!(
            &events[0],
            OpenResponsesStreamEvent::ResponseCreated { .. }
        ));
        assert!(matches!(
            &events[1],
            OpenResponsesStreamEvent::ResponseInProgress { .. }
        ));
    }

    #[test]
    fn text_block_lifecycle() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        stream
            .transform(make_message_start("msg_1", "claude"))
            .unwrap();

        let events = stream
            .transform(AnthropicStreamEvent::ContentBlockStart {
                index: 0,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::Text {
                        text: String::new(),
                        citations: vec![],
                    },
                ),
            })
            .unwrap();
        // OutputItemAdded (Message) + ContentPartAdded (OutputText)
        assert_eq!(events.len(), 2);
        assert!(matches!(
            &events[0],
            OpenResponsesStreamEvent::OutputItemAdded { .. }
        ));
        assert!(matches!(
            &events[1],
            OpenResponsesStreamEvent::ContentPartAdded { .. }
        ));

        let events = stream
            .transform(AnthropicStreamEvent::ContentBlockDelta {
                index: 0,
                delta: AnthropicStreamDelta::TextDelta {
                    text: "hello".into(),
                },
            })
            .unwrap();
        assert_eq!(events.len(), 1);
        assert!(matches!(
            &events[0],
            OpenResponsesStreamEvent::OutputTextDelta { delta, .. } if delta == "hello"
        ));

        let events = stream
            .transform(AnthropicStreamEvent::ContentBlockStop { index: 0 })
            .unwrap();
        // OutputTextDone + ContentPartDone
        assert_eq!(events.len(), 2);
        assert!(matches!(
            &events[0],
            OpenResponsesStreamEvent::OutputTextDone { text, .. } if text == "hello"
        ));
    }

    #[test]
    fn ping_maps_to_keepalive() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let out = stream.transform(AnthropicStreamEvent::Ping).unwrap();
        assert_eq!(out.len(), 1);
        assert!(matches!(
            &out[0],
            OpenResponsesStreamEvent::Keepalive { sequence_number: 0 }
        ));
    }

    #[test]
    fn ping_after_message_start_uses_next_sequence_number() {
        // MessageStart consumes seq 0 + 1, so the Ping's Keepalive lands at seq 2.
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let prelude = stream
            .transform(make_message_start("msg_1", "claude"))
            .unwrap();
        assert_eq!(prelude.len(), 2);

        let out = stream.transform(AnthropicStreamEvent::Ping).unwrap();
        assert_eq!(out.len(), 1);
        assert!(matches!(
            &out[0],
            OpenResponsesStreamEvent::Keepalive { sequence_number: 2 }
        ));
    }

    #[test]
    fn ping_inside_thinking_block_emits_keepalive_with_correct_seq() {
        // Real ENG-1250 shape: Ping arrives mid-reasoning, between thinking
        // block_start and the first thinking_delta.
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        stream
            .transform(make_message_start("msg_1", "claude-opus-4-7"))
            .unwrap();
        let block_start = stream
            .transform(AnthropicStreamEvent::ContentBlockStart {
                index: 0,
                content_block: AnthropicOutputContentBlock::Known(
                    AnthropicKnownOutputContentBlock::Thinking {
                        thinking: String::new(),
                        signature: String::new(),
                    },
                ),
            })
            .unwrap();
        // OutputItemAdded (seq=2) + ReasoningSummaryPartAdded (seq=3).
        assert_eq!(block_start.len(), 2);

        let ping_out = stream.transform(AnthropicStreamEvent::Ping).unwrap();
        assert_eq!(ping_out.len(), 1);
        assert!(matches!(
            &ping_out[0],
            OpenResponsesStreamEvent::Keepalive { sequence_number: 4 }
        ));

        // Next reasoning delta seqs cleanly from 5 — Keepalive consumed seq 4.
        let delta_out = stream
            .transform(AnthropicStreamEvent::ContentBlockDelta {
                index: 0,
                delta: AnthropicStreamDelta::ThinkingDelta {
                    thinking: "x".into(),
                },
            })
            .unwrap();
        assert_eq!(delta_out.len(), 1);
        assert!(matches!(
            &delta_out[0],
            OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                sequence_number: 5,
                ..
            }
        ));
    }

    #[test]
    fn error_maps_to_response_failed() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        stream
            .transform(make_message_start("msg_1", "claude"))
            .unwrap();
        let events = stream
            .transform(AnthropicStreamEvent::Error {
                error: AnthropicStreamError {
                    kind: "overloaded_error".into(),
                    message: "Overloaded".into(),
                },
            })
            .unwrap();
        assert!(matches!(
            events.last(),
            Some(OpenResponsesStreamEvent::ResponseFailed { .. })
        ));
    }

    #[test]
    fn error_before_message_start_is_invalid_input() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let result = stream.transform(AnthropicStreamEvent::Error {
            error: AnthropicStreamError {
                kind: "overloaded_error".into(),
                message: "Overloaded".into(),
            },
        });
        assert!(result.is_err());
    }

    #[test]
    fn sequence_numbers_increment() {
        let mut stream = AnthropicMessagesToOpenResponsesStream::new();
        let events = stream
            .transform(make_message_start("msg_1", "claude"))
            .unwrap();
        // ResponseCreated (seq=0), ResponseInProgress (seq=1)
        match &events[0] {
            OpenResponsesStreamEvent::ResponseCreated {
                sequence_number, ..
            } => assert_eq!(*sequence_number, 0),
            _ => panic!("expected ResponseCreated"),
        }
        match &events[1] {
            OpenResponsesStreamEvent::ResponseInProgress {
                sequence_number, ..
            } => assert_eq!(*sequence_number, 1),
            _ => panic!("expected ResponseInProgress"),
        }
    }
}
