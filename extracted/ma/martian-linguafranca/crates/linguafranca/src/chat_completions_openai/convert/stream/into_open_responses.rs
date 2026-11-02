use std::collections::BTreeMap;

use crate::chat_completions_openai::convert::mapping::{
    chat_completions_finish_reason_to_open_responses_status,
    warn_dropped_chat_completions_usage_details,
};
use crate::chat_completions_openai::stream::{
    ChatCompletionsStreamChunk, ChatCompletionsStreamDelta, ChatCompletionsStreamToolCall,
};
use crate::convert::open_responses_id::{OpenResponsesOutputItemKind, output_item_id};
use crate::convert::tool_namespace::split_tool_name;
use crate::error::{ConversionError, ConversionWarning, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;
use crate::stream::StreamTransform;

use super::accum::{
    ChatCompletionsToOpenResponsesAccum, ResponsePhase, ToolCallAccum, ToolCallKind,
};

struct PendingTerminal {
    status: ResponseStatus,
    incomplete_details: Option<IncompleteDetails>,
    error: Option<OpenResponsesError>,
}

/// Converts Chat Completions stream chunks to Open Responses stream events.
pub struct ChatCompletionsToOpenResponsesStream {
    accum: ChatCompletionsToOpenResponsesAccum,
    message_content_parts: Vec<ContentPart>,
    // Items can finish out of order; retain their assigned output_index.
    output_items: BTreeMap<u64, OutputItem>,
    reasoning_text: String,
    pending_terminal: Option<PendingTerminal>,
    pending_usage: Option<crate::chat_completions_openai::types::ChatCompletionsUsage>,
}

impl Default for ChatCompletionsToOpenResponsesStream {
    fn default() -> Self {
        Self::new()
    }
}

impl ChatCompletionsToOpenResponsesStream {
    pub fn new() -> Self {
        Self {
            accum: ChatCompletionsToOpenResponsesAccum::new(),
            message_content_parts: Vec::new(),
            output_items: BTreeMap::new(),
            reasoning_text: String::new(),
            pending_terminal: None,
            pending_usage: None,
        }
    }

    fn finalize_pending(&mut self) -> Vec<OpenResponsesStreamEvent> {
        let accum = &mut self.accum;
        let PendingTerminal {
            status,
            incomplete_details,
            error,
        } = if let Some(terminal) = self.pending_terminal.take() {
            terminal
        } else {
            accum.ctx.warn(
                "finish_reason",
                WarningAction::Dropped,
                "stream finalized without explicit terminal finish_reason; emitted response as incomplete",
            );
            PendingTerminal {
                status: ResponseStatus::Incomplete,
                incomplete_details: Some(IncompleteDetails {
                    reason: "stream_ended".into(),
                }),
                error: None,
            }
        };

        let mut events = Vec::new();
        events.extend(close_message(
            accum,
            &mut self.message_content_parts,
            &mut self.output_items,
            status,
        ));
        close_reasoning(accum, &mut self.output_items, &mut self.reasoning_text);
        events.extend(close_tool_calls(accum, &mut self.output_items, status));

        // Gateway carriers arrive after text/tool deltas. Hold reasoning completion
        // until finalization so output_item.done includes the replay carrier.
        if let Some(carrier) = accum.reasoning_encrypted_content.take() {
            if let Some(OutputItem::Reasoning {
                encrypted_content, ..
            }) = self
                .output_items
                .values_mut()
                .rev()
                .find(|item| matches!(item, OutputItem::Reasoning { .. }))
            {
                *encrypted_content = Some(carrier);
            } else {
                let (id, output_index) = allocate_item_id_and_output_index(
                    accum,
                    OpenResponsesOutputItemKind::Reasoning,
                    None,
                );
                let item = OutputItem::Reasoning {
                    id,
                    summary: vec![],
                    content: None,
                    encrypted_content: Some(carrier),
                };
                events.push(OpenResponsesStreamEvent::OutputItemAdded {
                    sequence_number: accum.next_sequence_number(),
                    output_index,
                    item: item.clone(),
                });
                self.output_items.insert(output_index, item);
            }
        }

        for (&output_index, item) in &self.output_items {
            let OutputItem::Reasoning { id, summary, .. } = item else {
                continue;
            };
            if let Some(part @ ContentPart::SummaryText { text }) = summary.first() {
                events.push(OpenResponsesStreamEvent::ReasoningSummaryTextDone {
                    sequence_number: accum.next_sequence_number(),
                    item_id: id.clone(),
                    output_index,
                    summary_index: 0,
                    text: text.clone(),
                });
                events.push(OpenResponsesStreamEvent::ReasoningSummaryPartDone {
                    sequence_number: accum.next_sequence_number(),
                    item_id: id.clone(),
                    output_index,
                    summary_index: 0,
                    part: part.clone(),
                });
            }
            events.push(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: accum.next_sequence_number(),
                output_index,
                item: item.clone(),
            });
        }

        let usage = self.pending_usage.take().map(|usage| {
            warn_dropped_chat_completions_usage_details(&usage, &mut accum.ctx, "usage");
            usage.into()
        });
        let response = OpenResponsesResponse {
            id: accum.response_id.clone(),
            object: "response".into(),
            created_at: accum.created_at,
            status,
            model: accum.model.clone(),
            output: std::mem::take(&mut self.output_items)
                .into_values()
                .collect(),
            usage,
            incomplete_details,
            error,
            ..Default::default()
        };

        events.push(match status {
            ResponseStatus::Completed => OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: accum.next_sequence_number(),
                response,
            },
            ResponseStatus::Incomplete => OpenResponsesStreamEvent::ResponseIncomplete {
                sequence_number: accum.next_sequence_number(),
                response,
            },
            ResponseStatus::Failed => OpenResponsesStreamEvent::ResponseFailed {
                sequence_number: accum.next_sequence_number(),
                response,
            },
            ResponseStatus::InProgress | ResponseStatus::Queued => {
                OpenResponsesStreamEvent::ResponseCompleted {
                    sequence_number: accum.next_sequence_number(),
                    response,
                }
            }
        });

        accum.phase = ResponsePhase::TerminalEmitted;
        events
    }
}

