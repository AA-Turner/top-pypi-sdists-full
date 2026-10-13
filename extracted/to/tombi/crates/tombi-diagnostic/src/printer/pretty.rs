use nu_ansi_term::{Color, Style};

use crate::{Level, LocatedDiagnostic, Print, printer::Simple};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Pretty {
    pub use_ansi_color: bool,
}

impl std::default::Default for Pretty {
    fn default() -> Self {
        Self {
            use_ansi_color: true,
        }
    }
}

impl Print<Pretty> for Level {
    fn print(&self, printer: &Pretty, writer: &mut dyn std::io::Write) -> std::io::Result<()> {
        self.print(
            &Simple {
                use_ansi_color: printer.use_ansi_color,
            },
            writer,
        )
    }
}

impl Print<Pretty> for LocatedDiagnostic<'_> {
    fn print(&self, printer: &Pretty, writer: &mut dyn std::io::Write) -> std::io::Result<()> {
        let diagnostic = self.diagnostic();
        diagnostic.level().print(printer, writer)?;

        let (message_style, at_style, link_style) = if printer.use_ansi_color {
            (
                Style::new().bold(),
                Style::new().fg(Color::DarkGray),
                Style::new().fg(Color::Cyan),
            )
        } else {
            (Style::new(), Style::new(), Style::new())
        };

        writeln!(writer, ": {}", message_style.paint(diagnostic.message()))?;

        if let Some(source_file) = diagnostic.source_file() {
            writeln!(
                writer,
                "    {} {}",
                at_style.paint("at"),
                link_style.paint(format!(
                    "{}:{}:{}",
                    source_file.display(),
                    self.range().start.line + 1,
                    self.range().start.column + 1
                )),
            )
        } else {
            writeln!(
                writer,
                "    {}",
                at_style.paint(format!(
                    "at line {} column {}",
                    self.range().start.line + 1,
                    self.range().start.column + 1
                )),
            )
        }
    }
}
