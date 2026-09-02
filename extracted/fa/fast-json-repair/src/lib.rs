use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyModule};
use pyo3::IntoPyObjectExt;

#[derive(Debug, Clone, Copy)]
enum RepairKind {
    RemovedLineComment,
    RemovedBlockComment,
    ConvertedSingleQuotedString,
    ClosedUnterminatedString,
    RemovedInvalidEscape,
    PreservedInvalidUnicodeEscape,
    SkippedLeadingContent,
    SkippedTrailingContent,
    CombinedMultipleRootValues,
    QuotedUnquotedKey,
    QuotedUnquotedValue,
    ConvertedPythonLiteral,
    NormalizedInvalidNumber,
    ReplacedInvalidNumber,
    RemovedExtraComma,
    RemovedTrailingComma,
    InsertedMissingColon,
    InsertedMissingComma,
    InsertedMissingValue,
    InsertedMissingObjectCloser,
    InsertedMissingArrayCloser,
    ReplacedMismatchedObjectCloser,
    ReplacedMismatchedArrayCloser,
    ReplacedUnexpectedToken,
    MaximumDepthExceeded,
}

impl RepairKind {
    fn code(self) -> &'static str {
        match self {
            Self::RemovedLineComment => "removed_line_comment",
            Self::RemovedBlockComment => "removed_block_comment",
            Self::ConvertedSingleQuotedString => "converted_single_quoted_string",
            Self::ClosedUnterminatedString => "closed_unterminated_string",
            Self::RemovedInvalidEscape => "removed_invalid_escape",
            Self::PreservedInvalidUnicodeEscape => "preserved_invalid_unicode_escape",
            Self::SkippedLeadingContent => "skipped_leading_content",
            Self::SkippedTrailingContent => "skipped_trailing_content",
            Self::CombinedMultipleRootValues => "combined_multiple_root_values",
            Self::QuotedUnquotedKey => "quoted_unquoted_key",
            Self::QuotedUnquotedValue => "quoted_unquoted_value",
            Self::ConvertedPythonLiteral => "converted_python_literal",
            Self::NormalizedInvalidNumber => "normalized_invalid_number",
            Self::ReplacedInvalidNumber => "replaced_invalid_number",
            Self::RemovedExtraComma => "removed_extra_comma",
            Self::RemovedTrailingComma => "removed_trailing_comma",
            Self::InsertedMissingColon => "inserted_missing_colon",
            Self::InsertedMissingComma => "inserted_missing_comma",
            Self::InsertedMissingValue => "inserted_missing_value",
            Self::InsertedMissingObjectCloser => "inserted_missing_object_closer",
            Self::InsertedMissingArrayCloser => "inserted_missing_array_closer",
            Self::ReplacedMismatchedObjectCloser => "replaced_mismatched_object_closer",
            Self::ReplacedMismatchedArrayCloser => "replaced_mismatched_array_closer",
            Self::ReplacedUnexpectedToken => "replaced_unexpected_token",
            Self::MaximumDepthExceeded => "maximum_depth_exceeded",
        }
    }

    fn text(self) -> &'static str {
        match self {
            Self::RemovedLineComment => "Removed a JavaScript-style line comment",
            Self::RemovedBlockComment => "Removed a JavaScript-style block comment",
            Self::ConvertedSingleQuotedString => {
                "Converted a single-quoted string to a JSON string"
            }
            Self::ClosedUnterminatedString => "Closed an unterminated string",
            Self::RemovedInvalidEscape => "Removed an invalid string escape",
            Self::PreservedInvalidUnicodeEscape => "Preserved an invalid Unicode escape as text",
            Self::SkippedLeadingContent => "Skipped content before the first JSON container",
            Self::SkippedTrailingContent => "Skipped content outside a JSON container",
            Self::CombinedMultipleRootValues => {
                "Combined multiple top-level JSON values into an array"
            }
            Self::QuotedUnquotedKey => "Quoted an unquoted object key",
            Self::QuotedUnquotedValue => "Quoted an unquoted string value",
            Self::ConvertedPythonLiteral => "Converted a Python literal to JSON",
            Self::NormalizedInvalidNumber => "Normalized a non-standard JSON number",
            Self::ReplacedInvalidNumber => "Replaced an invalid number with null",
            Self::RemovedExtraComma => "Removed an extra comma",
            Self::RemovedTrailingComma => "Removed a trailing comma",
            Self::InsertedMissingColon => "Inserted a missing colon after an object key",
            Self::InsertedMissingComma => "Inserted a missing comma between values",
            Self::InsertedMissingValue => "Inserted null for a missing value",
            Self::InsertedMissingObjectCloser => "Inserted a missing closing brace",
            Self::InsertedMissingArrayCloser => "Inserted a missing closing bracket",
            Self::ReplacedMismatchedObjectCloser => {
                "Replaced a mismatched closing bracket with a closing brace"
            }
            Self::ReplacedMismatchedArrayCloser => {
                "Replaced a mismatched closing brace with a closing bracket"
            }
            Self::ReplacedUnexpectedToken => "Replaced an unexpected token with null",
            Self::MaximumDepthExceeded => "Maximum nesting depth was exceeded",
        }
    }
}

