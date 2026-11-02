use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;
use crate::traits::DecomposeToStream;

struct SequenceCounter(u64);

impl SequenceCounter {
    fn new() -> Self {
        Self(0)
    }

    #[must_use]
    fn next(&mut self) -> u64 {
        let current = self.0;
        self.0 += 1;
        current
    }
}

impl DecomposeToStream for OpenResponsesResponse {
    type Event = OpenResponsesStreamEvent;

    fn decompose_to_stream(
        mut self,
    ) -> Result<ConversionResult<Vec<OpenResponsesStreamEvent>>, ConversionError> {
        let mut seq = SequenceCounter::new();
        let mut events = Vec::new();

        // Emit ResponseCreated and ResponseInProgress with a skeleton response
        // (empty output, in_progress status, no usage).
        let skeleton = OpenResponsesResponse {
            status: ResponseStatus::InProgress,
            output: vec![],
            usage: None,
            completed_at: None,
            error: None,
            incomplete_details: None,
            ..self.clone()
        };

        events.push(OpenResponsesStreamEvent::ResponseCreated {
            sequence_number: seq.next(),
            response: skeleton.clone(),
        });
        events.push(OpenResponsesStreamEvent::ResponseInProgress {
            sequence_number: seq.next(),
            response: skeleton,
        });

        // Emit events for each output item.
        for (output_index, item) in self.output.iter().enumerate() {
            let output_index = output_index as u64;
            emit_output_item_events(&mut events, &mut seq, output_index, item);
        }

        // Emit the terminal event with the full response.
        let mut warnings = Vec::new();
        let terminal = match self.status {
            ResponseStatus::Completed => OpenResponsesStreamEvent::ResponseCompleted {
                sequence_number: seq.next(),
                response: self,
            },
            ResponseStatus::Failed => OpenResponsesStreamEvent::ResponseFailed {
                sequence_number: seq.next(),
                response: self,
            },
            ResponseStatus::Incomplete => OpenResponsesStreamEvent::ResponseIncomplete {
                sequence_number: seq.next(),
                response: self,
            },
            ResponseStatus::InProgress | ResponseStatus::Queued => {
                warnings.push(crate::error::ConversionWarning {
                    field: "status".into(),
                    action: WarningAction::Changed,
                    message: format!(
                        "non-terminal status '{:?}' decomposed as response.completed",
                        self.status
                    ),
                });
                self.status = ResponseStatus::Completed;
                OpenResponsesStreamEvent::ResponseCompleted {
                    sequence_number: seq.next(),
                    response: self,
                }
            }
        };
        events.push(terminal);

        Ok(ConversionResult::with_warnings(events, warnings))
    }
}

fn emit_output_item_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item: &OutputItem,
) {
    match item {
        OutputItem::Reasoning { .. } => {
            emit_reasoning_events(events, seq, output_index, item);
        }
        OutputItem::Message {
            id,
            status: _,
            role,
            content,
        } => {
            emit_message_events(events, seq, output_index, id, *role, content, item);
        }
        OutputItem::FunctionCall {
            id,
            arguments,
            status,
            ..
        } => {
            emit_function_call_events(events, seq, output_index, id, arguments, status, item);
        }
        OutputItem::CustomToolCall {
            id, input, status, ..
        } => {
            emit_custom_tool_call_events(events, seq, output_index, id, input, status, item);
        }
        OutputItem::WebSearchCall { id, status, .. } => {
            emit_web_search_call_events(events, seq, output_index, id, status, item);
        }
        // Items without dedicated delta events: emit Added + Done only.
        OutputItem::FunctionCallOutput { .. }
        | OutputItem::CustomToolCallOutput { .. }
        | OutputItem::ToolSearchCall { .. }
        | OutputItem::ToolSearchOutput { .. } => {
            events.push(OpenResponsesStreamEvent::OutputItemAdded {
                sequence_number: seq.next(),
                output_index,
                item: item.clone(),
            });
            events.push(OpenResponsesStreamEvent::OutputItemDone {
                sequence_number: seq.next(),
                output_index,
                item: item.clone(),
            });
        }
        OutputItem::Unknown => {}
    }
}

