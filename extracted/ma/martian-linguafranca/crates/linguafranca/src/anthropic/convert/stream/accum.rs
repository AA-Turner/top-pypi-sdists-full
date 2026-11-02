use crate::anthropic::convert::ctx::ConversionCtx;
use crate::anthropic::types::*;
use crate::convert::open_responses_id::{OpenResponsesOutputItemKind, output_item_id};
use crate::open_responses::stream::OpenResponsesStreamEvent;
use crate::open_responses::types::*;

/// Tracks state for Anthropic Messages → Open Responses streaming conversion.
///
/// Consecutive Anthropic Messages text content blocks map to content parts within a single
/// Open Responses Message item. Tool use and thinking blocks produce separate Open Responses items.
/// This accumulator manages the open Message, content indexing, sequence
/// numbering, and string buffers for "done" events.
pub(super) struct AnthropicMessagesToOpenResponsesAccum {
    pub ctx: ConversionCtx,
    pub seq: u64,
    pub output_index: u64,
    pub content_index: u64,

    pub response_id: String,
    pub model: String,
    pub service_tier: Option<ServiceTier>,

    pub message_open: bool,
    pub message_item_id: String,
    pub message_output_index: u64,

    pub current_block: CurrentBlock,
    pub text_buf: String,
    pub text_citations: Vec<PendingTextCitation>,
    pub args_buf: String,
    pub thinking_buf: String,
    pub signature_buf: String,

    pub message_content_parts: Vec<ContentPart>,
    pub output_items: Vec<OutputItem>,
    pub usage: Option<AnthropicUsage>,
    pub stop_reason: Option<AnthropicStopReason>,

    pub pending_web_search: Option<PendingWebSearch>,
    pub pending_tool_search: Option<PendingToolSearch>,
}

#[derive(Default)]
pub(super) enum CurrentBlock {
    #[default]
    None,
    Text,
    ToolUse {
        id: String,
        name: String,
        fc_id: String,
        output_index: u64,
    },
    Thinking {
        rs_id: String,
        output_index: u64,
    },
    RedactedThinking,
    WebSearchServerToolUse {
        id: String,
        output_index: u64,
    },
    WebSearchToolResult,
    ToolSearchServerToolUse,
}

pub(super) struct PendingTextCitation {
    pub citation: AnthropicCitation,
    pub fallback_start_index: Option<u64>,
}

pub(super) struct PendingWebSearch {
    pub id: String,
    pub query: Option<String>,
    pub output_index: u64,
}

pub(super) struct PendingToolSearch {
    pub id: String,
    pub arguments: serde_json::Value,
}

impl AnthropicMessagesToOpenResponsesAccum {
    pub fn new() -> Self {
        Self {
            ctx: ConversionCtx::new(),
            seq: 0,
            output_index: 0,
            content_index: 0,
            response_id: String::new(),
            model: String::new(),
            service_tier: None,
            message_open: false,
            message_item_id: String::new(),
            message_output_index: 0,
            current_block: CurrentBlock::None,
            text_buf: String::new(),
            text_citations: Vec::new(),
            args_buf: String::new(),
            thinking_buf: String::new(),
            signature_buf: String::new(),
            message_content_parts: Vec::new(),
            output_items: Vec::new(),
            usage: None,
            stop_reason: None,
            pending_web_search: None,
            pending_tool_search: None,
        }
    }

    pub fn next_seq(&mut self) -> u64 {
        let current = self.seq;
        self.seq += 1;
        current
    }

    pub fn next_output_index(&mut self) -> u64 {
        let current = self.output_index;
        self.output_index += 1;
        current
    }

    pub fn next_content_index(&mut self) -> u64 {
        let current = self.content_index;
        self.content_index += 1;
        current
    }

    pub fn item_id(
        &self,
        kind: OpenResponsesOutputItemKind,
        output_index: u64,
        source_hint: Option<&str>,
    ) -> String {
        output_item_id(&self.response_id, kind, output_index, source_hint)
    }

    /// Emit an output item that is immediately complete (Added + Done).
    pub fn emit_item_immediate(
        &mut self,
        item: OutputItem,
        events: &mut Vec<OpenResponsesStreamEvent>,
    ) {
        let output_index = self.next_output_index();
        self.output_items.push(item.clone());
        let seq_added = self.next_seq();
        events.push(OpenResponsesStreamEvent::OutputItemAdded {
            sequence_number: seq_added,
            output_index,
            item: item.clone(),
        });
        let seq_done = self.next_seq();
        events.push(OpenResponsesStreamEvent::OutputItemDone {
            sequence_number: seq_done,
            output_index,
            item,
        });
    }
}

/// Tracks state for Open Responses → Anthropic Messages streaming conversion.
///
/// Nearly stateless — only tracks the flat content block index and whether
/// the current thinking block needs a deferred ContentBlockStop.
pub(super) struct OpenResponsesToAnthropicMessagesAccum {
    pub ctx: ConversionCtx,
    pub block_index: u64,
    /// True once we've seen an OR reasoning item and are waiting to decide
    /// whether it becomes an Anthropic thinking block, a redacted thinking
    /// block, or gets dropped.
    pub pending_reasoning_item: bool,
    /// When true, the current thinking block's ContentBlockStop is deferred
    /// until OutputItemDone arrives with encrypted_content for SignatureDelta.
    pub thinking_block_open: bool,
    pub thinking_block_index: Option<u64>,
    /// True once we've actually emitted the Anthropic thinking ContentBlockStart.
    pub thinking_block_started: bool,
    /// Block index of the server_tool_use block awaiting completion via OutputItemDone.
    pub pending_web_search_block_index: Option<u64>,
}

impl OpenResponsesToAnthropicMessagesAccum {
    pub fn new() -> Self {
        Self {
            ctx: ConversionCtx::new(),
            block_index: 0,
            pending_reasoning_item: false,
            thinking_block_open: false,
            thinking_block_index: None,
            thinking_block_started: false,
            pending_web_search_block_index: None,
        }
    }

    pub fn next_block_index(&mut self) -> u64 {
        let current = self.block_index;
        self.block_index += 1;
        current
    }
}
