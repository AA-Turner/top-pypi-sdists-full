use lsp_types::{Hover, HoverContents, MarkupContent, MarkupKind};

use crate::analysis::word_at_position;
use crate::catalog::Catalog;

/// Produce hover information for the word at the given position.
pub fn hover(sql: &str, line: u32, col: u32) -> Option<Hover> {
    let word = word_at_position(sql, line, col)?;
    let catalog = Catalog::get();
    let func = catalog.find_function(&word)?;

    let mut md = String::new();

    // Category
    md.push_str(&format!("**{}**\n\n", func.category));

    // Documentation
    if let Some(docs) = &func.docs {
        md.push_str(docs);
        md.push_str("\n\n");
    }

    // All overloads
    md.push_str("### Signatures\n\n");
    for overload in &func.overloads {
        md.push_str(&format!(
            "```sql\n{}\n```\n\n",
            overload.render_signature(&func.name)
        ));
    }

    Some(Hover {
        contents: HoverContents::Markup(MarkupContent {
            kind: MarkupKind::Markdown,
            value: md,
        }),
        range: None,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hover_on_known_function() {
        let h = hover("SELECT abs(x) FROM t", 0, 8);
        assert!(h.is_some());
        let contents = match h.unwrap().contents {
            HoverContents::Markup(m) => m.value,
            _ => panic!("expected markup"),
        };
        assert!(contents.contains("abs"));
        assert!(contents.contains("Numeric Functions"));
    }

    #[test]
    fn test_hover_on_unknown_word() {
        let h = hover("SELECT foobar FROM t", 0, 8);
        assert!(h.is_none());
    }
}
