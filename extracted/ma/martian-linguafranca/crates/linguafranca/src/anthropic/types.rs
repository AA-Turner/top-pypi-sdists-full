use serde::{Deserialize, Serialize};

// ── Cache control ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct CacheControl {
    #[serde(rename = "type")]
    pub kind: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ttl: Option<String>,
}

// ── Citations ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicCitation {
    #[serde(rename = "char_location")]
    CharLocation {
        cited_text: String,
        document_index: u64,
        document_title: String,
        start_char_index: u64,
        end_char_index: u64,
    },
    #[serde(rename = "page_location")]
    PageLocation {
        cited_text: String,
        document_index: u64,
        document_title: String,
        start_page_number: u64,
        end_page_number: u64,
    },
    #[serde(rename = "content_block_location")]
    ContentBlockLocation {
        cited_text: String,
        document_index: u64,
        document_title: String,
        start_block_index: u64,
        end_block_index: u64,
    },
    #[serde(rename = "web_search_result_location")]
    WebSearchResultLocation {
        cited_text: String,
        encrypted_index: String,
        title: String,
        url: String,
    },
    #[serde(rename = "search_result_location")]
    SearchResultLocation {
        cited_text: String,
        search_result_index: u64,
        start_block_index: u64,
        end_block_index: u64,
        source: String,
        title: String,
    },
}

// ── Image source ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ImageSource {
    #[serde(rename = "base64")]
    Base64 { data: String, media_type: String },
    #[serde(rename = "url")]
    Url { url: String },
}

// ── Document source ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum DocumentSource {
    #[serde(rename = "base64")]
    Base64 { data: String, media_type: String },
    #[serde(rename = "text")]
    PlainText { data: String, media_type: String },
    #[serde(rename = "url")]
    Url { url: String },
    #[serde(rename = "content")]
    Content { content: AnthropicDocumentContent },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicDocumentContent {
    Text(String),
    Blocks(Vec<AnthropicInputContentBlock>),
}

// ── Citations config ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct CitationsConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub enabled: Option<bool>,
}

