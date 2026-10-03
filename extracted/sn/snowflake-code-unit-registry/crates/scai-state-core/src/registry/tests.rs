use super::*;
use crate::generated::types::{
    Dependencies, Dependency, Kind as CodeUnitKind, ObjectType as CodeUnitObjectType, Part,
    PartTarget, SourceFormat, SourceMetadata, SourcePlatform, TargetFormat, TargetMetadata,
};
use crate::migration::SCHEMA_VERSION_FIELD;

fn temp_dir() -> tempfile::TempDir {
    tempfile::tempdir().unwrap()
}

fn schema_enum_values(definition_name: &str) -> Vec<String> {
    let schema: serde_json::Value =
        serde_json::from_str(include_str!("../../schemas/code-unit.schema.json")).unwrap();
    schema
        .get("definitions")
        .and_then(|definitions| definitions.get(definition_name))
        .and_then(|definition| definition.get("enum"))
        .and_then(|values| values.as_array())
        .unwrap_or_else(|| panic!("missing schema enum definition: {definition_name}"))
        .iter()
        .map(|value| value.as_str().unwrap().to_string())
        .collect()
}

fn assert_schema_enum_round_trips<T>(definition_name: &str)
where
    T: std::str::FromStr + ToString,
{
    let schema_values = schema_enum_values(definition_name);
    let generated_values = schema_values
        .iter()
        .map(|value| value.parse::<T>().ok().unwrap().to_string())
        .collect::<Vec<_>>();
    assert_eq!(generated_values, schema_values);
}

/// Select the platform-specific expected value for an assertion.
macro_rules! platform_path {
    (unix: $u:literal, windows: $w:literal $(,)?) => {
        if cfg!(windows) {
            $w
        } else {
            $u
        }
    };
}

/// Create a registry with no built-in hooks (no checksum, no dependency
/// refresh). Use this in tests that don't need hook side-effects.
fn init_bare(path: &std::path::Path) -> CodeUnitRegistry {
    let root = path.to_path_buf();
    let registry_dir = root.join("registry");
    fs::create_dir_all(registry_dir.join(".locks")).unwrap();
    CodeUnitRegistry {
        root,
        hooks: vec![],
        in_hook: std::sync::atomic::AtomicBool::new(false),
    }
}

fn make_code_unit(id: &str, name: &str, object_type: CodeUnitObjectType) -> CodeUnit {
    CodeUnit {
        id: Some(id.to_string()),
        kind: Some(CodeUnitKind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(object_type),
            database: Some("DB".to_string()),
            schema: Some("dbo".to_string()),
            name: Some(name.to_string()),
            ..Default::default()
        }),
        target: Some(TargetMetadata {
            object_type: Some(object_type),
            database: Some("DB".to_string()),
            schema: Some("DBO".to_string()),
            name: Some(name.to_uppercase()),
            ..Default::default()
        }),
        ..Default::default()
    }
}

fn sorted_ids(units: Vec<CodeUnit>) -> Vec<String> {
    let mut ids: Vec<String> = units.into_iter().filter_map(|unit| unit.id).collect();
    ids.sort_unstable();
    ids
}

fn set_dependencies(unit: &mut CodeUnit, deps: &[(&str, Option<bool>)]) {
    use crate::generated::types::{Dependencies, Dependency};

    if deps.is_empty() {
        unit.dependencies = None;
        return;
    }

    unit.dependencies = Some(Dependencies {
        depends_on: deps
            .iter()
            .map(|(id, is_missing)| Dependency {
                id: Some((*id).to_string()),
                is_missing: *is_missing,
                relation_types: vec!["SELECT".to_string()],
            })
            .collect(),
        ..Default::default()
    });
}

fn set_dependency_ids(unit: &mut CodeUnit, dep_ids: &[&str]) {
    let deps: Vec<(&str, Option<bool>)> = dep_ids.iter().map(|dep_id| (*dep_id, None)).collect();
    set_dependencies(unit, &deps);
}

fn normalize_datetime_fields(val: &mut serde_json::Value, paths: &[&str]) {
    for path in paths {
        if let Some(v) = val.pointer_mut(path) {
            *v = serde_json::Value::String("<datetime>".to_string());
        }
    }
}

fn normalize_part_dependencies(val: &mut serde_json::Value, remove_has_transitive: bool) {
    if let Some(parts) = val.pointer_mut("/parts") {
        if let Some(arr) = parts.as_array_mut() {
            for part in arr {
                if let Some(deps) = part.pointer_mut("/dependencies/dependsOn") {
                    if let Some(dep_arr) = deps.as_array_mut() {
                        for dep in dep_arr {
                            if let Some(v) = dep.pointer_mut("/isMissing") {
                                *v = serde_json::Value::Bool(true);
                            }
                        }
                    }
                }
                if let Some(deps) = part.pointer_mut("/dependencies") {
                    let deps_obj = deps.as_object_mut().unwrap();
                    deps_obj.remove("requiredBy");
                    if remove_has_transitive {
                        deps_obj.remove("hasTransitiveMissingDependencies");
                    }
                }
            }
        }
    }
}

#[test]
fn test_exists_before_and_after_init() {
    let dir = temp_dir();
    assert!(!CodeUnitRegistry::exists(dir.path()));
    CodeUnitRegistry::init(dir.path()).unwrap();
    assert!(CodeUnitRegistry::exists(dir.path()));
}

#[test]
fn test_init_registry() {
    let dir = temp_dir();
    let _registry = CodeUnitRegistry::init(dir.path()).unwrap();
    assert!(dir.path().join("registry").exists());
    assert!(dir.path().join("registry").join(".locks").exists());
}

#[test]
fn test_open_registry() {
    let dir = temp_dir();
    let _registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let registry2 = CodeUnitRegistry::open(dir.path()).unwrap();
    assert_eq!(registry2.root(), dir.path().to_path_buf());
}

#[test]
fn test_id_to_path() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let id = "abcdef12-3456-7890-abcd-ef1234567890";
    let expected = dir.path().join("registry").join(format!("{}.json", id));
    assert_eq!(registry.id_to_path(id), expected);
}

#[test]
fn test_create_batch_success() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut batch = vec![
        make_code_unit("id1", "Table1", CodeUnitObjectType::Table),
        make_code_unit("id2", "Table2", CodeUnitObjectType::Table),
        make_code_unit("id3", "Proc1", CodeUnitObjectType::Procedure),
    ];

    let result = registry.create_batch(&mut batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 3);
    assert!(result.succeeded.contains(&"id1".to_string()));
    assert!(result.succeeded.contains(&"id2".to_string()));
    assert!(result.succeeded.contains(&"id3".to_string()));
    assert_eq!(result.failed.len(), 0);
    assert_eq!(result.total(), 3);

    // Verify all were created
    let all = registry.find_all(FindOptions::default()).unwrap();
    assert_eq!(all.len(), 3);
}

#[test]
fn test_create_batch_partial_failure_duplicate_ids() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);

    // First create one
    registry.create(&mut cu1, None).unwrap();

    // Now batch create with duplicate
    let mut batch = vec![
        make_code_unit("id1", "Table1", CodeUnitObjectType::Table), // duplicate - should fail
        make_code_unit("id2", "Table2", CodeUnitObjectType::Table), // new - should succeed
    ];

    let result = registry.create_batch(&mut batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 1);
    assert!(result.succeeded.contains(&"id2".to_string()));
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "id1");
    assert_eq!(result.failed[0].error.code, 1004); // CodeUnitAlreadyExists
    assert!(result.failed[0].error.message.contains("already exists"));
}

#[test]
fn test_update_batch_success() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    let batch: Vec<(&str, Vec<(&str, Value)>)> = vec![
        (
            "id1",
            vec![("source.name", Value::String("UpdatedTable1".to_string()))],
        ),
        (
            "id2",
            vec![("source.name", Value::String("UpdatedTable2".to_string()))],
        ),
    ];

    let result = registry.update_batch(&batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 2);
    assert!(result.succeeded.contains(&"id1".to_string()));
    assert!(result.succeeded.contains(&"id2".to_string()));
    assert_eq!(result.failed.len(), 0);

    // Verify updates
    let loaded1 = registry.get_by_id("id1", None).unwrap();
    assert_eq!(loaded1.source.unwrap().name.unwrap(), "UpdatedTable1");
}

/// A successful write must never surface the trailing directory-fsync as a
/// failed unit. Before the `#[cfg(not(windows))]` guard on `sync()`, the flush
/// opened the registry dir as a `File`, which Windows rejects with
/// ERROR_ACCESS_DENIED (os error 5), producing a synthetic `_sync` failure on
/// every write even though the rename had already persisted (SNOW-3421123).
#[test]
fn test_update_batch_reports_no_sync_failure() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();

    let batch: Vec<(&str, Vec<(&str, Value)>)> = vec![(
        "id1",
        vec![("source.name", Value::String("Updated".to_string()))],
    )];

    let result = registry.update_batch(&batch, None).unwrap();
    assert!(
        !result.failed.iter().any(|f| f.id == "_sync"),
        "durability flush must not surface as a `_sync` unit failure: {:?}",
        result.failed
    );
    assert_eq!(result.succeeded, vec!["id1".to_string()]);
}

/// User-initiated writes go through the durable-rename path. It must still
/// land the new content and leave no `.json.tmp` behind. On Windows this
/// exercises the write-through `MoveFileExW`; on POSIX, the plain rename whose
/// durability comes from the batch-level directory fsync (SNOW-3421123).
#[test]
fn test_durable_write_leaves_no_temp_file() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let batch: Vec<(&str, Vec<(&str, Value)>)> = vec![(
        "id1",
        vec![("source.name", Value::String("Renamed".to_string()))],
    )];
    registry.update_batch(&batch, None).unwrap();

    let leftover: Vec<_> = fs::read_dir(dir.path().join("registry"))
        .unwrap()
        .filter_map(|e| e.ok())
        .map(|e| e.path())
        .filter(|p| p.extension().and_then(|s| s.to_str()) == Some("tmp"))
        .collect();
    assert!(leftover.is_empty(), "leftover temp files: {leftover:?}");
    assert_eq!(
        registry
            .get_by_id("id1", None)
            .unwrap()
            .source
            .unwrap()
            .name
            .unwrap(),
        "Renamed"
    );
}

#[test]
fn test_update_batch_partial_failure_not_found() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();

    let batch: Vec<(&str, Vec<(&str, Value)>)> = vec![
        (
            "id1",
            vec![("source.name", Value::String("Updated".to_string()))],
        ),
        (
            "nonexistent",
            vec![("source.name", Value::String("X".to_string()))],
        ),
    ];

    let result = registry.update_batch(&batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 1);
    assert!(result.succeeded.contains(&"id1".to_string()));
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "nonexistent");
    assert_eq!(result.failed[0].error.code, 1003); // CodeUnitNotFound
    assert!(result.failed[0].error.message.contains("not found"));
}

#[test]
fn test_update_where_success() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);
    let mut cu3 = make_code_unit("id3", "Proc1", CodeUnitObjectType::Procedure);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    let updates: Vec<(&str, Value)> = vec![("source.database", Value::String("NEWDB".to_string()))];

    let result = registry
        .update_where("source.objectType = 'table'", &updates, None)
        .unwrap();
    assert_eq!(result.succeeded.len(), 2);
    assert!(result.succeeded.contains(&"id1".to_string()));
    assert!(result.succeeded.contains(&"id2".to_string()));
    assert_eq!(result.failed.len(), 0);

    // Verify only tables were updated
    let loaded1 = registry.get_by_id("id1", None).unwrap();
    assert_eq!(loaded1.source.unwrap().database.unwrap(), "NEWDB");

    let loaded3 = registry.get_by_id("id3", None).unwrap();
    assert_eq!(loaded3.source.unwrap().database.unwrap(), "DB"); // unchanged
}

#[test]
fn test_update_where_no_matches() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();

    let updates: Vec<(&str, Value)> = vec![("source.database", Value::String("NEWDB".to_string()))];

    let result = registry
        .update_where("objectType = 'view'", &updates, None)
        .unwrap();
    assert_eq!(result.succeeded.len(), 0);
    assert_eq!(result.failed.len(), 0);
}

#[test]
fn test_find_all_include_dependencies_expands_transitive_matches() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut root = make_code_unit("root", "RootProc", CodeUnitObjectType::Procedure);
    let mut mid = make_code_unit("mid", "MidTable", CodeUnitObjectType::Table);
    let mut leaf = make_code_unit("leaf", "LeafView", CodeUnitObjectType::View);

    set_dependencies(&mut root, &[("mid", Some(false))]);
    set_dependencies(&mut mid, &[("leaf", Some(false))]);

    registry.create(&mut root, None).unwrap();
    registry.create(&mut mid, None).unwrap();
    registry.create(&mut leaf, None).unwrap();

    let filtered = registry
        .find_all(FindOptions {
            filter: Some("source.name = 'RootProc'"),
            ..FindOptions::default()
        })
        .unwrap();
    let filtered_ids = sorted_ids(filtered);
    assert_eq!(filtered_ids, vec!["root".to_string()]);

    let expanded = registry
        .find_all(FindOptions {
            filter: Some("source.name = 'RootProc'"),
            include_dependencies: true,
            ..FindOptions::default()
        })
        .unwrap();
    let expanded_ids = sorted_ids(expanded);
    assert_eq!(
        expanded_ids,
        vec!["leaf".to_string(), "mid".to_string(), "root".to_string()]
    );
}

#[test]
fn test_find_all_include_dependencies_noop_without_filter() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut root = make_code_unit("root", "RootProc", CodeUnitObjectType::Procedure);
    let mut dep = make_code_unit("dep", "DepTable", CodeUnitObjectType::Table);
    set_dependencies(&mut root, &[("dep", Some(false))]);

    registry.create(&mut root, None).unwrap();
    registry.create(&mut dep, None).unwrap();

    let all_default = registry.find_all(FindOptions::default()).unwrap();
    let all_include = registry
        .find_all(FindOptions {
            include_dependencies: true,
            ..FindOptions::default()
        })
        .unwrap();

    let default_ids = sorted_ids(all_default);
    let include_ids = sorted_ids(all_include);
    assert_eq!(default_ids, include_ids);
}

#[test]
fn test_batch_result_default() {
    let result = BatchResult::default();
    assert_eq!(result.succeeded.len(), 0);
    assert_eq!(result.failed.len(), 0);
    assert_eq!(result.total(), 0);
}

#[test]
fn test_create_generates_id_when_missing() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = CodeUnit {
        id: None,
        kind: Some(CodeUnitKind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            database: None,
            schema: None,
            name: None,
            ..Default::default()
        }),
        ..Default::default()
    };

    let id = registry.create(&mut cu, None).unwrap();
    assert_eq!(id.len(), 36); // UUID v4 without dashes
    assert_eq!(cu.id, Some(id.clone())); // ID was set on the code unit

    // Verify it was created
    let loaded = registry.get_by_id(&id, None).unwrap();
    assert_eq!(loaded.id, Some(id));
}

#[test]
fn test_create_uses_existing_id() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("my_custom_id", "Table1", CodeUnitObjectType::Table);

    let id = registry.create(&mut cu, None).unwrap();
    assert_eq!(id, "my_custom_id");

    // Verify it was created with the provided ID
    let loaded = registry.get_by_id("my_custom_id", None).unwrap();
    assert_eq!(loaded.id, Some("my_custom_id".to_string()));
}

#[test]
fn test_delete_syncs() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let mut cu = make_code_unit("id_del", "T", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    registry.delete("id_del").unwrap();
    assert!(!registry.id_to_path("id_del").exists());
}

#[test]
fn test_upsert_creates_new() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("upsert1", "Table1", CodeUnitObjectType::Table);
    let id = registry.upsert(&mut cu, None).unwrap();
    assert_eq!(id, "upsert1");

    let loaded = registry.get_by_id("upsert1", None).unwrap();
    assert_eq!(
        loaded.source.as_ref().unwrap().name.as_deref(),
        Some("Table1")
    );
}

#[test]
fn test_upsert_merges_existing() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    use crate::generated::types::{ArtifactsEntry, Files};
    // Create initial — include an artifacts path to verify merge preserves it
    let mut cu = make_code_unit("upsert2", "Table1", CodeUnitObjectType::Table);
    cu.files = Some(Files {
        artifacts: Some(ArtifactsEntry {
            path: Some("artifacts/dbo/Tables/Table1".to_string()),
        }),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    // Upsert with updated source name but no target
    let mut patch = CodeUnit {
        id: Some("upsert2".to_string()),
        source: Some(SourceMetadata {
            name: Some("UpdatedTable1".to_string()),
            ..Default::default()
        }),
        ..Default::default()
    };

    let id = registry.upsert(&mut patch, None).unwrap();
    assert_eq!(id, "upsert2");

    let loaded = registry.get_by_id("upsert2", None).unwrap();
    // Source name should be updated
    assert_eq!(
        loaded.source.as_ref().unwrap().name.as_deref(),
        Some("UpdatedTable1")
    );
    // Target should still be present from original create
    assert!(loaded.target.is_some());
    assert_eq!(
        loaded.target.as_ref().unwrap().name.as_deref(),
        Some("TABLE1")
    );
    // Artifacts should be preserved from original create
    assert_eq!(
        loaded.files.unwrap().artifacts.unwrap().path.as_deref(),
        Some("artifacts/dbo/Tables/Table1")
    );

    fs::remove_dir_all(&dir).unwrap();
}

#[test]
fn test_upsert_generates_id_when_missing() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = CodeUnit {
        kind: Some(CodeUnitKind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            ..Default::default()
        }),
        ..Default::default()
    };

    let id = registry.upsert(&mut cu, None).unwrap();
    assert_eq!(id.len(), 36); // UUID v4 with hyphens (8-4-4-4-12)
    assert_eq!(cu.id, Some(id.clone()));
}

#[test]
fn test_upsert_batch() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    // Create one existing
    let mut existing = make_code_unit("ub1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut existing, None).unwrap();

    // Batch upsert: one existing (merge) + one new (create)
    let mut batch = vec![
        {
            let mut cu = make_code_unit("ub1", "UpdatedTable1", CodeUnitObjectType::Table);
            cu.target = None; // don't touch target
            cu
        },
        make_code_unit("ub2", "Table2", CodeUnitObjectType::Table),
    ];

    let result = registry.upsert_batch(&mut batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 2);
    assert_eq!(result.failed.len(), 0);

    // ub1 should have merged source name but kept original target
    let loaded = registry.get_by_id("ub1", None).unwrap();
    assert_eq!(
        loaded.source.as_ref().unwrap().name.as_deref(),
        Some("UpdatedTable1")
    );
    assert!(loaded.target.is_some());

    // ub2 should be brand new
    let loaded2 = registry.get_by_id("ub2", None).unwrap();
    assert_eq!(
        loaded2.source.as_ref().unwrap().name.as_deref(),
        Some("Table2")
    );
}

#[test]
fn test_error_codes() {
    let err = RegistryNotFoundSnafu { path: "/tmp/x" }.build();
    assert_eq!(err.error_code_i32(), 1001);

    let err = CodeUnitNotFoundSnafu { id: "abc" }.build();
    assert_eq!(err.error_code_i32(), 1003);

    let err = FilterSnafu { message: "bad" }.build();
    assert_eq!(err.error_code_i32(), 1011);
}

// ── find_by_object tests ─────────────────────────────────────────────

#[test]
fn test_find_by_object_match_by_object_type() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);
    let mut cu3 = make_code_unit("id3", "Proc1", CodeUnitObjectType::Procedure);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    // Match by source.objectType = table
    let partial = serde_json::json!({ "source": { "objectType": "table" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 2);
    assert_eq!(
        sorted_ids(results),
        vec!["id1".to_string(), "id2".to_string()]
    );

    // Match by source.objectType = procedure
    let partial = serde_json::json!({ "source": { "objectType": "procedure" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id3".to_string()));
}

#[test]
fn test_find_by_object_match_nested_fields() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);

    // cu2 has a different schema
    cu2.source = Some(SourceMetadata {
        object_type: Some(CodeUnitObjectType::Table),
        database: Some("DB".to_string()),
        schema: Some("sales".to_string()),
        name: Some("Table2".to_string()),
        ..Default::default()
    });

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Match by source.schema = "dbo"
    let partial = serde_json::json!({ "source": { "schema": "dbo" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));

    // Match by source.schema = "sales"
    let partial = serde_json::json!({ "source": { "schema": "sales" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id2".to_string()));
}

#[test]
fn test_find_by_object_multiple_fields() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Proc1", CodeUnitObjectType::Procedure);
    let mut cu3 = make_code_unit("id3", "Table2", CodeUnitObjectType::Table);

    // cu3 has a different schema
    cu3.source = Some(SourceMetadata {
        object_type: Some(CodeUnitObjectType::Table),
        database: Some("DB".to_string()),
        schema: Some("sales".to_string()),
        name: Some("Table2".to_string()),
        ..Default::default()
    });

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    // Match source.objectType = table AND source.schema = dbo
    let partial = serde_json::json!({
        "source": { "objectType": "table", "schema": "dbo" }
    });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));
}

#[test]
fn test_find_by_object_no_matches() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();

    // Match source.objectType = view (no views exist)
    let partial = serde_json::json!({ "source": { "objectType": "view" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 0);
}

#[test]
fn test_find_by_object_empty_registry() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let partial = serde_json::json!({ "objectType": "table" });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 0);
}

#[test]
fn test_find_by_object_empty_partial_matches_all() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Proc1", CodeUnitObjectType::Procedure);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Empty partial matches all code units
    let partial = serde_json::json!({});
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 2);
}

#[test]
fn test_find_by_object_with_field_projection() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);
    let mut cu3 = make_code_unit("id3", "Proc1", CodeUnitObjectType::Procedure);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    // Match tables, project only id and source
    let partial = serde_json::json!({ "source": { "objectType": "table" } });
    let fields = vec!["id", "source"];
    let results = registry.find_by_object(&partial, Some(&fields)).unwrap();
    assert_eq!(results.len(), 2);

    // Projected results should have source but NOT target
    for cu in &results {
        assert!(cu.id.is_some());
        assert!(cu.source.is_some());
        assert!(cu.target.is_none());
        assert!(cu.kind.is_none());
    }
}

#[test]
fn test_find_by_object_match_by_kind() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();

    let partial = serde_json::json!({ "kind": "databaseObject" });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);

    let partial = serde_json::json!({ "kind": "script" });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 0);
}

#[test]
fn test_find_by_object_match_by_boolean_field() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);
    cu2.is_missing = true;

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Match isMissing = true
    let partial = serde_json::json!({ "isMissing": true });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id2".to_string()));

    // Match isMissing = false
    let partial = serde_json::json!({ "isMissing": false });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));
}

