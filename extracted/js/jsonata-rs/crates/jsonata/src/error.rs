//! Port of `com.dashjoin.jsonata.JException`.

use crate::value::JValue;
use std::fmt;

/// A JSONata exception carrying an error code (e.g. "S0201"), a character
/// location, and optional `current`/`expected` tokens.
#[derive(Debug, Clone)]
pub struct JError {
    pub error: String,
    pub location: i32,
    pub current: Option<JValue>,
    pub expected: Option<JValue>,
    /// Parser recovery bookkeeping (Tokenizer remaining tokens) is not modelled
    /// here yet; `error_type` mirrors `JException.type`.
    pub error_type: Option<String>,
}

impl JError {
    pub fn new(error: &str) -> JError {
        JError {
            error: error.to_string(),
            location: -1,
            current: None,
            expected: None,
            error_type: None,
        }
    }

    pub fn at(error: &str, location: i32) -> JError {
        JError {
            error: error.to_string(),
            location,
            current: None,
            expected: None,
            error_type: None,
        }
    }

    pub fn with_current(error: &str, location: i32, current: JValue) -> JError {
        JError {
            error: error.to_string(),
            location,
            current: Some(current),
            expected: None,
            error_type: None,
        }
    }

    pub fn with_current_expected(
        error: &str,
        location: i32,
        current: JValue,
        expected: JValue,
    ) -> JError {
        JError {
            error: error.to_string(),
            location,
            current: Some(current),
            expected: Some(expected),
            error_type: None,
        }
    }

    /// Returns the error code, e.g. "S0201".
    pub fn code(&self) -> &str {
        &self.error
    }

    /// Generate the error message from the error code (see `JException.msg`).
    pub fn message(&self) -> String {
        msg(
            &self.error,
            self.location,
            self.current.as_ref(),
            self.expected.as_ref(),
            false,
        )
    }

    pub fn detailed_message(&self) -> String {
        msg(
            &self.error,
            self.location,
            self.current.as_ref(),
            self.expected.as_ref(),
            true,
        )
    }
}

impl fmt::Display for JError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message())
    }
}

impl std::error::Error for JError {}

pub type JResult<T> = Result<T, JError>;

/// Render an argument the way Java `String.valueOf`/string concatenation would
/// for the error-message substitution.
fn arg_to_string(arg: Option<&JValue>) -> String {
    match arg {
        None => "null".to_string(),
        Some(v) => v.error_arg_string(),
    }
}

/// Port of `JException.msg`.
pub fn msg(
    error: &str,
    location: i32,
    arg1: Option<&JValue>,
    arg2: Option<&JValue>,
    details: bool,
) -> String {
    let message = crate::errors::error_code_message(error);

    let message = match message {
        None => {
            return format!(
                "JSonataException {}{}",
                error,
                if details {
                    format!(
                        " {{code=unknown position={} arg1={} arg2={}}}",
                        location,
                        arg_to_string(arg1),
                        arg_to_string(arg2)
                    )
                } else {
                    String::new()
                }
            );
        }
        Some(m) => m,
    };

    if message == "{{{message}}}" {
        return arg_to_string(arg1);
    }

    // Replace first {{var}} with "%1$s"-style and second with "%2$s", then
    // substitute. We emulate Java's String.format("\"%1$s\"", arg1).
    let mut formatted = replace_first_braces(message, &format!("\"{}\"", arg_to_string(arg1)));
    formatted = replace_first_braces(&formatted, &format!("\"{}\"", arg_to_string(arg2)));

    if details {
        let mut s = format!("{} {{code={}", formatted, error);
        if location >= 0 {
            s.push_str(&format!(" position={}", location));
        }
        s.push('}');
        s
    } else {
        formatted
    }
}

/// Replace the first `{{word}}` occurrence with the replacement.
fn replace_first_braces(s: &str, replacement: &str) -> String {
    // matches \{\{\w+\}\} — like Java's `replaceFirst`, keep scanning past
    // candidates that don't satisfy \w+ (e.g. the leading `{{` of `${{{token}}}`).
    let mut from = 0;
    while let Some(rel) = s[from..].find("{{") {
        let start = from + rel;
        let rest = &s[start + 2..];
        if let Some(we) = rest.find("}}") {
            let word = &rest[..we];
            if !word.is_empty() && word.chars().all(|c| c.is_alphanumeric() || c == '_') {
                let end = start + 2 + we + 2;
                return format!("{}{}{}", &s[..start], replacement, &s[end..]);
            }
        }
        from = start + 1;
    }
    s.to_string()
}