#[derive(Debug)]
struct RepairEvent {
    kind: RepairKind,
    position: usize,
}

trait DiagnosticSink {
    const ENABLED: bool;

    fn record(&mut self, kind: RepairKind, position: usize);
    fn set_token_position(&mut self, position: usize);
    fn token_position(&self, fallback: usize) -> usize;
}

#[derive(Default)]
struct NoDiagnostics;

impl DiagnosticSink for NoDiagnostics {
    const ENABLED: bool = false;

    #[inline(always)]
    fn record(&mut self, _kind: RepairKind, _position: usize) {}

    #[inline(always)]
    fn set_token_position(&mut self, _position: usize) {}

    #[inline(always)]
    fn token_position(&self, fallback: usize) -> usize {
        fallback
    }
}

#[derive(Default)]
struct RepairDiagnostics {
    events: Vec<RepairEvent>,
    token_position: usize,
}

impl DiagnosticSink for RepairDiagnostics {
    const ENABLED: bool = true;

    #[inline]
    fn record(&mut self, kind: RepairKind, position: usize) {
        self.events.push(RepairEvent { kind, position });
    }

    #[inline]
    fn set_token_position(&mut self, position: usize) {
        self.token_position = position;
    }

    #[inline]
    fn token_position(&self, _fallback: usize) -> usize {
        self.token_position
    }
}

#[derive(Debug, Clone, PartialEq)]
enum Token {
    LeftBrace,
    RightBrace,
    LeftBracket,
    RightBracket,
    Comma,
    Colon,
    Quoted(String),
    Bare(String),
    Number(String),
    Eof,
}

struct Lexer<'a, D> {
    input: &'a str,
    position: usize,
    diagnostics: D,
}

impl<'a, D: DiagnosticSink> Lexer<'a, D> {
    fn new(input: &'a str, diagnostics: D) -> Self {
        Self {
            input,
            position: 0,
            diagnostics,
        }
    }

    #[inline]
    fn current_char(&self) -> Option<char> {
        self.input.get(self.position..)?.chars().next()
    }

    #[inline]
    fn advance(&mut self) -> Option<char> {
        let ch = self.current_char()?;
        self.position += ch.len_utf8();
        Some(ch)
    }

    #[inline]
    fn starts_with(&self, value: &str) -> bool {
        self.input
            .get(self.position..)
            .is_some_and(|remaining| remaining.starts_with(value))
    }

    fn skip_ignored(&mut self) {
        loop {
            while self.current_char().is_some_and(char::is_whitespace) {
                self.advance();
            }

            if self.starts_with("//") {
                if D::ENABLED {
                    let comment_position = self.position;
                    self.diagnostics
                        .record(RepairKind::RemovedLineComment, comment_position);
                }
                while let Some(ch) = self.advance() {
                    if ch == '\n' {
                        break;
                    }
                }
            } else if self.starts_with("/*") {
                if D::ENABLED {
                    let comment_position = self.position;
                    self.diagnostics
                        .record(RepairKind::RemovedBlockComment, comment_position);
                }
                self.position += 2;
                while self.current_char().is_some() && !self.starts_with("*/") {
                    self.advance();
                }
                if self.starts_with("*/") {
                    self.position += 2;
                }
            } else {
                break;
            }
        }
    }

    fn read_hex_quad(&mut self) -> Option<u16> {
        let start = self.position;
        let mut value = 0_u16;

        for _ in 0..4 {
            let Some(ch) = self.advance() else {
                self.position = start;
                return None;
            };
            let Some(digit) = ch.to_digit(16) else {
                self.position = start;
                return None;
            };
            value = (value << 4) | digit as u16;
        }

        Some(value)
    }

    fn push_unicode_escape(&mut self, result: &mut String) {
        let escape_position = self.position.saturating_sub(2);
        let Some(first) = self.read_hex_quad() else {
            self.diagnostics
                .record(RepairKind::PreservedInvalidUnicodeEscape, escape_position);
            result.push_str("\\u");
            return;
        };

        if (0xD800..=0xDBFF).contains(&first) {
            let low_start = self.position;
            if self.starts_with("\\u") {
                self.position += 2;
                if let Some(second) = self.read_hex_quad() {
                    if (0xDC00..=0xDFFF).contains(&second) {
                        let codepoint =
                            0x1_0000 + (((first as u32 - 0xD800) << 10) | (second as u32 - 0xDC00));
                        if let Some(ch) = char::from_u32(codepoint) {
                            result.push(ch);
                            return;
                        }
                    }
                }
            }
            self.position = low_start;
            self.diagnostics
                .record(RepairKind::PreservedInvalidUnicodeEscape, escape_position);
        } else if !(0xDC00..=0xDFFF).contains(&first) {
            if let Some(ch) = char::from_u32(first as u32) {
                result.push(ch);
                return;
            }
        } else {
            self.diagnostics
                .record(RepairKind::PreservedInvalidUnicodeEscape, escape_position);
        }

        result.push_str("\\u");
        push_hex4(result, first);
    }

