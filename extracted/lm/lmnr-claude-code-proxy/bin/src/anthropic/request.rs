use std::collections::HashMap;

use serde::{Deserialize, Serialize};

use super::common::{CacheControl, ImageSource};

#[derive(Debug, Deserialize, Clone)]
pub struct PostMessagesRequest {
    pub model: String,
    pub max_tokens: u32,
    pub messages: Vec<Message>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub system: Option<SystemPrompt>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stream: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub temperature: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub top_k: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub top_p: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stop_sequences: Option<Vec<String>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tools: Option<Vec<Tool>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub metadata: Option<Metadata>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub tool_choice: Option<ToolChoice>,
}

#[derive(Debug, Deserialize, Clone)]
#[serde(untagged)]
pub enum SystemPrompt {
    String(String),
    Blocks(Vec<SystemBlock>),
}

impl SystemPrompt {
    pub fn to_string(self) -> String {
        match self {
            SystemPrompt::String(s) => s,
            SystemPrompt::Blocks(blocks) => blocks
                .iter()
                .map(|block| match block {
                    SystemBlock::Text { text, .. } => text.clone(),
                })
                .collect::<Vec<String>>()
                .join("\n"),
        }
    }
}

#[derive(Debug, Deserialize, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum SystemBlock {
    Text {
        text: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
}

#[derive(Debug, Deserialize, Clone)]
pub struct Metadata {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub user_id: Option<String>,
}

#[derive(Debug, Deserialize, Clone, Eq, PartialEq)]
pub enum MessageRole {
    #[serde(rename = "user")]
    User,
    #[serde(rename = "assistant")]
    Assistant,
}

#[derive(Debug, Deserialize, Clone)]
pub struct Message {
    pub role: MessageRole,
    pub content: MessageContent,
}

impl Message {
    pub fn is_tool_result(&self) -> bool {
        self.role == MessageRole::User && self.content.is_tool_result()
    }

    pub fn is_tool_use(&self) -> bool {
        self.role == MessageRole::Assistant && self.content.is_tool_use()
    }
}

#[derive(Debug, Deserialize, Clone)]
#[serde(untagged)]
pub enum MessageContent {
    String(String),
    Blocks(Vec<ContentBlock>),
}

impl MessageContent {
    pub fn is_tool_result(&self) -> bool {
        match self {
            MessageContent::Blocks(blocks) => blocks
                .iter()
                .any(|block| matches!(block, ContentBlock::ToolResult { .. })),
            _ => false,
        }
    }

    /// Returns a map of tool use IDs to tool result content blocks.
    pub fn tool_results(&self) -> HashMap<String, ContentBlock> {
        match self {
            MessageContent::Blocks(blocks) => blocks
                .iter()
                .filter_map(|block| match block {
                    ContentBlock::ToolResult { tool_use_id, .. } => {
                        Some((tool_use_id.clone(), block.clone()))
                    }
                    _ => None,
                })
                .collect(),
            _ => HashMap::new(),
        }
    }

    pub fn is_tool_use(&self) -> bool {
        match self {
            MessageContent::Blocks(blocks) => blocks
                .iter()
                .any(|block| matches!(block, ContentBlock::ToolUse { .. })),
            _ => false,
        }
    }

    /// Returns a HashMap of tool use IDs to tool use content blocks.
    pub fn tool_uses(&self) -> HashMap<String, ContentBlock> {
        match self {
            MessageContent::Blocks(blocks) => blocks
                .iter()
                .filter_map(|block| match block {
                    ContentBlock::ToolUse { id, .. } => Some((id.clone(), block.clone())),
                    _ => None,
                })
                .collect(),
            _ => HashMap::new(),
        }
    }
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum DocumentSourceNestedContentBlock {
    Text { text: String },
    Image { source: ImageSource },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum DocumentSourceNestedContent {
    String(String),
    Blocks(Vec<DocumentSourceNestedContentBlock>),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum DocumentSource {
    Base64 {
        media_type: String,
        data: String,
    },
    Text {
        media_type: String,
        data: String,
    },
    Content {
        content: Box<DocumentSourceNestedContent>,
    },
    Url {
        url: String,
    },
    File {
        file_id: String,
    },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CitationConfig {
    pub enabled: bool,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct SearchResultContentBlock {
    pub text: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_control: Option<CacheControl>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum SearchResultContent {
    String(String),
    Blocks(Vec<SearchResultContentBlock>),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebSearchResultContentBlock {
    pub encrypted_content: String,
    pub title: String,
    pub url: String,
    #[serde(rename = "type")]
    pub block_type: String,
    pub page_age: Option<String>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum McpToolResultContentBlock {
    Text { text: String },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum McpToolResultContent {
    String(String),
    Blocks(Vec<McpToolResultContentBlock>),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ContentBlock {
    Text {
        text: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    Image {
        source: ImageSource,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    Document {
        source: DocumentSource,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        citations: Option<CitationConfig>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        context: Option<String>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        title: Option<String>,
    },
    ToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
    },
    ToolResult {
        tool_use_id: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        content: Option<ToolResultContent>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        is_error: Option<bool>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    Thinking {
        thinking: String,
        signature: String,
    },
    RedactedThinking {
        data: String,
    },
    SearchResult {
        content: SearchResultContent,
        source: String,
        title: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        citations: Option<Vec<super::common::Citation>>,
    },
    ServerToolUse {
        id: String,
        input: serde_json::Value,
        name: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    WebSearchToolResult {
        tool_use_id: String,
        content: Vec<WebSearchResultContentBlock>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    WebFetchToolResult {
        tool_use_id: String,
        // TODO: type this
        content: serde_json::Value,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    CodeExecutionToolResult {
        tool_use_id: String,
        // TODO: type this
        content: serde_json::Value,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    BashCodeExecutionToolResult {
        tool_use_id: String,
        // TODO: type this
        content: serde_json::Value,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    TextEditorCodeExecutionToolResult {
        tool_use_id: String,
        // TODO: type this
        content: serde_json::Value,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    McpToolUse {
        id: String,
        input: serde_json::Value,
        name: String,
        server_name: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
    McpToolResult {
        tool_use_id: String,
        content: McpToolResultContent,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        is_error: Option<bool>,
    },
    ContainerUpload {
        file_id: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
    },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum ToolResultContent {
    String(String),
    Blocks(Vec<ToolResultBlock>),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ToolResultBlock {
    Text { text: String },
    Image { source: ImageSource },
}

fn default_input_schema() -> serde_json::Value {
    serde_json::json!({})
}

#[derive(Debug, Deserialize, Clone)]
pub struct Tool {
    pub name: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub description: Option<String>,
    #[serde(default = "default_input_schema")]
    pub input_schema: serde_json::Value,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_control: Option<CacheControl>,
}

#[derive(Debug, Deserialize, Clone)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ToolChoice {
    Auto,
    Any,
    Tool { name: String },
}