fn emit_reasoning_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item: &OutputItem,
) {
    let OutputItem::Reasoning {
        id: item_id,
        summary,
        content,
        encrypted_content,
    } = item
    else {
        return;
    };

    // OutputItemAdded with empty summary.
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq.next(),
        output_index,
        item: OutputItem::Reasoning {
            id: item_id.to_string(),
            summary: vec![],
            content: None,
            encrypted_content: encrypted_content.clone(),
        },
    });

    // Each summary part.
    for (summary_index, part) in summary.iter().enumerate() {
        let summary_index = summary_index as u64;
        let text = content_part_text(part);

        events.push(OpenResponsesStreamEvent::ReasoningSummaryPartAdded {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            summary_index,
            part: empty_summary_part(part),
        });

        if !text.is_empty() {
            events.push(OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                sequence_number: seq.next(),
                item_id: item_id.to_string(),
                output_index,
                summary_index,
                delta: text.to_string(),
                obfuscation: None,
            });
        }

        events.push(OpenResponsesStreamEvent::ReasoningSummaryTextDone {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            summary_index,
            text: text.to_string(),
        });

        events.push(OpenResponsesStreamEvent::ReasoningSummaryPartDone {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            summary_index,
            part: part.clone(),
        });
    }

    // Reasoning content parts (if present, distinct from summary).
    if let Some(content_parts) = content {
        for (content_index, part) in content_parts.iter().enumerate() {
            let content_index = content_index as u64;
            let text = content_part_text(part);

            if !text.is_empty() {
                events.push(OpenResponsesStreamEvent::ReasoningDelta {
                    sequence_number: seq.next(),
                    item_id: item_id.to_string(),
                    output_index,
                    content_index,
                    delta: text.to_string(),
                    obfuscation: None,
                });
            }

            events.push(OpenResponsesStreamEvent::ReasoningDone {
                sequence_number: seq.next(),
                item_id: item_id.to_string(),
                output_index,
                content_index,
                text: text.to_string(),
            });
        }
    }

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq.next(),
        output_index,
        item: item.clone(),
    });
}

fn emit_message_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item_id: &str,
    role: MessageRole,
    content: &[ContentPart],
    full_item: &OutputItem,
) {
    // OutputItemAdded with empty content and in_progress status.
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq.next(),
        output_index,
        item: OutputItem::Message {
            id: item_id.to_string(),
            status: ItemStatus::InProgress,
            role,
            content: vec![],
        },
    });

    for (content_index, part) in content.iter().enumerate() {
        let content_index = content_index as u64;

        events.push(OpenResponsesStreamEvent::ContentPartAdded {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            content_index,
            part: empty_content_part(part),
        });

        match part {
            ContentPart::OutputText {
                text,
                annotations,
                logprobs,
            } => {
                if !text.is_empty() {
                    events.push(OpenResponsesStreamEvent::OutputTextDelta {
                        sequence_number: seq.next(),
                        item_id: item_id.to_string(),
                        output_index,
                        content_index,
                        delta: text.clone(),
                        logprobs: vec![],
                        obfuscation: None,
                    });
                }

                for (annotation_index, annotation) in annotations.iter().enumerate() {
                    events.push(OpenResponsesStreamEvent::OutputTextAnnotationAdded {
                        sequence_number: seq.next(),
                        item_id: item_id.to_string(),
                        output_index,
                        content_index,
                        annotation_index: annotation_index as u64,
                        annotation: Some(annotation.clone()),
                    });
                }

                events.push(OpenResponsesStreamEvent::OutputTextDone {
                    sequence_number: seq.next(),
                    item_id: item_id.to_string(),
                    output_index,
                    content_index,
                    text: text.clone(),
                    logprobs: logprobs.clone(),
                });
            }
            ContentPart::Refusal { refusal } => {
                if !refusal.is_empty() {
                    events.push(OpenResponsesStreamEvent::RefusalDelta {
                        sequence_number: seq.next(),
                        item_id: item_id.to_string(),
                        output_index,
                        content_index,
                        delta: refusal.clone(),
                    });
                }

                events.push(OpenResponsesStreamEvent::RefusalDone {
                    sequence_number: seq.next(),
                    item_id: item_id.to_string(),
                    output_index,
                    content_index,
                    refusal: refusal.clone(),
                });
            }
            // Non-output content parts in a message have no dedicated delta events.
            // They are covered by ContentPartAdded/ContentPartDone only.
            _ => {}
        }

        events.push(OpenResponsesStreamEvent::ContentPartDone {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            content_index,
            part: part.clone(),
        });
    }

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq.next(),
        output_index,
        item: full_item.clone(),
    });
}

fn emit_function_call_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item_id: &str,
    arguments: &str,
    _status: &ItemStatus,
    full_item: &OutputItem,
) {
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq.next(),
        output_index,
        item: with_in_progress_status(full_item),
    });

    if !arguments.is_empty() {
        events.push(OpenResponsesStreamEvent::FunctionCallArgumentsDelta {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            delta: arguments.to_string(),
            obfuscation: None,
        });
    }

    events.push(OpenResponsesStreamEvent::FunctionCallArgumentsDone {
        sequence_number: seq.next(),
        item_id: item_id.to_string(),
        output_index,
        arguments: arguments.to_string(),
    });

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq.next(),
        output_index,
        item: full_item.clone(),
    });
}

