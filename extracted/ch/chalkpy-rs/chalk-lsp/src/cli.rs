use std::{
    error::Error,
    fs,
    io::{self, Write},
    path::{Path, PathBuf},
    thread,
};

use clap::{Args, Parser, Subcommand, ValueEnum};
use crossbeam_channel::{unbounded, Sender};
use lsp_types::{Diagnostic, NumberOrString, Uri};

use chalk_lsp::diagnostics;
use chalk_lsp::external_diagnostics::{run_external_diagnostics, DEFAULT_LSP_DIAGNOSTICS_API_HOST};
use chalk_lsp::project::{uri_to_file_path, PathScope};

use crate::{
    cheapo,
    config::{Configuration, Linter},
};

pub fn run<F>(run_lsp_command: F) -> Result<(), Box<dyn Error + Sync + Send>>
where
    F: FnOnce(LspCommandArgs, Option<Configuration>) -> Result<(), Box<dyn Error + Sync + Send>>,
{
    let CliArgs { config, command } = CliArgs::parse();
    let config = config
        .map(|config| Configuration::from_json(&config))
        .transpose()?;
    match command {
        Command::Lsp(args) => run_lsp_command(args, config),
        Command::Diagnostics(args) => run_diagnostics_command(args, config.unwrap_or_default()),
    }
}

#[derive(Debug, Parser)]
#[command(name = "chalk-lsp", version = env!("CHALK_LSP_VERSION"))]
struct CliArgs {
    /// JSON configuration using the same shape as LSP settings.
    #[arg(long, global = true, value_name = "JSON")]
    config: Option<String>,

    #[command(subcommand)]
    command: Command,
}

#[derive(Debug, Subcommand)]
enum Command {
    /// Serve LSP requests
    Lsp(LspCommandArgs),

    /// Print project diagnostics
    Diagnostics(DiagnosticsCommandArgs),
}

#[derive(Debug, Args)]
pub struct LspCommandArgs {
    /// Listen for LSP over TCP on localhost instead of stdio.
    #[arg(long, value_name = "PORT")]
    pub port: Option<u16>,
}

#[derive(Debug, Args)]
struct DiagnosticsCommandArgs {
    /// Comma-separated lint sources to run. Defaults to "local,accel".
    #[arg(long, value_name = "SOURCES", value_delimiter = ',', value_enum)]
    lints: Option<Vec<Linter>>,

    /// Files or directories to scope diagnostics to.
    #[arg(value_name = "PATH")]
    paths: Vec<PathBuf>,
}

#[derive(Debug)]
struct DiagnosticLine {
    path: String,
    line: u32,
    column: u32,
    code: String,
    message: String,
    origin: String,
}

enum DiagnosticCommandEvent {
    Diagnostic(DiagnosticLine),
    Error { origin: String, message: String },
    Done { failed: bool },
}

fn run_diagnostics_command(
    args: DiagnosticsCommandArgs,
    config: Configuration,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let current_dir = std::env::current_dir()?;
    let project_root = find_chalk_project_root(&current_dir).ok_or_else(|| {
        format!(
            "failed to find chalk.yaml or chalk.yml in {} or any parent directory",
            current_dir.display()
        )
    })?;

    let selected_lints = args.lints.unwrap_or_else(|| config.chalk.linters.clone());
    let scoped_paths = resolve_diagnostics_scope_paths(&current_dir, &project_root, &args.paths)?;
    let api_host = config
        .chalk
        .remote_diagnostics
        .api_host
        .filter(|api_host| !api_host.trim().is_empty())
        .unwrap_or_else(|| DEFAULT_LSP_DIAGNOSTICS_API_HOST.to_string());
    let (sender, receiver) = unbounded();
    let lint_count = selected_lints.len();

    for lint_source in selected_lints {
        let origin = lint_source
            .to_possible_value()
            .map(|value| value.get_name().to_string())
            .unwrap_or_else(|| format!("{lint_source:?}").to_ascii_lowercase());
        let job = DiagnosticCommandJob {
            lint_source,
            origin,
            project_root: project_root.clone(),
            scoped_paths: scoped_paths.clone(),
            api_host: api_host.clone(),
            chalkpy_path_override: config
                .chalk
                .remote_diagnostics
                .chalkpy_path_override
                .clone(),
        };
        let sender = sender.clone();
        thread::spawn(move || run_diagnostic_command_job(job, sender));
    }
    drop(sender);

    let mut failed = false;
    let mut finished_lints = 0;
    while finished_lints < lint_count {
        let event = match receiver.recv() {
            Ok(event) => event,
            Err(_) => {
                failed = true;
                break;
            }
        };
        match event {
            DiagnosticCommandEvent::Diagnostic(line) => {
                print_diagnostic_line(&line)?;
            }
            DiagnosticCommandEvent::Error { origin, message } => {
                eprintln!("error: {origin} diagnostics failed: {message}");
            }
            DiagnosticCommandEvent::Done {
                failed: lint_failed,
            } => {
                finished_lints += 1;
                failed |= lint_failed;
            }
        }
    }

    if failed {
        Err("one or more diagnostics lints failed".into())
    } else {
        Ok(())
    }
}

