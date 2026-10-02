//! Shared path utilities for registry file operations.

use std::fs;
use std::path::{Path, PathBuf};

use serde_json::Value;

use crate::error::*;
use crate::generated::types::CodeUnit;
use snafu::OptionExt;

/// Collect all `.json` file paths from a directory.
pub(crate) fn json_file_paths(dir: &Path) -> Result<Vec<PathBuf>> {
    let mut paths = Vec::new();
    for entry in fs::read_dir(dir)? {
        let path = entry?.path();
        if path.extension().is_some_and(|e| e == "json") {
            paths.push(path);
        }
    }
    Ok(paths)
}

/// Extract the filename (e.g. "abc.json") from a path as a `String`.
pub(crate) fn filename_of(path: &Path) -> String {
    path.file_name()
        .unwrap_or_default()
        .to_string_lossy()
        .into_owned()
}

/// Extract the filename stem (e.g. "abc" from "abc.json") as a `&str`.
///
/// Returns `Err(ValidationError)` if the stem is missing or contains
/// non-UTF-8 bytes.
pub(crate) fn filename_stem(path: &Path) -> Result<&str> {
    path.file_stem()
        .and_then(|s| s.to_str())
        .context(ValidationSnafu {
            message: format!("Cannot derive ID from filename: {}", path.display()),
        })
}

// ── Path normalization ──────────────────────────────────────────────────

/// Normalize a path string for registry storage.
///
/// On every platform we strip a redundant `./` prefix. The `\` → `/`
/// rewrite is **Windows-only** by design:
///
/// * On Windows, `\` and `/` are interchangeable separators, so collapsing
///   to `/` produces a single canonical form that is portable across hosts
///   and round-trips through Git, JSON, and shell tooling without escaping.
/// * On Unix-like systems, `\` is a *valid filename byte* with no separator
///   meaning. Identifiers sourced from SQL (e.g. `[LSH\external]`) or archives
///   produced on Windows can legitimately appear in on-disk names, and
///   rewriting them silently corrupts paths and breaks `File::open`.
///
/// Do not remove the `cfg!(windows)` guard without auditing every caller
/// that resolves the stored string back to a real filesystem path.
pub(crate) fn normalize_path_str(path: &str) -> String {
    let normalized = if cfg!(windows) {
        path.replace('\\', "/")
    } else {
        path.to_string()
    };
    normalized
        .strip_prefix("./")
        .unwrap_or(&normalized)
        .to_string()
}

/// Normalize a `std::path::Path` to the registry's stored string form.
pub(crate) fn normalize_os_path(path: &Path) -> String {
    normalize_path_str(&path.to_string_lossy())
}

/// Normalize all file path fields on a CodeUnit in place.
/// Uses the schema-generated `FILE_PATH_FIELDS` constant so new path
/// fields added to the schema are automatically covered.
/// Returns `true` if any path was changed.
pub(crate) fn normalize_code_unit_paths(unit: &mut CodeUnit) -> bool {
    use crate::generated::file_path_fields::FILE_PATH_FIELDS;

    let Ok(mut json) = serde_json::to_value(&*unit) else {
        return false;
    };

    let mut changed = false;
    for path in FILE_PATH_FIELDS {
        if let Some(val) = navigate_path_mut(&mut json, path) {
            if let Some(s) = val.as_str() {
                let norm = normalize_path_str(s);
                if norm != s {
                    *val = Value::String(norm);
                    changed = true;
                }
            }
        }
    }

    if changed {
        if let Ok(normalized) = serde_json::from_value(json) {
            *unit = normalized;
        }
    }
    changed
}

// ── JSON Value navigation helpers ───────────────────────────────────────

/// Traverse a JSON Value by path segments (read-only).
/// Returns `None` if any segment is missing.
pub(crate) fn navigate_path<'a>(value: &'a Value, path: &[&str]) -> Option<&'a Value> {
    let mut current = value;
    for segment in path {
        current = current.get(*segment)?;
    }
    Some(current)
}

/// Traverse a JSON Value by path segments (mutable).
/// Returns `None` if any segment is missing -- does NOT create intermediates.
pub(crate) fn navigate_path_mut<'a>(value: &'a mut Value, path: &[&str]) -> Option<&'a mut Value> {
    let mut current = value;
    for segment in path {
        current = current.as_object_mut()?.get_mut(*segment)?;
    }
    Some(current)
}

