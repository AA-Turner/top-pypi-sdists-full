//! Shared in-memory state for registry query operations.
//!
//! `InMemoryRegistry` owns strict-loaded units and indexing data.
//! `RegistryQuery` provides a read-only traversal view over that state.

use std::collections::{HashMap, HashSet};

use rayon::prelude::*;

use crate::error::*;
use crate::generated::types::CodeUnit;

use super::graph::RegistryGraph;
use super::loader::RegistryLoader;
use super::query::RegistryQuery;
use super::{project_fields, CodeUnitRegistry};

/// Per-call in-memory registry state for query operations.
///
/// The state owns loaded units and a lightweight ID index for fast
/// dependency traversal. It is intentionally short-lived and rebuilt for each
/// top-level query call.
#[derive(Debug)]
pub(super) struct InMemoryRegistry {
    units: Vec<CodeUnit>,
    id_to_index: HashMap<String, usize>,
}

impl InMemoryRegistry {
    /// Build state from strict registry storage.
    ///
    /// Malformed JSON or ID/filename mismatches surface as errors here.
    pub(super) fn build(registry: &CodeUnitRegistry) -> Result<Self> {
        Ok(Self::new(RegistryLoader::new(registry).read_all_units()?))
    }

    /// Construct state from already loaded units.
    ///
    /// IDs are indexed for O(1)-ish dependency lookups. Units without IDs are
    /// ignored by the index (strict loading should already assign IDs).
    fn new(units: Vec<CodeUnit>) -> Self {
        let id_to_index = units
            .iter()
            .enumerate()
            .filter_map(|(index, unit)| unit.id.as_ref().map(|id| (id.clone(), index)))
            .collect();
        Self { units, id_to_index }
    }

    /// Create a read-only query view over this state.
    pub(super) fn query(&self) -> RegistryQuery<'_> {
        RegistryQuery::new(&self.units, &self.id_to_index)
    }

    /// Create a mutation-oriented graph view over this in-memory dataset.
    pub(super) fn graph(&mut self) -> RegistryGraph<'_> {
        RegistryGraph::new(&mut self.units, &self.id_to_index)
    }

    /// Access a unit by its position index.
    pub(super) fn unit(&self, index: usize) -> &CodeUnit {
        &self.units[index]
    }

    pub(super) fn unit_mut(&mut self, index: usize) -> &mut CodeUnit {
        &mut self.units[index]
    }

    /// Add a new unit and return its position index.
    pub(super) fn add_unit(&mut self, unit: CodeUnit) -> usize {
        let index = self.units.len();
        if let Some(id) = unit.id.as_ref() {
            self.id_to_index.insert(id.clone(), index);
        }
        self.units.push(unit);
        index
    }

    /// Remove a unit by ID. Clears the unit's ID so the graph treats it as
    /// absent (other units' dependencies on it will resolve as missing).
    pub(super) fn remove_unit(&mut self, id: &str) {
        if let Some(idx) = self.id_to_index.remove(id) {
            self.units[idx].id = None;
            self.units[idx].dependencies = None;
        }
    }

    /// Look up a unit's position index by its string ID.
    pub(super) fn id_to_index(&self, id: &str) -> Option<usize> {
        self.id_to_index.get(id).copied()
    }

    /// Clone all units for snapshotting before a destructive operation.
    pub(super) fn snapshot_units(&self) -> Vec<CodeUnit> {
        self.units.clone()
    }

    /// Return all units, optionally projected to a subset of fields.
    ///
    /// Consumes state to avoid cloning large vectors. Output order follows
    /// strict-load iteration order.
    pub(super) fn all_units(self, fields: Option<&[&str]>) -> Result<Vec<CodeUnit>> {
        Self::project_units(self.units, fields)
    }

    /// Materialize selected units, preserving strict-load iteration order.
    ///
    /// The resulting set is optionally projected to requested fields.
    pub(super) fn selected_units(
        self,
        selected: HashSet<usize>,
        fields: Option<&[&str]>,
    ) -> Result<Vec<CodeUnit>> {
        let units: Vec<CodeUnit> = self
            .units
            .into_iter()
            .enumerate()
            .filter_map(|(index, unit)| selected.contains(&index).then_some(unit))
            .collect();
        Self::project_units(units, fields)
    }

    /// Apply optional field projection to a unit collection.
    ///
    /// Projection is performed via JSON (`project_fields`) and deserialized back
    /// into `CodeUnit`, so projection shape errors are returned as `Error`.
    /// Runs in parallel via rayon when projection is active.
    fn project_units(units: Vec<CodeUnit>, fields: Option<&[&str]>) -> Result<Vec<CodeUnit>> {
        match fields {
            None => Ok(units),
            Some(fields) => units
                .into_par_iter()
                .map(|unit| {
                    let json_value = serde_json::to_value(&unit)?;
                    let projected = project_fields(&json_value, fields)?;
                    serde_json::from_value(projected).map_err(Error::from)
                })
                .collect(),
        }
    }
}
