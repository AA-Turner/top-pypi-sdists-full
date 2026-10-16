//! Parsing helpers for Chalk `.chalk.sql` resolver files.
//!
//! These resolvers begin with a block of `-- key: value` comment directives
//! followed by a single SQL `SELECT`. Two pieces of structure power "go to
//! definition":
//!
//! * `-- resolves: <namespace-or-class>` — the feature class the resolver
//!   populates.
//! * the `SELECT` output columns — each names a feature on that class.
//!
//! The functions here are intentionally pure (text in, ranges out); turning a
//! range into a Python location is the caller's job.

use lsp_types::{Position, Range};

/// The target named by a `-- resolves:` directive, plus the range of the
/// identifier itself (so the caller can decide whether the cursor is on it).
#[derive(Debug, Clone, PartialEq)]
pub struct ResolvesRef {
    pub identifier: String,
    pub range: Range,
}

/// A single `SELECT` output column that maps to a feature, plus the range of the
/// identifier that names the feature (the alias when aliased, otherwise the
/// column name).
#[derive(Debug, Clone, PartialEq)]
pub struct OutputColumn {
    pub name: String,
    pub range: Range,
}

/// Find the `-- resolves:` directive and the range of its target identifier.
pub fn resolves_ref(text: &str) -> Option<ResolvesRef> {
    for (line_idx, line) in text.lines().enumerate() {
        if let Some(reference) = parse_resolves_line(line, line_idx as u32) {
            return Some(reference);
        }
    }
    None
}

/// Return the `-- resolves:` target if the cursor sits on it.
pub fn resolves_ref_at(text: &str, line: u32, col: u32) -> Option<ResolvesRef> {
    let reference = resolves_ref(text)?;
    range_contains(&reference.range, line, col).then_some(reference)
}

/// Return the `SELECT` output column if the cursor sits on the identifier that
/// names it.
pub fn output_column_at(text: &str, line: u32, col: u32) -> Option<OutputColumn> {
    output_columns(text)
        .into_iter()
        .find(|column| range_contains(&column.range, line, col))
}

fn parse_resolves_line(line: &str, line_idx: u32) -> Option<ResolvesRef> {
    let comment_start = line.find("--")?;
    let after_dashes = &line[comment_start + 2..];
    let colon = after_dashes.find(':')?;
    if after_dashes[..colon].trim() != "resolves" {
        return None;
    }

    let value_part = &after_dashes[colon + 1..];
    let leading_ws = value_part.find(|c: char| !c.is_whitespace())?;
    let value_rest = &value_part[leading_ws..];
    let value_len = value_rest
        .find(char::is_whitespace)
        .unwrap_or(value_rest.len());
    let identifier = value_rest[..value_len].to_string();
    if identifier.is_empty() {
        return None;
    }

    let col_start = comment_start + 2 + colon + 1 + leading_ws;
    let col_end = col_start + value_len;
    Some(ResolvesRef {
        identifier,
        range: Range::new(
            Position::new(line_idx, col_start as u32),
            Position::new(line_idx, col_end as u32),
        ),
    })
}

/// Parse the output columns of the resolver's `SELECT`.
pub fn output_columns(text: &str) -> Vec<OutputColumn> {
    let tokens = tokenize(text);
    let Some(select_idx) = find_top_level_keyword(&tokens, 0, "select") else {
        return Vec::new();
    };

    // Collect tokens of the SELECT list, stopping at the matching top-level
    // FROM (or statement terminator).
    let mut depth = 0i32;
    let mut list: Vec<&Token> = Vec::new();
    for token in &tokens[select_idx + 1..] {
        match &token.kind {
            TokenKind::Punct('(') => {
                depth += 1;
                list.push(token);
            }
            TokenKind::Punct(')') => {
                depth -= 1;
                list.push(token);
            }
            TokenKind::Ident if depth == 0 && token.text.eq_ignore_ascii_case("from") => break,
            TokenKind::Punct(';') if depth == 0 => break,
            _ => list.push(token),
        }
    }

    // Split the list into comma-separated items at the top level.
    let mut columns = Vec::new();
    let mut depth = 0i32;
    let mut item: Vec<&Token> = Vec::new();
    for token in list {
        match &token.kind {
            TokenKind::Punct('(') => {
                depth += 1;
                item.push(token);
            }
            TokenKind::Punct(')') => {
                depth -= 1;
                item.push(token);
            }
            TokenKind::Punct(',') if depth == 0 => {
                if let Some(column) = feature_from_item(&item) {
                    columns.push(column);
                }
                item.clear();
            }
            _ => item.push(token),
        }
    }
    if let Some(column) = feature_from_item(&item) {
        columns.push(column);
    }

    columns
}

