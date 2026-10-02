//! Port of `com.dashjoin.jsonata.Tokenizer`.

use crate::error::{JError, JResult};
use std::collections::HashMap;

/// Token value: either a literal value, an operator/name string, or a regex.
#[derive(Debug, Clone)]
pub enum TokenValue {
    /// A name / operator / variable string value.
    Str(String),
    Number(f64),
    Bool(bool),
    /// `null` literal token value (Java null).
    Null,
    /// A scanned regex: (pattern, case_insensitive, multiline).
    Regex(String, bool, bool),
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: String,
    pub value: TokenValue,
    pub position: usize,
    pub id: Option<String>,
}

pub struct Tokenizer {
    path: Vec<char>,
    pub position: usize,
    length: usize,
    depth: i32,
    operators: HashMap<&'static str, i32>,
    escapes: HashMap<char, char>,
    /// Cumulative UTF-16 lengths (see [`Tokenizer::u16`]).
    u16_prefix: Vec<usize>,
}

/// Binding powers for the operators (`Tokenizer.operators`). Public so the
/// parser can share the table.
pub fn operators_table() -> HashMap<&'static str, i32> {
    let mut m = HashMap::new();
    m.insert(".", 75);
    m.insert("[", 80);
    m.insert("]", 0);
    m.insert("{", 70);
    m.insert("}", 0);
    m.insert("(", 80);
    m.insert(")", 0);
    m.insert(",", 0);
    m.insert("@", 80);
    m.insert("#", 80);
    m.insert(";", 80);
    m.insert(":", 80);
    m.insert("?", 20);
    m.insert("+", 50);
    m.insert("-", 50);
    m.insert("*", 60);
    m.insert("/", 60);
    m.insert("%", 60);
    m.insert("|", 20);
    m.insert("=", 40);
    m.insert("<", 40);
    m.insert(">", 40);
    m.insert("^", 40);
    m.insert("**", 60);
    m.insert("..", 20);
    m.insert(":=", 10);
    m.insert("!=", 40);
    m.insert("<=", 40);
    m.insert(">=", 40);
    m.insert("~>", 40);
    m.insert("?:", 40);
    m.insert("??", 40);
    m.insert("and", 30);
    m.insert("or", 25);
    m.insert("in", 40);
    m.insert("&", 50);
    m.insert("!", 0);
    m.insert("~", 0);
    m
}

impl Tokenizer {
    pub fn new(path: &str) -> Tokenizer {
        let chars: Vec<char> = path.chars().collect();
        let length = chars.len();
        let mut escapes = HashMap::new();
        escapes.insert('"', '"');
        escapes.insert('\\', '\\');
        escapes.insert('/', '/');
        escapes.insert('b', '\u{08}');
        escapes.insert('f', '\u{0C}');
        escapes.insert('n', '\n');
        escapes.insert('r', '\r');
        escapes.insert('t', '\t');
        // Cumulative UTF-16 length before each char index (len+1 entries).
        // Token/error positions are reported in UTF-16 code units to match
        // Java's String indexing (jsonata-js positions are UTF-16 too); the
        // internal scanning below stays code-point based.
        let mut u16_prefix = Vec::with_capacity(length + 1);
        let mut acc = 0usize;
        u16_prefix.push(0);
        for c in &chars {
            acc += c.len_utf16();
            u16_prefix.push(acc);
        }
        Tokenizer {
            path: chars,
            position: 0,
            length,
            depth: 0,
            operators: operators_table(),
            escapes,
            u16_prefix,
        }
    }

    /// Translate an internal code-point index into a UTF-16 unit offset
    /// (Java `String` position) for externally visible positions.
    fn u16(&self, char_pos: usize) -> usize {
        *self
            .u16_prefix
            .get(char_pos)
            .unwrap_or(self.u16_prefix.last().unwrap_or(&0))
    }

    fn create(&self, token_type: &str, value: TokenValue) -> Token {
        Token {
            token_type: token_type.to_string(),
            value,
            position: self.u16(self.position),
            id: None,
        }
    }

    fn char_at(&self, pos: usize) -> char {
        // Java String.charAt throws on OOB; the original code relies on certain
        // accesses being valid. We return '\0' for OOB to mirror the few places
        // that compare against fixed chars; callers guard with `haveMore`.
        if pos < self.length {
            self.path[pos]
        } else {
            '\0'
        }
    }

    fn is_closing_slash(&self, position: usize) -> bool {
        if self.char_at(position) == '/' && self.depth == 0 {
            let mut backslash_count = 0;
            while self.char_at(position - (backslash_count + 1)) == '\\' {
                backslash_count += 1;
            }
            if backslash_count % 2 == 0 {
                return true;
            }
        }
        false
    }

