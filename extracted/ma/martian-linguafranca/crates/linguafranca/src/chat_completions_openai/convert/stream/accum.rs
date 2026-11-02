use std::collections::{BTreeMap, HashMap};

use crate::convert::ctx::ConversionCtx;
use crate::convert::open_responses_id::{OpenResponsesOutputItemKind, output_item_id};
use crate::error::WarningAction;
use crate::open_responses::types::ServiceTier;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub(super) enum ResponsePhase {
    #[default]
    NotStarted,
    InProgress,
    TerminalPending,
    TerminalEmitted,
}

#[derive(Default)]
pub(super) struct MessagePartAccum {
    pub content_index: u64,
    pub accumulated_text: String,
    pub is_open: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ToolCallKind {
    Function,
    Custom,
}

pub(super) struct ToolCallAccum {
    pub output_index: Option<u64>,
    pub item_id: String,
    pub call_id: String,
    pub kind: Option<ToolCallKind>,
    pub name: String,
    pub payload: String,
    pub output_item_added: bool,
}

pub(super) struct ChatCompletionsToOpenResponsesAccum {
    pub ctx: ConversionCtx<()>,

    pub phase: ResponsePhase,

    pub next_sequence_number: u64,
    pub next_output_index: u64,
    pub next_content_index: u64,

    pub response_id: String,
    pub model: String,
    pub created_at: u64,

    pub message_is_open: bool,
    pub message_item_id: String,
    pub message_output_index: u64,
    pub text_part: MessagePartAccum,
    pub refusal_part: MessagePartAccum,

    pub reasoning_is_open: bool,
    pub reasoning_item_id: String,
    pub reasoning_output_index: u64,
    pub reasoning_summary_index: u64,
    pub reasoning_encrypted_content: Option<String>,

    pub tool_call_accums: BTreeMap<u32, ToolCallAccum>,

    pub saw_system_fingerprint: bool,
    pub saw_service_tier: bool,
    pub saw_obfuscation: bool,
}

impl ChatCompletionsToOpenResponsesAccum {
    pub fn new() -> Self {
        Self {
            ctx: ConversionCtx::new(),
            phase: ResponsePhase::NotStarted,
            next_sequence_number: 0,
            next_output_index: 0,
            next_content_index: 0,
            response_id: String::new(),
            model: String::new(),
            created_at: 0,
            message_is_open: false,
            message_item_id: String::new(),
            message_output_index: 0,
            text_part: MessagePartAccum::default(),
            refusal_part: MessagePartAccum::default(),
            reasoning_is_open: false,
            reasoning_item_id: String::new(),
            reasoning_output_index: 0,
            reasoning_summary_index: 0,
            reasoning_encrypted_content: None,
            tool_call_accums: BTreeMap::new(),
            saw_system_fingerprint: false,
            saw_service_tier: false,
            saw_obfuscation: false,
        }
    }

    pub fn next_sequence_number(&mut self) -> u64 {
        let current = self.next_sequence_number;
        self.next_sequence_number += 1;
        current
    }

    pub fn next_output_index(&mut self) -> u64 {
        let current = self.next_output_index;
        self.next_output_index += 1;
        current
    }

    pub fn next_content_index(&mut self) -> u64 {
        let current = self.next_content_index;
        self.next_content_index += 1;
        current
    }

    pub fn output_item_id(
        &self,
        kind: OpenResponsesOutputItemKind,
        output_index: u64,
        source_hint: Option<&str>,
    ) -> String {
        output_item_id(&self.response_id, kind, output_index, source_hint)
    }

    pub fn reset_message_parts(&mut self) {
        self.next_content_index = 0;
        self.text_part = MessagePartAccum::default();
        self.refusal_part = MessagePartAccum::default();
    }
}

pub(super) struct OpenResponsesToChatCompletionsAccum {
    pub ctx: ConversionCtx<()>,

    pub response_id: String,
    pub model: String,
    pub created: u64,
    pub service_tier: Option<String>,
    pub saw_response_header: bool,

    pub role_prelude_emitted: bool,
    pub next_tool_call_index: u32,
    pub tool_call_indexes: HashMap<String, u32>,
    pub emitted_tool_call_arguments: HashMap<String, String>,
    pub saw_function_call: bool,
    pub saw_any_event: bool,
    pub saw_terminal_event: bool,
    pub warned_missing_response_header: bool,
}

impl OpenResponsesToChatCompletionsAccum {
    pub fn new() -> Self {
        Self {
            ctx: ConversionCtx::new(),
            response_id: String::new(),
            model: String::new(),
            created: 0,
            service_tier: None,
            saw_response_header: false,
            role_prelude_emitted: false,
            next_tool_call_index: 0,
            tool_call_indexes: HashMap::new(),
            emitted_tool_call_arguments: HashMap::new(),
            saw_function_call: false,
            saw_any_event: false,
            saw_terminal_event: false,
            warned_missing_response_header: false,
        }
    }