#[test]
fn test_find_by_object_match_by_source_database_and_name() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);

    cu2.source = Some(SourceMetadata {
        object_type: Some(CodeUnitObjectType::Table),
        database: Some("OTHER_DB".to_string()),
        schema: Some("dbo".to_string()),
        name: Some("Table2".to_string()),
        ..Default::default()
    });

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Match by source database
    let partial = serde_json::json!({ "source": { "database": "DB" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));

    // Match by source database AND name
    let partial = serde_json::json!({
        "source": { "database": "OTHER_DB", "name": "Table2" }
    });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id2".to_string()));

    // Match by source name that doesn't exist
    let partial = serde_json::json!({
        "source": { "database": "DB", "name": "NonExistent" }
    });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 0);
}

#[test]
fn test_find_by_object_match_by_target() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Match by target name
    let partial = serde_json::json!({ "target": { "name": "TABLE1" } });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));
}

#[test]
fn test_find_by_object_match_by_id() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit("id1", "Table1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("id2", "Table2", CodeUnitObjectType::Table);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    // Match by id directly
    let partial = serde_json::json!({ "id": "id1" });
    let results = registry.find_by_object(&partial, None).unwrap();
    assert_eq!(results.len(), 1);
    assert_eq!(results[0].id, Some("id1".to_string()));
}

#[test]
fn test_example_json_roundtrip_fidelity() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let example = include_str!("../../examples/code-unit.example.json");
    let original: serde_json::Value = serde_json::from_str(example).unwrap();

    let mut code_unit: CodeUnit = serde_json::from_str(example).unwrap();
    let id = registry.create(&mut code_unit, None).unwrap();

    let file_path = registry.id_to_path(&id);
    let on_disk = fs::read_to_string(&file_path).unwrap();
    let roundtripped: serde_json::Value = serde_json::from_str(&on_disk).unwrap();

    let mut original_norm = original.clone();
    let mut roundtripped_norm = roundtripped.clone();

    // Auto-refresh reconciles dependency-derived fields. The example's
    // dependencies reference IDs absent from this test registry, so:
    if let Some(v) = original_norm.pointer_mut("/planning/topologicalRank") {
        *v = serde_json::Value::Number(0.into());
    }
    if let Some(v) = original_norm.pointer_mut("/dependencies/hasTransitiveMissingDependencies") {
        *v = serde_json::Value::Bool(true);
    }
    if let Some(deps) = original_norm.pointer_mut("/dependencies/dependsOn") {
        if let Some(arr) = deps.as_array_mut() {
            for dep in arr {
                if let Some(v) = dep.pointer_mut("/isMissing") {
                    *v = serde_json::Value::Bool(true);
                }
            }
        }
    }

    for val in [&mut original_norm, &mut roundtripped_norm] {
        normalize_datetime_fields(
            val,
            &[
                "/updatedAt",
                "/codeStatus/registration/updatedAt",
                "/codeStatus/conversion/updatedAt",
                "/codeStatus/resync/updatedAt",
                "/cloudStatus/testing/updatedAt",
                "/cloudStatus/deployment/updatedAt",
                "/cloudStatus/dataMigration/updatedAt",
                "/cloudStatus/dataValidation/updatedAt",
                "/codeStatus/stabilization/updatedAt",
            ],
        );

        if let Some(deps) = val.pointer_mut("/dependencies") {
            deps.as_object_mut().unwrap().remove("requiredBy");
        }
        normalize_part_dependencies(val, false);
    }

    assert_eq!(
        original_norm, roundtripped_norm,
        "Schema round-trip lost or renamed fields"
    );
}

#[test]
fn test_etl_example_json_roundtrip_fidelity() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let example = include_str!("../../examples/etl-code-unit.example.json");
    let original: serde_json::Value = serde_json::from_str(example).unwrap();

    let mut code_unit: CodeUnit = serde_json::from_str(example).unwrap();
    let id = registry.create(&mut code_unit, None).unwrap();

    let file_path = registry.id_to_path(&id);
    let on_disk = fs::read_to_string(&file_path).unwrap();
    let roundtripped: serde_json::Value = serde_json::from_str(&on_disk).unwrap();

    let mut original_norm = original.clone();
    let mut roundtripped_norm = roundtripped.clone();

    // Graph refresh recomputes topologicalRank
    if let Some(v) = original_norm.pointer_mut("/planning/topologicalRank") {
        *v = serde_json::Value::Number(0.into());
    }

    for val in [&mut original_norm, &mut roundtripped_norm] {
        normalize_datetime_fields(
            val,
            &[
                "/updatedAt",
                "/codeStatus/registration/updatedAt",
                "/codeStatus/assessment/updatedAt",
                "/codeStatus/conversion/updatedAt",
                "/codeStatus/resync/updatedAt",
                "/codeStatus/stabilization/updatedAt",
            ],
        );

        normalize_part_dependencies(val, true);

        let val_obj = val.as_object_mut().unwrap();
        val_obj.remove("dependencies");
    }

    assert_eq!(
        original_norm, roundtripped_norm,
        "ETL example round-trip lost or renamed fields"
    );
}

#[test]
fn test_object_type_macro_roundtrips() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("macro-enum-001", "m1", CodeUnitObjectType::Macro);
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("macro-enum-001", None).unwrap();
    assert_eq!(
        loaded.source.and_then(|s| s.object_type),
        Some(CodeUnitObjectType::Macro)
    );
    assert_eq!(
        loaded.target.and_then(|t| t.object_type),
        Some(CodeUnitObjectType::Macro)
    );
}

#[test]
fn test_object_type_external_table_roundtrips() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ext-tbl-001", "ext1", CodeUnitObjectType::ExternalTable);
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("ext-tbl-001", None).unwrap();
    assert_eq!(
        loaded.source.and_then(|s| s.object_type),
        Some(CodeUnitObjectType::ExternalTable)
    );
    assert_eq!(
        loaded.target.and_then(|t| t.object_type),
        Some(CodeUnitObjectType::ExternalTable)
    );
}

#[test]
fn test_source_package_roundtrips() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("pkg-001", "proc1", CodeUnitObjectType::Procedure);
    cu.source.as_mut().unwrap().package = Some("PKG_BILLING".to_string());
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("pkg-001", None).unwrap();
    assert_eq!(
        loaded.source.as_ref().and_then(|s| s.package.as_deref()),
        Some("PKG_BILLING")
    );
    assert_eq!(
        loaded
            .source
            .as_ref()
            .and_then(|s| s.canonical_name.as_deref()),
        Some("DB.dbo.PKG_BILLING.proc1")
    );
}

#[test]
fn test_loads_legacy_document_without_new_optional_fields() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let legacy_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa";
    let path = dir
        .path()
        .join("registry")
        .join(format!("{legacy_id}.json"));
    let json = r#"{
  "schemaVersion": 1,
  "kind": "databaseObject",
  "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "source": {
    "objectType": "procedure",
    "database": "DB",
    "schema": "dbo",
    "name": "p1"
  },
  "target": {
    "objectType": "procedure",
    "database": "DB",
    "schema": "DBO",
    "name": "P1"
  }
}"#;
    fs::write(&path, json).unwrap();

    let loaded = registry.get_by_id(legacy_id, None).unwrap();
    assert_eq!(
        loaded.source.and_then(|s| s.object_type),
        Some(CodeUnitObjectType::Procedure)
    );
    assert!(loaded.signature.is_none());
}

/// Recursively inject `"required": [all property keys]` into every
/// JSON Schema object that has `"properties"`, including nested objects,
/// `definitions`, and array `items`.  This turns an all-optional schema
/// into one where every property must be present.
fn make_all_properties_required(value: &mut serde_json::Value) {
    let obj = match value.as_object_mut() {
        Some(o) => o,
        None => return,
    };

    if let Some(keys) = obj
        .get("properties")
        .and_then(|p| p.as_object())
        .map(|p| p.keys().cloned().collect::<Vec<_>>())
    {
        obj.insert("required".to_string(), serde_json::json!(keys));
    }

    if let Some(props) = obj.get_mut("properties").and_then(|p| p.as_object_mut()) {
        for prop_schema in props.values_mut() {
            make_all_properties_required(prop_schema);
        }
    }
    if let Some(defs) = obj.get_mut("definitions").and_then(|d| d.as_object_mut()) {
        for def_schema in defs.values_mut() {
            make_all_properties_required(def_schema);
        }
    }
    if let Some(items) = obj.get_mut("items") {
        make_all_properties_required(items);
    }
}

#[test]
fn test_example_json_covers_all_schema_fields() {
    let mut schema: serde_json::Value =
        serde_json::from_str(include_str!("../../schemas/code-unit.schema.json")).unwrap();
    let sql_example: serde_json::Value =
        serde_json::from_str(include_str!("../../examples/code-unit.example.json")).unwrap();
    let etl_example: serde_json::Value =
        serde_json::from_str(include_str!("../../examples/etl-code-unit.example.json")).unwrap();
    let script_example: serde_json::Value =
        serde_json::from_str(include_str!("../../examples/script-code-unit.example.json")).unwrap();
    let custom_example: serde_json::Value =
        serde_json::from_str(include_str!("../../examples/custom-code-unit.example.json")).unwrap();

    make_all_properties_required(&mut schema);

    let validator = jsonschema::validator_for(&schema).expect("Failed to compile modified schema");

    // Collect property paths covered by each example
    let sql_missing: std::collections::HashSet<String> = validator
        .iter_errors(&sql_example)
        .map(|e| format!("{} (at {})", e, e.instance_path()))
        .collect();
    let etl_missing: std::collections::HashSet<String> = validator
        .iter_errors(&etl_example)
        .map(|e| format!("{} (at {})", e, e.instance_path()))
        .collect();
    let script_missing: std::collections::HashSet<String> = validator
        .iter_errors(&script_example)
        .map(|e| format!("{} (at {})", e, e.instance_path()))
        .collect();
    let custom_missing: std::collections::HashSet<String> = validator
        .iter_errors(&custom_example)
        .map(|e| format!("{} (at {})", e, e.instance_path()))
        .collect();

    // A property is only truly missing if no example covers it. Script-gated
    // fields (scriptBindings, scriptMetadata.*) live solely in the script
    // example; databaseObject- and etl-only fields in their own examples;
    // customKind solely in the custom example.
    let uncovered: Vec<String> = sql_missing
        .intersection(&etl_missing)
        .cloned()
        .collect::<std::collections::HashSet<String>>()
        .intersection(&script_missing)
        .cloned()
        .collect::<std::collections::HashSet<String>>()
        .intersection(&custom_missing)
        .map(|s| format!("  {s}"))
        .collect();

    assert!(
        uncovered.is_empty(),
        "Schema properties not covered by any example (SQL, ETL, script, or custom):\n{}\n\
         Each property must appear in at least one example file.\n",
        uncovered.join("\n")
    );
}

// ── Checksum tests ────────────────────────────────────────────────────

/// Write a temp file in the registry's root and return its repo-relative path.
fn write_temp_source(dir: &Path, name: &str, content: &[u8]) -> String {
    let path = dir.join(name);
    fs::write(&path, content).unwrap();
    name.to_string()
}

fn make_code_unit_with_files(
    id: &str,
    source_path: Option<String>,
    converted_path: Option<String>,
    snapshot_path: Option<String>,
) -> CodeUnit {
    use crate::generated::types::{FileEntry, Files};
    let make_entry = |path: Option<String>| {
        path.map(|p| FileEntry {
            path: Some(p),
            checksum: None,
        })
    };
    CodeUnit {
        id: Some(id.to_string()),
        kind: Some(crate::generated::types::Kind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(crate::generated::types::ObjectType::Table),
            database: None,
            schema: None,
            name: None,
            ..Default::default()
        }),
        target: Some(TargetMetadata {
            object_type: Some(crate::generated::types::ObjectType::Table),
            ..Default::default()
        }),
        files: Some(Files {
            source: make_entry(source_path),
            converted: make_entry(converted_path),
            snapshot: make_entry(snapshot_path),
            ..Default::default()
        }),
        ..Default::default()
    }
}

#[test]
fn update_checksum_refreshes_all_changed_files() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "src.sql", b"src v1");
    write_temp_source(dir.path(), "snap.sql", b"snap v1");
    let mut cu =
        make_code_unit_with_files("cs5", Some("src.sql".into()), None, Some("snap.sql".into()));
    registry.create(&mut cu, None).unwrap();
    registry.update_checksum("cs5", ChecksumMode::ALL).unwrap();

    let before = registry.get_by_id("cs5", None).unwrap().files.unwrap();
    let source_before = before.source.unwrap().checksum.unwrap();
    let snapshot_before = before.snapshot.unwrap().checksum.unwrap();

    fs::write(dir.path().join("src.sql"), b"src v2").unwrap();
    fs::write(dir.path().join("snap.sql"), b"snap v2").unwrap();
    registry.update_checksum("cs5", ChecksumMode::ALL).unwrap();

    let after = registry.get_by_id("cs5", None).unwrap().files.unwrap();
    assert_ne!(source_before, after.source.unwrap().checksum.unwrap());
    assert_ne!(snapshot_before, after.snapshot.unwrap().checksum.unwrap());
}

#[test]
fn update_checksum_skips_unchanged_files() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "src.sql", b"src v1");
    write_temp_source(dir.path(), "snap.sql", b"snap v1");
    let mut cu = make_code_unit_with_files(
        "cs5b",
        Some("src.sql".into()),
        None,
        Some("snap.sql".into()),
    );
    registry.create(&mut cu, None).unwrap();
    registry.update_checksum("cs5b", ChecksumMode::ALL).unwrap();

    let before = registry.get_by_id("cs5b", None).unwrap().files.unwrap();
    let source_before = before.source.unwrap().checksum.unwrap();
    let snapshot_before = before.snapshot.unwrap().checksum.unwrap();

    fs::write(dir.path().join("src.sql"), b"src v2").unwrap();
    registry.update_checksum("cs5b", ChecksumMode::ALL).unwrap();

    let after = registry.get_by_id("cs5b", None).unwrap().files.unwrap();
    assert_ne!(source_before, after.source.unwrap().checksum.unwrap());
    assert_eq!(snapshot_before, after.snapshot.unwrap().checksum.unwrap());
}

#[test]
fn validate_checksum_reports_mismatch() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let path = write_temp_source(dir.path(), "mismatch.sql", b"version 1");
    let mut cu = make_code_unit_with_files("cs6", Some(path.clone()), None, None);
    registry.create(&mut cu, None).unwrap();
    registry.update_checksum("cs6", ChecksumMode::ALL).unwrap();

    fs::write(dir.path().join(path), b"version 2").unwrap();
    let report = registry
        .validate_checksum("cs6", ChecksumMode::SOURCE)
        .unwrap();
    let source = report
        .entries
        .iter()
        .find(|e| e.field == "files.source")
        .unwrap();
    assert_eq!(
        source.status,
        crate::checksum::ChecksumValidationStatus::Mismatch
    );
}

#[test]
fn validate_checksum_reports_missing_file() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let path = write_temp_source(dir.path(), "missing.sql", b"payload");
    let mut cu = make_code_unit_with_files("cs7", Some(path.clone()), None, None);
    registry.create(&mut cu, None).unwrap();
    registry.update_checksum("cs7", ChecksumMode::ALL).unwrap();

    fs::remove_file(dir.path().join(path)).unwrap();
    let report = registry
        .validate_checksum("cs7", ChecksumMode::SOURCE)
        .unwrap();
    let source = report
        .entries
        .iter()
        .find(|e| e.field == "files.source")
        .unwrap();
    assert_eq!(
        source.status,
        crate::checksum::ChecksumValidationStatus::MissingFile
    );
}

#[test]
fn test_matches_partial_helper() {
    // Exact match
    assert!(matches_partial(
        &serde_json::json!({"a": 1}),
        &serde_json::json!({"a": 1, "b": 2})
    ));

    // Nested match
    assert!(matches_partial(
        &serde_json::json!({"a": {"x": 1}}),
        &serde_json::json!({"a": {"x": 1, "y": 2}, "b": 3})
    ));

    // Mismatch value
    assert!(!matches_partial(
        &serde_json::json!({"a": 1}),
        &serde_json::json!({"a": 2})
    ));

    // Missing key in target
    assert!(!matches_partial(
        &serde_json::json!({"a": 1}),
        &serde_json::json!({"b": 1})
    ));

    // Empty partial matches everything
    assert!(matches_partial(
        &serde_json::json!({}),
        &serde_json::json!({"a": 1, "b": 2})
    ));

    // Scalar vs object mismatch
    assert!(!matches_partial(
        &serde_json::json!({"a": {"x": 1}}),
        &serde_json::json!({"a": 1})
    ));

    // Array match (exact)
    assert!(matches_partial(
        &serde_json::json!({"a": [1, 2]}),
        &serde_json::json!({"a": [1, 2]})
    ));

    // Array mismatch
    assert!(!matches_partial(
        &serde_json::json!({"a": [1, 2]}),
        &serde_json::json!({"a": [1, 3]})
    ));
}

// ── Refresh tests ────────────────────────────────────────────────────

fn make_unit_with_deps(id: &str, dep_ids: &[&str]) -> CodeUnit {
    let mut unit = make_code_unit(id, id, CodeUnitObjectType::Table);
    set_dependency_ids(&mut unit, dep_ids);
    unit
}

fn read_unit(registry: &CodeUnitRegistry, id: &str) -> CodeUnit {
    let path = registry.root().join("registry").join(format!("{id}.json"));
    registry.read_json(&path).unwrap()
}

#[test]
fn create_auto_refreshes_ranks() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut c = make_unit_with_deps("c", &[]);
    c.planning.get_or_insert_with(Default::default).wave_rank = Some(42);
    let mut b = make_unit_with_deps("b", &["c"]);
    b.planning.get_or_insert_with(Default::default).wave_rank = Some(42);
    let mut a = make_unit_with_deps("a", &["b"]);
    a.planning.get_or_insert_with(Default::default).wave_rank = Some(42);

    registry.create(&mut c, None).unwrap();
    registry.create(&mut b, None).unwrap();
    registry.create(&mut a, None).unwrap();

    let c = read_unit(&registry, "c");
    let b = read_unit(&registry, "b");
    let a = read_unit(&registry, "a");
    assert_eq!(c.planning.as_ref().unwrap().topological_rank, Some(0));
    assert_eq!(b.planning.as_ref().unwrap().topological_rank, Some(1));
    assert_eq!(a.planning.as_ref().unwrap().topological_rank, Some(2));
    assert_eq!(c.planning.unwrap().wave_rank, Some(42));
    assert_eq!(b.planning.unwrap().wave_rank, Some(42));
    assert_eq!(a.planning.unwrap().wave_rank, Some(42));
}

#[test]
fn create_auto_refresh_best_effort_on_cycle() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let id_x = registry
        .create(&mut make_unit_with_deps("x", &["y"]), None)
        .unwrap();
    let id_y = registry
        .create(&mut make_unit_with_deps("y", &["x"]), None)
        .unwrap();

    assert_eq!(id_x, "x");
    assert_eq!(id_y, "y");

    let x = read_unit(&registry, "x");
    assert_eq!(x.planning.unwrap().topological_rank, Some(-1));
    assert!(
        x.dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let y = read_unit(&registry, "y");
    assert_eq!(y.planning.unwrap().topological_rank, Some(-1));
    assert!(
        y.dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );
}

#[test]
fn create_auto_refresh_self_reference() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let id = registry
        .create(&mut make_unit_with_deps("a", &["a"]), None)
        .unwrap();
    assert_eq!(id, "a");

    let a = read_unit(&registry, "a");
    assert_eq!(a.planning.unwrap().topological_rank, Some(0));
    assert_eq!(
        a.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(false)
    );
    assert!(
        !a.dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    registry.refresh_dependencies().unwrap();

    let a_after = read_unit(&registry, "a");
    assert_eq!(a_after.planning.unwrap().topological_rank, Some(0));
}

#[test]
fn create_with_corrupt_sibling_succeeds_without_hooks() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    registry
        .create(&mut make_unit_with_deps("good", &[]), None)
        .unwrap();

    let corrupt_path = registry.root().join("registry").join("corrupt.json");
    std::fs::write(&corrupt_path, "NOT VALID JSON").unwrap();

    registry
        .create(&mut make_unit_with_deps("new_unit", &[]), None)
        .unwrap();

    assert!(registry.id_to_path("new_unit").exists());
}

#[test]
fn create_batch_with_corrupt_sibling_succeeds_without_hooks() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let corrupt_path = registry.root().join("registry").join("corrupt.json");
    std::fs::write(&corrupt_path, "NOT VALID JSON").unwrap();

    let mut batch = vec![
        make_unit_with_deps("b1", &[]),
        make_unit_with_deps("b2", &[]),
    ];
    let result = registry.create_batch(&mut batch, None).unwrap();

    assert_eq!(result.succeeded.len(), 2);
    assert_eq!(result.failed.len(), 0);
}

#[test]
fn refresh_reconciles_dependency_is_missing() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut a = make_code_unit("a", "A", CodeUnitObjectType::Table);
    set_dependencies(&mut a, &[("b", Some(true))]);
    registry.create(&mut a, None).unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();

    registry.refresh_dependencies().unwrap();

    let a_after = read_unit(&registry, "a");
    let dep = &a_after.dependencies.unwrap().depends_on[0];
    assert_eq!(dep.is_missing, Some(false));
}

#[test]
fn refresh_strict_returns_cycle_error() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("x", &["y"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("y", &["x"]), None)
        .unwrap();

    let err = registry.refresh_dependencies().unwrap_err();
    assert_eq!(err.error_code_i32(), 1014);
}

#[test]
fn refresh_empty_registry_is_noop() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.refresh_dependencies().unwrap();
}

#[test]
fn refresh_propagates_transitive_missing() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["missing"]), None)
        .unwrap();

    registry.refresh_dependencies().unwrap();

    let b = read_unit(&registry, "b");
    assert!(
        b.dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let a = read_unit(&registry, "a");
    assert!(
        a.dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );
}

#[test]
fn refresh_is_idempotent() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["missing"]), None)
        .unwrap();

    registry.refresh_dependencies().unwrap();
    let a_first = serde_json::to_value(read_unit(&registry, "a")).unwrap();
    let b_first = serde_json::to_value(read_unit(&registry, "b")).unwrap();

    registry.refresh_dependencies().unwrap();
    let a_second = serde_json::to_value(read_unit(&registry, "a")).unwrap();
    let b_second = serde_json::to_value(read_unit(&registry, "b")).unwrap();

    assert_eq!(a_first, a_second);
    assert_eq!(b_first, b_second);
}