    fn read_string(&mut self, quote_char: char) -> String {
        let mut result = String::with_capacity(64);
        let string_position = self.position;
        if D::ENABLED && quote_char == '\'' {
            self.diagnostics
                .record(RepairKind::ConvertedSingleQuotedString, string_position);
        }
        self.advance();
        let mut closed = !D::ENABLED;

        while let Some(ch) = self.advance() {
            if ch == quote_char {
                let previous_is_word = result
                    .chars()
                    .next_back()
                    .is_some_and(char::is_alphanumeric);
                let next_is_word = self.current_char().is_some_and(char::is_alphanumeric);

                if quote_char == '\'' && previous_is_word && next_is_word {
                    result.push(ch);
                    continue;
                }
                if D::ENABLED {
                    closed = true;
                }
                break;
            }

            if ch != '\\' {
                result.push(ch);
                continue;
            }

            let escape_position = self.position.saturating_sub(1);
            match self.advance() {
                Some('n') => result.push('\n'),
                Some('r') => result.push('\r'),
                Some('t') => result.push('\t'),
                Some('b') => result.push('\u{0008}'),
                Some('f') => result.push('\u{000C}'),
                Some('"') => result.push('"'),
                Some('\'') => result.push('\''),
                Some('\\') => result.push('\\'),
                Some('/') => result.push('/'),
                Some('u') => self.push_unicode_escape(&mut result),
                Some(escaped) => {
                    if D::ENABLED {
                        self.diagnostics
                            .record(RepairKind::RemovedInvalidEscape, escape_position);
                    }
                    result.push(escaped);
                }
                None => {
                    if D::ENABLED {
                        self.diagnostics
                            .record(RepairKind::RemovedInvalidEscape, escape_position);
                    }
                    result.push('\\');
                }
            }
        }

        if D::ENABLED && !closed {
            self.diagnostics
                .record(RepairKind::ClosedUnterminatedString, self.position);
        }

        result
    }

    fn read_bare(&mut self) -> String {
        let mut result = String::with_capacity(32);
        let mut url_mode = false;

        while let Some(ch) = self.current_char() {
            if ch == ',' || ch == '}' || ch == ']' || ch.is_whitespace() {
                break;
            }
            if ch == ':' && !url_mode {
                if matches!(result.as_str(), "http" | "https" | "ftp" | "file") {
                    url_mode = true;
                } else {
                    break;
                }
            }
            result.push(ch);
            self.advance();
        }

        result
    }

    fn read_number(&mut self) -> String {
        let start = self.position;

        if self.current_char() == Some('-') {
            self.advance();
        }
        while self.current_char().is_some_and(|ch| ch.is_ascii_digit()) {
            self.advance();
        }
        if self.current_char() == Some('.') {
            self.advance();
            while self.current_char().is_some_and(|ch| ch.is_ascii_digit()) {
                self.advance();
            }
        }
        if self.current_char().is_some_and(|ch| ch == 'e' || ch == 'E') {
            self.advance();
            if self.current_char().is_some_and(|ch| ch == '+' || ch == '-') {
                self.advance();
            }
            while self.current_char().is_some_and(|ch| ch.is_ascii_digit()) {
                self.advance();
            }
        }

        self.input[start..self.position].to_owned()
    }

    fn next_token(&mut self) -> Token {
        self.skip_ignored();
        if D::ENABLED {
            self.diagnostics.set_token_position(self.position);
        }

        match self.current_char() {
            None => Token::Eof,
            Some('{') => {
                self.advance();
                Token::LeftBrace
            }
            Some('}') => {
                self.advance();
                Token::RightBrace
            }
            Some('[') => {
                self.advance();
                Token::LeftBracket
            }
            Some(']') => {
                self.advance();
                Token::RightBracket
            }
            Some(',') => {
                self.advance();
                Token::Comma
            }
            Some(':') => {
                self.advance();
                Token::Colon
            }
            Some('"') => Token::Quoted(self.read_string('"')),
            Some('\'') => Token::Quoted(self.read_string('\'')),
            Some('-') | Some('0'..='9') => Token::Number(self.read_number()),
            Some(_) => Token::Bare(self.read_bare()),
        }
    }
}

struct Parser<'a, D> {
    lexer: Lexer<'a, D>,
    current_token: Token,
    depth: usize,
    max_depth: usize,
}

impl<'a, D: DiagnosticSink> Parser<'a, D> {
    fn new(input: &'a str, diagnostics: D) -> Self {
        let mut lexer = Lexer::new(input, diagnostics);
        let current_token = lexer.next_token();
        Self {
            lexer,
            current_token,
            depth: 0,
            max_depth: 1000,
        }
    }

    #[inline(always)]
    fn record(&mut self, kind: RepairKind) {
        let position = self.lexer.diagnostics.token_position(self.lexer.position);
        self.lexer.diagnostics.record(kind, position);
    }