// ── Input content blocks ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicInputContentBlock {
    #[serde(rename = "text")]
    Text {
        text: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(skip_serializing_if = "Option::is_none")]
        citations: Option<Vec<AnthropicCitation>>,
    },
    #[serde(rename = "image")]
    Image {
        source: ImageSource,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    #[serde(rename = "tool_use")]
    ToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    #[serde(rename = "tool_result")]
    ToolResult {
        tool_use_id: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        content: Option<AnthropicToolResultContent>,
        #[serde(skip_serializing_if = "Option::is_none")]
        is_error: Option<bool>,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    #[serde(rename = "document")]
    Document {
        source: DocumentSource,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(skip_serializing_if = "Option::is_none")]
        citations: Option<CitationsConfig>,
        #[serde(skip_serializing_if = "Option::is_none")]
        context: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        title: Option<String>,
    },
    #[serde(rename = "search_result")]
    SearchResult {
        content: Vec<AnthropicSearchResultText>,
        source: String,
        title: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(skip_serializing_if = "Option::is_none")]
        citations: Option<CitationsConfig>,
    },
    #[serde(rename = "thinking")]
    Thinking { thinking: String, signature: String },
    #[serde(rename = "redacted_thinking")]
    RedactedThinking { data: String },
    #[serde(rename = "server_tool_use")]
    ServerToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    #[serde(rename = "web_search_tool_result")]
    WebSearchToolResult {
        tool_use_id: String,
        content: Vec<AnthropicWebSearchToolResultItem>,
    },
    #[serde(rename = "tool_search_tool_result")]
    ToolSearchToolResult {
        tool_use_id: String,
        content: AnthropicToolSearchToolResultContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicSearchResultText {
    pub text: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_control: Option<CacheControl>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicToolResultContent {
    Text(String),
    Blocks(Vec<AnthropicToolResultBlock>),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicToolResultBlock {
    #[serde(rename = "text")]
    Text { text: String },
    #[serde(rename = "image")]
    Image { source: ImageSource },
    #[serde(rename = "document")]
    Document {
        source: DocumentSource,
        #[serde(skip_serializing_if = "Option::is_none")]
        citations: Option<CitationsConfig>,
        #[serde(skip_serializing_if = "Option::is_none")]
        context: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        title: Option<String>,
    },
    #[serde(rename = "search_result")]
    SearchResult {
        content: Vec<AnthropicSearchResultText>,
        source: String,
        title: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        citations: Option<CitationsConfig>,
    },
    #[serde(rename = "tool_reference")]
    ToolReference { tool_name: String },
}

// ── Tool search tool result ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicToolSearchToolResultContent {
    #[serde(rename = "tool_search_tool_result_error")]
    Error {
        error_code: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        error_message: Option<String>,
    },
    #[serde(rename = "tool_search_tool_search_result")]
    SearchResult {
        tool_references: Vec<AnthropicToolReference>,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicToolReference {
    #[serde(rename = "type", default = "AnthropicToolReference::default_type")]
    pub kind: String,
    pub tool_name: String,
}

impl AnthropicToolReference {
    fn default_type() -> String {
        "tool_reference".to_string()
    }

    pub fn new(tool_name: String) -> Self {
        Self {
            kind: Self::default_type(),
            tool_name,
        }
    }
}

// ── Output content blocks ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicWebSearchToolResultItem {
    #[serde(rename = "web_search_result")]
    WebSearchResult {
        url: String,
        title: String,
        encrypted_content: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        page_age: Option<String>,
    },
    #[serde(rename = "web_search_tool_result_error")]
    Error { error_code: String },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicKnownOutputContentBlock {
    #[serde(rename = "text")]
    Text {
        text: String,
        #[serde(default, skip_serializing_if = "Vec::is_empty")]
        citations: Vec<AnthropicCitation>,
    },
    #[serde(rename = "tool_use")]
    ToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
    },
    #[serde(rename = "thinking")]
    Thinking { thinking: String, signature: String },
    #[serde(rename = "redacted_thinking")]
    RedactedThinking { data: String },
    #[serde(rename = "web_search_tool_result")]
    WebSearchToolResult {
        tool_use_id: String,
        content: Vec<AnthropicWebSearchToolResultItem>,
    },
    #[serde(rename = "server_tool_use")]
    ServerToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        caller: Option<serde_json::Value>,
    },
    #[serde(rename = "tool_search_tool_result")]
    ToolSearchToolResult {
        tool_use_id: String,
        content: AnthropicToolSearchToolResultContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
}

/// Wraps the tagged enum so unknown server tool types (code_execution_tool_result, etc.)
/// pass through as opaque JSON instead of failing deserialization.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicOutputContentBlock {
    Known(AnthropicKnownOutputContentBlock),
    Other(serde_json::Value),
}

// ── Messages ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicMessage {
    pub role: AnthropicRole,
    pub content: AnthropicMessageContent,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum AnthropicRole {
    User,
    Assistant,
    // Mid-conversation system instruction. Only honored by Claude Opus 4.8;
    // see `model_supports_mid_conversation_system`.
    System,
}

/// Whether the target model supports mid-conversation `system` messages
/// (a `{"role": "system"}` entry inside `messages`).
///
/// Per Anthropic docs this feature is available on **Claude Opus 4.8 only**
/// (Claude API and Claude Platform on AWS; not Bedrock/Vertex/Foundry).
/// For any other model the conversion must fall back to hoisting instruction
/// messages into the top-level `system` field.
pub fn model_supports_mid_conversation_system(model: &str) -> bool {
    // Match "claude-opus-4-8" and dated/suffixed variants like
    // "claude-opus-4-8-20260515", case-insensitively.
    //
    // Reject any provider-prefixed ID (containing a '/' separator): the
    // feature is unavailable on Bedrock/Vertex/Foundry, and we cannot tell a
    // supporting platform from an unsupporting one by prefix alone, so only
    // raw / Anthropic-hosted IDs are allowed to match.
    if model.contains('/') {
        return false;
    }
    let m = model.to_ascii_lowercase();
    let base = "claude-opus-4-8";
    match m.strip_prefix(base) {
        Some("") => true,
        Some(rest) => rest.starts_with('-'),
        None => false,
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicMessageContent {
    Text(String),
    Blocks(Vec<AnthropicInputContentBlock>),
}

// ── System ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicSystem {
    Text(String),
    Blocks(Vec<AnthropicSystemBlock>),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicSystemBlock {
    #[serde(rename = "type")]
    pub kind: String,
    pub text: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_control: Option<CacheControl>,
}

// ── Output config ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicOutputConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub effort: Option<AnthropicOutputEffort>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format: Option<AnthropicOutputFormat>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum AnthropicOutputEffort {
    Low,
    Medium,
    High,
    Xhigh,
    Max,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicOutputFormat {
    #[serde(rename = "json_schema")]
    JsonSchema { schema: serde_json::Value },
}

// ── Tools ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicTool {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    pub input_schema: serde_json::Value,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_control: Option<CacheControl>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub strict: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none", rename = "type")]
    pub kind: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub defer_loading: Option<bool>,
}

/// Custom tools deserialize into `Known(AnthropicTool)`;
/// server tools (bash_20250124, web_search_20250305, etc.) fall through to `Other`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicToolUnion {
    Known(AnthropicTool),
    Other(serde_json::Value),
}

// ── Tool choice ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicToolChoice {
    #[serde(rename = "auto")]
    Auto {
        #[serde(skip_serializing_if = "Option::is_none")]
        disable_parallel_tool_use: Option<bool>,
    },
    #[serde(rename = "any")]
    Any {
        #[serde(skip_serializing_if = "Option::is_none")]
        disable_parallel_tool_use: Option<bool>,
    },
    #[serde(rename = "tool")]
    Tool {
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        disable_parallel_tool_use: Option<bool>,
    },
    #[serde(rename = "none")]
    None,
}

// ── Thinking config ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum AnthropicThinkingDisplay {
    Summarized,
    Omitted,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum AnthropicThinkingConfig {
    #[serde(rename = "enabled")]
    Enabled {
        budget_tokens: u64,
        #[serde(skip_serializing_if = "Option::is_none")]
        display: Option<AnthropicThinkingDisplay>,
    },
    #[serde(rename = "disabled")]
    Disabled,
    #[serde(rename = "adaptive")]
    Adaptive {
        #[serde(skip_serializing_if = "Option::is_none")]
        display: Option<AnthropicThinkingDisplay>,
    },
}

// ── Stop reason ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum AnthropicStopReason {
    EndTurn,
    MaxTokens,
    StopSequence,
    ToolUse,
    PauseTurn,
    Refusal,
}