fn synthesize_error_for_finish_reason(
    finish_reason: &crate::chat_completions_openai::types::ChatCompletionsFinishReason,
) -> Option<OpenResponsesError> {
    match finish_reason {
        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ContentFilter => {
            Some(OpenResponsesError {
                code: ERROR_CODE_CONTENT_FILTER.into(),
                message: "blocked by content filter".into(),
            })
        }
        crate::chat_completions_openai::types::ChatCompletionsFinishReason::Error => {
            Some(OpenResponsesError {
                code: "error".into(),
                message: "chat completions stream ended with error finish_reason".into(),
            })
        }
        crate::chat_completions_openai::types::ChatCompletionsFinishReason::Stop
        | crate::chat_completions_openai::types::ChatCompletionsFinishReason::Length
        | crate::chat_completions_openai::types::ChatCompletionsFinishReason::ToolCalls => None,
    }
}

impl StreamTransform for ChatCompletionsToOpenResponsesStream {
    type Input = ChatCompletionsStreamChunk;
    type Output = OpenResponsesStreamEvent;

    fn transform(
        &mut self,
        input: ChatCompletionsStreamChunk,
    ) -> Result<Vec<OpenResponsesStreamEvent>, ConversionError> {
        let accum = &mut self.accum;
        let mut events = Vec::new();

        events.extend(handle_response_start(accum, &input));
        warn_unsupported_chunk_fields(accum, &input);

        let chunk_has_usage = input.usage.is_some();
        if let Some(usage) = input.usage {
            self.pending_usage = Some(usage);
        }

        if input.choices.is_empty() {
            // Providers may emit one or more empty-choices metadata chunks after the
            // terminal finish_reason before the final usage-bearing chunk. Keep the
            // terminal pending until usage arrives or flush() finalizes it.
            if self.pending_terminal.is_some() && chunk_has_usage {
                events.extend(self.finalize_pending());
            }
            return Ok(events);
        }

        if input.choices.len() > 1 {
            accum.ctx.warn(
                "choices",
                WarningAction::Dropped,
                "multiple stream choices are not representable in Open Responses stream; only the first choice was used",
            );
        }

        let choice = &input.choices[0];
        if choice.logprobs.is_some() {
            accum.ctx.warn(
                "choices[0].logprobs",
                WarningAction::Dropped,
                "choice-level logprobs are not supported in Open Responses stream",
            );
        }

        events.extend(handle_delta(
            accum,
            &choice.delta,
            &mut self.message_content_parts,
            &mut self.output_items,
            &mut self.reasoning_text,
        ));

        if let Some(finish_reason) = choice.finish_reason.clone() {
            let (status, incomplete_details) =
                chat_completions_finish_reason_to_open_responses_status(Some(
                    finish_reason.clone(),
                ));
            self.pending_terminal = Some(PendingTerminal {
                status,
                incomplete_details,
                error: synthesize_error_for_finish_reason(&finish_reason),
            });
            accum.phase = ResponsePhase::TerminalPending;
            if self.pending_usage.is_some() {
                events.extend(self.finalize_pending());
            }
        }

        Ok(events)
    }

    fn flush(&mut self) -> Result<Vec<OpenResponsesStreamEvent>, ConversionError> {
        if self.pending_terminal.is_none()
            && !matches!(
                self.accum.phase,
                ResponsePhase::InProgress | ResponsePhase::TerminalPending
            )
        {
            return Ok(vec![]);
        }

        Ok(self.finalize_pending())
    }

    fn take_warnings(&mut self) -> Vec<ConversionWarning> {
        self.accum.ctx.take_warnings()
    }
}

fn handle_response_start(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    chunk: &ChatCompletionsStreamChunk,
) -> Vec<OpenResponsesStreamEvent> {
    if accum.phase != ResponsePhase::NotStarted {
        return vec![];
    }

    accum.phase = ResponsePhase::InProgress;
    accum.response_id = chunk.id.clone();
    accum.model = chunk.model.clone();
    accum.created_at = chunk.created;

    let response = OpenResponsesResponse {
        id: accum.response_id.clone(),
        object: "response".into(),
        created_at: accum.created_at,
        status: ResponseStatus::InProgress,
        model: accum.model.clone(),
        output: vec![],
        ..Default::default()
    };

    vec![
        OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: accum.next_sequence_number(),
            response: response.clone(),
        },
        OpenResponsesStreamEvent::ResponseInProgress {
            sequence_number: accum.next_sequence_number(),
            response,
        },
    ]
}

