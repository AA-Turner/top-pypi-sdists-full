use anyhow::{Context, bail};
use std::path::PathBuf;

use chrono::Local;
use owo_colors::OwoColorize;
use tokio::{fs::OpenOptions, io::AsyncWriteExt};

use crate::helpers::PathAsStr;
use crate::shell::SupportedShell;
use crate::{
    cli::{EnsurepathOptions, Process},
    metadata::ensure_bin_dir,
};

pub fn now() -> String {
    let dt = Local::now();

    match dt.to_string().split_once('.') {
        None => String::new(),
        Some((datetime, _)) => datetime.to_owned(),
    }
}

pub async fn append(
    file_path: &PathBuf,
    text: &str,
) -> anyhow::Result<()> {
    let mut file = OpenOptions::new().append(true).open(file_path).await?;

    file.write_all(text.as_bytes()).await?;
    file.flush().await?;
    Ok(())
}

pub fn check_in_path(dir: &str) -> bool {
    let path = std::env::var("PATH").unwrap_or_default();

    path.split(':').any(|x| x == dir)
}

pub const SNAP_ENSUREPATH: &str = "eval \"$(uvenv --generate=bash ensurepath)\"";

pub async fn ensure_path(force: bool) -> anyhow::Result<i32> {
    let bin_path = ensure_bin_dir().await;
    let bin_dir = bin_path.as_str();

    let shell = SupportedShell::detect();

    let already_in_path = check_in_path(bin_dir);
    let rcfile = shell.rc_file().unwrap_or("rc");

    if !force && already_in_path {
        eprintln!(
            "{}: {} is already added to your path. Use '{}' to add it to your {} file anyway.",
            "Warning".yellow(),
            bin_dir.green(),
            "--force".blue(),
            rcfile,
        );
        // don't bail/Err because it's just a warning.
        // still exit with code > 0
        Ok(2) // missing -f
    } else {
        if cfg!(feature = "snap") {
            bail!(
                "{} snap-installed {} cannot write directly to `{}`. You can add the following line to make this feature work:\n\n{SNAP_ENSUREPATH}\n",
                "Warning:".yellow(),
                "`uvenv`".blue(),
                rcfile.blue()
            );
        }

        shell.add_to_path(bin_dir, true).await?;

        eprintln!(
            "Added '{}' to ~/{}",
            bin_dir.green(),
            shell.rc_file().unwrap_or_default()
        );
        Ok(0)
    }
}

pub async fn ensure_path_generate() -> String {
    let bin_path = ensure_bin_dir().await;
    let bin_dir = bin_path.as_str();
    format!("export PATH=\"$PATH:{bin_dir}\"")
}

impl Process for EnsurepathOptions {
    async fn process(self) -> anyhow::Result<i32> {
        if let Err(msg) = ensure_path(self.force).await {
            Err(msg).with_context(|| "Something went wrong trying to ensure a proper PATH;")
        } else {
            Ok(0)
        }
    }
}
