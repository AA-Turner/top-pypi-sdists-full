use sqlparser::dialect::DuckDbDialect;
use sqlparser::keywords::Keyword;
use sqlparser::parser::Parser;
use sqlparser::tokenizer::{Token, Tokenizer, Word};

/// A parse error with location info.
#[derive(Debug)]
pub struct ParseError {
    pub message: String,
    pub line: u32,
    pub column: u32,
}

/// Context at cursor position, used for completions and signature help.
#[derive(Debug, PartialEq)]
pub enum CursorContext {
    /// Cursor is typing a function/identifier name (or in expression position).
    FunctionName { prefix: String },
    /// Cursor is inside a function call's argument list.
    FunctionArg {
        function_name: String,
        arg_index: usize,
    },
}

/// Parse SQL and return any errors with locations.
pub fn parse_errors(sql: &str) -> Vec<ParseError> {
    let dialect = DuckDbDialect {};
    match Parser::parse_sql(&dialect, sql) {
        Ok(_) => vec![],
        Err(e) => {
            let msg = e.to_string();
            let (line, column) = extract_location_from_error(&msg);
            vec![ParseError {
                message: msg,
                line,
                column,
            }]
        }
    }
}

/// Flag syntax that the DuckDB dialect accepts but Chalk SQL does not.
///
/// `sqlparser` only gates the angle-bracket array type on Snowflake and
/// ClickHouse; every other dialect — DuckDB included — falls through to
/// `ARRAY '<' <type> '>'`, so `CAST(x AS ARRAY<VARCHAR(123)>)` parses cleanly
/// even though it is BigQuery syntax. There is no `Dialect` hook to turn that
/// off, so it is rejected here instead.
///
/// This runs on the token stream rather than the AST, so it still reports when
/// the statement fails to parse for some unrelated reason. The tradeoff is that
/// an unquoted column named `array` compared with `<` would be flagged — quote
/// it to avoid that (a quoted word never carries a `Keyword`).
pub fn unsupported_syntax_errors(sql: &str) -> Vec<ParseError> {
    let tokens: Vec<(Token, usize, usize)> = tokenize(sql)
        .into_iter()
        .filter(|(token, _, _)| !matches!(token, Token::Whitespace(_)))
        .collect();

    tokens
        .windows(2)
        .filter(|pair| {
            matches!(
                pair[0].0,
                Token::Word(Word {
                    keyword: Keyword::ARRAY,
                    ..
                })
            ) && matches!(pair[1].0, Token::Lt)
        })
        .map(|pair| {
            let (_, line, column) = pair[1];
            ParseError {
                message:
                    "`ARRAY<...>` is BigQuery syntax: use `<type>[]` instead, e.g. `VARCHAR(123)[]`"
                        .to_string(),
                line: line as u32,
                column: column as u32,
            }
        })
        .collect()
}

/// Extract line/column from sqlparser error messages.
/// Format: "... at Line: N, Column: M"
fn extract_location_from_error(msg: &str) -> (u32, u32) {
    if let Some(at_pos) = msg.rfind(" at Line: ") {
        let location_part = &msg[at_pos..];
        let parts: Vec<&str> = location_part.split(", ").collect();
        let line = parts
            .first()
            .and_then(|p| p.strip_prefix(" at Line: "))
            .and_then(|s| s.parse::<u32>().ok())
            .unwrap_or(1);
        let column = parts
            .get(1)
            .and_then(|p| p.strip_prefix("Column: "))
            .and_then(|s| s.parse::<u32>().ok())
            .unwrap_or(1);
        (line, column)
    } else {
        (1, 1)
    }
}

/// Determine cursor context by scanning backwards from cursor position.
pub fn cursor_context(text: &str, line: u32, col: u32) -> CursorContext {
    let offset = line_col_to_offset(text, line, col);
    let before = &text[..offset];

    // Extract the partial word at the cursor
    let word_start = before
        .rfind(|c: char| !c.is_alphanumeric() && c != '_')
        .map(|i| i + 1)
        .unwrap_or(0);
    let partial_word = &before[word_start..];

    // Scan backwards to find if we're inside a function call
    let mut paren_depth: i32 = 0;
    let mut comma_count: usize = 0;

    for ch in before.chars().rev() {
        match ch {
            ')' => paren_depth += 1,
            '(' => {
                paren_depth -= 1;
                if paren_depth < 0 {
                    // Found an unmatched open paren — extract the function name before it
                    let paren_pos = before.len()
                        - before
                            .chars()
                            .rev()
                            .position(|c| c == '(')
                            .unwrap_or(before.len())
                        - 1;
                    let before_paren = &before[..paren_pos];
                    let fn_name = extract_identifier_before(before_paren);
                    if !fn_name.is_empty() {
                        return CursorContext::FunctionArg {
                            function_name: fn_name,
                            arg_index: comma_count,
                        };
                    }
                    break;
                }
            }
            ',' if paren_depth == 0 => comma_count += 1,
            _ => {}
        }
    }

    CursorContext::FunctionName {
        prefix: partial_word.to_string(),
    }
}

