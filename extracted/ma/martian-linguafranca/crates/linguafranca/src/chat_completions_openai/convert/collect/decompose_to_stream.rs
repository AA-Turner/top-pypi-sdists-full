use crate::chat_completions_openai::response::*;
use crate::chat_completions_openai::stream::*;
use crate::chat_completions_openai::types::*;
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::traits::DecomposeToStream;

/// Envelope fields shared by every chunk in a decomposed stream.
struct Envelope {
    id: String,
    created: u64,
    model: String,
    system_fingerprint: Option<String>,
    service_tier: Option<String>,
    choice_index: u32,
}

impl Envelope {
    /// Build a chunk carrying a single choice delta.
    fn delta_chunk(
        &self,
        delta: ChatCompletionsStreamDelta,
        finish_reason: Option<ChatCompletionsFinishReason>,
    ) -> ChatCompletionsStreamChunk {
        self.chunk(
            vec![ChatCompletionsStreamChoice {
                index: self.choice_index,
                delta,
                finish_reason,
                logprobs: None,
            }],
            None,
        )
    }

    /// Build a chunk with arbitrary choices and optional usage.
    fn chunk(
        &self,
        choices: Vec<ChatCompletionsStreamChoice>,
        usage: Option<ChatCompletionsUsage>,
    ) -> ChatCompletionsStreamChunk {
        ChatCompletionsStreamChunk {
            id: self.id.clone(),
            object: "chat.completion.chunk".into(),
            created: self.created,
            model: self.model.clone(),
            choices,
            usage,
            system_fingerprint: self.system_fingerprint.clone(),
            service_tier: self.service_tier.clone(),
            obfuscation: None,
        }
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

fn tool_call_delta(tc: ChatCompletionsStreamToolCall) -> ChatCompletionsStreamDelta {
    ChatCompletionsStreamDelta {
        tool_calls: Some(vec![tc]),
        ..empty_delta()
    }
}

/// Emit start + optional payload chunks for a single tool call.
fn emit_tool_call_chunks(
    events: &mut Vec<ChatCompletionsStreamChunk>,
    env: &Envelope,
    index: u32,
    tc: &ChatCompletionsToolCall,
) {
    match tc {
        ChatCompletionsToolCall::Function { id, function } => {
            events.push(env.delta_chunk(
                tool_call_delta(ChatCompletionsStreamToolCall {
                    index,
                    id: Some(id.clone()),
                    kind: Some("function".into()),
                    function: Some(ChatCompletionsStreamFunctionDelta {
                        name: Some(function.name.clone()),
                        arguments: Some(String::new()),
                    }),
                    custom: None,
                }),
                None,
            ));
            if !function.arguments.is_empty() {
                events.push(env.delta_chunk(
                    tool_call_delta(ChatCompletionsStreamToolCall {
                        index,
                        id: None,
                        kind: None,
                        function: Some(ChatCompletionsStreamFunctionDelta {
                            name: None,
                            arguments: Some(function.arguments.clone()),
                        }),
                        custom: None,
                    }),
                    None,
                ));
            }
        }
        ChatCompletionsToolCall::Custom { id, custom } => {
            events.push(env.delta_chunk(
                tool_call_delta(ChatCompletionsStreamToolCall {
                    index,
                    id: Some(id.clone()),
                    kind: Some("custom".into()),
                    function: None,
                    custom: Some(ChatCompletionsStreamCustomDelta {
                        name: Some(custom.name.clone()),
                        input: Some(String::new()),
                    }),
                }),
                None,
            ));
            if !custom.input.is_empty() {
                events.push(env.delta_chunk(
                    tool_call_delta(ChatCompletionsStreamToolCall {
                        index,
                        id: None,
                        kind: None,
                        function: None,
                        custom: Some(ChatCompletionsStreamCustomDelta {
                            name: None,
                            input: Some(custom.input.clone()),
                        }),
                    }),
                    None,
                ));
            }
        }
    }
}

impl DecomposeToStream for ChatCompletionsOpenAiResponse {
    type Event = ChatCompletionsStreamChunk;

    fn decompose_to_stream(
        self,
    ) -> Result<ConversionResult<Vec<ChatCompletionsStreamChunk>>, ConversionError> {
        let mut warnings = Vec::new();

        if self.choices.is_empty() {
            return Err(ConversionError::InvalidInput(
                "cannot decompose response with no choices".into(),
            ));
        }

        if self.choices.len() > 1 {
            warnings.push(crate::error::ConversionWarning {
                field: "choices".into(),
                action: WarningAction::Changed,
                message: format!(
                    "response has {} choices; only the first is decomposed, rest dropped",
                    self.choices.len()
                ),
            });
        }

        let choice = &self.choices[0];
        let message = &choice.message;
        let mut events = Vec::new();

        let env = Envelope {
            id: self.id.clone(),
            created: self.created,
            model: self.model.clone(),
            system_fingerprint: self.system_fingerprint.clone(),
            service_tier: self.service_tier.clone(),
            choice_index: choice.index,
        };

        // 1. Role prelude chunk.
        events.push(env.delta_chunk(
            ChatCompletionsStreamDelta {
                role: Some(message.role.clone()),
                content: Some(String::new()),
                ..empty_delta()
            },
            None,
        ));

        // 2. Reasoning content (before main content, matching real stream order).
        if let Some(reasoning) = &message.reasoning_content
            && !reasoning.is_empty()
        {
            events.push(env.delta_chunk(
                ChatCompletionsStreamDelta {
                    reasoning_content: Some(reasoning.clone()),
                    ..empty_delta()
                },
                None,
            ));
        }

        // 3. Content delta.
        if let Some(content) = &message.content
            && !content.is_empty()
        {
            events.push(env.delta_chunk(
                ChatCompletionsStreamDelta {
                    content: Some(content.clone()),
                    ..empty_delta()
                },
                None,
            ));
        }

        // 4. Refusal delta.
        if let Some(refusal) = &message.refusal
            && !refusal.is_empty()
        {
            events.push(env.delta_chunk(
                ChatCompletionsStreamDelta {
                    refusal: Some(refusal.clone()),
                    ..empty_delta()
                },
                None,
            ));
        }

        // 5. Tool call chunks.
        if let Some(tool_calls) = &message.tool_calls {
            for (i, tc) in tool_calls.iter().enumerate() {
                emit_tool_call_chunks(&mut events, &env, i as u32, tc);
            }
        }

        if let Some(details) = &message.reasoning_details {
            events.push(env.delta_chunk(
                ChatCompletionsStreamDelta {
                    reasoning_details: Some(details.clone()),
                    ..empty_delta()
                },
                None,
            ));
        }

        // 6. Finish chunk.
        events.push(env.delta_chunk(empty_delta(), choice.finish_reason.clone()));

        // 7. Usage chunk (if present).
        if let Some(usage) = &self.usage {
            events.push(env.chunk(vec![], Some(usage.clone())));
        }

        // Warn about fields lost in stream format.
        if !message.annotations.is_empty() {
            warnings.push(crate::error::ConversionWarning {
                field: "annotations".into(),
                action: WarningAction::Dropped,
                message: format!(
                    "{} annotation(s) dropped; annotations have no stream delta representation",
                    message.annotations.len()
                ),
            });
        }

        if message.audio.is_some() {
            warnings.push(crate::error::ConversionWarning {
                field: "audio".into(),
                action: WarningAction::Dropped,
                message: "audio output dropped; audio has no stream delta representation".into(),
            });
        }

        if choice.logprobs.is_some() {
            warnings.push(crate::error::ConversionWarning {
                field: "logprobs".into(),
                action: WarningAction::Dropped,
                message: "logprobs dropped; per-token logprobs have no stream delta representation"
                    .into(),
            });
        }

        Ok(ConversionResult::with_warnings(events, warnings))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::traits::CollectStream;

    fn make_response(
        message: ChatCompletionsAssistantMessage,
        finish_reason: Option<ChatCompletionsFinishReason>,
    ) -> ChatCompletionsOpenAiResponse {
        ChatCompletionsOpenAiResponse {
            id: "chatcmpl_1".into(),
            object: "chat.completion".into(),
            created: 100,
            model: "gpt-5".into(),
            choices: vec![ChatCompletionsChoice {
                index: 0,
                message,
                finish_reason,
                logprobs: None,
            }],
            usage: Some(ChatCompletionsUsage {
                prompt_tokens: 10,
                completion_tokens: 20,
                total_tokens: 30,
                prompt_tokens_details: None,
                completion_tokens_details: None,
            }),
            system_fingerprint: None,
            service_tier: None,
        }
    }

    fn simple_message(content: &str) -> ChatCompletionsAssistantMessage {
        ChatCompletionsAssistantMessage {
            role: "assistant".into(),
            content: Some(content.into()),
            tool_calls: None,
            refusal: None,
            reasoning_content: None,
            reasoning_details: None,
            annotations: vec![],
            audio: None,
        }
    }

    fn decompose(response: ChatCompletionsOpenAiResponse) -> Vec<ChatCompletionsStreamChunk> {
        response.decompose_to_stream().expect("decompose").value
    }

    fn chunk_deltas(chunks: &[ChatCompletionsStreamChunk]) -> Vec<String> {
        chunks
            .iter()
            .map(|c| {
                if c.choices.is_empty() {
                    return "usage".into();
                }
                let d = &c.choices[0].delta;
                if d.role.is_some() {
                    "role".into()
                } else if d.content.is_some() {
                    format!("content:{}", d.content.as_ref().unwrap())
                } else if d.reasoning_content.is_some() {
                    "reasoning".into()
                } else if d.refusal.is_some() {
                    "refusal".into()
                } else if d.tool_calls.is_some() {
                    let tc = d.tool_calls.as_ref().unwrap();
                    if tc[0].id.is_some() {
                        format!("tc_start:{}", tc[0].index)
                    } else {
                        format!("tc_args:{}", tc[0].index)
                    }
                } else if c.choices[0].finish_reason.is_some() {
                    "finish".into()
                } else {
                    "empty".into()
                }
            })
            .collect()
    }

    // ── Envelope ──

    #[test]
    fn envelope_matches_response() {
        let chunks = decompose(make_response(
            simple_message("hi"),
            Some(ChatCompletionsFinishReason::Stop),
        ));
        for ch in &chunks {
            assert_eq!(ch.id, "chatcmpl_1");
            assert_eq!(ch.object, "chat.completion.chunk");
            assert_eq!(ch.created, 100);
            assert_eq!(ch.model, "gpt-5");
        }
    }

    #[test]
    fn choice_index_preserved() {
        let mut response = make_response(
            simple_message("hi"),
            Some(ChatCompletionsFinishReason::Stop),
        );
        response.choices[0].index = 7;
        let chunks = decompose(response);
        for ch in &chunks {
            for choice in &ch.choices {
                assert_eq!(choice.index, 7, "choice index should be preserved");
            }
        }
    }

    // ── Event sequence ──

    #[test]
    fn simple_text_event_sequence() {
        let chunks = decompose(make_response(
            simple_message("Hello"),
            Some(ChatCompletionsFinishReason::Stop),
        ));
        assert_eq!(
            chunk_deltas(&chunks),
            ["role", "content:Hello", "finish", "usage"]
        );
    }

    #[test]
    fn empty_content_skips_content_delta() {
        let msg = ChatCompletionsAssistantMessage {
            content: None,
            ..simple_message("")
        };
        let chunks = decompose(make_response(msg, Some(ChatCompletionsFinishReason::Stop)));
        assert_eq!(chunk_deltas(&chunks), ["role", "finish", "usage"]);
    }

    #[test]
    fn reasoning_before_content() {
        let msg = ChatCompletionsAssistantMessage {
            reasoning_content: Some("think".into()),
            ..simple_message("answer")
        };
        let chunks = decompose(make_response(msg, Some(ChatCompletionsFinishReason::Stop)));
        assert_eq!(
            chunk_deltas(&chunks),
            ["role", "reasoning", "content:answer", "finish", "usage"]
        );
    }

    #[test]
    fn refusal_emitted() {
        let msg = ChatCompletionsAssistantMessage {
            refusal: Some("no".into()),
            content: None,
            ..simple_message("")
        };
        let chunks = decompose(make_response(msg, Some(ChatCompletionsFinishReason::Stop)));
        assert_eq!(
            chunk_deltas(&chunks),
            ["role", "refusal", "finish", "usage"]
        );
    }

    #[test]
    fn tool_calls_emit_start_and_args() {
        let msg = ChatCompletionsAssistantMessage {
            content: None,
            tool_calls: Some(vec![
                ChatCompletionsToolCall::Function {
                    id: "call_1".into(),
                    function: ChatCompletionsFunctionCallData {
                        name: "fn_a".into(),
                        arguments: "{\"x\":1}".into(),
                    },
                },
                ChatCompletionsToolCall::Function {
                    id: "call_2".into(),
                    function: ChatCompletionsFunctionCallData {
                        name: "fn_b".into(),
                        arguments: "{}".into(),
                    },
                },
            ]),
            ..simple_message("")
        };
        let chunks = decompose(make_response(
            msg,
            Some(ChatCompletionsFinishReason::ToolCalls),
        ));
        assert_eq!(
            chunk_deltas(&chunks),
            [
                "role",
                "tc_start:0",
                "tc_args:0",
                "tc_start:1",
                "tc_args:1",
                "finish",
                "usage"
            ]
        );
    }

    #[test]
    fn empty_arguments_skips_args_chunk() {
        let msg = ChatCompletionsAssistantMessage {
            content: None,
            tool_calls: Some(vec![ChatCompletionsToolCall::Function {
                id: "call_1".into(),
                function: ChatCompletionsFunctionCallData {
                    name: "fn_a".into(),
                    arguments: String::new(),
                },
            }]),
            ..simple_message("")
        };
        let chunks = decompose(make_response(
            msg,
            Some(ChatCompletionsFinishReason::ToolCalls),
        ));
        assert_eq!(
            chunk_deltas(&chunks),
            ["role", "tc_start:0", "finish", "usage"]
        );
    }

    // ── Warnings ──

    #[test]
    fn annotations_warn_dropped() {
        let msg = ChatCompletionsAssistantMessage {
            annotations: vec![ChatCompletionsAnnotation::UrlCitation {
                url_citation: ChatCompletionsUrlCitation {
                    url: "https://example.com".into(),
                    title: "Ex".into(),
                    start_index: 0,
                    end_index: 3,
                },
            }],
            ..simple_message("text")
        };
        let result = make_response(msg, Some(ChatCompletionsFinishReason::Stop))
            .decompose_to_stream()
            .unwrap();
        assert!(result.warnings.iter().any(|w| w.field == "annotations"));
    }

    #[test]
    fn audio_warns_dropped() {
        let msg = ChatCompletionsAssistantMessage {
            audio: Some(ChatCompletionsAudioOutput {
                id: "a".into(),
                data: "d".into(),
                expires_at: 0,
                transcript: "t".into(),
            }),
            ..simple_message("text")
        };
        let result = make_response(msg, Some(ChatCompletionsFinishReason::Stop))
            .decompose_to_stream()
            .unwrap();
        assert!(result.warnings.iter().any(|w| w.field == "audio"));
    }

    #[test]
    fn logprobs_warns_dropped() {
        let response = ChatCompletionsOpenAiResponse {
            choices: vec![ChatCompletionsChoice {
                logprobs: Some(serde_json::json!({"content": []})),
                ..ChatCompletionsChoice {
                    index: 0,
                    message: simple_message("text"),
                    finish_reason: Some(ChatCompletionsFinishReason::Stop),
                    logprobs: None,
                }
            }],
            ..make_response(
                simple_message("text"),
                Some(ChatCompletionsFinishReason::Stop),
            )
        };
        let result = response.decompose_to_stream().unwrap();
        assert!(result.warnings.iter().any(|w| w.field == "logprobs"));
    }

    #[test]
    fn no_choices_returns_error() {
        let response = ChatCompletionsOpenAiResponse {
            id: "x".into(),
            object: "chat.completion".into(),
            created: 0,
            model: "m".into(),
            choices: vec![],
            usage: None,
            system_fingerprint: None,
            service_tier: None,
        };
        assert!(response.decompose_to_stream().is_err());
    }

    // ── Round-trips ──

    fn assert_round_trip(response: ChatCompletionsOpenAiResponse) {
        let events = response.clone().decompose_to_stream().expect("decompose");
        // Only check if decompose had no warnings (annotations/audio cause expected loss).
        let collected =
            ChatCompletionsOpenAiResponse::collect_stream(events.value).expect("collect");
        assert_eq!(collected.value, response, "round-trip mismatch");
        assert!(
            collected.warnings.is_empty(),
            "unexpected collect warnings: {:?}",
            collected.warnings
        );
    }

    #[test]
    fn round_trip_simple_text() {
        assert_round_trip(make_response(
            simple_message("Hello world"),
            Some(ChatCompletionsFinishReason::Stop),
        ));
    }

    #[test]
    fn round_trip_with_reasoning() {
        assert_round_trip(make_response(
            ChatCompletionsAssistantMessage {
                reasoning_content: Some("thinking...".into()),
                ..simple_message("answer")
            },
            Some(ChatCompletionsFinishReason::Stop),
        ));
    }

    #[test]
    fn round_trip_tool_calls() {
        assert_round_trip(make_response(
            ChatCompletionsAssistantMessage {
                content: None,
                tool_calls: Some(vec![
                    ChatCompletionsToolCall::Function {
                        id: "call_1".into(),
                        function: ChatCompletionsFunctionCallData {
                            name: "get_weather".into(),
                            arguments: "{\"city\":\"Paris\"}".into(),
                        },
                    },
                    ChatCompletionsToolCall::Custom {
                        id: "call_2".into(),
                        custom: ChatCompletionsCustomCallData {
                            name: "apply_patch".into(),
                            input: "patch data".into(),
                        },
                    },
                ]),
                ..simple_message("")
            },
            Some(ChatCompletionsFinishReason::ToolCalls),
        ));
    }

    #[test]
    fn round_trip_max_tokens() {
        assert_round_trip(make_response(
            simple_message("truncated"),
            Some(ChatCompletionsFinishReason::Length),
        ));
    }

    #[test]
    fn round_trip_with_refusal() {
        assert_round_trip(make_response(
            ChatCompletionsAssistantMessage {
                content: Some("partial".into()),
                refusal: Some("Policy block".into()),
                ..simple_message("")
            },
            Some(ChatCompletionsFinishReason::Stop),
        ));
    }

    #[test]
    fn round_trip_content_and_tool_calls() {
        assert_round_trip(make_response(
            ChatCompletionsAssistantMessage {
                content: Some("Let me look that up.".into()),
                tool_calls: Some(vec![ChatCompletionsToolCall::Function {
                    id: "call_1".into(),
                    function: ChatCompletionsFunctionCallData {
                        name: "search".into(),
                        arguments: "{\"q\":\"rust\"}".into(),
                    },
                }]),
                ..simple_message("")
            },
            Some(ChatCompletionsFinishReason::ToolCalls),
        ));
    }
}
