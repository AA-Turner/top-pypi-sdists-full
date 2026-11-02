use crate::chat_completions_openai::convert::collect::collector::ChatCompletionsCollector;
use crate::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
use crate::chat_completions_openai::stream::ChatCompletionsStreamChunk;
use crate::collect::ResponseCollector;
use crate::error::{ConversionError, ConversionResult};
use crate::traits::CollectStream;

impl CollectStream for ChatCompletionsOpenAiResponse {
    type Event = ChatCompletionsStreamChunk;
    type Response = ChatCompletionsOpenAiResponse;

    fn collect_stream(
        events: impl IntoIterator<Item = ChatCompletionsStreamChunk>,
    ) -> Result<ConversionResult<ChatCompletionsOpenAiResponse>, ConversionError> {
        let mut collector = ChatCompletionsCollector::new();
        for event in events {
            collector.feed(event)?;
        }
        collector.finalize()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::chat_completions_openai::stream::*;
    use crate::chat_completions_openai::types::*;

    fn minimal_stream() -> Vec<ChatCompletionsStreamChunk> {
        vec![
            ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 100,
                model: "gpt-5".into(),
                choices: vec![ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: Some("assistant".into()),
                        content: Some("hi".into()),
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: None,
                    logprobs: None,
                }],
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
            },
            ChatCompletionsStreamChunk {
                id: "chatcmpl_1".into(),
                object: "chat.completion.chunk".into(),
                created: 100,
                model: "gpt-5".into(),
                choices: vec![ChatCompletionsStreamChoice {
                    index: 0,
                    delta: ChatCompletionsStreamDelta {
                        role: None,
                        content: None,
                        tool_calls: None,
                        refusal: None,
                        reasoning_content: None,
                        reasoning_details: None,
                    },
                    finish_reason: Some(ChatCompletionsFinishReason::Stop),
                    logprobs: None,
                }],
                usage: None,
                system_fingerprint: None,
                service_tier: None,
                obfuscation: None,
            },
        ]
    }

    #[test]
    fn delegates_to_collector() {
        let r = ChatCompletionsOpenAiResponse::collect_stream(minimal_stream()).expect("ok");
        assert_eq!(r.value.id, "chatcmpl_1");
        assert_eq!(r.value.choices[0].message.content.as_deref(), Some("hi"));
        assert_eq!(
            r.value.choices[0].finish_reason,
            Some(ChatCompletionsFinishReason::Stop)
        );
        assert!(r.warnings.is_empty());
    }

    #[test]
    fn empty_stream_returns_error() {
        assert!(matches!(
            ChatCompletionsOpenAiResponse::collect_stream(vec![]),
            Err(ConversionError::InvalidInput(_))
        ));
    }
}
