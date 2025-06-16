use crate::cli::{CompletionsOptions, Process};
use anyhow::{Context, bail};

use crate::shell::{SupportedShell, run_if_supported_shell_else_warn};
use owo_colors::OwoColorize;

pub async fn completions(install: bool) -> anyhow::Result<i32> {
    let shell = SupportedShell::detect();
    let shell_code = format!(r#"eval "$(uvenv --generate={} completions)""#, shell.name());
    let Some(rc_file) = shell.rc_file() else {
        bail!("Unsupported shell {}!", shell.name());
    };

    if install {
        // you probably want `uvenv setup` but keep this for legacy.
        shell.add_to_rcfile(&shell_code, true).await?;
        Ok(0)
    } else {
        Ok(run_if_supported_shell_else_warn(|_shell| {
            eprintln!(
                "Tip: place this line in your {} or run '{}' to do this automatically!",
                format!("~/{rc_file}").blue(),
                "uvenv setup".green()
            );
            println!("{shell_code}");
            Some(0)
        })
        .unwrap_or(1))
    }
}

impl Process for CompletionsOptions {
    async fn process(self) -> anyhow::Result<i32> {
        completions(self.install)
            .await
            .with_context(|| "Something went wrong trying to generate or install completions;")
    }
}
