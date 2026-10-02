//! Read-only query traversal view over in-memory registry state.
//!
//! Encapsulates filter matching and transitive dependency expansion over
//! already-loaded units.

use std::collections::{HashMap, HashSet};

use rayon::prelude::*;
use serde_json::Value;

use crate::error::Result;
use crate::generated::types::CodeUnit;

/// Read-only query traversal view over an `InMemoryRegistry`.
pub(super) struct RegistryQuery<'a> {
    units: &'a [CodeUnit],
    id_to_index: &'a HashMap<String, usize>,
}

impl<'a> RegistryQuery<'a> {
    pub(super) fn new(units: &'a [CodeUnit], id_to_index: &'a HashMap<String, usize>) -> Self {
        Self { units, id_to_index }
    }

    /// Return indices of units matching the provided JSON predicate.
    ///
    /// Each unit is serialized to `serde_json::Value` and tested against the
    /// predicate in parallel via rayon.
    pub(super) fn matching_indices<F>(&self, predicate: F) -> Result<HashSet<usize>>
    where
        F: Fn(&Value) -> bool + Sync,
    {
        self.units
            .par_iter()
            .enumerate()
            .filter_map(|(index, unit)| match serde_json::to_value(unit) {
                Ok(json_value) if predicate(&json_value) => Some(Ok(index)),
                Ok(_) => None,
                Err(e) => Some(Err(e.into())),
            })
            .collect::<Result<HashSet<usize>>>()
    }

    /// Expand a selected set to include all transitive dependencies.
    ///
    /// Traversal follows `dependencies.depends_on[*].id` using an explicit stack
    /// (depth-first). Missing or unknown dependency IDs are ignored.
    pub(super) fn include_transitive_dependencies(&self, selected: &mut HashSet<usize>) {
        let mut stack: Vec<usize> = selected.iter().copied().collect();

        while let Some(index) = stack.pop() {
            if let Some(dependencies) = self.units[index].dependencies.as_ref() {
                for dependency in &dependencies.depends_on {
                    if let Some(dep_id) = dependency.id.as_deref() {
                        if let Some(dep_index) = self.id_to_index.get(dep_id).copied() {
                            if selected.insert(dep_index) {
                                stack.push(dep_index);
                            }
                        }
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use super::RegistryQuery;
    use crate::registry::test_helpers::{id_index, unit, unit_with_dependencies};

    #[test]
    fn matching_indices_filters_by_predicate() {
        let units = vec![unit("a"), unit("b"), unit("c")];
        let index = id_index(&units);
        let query = RegistryQuery::new(&units, &index);

        let selected = query
            .matching_indices(|json| json.pointer("/id").and_then(|v| v.as_str()) == Some("b"))
            .unwrap();

        assert_eq!(selected, HashSet::from([1usize]));
    }

    #[test]
    fn include_transitive_dependencies_expands_dependency_chain() {
        let units = vec![
            unit_with_dependencies("a", &[Some("b")]),
            unit_with_dependencies("b", &[Some("c")]),
            unit("c"),
        ];
        let index = id_index(&units);
        let query = RegistryQuery::new(&units, &index);

        let mut selected = HashSet::from([0usize]);
        query.include_transitive_dependencies(&mut selected);

        assert_eq!(selected, HashSet::from([0usize, 1usize, 2usize]));
    }

    #[test]
    fn include_transitive_dependencies_ignores_unknown_and_missing_dependency_ids() {
        let units = vec![unit_with_dependencies("a", &[Some("does-not-exist"), None])];
        let index = id_index(&units);
        let query = RegistryQuery::new(&units, &index);

        let mut selected = HashSet::from([0usize]);
        query.include_transitive_dependencies(&mut selected);

        assert_eq!(selected, HashSet::from([0usize]));
    }
}