fn emit_custom_tool_call_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item_id: &str,
    input: &str,
    _status: &ItemStatus,
    full_item: &OutputItem,
) {
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq.next(),
        output_index,
        item: with_in_progress_status(full_item),
    });

    if !input.is_empty() {
        events.push(OpenResponsesStreamEvent::CustomToolCallInputDelta {
            sequence_number: seq.next(),
            item_id: item_id.to_string(),
            output_index,
            delta: input.to_string(),
            obfuscation: None,
        });
    }

    events.push(OpenResponsesStreamEvent::CustomToolCallInputDone {
        sequence_number: seq.next(),
        item_id: item_id.to_string(),
        output_index,
        input: input.to_string(),
    });

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq.next(),
        output_index,
        item: full_item.clone(),
    });
}

fn emit_web_search_call_events(
    events: &mut Vec<OpenResponsesStreamEvent>,
    seq: &mut SequenceCounter,
    output_index: u64,
    item_id: &str,
    status: &WebSearchCallStatus,
    full_item: &OutputItem,
) {
    events.push(OpenResponsesStreamEvent::OutputItemAdded {
        sequence_number: seq.next(),
        output_index,
        item: with_in_progress_status(full_item),
    });

    events.push(OpenResponsesStreamEvent::WebSearchCallInProgress {
        sequence_number: seq.next(),
        output_index,
        item_id: item_id.to_string(),
    });

    if matches!(
        status,
        WebSearchCallStatus::Searching | WebSearchCallStatus::Completed
    ) {
        events.push(OpenResponsesStreamEvent::WebSearchCallSearching {
            sequence_number: seq.next(),
            output_index,
            item_id: item_id.to_string(),
        });
    }

    if matches!(status, WebSearchCallStatus::Completed) {
        events.push(OpenResponsesStreamEvent::WebSearchCallCompleted {
            sequence_number: seq.next(),
            output_index,
            item_id: item_id.to_string(),
        });
    }

    events.push(OpenResponsesStreamEvent::OutputItemDone {
        sequence_number: seq.next(),
        output_index,
        item: full_item.clone(),
    });
}

// ── Helpers ──

/// Extract the text payload from any content part variant.
fn content_part_text(part: &ContentPart) -> &str {
    match part {
        ContentPart::SummaryText { text }
        | ContentPart::OutputText { text, .. }
        | ContentPart::Text { text }
        | ContentPart::ReasoningText { text }
        | ContentPart::InputText { text } => text.as_str(),
        ContentPart::Refusal { refusal } => refusal.as_str(),
        ContentPart::InputImage { .. } | ContentPart::InputFile { .. } => "",
    }
}

/// Create an empty version of a summary part (with text cleared).
fn empty_summary_part(part: &ContentPart) -> ContentPart {
    match part {
        ContentPart::SummaryText { .. } => ContentPart::SummaryText {
            text: String::new(),
        },
        ContentPart::ReasoningText { .. } => ContentPart::ReasoningText {
            text: String::new(),
        },
        other => other.clone(),
    }
}

/// Create an empty version of a content part (with text/refusal cleared).
fn empty_content_part(part: &ContentPart) -> ContentPart {
    match part {
        ContentPart::OutputText { .. } => ContentPart::OutputText {
            text: String::new(),
            annotations: vec![],
            logprobs: vec![],
        },
        ContentPart::Refusal { .. } => ContentPart::Refusal {
            refusal: String::new(),
        },
        ContentPart::SummaryText { .. } => ContentPart::SummaryText {
            text: String::new(),
        },
        ContentPart::Text { .. } => ContentPart::Text {
            text: String::new(),
        },
        ContentPart::ReasoningText { .. } => ContentPart::ReasoningText {
            text: String::new(),
        },
        ContentPart::InputText { .. } => ContentPart::InputText {
            text: String::new(),
        },
        other => other.clone(),
    }
}

