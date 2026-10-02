//! Port of `com.dashjoin.jsonata.json` (eclipsesource minimal-json based
//! parser) plus the value→JSON serializer used by `$string`.
//!
//! JSON `null` parses to [`JValue::Null`] (== `Jsonata.NULL_VALUE`), since our
//! value model distinguishes Null from Undefined directly (see module docs in
//! `value.rs`). Numbers parse through `Double.parseDouble` semantics → f64.

use crate::value::{JValue, Object};

#[derive(Debug, Clone)]
pub struct JsonParseError {
    pub message: String,
    pub offset: usize,
    pub line: usize,
    pub column: usize,
}

impl std::fmt::Display for JsonParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{} at {}:{}", self.message, self.line, self.column)
    }
}

const MAX_NESTING_LEVEL: i32 = 1000;

struct Parser {
    chars: Vec<char>,
    index: usize, // index of next char to read (current is chars[index-1])
    current: Option<char>,
    line: usize,
    line_offset: usize, // offset of start of current line
    nesting: i32,
}

impl Parser {
    fn new(s: &str) -> Parser {
        Parser {
            chars: s.chars().collect(),
            index: 0,
            current: None,
            line: 1,
            line_offset: 0,
            nesting: 0,
        }
    }

    fn read(&mut self) {
        if self.current == Some('\n') {
            self.line += 1;
            self.line_offset = self.index;
        }
        if self.index < self.chars.len() {
            self.current = Some(self.chars[self.index]);
            self.index += 1;
        } else {
            self.current = None;
            self.index += 1;
        }
    }

    fn location(&self) -> (usize, usize, usize) {
        // offset of the current char = index - 1
        let offset = self.index.saturating_sub(1);
        // Java counts the column in UTF-16 code units within the line.
        let column = self.chars[self.line_offset..offset.min(self.chars.len())]
            .iter()
            .map(|c| c.len_utf16())
            .sum::<usize>()
            + 1;
        (offset, self.line, column)
    }

    fn error(&self, message: &str) -> JsonParseError {
        let (offset, line, column) = self.location();
        JsonParseError {
            message: message.to_string(),
            offset,
            line,
            column,
        }
    }

    fn expected(&self, what: &str) -> JsonParseError {
        if self.current.is_none() {
            self.error("Unexpected end of input")
        } else {
            self.error(&format!("Expected {}", what))
        }
    }

    fn parse(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.skip_ws();
        let v = self.read_value()?;
        self.skip_ws();
        if self.current.is_some() {
            return Err(self.error("Unexpected character"));
        }
        Ok(v)
    }

    fn skip_ws(&mut self) {
        while matches!(
            self.current,
            Some(' ') | Some('\t') | Some('\n') | Some('\r')
        ) {
            self.read();
        }
    }

    fn read_value(&mut self) -> Result<JValue, JsonParseError> {
        match self.current {
            Some('n') => self.read_null(),
            Some('t') => self.read_true(),
            Some('f') => self.read_false(),
            Some('"') => Ok(JValue::string(self.read_string_internal()?)),
            Some('[') => self.read_array(),
            Some('{') => self.read_object(),
            Some(c) if c == '-' || c.is_ascii_digit() => self.read_number(),
            _ => Err(self.expected("value")),
        }
    }

    fn read_char(&mut self, ch: char) -> bool {
        if self.current != Some(ch) {
            return false;
        }
        self.read();
        true
    }

    fn read_required_char(&mut self, ch: char) -> Result<(), JsonParseError> {
        if !self.read_char(ch) {
            return Err(self.expected(&format!("'{}'", ch)));
        }
        Ok(())
    }

    fn read_null(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.read_required_char('u')?;
        self.read_required_char('l')?;
        self.read_required_char('l')?;
        Ok(JValue::Null)
    }

    fn read_true(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.read_required_char('r')?;
        self.read_required_char('u')?;
        self.read_required_char('e')?;
        Ok(JValue::Bool(true))
    }

    fn read_false(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.read_required_char('a')?;
        self.read_required_char('l')?;
        self.read_required_char('s')?;
        self.read_required_char('e')?;
        Ok(JValue::Bool(false))
    }

    fn read_array(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.nesting += 1;
        if self.nesting > MAX_NESTING_LEVEL {
            return Err(self.error("Nesting too deep"));
        }
        self.skip_ws();
        let mut items = Vec::new();
        if self.read_char(']') {
            self.nesting -= 1;
            return Ok(JValue::array(items, Default::default()));
        }
        loop {
            self.skip_ws();
            items.push(self.read_value()?);
            self.skip_ws();
            if !self.read_char(',') {
                break;
            }
        }
        if !self.read_char(']') {
            return Err(self.expected("',' or ']'"));
        }
        self.nesting -= 1;
        Ok(JValue::array(items, Default::default()))
    }

    fn read_object(&mut self) -> Result<JValue, JsonParseError> {
        self.read();
        self.nesting += 1;
        if self.nesting > MAX_NESTING_LEVEL {
            return Err(self.error("Nesting too deep"));
        }
        self.skip_ws();
        let mut obj = Object::new();
        if self.read_char('}') {
            self.nesting -= 1;
            return Ok(JValue::object(obj));
        }
        loop {
            self.skip_ws();
            if self.current != Some('"') {
                return Err(self.expected("name"));
            }
            let name = self.read_string_internal()?;
            self.skip_ws();
            if !self.read_char(':') {
                return Err(self.expected("':'"));
            }
            self.skip_ws();
            let value = self.read_value()?;
            obj.insert(name, value); // LinkedHashMap.put semantics (keeps order, replaces)
            self.skip_ws();
            if !self.read_char(',') {
                break;
            }
        }
        if !self.read_char('}') {
            return Err(self.expected("',' or '}'"));
        }
        self.nesting -= 1;
        Ok(JValue::object(obj))
    }

