use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::str::FromStr;
use std::time::Duration;

use chalk_proto::chalk::artifacts::v1::Export;
use chalk_proto::chalk::graph::v1::{
    function_reference_captured_global::CapturedGlobal, FunctionReferenceCapturedGlobal,
};
use chalk_proto::chalk::lsp::v1 as proto_lsp;
use crossbeam_channel::Sender;
use log::{debug, error, info, warn};
use lsp_types::{Diagnostic, DiagnosticSeverity, NumberOrString, Position, Range, Uri};
use prost::Message;
use serde::Deserialize;

use crate::project::{path_to_file_uri, uri_to_file_path, ExternalFileDiagnostics, PathScope};

pub const DEFAULT_LSP_DIAGNOSTICS_API_HOST: &str = "https://api.chalk.ai";

const STATIC_CONVERSION_PATH: &str = "/v1/static-conversion-diagnostics";
const STATIC_CONVERSION_SERVER_HEADER: &str = "X-Chalk-Server";
const STATIC_CONVERSION_SERVER_HEADER_VALUE: &str = "static-accelerator";
const STATIC_CONVERSION_TIMEOUT_SECS: u64 = 300;

pub struct ExternalDiagnosticsJob {
    pub run_id: u64,
    pub trigger_uri: Uri,
    pub trigger_uri_key: String,
    pub trigger_file_path: PathBuf,
    pub trigger_text: String,
    pub trigger_project_root: PathBuf,
    pub workspace_roots: Vec<PathBuf>,
    pub requested_paths: Vec<PathBuf>,
    pub api_host: String,
    pub chalkpy_path_override: Option<PathBuf>,
}

pub struct ExternalDiagnosticsResult {
    pub run_id: u64,
    pub files: Vec<ExternalFileDiagnostics>,
}

type ExternalDiagnosticsRunResult<T> = Result<T, String>;

pub fn spawn_external_diagnostics(
    result_sender: Sender<ExternalDiagnosticsResult>,
    job: ExternalDiagnosticsJob,
) {
    // Quick hack: one thread per save; run_id filtering drops stale results.
    std::thread::spawn(move || {
        let files = match run_external_diagnostics(
            &job.trigger_project_root,
            &job.api_host,
            job.chalkpy_path_override.as_deref(),
            &job.requested_paths,
        ) {
            Ok(files) => files,
            Err(err) => {
                warn!(
                    "failed to run static-conversion diagnostics for {}: {err}",
                    job.trigger_uri.as_str()
                );
                Vec::new()
            }
        };
        let _ = result_sender.send(ExternalDiagnosticsResult {
            run_id: job.run_id,
            files,
        });
    });
}

pub fn run_external_diagnostics(
    project_root: &Path,
    api_host: &str,
    chalkpy_path_override: Option<&Path>,
    requested_paths: &[PathBuf],
) -> Result<Vec<ExternalFileDiagnostics>, String> {
    info!(
        "running static-conversion diagnostics: cwd={}, api_host={}, requested_path_count={}",
        project_root.display(),
        api_host,
        requested_paths.len(),
    );

    let mut export = build_static_conversion_export(project_root, chalkpy_path_override)?;
    if !requested_paths.is_empty() {
        let selected_resolvers =
            prune_export_to_requested_paths(&mut export, project_root, requested_paths);
        if selected_resolvers == 0 {
            info!(
                "skipping static-conversion diagnostics: no resolver source files matched {} requested path(s)",
                requested_paths.len(),
            );
            return Ok(Vec::new());
        }
    }

    let response = get_static_conversion_diagnostics(api_host, export)?;
    let files = external_diagnostics_from_response(project_root, response)?;
    if requested_paths.is_empty() {
        return Ok(files);
    }

    let scopes = PathScope::from_paths(project_root, requested_paths);
    Ok(files
        .into_iter()
        .filter(|file| {
            uri_to_file_path(&file.uri).as_deref().is_some_and(|path| {
                scopes
                    .iter()
                    .any(|scope| scope.contains(project_root, path))
            })
        })
        .collect())
}