fn handle_delta(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    delta: &ChatCompletionsStreamDelta,
    message_content_parts: &mut Vec<ContentPart>,
    output_items: &mut BTreeMap<u64, OutputItem>,
    reasoning_text: &mut String,
) -> Vec<OpenResponsesStreamEvent> {
    let mut events = Vec::new();

    if delta
        .role
        .as_deref()
        .is_some_and(|role| role != "assistant")
    {
        accum.ctx.warn(
            "choices[0].delta.role",
            WarningAction::Changed,
            "non-assistant delta role is not valid in Open Responses stream and was coerced to assistant",
        );
    }

    if let Some(encrypted_content) = delta.reasoning_details.as_ref().and_then(|details| {
        details
            .iter()
            .filter(|detail| detail["type"] == "reasoning.encrypted")
            .find_map(|detail| {
                detail["data"]
                    .as_str()
                    .or_else(|| detail["encrypted_content"].as_str())
            })
    }) {
        accum.reasoning_encrypted_content = Some(encrypted_content.to_owned());
    } else if delta
        .reasoning_details
        .as_ref()
        .is_some_and(|details| !details.is_empty())
    {
        accum.ctx.warn(
            "choices[0].delta.reasoning_details",
            WarningAction::Dropped,
            "reasoning_details without a supported reasoning.encrypted carrier are not representable in Open Responses",
        );
    }

    if let Some(content) = &delta.content
        && !content.is_empty()
    {
        close_reasoning(accum, output_items, reasoning_text);
        events.extend(open_message_if_needed(accum));
        events.extend(open_text_part_if_needed(accum));

        accum.text_part.accumulated_text.push_str(content);
        events.push(OpenResponsesStreamEvent::OutputTextDelta {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index: accum.text_part.content_index,
            delta: content.clone(),
            logprobs: vec![],
            obfuscation: None,
        });
    }

    if let Some(refusal) = &delta.refusal
        && !refusal.is_empty()
    {
        close_reasoning(accum, output_items, reasoning_text);
        events.extend(open_message_if_needed(accum));
        events.extend(open_refusal_part_if_needed(accum));

        accum.refusal_part.accumulated_text.push_str(refusal);
        events.push(OpenResponsesStreamEvent::RefusalDelta {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index: accum.refusal_part.content_index,
            delta: refusal.clone(),
        });
    }

    if let Some(reasoning_delta) = &delta.reasoning_content
        && !reasoning_delta.is_empty()
    {
        events.extend(close_message(
            accum,
            message_content_parts,
            output_items,
            ResponseStatus::InProgress,
        ));
        events.extend(open_reasoning_if_needed(accum));

        reasoning_text.push_str(reasoning_delta);
        events.push(OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.reasoning_item_id.clone(),
            output_index: accum.reasoning_output_index,
            summary_index: accum.reasoning_summary_index,
            delta: reasoning_delta.clone(),
            obfuscation: None,
        });
    }

    if let Some(tool_calls) = &delta.tool_calls {
        events.extend(close_message(
            accum,
            message_content_parts,
            output_items,
            ResponseStatus::InProgress,
        ));
        close_reasoning(accum, output_items, reasoning_text);
        for (index, tool_call) in tool_calls.iter().enumerate() {
            accum
                .ctx
                .push(format!("choices[0].delta.tool_calls[{index}]"));
            events.extend(handle_tool_call_delta(accum, tool_call));
            accum.ctx.pop();
        }
    }

    events
}

fn open_responses_item_kind(kind: ToolCallKind) -> OpenResponsesOutputItemKind {
    match kind {
        ToolCallKind::Function => OpenResponsesOutputItemKind::FunctionCall,
        ToolCallKind::Custom => OpenResponsesOutputItemKind::CustomToolCall,
    }
}

fn ensure_tool_call_item_id(response_id: &str, entry: &mut ToolCallAccum) {
    if !entry.item_id.is_empty() {
        return;
    }
    let Some(output_index) = entry.output_index else {
        return;
    };
    let Some(kind) = entry.kind else {
        return;
    };
    let source_hint = (!entry.call_id.is_empty()).then_some(entry.call_id.as_str());
    entry.item_id = output_item_id(
        response_id,
        open_responses_item_kind(kind),
        output_index,
        source_hint,
    );
}

fn ensure_tool_call_output_index(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    tool_call_index: u32,
) -> u64 {
    if let Some(output_index) = accum
        .tool_call_accums
        .get(&tool_call_index)
        .and_then(|entry| entry.output_index)
    {
        return output_index;
    }

    let output_index = accum.next_output_index();
    let entry = accum
        .tool_call_accums
        .get_mut(&tool_call_index)
        .expect("tool call accum exists");
    entry.output_index = Some(output_index);
    output_index
}

fn explicit_tool_call_kind(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    kind: Option<&str>,
) -> Option<ToolCallKind> {
    match kind {
        Some("function") => Some(ToolCallKind::Function),
        Some("custom") => Some(ToolCallKind::Custom),
        Some(other) => {
            accum.ctx.warn(
                "type",
                WarningAction::Changed,
                format!(
                    "unsupported tool call type '{other}', inferred from payload when possible"
                ),
            );
            None
        }
        None => None,
    }
}

fn initial_tool_call_kind(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    explicit_kind: Option<ToolCallKind>,
    tool_call: &ChatCompletionsStreamToolCall,
) -> Option<ToolCallKind> {
    let has_function = tool_call.function.is_some();
    let has_custom = tool_call.custom.is_some();

    match (explicit_kind, has_function, has_custom) {
        (Some(ToolCallKind::Custom), _, _) => Some(ToolCallKind::Custom),
        (Some(ToolCallKind::Function), false, true) => {
            accum.ctx.warn(
                "type",
                WarningAction::Changed,
                "tool call type=function carried only custom payload; inferred custom tool call",
            );
            Some(ToolCallKind::Custom)
        }
        (Some(ToolCallKind::Function), _, _) => Some(ToolCallKind::Function),
        (None, false, true) => Some(ToolCallKind::Custom),
        (None, true, false) => Some(ToolCallKind::Function),
        (None, true, true) => {
            accum.ctx.warn(
                "tool_call",
                WarningAction::Changed,
                "tool call delta contained both function and custom payloads; defaulted to function payload",
            );
            Some(ToolCallKind::Function)
        }
        (None, false, false) => None,
    }
}

