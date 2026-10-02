//! Script-I/O BTEQ flow surface: structural validation of a script's declared
//! `scriptMetadata.IO[]` against the file references a test case supplies.
//!
//! Parallel to [`crate::bindings`] — operates on already-loaded `CodeUnit`
//! values rather than registry state, and leaves all test-domain policy to the
//! caller (the runner). It answers one structural question: do the test's
//! declared file entries line up, by path reference and direction, with the
//! `scriptMetadata.IO[]` the converter recorded?

use std::collections::BTreeMap;

use crate::error::{Error, Result};
use crate::generated::types::{CodeUnit, Kind, ScriptIoDirection, ScriptIoPath, ScriptIoPathKind};

/// A test-declared file reference — one `reads[]`/`writes[]` entry of the YAML
/// `files:` block, normalised for diffing against `scriptMetadata.IO[]`.
///
/// The caller maps each YAML entry to a `(direction, path)` pair: a `binding:`
/// entry becomes `ScriptIoPath { kind: binding, name }`, a `path:` entry
/// becomes `ScriptIoPath { kind: literal, source, target }`.
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ProvidedIo {
    /// Direction the test expects (`read` = `.IMPORT`, `write` = `.EXPORT`).
    pub direction: ScriptIoDirection,
    /// Path reference (binding name or literal path) the entry points at.
    pub path: ScriptIoPath,
}

/// Structural diff between a script's declared `scriptMetadata.IO[]` and the
/// file references a test case supplies.
///
/// Each element is a stable identity key — `binding:<name>` or
/// `literal:<source>`. Output vectors are ASCII-sorted so callers can format
/// diffs deterministically.
#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ScriptIoDiff {
    /// Keys declared in `scriptMetadata.IO[]` but absent from `provided`.
    pub missing: Vec<String>,
    /// Keys present in `provided` but not declared in `scriptMetadata.IO[]`.
    pub extra: Vec<String>,
    /// Keys present on both sides whose `direction` disagrees (e.g. declared
    /// `write`, supplied `read`).
    pub direction_mismatch: Vec<String>,
}

/// Stable identity key for a path reference, or `None` when the reference is
/// malformed (no `kind`, or the `kind`'s payload field is empty) — such an entry
/// is skipped rather than reported, mirroring [`crate::bindings::validate_bindings`]'s
/// handling of a `name: None` binding.
///
/// Bindings key on `name` (side-neutral); literals key on `source` (the
/// source-side text), falling back to `target` when only that side is present.
fn path_key(path: &ScriptIoPath) -> Option<String> {
    match path.kind? {
        ScriptIoPathKind::Binding => path.name.as_deref().map(|n| format!("binding:{n}")),
        ScriptIoPathKind::Literal => path
            .source
            .as_deref()
            .or(path.target.as_deref())
            .map(|v| format!("literal:{v}")),
    }
}