fn build_static_conversion_export(
    root: &Path,
    chalkpy_path_override: Option<&Path>,
) -> ExternalDiagnosticsRunResult<Export> {
    let export_file = tempfile::NamedTempFile::new()
        .map_err(|err| format!("failed to create temporary export file: {err}"))?;
    let export_path = export_file.into_temp_path();

    let project_files_file = tempfile::NamedTempFile::new()
        .map_err(|err| format!("failed to create temporary project file allowlist: {err}"))?;
    let project_files_path = project_files_file.into_temp_path();
    write_project_file_allowlist(root, project_files_path.as_ref())?;

    let chalkpy = resolve_chalkpy_executable(root, chalkpy_path_override)?;
    info!(
        "running chalkpy static-conversion export: executable={}, root={}, output={}, file_filter={}",
        chalkpy.display(),
        root.display(),
        export_path.display(),
        project_files_path.display(),
    );

    let output = Command::new(&chalkpy)
        .arg("export")
        .arg(export_path.as_os_str())
        .arg("--directory")
        .arg(root)
        .arg("--file_filter")
        .arg(project_files_path.as_os_str())
        .arg("--proto")
        .arg("--include-captured-global-values")
        .current_dir(root)
        .output()
        .map_err(|err| {
            format!(
                "failed to run chalkpy static-conversion export with {}: {err}",
                chalkpy.display()
            )
        })?;

    info!(
        "chalkpy static-conversion export exited: status={}",
        output.status
    );
    log_command_output("chalkpy static-conversion export stdout", &output.stdout);
    log_command_output("chalkpy static-conversion export stderr", &output.stderr);

    if !output.status.success() || !output.stderr.is_empty() {
        let message = combined_command_output(&output.stdout, &output.stderr);
        return Err(if message.is_empty() {
            format!(
                "chalkpy static-conversion export failed with status {}",
                output.status
            )
        } else {
            format!(
                "chalkpy static-conversion export failed with status {}: {message}",
                output.status
            )
        });
    }

    let export_path_for_read: &Path = export_path.as_ref();
    let export_bytes = fs::read(export_path_for_read)
        .map_err(|err| format!("failed to read static-conversion export output: {err}"))?;
    Export::decode(export_bytes.as_slice())
        .map_err(|err| format!("failed to decode static-conversion export output: {err}"))
}

fn prune_export_to_requested_paths(
    export: &mut Export,
    project_root: &Path,
    requested_paths: &[PathBuf],
) -> usize {
    let Some(graph) = export.graph.as_mut() else {
        return 0;
    };

    let scopes = PathScope::from_paths(project_root, requested_paths);
    let captured_by_id: HashMap<String, FunctionReferenceCapturedGlobal> = graph
        .captured_global_values
        .iter()
        .filter_map(|captured| {
            captured
                .value
                .as_ref()
                .map(|value| (captured.id.clone(), value.clone()))
        })
        .collect();

    let resolver_count = graph.resolvers.len();
    graph.resolvers.retain(|resolver| {
        let mut visited_value_refs = HashSet::new();
        resolver.function.as_ref().is_some_and(|function| {
            let function_file_matches = !function.file_name.trim().is_empty()
                && scopes
                    .iter()
                    .any(|scope| scope.contains(project_root, Path::new(&function.file_name)));
            function_file_matches
                || function.captured_globals.iter().any(|captured| {
                    captured_global_matches_requested_paths(
                        captured,
                        &captured_by_id,
                        project_root,
                        &scopes,
                        &mut visited_value_refs,
                    )
                })
        })
    });

    info!(
        "pruned static-conversion export resolvers: before={}, after={}, requested_path_count={}",
        resolver_count,
        graph.resolvers.len(),
        requested_paths.len(),
    );
    graph.resolvers.len()
}