    fn into_diagnostics(self) -> D {
        self.lexer.diagnostics
    }

    #[inline]
    fn advance(&mut self) {
        self.current_token = self.lexer.next_token();
    }

    fn parse(&mut self) -> Result<serde_json::Value, String> {
        let first_token = self.current_token.clone();
        let first_position = if D::ENABLED {
            self.lexer.diagnostics.token_position(self.lexer.position)
        } else {
            0
        };
        let mut found_container =
            matches!(self.current_token, Token::LeftBrace | Token::LeftBracket);

        while !found_container && self.current_token != Token::Eof {
            self.advance();
            found_container = matches!(self.current_token, Token::LeftBrace | Token::LeftBracket);
        }

        let first_value = if found_container {
            if D::ENABLED && !matches!(first_token, Token::LeftBrace | Token::LeftBracket) {
                self.lexer
                    .diagnostics
                    .record(RepairKind::SkippedLeadingContent, first_position);
            }
            self.parse_value()?
        } else {
            if D::ENABLED {
                self.lexer.diagnostics.set_token_position(first_position);
            }
            self.value_from_token(first_token)
        };

        let mut values = vec![first_value];
        let mut logged_skipped_content = false;
        while self.current_token != Token::Eof {
            if matches!(self.current_token, Token::LeftBrace | Token::LeftBracket) {
                if D::ENABLED {
                    self.record(RepairKind::CombinedMultipleRootValues);
                }
                values.push(self.parse_value()?);
            } else {
                if D::ENABLED && !logged_skipped_content {
                    self.record(RepairKind::SkippedTrailingContent);
                    logged_skipped_content = true;
                }
                self.advance();
            }
        }

        if values.len() == 1 {
            Ok(values.pop().expect("one parsed value"))
        } else {
            Ok(serde_json::Value::Array(values))
        }
    }

    fn value_from_token(&mut self, token: Token) -> serde_json::Value {
        match token {
            Token::Quoted(value) => serde_json::Value::String(value),
            Token::Bare(value) => {
                if D::ENABLED {
                    self.record_bare_value(&value);
                }
                bare_value(value)
            }
            Token::Number(value) => {
                if D::ENABLED {
                    self.record_number_value(&value);
                }
                number_value(&value)
            }
            _ => {
                if D::ENABLED {
                    self.record(RepairKind::ReplacedUnexpectedToken);
                }
                serde_json::Value::Null
            }
        }
    }

    fn record_bare_value(&mut self, value: &str) {
        match value {
            "true" | "false" | "null" => {}
            "True" | "False" | "None" => self.record(RepairKind::ConvertedPythonLiteral),
            _ => match normalize_number(value) {
                Some(normalized) if normalized != value => {
                    self.record(RepairKind::NormalizedInvalidNumber);
                }
                Some(_) => {}
                None => self.record(RepairKind::QuotedUnquotedValue),
            },
        }
    }

    fn record_number_value(&mut self, value: &str) {
        match normalize_number(value) {
            Some(normalized) if normalized != value => {
                self.record(RepairKind::NormalizedInvalidNumber);
            }
            Some(_) => {}
            None => self.record(RepairKind::ReplacedInvalidNumber),
        }
    }

    fn parse_value(&mut self) -> Result<serde_json::Value, String> {
        match self.current_token.clone() {
            Token::LeftBrace => self.parse_object(),
            Token::LeftBracket => self.parse_array(),
            Token::Quoted(value) => {
                self.advance();
                Ok(serde_json::Value::String(value))
            }
            Token::Bare(value) => {
                if D::ENABLED {
                    self.record_bare_value(&value);
                }
                self.advance();
                Ok(bare_value(value))
            }
            Token::Number(value) => {
                if D::ENABLED {
                    self.record_number_value(&value);
                }
                self.advance();
                Ok(number_value(&value))
            }
            Token::Eof => {
                if D::ENABLED {
                    self.record(RepairKind::InsertedMissingValue);
                }
                Ok(serde_json::Value::Null)
            }
            _ => {
                if D::ENABLED {
                    self.record(RepairKind::ReplacedUnexpectedToken);
                }
                self.advance();
                Ok(serde_json::Value::Null)
            }
        }
    }

    fn enter_container(&mut self) -> Result<(), String> {
        if self.depth >= self.max_depth {
            if D::ENABLED {
                self.record(RepairKind::MaximumDepthExceeded);
            }
            return Err("Maximum nesting depth exceeded".to_owned());
        }
        self.depth += 1;
        Ok(())
    }

    fn parse_object(&mut self) -> Result<serde_json::Value, String> {
        if D::ENABLED {
            self.parse_object_with_diagnostics()
        } else {
            self.parse_object_fast()
        }
    }

