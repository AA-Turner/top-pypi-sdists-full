use crate::chat_completions_openai::types::{
    ChatCompletionsContent, ChatCompletionsMessage, ChatCompletionsToolCall,
};
use crate::open_responses::types::{
    FunctionCallOutputValue, InputContent, InputItem, MessageRole, SummaryContent,
    SummaryContentType,
};

/// Accumulates Chat Completions messages while buffering consecutive
/// function calls into one assistant message with `tool_calls`.
pub(super) struct ChatCompletionsMessageAccum {
    messages: Vec<ChatCompletionsMessage>,
    pending_tool_calls: Vec<ChatCompletionsToolCall>,
}

impl ChatCompletionsMessageAccum {
    pub(super) fn new() -> Self {
        Self {
            messages: Vec::new(),
            pending_tool_calls: Vec::new(),
        }
    }

    pub(super) fn push_message(&mut self, mut message: ChatCompletionsMessage) {
        self.flush_pending_tool_calls();
        if let ChatCompletionsMessage::Assistant { content, .. } = &mut message
            && let Some(ChatCompletionsMessage::Assistant {
                content: pending_content,
                reasoning_details: Some(_),
                tool_calls: None,
                ..
            }) = self.messages.last_mut()
            && matches!(pending_content.as_ref(), Some(ChatCompletionsContent::Text(text)) if text.is_empty())
        {
            *pending_content = content.take();
            return;
        }

        self.messages.push(message);
    }

    pub(super) fn push_function_call(&mut self, call: ChatCompletionsToolCall) {
        self.pending_tool_calls.push(call);
    }

    pub(super) fn push_tool_output(&mut self, tool_output: ChatCompletionsMessage) {
        self.flush_pending_tool_calls();
        self.messages.push(tool_output);
    }

    pub(super) fn push_reasoning(&mut self, reasoning: ChatCompletionsMessage) {
        self.flush_pending_tool_calls();
        self.messages.push(reasoning);
    }

    pub(super) fn flush_pending_tool_calls(&mut self) {
        if self.pending_tool_calls.is_empty() {
            return;
        }
        let tool_calls = std::mem::take(&mut self.pending_tool_calls);
        // Keep the encrypted reasoning carrier on the assistant turn that calls tools.
        if let Some(ChatCompletionsMessage::Assistant {
            reasoning_details: Some(_),
            tool_calls: pending @ None,
            ..
        }) = self.messages.last_mut()
        {
            *pending = Some(tool_calls);
            return;
        }

        self.messages.push(ChatCompletionsMessage::Assistant {
            content: None,
            name: None,
            tool_calls: Some(tool_calls),
            refusal: None,
            reasoning_content: None,
            reasoning_details: None,
        });
    }

    pub(super) fn finish(mut self) -> Vec<ChatCompletionsMessage> {
        self.flush_pending_tool_calls();
        self.messages
    }
}

/// Accumulates Open Responses input items while preserving source message order.
pub(super) struct OrInputItemAccum {
    items: Vec<InputItem>,
}

impl OrInputItemAccum {
    pub(super) fn new() -> Self {
        Self { items: Vec::new() }
    }

    pub(super) fn push_message(&mut self, role: MessageRole, content: InputContent) {
        self.items.push(InputItem::Message {
            role,
            content,
            id: None,
            status: None,
        });
    }

    pub(super) fn push_reasoning(
        &mut self,
        text: Option<String>,
        encrypted_content: Option<String>,
    ) {
        self.items.push(InputItem::Reasoning {
            summary: text
                .map(|text| SummaryContent {
                    kind: SummaryContentType::SummaryText,
                    text,
                })
                .into_iter()
                .collect(),
            id: None,
            encrypted_content,
        });
    }

    pub(super) fn push_function_call(&mut self, call_id: String, name: String, arguments: String) {
        self.items.push(InputItem::FunctionCall {
            call_id,
            name,
            namespace: None,
            arguments,
            id: None,
            status: None,
        });
    }

    pub(super) fn push_function_call_output(
        &mut self,
        call_id: String,
        output: FunctionCallOutputValue,
    ) {
        self.items.push(InputItem::FunctionCallOutput {
            call_id,
            output,
            id: None,
            status: None,
        });
    }

    pub(super) fn push_custom_tool_call(&mut self, call_id: String, name: String, input: String) {
        self.items.push(InputItem::CustomToolCall {
            call_id,
            name,
            namespace: None,
            input,
            id: None,
            status: None,
        });
    }

    pub(super) fn finish(self) -> Vec<InputItem> {
        self.items
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::chat_completions_openai::types::ChatCompletionsFunctionCallData;

    #[test]
    fn preserves_order_when_tool_calls_flush_between_messages() {
        let mut accum = ChatCompletionsMessageAccum::new();

        accum.push_message(ChatCompletionsMessage::User {
            content: ChatCompletionsContent::Text("first user".into()),
            name: None,
        });
        accum.push_function_call(ChatCompletionsToolCall::Function {
            id: "call_1".into(),
            function: ChatCompletionsFunctionCallData {
                name: "lookup".into(),
                arguments: "{}".into(),
            },
        });
        accum.push_message(ChatCompletionsMessage::User {
            content: ChatCompletionsContent::Text("second user".into()),
            name: None,
        });

        let messages = accum.finish();
        assert_eq!(messages.len(), 3);
        assert!(matches!(messages[0], ChatCompletionsMessage::User { .. }));
        assert!(matches!(
            messages[1],
            ChatCompletionsMessage::Assistant { .. }
        ));
        assert!(matches!(messages[2], ChatCompletionsMessage::User { .. }));

        match &messages[0] {
            ChatCompletionsMessage::User {
                content: ChatCompletionsContent::Text(t),
                ..
            } => assert_eq!(t, "first user"),
            other => panic!("expected first user message, got {other:?}"),
        }

        match &messages[1] {
            ChatCompletionsMessage::Assistant { tool_calls, .. } => {
                let tool_calls = tool_calls.as_ref().expect("expected tool calls");
                assert_eq!(tool_calls.len(), 1);
                assert!(matches!(
                    tool_calls[0],
                    ChatCompletionsToolCall::Function { .. }
                ));
            }
            other => panic!("expected assistant tool call message, got {other:?}"),
        }

        match &messages[2] {
            ChatCompletionsMessage::User {
                content: ChatCompletionsContent::Text(t),
                ..
            } => assert_eq!(t, "second user"),
            other => panic!("expected second user message, got {other:?}"),
        }
    }

    #[test]
    fn or_input_item_accum_preserves_append_order() {
        let mut accum = OrInputItemAccum::new();
        accum.push_message(MessageRole::User, InputContent::Text("one".into()));
        accum.push_function_call("call_1".into(), "lookup".into(), "{}".into());
        accum
            .push_function_call_output("call_1".into(), FunctionCallOutputValue::Text("ok".into()));
        accum.push_reasoning(Some("thinking".into()), None);
        let items = accum.finish();

        assert_eq!(items.len(), 4);
        assert!(matches!(items[0], InputItem::Message { .. }));
        assert!(matches!(items[1], InputItem::FunctionCall { .. }));
        assert!(matches!(items[2], InputItem::FunctionCallOutput { .. }));
        assert!(matches!(items[3], InputItem::Reasoning { .. }));
    }
}
