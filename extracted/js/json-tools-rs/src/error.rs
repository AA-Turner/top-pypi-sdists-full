use crate::json_parser;

/// Comprehensive error type for all JSON Tools operations with detailed information and suggestions
///
/// Each error variant includes:
/// - Machine-readable error code (E001-E008) for programmatic handling
/// - Human-readable message
/// - Actionable suggestion
/// - Source error (where applicable)
#[derive(Debug)]
#[non_exhaustive]
pub enum JsonToolsError {
    /// Error parsing JSON input with detailed context and suggestions
    JsonParseError {
        message: String,
        suggestion: String,
        source: json_parser::JsonError,
    },

    /// Error compiling or using regex patterns with helpful suggestions
    RegexError {
        message: String,
        suggestion: String,
        source: regex::Error,
    },

    /// Invalid replacement pattern configuration with detailed guidance
    InvalidReplacementPattern { message: String, suggestion: String },

    /// Invalid JSON structure for the requested operation
    InvalidJsonStructure { message: String, suggestion: String },

    /// Configuration error when operation mode is not set
    ConfigurationError { message: String, suggestion: String },

    /// Error processing batch item with detailed context
    BatchProcessingError {
        index: usize,
        message: String,
        suggestion: String,
        source: Box<JsonToolsError>,
    },

    /// Input validation error with helpful guidance
    InputValidationError { message: String, suggestion: String },

    /// Serialization error when converting results back to JSON
    SerializationError {
        message: String,
        suggestion: String,
        source: json_parser::JsonError,
    },
}

impl std::fmt::Display for JsonToolsError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::JsonParseError {
                message,
                suggestion,
                ..
            } => {
                write!(
                    f,
                    "[E001] JSON parsing failed: {message}\n\u{1f4a1} Suggestion: {suggestion}"
                )
            }
            Self::RegexError {
                message,
                suggestion,
                ..
            } => {
                write!(
                    f,
                    "[E002] Regex pattern error: {message}\n\u{1f4a1} Suggestion: {suggestion}"
                )
            }
            Self::InvalidReplacementPattern {
                message,
                suggestion,
            } => {
                write!(f, "[E003] Invalid replacement pattern: {message}\n\u{1f4a1} Suggestion: {suggestion}")
            }
            Self::InvalidJsonStructure {
                message,
                suggestion,
            } => {
                write!(
                    f,
                    "[E004] Invalid JSON structure: {message}\n\u{1f4a1} Suggestion: {suggestion}"
                )
            }
            Self::ConfigurationError {
                message,
                suggestion,
            } => {
                write!(f, "[E005] Operation mode not configured: {message}\n\u{1f4a1} Suggestion: {suggestion}")
            }
            Self::BatchProcessingError {
                index,
                message,
                suggestion,
                ..
            } => {
                write!(f, "[E006] Batch processing failed at index {index}: {message}\n\u{1f4a1} Suggestion: {suggestion}")
            }
            Self::InputValidationError {
                message,
                suggestion,
            } => {
                write!(
                    f,
                    "[E007] Input validation failed: {message}\n\u{1f4a1} Suggestion: {suggestion}"
                )
            }
            Self::SerializationError {
                message,
                suggestion,
                ..
            } => {
                write!(f, "[E008] JSON serialization failed: {message}\n\u{1f4a1} Suggestion: {suggestion}")
            }
        }
    }
}

impl std::error::Error for JsonToolsError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::JsonParseError { source, .. } => Some(source),
            Self::RegexError { source, .. } => Some(source),
            Self::BatchProcessingError { source, .. } => Some(source.as_ref()),
            Self::SerializationError { source, .. } => Some(source),
            _ => None,
        }
    }
}

