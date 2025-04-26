use crate::Lint;

impl Lint for tombi_ast::Float {
    fn lint(&self, _l: &mut crate::Linter) {}
}
