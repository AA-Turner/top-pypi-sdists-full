use sha2::{Digest, Sha256};

const OUTPUT_ITEM_ID_HEX_LEN: usize = 50;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum OpenResponsesOutputItemKind {
    Message,
    Reasoning,
    FunctionCall,
    CustomToolCall,
}

impl OpenResponsesOutputItemKind {
    pub(crate) fn prefix(self) -> &'static str {
        match self {
            Self::Message => "msg",
            Self::Reasoning => "rs",
            Self::FunctionCall => "fc",
            Self::CustomToolCall => "ctc",
        }
    }

    fn item_type(self) -> &'static str {
        match self {
            Self::Message => "message",
            Self::Reasoning => "reasoning",
            Self::FunctionCall => "function_call",
            Self::CustomToolCall => "custom_tool_call",
        }
    }
}

pub(crate) fn output_item_id(
    response_id: &str,
    kind: OpenResponsesOutputItemKind,
    output_index: u64,
    source_hint: Option<&str>,
) -> String {
    let mut hasher = Sha256::new();
    hasher.update(response_id.as_bytes());
    hasher.update(b"\0");
    hasher.update(kind.prefix().as_bytes());
    hasher.update(b"\0");
    hasher.update(output_index.to_le_bytes());
    hasher.update(b"\0");
    hasher.update(kind.item_type().as_bytes());
    hasher.update(b"\0");
    match source_hint {
        Some(source_hint) => {
            hasher.update([1]);
            hasher.update(source_hint.as_bytes());
        }
        None => hasher.update([0]),
    }

    let digest = hasher.finalize();
    let hex: String = digest.iter().map(|b| format!("{b:02x}")).collect();
    format!("{}_{}", kind.prefix(), &hex[..OUTPUT_ITEM_ID_HEX_LEN])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn output_item_ids_are_stable_and_opaque() {
        let a = output_item_id("resp_1", OpenResponsesOutputItemKind::Message, 0, None);
        let b = output_item_id("resp_1", OpenResponsesOutputItemKind::Message, 0, None);
        let c = output_item_id("resp_1", OpenResponsesOutputItemKind::Message, 1, None);

        assert_eq!(a, b);
        assert_ne!(a, c);
        assert!(a.starts_with("msg_"));
        assert_ne!(a, "msg_0");
        assert_eq!(a.trim_start_matches("msg_").len(), OUTPUT_ITEM_ID_HEX_LEN);
        let without_hint =
            output_item_id("resp_1", OpenResponsesOutputItemKind::FunctionCall, 0, None);
        let empty_hint = output_item_id(
            "resp_1",
            OpenResponsesOutputItemKind::FunctionCall,
            0,
            Some(""),
        );
        assert_ne!(without_hint, empty_hint);
    }
}
