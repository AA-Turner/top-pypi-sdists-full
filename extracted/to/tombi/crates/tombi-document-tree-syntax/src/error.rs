#[derive(thiserror::Error, Debug, Clone, PartialEq, Eq)]
#[non_exhaustive]
pub enum Error {
    #[error("duplicate key: {key}")]
    DuplicateKey { key: String, span: tombi_text::Span },

    #[error("conflicting table")]
    ConflictTable {
        range1: tombi_text::Span,
        range2: tombi_text::Span,
    },

    #[error("conflicting array")]
    ConflictArray {
        range1: tombi_text::Span,
        range2: tombi_text::Span,
    },

    #[error("invalid integer: {error}")]
    ParseIntError {
        error: std::num::ParseIntError,
        span: tombi_text::Span,
    },

    #[error("invalid float: {error}")]
    ParseFloatError {
        error: crate::support::float::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid string: {error}")]
    ParseStringError {
        error: tombi_toml_text::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid offset date time: {error}")]
    ParseOffsetDateTimeError {
        error: crate::support::chrono::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid local date time: {error}")]
    ParseLocalDateTimeError {
        error: crate::support::chrono::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid local date: {error}")]
    ParseLocalDateError {
        error: crate::support::chrono::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid local time: {error}")]
    ParseLocalTimeError {
        error: crate::support::chrono::ParseError,
        span: tombi_text::Span,
    },

    #[error("invalid date-time: {error}")]
    ParseDateTimeError {
        error: tombi_date_time::parse::Error,
        span: tombi_text::Span,
    },

    #[error("invalid comment: {error}")]
    ParseCommentError {
        error: crate::support::comment::ParseError,
        span: tombi_text::Span,
    },

    /// Error when `ast::Node` is None
    #[error("incomplete node")]
    IncompleteNode { span: tombi_text::Span },
}

impl Error {
    pub fn to_message(&self) -> String {
        self.to_string()
    }

    pub fn code(&self) -> &'static str {
        match self {
            Self::DuplicateKey { .. } => "duplicate-key",
            Self::ConflictTable { .. } => "conflict-table",
            Self::ConflictArray { .. } => "conflict-array",
            Self::ParseIntError { .. } => "parse-int-error",
            Self::ParseFloatError { .. } => "parse-float-error",
            Self::ParseStringError { .. } => "parse-string-error",
            Self::ParseOffsetDateTimeError { .. } => "parse-offset-date-time-error",
            Self::ParseLocalDateTimeError { .. } => "parse-local-date-time-error",
            Self::ParseLocalDateError { .. } => "parse-local-date-error",
            Self::ParseLocalTimeError { .. } => "parse-local-time-error",
            Self::ParseDateTimeError { .. } => "parse-date-time-error",
            Self::ParseCommentError { .. } => "parse-comment-error",
            Self::IncompleteNode { .. } => "incomplete-node",
        }
    }

    pub fn span(&self) -> tombi_text::Span {
        match self {
            Self::DuplicateKey { span, .. } => *span,
            Self::ConflictTable { range2, .. } => *range2,
            Self::ConflictArray { range2, .. } => *range2,
            Self::ParseIntError { span, .. } => *span,
            Self::ParseFloatError { span, .. } => *span,
            Self::ParseStringError { span, .. } => *span,
            Self::ParseOffsetDateTimeError { span, .. } => *span,
            Self::ParseLocalDateTimeError { span, .. } => *span,
            Self::ParseLocalDateError { span, .. } => *span,
            Self::ParseLocalTimeError { span, .. } => *span,
            Self::ParseCommentError { span, .. } => *span,
            Self::IncompleteNode { span } => *span,
            Self::ParseDateTimeError { span, .. } => *span,
        }
    }
}

#[cfg(feature = "diagnostic")]
impl tombi_diagnostic::SetDiagnostics for Error {
    fn set_diagnostics(self, diagnostics: &mut Vec<tombi_diagnostic::Diagnostic>) {
        match self {
            Self::ConflictArray { range1, range2 } => {
                let diagnostic1 =
                    tombi_diagnostic::Diagnostic::new_error(self.to_message(), self.code(), range1);
                if !diagnostics.contains(&diagnostic1) {
                    diagnostics.push(diagnostic1);
                }
                diagnostics.push(tombi_diagnostic::Diagnostic::new_error(
                    self.to_message(),
                    self.code(),
                    range2,
                ));
            }
            _ => {
                diagnostics.push(tombi_diagnostic::Diagnostic::new_error(
                    self.to_message(),
                    self.code(),
                    self.span(),
                ));
            }
        }
    }
}