    fn parse_object_fast(&mut self) -> Result<serde_json::Value, String> {
        self.enter_container()?;
        let mut object = serde_json::Map::new();
        self.advance();

        while self.current_token == Token::Comma {
            self.advance();
        }

        while !matches!(
            self.current_token,
            Token::RightBrace | Token::RightBracket | Token::Eof
        ) {
            let key = match self.current_token.clone() {
                Token::Quoted(key) | Token::Bare(key) | Token::Number(key) => {
                    self.advance();
                    key
                }
                Token::Comma => {
                    self.advance();
                    continue;
                }
                _ => {
                    self.advance();
                    continue;
                }
            };

            if self.current_token == Token::Colon {
                self.advance();
            }

            let value = self.parse_value()?;
            object.insert(key, value);

            while self.current_token == Token::Comma {
                self.advance();
            }
        }

        if self.current_token == Token::RightBrace {
            self.advance();
        }
        self.depth -= 1;
        Ok(serde_json::Value::Object(object))
    }

    fn parse_object_with_diagnostics(&mut self) -> Result<serde_json::Value, String> {
        self.enter_container()?;
        let mut object = serde_json::Map::new();
        self.advance();

        while self.current_token == Token::Comma {
            self.record(RepairKind::RemovedExtraComma);
            self.advance();
        }

        while !matches!(
            self.current_token,
            Token::RightBrace | Token::RightBracket | Token::Eof
        ) {
            let key = match self.current_token.clone() {
                Token::Quoted(key) => {
                    self.advance();
                    key
                }
                Token::Bare(key) | Token::Number(key) => {
                    self.record(RepairKind::QuotedUnquotedKey);
                    self.advance();
                    key
                }
                Token::Comma => {
                    self.record(RepairKind::RemovedExtraComma);
                    self.advance();
                    continue;
                }
                _ => {
                    self.record(RepairKind::ReplacedUnexpectedToken);
                    self.advance();
                    continue;
                }
            };

            if self.current_token == Token::Colon {
                self.advance();
            } else {
                self.record(RepairKind::InsertedMissingColon);
            }

            let value = if matches!(
                self.current_token,
                Token::RightBrace | Token::RightBracket | Token::Eof
            ) {
                self.record(RepairKind::InsertedMissingValue);
                if self.current_token != Token::Eof {
                    self.advance();
                }
                serde_json::Value::Null
            } else {
                self.parse_value()?
            };
            object.insert(key, value);

            if self.current_token == Token::Comma {
                let separator_position = self.lexer.diagnostics.token_position(self.lexer.position);
                self.advance();
                while self.current_token == Token::Comma {
                    self.record(RepairKind::RemovedExtraComma);
                    self.advance();
                }
                if matches!(
                    self.current_token,
                    Token::RightBrace | Token::RightBracket | Token::Eof
                ) {
                    self.lexer
                        .diagnostics
                        .record(RepairKind::RemovedTrailingComma, separator_position);
                }
            } else if !matches!(
                self.current_token,
                Token::RightBrace | Token::RightBracket | Token::Eof
            ) {
                self.record(RepairKind::InsertedMissingComma);
            }
        }

        match self.current_token {
            Token::RightBrace => self.advance(),
            Token::RightBracket => {
                self.record(RepairKind::ReplacedMismatchedObjectCloser);
            }
            Token::Eof => self.record(RepairKind::InsertedMissingObjectCloser),
            _ => {}
        }
        self.depth -= 1;
        Ok(serde_json::Value::Object(object))
    }

    fn parse_array(&mut self) -> Result<serde_json::Value, String> {
        if D::ENABLED {
            self.parse_array_with_diagnostics()
        } else {
            self.parse_array_fast()
        }
    }

    fn parse_array_fast(&mut self) -> Result<serde_json::Value, String> {
        self.enter_container()?;
        let mut array = Vec::new();
        self.advance();

        while self.current_token == Token::Comma {
            self.advance();
        }

        while !matches!(
            self.current_token,
            Token::RightBracket | Token::RightBrace | Token::Eof
        ) {
            if self.current_token == Token::Comma {
                self.advance();
                continue;
            }

            array.push(self.parse_value()?);
            while self.current_token == Token::Comma {
                self.advance();
            }
        }

        if self.current_token == Token::RightBracket {
            self.advance();
        }
        self.depth -= 1;
        Ok(serde_json::Value::Array(array))
    }

    fn parse_array_with_diagnostics(&mut self) -> Result<serde_json::Value, String> {
        self.enter_container()?;
        let mut array = Vec::new();
        self.advance();

        while self.current_token == Token::Comma {
            self.record(RepairKind::RemovedExtraComma);
            self.advance();
        }

        while !matches!(
            self.current_token,
            Token::RightBracket | Token::RightBrace | Token::Eof
        ) {
            if self.current_token == Token::Comma {
                self.record(RepairKind::RemovedExtraComma);
                self.advance();
                continue;
            }

            array.push(self.parse_value()?);
            if self.current_token == Token::Comma {
                let separator_position = self.lexer.diagnostics.token_position(self.lexer.position);
                self.advance();
                while self.current_token == Token::Comma {
                    self.record(RepairKind::RemovedExtraComma);
                    self.advance();
                }
                if matches!(
                    self.current_token,
                    Token::RightBracket | Token::RightBrace | Token::Eof
                ) {
                    self.lexer
                        .diagnostics
                        .record(RepairKind::RemovedTrailingComma, separator_position);
                }
            } else if !matches!(
                self.current_token,
                Token::RightBracket | Token::RightBrace | Token::Eof
            ) {
                self.record(RepairKind::InsertedMissingComma);
            }
        }

        match self.current_token {
            Token::RightBracket => self.advance(),
            Token::RightBrace => {
                self.record(RepairKind::ReplacedMismatchedArrayCloser);
            }
            Token::Eof => self.record(RepairKind::InsertedMissingArrayCloser),
            _ => {}
        }
        self.depth -= 1;
        Ok(serde_json::Value::Array(array))
    }
}