#[test]
fn refresh_preserves_external_writes_in_load_to_write_window() {
    // Contract: `write_json`'s read-modify-write is the defense against
    // *uncooperating* writers (editors, scripts, git, IDEs) modifying
    // `<id>.json` between `refresh_and_sync`'s load and its per-unit write.
    // The advisory `acquire_lock` only coordinates cooperating registry
    // instances; it does not stop external file writes.
    //
    // Any optimization that caches raw JSON at load time and reuses it at
    // write time MUST NOT regress this property. Forward-compat fields
    // added to the file in the load -> write window must survive the
    // refresh.
    use crate::migration::CURRENT_SCHEMA_VERSION;
    use crate::registry::test_hooks::{clear_after_load_hook, set_after_load_hook};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    // Seed a unit directly on disk with no derived state — bypasses the
    // auto-refresh write-hook so refresh_dependencies will mark it dirty
    // and enter the per-unit write loop.
    let path = registry.id_to_path("a");
    let initial = serde_json::json!({
        SCHEMA_VERSION_FIELD: CURRENT_SCHEMA_VERSION,
        "id": "a",
    });
    fs::write(&path, serde_json::to_string_pretty(&initial).unwrap()).unwrap();

    // Hook fires after load + graph refresh, before the first write.
    // Simulates an uncooperating external writer that adds a forward-compat
    // field unknown to the typed `CodeUnit`.
    let inject_path = path.clone();
    set_after_load_hook(move || {
        let mut current: serde_json::Value =
            serde_json::from_str(&fs::read_to_string(&inject_path).unwrap()).unwrap();
        current["futureField"] = serde_json::json!("external-value");
        fs::write(
            &inject_path,
            serde_json::to_string_pretty(&current).unwrap(),
        )
        .unwrap();
    });

    let result = registry.refresh_dependencies();
    clear_after_load_hook();
    result.unwrap();

    let final_value: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
    assert_eq!(
        final_value.get("futureField"),
        Some(&serde_json::json!("external-value")),
        "refresh_dependencies must re-read each file at write time so \
         forward-compat fields added by an uncooperating external writer \
         in the load -> write window are preserved"
    );
    // Sanity: refresh still produced its derived fields (would be missing
    // if we accidentally short-circuited the write).
    assert!(
        final_value.get("planning").is_some(),
        "refresh should have populated planning.topologicalRank for the seeded unit"
    );
}

// ── Scoped refresh integration tests ─────────────────────────────────

#[test]
fn test_create_populates_required_by_on_deps() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();

    let b = read_unit(&registry, "b");
    assert_eq!(b.dependencies.as_ref().unwrap().required_by, vec!["a"]);

    let a = read_unit(&registry, "a");
    assert_eq!(
        a.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(false)
    );
    assert!(
        a.planning.unwrap().topological_rank.unwrap()
            > b.planning.unwrap().topological_rank.unwrap()
    );
}

#[test]
fn test_update_add_dep_refreshes_target() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();

    let b_before = read_unit(&registry, "b");
    assert!(b_before
        .dependencies
        .as_ref()
        .is_none_or(|d| d.required_by.is_empty()));

    registry
        .update(
            "a",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": [{ "id": "b", "relationTypes": ["SELECT"] }]
                }),
            )],
            None,
        )
        .unwrap();

    let b_after = read_unit(&registry, "b");
    assert_eq!(
        b_after.dependencies.as_ref().unwrap().required_by,
        vec!["a"]
    );

    let a_after = read_unit(&registry, "a");
    assert!(
        a_after.planning.unwrap().topological_rank.unwrap()
            > b_after.planning.unwrap().topological_rank.unwrap()
    );
}

#[test]
fn test_update_remove_dep_clears_required_by() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();

    let b_before = read_unit(&registry, "b");
    assert_eq!(
        b_before.dependencies.as_ref().unwrap().required_by,
        vec!["a"]
    );

    registry
        .update(
            "a",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": []
                }),
            )],
            None,
        )
        .unwrap();

    let b_after = read_unit(&registry, "b");
    assert!(b_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());

    let a_after = read_unit(&registry, "a");
    assert_eq!(a_after.planning.unwrap().topological_rank, Some(0));
}

#[test]
fn test_update_swap_dep_refreshes_old_and_new() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();

    assert_eq!(
        read_unit(&registry, "b")
            .dependencies
            .as_ref()
            .unwrap()
            .required_by,
        vec!["a"]
    );

    registry
        .update(
            "a",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": [{ "id": "c", "relationTypes": ["SELECT"] }]
                }),
            )],
            None,
        )
        .unwrap();

    let b_after = read_unit(&registry, "b");
    assert!(b_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());

    let c_after = read_unit(&registry, "c");
    assert_eq!(
        c_after.dependencies.as_ref().unwrap().required_by,
        vec!["a"]
    );
}

#[test]
fn test_update_middle_node_propagates_via_stored_required_by() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    // A -> B -> C
    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["c"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();

    let a_before = read_unit(&registry, "a");
    assert!(
        !a_before
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    // Update B: swap its dep from C to D (D doesn't exist).
    // Seeds will be ["b", "c"] — A is NOT explicitly seeded.
    // A is only reachable via B's stored requiredBy = ["a"].
    registry
        .update(
            "b",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": [{ "id": "d", "relationTypes": ["SELECT"] }]
                }),
            )],
            None,
        )
        .unwrap();

    let b_after = read_unit(&registry, "b");
    assert_eq!(
        b_after.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(true)
    );
    assert!(
        b_after
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let a_after = read_unit(&registry, "a");
    assert!(
        a_after
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let c_after = read_unit(&registry, "c");
    assert!(c_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());
}

#[test]
fn test_delete_refreshes_deps_and_successors() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["c"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();

    let a_before = read_unit(&registry, "a");
    assert_eq!(
        a_before.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(false)
    );
    assert!(
        !a_before
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    registry.delete("b").unwrap();

    let a_after = read_unit(&registry, "a");
    assert_eq!(
        a_after.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(true)
    );
    assert!(
        a_after
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let c_after = read_unit(&registry, "c");
    assert!(c_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());
}

#[test]
fn test_upsert_merge_changing_deps() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();

    assert_eq!(
        read_unit(&registry, "b")
            .dependencies
            .as_ref()
            .unwrap()
            .required_by,
        vec!["a"]
    );

    let mut patch = make_unit_with_deps("a", &["c"]);
    registry.upsert(&mut patch, None).unwrap();

    let b_after = read_unit(&registry, "b");
    assert!(b_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());

    let c_after = read_unit(&registry, "c");
    assert_eq!(
        c_after.dependencies.as_ref().unwrap().required_by,
        vec!["a"]
    );
}

#[test]
fn test_upsert_middle_node_propagates_via_stored_required_by() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    // A -> B -> C
    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["c"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();

    let a_before = read_unit(&registry, "a");
    assert!(
        !a_before
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    // Upsert B: swap its dep from C to D (D doesn't exist).
    // A is NOT explicitly seeded — only reachable via B's stored requiredBy.
    let mut patch = make_unit_with_deps("b", &["d"]);
    registry.upsert(&mut patch, None).unwrap();

    let b_after = read_unit(&registry, "b");
    assert_eq!(
        b_after.dependencies.as_ref().unwrap().depends_on[0].is_missing,
        Some(true)
    );
    assert!(
        b_after
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let a_after = read_unit(&registry, "a");
    assert!(
        a_after
            .dependencies
            .as_ref()
            .unwrap()
            .has_transitive_missing_dependencies
    );

    let c_after = read_unit(&registry, "c");
    assert!(c_after
        .dependencies
        .as_ref()
        .unwrap()
        .required_by
        .is_empty());
}

#[test]
fn test_first_create_triggers_full_refresh_fallback() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    registry
        .create(&mut make_unit_with_deps("c", &[]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("b", &["c"]), None)
        .unwrap();
    registry
        .create(&mut make_unit_with_deps("a", &["b"]), None)
        .unwrap();

    let a = read_unit(&registry, "a");
    let b = read_unit(&registry, "b");
    let c = read_unit(&registry, "c");

    assert_eq!(a.planning.unwrap().topological_rank, Some(2));
    assert_eq!(b.planning.unwrap().topological_rank, Some(1));
    assert_eq!(c.planning.unwrap().topological_rank, Some(0));

    assert_eq!(b.dependencies.as_ref().unwrap().required_by, vec!["a"]);
    assert_eq!(c.dependencies.as_ref().unwrap().required_by, vec!["b"]);
}

// ── Testing status tests ───────────────────────────────────────────

fn make_code_unit_with_testing(id: &str, name: &str, testing_status: &str) -> CodeUnit {
    use crate::generated::types::{CloudStatus, OperationStatus, TestingStatus};

    let status = testing_status.parse::<OperationStatus>().ok();
    let mut cu = make_code_unit(id, name, CodeUnitObjectType::Table);
    cu.cloud_status = Some(CloudStatus {
        testing: Some(TestingStatus {
            status,
            updated_at: Some(
                chrono::DateTime::parse_from_rfc3339("2025-06-15T14:30:00Z")
                    .unwrap()
                    .with_timezone(&chrono::Utc),
            ),
            details: {
                let mut m = serde_json::Map::new();
                m.insert(
                    "runner".to_string(),
                    serde_json::Value::String("pytest".to_string()),
                );
                m
            },
        }),
        ..Default::default()
    });
    cu
}

#[test]
fn test_create_with_testing_status_roundtrips() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit_with_testing("ts-001", "T1", "completed");
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("ts-001", None).unwrap();
    let testing = loaded.cloud_status.unwrap().testing.unwrap();

    assert_eq!(
        testing.status,
        Some(crate::generated::types::OperationStatus::Completed)
    );
    assert!(testing.updated_at.is_some());
    assert_eq!(
        testing.details.get("runner").and_then(|v| v.as_str()),
        Some("pytest")
    );
}

#[test]
fn test_filter_by_testing_status() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu1 = make_code_unit_with_testing("ft-001", "T1", "completed");
    let mut cu2 = make_code_unit_with_testing("ft-002", "T2", "failed");
    let mut cu3 = make_code_unit("ft-003", "T3", CodeUnitObjectType::Table);

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    let completed = registry
        .find_all(FindOptions {
            filter: Some("cloudStatus.testing.status = 'completed'"),
            ..FindOptions::default()
        })
        .unwrap();
    assert_eq!(sorted_ids(completed), vec!["ft-001"]);

    let failed = registry
        .find_all(FindOptions {
            filter: Some("cloudStatus.testing.status = 'failed'"),
            ..FindOptions::default()
        })
        .unwrap();
    assert_eq!(sorted_ids(failed), vec!["ft-002"]);

    let testing_null = registry
        .find_all(FindOptions {
            filter: Some("cloudStatus.testing IS NULL"),
            ..FindOptions::default()
        })
        .unwrap();
    assert_eq!(sorted_ids(testing_null), vec!["ft-003"]);
}

#[test]
fn test_update_where_sets_testing_status() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let mut cu1 = make_code_unit_with_testing("uw-001", "T1", "pending");
    let mut cu2 = make_code_unit_with_testing("uw-002", "T2", "pending");
    let mut cu3 = make_code_unit_with_testing("uw-003", "T3", "completed");

    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();
    registry.create(&mut cu3, None).unwrap();

    let updates: Vec<(&str, Value)> = vec![(
        "cloudStatus.testing.status",
        Value::String("completed".to_string()),
    )];

    let result = registry
        .update_where("cloudStatus.testing.status = 'pending'", &updates, None)
        .unwrap();
    assert_eq!(result.succeeded.len(), 2);

    let loaded1 = registry.get_by_id("uw-001", None).unwrap();
    assert_eq!(
        loaded1.cloud_status.unwrap().testing.unwrap().status,
        Some(crate::generated::types::OperationStatus::Completed)
    );

    let loaded3 = registry.get_by_id("uw-003", None).unwrap();
    assert_eq!(
        loaded3.cloud_status.unwrap().testing.unwrap().status,
        Some(crate::generated::types::OperationStatus::Completed)
    );
}

// ── Custom codeStatus phases (additionalProperties) ────────────────

#[test]
fn test_custom_code_status_phase_roundtrip() {
    use crate::generated::types::{CodeStatus, OperationStatus, RegistrationStatus};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("custom-001", "T1", CodeUnitObjectType::Table);
    let mut status = CodeStatus::default();
    status.registration = Some(RegistrationStatus {
        status: Some(OperationStatus::Completed),
        ..Default::default()
    });
    status.extra.insert(
        "dataQuality".to_string(),
        serde_json::json!({
            "status": "completed",
            "score": 95,
            "checkedAt": "2025-01-15T11:00:00Z"
        }),
    );
    cu.code_status = Some(status);
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("custom-001", None).unwrap();
    let cs = loaded.code_status.unwrap();

    assert_eq!(
        cs.registration.unwrap().status,
        Some(OperationStatus::Completed)
    );
    let dq = cs
        .extra
        .get("dataQuality")
        .expect("custom phase must survive roundtrip");
    assert_eq!(dq["status"], "completed");
    assert_eq!(dq["score"], 95);
    assert_eq!(dq["checkedAt"], "2025-01-15T11:00:00Z");
}

#[test]
fn test_custom_code_status_phase_upsert_merge() {
    use crate::generated::types::{CodeStatus, OperationStatus, RegistrationStatus};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("custom-002", "T2", CodeUnitObjectType::Table);
    let mut status = CodeStatus::default();
    status.registration = Some(RegistrationStatus {
        status: Some(OperationStatus::Completed),
        ..Default::default()
    });
    status.extra.insert(
        "dataQuality".to_string(),
        serde_json::json!({"status": "pending"}),
    );
    cu.code_status = Some(status);
    registry.create(&mut cu, None).unwrap();

    let mut merge = CodeUnit {
        id: Some("custom-002".to_string()),
        ..Default::default()
    };
    let mut merge_status = CodeStatus::default();
    merge_status.extra.insert(
        "dataQuality".to_string(),
        serde_json::json!({"status": "completed", "score": 88}),
    );
    merge.code_status = Some(merge_status);
    registry.upsert(&mut merge, None).unwrap();

    let loaded = registry.get_by_id("custom-002", None).unwrap();
    let cs = loaded.code_status.unwrap();
    let dq = cs
        .extra
        .get("dataQuality")
        .expect("custom phase must survive upsert");
    assert_eq!(dq["status"], "completed");
    assert_eq!(dq["score"], 88);
}

// ── find_sql_file_changes integration tests ─────────────────────────

fn make_unit_with_source_file(id: &str, source_path: &str) -> CodeUnit {
    use crate::generated::types::{FileEntry, Files};
    CodeUnit {
        id: Some(id.to_string()),
        kind: Some(CodeUnitKind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            ..Default::default()
        }),
        target: Some(TargetMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            ..Default::default()
        }),
        files: Some(Files {
            source: Some(FileEntry {
                path: Some(source_path.to_string()),
                ..Default::default()
            }),
            ..Default::default()
        }),
        ..Default::default()
    }
}

fn make_unit_with_source_and_converted(
    id: &str,
    source_path: &str,
    converted_path: &str,
) -> CodeUnit {
    use crate::generated::types::{FileEntry, Files};
    CodeUnit {
        id: Some(id.to_string()),
        kind: Some(CodeUnitKind::DatabaseObject),
        source: Some(SourceMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            ..Default::default()
        }),
        target: Some(TargetMetadata {
            object_type: Some(CodeUnitObjectType::Table),
            ..Default::default()
        }),
        files: Some(Files {
            source: Some(FileEntry {
                path: Some(source_path.to_string()),
                ..Default::default()
            }),
            converted: Some(FileEntry {
                path: Some(converted_path.to_string()),
                ..Default::default()
            }),
            ..Default::default()
        }),
        ..Default::default()
    }
}

#[test]
fn find_sql_file_changes_empty_registry() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let result = registry
        .find_sql_file_changes(ChecksumMode::ALL, None)
        .unwrap();
    assert!(result.code_unit_changes.is_empty());
    assert!(result.untracked_files.is_empty());
    assert!(result.errors.is_empty());
}

#[test]
fn find_sql_file_changes_no_changes_when_files_match() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("src.sql"), b"SELECT 1").unwrap();
    std::fs::write(root.join("cvt.sql"), b"SELECT 1 AS col").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(
            &mut make_unit_with_source_and_converted("u1", "src.sql", "cvt.sql"),
            None,
        )
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::ALL, None)
        .unwrap();
    assert!(result.code_unit_changes.is_empty());
}

#[test]
fn find_sql_file_changes_detects_modified_source() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("src.sql"), b"SELECT 1").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u1", "src.sql"), None)
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    std::fs::write(root.join("src.sql"), b"SELECT 2 -- modified").unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, None)
        .unwrap();
    assert!(result.code_unit_changes.contains_key("u1"));
    let changes = &result.code_unit_changes["u1"];
    assert_eq!(changes.len(), 1);
    assert_eq!(
        changes[0].change_type,
        crate::checksum::ChangeType::Modified
    );
}

#[test]
fn find_sql_file_changes_detects_removed_source() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("src.sql"), b"SELECT 1").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u1", "src.sql"), None)
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    std::fs::remove_file(root.join("src.sql")).unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, None)
        .unwrap();
    assert!(result.code_unit_changes.contains_key("u1"));
    assert_eq!(
        result.code_unit_changes["u1"][0].change_type,
        crate::checksum::ChangeType::Removed
    );
}

#[test]
fn find_sql_file_changes_detects_untracked_source_files() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("tracked.sql"), b"ok").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u1", "tracked.sql"), None)
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    let source_dir = root.join("source");
    std::fs::create_dir_all(&source_dir).unwrap();
    std::fs::write(source_dir.join("orphan.sql"), b"surprise").unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, None)
        .unwrap();
    assert!(result.code_unit_changes.is_empty());
    assert!(!result.untracked_files.is_empty());
    assert!(result
        .untracked_files
        .iter()
        .any(|f| f.path.contains("orphan.sql")));
}

#[test]
fn find_sql_file_changes_mode_source_ignores_converted() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("src.sql"), b"SELECT 1").unwrap();
    std::fs::write(root.join("cvt.sql"), b"SELECT 1 AS col").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(
            &mut make_unit_with_source_and_converted("u1", "src.sql", "cvt.sql"),
            None,
        )
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    std::fs::write(root.join("cvt.sql"), b"modified converted!").unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, None)
        .unwrap();
    assert!(result.code_unit_changes.is_empty());
}

#[test]
fn find_sql_file_changes_with_filter() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("a.sql"), b"SELECT 1").unwrap();
    std::fs::write(root.join("b.sql"), b"SELECT 2").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    let mut u1 = make_unit_with_source_file("u1", "a.sql");
    u1.source.as_mut().unwrap().name = Some("Alpha".to_string());
    registry.create(&mut u1, None).unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    let mut u2 = make_unit_with_source_file("u2", "b.sql");
    u2.source.as_mut().unwrap().name = Some("Beta".to_string());
    registry.create(&mut u2, None).unwrap();
    registry.update_checksum("u2", ChecksumMode::ALL).unwrap();

    std::fs::write(root.join("a.sql"), b"modified a").unwrap();
    std::fs::write(root.join("b.sql"), b"modified b").unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, Some("source.name = 'Alpha'"))
        .unwrap();
    assert_eq!(result.code_unit_changes.len(), 1);
    assert!(result.code_unit_changes.contains_key("u1"));
    assert!(!result.code_unit_changes.contains_key("u2"));
}

#[test]
fn find_sql_file_changes_multiple_units_mixed() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("a.sql"), b"file a").unwrap();
    std::fs::write(root.join("b.sql"), b"file b").unwrap();
    std::fs::write(root.join("c.sql"), b"file c").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u1", "a.sql"), None)
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u2", "b.sql"), None)
        .unwrap();
    registry.update_checksum("u2", ChecksumMode::ALL).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u3", "c.sql"), None)
        .unwrap();
    registry.update_checksum("u3", ChecksumMode::ALL).unwrap();

    std::fs::write(root.join("a.sql"), b"modified a").unwrap();
    std::fs::remove_file(root.join("b.sql")).unwrap();
    // c.sql unchanged

    let result = registry
        .find_sql_file_changes(ChecksumMode::SOURCE, None)
        .unwrap();
    assert_eq!(result.code_unit_changes.len(), 2);
    assert_eq!(
        result.code_unit_changes["u1"][0].change_type,
        crate::checksum::ChangeType::Modified
    );
    assert_eq!(
        result.code_unit_changes["u2"][0].change_type,
        crate::checksum::ChangeType::Removed
    );
    assert!(!result.code_unit_changes.contains_key("u3"));
}

#[test]
fn find_sql_file_changes_errors_field_is_empty_on_success() {
    let dir = temp_dir();
    let root = dir.path();
    std::fs::write(root.join("src.sql"), b"content").unwrap();

    let registry = CodeUnitRegistry::init(root).unwrap();
    registry
        .create(&mut make_unit_with_source_file("u1", "src.sql"), None)
        .unwrap();
    registry.update_checksum("u1", ChecksumMode::ALL).unwrap();

    let result = registry
        .find_sql_file_changes(ChecksumMode::ALL, None)
        .unwrap();
    assert!(result.errors.is_empty());
}

// ── Before-write hook tests ─────────────────────────────────────────

use std::sync::{Arc, Mutex};

type HookCallLog = Arc<Mutex<Vec<(ChangeType, Vec<String>)>>>;

#[derive(Clone, Default)]
struct TrackingHook {
    calls: HookCallLog,
}

impl RegistryHook for TrackingHook {
    fn before_persist(
        &self,
        kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        let ids: Vec<String> = changes.iter().map(|c| c.id.clone()).collect();
        self.calls.lock().unwrap().push((kind, ids));
        Ok(changes)
    }
}

struct FailingHook;

impl RegistryHook for FailingHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        _changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        Err(ValidationSnafu {
            message: "hook rejected",
        }
        .build())
    }
}

#[test]
fn hook_fires_on_create() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu = make_code_unit("h1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 1);
    assert_eq!(log[0].0, ChangeType::Create);
    assert_eq!(log[0].1, vec!["h1"]);
}

#[test]
fn hook_fires_on_update() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu = make_code_unit("h2", "T2", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();
    registry
        .update(
            "h2",
            &[("source.name", Value::String("Updated".into()))],
            None,
        )
        .unwrap();

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 2);
    assert_eq!(log[0].0, ChangeType::Create);
    assert_eq!(log[1].0, ChangeType::Update);
    assert_eq!(log[1].1, vec!["h2"]);
}

#[test]
fn hook_fires_on_upsert() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu = make_code_unit("h3", "T3", CodeUnitObjectType::Table);
    registry.upsert(&mut cu, None).unwrap();

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 1);
    assert_eq!(log[0].0, ChangeType::Upsert);
    assert_eq!(log[0].1, vec!["h3"]);
}