    fn scan_regex(&mut self) -> JResult<TokenValue> {
        let start = self.position;
        let pattern;
        while self.position < self.length {
            let current_char = self.char_at(self.position);
            if self.is_closing_slash(self.position) {
                pattern = self.substring(start, self.position);
                if pattern.is_empty() {
                    return Err(JError::at("S0301", self.u16(self.position) as i32));
                }
                self.position += 1;
                let mut cc = if self.position < self.length {
                    self.char_at(self.position)
                } else {
                    '\0'
                };
                let flag_start = self.position;
                while cc == 'i' || cc == 'm' {
                    self.position += 1;
                    cc = if self.position < self.length {
                        self.char_at(self.position)
                    } else {
                        '\0'
                    };
                }
                let flags: String = self.substring(flag_start, self.position) + "g";
                let case_insensitive = flags.contains('i');
                let multiline = flags.contains('m');
                return Ok(TokenValue::Regex(pattern, case_insensitive, multiline));
            }
            if (current_char == '(' || current_char == '[' || current_char == '{')
                && self.char_at(self.position - 1) != '\\'
            {
                self.depth += 1;
            }
            if (current_char == ')' || current_char == ']' || current_char == '}')
                && self.char_at(self.position - 1) != '\\'
            {
                self.depth -= 1;
            }
            self.position += 1;
        }
        Err(JError::at("S0302", self.u16(self.position) as i32))
    }

    fn substring(&self, start: usize, end: usize) -> String {
        self.path[start..end].iter().collect()
    }