    fn read_string_internal(&mut self) -> Result<String, JsonParseError> {
        self.read(); // opening quote
                     // Build as UTF-16 code units so surrogate pairs from \u escapes combine.
        let mut units: Vec<u16> = Vec::new();
        loop {
            match self.current {
                None => return Err(self.expected("valid string character")),
                Some('"') => break,
                Some('\\') => {
                    self.read_escape(&mut units)?;
                }
                Some(c) if (c as u32) < 0x20 => {
                    return Err(self.expected("valid string character"));
                }
                Some(c) => {
                    let mut buf = [0u16; 2];
                    for u in c.encode_utf16(&mut buf) {
                        units.push(*u);
                    }
                    self.read();
                }
            }
        }
        self.read(); // closing quote
        Ok(String::from_utf16_lossy(&units))
    }

    fn read_escape(&mut self, units: &mut Vec<u16>) -> Result<(), JsonParseError> {
        self.read();
        match self.current {
            Some('"') => units.push('"' as u16),
            Some('/') => units.push('/' as u16),
            Some('\\') => units.push('\\' as u16),
            Some('b') => units.push(0x08),
            Some('f') => units.push(0x0C),
            Some('n') => units.push('\n' as u16),
            Some('r') => units.push('\r' as u16),
            Some('t') => units.push('\t' as u16),
            Some('u') => {
                let mut value: u16 = 0;
                for _ in 0..4 {
                    self.read();
                    let d = match self.current {
                        Some(c) if c.is_ascii_hexdigit() => c.to_digit(16).unwrap() as u16,
                        _ => return Err(self.expected("hexadecimal digit")),
                    };
                    value = value * 16 + d;
                }
                units.push(value);
            }
            _ => return Err(self.expected("valid escape sequence")),
        }
        self.read();
        Ok(())
    }

    fn read_number(&mut self) -> Result<JValue, JsonParseError> {
        let start = self.index - 1;
        self.read_char('-');
        let first_digit = self.current;
        if !self.read_digit() {
            return Err(self.expected("digit"));
        }
        if first_digit != Some('0') {
            while self.read_digit() {}
        }
        self.read_fraction()?;
        self.read_exponent()?;
        let end = self.index - 1;
        let s: String = self.chars[start..end.min(self.chars.len())]
            .iter()
            .collect();
        let d: f64 = s.parse().map_err(|_| self.error("Invalid number"))?;
        // A literal like 1e400 overflows to infinity (same as Double.parseDouble).
        // Java's handler swallows the D1001 that Utils.convertNumber throws and
        // corrupts the parse (stale previous value) — a bug we do not replicate;
        // reject the document instead so Infinity never enters the value space.
        if !d.is_finite() {
            return Err(self.error("Number out of range"));
        }
        Ok(JValue::Number(d))
    }

    fn read_fraction(&mut self) -> Result<bool, JsonParseError> {
        if !self.read_char('.') {
            return Ok(false);
        }
        if !self.read_digit() {
            return Err(self.expected("digit"));
        }
        while self.read_digit() {}
        Ok(true)
    }

    fn read_exponent(&mut self) -> Result<bool, JsonParseError> {
        if !self.read_char('e') && !self.read_char('E') {
            return Ok(false);
        }
        if !self.read_char('+') {
            self.read_char('-');
        }
        if !self.read_digit() {
            return Err(self.expected("digit"));
        }
        while self.read_digit() {}
        Ok(true)
    }

    fn read_digit(&mut self) -> bool {
        match self.current {
            Some(c) if c.is_ascii_digit() => {
                self.read();
                true
            }
            _ => false,
        }
    }
}

/// Parse a JSON string into a [`JValue`]. (`Json.parseJson`)
pub fn parse_json(s: &str) -> Result<JValue, JsonParseError> {
    Parser::new(s).parse()
}

// ---------------------------------------------------------------------------
// Serialization (used by `$string` / Functions.string when no pretty printing)
// ---------------------------------------------------------------------------

/// Quote a string into `out`, mirroring `Utils.quote`.
pub fn quote(string: &str, out: &mut String) {
    for c in string.chars() {
        match c {
            '\\' | '"' => {
                out.push('\\');
                out.push(c);
            }
            '\u{08}' => out.push_str("\\b"),
            '\t' => out.push_str("\\t"),
            '\n' => out.push_str("\\n"),
            '\u{0C}' => out.push_str("\\f"),
            '\r' => out.push_str("\\r"),
            _ => {
                let n = c as u32;
                if n < 0x20 || (0x80..0xa0).contains(&n) || (0x2000..0x2100).contains(&n) {
                    out.push_str("\\u");
                    let hhhh = format!("{:x}", n);
                    for _ in 0..(4 - hhhh.len()) {
                        out.push('0');
                    }
                    out.push_str(&hhhh);
                } else {
                    out.push(c);
                }
            }
        }
    }
}