#[test]
fn hook_fires_on_delete() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu = make_code_unit("h4", "T4", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();
    registry.delete("h4").unwrap();

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 2);
    assert_eq!(log[1].0, ChangeType::Delete);
    assert_eq!(log[1].1, vec!["h4"]);
}

#[test]
fn hook_can_transform_unit() {
    let dir = temp_dir();

    struct TransformHook;
    impl RegistryHook for TransformHook {
        fn before_persist(
            &self,
            _kind: ChangeType,
            changes: Vec<CodeUnitChange>,
            _registry: &CodeUnitRegistry,
            _options: &WriteOptions,
        ) -> Result<Vec<CodeUnitChange>> {
            Ok(changes
                .into_iter()
                .map(|mut change| {
                    if let Some(ref mut unit) = change.after {
                        if let Some(ref mut source) = unit.source {
                            source.name = Some("TransformedByHook".to_string());
                        }
                    }
                    change
                })
                .collect())
        }
    }

    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(TransformHook);

    let mut cu = make_code_unit("ht1", "Original", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let unit = registry.get_by_id("ht1", None).unwrap();
    assert_eq!(
        unit.source.as_ref().unwrap().name.as_deref(),
        Some("TransformedByHook"),
        "hook should have transformed the unit before it was written"
    );
}

#[test]
fn hook_receives_before_and_after() {
    let dir = temp_dir();
    let captured_before = Arc::new(Mutex::new(None::<Option<CodeUnit>>));
    let captured_after = Arc::new(Mutex::new(None::<Option<CodeUnit>>));
    let cb = captured_before.clone();
    let ca = captured_after.clone();

    struct CaptureHook {
        before: Arc<Mutex<Option<Option<CodeUnit>>>>,
        after: Arc<Mutex<Option<Option<CodeUnit>>>>,
    }
    impl RegistryHook for CaptureHook {
        fn before_persist(
            &self,
            _kind: ChangeType,
            changes: Vec<CodeUnitChange>,
            _registry: &CodeUnitRegistry,
            _options: &WriteOptions,
        ) -> Result<Vec<CodeUnitChange>> {
            if let Some(change) = changes.first() {
                *self.before.lock().unwrap() = Some(change.before.clone());
                *self.after.lock().unwrap() = Some(change.after.clone());
            }
            Ok(changes)
        }
    }

    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(CaptureHook {
        before: cb,
        after: ca,
    });

    let mut cu = make_code_unit("hba1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let before = captured_before.lock().unwrap().take().unwrap();
    assert!(before.is_none(), "before should be None for creates");
    let after = captured_after.lock().unwrap().take().unwrap();
    assert!(after.is_some(), "after should be Some for creates");
}

#[test]
fn hook_fires_on_create_batch() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut batch = vec![
        make_code_unit("hb1", "T1", CodeUnitObjectType::Table),
        make_code_unit("hb2", "T2", CodeUnitObjectType::Table),
    ];
    let result = registry.create_batch(&mut batch, None).unwrap();
    assert_eq!(result.succeeded.len(), 2);

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 1);
    assert_eq!(log[0].0, ChangeType::Create);
    assert_eq!(log[0].1.len(), 2);
}

#[test]
fn hook_fires_on_update_batch() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu1 = make_code_unit("hub1", "T1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("hub2", "T2", CodeUnitObjectType::Table);
    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    let batch: Vec<(&str, Vec<(&str, Value)>)> = vec![
        ("hub1", vec![("source.name", Value::String("U1".into()))]),
        ("hub2", vec![("source.name", Value::String("U2".into()))]),
    ];
    registry.update_batch(&batch, None).unwrap();

    let log = calls.lock().unwrap();
    assert!(log
        .iter()
        .any(|(k, ids)| *k == ChangeType::Update && ids.len() == 2));
}

#[test]
fn hook_fires_on_update_where() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut cu1 = make_code_unit("huw1", "T1", CodeUnitObjectType::Table);
    let mut cu2 = make_code_unit("huw2", "T2", CodeUnitObjectType::Procedure);
    registry.create(&mut cu1, None).unwrap();
    registry.create(&mut cu2, None).unwrap();

    let updates: Vec<(&str, Value)> = vec![("source.database", Value::String("NEWDB".into()))];
    registry
        .update_where("source.objectType = 'table'", &updates, None)
        .unwrap();

    let log = calls.lock().unwrap();
    let update_entry = log.iter().find(|(k, _)| *k == ChangeType::Update).unwrap();
    assert_eq!(update_entry.1, vec!["huw1".to_string()]);
}

#[test]
fn hook_fires_on_upsert_batch() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(hook);

    let mut batch = vec![
        make_code_unit("husb1", "T1", CodeUnitObjectType::Table),
        make_code_unit("husb2", "T2", CodeUnitObjectType::Table),
    ];
    registry.upsert_batch(&mut batch, None).unwrap();

    let log = calls.lock().unwrap();
    assert!(log
        .iter()
        .any(|(k, ids)| *k == ChangeType::Upsert && ids.len() == 2));
}

#[test]
fn hook_error_aborts_create() {
    let dir = temp_dir();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(FailingHook);

    let mut cu = make_code_unit("hf1", "T1", CodeUnitObjectType::Table);
    let err = registry.create(&mut cu, None).unwrap_err();
    assert_eq!(err.error_code_i32(), 1007);

    assert!(
        !registry.id_to_path("hf1").exists(),
        "unit should NOT be written when hook aborts"
    );
}

#[test]
fn multiple_hooks_fire_in_order() {
    let dir = temp_dir();
    let log = Arc::new(Mutex::new(Vec::<String>::new()));

    struct OrderedHook(String, Arc<Mutex<Vec<String>>>);
    impl RegistryHook for OrderedHook {
        fn before_persist(
            &self,
            _kind: ChangeType,
            changes: Vec<CodeUnitChange>,
            _registry: &CodeUnitRegistry,
            _options: &WriteOptions,
        ) -> Result<Vec<CodeUnitChange>> {
            self.1.lock().unwrap().push(self.0.clone());
            Ok(changes)
        }
    }

    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(OrderedHook("first".into(), log.clone()));
    registry.add_hook(OrderedHook("second".into(), log.clone()));

    let mut cu = make_code_unit("ord1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let entries = log.lock().unwrap();
    assert_eq!(*entries, vec!["first", "second"]);
}

#[test]
fn no_hooks_operations_work() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("nh1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();
    registry
        .update("nh1", &[("source.name", Value::String("U".into()))], None)
        .unwrap();
    registry.delete("nh1").unwrap();
}

#[test]
fn add_hook_after_construction() {
    let dir = temp_dir();
    let hook = TrackingHook::default();
    let calls = hook.calls.clone();
    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ah1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();
    assert!(calls.lock().unwrap().is_empty(), "no hook yet");

    registry.add_hook(hook);

    registry
        .update(
            "ah1",
            &[("source.name", Value::String("After".into()))],
            None,
        )
        .unwrap();

    let log = calls.lock().unwrap();
    assert_eq!(log.len(), 1);
    assert_eq!(log[0].0, ChangeType::Update);
}

#[test]
fn delete_hook_can_cancel_delete() {
    let dir = temp_dir();

    struct CancelDeleteHook;
    impl RegistryHook for CancelDeleteHook {
        fn before_persist(
            &self,
            kind: ChangeType,
            changes: Vec<CodeUnitChange>,
            _registry: &CodeUnitRegistry,
            _options: &WriteOptions,
        ) -> Result<Vec<CodeUnitChange>> {
            if kind == ChangeType::Delete {
                Ok(changes
                    .into_iter()
                    .map(|mut change| {
                        if let Some(ref before) = change.before {
                            change.after = Some(before.clone());
                        }
                        change
                    })
                    .collect())
            } else {
                Ok(changes)
            }
        }
    }

    let mut registry = CodeUnitRegistry::init(dir.path()).unwrap();
    registry.add_hook(CancelDeleteHook);

    let mut cu = make_code_unit("cd1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();
    registry.delete("cd1").unwrap();

    assert!(
        registry.id_to_path("cd1").exists(),
        "unit should still exist after hook cancelled delete"
    );
}

// ── UpdatedAtHook tests ──────────────────────────────────────────────────

#[test]
fn test_create_with_testing_status_populates_updated_at() {
    use crate::generated::types::{CloudStatus, OperationStatus, TestingStatus};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ua1", "T1", CodeUnitObjectType::Table);
    cu.cloud_status = Some(CloudStatus {
        testing: Some(TestingStatus {
            status: Some(OperationStatus::Pending),
            ..Default::default()
        }),
        ..Default::default()
    });

    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("ua1", None).unwrap();
    let testing = stored
        .cloud_status
        .as_ref()
        .and_then(|cs| cs.testing.as_ref())
        .expect("testing should exist");
    assert!(
        testing.updated_at.is_some(),
        "updatedAt should be set after create with testing status"
    );
}

#[test]
fn test_update_sibling_triggers_updated_at() {
    use crate::generated::types::{CloudStatus, OperationStatus, TestingStatus};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ua2", "T2", CodeUnitObjectType::Table);
    cu.cloud_status = Some(CloudStatus {
        testing: Some(TestingStatus {
            status: Some(OperationStatus::Pending),
            ..Default::default()
        }),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let stored_before = registry.get_by_id("ua2", None).unwrap();
    let ts_before = stored_before
        .cloud_status
        .as_ref()
        .unwrap()
        .testing
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "ua2",
            &[("cloudStatus.testing.status", serde_json::json!("completed"))],
            None,
        )
        .unwrap();

    let stored_after = registry.get_by_id("ua2", None).unwrap();
    let ts_after = stored_after
        .cloud_status
        .as_ref()
        .unwrap()
        .testing
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();

    assert!(
        ts_after > ts_before,
        "updatedAt should advance when a sibling changes"
    );
}

#[test]
fn test_update_unrelated_field_preserves_updated_at() {
    use crate::generated::types::{CloudStatus, OperationStatus, TestingStatus};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ua3", "T3", CodeUnitObjectType::Table);
    cu.cloud_status = Some(CloudStatus {
        testing: Some(TestingStatus {
            status: Some(OperationStatus::Pending),
            ..Default::default()
        }),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let stored_before = registry.get_by_id("ua3", None).unwrap();
    let ts_before = stored_before
        .cloud_status
        .as_ref()
        .unwrap()
        .testing
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "ua3",
            &[("source.name", serde_json::json!("Renamed"))],
            None,
        )
        .unwrap();

    let stored_after = registry.get_by_id("ua3", None).unwrap();
    let ts_after = stored_after
        .cloud_status
        .as_ref()
        .unwrap()
        .testing
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();

    assert_eq!(
        ts_before, ts_after,
        "updatedAt should NOT change when only unrelated fields are modified"
    );
}

#[test]
fn test_upsert_creates_updated_at_when_testing_added() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("ua4", "T4", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("ua4", None).unwrap();
    assert!(stored.code_status.is_none(), "no codeStatus initially");

    let mut patch = CodeUnit {
        id: Some("ua4".to_string()),
        cloud_status: Some(crate::generated::types::CloudStatus {
            testing: Some(crate::generated::types::TestingStatus {
                status: Some(crate::generated::types::OperationStatus::Pending),
                details: {
                    let mut m = serde_json::Map::new();
                    m.insert("note".to_string(), serde_json::json!("first run"));
                    m
                },
                ..Default::default()
            }),
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let stored = registry.get_by_id("ua4", None).unwrap();
    let testing = stored
        .cloud_status
        .as_ref()
        .and_then(|cs| cs.testing.as_ref())
        .expect("testing should exist after upsert");
    assert!(
        testing.updated_at.is_some(),
        "updatedAt should be created when testing is added via upsert"
    );
}

// ── codeStatus.conversion.updatedAt contract tests ──────────────────────
//
// SnowConvert's idempotent-write guard relies on a strict contract:
//   * Writes to codeStatus.conversion.{status,converterVersion} MUST bump
//     codeStatus.conversion.updatedAt.
//   * Writes to dependsOn / requiredBy / Files.Converted.Checksum (the
//     fields a `--resync` workflow mutates) MUST NOT bump
//     codeStatus.conversion.updatedAt.
// Without these guarantees the timestamp signal is unsound.

fn conversion_status_with(
    status: crate::generated::types::OperationStatus,
    version: &str,
) -> crate::generated::types::ConversionStatus {
    crate::generated::types::ConversionStatus {
        status: Some(status),
        converter_version: Some(version.to_string()),
        ..Default::default()
    }
}

#[test]
fn test_create_with_conversion_status_populates_conversion_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("conv-ua1", "T1", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        ..Default::default()
    });

    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("conv-ua1", None).unwrap();
    let conversion = stored
        .code_status
        .as_ref()
        .and_then(|cs| cs.conversion.as_ref())
        .expect("conversion should exist");
    assert!(
        conversion.updated_at.is_some(),
        "codeStatus.conversion.updatedAt should be set after create with conversion status"
    );
}

#[test]
fn test_update_conversion_status_advances_conversion_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("conv-ua2", "T2", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Pending, "1.0.0")),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let ts_before = registry
        .get_by_id("conv-ua2", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "conv-ua2",
            &[(
                "codeStatus.conversion.status",
                serde_json::json!("completed"),
            )],
            None,
        )
        .unwrap();

    let ts_after = registry
        .get_by_id("conv-ua2", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    assert!(
        ts_after > ts_before,
        "conversion.updatedAt should advance when conversion.status changes"
    );
}

#[test]
fn test_update_converter_version_advances_conversion_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("conv-ua3", "T3", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let ts_before = registry
        .get_by_id("conv-ua3", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "conv-ua3",
            &[(
                "codeStatus.conversion.converterVersion",
                serde_json::json!("1.1.0"),
            )],
            None,
        )
        .unwrap();

    let ts_after = registry
        .get_by_id("conv-ua3", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    assert!(
        ts_after > ts_before,
        "conversion.updatedAt should advance when converterVersion changes"
    );
}

#[test]
fn test_dependency_update_does_not_advance_conversion_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("conv-ua4", "T4", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let stored_before = registry.get_by_id("conv-ua4", None).unwrap();
    let conv_ts_before = stored_before
        .code_status
        .as_ref()
        .unwrap()
        .conversion
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let root_ts_before = stored_before.updated_at.unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "conv-ua4",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": [
                        { "id": "other-id", "relationTypes": ["SELECT"] }
                    ]
                }),
            )],
            None,
        )
        .unwrap();

    let stored_after = registry.get_by_id("conv-ua4", None).unwrap();
    let conv_ts_after = stored_after
        .code_status
        .as_ref()
        .unwrap()
        .conversion
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let root_ts_after = stored_after.updated_at.unwrap();

    assert_eq!(
        conv_ts_before, conv_ts_after,
        "conversion.updatedAt MUST NOT advance when only dependencies change"
    );
    assert!(
        root_ts_after > root_ts_before,
        "root.updatedAt SHOULD advance on any update"
    );
}

#[test]
fn test_checksum_refresh_does_not_advance_conversion_updated_at() {
    use crate::checksum::ChecksumMode;
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "conv-ua5.sql", b"converted v1");

    let mut cu = make_code_unit_with_files("conv-ua5", None, Some("conv-ua5.sql".into()), None);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let conv_ts_before = registry
        .get_by_id("conv-ua5", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    fs::write(
        dir.path().join("conv-ua5.sql"),
        b"converted v2 (modified externally)",
    )
    .unwrap();
    registry
        .update_checksum("conv-ua5", ChecksumMode::CONVERTED)
        .unwrap();

    let conv_ts_after = registry
        .get_by_id("conv-ua5", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    assert_eq!(
        conv_ts_before, conv_ts_after,
        "conversion.updatedAt MUST NOT advance when only Files.Converted.Checksum is refreshed"
    );
}

#[test]
fn test_upsert_with_omitted_conversion_preserves_existing_block() {
    // Pins the contract that SnowConvert's idempotent-write guard depends on:
    // when an upsert patch omits codeStatus.conversion entirely (because the
    // C# binding skips null fields under JsonIgnoreCondition.WhenWritingNull),
    // the registry's deep_merge MUST keep the previously persisted Conversion
    // block — including Status, ConverterVersion, and the auto-stamped
    // updatedAt — untouched.
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("conv-merge-1", "T1", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let conv_ts_before = registry
        .get_by_id("conv-merge-1", None)
        .unwrap()
        .code_status
        .unwrap()
        .conversion
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    // Mimic what RegistryConversion sends when the idempotent-write guard
    // preserves a converted file: Conversion is None on the patch, so it is
    // omitted from the serialized JSON entirely.
    let mut patch = CodeUnit {
        id: Some("conv-merge-1".to_string()),
        source: Some(SourceMetadata {
            name: Some("T1-renamed".to_string()),
            ..Default::default()
        }),
        code_status: Some(crate::generated::types::CodeStatus {
            conversion: None,
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let stored = registry.get_by_id("conv-merge-1", None).unwrap();
    let conversion = stored
        .code_status
        .as_ref()
        .and_then(|cs| cs.conversion.as_ref())
        .expect("conversion block must be preserved when patch omits it");

    assert_eq!(
        conversion.status,
        Some(OperationStatus::Completed),
        "Conversion.status must be preserved through merge",
    );
    assert_eq!(
        conversion.converter_version.as_deref(),
        Some("1.0.0"),
        "Conversion.converterVersion must be preserved through merge",
    );
    assert_eq!(
        conversion.updated_at,
        Some(conv_ts_before),
        "Conversion.updatedAt must be preserved through merge",
    );
}

// ── codeStatus.resync.updatedAt auto-stamp tests ─────────────────────────
//
// Pin the contract that the SnowConvert idempotent-write guard depends on:
//
//  * Writing codeStatus.resync.status MUST auto-stamp
//    codeStatus.resync.updatedAt (so a --resync run that touches a unit
//    leaves a detectable timestamp).
//  * Writing root-level fields (e.g. dependencies, signature) MUST NOT
//    advance codeStatus.resync.updatedAt (keeping the rule false-positive
//    free for unrelated metadata writes).
//  * Omitting codeStatus.resync from a merge patch MUST preserve the
//    previously persisted Resync block intact (mirrors the conversion null
//    merge contract).
//  * codeStatus.resync.updatedAt and codeStatus.conversion.updatedAt
//    advance independently.

fn resync_status_with(
    status: crate::generated::types::OperationStatus,
) -> crate::generated::types::ResyncStatus {
    crate::generated::types::ResyncStatus {
        status: Some(status),
        ..Default::default()
    }
}

#[test]
fn test_upsert_resync_status_advances_resync_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("resync-ua1", "T1", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        resync: Some(resync_status_with(OperationStatus::Completed)),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let ts_before = registry
        .get_by_id("resync-ua1", None)
        .unwrap()
        .code_status
        .unwrap()
        .resync
        .unwrap()
        .updated_at
        .expect("resync.updatedAt should be set on create");

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "resync-ua1",
            &[("codeStatus.resync.status", serde_json::json!("inProgress"))],
            None,
        )
        .unwrap();

    let ts_after = registry
        .get_by_id("resync-ua1", None)
        .unwrap()
        .code_status
        .unwrap()
        .resync
        .unwrap()
        .updated_at
        .unwrap();

    assert!(
        ts_after > ts_before,
        "resync.updatedAt should advance when resync.status changes"
    );
}

#[test]
fn test_dependency_update_does_not_advance_resync_updated_at() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("resync-ua2", "T2", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        resync: Some(resync_status_with(OperationStatus::Completed)),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let stored_before = registry.get_by_id("resync-ua2", None).unwrap();
    let resync_ts_before = stored_before
        .code_status
        .as_ref()
        .unwrap()
        .resync
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let root_ts_before = stored_before.updated_at.unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "resync-ua2",
            &[(
                "dependencies",
                serde_json::json!({
                    "dependsOn": [
                        { "id": "other-id", "relationTypes": ["SELECT"] }
                    ]
                }),
            )],
            None,
        )
        .unwrap();

    let stored_after = registry.get_by_id("resync-ua2", None).unwrap();
    let resync_ts_after = stored_after
        .code_status
        .as_ref()
        .unwrap()
        .resync
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let root_ts_after = stored_after.updated_at.unwrap();

    assert_eq!(
        resync_ts_before, resync_ts_after,
        "resync.updatedAt MUST NOT advance when only dependencies change"
    );
    assert!(
        root_ts_after > root_ts_before,
        "root.updatedAt SHOULD advance on any update"
    );
}

#[test]
fn test_upsert_with_omitted_resync_preserves_existing_block() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("resync-merge-1", "T1", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        resync: Some(resync_status_with(OperationStatus::Completed)),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let resync_ts_before = registry
        .get_by_id("resync-merge-1", None)
        .unwrap()
        .code_status
        .unwrap()
        .resync
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    let mut patch = CodeUnit {
        id: Some("resync-merge-1".to_string()),
        source: Some(SourceMetadata {
            name: Some("T1-renamed".to_string()),
            ..Default::default()
        }),
        code_status: Some(crate::generated::types::CodeStatus {
            resync: None,
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let stored = registry.get_by_id("resync-merge-1", None).unwrap();
    let resync = stored
        .code_status
        .as_ref()
        .and_then(|cs| cs.resync.as_ref())
        .expect("resync block must be preserved when patch omits it");

    assert_eq!(
        resync.status,
        Some(OperationStatus::Completed),
        "Resync.status must be preserved through merge",
    );
    assert_eq!(
        resync.updated_at,
        Some(resync_ts_before),
        "Resync.updatedAt must be preserved through merge",
    );
}

#[test]
fn test_resync_and_conversion_updated_at_are_independent() {
    use crate::generated::types::OperationStatus;

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("resync-vs-conv-1", "T1", CodeUnitObjectType::Table);
    cu.code_status = Some(crate::generated::types::CodeStatus {
        conversion: Some(conversion_status_with(OperationStatus::Completed, "1.0.0")),
        resync: Some(resync_status_with(OperationStatus::Completed)),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let baseline = registry.get_by_id("resync-vs-conv-1", None).unwrap();
    let conv_ts0 = baseline
        .code_status
        .as_ref()
        .unwrap()
        .conversion
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let resync_ts0 = baseline
        .code_status
        .as_ref()
        .unwrap()
        .resync
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    // Bumping conversion.status should ONLY advance conversion.updatedAt.
    registry
        .update(
            "resync-vs-conv-1",
            &[(
                "codeStatus.conversion.status",
                serde_json::json!("inProgress"),
            )],
            None,
        )
        .unwrap();

    let mid = registry.get_by_id("resync-vs-conv-1", None).unwrap();
    let conv_ts1 = mid
        .code_status
        .as_ref()
        .unwrap()
        .conversion
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let resync_ts1 = mid
        .code_status
        .as_ref()
        .unwrap()
        .resync
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    assert!(conv_ts1 > conv_ts0, "conversion.updatedAt should advance");
    assert_eq!(
        resync_ts1, resync_ts0,
        "resync.updatedAt MUST NOT advance when only conversion changes"
    );

    std::thread::sleep(std::time::Duration::from_secs(1));

    // Bumping resync.status should ONLY advance resync.updatedAt.
    registry
        .update(
            "resync-vs-conv-1",
            &[("codeStatus.resync.status", serde_json::json!("inProgress"))],
            None,
        )
        .unwrap();

    let after = registry.get_by_id("resync-vs-conv-1", None).unwrap();
    let conv_ts2 = after
        .code_status
        .as_ref()
        .unwrap()
        .conversion
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    let resync_ts2 = after
        .code_status
        .as_ref()
        .unwrap()
        .resync
        .as_ref()
        .unwrap()
        .updated_at
        .unwrap();
    assert_eq!(
        conv_ts2, conv_ts1,
        "conversion.updatedAt MUST NOT advance when only resync changes"
    );
    assert!(
        resync_ts2 > resync_ts1,
        "resync.updatedAt should advance when resync.status changes"
    );
}

// ── Root-level updatedAt tests ───────────────────────────────────────────

#[test]
fn test_create_sets_root_updated_at() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("root-ua1", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("root-ua1", None).unwrap();
    assert!(
        stored.updated_at.is_some(),
        "root updatedAt should be set on create"
    );
}

#[test]
fn test_update_advances_root_updated_at() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("root-ua2", "T2", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let before = registry.get_by_id("root-ua2", None).unwrap();
    let ts_before = before.updated_at.unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    registry
        .update(
            "root-ua2",
            &[("source.name", serde_json::json!("Renamed"))],
            None,
        )
        .unwrap();

    let after = registry.get_by_id("root-ua2", None).unwrap();
    let ts_after = after.updated_at.unwrap();

    assert!(
        ts_after > ts_before,
        "root updatedAt should advance on any update"
    );
}

#[test]
fn test_upsert_advances_root_updated_at() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("root-ua3", "T3", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let before = registry.get_by_id("root-ua3", None).unwrap();
    let ts_before = before.updated_at.unwrap();

    std::thread::sleep(std::time::Duration::from_secs(1));

    let mut patch = CodeUnit {
        id: Some("root-ua3".to_string()),
        source: Some(SourceMetadata {
            name: Some("Updated".to_string()),
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let after = registry.get_by_id("root-ua3", None).unwrap();
    let ts_after = after.updated_at.unwrap();

    assert!(
        ts_after > ts_before,
        "root updatedAt should advance on upsert"
    );
}

// ── WriteOptions / ChecksumHook tests ──────────────────────────────────

#[test]
fn create_with_checksum_source_populates_source_checksum() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "hw.sql", b"SELECT 1");

    let mut cu = make_code_unit_with_files("woc1", Some("hw.sql".into()), None, None);
    let opts = WriteOptions {
        checksum_mode: ChecksumMode::SOURCE,
    };
    registry.create(&mut cu, Some(&opts)).unwrap();

    let stored = registry.get_by_id("woc1", None).unwrap();
    let checksum = stored.files.unwrap().source.unwrap().checksum;
    assert!(checksum.is_some(), "source checksum should be populated");
    assert!(!checksum.unwrap().is_empty());
}

#[test]
fn upsert_with_checksum_all_populates_all_checksums() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "s.sql", b"SELECT 1");
    write_temp_source(dir.path(), "c.sql", b"SELECT 2");
    write_temp_source(dir.path(), "snap.sql", b"SELECT 3");

    let mut cu = make_code_unit_with_files(
        "woc2",
        Some("s.sql".into()),
        Some("c.sql".into()),
        Some("snap.sql".into()),
    );
    let opts = WriteOptions {
        checksum_mode: ChecksumMode::ALL,
    };
    registry.upsert(&mut cu, Some(&opts)).unwrap();

    let stored = registry.get_by_id("woc2", None).unwrap();
    let files = stored.files.unwrap();
    assert!(
        files.source.as_ref().unwrap().checksum.is_some(),
        "source checksum should be populated"
    );
    assert!(
        files.converted.as_ref().unwrap().checksum.is_some(),
        "converted checksum should be populated"
    );
    assert!(
        files.snapshot.as_ref().unwrap().checksum.is_some(),
        "snapshot checksum should be populated"
    );
}

#[test]
fn create_with_none_options_leaves_checksum_empty() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "noop.sql", b"SELECT 1");

    let mut cu = make_code_unit_with_files("woc3", Some("noop.sql".into()), None, None);
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("woc3", None).unwrap();
    let checksum = stored.files.unwrap().source.unwrap().checksum;
    assert!(
        checksum.is_none(),
        "checksum should remain empty when options is None"
    );
}

#[test]
fn update_with_checksum_source_refreshes_checksum() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    write_temp_source(dir.path(), "upd.sql", b"v1");

    let mut cu = make_code_unit_with_files("woc4", Some("upd.sql".into()), None, None);
    let opts_src = WriteOptions {
        checksum_mode: ChecksumMode::SOURCE,
    };
    registry.create(&mut cu, Some(&opts_src)).unwrap();

    let before = registry
        .get_by_id("woc4", None)
        .unwrap()
        .files
        .unwrap()
        .source
        .unwrap()
        .checksum
        .unwrap();

    fs::write(dir.path().join("upd.sql"), b"v2").unwrap();
    registry
        .update(
            "woc4",
            &[("source.name", serde_json::json!("Renamed"))],
            Some(&opts_src),
        )
        .unwrap();

    let after = registry
        .get_by_id("woc4", None)
        .unwrap()
        .files
        .unwrap()
        .source
        .unwrap()
        .checksum
        .unwrap();

    assert_ne!(
        before, after,
        "checksum should change after file modification"
    );
}

// ── Validation ───────────────────────────────────────────────────────────

use crate::checksum::ChecksumMode;
use crate::validation::ValidationIssueKind;

#[test]
fn validate_empty_registry() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(report.is_valid);
    assert_eq!(report.files_checked, 0);
    assert!(report.issues.is_empty());
}

#[test]
fn validate_valid_registry() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let mut unit = make_code_unit("v1", "my_table", CodeUnitObjectType::Table);
    registry.create(&mut unit, None).unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(report.is_valid);
    assert_eq!(report.files_checked, 1);
}

#[test]
fn validate_detects_invalid_json() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    fs::write(dir.path().join("registry/bad.json"), "not json{{{").unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert_eq!(report.files_checked, 1);
    assert_eq!(report.issues.len(), 1);
    assert_eq!(report.issues[0].kind, ValidationIssueKind::InvalidJson);
    assert_eq!(report.issues[0].file, "bad.json");
}

// ── migrate_schema_all / migrate_schema_file ─────────────────────────────

#[test]
fn migrate_schema_all_empty_registry() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let result = registry.migrate_schema_all().unwrap();
    assert!(result.succeeded.is_empty());
    assert!(result.failed.is_empty());
}