struct DiagnosticCommandJob {
    lint_source: Linter,
    origin: String,
    project_root: PathBuf,
    scoped_paths: Vec<PathBuf>,
    api_host: String,
    chalkpy_path_override: Option<PathBuf>,
}

fn run_diagnostic_command_job(job: DiagnosticCommandJob, sender: Sender<DiagnosticCommandEvent>) {
    let result = match job.lint_source {
        Linter::Local => run_local_diagnostic_command_job(&job, &sender),
        Linter::Remote => run_accelerator_diagnostic_command_job(&job, &sender),
        Linter::Accel => run_cheapo_diagnostic_command_job(&job, &sender),
    };

    let failed = match result {
        Ok(()) => false,
        Err(err) => {
            let _ = sender.send(DiagnosticCommandEvent::Error {
                origin: job.origin,
                message: err.to_string(),
            });
            true
        }
    };
    let _ = sender.send(DiagnosticCommandEvent::Done { failed });
}

fn run_local_diagnostic_command_job(
    job: &DiagnosticCommandJob,
    sender: &Sender<DiagnosticCommandEvent>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let scopes = PathScope::from_paths(&job.project_root, &job.scoped_paths);
    for file_path in local_diagnostic_files(&job.project_root)? {
        if !scopes.is_empty()
            && !scopes
                .iter()
                .any(|scope| scope.contains(&job.project_root, &file_path))
        {
            continue;
        }
        let source = fs::read_to_string(&file_path)
            .map_err(|err| format!("failed to read {}: {err}", file_path.display()))?;
        let diagnostics = diagnostics::lint(Some(&job.project_root), &file_path, &source);
        for line in
            diagnostic_lines_for_path(&job.project_root, &file_path, diagnostics, &job.origin)
        {
            let _ = sender.send(DiagnosticCommandEvent::Diagnostic(line));
        }
    }
    Ok(())
}

fn run_accelerator_diagnostic_command_job(
    job: &DiagnosticCommandJob,
    sender: &Sender<DiagnosticCommandEvent>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let external_files = run_external_diagnostics(
        &job.project_root,
        &job.api_host,
        job.chalkpy_path_override.as_deref(),
        &job.scoped_paths,
    )?;
    for file in external_files {
        for line in
            diagnostic_lines_for_uri(&job.project_root, &file.uri, file.diagnostics, &job.origin)
        {
            let _ = sender.send(DiagnosticCommandEvent::Diagnostic(line));
        }
    }
    Ok(())
}

fn run_cheapo_diagnostic_command_job(
    job: &DiagnosticCommandJob,
    sender: &Sender<DiagnosticCommandEvent>,
) -> Result<(), Box<dyn Error + Sync + Send>> {
    let cheapo_files = cheapo::diagnostics_for_project(&job.project_root, &job.scoped_paths)?;
    for file in cheapo_files {
        for line in
            diagnostic_lines_for_uri(&job.project_root, &file.uri, file.diagnostics, &job.origin)
        {
            let _ = sender.send(DiagnosticCommandEvent::Diagnostic(line));
        }
    }
    Ok(())
}

fn resolve_diagnostics_scope_paths(
    current_dir: &Path,
    project_root: &Path,
    paths: &[PathBuf],
) -> Result<Vec<PathBuf>, Box<dyn Error + Sync + Send>> {
    let project_root = project_root.canonicalize().map_err(|err| {
        format!(
            "failed to resolve Chalk project root {}: {err}",
            project_root.display()
        )
    })?;
    let mut resolved_paths = Vec::new();
    for path in paths {
        let absolute = if path.is_absolute() {
            path.clone()
        } else {
            current_dir.join(path)
        };
        let resolved = absolute.canonicalize().map_err(|err| {
            format!(
                "failed to resolve diagnostics path {}: {err}",
                absolute.display()
            )
        })?;
        if resolved != project_root && !resolved.starts_with(&project_root) {
            return Err(format!(
                "diagnostics path {} is outside Chalk project root {}",
                resolved.display(),
                project_root.display()
            )
            .into());
        }
        resolved_paths.push(resolved);
    }
    resolved_paths.sort();
    resolved_paths.dedup();
    Ok(resolved_paths)
}

