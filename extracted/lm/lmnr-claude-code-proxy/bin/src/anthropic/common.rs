use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct CacheControl {
    #[serde(rename = "type")]
    pub cache_type: String,
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ImageSource {
    Base64 { media_type: String, data: String },
    Url { url: String },
}

#[derive(Debug, Deserialize, Clone)]
pub struct Usage {
    pub input_tokens: u32,
    pub output_tokens: u32,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_creation_input_tokens: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub cache_read_input_tokens: Option<u32>,
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
        document_title: Option<String>,
        end_char_index: i32,
        file_id: Option<String>,
        start_char_index: i32,
    },
    PageLocation {
        cited_text: String,
        document_index: u32,
        document_title: Option<String>,
        end_page_number: i32,
        file_id: Option<String>,
        start_page_number: i32,
    },
    ContentBlockLocation {
        cited_text: String,
        document_index: u32,
        document_title: Option<String>,
        end_block_index: i32,
        file_id: Option<String>,
        start_block_index: i32,
    },
    WebSearchResultLocation {
        cited_text: String,
        encrypted_text: String,
        title: Option<String>,
        url: String,
    },
    SearchResultLocation {
        cited_text: String,
        end_block_index: i32,
        search_result_index: u32,
        source: String,
        start_block_index: i32,
        title: Option<String>,
    },
}