fn captured_global_matches_requested_paths(
    captured: &FunctionReferenceCapturedGlobal,
    captured_by_id: &HashMap<String, FunctionReferenceCapturedGlobal>,
    project_root: &Path,
    scopes: &[PathScope],
    visited_value_refs: &mut HashSet<String>,
) -> bool {
    if let Some(source_reference) = captured.source_reference.as_ref() {
        if !source_reference.file_name.trim().is_empty()
            && scopes
                .iter()
                .any(|scope| scope.contains(project_root, Path::new(&source_reference.file_name)))
        {
            return true;
        }
    }

    match captured.captured_global.as_ref() {
        Some(CapturedGlobal::Function(function)) => {
            function.captured_globals.iter().any(|captured| {
                captured_global_matches_requested_paths(
                    captured,
                    captured_by_id,
                    project_root,
                    scopes,
                    visited_value_refs,
                )
            })
        }
        Some(CapturedGlobal::ValueRef(value_ref)) => {
            if !visited_value_refs.insert(value_ref.id.clone()) {
                return false;
            }
            captured_by_id.get(&value_ref.id).is_some_and(|captured| {
                captured_global_matches_requested_paths(
                    captured,
                    captured_by_id,
                    project_root,
                    scopes,
                    visited_value_refs,
                )
            })
        }
        _ => false,
    }
}

fn write_project_file_allowlist(
    root: &Path,
    destination: &Path,
) -> ExternalDiagnosticsRunResult<()> {
    let chalkignore_path = chalk_ignore::get_chalkignore_path(root, None)
        .map_err(|err| format!("failed to resolve chalkignore path: {err}"))?;
    let project_files = chalk_ignore::get_project_files(root, chalkignore_path.as_deref(), &[])
        .map_err(|err| format!("failed to collect project files: {err}"))?;
    let content = project_files
        .iter()
        .map(|path| path.to_string_lossy())
        .collect::<Vec<_>>()
        .join("\n");
    fs::write(destination, content)
        .map_err(|err| format!("failed to write project file allowlist: {err}"))
}

fn get_static_conversion_diagnostics(
    api_host: &str,
    export: Export,
) -> ExternalDiagnosticsRunResult<StaticConversionDiagnosticsResponse> {
    let mut request_body = Vec::with_capacity(export.encoded_len());
    export
        .encode(&mut request_body)
        .map_err(|err| format!("failed to encode static-conversion export: {err}"))?;

    let url = static_conversion_url(api_host);
    let agent = ureq::AgentBuilder::new()
        .timeout(Duration::from_secs(STATIC_CONVERSION_TIMEOUT_SECS))
        .build();
    let response = agent
        .post(&url)
        .set("content-type", "application/x-protobuf")
        .set(
            STATIC_CONVERSION_SERVER_HEADER,
            STATIC_CONVERSION_SERVER_HEADER_VALUE,
        )
        .send_bytes(&request_body)
        .map_err(format_ureq_error)?;

    let mut response_body = Vec::new();
    response
        .into_reader()
        .read_to_end(&mut response_body)
        .map_err(|err| format!("failed to read static-conversion response body: {err}"))?;
    let response: StaticConversionDiagnosticsResponse = serde_json::from_slice(&response_body)
        .map_err(|err| format!("failed to decode static-conversion JSON response body: {err}"))?;
    Ok(response)
}

fn static_conversion_url(api_host: &str) -> String {
    format!(
        "{}{}",
        api_host.trim_end_matches('/'),
        STATIC_CONVERSION_PATH
    )
}

fn format_ureq_error(err: ureq::Error) -> String {
    match err {
        ureq::Error::Status(status, response) => {
            let body = response.into_string().unwrap_or_else(|err| {
                format!("<failed to read static-conversion error body: {err}>")
            });
            format!("static-conversion request failed with HTTP status {status}: {body}")
        }
        ureq::Error::Transport(transport) => {
            format!("static-conversion request transport error: {transport}")
        }
    }
}

