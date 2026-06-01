use std::fs;
use std::path::{Path, PathBuf};

use chalk_lsp::diagnostics::lint;
use lsp_types::{Diagnostic, DiagnosticSeverity, NumberOrString};

fn fixtures_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures")
}

/// Run a fixture-based diagnostics test.
///
/// The fixture folder must contain exactly one input file `X` paired with a
/// companion `X.diagnostics` file listing the expected diagnostics, one per
/// line. Lines starting with `#` and blank lines are ignored. Diagnostics are
/// sorted before comparison.
///
/// If a `_no_project_root` marker file is present in the folder, the lint
/// function is called with `project_root = None`; otherwise the fixture
/// folder itself is used as the project root.
fn run_fixture(scenario: &str) {
    let dir = fixtures_dir().join(scenario);
    let input_file = find_input_file(&dir);
    let diagnostics_file = with_suffix(&input_file, ".diagnostics");

    let source = fs::read_to_string(&input_file)
        .unwrap_or_else(|_| panic!("failed to read {}", input_file.display()));

    let no_project_root = dir.join("_no_project_root").is_file();
    let project_root: Option<&Path> = if no_project_root { None } else { Some(&dir) };

    let diags = lint(project_root, &input_file, &source);

    let mut actual: Vec<String> = diags.iter().map(format_diagnostic).collect();
    actual.sort();

    let expected_text = fs::read_to_string(&diagnostics_file)
        .unwrap_or_else(|_| panic!("failed to read {}", diagnostics_file.display()));
    let mut expected: Vec<String> = expected_text
        .lines()
        .map(|line| line.trim_end().to_string())
        .filter(|line| !line.is_empty() && !line.starts_with('#'))
        .collect();
    expected.sort();

    if actual != expected {
        let mut msg = format!("diagnostics mismatch for {scenario}:\n");
        msg.push_str("\n--- expected ---\n");
        for e in &expected {
            msg.push_str(&format!("  {e}\n"));
        }
        msg.push_str("\n--- actual ---\n");
        for a in &actual {
            msg.push_str(&format!("  {a}\n"));
        }
        panic!("{msg}");
    }
}

fn find_input_file(dir: &Path) -> PathBuf {
    let entries = fs::read_dir(dir)
        .unwrap_or_else(|_| panic!("missing fixture dir: {}", dir.display()));
    let mut candidates = Vec::new();
    for entry in entries {
        let entry = entry.expect("read_dir entry");
        let path = entry.path();
        let Some(name) = path.file_name().and_then(|n| n.to_str()) else {
            continue;
        };
        if name == "_no_project_root" || name.ends_with(".diagnostics") {
            continue;
        }
        let companion = dir.join(format!("{name}.diagnostics"));
        if companion.is_file() {
            candidates.push(path);
        }
    }
    assert_eq!(
        candidates.len(),
        1,
        "fixture {} must contain exactly one input file paired with a `.diagnostics` companion (found {:?})",
        dir.display(),
        candidates,
    );
    candidates.into_iter().next().unwrap()
}

fn with_suffix(path: &Path, suffix: &str) -> PathBuf {
    let mut s = path.as_os_str().to_owned();
    s.push(suffix);
    PathBuf::from(s)
}

fn format_diagnostic(d: &Diagnostic) -> String {
    let severity = match d.severity {
        Some(DiagnosticSeverity::ERROR) => "error",
        Some(DiagnosticSeverity::WARNING) => "warning",
        Some(DiagnosticSeverity::INFORMATION) => "info",
        Some(DiagnosticSeverity::HINT) => "hint",
        _ => "?",
    };
    let code = d.code.as_ref().and_then(|c| match c {
        NumberOrString::String(s) => Some(s.as_str()),
        _ => None,
    });
    match code {
        Some(c) => format!("{severity}[{c}]: {}", d.message),
        None => format!("{severity}: {}", d.message),
    }
}

#[test]
fn chalk_config_missing_project() {
    run_fixture("chalk_config_missing_project");
}

#[test]
fn chalk_config_missing_environments() {
    run_fixture("chalk_config_missing_environments");
}

#[test]
fn chalk_config_missing_runtime() {
    run_fixture("chalk_config_missing_runtime");
}

#[test]
fn chalk_config_parse_error() {
    run_fixture("chalk_config_parse_error");
}

#[test]
fn chalk_config_valid() {
    run_fixture("chalk_config_valid");
}

#[test]
fn duplicate_field() {
    run_fixture("duplicate_field");
}

#[test]
fn empty_feature_class() {
    run_fixture("empty_feature_class");
}

#[test]
fn resolver_missing_return_type() {
    run_fixture("resolver_missing_return_type");
}

#[test]
fn resolver_missing_arg_type() {
    run_fixture("resolver_missing_arg_type");
}

#[test]
fn valid_python() {
    run_fixture("valid_python");
}

#[test]
fn non_python_file() {
    run_fixture("non_python_file");
}

#[test]
fn no_project_root_python() {
    run_fixture("no_project_root_python");
}
