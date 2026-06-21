use tombi_rg_tree::Language;

use crate::TomlLanguage;

#[derive(Debug)]
pub struct SyntaxTreeBuilder<E> {
    inner: tombi_rg_tree::GreenNodeBuilder<'static>,
    errors: Vec<E>,
}

impl<E> SyntaxTreeBuilder<E> {
    pub fn finish(self) -> (tombi_rg_tree::GreenNode, Vec<E>) {
        let green = self.inner.finish();
        (green, self.errors)
    }

    pub fn token(&mut self, kind: crate::SyntaxKind, text: &str) {
        let kind = TomlLanguage::kind_to_raw(kind);
        self.inner.token(kind, text);
    }

    pub fn start_node(&mut self, kind: crate::SyntaxKind) {
        let kind = TomlLanguage::kind_to_raw(kind);
        self.inner.start_node(kind);
    }

    pub fn finish_node(&mut self) {
        self.inner.finish_node();
    }

    pub fn error(&mut self, error: E) {
        self.errors.push(error);
    }
}

impl<E> Default for SyntaxTreeBuilder<E> {
    fn default() -> SyntaxTreeBuilder<E> {
        SyntaxTreeBuilder {
            inner: tombi_rg_tree::GreenNodeBuilder::new(),
            errors: Vec::new(),
        }
    }
}
