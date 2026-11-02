use serde::{Deserialize, Serialize};

use super::types::*;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsOpenAiResponse {
    pub id: String,
    pub object: String,
    pub created: u64,
    pub model: String,
    pub choices: Vec<ChatCompletionsChoice>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub usage: Option<ChatCompletionsUsage>,
    pub system_fingerprint: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub service_tier: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsChoice {
    pub index: u32,
    pub message: ChatCompletionsAssistantMessage,
    pub finish_reason: Option<ChatCompletionsFinishReason>,
    pub logprobs: Option<serde_json::Value>,
}

// Separate from ChatCompletionsMessage (input enum) because response messages
// always have role "assistant" and content is always a plain string (not parts).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsAssistantMessage {
    pub role: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub content: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub tool_calls: Option<Vec<ChatCompletionsToolCall>>,
    pub refusal: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reasoning_content: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reasoning_details: Option<Vec<serde_json::Value>>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub annotations: Vec<ChatCompletionsAnnotation>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub audio: Option<ChatCompletionsAudioOutput>,
}