fn tool_call_name_delta(
    tool_call: &ChatCompletionsStreamToolCall,
    kind: ToolCallKind,
) -> Option<String> {
    match kind {
        ToolCallKind::Function => tool_call
            .function
            .as_ref()
            .and_then(|delta| delta.name.clone()),
        ToolCallKind::Custom => tool_call
            .custom
            .as_ref()
            .and_then(|delta| delta.name.clone())
            .filter(|name| !name.is_empty())
            .or_else(|| {
                tool_call
                    .function
                    .as_ref()
                    .and_then(|delta| delta.name.clone())
            }),
    }
}

fn tool_call_payload_delta(
    tool_call: &ChatCompletionsStreamToolCall,
    kind: ToolCallKind,
) -> Option<String> {
    match kind {
        ToolCallKind::Function => tool_call
            .function
            .as_ref()
            .and_then(|delta| delta.arguments.clone()),
        ToolCallKind::Custom => tool_call
            .custom
            .as_ref()
            .and_then(|delta| delta.input.clone())
            .filter(|input| !input.is_empty())
            .or_else(|| {
                tool_call
                    .function
                    .as_ref()
                    .and_then(|delta| delta.arguments.clone())
            }),
    }
}

fn in_progress_tool_call_item(entry: &ToolCallAccum) -> OutputItem {
    let (namespace, name) = split_tool_name(entry.name.clone());
    match entry.kind.expect("tool call kind is known") {
        ToolCallKind::Function => OutputItem::FunctionCall {
            id: entry.item_id.clone(),
            call_id: entry.call_id.clone(),
            name,
            namespace,
            arguments: entry.payload.clone(),
            status: ItemStatus::InProgress,
        },
        ToolCallKind::Custom => OutputItem::CustomToolCall {
            id: entry.item_id.clone(),
            call_id: entry.call_id.clone(),
            name,
            namespace,
            input: entry.payload.clone(),
            status: ItemStatus::InProgress,
        },
    }
}

fn finalized_tool_call_item(entry: ToolCallAccum, status: ItemStatus) -> OutputItem {
    let (namespace, name) = split_tool_name(entry.name);
    match entry.kind.expect("tool call kind is known") {
        ToolCallKind::Function => OutputItem::FunctionCall {
            id: entry.item_id,
            call_id: entry.call_id,
            name,
            namespace,
            arguments: entry.payload,
            status,
        },
        ToolCallKind::Custom => OutputItem::CustomToolCall {
            id: entry.item_id,
            call_id: entry.call_id,
            name,
            namespace,
            input: entry.payload,
            status,
        },
    }
}

fn handle_tool_call_delta(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    tool_call: &ChatCompletionsStreamToolCall,
) -> Vec<OpenResponsesStreamEvent> {
    let mut events = Vec::new();

    accum
        .tool_call_accums
        .entry(tool_call.index)
        .or_insert_with(|| ToolCallAccum {
            output_index: None,
            item_id: String::new(),
            call_id: String::new(),
            kind: None,
            name: String::new(),
            payload: String::new(),
            output_item_added: false,
        });

    let mut maybe_added: Option<(u64, OutputItem)> = None;
    let mut maybe_payload_delta_text: Option<String> = None;
    let mut maybe_payload_delta_kind: Option<ToolCallKind> = None;
    let mut should_emit_output_item_added = false;
    let explicit_kind = explicit_tool_call_kind(accum, tool_call.kind.as_deref());
    let initial_kind = initial_tool_call_kind(accum, explicit_kind, tool_call);

    {
        let entry = accum
            .tool_call_accums
            .get_mut(&tool_call.index)
            .expect("tool call accum exists");

        if let Some(id) = &tool_call.id
            && !id.is_empty()
        {
            entry.call_id = id.clone();
        }

        if let Some(existing_kind) = entry.kind {
            if let Some(explicit_kind) = explicit_kind
                && explicit_kind != existing_kind
            {
                accum.ctx.warn(
                    "type",
                    WarningAction::Changed,
                    "tool call type changed mid-stream; kept original type",
                );
            }
        } else if let Some(kind) = initial_kind {
            entry.kind = Some(kind);
        }

        let Some(kind) = entry.kind else {
            return events;
        };

        if let Some(name) = tool_call_name_delta(tool_call, kind)
            && !name.is_empty()
        {
            entry.name.push_str(&name);
        }

        if let Some(payload_delta) = tool_call_payload_delta(tool_call, kind)
            && !payload_delta.is_empty()
        {
            entry.payload.push_str(&payload_delta);
            if entry.output_item_added {
                maybe_payload_delta_text = Some(payload_delta);
                maybe_payload_delta_kind = Some(kind);
            }
        }

        if !entry.output_item_added && !entry.name.is_empty() && !entry.call_id.is_empty() {
            should_emit_output_item_added = true;
        }
    }

    if should_emit_output_item_added {
        let output_index = ensure_tool_call_output_index(accum, tool_call.index);
        let response_id = accum.response_id.clone();
        let entry = accum
            .tool_call_accums
            .get_mut(&tool_call.index)
            .expect("tool call accum exists");
        ensure_tool_call_item_id(&response_id, entry);
        if !entry.output_item_added {
            entry.output_item_added = true;
            maybe_added = Some((output_index, in_progress_tool_call_item(entry)));
        }
    }

    if let Some(delta) = maybe_payload_delta_text {
        let (item_id, output_index) = {
            let entry = accum
                .tool_call_accums
                .get(&tool_call.index)
                .expect("tool call accum exists");
            (
                entry.item_id.clone(),
                entry
                    .output_index
                    .expect("emitted tool call has output_index"),
            )
        };
        events.push(
            match maybe_payload_delta_kind.expect("payload delta has kind") {
                ToolCallKind::Function => OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
                    sequence_number: accum.next_sequence_number(),
                    item_id,
                    output_index,
                    delta,
                    obfuscation: None,
                },
                ToolCallKind::Custom => OpenResponsesStreamEvent::CustomToolCallInputDelta {
                    sequence_number: accum.next_sequence_number(),
                    item_id,
                    output_index,
                    delta,
                    obfuscation: None,
                },
            },
        );
    }

    if let Some((output_index, item)) = maybe_added {
        events.push(OpenResponsesStreamEvent::OutputItemAdded {
            sequence_number: accum.next_sequence_number(),
            output_index,
            item,
        });
    }

    events
}