    pub fn remember_response_header(
        &mut self,
        id: String,
        model: String,
        created: u64,
        service_tier: Option<ServiceTier>,
    ) {
        if !self.saw_response_header {
            self.response_id = id;
            self.model = model;
            self.created = created;
            self.saw_response_header = true;
        }
        if let Some(service_tier) = service_tier {
            self.service_tier = Some(match service_tier {
                ServiceTier::Auto => "auto".into(),
                ServiceTier::Default => "default".into(),
                ServiceTier::Flex => "flex".into(),
                ServiceTier::Priority => "priority".into(),
            });
        }
    }

    pub fn record_emitted_tool_call_arguments(&mut self, item_id: &str, arguments: &str) {
        if arguments.is_empty() {
            return;
        }
        self.emitted_tool_call_arguments
            .entry(item_id.to_string())
            .or_default()
            .push_str(arguments);
    }

    pub fn inline_tool_call_arguments_to_emit(
        &mut self,
        item_id: &str,
        inline_arguments: String,
        field: &str,
    ) -> Option<String> {
        let Some(emitted_arguments) = self.emitted_tool_call_arguments.get(item_id) else {
            return Some(inline_arguments);
        };

        if inline_arguments.is_empty() || emitted_arguments.is_empty() {
            return Some(inline_arguments);
        }

        if let Some(suffix) = inline_arguments.strip_prefix(emitted_arguments.as_str()) {
            return (!suffix.is_empty()).then(|| suffix.to_string());
        }

        if emitted_arguments.starts_with(&inline_arguments) {
            return None;
        }

        self.ctx.warn(
            field,
            WarningAction::Dropped,
            "inline tool call arguments conflicted with previously emitted argument deltas",
        );
        None
    }

    pub fn get_or_create_tool_call_index(&mut self, item_id: &str) -> u32 {
        if let Some(index) = self.tool_call_indexes.get(item_id) {
            return *index;
        }
        let index = self.next_tool_call_index;
        self.next_tool_call_index += 1;
        self.tool_call_indexes.insert(item_id.to_string(), index);
        index
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reset_message_parts_clears_open_parts() {
        let mut accum = ChatCompletionsToOpenResponsesAccum::new();
        accum.next_content_index = 3;
        accum.text_part.is_open = true;
        accum.text_part.accumulated_text = "a".into();
        accum.refusal_part.is_open = true;
        accum.refusal_part.accumulated_text = "b".into();
        accum.reset_message_parts();

        assert_eq!(accum.next_content_index, 0);
        assert!(!accum.text_part.is_open);
        assert!(accum.text_part.accumulated_text.is_empty());
        assert!(!accum.refusal_part.is_open);
        assert!(accum.refusal_part.accumulated_text.is_empty());
    }

    #[test]
    fn remember_response_header_sets_identity_once_and_updates_service_tier() {
        let mut accum = OpenResponsesToChatCompletionsAccum::new();
        accum.remember_response_header("resp_1".into(), "gpt-5".into(), 0, Some(ServiceTier::Auto));
        accum.remember_response_header(
            "resp_2".into(),
            "gpt-6".into(),
            20,
            Some(ServiceTier::Default),
        );
        assert_eq!(accum.response_id, "resp_1");
        assert_eq!(accum.model, "gpt-5");
        assert_eq!(accum.created, 0);
        assert!(accum.saw_response_header);
        assert_eq!(accum.service_tier.as_deref(), Some("default"));
    }

    #[test]
    fn inline_tool_call_arguments_to_emit_omits_duplicate_prefix() {
        let mut accum = OpenResponsesToChatCompletionsAccum::new();
        accum.record_emitted_tool_call_arguments("fc_1", "{\"q\":\"x\"}");

        let emitted = accum.inline_tool_call_arguments_to_emit(
            "fc_1",
            "{\"q\":\"x\"}".into(),
            "function_call.arguments",
        );
        assert_eq!(emitted, None);
    }

    #[test]
    fn inline_tool_call_arguments_to_emit_handles_partial_prefix_replay() {
        let mut accum = OpenResponsesToChatCompletionsAccum::new();
        accum.record_emitted_tool_call_arguments("fc_1", "{\"q\":\"");

        let emitted = accum.inline_tool_call_arguments_to_emit(
            "fc_1",
            "{\"q\":\"x\"}".into(),
            "function_call.arguments",
        );
        assert_eq!(emitted.as_deref(), Some("x\"}"));
    }

    #[test]
    fn inline_tool_call_arguments_conflict_warns_dropped() {
        let mut accum = OpenResponsesToChatCompletionsAccum::new();
        accum.record_emitted_tool_call_arguments("fc_1", "{\"a\":1}");

        let emitted = accum.inline_tool_call_arguments_to_emit(
            "fc_1",
            "{\"b\":2}".into(),
            "function_call.arguments",
        );
        assert_eq!(emitted, None);

        let warnings = accum.ctx.take_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "function_call.arguments");
        assert_eq!(warnings[0].action, crate::error::WarningAction::Dropped);
        assert_eq!(
            warnings[0].message,
            "inline tool call arguments conflicted with previously emitted argument deltas"
        );
    }
}
