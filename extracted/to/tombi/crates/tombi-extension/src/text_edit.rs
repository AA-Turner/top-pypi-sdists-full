#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TextEdit {
    pub span: tombi_text::Span,
    pub new_text: String,
}