/// Extract the identifier immediately before a position (trimming whitespace).
fn extract_identifier_before(text: &str) -> String {
    let trimmed = text.trim_end();
    let start = trimmed
        .rfind(|c: char| !c.is_alphanumeric() && c != '_')
        .map(|i| i + 1)
        .unwrap_or(0);
    trimmed[start..].to_string()
}

/// Convert 0-based line/col to byte offset.
fn line_col_to_offset(text: &str, line: u32, col: u32) -> usize {
    let mut current_line = 0u32;
    let mut offset = 0usize;

    for (i, ch) in text.char_indices() {
        if current_line == line {
            let col_offset = i + col as usize;
            return col_offset.min(text.len());
        }
        if ch == '\n' {
            current_line += 1;
            offset = i + 1;
        }
    }

    // If we're on the target line but ran out of chars
    if current_line == line {
        (offset + col as usize).min(text.len())
    } else {
        text.len()
    }
}

/// Extract the word (identifier) at a given position in the text.
pub fn word_at_position(text: &str, line: u32, col: u32) -> Option<String> {
    let offset = line_col_to_offset(text, line, col);

    // Find word boundaries around the offset
    let start = text[..offset]
        .rfind(|c: char| !c.is_alphanumeric() && c != '_')
        .map(|i| i + 1)
        .unwrap_or(0);

    let end = text[offset..]
        .find(|c: char| !c.is_alphanumeric() && c != '_')
        .map(|i| offset + i)
        .unwrap_or(text.len());

    let word = &text[start..end];
    if word.is_empty() {
        None
    } else {
        Some(word.to_string())
    }
}

/// Tokenize SQL text (always succeeds, unlike full parsing).
pub fn tokenize(sql: &str) -> Vec<(Token, usize, usize)> {
    let dialect = DuckDbDialect {};
    let mut tokenizer = Tokenizer::new(&dialect, sql);
    match tokenizer.tokenize_with_location() {
        Ok(tokens) => tokens
            .into_iter()
            .map(|t| {
                (
                    t.token,
                    t.span.start.line as usize,
                    t.span.start.column as usize,
                )
            })
            .collect(),
        Err(_) => vec![],
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_valid_sql() {
        let errors = parse_errors("SELECT 1");
        assert!(errors.is_empty());
    }

    #[test]
    fn test_parse_invalid_sql() {
        let errors = parse_errors("SELEC 1");
        assert!(!errors.is_empty());
    }

    #[test]
    fn test_angle_bracket_array_type_rejected() {
        let errors = unsupported_syntax_errors("select CAST(foo as array<varchar(123)>);");
        assert_eq!(errors.len(), 1);
        assert_eq!((errors[0].line, errors[0].column), (1, 25));
    }

    #[test]
    fn test_angle_bracket_array_type_rejected_with_whitespace() {
        let errors = unsupported_syntax_errors("select CAST(foo as ARRAY\n  <int64>);");
        assert_eq!(errors.len(), 1);
        assert_eq!((errors[0].line, errors[0].column), (2, 3));
    }

    #[test]
    fn test_bracket_array_type_allowed() {
        assert!(unsupported_syntax_errors("select CAST(foo as varchar(123)[]);").is_empty());
    }

    #[test]
    fn test_quoted_array_identifier_allowed() {
        assert!(unsupported_syntax_errors(r#"select x from t where "array" < 5"#).is_empty());
    }

    #[test]
    fn test_cursor_context_function_name() {
        let ctx = cursor_context("SELECT ab", 0, 9);
        assert_eq!(
            ctx,
            CursorContext::FunctionName {
                prefix: "ab".to_string()
            }
        );
    }

    #[test]
    fn test_cursor_context_function_arg() {
        let ctx = cursor_context("SELECT abs(", 0, 11);
        assert_eq!(
            ctx,
            CursorContext::FunctionArg {
                function_name: "abs".to_string(),
                arg_index: 0,
            }
        );
    }

    #[test]
    fn test_cursor_context_second_arg() {
        let ctx = cursor_context("SELECT concat(a, ", 0, 17);
        assert_eq!(
            ctx,
            CursorContext::FunctionArg {
                function_name: "concat".to_string(),
                arg_index: 1,
            }
        );
    }

    #[test]
    fn test_word_at_position() {
        let word = word_at_position("SELECT abs FROM t", 0, 8);
        assert_eq!(word, Some("abs".to_string()));
    }

    #[test]
    fn test_line_col_to_offset_multiline() {
        let text = "line0\nline1\nline2";
        assert_eq!(line_col_to_offset(text, 0, 0), 0);
        assert_eq!(line_col_to_offset(text, 1, 0), 6);
        assert_eq!(line_col_to_offset(text, 2, 3), 15);
    }
}
