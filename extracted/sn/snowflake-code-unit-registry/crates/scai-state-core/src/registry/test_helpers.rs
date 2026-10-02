//! Shared test helpers for `registry` submodule unit tests.
//!
//! Keep these fixtures lightweight and focused on graph/query behavior.

use std::collections::HashMap;

use crate::generated::types::{CodeUnit, Dependencies, Dependency, Part, PartTarget, TargetFormat};

/// Minimal `CodeUnit` fixture with only an ID.
pub(crate) fn unit(id: &str) -> CodeUnit {
    CodeUnit {
        id: Some(id.to_string()),
        ..Default::default()
    }
}

/// Minimal `CodeUnit` fixture marked as missing (referenced but absent).
pub(crate) fn unit_missing(id: &str) -> CodeUnit {
    let mut u = unit(id);
    u.is_missing = true;
    u
}

/// Build a minimal `CodeUnit` with direct dependency IDs.
///
/// `None` entries are serialized as dependencies with no target ID.
pub(crate) fn unit_with_dependencies(id: &str, dependency_ids: &[Option<&str>]) -> CodeUnit {
    let mut unit = unit(id);
    unit.dependencies = Some(Dependencies {
        depends_on: dependency_ids
            .iter()
            .map(|dep_id| Dependency {
                id: dep_id.map(ToString::to_string),
                is_missing: None,
                relation_types: vec!["SELECT".to_string()],
            })
            .collect(),
        ..Default::default()
    });
    unit
}

/// Build an ID -> index lookup for fixture vectors.
pub(crate) fn id_index(units: &[CodeUnit]) -> HashMap<String, usize> {
    units
        .iter()
        .enumerate()
        .filter_map(|(index, unit)| unit.id.as_ref().map(|id| (id.clone(), index)))
        .collect()
}

/// Build an ETL-style CodeUnit with parts, each carrying its own dependencies.
///
/// Each `(part_id, dep_ids)` tuple becomes one part with `Some(Dependencies {...})`.
pub(crate) fn etl_unit_with_part_deps(
    id: &str,
    parts_with_deps: &[(&str, &[Option<&str>])],
) -> CodeUnit {
    let parts = parts_with_deps
        .iter()
        .map(|(part_id, dep_ids)| Part {
            id: Some(part_id.to_string()),
            name: Some(part_id.to_string()),
            part_type: Some("dataFlow".to_string()),
            target: Some(PartTarget {
                path: Some(format!("converted/{part_id}/")),
                format: Some(TargetFormat::Dbt),
                ..Default::default()
            }),
            dependencies: Some(Dependencies {
                depends_on: dep_ids
                    .iter()
                    .map(|dep_id| Dependency {
                        id: dep_id.map(ToString::to_string),
                        is_missing: None,
                        relation_types: vec!["SELECT".to_string()],
                    })
                    .collect(),
                ..Default::default()
            }),
            ..Default::default()
        })
        .collect();

    let mut u = unit(id);
    u.kind = Some(crate::generated::types::Kind::Etl);
    u.parts = Some(parts);
    u
}
