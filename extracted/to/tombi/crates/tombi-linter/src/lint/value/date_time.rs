use crate::Lint;

impl Lint for tombi_ast::OffsetDateTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::LocalDateTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::LocalDate {
    fn lint(&self, _l: &mut crate::Linter) {}
}

impl Lint for tombi_ast::LocalTime {
    fn lint(&self, _l: &mut crate::Linter) {}
}