fn bare_value(value: String) -> serde_json::Value {
    match value.as_str() {
        "true" | "True" => serde_json::Value::Bool(true),
        "false" | "False" => serde_json::Value::Bool(false),
        "null" | "None" => serde_json::Value::Null,
        _ => normalize_number(&value)
            .map(serde_json::Number::from_string_unchecked)
            .map(serde_json::Value::Number)
            .unwrap_or(serde_json::Value::String(value)),
    }
}

fn normalize_number(raw: &str) -> Option<String> {
    if raw.is_empty() {
        return None;
    }

    let (negative, unsigned) = if let Some(value) = raw.strip_prefix('-') {
        (true, value)
    } else if let Some(value) = raw.strip_prefix('+') {
        (false, value)
    } else {
        (false, raw)
    };

    let exponent_index = unsigned.find(['e', 'E']);
    let (mantissa, exponent) = match exponent_index {
        Some(index) => {
            if unsigned[index + 1..].contains(['e', 'E']) {
                return None;
            }
            (&unsigned[..index], Some(&unsigned[index + 1..]))
        }
        None => (unsigned, None),
    };

    if let Some(exponent) = exponent {
        let digits = exponent.strip_prefix(['+', '-']).unwrap_or(exponent);
        if digits.is_empty() || !digits.chars().all(|ch| ch.is_ascii_digit()) {
            return None;
        }
    }

    let mut mantissa_parts = mantissa.split('.');
    let integer = mantissa_parts.next().unwrap_or_default();
    let fraction = mantissa_parts.next();
    if mantissa_parts.next().is_some() {
        return None;
    }
    if integer.is_empty() && fraction.is_none_or(str::is_empty) {
        return None;
    }
    if !integer.chars().all(|ch| ch.is_ascii_digit())
        || fraction.is_some_and(|value| !value.chars().all(|ch| ch.is_ascii_digit()))
    {
        return None;
    }

    let integer = integer.trim_start_matches('0');
    let integer = if integer.is_empty() { "0" } else { integer };
    let mut normalized = String::with_capacity(raw.len() + 2);
    if negative {
        normalized.push('-');
    }
    normalized.push_str(integer);
    if let Some(fraction) = fraction {
        normalized.push('.');
        normalized.push_str(if fraction.is_empty() { "0" } else { fraction });
    }
    if let Some(exponent) = exponent {
        normalized.push('e');
        normalized.push_str(exponent);
    }

    if (fraction.is_some() || exponent.is_some())
        && !normalized.parse::<f64>().ok().is_some_and(f64::is_finite)
    {
        return None;
    }

    Some(normalized)
}

fn number_value(raw: &str) -> serde_json::Value {
    normalize_number(raw)
        .map(serde_json::Number::from_string_unchecked)
        .map(serde_json::Value::Number)
        .unwrap_or(serde_json::Value::Null)
}

#[inline]
fn push_hex4(output: &mut String, value: u16) {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    output.push(HEX[((value >> 12) & 0xF) as usize] as char);
    output.push(HEX[((value >> 8) & 0xF) as usize] as char);
    output.push(HEX[((value >> 4) & 0xF) as usize] as char);
    output.push(HEX[(value & 0xF) as usize] as char);
}

#[inline]
fn push_unicode_escape(output: &mut String, value: u16) {
    output.push_str("\\u");
    push_hex4(output, value);
}

fn write_escaped_string(output: &mut String, value: &str, ensure_ascii: bool) {
    for ch in value.chars() {
        match ch {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            '\u{0008}' => output.push_str("\\b"),
            '\u{000C}' => output.push_str("\\f"),
            ch if ensure_ascii && !ch.is_ascii() => {
                let mut units = [0_u16; 2];
                for unit in ch.encode_utf16(&mut units) {
                    push_unicode_escape(output, *unit);
                }
            }
            ch if ch.is_control() => push_unicode_escape(output, ch as u16),
            ch => output.push(ch),
        }
    }
}

fn write_indent(output: &mut String, count: usize) {
    output.extend(std::iter::repeat_n(' ', count));
}

