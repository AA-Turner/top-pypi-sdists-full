use serde::Deserialize;

use super::common::StopReason;
use super::error::ApiError;
use super::response::MessageResponse;

#[derive(Debug, Deserialize, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum StreamEvent {
    MessageStart {
        message: MessageResponse,
    },
    ContentBlockStart {
        index: u32,
        content_block: StreamContentBlock,
    },
    Ping,
    ContentBlockDelta {
        index: u32,
        delta: ContentDelta,
    },
    ContentBlockStop {
        index: u32,
    },
    MessageDelta {
        delta: MessageDelta,
        usage: DeltaUsage,
    },
    MessageStop,
    Error {
        error: ApiError,
    },
}

#[derive(Debug, Deserialize, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum StreamContentBlock {
    /// Regular text content block
    Text { text: String },

    /// Tool use content block (for tool invocations)
    ToolUse { id: String, name: String },

    /// Servert tool use (for built-in tools like web search)
    ServerToolUse { id: String, name: String },

    /// Extended thinking content block
    Thinking { thinking: String, signature: String },
}

#[derive(Debug, Deserialize, Clone)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ContentDelta {
    /// Text content delta for text blocks
    TextDelta { text: String },

    /// JSON input delta for tool_use blocks
    InputJsonDelta { partial_json: String },

    /// Thinking text delta for thinking blocks
    ThinkingDelta { thinking: String },

    /// Signature delta for thinking blocks
    SignatureDelta { signature: String },
}

#[derive(Debug, Deserialize, Clone)]
pub struct MessageDelta {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stop_reason: Option<StopReason>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stop_sequence: Option<String>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct DeltaUsage {
    pub output_tokens: u32,
}
