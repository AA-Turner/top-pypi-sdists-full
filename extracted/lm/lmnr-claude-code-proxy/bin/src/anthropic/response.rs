use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use super::common::{
    Citation, ServerToolUseBlock, ServerToolUseNameWrapper, StopReason, ToolUseBlock,
    ToolUseCaller, Usage,
};
use super::request::{McpToolResultContent, TextBlockWrapper};
use super::stream::{ContentDelta, StreamContentBlock, StreamEvent};
use super::tool_result::{
    BashCodeExecutionToolResultBlock, CodeExecutionToolResultBlock,
    TextEditorCodeExecutionToolResultBlock, ToolSearchToolResultBlock, WebFetchToolResultBlock,
    WebSearchToolResultBlock,
};
use crate::spans::SpanError;

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
                // TODO: this will be needed to create tool spans as they end
                StreamEvent::ContentBlockStop { .. } => {}
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
                citations: None,
            },
            ContentBlockBuilder::ToolUse {
                id,
                name,
                input_json,
            } => {
                let input =
                    serde_json::from_str(&input_json).unwrap_or(std::collections::BTreeMap::new());
                ResponseContentBlock::ToolUse(ToolUseBlock {
                    id,
                    name,
                    input,
                    caller: None,
                })
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
            } => ResponseContentBlock::ServerToolUse(ServerToolUseBlock {
                id,
                name: ServerToolUseNameWrapper::String(name),
                input: serde_json::from_str(&input_json).unwrap_or(BTreeMap::new()),
                caller: None,
            }),
        }
    }
}

#[derive(Debug, Deserialize, Clone, Serialize)]
#[serde(tag = "type")]
#[serde(rename_all = "snake_case")]
pub enum ResponseContentBlock {
    Text {
        text: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        citations: Option<Vec<Citation>>,
    },
    Thinking {
        thinking: String,
        signature: String,
    },
    RedactedThinking {
        data: String,
    },
    ToolUse(ToolUseBlock),
    ServerToolUse(ServerToolUseBlock),
    WebSearchToolResult(WebSearchToolResultBlock),
    WebFetchToolResult(WebFetchToolResultBlock),
    CodeExecutionToolResult(CodeExecutionToolResultBlock),
    BashCodeExecutionToolResult(BashCodeExecutionToolResultBlock),
    TextEditorCodeExecutionToolResult(TextEditorCodeExecutionToolResultBlock),
    ToolSearchToolResult(ToolSearchToolResultBlock),
    ContainerUpload {
        file_id: String,
    },
    // The below are undocumented / deprecated
    SearchResult {
        content: TextBlockWrapper,
        source: String,
        title: String,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        citations: Option<Vec<Citation>>,
    },
    McpToolUse {
        id: String,
        input: serde_json::Value,
        name: String,
        server_name: String,
    },
    McpToolResult {
        tool_use_id: String,
        content: McpToolResultContent,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        is_error: Option<bool>,
    },
}