/// Diff a script's declared `scriptMetadata.IO[]` against the file references a
/// test case supplies.
///
/// Narrow by design: no fixture existence, no `compare:` compatibility, no
/// `opaque`/untestable refusal, no reachability reasoning. Those are
/// test-domain rules and live in the runner. This helper reports only the
/// structural mismatch — declared-but-not-supplied, supplied-but-not-declared,
/// and direction divergence on matched path references.
///
/// Entries on either side with a malformed `path` (no resolvable key) are
/// skipped. When the same path key appears on more than one declared entry the
/// last one wins (same-path multi-write is rejected upstream at extraction).
///
/// Returns `Err(Error::ValidationError)` only on misuse — when `script.kind`
/// is not [`Kind::Script`].
pub fn validate_script_io(script: &CodeUnit, provided: &[ProvidedIo]) -> Result<ScriptIoDiff> {
    if script.kind != Some(Kind::Script) {
        return Err(Error::validation(format!(
            "validate_script_io expects a code unit with kind=script, got {:?}",
            script.kind
        )));
    }

    // key -> declared direction (Option: a malformed entry may lack one)
    let mut declared: BTreeMap<String, Option<ScriptIoDirection>> = BTreeMap::new();
    if let Some(meta) = script.script_metadata.as_ref() {
        for entry in &meta.io {
            if let Some(key) = entry.path.as_ref().and_then(path_key) {
                declared.insert(key, entry.direction);
            }
        }
    }

    // key -> supplied direction
    let mut supplied: BTreeMap<String, ScriptIoDirection> = BTreeMap::new();
    for p in provided {
        if let Some(key) = path_key(&p.path) {
            supplied.insert(key, p.direction);
        }
    }

    let mut missing: Vec<String> = Vec::new();
    let mut direction_mismatch: Vec<String> = Vec::new();
    for (key, declared_dir) in &declared {
        match supplied.get(key) {
            None => missing.push(key.clone()),
            Some(supplied_dir) => {
                if let Some(d) = declared_dir {
                    if d != supplied_dir {
                        direction_mismatch.push(key.clone());
                    }
                }
            }
        }
    }

    let mut extra: Vec<String> = supplied
        .keys()
        .filter(|k| !declared.contains_key(*k))
        .cloned()
        .collect();

    // BTreeMap iteration is already ordered; sort defensively so the contract
    // ("ASCII-sorted") holds regardless of how the maps are built.
    missing.sort();
    extra.sort();
    direction_mismatch.sort();

    Ok(ScriptIoDiff {
        missing,
        extra,
        direction_mismatch,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::types::{ScriptIoEntry, ScriptMetadata};

    fn binding_path(name: &str) -> ScriptIoPath {
        ScriptIoPath {
            kind: Some(ScriptIoPathKind::Binding),
            name: Some(name.to_string()),
            source: None,
            target: None,
        }
    }

    fn literal_path(value: &str) -> ScriptIoPath {
        ScriptIoPath {
            kind: Some(ScriptIoPathKind::Literal),
            name: None,
            source: Some(value.to_string()),
            target: None,
        }
    }

    fn script(io: Vec<ScriptIoEntry>) -> CodeUnit {
        CodeUnit {
            kind: Some(Kind::Script),
            script_metadata: Some(ScriptMetadata { io }),
            ..Default::default()
        }
    }

    fn entry(direction: ScriptIoDirection, path: ScriptIoPath) -> ScriptIoEntry {
        ScriptIoEntry {
            direction: Some(direction),
            path: Some(path),
            ..Default::default()
        }
    }

    fn provided(direction: ScriptIoDirection, path: ScriptIoPath) -> ProvidedIo {
        ProvidedIo { direction, path }
    }

    #[test]
    fn clean_when_provided_matches_declared() {
        let unit = script(vec![
            entry(ScriptIoDirection::Write, binding_path("err_file")),
            entry(
                ScriptIoDirection::Read,
                literal_path("/etl/in/customers.dat"),
            ),
        ]);
        let diff = validate_script_io(
            &unit,
            &[
                provided(ScriptIoDirection::Write, binding_path("err_file")),
                provided(
                    ScriptIoDirection::Read,
                    literal_path("/etl/in/customers.dat"),
                ),
            ],
        )
        .unwrap();
        assert_eq!(diff, ScriptIoDiff::default());
    }

    #[test]
    fn reports_missing_and_extra() {
        let unit = script(vec![entry(
            ScriptIoDirection::Write,
            binding_path("err_file"),
        )]);
        let diff = validate_script_io(
            &unit,
            &[provided(ScriptIoDirection::Read, binding_path("in_file"))],
        )
        .unwrap();
        assert_eq!(diff.missing, vec!["binding:err_file".to_string()]);
        assert_eq!(diff.extra, vec!["binding:in_file".to_string()]);
        assert!(diff.direction_mismatch.is_empty());
    }

    #[test]
    fn reports_direction_mismatch() {
        let unit = script(vec![entry(
            ScriptIoDirection::Write,
            binding_path("err_file"),
        )]);
        let diff = validate_script_io(
            &unit,
            &[provided(ScriptIoDirection::Read, binding_path("err_file"))],
        )
        .unwrap();
        assert!(diff.missing.is_empty());
        assert!(diff.extra.is_empty());
        assert_eq!(
            diff.direction_mismatch,
            vec!["binding:err_file".to_string()]
        );
    }

    #[test]
    fn skips_malformed_path_entries() {
        let unit = script(vec![entry(
            ScriptIoDirection::Write,
            ScriptIoPath {
                kind: Some(ScriptIoPathKind::Binding),
                name: None, // malformed: binding with no name
                source: None,
                target: None,
            },
        )]);
        let diff = validate_script_io(&unit, &[]).unwrap();
        assert_eq!(diff, ScriptIoDiff::default());
    }

    #[test]
    fn empty_script_metadata_is_clean() {
        let unit = script(vec![]);
        let diff = validate_script_io(&unit, &[]).unwrap();
        assert_eq!(diff, ScriptIoDiff::default());
    }

    #[test]
    fn errors_on_non_script_kind() {
        let unit = CodeUnit {
            kind: Some(Kind::DatabaseObject),
            ..Default::default()
        };
        let err = validate_script_io(&unit, &[]).unwrap_err();
        assert!(err.to_string().contains("kind=script"));
    }
}