// ── Service tier ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum AnthropicKnownServiceTier {
    Auto,
    Standard,
    Priority,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum AnthropicServiceTier {
    Known(AnthropicKnownServiceTier),
    Other(String),
}

// ── Container ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicContainer {
    pub id: String,
    pub expires_at: String,
}

// ── Usage ──

#[derive(Debug, Clone, Default, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicUsage {
    pub input_tokens: u64,
    pub output_tokens: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub output_tokens_details: Option<AnthropicOutputTokensDetails>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_creation_input_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_read_input_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_creation: Option<AnthropicCacheCreation>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub server_tool_use: Option<AnthropicServerToolUsage>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub service_tier: Option<AnthropicServiceTier>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub inference_geo: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicOutputTokensDetails {
    pub thinking_tokens: u64,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicCacheCreation {
    pub ephemeral_5m_input_tokens: u64,
    pub ephemeral_1h_input_tokens: u64,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicServerToolUsage {
    pub web_search_requests: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub web_fetch_requests: Option<u64>,
}

// ── Metadata ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AnthropicMetadata {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub user_id: Option<String>,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn service_tier_known_roundtrips() {
        let tier: AnthropicServiceTier = serde_json::from_str("\"standard\"").unwrap();
        assert_eq!(
            tier,
            AnthropicServiceTier::Known(AnthropicKnownServiceTier::Standard)
        );
        let serialized = serde_json::to_string(&tier).unwrap();
        assert_eq!(serialized, "\"standard\"");
    }

    #[test]
    fn service_tier_unknown_roundtrips_as_other() {
        let tier: AnthropicServiceTier = serde_json::from_str("\"burst\"").unwrap();
        assert_eq!(tier, AnthropicServiceTier::Other("burst".into()));
        let serialized = serde_json::to_string(&tier).unwrap();
        assert_eq!(serialized, "\"burst\"");
    }

    #[test]
    fn output_effort_roundtrips() {
        let cases = [
            (AnthropicOutputEffort::Low, "\"low\""),
            (AnthropicOutputEffort::Medium, "\"medium\""),
            (AnthropicOutputEffort::High, "\"high\""),
            (AnthropicOutputEffort::Xhigh, "\"xhigh\""),
            (AnthropicOutputEffort::Max, "\"max\""),
        ];
        for (variant, expected_json) in cases {
            let serialized = serde_json::to_string(&variant).unwrap();
            assert_eq!(serialized, expected_json, "serializing {variant:?}");
            let deserialized: AnthropicOutputEffort = serde_json::from_str(expected_json).unwrap();
            assert_eq!(deserialized, variant, "deserializing {expected_json}");
        }
    }

    #[test]
    fn role_system_roundtrips() {
        let role: AnthropicRole = serde_json::from_str("\"system\"").unwrap();
        assert_eq!(role, AnthropicRole::System);
        assert_eq!(serde_json::to_string(&role).unwrap(), "\"system\"");
    }

    #[test]
    fn mid_conversation_system_only_on_opus_4_8() {
        // Supported: exact and dated/suffixed variants, case-insensitive.
        assert!(model_supports_mid_conversation_system("claude-opus-4-8"));
        assert!(model_supports_mid_conversation_system(
            "claude-opus-4-8-20260515"
        ));
        assert!(model_supports_mid_conversation_system("Claude-Opus-4-8"));

        // Not supported: provider-prefixed IDs. The feature is unavailable on
        // Bedrock/Vertex/Foundry, so any "<provider>/..." ID is rejected.
        assert!(!model_supports_mid_conversation_system(
            "bedrock/claude-opus-4-8"
        ));
        assert!(!model_supports_mid_conversation_system(
            "vertex/claude-opus-4-8-20260515"
        ));
        assert!(!model_supports_mid_conversation_system(
            "foundry/claude-opus-4-8"
        ));
        assert!(!model_supports_mid_conversation_system(
            "anthropic/claude-opus-4-8"
        ));

        // Not supported: other models, including near-matches.
        assert!(!model_supports_mid_conversation_system("claude-opus-4-7"));
        assert!(!model_supports_mid_conversation_system("claude-opus-4-5"));
        assert!(!model_supports_mid_conversation_system("claude-sonnet-4-6"));
        assert!(!model_supports_mid_conversation_system("claude-opus-4-80"));
        assert!(!model_supports_mid_conversation_system("gpt-5"));
        assert!(!model_supports_mid_conversation_system(""));
    }
}
