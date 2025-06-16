use owo_colors::OwoColorize;
use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::cli::{CheckOptions, Process};
use crate::commands::ensurepath::{SNAP_ENSUREPATH, check_in_path};
use crate::commands::list::list_packages;
use crate::helpers::PathAsStr;
use crate::metadata::{LoadMetadataConfig, get_bin_dir};
use crate::shell::SupportedShell;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Default, Serialize, Deserialize)]
struct Issues<'metadata> {
    path_correct: bool,
    #[serde(borrow)]
    outdated: Vec<&'metadata str>,
    #[serde(borrow)]
    broken: BTreeMap<&'metadata str, Vec<String>>,
    #[serde(borrow)]
    scripts: BTreeMap<&'metadata str, Vec<String>>,
}

impl Issues<'_> {
    pub const fn new() -> Self {
        Self {
            path_correct: false,
            outdated: Vec::new(),
            broken: BTreeMap::new(),
            scripts: BTreeMap::new(),
        }
    }

    fn check_path(&mut self) {
        let bin_dir = get_bin_dir();

        if cfg!(feature = "snap") {
            let shell = SupportedShell::detect();

            let rcfile = shell.rc_file().unwrap_or("rc");
            eprintln!(
                "{}: snap-installed `{}` cannot access $PATH. \
            To ensure '{}' exists in your PATH, you can add `{}` to your {} file.",
                "Warning".yellow(),
                "uvenv".blue(),
                bin_dir.as_str().blue(),
                SNAP_ENSUREPATH.green(),
                rcfile
            );
            self.path_correct = true;
        } else {
            self.path_correct = check_in_path(bin_dir.as_str());
        }
    }

    #[expect(clippy::as_conversions, reason = "The number won't be that big")]
    pub const fn count_outdated(&self) -> i32 {
        self.outdated.len() as i32
    }
    #[expect(clippy::as_conversions, reason = "The number won't be that big")]
    pub fn count_scripts(&self) -> i32 {
        self.scripts
            .values()
            .fold(0, |acc, vec| acc + vec.len() as i32)
    }

    pub fn count(&self) -> i32 {
        let mut count = 0;

        count += self.count_outdated();
        count += self.count_scripts();

        if !self.path_correct {
            count += 1;
        }

        count
    }

    pub fn print_json(&self) -> anyhow::Result<i32> {
        let json = serde_json::to_string_pretty(self)?;

        eprintln!("{json}");

        Ok(self.count())
    }

    fn print_human(&self) -> i32 {
        let issue_count = self.count();

        if issue_count == 0 {
            println!("{}", "✅ No issues found. Everything is up-to-date and all scripts are properly installed!".green().bold());
            return 0;
        }

        println!("{}", "🚨 Issues Overview:".bold().underline());

        if !self.path_correct {
            let bin_dir = get_bin_dir();
            println!(
                "{}",
                format!("  - {} is not in $PATH", bin_dir.as_str()).red()
            );

            println!(
                "{}",
                "💡 Tip: you can use `uvenv ensurepath` to fix this.".blue()
            );
        }

        // Display outdated issues
        if !self.outdated.is_empty() {
            println!("{}", "\n🔶 Outdated:".bold().yellow());
            for issue in &self.outdated {
                println!("  - {}", issue.red());
            }

            println!(
                "{}",
                "💡 Tip: you can use `uvenv upgrade <package>` to update a specific environment."
                    .blue()
            );
        }

        // Display script issues
        if !self.scripts.is_empty() {
            println!("{}", "\n🔶 Missing Scripts:".bold().yellow());
            for (script, problems) in &self.scripts {
                println!("  - {}", format!("{script}:").red().bold());
                for problem in problems {
                    println!("    - {}", problem.red());
                }
            }

            println!("{}", "💡 Tip: you can use `uvenv reinstall <package>` to reinstall an environment, which might fix the missing scripts.".blue());
        }

        if !self.broken.is_empty() {
            println!("{}", "\n🔶 Broken Scripts:".bold().yellow());
            for (script, problems) in &self.broken {
                println!("  - {}", format!("{script}:").red().bold());
                for problem in problems {
                    println!("    - {}", problem.red());
                }
            }

            println!("{}", "💡 Tip: you can use `uvenv reinstall <package>` to reinstall an environment, which might fix the broken scripts.".blue());
        }

        issue_count
    }
}

impl CheckOptions {
    const fn to_metadataconfig(&self) -> LoadMetadataConfig {
        LoadMetadataConfig {
            recheck_scripts: !self.skip_scripts,
            updates_check: !self.skip_updates,
            updates_prereleases: self.show_prereleases,
            updates_ignore_constraints: self.ignore_constraints,
        }
    }
}

impl Process for CheckOptions {
    async fn process(self) -> anyhow::Result<i32> {
        let config = self.to_metadataconfig();

        let items = list_packages(&config, Some(&self.venv_names), None).await?;

        // collect issues:

        let mut issues = Issues::new();

        issues.check_path();

        for metadata in &items {
            let invalid_scripts = metadata.invalid_scripts();
            if !self.skip_scripts && !invalid_scripts.is_empty() {
                issues.scripts.insert(&metadata.name, invalid_scripts);
            }

            if !self.skip_updates && metadata.outdated {
                issues.outdated.push(&metadata.name);
            }

            if !self.skip_broken {
                let broken_scripts = metadata.broken_scripts().await;
                if !broken_scripts.is_empty() {
                    issues.broken.insert(&metadata.name, broken_scripts);
                }
            }
        }

        // show issues:

        if self.json {
            issues.print_json()
        } else {
            Ok(issues.print_human())
        }
    }
}
