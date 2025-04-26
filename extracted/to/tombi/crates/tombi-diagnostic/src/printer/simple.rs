use nu_ansi_term::Style;

use crate::{Diagnostic, Level, Print};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Simple;

impl Print<Simple> for Level {
    fn print(&self, _printer: Simple) {
        print!("{}", self.color().bold().paint(self.as_padded_str()));
    }
}

impl Print<Simple> for Diagnostic {
    fn print(&self, printer: Simple) {
        self.level().print(printer);
        println!(": {}", Style::new().bold().paint(self.message()));
    }
}
