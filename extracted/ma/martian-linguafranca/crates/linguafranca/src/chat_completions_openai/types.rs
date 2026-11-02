use schemars::Schema;
use serde::{Deserialize, Deserializer, Serialize};
use serde_json::{Map, Value};

fn is_map_empty(map: &Map<String, Value>) -> bool {
    map.is_empty()
}

fn web_search_type_pattern(schema: &mut Schema) {
    if let Some(type_prop) = schema
        .get_mut("properties")
        .and_then(Value::as_object_mut)
        .and_then(|properties| properties.get_mut("type"))
        .and_then(Value::as_object_mut)
    {
        type_prop.remove("const");
        type_prop.insert("pattern".to_owned(), "^web_search(?:_.*)?$".into());
    }
}

// ── Cache control ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsCacheControl {
    #[serde(rename = "type")]
    pub kind: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub ttl: Option<String>,
}

// ── Content ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsContent {
    Text(String),
    Parts(Vec<ChatCompletionsContentPart>),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ChatCompletionsContentPart {
    #[serde(rename = "text")]
    Text {
        text: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        cache_control: Option<ChatCompletionsCacheControl>,
    },
    #[serde(rename = "image_url")]
    ImageUrl { image_url: ChatCompletionsImageUrl },
    #[serde(rename = "input_audio")]
    InputAudio {
        input_audio: ChatCompletionsInputAudio,
    },
    #[serde(rename = "file")]
    File { file: ChatCompletionsFileData },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsImageUrl {
    pub url: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub detail: Option<ChatCompletionsImageDetail>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsKnownImageDetail {
    Auto,
    Low,
    High,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsImageDetail {
    Known(ChatCompletionsKnownImageDetail),
    Other(String),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsInputAudio {
    pub data: String,
    pub format: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsFileData {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub file_data: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub file_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub filename: Option<String>,
}

// ── Messages ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "role")]
pub enum ChatCompletionsMessage {
    #[serde(rename = "system")]
    System {
        content: ChatCompletionsContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        name: Option<String>,
    },
    #[serde(rename = "developer")]
    Developer {
        content: ChatCompletionsContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        name: Option<String>,
    },
    #[serde(rename = "user")]
    User {
        content: ChatCompletionsContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        name: Option<String>,
    },
    #[serde(rename = "assistant")]
    Assistant {
        #[serde(skip_serializing_if = "Option::is_none")]
        content: Option<ChatCompletionsContent>,
        #[serde(skip_serializing_if = "Option::is_none")]
        name: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        tool_calls: Option<Vec<ChatCompletionsToolCall>>,
        #[serde(skip_serializing_if = "Option::is_none")]
        refusal: Option<String>,
        // Undocumented but widely supported by reasoning providers (DeepSeek, etc.)
        #[serde(skip_serializing_if = "Option::is_none")]
        reasoning_content: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        reasoning_details: Option<Vec<serde_json::Value>>,
    },
    #[serde(rename = "tool")]
    Tool {
        content: ChatCompletionsContent,
        tool_call_id: String,
    },
}

// ── Tool calls (in assistant messages) ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ChatCompletionsToolCall {
    #[serde(rename = "function")]
    Function {
        id: String,
        function: ChatCompletionsFunctionCallData,
    },
    #[serde(rename = "custom")]
    Custom {
        id: String,
        custom: ChatCompletionsCustomCallData,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsFunctionCallData {
    pub name: String,
    pub arguments: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsCustomCallData {
    pub name: String,
    pub input: String,
}

// ── Tool definitions (in request) ──

#[derive(Debug, Clone, PartialEq, Serialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ChatCompletionsTool {
    #[serde(rename = "function")]
    Function {
        function: ChatCompletionsFunctionDef,
    },
    #[serde(rename = "custom")]
    Custom {
        custom: ChatCompletionsCustomToolDef,
    },
    /// Covers `web_search`, `web_search_preview`, `web_search_preview_2025_03_11`,
    /// and any future `web_search_*` variants sent by OpenAI clients.
    /// These are OpenAI-hosted tools that most non-OpenAI backends do not support.
    #[serde(rename = "web_search")]
    #[schemars(
        title = "ChatCompletionsToolWebSearch",
        transform = web_search_type_pattern
    )]
    WebSearch {
        #[serde(skip_serializing_if = "Option::is_none")]
        search_context_size: Option<Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        user_location: Option<Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        filters: Option<Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        domains: Option<Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        search_content_types: Option<Value>,
        #[serde(flatten, skip_serializing_if = "is_map_empty")]
        extra: Map<String, Value>,
    },
}

impl<'de> Deserialize<'de> for ChatCompletionsTool {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let value = serde_json::Value::deserialize(deserializer)?;
        let type_str = value
            .get("type")
            .and_then(|v| v.as_str())
            .ok_or_else(|| serde::de::Error::missing_field("type"))?;

        if type_str == "web_search" || type_str.starts_with("web_search_") {
            #[derive(Deserialize)]
            struct WebSearchInner {
                #[serde(rename = "type")]
                _kind: String,
                search_context_size: Option<Value>,
                user_location: Option<Value>,
                filters: Option<Value>,
                domains: Option<Value>,
                search_content_types: Option<Value>,
                #[serde(flatten)]
                extra: Map<String, Value>,
            }

            let inner: WebSearchInner =
                serde_json::from_value(value).map_err(serde::de::Error::custom)?;
            return Ok(ChatCompletionsTool::WebSearch {
                search_context_size: inner.search_context_size,
                user_location: inner.user_location,
                filters: inner.filters,
                domains: inner.domains,
                search_content_types: inner.search_content_types,
                extra: inner.extra,
            });
        }

        // Re-deserialize the remaining variants through the derived path.
        #[derive(Deserialize)]
        #[serde(tag = "type")]
        enum Inner {
            #[serde(rename = "function")]
            Function {
                function: ChatCompletionsFunctionDef,
            },
            #[serde(rename = "custom")]
            Custom {
                custom: ChatCompletionsCustomToolDef,
            },
        }
        match serde_json::from_value::<Inner>(value).map_err(serde::de::Error::custom)? {
            Inner::Function { function } => Ok(ChatCompletionsTool::Function { function }),
            Inner::Custom { custom } => Ok(ChatCompletionsTool::Custom { custom }),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsFunctionDef {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub parameters: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub strict: Option<bool>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsCustomToolDef {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    // Two possible object shapes depending on format type; passed through opaquely
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format: Option<serde_json::Value>,
}

// ── Tool choice ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsToolChoice {
    // "none" | "auto" | "required"
    Mode(String),
    AllowedTools(ChatCompletionsAllowedToolChoice),
    Function(ChatCompletionsNamedToolChoice),
    Custom(ChatCompletionsNamedToolChoiceCustom),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsAllowedToolChoice {
    #[serde(rename = "type")]
    pub kind: String, // "allowed_tools"
    pub allowed_tools: ChatCompletionsAllowedTools,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsAllowedTools {
    pub mode: String, // "auto" | "required"
    pub tools: Vec<serde_json::Value>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsNamedToolChoice {
    #[serde(rename = "type")]
    pub kind: String, // "function"
    pub function: ChatCompletionsNamedToolChoiceFunction,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsNamedToolChoiceFunction {
    pub name: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsNamedToolChoiceCustom {
    #[serde(rename = "type")]
    pub kind: String, // "custom"
    pub custom: ChatCompletionsNamedToolChoiceCustomData,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsNamedToolChoiceCustomData {
    pub name: String,
}

// ── Response format ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ChatCompletionsResponseFormat {
    #[serde(rename = "text")]
    Text,
    #[serde(rename = "json_object")]
    JsonObject,
    #[serde(rename = "json_schema")]
    JsonSchema {
        json_schema: ChatCompletionsJsonSchemaConfig,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsJsonSchemaConfig {
    pub name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub schema: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub strict: Option<bool>,
}

// ── Stop sequences ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsStop {
    Single(String),
    Multiple(Vec<String>),
}

// ── Finish reason ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsFinishReason {
    Stop,
    Length,
    ToolCalls,
    ContentFilter,
    Error,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsReasoningEffort {
    None,
    Minimal,
    Low,
    Medium,
    High,
    Xhigh,
    Max,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsReasoningSummary {
    Auto,
    Concise,
    Detailed,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsReasoningConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub effort: Option<ChatCompletionsReasoningEffort>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub summary: Option<ChatCompletionsReasoningSummary>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsReasoning {
    Config(ChatCompletionsReasoningConfig),
    Enabled(bool),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsVerbosity {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ChatCompletionsKnownServiceTier {
    Auto,
    Default,
    Flex,
    Scale,
    Priority,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ChatCompletionsServiceTier {
    Known(ChatCompletionsKnownServiceTier),
    Other(String),
}

// ── Usage ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsUsage {
    pub prompt_tokens: u64,
    pub completion_tokens: u64,
    pub total_tokens: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub prompt_tokens_details: Option<ChatCompletionsPromptTokensDetails>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub completion_tokens_details: Option<ChatCompletionsCompletionTokensDetails>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsPromptTokensDetails {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cached_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_write_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub audio_tokens: Option<u64>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsCompletionTokensDetails {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub reasoning_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub audio_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub accepted_prediction_tokens: Option<u64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub rejected_prediction_tokens: Option<u64>,
}

// ── Audio output ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsAudioOutput {
    pub id: String,
    pub data: String,
    pub expires_at: u64,
    pub transcript: String,
}

// ── Annotations ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ChatCompletionsAnnotation {
    #[serde(rename = "url_citation")]
    UrlCitation {
        url_citation: ChatCompletionsUrlCitation,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsUrlCitation {
    pub url: String,
    pub title: String,
    pub start_index: u64,
    pub end_index: u64,
}

// ── Stream options ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ChatCompletionsStreamOptions {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub include_usage: Option<bool>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub include_obfuscation: Option<bool>,
}