fn open_message_if_needed(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    if accum.message_is_open {
        return vec![];
    }

    accum.message_is_open = true;
    let (item_id, output_index) =
        allocate_item_id_and_output_index(accum, OpenResponsesOutputItemKind::Message, None);
    accum.message_item_id = item_id;
    accum.message_output_index = output_index;
    accum.reset_message_parts();

    vec![OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: accum.next_sequence_number(),
        output_index: accum.message_output_index,
        item: OutputItem::Message {
            id: accum.message_item_id.clone(),
            status: ItemStatus::InProgress,
            role: MessageRole::Assistant,
            content: vec![],
        },
    }]
}

fn open_text_part_if_needed(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    if accum.text_part.is_open {
        return vec![];
    }

    accum.text_part.is_open = true;
    accum.text_part.content_index = accum.next_content_index();

    vec![OpenResponsesStreamEvent::ContentPartAdded {
        sequence_number: accum.next_sequence_number(),
        item_id: accum.message_item_id.clone(),
        output_index: accum.message_output_index,
        content_index: accum.text_part.content_index,
        part: ContentPart::OutputText {
            text: String::new(),
            annotations: vec![],
            logprobs: vec![],
        },
    }]
}

fn open_refusal_part_if_needed(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    if accum.refusal_part.is_open {
        return vec![];
    }

    accum.refusal_part.is_open = true;
    accum.refusal_part.content_index = accum.next_content_index();

    vec![OpenResponsesStreamEvent::ContentPartAdded {
        sequence_number: accum.next_sequence_number(),
        item_id: accum.message_item_id.clone(),
        output_index: accum.message_output_index,
        content_index: accum.refusal_part.content_index,
        part: ContentPart::Refusal {
            refusal: String::new(),
        },
    }]
}

fn open_reasoning_if_needed(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
) -> Vec<OpenResponsesStreamEvent> {
    if accum.reasoning_is_open {
        return vec![];
    }

    accum.reasoning_is_open = true;
    let (item_id, output_index) =
        allocate_item_id_and_output_index(accum, OpenResponsesOutputItemKind::Reasoning, None);
    accum.reasoning_item_id = item_id;
    accum.reasoning_output_index = output_index;
    accum.reasoning_summary_index = 0;

    vec![
        OpenResponsesStreamEvent::OutputItemAdded {
            sequence_number: accum.next_sequence_number(),
            output_index: accum.reasoning_output_index,
            item: OutputItem::Reasoning {
                id: accum.reasoning_item_id.clone(),
                summary: vec![],
                content: None,
                encrypted_content: None,
            },
        },
        OpenResponsesStreamEvent::ReasoningSummaryPartAdded {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.reasoning_item_id.clone(),
            output_index: accum.reasoning_output_index,
            summary_index: accum.reasoning_summary_index,
            part: ContentPart::SummaryText {
                text: String::new(),
            },
        },
    ]
}

fn allocate_item_id_and_output_index(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    kind: OpenResponsesOutputItemKind,
    source_hint: Option<&str>,
) -> (String, u64) {
    let output_index = accum.next_output_index();
    (
        accum.output_item_id(kind, output_index, source_hint),
        output_index,
    )
}

fn item_status_for_open_item(status: ResponseStatus) -> ItemStatus {
    if matches!(status, ResponseStatus::Incomplete | ResponseStatus::Failed) {
        ItemStatus::Incomplete
    } else {
        ItemStatus::Completed
    }
}

fn close_message(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    message_content_parts: &mut Vec<ContentPart>,
    output_items: &mut BTreeMap<u64, OutputItem>,
    status: ResponseStatus,
) -> Vec<OpenResponsesStreamEvent> {
    if !accum.message_is_open {
        return vec![];
    }

    let mut events = Vec::new();

    if accum.text_part.is_open {
        let text = std::mem::take(&mut accum.text_part.accumulated_text);
        let content_index = accum.text_part.content_index;
        events.push(OpenResponsesStreamEvent::OutputTextDone {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index,
            text: text.clone(),
            logprobs: vec![],
        });
        events.push(OpenResponsesStreamEvent::ContentPartDone {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index,
            part: ContentPart::OutputText {
                text: text.clone(),
                annotations: vec![],
                logprobs: vec![],
            },
        });
        message_content_parts.push(ContentPart::OutputText {
            text,
            annotations: vec![],
            logprobs: vec![],
        });
    }

    if accum.refusal_part.is_open {
        let refusal = std::mem::take(&mut accum.refusal_part.accumulated_text);
        let content_index = accum.refusal_part.content_index;
        events.push(OpenResponsesStreamEvent::RefusalDone {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index,
            refusal: refusal.clone(),
        });
        events.push(OpenResponsesStreamEvent::ContentPartDone {
            sequence_number: accum.next_sequence_number(),
            item_id: accum.message_item_id.clone(),
            output_index: accum.message_output_index,
            content_index,
            part: ContentPart::Refusal {
                refusal: refusal.clone(),
            },
        });
        message_content_parts.push(ContentPart::Refusal { refusal });
    }

    let item = OutputItem::Message {
        id: accum.message_item_id.clone(),
        status: item_status_for_open_item(status),
        role: MessageRole::Assistant,
        content: std::mem::take(message_content_parts),
    };
    output_items.insert(accum.message_output_index, item.clone());

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: accum.next_sequence_number(),
        output_index: accum.message_output_index,
        item,
    });

    accum.message_is_open = false;
    accum.reset_message_parts();

    events
}

