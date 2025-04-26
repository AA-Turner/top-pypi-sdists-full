pub mod format;
pub mod lint;
pub mod serve;

#[derive(clap::Subcommand)]
pub enum TomlCommand {
    #[command(alias = "fmt")]
    Format(format::Args),

    #[command(alias = "check")]
    Lint(lint::Args),

    #[command(alias = "lsp")]
    Serve(serve::Args),
}
