#[derive(Debug, PartialEq, Eq)]
pub struct Error {
    kind: ErrorKind,
    span: tombi_text::Span,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ErrorKind {
    InvalidKey,
    InvalidBasicString,
    InvalidLiteralString,
    InvalidMultilineBasicString,
    InvalidMultilineLiteralString,
    InvalidNumber,
    InvalidOffsetDateTime,
    InvalidLocalDateTime,
    InvalidLocalDate,
    InvalidLocalTime,
    InvalidLineBreak,
    InvalidToken,
}

impl Error {
    #[inline]
    pub fn new(kind: ErrorKind, span: tombi_text::Span) -> Self {
        Self { kind, span }
    }

    #[inline]
    pub fn kind(&self) -> ErrorKind {
        self.kind
    }

    #[inline]
    pub fn span(&self) -> tombi_text::Span {
        self.span
    }
}
