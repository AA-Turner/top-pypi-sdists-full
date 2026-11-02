use crate::anthropic::types::*;

/// Accumulates Anthropic messages while enforcing the alternating-turns
/// constraint: consecutive same-role blocks are merged into one message.
pub(super) struct AnthropicMessageAccum {
    messages: Vec<AnthropicMessage>,
}

impl AnthropicMessageAccum {
    pub(super) fn new() -> Self {
        Self {
            messages: Vec::new(),
        }
    }

    /// Merge blocks into the last message if it has the same role,
    /// otherwise push a new message. Always uses the array content form.
    pub(super) fn push_blocks(
        &mut self,
        role: AnthropicRole,
        blocks: Vec<AnthropicInputContentBlock>,
    ) {
        if let Some(last) = self.messages.last_mut()
            && last.role == role
        {
            append_blocks_to_content(&mut last.content, blocks);
            return;
        }

        self.messages.push(AnthropicMessage {
            role,
            content: AnthropicMessageContent::Blocks(blocks),
        });
    }

    /// Push a plain text message using the shorthand form when possible.
    /// Falls back to blocks form if merging with the previous same-role message.
    pub(super) fn push_text(&mut self, role: AnthropicRole, text: String) {
        if self.messages.last().is_some_and(|m| m.role == role) {
            self.push_blocks(
                role,
                vec![AnthropicInputContentBlock::Text {
                    text,
                    cache_control: None,
                    citations: None,
                }],
            );
        } else {
            self.messages.push(AnthropicMessage {
                role,
                content: AnthropicMessageContent::Text(text),
            });
        }
    }

    pub(super) fn into_messages(self) -> Vec<AnthropicMessage> {
        self.messages
    }
}

/// Append `blocks` onto an existing message's content, upgrading the shorthand
/// text form to the array form when needed. Shared by `push_blocks` and by the
/// post-hoc placement repair so the alternation-merge logic lives in one place.
pub(super) fn append_blocks_to_content(
    content: &mut AnthropicMessageContent,
    blocks: Vec<AnthropicInputContentBlock>,
) {
    match content {
        AnthropicMessageContent::Blocks(existing) => {
            existing.extend(blocks);
        }
        AnthropicMessageContent::Text(t) => {
            let mut new_blocks = vec![AnthropicInputContentBlock::Text {
                text: std::mem::take(t),
                cache_control: None,
                citations: None,
            }];
            new_blocks.extend(blocks);
            *content = AnthropicMessageContent::Blocks(new_blocks);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn text_block(s: &str) -> AnthropicInputContentBlock {
        AnthropicInputContentBlock::Text {
            text: s.into(),
            cache_control: None,
            citations: None,
        }
    }

    fn tool_use_block(id: &str, name: &str) -> AnthropicInputContentBlock {
        AnthropicInputContentBlock::ToolUse {
            id: id.into(),
            name: name.into(),
            input: serde_json::json!({}),
            cache_control: None,
        }
    }

    #[test]
    fn push_text_shorthand() {
        let mut accum = AnthropicMessageAccum::new();
        accum.push_text(AnthropicRole::User, "hello".into());

        let msgs = accum.into_messages();
        assert_eq!(msgs.len(), 1);
        assert!(matches!(&msgs[0].content, AnthropicMessageContent::Text(t) if t == "hello"));
    }

    #[test]
    fn push_text_merges_same_role() {
        let mut accum = AnthropicMessageAccum::new();
        accum.push_text(AnthropicRole::User, "hello".into());
        accum.push_text(AnthropicRole::User, "world".into());

        let msgs = accum.into_messages();
        assert_eq!(msgs.len(), 1);
        match &msgs[0].content {
            AnthropicMessageContent::Blocks(blocks) => {
                assert_eq!(blocks.len(), 2);
            }
            other => panic!("expected Blocks, got {other:?}"),
        }
    }

    #[test]
    fn push_blocks_merges_same_role() {
        let mut accum = AnthropicMessageAccum::new();
        accum.push_blocks(AnthropicRole::Assistant, vec![text_block("a")]);
        accum.push_blocks(AnthropicRole::Assistant, vec![tool_use_block("1", "f")]);

        let msgs = accum.into_messages();
        assert_eq!(msgs.len(), 1);
        match &msgs[0].content {
            AnthropicMessageContent::Blocks(blocks) => assert_eq!(blocks.len(), 2),
            other => panic!("expected Blocks, got {other:?}"),
        }
    }

    #[test]
    fn different_roles_separate_messages() {
        let mut accum = AnthropicMessageAccum::new();
        accum.push_text(AnthropicRole::User, "hi".into());
        accum.push_blocks(AnthropicRole::Assistant, vec![text_block("hey")]);
        accum.push_text(AnthropicRole::User, "bye".into());

        let msgs = accum.into_messages();
        assert_eq!(msgs.len(), 3);
        assert_eq!(msgs[0].role, AnthropicRole::User);
        assert_eq!(msgs[1].role, AnthropicRole::Assistant);
        assert_eq!(msgs[2].role, AnthropicRole::User);
    }

    #[test]
    fn push_blocks_upgrades_text_to_blocks() {
        let mut accum = AnthropicMessageAccum::new();
        accum.push_text(AnthropicRole::User, "hello".into());
        accum.push_blocks(AnthropicRole::User, vec![tool_use_block("1", "f")]);

        let msgs = accum.into_messages();
        assert_eq!(msgs.len(), 1);
        match &msgs[0].content {
            AnthropicMessageContent::Blocks(blocks) => {
                assert_eq!(blocks.len(), 2);
                assert!(
                    matches!(&blocks[0], AnthropicInputContentBlock::Text { text, .. } if text == "hello")
                );
                assert!(matches!(
                    &blocks[1],
                    AnthropicInputContentBlock::ToolUse { .. }
                ));
            }
            other => panic!("expected Blocks, got {other:?}"),
        }
    }
}
