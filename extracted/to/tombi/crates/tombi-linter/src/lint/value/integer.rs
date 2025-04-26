use crate::Lint;

impl Lint for tombi_ast::IntegerBin {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::IntegerOct {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::IntegerDec {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::IntegerHex {
    fn lint(&self, _l: &mut crate::Linter) {}
}