/// Clone an OutputItem but set its status to InProgress.
fn with_in_progress_status(item: &OutputItem) -> OutputItem {
    match item {
        OutputItem::FunctionCall {
            id,
            call_id,
            name,
            namespace,
            arguments,
            ..
        } => OutputItem::FunctionCall {
            id: id.clone(),
            call_id: call_id.clone(),
            name: name.clone(),
            namespace: namespace.clone(),
            arguments: arguments.clone(),
            status: ItemStatus::InProgress,
        },
        OutputItem::CustomToolCall {
            id,
            call_id,
            name,
            namespace,
            input,
            ..
        } => OutputItem::CustomToolCall {
            id: id.clone(),
            call_id: call_id.clone(),
            name: name.clone(),
            namespace: namespace.clone(),
            input: input.clone(),
            status: ItemStatus::InProgress,
        },
        OutputItem::Message {
            id, role, content, ..
        } => OutputItem::Message {
            id: id.clone(),
            status: ItemStatus::InProgress,
            role: *role,
            content: content.clone(),
        },
        OutputItem::WebSearchCall { id, action, .. } => OutputItem::WebSearchCall {
            id: id.clone(),
            status: WebSearchCallStatus::InProgress,
            action: action.clone(),
        },
        other => other.clone(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::traits::CollectStream;

    fn make_response(status: ResponseStatus, output: Vec<OutputItem>) -> OpenResponsesResponse {
        OpenResponsesResponse {
            id: "resp_1".into(),
            object: "response".into(),
            created_at: 100,
            status,
            model: "gpt-5".into(),
            output,
            ..Default::default()
        }
    }

    fn assert_sequence_numbers_monotonic(events: &[OpenResponsesStreamEvent]) {
        let json = serde_json::to_value(events).expect("serialize events");
        let arr = json.as_array().expect("events is array");
        for window in arr.windows(2) {
            let a = window[0]["sequence_number"].as_u64().expect("seq a");
            let b = window[1]["sequence_number"].as_u64().expect("seq b");
            assert_eq!(b, a + 1, "sequence numbers must increment: {a} -> {b}");
        }
    }

    fn event_types(events: &[OpenResponsesStreamEvent]) -> Vec<String> {
        let json = serde_json::to_value(events).expect("serialize events");
        json.as_array()
            .unwrap()
            .iter()
            .map(|e| e["type"].as_str().unwrap().to_string())
            .collect()
    }

    #[test]
    fn decompose_empty_response() {
        let events = make_response(ResponseStatus::Completed, vec![])
            .decompose_to_stream()
            .expect("ok")
            .value;

        assert_eq!(
            event_types(&events),
            vec![
                "response.created",
                "response.in_progress",
                "response.completed"
            ]
        );
        assert_sequence_numbers_monotonic(&events);
    }

    #[test]
    fn decompose_message_with_text() {
        let events = make_response(
            ResponseStatus::Completed,
            vec![OutputItem::Message {
                id: "msg_0".into(),
                status: ItemStatus::Completed,
                role: MessageRole::Assistant,
                content: vec![ContentPart::OutputText {
                    text: "hello world".into(),
                    annotations: vec![],
                    logprobs: vec![],
                }],
            }],
        )
        .decompose_to_stream()
        .expect("ok")
        .value;

        assert_sequence_numbers_monotonic(&events);

        // OutputItemAdded has in_progress status and empty content.
        match &events[2] {
            OpenResponsesStreamEvent::OutputItemAdded { item, .. } => match item {
                OutputItem::Message {
                    status, content, ..
                } => {
                    assert_eq!(*status, ItemStatus::InProgress);
                    assert!(content.is_empty());
                }
                other => panic!("expected Message, got {other:?}"),
            },
            other => panic!("expected OutputItemAdded, got {other:?}"),
        }

        // OutputTextDelta carries the full text.
        assert!(matches!(
            &events[4],
            OpenResponsesStreamEvent::OutputTextDelta { delta, .. } if delta == "hello world"
        ));
    }

    #[test]
    fn decompose_function_call_has_in_progress_added() {
        let events = make_response(
            ResponseStatus::Completed,
            vec![OutputItem::FunctionCall {
                id: "fc_0".into(),
                call_id: "call_1".into(),
                name: "lookup".into(),
                namespace: None,
                arguments: "{\"q\":\"x\"}".into(),
                status: ItemStatus::Completed,
            }],
        )
        .decompose_to_stream()
        .expect("ok")
        .value;

        assert_sequence_numbers_monotonic(&events);

        // OutputItemAdded should have InProgress status.
        match &events[2] {
            OpenResponsesStreamEvent::OutputItemAdded { item, .. } => match item {
                OutputItem::FunctionCall { status, .. } => {
                    assert_eq!(*status, ItemStatus::InProgress);
                }
                other => panic!("expected FunctionCall, got {other:?}"),
            },
            other => panic!("expected OutputItemAdded, got {other:?}"),
        }
    }

    #[test]
    fn decompose_reasoning_summary_indices() {
        let events = make_response(
            ResponseStatus::Completed,
            vec![OutputItem::Reasoning {
                id: "rs_0".into(),
                summary: vec![
                    ContentPart::SummaryText {
                        text: "First".into(),
                    },
                    ContentPart::SummaryText {
                        text: "Second".into(),
                    },
                ],
                content: None,
                encrypted_content: None,
            }],
        )
        .decompose_to_stream()
        .expect("ok")
        .value;

        let summary_deltas: Vec<_> = events
            .iter()
            .filter_map(|e| match e {
                OpenResponsesStreamEvent::ReasoningSummaryTextDelta {
                    summary_index,
                    delta,
                    ..
                } => Some((*summary_index, delta.as_str())),
                _ => None,
            })
            .collect();
        assert_eq!(summary_deltas, vec![(0, "First"), (1, "Second")]);
    }

    #[test]
    fn decompose_empty_text_skips_delta() {
        let events = make_response(
            ResponseStatus::Completed,
            vec![OutputItem::Message {
                id: "msg_0".into(),
                status: ItemStatus::Completed,
                role: MessageRole::Assistant,
                content: vec![ContentPart::OutputText {
                    text: String::new(),
                    annotations: vec![],
                    logprobs: vec![],
                }],
            }],
        )
        .decompose_to_stream()
        .expect("ok")
        .value;

        assert!(
            !events
                .iter()
                .any(|e| matches!(e, OpenResponsesStreamEvent::OutputTextDelta { .. }))
        );
    }

    #[test]
    fn decompose_empty_arguments_skips_delta_but_emits_done() {
        let events = make_response(
            ResponseStatus::Completed,
            vec![OutputItem::FunctionCall {
                id: "fc_0".into(),
                call_id: "call_1".into(),
                name: "noop".into(),
                namespace: None,
                arguments: String::new(),
                status: ItemStatus::Completed,
            }],
        )
        .decompose_to_stream()
        .expect("ok")
        .value;

        assert!(!events.iter().any(|e| matches!(
            e,
            OpenResponsesStreamEvent::FunctionCallArgumentsDelta { .. }
        )));
        assert!(events.iter().any(|e| matches!(
            e,
            OpenResponsesStreamEvent::FunctionCallArgumentsDone { .. }
        )));
    }

    #[test]
    fn decompose_terminal_event_matches_status() {
        for (status, expected_type) in [
            (ResponseStatus::Completed, "response.completed"),
            (ResponseStatus::Incomplete, "response.incomplete"),
            (ResponseStatus::Failed, "response.failed"),
        ] {
            let events = make_response(status, vec![])
                .decompose_to_stream()
                .expect("ok")
                .value;
            let last_type = event_types(&events).pop().unwrap();
            assert_eq!(last_type, expected_type, "status={status:?}");
        }
    }

    #[test]
    fn round_trip_collect_after_decompose() {
        let original = OpenResponsesResponse {
            usage: Some(Usage {
                input_tokens: 10,
                output_tokens: 20,
                total_tokens: 30,
                input_tokens_details: None,
                output_tokens_details: None,
            }),
            ..make_response(
                ResponseStatus::Completed,
                vec![
                    OutputItem::Reasoning {
                        id: "rs_0".into(),
                        summary: vec![
                            ContentPart::SummaryText {
                                text: "step 1".into(),
                            },
                            ContentPart::SummaryText {
                                text: "step 2".into(),
                            },
                        ],
                        content: None,
                        encrypted_content: Some("enc".into()),
                    },
                    OutputItem::Message {
                        id: "msg_0".into(),
                        status: ItemStatus::Completed,
                        role: MessageRole::Assistant,
                        content: vec![
                            ContentPart::OutputText {
                                text: "hello".into(),
                                annotations: vec![Annotation::UrlCitation {
                                    url: "https://example.com".into(),
                                    title: "Ex".into(),
                                    start_index: 0,
                                    end_index: 5,
                                }],
                                logprobs: vec![],
                            },
                            ContentPart::Refusal {
                                refusal: "no".into(),
                            },
                        ],
                    },
                    OutputItem::FunctionCall {
                        id: "fc_0".into(),
                        call_id: "call_1".into(),
                        name: "lookup".into(),
                        namespace: None,
                        arguments: "{}".into(),
                        status: ItemStatus::Completed,
                    },
                ],
            )
        };

        let events = original
            .clone()
            .decompose_to_stream()
            .expect("decompose")
            .value;
        let collected = OpenResponsesResponse::collect_stream(events).expect("collect");

        assert_eq!(collected.value, original);
        assert!(collected.warnings.is_empty());
    }
}
