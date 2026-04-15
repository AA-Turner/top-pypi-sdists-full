use lsp_types::{Diagnostic, DiagnosticSeverity, Position, Range};

use crate::analysis;

/// Produce LSP diagnostics for a SQL text.
pub fn diagnostics(sql: &str) -> Vec<Diagnostic> {
    analysis::parse_errors(sql)
        .into_iter()
        .map(|e| {
            // sqlparser locations are 1-based; LSP positions are 0-based
            let line = e.line.saturating_sub(1);
            let col = e.column.saturating_sub(1);
            Diagnostic {
                range: Range::new(Position::new(line, col), Position::new(line, col + 1)),
                severity: Some(DiagnosticSeverity::ERROR),
                source: Some("chalk-sql".to_string()),
                message: e.message,
                ..Default::default()
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_sql_no_diagnostics() {
        let diags = diagnostics("SELECT 1");
        assert!(diags.is_empty());
    }

    #[test]
    fn test_invalid_sql_has_diagnostics() {
        let diags = diagnostics("SELEC 1");
        assert!(!diags.is_empty());
        assert_eq!(diags[0].severity, Some(DiagnosticSeverity::ERROR));
        assert_eq!(diags[0].source.as_deref(), Some("chalk-sql"));
    }
}