fn write_json_value(
    output: &mut String,
    value: &serde_json::Value,
    ensure_ascii: bool,
    indent: usize,
    current_indent: usize,
) {
    match value {
        serde_json::Value::Null => output.push_str("null"),
        serde_json::Value::Bool(value) => {
            output.push_str(if *value { "true" } else { "false" });
        }
        serde_json::Value::Number(value) => output.push_str(value.as_str()),
        serde_json::Value::String(value) => {
            output.push('"');
            write_escaped_string(output, value, ensure_ascii);
            output.push('"');
        }
        serde_json::Value::Array(values) => {
            if values.is_empty() {
                output.push_str("[]");
                return;
            }

            output.push('[');
            let inner_indent = current_indent.saturating_add(indent);
            if indent > 0 {
                output.push('\n');
            }
            for (index, value) in values.iter().enumerate() {
                if indent > 0 {
                    write_indent(output, inner_indent);
                }
                write_json_value(output, value, ensure_ascii, indent, inner_indent);
                if index + 1 < values.len() {
                    output.push(',');
                }
                if indent > 0 {
                    output.push('\n');
                }
            }
            if indent > 0 {
                write_indent(output, current_indent);
            }
            output.push(']');
        }
        serde_json::Value::Object(values) => {
            if values.is_empty() {
                output.push_str("{}");
                return;
            }

            output.push('{');
            let inner_indent = current_indent.saturating_add(indent);
            if indent > 0 {
                output.push('\n');
            }
            for (index, (key, value)) in values.iter().enumerate() {
                if indent > 0 {
                    write_indent(output, inner_indent);
                }
                output.push('"');
                write_escaped_string(output, key, ensure_ascii);
                output.push('"');
                output.push(':');
                if indent > 0 {
                    output.push(' ');
                }
                write_json_value(output, value, ensure_ascii, indent, inner_indent);
                if index + 1 < values.len() {
                    output.push(',');
                }
                if indent > 0 {
                    output.push('\n');
                }
            }
            if indent > 0 {
                write_indent(output, current_indent);
            }
            output.push('}');
        }
    }
}

fn format_json_value(
    value: &serde_json::Value,
    ensure_ascii: bool,
    indent: usize,
    capacity: usize,
) -> String {
    let mut output = String::with_capacity(capacity);
    write_json_value(&mut output, value, ensure_ascii, indent, 0);
    output
}

fn value_to_python(py: Python<'_>, value: &serde_json::Value) -> PyResult<Py<PyAny>> {
    match value {
        serde_json::Value::Null => Ok(py.None()),
        serde_json::Value::Bool(value) => value.into_py_any(py),
        serde_json::Value::Number(value) => {
            let raw = value.as_str();
            if !raw.contains(['.', 'e', 'E']) {
                if let Some(value) = value.as_i128() {
                    return value.into_py_any(py);
                }
                if let Some(value) = value.as_u128() {
                    return value.into_py_any(py);
                }
                return Ok(PyModule::import(py, "builtins")?
                    .getattr("int")?
                    .call1((raw,))?
                    .unbind());
            }
            raw.parse::<f64>()
                .map_err(|error| PyValueError::new_err(error.to_string()))?
                .into_py_any(py)
        }
        serde_json::Value::String(value) => value.as_str().into_py_any(py),
        serde_json::Value::Array(values) => {
            let output = PyList::empty(py);
            for value in values {
                output.append(value_to_python(py, value)?)?;
            }
            Ok(output.into_any().unbind())
        }
        serde_json::Value::Object(values) => {
            let output = PyDict::new(py);
            for (key, value) in values {
                output.set_item(key, value_to_python(py, value)?)?;
            }
            Ok(output.into_any().unbind())
        }
    }
}

fn parse_repaired(json_string: &str) -> Result<serde_json::Value, String> {
    Parser::new(json_string, NoDiagnostics).parse()
}

fn parse_repaired_with_diagnostics(json_string: &str) -> (serde_json::Value, Vec<RepairEvent>) {
    let mut parser = Parser::new(json_string, RepairDiagnostics::default());
    let value = parser.parse().unwrap_or(serde_json::Value::Null);
    let diagnostics = parser.into_diagnostics();
    (value, diagnostics.events)
}

fn nearest_char_boundary(json_string: &str, position: usize) -> usize {
    let mut position = position.min(json_string.len());
    while position > 0 && !json_string.is_char_boundary(position) {
        position -= 1;
    }
    position
}

fn context_window(json_string: &str, position: usize) -> &str {
    let position = nearest_char_boundary(json_string, position);
    let mut start = position.saturating_sub(20);
    while start < position && !json_string.is_char_boundary(start) {
        start += 1;
    }
    let mut end = position.saturating_add(20).min(json_string.len());
    while end > position && !json_string.is_char_boundary(end) {
        end -= 1;
    }
    &json_string[start..end]
}

fn repair_event_locations(json_string: &str, events: &[RepairEvent]) -> Vec<(usize, usize)> {
    let mut order: Vec<usize> = (0..events.len()).collect();
    order.sort_unstable_by_key(|index| events[*index].position);

    let mut locations = vec![(1, 1); events.len()];
    let mut cursor = 0;
    let mut line = 1;
    let mut column = 1;

    for index in order {
        let target = nearest_char_boundary(json_string, events[index].position);
        for ch in json_string[cursor..target].chars() {
            if ch == '\n' {
                line += 1;
                column = 1;
            } else {
                column += 1;
            }
        }
        cursor = target;
        locations[index] = (line, column);
    }

    locations
}