/// Traverse a JSON Value by path segments (mutable), creating
/// intermediate objects if they don't exist.
pub(crate) fn ensure_path<'a>(value: &'a mut Value, path: &[&str]) -> Option<&'a mut Value> {
    let mut current = value;
    for segment in path {
        if !current.is_object() {
            return None;
        }
        current = current
            .as_object_mut()
            .unwrap()
            .entry(*segment)
            .or_insert_with(|| Value::Object(serde_json::Map::new()));
    }
    Some(current)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    // ── normalize_path_str ──────────────────────────────────────────────

    #[cfg(windows)]
    #[test]
    fn normalize_path_str_converts_windows_separators() {
        assert_eq!(
            normalize_path_str(r"source\Sales\file.sql"),
            "source/Sales/file.sql"
        );
        assert_eq!(
            normalize_path_str(r"source\Sales/file.sql"),
            "source/Sales/file.sql"
        );
        assert_eq!(normalize_path_str("./source/file.sql"), "source/file.sql");
        assert_eq!(normalize_path_str(r".\source\file.sql"), "source/file.sql");
        assert_eq!(normalize_path_str("source/file.sql"), "source/file.sql");
        assert_eq!(normalize_path_str(""), "");
    }

    #[cfg(not(windows))]
    #[test]
    fn normalize_path_str_preserves_literal_backslashes_on_unix() {
        assert_eq!(
            normalize_path_str(r"source\Sales\file.sql"),
            r"source\Sales\file.sql"
        );
        assert_eq!(
            normalize_path_str(r"source\Sales/file.sql"),
            r"source\Sales/file.sql"
        );
        assert_eq!(normalize_path_str("./source/file.sql"), "source/file.sql");
        assert_eq!(
            normalize_path_str(r".\source\file.sql"),
            r".\source\file.sql"
        );
        assert_eq!(normalize_path_str("source/file.sql"), "source/file.sql");
        assert_eq!(normalize_path_str(""), "");
    }

    // ── navigate_path (read-only) ───────────────────────────────────────

    #[test]
    fn navigate_path_reaches_nested_value() {
        let v = json!({"a": {"b": {"c": 42}}});
        assert_eq!(navigate_path(&v, &["a", "b", "c"]), Some(&json!(42)));
    }

    #[test]
    fn navigate_path_returns_none_on_missing_segment() {
        let v = json!({"a": {"b": 1}});
        assert_eq!(navigate_path(&v, &["a", "x"]), None);
    }

    #[test]
    fn navigate_path_empty_segments_returns_root() {
        let v = json!({"a": 1});
        assert_eq!(navigate_path(&v, &[]), Some(&v));
    }

    // ── navigate_path_mut ───────────────────────────────────────────────

    #[test]
    fn navigate_path_mut_modifies_in_place() {
        let mut v = json!({"a": {"b": "old"}});
        *navigate_path_mut(&mut v, &["a", "b"]).unwrap() = json!("new");
        assert_eq!(v, json!({"a": {"b": "new"}}));
    }

    #[test]
    fn navigate_path_mut_returns_none_on_missing() {
        let mut v = json!({"a": 1});
        assert!(navigate_path_mut(&mut v, &["a", "b"]).is_none());
    }

    #[test]
    fn navigate_path_mut_returns_none_on_non_object() {
        let mut v = json!("scalar");
        assert!(navigate_path_mut(&mut v, &["a"]).is_none());
    }

    // ── ensure_path ─────────────────────────────────────────────────────

    #[test]
    fn ensure_path_creates_intermediates() {
        let mut v = json!({});
        let target = ensure_path(&mut v, &["a", "b"]).unwrap();
        *target = json!("created");
        assert_eq!(v, json!({"a": {"b": "created"}}));
    }

    #[test]
    fn ensure_path_reuses_existing_objects() {
        let mut v = json!({"a": {"x": 1}});
        let target = ensure_path(&mut v, &["a", "b"]).unwrap();
        *target = json!(2);
        assert_eq!(v, json!({"a": {"x": 1, "b": 2}}));
    }

    #[test]
    fn ensure_path_returns_none_when_intermediate_is_non_object() {
        let mut v = json!({"a": "scalar"});
        assert!(ensure_path(&mut v, &["a", "b"]).is_none());
    }

    #[test]
    fn ensure_path_empty_segments_returns_root() {
        let mut v = json!({"a": 1});
        let target = ensure_path(&mut v, &[]).unwrap();
        assert_eq!(*target, json!({"a": 1}));
    }
}