/// Determine the feature named by a single SELECT-list item.
fn feature_from_item(item: &[&Token]) -> Option<OutputColumn> {
    // An explicit `AS alias` wins.
    if let Some(as_pos) = find_top_level_keyword_in(item, "as") {
        let token = item.get(as_pos + 1)?;
        if matches!(token.kind, TokenKind::Ident) && is_name_like(&token.text) {
            return Some(output_column(token));
        }
        return None;
    }

    // Otherwise the last top-level identifier that is neither a keyword nor a
    // function call name (i.e. not immediately followed by `(`). This handles
    // bare columns (`name`), qualified columns (`t.name`), and bare aliases
    // (`expr alias`), while skipping `count(*)` and the like.
    let mut depth = 0i32;
    let mut best: Option<&Token> = None;
    for (idx, token) in item.iter().enumerate() {
        match &token.kind {
            TokenKind::Punct('(') => depth += 1,
            TokenKind::Punct(')') => depth -= 1,
            TokenKind::Ident
                if depth == 0 && is_name_like(&token.text) && !is_sql_keyword(&token.text) =>
            {
                let followed_by_paren =
                    matches!(item.get(idx + 1).map(|next| &next.kind), Some(TokenKind::Punct('(')));
                if !followed_by_paren {
                    best = Some(token);
                }
            }
            _ => {}
        }
    }
    best.map(output_column)
}

fn output_column(token: &Token) -> OutputColumn {
    OutputColumn {
        name: token.text.clone(),
        range: token.range(),
    }
}

fn find_top_level_keyword(tokens: &[Token], start: usize, keyword: &str) -> Option<usize> {
    let mut depth = 0i32;
    for (idx, token) in tokens.iter().enumerate().skip(start) {
        match &token.kind {
            TokenKind::Punct('(') => depth += 1,
            TokenKind::Punct(')') => depth -= 1,
            TokenKind::Ident if depth == 0 && token.text.eq_ignore_ascii_case(keyword) => {
                return Some(idx)
            }
            _ => {}
        }
    }
    None
}

fn find_top_level_keyword_in(item: &[&Token], keyword: &str) -> Option<usize> {
    let mut depth = 0i32;
    for (idx, token) in item.iter().enumerate() {
        match &token.kind {
            TokenKind::Punct('(') => depth += 1,
            TokenKind::Punct(')') => depth -= 1,
            TokenKind::Ident if depth == 0 && token.text.eq_ignore_ascii_case(keyword) => {
                return Some(idx)
            }
            _ => {}
        }
    }
    None
}

fn is_name_like(text: &str) -> bool {
    text.chars()
        .next()
        .is_some_and(|c| c.is_alphabetic() || c == '_')
}

fn is_sql_keyword(text: &str) -> bool {
    const KEYWORDS: &[&str] = &[
        "select", "from", "as", "where", "distinct", "and", "or", "not", "null", "true", "false",
        "case", "when", "then", "else", "end", "on", "over", "partition", "by", "order", "group",
        "having", "limit", "asc", "desc", "is", "in", "join", "left", "right", "inner", "outer",
    ];
    KEYWORDS
        .iter()
        .any(|keyword| text.eq_ignore_ascii_case(keyword))
}

fn range_contains(range: &Range, line: u32, col: u32) -> bool {
    line == range.start.line
        && line == range.end.line
        && col >= range.start.character
        && col <= range.end.character
}

#[derive(Debug, Clone, PartialEq)]
enum TokenKind {
    Ident,
    Punct(char),
}

#[derive(Debug, Clone)]
struct Token {
    text: String,
    kind: TokenKind,
    line: u32,
    col_start: u32,
    col_end: u32,
}

impl Token {
    fn range(&self) -> Range {
        Range::new(
            Position::new(self.line, self.col_start),
            Position::new(self.line, self.col_end),
        )
    }
}

/// Tokenize SQL, skipping comments, string literals, and `${...}` Chalk input
/// interpolations. Positions are tracked as 0-based (line, character).
fn tokenize(text: &str) -> Vec<Token> {
    let chars: Vec<char> = text.chars().collect();
    let mut tokens = Vec::new();
    let mut line: u32 = 0;
    let mut col: u32 = 0;
    let mut i = 0;

    while i < chars.len() {
        let c = chars[i];
        match c {
            '\n' => {
                line += 1;
                col = 0;
                i += 1;
            }
            c if c.is_whitespace() => {
                col += 1;
                i += 1;
            }
            '-' if chars.get(i + 1) == Some(&'-') => {
                while i < chars.len() && chars[i] != '\n' {
                    i += 1;
                    col += 1;
                }
            }
            '/' if chars.get(i + 1) == Some(&'*') => {
                i += 2;
                col += 2;
                while i < chars.len() && !(chars[i] == '*' && chars.get(i + 1) == Some(&'/')) {
                    advance(&chars, &mut i, &mut line, &mut col);
                }
                if i < chars.len() {
                    i += 2;
                    col += 2;
                }
            }
            '\'' | '"' => {
                let quote = c;
                i += 1;
                col += 1;
                while i < chars.len() && chars[i] != quote {
                    advance(&chars, &mut i, &mut line, &mut col);
                }
                if i < chars.len() {
                    i += 1;
                    col += 1;
                }
            }
            '$' if chars.get(i + 1) == Some(&'{') => {
                i += 2;
                col += 2;
                while i < chars.len() && chars[i] != '}' {
                    advance(&chars, &mut i, &mut line, &mut col);
                }
                if i < chars.len() {
                    i += 1;
                    col += 1;
                }
            }
            c if c.is_alphanumeric() || c == '_' => {
                let start_col = col;
                let mut ident = String::new();
                while i < chars.len() && (chars[i].is_alphanumeric() || chars[i] == '_') {
                    ident.push(chars[i]);
                    i += 1;
                    col += 1;
                }
                tokens.push(Token {
                    text: ident,
                    kind: TokenKind::Ident,
                    line,
                    col_start: start_col,
                    col_end: col,
                });
            }
            other => {
                tokens.push(Token {
                    text: other.to_string(),
                    kind: TokenKind::Punct(other),
                    line,
                    col_start: col,
                    col_end: col + 1,
                });
                i += 1;
                col += 1;
            }
        }
    }

    tokens
}

