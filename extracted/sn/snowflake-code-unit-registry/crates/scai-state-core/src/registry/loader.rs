//! Strict storage loader for registry code units.
//!
//! This module centralizes scan/parse/ID-validation rules so query and refresh
//! paths share one consistent loading behavior.

use std::collections::{HashMap, HashSet};

use serde_json::value::RawValue;
use serde_json::Value;

use crate::error::*;
use crate::generated::types::CodeUnit;
use crate::migration::{CURRENT_SCHEMA_VERSION, SCHEMA_VERSION_FIELD};

use super::storage::index::Prefilter;
use super::{paths, project_unit, CodeUnitRegistry};

/// Loads registry code units from storage using strict validation rules.
///
/// The loader enforces storage-key/ID invariants and treats malformed input as a
/// hard error instead of silently skipping files.
pub(super) struct RegistryLoader<'a> {
    registry: &'a CodeUnitRegistry,
}

impl<'a> RegistryLoader<'a> {
    /// Create a loader bound to the target registry.
    pub(super) fn new(registry: &'a CodeUnitRegistry) -> Self {
        Self { registry }
    }

    /// Read all code units from the registry with strict validation.
    ///
    /// Documents are read in chunks and parsed in parallel using rayon. Each
    /// document is independently deserialized and validated, then results
    /// are collected.
    ///
    /// This method:
    /// - Returns an error on malformed JSON
    /// - Validates that each unit's `id` field (if present) matches its storage key
    /// - Derives `id` from the storage key when `id` is `None`
    /// - Guarantees every returned unit has a valid, unique `id`
    pub(super) fn read_all_units(&self) -> Result<Vec<CodeUnit>> {
        self.registry
            .storage
            .load_all(|key, text| self.parse_checked(key, text))?
            .into_iter()
            .collect()
    }

    /// Read only the units that may satisfy `prefilter`, with the same strict
    /// validation as [`Self::read_all_units`] — or `None` when the backend
    /// can't push the prefilter down. The result is a superset of the
    /// matches; callers must still apply the original predicate.
    pub(super) fn read_candidate_units(
        &self,
        prefilter: &Prefilter,
    ) -> Result<Option<Vec<CodeUnit>>> {
        self.registry
            .storage
            .load_candidates(prefilter, |key, text| self.parse_checked(key, text))?
            .map(|units| units.into_iter().collect())
            .transpose()
    }

    /// Read all units projected to `fields`, decoding only the top-level keys
    /// the projection needs.
    ///
    /// Same result as [`Self::read_all_units`] followed by projection: every
    /// top-level `CodeUnit` field deserializes independently of its siblings,
    /// so a unit decoded from just the needed keys has exactly the values a
    /// full decode would have there. Each document's JSON syntax,
    /// `schemaVersion`, and storage-key/ID match are still checked; fields
    /// outside the projection are not deserialized, so a type error in one of
    /// them no longer fails the read. Documents that need migration (or are
    /// otherwise unusual) take the full path, with its exact errors.
    pub(super) fn read_all_projected(&self, fields: &[&str]) -> Result<Vec<CodeUnit>> {
        let top_level: HashSet<&str> = fields
            .iter()
            .map(|f| f.split('.').next().unwrap_or(f))
            .collect();
        self.registry
            .storage
            .load_all(|key, text| self.parse_projected(key, text?, fields, &top_level))?
            .into_iter()
            .collect()
    }

    fn parse_projected(
        &self,
        key: &str,
        text: String,
        fields: &[&str],
        top_level: &HashSet<&str>,
    ) -> Result<CodeUnit> {
        // Scans (and syntax-checks) the whole document without building
        // values for the keys the projection doesn't need.
        let Ok(raw) = serde_json::from_str::<HashMap<String, &RawValue>>(&text) else {
            return self.parse_full_projected(key, text, fields);
        };
        let at_current_version = match raw.get(SCHEMA_VERSION_FIELD) {
            None => CURRENT_SCHEMA_VERSION == 1,
            Some(v) => serde_json::from_str::<i64>(v.get()).ok() == Some(CURRENT_SCHEMA_VERSION),
        };
        let id_matches_key = match raw.get("id") {
            None => true,
            Some(v) => match serde_json::from_str::<Option<String>>(v.get()) {
                Ok(id) => id.is_none_or(|id| id == key),
                Err(_) => false,
            },
        };
        if !at_current_version || !id_matches_key {
            return self.parse_full_projected(key, text, fields);
        }

        let mut needed = serde_json::Map::new();
        for (name, value) in &raw {
            if top_level.contains(name.as_str()) {
                needed.insert(name.clone(), serde_json::from_str(value.get())?);
            }
        }
        let mut needed = Value::Object(needed);
        paths::normalize_value_paths(&mut needed);
        let mut code_unit: CodeUnit = serde_json::from_value(needed)?;
        if code_unit.id.is_none() {
            code_unit.id = Some(key.to_string());
        }
        project_unit(&code_unit, fields)
    }

    /// Full strict parse, then projection.
    fn parse_full_projected(&self, key: &str, text: String, fields: &[&str]) -> Result<CodeUnit> {
        project_unit(&self.parse_checked(key, Ok(text))?, fields)
    }

    /// Parse one stored document and enforce the storage-key/ID invariants.
    fn parse_checked(&self, key: &str, text: Result<String>) -> Result<CodeUnit> {
        parse_stored(key, &text?, || self.registry.storage.location(key))
    }
}

/// The strict load of the document stored under `key`: JSON syntax, schema
/// migration, deserialization into `CodeUnit`, and an embedded `id` that is
/// absent (then set to `key`) or equal to `key`. `location` names the
/// document in the ID-mismatch error.
///
/// Every strict read goes through this, and so does the SQLite index's
/// classification of a document as *regular* (`storage::index::derive`):
/// the index can only vouch for documents this accepts, so the two must
/// never drift apart.
pub(super) fn parse_stored(
    key: &str,
    text: &str,
    location: impl FnOnce() -> String,
) -> Result<CodeUnit> {
    let mut code_unit = CodeUnitRegistry::parse_unit(text)?;

    match &code_unit.id {
        Some(id) if id != key => {
            return ValidationSnafu {
                message: format!(
                    "ID/filename mismatch: file '{}' contains id '{}'",
                    location(),
                    id,
                ),
            }
            .fail();
        }
        None => {
            code_unit.id = Some(key.to_string());
        }
        Some(_) => {}
    }

    Ok(code_unit)
}
