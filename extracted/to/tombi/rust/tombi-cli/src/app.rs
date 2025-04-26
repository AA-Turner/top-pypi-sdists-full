mod arg;
mod command;
mod tracing_formatter;

use clap::{
    builder::styling::{AnsiColor, Color, Style},
    Parser,
};
use clap_verbosity_flag::{InfoLevel, Verbosity};
use tracing_formatter::TombiFormatter;
use tracing_subscriber::prelude::*;

#[derive(clap::Parser)]
#[command(
    name="tombi",
    about = app_about(),
    version,
    styles=app_styles(),
    disable_help_subcommand(true),
)]
pub struct Args {
    #[command(subcommand)]
    pub subcommand: command::TomlCommand,

    /// Do not fetch from remote
    #[clap(long, global = true)]
    offline: bool,

    #[command(flatten)]
    verbose: Verbosity<InfoLevel>,
}

impl<I, T> From<I> for Args
where
    I: IntoIterator<Item = T>,
    T: Into<std::ffi::OsString> + Clone,
{
    #[inline]
    fn from(value: I) -> Self {
        Self::parse_from(value)
    }
}

pub fn run(args: impl Into<Args>) -> Result<(), crate::Error> {
    let args: Args = args.into();
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::from(
            args.verbose.log_level_filter().to_string(),
        ))
        .with(
            tracing_subscriber::fmt::layer()
                .event_format(TombiFormatter::from(args.verbose.log_level_filter()))
                .with_writer(std::io::stderr),
        )
        .init();

    let offline = args.offline;
    match args.subcommand {
        command::TomlCommand::Format(args) => command::format::run(args, offline),
        command::TomlCommand::Lint(args) => command::lint::run(args, offline),
        command::TomlCommand::Serve(args) => command::serve::run(args, offline),
    }
}

fn app_about() -> String {
    let title = "Tombi";
    let title_style = Style::new()
        .bold()
        .bg_color(Some(Color::Ansi(AnsiColor::Blue)))
        .fg_color(Some(Color::Ansi(AnsiColor::White)));

    let desc_style = Style::new()
        .bg_color(Some(Color::Ansi(AnsiColor::Blue)))
        .fg_color(Some(Color::Ansi(AnsiColor::White)));

    format!(
        "{title_style}              {title} {title_style:#}{desc_style}: TOML Toolkit              {desc_style:#}"
    )
}

const fn app_styles() -> clap::builder::Styles {
    clap::builder::Styles::plain()
        .header(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Blue))),
        )
        .error(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Red))),
        )
        .usage(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Blue))),
        )
        .literal(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Cyan))),
        )
        .placeholder(Style::new().fg_color(Some(Color::Ansi(AnsiColor::Cyan))))
        .valid(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Green))),
        )
        .invalid(
            Style::new()
                .bold()
                .fg_color(Some(Color::Ansi(AnsiColor::Red))),
        )
}
