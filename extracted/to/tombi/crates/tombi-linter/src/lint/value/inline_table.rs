use crate::Lint;

impl Lint for tombi_ast::InlineTable {
    fn lint(&self, _l: &mut crate::Linter) {}
}
