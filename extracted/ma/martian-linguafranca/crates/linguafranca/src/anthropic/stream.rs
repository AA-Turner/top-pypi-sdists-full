use serde::{Deserialize, Serialize};

use super::response::AnthropicResponse;
use super::types::*;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicStreamEvent {
    #[serde(rename = "message_start")]
    MessageStart { message: AnthropicResponse },
    #[serde(rename = "content_block_start")]
    ContentBlockStart {
        index: u64,
        content_block: AnthropicOutputContentBlock,
    },
    #[serde(rename = "content_block_delta")]
    ContentBlockDelta {
        index: u64,
        delta: AnthropicStreamDelta,
    },
    #[serde(rename = "content_block_stop")]
    ContentBlockStop { index: u64 },
    #[serde(rename = "message_delta")]
    MessageDelta {
        delta: AnthropicMessageDelta,
        #[serde(skip_serializing_if = "Option::is_none")]
        usage: Option<AnthropicUsage>,
    },
    #[serde(rename = "message_stop")]
    MessageStop,
    #[serde(rename = "ping")]
    Ping,
    #[serde(rename = "error")]
    Error { error: AnthropicStreamError },
    #[schemars(title = "AnthropicStreamUnknownEvent")]
    #[serde(other)]
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicStreamDelta {
    #[serde(rename = "text_delta")]
    TextDelta { text: String },
    #[serde(rename = "input_json_delta")]
    InputJsonDelta { partial_json: String },
    #[serde(rename = "citations_delta")]
    CitationsDelta { citation: AnthropicCitation },
    #[serde(rename = "thinking_delta")]
    ThinkingDelta { thinking: String },
    #[serde(rename = "signature_delta")]
    SignatureDelta { signature: String },
    #[schemars(title = "AnthropicStreamUnknownDelta")]
    #[serde(other)]
    Unknown,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicMessageDelta {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stop_reason: Option<AnthropicStopReason>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stop_sequence: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicStreamError {
    #[serde(rename = "type")]
    pub kind: String,
    pub message: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_unknown_event_as_unknown() {
        let raw = r#"{
            "type": "new_event",
            "payload": {"ignored": true}
        }"#;
        let event: AnthropicStreamEvent = serde_json::from_str(raw).unwrap();
        assert_eq!(event, AnthropicStreamEvent::Unknown);
    }

    #[test]
    fn parses_unknown_delta_as_unknown() {
        let raw = r#"{
            "type": "new_delta",
            "payload": {"ignored": true}
        }"#;
        let delta: AnthropicStreamDelta = serde_json::from_str(raw).unwrap();
        assert_eq!(delta, AnthropicStreamDelta::Unknown);
    }
}
