use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ImageSource {
    Base64 { media_type: String, data: String },
    Url { url: String },
}

#[derive(Debug, Deserialize, Clone)]
pub struct CacheCreation {
    ephemeral_1h_input_tokens: i32,
    ephemeral_5m_input_tokens: i32,
}

#[derive(Debug, Deserialize, Clone)]
pub struct ServerToolUsage {
    web_fetch_requests: i32,
    web_search_requests: i32,
}

#[derive(Debug, Deserialize, Clone)]
#[serde(rename_all = "snake_case")]
pub enum ServiceTier {
    Standard,
    Priority,
    Batch,
}

#[derive(Debug, Deserialize, Clone)]
#[serde(untagged)]
pub enum ServiceTierWrapper {
    KnownServiceTier(ServiceTier),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Default)]
pub struct Usage {
    pub input_tokens: i32,
    pub output_tokens: i32,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_creation_input_tokens: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_read_input_tokens: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_creation: Option<CacheCreation>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub inference_geo: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub server_tool_use: Option<ServerToolUsage>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub service_tier: Option<ServiceTierWrapper>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum StopReason {
    EndTurn,
    MaxTokens,
    StopSequence,
    ToolUse,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case", rename = "snake_case")]
pub enum Citation {
    CharLocation {
        cited_text: String,
        document_index: u32,
        #[serde(default)]
        document_title: Option<String>,
        end_char_index: i32,
        file_id: Option<String>,
        start_char_index: i32,
    },
    PageLocation {
        cited_text: String,
        document_index: u32,
        #[serde(default)]
        document_title: Option<String>,
        end_page_number: i32,
        file_id: Option<String>,
        start_page_number: i32,
    },
    ContentBlockLocation {
        cited_text: String,
        document_index: u32,
        #[serde(default)]
        document_title: Option<String>,
        end_block_index: i32,
        #[serde(default)]
        file_id: Option<String>,
        start_block_index: i32,
    },
    WebSearchResultLocation {
        cited_text: String,
        encrypted_text: String,
        #[serde(default)]
        title: Option<String>,
        url: String,
    },
    SearchResultLocation {
        cited_text: String,
        end_block_index: i32,
        search_result_index: u32,
        source: String,
        start_block_index: i32,
        #[serde(default)]
        title: Option<String>,
    },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
pub enum ToolUseCaller {
    #[serde(rename = "direct")]
    Direct,
    #[serde(rename = "code_execution_20250825")]
    ServerToolCaller { tool_id: String },
    #[serde(rename = "code_execution_20260120")]
    ServerToolCaller20260120 { tool_id: String },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ToolUseBlock {
    pub id: String,
    pub name: String,
    pub input: std::collections::BTreeMap<String, serde_json::Value>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub caller: Option<ToolUseCaller>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ServerToolUseBlock {
    pub id: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub caller: Option<ToolUseCaller>,
    pub name: ServerToolUseNameWrapper,
    pub input: std::collections::BTreeMap<String, serde_json::Value>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum ServerToolUseNameWrapper {
    KnownName(ServerToolUseName),
    String(String),
}

impl ToString for ServerToolUseNameWrapper {
    fn to_string(&self) -> String {
        match self {
            Self::KnownName(name) => name.to_string(),
            Self::String(s) => s.clone(),
        }
    }
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ServerToolUseName {
    WebSearch,
    WebFetch,
    CodeExecution,
    BashCodeExecution,
    TextEditorCodeExecution,
    ToolSearchToolRegex,
    ToolSearchBm25,
}

impl ToString for ServerToolUseName {
    fn to_string(&self) -> String {
        let s = match self {
            Self::WebSearch => "web_search",
            Self::WebFetch => "web_fetch",
            Self::CodeExecution => "code_execution",
            Self::BashCodeExecution => "bash_code_execution",
            Self::TextEditorCodeExecution => "text_editor_code_execution",
            Self::ToolSearchToolRegex => "tool_search_tool_regex",
            Self::ToolSearchBm25 => "tool_search_bm25",
        };
        s.to_string()
    }
}
