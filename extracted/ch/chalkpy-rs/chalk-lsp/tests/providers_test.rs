//! End-to-end tests for the go-to-definition and completion providers against a
//! real on-disk Chalk project.

use std::collections::HashMap;
use std::fs;
use std::path::Path;

use chalk_lsp::index::build_project_index;
use chalk_lsp::providers;
use tempfile::TempDir;

const FEATURES_PY: &str = r#"from chalk.features import features, DataFrame, windowed, Windowed
from typing import Optional


@features(name="superhero")
class Superhero:
    id: int
    name: str
    size: int


@features
class Child:
    id: int
    date: int


@features
class Parent:
    id: int
    children: DataFrame[Child]
    child_count: Windowed[int] = windowed(
        "1d",
        "30d",
        expression=_.children[
            _.date < _.chalk_now,
            _.date > _.chalk_window,
        ].count(),
        materialization=True,
    )
"#;

const RESOLVER_SQL: &str = r#"-- source: RISK_SF
-- resolves: superhero
select name, size from superhero_table where id = ${superhero.id}
"#;

struct Project {
    _dir: TempDir,
    root: std::path::PathBuf,
    features_path: String,
}

fn write_project() -> Project {
    let dir = TempDir::new().expect("temp dir");
    let root = dir.path().to_path_buf();
    fs::write(root.join("chalk.yaml"), "project: test\n").unwrap();
    let features_path = root.join("features.py");
    fs::write(&features_path, FEATURES_PY).unwrap();
    fs::write(root.join("resolver.chalk.sql"), RESOLVER_SQL).unwrap();
    Project {
        _dir: dir,
        root,
        features_path: features_path.to_string_lossy().to_string(),
    }
}

fn line_index(text: &str, needle: &str) -> u32 {
    text.lines()
        .position(|line| line.contains(needle))
        .unwrap_or_else(|| panic!("line containing {needle:?} not found")) as u32
}

fn col_of(text: &str, line: u32, needle: &str) -> u32 {
    text.lines()
        .nth(line as usize)
        .unwrap()
        .find(needle)
        .unwrap_or_else(|| panic!("{needle:?} not found on line {line}")) as u32
}

fn build(project: &Project) -> chalk_ast::AstProjectIndex {
    build_project_index(&project.root, &HashMap::new()).expect("index should build")
}

fn uri_ends_with(uri: &lsp_types::Uri, suffix: &str) -> bool {
    uri.as_str().ends_with(suffix)
}

#[test]
fn sql_resolves_directive_jumps_to_feature_class() {
    let project = write_project();
    let index = build(&project);

    let line = line_index(RESOLVER_SQL, "resolves:");
    let col = col_of(RESOLVER_SQL, line, "superhero") + 1;
    let locations = providers::sql_definition(&index, RESOLVER_SQL, line, col);

    assert_eq!(locations.len(), 1, "expected one definition location");
    let location = &locations[0];
    assert!(uri_ends_with(&location.uri, "features.py"));
    assert_eq!(
        location.range.start.line,
        line_index(FEATURES_PY, "class Superhero")
    );
}

#[test]
fn sql_output_column_jumps_to_feature_field() {
    let project = write_project();
    let index = build(&project);

    let line = line_index(RESOLVER_SQL, "select name");
    let col = col_of(RESOLVER_SQL, line, "name") + 1;
    let locations = providers::sql_definition(&index, RESOLVER_SQL, line, col);

    assert_eq!(locations.len(), 1);
    assert!(uri_ends_with(&locations[0].uri, "features.py"));
    assert_eq!(
        locations[0].range.start.line,
        line_index(FEATURES_PY, "    name: str")
    );
}

#[test]
fn underscore_relationship_member_jumps_to_field() {
    let project = write_project();
    let index = build(&project);

    let line = line_index(FEATURES_PY, "expression=_.children");
    let col = col_of(FEATURES_PY, line, "children") + 1;
    let locations =
        providers::python_definition(&index, &project.features_path, FEATURES_PY, line, col);

    assert_eq!(locations.len(), 1, "expected to resolve _.children");
    assert_eq!(
        locations[0].range.start.line,
        line_index(FEATURES_PY, "    children: DataFrame[Child]")
    );
}