#[test]
fn migrate_schema_all_current_version_is_noop() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let cu = make_code_unit("msa-1", "tbl1", CodeUnitObjectType::Table);
    registry.create(&mut cu.clone(), None).unwrap();

    let result = registry.migrate_schema_all().unwrap();
    assert!(
        result.succeeded.is_empty(),
        "current-version files should be skipped"
    );
    assert!(result.failed.is_empty());
}

#[test]
fn migrate_schema_all_future_version_reports_failure() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({(SCHEMA_VERSION_FIELD): 999, "id": "future"});
    fs::write(
        dir.path().join("registry/future.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let result = registry.migrate_schema_all().unwrap();
    assert!(result.succeeded.is_empty());
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "future");
    assert_eq!(result.failed[0].error.code, 1020);
}

#[test]
fn migrate_schema_all_malformed_version_reports_failure() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({(SCHEMA_VERSION_FIELD): "bad", "id": "broken"});
    fs::write(
        dir.path().join("registry/broken.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let result = registry.migrate_schema_all().unwrap();
    assert!(result.succeeded.is_empty());
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "broken");
    assert_eq!(result.failed[0].error.code, 1021);
}

#[test]
fn migrate_schema_all_invalid_json_reports_failure() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    fs::write(dir.path().join("registry/garbage.json"), "not json{{{").unwrap();

    let result = registry.migrate_schema_all().unwrap();
    assert!(result.succeeded.is_empty());
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "garbage");
    assert_eq!(result.failed[0].error.code, 1009);
}

#[test]
fn migrate_schema_all_partial_failure_isolates_errors() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut good = make_code_unit("good-1", "tbl1", CodeUnitObjectType::Table);
    registry.create(&mut good, None).unwrap();

    let bad_doc = serde_json::json!({(SCHEMA_VERSION_FIELD): 999, "id": "bad-1"});
    fs::write(
        dir.path().join("registry/bad-1.json"),
        serde_json::to_string_pretty(&bad_doc).unwrap(),
    )
    .unwrap();

    let result = registry.migrate_schema_all().unwrap();
    assert_eq!(result.failed.len(), 1);
    assert_eq!(result.failed[0].id, "bad-1");
    assert_eq!(result.failed[0].error.code, 1020);
    assert!(
        !result.failed.iter().any(|f| f.id == "good-1"),
        "valid file should not appear in failures"
    );
}

#[test]
fn validate_rejects_future_schema_version() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({ (SCHEMA_VERSION_FIELD): 9999 });
    fs::write(
        dir.path().join("registry/future.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert_eq!(report.issues.len(), 1);
    assert_eq!(
        report.issues[0].kind,
        ValidationIssueKind::SchemaMigrationError
    );
    assert_eq!(report.issues[0].error_code, Some(1020));
}

#[test]
fn validate_rejects_malformed_schema_version() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({ (SCHEMA_VERSION_FIELD): "bad" });
    fs::write(
        dir.path().join("registry/bad-version.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert_eq!(report.issues.len(), 1);
    assert_eq!(
        report.issues[0].kind,
        ValidationIssueKind::SchemaMigrationError
    );
    assert_eq!(report.issues[0].error_code, Some(1021));
}

#[test]
fn validate_detects_schema_violation() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({ (SCHEMA_VERSION_FIELD): 1, "isMissing": "not-a-bool" });
    fs::write(
        dir.path().join("registry/bad-type.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert!(
        report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::SchemaViolation),
        "expected a schema violation, got: {:?}",
        report.issues
    );
}

#[test]
fn validate_allows_root_issues_on_etl() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({
        SCHEMA_VERSION_FIELD: 1,
        "id": "etl-with-root-issues",
        "kind": "etl",
        "files": { "source": { "path": "source/_etl/Package.dtsx" } },
        "issues": [{ "code": "X", "severity": "low", "count": 1 }],
    });
    fs::write(
        dir.path().join("registry/etl-with-root-issues.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(
        report.is_valid,
        "etl unit with root issues should pass validation, got validation issues: {:?}",
        report.issues
    );
    assert!(
        !report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::PerKindStructure),
        "expected no per-kind-structure issue, got: {:?}",
        report.issues
    );
}

#[test]
fn objecttype_schema_includes_informatica_types() {
    let allowed_types = schema_enum_values("ObjectType");
    assert!(
        allowed_types.contains(&"workflow".to_string()),
        "ObjectType schema should include 'workflow' for Informatica support"
    );
    assert!(
        allowed_types.contains(&"mapping".to_string()),
        "ObjectType schema should include 'mapping' for Informatica support"
    );
}

#[test]
fn validate_rejects_unknown_platform_and_format_values() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let doc = serde_json::json!({
        (SCHEMA_VERSION_FIELD): 1,
        "id": "bad-platform-format",
        "kind": "script",
        "source": {
            "platform": "invalidPlatform",
            "format": "invalidFormat"
        },
        "files": {
            "source": {
                "path": "source/load.invalid"
            }
        }
    });
    fs::write(
        dir.path().join("registry/bad-platform-format.json"),
        serde_json::to_string_pretty(&doc).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert!(
        report.issues.iter().any(|i| {
            i.kind == ValidationIssueKind::SchemaViolation && i.message.contains("invalidPlatform")
        }),
        "expected invalid platform schema violation, got: {:?}",
        report.issues
    );
    assert!(
        report.issues.iter().any(|i| {
            i.kind == ValidationIssueKind::SchemaViolation && i.message.contains("invalidFormat")
        }),
        "expected invalid format schema violation, got: {:?}",
        report.issues
    );
}

#[test]
fn platform_and_format_enum_values_match_schema_contract() {
    assert_schema_enum_round_trips::<SourcePlatform>("SourcePlatform");
    assert_schema_enum_round_trips::<SourceFormat>("SourceFormat");
    assert_schema_enum_round_trips::<TargetFormat>("TargetFormat");
}

#[test]
fn validate_detects_id_filename_mismatch() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let unit = serde_json::json!({ "id": "wrong-id" });
    fs::write(
        dir.path().join("registry/correct-name.json"),
        serde_json::to_string_pretty(&unit).unwrap(),
    )
    .unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert!(report
        .issues
        .iter()
        .any(|i| i.kind == ValidationIssueKind::IdFilenameMismatch));
}

#[test]
fn validate_detects_duplicate_ids() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    let unit_a = serde_json::json!({ "id": "dup" });
    let unit_b = serde_json::json!({ "id": "dup" });
    fs::write(
        dir.path().join("registry/dup.json"),
        serde_json::to_string_pretty(&unit_a).unwrap(),
    )
    .unwrap();
    fs::write(
        dir.path().join("registry/dup2.json"),
        serde_json::to_string_pretty(&unit_b).unwrap(),
    )
    .unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    let dup_issues: Vec<_> = report
        .issues
        .iter()
        .filter(|i| i.kind == ValidationIssueKind::DuplicateId)
        .collect();
    assert!(
        !dup_issues.is_empty(),
        "expected duplicate ID issues, got: {:?}",
        report.issues
    );
}

#[test]
fn validate_detects_unresolved_dependency() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let mut unit = make_code_unit("dep-src", "t1", CodeUnitObjectType::Table);
    set_dependency_ids(&mut unit, &["nonexistent-id"]);
    registry.create(&mut unit, None).unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert!(report
        .issues
        .iter()
        .any(|i| i.kind == ValidationIssueKind::UnresolvedDependency));
}

#[test]
fn validate_unit_single_valid_file() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let mut unit = make_code_unit("vu1", "my_proc", CodeUnitObjectType::Procedure);
    registry.create(&mut unit, None).unwrap();
    let report = registry.validate_unit("vu1", ChecksumMode::NONE).unwrap();
    assert!(report.is_valid);
    assert_eq!(report.files_checked, 1);
}

#[test]
fn validate_unit_not_found() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let err = registry
        .validate_unit("nonexistent", ChecksumMode::NONE)
        .unwrap_err();
    assert_eq!(err.error_code_i32(), 1003);
}

#[test]
fn validate_collects_multiple_issues() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    fs::write(dir.path().join("registry/bad1.json"), "not-json").unwrap();
    fs::write(dir.path().join("registry/bad2.json"), "also-bad").unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert_eq!(report.files_checked, 2);
    let json_issues: Vec<_> = report
        .issues
        .iter()
        .filter(|i| i.kind == ValidationIssueKind::InvalidJson)
        .collect();
    assert_eq!(json_issues.len(), 2);
}

#[test]
fn validate_detects_missing_id() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    let unit_without_id = serde_json::json!({
        "kind": "databaseObject",
        "source": { "objectType": "table", "database": "DB", "schema": "dbo", "name": "T" },
        "target": { "objectType": "table", "database": "DB", "schema": "DBO", "name": "T" }
    });
    fs::write(
        dir.path().join("registry/no-id-unit.json"),
        serde_json::to_string_pretty(&unit_without_id).unwrap(),
    )
    .unwrap();
    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(!report.is_valid);
    assert!(
        report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::MissingId),
        "expected a MissingId issue, got: {:?}",
        report.issues
    );
}

#[test]
fn validate_checksum_detects_missing_file() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let path = write_temp_source(dir.path(), "gone.sql", b"content");
    let mut cu = make_code_unit_with_files("vc1", Some(path.clone()), None, None);
    registry.create(&mut cu, None).unwrap();
    registry
        .update_checksum("vc1", ChecksumMode::SOURCE)
        .unwrap();

    fs::remove_file(dir.path().join(path)).unwrap();

    let report = registry.validate(ChecksumMode::SOURCE).unwrap();
    assert!(!report.is_valid);
    assert!(
        report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::ChecksumMismatch
                && i.message.contains("File not found")),
        "expected a ChecksumMismatch for missing file, got: {:?}",
        report.issues
    );
}

#[test]
fn validate_checksum_detects_mismatch() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let path = write_temp_source(dir.path(), "drift.sql", b"v1");
    let mut cu = make_code_unit_with_files("vc2", Some(path.clone()), None, None);
    registry.create(&mut cu, None).unwrap();
    registry
        .update_checksum("vc2", ChecksumMode::SOURCE)
        .unwrap();

    fs::write(dir.path().join(path), b"v2").unwrap();

    let report = registry.validate(ChecksumMode::SOURCE).unwrap();
    assert!(!report.is_valid);
    assert!(
        report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::ChecksumMismatch
                && i.message.contains("Checksum mismatch")),
        "expected a ChecksumMismatch for content drift, got: {:?}",
        report.issues
    );
}

// ── Path normalization tests ──────────────────────────────────────────

#[test]
fn create_normalizes_backslash_paths() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    let mut cu = make_code_unit_with_files(
        "pn1",
        Some(r"source\Sales\tbl1.sql".to_string()),
        None,
        None,
    );
    registry.create(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("pn1", None).unwrap();
    assert_eq!(
        loaded.files.unwrap().source.unwrap().path.unwrap(),
        platform_path!(
            unix: r"source\Sales\tbl1.sql",
            windows: "source/Sales/tbl1.sql",
        ),
    );
}

#[test]
fn read_normalizes_backslash_paths_on_disk() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let raw_json = serde_json::json!({
        "id": "pn2",
        "kind": "databaseObject",
        "files": {
            "source": { "path": "source\\Sales\\file.sql" }
        }
    });
    let registry_dir = dir.path().join("registry");
    fs::write(
        registry_dir.join("pn2.json"),
        serde_json::to_string_pretty(&raw_json).unwrap(),
    )
    .unwrap();

    let loaded = registry.get_by_id("pn2", None).unwrap();
    assert_eq!(
        loaded.files.unwrap().source.unwrap().path.unwrap(),
        platform_path!(
            unix: r"source\Sales\file.sql",
            windows: "source/Sales/file.sql",
        ),
    );
}

#[test]
fn upsert_normalizes_dot_prefix_paths() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    let mut cu =
        make_code_unit_with_files("pn3", Some(r".\source\file.sql".to_string()), None, None);
    registry.upsert(&mut cu, None).unwrap();

    let loaded = registry.get_by_id("pn3", None).unwrap();
    // On Windows `.\` collapses to `./` and is stripped; on Unix the whole
    // string is a single literal filename so the `./` strip rule never matches.
    assert_eq!(
        loaded.files.unwrap().source.unwrap().path.unwrap(),
        platform_path!(
            unix: r".\source\file.sql",
            windows: "source/file.sql",
        ),
    );
}

#[test]
fn validate_reports_non_canonical_paths() {
    use crate::checksum::ChecksumMode;

    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let raw_json = serde_json::json!({
        "id": "pn4",
        "kind": "databaseObject",
        "files": {
            "source": { "path": "source\\Sales\\file.sql" }
        }
    });
    let registry_dir = dir.path().join("registry");
    fs::write(
        registry_dir.join("pn4.json"),
        serde_json::to_string_pretty(&raw_json).unwrap(),
    )
    .unwrap();

    let report = registry.validate(ChecksumMode::NONE).unwrap();
    assert!(
        !report.is_valid,
        "NonCanonicalPath should make is_valid false"
    );
    assert!(
        report
            .issues
            .iter()
            .any(|i| i.kind == ValidationIssueKind::NonCanonicalPath),
        "expected a NonCanonicalPath issue, got: {:?}",
        report.issues
    );
}

// ── Registry-aware schema migration integration tests ──────────────────

use crate::migration::SchemaMigrationContext;
use crate::migration::SchemaMigrationStep;

/// Fake per-file v1→v2: adds "addedInV2": "hello".
fn test_per_file_v1_to_v2(doc: &mut serde_json::Value) -> crate::error::Result<()> {
    if let Some(obj) = doc.as_object_mut() {
        obj.insert("addedInV2".to_string(), serde_json::json!("hello"));
    }
    Ok(())
}

/// Fake registry-aware v1→v2: reads all docs and stamps "peerCount"
/// on each target with the total document count.
fn test_registry_aware_v1_to_v2(ctx: &mut SchemaMigrationContext) -> crate::error::Result<()> {
    let total = ctx.len();
    let target_ids: Vec<String> = ctx.target_ids().map(|s| s.to_string()).collect();
    for id in &target_ids {
        if let Some(doc) = ctx.get_target_mut(id) {
            doc["peerCount"] = serde_json::json!(total);
        }
    }
    Ok(())
}

/// Fake registry-aware v2→v3: reads a non-target document and copies a
/// field from it into each target.
fn test_registry_aware_v2_to_v3(ctx: &mut SchemaMigrationContext) -> crate::error::Result<()> {
    let target_ids: Vec<String> = ctx.target_ids().map(|s| s.to_string()).collect();
    for id in &target_ids {
        let all_ids: Vec<String> = ctx.iter().map(|(i, _)| i.to_string()).collect();
        let non_target = all_ids.iter().find(|i| !target_ids.contains(i));
        let stamp = non_target
            .and_then(|nt_id| ctx.get(nt_id))
            .and_then(|d| d.get("id"))
            .cloned()
            .unwrap_or(serde_json::json!("none"));
        if let Some(doc) = ctx.get_target_mut(id) {
            doc["readFromPeer"] = stamp;
        }
    }
    Ok(())
}

/// Fake registry-aware step that always fails.
fn test_registry_aware_failing(_ctx: &mut SchemaMigrationContext) -> crate::error::Result<()> {
    SchemaMigrationSnafu {
        message: "simulated registry-aware failure".to_string(),
        context: None,
    }
    .fail()
}

/// Write a minimal JSON document at the given schema version.
fn write_test_doc(registry: &CodeUnitRegistry, id: &str, version: i64) {
    let doc = serde_json::json!({
        (SCHEMA_VERSION_FIELD): version,
        "id": id,
        "kind": "databaseObject",
        "source": {"objectType": "table", "name": id},
        "target": {"objectType": "table", "name": id}
    });
    let path = registry.id_to_path(id);
    fs::write(&path, serde_json::to_string_pretty(&doc).unwrap()).unwrap();
}

