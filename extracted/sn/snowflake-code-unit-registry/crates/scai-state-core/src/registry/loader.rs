//! Strict file-system loader for registry code units.
//!
//! This module centralizes scan/parse/ID-validation rules so query and refresh
//! paths share one consistent loading behavior.

use rayon::prelude::*;

use crate::error::*;
use crate::generated::types::CodeUnit;

use super::CodeUnitRegistry;

/// Loads registry code units from disk using strict validation rules.
///
/// The loader enforces filename/ID invariants and treats malformed input as a
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
    /// Files are read and parsed in parallel using rayon. Each file is
    /// independently deserialized and validated, then results are collected.
    ///
    /// This method:
    /// - Returns an error on malformed JSON
    /// - Validates that each unit's `id` field (if present) matches filename stem
    /// - Derives `id` from the filename stem when `id` is `None`
    /// - Guarantees every returned unit has a valid, unique `id`
    pub(super) fn read_all_units(&self) -> Result<Vec<CodeUnit>> {
        let registry_dir = self.registry.registry_dir();

        if !registry_dir.exists() {
            return Ok(Vec::new());
        }

        let paths = super::paths::json_file_paths(&registry_dir)?;

        paths
            .par_iter()
            .map(|path| {
                let mut code_unit = self.registry.read_json(path)?;

                let filename_stem = super::paths::filename_stem(path)?;

                match &code_unit.id {
                    Some(id) if id != filename_stem => {
                        return ValidationSnafu {
                            message: format!(
                                "ID/filename mismatch: file '{}' contains id '{}'",
                                path.display(),
                                id,
                            ),
                        }
                        .fail();
                    }
                    None => {
                        code_unit.id = Some(filename_stem.to_string());
                    }
                    Some(_) => {}
                }

                Ok(code_unit)
            })
            .collect()
    }
}
