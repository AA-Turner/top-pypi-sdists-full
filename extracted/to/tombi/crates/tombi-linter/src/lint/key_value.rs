use crate::Lint;

impl Lint for tombi_ast::KeyValue {
    fn lint(&self, l: &mut crate::Linter) {
        if let Some(keys) = self.keys() {
            for key in keys.keys() {
                key.lint(l);
            }

            if let Some(value) = self.value() {
                value.lint(l);
            }
        }
    }
}