#[test]
fn nested_underscore_member_resolves_through_relationship() {
    let project = write_project();
    let index = build(&project);

    // The first `date` in `_.date < _.chalk_now` is scoped to the `children`
    // relationship, so it resolves to `Child.date`.
    let line = line_index(FEATURES_PY, "_.date < _.chalk_now");
    let col = col_of(FEATURES_PY, line, "date") + 1;
    let locations =
        providers::python_definition(&index, &project.features_path, FEATURES_PY, line, col);

    assert_eq!(locations.len(), 1, "expected to resolve nested _.date");
    assert_eq!(
        locations[0].range.start.line,
        line_index(FEATURES_PY, "    date: int")
    );
}

#[test]
fn underscore_completion_lists_enclosing_class_members() {
    let project = write_project();
    let index = build(&project);

    // Cursor right after `_.` in `expression=_.children`.
    let line = line_index(FEATURES_PY, "expression=_.children");
    let col = col_of(FEATURES_PY, line, "children");
    let items =
        providers::python_completion(&index, &project.features_path, FEATURES_PY, line, col);

    let labels: Vec<&str> = items.iter().map(|item| item.label.as_str()).collect();
    assert!(labels.contains(&"id"), "labels: {labels:?}");
    assert!(labels.contains(&"children"), "labels: {labels:?}");
    assert!(labels.contains(&"child_count"), "labels: {labels:?}");
}

#[test]
fn underscore_completion_inside_relationship_lists_related_class_members() {
    let project = write_project();
    let index = build(&project);

    // Cursor right after `_.` in `_.date` (inside `_.children[...]`).
    let line = line_index(FEATURES_PY, "_.date < _.chalk_now");
    let col = col_of(FEATURES_PY, line, "date");
    let items =
        providers::python_completion(&index, &project.features_path, FEATURES_PY, line, col);

    let labels: Vec<&str> = items.iter().map(|item| item.label.as_str()).collect();
    // Child's members, not Parent's.
    assert!(labels.contains(&"date"), "labels: {labels:?}");
    assert!(labels.contains(&"id"), "labels: {labels:?}");
    assert!(!labels.contains(&"children"), "labels: {labels:?}");
    assert!(!labels.contains(&"child_count"), "labels: {labels:?}");
}

#[test]
fn overlay_serves_unsaved_edits() {
    // An open buffer with an extra field that is not yet on disk should still be
    // visible to completion via the overlay filesystem.
    let project = write_project();

    // Add a `nickname` field to `Parent` (anchored on its unique `children`
    // field) that exists only in the buffer, not on disk.
    let edited = FEATURES_PY.replace(
        "    id: int\n    children: DataFrame[Child]",
        "    id: int\n    nickname: str\n    children: DataFrame[Child]",
    );
    assert!(edited.contains("nickname"), "replacement should apply");
    let mut open_docs = HashMap::new();
    open_docs.insert(project.features_path.clone(), edited.clone());
    let index = build_project_index(&project.root, &open_docs).expect("index should build");

    let line = line_index(&edited, "expression=_.children");
    let col = col_of(&edited, line, "children");
    let items =
        providers::python_completion(&index, &project.features_path, &edited, line, col);
    let labels: Vec<&str> = items.iter().map(|item| item.label.as_str()).collect();
    assert!(labels.contains(&"nickname"), "labels: {labels:?}");
}

#[test]
fn definition_returns_empty_when_class_is_missing() {
    let dir = TempDir::new().unwrap();
    let root = dir.path();
    fs::write(root.join("chalk.yaml"), "project: test\n").unwrap();
    // No python files at all.
    let index = build_project_index(root, &HashMap::new()).expect("index should build");

    let sql = "-- resolves: nonexistent\nselect a from t";
    let locations = providers::sql_definition(&index, sql, 0, col_of(sql, 0, "nonexistent") + 1);
    assert!(locations.is_empty());
    let _ = Path::new(root);
}
