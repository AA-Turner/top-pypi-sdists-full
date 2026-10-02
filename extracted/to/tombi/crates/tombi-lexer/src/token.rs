use tombi_ast_syntax::SyntaxKind;

#[derive(Clone, Copy, PartialEq, Eq)]
pub struct Token {
    kind: SyntaxKind,
    span: tombi_text::Span,
}

impl Token {
    pub fn new(kind: SyntaxKind, span: tombi_text::Span) -> Self {
        Self { kind, span }
    }

    pub const fn eof() -> Self {
        Self {
            kind: SyntaxKind::EOF,
            span: tombi_text::Span::MAX,
        }
    }

    #[inline]
    pub fn is_eof(&self) -> bool {
        self.kind == SyntaxKind::EOF
    }

    #[inline]
    pub fn kind(&self) -> SyntaxKind {
        self.kind
    }

    #[inline]
    pub fn span(&self) -> tombi_text::Span {
        self.span
    }
}

impl std::fmt::Debug for Token {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?} @{}", self.kind, self.span)
    }
}
