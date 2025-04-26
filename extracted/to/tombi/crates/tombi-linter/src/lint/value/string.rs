use crate::Lint;

impl Lint for tombi_ast::BasicString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::LiteralString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::MultiLineBasicString {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::MultiLineLiteralString {
    fn lint(&self, _l: &mut crate::Linter) {}
}