fn advance(chars: &[char], i: &mut usize, line: &mut u32, col: &mut u32) {
    if chars[*i] == '\n' {
        *line += 1;
        *col = 0;
    } else {
        *col += 1;
    }
    *i += 1;
}

#[cfg(test)]
mod tests {
    use super::*;

    const RESOLVER: &str = "-- source: RISK_SF\n\
-- cron: 1h\n\
-- resolves: superhero\n\
-- count: all\n\
select name, size from superhero_table where id = ${superhero.id}";

    #[test]
    fn finds_resolves_identifier_and_range() {
        let reference = resolves_ref(RESOLVER).expect("resolves directive should be found");
        assert_eq!(reference.identifier, "superhero");
        assert_eq!(reference.range.start.line, 2);
        // `-- resolves: ` is 13 characters, so the identifier starts at col 13.
        assert_eq!(reference.range.start.character, 13);
        assert_eq!(reference.range.end.character, 13 + "superhero".len() as u32);
    }

    #[test]
    fn resolves_ref_at_only_matches_on_the_identifier() {
        // On the `s` of `superhero`.
        assert!(resolves_ref_at(RESOLVER, 2, 13).is_some());
        // On the `resolves` key, not the value.
        assert!(resolves_ref_at(RESOLVER, 2, 3).is_none());
        // On the SQL line.
        assert!(resolves_ref_at(RESOLVER, 4, 7).is_none());
    }

    #[test]
    fn parses_select_output_columns() {
        let columns = output_columns(RESOLVER);
        let names: Vec<&str> = columns.iter().map(|c| c.name.as_str()).collect();
        assert_eq!(names, vec!["name", "size"]);
        // `name` is on the SELECT line (line 4) starting at column 7.
        assert_eq!(columns[0].range.start.line, 4);
        assert_eq!(columns[0].range.start.character, 7);
    }

    #[test]
    fn output_column_at_locates_the_column_under_cursor() {
        let column = output_column_at(RESOLVER, 4, 8).expect("cursor is on `name`");
        assert_eq!(column.name, "name");
        // The `${superhero.id}` interpolation is opaque, so `id` is not a column.
        assert!(output_column_at(RESOLVER, 4, 60).is_none());
    }

    #[test]
    fn aliases_resolve_to_the_alias_name() {
        let sql = "-- resolves: superhero\nselect raw_name as name, count(*) as c from t";
        let columns = output_columns(sql);
        assert_eq!(
            columns.iter().map(|c| c.name.as_str()).collect::<Vec<_>>(),
            vec!["name", "c"]
        );
    }

    #[test]
    fn qualified_columns_resolve_to_the_trailing_identifier() {
        let sql = "-- resolves: superhero\nselect t.name, t.size from t";
        let columns = output_columns(sql);
        assert_eq!(
            columns.iter().map(|c| c.name.as_str()).collect::<Vec<_>>(),
            vec!["name", "size"]
        );
    }

    #[test]
    fn function_calls_without_aliases_are_skipped() {
        let sql = "-- resolves: superhero\nselect count(*), name from t";
        let columns = output_columns(sql);
        assert_eq!(
            columns.iter().map(|c| c.name.as_str()).collect::<Vec<_>>(),
            vec!["name"]
        );
    }

    #[test]
    fn distinct_is_not_treated_as_a_column() {
        let sql = "-- resolves: superhero\nselect distinct name from t";
        let columns = output_columns(sql);
        assert_eq!(
            columns.iter().map(|c| c.name.as_str()).collect::<Vec<_>>(),
            vec!["name"]
        );
    }

    #[test]
    fn resolves_can_be_a_class_name() {
        let sql = "-- source: RISK_SF\n-- resolves: ConfirmedFraud\nSELECT id FROM t";
        let reference = resolves_ref(sql).expect("resolves directive should be found");
        assert_eq!(reference.identifier, "ConfirmedFraud");
    }
}
