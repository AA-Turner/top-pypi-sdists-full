use std::path::{Path, PathBuf};

use serde::Deserialize;

// ── Fixture format ──────────────────────────────────────────────────────────

/// Parse a `.a.sql` file into the SQL text (cursor line stripped) and an
/// optional cursor position (0-based line, col).
///
/// A cursor line starts with `~` and contains exactly one `^` whose column
/// indicates the cursor column on the *previous* SQL line.
///
/// ```text
/// SELECT ab
/// ~        ^
/// ```
fn parse_sql_file(contents: &str) -> (String, Option<(u32, u32)>) {
    let mut sql_lines: Vec<&str> = Vec::new();
    let mut cursor: Option<(u32, u32)> = None;

    for line in contents.lines() {
        if line.starts_with('~') {
            // Cursor marker line — find the `^`
            let col = line
                .find('^')
                .unwrap_or_else(|| panic!("cursor line has no `^`: {line:?}"));
            // The cursor refers to the line *above* this marker
            let cursor_line = sql_lines.len().saturating_sub(1) as u32;
            cursor = Some((cursor_line, col as u32));
        } else {
            sql_lines.push(line);
        }
    }

    let sql = sql_lines.join("\n");
    (sql, cursor)
}

// ── Completion expectations ─────────────────────────────────────────────────

#[derive(Debug, Deserialize)]
struct CompletionFixture {
    completions: Vec<ExpectedCompletion>,
}

#[derive(Debug, Deserialize)]
struct ExpectedCompletion {
    label: String,
    #[serde(default)]
    kind: Option<String>,
    #[serde(default)]
    insert_text: Option<String>,
}

// ── Diagnostic expectations ─────────────────────────────────────────────────

#[derive(Debug, Deserialize)]
struct DiagnosticFixture {
    diagnostics: Vec<ExpectedDiagnostic>,
}

#[derive(Debug, Deserialize)]
struct ExpectedDiagnostic {
    line: u32,
    column: u32,
    severity: String,
}

// ── Test runner ─────────────────────────────────────────────────────────────

fn fixture_dir() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures")
}

fn collect_sql_fixtures() -> Vec<PathBuf> {
    let pattern = fixture_dir().join("*.a.sql").to_string_lossy().to_string();
    let mut paths: Vec<PathBuf> = glob::glob(&pattern)
        .expect("bad glob pattern")
        .filter_map(Result::ok)
        .collect();
    paths.sort();
    paths
}

#[test]
fn run_completion_fixtures() {
    let mut ran = 0;
    for sql_path in collect_sql_fixtures() {
        let comp_path = PathBuf::from(format!("{}.completion", sql_path.display()));
        if !comp_path.exists() {
            continue;
        }
        let name = sql_path.file_name().unwrap().to_string_lossy();
        eprintln!("completion fixture: {name}");

        let sql_contents = std::fs::read_to_string(&sql_path).unwrap();
        let (sql, cursor) = parse_sql_file(&sql_contents);
        let (line, col) = cursor.unwrap_or_else(|| {
            panic!("{name}: completion fixture requires a cursor line (~ with ^)")
        });

        let comp_contents = std::fs::read_to_string(&comp_path).unwrap();
        let expected: CompletionFixture = serde_yaml::from_str(&comp_contents)
            .unwrap_or_else(|e| panic!("{name}.completion: bad yaml: {e}"));

        let items = chalk_sql_lsp::completions::completions(&sql, line, col);

        if expected.completions.is_empty() {
            assert!(
                items.is_empty(),
                "{name}: expected no completions, got {} items: {:?}",
                items.len(),
                items.iter().map(|i| &i.label).collect::<Vec<_>>()
            );
        } else {
            for exp in &expected.completions {
                let found = items.iter().find(|i| i.label == exp.label);
                assert!(
                    found.is_some(),
                    "{name}: expected completion `{}` not found in {:?}",
                    exp.label,
                    items.iter().map(|i| &i.label).collect::<Vec<_>>()
                );
                let found = found.unwrap();

                if let Some(ref kind) = exp.kind {
                    let actual_kind = found.kind.map(|k| match k {
                        lsp_types::CompletionItemKind::FUNCTION => "function",
                        lsp_types::CompletionItemKind::KEYWORD => "keyword",
                        lsp_types::CompletionItemKind::VARIABLE => "variable",
                        _ => "other",
                    });
                    assert_eq!(
                        actual_kind,
                        Some(kind.as_str()),
                        "{name}: completion `{}` kind mismatch",
                        exp.label
                    );
                }

                if let Some(ref insert) = exp.insert_text {
                    assert_eq!(
                        found.insert_text.as_deref(),
                        Some(insert.as_str()),
                        "{name}: completion `{}` insert_text mismatch",
                        exp.label
                    );
                }
            }
        }

        ran += 1;
    }
    assert!(ran > 0, "no completion fixtures found");
    eprintln!("{ran} completion fixtures passed");
}

#[test]
fn run_diagnostic_fixtures() {
    let mut ran = 0;
    for sql_path in collect_sql_fixtures() {
        let diag_path = PathBuf::from(format!("{}.diagnostic", sql_path.display()));
        if !diag_path.exists() {
            continue;
        }
        let name = sql_path.file_name().unwrap().to_string_lossy();
        eprintln!("diagnostic fixture: {name}");

        let sql_contents = std::fs::read_to_string(&sql_path).unwrap();
        let (sql, _cursor) = parse_sql_file(&sql_contents);

        let diag_contents = std::fs::read_to_string(&diag_path).unwrap();
        let expected: DiagnosticFixture = serde_yaml::from_str(&diag_contents)
            .unwrap_or_else(|e| panic!("{name}.diagnostic: bad yaml: {e}"));

        let diags = chalk_sql_lsp::diagnostics::diagnostics(&sql);

        if expected.diagnostics.is_empty() {
            assert!(
                diags.is_empty(),
                "{name}: expected no diagnostics, got {}: {:?}",
                diags.len(),
                diags.iter().map(|d| &d.message).collect::<Vec<_>>()
            );
        } else {
            assert_eq!(
                diags.len(),
                expected.diagnostics.len(),
                "{name}: expected {} diagnostics, got {}: {:?}",
                expected.diagnostics.len(),
                diags.len(),
                diags
                    .iter()
                    .map(|d| format!(
                        "({},{}) {}",
                        d.range.start.line, d.range.start.character, d.message
                    ))
                    .collect::<Vec<_>>()
            );

            for (i, exp) in expected.diagnostics.iter().enumerate() {
                let d = &diags[i];
                assert_eq!(
                    d.range.start.line, exp.line,
                    "{name}: diagnostic[{i}] line mismatch"
                );
                assert_eq!(
                    d.range.start.character, exp.column,
                    "{name}: diagnostic[{i}] column mismatch"
                );
                let expected_severity = match exp.severity.as_str() {
                    "error" => lsp_types::DiagnosticSeverity::ERROR,
                    "warning" => lsp_types::DiagnosticSeverity::WARNING,
                    "info" => lsp_types::DiagnosticSeverity::INFORMATION,
                    "hint" => lsp_types::DiagnosticSeverity::HINT,
                    other => panic!("{name}: unknown severity `{other}`"),
                };
                assert_eq!(
                    d.severity,
                    Some(expected_severity),
                    "{name}: diagnostic[{i}] severity mismatch"
                );
            }
        }

        ran += 1;
    }
    assert!(ran > 0, "no diagnostic fixtures found");
    eprintln!("{ran} diagnostic fixtures passed");
}