    /// Port of `Tokenizer.next(boolean prefix)`. Returns Ok(None) at EOF.
    pub fn next(&mut self, prefix: bool) -> JResult<Option<Token>> {
        if self.position >= self.length {
            return Ok(None);
        }
        let mut current_char = self.path[self.position];
        // skip whitespace
        while self.position < self.length && " \t\n\r".contains(current_char) {
            self.position += 1;
            if self.position >= self.length {
                return Ok(None);
            }
            current_char = self.path[self.position];
        }
        // skip comments
        if current_char == '/' && self.char_at(self.position + 1) == '*' {
            let comment_start = self.position;
            self.position += 2;
            current_char = self.char_at(self.position);
            while !(current_char == '*' && self.char_at(self.position + 1) == '/') {
                self.position += 1;
                current_char = self.char_at(self.position);
                if self.position >= self.length {
                    return Err(JError::at("S0106", self.u16(comment_start) as i32));
                }
            }
            self.position += 2;
            // (currentChar reassigned but immediately recursing)
            return self.next(prefix);
        }
        // test for regex
        if !prefix && current_char == '/' {
            self.position += 1;
            let r = self.scan_regex()?;
            return Ok(Some(self.create("regex", r)));
        }
        let have_more = self.position < self.length - 1;
        // double-char operators
        if current_char == '.' && have_more && self.char_at(self.position + 1) == '.' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("..".into()))));
        }
        if current_char == ':' && have_more && self.char_at(self.position + 1) == '=' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str(":=".into()))));
        }
        if current_char == '!' && have_more && self.char_at(self.position + 1) == '=' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("!=".into()))));
        }
        if current_char == '>' && have_more && self.char_at(self.position + 1) == '=' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str(">=".into()))));
        }
        if current_char == '<' && have_more && self.char_at(self.position + 1) == '=' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("<=".into()))));
        }
        if current_char == '*' && have_more && self.char_at(self.position + 1) == '*' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("**".into()))));
        }
        if current_char == '~' && have_more && self.char_at(self.position + 1) == '>' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("~>".into()))));
        }
        if current_char == '?' && have_more && self.char_at(self.position + 1) == ':' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("?:".into()))));
        }
        if current_char == '?' && have_more && self.char_at(self.position + 1) == '?' {
            self.position += 2;
            return Ok(Some(self.create("operator", TokenValue::Str("??".into()))));
        }
        // single char operators
        let cc_str = current_char.to_string();
        if self.operators.contains_key(cc_str.as_str()) {
            self.position += 1;
            return Ok(Some(self.create("operator", TokenValue::Str(cc_str))));
        }
        // string literals
        if current_char == '"' || current_char == '\'' {
            let quote_type = current_char;
            self.position += 1;
            // Accumulate UTF-16 code units (like Java's String) so that
            // `𝄞` surrogate pairs combine into one code point.
            let mut units: Vec<u16> = Vec::new();
            while self.position < self.length {
                current_char = self.path[self.position];
                if current_char == '\\' {
                    self.position += 1;
                    if self.position < self.length {
                        current_char = self.path[self.position];
                    } else {
                        return Err(JError::with_current(
                            "S0103",
                            self.u16(self.position) as i32,
                            JValue_str(""),
                        ));
                    }
                    if let Some(esc) = self.escapes.get(&current_char) {
                        let mut buf = [0u16; 2];
                        for u in esc.encode_utf16(&mut buf) {
                            units.push(*u);
                        }
                    } else if current_char == 'u' {
                        // u should be followed by 4 hex digits
                        let octets: String = if self.position + 5 < self.length {
                            self.path[self.position + 1..self.position + 1 + 4]
                                .iter()
                                .collect()
                        } else {
                            String::new()
                        };
                        if !octets.is_empty() && octets.chars().all(|c| c.is_ascii_hexdigit()) {
                            let codepoint = u32::from_str_radix(&octets, 16).unwrap();
                            // Java: Character.toString((char) codepoint) — raw UTF-16 code unit
                            units.push(codepoint as u16);
                            self.position += 4;
                        } else {
                            return Err(JError::at("S0104", self.u16(self.position) as i32));
                        }
                    } else {
                        return Err(JError::with_current(
                            "S0103",
                            self.u16(self.position) as i32,
                            JValue_str(&current_char.to_string()),
                        ));
                    }
                } else if current_char == quote_type {
                    self.position += 1;
                    let qstr = String::from_utf16_lossy(&units);
                    return Ok(Some(self.create("string", TokenValue::Str(qstr))));
                } else {
                    let mut buf = [0u16; 2];
                    for u in current_char.encode_utf16(&mut buf) {
                        units.push(*u);
                    }
                }
                self.position += 1;
            }
            return Err(JError::at("S0101", self.u16(self.position) as i32));
        }
        // numbers
        if let Some(numstr) = self.match_number() {
            let num: f64 = numstr.parse().unwrap_or(f64::NAN);
            if !num.is_nan() && num.is_finite() {
                self.position += numstr.chars().count();
                return Ok(Some(self.create("number", TokenValue::Number(num))));
            } else {
                return Err(JError::at("S0102", self.u16(self.position) as i32));
            }
        }
        // quoted names (backticks)
        if current_char == '`' {
            self.position += 1;
            if let Some(end) = self.index_of('`', self.position) {
                let name = self.substring(self.position, end);
                self.position = end + 1;
                return Ok(Some(self.create("name", TokenValue::Str(name))));
            }
            self.position = self.length;
            return Err(JError::at("S0105", self.u16(self.position) as i32));
        }
        // names
        let mut i = self.position;
        loop {
            let ch = if i < self.length { self.path[i] } else { '\0' };
            let is_op = self.operators.contains_key(ch.to_string().as_str());
            if i == self.length || " \t\n\r".contains(ch) || is_op {
                if self.path[self.position] == '$' {
                    let name = self.substring(self.position + 1, i);
                    self.position = i;
                    return Ok(Some(self.create("variable", TokenValue::Str(name))));
                } else {
                    let name = self.substring(self.position, i);
                    self.position = i;
                    return Ok(Some(match name.as_str() {
                        "or" | "in" | "and" => self.create("operator", TokenValue::Str(name)),
                        "true" => self.create("value", TokenValue::Bool(true)),
                        "false" => self.create("value", TokenValue::Bool(false)),
                        "null" => self.create("value", TokenValue::Null),
                        _ => {
                            if self.position == self.length && name.is_empty() {
                                return Ok(None);
                            }
                            self.create("name", TokenValue::Str(name))
                        }
                    }));
                }
            } else {
                i += 1;
            }
        }
    }

    fn index_of(&self, ch: char, from: usize) -> Option<usize> {
        (from..self.length).find(|&i| self.path[i] == ch)
    }

    /// Match the number regex `^-?(0|([1-9][0-9]*))(\.[0-9]+)?([Ee][-+]?[0-9]+)?`
    /// at the current position, returning the matched substring.
    fn match_number(&self) -> Option<String> {
        let s = &self.path[self.position..];
        let mut i = 0;
        let n = s.len();
        let peek = |idx: usize| if idx < n { s[idx] } else { '\0' };
        // optional -
        if peek(i) == '-' {
            i += 1;
        }
        // 0 | [1-9][0-9]*
        if peek(i) == '0' {
            i += 1;
        } else if ('1'..='9').contains(&peek(i)) {
            i += 1;
            while peek(i).is_ascii_digit() {
                i += 1;
            }
        } else {
            return None;
        }
        // (\.[0-9]+)?
        if peek(i) == '.' && peek(i + 1).is_ascii_digit() {
            i += 1;
            while peek(i).is_ascii_digit() {
                i += 1;
            }
        }
        // ([Ee][-+]?[0-9]+)?
        if peek(i) == 'e' || peek(i) == 'E' {
            let mut j = i + 1;
            if peek(j) == '-' || peek(j) == '+' {
                j += 1;
            }
            if peek(j).is_ascii_digit() {
                j += 1;
                while peek(j).is_ascii_digit() {
                    j += 1;
                }
                i = j;
            }
        }
        Some(s[..i].iter().collect())
    }
}

#[allow(non_snake_case)]
fn JValue_str(s: &str) -> crate::value::JValue {
    crate::value::JValue::from_str_value(s)
}
