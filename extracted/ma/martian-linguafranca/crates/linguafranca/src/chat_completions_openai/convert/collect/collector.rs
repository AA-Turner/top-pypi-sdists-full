use std::collections::BTreeMap;

use crate::chat_completions_openai::response::*;
use crate::chat_completions_openai::stream::*;
use crate::chat_completions_openai::types::*;
use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult, ConversionWarning, WarningAction};

/// Stateful collector that accumulates Chat Completions stream chunks
/// into a single [`ChatCompletionsOpenAiResponse`].
///
/// Feed chunks one at a time via [`ResponseCollector::feed`], then call
/// [`ResponseCollector::finalize`] to obtain the response.
///
/// Implements [`DynResponseCollector`](crate::collect::DynResponseCollector)
/// via the blanket impl, so it can be used type-erased at the Python boundary.
pub struct ChatCompletionsCollector {
    // Envelope (captured from the first chunk).
    id: Option<String>,
    object: Option<String>,
    created: Option<u64>,
    model: Option<String>,
    system_fingerprint: Option<String>,
    service_tier: Option<String>,

    // Accumulated message fields.
    role: Option<String>,
    content: String,
    reasoning_content: String,
    reasoning_details: Vec<serde_json::Value>,
    refusal: String,

    // Tool calls keyed by their stream `index`.
    tool_calls: BTreeMap<u32, ToolCallInProgress>,

    // Terminal state.
    finish_reason: Option<ChatCompletionsFinishReason>,
    usage: Option<ChatCompletionsUsage>,

    // Bookkeeping.
    warnings: Vec<ConversionWarning>,
    saw_any_event: bool,
    saw_finish_reason: bool,
    warned_multiple_choices: bool,
    warned_logprobs: bool,
    finalized: bool,
}

enum ToolCallInProgress {
    Function {
        id: String,
        name: String,
        arguments: String,
    },
    Custom {
        id: String,
        name: String,
        input: String,
    },
}

impl Default for ChatCompletionsCollector {
    fn default() -> Self {
        Self::new()
    }
}

impl ChatCompletionsCollector {
    pub fn new() -> Self {
        Self {
            id: None,
            object: None,
            created: None,
            model: None,
            system_fingerprint: None,
            service_tier: None,

            role: None,
            content: String::new(),
            reasoning_content: String::new(),
            reasoning_details: Vec::new(),
            refusal: String::new(),

            tool_calls: BTreeMap::new(),

            finish_reason: None,
            usage: None,

            warnings: Vec::new(),
            saw_any_event: false,
            saw_finish_reason: false,
            warned_multiple_choices: false,
            warned_logprobs: false,
            finalized: false,
        }
    }

    fn capture_envelope(&mut self, chunk: &ChatCompletionsStreamChunk) {
        if self.id.is_none() {
            self.id = Some(chunk.id.clone());
            self.object = Some("chat.completion".into());
            self.created = Some(chunk.created);
            self.model = Some(chunk.model.clone());
            self.system_fingerprint = chunk.system_fingerprint.clone();
            self.service_tier = chunk.service_tier.clone();
        }
    }

