use lsp_types::{
    CompletionItem, CompletionItemKind, Documentation, InsertTextFormat, MarkupContent, MarkupKind,
};

use crate::analysis::{cursor_context, CursorContext};
use crate::catalog::Catalog;

/// Produce completion items for the given SQL text and cursor position (0-based).
pub fn completions(sql: &str, line: u32, col: u32) -> Vec<CompletionItem> {
    let ctx = cursor_context(sql, line, col);
    let catalog = Catalog::get();

    match ctx {
        CursorContext::FunctionName { prefix } => {
            let matches = if prefix.is_empty() {
                // Return all functions when no prefix (e.g., triggered explicitly)
                catalog.functions.iter().collect::<Vec<_>>()
            } else {
                catalog.functions_with_prefix(&prefix)
            };
            matches
                .into_iter()
                .map(|f| {
                    let detail = f.signature_short();
                    let docs = f.docs.as_deref().unwrap_or("");
                    let doc_text = format!("**{}**\n\n{}\n\n{}", f.category, docs, signatures_markdown(f));

                    CompletionItem {
                        label: f.name.clone(),
                        kind: Some(CompletionItemKind::FUNCTION),
                        detail: Some(detail),
                        documentation: Some(Documentation::MarkupContent(MarkupContent {
                            kind: MarkupKind::Markdown,
                            value: doc_text,
                        })),
                        insert_text: Some(format!("{}($0)", f.name)),
                        insert_text_format: Some(InsertTextFormat::SNIPPET),
                        ..Default::default()
                    }
                })
                .collect()
        }
        CursorContext::FunctionArg { .. } => {
            // Inside a function call — no function completions, but we could
            // offer keyword completions in the future
            vec![]
        }
    }
}

fn signatures_markdown(f: &crate::catalog::FunctionDef) -> String {
    f.overloads
        .iter()
        .map(|o| format!("```\n{}\n```", o.render_signature(&f.name)))
        .collect::<Vec<_>>()
        .join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_completions_with_prefix() {
        let items = completions("SELECT ab", 0, 9);
        assert!(!items.is_empty());
        assert!(items.iter().any(|i| i.label == "abs"));
    }

    #[test]
    fn test_completions_inside_function_call() {
        let items = completions("SELECT abs(", 0, 11);
        assert!(items.is_empty());
    }

    #[test]
    fn test_completion_has_snippet() {
        let items = completions("SELECT ab", 0, 9);
        let abs_item = items.iter().find(|i| i.label == "abs").unwrap();
        assert_eq!(abs_item.insert_text.as_deref(), Some("abs($0)"));
        assert_eq!(abs_item.insert_text_format, Some(InsertTextFormat::SNIPPET));
    }
}