/// Read raw JSON from disk (bypasses registry read APIs).
fn read_raw_doc(registry: &CodeUnitRegistry, id: &str) -> serde_json::Value {
    let path = registry.id_to_path(id);
    serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap()
}

#[test]
fn test_migrate_schema_all_with_registry_aware_step() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "ra-1", 1);
    write_test_doc(&registry, "ra-2", 1);

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_v1_to_v2),
    )];

    let result = registry.migrate_schema_all_with_steps(steps, 2).unwrap();

    assert_eq!(result.succeeded.len(), 2);
    assert!(result.failed.is_empty());

    let doc1 = read_raw_doc(&registry, "ra-1");
    assert_eq!(doc1[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(doc1["peerCount"], 2);

    let doc2 = read_raw_doc(&registry, "ra-2");
    assert_eq!(doc2[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(doc2["peerCount"], 2);
}

#[test]
fn test_migrate_schema_all_registry_aware_can_read_non_target_documents() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "target-1", 1);
    write_test_doc(&registry, "already-v2", 2);

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_v1_to_v2),
    )];

    let result = registry.migrate_schema_all_with_steps(steps, 2).unwrap();

    assert_eq!(result.succeeded.len(), 1);
    assert!(result.failed.is_empty());

    let target = read_raw_doc(&registry, "target-1");
    assert_eq!(target[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(
        target["peerCount"], 2,
        "should see total count including non-target"
    );

    let non_target = read_raw_doc(&registry, "already-v2");
    assert_eq!(
        non_target[SCHEMA_VERSION_FIELD], 2,
        "non-target version unchanged"
    );
    assert!(
        non_target.get("peerCount").is_none(),
        "non-target should not have been modified"
    );
}

#[test]
fn test_migrate_schema_all_registry_aware_failure_is_all_or_nothing() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "aon-1", 1);
    write_test_doc(&registry, "aon-2", 1);

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_failing),
    )];

    let err = registry
        .migrate_schema_all_with_steps(steps, 2)
        .unwrap_err();
    assert_eq!(err.error_code_i32(), 1021);
    assert!(err.to_string().contains("simulated registry-aware failure"));

    let details = err.details().expect("should have structured details");
    assert_eq!(details["context"]["fromVersion"], 1);
    assert_eq!(details["context"]["toVersion"], 2);
    assert!(
        details["context"]["priorFailures"]
            .as_array()
            .unwrap()
            .is_empty(),
        "no prior failures in this test"
    );

    let doc1 = read_raw_doc(&registry, "aon-1");
    assert_eq!(
        doc1[SCHEMA_VERSION_FIELD], 1,
        "on failure, documents must not be modified on disk"
    );
    let doc2 = read_raw_doc(&registry, "aon-2");
    assert_eq!(doc2[SCHEMA_VERSION_FIELD], 1);
}

#[test]
fn test_migrate_schema_all_registry_aware_failure_includes_prior_failures() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "prior-good", 1);
    // Invalid JSON triggers a load-time failure recorded in BatchResult
    // *before* the registry-aware step runs.
    fs::write(
        dir.path().join("registry/prior-bad.json"),
        "not valid json{{{",
    )
    .unwrap();

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_failing),
    )];

    let err = registry
        .migrate_schema_all_with_steps(steps, 2)
        .unwrap_err();
    assert_eq!(err.error_code_i32(), 1021);

    let details = err.details().expect("should have structured details");
    let prior = details["context"]["priorFailures"].as_array().unwrap();
    assert_eq!(
        prior.len(),
        1,
        "one prior failure from the invalid-JSON doc"
    );
    assert_eq!(prior[0]["id"], "prior-bad");
    assert_eq!(prior[0]["error"]["code"], 1009, "JSON parse error code");
    assert!(
        prior[0]["error"]["trace"].is_array(),
        "full ErrorInfo trace should be preserved"
    );
}

#[test]
fn test_migrate_schema_all_mixed_chain() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "mix-1", 1);
    write_test_doc(&registry, "mix-2", 1);

    let steps: &[(i64, SchemaMigrationStep)] = &[
        (1, SchemaMigrationStep::PerFile(test_per_file_v1_to_v2)),
        (
            2,
            SchemaMigrationStep::RegistryAware(test_registry_aware_v2_to_v3),
        ),
    ];

    let result = registry.migrate_schema_all_with_steps(steps, 3).unwrap();

    assert_eq!(result.succeeded.len(), 2);
    assert!(result.failed.is_empty());

    let doc1 = read_raw_doc(&registry, "mix-1");
    assert_eq!(doc1[SCHEMA_VERSION_FIELD], 3);
    assert_eq!(doc1["addedInV2"], "hello");
    assert!(
        doc1.get("readFromPeer").is_some(),
        "registry-aware step should have run"
    );

    let doc2 = read_raw_doc(&registry, "mix-2");
    assert_eq!(doc2[SCHEMA_VERSION_FIELD], 3);
    assert_eq!(doc2["addedInV2"], "hello");
}

#[test]
fn test_migrate_schema_all_records_each_failed_document_once() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let future_doc = serde_json::json!({(SCHEMA_VERSION_FIELD): 999, "id": "future-dedup"});
    fs::write(
        dir.path().join("registry/future-dedup.json"),
        serde_json::to_string_pretty(&future_doc).unwrap(),
    )
    .unwrap();
    write_test_doc(&registry, "good-dedup", 1);

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_v1_to_v2),
    )];

    let result = registry.migrate_schema_all_with_steps(steps, 2).unwrap();

    let future_failures: Vec<_> = result
        .failed
        .iter()
        .filter(|f| f.id == "future-dedup")
        .collect();
    assert_eq!(
        future_failures.len(),
        1,
        "failed document should appear exactly once, got {}",
        future_failures.len()
    );
}

#[test]
fn test_migrate_schema_all_registry_aware_preserves_doc_count() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "count-1", 1);
    write_test_doc(&registry, "count-2", 1);
    write_test_doc(&registry, "count-3", 1);

    let steps: &[(i64, SchemaMigrationStep)] = &[(
        1,
        SchemaMigrationStep::RegistryAware(test_registry_aware_v1_to_v2),
    )];

    let result = registry.migrate_schema_all_with_steps(steps, 2).unwrap();

    assert_eq!(result.succeeded.len(), 3);
    assert!(result.failed.is_empty());

    for id in &["count-1", "count-2", "count-3"] {
        let doc = read_raw_doc(&registry, id);
        assert_eq!(doc[SCHEMA_VERSION_FIELD], 2);
        assert_eq!(doc["peerCount"], 3);
    }
}

#[test]
fn test_migrate_schema_all_registry_aware_failure_restores_docs() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "restore-1", 1);
    write_test_doc(&registry, "restore-2", 1);

    /// Modifies a target, then returns Err — tests that docs are restored.
    fn modify_then_fail(ctx: &mut SchemaMigrationContext) -> crate::error::Result<()> {
        let ids: Vec<String> = ctx.target_ids().map(|s| s.to_string()).collect();
        for id in &ids {
            if let Some(doc) = ctx.get_target_mut(id) {
                doc["shouldNotPersist"] = serde_json::json!(true);
            }
        }
        SchemaMigrationSnafu {
            message: "fail after mutation".to_string(),
            context: None,
        }
        .fail()
    }

    let steps: &[(i64, SchemaMigrationStep)] =
        &[(1, SchemaMigrationStep::RegistryAware(modify_then_fail))];

    let err = registry
        .migrate_schema_all_with_steps(steps, 2)
        .unwrap_err();
    assert_eq!(err.error_code_i32(), 1021);

    let doc1 = read_raw_doc(&registry, "restore-1");
    assert!(
        doc1.get("shouldNotPersist").is_none(),
        "on-disk documents must not reflect in-memory mutations from a failed step"
    );
    assert_eq!(doc1[SCHEMA_VERSION_FIELD], 1);
}

#[test]
fn test_migrate_schema_all_per_file_only_short_circuit() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "pf-1", 1);

    let steps: &[(i64, SchemaMigrationStep)] =
        &[(1, SchemaMigrationStep::PerFile(test_per_file_v1_to_v2))];

    let result = registry.migrate_schema_all_with_steps(steps, 2).unwrap();

    assert_eq!(result.succeeded.len(), 1);
    assert!(result.failed.is_empty());

    let doc = read_raw_doc(&registry, "pf-1");
    assert_eq!(doc[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(doc["addedInV2"], "hello");
}

// ── Unknown field preservation tests ───────────────────────────────────

#[test]
fn test_unknown_fields_preserved_through_update() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("preserve-001", "T1", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let file_path = registry.id_to_path("preserve-001");
    let mut raw: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    raw["futureField"] = serde_json::json!("preserved_value");
    raw["futureObject"] = serde_json::json!({"nested": true, "count": 42});
    raw["source"]["futureSourceField"] = serde_json::json!("nested_preserved");
    fs::write(&file_path, serde_json::to_string_pretty(&raw).unwrap()).unwrap();

    registry
        .update(
            "preserve-001",
            &[("source.name", serde_json::json!("UpdatedName"))],
            None,
        )
        .unwrap();

    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    assert_eq!(on_disk["futureField"], "preserved_value");
    assert_eq!(on_disk["futureObject"]["nested"], true);
    assert_eq!(on_disk["futureObject"]["count"], 42);
    assert_eq!(on_disk["source"]["futureSourceField"], "nested_preserved");
    assert_eq!(on_disk["source"]["name"], "UpdatedName");
}

#[test]
fn test_unknown_fields_preserved_through_upsert() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("preserve-002", "T2", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let file_path = registry.id_to_path("preserve-002");
    let mut raw: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    raw["futureField"] = serde_json::json!("keep_me");
    fs::write(&file_path, serde_json::to_string_pretty(&raw).unwrap()).unwrap();

    let mut patch = CodeUnit {
        id: Some("preserve-002".to_string()),
        source: Some(SourceMetadata {
            name: Some("MergedName".to_string()),
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    assert_eq!(on_disk["futureField"], "keep_me");
    assert_eq!(on_disk["source"]["name"], "MergedName");
}

#[test]
fn test_unknown_fields_preserved_through_dependency_refresh() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut dep = make_code_unit("dep-target", "DepTarget", CodeUnitObjectType::Table);
    registry.create(&mut dep, None).unwrap();

    let dep_path = registry.id_to_path("dep-target");
    let mut raw: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&dep_path).unwrap()).unwrap();
    raw["futureDepField"] = serde_json::json!("dep_preserved");
    fs::write(&dep_path, serde_json::to_string_pretty(&raw).unwrap()).unwrap();

    let mut dependent = make_code_unit("dep-source", "DepSource", CodeUnitObjectType::View);
    set_dependency_ids(&mut dependent, &["dep-target"]);
    registry.create(&mut dependent, None).unwrap();

    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&dep_path).unwrap()).unwrap();
    assert_eq!(on_disk["futureDepField"], "dep_preserved");
}

#[test]
fn test_unknown_fields_preserved_through_hooks() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("preserve-hooks", "HookTest", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let file_path = registry.id_to_path("preserve-hooks");
    let mut raw: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    raw["futureHookField"] = serde_json::json!({"nested": "value"});
    raw["codeStatus"]["futurePhase"] = serde_json::json!({"status": "testing"});
    fs::write(&file_path, serde_json::to_string_pretty(&raw).unwrap()).unwrap();

    registry
        .update(
            "preserve-hooks",
            &[(
                "codeStatus.registration.status",
                serde_json::json!("completed"),
            )],
            None,
        )
        .unwrap();

    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    assert_eq!(on_disk["futureHookField"]["nested"], "value");
    assert_eq!(on_disk["codeStatus"]["futurePhase"]["status"], "testing");
    assert_eq!(on_disk["codeStatus"]["registration"]["status"], "completed");
}

#[test]
fn test_unknown_fields_preserved_through_migrate_schema_all() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("preserve-migrate", "MigTest", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let file_path = registry.id_to_path("preserve-migrate");
    let mut raw: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    raw["futureFieldFromNewerSchema"] = serde_json::json!("should_survive_migration");
    raw["source"]["futureNested"] = serde_json::json!(42);
    fs::write(&file_path, serde_json::to_string_pretty(&raw).unwrap()).unwrap();

    // migrate_schema_all is a no-op at schema v1 (no migrations exist yet),
    // so also exercise the write path that migrate_schema_file uses when a
    // real migration runs: read → mutate → validate → write_json_inner.
    let result = registry.migrate_schema_all().unwrap();
    assert!(result.failed.is_empty());

    let mut migrated =
        serde_json::from_str::<serde_json::Value>(&fs::read_to_string(&file_path).unwrap())
            .unwrap();
    migrated["source"]["name"] = serde_json::json!("MigratedName");
    let _validated: CodeUnit = serde_json::from_value(migrated.clone()).unwrap();
    registry
        .write_json_inner(&file_path, &migrated, false, false)
        .unwrap();

    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();
    assert_eq!(
        on_disk["futureFieldFromNewerSchema"],
        "should_survive_migration"
    );
    assert_eq!(on_disk["source"]["futureNested"], 42);
    assert_eq!(on_disk["source"]["name"], "MigratedName");
}

#[test]
fn test_create_does_not_introduce_phantom_fields() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("phantom-check", "PC", CodeUnitObjectType::Table);
    let id = registry.create(&mut cu, None).unwrap();

    let file_path = registry.id_to_path(&id);
    let on_disk: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&file_path).unwrap()).unwrap();

    let loaded = registry.get_by_id(&id, None).unwrap();
    let from_struct = serde_json::to_value(&loaded).unwrap();

    let disk_keys: std::collections::BTreeSet<&String> =
        on_disk.as_object().unwrap().keys().collect();
    let struct_keys: std::collections::BTreeSet<&String> =
        from_struct.as_object().unwrap().keys().collect();

    assert_eq!(
        disk_keys, struct_keys,
        "On-disk keys should match CodeUnit serialization keys exactly"
    );
}

#[test]
fn test_empty_vec_fields_not_skipped_during_serialization() {
    use crate::generated::types::Dependencies;
    let deps = Dependencies {
        depends_on: vec![],
        required_by: vec![],
        ..Default::default()
    };
    let value = serde_json::to_value(&deps).unwrap();
    let obj = value.as_object().unwrap();
    assert!(
        obj.contains_key("dependsOn"),
        "empty dependsOn must be serialized"
    );
    assert!(
        obj.contains_key("requiredBy"),
        "empty requiredBy must be serialized"
    );
}

// ── CanonicalNameHook tests ──────────────────────────────────────────

#[test]
fn canonical_name_set_on_create_table() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("cn1", "MyTable", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("cn1", None).unwrap();
    assert_eq!(
        stored.source.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.dbo.MyTable"),
    );
    assert_eq!(
        stored.target.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.DBO.MYTABLE"),
    );
}

#[test]
fn canonical_name_includes_params_for_procedure() {
    use crate::generated::types::{ParameterDef, Parameters, Signature};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("cn2", "MyProc", CodeUnitObjectType::Procedure);
    cu.signature = Some(Signature {
        parameters: Some(Parameters {
            arguments: vec![
                ParameterDef {
                    name: Some("@StartDate".to_string()),
                    type_: Some("DATETIME".to_string()),
                    target_type: Some("TIMESTAMP_NTZ".to_string()),
                    ..Default::default()
                },
                ParameterDef {
                    name: Some("@Region".to_string()),
                    type_: Some("NVARCHAR(50)".to_string()),
                    target_type: Some("VARCHAR(50)".to_string()),
                    ..Default::default()
                },
            ],
            ..Default::default()
        }),
        ..Default::default()
    });
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("cn2", None).unwrap();
    assert_eq!(
        stored.source.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.dbo.MyProc(DATETIME,NVARCHAR)"),
    );
    assert_eq!(
        stored.target.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.DBO.MYPROC(TIMESTAMP_NTZ,VARCHAR)"),
    );
}

#[test]
fn canonical_name_updated_on_update() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("cn6", "OldName", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let stored = registry.get_by_id("cn6", None).unwrap();
    assert_eq!(
        stored.source.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.dbo.OldName"),
    );

    registry
        .update(
            "cn6",
            &[("source.name", serde_json::json!("NewName"))],
            None,
        )
        .unwrap();

    let updated = registry.get_by_id("cn6", None).unwrap();
    assert_eq!(
        updated.source.as_ref().unwrap().canonical_name.as_deref(),
        Some("DB.dbo.NewName"),
        "canonicalName should reflect the updated name"
    );
}

fn make_etl_code_unit(id: &str, parts_config: Vec<(&str, &str, Vec<(&str, &[&str])>)>) -> CodeUnit {
    let parts = parts_config
        .into_iter()
        .map(|(part_id, target_format, deps)| Part {
            id: Some(part_id.to_string()),
            name: Some(part_id.to_string()),
            part_type: Some("dataFlow".to_string()),
            target: Some(PartTarget {
                path: Some(format!("converted/{part_id}/")),
                format: Some(target_format.parse::<TargetFormat>().unwrap()),
                ..Default::default()
            }),
            dependencies: Some(Dependencies {
                depends_on: deps
                    .into_iter()
                    .map(|(dep_id, rel_types)| Dependency {
                        id: Some(dep_id.to_string()),
                        is_missing: None,
                        relation_types: rel_types.iter().map(|s| s.to_string()).collect(),
                    })
                    .collect(),
                ..Default::default()
            }),
            ..Default::default()
        })
        .collect();

    CodeUnit {
        id: Some(id.to_string()),
        kind: Some(CodeUnitKind::Etl),
        parts: Some(parts),
        ..Default::default()
    }
}

#[test]
fn test_create_etl_with_part_deps_triggers_graph_refresh() {
    let dir = temp_dir();
    let reg = CodeUnitRegistry::init(dir.path()).unwrap();

    let table = make_code_unit("src-table", "Customers", CodeUnitObjectType::Table);
    let etl = make_etl_code_unit(
        "etl-pkg",
        vec![("df-1", "dbt", vec![("src-table", &["SELECT"])])],
    );

    reg.create_batch(&mut [table, etl], None).unwrap();

    let loaded = reg.get_by_id("src-table", None).unwrap();
    let required_by = &loaded.dependencies.as_ref().unwrap().required_by;
    assert!(
        required_by.contains(&"etl-pkg".to_string()),
        "Expected src-table to be required by etl-pkg, got: {:?}",
        required_by
    );
}

#[test]
fn validate_allows_root_depends_on_between_etl_units() {
    let dir = temp_dir();
    let reg = CodeUnitRegistry::init(dir.path()).unwrap();

    // A workflow uses its mapping: the authored edge is workflow.dependsOn ->
    // mapping, so the mapping is the predecessor (deploys first) and the
    // mapping's requiredBy is the derived inverse computed by refresh.
    let mapping = make_etl_code_unit("etl-mapping", vec![("df-map", "dbt", vec![])]);
    let mut workflow = make_etl_code_unit("etl-workflow", vec![("df-wf", "dbt", vec![])]);
    workflow.dependencies = Some(Dependencies {
        depends_on: vec![Dependency {
            id: Some("etl-mapping".to_string()),
            is_missing: None,
            relation_types: vec![],
        }],
        ..Default::default()
    });

    reg.create_batch(&mut [mapping, workflow], None).unwrap();

    let report = reg.validate(ChecksumMode::NONE).unwrap();
    assert!(
        report.is_valid,
        "etl units with root dependsOn should pass validation, got validation issues: {:?}",
        report.issues
    );

    let mapping = reg.get_by_id("etl-mapping", None).unwrap();
    let required_by = &mapping.dependencies.as_ref().unwrap().required_by;
    assert!(
        required_by.contains(&"etl-workflow".to_string()),
        "Expected etl-mapping to be required by etl-workflow, got: {:?}",
        required_by
    );

    let workflow = reg.get_by_id("etl-workflow", None).unwrap();
    let workflow_rank = workflow.planning.unwrap().topological_rank.unwrap();
    let mapping_rank = mapping.planning.unwrap().topological_rank.unwrap();
    assert!(
        workflow_rank > mapping_rank,
        "workflow should deploy after mapping (higher rank), got workflow={workflow_rank} mapping={mapping_rank}",
    );
}

#[test]
fn test_etl_code_unit_round_trip() {
    let dir = temp_dir();
    let reg = init_bare(dir.path());

    let mut etl = make_etl_code_unit("etl-rt", vec![("df-1", "dbt", vec![])]);
    etl.parts.as_mut().unwrap()[0]
        .target
        .as_mut()
        .unwrap()
        .model_name = Some("my_model".to_string());

    reg.create_batch(&mut [etl], None).unwrap();

    let loaded = reg.get_by_id("etl-rt", None).unwrap();
    assert_eq!(loaded.parts.as_ref().unwrap().len(), 1);
    let target = loaded.parts.as_ref().unwrap()[0].target.as_ref().unwrap();
    assert_eq!(target.model_name.as_deref(), Some("my_model"));
    assert_eq!(target.format.as_ref(), Some(&TargetFormat::Dbt));
    assert_eq!(loaded.kind, Some(CodeUnitKind::Etl));
}

#[test]
fn test_etl_part_deps_get_is_missing_from_graph() {
    let dir = temp_dir();
    let reg = CodeUnitRegistry::init(dir.path()).unwrap();

    let etl = make_etl_code_unit(
        "etl-missing",
        vec![("df-1", "dbt", vec![("nonexistent-dep", &["SELECT"])])],
    );

    reg.create_batch(&mut [etl], None).unwrap();

    let loaded = reg.get_by_id("etl-missing", None).unwrap();
    let part_deps = loaded.parts.as_ref().unwrap()[0]
        .dependencies
        .as_ref()
        .unwrap();
    assert_eq!(part_deps.depends_on[0].is_missing, Some(true));
}

// ── End-to-end tests for kind: script ────────────────────────────────────

#[cfg(test)]
mod script_kind_e2e_tests {
    use super::*;
    use crate::generated::types::{FileEntry, Files};
    use crate::validation::ValidationIssueKind;

    // ── Fixture values ──────────────────────────────────────────────────
    // Centralised so the same platform/format/path strings drive both the
    // unit under test and the canonical-name assertions, keeping the two
    // in lockstep.

    /// Source side of a Teradata BTEQ script.
    const SOURCE_PLATFORM: &str = "teradata";
    const SOURCE_FORMAT: &str = "bteq";
    const SOURCE_PATH: &str = "source/etl/daily/load_sales.bteq";