    fn process_tool_call_delta(&mut self, tc: ChatCompletionsStreamToolCall) {
        let idx = tc.index;

        if let Some(existing) = self.tool_calls.get_mut(&idx) {
            // Append payload to existing tool call.
            match existing {
                ToolCallInProgress::Function { arguments, .. } => {
                    if let Some(f) = &tc.function
                        && let Some(args) = &f.arguments
                    {
                        arguments.push_str(args);
                    }
                }
                ToolCallInProgress::Custom { input, .. } => {
                    if let Some(c) = &tc.custom
                        && let Some(inp) = &c.input
                    {
                        input.push_str(inp);
                    }
                }
            }
            return;
        }

        // New tool call — must have an id.
        let Some(id) = tc.id else {
            self.warnings.push(ConversionWarning {
                field: "tool_calls".into(),
                action: WarningAction::Dropped,
                message: format!(
                    "tool_call delta at index {idx} has no id and no existing entry, dropped"
                ),
            });
            return;
        };

        let kind = tc.kind.as_deref().unwrap_or("function");
        match kind {
            "function" => {
                let (name, arguments) = match tc.function {
                    Some(f) => (f.name.unwrap_or_default(), f.arguments.unwrap_or_default()),
                    None => (String::new(), String::new()),
                };
                self.tool_calls.insert(
                    idx,
                    ToolCallInProgress::Function {
                        id,
                        name,
                        arguments,
                    },
                );
            }
            "custom" => {
                let (name, input) = match tc.custom {
                    Some(c) => (c.name.unwrap_or_default(), c.input.unwrap_or_default()),
                    None => (String::new(), String::new()),
                };
                self.tool_calls
                    .insert(idx, ToolCallInProgress::Custom { id, name, input });
            }
            other => {
                self.warnings.push(ConversionWarning {
                    field: "tool_calls".into(),
                    action: WarningAction::Dropped,
                    message: format!("unknown tool_call type '{other}' at index {idx}, dropped"),
                });
            }
        }
    }
}

impl ResponseCollector for ChatCompletionsCollector {
    type Event = ChatCompletionsStreamChunk;
    type Response = ChatCompletionsOpenAiResponse;

    fn feed(&mut self, chunk: ChatCompletionsStreamChunk) -> Result<(), ConversionError> {
        if self.finalized {
            return Err(ConversionError::InvalidInput(
                "cannot feed events after finalize".into(),
            ));
        }

        self.saw_any_event = true;
        self.capture_envelope(&chunk);

        // Usage-only chunk (empty choices).
        if chunk.choices.is_empty() {
            if let Some(usage) = chunk.usage {
                self.usage = Some(usage);
            }
            return Ok(());
        }

        if chunk.choices.len() > 1 && !self.warned_multiple_choices {
            self.warned_multiple_choices = true;
            self.warnings.push(ConversionWarning {
                field: "choices".into(),
                action: WarningAction::Changed,
                message: format!(
                    "stream chunk has {} choices; only the first is collected, rest dropped",
                    chunk.choices.len()
                ),
            });
        }

        // Process the first choice only.
        let choice = &chunk.choices[0];

        if choice.logprobs.is_some() && !self.warned_logprobs {
            self.warned_logprobs = true;
            self.warnings.push(ConversionWarning {
                field: "logprobs".into(),
                action: WarningAction::Dropped,
                message: "per-token logprobs dropped; not collected into the response".into(),
            });
        }

        if let Some(fr) = &choice.finish_reason {
            self.finish_reason = Some(fr.clone());
            self.saw_finish_reason = true;
        }

        let delta = &choice.delta;

        if let Some(role) = &delta.role
            && self.role.is_none()
        {
            self.role = Some(role.clone());
        }

        if let Some(text) = &delta.content {
            self.content.push_str(text);
        }

        if let Some(reasoning) = &delta.reasoning_content {
            self.reasoning_content.push_str(reasoning);
        }

        if let Some(details) = &delta.reasoning_details {
            self.reasoning_details.extend(details.iter().cloned());
        }

        if let Some(refusal) = &delta.refusal {
            self.refusal.push_str(refusal);
        }

        if let Some(tool_calls) = delta.tool_calls.clone() {
            for tc in tool_calls {
                self.process_tool_call_delta(tc);
            }
        }

        Ok(())
    }