fn repair_events_to_python(
    py: Python<'_>,
    json_string: &str,
    events: &[RepairEvent],
) -> PyResult<Py<PyAny>> {
    let locations = repair_event_locations(json_string, events);
    let output = PyList::empty(py);

    for (event, (line, column)) in events.iter().zip(locations) {
        let item = PyDict::new(py);
        item.set_item("type", event.kind.code())?;
        item.set_item("text", event.kind.text())?;
        item.set_item("context", context_window(json_string, event.position))?;
        item.set_item("position", event.position)?;
        item.set_item("line", line)?;
        item.set_item("column", column)?;
        output.append(item)?;
    }

    Ok(output.into_any().unbind())
}

fn contains_wide_integer(json_string: &str) -> bool {
    let bytes = json_string.as_bytes();
    let mut index = 0;
    let mut in_string = false;
    let mut escaped = false;

    while index < bytes.len() {
        let byte = bytes[index];
        if in_string {
            if escaped {
                escaped = false;
            } else if byte == b'\\' {
                escaped = true;
            } else if byte == b'"' {
                in_string = false;
            }
            index += 1;
            continue;
        }
        if byte == b'"' {
            in_string = true;
            index += 1;
            continue;
        }

        if byte == b'-' || byte.is_ascii_digit() {
            let start = index;
            if byte == b'-' {
                index += 1;
            }
            let digit_start = index;
            while index < bytes.len() && bytes[index].is_ascii_digit() {
                index += 1;
            }
            if digit_start == index {
                continue;
            }
            if index < bytes.len() && bytes[index] == b'.' {
                index += 1;
                while index < bytes.len() && bytes[index].is_ascii_digit() {
                    index += 1;
                }
            }
            if index < bytes.len() && matches!(bytes[index], b'e' | b'E') {
                index += 1;
                if index < bytes.len() && matches!(bytes[index], b'+' | b'-') {
                    index += 1;
                }
                while index < bytes.len() && bytes[index].is_ascii_digit() {
                    index += 1;
                }
            }
            if bytes[start..index]
                .iter()
                .any(|byte| matches!(byte, b'.' | b'e' | b'E'))
            {
                continue;
            }

            let raw = &json_string[start..index];
            if (raw.starts_with('-') && raw.parse::<i64>().is_err())
                || (!raw.starts_with('-') && raw.parse::<u64>().is_err())
            {
                return true;
            }
            continue;
        }
        index += 1;
    }

    false
}

#[pyfunction]
fn _has_wide_integer(json_string: &str) -> bool {
    contains_wide_integer(json_string)
}

#[pyfunction]
fn _escape_non_ascii_json(py: Python<'_>, json_bytes: &[u8]) -> PyResult<String> {
    let json_string = std::str::from_utf8(json_bytes)
        .map_err(|error| PyValueError::new_err(error.to_string()))?;
    Ok(py.detach(|| {
        let mut output = String::with_capacity(json_string.len());
        for ch in json_string.chars() {
            if ch.is_ascii() {
                output.push(ch);
            } else {
                let mut units = [0_u16; 2];
                for unit in ch.encode_utf16(&mut units) {
                    push_unicode_escape(&mut output, *unit);
                }
            }
        }
        output
    }))
}

#[pyfunction]
fn _repair_json_rust(
    py: Python<'_>,
    json_string: &str,
    ensure_ascii: bool,
    indent: usize,
) -> String {
    py.detach(|| match parse_repaired(json_string) {
        Ok(value) => format_json_value(&value, ensure_ascii, indent, json_string.len()),
        Err(_) => "null".to_owned(),
    })
}

#[pyfunction]
fn _repair_json_obj_rust(py: Python<'_>, json_string: &str) -> PyResult<Py<PyAny>> {
    let value = py
        .detach(|| parse_repaired(json_string))
        .unwrap_or(serde_json::Value::Null);
    value_to_python(py, &value)
}

#[pyfunction]
fn _repair_json_obj_with_log_rust(
    py: Python<'_>,
    json_string: &str,
) -> PyResult<(Py<PyAny>, Py<PyAny>)> {
    let (value, events) = py.detach(|| parse_repaired_with_diagnostics(json_string));
    let value = value_to_python(py, &value)?;
    let log = repair_events_to_python(py, json_string, &events)?;
    Ok((value, log))
}

#[pymodule]
fn _fast_json_repair(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(_repair_json_rust, module)?)?;
    module.add_function(wrap_pyfunction!(_repair_json_obj_rust, module)?)?;
    module.add_function(wrap_pyfunction!(_repair_json_obj_with_log_rust, module)?)?;
    module.add_function(wrap_pyfunction!(_escape_non_ascii_json, module)?)?;
    module.add_function(wrap_pyfunction!(_has_wide_integer, module)?)?;
    Ok(())
}
