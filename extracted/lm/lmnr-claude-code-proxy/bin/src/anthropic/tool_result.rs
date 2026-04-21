use serde::{Deserialize, Serialize};

use crate::anthropic::{common::ToolUseCaller, request::CitationConfig};

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebSearchToolResultBlock {
    pub tool_use_id: String,
    pub content: WebSearchToolResultContent,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub caller: Option<ToolUseCaller>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum WebSearchToolResultContent {
    Results(Vec<WebSearchToolResultContentBlockWrapper>),
    Error(WebSearchToolResultErrorWrapper),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum WebSearchToolResultContentBlockWrapper {
    WebSearchResult(WebSearchToolResultContentBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebSearchToolResultContentBlock {
    encrypted_content: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    page_age: Option<String>,
    title: String,
    url: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum WebSearchToolResultErrorWrapper {
    WebSearchToolResultError(WebSearchToolResultError),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebSearchToolResultError {
    error_code: WebSearchToolResultErrorCodeWrapper,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum WebSearchToolResultErrorCodeWrapper {
    WebSearchToolResultErrorCode(WebSearchToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum WebSearchToolResultErrorCode {
    InvalidToolInput,
    Unavailable,
    MaxUsesExceeded,
    TooManyRequests,
    QueryTooLong,
    RequestTooLarge,
}

// ===================================================== //

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebFetchToolResultBlock {
    pub tool_use_id: String,
    pub content: WebFetchToolResultContent,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub caller: Option<ToolUseCaller>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum WebFetchToolResultContent {
    WebFetchResult(WebFetchResult),
    WebFetchToolResultError(WebFetchToolResultError),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebFetchResult {
    content: WebFetchResultDocumentBlockWrapper,
    // with chrono, can be typed as Option<DateTime<Utc>>
    #[serde(default, skip_serializing_if = "Option::is_none")]
    retrieved_at: Option<String>,
    url: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct WebFetchToolResultError {
    error_code: WebFetchToolResultErrorCodeWrapper,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum WebFetchToolResultErrorCodeWrapper {
    WebFetchToolResultErrorCode(WebFetchToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum WebFetchToolResultErrorCode {
    InvalidToolInput,
    UrlTooLong,
    UrlNotAllowed,
    UrlNotAccessible,
    UnsupportedContentType,
    TooManyRequests,
    MaxUsesExceeded,
    Unavailable,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum WebFetchResultDocumentBlockWrapper {
    Document(WebFetchResultDocumentBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
struct WebFetchResultDocumentBlock {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub citations: Option<CitationConfig>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub title: Option<String>,
    pub source: WebFetchResultDocumentBlockSource,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum WebFetchResultDocumentBlockSource {
    Base64 {
        data: String,
        media_type: String, // application/pdf
    },
    Text {
        data: String,
        media_type: String, // text/plain
    },
}

// ===================================================== //

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CodeExecutionToolResultBlock {
    pub tool_use_id: String,
    pub content: CodeExecutionToolResultContent,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum CodeExecutionToolResultContent {
    CodeExecutionResult(CodeExecutionToolResult),
    EncryptedCodeExecutionResult(EncryptedCodeExecutionToolResult),
    CodeExecutionToolResultError(CodeExecutionToolResultError),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CodeExecutionToolResult {
    content: Vec<CodeExecutionToolResultContentBlockWrapper>,
    return_code: i32,
    stderr: String,
    stdout: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum CodeExecutionToolResultContentBlockWrapper {
    CodeExecutionOutput(CodeExecutionToolResultContentBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CodeExecutionToolResultContentBlock {
    file_id: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct EncryptedCodeExecutionToolResult {
    content: Vec<CodeExecutionToolResultContentBlockWrapper>,
    return_code: i32,
    stderr: String,
    encrypted_stdout: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CodeExecutionToolResultError {
    error_code: CodeExecutionToolResultErrorCodeWrapper,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum CodeExecutionToolResultErrorCodeWrapper {
    CodeExecutionToolResultErrorCode(CodeExecutionToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum CodeExecutionToolResultErrorCode {
    InvalidToolInput,
    TooManyRequests,
    ExecutionTimeExceeded,
    Unavailable,
}

// ===================================================== //

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct BashCodeExecutionToolResultBlock {
    pub tool_use_id: String,
    pub content: BashCodeExecutionToolResultContent,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum BashCodeExecutionToolResultContent {
    BashCodeExecutionResult(BashCodeExecutionToolResult),
    BashCodeExecutionToolResultError(BashCodeExecutionToolResultError),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct BashCodeExecutionToolResult {
    content: Vec<BashCodeExecutionToolResultContentBlockWrapper>,
    return_code: i32,
    stderr: String,
    stdout: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum BashCodeExecutionToolResultContentBlockWrapper {
    // re-use the regular code execution block
    BashCodeExecutionOutput(CodeExecutionToolResultContentBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct BashCodeExecutionToolResultError {
    error_code: BashCodeExecutionToolResultErrorCodeWrapper,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum BashCodeExecutionToolResultErrorCodeWrapper {
    BashCodeExecutionToolResultErrorCode(BashCodeExecutionToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum BashCodeExecutionToolResultErrorCode {
    InvalidToolInput,
    TooManyRequests,
    ExecutionTimeExceeded,
    Unavailable,
    OutputFileTooLarge,
}

// ===================================================== //

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct TextEditorCodeExecutionToolResultBlock {
    pub tool_use_id: String,
    pub content: TextEditorCodeExecutionToolResultContent,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum TextEditorCodeExecutionToolResultContent {
    TextEditorCodeExecutionToolResultError(TextEditorCodeExecutionToolResultError),
    TextEditorCodeExecutionViewResultBlock(TextEditorCodeExecutionViewResultBlock),
    TextEditorCodeExecutionCreateResultBlock(TextEditorCodeExecutionCreateResultBlock),
    TextEditorCodeExecutionStrReplaceResultBlock(TextEditorCodeExecutionStrReplaceResultBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct TextEditorCodeExecutionViewResultBlock {
    content: String,
    file_type: String, // "text", "image", "pdf"
    #[serde(default, skip_serializing_if = "Option::is_none")]
    num_lines: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    start_line: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    total_lines: Option<i32>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct TextEditorCodeExecutionCreateResultBlock {
    is_file_update: bool,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct TextEditorCodeExecutionStrReplaceResultBlock {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    lines: Option<Vec<String>>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    new_lines: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    new_start: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    old_lines: Option<i32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    old_start: Option<i32>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct TextEditorCodeExecutionToolResultError {
    error_code: TextEditorCodeExecutionToolResultErrorCodeWrapper,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    error_message: Option<String>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum TextEditorCodeExecutionToolResultErrorCodeWrapper {
    TextEditorCodeExecutionToolResultErrorCodeWrapper(TextEditorCodeExecutionToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum TextEditorCodeExecutionToolResultErrorCode {
    InvalidToolInput,
    TooManyRequests,
    ExecutionTimeExceeded,
    Unavailable,
    FileNotFound,
}

// ===================================================== //

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ToolSearchToolResultBlock {
    pub tool_use_id: String,
    pub content: ToolSearchToolResultContent,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ToolSearchToolResultContent {
    ToolSearchToolSearchResult(ToolSearchToolResult),
    ToolSearchToolResultError(ToolSearchToolResultError),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ToolSearchToolResult {
    tool_references: Vec<ToolReferenceBlockWrapper>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ToolReferenceBlockWrapper {
    ToolReference(ToolReferenceBlock),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ToolReferenceBlock {
    tool_name: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct ToolSearchToolResultError {
    error_code: ToolSearchToolResultErrorCodeWrapper,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    error_message: Option<String>,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum ToolSearchToolResultErrorCodeWrapper {
    ToolResultErrorCode(ToolSearchToolResultErrorCode),
    String(String),
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum ToolSearchToolResultErrorCode {
    InvalidToolInput,
    TooManyRequests,
    ExecutionTimeExceeded,
    Unavailable,
}