    fn finalize(
        &mut self,
    ) -> Result<ConversionResult<ChatCompletionsOpenAiResponse>, ConversionError> {
        if self.finalized {
            return Err(ConversionError::InvalidInput(
                "collector has already been finalized".into(),
            ));
        }
        self.finalized = true;

        if !self.saw_any_event {
            return Err(ConversionError::InvalidInput(
                "cannot collect stream: no events received".into(),
            ));
        }

        // Build tool_calls vec from accumulated data.
        let tool_calls: Vec<ChatCompletionsToolCall> = self
            .tool_calls
            .values()
            .map(|tc| match tc {
                ToolCallInProgress::Function {
                    id,
                    name,
                    arguments,
                } => ChatCompletionsToolCall::Function {
                    id: id.clone(),
                    function: ChatCompletionsFunctionCallData {
                        name: name.clone(),
                        arguments: arguments.clone(),
                    },
                },
                ToolCallInProgress::Custom { id, name, input } => ChatCompletionsToolCall::Custom {
                    id: id.clone(),
                    custom: ChatCompletionsCustomCallData {
                        name: name.clone(),
                        input: input.clone(),
                    },
                },
            })
            .collect();

        let message = ChatCompletionsAssistantMessage {
            role: self.role.take().unwrap_or_else(|| "assistant".into()),
            content: if self.content.is_empty() {
                None
            } else {
                Some(std::mem::take(&mut self.content))
            },
            tool_calls: if tool_calls.is_empty() {
                None
            } else {
                Some(tool_calls)
            },
            refusal: if self.refusal.is_empty() {
                None
            } else {
                Some(std::mem::take(&mut self.refusal))
            },
            reasoning_content: if self.reasoning_content.is_empty() {
                None
            } else {
                Some(std::mem::take(&mut self.reasoning_content))
            },
            reasoning_details: (!self.reasoning_details.is_empty())
                .then(|| std::mem::take(&mut self.reasoning_details)),
            annotations: vec![],
            audio: None,
        };

        let choice = ChatCompletionsChoice {
            index: 0,
            message,
            finish_reason: self.finish_reason.take(),
            logprobs: None,
        };

        let response = ChatCompletionsOpenAiResponse {
            id: self.id.take().unwrap_or_default(),
            object: self
                .object
                .take()
                .unwrap_or_else(|| "chat.completion".into()),
            created: self.created.unwrap_or(0),
            model: self.model.take().unwrap_or_default(),
            choices: vec![choice],
            usage: self.usage.take(),
            system_fingerprint: self.system_fingerprint.take(),
            service_tier: self.service_tier.take(),
        };

        let mut result =
            ConversionResult::with_warnings(response, std::mem::take(&mut self.warnings));

        if !self.saw_finish_reason {
            result.warn(
                "finish_reason",
                WarningAction::Changed,
                "stream ended without a finish_reason chunk",
            );
        }

        Ok(result)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // ── Helpers ──

    fn chunk(
        delta: ChatCompletionsStreamDelta,
        finish_reason: Option<ChatCompletionsFinishReason>,
    ) -> ChatCompletionsStreamChunk {
        ChatCompletionsStreamChunk {
            id: "chatcmpl_1".into(),
            object: "chat.completion.chunk".into(),
            created: 100,
            model: "gpt-5".into(),
            choices: vec![ChatCompletionsStreamChoice {
                index: 0,
                delta,
                finish_reason,
                logprobs: None,
            }],
            usage: None,
            system_fingerprint: None,
            service_tier: None,
            obfuscation: None,
        }
    }

    fn empty_delta() -> ChatCompletionsStreamDelta {
        ChatCompletionsStreamDelta {
            role: None,
            content: None,
            tool_calls: None,
            refusal: None,
            reasoning_content: None,
            reasoning_details: None,
        }
    }

    fn role_chunk() -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                role: Some("assistant".into()),
                content: Some(String::new()),
                ..empty_delta()
            },
            None,
        )
    }

    fn content_chunk(text: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                content: Some(text.into()),
                ..empty_delta()
            },
            None,
        )
    }

    fn reasoning_chunk(text: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                reasoning_content: Some(text.into()),
                ..empty_delta()
            },
            None,
        )
    }

    fn refusal_chunk(text: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                refusal: Some(text.into()),
                ..empty_delta()
            },
            None,
        )
    }

    fn finish_chunk(reason: ChatCompletionsFinishReason) -> ChatCompletionsStreamChunk {
        chunk(empty_delta(), Some(reason))
    }

    fn fn_tc_start(index: u32, id: &str, name: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                    index,
                    id: Some(id.into()),
                    kind: Some("function".into()),
                    function: Some(ChatCompletionsStreamFunctionDelta {
                        name: Some(name.into()),
                        arguments: Some(String::new()),
                    }),
                    custom: None,
                }]),
                ..empty_delta()
            },
            None,
        )
    }

    fn fn_tc_args(index: u32, args: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                    index,
                    id: None,
                    kind: None,
                    function: Some(ChatCompletionsStreamFunctionDelta {
                        name: None,
                        arguments: Some(args.into()),
                    }),
                    custom: None,
                }]),
                ..empty_delta()
            },
            None,
        )
    }

    fn custom_tc_start(index: u32, id: &str, name: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                    index,
                    id: Some(id.into()),
                    kind: Some("custom".into()),
                    function: None,
                    custom: Some(ChatCompletionsStreamCustomDelta {
                        name: Some(name.into()),
                        input: Some(String::new()),
                    }),
                }]),
                ..empty_delta()
            },
            None,
        )
    }

    fn custom_tc_input(index: u32, input: &str) -> ChatCompletionsStreamChunk {
        chunk(
            ChatCompletionsStreamDelta {
                tool_calls: Some(vec![ChatCompletionsStreamToolCall {
                    index,
                    id: None,
                    kind: None,
                    function: None,
                    custom: Some(ChatCompletionsStreamCustomDelta {
                        name: None,
                        input: Some(input.into()),
                    }),
                }]),
                ..empty_delta()
            },
            None,
        )
    }

    fn orphan_tc_args(index: u32, args: &str) -> ChatCompletionsStreamChunk {
        fn_tc_args(index, args) // same shape: no id, just arguments
    }

    fn usage_chunk(usage: ChatCompletionsUsage) -> ChatCompletionsStreamChunk {
        ChatCompletionsStreamChunk {
            id: "chatcmpl_1".into(),
            object: "chat.completion.chunk".into(),
            created: 100,
            model: "gpt-5".into(),
            choices: vec![],
            usage: Some(usage),
            system_fingerprint: None,
            service_tier: None,
            obfuscation: None,
        }
    }

    fn simple_usage() -> ChatCompletionsUsage {
        ChatCompletionsUsage {
            prompt_tokens: 10,
            completion_tokens: 5,
            total_tokens: 15,
            prompt_tokens_details: None,
            completion_tokens_details: None,
        }
    }

    fn collect(
        chunks: Vec<ChatCompletionsStreamChunk>,
    ) -> ConversionResult<ChatCompletionsOpenAiResponse> {
        let mut c = ChatCompletionsCollector::new();
        for ch in chunks {
            c.feed(ch).unwrap();
        }
        c.finalize().unwrap()
    }

    // ── Basic text collection ──

    #[test]
    fn text_deltas_are_concatenated() {
        let r = collect(vec![
            role_chunk(),
            content_chunk("Hello"),
            content_chunk(" world"),
            finish_chunk(ChatCompletionsFinishReason::Stop),
            usage_chunk(simple_usage()),
        ]);

        assert_eq!(
            r.value.choices[0].message.content.as_deref(),
            Some("Hello world")
        );
        assert_eq!(
            r.value.choices[0].finish_reason,
            Some(ChatCompletionsFinishReason::Stop)
        );
        assert_eq!(r.value.usage.as_ref().unwrap().completion_tokens, 5);
        assert!(r.warnings.is_empty());
    }

    #[test]
    fn envelope_captured_from_first_chunk() {
        let r = collect(vec![
            role_chunk(),
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);

        assert_eq!(r.value.id, "chatcmpl_1");
        assert_eq!(r.value.object, "chat.completion");
        assert_eq!(r.value.created, 100);
        assert_eq!(r.value.model, "gpt-5");
    }

    // ── Tool calls ──

    #[test]
    fn function_tool_call_reassembled() {
        let r = collect(vec![
            role_chunk(),
            fn_tc_start(0, "call_1", "get_weather"),
            fn_tc_args(0, "{\"city\":\"Paris\"}"),
            finish_chunk(ChatCompletionsFinishReason::ToolCalls),
        ]);

        let tc = r.value.choices[0].message.tool_calls.as_ref().unwrap();
        assert_eq!(tc.len(), 1);
        match &tc[0] {
            ChatCompletionsToolCall::Function { id, function } => {
                assert_eq!(id, "call_1");
                assert_eq!(function.name, "get_weather");
                assert_eq!(function.arguments, "{\"city\":\"Paris\"}");
            }
            other => panic!("expected Function, got {other:?}"),
        }
    }

    #[test]
    fn multiple_tool_calls_ordered_by_index() {
        let r = collect(vec![
            role_chunk(),
            fn_tc_start(0, "call_a", "fn_a"),
            fn_tc_args(0, "{}"),
            fn_tc_start(1, "call_b", "fn_b"),
            fn_tc_args(1, "{\"x\":1}"),
            finish_chunk(ChatCompletionsFinishReason::ToolCalls),
        ]);

        let tc = r.value.choices[0].message.tool_calls.as_ref().unwrap();
        assert_eq!(tc.len(), 2);
        match &tc[0] {
            ChatCompletionsToolCall::Function { id, .. } => assert_eq!(id, "call_a"),
            other => panic!("expected Function, got {other:?}"),
        }
        match &tc[1] {
            ChatCompletionsToolCall::Function { id, .. } => assert_eq!(id, "call_b"),
            other => panic!("expected Function, got {other:?}"),
        }
    }

    #[test]
    fn custom_tool_call_reassembled() {
        let r = collect(vec![
            role_chunk(),
            custom_tc_start(0, "call_c", "apply_patch"),
            custom_tc_input(0, "patch_"),
            custom_tc_input(0, "data"),
            finish_chunk(ChatCompletionsFinishReason::ToolCalls),
        ]);

        let tc = r.value.choices[0].message.tool_calls.as_ref().unwrap();
        match &tc[0] {
            ChatCompletionsToolCall::Custom { id, custom } => {
                assert_eq!(id, "call_c");
                assert_eq!(custom.name, "apply_patch");
                assert_eq!(custom.input, "patch_data");
            }
            other => panic!("expected Custom, got {other:?}"),
        }
    }

    #[test]
    fn tool_call_delta_without_id_warns() {
        let r = collect(vec![
            role_chunk(),
            orphan_tc_args(5, "orphan"),
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);

        assert!(r.warnings.iter().any(|w| w.field == "tool_calls"
            && w.message.contains("index 5")
            && w.message.contains("no id")));
    }

    // ── Reasoning and refusal ──

    #[test]
    fn reasoning_content_accumulated() {
        let r = collect(vec![
            role_chunk(),
            reasoning_chunk("step 1"),
            reasoning_chunk(", step 2"),
            content_chunk("answer"),
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);

        assert_eq!(
            r.value.choices[0].message.reasoning_content.as_deref(),
            Some("step 1, step 2")
        );
        assert_eq!(
            r.value.choices[0].message.content.as_deref(),
            Some("answer")
        );
    }

    #[test]
    fn refusal_accumulated() {
        let r = collect(vec![
            role_chunk(),
            refusal_chunk("I cannot"),
            refusal_chunk(" comply"),
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);

        assert_eq!(
            r.value.choices[0].message.refusal.as_deref(),
            Some("I cannot comply")
        );
    }

    // ── Edge cases ──

    #[test]
    fn missing_finish_reason_warns() {
        let r = collect(vec![role_chunk(), content_chunk("hi")]);
        assert!(r.warnings.iter().any(|w| w.field == "finish_reason"));
    }

    #[test]
    fn empty_content_becomes_none() {
        let r = collect(vec![
            role_chunk(),
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);
        assert_eq!(r.value.choices[0].message.content, None);
    }

    #[test]
    fn no_events_returns_error() {
        assert!(
            ChatCompletionsCollector::new()
                .finalize()
                .unwrap_err()
                .to_string()
                .contains("no events")
        );
    }

    #[test]
    fn double_finalize_returns_error() {
        let mut c = ChatCompletionsCollector::new();
        c.feed(role_chunk()).unwrap();
        c.feed(finish_chunk(ChatCompletionsFinishReason::Stop))
            .unwrap();
        assert!(c.finalize().is_ok());
        assert!(
            c.finalize()
                .unwrap_err()
                .to_string()
                .contains("already been finalized")
        );
    }

    #[test]
    fn feed_after_finalize_returns_error() {
        let mut c = ChatCompletionsCollector::new();
        c.feed(role_chunk()).unwrap();
        c.finalize().unwrap();
        assert!(
            c.feed(role_chunk())
                .unwrap_err()
                .to_string()
                .contains("after finalize")
        );
    }

    #[test]
    fn usage_from_dedicated_chunk() {
        let r = collect(vec![
            role_chunk(),
            content_chunk("hi"),
            finish_chunk(ChatCompletionsFinishReason::Stop),
            usage_chunk(simple_usage()),
        ]);
        assert_eq!(r.value.usage.as_ref().unwrap().total_tokens, 15);
    }

    #[test]
    fn service_tier_and_fingerprint_captured() {
        let mut ch = role_chunk();
        ch.service_tier = Some("default".into());
        ch.system_fingerprint = Some("fp_abc".into());
        let r = collect(vec![ch, finish_chunk(ChatCompletionsFinishReason::Stop)]);
        assert_eq!(r.value.service_tier.as_deref(), Some("default"));
        assert_eq!(r.value.system_fingerprint.as_deref(), Some("fp_abc"));
    }

    #[test]
    fn logprobs_in_stream_warns_once() {
        let mut ch = chunk(
            ChatCompletionsStreamDelta {
                content: Some("hi".into()),
                ..empty_delta()
            },
            None,
        );
        ch.choices[0].logprobs = Some(serde_json::json!({"content": []}));

        let mut ch2 = chunk(
            ChatCompletionsStreamDelta {
                content: Some(" there".into()),
                ..empty_delta()
            },
            None,
        );
        ch2.choices[0].logprobs = Some(serde_json::json!({"content": []}));

        let r = collect(vec![
            role_chunk(),
            ch,
            ch2,
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);
        let lp_warnings: Vec<_> = r
            .warnings
            .iter()
            .filter(|w| w.field == "logprobs")
            .collect();
        assert_eq!(lp_warnings.len(), 1);
        assert!(lp_warnings[0].message.contains("logprobs"));
    }

    #[test]
    fn multiple_choices_warns_once() {
        let multi_choice = ChatCompletionsStreamChunk {
            choices: vec![
                ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        content: Some("a".into()),
                        ..empty_delta()
                    },
                    finish_reason: None,
                    logprobs: None,
                },
                ChatCompletionsStreamChoice {
                    index: 1,
                    delta: ChatCompletionsStreamDelta {
                        content: Some("b".into()),
                        ..empty_delta()
                    },
                    finish_reason: None,
                    logprobs: None,
                },
            ],
            ..role_chunk()
        };
        let r = collect(vec![
            role_chunk(),
            multi_choice.clone(),
            multi_choice,
            finish_chunk(ChatCompletionsFinishReason::Stop),
        ]);

        // Only first choice collected.
        assert_eq!(r.value.choices[0].message.content.as_deref(), Some("aa"));
        // Warning emitted exactly once.
        let choice_warnings: Vec<_> = r.warnings.iter().filter(|w| w.field == "choices").collect();
        assert_eq!(choice_warnings.len(), 1);
        assert!(choice_warnings[0].message.contains("2 choices"));
    }
}