impl JsonToolsError {
    /// Get machine-readable error code for programmatic handling
    ///
    /// # Examples
    /// ```
    /// use json_tools_rs::{JSONTools, JsonToolsError};
    ///
    /// let result = JSONTools::new().flatten().execute("invalid json");
    /// if let Err(e) = result {
    ///     match e.error_code() {
    ///         "E001" => println!("JSON parsing error"),
    ///         "E005" => println!("Configuration error"),
    ///         _ => println!("Other error"),
    ///     }
    /// }
    /// ```
    pub fn error_code(&self) -> &'static str {
        match self {
            JsonToolsError::JsonParseError { .. } => "E001",
            JsonToolsError::RegexError { .. } => "E002",
            JsonToolsError::InvalidReplacementPattern { .. } => "E003",
            JsonToolsError::InvalidJsonStructure { .. } => "E004",
            JsonToolsError::ConfigurationError { .. } => "E005",
            JsonToolsError::BatchProcessingError { .. } => "E006",
            JsonToolsError::InputValidationError { .. } => "E007",
            JsonToolsError::SerializationError { .. } => "E008",
        }
    }

    /// Create a JSON parse error with helpful suggestions
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn json_parse_error(source: json_parser::JsonError) -> Self {
        let suggestion = "Verify your JSON syntax using a JSON validator. Common issues include: missing quotes around keys or values, trailing commas, unescaped characters, incomplete JSON (missing closing braces or brackets), or invalid escape sequences.";

        JsonToolsError::JsonParseError {
            message: source.to_string(),
            suggestion: suggestion.into(),
            source,
        }
    }

    /// Create a regex error with helpful suggestions
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn regex_error(source: regex::Error) -> Self {
        let suggestion = match source {
            regex::Error::Syntax(_) =>
                "Check your regex pattern syntax. Use online regex testers to validate your pattern. Remember to escape special characters like '.', '*', '+', '?', etc.",
            regex::Error::CompiledTooBig(_) =>
                "Your regex pattern is too complex. Try simplifying it or breaking it into multiple smaller patterns.",
            _ => "Verify your regex pattern is valid. Use tools like regex101.com to test and debug your pattern.",
        };

        JsonToolsError::RegexError {
            message: source.to_string(),
            suggestion: suggestion.into(),
            source,
        }
    }

    /// Create an invalid replacement pattern error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn invalid_replacement_pattern(message: impl Into<String>) -> Self {
        let msg = message.into();
        let suggestion = if msg.contains("pairs") {
            "Replacement patterns must be provided in pairs (pattern, replacement). Ensure you have an even number of arguments."
        } else if msg.contains("regex") {
            "Patterns are matched literally (exact substring) by default. Wrap a pattern in r'...' to use it as a regex instead, e.g. r'^user_' to match keys starting with 'user_'."
        } else {
            "Check your replacement pattern configuration. Patterns should be in the format: pattern1, replacement1, pattern2, replacement2, etc."
        };

        JsonToolsError::InvalidReplacementPattern {
            message: msg,
            suggestion: suggestion.into(),
        }
    }

    /// Create an invalid JSON structure error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn invalid_json_structure(message: impl Into<String>) -> Self {
        let msg = message.into();
        let suggestion = if msg.contains("unflatten") {
            "For unflattening, ensure your JSON is a flat object with dot-separated keys like {'user.name': 'John', 'user.age': 30}."
        } else if msg.contains("object") {
            "The operation requires a JSON object ({}), but received a different type. Check that your input is a valid JSON object."
        } else {
            "Verify that your JSON structure is compatible with the requested operation. Flattening works on nested objects/arrays, unflattening works on flat objects."
        };

        JsonToolsError::InvalidJsonStructure {
            message: msg,
            suggestion: suggestion.into(),
        }
    }

    /// Create a configuration error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn configuration_error(message: impl Into<String>) -> Self {
        JsonToolsError::ConfigurationError {
            message: message.into(),
            suggestion: "Call .flatten() or .unflatten() on your JSONTools instance before calling .execute() to set the operation mode.".into(),
        }
    }

    /// Create a batch processing error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn batch_processing_error(index: usize, source: JsonToolsError) -> Self {
        JsonToolsError::BatchProcessingError {
            index,
            message: format!("Failed to process item at index {}", index),
            suggestion: "Check the JSON at the specified index. All items in a batch must be valid JSON strings or objects.".to_string(),
            source: Box::new(source),
        }
    }

    /// Create an input validation error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn input_validation_error(message: impl Into<String>) -> Self {
        let msg = message.into();
        let suggestion = if msg.contains("type") {
            "Ensure your input is a valid JSON string, Python dict, or list of JSON strings/dicts."
        } else if msg.contains("empty") {
            "Provide non-empty input for processing."
        } else {
            "Check that your input format matches the expected type for the operation."
        };

        JsonToolsError::InputValidationError {
            message: msg,
            suggestion: suggestion.to_string(),
        }
    }

    /// Create a serialization error
    #[cold] // Error paths are rarely taken; keep out of hot code
    #[inline(never)]
    pub fn serialization_error(source: json_parser::JsonError) -> Self {
        JsonToolsError::SerializationError {
            message: source.to_string(),
            suggestion: "This is likely an internal error. The processed data couldn't be serialized back to JSON. Please report this issue.".to_string(),
            source,
        }
    }
}

// Automatic conversion from json_parser::JsonError
impl From<json_parser::JsonError> for JsonToolsError {
    fn from(error: json_parser::JsonError) -> Self {
        JsonToolsError::json_parse_error(error)
    }
}

// Automatic conversion from regex::Error
impl From<regex::Error> for JsonToolsError {
    fn from(error: regex::Error) -> Self {
        JsonToolsError::regex_error(error)
    }
}

// Automatic conversion from pyo3::PyErr (needed for closures mixing PyResult and JsonToolsError)
#[cfg(feature = "python")]
impl From<pyo3::PyErr> for JsonToolsError {
    fn from(err: pyo3::PyErr) -> Self {
        JsonToolsError::configuration_error(format!("Python error: {err}"))
    }
}
