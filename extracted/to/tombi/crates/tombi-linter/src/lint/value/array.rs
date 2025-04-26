use crate::Lint;

impl Lint for tombi_ast::Array {
    fn lint(&self, _l: &mut crate::Linter) {}
}
