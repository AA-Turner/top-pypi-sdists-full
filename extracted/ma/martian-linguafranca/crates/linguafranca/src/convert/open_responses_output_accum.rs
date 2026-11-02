use crate::convert::open_responses_id::{OpenResponsesOutputItemKind, output_item_id};
use crate::open_responses::types::*;

/// Accumulates Open Responses output items while buffering content parts.
///
/// Anthropic Messages responses are a flat `Vec<OutputContentBlock>`. Open Responses splits them:
/// text parts become an `OutputItem::Message`, tool calls become separate
/// `FunctionCall` items, reasoning becomes `Reasoning` items.
/// This accumulator buffers content parts and flushes them into a Message
/// whenever a non-content item appears.
pub(crate) struct OpenResponsesOutputAccum {
    response_id: String,
    items: Vec<OutputItem>,
    pending_parts: Vec<ContentPart>,
}

impl OpenResponsesOutputAccum {
    pub(crate) fn new(response_id: impl Into<String>) -> Self {
        Self {
            response_id: response_id.into(),
            items: Vec::new(),
            pending_parts: Vec::new(),
        }
    }

    pub(crate) fn push_content_part(&mut self, part: ContentPart) {
        self.pending_parts.push(part);
    }

    /// Drain pending content parts into an `OutputItem::Message`.
    pub(crate) fn flush_message(&mut self) {
        if self.pending_parts.is_empty() {
            return;
        }
        let output_index = u64::try_from(self.items.len()).expect("output item count fits in u64");
        let id = output_item_id(
            &self.response_id,
            OpenResponsesOutputItemKind::Message,
            output_index,
            None,
        );
        self.items.push(OutputItem::Message {
            id,
            status: ItemStatus::Completed,
            role: MessageRole::Assistant,
            content: std::mem::take(&mut self.pending_parts),
        });
    }

    pub(crate) fn generated_item_id_after_flush(
        &mut self,
        kind: OpenResponsesOutputItemKind,
        source_hint: Option<&str>,
    ) -> String {
        self.flush_message();
        let output_index = u64::try_from(self.items.len()).expect("output item count fits in u64");
        output_item_id(&self.response_id, kind, output_index, source_hint)
    }

    pub(crate) fn push_flushed_item(&mut self, item: OutputItem) {
        assert!(
            self.pending_parts.is_empty(),
            "push_flushed_item called with pending message parts; call generated_item_id_after_flush first"
        );
        self.items.push(item);
    }

    /// Flush pending parts then push a standalone item.
    pub(crate) fn push_item(&mut self, item: OutputItem) {
        self.flush_message();
        self.items.push(item);
    }

    pub(crate) fn into_items(self) -> Vec<OutputItem> {
        debug_assert!(
            self.pending_parts.is_empty(),
            "OpenResponsesOutputAccum has unflushed parts - call flush_message() before into_items()"
        );
        self.items
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn single_text_flushes_as_message() {
        let mut accum = OpenResponsesOutputAccum::new("resp_1");
        accum.push_content_part(ContentPart::OutputText {
            text: "hello".into(),
            annotations: vec![],
            logprobs: vec![],
        });
        accum.flush_message();

        let items = accum.into_items();
        assert_eq!(items.len(), 1);
        match &items[0] {
            OutputItem::Message { content, role, .. } => {
                assert_eq!(*role, MessageRole::Assistant);
                assert_eq!(content.len(), 1);
            }
            other => panic!("expected Message, got {other:?}"),
        }
    }

    #[test]
    fn push_item_flushes_pending() {
        let mut accum = OpenResponsesOutputAccum::new("resp_1");
        accum.push_content_part(ContentPart::OutputText {
            text: "before".into(),
            annotations: vec![],
            logprobs: vec![],
        });
        accum.push_item(OutputItem::FunctionCall {
            id: "fc_0".into(),
            call_id: "call_1".into(),
            name: "func".into(),
            namespace: None,
            arguments: "{}".into(),
            status: ItemStatus::Completed,
        });

        let items = accum.into_items();
        assert_eq!(items.len(), 2);
        assert!(matches!(&items[0], OutputItem::Message { .. }));
        assert!(matches!(&items[1], OutputItem::FunctionCall { .. }));
    }

    #[test]
    fn empty_flush_is_noop() {
        let mut accum = OpenResponsesOutputAccum::new("resp_1");
        accum.flush_message();
        assert!(accum.into_items().is_empty());
    }

    #[test]
    fn message_ids_are_opaque_and_unique() {
        let mut accum = OpenResponsesOutputAccum::new("resp_1");
        accum.push_content_part(ContentPart::OutputText {
            text: "a".into(),
            annotations: vec![],
            logprobs: vec![],
        });
        accum.flush_message();
        accum.push_content_part(ContentPart::OutputText {
            text: "b".into(),
            annotations: vec![],
            logprobs: vec![],
        });
        accum.flush_message();

        let items = accum.into_items();
        match (&items[0], &items[1]) {
            (OutputItem::Message { id: id0, .. }, OutputItem::Message { id: id1, .. }) => {
                assert!(id0.starts_with("msg_"));
                assert!(id1.starts_with("msg_"));
                assert_ne!(id0, "msg_0");
                assert_ne!(id1, "msg_1");
                assert_ne!(id0, id1);
            }
            _ => panic!("expected two Messages"),
        }
    }
}
