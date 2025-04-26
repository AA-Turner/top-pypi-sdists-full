mod array;
mod boolean;
mod date_time;
mod float;
mod inline_table;
mod integer;
mod string;

use crate::Lint;

impl Lint for tombi_ast::Value {
    fn lint(&self, l: &mut crate::Linter) {
        match self {
            Self::Boolean(value) => value.lint(l),
            Self::IntegerBin(value) => value.lint(l),
            Self::IntegerOct(value) => value.lint(l),
            Self::IntegerDec(value) => value.lint(l),
            Self::IntegerHex(value) => value.lint(l),
            Self::Float(value) => value.lint(l),
            Self::BasicString(value) => value.lint(l),
            Self::LiteralString(value) => value.lint(l),
            Self::MultiLineBasicString(value) => value.lint(l),
            Self::MultiLineLiteralString(value) => value.lint(l),
            Self::OffsetDateTime(value) => value.lint(l),
            Self::LocalDateTime(value) => value.lint(l),
            Self::LocalDate(value) => value.lint(l),
            Self::LocalTime(value) => value.lint(l),
            Self::Array(value) => value.lint(l),
            Self::InlineTable(value) => value.lint(l),
        }
    }
}