    /// Target side: the converted Snowflake/Python form of the BTEQ script.
    const TARGET_PLATFORM: &str = "snowflake";
    const TARGET_FORMAT: &str = "python";
    const TARGET_PATH: &str = "converted/etl/daily/load_sales.py";

    /// Generated helper script: target-only Python module produced by the
    /// converter (no Teradata source — exercises the target-only lifecycle).
    const GENERATED_HELPER_PATH: &str = "converted/helpers/snowconvert_helpers/__init__.py";

    /// Fixture databaseObject name shared by the databaseObject e2e tests.
    const DB_OBJECT_NAME: &str = "Customers";

    /// Canonical-name composition mirrors `compute_path_based_canonical_name`
    /// in `crate::canonical_name` so a change to the format is caught here.
    fn canonical_name(platform: &str, format: &str, path: &str) -> String {
        format!("{platform}:{format}:{path}")
    }

    fn make_bteq_script(id: &str) -> CodeUnit {
        CodeUnit {
            id: Some(id.to_string()),
            kind: Some(CodeUnitKind::Script),
            source: Some(SourceMetadata {
                platform: Some(SourcePlatform::Teradata),
                format: Some(SourceFormat::Bteq),
                ..Default::default()
            }),
            target: Some(TargetMetadata {
                format: Some(TargetFormat::Python),
                ..Default::default()
            }),
            files: Some(Files {
                source: Some(FileEntry {
                    path: Some(SOURCE_PATH.to_string()),
                    checksum: None,
                }),
                converted: Some(FileEntry {
                    path: Some(TARGET_PATH.to_string()),
                    checksum: None,
                }),
                ..Default::default()
            }),
            ..Default::default()
        }
    }

    #[test]
    fn script_unit_round_trips_and_validates_clean() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = make_bteq_script("11223344-5566-7788-99aa-bbccddeeff00");
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "BTEQ script should validate clean, issues: {:?}",
            report.issues
        );

        let loaded = registry
            .find_all(FindOptions::default())
            .unwrap()
            .into_iter()
            .next()
            .expect("one unit");
        assert_eq!(loaded.kind, Some(CodeUnitKind::Script));
        let s = loaded.source.as_ref().expect("source");
        assert_eq!(s.platform.as_ref(), Some(&SourcePlatform::Teradata));
        assert_eq!(s.format.as_ref(), Some(&SourceFormat::Bteq));
        let t = loaded.target.as_ref().expect("target");
        assert_eq!(t.format.as_ref(), Some(&TargetFormat::Python));
    }

    #[test]
    fn script_metadata_io_round_trips_and_validates_clean() {
        use crate::generated::types::{
            ScriptBinding, ScriptBindingKind, ScriptIoDirection, ScriptIoEntry, ScriptIoFormat,
            ScriptIoPath, ScriptIoPathKind, ScriptIoReachability, ScriptMetadata,
        };
        use crate::validation::script_io::{validate_script_io, ProvidedIo};

        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = make_bteq_script("33445566-7788-99aa-bbcc-ddeeff001122");
        unit.script_bindings = Some(vec![ScriptBinding {
            name: Some("err_file".to_string()),
            kind: ScriptBindingKind::File,
        }]);
        unit.script_metadata = Some(ScriptMetadata {
            io: vec![ScriptIoEntry {
                direction: Some(ScriptIoDirection::Write),
                format: Some(ScriptIoFormat::Text),
                format_native: Some("report".to_string()),
                ordinal: Some(0),
                reachability: Some(ScriptIoReachability::Always),
                path: Some(ScriptIoPath {
                    kind: Some(ScriptIoPathKind::Binding),
                    name: Some("err_file".to_string()),
                    source: Some("${err_file}".to_string()),
                    target: Some("<%err_file%>".to_string()),
                }),
                ..Default::default()
            }],
        });
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "script with scriptMetadata should validate clean, issues: {:?}",
            report.issues
        );

        let loaded = registry
            .find_all(FindOptions::default())
            .unwrap()
            .into_iter()
            .next()
            .expect("one unit");
        let io = &loaded
            .script_metadata
            .as_ref()
            .expect("scriptMetadata missing")
            .io;
        assert_eq!(io.len(), 1, "one IO entry should round-trip");
        let entry = &io[0];
        assert_eq!(entry.direction, Some(ScriptIoDirection::Write));
        assert_eq!(entry.format, Some(ScriptIoFormat::Text));
        assert_eq!(entry.format_native.as_deref(), Some("report"));
        assert_eq!(entry.ordinal, Some(0));
        assert_eq!(entry.reachability, Some(ScriptIoReachability::Always));
        let path = entry.path.as_ref().expect("path");
        assert_eq!(path.kind, Some(ScriptIoPathKind::Binding));
        assert_eq!(path.name.as_deref(), Some("err_file"));
        assert_eq!(path.source.as_deref(), Some("${err_file}"));
        assert_eq!(path.target.as_deref(), Some("<%err_file%>"));

        // The standalone helper agrees the test's declared write lines up.
        let diff = validate_script_io(
            &loaded,
            &[ProvidedIo {
                direction: ScriptIoDirection::Write,
                path: ScriptIoPath {
                    kind: Some(ScriptIoPathKind::Binding),
                    name: Some("err_file".to_string()),
                    source: None,
                    target: None,
                },
            }],
        )
        .unwrap();
        assert!(
            diff.missing.is_empty() && diff.extra.is_empty() && diff.direction_mismatch.is_empty(),
            "helper should report a clean diff, got {diff:?}"
        );
    }

    #[test]
    fn script_canonical_name_is_set_per_side_by_hook() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = make_bteq_script("22334455-6677-8899-aabb-ccddeeff0011");
        registry.create(&mut unit, None).unwrap();

        let loaded = registry
            .find_all(FindOptions::default())
            .unwrap()
            .into_iter()
            .next()
            .expect("one unit");
        let expected_source = canonical_name(SOURCE_PLATFORM, SOURCE_FORMAT, SOURCE_PATH);
        let expected_target = canonical_name(TARGET_PLATFORM, TARGET_FORMAT, TARGET_PATH);
        assert_eq!(
            loaded
                .source
                .as_ref()
                .and_then(|s| s.canonical_name.as_deref()),
            Some(expected_source.as_str()),
            "source.canonicalName should be computed by the persistence hook"
        );
        assert_eq!(
            loaded
                .target
                .as_ref()
                .and_then(|t| t.canonical_name.as_deref()),
            Some(expected_target.as_str()),
            "target.canonicalName should be computed by the persistence hook"
        );
    }

    #[test]
    fn generated_script_target_only_validates_clean() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = CodeUnit {
            id: Some("99aabbcc-ddee-ff00-1122-334455667788".to_string()),
            kind: Some(CodeUnitKind::Script),
            target: Some(TargetMetadata {
                format: Some(TargetFormat::Python),
                ..Default::default()
            }),
            files: Some(Files {
                converted: Some(FileEntry {
                    path: Some(GENERATED_HELPER_PATH.to_string()),
                    checksum: None,
                }),
                ..Default::default()
            }),
            ..Default::default()
        };
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "generated script (target-only) should validate clean, issues: {:?}",
            report.issues
        );
    }

    #[test]
    fn database_object_without_platform_format_validates_clean() {
        // platform and format are optional on databaseObject — `make_code_unit`
        // omits them, so creating a unit through it exercises that path.
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = make_code_unit(
            "deadbeef-cafe-0000-0000-000000000001",
            DB_OBJECT_NAME,
            CodeUnitObjectType::Table,
        );
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "databaseObject without platform/format should validate clean, issues: {:?}",
            report.issues
        );
    }

    #[test]
    fn database_object_missing_source_name_is_rejected_by_per_kind_validation() {
        // Confirms that PerKindStructure issues bubble up through the public
        // CodeUnitRegistry::validate API.
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = make_code_unit(
            "deadbeef-cafe-0000-0000-000000000002",
            DB_OBJECT_NAME,
            CodeUnitObjectType::Table,
        );
        unit.source.as_mut().unwrap().name = None;
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(!report.is_valid, "expected validation to fail");
        assert!(
            report
                .issues
                .iter()
                .any(|i| i.kind == ValidationIssueKind::PerKindStructure
                    && i.message.contains("source.name")),
            "expected PerKindStructure issue mentioning source.name, got: {:?}",
            report.issues
        );
    }
}

#[cfg(test)]
mod script_bindings_tests {
    use super::*;
    use crate::generated::types::{
        ScriptBinding, ScriptBindingKind, ScriptIoDirection, ScriptIoEntry, ScriptIoPath,
        ScriptIoPathKind, ScriptMetadata, SourceFormat, SourcePlatform,
    };
    use std::collections::HashMap;

    fn make_dep_with_tokens(id: &str, src_db: &str, tgt_db: &str) -> CodeUnit {
        let mut unit = make_code_unit(id, "error_codes", CodeUnitObjectType::Table);
        unit.is_missing = true;
        let src = unit.source.as_mut().unwrap();
        src.database = Some(src_db.to_string());
        let tgt = unit.target.as_mut().unwrap();
        tgt.database = Some(tgt_db.to_string());
        unit
    }

    fn make_script(id: &str, bindings: Vec<(&str, ScriptBindingKind)>) -> CodeUnit {
        CodeUnit {
            id: Some(id.to_string()),
            kind: Some(CodeUnitKind::Script),
            source: Some(SourceMetadata {
                platform: Some(SourcePlatform::Teradata),
                format: Some(SourceFormat::Bteq),
                ..Default::default()
            }),
            script_bindings: Some(
                bindings
                    .into_iter()
                    .map(|(name, kind)| ScriptBinding {
                        name: Some(name.to_string()),
                        kind,
                    })
                    .collect(),
            ),
            ..Default::default()
        }
    }

    fn find_one(units: &[CodeUnit], id: &str) -> CodeUnit {
        units
            .iter()
            .find(|u| u.id.as_deref() == Some(id))
            .unwrap_or_else(|| panic!("unit {id} missing from result"))
            .clone()
    }

    #[test]
    fn test_find_all_bindings_substitutes_literal_tokens() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut script = make_script("script", vec![("DB", ScriptBindingKind::Database)]);
        let mut dep = make_dep_with_tokens("dep", "${DB}", "<% DB %>");
        set_dependencies(&mut script, &[("dep", Some(true))]);
        registry.create(&mut script, None).unwrap();
        registry.create(&mut dep, None).unwrap();

        // bindings: None → tokens preserved (regression guard)
        let none_units = registry.find_all(FindOptions::default()).unwrap();
        let dep_none = find_one(&none_units, "dep");
        assert_eq!(
            dep_none.source.as_ref().unwrap().database.as_deref(),
            Some("${DB}")
        );
        assert_eq!(
            dep_none.target.as_ref().unwrap().database.as_deref(),
            Some("<% DB %>")
        );

        // bindings with only the source-side wrapper → only source.* substituted
        let mut source_only = HashMap::new();
        source_only.insert("${DB}".to_string(), "PROD_UTIL".to_string());
        let src_units = registry
            .find_all(FindOptions {
                bindings: Some(&source_only),
                ..FindOptions::default()
            })
            .unwrap();
        let dep_src = find_one(&src_units, "dep");
        assert_eq!(
            dep_src.source.as_ref().unwrap().database.as_deref(),
            Some("PROD_UTIL")
        );
        assert_eq!(
            dep_src.target.as_ref().unwrap().database.as_deref(),
            Some("<% DB %>")
        );