fn external_diagnostics_from_response(
    project_root: &Path,
    response: StaticConversionDiagnosticsResponse,
) -> ExternalDiagnosticsRunResult<Vec<ExternalFileDiagnostics>> {
    let StaticConversionDiagnosticsResponse { diagnostics, logs } = response;

    let log_count = logs.len();
    for log_message in logs {
        emit_static_conversion_log(log_message);
    }

    let mut files = Vec::new();
    let mut diagnostic_count = 0usize;
    for file in diagnostics {
        let (uri, uri_key) = diagnostic_uri_to_lsp_uri(project_root, &file.uri)?;
        diagnostic_count += file.diagnostics.len();
        let diagnostics = file
            .diagnostics
            .into_iter()
            .map(external_diagnostic_to_lsp)
            .collect();
        files.push(ExternalFileDiagnostics {
            uri,
            uri_key,
            diagnostics,
        });
    }

    info!(
        "static-conversion diagnostics completed: {} file(s), {} diagnostic(s), {} log(s)",
        files.len(),
        diagnostic_count,
        log_count,
    );
    Ok(files)
}

#[derive(Debug, Deserialize)]
struct StaticConversionDiagnosticsResponse {
    #[serde(default)]
    diagnostics: Vec<ExternalPublishDiagnosticsParams>,
    #[serde(default)]
    logs: Vec<ExternalLogMessage>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ExternalPublishDiagnosticsParams {
    #[serde(default)]
    uri: String,
    #[serde(default)]
    diagnostics: Vec<ExternalDiagnostic>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ExternalDiagnostic {
    range: Option<ExternalRange>,
    #[serde(default)]
    message: String,
    #[serde(default, deserialize_with = "deserialize_diagnostic_severity")]
    severity: i32,
    code: Option<String>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ExternalRange {
    start: Option<ExternalPosition>,
    end: Option<ExternalPosition>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ExternalPosition {
    line: Option<i32>,
    character: Option<i32>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct ExternalLogMessage {
    #[serde(default, deserialize_with = "deserialize_log_message_severity")]
    severity: i32,
    #[serde(default)]
    message: String,
    #[serde(default)]
    traceback: String,
}

fn deserialize_diagnostic_severity<'de, D>(deserializer: D) -> Result<i32, D::Error>
where
    D: serde::Deserializer<'de>,
{
    let severity = Option::<String>::deserialize(deserializer)?;
    Ok(severity
        .as_deref()
        .and_then(proto_lsp::DiagnosticSeverity::from_str_name)
        .unwrap_or(proto_lsp::DiagnosticSeverity::Error) as i32)
}

fn deserialize_log_message_severity<'de, D>(deserializer: D) -> Result<i32, D::Error>
where
    D: serde::Deserializer<'de>,
{
    let severity = Option::<String>::deserialize(deserializer)?;
    Ok(severity
        .as_deref()
        .and_then(proto_lsp::LogMessageSeverity::from_str_name)
        .unwrap_or(proto_lsp::LogMessageSeverity::Error) as i32)
}

fn emit_static_conversion_log(log_message: ExternalLogMessage) {
    let severity = proto_lsp::LogMessageSeverity::try_from(log_message.severity)
        .unwrap_or(proto_lsp::LogMessageSeverity::Error);
    match severity {
        proto_lsp::LogMessageSeverity::Warning => warn!("{}", log_message.message),
        proto_lsp::LogMessageSeverity::Info => info!("{}", log_message.message),
        proto_lsp::LogMessageSeverity::Debug => debug!("{}", log_message.message),
        proto_lsp::LogMessageSeverity::Unspecified | proto_lsp::LogMessageSeverity::Error => {
            error!("{}", log_message.message)
        }
    }

    if !log_message.traceback.is_empty() {
        debug!("{}", log_message.traceback);
    }
}

fn diagnostic_uri_to_lsp_uri(
    project_root: &Path,
    uri_or_path: &str,
) -> ExternalDiagnosticsRunResult<(Uri, String)> {
    if uri_or_path.starts_with("file://") {
        let uri = Uri::from_str(uri_or_path)
            .map_err(|err| format!("failed to parse static-conversion diagnostic URI: {err}"))?;
        let uri_key = uri.as_str().to_string();
        return Ok((uri, uri_key));
    }

    let mut file_path = PathBuf::from(uri_or_path);
    if !file_path.is_absolute() {
        file_path = project_root.join(file_path);
    }
    let Some(uri) = path_to_file_uri(&file_path) else {
        return Err(format!(
            "failed to convert static-conversion diagnostic path to URI: {}",
            file_path.display()
        ));
    };
    let uri_key = uri.as_str().to_string();
    Ok((uri, uri_key))
}

fn external_diagnostic_to_lsp(diagnostic: ExternalDiagnostic) -> Diagnostic {
    Diagnostic {
        range: external_range_to_lsp(diagnostic.range),
        severity: Some(external_severity_to_lsp(diagnostic.severity)),
        code: diagnostic.code.map(NumberOrString::String),
        source: Some("remote".to_string()),
        message: diagnostic.message,
        ..Default::default()
    }
}

fn external_range_to_lsp(range: Option<ExternalRange>) -> Range {
    let Some(range) = range else {
        return Range::default();
    };
    Range {
        start: external_position_to_lsp(range.start),
        end: external_position_to_lsp(range.end),
    }
}

fn external_position_to_lsp(position: Option<ExternalPosition>) -> Position {
    let Some(position) = position else {
        return Position::default();
    };
    Position {
        line: external_coordinate_to_lsp(position.line),
        character: external_coordinate_to_lsp(position.character),
    }
}

fn external_coordinate_to_lsp(value: Option<i32>) -> u32 {
    value
        .and_then(|value| u32::try_from(value).ok())
        .unwrap_or_default()
}

fn external_severity_to_lsp(severity: i32) -> DiagnosticSeverity {
    match proto_lsp::DiagnosticSeverity::try_from(severity)
        .unwrap_or(proto_lsp::DiagnosticSeverity::Error)
    {
        proto_lsp::DiagnosticSeverity::Warning => DiagnosticSeverity::WARNING,
        proto_lsp::DiagnosticSeverity::Information => DiagnosticSeverity::INFORMATION,
        proto_lsp::DiagnosticSeverity::Hint => DiagnosticSeverity::HINT,
        proto_lsp::DiagnosticSeverity::Unspecified | proto_lsp::DiagnosticSeverity::Error => {
            DiagnosticSeverity::ERROR
        }
    }
}

fn resolve_chalkpy_executable(
    root: &Path,
    chalkpy_path_override: Option<&Path>,
) -> ExternalDiagnosticsRunResult<PathBuf> {
    if let Some(path) = chalkpy_path_override {
        let resolved = if path.is_absolute() {
            path.to_path_buf()
        } else {
            root.join(path)
        };
        if is_executable_file(&resolved) {
            return Ok(resolved);
        }
        return Err(format!(
            "configured chalk.remoteDiagnostics.chalkpyPathOverride is not an executable file: {}",
            resolved.display()
        ));
    }

    let project_local_candidates = [
        root.join(".venv").join("bin").join("chalkpy"),
        root.join("venv").join("bin").join("chalkpy"),
    ];
    for candidate in &project_local_candidates {
        if is_executable_file(candidate) {
            return Ok(candidate.clone());
        }
    }

    Err(format!(
        "failed to find project-local chalkpy; checked {} and {}",
        project_local_candidates[0].display(),
        project_local_candidates[1].display()
    ))
}

fn is_executable_file(path: &Path) -> bool {
    let Ok(metadata) = fs::metadata(path) else {
        return false;
    };
    if !metadata.is_file() {
        return false;
    }

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        metadata.permissions().mode() & 0o111 != 0
    }

    #[cfg(not(unix))]
    {
        true
    }
}

fn log_command_output(label: &str, output: &[u8]) {
    if output.is_empty() {
        info!("{label}: <empty>");
    } else {
        info!("{label}:\n{}", String::from_utf8_lossy(output));
    }
}

fn combined_command_output(stdout: &[u8], stderr: &[u8]) -> String {
    let mut parts = Vec::new();
    let stdout = String::from_utf8_lossy(stdout).trim().to_string();
    let stderr = String::from_utf8_lossy(stderr).trim().to_string();
    if !stdout.is_empty() {
        parts.push(stdout);
    }
    if !stderr.is_empty() {
        parts.push(stderr);
    }
    parts.join("\n")
}
