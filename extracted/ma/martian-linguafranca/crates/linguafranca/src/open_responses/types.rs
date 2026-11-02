use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// ── Enums ──

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum MessageRole {
    User,
    Assistant,
    System,
    Developer,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ItemStatus {
    InProgress,
    Completed,
    Incomplete,
}

#[derive(Debug, Clone, Copy, Default, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ResponseStatus {
    Completed,
    Failed,
    #[default]
    InProgress,
    Incomplete,
    Queued,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Truncation {
    Auto,
    Disabled,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ServiceTier {
    Auto,
    Default,
    Flex,
    Priority,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ReasoningEffort {
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
pub enum ReasoningSummary {
    Concise,
    Detailed,
    Auto,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ImageDetail {
    Low,
    High,
    Auto,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Verbosity {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum Include {
    Known(KnownInclude),
    Other(String),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub enum KnownInclude {
    #[serde(rename = "reasoning.encrypted_content")]
    ReasoningEncryptedContent,
    #[serde(rename = "message.output_text.logprobs")]
    MessageOutputTextLogprobs,
}

// ── Annotations & LogProbs ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum Annotation {
    #[serde(rename = "url_citation")]
    UrlCitation {
        url: String,
        title: String,
        start_index: u64,
        end_index: u64,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct TopLogProb {
    pub token: String,
    pub logprob: f64,
    pub bytes: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct LogProb {
    pub token: String,
    pub logprob: f64,
    pub bytes: Vec<u8>,
    pub top_logprobs: Vec<TopLogProb>,
}

// ── Input content ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum InputContentPart {
    #[serde(rename = "input_text")]
    Text { text: String },
    #[serde(rename = "output_text")]
    OutputText {
        text: String,
        #[serde(default)]
        annotations: Vec<Annotation>,
        #[serde(default)]
        logprobs: Vec<LogProb>,
    },
    #[serde(rename = "input_image")]
    Image {
        #[serde(skip_serializing_if = "Option::is_none")]
        image_url: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        detail: Option<ImageDetail>,
    },
    #[serde(rename = "input_file")]
    File {
        #[serde(skip_serializing_if = "Option::is_none")]
        filename: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        file_data: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        file_url: Option<String>,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum InputContent {
    Text(String),
    Parts(Vec<InputContentPart>),
}

// ── Output content ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum OutputContentPart {
    #[serde(rename = "output_text")]
    Text {
        text: String,
        #[serde(default)]
        annotations: Vec<Annotation>,
        #[serde(default)]
        logprobs: Vec<LogProb>,
    },
    #[serde(rename = "refusal")]
    Refusal { refusal: String },
}

// ── Content parts (union used in Message.content and Reasoning.content/summary) ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum ContentPart {
    #[serde(rename = "input_text")]
    InputText { text: String },
    #[serde(rename = "output_text")]
    OutputText {
        text: String,
        #[serde(default)]
        annotations: Vec<Annotation>,
        #[serde(default)]
        logprobs: Vec<LogProb>,
    },
    #[serde(rename = "text")]
    Text { text: String },
    #[serde(rename = "summary_text")]
    SummaryText { text: String },
    #[serde(rename = "reasoning_text")]
    ReasoningText { text: String },
    #[serde(rename = "refusal")]
    Refusal { refusal: String },
    #[serde(rename = "input_image")]
    InputImage {
        #[serde(skip_serializing_if = "Option::is_none")]
        image_url: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        detail: Option<ImageDetail>,
    },
    #[serde(rename = "input_file")]
    InputFile {
        #[serde(skip_serializing_if = "Option::is_none")]
        filename: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        file_data: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        file_url: Option<String>,
    },
}

// ── Reasoning summary (input) ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum SummaryContentType {
    SummaryText,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct SummaryContent {
    #[serde(rename = "type")]
    pub kind: SummaryContentType,
    pub text: String,
}

// ── Input items ──

#[derive(Debug, Clone, PartialEq, Serialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum InputItem {
    #[serde(rename = "message")]
    Message {
        role: MessageRole,
        content: InputContent,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ItemStatus>,
    },
    #[serde(rename = "function_call")]
    FunctionCall {
        call_id: String,
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        namespace: Option<String>,
        arguments: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ItemStatus>,
    },
    #[serde(rename = "function_call_output")]
    FunctionCallOutput {
        call_id: String,
        output: FunctionCallOutputValue,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ItemStatus>,
    },
    #[serde(rename = "custom_tool_call")]
    CustomToolCall {
        call_id: String,
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        namespace: Option<String>,
        input: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ItemStatus>,
    },
    #[serde(rename = "custom_tool_call_output")]
    CustomToolCallOutput {
        call_id: String,
        output: FunctionCallOutputValue,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ItemStatus>,
    },
    #[serde(rename = "web_search_call")]
    WebSearchCall {
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<WebSearchCallStatus>,
        #[serde(skip_serializing_if = "Option::is_none")]
        action: Option<WebSearchAction>,
    },
    #[serde(rename = "tool_search_call")]
    ToolSearchCall {
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        call_id: Option<String>,
        arguments: serde_json::Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        execution: Option<ToolSearchExecution>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ToolSearchCallStatus>,
    },
    #[serde(rename = "tool_search_output")]
    ToolSearchOutput {
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        call_id: Option<String>,
        tools: Vec<Tool>,
        #[serde(skip_serializing_if = "Option::is_none")]
        execution: Option<ToolSearchExecution>,
        #[serde(skip_serializing_if = "Option::is_none")]
        status: Option<ToolSearchCallStatus>,
    },
    #[serde(rename = "reasoning")]
    Reasoning {
        summary: Vec<SummaryContent>,
        #[serde(skip_serializing_if = "Option::is_none")]
        id: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        encrypted_content: Option<String>,
    },
    #[serde(rename = "item_reference")]
    ItemReference { id: String },
}

// Defaults to Message when "type" is absent
impl<'de> Deserialize<'de> for InputItem {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let mut value = serde_json::Value::deserialize(deserializer)?;
        if let Some(obj) = value.as_object_mut() {
            obj.entry("type").or_insert_with(|| "message".into());
        }

        #[derive(Deserialize)]
        #[serde(tag = "type")]
        enum Tagged {
            #[serde(rename = "message")]
            Message {
                role: MessageRole,
                content: InputContent,
                id: Option<String>,
                status: Option<ItemStatus>,
            },
            #[serde(rename = "function_call")]
            FunctionCall {
                call_id: String,
                name: String,
                namespace: Option<String>,
                arguments: String,
                id: Option<String>,
                status: Option<ItemStatus>,
            },
            #[serde(rename = "function_call_output")]
            FunctionCallOutput {
                call_id: String,
                output: FunctionCallOutputValue,
                id: Option<String>,
                status: Option<ItemStatus>,
            },
            #[serde(rename = "custom_tool_call")]
            CustomToolCall {
                call_id: String,
                name: String,
                namespace: Option<String>,
                input: String,
                id: Option<String>,
                status: Option<ItemStatus>,
            },
            #[serde(rename = "custom_tool_call_output")]
            CustomToolCallOutput {
                call_id: String,
                output: FunctionCallOutputValue,
                id: Option<String>,
                status: Option<ItemStatus>,
            },
            #[serde(rename = "web_search_call")]
            WebSearchCall {
                id: Option<String>,
                status: Option<WebSearchCallStatus>,
                action: Option<WebSearchAction>,
            },
            #[serde(rename = "tool_search_call")]
            ToolSearchCall {
                id: Option<String>,
                call_id: Option<String>,
                arguments: serde_json::Value,
                execution: Option<ToolSearchExecution>,
                status: Option<ToolSearchCallStatus>,
            },
            #[serde(rename = "tool_search_output")]
            ToolSearchOutput {
                id: Option<String>,
                call_id: Option<String>,
                tools: Vec<Tool>,
                execution: Option<ToolSearchExecution>,
                status: Option<ToolSearchCallStatus>,
            },
            #[serde(rename = "reasoning")]
            Reasoning {
                summary: Vec<SummaryContent>,
                id: Option<String>,
                encrypted_content: Option<String>,
            },
            #[serde(rename = "item_reference")]
            ItemReference { id: String },
        }

        match serde_json::from_value::<Tagged>(value).map_err(serde::de::Error::custom)? {
            Tagged::Message {
                role,
                content,
                id,
                status,
            } => Ok(Self::Message {
                role,
                content,
                id,
                status,
            }),
            Tagged::FunctionCall {
                call_id,
                name,
                namespace,
                arguments,
                id,
                status,
            } => Ok(Self::FunctionCall {
                call_id,
                name,
                namespace,
                arguments,
                id,
                status,
            }),
            Tagged::FunctionCallOutput {
                call_id,
                output,
                id,
                status,
            } => Ok(Self::FunctionCallOutput {
                call_id,
                output,
                id,
                status,
            }),
            Tagged::CustomToolCall {
                call_id,
                name,
                namespace,
                input,
                id,
                status,
            } => Ok(Self::CustomToolCall {
                call_id,
                name,
                namespace,
                input,
                id,
                status,
            }),
            Tagged::CustomToolCallOutput {
                call_id,
                output,
                id,
                status,
            } => Ok(Self::CustomToolCallOutput {
                call_id,
                output,
                id,
                status,
            }),
            Tagged::WebSearchCall { id, status, action } => {
                Ok(Self::WebSearchCall { id, status, action })
            }
            Tagged::ToolSearchCall {
                id,
                call_id,
                arguments,
                execution,
                status,
            } => Ok(Self::ToolSearchCall {
                id,
                call_id,
                arguments,
                execution,
                status,
            }),
            Tagged::ToolSearchOutput {
                id,
                call_id,
                tools,
                execution,
                status,
            } => Ok(Self::ToolSearchOutput {
                id,
                call_id,
                tools,
                execution,
                status,
            }),
            Tagged::Reasoning {
                summary,
                id,
                encrypted_content,
            } => Ok(Self::Reasoning {
                summary,
                id,
                encrypted_content,
            }),
            Tagged::ItemReference { id } => Ok(Self::ItemReference { id }),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum FunctionCallOutputValue {
    Text(String),
    Parts(Vec<InputContentPart>),
}

// ── Web search ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum WebSearchCallStatus {
    InProgress,
    Searching,
    Completed,
    Incomplete,
    Failed,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct WebSearchSource {
    #[serde(rename = "type")]
    pub source_type: String,
    pub url: String,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum WebSearchAction {
    #[serde(rename = "search")]
    Search {
        #[serde(skip_serializing_if = "Option::is_none")]
        query: Option<String>,
        #[serde(default, skip_serializing_if = "Vec::is_empty")]
        queries: Vec<String>,
        #[serde(default, skip_serializing_if = "Vec::is_empty")]
        sources: Vec<WebSearchSource>,
    },
    #[serde(rename = "open_page")]
    OpenPage {
        #[serde(skip_serializing_if = "Option::is_none")]
        url: Option<String>,
    },
    #[serde(rename = "find_in_page")]
    FindInPage { pattern: String, url: String },
}

// ── Tool search ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ToolSearchExecution {
    Server,
    Client,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ToolSearchCallStatus {
    InProgress,
    Completed,
    Incomplete,
}

// ── Output items ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum OutputItem {
    #[serde(rename = "message")]
    Message {
        id: String,
        status: ItemStatus,
        role: MessageRole,
        content: Vec<ContentPart>,
    },
    #[serde(rename = "function_call")]
    FunctionCall {
        id: String,
        call_id: String,
        name: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        namespace: Option<String>,
        arguments: String,
        status: ItemStatus,
    },
    #[serde(rename = "function_call_output")]
    FunctionCallOutput {
        id: String,
        call_id: String,
        output: FunctionCallOutputValue,
        status: ItemStatus,
    },
    #[serde(rename = "custom_tool_call")]
    CustomToolCall {
        id: String,
        call_id: String,
        name: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        namespace: Option<String>,
        input: String,
        status: ItemStatus,
    },
    #[serde(rename = "custom_tool_call_output")]
    CustomToolCallOutput {
        id: String,
        call_id: String,
        output: FunctionCallOutputValue,
        status: ItemStatus,
    },
    #[serde(rename = "reasoning")]
    Reasoning {
        id: String,
        summary: Vec<ContentPart>,
        #[serde(skip_serializing_if = "Option::is_none")]
        content: Option<Vec<ContentPart>>,
        #[serde(skip_serializing_if = "Option::is_none")]
        encrypted_content: Option<String>,
    },
    #[serde(rename = "web_search_call")]
    WebSearchCall {
        id: String,
        status: WebSearchCallStatus,
        #[serde(skip_serializing_if = "Option::is_none")]
        action: Option<WebSearchAction>,
    },
    #[serde(rename = "tool_search_call")]
    ToolSearchCall {
        id: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        call_id: Option<String>,
        arguments: serde_json::Value,
        #[serde(skip_serializing_if = "Option::is_none")]
        execution: Option<ToolSearchExecution>,
        status: ToolSearchCallStatus,
    },
    #[serde(rename = "tool_search_output")]
    ToolSearchOutput {
        id: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        call_id: Option<String>,
        tools: Vec<Tool>,
        #[serde(skip_serializing_if = "Option::is_none")]
        execution: Option<ToolSearchExecution>,
        status: ToolSearchCallStatus,
    },
    #[schemars(title = "OutputItemUnknown")]
    #[serde(other)]
    Unknown,
}

// ── Tools ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum SearchContextSize {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct UserLocation {
    #[serde(rename = "type")]
    pub kind: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub city: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub country: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub region: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub timezone: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct WebSearchFilters {
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub allowed_domains: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum Tool {
    #[serde(rename = "function")]
    Function {
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        description: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        parameters: Option<serde_json::Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        strict: Option<bool>,
        #[serde(skip_serializing_if = "Option::is_none")]
        defer_loading: Option<bool>,
    },
    #[serde(rename = "web_search")]
    WebSearch {
        #[serde(skip_serializing_if = "Option::is_none")]
        search_context_size: Option<SearchContextSize>,
        #[serde(skip_serializing_if = "Option::is_none")]
        user_location: Option<UserLocation>,
        #[serde(skip_serializing_if = "Option::is_none")]
        filters: Option<WebSearchFilters>,
    },
    #[serde(rename = "custom")]
    Custom {
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        description: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        format: Option<serde_json::Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        defer_loading: Option<bool>,
    },
    #[serde(rename = "tool_search")]
    ToolSearch {
        #[serde(skip_serializing_if = "Option::is_none")]
        description: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        execution: Option<ToolSearchExecution>,
        #[serde(skip_serializing_if = "Option::is_none")]
        parameters: Option<serde_json::Value>,
    },
    /// Groups function and custom tools; calls to them carry the namespace separately.
    #[serde(rename = "namespace")]
    Namespace {
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        description: Option<String>,
        tools: Vec<Tool>,
    },
}

impl<'de> Deserialize<'de> for Tool {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let value = serde_json::Value::deserialize(deserializer)?;
        let type_str = value
            .get("type")
            .and_then(|v| v.as_str())
            .ok_or_else(|| serde::de::Error::missing_field("type"))?;

        if type_str == "function" {
            Ok(Tool::Function {
                name: value
                    .get("name")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| serde::de::Error::missing_field("name"))?
                    .to_string(),
                description: value
                    .get("description")
                    .and_then(|v| v.as_str())
                    .map(|s| s.to_string()),
                parameters: value.get("parameters").filter(|v| !v.is_null()).cloned(),
                strict: value.get("strict").and_then(|v| v.as_bool()),
                defer_loading: value.get("defer_loading").and_then(|v| v.as_bool()),
            })
        } else if type_str == "web_search" || type_str.starts_with("web_search_") {
            Ok(Tool::WebSearch {
                search_context_size: value
                    .get("search_context_size")
                    .filter(|v| !v.is_null())
                    .map(|v| serde_json::from_value(v.clone()))
                    .transpose()
                    .map_err(serde::de::Error::custom)?,
                user_location: value
                    .get("user_location")
                    .filter(|v| !v.is_null())
                    .map(|v| serde_json::from_value(v.clone()))
                    .transpose()
                    .map_err(serde::de::Error::custom)?,
                filters: value
                    .get("filters")
                    .filter(|v| !v.is_null())
                    .map(|v| serde_json::from_value(v.clone()))
                    .transpose()
                    .map_err(serde::de::Error::custom)?,
            })
        } else if type_str == "custom" {
            Ok(Tool::Custom {
                name: value
                    .get("name")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| serde::de::Error::missing_field("name"))?
                    .to_string(),
                description: value
                    .get("description")
                    .and_then(|v| v.as_str())
                    .map(|s| s.to_string()),
                format: value.get("format").filter(|v| !v.is_null()).cloned(),
                defer_loading: value.get("defer_loading").and_then(|v| v.as_bool()),
            })
        } else if type_str == "tool_search" {
            Ok(Tool::ToolSearch {
                description: value
                    .get("description")
                    .and_then(|v| v.as_str())
                    .map(|s| s.to_string()),
                execution: value
                    .get("execution")
                    .filter(|v| !v.is_null())
                    .map(|v| serde_json::from_value(v.clone()))
                    .transpose()
                    .map_err(serde::de::Error::custom)?,
                parameters: value.get("parameters").filter(|v| !v.is_null()).cloned(),
            })
        } else if type_str == "namespace" {
            Ok(Tool::Namespace {
                name: value
                    .get("name")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| serde::de::Error::missing_field("name"))?
                    .to_string(),
                description: value
                    .get("description")
                    .and_then(|v| v.as_str())
                    .map(|s| s.to_string()),
                tools: serde_json::from_value(
                    value
                        .get("tools")
                        .cloned()
                        .ok_or_else(|| serde::de::Error::missing_field("tools"))?,
                )
                .map_err(serde::de::Error::custom)?,
            })
        } else {
            Err(serde::de::Error::unknown_variant(
                type_str,
                &[
                    "function",
                    "web_search*",
                    "custom",
                    "tool_search",
                    "namespace",
                ],
            ))
        }
    }
}

// ── Tool choice ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ToolChoiceMode {
    None,
    Auto,
    Required,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum SpecificToolChoice {
    #[serde(rename = "function")]
    Function {
        #[serde(skip_serializing_if = "Option::is_none")]
        name: Option<String>,
    },
    #[serde(rename = "custom")]
    Custom { name: String },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct AllowedToolChoice {
    #[serde(rename = "type")]
    pub kind: String,
    pub tools: Vec<SpecificToolChoice>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub mode: Option<ToolChoiceMode>,
}

/// `ToolChoice` can be a simple mode string ("none"/"auto"/"required"),
/// a specific tool object, or an allowed_tools object.
/// Order matters for untagged: try object variants before the string.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(untagged)]
pub enum ToolChoice {
    Specific(SpecificToolChoice),
    AllowedTools(AllowedToolChoice),
    Mode(ToolChoiceMode),
}

// ── Text format / config ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
#[serde(tag = "type")]
pub enum TextFormat {
    #[serde(rename = "text")]
    Text,
    #[serde(rename = "json_object")]
    JsonObject,
    #[serde(rename = "json_schema")]
    JsonSchema {
        name: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        description: Option<String>,
        #[serde(skip_serializing_if = "Option::is_none")]
        schema: Option<serde_json::Value>,
        #[serde(skip_serializing_if = "Option::is_none")]
        strict: Option<bool>,
    },
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct TextConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub format: Option<TextFormat>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub verbosity: Option<Verbosity>,
}

// ── Reasoning config ──

/// Reasoning configuration used on Open Responses requests.
///
/// Request JSON omits `summary` when it is `None`.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ReasoningConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub effort: Option<ReasoningEffort>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub summary: Option<ReasoningSummary>,
}

/// Reasoning configuration echoed on Open Responses responses.
///
/// Response JSON preserves a present-but-empty summary as `"summary": null`,
/// matching native Responses payloads. Converting this type into
/// [`ReasoningConfig`] is intentionally serialization-lossy: a `None` summary
/// will be omitted if it is later serialized as a request.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct ResponseReasoningConfig {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub effort: Option<ReasoningEffort>,
    #[serde(default)]
    pub summary: Option<ReasoningSummary>,
}

impl From<ReasoningConfig> for ResponseReasoningConfig {
    fn from(value: ReasoningConfig) -> Self {
        Self {
            effort: value.effort,
            summary: value.summary,
        }
    }
}

impl From<ResponseReasoningConfig> for ReasoningConfig {
    fn from(value: ResponseReasoningConfig) -> Self {
        Self {
            effort: value.effort,
            summary: value.summary,
        }
    }
}

// ── Stream options ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct StreamOptions {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub include_obfuscation: Option<bool>,
}

// ── Usage ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct InputTokensDetails {
    pub cached_tokens: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cache_write_tokens: Option<u64>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct OutputTokensDetails {
    pub reasoning_tokens: u64,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct Usage {
    pub input_tokens: u64,
    pub output_tokens: u64,
    pub total_tokens: u64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub input_tokens_details: Option<InputTokensDetails>,
    pub output_tokens_details: Option<OutputTokensDetails>,
}

// ── Error ──

pub const ERROR_CODE_CONTENT_FILTER: &str = "content_filter";

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct OpenResponsesError {
    pub code: String,
    pub message: String,
}

// ── Incomplete details ──

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, schemars::JsonSchema)]
pub struct IncompleteDetails {
    pub reason: String,
}

// ── Metadata ──

pub type Metadata = HashMap<String, String>;

#[cfg(test)]
mod tests {
    use serde::de::DeserializeOwned;

    use super::*;

    fn sample_annotation() -> Annotation {
        Annotation::UrlCitation {
            url: "https://example.com".into(),
            title: "Example".into(),
            start_index: 0,
            end_index: 7,
        }
    }

    fn assert_round_trip<T>(value: T)
    where
        T: Serialize + DeserializeOwned + PartialEq + std::fmt::Debug,
    {
        let json = serde_json::to_string(&value).unwrap();
        let reparsed: T = serde_json::from_str(&json).unwrap();
        assert_eq!(reparsed, value);
    }

    #[test]
    fn input_item_defaults_to_message_when_type_absent() {
        let json = r#"{"role": "user", "content": "hello"}"#;
        let item: InputItem = serde_json::from_str(json).unwrap();
        assert!(matches!(
            item,
            InputItem::Message {
                role: MessageRole::User,
                ..
            }
        ));
    }

    #[test]
    fn input_item_with_explicit_type_still_works() {
        let json = r#"{"type": "message", "role": "user", "content": "hello"}"#;
        let item: InputItem = serde_json::from_str(json).unwrap();
        assert!(matches!(
            item,
            InputItem::Message {
                role: MessageRole::User,
                ..
            }
        ));
    }

    #[test]
    fn input_item_serializes_with_type_tag() {
        let item = InputItem::Message {
            role: MessageRole::User,
            content: InputContent::Text("hello".into()),
            id: None,
            status: None,
        };
        let json = serde_json::to_value(&item).unwrap();
        assert_eq!(json["type"], "message");
    }

    #[test]
    fn output_item_unknown_type_deserializes_as_unknown() {
        let json = r#"{"type":"new_output_item","id":"item_1","payload":{"ignored":true}}"#;
        let item: OutputItem = serde_json::from_str(json).unwrap();
        assert_eq!(item, OutputItem::Unknown);
    }

    #[test]
    fn tool_deserializes_any_web_search_variant() {
        let cases = [
            "web_search",
            "web_search_preview",
            "web_search_preview_2025_03_11",
            "web_search_2025_08_26",
        ];
        for variant in cases {
            let json = format!(r#"{{"type": "{variant}", "search_context_size": "medium"}}"#);
            let tool: Tool = serde_json::from_str(&json)
                .unwrap_or_else(|e| panic!("failed to deserialize {variant}: {e}"));
            assert!(
                matches!(
                    tool,
                    Tool::WebSearch {
                        search_context_size: Some(SearchContextSize::Medium),
                        ..
                    }
                ),
                "expected WebSearch for type={variant}"
            );
        }
    }

    #[test]
    fn tool_serializes_web_search_as_web_search() {
        let tool = Tool::WebSearch {
            search_context_size: Some(SearchContextSize::Medium),
            user_location: None,
            filters: None,
        };
        let json = serde_json::to_value(&tool).unwrap();
        assert_eq!(json["type"], "web_search");
    }

    #[test]
    fn input_content_part_output_text_annotations_round_trip() {
        assert_round_trip(InputContentPart::OutputText {
            text: "hello".into(),
            annotations: vec![sample_annotation()],
            logprobs: vec![],
        });
    }

    #[test]
    fn input_content_part_output_text_annotations_default_when_omitted() {
        let part: InputContentPart =
            serde_json::from_str(r#"{"type":"output_text","text":"hello"}"#).unwrap();
        assert_eq!(
            part,
            InputContentPart::OutputText {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            }
        );
    }

    #[test]
    fn output_content_part_text_annotations_round_trip() {
        assert_round_trip(OutputContentPart::Text {
            text: "hello".into(),
            annotations: vec![sample_annotation()],
            logprobs: vec![],
        });
    }

    #[test]
    fn output_content_part_text_annotations_default_when_omitted() {
        let part: OutputContentPart =
            serde_json::from_str(r#"{"type":"output_text","text":"hello"}"#).unwrap();
        assert_eq!(
            part,
            OutputContentPart::Text {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            }
        );
    }

    #[test]
    fn content_part_output_text_annotations_round_trip() {
        assert_round_trip(ContentPart::OutputText {
            text: "hello".into(),
            annotations: vec![sample_annotation()],
            logprobs: vec![],
        });
    }

    #[test]
    fn output_text_logprobs_serialize_when_empty() {
        for value in [
            serde_json::to_value(InputContentPart::OutputText {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            })
            .unwrap(),
            serde_json::to_value(OutputContentPart::Text {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            })
            .unwrap(),
            serde_json::to_value(ContentPart::OutputText {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            })
            .unwrap(),
        ] {
            assert_eq!(value.get("logprobs"), Some(&serde_json::json!([])));
        }
    }

    #[test]
    fn response_reasoning_summary_serializes_null_when_absent() {
        let json = serde_json::to_value(ResponseReasoningConfig {
            effort: Some(ReasoningEffort::Low),
            summary: None,
        })
        .unwrap();

        assert_eq!(json["effort"], "low");
        assert_eq!(json.get("summary"), Some(&serde_json::Value::Null));
    }

    #[test]
    fn response_reasoning_summary_defaults_when_omitted() {
        let reasoning: ResponseReasoningConfig = serde_json::from_value(serde_json::json!({
            "effort": "low"
        }))
        .unwrap();

        assert_eq!(reasoning.effort, Some(ReasoningEffort::Low));
        assert_eq!(reasoning.summary, None);
    }

    #[test]
    fn usage_output_tokens_details_serializes_when_absent() {
        let json = serde_json::to_value(Usage {
            input_tokens: 1,
            output_tokens: 2,
            total_tokens: 3,
            input_tokens_details: None,
            output_tokens_details: None,
        })
        .unwrap();
        assert_eq!(
            json.get("output_tokens_details"),
            Some(&serde_json::Value::Null)
        );
    }

    #[test]
    fn content_part_output_text_annotations_default_when_omitted() {
        let part: ContentPart =
            serde_json::from_str(r#"{"type":"output_text","text":"hello"}"#).unwrap();
        assert_eq!(
            part,
            ContentPart::OutputText {
                text: "hello".into(),
                annotations: vec![],
                logprobs: vec![],
            }
        );
    }
}
