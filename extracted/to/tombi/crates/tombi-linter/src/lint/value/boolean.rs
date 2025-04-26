use crate::Lint;

impl Lint for tombi_ast::Boolean {
    fn lint(&self, _l: &mut crate::Linter) {}
}
