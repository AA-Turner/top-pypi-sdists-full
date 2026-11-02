use serde::{Deserialize, Serialize};

use super::response::OpenResponsesResponse;
use super::types::*;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum OpenResponsesStreamEvent {
    #[serde(rename = "response.created")]
    ResponseCreated {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },
    #[serde(rename = "response.queued")]
    ResponseQueued {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },
    #[serde(rename = "response.in_progress")]
    ResponseInProgress {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },
    #[serde(rename = "response.completed")]
    ResponseCompleted {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },
    #[serde(rename = "response.failed")]
    ResponseFailed {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },
    #[serde(rename = "response.incomplete")]
    ResponseIncomplete {
        sequence_number: u64,
        response: OpenResponsesResponse,
    },

    #[serde(rename = "response.output_item.added")]
    OutputItemAdded {
        sequence_number: u64,
        output_index: u64,
        item: OutputItem,
    },
    #[serde(rename = "response.output_item.done")]
    OutputItemDone {
        sequence_number: u64,
        output_index: u64,
        item: OutputItem,
    },

    #[serde(rename = "response.content_part.added")]
    ContentPartAdded {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        part: ContentPart,
    },
    #[serde(rename = "response.content_part.done")]
    ContentPartDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        part: ContentPart,
    },

    #[serde(rename = "response.output_text.delta")]
    OutputTextDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        delta: String,
        #[serde(default)]
        logprobs: Vec<LogProb>,
        #[serde(skip_serializing_if = "Option::is_none")]
        obfuscation: Option<String>,
    },
    #[serde(rename = "response.output_text.done")]
    OutputTextDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        text: String,
        #[serde(default)]
        logprobs: Vec<LogProb>,
    },

    #[serde(rename = "response.output_text.annotation.added")]
    OutputTextAnnotationAdded {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        annotation_index: u64,
        #[serde(skip_serializing_if = "Option::is_none")]
        annotation: Option<Annotation>,
    },

    #[serde(rename = "response.refusal.delta")]
    RefusalDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        delta: String,
    },
    #[serde(rename = "response.refusal.done")]
    RefusalDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        refusal: String,
    },

    #[serde(
        rename = "response.reasoning.delta",
        alias = "response.reasoning_text.delta"
    )]
    ReasoningDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        delta: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        obfuscation: Option<String>,
    },
    #[serde(
        rename = "response.reasoning.done",
        alias = "response.reasoning_text.done"
    )]
    ReasoningDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        content_index: u64,
        text: String,
    },

    #[serde(rename = "response.reasoning_summary_part.added")]
    ReasoningSummaryPartAdded {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        summary_index: u64,
        part: ContentPart,
    },
    #[serde(rename = "response.reasoning_summary_part.done")]
    ReasoningSummaryPartDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        summary_index: u64,
        part: ContentPart,
    },
    #[serde(rename = "response.reasoning_summary_text.delta")]
    ReasoningSummaryTextDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        summary_index: u64,
        delta: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        obfuscation: Option<String>,
    },
    #[serde(rename = "response.reasoning_summary_text.done")]
    ReasoningSummaryTextDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        summary_index: u64,
        text: String,
    },

    #[serde(rename = "response.function_call_arguments.delta")]
    FunctionCallArgumentsDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        delta: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        obfuscation: Option<String>,
    },
    #[serde(rename = "response.function_call_arguments.done")]
    FunctionCallArgumentsDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        arguments: String,
    },

    #[serde(rename = "response.custom_tool_call_input.delta")]
    CustomToolCallInputDelta {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        delta: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        obfuscation: Option<String>,
    },
    #[serde(rename = "response.custom_tool_call_input.done")]
    CustomToolCallInputDone {
        sequence_number: u64,
        item_id: String,
        output_index: u64,
        input: String,
    },
    #[serde(rename = "response.web_search_call.in_progress")]
    WebSearchCallInProgress {
        sequence_number: u64,
        output_index: u64,
        item_id: String,
    },
    #[serde(rename = "response.web_search_call.searching")]
    WebSearchCallSearching {
        sequence_number: u64,
        output_index: u64,
        item_id: String,
    },
    #[serde(rename = "response.web_search_call.completed")]
    WebSearchCallCompleted {
        sequence_number: u64,
        output_index: u64,
        item_id: String,
    },

    /// Heartbeat event sent by the provider to keep the connection alive.
    /// Maps to Anthropic Messages `ping`; dropped for Chat Completions (no equivalent).
    #[serde(rename = "keepalive")]
    Keepalive { sequence_number: u64 },

    /// Emitted when an error occurs mid-stream.
    ///
    /// See OpenAI's [Responses streaming events reference][docs].
    ///
    /// [docs]: https://developers.openai.com/api/reference/resources/responses/streaming-events
    #[serde(rename = "error")]
    // Explicit schemars title prevents a name collision with `AnthropicStreamEvent::Error`
    // when the Python codegen turns each variant into a `Model{Discriminator}` dataclass.
    #[schemars(title = "ResponsesStreamError")]
    Error {
        sequence_number: u64,
        // OpenAI marks these as required-but-nullable; accept missing too.
        #[serde(default, skip_serializing_if = "Option::is_none")]
        code: Option<String>,
        message: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        param: Option<String>,
    },

    #[schemars(title = "ResponsesStreamUnknownEvent")]
    #[serde(other)]
    Unknown,
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Exact shape from OpenAI's [Responses streaming events reference][docs].
    ///
    /// [docs]: https://developers.openai.com/api/reference/resources/responses/streaming-events
    #[test]
    fn parses_error_event_from_openai_wire_format() {
        let raw = r#"{
            "type": "error",
            "code": "ERR_SOMETHING",
            "message": "Something went wrong",
            "param": null,
            "sequence_number": 1
        }"#;
        let event: OpenResponsesStreamEvent = serde_json::from_str(raw).unwrap();
        match event {
            OpenResponsesStreamEvent::Error {
                sequence_number,
                code,
                message,
                param,
            } => {
                assert_eq!(sequence_number, 1);
                assert_eq!(code.as_deref(), Some("ERR_SOMETHING"));
                assert_eq!(message, "Something went wrong");
                assert_eq!(param, None);
            }
            other => panic!("expected Error variant, got {other:?}"),
        }
    }

    #[test]
    fn parses_error_event_with_optional_fields_missing() {
        let raw = r#"{
            "type": "error",
            "message": "boom",
            "sequence_number": 0
        }"#;
        let event: OpenResponsesStreamEvent = serde_json::from_str(raw).unwrap();
        assert!(matches!(
            event,
            OpenResponsesStreamEvent::Error {
                code: None,
                param: None,
                ..
            }
        ));
    }

    #[test]
    fn parses_unknown_event_as_unknown() {
        let raw = r#"{
            "type": "response.new_event",
            "sequence_number": 1,
            "payload": {"ignored": true}
        }"#;
        let event: OpenResponsesStreamEvent = serde_json::from_str(raw).unwrap();
        assert_eq!(event, OpenResponsesStreamEvent::Unknown);
    }

    #[test]
    fn output_text_stream_events_serialize_logprobs_when_empty() {
        let delta = serde_json::to_value(OpenResponsesStreamEvent::OutputTextDelta {
            sequence_number: 1,
            item_id: "msg_1".into(),
            output_index: 0,
            content_index: 0,
            delta: "hi".into(),
            logprobs: vec![],
            obfuscation: None,
        })
        .unwrap();
        assert_eq!(delta.get("logprobs"), Some(&serde_json::json!([])));

        let done = serde_json::to_value(OpenResponsesStreamEvent::OutputTextDone {
            sequence_number: 2,
            item_id: "msg_1".into(),
            output_index: 0,
            content_index: 0,
            text: "hi".into(),
            logprobs: vec![],
        })
        .unwrap();
        assert_eq!(done.get("logprobs"), Some(&serde_json::json!([])));
    }
}