fn close_reasoning(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    output_items: &mut BTreeMap<u64, OutputItem>,
    reasoning_text: &mut String,
) {
    if !accum.reasoning_is_open {
        return;
    }

    let item = OutputItem::Reasoning {
        id: accum.reasoning_item_id.clone(),
        summary: vec![ContentPart::SummaryText {
            text: std::mem::take(reasoning_text),
        }],
        content: None,
        encrypted_content: accum.reasoning_encrypted_content.take(),
    };
    output_items.insert(accum.reasoning_output_index, item);
    accum.reasoning_is_open = false;
}

fn close_tool_calls(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    output_items: &mut BTreeMap<u64, OutputItem>,
    status: ResponseStatus,
) -> Vec<OpenResponsesStreamEvent> {
    let item_status = item_status_for_open_item(status);

    let mut accums = std::mem::take(&mut accum.tool_call_accums)
        .into_iter()
        .collect::<Vec<_>>();
    let response_id = accum.response_id.clone();
    for (_, entry) in accums.iter_mut() {
        if entry.name.is_empty() {
            continue;
        }
        if entry.output_index.is_none() {
            entry.output_index = Some(accum.next_output_index());
        }
        ensure_tool_call_item_id(&response_id, entry);
    }
    accums.sort_by_key(|(_, entry)| entry.output_index.unwrap_or(u64::MAX));

    let mut events = Vec::new();
    for (index, entry) in accums {
        let name_field = match entry.kind.unwrap_or(ToolCallKind::Function) {
            ToolCallKind::Function => "function.name",
            ToolCallKind::Custom => "custom.name",
        };
        let missing_name_message = match entry.kind.unwrap_or(ToolCallKind::Function) {
            ToolCallKind::Function => "tool call finalized without a function name",
            ToolCallKind::Custom => "tool call finalized without a custom tool name",
        };

        if entry.name.is_empty() {
            accum.ctx.push(format!("tool_calls[{index}]"));
            accum
                .ctx
                .warn(name_field, WarningAction::Dropped, missing_name_message);
            accum.ctx.pop();
            continue;
        }

        let output_index = entry
            .output_index
            .expect("named tool call has output_index");

        if !entry.output_item_added {
            events.push(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: accum.next_sequence_number(),
                output_index,
                item: in_progress_tool_call_item(&entry),
            });
        }

        match entry.kind.expect("named tool call has kind") {
            ToolCallKind::Function => {
                events.push(OpenResponsesStreamEvent::FunctionCallArgumentsDone {
                    sequence_number: accum.next_sequence_number(),
                    item_id: entry.item_id.clone(),
                    output_index,
                    arguments: entry.payload.clone(),
                });
            }
            ToolCallKind::Custom => {
                events.push(OpenResponsesStreamEvent::CustomToolCallInputDone {
                    sequence_number: accum.next_sequence_number(),
                    item_id: entry.item_id.clone(),
                    output_index,
                    input: entry.payload.clone(),
                });
            }
        }

        let item = finalized_tool_call_item(entry, item_status.clone());
        output_items.insert(output_index, item.clone());
        events.push(OpenResponsesStreamEvent::OutputItemDone {
            sequence_number: accum.next_sequence_number(),
            output_index,
            item,
        });
    }

    events
}

