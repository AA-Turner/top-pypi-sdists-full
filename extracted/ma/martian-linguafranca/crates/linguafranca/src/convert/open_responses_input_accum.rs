use crate::open_responses::types::*;

/// Accumulates Open Responses input items while buffering text/image parts.
///
/// Anthropic Messages puts text, images, tool results etc. in one flat message.
/// Open Responses splits them: text/image parts become Messages, tool results
/// become FunctionCallOutput items.
/// This accumulator buffers content parts and flushes them into a Message
/// whenever a non-content item (tool use, tool result, thinking) appears.
pub(crate) struct OpenResponsesInputAccum {
    items: Vec<InputItem>,
    pending_parts: Vec<InputContentPart>,
}

impl OpenResponsesInputAccum {
    pub(crate) fn new() -> Self {
        Self {
            items: Vec::new(),
            pending_parts: Vec::new(),
        }
    }

    pub(crate) fn push_part(&mut self, part: InputContentPart) {
        self.pending_parts.push(part);
    }

    /// Drain pending text/image parts into an InputItem::Message.
    pub(crate) fn flush_parts(&mut self, role: MessageRole) {
        if self.pending_parts.is_empty() {
            return;
        }
        let content = if self.pending_parts.len() == 1 {
            match self.pending_parts.pop().unwrap() {
                InputContentPart::Text { text } | InputContentPart::OutputText { text, .. } => {
                    InputContent::Text(text)
                }
                other => InputContent::Parts(vec![other]),
            }
        } else {
            InputContent::Parts(std::mem::take(&mut self.pending_parts))
        };
        self.items.push(InputItem::Message {
            role,
            content,
            id: None,
            status: None,
        });
    }

    /// Flush pending parts then push a standalone item.
    pub(crate) fn push_item(&mut self, role: MessageRole, item: InputItem) {
        self.flush_parts(role);
        self.items.push(item);
    }

    pub(crate) fn into_items(self) -> Vec<InputItem> {
        debug_assert!(
            self.pending_parts.is_empty(),
            "OpenResponsesInputAccum has unflushed parts - call flush_parts() before into_items()"
        );
        self.items
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn single_text_flushes_as_text() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_part(InputContentPart::Text {
            text: "hello".into(),
        });
        accum.flush_parts(MessageRole::User);

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        match &items[0] {
            InputItem::Message {
                content: InputContent::Text(t),
                ..
            } => assert_eq!(t, "hello"),
            other => panic!("expected Text message, got {other:?}"),
        }
    }

    #[test]
    fn single_output_text_flushes_as_text() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_part(InputContentPart::OutputText {
            text: "assistant said this".into(),
            annotations: vec![],
            logprobs: vec![],
        });
        accum.flush_parts(MessageRole::Assistant);

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        match &items[0] {
            InputItem::Message {
                content: InputContent::Text(t),
                ..
            } => assert_eq!(t, "assistant said this"),
            other => panic!("expected Text message, got {other:?}"),
        }
    }

    #[test]
    fn single_image_flushes_as_parts() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_part(InputContentPart::Image {
            image_url: Some("https://example.com/img.png".into()),
            detail: None,
        });
        accum.flush_parts(MessageRole::User);

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        assert!(matches!(
            &items[0],
            InputItem::Message {
                content: InputContent::Parts(_),
                ..
            }
        ));
    }

    #[test]
    fn multiple_parts_flushes_as_parts() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_part(InputContentPart::Text {
            text: "hello".into(),
        });
        accum.push_part(InputContentPart::Text {
            text: "world".into(),
        });
        accum.flush_parts(MessageRole::User);

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        match &items[0] {
            InputItem::Message {
                content: InputContent::Parts(parts),
                ..
            } => assert_eq!(parts.len(), 2),
            other => panic!("expected Parts message, got {other:?}"),
        }
    }

    #[test]
    fn push_item_flushes_pending_parts() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_part(InputContentPart::Text {
            text: "before".into(),
        });
        accum.push_item(
            MessageRole::User,
            InputItem::FunctionCallOutput {
                call_id: "call_1".into(),
                output: FunctionCallOutputValue::Text("result".into()),
                id: None,
                status: None,
            },
        );

        let items = accum.into_items();
        assert_eq!(items.len(), 2);
        assert!(matches!(&items[0], InputItem::Message { .. }));
        assert!(matches!(&items[1], InputItem::FunctionCallOutput { .. }));
    }

    #[test]
    fn empty_flush_is_noop() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.flush_parts(MessageRole::User);

        assert!(accum.into_items().is_empty());
    }

    #[test]
    fn push_item_without_pending_parts() {
        let mut accum = OpenResponsesInputAccum::new();
        accum.push_item(
            MessageRole::User,
            InputItem::FunctionCall {
                call_id: "call_1".into(),
                name: "func".into(),
                namespace: None,
                arguments: "{}".into(),
                id: None,
                status: None,
            },
        );

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        assert!(matches!(&items[0], InputItem::FunctionCall { .. }));
    }
}
