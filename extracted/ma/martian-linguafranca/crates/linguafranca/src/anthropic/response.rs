use serde::{Deserialize, Serialize};

use super::types::*;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicResponse {
    pub id: String,
    #[serde(rename = "type")]
    pub kind: String,
    pub role: AnthropicRole,
    pub model: String,
    pub content: Vec<AnthropicOutputContentBlock>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stop_reason: Option<AnthropicStopReason>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub stop_sequence: Option<String>,
    pub usage: AnthropicUsage,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub container: Option<AnthropicContainer>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub service_tier: Option<AnthropicServiceTier>,
}
