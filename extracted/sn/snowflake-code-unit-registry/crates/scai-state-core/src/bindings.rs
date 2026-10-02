//! Script-bindings BTEQ flow surfaces: structural validation against a
//! script's declared `scriptBindings[]` and query-time literal substitution
//! over the `source.*` / `target.*` string slots of returned units.
//!
//! Lives outside `registry` because it operates on already-loaded `CodeUnit`
//! values rather than on registry state.

use std::collections::{HashMap, HashSet};

use crate::error::{Error, Result};
use crate::generated::types::CodeUnit;

/// Structural name + value-presence diff between a script's declared
/// `scriptBindings[].name` set and a caller-supplied `name → value` map.
///
/// See [`validate_bindings`] for semantics. Output vectors are sorted ASCII-betically
/// so that callers can format diffs deterministically.
#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct BindingDiff {
    /// Names declared in `scriptBindings[]` but absent from `provided`.
    pub missing: Vec<String>,
    /// Names present in `provided` but not declared in `scriptBindings[]`.
    pub extra: Vec<String>,
    /// Names declared in `scriptBindings[]` and present in `provided` whose value is empty
    /// after `str::trim` (i.e. empty or whitespace-only).
    pub empty: Vec<String>,
}

/// Diff a script's declared `scriptBindings[].name` set against a caller-supplied
/// `name → value` map.
///
/// Narrow by design: no kind awareness, no value-shape rules, no `__REPLACE_ME__`
/// sentinel rejection, no source/target asymmetry, no file pre-flight, no sensitive-
/// binding policy. Those are test-domain rules and live in the runner-side resolver.
/// Callers (runner, linter, planner) decide policy on the returned diff.
///
/// A binding declared with `name: None` is skipped — it's a malformed declaration,
/// not a structural mismatch.
///
/// Returns `Err(Error::ValidationError)` only on misuse — when `script.kind` is not
/// [`Kind::Script`].
pub fn validate_bindings(
    script: &CodeUnit,
    provided: &HashMap<String, String>,
) -> Result<BindingDiff> {
    use crate::generated::types::Kind;

    if script.kind != Some(Kind::Script) {
        return Err(Error::validation(format!(
            "validate_bindings expects a code unit with kind=script, got {:?}",
            script.kind
        )));
    }

    let declared: HashSet<&str> = script
        .script_bindings
        .as_deref()
        .unwrap_or(&[])
        .iter()
        .filter_map(|b| b.name.as_deref())
        .collect();

    let mut missing: Vec<String> = declared
        .iter()
        .filter(|name| !provided.contains_key(**name))
        .map(|s| (*s).to_string())
        .collect();

    let mut extra: Vec<String> = provided
        .keys()
        .filter(|k| !declared.contains(k.as_str()))
        .cloned()
        .collect();

    let mut empty: Vec<String> = declared
        .iter()
        .filter_map(|name| {
            provided
                .get(*name)
                .filter(|v| v.trim().is_empty())
                .map(|_| (*name).to_string())
        })
        .collect();

    missing.sort();
    extra.sort();
    empty.sort();

    Ok(BindingDiff {
        missing,
        extra,
        empty,
    })
}

/// Single-pass literal substitution against a token map.
///
/// At each byte position, the longest key that matches as a literal prefix
/// is replaced with its mapped value; replacement values are emitted as-is
/// and never re-scanned, so substitutions cannot chain-react. When no key
/// matches, one UTF-8 code point is copied through and scanning resumes.
fn substitute_literal(s: &str, sorted_keys: &[&str], bindings: &HashMap<String, String>) -> String {
    let mut out = String::with_capacity(s.len());
    let mut i = 0;
    while i < s.len() {
        let mut matched = false;
        for &key in sorted_keys {
            if s[i..].starts_with(key) {
                out.push_str(&bindings[key]);
                i += key.len();
                matched = true;
                break;
            }
        }
        if !matched {
            let ch_len = s[i..].chars().next().map(char::len_utf8).unwrap_or(1);
            out.push_str(&s[i..i + ch_len]);
            i += ch_len;
        }
    }
    out
}

/// Apply literal-token substitution to every string slot under `source.*`
/// and `target.*` of `unit`, and to each `scriptMetadata.IO[].path`'s per-side
/// `source` / `target` slots. Other fields (including `dependsOn[].id`) are
/// untouched. No-op when `bindings` is empty.
///
/// `scriptMetadata.IO[].path` resolution substitutes the per-side `source` and
/// `target` slots in place using the same `bindings` map — the same generic,
/// map-key-based pass `parameterizedReference` slots use, with no wrapper
/// spelling baked into CUR. A source-side map (e.g. keyed by `${name}`)
/// resolves `source` and leaves `target` untouched, and vice versa.
pub(crate) fn apply_bindings(unit: &mut CodeUnit, bindings: &HashMap<String, String>) {
    if bindings.is_empty() {
        return;
    }
    let mut sorted_keys: Vec<&str> = bindings.keys().map(String::as_str).collect();
    sorted_keys.sort_by_key(|k| std::cmp::Reverse(k.len()));

    if let Some(src) = unit.source.as_mut() {
        for slot in [
            &mut src.canonical_name,
            &mut src.database,
            &mut src.schema,
            &mut src.package,
            &mut src.name,
        ] {
            if let Some(v) = slot.as_mut() {
                *v = substitute_literal(v, &sorted_keys, bindings);
            }
        }
    }
    if let Some(tgt) = unit.target.as_mut() {
        for slot in [
            &mut tgt.canonical_name,
            &mut tgt.database,
            &mut tgt.schema,
            &mut tgt.name,
        ] {
            if let Some(v) = slot.as_mut() {
                *v = substitute_literal(v, &sorted_keys, bindings);
            }
        }
    }

    // Substitute scriptMetadata.IO path slots in place — the same generic pass
    // applied to source.* / target.* above.
    if let Some(meta) = unit.script_metadata.as_mut() {
        for entry in meta.io.iter_mut() {
            if let Some(path) = entry.path.as_mut() {
                for slot in [&mut path.source, &mut path.target] {
                    if let Some(v) = slot.as_mut() {
                        *v = substitute_literal(v, &sorted_keys, bindings);
                    }
                }
            }
        }
    }
}