        // bindings with both wrappers → both sides substituted
        let mut both = HashMap::new();
        both.insert("${DB}".to_string(), "PROD_UTIL".to_string());
        both.insert("<% DB %>".to_string(), "SC_TEST_UTIL".to_string());
        let both_units = registry
            .find_all(FindOptions {
                bindings: Some(&both),
                ..FindOptions::default()
            })
            .unwrap();
        let dep_both = find_one(&both_units, "dep");
        assert_eq!(
            dep_both.source.as_ref().unwrap().database.as_deref(),
            Some("PROD_UTIL")
        );
        assert_eq!(
            dep_both.target.as_ref().unwrap().database.as_deref(),
            Some("SC_TEST_UTIL")
        );
    }

    /// A `database-bindings.yml` drives `find_all` end to end.
    ///
    /// This is the whole point of `database_bindings`: the caller supplies the file
    /// SnowConvert generated, not a hand-wrapped token map, and the read returns
    /// physical names.
    #[test]
    /// A bindings file whose key case differs from the case the conversion wrote
    /// must still resolve, end to end through `find_all` — not merely produce a
    /// map containing the right keys.
    ///
    /// This is the integration form of the regression: `substitute_literal`
    /// matches byte-exact and `apply_bindings` leaves an unmatched token alone, so
    /// before the token map emitted case variants this returned the token verbatim
    /// with no error, and the caller shipped `<%dutchie_test%>` into SQL.
    #[test]
    fn test_find_all_binds_when_yaml_key_case_differs_from_the_token() {
        use crate::database_bindings::parse_database_bindings;

        let dir = temp_dir();
        let registry = init_bare(dir.path());

        // the engine writes the canonical name lower-case ...
        let mut dep = make_dep_with_tokens("dep", "${dutchie_test}", "<%dutchie_test%>");
        registry.create(&mut dep, None).unwrap();

        // ... while the config normaliser upper-cases it in the bindings file
        let bindings = parse_database_bindings(
            "source:\n  DUTCHIE_TEST: dutchie_test\nsnow:\n  DUTCHIE_TEST: DUTCHIE_EXTRACT_MIG\n",
        )
        .unwrap();

        let snow = bindings.snow_token_map();
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&snow),
                ..FindOptions::default()
            })
            .unwrap();
        assert_eq!(
            find_one(&units, "dep")
                .target
                .as_ref()
                .unwrap()
                .database
                .as_deref(),
            Some("DUTCHIE_EXTRACT_MIG"),
            "upper-case YAML key must resolve the lower-case token the engine wrote"
        );

        let source = bindings.source_token_map_default();
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&source),
                ..FindOptions::default()
            })
            .unwrap();
        assert_eq!(
            find_one(&units, "dep")
                .source
                .as_ref()
                .unwrap()
                .database
                .as_deref(),
            Some("dutchie_test"),
            "same on the source side"
        );
    }

    /// The caller passes a *path* and gets bound units — no parsing, no token map,
    /// and both sides resolved in one read.
    #[test]
    fn test_find_all_binds_from_a_path_alone() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());
        let mut dep = make_dep_with_tokens("dep", "${dutchie_test}", "<%dutchie_test%>");
        registry.create(&mut dep, None).unwrap();

        let bindings_file = dir.path().join("database-bindings.yml");
        std::fs::write(
            &bindings_file,
            "source:\n  dutchie_test: dutchie_test\nsnow:\n  dutchie_test: DUTCHIE_EXTRACT_MIG\n",
        )
        .unwrap();

        let units = registry
            .find_all(FindOptions {
                bindings_path: Some(&bindings_file),
                ..FindOptions::default()
            })
            .unwrap();
        let got = find_one(&units, "dep");
        // Both sides at once: safe because `${...}` and `<%...%>` cannot match each other.
        assert_eq!(
            got.target.as_ref().unwrap().database.as_deref(),
            Some("DUTCHIE_EXTRACT_MIG")
        );
        assert_eq!(
            got.source.as_ref().unwrap().database.as_deref(),
            Some("dutchie_test")
        );
    }

    /// Both inputs set is ambiguous, so it is refused rather than given a silent
    /// precedence rule.
    #[test]
    fn test_find_all_rejects_bindings_and_bindings_path_together() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());
        let bindings_file = dir.path().join("database-bindings.yml");
        std::fs::write(&bindings_file, "snow:\n  a: B\n").unwrap();
        let map: std::collections::HashMap<String, String> =
            [("<%a%>".to_string(), "C".to_string())]
                .into_iter()
                .collect();

        let err = registry
            .find_all(FindOptions {
                bindings: Some(&map),
                bindings_path: Some(&bindings_file),
                ..FindOptions::default()
            })
            .unwrap_err();
        assert!(
            format!("{err}").contains("not both"),
            "unexpected error: {err}"
        );
    }

    /// A missing file surfaces from the read instead of silently binding nothing —
    /// the whole point of moving the IO in here.
    #[test]
    fn test_find_all_bindings_path_missing_file_errors() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());
        let err = registry
            .find_all(FindOptions {
                bindings_path: Some(&dir.path().join("nope.yml")),
                ..FindOptions::default()
            })
            .unwrap_err();
        let msg = format!("{err}");
        assert!(
            !msg.is_empty(),
            "a missing bindings file must not read as success"
        );
    }

    /// The round trip a bindable conversion produces: a snow map resolves the target
    /// side and provably leaves the source token alone, and the source map the mirror.
    #[test]
    fn test_find_all_with_database_bindings_file() {
        use crate::database_bindings::parse_database_bindings;

        let dir = temp_dir();
        let registry = init_bare(dir.path());

        // exactly what a bindable conversion writes
        let mut dep = make_dep_with_tokens("dep", "${dutchie_test}", "<%dutchie_test%>");
        registry.create(&mut dep, None).unwrap();

        let bindings = parse_database_bindings(
            "source:\n  dutchie_test: dutchie_test\nsnow:\n  dutchie_test: DUTCHIE_EXTRACT_MIG\n",
        )
        .unwrap();

        // snow map resolves the target side and leaves the source token alone
        let snow = bindings.snow_token_map();
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&snow),
                ..FindOptions::default()
            })
            .unwrap();
        let got = find_one(&units, "dep");
        assert_eq!(
            got.target.as_ref().unwrap().database.as_deref(),
            Some("DUTCHIE_EXTRACT_MIG")
        );
        assert_eq!(
            got.source.as_ref().unwrap().database.as_deref(),
            Some("${dutchie_test}"),
            "a snow-only map must not touch the source side"
        );

        // source map resolves the source side, identity value included
        let source = bindings.source_token_map_default();
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&source),
                ..FindOptions::default()
            })
            .unwrap();
        let got = find_one(&units, "dep");
        assert_eq!(
            got.source.as_ref().unwrap().database.as_deref(),
            Some("dutchie_test")
        );
        assert_eq!(
            got.target.as_ref().unwrap().database.as_deref(),
            Some("<%dutchie_test%>")
        );
    }

    /// Pins the hazard documented on `database_bindings`: a bound read also
    /// rewrites `target.canonical_name`.
    ///
    /// Consumers deriving a frozen identity (baseline keys, stage paths, on-disk
    /// layout) must read *unbound*, because this substitution is silent — nothing
    /// errors, the identity simply changes and previously stored artifacts stop
    /// matching. Asserted so the property is known rather than discovered.
    #[test]
    fn test_find_all_bindings_also_rewrites_canonical_name() {
        use crate::database_bindings::parse_database_bindings;

        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut dep = make_dep_with_tokens("dep", "${db}", "<%db%>");
        dep.target.as_mut().unwrap().canonical_name = Some("<%db%>.rpt.ProductBasics".to_string());
        registry.create(&mut dep, None).unwrap();

        let bindings = parse_database_bindings("snow:\n  db: PHYSICAL\n").unwrap();
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&bindings.snow_token_map()),
                ..FindOptions::default()
            })
            .unwrap();
        let got = find_one(&units, "dep");
        assert_eq!(
            got.target.as_ref().unwrap().canonical_name.as_deref(),
            Some("PHYSICAL.rpt.ProductBasics"),
            "canonical_name is substituted too -- read unbound when it keys an identity"
        );

        // and unbound leaves it frozen, which is what such a caller must do
        let unbound = registry.find_all(FindOptions::default()).unwrap();
        assert_eq!(
            find_one(&unbound, "dep")
                .target
                .as_ref()
                .unwrap()
                .canonical_name
                .as_deref(),
            Some("<%db%>.rpt.ProductBasics")
        );
    }

    #[test]
    fn test_find_all_bindings_resolves_script_io_paths() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let io = vec![
            // binding write — source/target carry the per-side token spellings
            ScriptIoEntry {
                direction: Some(ScriptIoDirection::Write),
                ordinal: Some(0),
                path: Some(ScriptIoPath {
                    kind: Some(ScriptIoPathKind::Binding),
                    name: Some("err_file".to_string()),
                    source: Some("${err_file}".to_string()),
                    target: Some("<%err_file%>".to_string()),
                }),
                ..Default::default()
            },
            // plain literal read — no tokens, substitution is a no-op
            ScriptIoEntry {
                direction: Some(ScriptIoDirection::Read),
                ordinal: Some(1),
                path: Some(ScriptIoPath {
                    kind: Some(ScriptIoPathKind::Literal),
                    name: None,
                    source: Some("widget_daily.csv".to_string()),
                    target: Some("widget_daily.csv".to_string()),
                }),
                ..Default::default()
            },
            // templated literal — embedded token in each side's wrapper, e.g.
            // a target path like "<%IMPORT_DIR%>/widget_daily.csv"
            ScriptIoEntry {
                direction: Some(ScriptIoDirection::Read),
                ordinal: Some(2),
                path: Some(ScriptIoPath {
                    kind: Some(ScriptIoPathKind::Literal),
                    name: None,
                    source: Some("${IMPORT_DIR}/widget_daily.csv".to_string()),
                    target: Some("<%IMPORT_DIR%>/widget_daily.csv".to_string()),
                }),
                ..Default::default()
            },
        ];
        let mut script = CodeUnit {
            id: Some("s".to_string()),
            kind: Some(CodeUnitKind::Script),
            source: Some(SourceMetadata {
                platform: Some(SourcePlatform::Teradata),
                format: Some(SourceFormat::Bteq),
                ..Default::default()
            }),
            script_metadata: Some(ScriptMetadata { io }),
            ..Default::default()
        };
        registry.create(&mut script, None).unwrap();

        // bindings: None → source/target stay raw (regression guard).
        let none_io = find_one(&registry.find_all(FindOptions::default()).unwrap(), "s")
            .script_metadata
            .unwrap()
            .io;
        assert_eq!(
            none_io[0].path.as_ref().unwrap().source.as_deref(),
            Some("${err_file}")
        );
        assert_eq!(
            none_io[0].path.as_ref().unwrap().target.as_deref(),
            Some("<%err_file%>")
        );

        // Source side: a map keyed by the source-wrapper tokens resolves the
        // `source` slot in place and leaves `target` raw.
        let mut src = HashMap::new();
        src.insert("${err_file}".to_string(), "bteq_err.log".to_string());
        src.insert("${IMPORT_DIR}".to_string(), "/data/ecom".to_string());
        let io = find_one(
            &registry
                .find_all(FindOptions {
                    bindings: Some(&src),
                    ..FindOptions::default()
                })
                .unwrap(),
            "s",
        )
        .script_metadata
        .unwrap()
        .io;
        // identity (kind, name) untouched; source resolved, target raw
        assert_eq!(
            io[0].path.as_ref().unwrap().name.as_deref(),
            Some("err_file")
        );
        assert_eq!(
            io[0].path.as_ref().unwrap().source.as_deref(),
            Some("bteq_err.log")
        );
        assert_eq!(
            io[0].path.as_ref().unwrap().target.as_deref(),
            Some("<%err_file%>")
        );
        // plain literal: unchanged on both sides
        assert_eq!(
            io[1].path.as_ref().unwrap().source.as_deref(),
            Some("widget_daily.csv")
        );
        // templated literal: embedded ${IMPORT_DIR} substituted, suffix preserved
        assert_eq!(
            io[2].path.as_ref().unwrap().source.as_deref(),
            Some("/data/ecom/widget_daily.csv")
        );
        assert_eq!(
            io[2].path.as_ref().unwrap().target.as_deref(),
            Some("<%IMPORT_DIR%>/widget_daily.csv")
        );

        // Target side: a map keyed by the target-wrapper tokens resolves the
        // `target` slot in place (incl. an embedded "<%IMPORT_DIR%>/..." path)
        // and leaves `source` raw.
        let mut tgt = HashMap::new();
        tgt.insert("<%err_file%>".to_string(), "err.target.log".to_string());
        tgt.insert("<%IMPORT_DIR%>".to_string(), "/wh/in".to_string());
        let io = find_one(
            &registry
                .find_all(FindOptions {
                    bindings: Some(&tgt),
                    ..FindOptions::default()
                })
                .unwrap(),
            "s",
        )
        .script_metadata
        .unwrap()
        .io;
        assert_eq!(
            io[0].path.as_ref().unwrap().target.as_deref(),
            Some("err.target.log")
        );
        assert_eq!(
            io[0].path.as_ref().unwrap().source.as_deref(),
            Some("${err_file}")
        );
        // the user's case: "<%IMPORT_DIR%>/widget_daily.csv" resolves on target
        assert_eq!(
            io[2].path.as_ref().unwrap().target.as_deref(),
            Some("/wh/in/widget_daily.csv")
        );
    }

    #[test]
    fn test_find_all_bindings_lenient_on_unmatched_text() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut dep = make_dep_with_tokens("dep", "${KNOWN}", "<% UNKNOWN %>");
        registry.create(&mut dep, None).unwrap();

        let mut bindings = HashMap::new();
        bindings.insert("${KNOWN}".to_string(), "X".to_string());
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&bindings),
                ..FindOptions::default()
            })
            .unwrap();
        let dep = find_one(&units, "dep");
        assert_eq!(dep.source.as_ref().unwrap().database.as_deref(), Some("X"));
        assert_eq!(
            dep.target.as_ref().unwrap().database.as_deref(),
            Some("<% UNKNOWN %>")
        );
    }

    #[test]
    fn test_find_all_bindings_no_chain_reaction() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut dep = make_dep_with_tokens("dep", "${A}", "<% B %>");
        registry.create(&mut dep, None).unwrap();

        // Map ${A} → ${B} and ${B} → table1. With a single-pass scan, the
        // emitted ${B} must not be re-substituted into table1.
        let mut bindings = HashMap::new();
        bindings.insert("${A}".to_string(), "${B}".to_string());
        bindings.insert("${B}".to_string(), "table1".to_string());
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&bindings),
                ..FindOptions::default()
            })
            .unwrap();
        let dep = find_one(&units, "dep");
        assert_eq!(
            dep.source.as_ref().unwrap().database.as_deref(),
            Some("${B}")
        );
    }

    #[test]
    fn test_find_all_bindings_longest_match_wins() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut dep = make_dep_with_tokens("dep", "${FOOBAR}", "");
        registry.create(&mut dep, None).unwrap();

        let mut bindings = HashMap::new();
        bindings.insert("${FOO}".to_string(), "x".to_string());
        bindings.insert("${FOOBAR}".to_string(), "y".to_string());
        let units = registry
            .find_all(FindOptions {
                bindings: Some(&bindings),
                ..FindOptions::default()
            })
            .unwrap();
        let dep = find_one(&units, "dep");
        assert_eq!(dep.source.as_ref().unwrap().database.as_deref(), Some("y"));
    }

    #[test]
    fn test_find_all_bindings_does_not_touch_id_or_depends_on() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut script = make_script("script", vec![]);
        let mut dep = make_code_unit("dep", "T", CodeUnitObjectType::Table);
        set_dependencies(&mut script, &[("dep", None)]);
        registry.create(&mut script, None).unwrap();
        registry.create(&mut dep, None).unwrap();

        // Bindings whose key text matches the literal ids ("script", "dep").
        let mut bindings = HashMap::new();
        bindings.insert("script".to_string(), "REPLACED".to_string());
        bindings.insert("dep".to_string(), "REPLACED".to_string());

        let units = registry
            .find_all(FindOptions {
                bindings: Some(&bindings),
                ..FindOptions::default()
            })
            .unwrap();
        let script_unit = find_one(&units, "script");
        assert_eq!(script_unit.id.as_deref(), Some("script"));
        let edges = script_unit
            .dependencies
            .as_ref()
            .map(|d| d.depends_on.clone())
            .unwrap_or_default();
        assert_eq!(edges.len(), 1);
        assert_eq!(edges[0].id.as_deref(), Some("dep"));
    }

    #[test]
    fn test_script_bindings_round_trip_on_script_kind() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut script = make_script(
            "script",
            vec![
                ("APP_WORK_DIR", ScriptBindingKind::File),
                ("UTIL_DB_NAME", ScriptBindingKind::Database),
                ("batch_id", ScriptBindingKind::String),
            ],
        );
        registry.create(&mut script, None).unwrap();

        let units = registry.find_all(FindOptions::default()).unwrap();
        let loaded = find_one(&units, "script");
        let bindings = loaded.script_bindings.expect("scriptBindings missing");
        assert_eq!(bindings.len(), 3);
        assert!(bindings
            .iter()
            .any(|b| b.name.as_deref() == Some("APP_WORK_DIR")
                && matches!(b.kind, ScriptBindingKind::File)));
        assert!(bindings
            .iter()
            .any(|b| b.name.as_deref() == Some("UTIL_DB_NAME")
                && matches!(b.kind, ScriptBindingKind::Database)));
        assert!(bindings
            .iter()
            .any(|b| b.name.as_deref() == Some("batch_id")
                && matches!(b.kind, ScriptBindingKind::String)));
    }

    // ── validate_bindings ───────────────────────────────────────────────

    fn provided(pairs: &[(&str, &str)]) -> HashMap<String, String> {
        pairs
            .iter()
            .map(|(k, v)| ((*k).to_string(), (*v).to_string()))
            .collect()
    }

    #[test]
    fn test_validate_bindings_clean_when_provided_matches_declared() {
        let script = make_script(
            "s",
            vec![
                ("A", ScriptBindingKind::String),
                ("B", ScriptBindingKind::Database),
            ],
        );
        let diff = crate::validate_bindings(&script, &provided(&[("A", "x"), ("B", "PROD")]))
            .expect("validate_bindings should accept script kind");
        assert!(diff.missing.is_empty());
        assert!(diff.extra.is_empty());
        assert!(diff.empty.is_empty());
    }

    #[test]
    fn test_validate_bindings_reports_missing_names() {
        let script = make_script(
            "s",
            vec![
                ("A", ScriptBindingKind::String),
                ("B", ScriptBindingKind::String),
            ],
        );
        let diff = crate::validate_bindings(&script, &provided(&[("A", "x")])).unwrap();
        assert_eq!(diff.missing, vec!["B".to_string()]);
        assert!(diff.extra.is_empty());
        assert!(diff.empty.is_empty());
    }

    #[test]
    fn test_validate_bindings_reports_extra_names() {
        let script = make_script("s", vec![("A", ScriptBindingKind::String)]);
        let diff = crate::validate_bindings(&script, &provided(&[("A", "x"), ("Z", "y")])).unwrap();
        assert!(diff.missing.is_empty());
        assert_eq!(diff.extra, vec!["Z".to_string()]);
        assert!(diff.empty.is_empty());
    }

    #[test]
    fn test_validate_bindings_reports_empty_values_after_trim() {
        let script = make_script(
            "s",
            vec![
                ("A", ScriptBindingKind::String),
                ("B", ScriptBindingKind::String),
            ],
        );
        let diff =
            crate::validate_bindings(&script, &provided(&[("A", "  "), ("B", "x")])).unwrap();
        assert!(diff.missing.is_empty());
        assert!(diff.extra.is_empty());
        assert_eq!(diff.empty, vec!["A".to_string()]);
    }

    #[test]
    fn test_validate_bindings_sorts_output_deterministically() {
        let script = make_script(
            "s",
            vec![
                ("Z", ScriptBindingKind::String),
                ("A", ScriptBindingKind::String),
                ("M", ScriptBindingKind::String),
            ],
        );
        let diff = crate::validate_bindings(&script, &provided(&[])).unwrap();
        assert_eq!(
            diff.missing,
            vec!["A".to_string(), "M".to_string(), "Z".to_string()]
        );
    }

    #[test]
    fn test_validate_bindings_skips_bindings_with_no_name() {
        let mut script = make_script("s", vec![("A", ScriptBindingKind::String)]);
        // Append an unnamed binding (post-4b7a9d7 `name: Option<String>` is allowed).
        script
            .script_bindings
            .as_mut()
            .unwrap()
            .push(ScriptBinding {
                name: None,
                kind: ScriptBindingKind::String,
            });
        let diff = crate::validate_bindings(&script, &provided(&[("A", "x")])).unwrap();
        assert!(diff.missing.is_empty());
        assert!(diff.extra.is_empty());
        assert!(diff.empty.is_empty());
    }

    #[test]
    fn test_validate_bindings_errors_when_kind_is_not_script() {
        let unit = make_code_unit("u", "t", CodeUnitObjectType::Table);
        let err = crate::validate_bindings(&unit, &HashMap::new())
            .expect_err("non-script kind should error");
        let msg = format!("{err}");
        assert!(msg.contains("kind=script"), "got: {msg}");
    }

    #[test]
    fn test_validate_bindings_handles_script_with_no_bindings_field() {
        let mut script = make_script("s", vec![]);
        script.script_bindings = None;
        let diff = crate::validate_bindings(&script, &provided(&[("X", "y")])).unwrap();
        assert!(diff.missing.is_empty());
        assert_eq!(diff.extra, vec!["X".to_string()]);
        assert!(diff.empty.is_empty());
    }

    // ── parameterizedReference round-trip + bindings substitution ───────

    fn make_param_ref(id: &str, src_db: &str, tgt_db: &str, name: &str) -> CodeUnit {
        CodeUnit {
            id: Some(id.to_string()),
            kind: Some(CodeUnitKind::ParameterizedReference),
            source: Some(SourceMetadata {
                platform: Some(SourcePlatform::Teradata),
                database: Some(src_db.to_string()),
                name: Some(name.to_string()),
                ..Default::default()
            }),
            target: Some(TargetMetadata {
                database: Some(tgt_db.to_string()),
                name: Some(name.to_string()),
                ..Default::default()
            }),
            ..Default::default()
        }
    }

    #[test]
    fn test_parameterized_reference_round_trips_with_tokens() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut pref = make_param_ref(
            "pref",
            "${UTIL_DB_NAME}",
            "<% UTIL_DB_NAME %>",
            "error_codes",
        );
        registry.create(&mut pref, None).unwrap();

        let loaded = find_one(&registry.find_all(FindOptions::default()).unwrap(), "pref");
        assert_eq!(loaded.kind, Some(CodeUnitKind::ParameterizedReference));
        assert_eq!(
            loaded.source.as_ref().unwrap().database.as_deref(),
            Some("${UTIL_DB_NAME}")
        );
        assert_eq!(
            loaded.target.as_ref().unwrap().database.as_deref(),
            Some("<% UTIL_DB_NAME %>")
        );
    }

    #[test]
    fn test_parameterized_reference_substitution_via_find_options_bindings() {
        let dir = temp_dir();
        let registry = init_bare(dir.path());

        let mut pref = make_param_ref(
            "pref",
            "${UTIL_DB_NAME}",
            "<% UTIL_DB_NAME %>",
            "error_codes",
        );
        registry.create(&mut pref, None).unwrap();

        let mut both = HashMap::new();
        both.insert("${UTIL_DB_NAME}".to_string(), "PROD_UTIL".to_string());
        both.insert("<% UTIL_DB_NAME %>".to_string(), "SC_TEST_UTIL".to_string());

        let units = registry
            .find_all(FindOptions {
                bindings: Some(&both),
                ..FindOptions::default()
            })
            .unwrap();
        let loaded = find_one(&units, "pref");
        assert_eq!(
            loaded.source.as_ref().unwrap().database.as_deref(),
            Some("PROD_UTIL")
        );
        assert_eq!(
            loaded.target.as_ref().unwrap().database.as_deref(),
            Some("SC_TEST_UTIL")
        );
    }

    #[test]
    fn test_informatica_workflow_round_trip() {
        use crate::generated::types::{
            CodeStatus, ConversionStatus, FileEntry, Files, Kind, OperationStatus, SourceMetadata,
            SourcePlatform, TargetMetadata,
        };

        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        // Create workflow code unit
        let mut workflow_unit = CodeUnit {
            id: Some("test-workflow-id".to_string()),
            kind: Some(Kind::Etl),
            is_missing: false,
            source: Some(SourceMetadata {
                object_type: Some(CodeUnitObjectType::Workflow),
                name: Some("wf_test_workflow".to_string()),
                platform: Some(SourcePlatform::Informatica),
                ..Default::default()
            }),
            target: Some(TargetMetadata {
                object_type: Some(CodeUnitObjectType::Workflow),
                ..Default::default()
            }),
            files: Some(Files {
                source: Some(FileEntry {
                    path: Some("source/test/wf_test.xml".to_string()),
                    ..Default::default()
                }),
                converted: Some(FileEntry {
                    path: Some("converted/test/wf_test/".to_string()),
                    ..Default::default()
                }),
                artifacts: Some(crate::generated::types::ArtifactsEntry {
                    path: Some("artifacts/test/wf_test".to_string()),
                }),
                ..Default::default()
            }),
            code_status: Some(CodeStatus {
                conversion: Some(ConversionStatus {
                    status: Some(OperationStatus::Completed),
                    converter_version: Some("1.0.0".to_string()),
                    updated_at: Some(
                        chrono::DateTime::parse_from_rfc3339("2026-06-15T10:00:00Z")
                            .unwrap()
                            .with_timezone(&chrono::Utc),
                    ),
                    ..Default::default()
                }),
                ..Default::default()
            }),
            ..Default::default()
        };

        // Save to registry
        let save_result = registry.create(&mut workflow_unit, None);
        assert!(save_result.is_ok(), "Failed to save workflow code unit");

        // Load back from registry
        let load_result = registry.get_by_id("test-workflow-id", None);
        assert!(load_result.is_ok(), "Failed to load workflow code unit");

        let loaded_unit = load_result.unwrap();

        // Verify objectType preserved correctly
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().object_type,
            Some(CodeUnitObjectType::Workflow)
        );
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().name.as_deref(),
            Some("wf_test_workflow")
        );
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().platform,
            Some(SourcePlatform::Informatica)
        );
    }

    #[test]
    fn test_informatica_mapping_round_trip() {
        use crate::generated::types::{
            CodeStatus, ConversionStatus, FileEntry, Files, Kind, OperationStatus, SourceMetadata,
            SourcePlatform, TargetMetadata,
        };

        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        // Create mapping code unit
        let mut mapping_unit = CodeUnit {
            id: Some("test-mapping-id".to_string()),
            kind: Some(Kind::Etl),
            is_missing: false,
            source: Some(SourceMetadata {
                object_type: Some(CodeUnitObjectType::Mapping),
                name: Some("m_test_mapping".to_string()),
                platform: Some(SourcePlatform::Informatica),
                ..Default::default()
            }),
            target: Some(TargetMetadata {
                object_type: Some(CodeUnitObjectType::Mapping),
                ..Default::default()
            }),
            files: Some(Files {
                source: Some(FileEntry {
                    path: Some("source/test/m_test.xml".to_string()),
                    ..Default::default()
                }),
                converted: Some(FileEntry {
                    path: Some("converted/test/m_test/".to_string()),
                    ..Default::default()
                }),
                artifacts: Some(crate::generated::types::ArtifactsEntry {
                    path: Some("artifacts/test/m_test".to_string()),
                }),
                ..Default::default()
            }),
            code_status: Some(CodeStatus {
                conversion: Some(ConversionStatus {
                    status: Some(OperationStatus::Completed),
                    converter_version: Some("1.0.0".to_string()),
                    updated_at: Some(
                        chrono::DateTime::parse_from_rfc3339("2026-06-15T10:00:00Z")
                            .unwrap()
                            .with_timezone(&chrono::Utc),
                    ),
                    ..Default::default()
                }),
                ..Default::default()
            }),
            ..Default::default()
        };

        // Save to registry
        let save_result = registry.create(&mut mapping_unit, None);
        assert!(save_result.is_ok(), "Failed to save mapping code unit");

        // Load back from registry
        let load_result = registry.get_by_id("test-mapping-id", None);
        assert!(load_result.is_ok(), "Failed to load mapping code unit");

        let loaded_unit = load_result.unwrap();

        // Verify objectType preserved correctly
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().object_type,
            Some(CodeUnitObjectType::Mapping)
        );
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().name.as_deref(),
            Some("m_test_mapping")
        );
        assert_eq!(
            loaded_unit.source.as_ref().unwrap().platform,
            Some(SourcePlatform::Informatica)
        );
    }
}

#[cfg(test)]
mod custom_kind_e2e_tests {
    //! End-to-end coverage for `kind=custom` units: round-trip through
    //! `CodeUnitRegistry::create`/`find_all`, canonical name computation by
    //! the persistence hook, dependency relationships back to built-in kinds,
    //! validation rejection of incomplete units, and the field-gate exemption
    //! that lets a custom unit carry fields reserved for other kinds.

    use super::*;
    use crate::generated::types::{FileEntry, Files, Planning};

    fn power_bi_report(id: &str) -> CodeUnit {
        CodeUnit {
            id: Some(id.to_string()),
            kind: Some(CodeUnitKind::Custom),
            source: Some(SourceMetadata {
                custom_kind: Some("powerBiReport".into()),
                name: Some("SalesDashboard".into()),
                ..Default::default()
            }),
            ..Default::default()
        }
    }

    #[test]
    fn custom_unit_round_trips_with_canonical_name() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = power_bi_report("11111111-2222-3333-4444-555555555555");
        registry.create(&mut unit, None).unwrap();

        let loaded = registry
            .find_all(FindOptions::default())
            .unwrap()
            .into_iter()
            .next()
            .expect("one unit");
        assert_eq!(loaded.kind, Some(CodeUnitKind::Custom));
        let s = loaded.source.as_ref().expect("source");
        assert_eq!(s.custom_kind.as_deref(), Some("powerBiReport"));
        assert_eq!(
            s.canonical_name.as_deref(),
            Some("powerBiReport:SalesDashboard"),
            "source.canonicalName should be computed by the persistence hook"
        );
    }

    #[test]
    fn custom_unit_validates_clean() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = power_bi_report("11111111-2222-3333-4444-555555555556");
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "power BI report with name should validate clean, issues: {:?}",
            report.issues
        );
    }

    #[test]
    fn custom_can_depend_on_database_object() {
        // A Power BI report reads a Customers table. Both are valid units;
        // dependency reads are unaffected by kind.
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut table = make_code_unit(
            "aaaaaaaa-0000-0000-0000-000000000001",
            "Customers",
            CodeUnitObjectType::Table,
        );
        registry.create(&mut table, None).unwrap();

        let mut report_unit = power_bi_report("bbbbbbbb-0000-0000-0000-000000000001");
        report_unit.dependencies = Some(Dependencies {
            depends_on: vec![Dependency {
                id: Some(table.id.clone().unwrap()),
                relation_types: vec!["READ".into()],
                ..Default::default()
            }],
            ..Default::default()
        });
        registry.create(&mut report_unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "custom unit depending on a databaseObject should validate clean, issues: {:?}",
            report.issues
        );
    }

    #[test]
    fn custom_unit_without_name_or_path_fails_validation() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = CodeUnit {
            id: Some("cccccccc-0000-0000-0000-000000000001".into()),
            kind: Some(CodeUnitKind::Custom),
            source: Some(SourceMetadata {
                custom_kind: Some("powerBiReport".into()),
                ..Default::default()
            }),
            ..Default::default()
        };
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(!report.is_valid, "expected validation to fail");
        assert!(
            report
                .issues
                .iter()
                .any(|i| i.kind == ValidationIssueKind::PerKindStructure
                    && i.message.contains("customKind")),
            "expected PerKindStructure issue mentioning customKind, got: {:?}",
            report.issues
        );
    }

    #[test]
    fn custom_unit_with_path_only_validates_clean() {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = CodeUnit {
            id: Some("dddddddd-0000-0000-0000-000000000001".into()),
            kind: Some(CodeUnitKind::Custom),
            source: Some(SourceMetadata {
                custom_kind: Some("ssasCube".into()),
                ..Default::default()
            }),
            files: Some(Files {
                source: Some(FileEntry {
                    path: Some("source/cubes/Sales.bim".into()),
                    checksum: None,
                }),
                ..Default::default()
            }),
            ..Default::default()
        };
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "ssasCube path-only should validate clean, issues: {:?}",
            report.issues
        );
    }

    #[test]
    fn custom_unit_carries_files_and_status_reserved_for_other_kinds() {
        // `files`, `codeStatus` and `planning` are all gated away from
        // non-built-in kinds by `x-allowed-when`; a custom unit is exempt, so
        // a dbt Cloud job can track its own file, conversion and wave state.
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();

        let mut unit = CodeUnit {
            id: Some("eeeeeeee-0000-0000-0000-000000000001".into()),
            kind: Some(CodeUnitKind::Custom),
            source: Some(SourceMetadata {
                custom_kind: Some("dbtCloudJob".into()),
                name: Some("nightly_refresh".into()),
                ..Default::default()
            }),
            files: Some(Files {
                source: Some(FileEntry {
                    path: Some("source/dbt/nightly.yml".into()),
                    checksum: None,
                }),
                ..Default::default()
            }),
            planning: Some(Planning {
                wave: Some(2),
                ..Default::default()
            }),
            ..Default::default()
        };
        registry.create(&mut unit, None).unwrap();

        let report = registry.validate(ChecksumMode::NONE).unwrap();
        assert!(
            report.is_valid,
            "custom unit carrying files + planning should validate clean, issues: {:?}",
            report.issues
        );
    }
}
