//! Parsing helpers for Chalk underscore expressions (`_.foo`) inside Python
//! feature files.
//!
//! In a Chalk feature class, `_` refers to the feature class being defined, so
//! `_.member` is an attribute of that class. Inside a relationship subscript
//! such as `_.children[_.date < _.chalk_now]`, the inner `_` instead refers to
//! the class on the other side of the `children` relationship.
//!
//! These functions are pure text analysis: they find the `_.member` access (or
//! `_.` completion site) under the cursor and report the chain of relationship
//! members that scope it. Resolving those names to feature classes / fields is
//! the caller's job (it needs the project's AST index).

use lsp_types::{Position, Range};

/// A `_.member` attribute access under the cursor.
#[derive(Debug, Clone, PartialEq)]
pub struct UnderscoreMember {
    /// The accessed member name (e.g. `children`).
    pub member: String,
    /// The source range of the member identifier.
    pub range: Range,
    /// Relationship members that scope the `_` root, outermost first. Empty when
    /// `_` refers directly to the enclosing feature class. For the inner `date`
    /// in `_.children[_.date ...]` this is `["children"]`.
    pub scope_chain: Vec<String>,
}

/// A `_.` completion request under the cursor.
#[derive(Debug, Clone, PartialEq)]
pub struct UnderscoreCompletion {
    /// The partial member text already typed after `_.` (may be empty).
    pub prefix: String,
    /// Relationship members that scope the `_` root, outermost first.
    pub scope_chain: Vec<String>,
}

/// Return the `_.member` access under the cursor, if any.
pub fn underscore_member_at(text: &str, line: u32, col: u32) -> Option<UnderscoreMember> {
    let chars: Vec<char> = text.chars().collect();
    let offset = to_offset(&chars, line, col);

    // The identifier under (or adjacent to) the cursor.
    let mut id_start = offset;
    while id_start > 0 && is_ident_char(chars[id_start - 1]) {
        id_start -= 1;
    }
    let mut id_end = offset;
    while id_end < chars.len() && is_ident_char(chars[id_end]) {
        id_end += 1;
    }
    if id_start == id_end {
        return None;
    }
    let member: String = chars[id_start..id_end].iter().collect();

    // It must be a `_.member` access: the identifier is immediately preceded by
    // `.`, and the token before that `.` is a standalone `_`.
    let underscore_offset = underscore_root_before(&chars, id_start)?;
    let scope_chain = relationship_scope_chain(&chars, underscore_offset);

    Some(UnderscoreMember {
        member,
        range: Range::new(position_of(&chars, id_start), position_of(&chars, id_end)),
        scope_chain,
    })
}

/// Return the `_.` completion context under the cursor, if any.
pub fn underscore_completion_at(text: &str, line: u32, col: u32) -> Option<UnderscoreCompletion> {
    let chars: Vec<char> = text.chars().collect();
    let offset = to_offset(&chars, line, col);

    // The partial member typed to the left of the cursor.
    let mut prefix_start = offset;
    while prefix_start > 0 && is_ident_char(chars[prefix_start - 1]) {
        prefix_start -= 1;
    }
    let prefix: String = chars[prefix_start..offset].iter().collect();

    let underscore_offset = underscore_root_before(&chars, prefix_start)?;
    let scope_chain = relationship_scope_chain(&chars, underscore_offset);

    Some(UnderscoreCompletion {
        prefix,
        scope_chain,
    })
}

/// If the position `before` is immediately preceded by `_.`, return the offset
/// of the standalone `_` root.
fn underscore_root_before(chars: &[char], before: usize) -> Option<usize> {
    if before == 0 || chars[before - 1] != '.' {
        return None;
    }
    let dot = before - 1;
    let mut token_start = dot;
    while token_start > 0 && is_ident_char(chars[token_start - 1]) {
        token_start -= 1;
    }
    let token: String = chars[token_start..dot].iter().collect();
    if token != "_" {
        return None;
    }
    // The `_` must be a standalone root, not an attribute access like `foo._`.
    if token_start > 0 && (chars[token_start - 1] == '.' || is_ident_char(chars[token_start - 1])) {
        return None;
    }
    Some(token_start)
}

/// Walk outward from an `_` root, collecting the relationship members of any
/// enclosing `_.relationship[...]` subscripts (outermost first).
fn relationship_scope_chain(chars: &[char], underscore_offset: usize) -> Vec<String> {
    let mut chain = Vec::new();
    let mut pos = underscore_offset;
    while let Some(open_bracket) = enclosing_open_bracket(chars, pos) {
        let Some((relationship, root_offset)) = underscore_member_before(chars, open_bracket) else {
            break;
        };
        chain.push(relationship);
        pos = root_offset;
    }
    chain.reverse();
    chain
}

/// Scanning left from `pos`, find the index of the nearest `[` that encloses it.
/// Returns `None` if the nearest unmatched opener is `(` or `{` (meaning `pos`
/// is a call argument / dict entry, not a subscript element).
fn enclosing_open_bracket(chars: &[char], pos: usize) -> Option<usize> {
    let mut pending: Vec<char> = Vec::new();
    let mut i = pos;
    while i > 0 {
        i -= 1;
        match chars[i] {
            ')' | ']' | '}' => pending.push(chars[i]),
            '(' => {
                if pending.last() == Some(&')') {
                    pending.pop();
                } else if pending.is_empty() {
                    return None;
                } else {
                    pending.pop();
                }
            }
            '{' => {
                if pending.last() == Some(&'}') {
                    pending.pop();
                } else if pending.is_empty() {
                    return None;
                } else {
                    pending.pop();
                }
            }
            '[' => {
                if pending.last() == Some(&']') {
                    pending.pop();
                } else if pending.is_empty() {
                    return Some(i);
                } else {
                    pending.pop();
                }
            }
            _ => {}
        }
    }
    None
}