fn warn_unsupported_chunk_fields(
    accum: &mut ChatCompletionsToOpenResponsesAccum,
    input: &ChatCompletionsStreamChunk,
) {
    if input.system_fingerprint.is_some() && !accum.saw_system_fingerprint {
        accum.saw_system_fingerprint = true;
        accum.ctx.warn(
            "system_fingerprint",
            WarningAction::Dropped,
            "not supported in Open Responses streaming",
        );
    }
    if input.service_tier.is_some() && !accum.saw_service_tier {
        accum.saw_service_tier = true;
        accum.ctx.warn(
            "service_tier",
            WarningAction::Dropped,
            "not supported in Open Responses streaming",
        );
    }
    if input.obfuscation.is_some() && !accum.saw_obfuscation {
        accum.saw_obfuscation = true;
        accum.ctx.warn(
            "obfuscation",
            WarningAction::Dropped,
            "not supported in Open Responses streaming",
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn content_delta_emits_text_delta_immediately() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();
        let events = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![
                    crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                        index: 0,
                        delta: ChatCompletionsStreamDelta {
                            role: Some("assistant".into()),
                            content: Some("hello".into()),
                            tool_calls: None,
                            refusal: None,
                            reasoning_content: None,
                            reasoning_details: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    },
                ],
            })
            .expect("ok");

        assert!(
            events
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::OutputTextDelta { .. }))
        );
    }

    #[test]
    fn terminal_waits_through_empty_metadata_chunks_until_usage_chunk_arrives() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();
        let first = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: Some("hello".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::Stop,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");

        assert!(
            !first
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::ResponseCompleted { .. }))
        );

        let metadata = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![],
            })
            .expect("ok");

        assert!(metadata.is_empty());

        let usage = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: Some(
                    crate::chat_completions_openai::types::ChatCompletionsUsage {
                        prompt_tokens: 10,
                        completion_tokens: 5,
                        total_tokens: 15,
                        prompt_tokens_details: None,
                        completion_tokens_details: None,
                    },
                ),
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![],
            })
            .expect("ok");

        assert!(
            usage
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::ResponseCompleted { .. }))
        );
    }

    #[test]
    fn terminal_with_only_empty_metadata_chunks_after_finish_reason_finalizes_on_flush() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        let first = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: Some("hello".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::Stop,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");
        assert!(
            !first
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::ResponseCompleted { .. }))
        );

        for _ in 0..2 {
            let metadata = stream
                .transform(ChatCompletionsStreamChunk {
                    id: "chatcmpl_1".into(),
                    object: "chat.completion.chunk".into(),
                    created: 1,
                    model: "gpt-5".into(),
                    usage: None,
                    system_fingerprint: None,
                    service_tier: None,
                    obfuscation: None,
                    choices: vec![],
                })
                .expect("ok");
            assert!(metadata.is_empty());
        }

        let flushed = stream.flush().expect("ok");
        assert!(
            flushed
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::ResponseCompleted { .. }))
        );
    }

    #[test]
    fn text_reasoning_text_interleaving_defers_reasoning_completion_until_flush() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![
                    crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                        index: 0,
                        delta: ChatCompletionsStreamDelta {
                            role: Some("assistant".into()),
                            content: Some("A".into()),
                            tool_calls: None,
                            refusal: None,
                            reasoning_content: None,
                            reasoning_details: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    },
                ],
            })
            .expect("ok");

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![
                    crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                        index: 0,
                        delta: ChatCompletionsStreamDelta {
                            role: None,
                            content: None,
                            tool_calls: None,
                            refusal: None,
                            reasoning_content: Some("R".into()),
                            reasoning_details: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    },
                ],
            })
            .expect("ok");

        let events = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![
                    crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                        index: 0,
                        delta: ChatCompletionsStreamDelta {
                            role: None,
                            content: Some("B".into()),
                            tool_calls: None,
                            refusal: None,
                            reasoning_content: None,
                            reasoning_details: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    },
                ],
            })
            .expect("ok");

        assert!(
            events
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::OutputTextDelta { .. }))
        );
        assert!(!events.iter().any(|event| matches!(
            event,
            OpenResponsesStreamEvent::ReasoningSummaryTextDone { .. }
                | OpenResponsesStreamEvent::OutputItemDone {
                    item: OutputItem::Reasoning { .. },
                    ..
                }
        )));

        let events = stream.flush().expect("flush");
        let reasoning = events
            .iter()
            .find_map(|event| match event {
                OpenResponsesStreamEvent::OutputItemDone {
                    output_index: 1,
                    item: item @ OutputItem::Reasoning { .. },
                    ..
                } => Some(item),
                _ => None,
            })
            .expect("deferred reasoning done");
        let OpenResponsesStreamEvent::ResponseIncomplete { response, .. } = events.last().unwrap()
        else {
            panic!("expected incomplete response without a finish chunk");
        };
        assert_eq!(&response.output[1], reasoning);
        assert!(matches!(&response.output[0], OutputItem::Message { .. }));
        assert!(matches!(&response.output[2], OutputItem::Message { .. }));
    }

    #[test]
    fn flush_without_terminal_marks_response_incomplete_and_warns() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![
                    crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                        index: 0,
                        delta: ChatCompletionsStreamDelta {
                            role: Some("assistant".into()),
                            content: Some("hello".into()),
                            tool_calls: None,
                            refusal: None,
                            reasoning_content: None,
                            reasoning_details: None,
                        },
                        finish_reason: None,
                        logprobs: None,
                    },
                ],
            })
            .expect("ok");

        let events = stream.flush().expect("ok");
        assert!(
            events
                .iter()
                .any(|event| matches!(event, OpenResponsesStreamEvent::ResponseIncomplete { .. }))
        );

        let warnings = stream.take_warnings();
        assert!(warnings.iter().any(|warning| {
            warning.field == "finish_reason"
                && warning
                    .message
                    .contains("stream finalized without explicit terminal finish_reason")
        }));
    }

    #[test]
    fn tool_call_without_name_is_dropped_on_finalization() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        let first = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 0,
                            id: Some("call_1".into()),
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: None,
                                arguments: Some("{\"q\":\"x\"}".into()),
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
            })
            .expect("ok");
        assert_eq!(first.len(), 2);
        assert!(!first.iter().any(|event| {
            matches!(
                event,
                OpenResponsesStreamEvent::OutputItemAdded { .. }
                    | OpenResponsesStreamEvent::FunctionCallArgumentsDelta { .. }
            )
        }));

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ToolCalls,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");

        let flushed = stream.flush().expect("ok");
        assert!(!flushed.iter().any(|event| {
            matches!(
                event,
                OpenResponsesStreamEvent::OutputItemAdded { .. }
                    | OpenResponsesStreamEvent::OutputItemDone { .. }
                    | OpenResponsesStreamEvent::FunctionCallArgumentsDone { .. }
            )
        }));

        let warnings = stream.take_warnings();
        assert!(warnings.iter().any(|warning| {
            warning.field == "tool_calls[0].function.name"
                && warning
                    .message
                    .contains("tool call finalized without a function name")
        }));
    }

    #[test]
    fn tool_call_name_before_id_waits_for_call_id_before_emitting_item() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        let name_only = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 0,
                            id: None,
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: Some("lookup".into()),
                                arguments: None,
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
            })
            .expect("ok");

        assert!(!name_only.iter().any(|event| {
            matches!(
                event,
                OpenResponsesStreamEvent::OutputItemAdded {
                    item: OutputItem::FunctionCall { .. },
                    ..
                }
            )
        }));

        let with_id = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 0,
                            id: Some("call_1".into()),
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: None,
                                arguments: Some("{\"q\":\"x\"}".into()),
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
            })
            .expect("ok");

        let expected_id = output_item_id(
            "chatcmpl_1",
            OpenResponsesOutputItemKind::FunctionCall,
            0,
            Some("call_1"),
        );
        assert!(with_id.iter().any(|event| {
            matches!(event, OpenResponsesStreamEvent::OutputItemAdded {
                output_index: 0,
                item: OutputItem::FunctionCall { id, call_id, .. },
                ..
            } if id == &expected_id && call_id == "call_1")
        }));
    }

    #[test]
    fn dropped_unnamed_tool_call_does_not_consume_output_index_for_later_named_call() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        let first = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 0,
                            id: Some("call_0".into()),
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: None,
                                arguments: Some("{\"q\":\"orphan\"}".into()),
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
            })
            .expect("ok");
        assert!(!first.iter().any(|event| {
            matches!(
                event,
                OpenResponsesStreamEvent::OutputItemAdded { .. }
                    | OpenResponsesStreamEvent::FunctionCallArgumentsDelta { .. }
            )
        }));

        let second = stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 1,
                            id: Some("call_1".into()),
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: Some("lookup".into()),
                                arguments: Some("{\"q\":\"x\"}".into()),
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
            })
            .expect("ok");

        let added_output_index = second
            .iter()
            .find_map(|event| match event {
                OpenResponsesStreamEvent::OutputItemAdded {
                    output_index,
                    item: OutputItem::FunctionCall { id, .. },
                    ..
                } if id.starts_with("fc_") => Some(*output_index),
                _ => None,
            })
            .expect("named tool call added");
        assert_eq!(added_output_index, 0);

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ToolCalls,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");

        let flushed = stream.flush().expect("ok");
        let output_indices: Vec<u64> = flushed
            .iter()
            .filter_map(|event| match event {
                OpenResponsesStreamEvent::FunctionCallArgumentsDone { output_index, .. }
                | OpenResponsesStreamEvent::OutputItemDone {
                    output_index,
                    item: OutputItem::FunctionCall { .. },
                    ..
                } => Some(*output_index),
                _ => None,
            })
            .collect();
        assert!(output_indices.iter().all(|output_index| *output_index == 0));

        let response = flushed
            .iter()
            .find_map(|event| match event {
                OpenResponsesStreamEvent::ResponseCompleted { response, .. } => Some(response),
                _ => None,
            })
            .expect("response.completed event");
        assert_eq!(response.output.len(), 1);
        assert!(matches!(
            response.output.first(),
            Some(OutputItem::FunctionCall { id, .. }) if id.starts_with("fc_")
        ));
    }

    #[test]
    fn content_filter_finish_reason_synthesizes_error_and_marks_open_message_incomplete() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: Some("blocked".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::ContentFilter,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");

        let flushed = stream.flush().expect("ok");
        let response = flushed
            .iter()
            .find_map(|event| match event {
                OpenResponsesStreamEvent::ResponseFailed { response, .. } => Some(response),
                _ => None,
            })
            .expect("response.failed event");
        let error = response.error.as_ref().expect("error");
        assert_eq!(error.code, ERROR_CODE_CONTENT_FILTER);
        assert_eq!(error.message, "blocked by content filter");
        assert!(matches!(
            response.output.first(),
            Some(OutputItem::Message {
                status: ItemStatus::Incomplete,
                ..
            })
        ));
    }

    #[test]
    fn error_finish_reason_synthesizes_error_and_marks_open_tool_call_incomplete() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        stream
            .transform(ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 1,
                model: "gpt-5".into(),
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
                choices: vec![crate::chat_completions_openai::stream::ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: None,
                        tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                            index: 0,
                            id: Some("call_1".into()),
                            kind: Some("function".into()),
                            function: Some(crate::chat_completions_openai::stream::ChatCompletionsStreamFunctionDelta {
                                name: Some("lookup".into()),
                                arguments: Some("{\"q\":\"x\"}".into()),
                            }),
                            custom: None,
                        }]),
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(
                        crate::chat_completions_openai::types::ChatCompletionsFinishReason::Error,
                    ),
                    logprobs: None,
                }],
            })
            .expect("ok");

        let flushed = stream.flush().expect("ok");
        let response = flushed
            .iter()
            .find_map(|event| match event {
                OpenResponsesStreamEvent::ResponseFailed { response, .. } => Some(response),
                _ => None,
            })
            .expect("response.failed event");
        let error = response.error.as_ref().expect("error");
        assert_eq!(error.code, "error");
        assert_eq!(
            error.message,
            "chat completions stream ended with error finish_reason"
        );
        assert!(matches!(
            response.output.first(),
            Some(OutputItem::FunctionCall {
                status: ItemStatus::Incomplete,
                ..
            })
        ));
    }

    #[test]
    fn unsupported_chunk_fields_warn_once() {
        let mut stream = ChatCompletionsToOpenResponsesStream::new();

        for _ in 0..2 {
            stream
                .transform(ChatCompletionsStreamChunk {
                    id: "chatcmpl_1".into(),
                    object: "chat.completion.chunk".into(),
                    created: 1,
                    model: "gpt-5".into(),
                    usage: None,
                    system_fingerprint: Some("fp_123".into()),
                    service_tier: Some("default".into()),
                    obfuscation: Some("abc".into()),
                    choices: vec![],
                })
                .expect("ok");
        }

        let warnings = stream.take_warnings();
        let fields: Vec<&str> = warnings
            .iter()
            .map(|warning| warning.field.as_str())
            .collect();
        assert_eq!(
            fields,
            vec!["system_fingerprint", "service_tier", "obfuscation"]
        );
    }
}
