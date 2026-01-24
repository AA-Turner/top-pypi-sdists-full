use serde::{Deserialize, Serialize};

use crate::spans::SpanError;

use super::common::{CacheControl, Citation, StopReason, Usage};
use super::request::{McpToolResultContent, SearchResultContent, ToolResultContent};
use super::stream::{ContentDelta, StreamContentBlock, StreamEvent};

#[derive(Debug, Deserialize, Clone)]
pub struct MessageResponse {
    pub id: String,
    #[serde(rename = "type")]
    pub response_type: String,
    pub role: String,
    pub content: Vec<ResponseContentBlock>,
    pub model: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stop_reason: Option<StopReason>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub stop_sequence: Option<String>,
    pub usage: Usage,
}

impl MessageResponse {
    /// Reconstructs a complete MessageResponse from a sequence of streaming events
    ///
    /// The streaming API sends events in this order:
    /// 1. MessageStart - contains initial message structure with id, model, empty content
    /// 2. ContentBlockStart - announces each content block (text, tool_use, etc.)
    /// 3. ContentBlockDelta - incremental updates (text chunks, JSON fragments)
    /// 4. ContentBlockStop - marks end of content block
    /// 5. MessageDelta - provides final stop_reason and usage
    /// 6. MessageStop - end of stream
    pub fn try_from_stream_events(events: Vec<StreamEvent>) -> Result<Self, SpanError> {
        // Extract the initial message from MessageStart
        let mut message = events
            .iter()
            .find_map(|event| match event {
                StreamEvent::MessageStart { message } => Some(message.clone()),
                _ => None,
            })
            .ok_or(SpanError::MessageStartEventNotFound)?;

        // Track content blocks being built
        // Map of index -> (type, accumulated content)
        let mut content_blocks: std::collections::BTreeMap<u32, ContentBlockBuilder> =
            std::collections::BTreeMap::new();

        // Process events to build content blocks
        for event in events.iter() {
            match event {
                StreamEvent::ContentBlockStart {
                    index,
                    content_block,
                } => {
                    let builder = match content_block {
                        StreamContentBlock::Text { text } => {
                            ContentBlockBuilder::Text { text: text.clone() }
                        }
                        StreamContentBlock::ToolUse { id, name } => ContentBlockBuilder::ToolUse {
                            id: id.clone(),
                            name: name.clone(),
                            input_json: String::new(),
                        },
                        StreamContentBlock::Thinking {
                            thinking,
                            signature,
                        } => ContentBlockBuilder::Thinking {
                            thinking: thinking.clone(),
                            signature: signature.clone(),
                        },
                        StreamContentBlock::ServerToolUse { id, name } => {
                            ContentBlockBuilder::ServerToolUse {
                                id: id.clone(),
                                name: name.clone(),
                                input_json: String::new(),
                            }
                        }
                    };
                    content_blocks.insert(*index, builder);
                }
                StreamEvent::ContentBlockDelta { index, delta } => {
                    if let Some(builder) = content_blocks.get_mut(index) {
                        match delta {
                            ContentDelta::TextDelta { text } => {
                                if let ContentBlockBuilder::Text { text: acc } = builder {
                                    acc.push_str(text);
                                }
                            }
                            ContentDelta::InputJsonDelta { partial_json } => {
                                if let ContentBlockBuilder::ToolUse { input_json, .. } = builder {
                                    input_json.push_str(partial_json);
                                }
                                if let ContentBlockBuilder::ServerToolUse { input_json, .. } =
                                    builder
                                {
                                    input_json.push_str(partial_json);
                                }
                            }
                            ContentDelta::ThinkingDelta { thinking } => {
                                if let ContentBlockBuilder::Thinking { thinking: acc, .. } = builder
                                {
                                    acc.push_str(thinking);
                                }
                            }
                            ContentDelta::SignatureDelta { signature } => {
                                if let ContentBlockBuilder::Thinking { signature: acc, .. } =
                                    builder
                                {
                                    acc.push_str(signature);
                                }
                            }
                        }
                    }
                }
                StreamEvent::MessageDelta { delta, usage } => {
                    // Update stop_reason and stop_sequence
                    message.stop_reason = delta.stop_reason.clone();
                    message.stop_sequence = delta.stop_sequence.clone();

                    // Update output token count from delta
                    message.usage.output_tokens = usage.output_tokens;
                }
                _ => {
                    // Ignore Ping, ContentBlockStop, MessageStop, MessageStart, and Error events
                }
            }
        }

        // Convert builders to ResponseContentBlock
        message.content = content_blocks
            .into_iter()
            .map(|(_, builder)| builder.into_response_content_block())
            .collect();

        Ok(message)
    }
}

/// Helper enum for building content blocks from streaming events
#[derive(Debug, Clone)]
enum ContentBlockBuilder {
    Text {
        text: String,
    },
    ToolUse {
        id: String,
        name: String,
        input_json: String,
    },
    Thinking {
        thinking: String,
        signature: String,
    },
    ServerToolUse {
        id: String,
        name: String,
        input_json: String,
    },
}

impl ContentBlockBuilder {
    fn into_response_content_block(self) -> ResponseContentBlock {
        match self {
            ContentBlockBuilder::Text { text } => ResponseContentBlock::Text {
                text,
                cache_control: None,
                citations: None,
            },
            ContentBlockBuilder::ToolUse {
                id,
                name,
                input_json,
            } => {
                let input =
                    serde_json::from_str(&input_json).unwrap_or_else(|_| serde_json::json!({}));
                ResponseContentBlock::ToolUse { id, name, input }
            }
            ContentBlockBuilder::Thinking {
                thinking,
                signature,
            } => ResponseContentBlock::Thinking {
                thinking,
                signature,
            },
            ContentBlockBuilder::ServerToolUse {
                id,
                name,
                input_json,
            } => ResponseContentBlock::ServerToolUse {
                id,
                name,
                input: serde_json::from_str(&input_json).unwrap_or(serde_json::json!({})),
                cache_control: None,
            },
        }
    }
}

/// Individual web search result block
#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum WebSearchResultBlock {
    WebSearchResult {
        url: String,
        title: String,
        encrypted_content: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        page_age: Option<String>,
    },
}

/// Web search tool result content - can be results or an error
#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(untagged)]
pub enum WebSearchToolResultContent {
    Results(Vec<WebSearchResultBlock>),
    Error {
        error_code: String,
        #[serde(rename = "type")]
        block_type: String,
    },
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ResponseContentBlock {
    Text {
        text: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        cache_control: Option<CacheControl>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        citations: Option<Vec<Citation>>,
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
        citations: Option<Vec<Citation>>,
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
        content: WebSearchToolResultContent,
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