/// If the `[` at `open_bracket` is preceded by `_.relationship`, return the
/// relationship name and the offset of its `_` root.
fn underscore_member_before(chars: &[char], open_bracket: usize) -> Option<(String, usize)> {
    let mut id_start = open_bracket;
    while id_start > 0 && is_ident_char(chars[id_start - 1]) {
        id_start -= 1;
    }
    if id_start == open_bracket {
        return None;
    }
    let relationship: String = chars[id_start..open_bracket].iter().collect();
    let root_offset = underscore_root_before(chars, id_start)?;
    Some((relationship, root_offset))
}

fn is_ident_char(c: char) -> bool {
    c.is_alphanumeric() || c == '_'
}

fn to_offset(chars: &[char], line: u32, col: u32) -> usize {
    let mut current_line = 0u32;
    let mut idx = 0usize;
    while idx < chars.len() && current_line < line {
        if chars[idx] == '\n' {
            current_line += 1;
        }
        idx += 1;
    }
    (idx + col as usize).min(chars.len())
}

fn position_of(chars: &[char], offset: usize) -> Position {
    let mut line = 0u32;
    let mut col = 0u32;
    for &c in chars.iter().take(offset) {
        if c == '\n' {
            line += 1;
            col = 0;
        } else {
            col += 1;
        }
    }
    Position::new(line, col)
}

#[cfg(test)]
mod tests {
    use super::*;

    const WINDOWED: &str = "from chalk.features import features, DataFrame, windowed, Windowed\n\
\n\
@features\n\
class Parent:\n\
    id: int\n\
    children: DataFrame[Child]\n\
    child_count: Windowed[int] = windowed(\n\
        \"1d\",\n\
        \"30d\",\n\
        expression=_.children[\n\
            _.date < _.chalk_now,\n\
            _.date > _.chalk_window,\n\
        ].count(),\n\
        materialization=True,\n\
    )";

    fn line_of(text: &str, needle: &str) -> u32 {
        text.lines()
            .position(|l| l.contains(needle))
            .expect("needle should be present") as u32
    }

    #[test]
    fn finds_top_level_relationship_member() {
        // Cursor on `children` in `expression=_.children[`.
        let line = line_of(WINDOWED, "expression=_.children");
        let col = WINDOWED.lines().nth(line as usize).unwrap().find("children").unwrap() as u32 + 2;
        let member = underscore_member_at(WINDOWED, line, col).expect("should find _.children");
        assert_eq!(member.member, "children");
        assert!(member.scope_chain.is_empty());
    }

    #[test]
    fn finds_nested_member_scoped_by_relationship() {
        // Cursor on the first `date` in `_.date < _.chalk_now`.
        let line = line_of(WINDOWED, "_.date < _.chalk_now");
        let raw = WINDOWED.lines().nth(line as usize).unwrap();
        let col = raw.find("date").unwrap() as u32 + 1;
        let member = underscore_member_at(WINDOWED, line, col).expect("should find _.date");
        assert_eq!(member.member, "date");
        assert_eq!(member.scope_chain, vec!["children".to_string()]);
    }

    #[test]
    fn nested_chalk_now_is_scoped_too() {
        let line = line_of(WINDOWED, "_.date < _.chalk_now");
        let raw = WINDOWED.lines().nth(line as usize).unwrap();
        let col = raw.find("chalk_now").unwrap() as u32 + 1;
        let member = underscore_member_at(WINDOWED, line, col).expect("should find _.chalk_now");
        assert_eq!(member.member, "chalk_now");
        assert_eq!(member.scope_chain, vec!["children".to_string()]);
    }

    #[test]
    fn plain_attribute_access_is_not_an_underscore_member() {
        let text = "x = obj.value\n";
        let col = text.find("value").unwrap() as u32 + 1;
        assert!(underscore_member_at(text, 0, col).is_none());
    }

    #[test]
    fn dotted_underscore_attribute_is_not_a_root() {
        // `foo._.bar` — the `_` here is an attribute of `foo`, not a Chalk root.
        let text = "y = foo._.bar\n";
        let col = text.find("bar").unwrap() as u32 + 1;
        assert!(underscore_member_at(text, 0, col).is_none());
    }

    #[test]
    fn completion_after_dot_lists_enclosing_class() {
        let text = "    total = _.\n";
        // Cursor right after `_.`.
        let col = text.find("_.").unwrap() as u32 + 2;
        let completion = underscore_completion_at(text, 0, col).expect("should be a completion site");
        assert_eq!(completion.prefix, "");
        assert!(completion.scope_chain.is_empty());
    }

    #[test]
    fn completion_with_partial_prefix() {
        let text = "    total = _.chi\n";
        let col = text.find("chi").unwrap() as u32 + 3;
        let completion = underscore_completion_at(text, 0, col).expect("should be a completion site");
        assert_eq!(completion.prefix, "chi");
        assert!(completion.scope_chain.is_empty());
    }

    #[test]
    fn completion_inside_relationship_is_scoped() {
        let text = "    rows = _.children[_.\n";
        let col = text.rfind("_.").unwrap() as u32 + 2;
        let completion = underscore_completion_at(text, 0, col).expect("should be a completion site");
        assert_eq!(completion.prefix, "");
        assert_eq!(completion.scope_chain, vec!["children".to_string()]);
    }

    #[test]
    fn completion_only_after_underscore() {
        // `obj.` should not produce an underscore completion.
        let text = "    total = obj.\n";
        let col = text.find("obj.").unwrap() as u32 + 4;
        assert!(underscore_completion_at(text, 0, col).is_none());
    }
}