fn local_diagnostic_files(
    project_root: &Path,
) -> Result<Vec<PathBuf>, Box<dyn Error + Sync + Send>> {
    let chalkignore_path = chalk_ignore::get_chalkignore_path(project_root, None)
        .map_err(|err| format!("failed to resolve chalkignore path: {err}"))?;
    let mut files = chalk_ignore::get_project_files(project_root, chalkignore_path.as_deref(), &[])
        .map_err(|err| format!("failed to collect project files: {err}"))?;
    for config_name in chalk_project::PROJECT_CONFIG_FILENAMES {
        let config_path = project_root.join(config_name);
        if config_path.is_file() {
            files.push(config_path);
        }
    }
    files.sort();
    files.dedup();
    files.retain(|path| is_local_diagnostic_file(path));
    Ok(files)
}

fn is_local_diagnostic_file(path: &Path) -> bool {
    if path.extension().and_then(|extension| extension.to_str()) == Some("py") {
        return true;
    }
    path.file_name()
        .and_then(|name| name.to_str())
        .is_some_and(|name| chalk_project::PROJECT_CONFIG_FILENAMES.contains(&name))
}

fn diagnostic_lines_for_uri(
    project_root: &Path,
    uri: &Uri,
    diagnostics: Vec<Diagnostic>,
    origin: &str,
) -> Vec<DiagnosticLine> {
    match uri_to_file_path(uri) {
        Some(path) => diagnostic_lines_for_path(project_root, &path, diagnostics, origin),
        None => diagnostics
            .into_iter()
            .map(|diagnostic| diagnostic_line(uri.as_str().to_string(), diagnostic, origin))
            .collect(),
    }
}

fn diagnostic_lines_for_path(
    project_root: &Path,
    file_path: &Path,
    diagnostics: Vec<Diagnostic>,
    origin: &str,
) -> Vec<DiagnosticLine> {
    let display_path = diagnostic_display_path(project_root, file_path);
    diagnostics
        .into_iter()
        .map(|diagnostic| diagnostic_line(display_path.clone(), diagnostic, origin))
        .collect()
}

fn diagnostic_line(path: String, diagnostic: Diagnostic, origin: &str) -> DiagnosticLine {
    DiagnosticLine {
        path,
        line: diagnostic.range.start.line.saturating_add(1),
        column: diagnostic.range.start.character.saturating_add(1),
        code: diagnostic_code(&diagnostic),
        message: diagnostic.message.replace('\r', ""),
        origin: origin.to_string(),
    }
}

fn print_diagnostic_line(line: &DiagnosticLine) -> io::Result<()> {
    let mut message_lines = line.message.lines();
    let message = message_lines.next().unwrap_or("");
    println!(
        "{}:{}:{}: [{}] {} [{}]",
        line.path, line.line, line.column, line.code, message, line.origin,
    );
    for detail in message_lines {
        println!("    {detail}");
    }
    io::stdout().flush()
}

fn diagnostic_display_path(project_root: &Path, file_path: &Path) -> String {
    file_path
        .strip_prefix(project_root)
        .unwrap_or(file_path)
        .to_string_lossy()
        .to_string()
}

fn diagnostic_code(diagnostic: &Diagnostic) -> String {
    match diagnostic.code.as_ref() {
        Some(NumberOrString::String(code)) => code.clone(),
        Some(NumberOrString::Number(code)) => code.to_string(),
        None => "-".to_string(),
    }
}

fn find_chalk_project_root(start: &Path) -> Option<PathBuf> {
    let mut current = if start.is_dir() {
        start.to_path_buf()
    } else {
        start.parent()?.to_path_buf()
    };

    loop {
        if has_chalk_config(&current) {
            return Some(current);
        }
        if !current.pop() {
            return None;
        }
    }
}

fn has_chalk_config(dir: &Path) -> bool {
    chalk_project::PROJECT_CONFIG_FILENAMES
        .iter()
        .any(|name| dir.join(name).is_file())
}
