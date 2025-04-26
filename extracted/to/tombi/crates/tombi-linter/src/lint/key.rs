use crate::{rule::KeyEmptyRule, Lint, Rule};

impl Lint for tombi_ast::Key {
    fn lint(&self, l: &mut crate::Linter) {
        KeyEmptyRule::check(self, l);
    }
}
