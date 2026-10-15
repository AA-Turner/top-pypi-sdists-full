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
        storage: storage::Storage::open(&registry_dir).unwrap(),
        root,
        hooks: vec![],
        in_hook: Default::default(),
    }
}

// ── Raw file access ──────────────────────────────────────────────────────
//
// These bypass hooks, migration and the typed write path, so tests can seed
// arbitrary (even corrupt) documents and inspect exactly what was persisted.
// Writes go in the way git does (temp file + rename), so the index sees them
// as external changes.

/// Store raw `text` under `id`. It need not be valid JSON, and its embedded
/// `id` need not match the key.
fn write_raw(registry: &CodeUnitRegistry, id: &str, text: &str) {
    registry.storage.put_raw_text(id, text).unwrap();
}

/// Store `value` (pretty-printed, as the library writes it) under `id`.
fn write_raw_value(registry: &CodeUnitRegistry, id: &str, value: &serde_json::Value) {
    write_raw(registry, id, &serde_json::to_string_pretty(value).unwrap());
}

/// Text of the file for `id`; panics if absent.
fn read_raw_text(registry: &CodeUnitRegistry, id: &str) -> String {
    let path = registry.storage.files().path_for(id);
    fs::read_to_string(&path).unwrap_or_else(|e| panic!("{}: {e}", path.display()))
}

/// The file for `id`, parsed as untyped JSON (no migration).
fn read_raw_value(registry: &CodeUnitRegistry, id: &str) -> serde_json::Value {
    serde_json::from_str(&read_raw_text(registry, id)).unwrap()
}

/// Whether a file is stored for `id`.
fn stored(registry: &CodeUnitRegistry, id: &str) -> bool {
    registry.storage.files().path_for(id).exists()
}

// ── Index observability ──────────────────────────────────────────────────

/// Whether this process runs with the SQLite index (`SCAI_REGISTRY_INDEX`
/// unset or not `off`/`0`/`false`). Read-only: tests never set env vars.
fn index_enabled() -> bool {
    !matches!(
        std::env::var(storage::INDEX_ENV_VAR)
            .map(|v| v.trim().to_ascii_lowercase())
            .as_deref(),
        Ok("off" | "0" | "false")
    )
}

/// The registry's index directory (`registry/.index/`).
fn index_dir(registry: &CodeUnitRegistry) -> std::path::PathBuf {
    registry.storage.files().dir().join(storage::INDEX_DIR)
}

/// Run `f` and, when the index is enabled, assert the index served at least
/// one of its reads — so an index-vs-files comparison can't pass vacuously.
fn index_served<T>(registry: &CodeUnitRegistry, label: &str, f: impl FnOnce() -> T) -> T {
    let before = registry.storage.index_reads();
    let result = f();
    if index_enabled() {
        assert!(
            registry.storage.index_reads() > before,
            "{label}: expected the index to serve this read"
        );
    }
    result
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
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    let registry_dir = dir.path().join("registry");
    assert!(registry_dir.exists());
    assert!(registry_dir.join(".locks").exists());

    let gitignore = fs::read_to_string(registry_dir.join(".gitignore")).unwrap();
    assert!(gitignore.contains(".locks/"));

    // The index is created on first use and ignores itself.
    registry.find_all(FindOptions::default()).unwrap();
    if index_enabled() {
        let index_dir = registry_dir.join(storage::INDEX_DIR);
        assert!(index_dir.is_dir(), "{} missing", index_dir.display());
        let ignore = fs::read_to_string(index_dir.join(".gitignore")).unwrap();
        assert!(ignore.lines().any(|line| line.trim() == "*"), "{ignore:?}");
        // The project's own .gitignore is left alone.
        let gitignore_after = fs::read_to_string(registry_dir.join(".gitignore")).unwrap();
        assert_eq!(gitignore_after, gitignore);
    }
    drop(registry);
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
    assert_eq!(registry.storage.files().path_for(id), expected);
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

    assert!(stored(&registry, "id_del"));

    registry.delete("id_del").unwrap();
    assert!(!stored(&registry, "id_del"));
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

    // Close storage first: Windows refuses to delete an open SQLite database.
    drop(registry);
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

    let roundtripped = read_raw_value(&registry, &id);

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

    let roundtripped = read_raw_value(&registry, &id);

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
    write_raw(&registry, legacy_id, json);

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

/// Stored document under `id`, parsed the way the registry reads it
/// (schema migration + path normalization) but without going through the
/// query layer.
fn read_unit(registry: &CodeUnitRegistry, id: &str) -> CodeUnit {
    CodeUnitRegistry::parse_unit(&read_raw_text(registry, id)).unwrap()
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

    write_raw(&registry, "corrupt", "NOT VALID JSON");

    registry
        .create(&mut make_unit_with_deps("new_unit", &[]), None)
        .unwrap();

    assert!(stored(&registry, "new_unit"));
}

#[test]
fn create_batch_with_corrupt_sibling_succeeds_without_hooks() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_raw(&registry, "corrupt", "NOT VALID JSON");

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
    // Contract: the persist path's read-modify-write is the defense against
    // *uncooperating* writers (editors, scripts, git, IDEs, or a second
    // storage handle) modifying a stored document between
    // `refresh_and_sync`'s load and its per-unit write. The advisory
    // `acquire_lock` only coordinates cooperating registry instances; it
    // does not stop external writes.
    //
    // Any optimization that caches raw JSON at load time and reuses it at
    // write time MUST NOT regress this property. Forward-compat fields
    // added to the file in the load -> write window must survive the
    // refresh.
    use crate::migration::CURRENT_SCHEMA_VERSION;
    use crate::registry::test_hooks::{clear_after_load_hook, set_after_load_hook};

    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    // Seed a unit directly in storage with no derived state — bypasses the
    // auto-refresh write-hook so refresh_dependencies will mark it dirty
    // and enter the per-unit write loop.
    let initial = serde_json::json!({
        SCHEMA_VERSION_FIELD: CURRENT_SCHEMA_VERSION,
        "id": "a",
    });
    write_raw_value(&registry, "a", &initial);

    // Hook fires after load + graph refresh, before the first write.
    // Simulates an uncooperating external writer — a separately opened
    // storage handle, as another process would have — that adds a
    // forward-compat field unknown to the typed `CodeUnit`.
    let root = dir.path().to_path_buf();
    set_after_load_hook(move || {
        let external = CodeUnitRegistry::open(&root).unwrap();
        let mut current = read_raw_value(&external, "a");
        current["futureField"] = serde_json::json!("external-value");
        write_raw_value(&external, "a", &current);
    });

    let result = registry.refresh_dependencies();
    clear_after_load_hook();
    result.unwrap();

    let final_value = read_raw_value(&registry, "a");
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
        !stored(&registry, "hf1"),
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
        stored(&registry, "cd1"),
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
    write_raw(&registry, "bad", "not json{{{");
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
    write_raw_value(&registry, "future", &doc);

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
    write_raw_value(&registry, "broken", &doc);

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

    write_raw(&registry, "garbage", "not json{{{");

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
    write_raw_value(&registry, "bad-1", &bad_doc);

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
    write_raw_value(&registry, "future", &doc);

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
    write_raw_value(&registry, "bad-version", &doc);

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
    write_raw_value(&registry, "bad-type", &doc);

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
    write_raw_value(&registry, "etl-with-root-issues", &doc);

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
    write_raw_value(&registry, "bad-platform-format", &doc);

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
    write_raw_value(&registry, "correct-name", &unit);
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
    write_raw_value(&registry, "dup", &unit_a);
    write_raw_value(&registry, "dup2", &unit_b);
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
    write_raw(&registry, "bad1", "not-json");
    write_raw(&registry, "bad2", "also-bad");
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
    write_raw_value(&registry, "no-id-unit", &unit_without_id);
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
    write_raw_value(&registry, "pn2", &raw_json);

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
    write_raw_value(&registry, "pn4", &raw_json);

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

/// Store a minimal JSON document at the given schema version.
fn write_test_doc(registry: &CodeUnitRegistry, id: &str, version: i64) {
    let doc = serde_json::json!({
        (SCHEMA_VERSION_FIELD): version,
        "id": id,
        "kind": "databaseObject",
        "source": {"objectType": "table", "name": id},
        "target": {"objectType": "table", "name": id}
    });
    write_raw_value(registry, id, &doc);
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

    let doc1 = read_raw_value(&registry, "ra-1");
    assert_eq!(doc1[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(doc1["peerCount"], 2);

    let doc2 = read_raw_value(&registry, "ra-2");
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

    let target = read_raw_value(&registry, "target-1");
    assert_eq!(target[SCHEMA_VERSION_FIELD], 2);
    assert_eq!(
        target["peerCount"], 2,
        "should see total count including non-target"
    );

    let non_target = read_raw_value(&registry, "already-v2");
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

    let doc1 = read_raw_value(&registry, "aon-1");
    assert_eq!(
        doc1[SCHEMA_VERSION_FIELD], 1,
        "on failure, documents must not be modified in storage"
    );
    let doc2 = read_raw_value(&registry, "aon-2");
    assert_eq!(doc2[SCHEMA_VERSION_FIELD], 1);
}

#[test]
fn test_migrate_schema_all_registry_aware_failure_includes_prior_failures() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    write_test_doc(&registry, "prior-good", 1);
    // Invalid JSON triggers a load-time failure recorded in BatchResult
    // *before* the registry-aware step runs.
    write_raw(&registry, "prior-bad", "not valid json{{{");

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

    let doc1 = read_raw_value(&registry, "mix-1");
    assert_eq!(doc1[SCHEMA_VERSION_FIELD], 3);
    assert_eq!(doc1["addedInV2"], "hello");
    assert!(
        doc1.get("readFromPeer").is_some(),
        "registry-aware step should have run"
    );

    let doc2 = read_raw_value(&registry, "mix-2");
    assert_eq!(doc2[SCHEMA_VERSION_FIELD], 3);
    assert_eq!(doc2["addedInV2"], "hello");
}

#[test]
fn test_migrate_schema_all_records_each_failed_document_once() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());

    let future_doc = serde_json::json!({(SCHEMA_VERSION_FIELD): 999, "id": "future-dedup"});
    write_raw_value(&registry, "future-dedup", &future_doc);
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
        let doc = read_raw_value(&registry, id);
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

    let doc1 = read_raw_value(&registry, "restore-1");
    assert!(
        doc1.get("shouldNotPersist").is_none(),
        "stored documents must not reflect in-memory mutations from a failed step"
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

    let doc = read_raw_value(&registry, "pf-1");
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

    let mut raw = read_raw_value(&registry, "preserve-001");
    raw["futureField"] = serde_json::json!("preserved_value");
    raw["futureObject"] = serde_json::json!({"nested": true, "count": 42});
    raw["source"]["futureSourceField"] = serde_json::json!("nested_preserved");
    write_raw_value(&registry, "preserve-001", &raw);

    registry
        .update(
            "preserve-001",
            &[("source.name", serde_json::json!("UpdatedName"))],
            None,
        )
        .unwrap();

    let on_disk = read_raw_value(&registry, "preserve-001");
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

    let mut raw = read_raw_value(&registry, "preserve-002");
    raw["futureField"] = serde_json::json!("keep_me");
    write_raw_value(&registry, "preserve-002", &raw);

    let mut patch = CodeUnit {
        id: Some("preserve-002".to_string()),
        source: Some(SourceMetadata {
            name: Some("MergedName".to_string()),
            ..Default::default()
        }),
        ..Default::default()
    };
    registry.upsert(&mut patch, None).unwrap();

    let on_disk = read_raw_value(&registry, "preserve-002");
    assert_eq!(on_disk["futureField"], "keep_me");
    assert_eq!(on_disk["source"]["name"], "MergedName");
}

#[test]
fn test_unknown_fields_preserved_through_dependency_refresh() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut dep = make_code_unit("dep-target", "DepTarget", CodeUnitObjectType::Table);
    registry.create(&mut dep, None).unwrap();

    let mut raw = read_raw_value(&registry, "dep-target");
    raw["futureDepField"] = serde_json::json!("dep_preserved");
    write_raw_value(&registry, "dep-target", &raw);

    let mut dependent = make_code_unit("dep-source", "DepSource", CodeUnitObjectType::View);
    set_dependency_ids(&mut dependent, &["dep-target"]);
    registry.create(&mut dependent, None).unwrap();

    let on_disk = read_raw_value(&registry, "dep-target");
    assert_eq!(on_disk["futureDepField"], "dep_preserved");
}

#[test]
fn test_unknown_fields_preserved_through_hooks() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();

    let mut cu = make_code_unit("preserve-hooks", "HookTest", CodeUnitObjectType::Table);
    registry.create(&mut cu, None).unwrap();

    let mut raw = read_raw_value(&registry, "preserve-hooks");
    raw["futureHookField"] = serde_json::json!({"nested": "value"});
    raw["codeStatus"]["futurePhase"] = serde_json::json!({"status": "testing"});
    write_raw_value(&registry, "preserve-hooks", &raw);

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

    let on_disk = read_raw_value(&registry, "preserve-hooks");
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

    let mut raw = read_raw_value(&registry, "preserve-migrate");
    raw["futureFieldFromNewerSchema"] = serde_json::json!("should_survive_migration");
    raw["source"]["futureNested"] = serde_json::json!(42);
    write_raw_value(&registry, "preserve-migrate", &raw);

    // migrate_schema_all is a no-op at schema v1 (no migrations exist yet),
    // so also exercise the write path that migrate_schema_file uses when a
    // real migration runs: read → mutate → validate → storage put of the
    // migrated value as-is (see `write_changed_schema_docs`).
    let result = registry.migrate_schema_all().unwrap();
    assert!(result.failed.is_empty());

    let mut migrated = read_raw_value(&registry, "preserve-migrate");
    migrated["source"]["name"] = serde_json::json!("MigratedName");
    let _validated: CodeUnit = serde_json::from_value(migrated.clone()).unwrap();
    let lock = registry.acquire_lock().unwrap();
    let outcomes = registry.storage.write_batch(
        &lock,
        &[storage::StorageWrite::Put {
            id: "preserve-migrate",
            value: &migrated,
        }],
        false,
    );
    assert_eq!(outcomes.len(), 1);
    outcomes.into_iter().for_each(|outcome| outcome.unwrap());

    let on_disk = read_raw_value(&registry, "preserve-migrate");
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

    let on_disk = read_raw_value(&registry, &id);

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

/// `(part_id, target_format, [(dep_id, relation_types)])` for [`make_etl_code_unit`].
type EtlPartConfig<'a> = (&'a str, &'a str, Vec<(&'a str, &'a [&'a str])>);

fn make_etl_code_unit(id: &str, parts_config: Vec<EtlPartConfig<'_>>) -> CodeUnit {
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

    /// A `database-bindings.yml` drives `find_all` end to end.
    ///
    /// This is the whole point of `database_bindings`: the caller supplies the file
    /// SnowConvert generated, not a hand-wrapped token map, and the read returns
    /// physical names.
    ///
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

// ── Filter pushdown differential tests ───────────────────────────────────
//
// Pushdown may only change *how many* documents are loaded, never the
// result: every query below must return exactly what a full load returns.

/// Regular documents spanning every indexed field's value shapes: absent
/// fields, numeric-looking strings, `inScope` absent (defaults to true).
fn seed_pushdown_registry(registry: &CodeUnitRegistry) {
    let types = [
        CodeUnitObjectType::Table,
        CodeUnitObjectType::View,
        CodeUnitObjectType::Procedure,
    ];
    let databases = [
        Some("DB"),
        Some("01"),
        Some("1"),
        Some("true"),
        Some(""),
        None,
    ];
    let schemas = [Some("dbo"), Some("SALES"), Some("1e3"), None];
    let waves = [None, Some(0), Some(1), Some(2), Some(3), Some(10), Some(-1)];
    let mut batch = Vec::new();
    for i in 0..120usize {
        let id = if i % 40 == 7 {
            i.to_string()
        } else {
            format!("unit-{i:03}")
        };
        let mut unit = make_code_unit(&id, &format!("OBJ_{i}"), types[i % types.len()]);
        let source = unit.source.as_mut().unwrap();
        source.database = databases[i % databases.len()].map(str::to_string);
        source.schema = schemas[(i / 2) % schemas.len()].map(str::to_string);
        let target = unit.target.as_mut().unwrap();
        target.object_type = Some(types[(i + 1) % types.len()]);
        target.database = databases[(i / 3) % databases.len()].map(str::to_string);
        target.schema = schemas[(i / 5) % schemas.len()].map(str::to_string);
        unit.in_scope = i % 3 != 0;
        if let Some(wave) = waves[i % waves.len()] {
            unit.planning.get_or_insert_with(Default::default).wave = Some(wave);
        }
        batch.push(unit);
    }
    let result = registry.create_batch(&mut batch, None).unwrap();
    assert!(result.failed.is_empty(), "{:?}", result.failed);
    // Stored without `inScope` at all: serde materializes `true` on read.
    let mut raw = read_raw_value(registry, "unit-001");
    raw.as_object_mut().unwrap().remove("inScope");
    write_raw_value(registry, "unit-001", &raw);
}

const PUSHDOWN_FILTERS: &[&str] = &[
    "id = 'unit-005'",
    "id IN ('unit-001', 'unit-002', 'unit-119', 'nope')",
    "id = '7'",
    "id = 7",
    "id IN ('7', 'unit-047')",
    "source.objectType = 'procedure'",
    "target.objectType IN ('table', 'view')",
    "source.database = 'DB'",
    "source.database = '1'",
    "source.database = 1",
    "source.database IN ('01', '1')",
    "source.database = 'true'",
    "source.database = ''",
    "source.database IS NULL",
    "source.database IS NOT NULL",
    "source.database = 'DB' AND source.schema = 'dbo'",
    "target.database = 'DB' AND target.schema IN ('SALES', '1e3')",
    "source.schema = '1e3'",
    "source.schema = 1000",
    "planning.wave = 2",
    "planning.wave = '2'",
    "planning.wave = 2.0",
    "planning.wave IN (1, 3)",
    "planning.wave IN ('1', '3.0')",
    "planning.wave > 1",
    "planning.wave >= 0 AND planning.wave < 3",
    "planning.wave BETWEEN 1 AND 3",
    "planning.wave IS NULL",
    "planning.wave <> 2",
    "inScope",
    "inScope = true",
    "inScope = false",
    "inScope = 1",
    "inScope = 'true'",
    "NOT inScope",
    "inScope IS TRUE",
    "inScope IS FALSE",
    "inScope AND planning.wave BETWEEN 1 AND 3",
    "inScope = false OR planning.wave = 10",
    "(id = 'unit-003') OR (source.schema = 'dbo' AND source.name = 'OBJ_8')",
    "source.objectType = 'table' AND source.name LIKE 'OBJ_1%'",
    "source.name LIKE 'OBJ_1%'",
    "NOT (source.objectType = 'table')",
    "source.objectType <> 'table'",
    "source.objectType NOT IN ('table')",
    "kind = 'databaseObject' AND source.objectType = 'view'",
];

fn sorted_values(units: Vec<CodeUnit>) -> Vec<serde_json::Value> {
    let mut values: Vec<serde_json::Value> = units
        .iter()
        .map(|u| serde_json::to_value(u).unwrap())
        .collect();
    // By id, then by content: projections without `id` still compare as
    // multisets, independent of the order documents were loaded in.
    values.sort_by_cached_key(|v| (v["id"].as_str().map(str::to_string), v.to_string()));
    values
}

#[test]
fn pushdown_find_all_matches_full_load() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_pushdown_registry(&registry);

    let fields: &[&str] = &["id", "source", "planning", "inScope"];
    for filter in PUSHDOWN_FILTERS {
        for projection in [None, Some(fields)] {
            let options = FindOptions {
                filter: Some(filter),
                fields: projection,
                ..FindOptions::default()
            };
            let label = format!("filter {filter:?}, fields {projection:?}");
            let pushed = sorted_values(
                index_served(&registry, &label, || registry.find_all(options)).unwrap(),
            );
            let full =
                sorted_values(test_hooks::without_index(|| registry.find_all(options)).unwrap());
            assert_eq!(pushed, full, "{label}");
        }
    }
}

#[test]
fn pushdown_find_by_object_matches_full_load() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_pushdown_registry(&registry);

    let partials = [
        serde_json::json!({ "id": "unit-010" }),
        serde_json::json!({ "source": { "objectType": "view" } }),
        serde_json::json!({ "source": { "database": "1", "schema": "dbo" } }),
        serde_json::json!({ "source": { "database": 1 } }),
        serde_json::json!({ "inScope": true }),
        serde_json::json!({ "inScope": false, "planning": { "wave": 3 } }),
        serde_json::json!({ "planning": { "wave": 2.0 } }),
        serde_json::json!({ "planning": { "wave": null } }),
        serde_json::json!({ "target": { "objectType": "table", "name": "OBJ_4" } }),
    ];
    for partial in &partials {
        let label = format!("partial {partial}");
        let pushed = sorted_values(
            index_served(&registry, &label, || registry.find_by_object(partial, None)).unwrap(),
        );
        let full = sorted_values(
            test_hooks::without_index(|| registry.find_by_object(partial, None)).unwrap(),
        );
        assert_eq!(pushed, full, "{label}");
    }
}

#[test]
fn pushdown_update_where_and_sql_changes_match_full_load() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_pushdown_registry(&registry);

    for filter in ["inScope AND planning.wave = 2", "source.database = '01'"] {
        let pushed = index_served(&registry, filter, || {
            registry.find_sql_file_changes(ChecksumMode::default(), Some(filter))
        })
        .unwrap();
        let full = test_hooks::without_index(|| {
            registry.find_sql_file_changes(ChecksumMode::default(), Some(filter))
        })
        .unwrap();
        assert_eq!(
            serde_json::to_value(&pushed).unwrap(),
            serde_json::to_value(&full).unwrap(),
            "filter {filter:?}"
        );
    }

    let filter = "source.objectType = 'view' AND inScope";
    let expected: Vec<String> = test_hooks::without_index(|| {
        registry.find_all(FindOptions {
            filter: Some(filter),
            ..FindOptions::default()
        })
    })
    .unwrap()
    .into_iter()
    .filter_map(|u| u.id)
    .collect();
    let result = index_served(&registry, filter, || {
        registry.update_where(
            filter,
            &[("source.name", serde_json::json!("RENAMED"))],
            None,
        )
    })
    .unwrap();
    assert!(result.failed.is_empty(), "{:?}", result.failed);
    let mut updated = result.succeeded.clone();
    updated.retain(|id| expected.contains(id));
    updated.sort();
    let mut expected = expected;
    expected.sort();
    assert_eq!(updated, expected);
}

/// Irregular documents are always candidates, so a corrupt document still
/// fails a selective filtered read exactly like a full load does.
#[test]
fn pushdown_keeps_strict_loading_for_irregular_documents() {
    let corruptions: [(&str, &str); 4] = [
        ("corrupt", "NOT VALID JSON"),
        (
            "wrong-type",
            r#"{"id":"wrong-type","source":{"database":5}}"#,
        ),
        ("future", r#"{"id":"future","schemaVersion":999}"#),
        ("mismatch", r#"{"id":"someone-else"}"#),
    ];
    for (key, text) in corruptions {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();
        seed_pushdown_registry(&registry);
        write_raw(&registry, key, text);

        for filter in [
            "id = 'unit-005'",
            "source.database = 'DB'",
            "planning.wave = 2",
        ] {
            let options = FindOptions {
                filter: Some(filter),
                ..FindOptions::default()
            };
            let label = format!("{key}: filter {filter:?}");
            let pushed = index_served(&registry, &label, || registry.find_all(options))
                .map(|_| ())
                .map_err(|e| e.error_code());
            let full = test_hooks::without_index(|| registry.find_all(options))
                .map(|_| ())
                .map_err(|e| e.error_code());
            assert!(full.is_err(), "{key}: full load should reject the document");
            assert_eq!(pushed, full, "{label}");
        }
    }
}

#[test]
fn pushdown_include_dependencies_matches_full_load() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    // a → b → c → d, e → (dangling), x ↔ y (cycle), p → {a, x}, q (isolated).
    let edges: &[(&str, &[&str])] = &[
        ("a", &["b"]),
        ("b", &["c"]),
        ("c", &["d"]),
        ("d", &[]),
        ("e", &["does-not-exist"]),
        ("x", &["y"]),
        ("y", &["x"]),
        ("p", &["a", "x"]),
        ("q", &[]),
    ];
    let mut batch: Vec<CodeUnit> = edges
        .iter()
        .map(|(id, deps)| {
            let mut unit = make_code_unit(id, &id.to_uppercase(), CodeUnitObjectType::View);
            set_dependency_ids(&mut unit, deps);
            unit
        })
        .collect();
    let result = registry.create_batch(&mut batch, None).unwrap();
    assert!(result.failed.is_empty(), "{:?}", result.failed);

    let filters = [
        "id = 'a'",
        "id = 'c'",
        "id IN ('e', 'x')",
        "id = 'p'",
        "id = 'q'",
        "id = 'nope'",
        "source.name = 'B'",
        "source.name LIKE 'P%'",
    ];
    for filter in filters {
        let options = FindOptions {
            filter: Some(filter),
            include_dependencies: true,
            ..FindOptions::default()
        };
        let label = format!("filter {filter:?}");
        let pushed =
            sorted_values(index_served(&registry, &label, || registry.find_all(options)).unwrap());
        let full = sorted_values(test_hooks::without_index(|| registry.find_all(options)).unwrap());
        assert_eq!(pushed, full, "{label}");
    }
}

/// Guards against pushdown silently degrading to full loads: production
/// filter shapes must be served by indexes and load only their candidates.
#[test]
fn pushdown_serves_production_filters_from_indexes() {
    if !index_enabled() {
        return; // Nothing to push down to: every read comes from the files.
    }
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_pushdown_registry(&registry);
    let total = registry.storage.file_ids().unwrap().len();

    let cases: &[(&str, usize)] = &[
        ("id = 'unit-005'", 1),
        ("id IN ('unit-001', 'unit-002', 'unit-119')", 3),
        (
            "inScope = true AND isMissing = false AND planning.wave = 2",
            20,
        ),
        ("kind = 'etl'", 0),
        ("source.objectType = 'procedure'", 40),
        (
            "(source.canonicalName = 'nope' OR (source.schema = 'dbo' AND source.name = 'OBJ_8'))",
            1,
        ),
    ];
    for (filter, max_candidates) in cases {
        let prefilter = pushdown::from_filter(&Filter::parse(filter).unwrap())
            .unwrap_or_else(|| panic!("{filter:?} did not translate"));
        let candidates = index_served(&registry, filter, || {
            registry
                .storage
                .load_candidates(&prefilter, |key, _| key.to_string())
        })
        .unwrap()
        .unwrap_or_else(|| panic!("{filter:?} fell back to a full scan"));
        assert!(
            candidates.len() <= *max_candidates && candidates.len() < total,
            "{filter:?}: {} candidates of {total}",
            candidates.len()
        );
    }
}

/// Review repro: a sibling document with an enum value serde rejects makes
/// every filtered read fail, as it does when reading the files — even a
/// filter the sibling cannot match.
#[test]
fn pushdown_invalid_enum_sibling_fails_filtered_reads_like_a_full_load() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    write_raw(
        &registry,
        "good",
        r#"{"id":"good","kind":"databaseObject"}"#,
    );
    write_raw(&registry, "bad", r#"{"id":"bad","kind":"invalid-kind"}"#);

    for filter in [
        "id = 'good'",
        "kind = 'databaseObject'",
        "kind = 'invalid-kind'",
        "source.schema = 'nope'",
    ] {
        let options = FindOptions {
            filter: Some(filter),
            ..FindOptions::default()
        };
        let pushed = read_outcome(index_served(&registry, filter, || {
            registry.find_all(options)
        }));
        let full = read_outcome(test_hooks::without_index(|| registry.find_all(options)));
        assert!(full.is_err(), "{filter:?}: the files reject 'bad'");
        assert_eq!(pushed, full, "{filter:?}");
    }
    let partial = serde_json::json!({ "id": "good" });
    let pushed = read_outcome(index_served(&registry, "partial", || {
        registry.find_by_object(&partial, None)
    }));
    let full = read_outcome(test_hooks::without_index(|| {
        registry.find_by_object(&partial, None)
    }));
    assert!(full.is_err());
    assert_eq!(pushed, full);
}

/// Review repro: with duplicate keys serde keeps the last one, so the
/// indexed value must be the last one too (SQLite's `json_extract` would
/// read the first).
#[test]
fn pushdown_finds_documents_by_their_last_duplicate_key() {
    let dir = temp_dir();
    let registry = init_bare(dir.path());
    write_raw(
        &registry,
        "duplicate",
        r#"{"id":"duplicate","source":{"schema":"A","schema":"B"}}"#,
    );
    write_raw(
        &registry,
        "plain",
        r#"{"id":"plain","source":{"schema":"A"}}"#,
    );

    for (filter, want) in [
        ("source.schema = 'B'", vec!["duplicate"]),
        ("source.schema = 'A'", vec!["plain"]),
        ("source.schema IN ('B', 'C')", vec!["duplicate"]),
    ] {
        let options = FindOptions {
            filter: Some(filter),
            ..FindOptions::default()
        };
        let pushed = read_outcome(index_served(&registry, filter, || {
            registry.find_all(options)
        }));
        let full = read_outcome(test_hooks::without_index(|| registry.find_all(options)));
        assert_eq!(pushed, full, "{filter:?}");
        let ids: Vec<&str> = full
            .as_ref()
            .unwrap()
            .iter()
            .map(|v| v["id"].as_str().unwrap())
            .collect();
        assert_eq!(ids, want, "{filter:?}");
    }
    for (partial, want) in [
        (
            serde_json::json!({ "source": { "schema": "B" } }),
            vec!["duplicate"],
        ),
        (
            serde_json::json!({ "source": { "schema": "A" } }),
            vec!["plain"],
        ),
    ] {
        let label = format!("partial {partial}");
        let pushed = read_outcome(index_served(&registry, &label, || {
            registry.find_by_object(&partial, None)
        }));
        let full = read_outcome(test_hooks::without_index(|| {
            registry.find_by_object(&partial, None)
        }));
        assert_eq!(pushed, full, "{label}");
        let ids: Vec<&str> = full
            .as_ref()
            .unwrap()
            .iter()
            .map(|v| v["id"].as_str().unwrap())
            .collect();
        assert_eq!(ids, want, "{label}");
    }
}

/// Deterministic generator for [`derived_values_match_what_predicates_see`]:
/// the state, and how many duplicate keys it generated.
struct DocRng(u64, usize);

impl DocRng {
    fn next(&mut self) -> u64 {
        // splitmix64
        self.0 = self.0.wrapping_add(0x9e37_79b9_7f4a_7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
        z ^ (z >> 31)
    }

    fn below(&mut self, n: usize) -> usize {
        (self.next() % n as u64) as usize
    }

    fn chance(&mut self, num: usize, den: usize) -> bool {
        self.below(den) < num
    }

    fn pick<'a>(&mut self, options: &[&'a str]) -> &'a str {
        options[self.below(options.len())]
    }
}

/// A JSON object that may hold duplicate keys, rendered as text.
struct DupObject(Vec<(String, String)>);

impl DupObject {
    fn new() -> Self {
        Self(Vec::new())
    }

    fn insert(&mut self, key: &str, raw: String) {
        self.0.push((key.to_string(), raw));
    }

    /// Possibly repeat one key with another value, before or after it.
    fn duplicate(&mut self, r: &mut DocRng, other: impl FnOnce(&mut DocRng, &str) -> String) {
        if self.0.is_empty() || !r.chance(1, 4) {
            return;
        }
        let at = r.below(self.0.len());
        let key = self.0[at].0.clone();
        let value = other(r, &key);
        let position = if r.chance(1, 2) { at } else { self.0.len() };
        self.0.insert(position, (key, value));
        r.1 += 1;
    }

    fn render(&self) -> String {
        let fields: Vec<String> = self
            .0
            .iter()
            .map(|(k, v)| format!("{}:{v}", serde_json::to_string(k).unwrap()))
            .collect();
        format!("{{{}}}", fields.join(","))
    }
}

const GEN_TEXTS: &[&str] = &[
    "\"A\"", "\"B\"", "\"01\"", "\"1\"", "\"\"", "\"x'y\"", "null", "5", "{}",
];
const GEN_KINDS: &[&str] = &[
    "\"databaseObject\"",
    "\"script\"",
    "\"etl\"",
    "\"custom\"",
    "\"invalid-kind\"",
    "\"Script\"",
    "null",
    "5",
    "[\"x\"]",
];
const GEN_OBJECT_TYPES: &[&str] = &[
    "\"table\"",
    "\"view\"",
    "\"procedure\"",
    "\"TABLE\"",
    "null",
    "3",
];
const GEN_WAVES: &[&str] = &[
    "0",
    "1",
    "2",
    "3",
    "-1",
    "10",
    "9007199254740993",
    "null",
    "\"2\"",
    "1.5",
    "2.0",
    "99999999999999999999",
];
const GEN_BOOLS: &[&str] = &["true", "false", "true", "false", "null", "\"yes\"", "1"];

/// Value for `key` at one level of a generated document (raw JSON text):
/// from the valid domain only (`valid`), or from every shape.
fn gen_value(r: &mut DocRng, key: &str, valid: bool) -> String {
    let pick = |r: &mut DocRng, options: &[&str], valid_prefix: usize| -> String {
        let n = if valid { valid_prefix } else { options.len() };
        options[r.below(n)].to_string()
    };
    match key {
        "kind" => pick(r, GEN_KINDS, 4),
        "objectType" => pick(r, GEN_OBJECT_TYPES, 3),
        "wave" => pick(r, GEN_WAVES, 8),
        "inScope" | "isMissing" => pick(r, GEN_BOOLS, 4),
        "schemaVersion" => pick(r, &["1", "0", "2", "999", "\"1\"", "1.0", "null"], 1),
        "id" => pick(r, &["null", "\"other\"", "7"], 1),
        _ => pick(r, GEN_TEXTS, 7),
    }
}

/// A random stored document for `key`: two thirds drawn from valid values
/// only (duplicate keys and unknown fields included), the rest with every
/// kind of irregularity (invalid enums, wrong types, other schema versions,
/// id mismatch, duplicate keys at every level, non-object and invalid JSON).
fn gen_stored_doc(r: &mut DocRng, key: &str) -> String {
    let valid = r.chance(2, 3);
    if !valid {
        match r.below(10) {
            0 => return r.pick(&["[1,2]", "5", "\"s\"", "null", "true"]).to_string(),
            1 => {
                return r
                    .pick(&["{", "{ not json", "", "{\"a\":1,}", "{a:1}"])
                    .to_string()
            }
            _ => {}
        }
    }
    let value = |r: &mut DocRng, key: &str| gen_value(r, key, valid);
    let mut doc = DupObject::new();
    match r.below(8) {
        0 => {}
        1 => doc.insert("id", value(r, "id")),
        _ => doc.insert("id", serde_json::to_string(key).unwrap()),
    }
    if r.chance(1, 6) {
        doc.insert("schemaVersion", value(r, "schemaVersion"));
    }
    if r.chance(3, 4) {
        doc.insert("kind", value(r, "kind"));
    }
    for side in ["source", "target"] {
        match r.below(12) {
            0 => continue,
            1 => {
                let n = if valid { 1 } else { 3 };
                doc.insert(side, ["null", "\"TABLE\"", "[]"][r.below(n)].to_string());
                continue;
            }
            _ => {}
        }
        let mut m = DupObject::new();
        let fields: &[&str] = if side == "source" {
            &["objectType", "database", "schema", "name", "canonicalName"]
        } else {
            &["objectType", "database", "schema", "name"]
        };
        for field in fields {
            if r.chance(2, 3) {
                m.insert(field, value(r, field));
            }
        }
        if r.chance(1, 8) {
            m.insert("unknownField", "{\"nested\":[1]}".to_string());
        }
        m.duplicate(r, value);
        doc.insert(side, m.render());
    }
    match r.below(8) {
        0 => {}
        1 => {
            let n = if valid { 1 } else { 3 };
            doc.insert("planning", ["{}", "null", "[3]"][r.below(n)].to_string());
        }
        _ => {
            let mut m = DupObject::new();
            m.insert("wave", value(r, "wave"));
            if r.chance(1, 4) {
                m.insert("waveRank", "4".to_string());
            }
            m.duplicate(r, value);
            doc.insert("planning", m.render());
        }
    }
    for flag in ["inScope", "isMissing"] {
        if r.chance(1, 2) {
            doc.insert(flag, value(r, flag));
        }
    }
    if r.chance(1, 10) {
        doc.insert("notes", "\"unknown top-level field\"".to_string());
    }
    if !valid && r.chance(1, 10) {
        doc.insert("issues", "[{\"severity\":\"nope\"}]".to_string());
    }
    doc.duplicate(r, value);
    doc.render()
}

/// The filter text testing `path` against the indexed `value`, which the
/// predicate must accept.
fn filter_for(
    path: &str,
    value: Option<&storage::index::IndexValue>,
    kind: storage::index::FieldKind,
) -> String {
    use storage::index::{FieldKind, IndexValue};
    match (value, kind) {
        (None, _) => format!("{path} IS NULL"),
        (Some(IndexValue::Text(s)), _) => format!("{path} = '{}'", s.replace('\'', "''")),
        (Some(IndexValue::Integer(i)), FieldKind::Bool) => format!("{path} = {}", *i == 1),
        // A string literal: the filter engine has no negative literals
        // (unary minus), but compares numeric-looking strings as numbers.
        (Some(IndexValue::Integer(i)), _) => format!("{path} = '{i}'"),
    }
}

/// `value` nested under `path`, as a `find_by_object` partial.
fn partial_for(path: &[&str], value: serde_json::Value) -> serde_json::Value {
    path.iter().rev().fold(
        value,
        |inner, segment| serde_json::json!({ *segment: inner }),
    )
}

/// Differential property: for generated documents of every shape, a
/// document is regular exactly when the files-only strict read accepts it,
/// and its indexed values are exactly what `Filter` and `matches_partial`
/// see in the loaded unit. Every irregular document — and every regular one
/// a predicate accepts — is a candidate for every prefilter.
#[test]
fn derived_values_match_what_predicates_see() {
    use storage::index::{derive, FieldKind, IndexValue, IndexedField, Prefilter};
    const DOCS: usize = 1500;
    let mut r = DocRng(0x5eed_f00d_d0c5, 0);
    // (key, text, whether it repeats a key)
    let docs: Vec<(String, String, bool)> = (0..DOCS)
        .map(|i| {
            let key = format!("k{i:04}");
            let before = r.1;
            let text = gen_stored_doc(&mut r, &key);
            (key, text, r.1 > before)
        })
        .collect();

    // Per document: the files-only strict read of a registry holding it alone.
    let dir = temp_dir();
    let single = init_bare(dir.path());
    let mut seen: Vec<Option<serde_json::Value>> = Vec::with_capacity(DOCS);
    let (mut regular, mut duplicates) = (0, 0);
    for (key, text, duplicated) in &docs {
        write_raw(&single, key, text);
        let read = test_hooks::without_index(|| single.find_all(FindOptions::default()));
        fs::remove_file(single.storage.files().path_for(key)).unwrap();
        let derived = derive(key, text);
        let loaded = read.ok().map(|units| {
            assert_eq!(units.len(), 1, "{text}");
            serde_json::to_value(&units[0]).unwrap()
        });
        assert_eq!(derived.regular, loaded.is_some(), "regular? {key}: {text}");
        if let Some(json) = &loaded {
            regular += 1;
            duplicates += usize::from(*duplicated);
            for field in IndexedField::ALL {
                let mut at = Some(json);
                for segment in field.path() {
                    at = at.and_then(|v| v.get(*segment));
                }
                let expected = match at {
                    None | Some(serde_json::Value::Null) => None,
                    Some(serde_json::Value::String(s)) => Some(IndexValue::Text(s.clone())),
                    Some(serde_json::Value::Bool(b)) => Some(IndexValue::Integer(i64::from(*b))),
                    Some(serde_json::Value::Number(n)) => {
                        Some(IndexValue::Integer(n.as_i64().unwrap()))
                    }
                    Some(other) => panic!("{field:?} = {other} in {json}"),
                };
                let value = derived.value(field);
                assert_eq!(value, expected.as_ref(), "{field:?} of {key}: {text}");
                if field.kind() == FieldKind::Bool {
                    assert!(value.is_some(), "{field:?} is never NULL: {text}");
                }
                // The predicates agree with the indexed value.
                let path = field.path().join(".");
                let filter = filter_for(&path, value, field.kind());
                assert!(
                    Filter::parse(&filter).unwrap().matches(json),
                    "{filter} on {json}"
                );
                if let Some(v) = value {
                    let not_null = format!("{path} IS NOT NULL");
                    assert!(
                        Filter::parse(&not_null).unwrap().matches(json),
                        "{not_null}"
                    );
                    let leaf = match (v, field.kind()) {
                        (IndexValue::Text(s), _) => serde_json::json!(s),
                        (IndexValue::Integer(i), FieldKind::Bool) => serde_json::json!(*i == 1),
                        (IndexValue::Integer(i), _) => serde_json::json!(i),
                    };
                    let partial = partial_for(field.path(), leaf);
                    assert!(matches_partial(&partial, json), "{partial} on {json}");
                }
            }
        } else {
            assert!(derived.values.iter().all(Option::is_none), "{text}");
        }
        seen.push(loaded);
    }
    // The generator covers both sides well.
    assert!(
        regular > DOCS / 5 && regular < DOCS * 4 / 5,
        "{regular} regular of {DOCS}"
    );
    assert!(
        duplicates > 100,
        "{duplicates} regular documents with duplicate keys"
    );

    // All documents in one registry: candidates for every prefilter.
    let dir = temp_dir();
    let all = init_bare(dir.path());
    for (key, text, _) in &docs {
        write_raw(&all, key, text);
    }
    let irregular: std::collections::BTreeSet<&str> = docs
        .iter()
        .zip(&seen)
        .filter(|(_, s)| s.is_none())
        .map(|((key, _, _), _)| key.as_str())
        .collect();
    let filters: Vec<String> = PUSHDOWN_FILTERS
        .iter()
        .map(|f| f.to_string())
        .chain(
            [
                "kind = 'script'",
                "kind IN ('etl', 'custom')",
                "source.schema = 'B'",
                "source.schema = 'x''y'",
                "target.name = 'A' OR source.canonicalName = '01'",
                "source.objectType = 'table' AND planning.wave >= 2",
                "planning.wave = 9007199254740993",
                "planning.wave < 0",
                "isMissing AND NOT inScope",
                "id = 'k0003'",
                "id IN ('k0001', 'k0002', 'k1499')",
            ]
            .map(String::from),
        )
        .collect();
    let mut prefilters: Vec<(String, Prefilter)> = filters
        .iter()
        .filter_map(|f| pushdown::from_filter(&Filter::parse(f).unwrap()).map(|p| (f.clone(), p)))
        .collect();
    prefilters.push((
        "constant false".into(),
        Prefilter::In(IndexedField::Kind, vec![]),
    ));
    let mut served = 0;
    for (label, prefilter) in &prefilters {
        let Some(candidates) = all
            .storage
            .load_candidates(prefilter, |key, _| key.to_string())
            .unwrap()
        else {
            continue; // Not servable (or no index): the caller scans.
        };
        served += 1;
        let candidates: std::collections::BTreeSet<String> = candidates.into_iter().collect();
        for key in &irregular {
            assert!(
                candidates.contains(*key),
                "{label}: irregular {key} missing"
            );
        }
        if let Ok(filter) = Filter::parse(label) {
            for ((key, text, _), json) in docs.iter().zip(&seen) {
                if json.as_ref().is_some_and(|json| filter.matches(json)) {
                    assert!(
                        candidates.contains(key),
                        "{label}: match {key} missing: {text}"
                    );
                }
            }
        }
    }
    if index_enabled() {
        assert!(
            served > prefilters.len() / 2,
            "{served} of {} served",
            prefilters.len()
        );
    }

    // Regular documents only: indexed reads equal files-only reads.
    let dir = temp_dir();
    let regular_only = init_bare(dir.path());
    for ((key, text, _), json) in docs.iter().zip(&seen) {
        if json.is_some() {
            write_raw(&regular_only, key, text);
        }
    }
    for filter in &filters {
        let options = FindOptions {
            filter: Some(filter),
            ..FindOptions::default()
        };
        let pushed = read_outcome(index_served(&regular_only, filter, || {
            regular_only.find_all(options)
        }));
        let full = read_outcome(test_hooks::without_index(|| regular_only.find_all(options)));
        assert!(full.is_ok(), "{filter}: {full:?}");
        assert_eq!(pushed, full, "{filter}");
    }
}

// ── Projected-read fast path ─────────────────────────────────────────────
//
// Unfiltered `find_all` with `fields` decodes only the needed top-level keys;
// it must return exactly what a full parse + projection returns.

/// Seed `registry` with created units plus raw documents covering the
/// shapes the fast path handles differently from a full decode.
fn seed_projection_registry(registry: &CodeUnitRegistry) {
    seed_pushdown_registry(registry);
    let mut with_files = make_code_unit_with_files(
        "with-files",
        Some("source/a.sql".to_string()),
        Some("snowflake/a.sql".to_string()),
        None,
    );
    set_dependency_ids(&mut with_files, &["unit-001", "unit-002"]);
    registry.create(&mut with_files, None).unwrap();

    let mut raw = read_raw_value(registry, "with-files");
    let doc = raw.as_object_mut().unwrap();
    // Path normalization only happens on read (strip `./`).
    doc["files"]["source"]["path"] = serde_json::json!("./source/a.sql");
    doc.insert("futureTopLevel".into(), serde_json::json!({ "x": 1 }));
    doc["source"]["futureNested"] = serde_json::json!(true);
    doc["source"]["schema"] = serde_json::Value::Null;
    write_raw_value(registry, "with-files", &raw);

    // No embedded id (derived from the key), no inScope (defaults to true),
    // explicit schemaVersion.
    let mut raw = read_raw_value(registry, "unit-002");
    let doc = raw.as_object_mut().unwrap();
    doc.remove("id");
    doc.remove("inScope");
    doc.insert("schemaVersion".into(), serde_json::json!(1));
    write_raw_value(registry, "unit-002", &raw);
}

const PROJECTIONS: &[&[&str]] = &[
    &["id"],
    &[
        "id",
        "kind",
        "source",
        "target",
        "codeStatus",
        "planning",
        "inScope",
        "isMissing",
    ],
    &["inScope"],
    &["isMissing", "schemaVersion"],
    &["planning.wave"],
    &["source.name", "target"],
    &["source.schema"],
    &["source.futureNested"],
    &["files"],
    &["files.source.path"],
    &["dependencies"],
    &["id", "dependencies.dependsOn"],
    &["futureTopLevel"],
    &["extensions"],
    &["nonexistent"],
    &[],
];

#[test]
fn fast_projection_matches_full_parse() {
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_projection_registry(&registry);
    for fields in PROJECTIONS {
        let options = FindOptions {
            fields: Some(fields),
            ..FindOptions::default()
        };
        let label = format!("{fields:?}");
        let fast =
            sorted_values(index_served(&registry, &label, || registry.find_all(options)).unwrap());
        let full = sorted_values(
            test_hooks::without_fast_projection(|| registry.find_all(options)).unwrap(),
        );
        assert_eq!(fast.len(), full.len(), "{label}");
        assert_eq!(fast, full, "{label}");
        // The fast path over the index equals the fast path over the files.
        let from_files =
            sorted_values(test_hooks::without_index(|| registry.find_all(options)).unwrap());
        assert_eq!(fast, from_files, "{label}: index vs files");
    }
}

/// Every document is still syntax-, version-, and id-checked; only a type
/// error in a field outside the projection no longer fails the read.
#[test]
fn fast_projection_strictness() {
    let fails_both: [(&str, &str); 4] = [
        ("corrupt", "NOT VALID JSON"),
        ("array", "[1, 2]"),
        ("future", r#"{"id":"future","schemaVersion":999}"#),
        ("mismatch", r#"{"id":"someone-else"}"#),
    ];
    for (key, text) in fails_both {
        let dir = temp_dir();
        let registry = CodeUnitRegistry::init(dir.path()).unwrap();
        seed_pushdown_registry(&registry);
        write_raw(&registry, key, text);
        let options = FindOptions {
            fields: Some(&["id"]),
            ..FindOptions::default()
        };
        let fast = index_served(&registry, key, || registry.find_all(options))
            .map(|_| ())
            .map_err(|e| e.error_code());
        let full = test_hooks::without_fast_projection(|| registry.find_all(options))
            .map(|_| ())
            .map_err(|e| e.error_code());
        let from_files = test_hooks::without_index(|| registry.find_all(options))
            .map(|_| ())
            .map_err(|e| e.error_code());
        assert!(full.is_err(), "{key}: full parse should fail");
        assert_eq!(fast, full, "{key}");
        assert_eq!(fast, from_files, "{key}: index vs files");
    }

    // A type error in a projected field still fails; outside the
    // projection it is no longer decoded, so the read succeeds.
    let dir = temp_dir();
    let registry = CodeUnitRegistry::init(dir.path()).unwrap();
    seed_pushdown_registry(&registry);
    write_raw(&registry, "bad-source", r#"{"id":"bad-source","source":5}"#);
    let read = |fields: &'static [&'static str]| {
        registry.find_all(FindOptions {
            fields: Some(fields),
            ..FindOptions::default()
        })
    };
    assert!(
        index_served(&registry, "projected type error", || read(&["source"])).is_err(),
        "projected type error"
    );
    let ids: Vec<String> = index_served(&registry, "unprojected type error", || read(&["id"]))
        .unwrap()
        .into_iter()
        .filter_map(|u| u.id)
        .collect();
    assert!(ids.contains(&"bad-source".to_string()));
    assert!(
        test_hooks::without_fast_projection(|| read(&["id"])).is_err(),
        "the full parse still rejects it"
    );
}

// ── Git simulation: the files change behind the library's back ───────────
//
// The JSON files are the record; git (checkout, pull, rebase), editors, and
// other tools change them without the library. Whatever the index serves
// afterwards must equal a files-only read (`without_index`). Each case
// applies one external change right before every query shape, so each shape
// is exercised as the first read after a change. Changes and reads run back
// to back, as real tools do, usually within one filesystem clock tick; the
// only sleep (`wait_out_racy_window`) is before the `update_where` check
// that requires the index to serve the write's own selection.

/// A query shape served by the index (when trusted) on the read path.
enum Shape {
    Filtered(&'static str),
    WithDependencies(&'static str),
    ByObject(serde_json::Value),
    Projected(&'static [&'static str]),
}

impl Shape {
    fn run(&self, registry: &CodeUnitRegistry) -> Result<Vec<CodeUnit>> {
        match self {
            Shape::Filtered(filter) => registry.find_all(FindOptions {
                filter: Some(filter),
                ..FindOptions::default()
            }),
            Shape::WithDependencies(filter) => registry.find_all(FindOptions {
                filter: Some(filter),
                include_dependencies: true,
                ..FindOptions::default()
            }),
            Shape::ByObject(partial) => registry.find_by_object(partial, None),
            Shape::Projected(fields) => registry.find_all(FindOptions {
                fields: Some(fields),
                ..FindOptions::default()
            }),
        }
    }

    fn label(&self) -> String {
        match self {
            Shape::Filtered(filter) => format!("find_all {filter:?}"),
            Shape::WithDependencies(filter) => format!("find_all+deps {filter:?}"),
            Shape::ByObject(partial) => format!("find_by_object {partial}"),
            Shape::Projected(fields) => format!("find_all fields {fields:?}"),
        }
    }
}

/// Every shape the git-simulation cases check. External changes write
/// `planning.wave` 7/8 and names `EXTERNAL`, so these filters see them.
fn git_shapes() -> Vec<Shape> {
    vec![
        // Indexed filters.
        Shape::Filtered("planning.wave = 7"),
        Shape::Filtered("planning.wave IN (2, 8)"),
        Shape::Filtered("source.objectType = 'view' AND inScope"),
        Shape::Filtered("source.schema = 'SALES'"),
        Shape::Filtered("source.name = 'EXTERNAL'"),
        Shape::Filtered("id IN ('unit-003', 'unit-010', 'unit-031', 'added-000', 'renamed-010')"),
        // Unindexed filters.
        Shape::Filtered("source.name LIKE 'OBJ_1%'"),
        Shape::Filtered("target.name = 'EXTERNAL'"),
        Shape::ByObject(serde_json::json!({ "planning": { "wave": 7 } })),
        Shape::ByObject(
            serde_json::json!({ "source": { "objectType": "view", "schema": "SALES" } }),
        ),
        Shape::ByObject(serde_json::json!({ "target": { "name": "EXTERNAL" } })),
        Shape::Projected(&["id", "planning", "source.name", "dependencies.dependsOn"]),
        Shape::WithDependencies("id = 'unit-040'"),
        Shape::WithDependencies("planning.wave = 7"),
        Shape::WithDependencies("source.name = 'EXTERNAL'"),
    ]
}

/// A read's result, comparable across the index and files-only paths.
fn read_outcome(result: Result<Vec<CodeUnit>>) -> std::result::Result<Vec<serde_json::Value>, u32> {
    result.map(sorted_values).map_err(|e| e.error_code())
}

/// Assert `shape` on `registry` equals the files-only reference, returning
/// the outcome. With `expect_index`, the index must have served the read.
fn check_shape_outcome(
    registry: &CodeUnitRegistry,
    label: &str,
    shape: &Shape,
    expect_index: bool,
) -> std::result::Result<Vec<serde_json::Value>, u32> {
    let label = format!("{label}: {}", shape.label());
    let actual = if expect_index {
        read_outcome(index_served(registry, &label, || shape.run(registry)))
    } else {
        read_outcome(shape.run(registry))
    };
    let expected = read_outcome(test_hooks::without_index(|| shape.run(registry)));
    assert_eq!(actual, expected, "{label}");
    actual
}

/// [`check_shape_outcome`] when only the comparison matters.
fn check_shape(registry: &CodeUnitRegistry, label: &str, shape: &Shape, expect_index: bool) {
    let _ = check_shape_outcome(registry, label, shape, expect_index);
}

/// For each shape: apply `change(round)`, then check that shape first. Then
/// check every shape again on the settled state, and finally `update_where`
/// right after one more change.
fn check_after_each_change(
    registry: &CodeUnitRegistry,
    label: &str,
    expect_index: bool,
    mut change: impl FnMut(&CodeUnitRegistry, usize),
) {
    let shapes = git_shapes();
    for (round, shape) in shapes.iter().enumerate() {
        change(registry, round);
        check_shape(
            registry,
            &format!("{label} round {round}"),
            shape,
            expect_index,
        );
    }
    for shape in &shapes {
        check_shape(registry, &format!("{label} settled"), shape, expect_index);
    }
    // Right after a change, the write's own selection may come from the
    // files (its sweep can't vouch for the racy directory mtime): correctness
    // only. Once the change is older than a clock tick, the index serves it.
    let rounds = shapes.len();
    change(registry, rounds);
    check_update_where(registry, label, "planning.wave IN (7, 8)", false);
    change(registry, rounds + 1);
    check_update_where(registry, label, "target.name = 'EXTERNAL'", expect_index);
    change(registry, rounds + 2);
    // Broad, so it writes some units in every case.
    check_update_where(registry, label, "source.objectType = 'view'", false);
}

/// Rounds [`check_after_each_change`] calls `change` for.
fn change_rounds() -> usize {
    git_shapes().len() + 3
}

/// Sleep until the registry directory's last change is older than any
/// same-tick race the index guards against (coarse kernel clocks: ≤ 10 ms
/// ticks; whole-second mtimes: filesystems with 1–2 s granularity), the way
/// a later command in a real session would run.
fn wait_out_racy_window(registry: &CodeUnitRegistry) {
    let mtime = fs::metadata(registry.storage.files().dir())
        .unwrap()
        .modified()
        .unwrap();
    let whole_second = mtime
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .subsec_nanos()
        == 0;
    let margin = std::time::Duration::from_millis(if whole_second { 2_100 } else { 50 });
    while std::time::SystemTime::now() < mtime + margin {
        std::thread::sleep(std::time::Duration::from_millis(5));
    }
}

/// Units for the git-simulation cases: indexed fields varied, plus
/// `dependsOn` chains (`unit-i` → `unit-i/2`) for `include_dependencies`.
fn seed_git_registry(registry: &CodeUnitRegistry) {
    let types = [
        CodeUnitObjectType::Table,
        CodeUnitObjectType::View,
        CodeUnitObjectType::Procedure,
    ];
    let mut batch = Vec::new();
    for i in 0..60usize {
        let mut unit = make_code_unit(&git_id(i), &format!("OBJ_{i}"), types[i % 3]);
        unit.source.as_mut().unwrap().schema = Some(["dbo", "SALES"][i % 2].to_string());
        unit.in_scope = i % 4 != 0;
        unit.planning.get_or_insert_with(Default::default).wave = Some((i % 5) as i64);
        if i > 0 && i % 3 != 0 {
            set_dependency_ids(&mut unit, &[&git_id(i / 2)]);
        }
        batch.push(unit);
    }
    let result = registry.create_batch(&mut batch, None).unwrap();
    assert!(result.failed.is_empty(), "{:?}", result.failed);
}

fn git_id(i: usize) -> String {
    format!("unit-{:03}", i % 60)
}

/// A git-sim registry: seeded, with the index warmed by one read.
fn init_git_registry(path: &std::path::Path) -> CodeUnitRegistry {
    let registry = CodeUnitRegistry::init(path).unwrap();
    seed_git_registry(&registry);
    index_served(&registry, "warm-up", || {
        registry.find_all(FindOptions::default())
    })
    .unwrap();
    registry
}

/// Externally replace `id`'s file (temp + rename, as git does) with `edit`
/// applied to its current document.
fn replace_external(
    registry: &CodeUnitRegistry,
    id: &str,
    edit: impl FnOnce(&mut serde_json::Value),
) {
    let mut doc = read_raw_value(registry, id);
    edit(&mut doc);
    write_raw_value(registry, id, &doc);
}

/// Set `planning.wave` to 7, or to 8 if it already is 7.
fn toggle_wave(doc: &mut serde_json::Value) {
    let wave = if doc["planning"]["wave"] == 7 { 8 } else { 7 };
    doc["planning"]["wave"] = serde_json::json!(wave);
}

/// A unit document as another library instance (a teammate) would write it.
fn teammate_doc(unit: CodeUnit) -> String {
    let dir = temp_dir();
    let teammate = CodeUnitRegistry::init(dir.path()).unwrap();
    let id = unit.id.clone().unwrap();
    teammate.create(&mut unit.clone(), None).unwrap();
    read_raw_text(&teammate, &id)
}

/// Copy the record (the JSON files only, no index) into `root/registry`.
fn copy_registry(registry: &CodeUnitRegistry, root: &std::path::Path) -> CodeUnitRegistry {
    let target = CodeUnitRegistry::init(root).unwrap();
    for id in registry.storage.file_ids().unwrap() {
        fs::copy(
            registry.storage.files().path_for(&id),
            target.storage.files().path_for(&id),
        )
        .unwrap();
    }
    target
}

/// Make `registry`'s files equal `branch`'s, the way `git checkout` does:
/// changed and new files are replaced/created, missing ones deleted. Every
/// other changed file is written by unlink + create (what git itself does),
/// the rest by temp + rename.
fn checkout(registry: &CodeUnitRegistry, branch: &CodeUnitRegistry) {
    let wanted = branch.storage.file_ids().unwrap();
    for id in registry.storage.file_ids().unwrap() {
        if !wanted.contains(&id) {
            fs::remove_file(registry.storage.files().path_for(&id)).unwrap();
        }
    }
    for (n, id) in wanted.iter().enumerate() {
        let text = read_raw_text(branch, id);
        let path = registry.storage.files().path_for(id);
        if fs::read_to_string(&path).ok().as_deref() == Some(text.as_str()) {
            continue;
        }
        if n % 2 == 0 {
            write_raw(registry, id, &text);
        } else {
            let _ = fs::remove_file(&path);
            fs::write(&path, &text).unwrap();
        }
    }
}

/// The record with `updatedAt` stamps removed, for comparing two registries
/// that ran the same writes at slightly different times.
fn record_snapshot(
    registry: &CodeUnitRegistry,
) -> std::collections::BTreeMap<String, serde_json::Value> {
    fn strip(value: &mut serde_json::Value) {
        match value {
            serde_json::Value::Object(map) => {
                map.remove("updatedAt");
                map.values_mut().for_each(strip);
            }
            serde_json::Value::Array(items) => items.iter_mut().for_each(strip),
            _ => {}
        }
    }
    registry
        .storage
        .file_ids()
        .unwrap()
        .into_iter()
        .map(|id| {
            let text = read_raw_text(registry, &id);
            let mut value = serde_json::from_str(&text).unwrap_or(serde_json::Value::String(text));
            strip(&mut value);
            (id, value)
        })
        .collect()
}

type BatchOutcome = std::result::Result<(Vec<String>, Vec<(String, i32)>, Vec<String>), u32>;

fn batch_outcome(result: Result<BatchResult>) -> BatchOutcome {
    result
        .map(|r| {
            let mut succeeded = r.succeeded;
            succeeded.sort();
            let mut failed: Vec<(String, i32)> =
                r.failed.into_iter().map(|f| (f.id, f.error.code)).collect();
            failed.sort();
            let mut side_effects = r.side_effect_ids;
            side_effects.sort();
            (succeeded, failed, side_effects)
        })
        .map_err(|e| e.error_code())
}

/// `update_where` on `registry` must select and write exactly what it does
/// on a files-only copy of the same record: same result, same files after.
fn check_update_where(registry: &CodeUnitRegistry, label: &str, filter: &str, expect_index: bool) {
    let label = format!("{label}: update_where {filter:?}");
    let reference_dir = temp_dir();
    let reference = copy_registry(registry, reference_dir.path());
    let updates = [
        ("target.name", serde_json::json!("UPDATED")),
        ("planning.waveRank", serde_json::json!(5)),
    ];
    if expect_index {
        wait_out_racy_window(registry);
    }
    let run = |r: &CodeUnitRegistry| batch_outcome(r.update_where(filter, &updates, None));
    let actual = if expect_index {
        index_served(registry, &label, || run(registry))
    } else {
        run(registry)
    };
    let expected = test_hooks::without_index(|| run(&reference));
    assert_eq!(actual, expected, "{label}");
    assert_eq!(
        record_snapshot(registry),
        record_snapshot(&reference),
        "{label}: files"
    );
}

/// (a) An external replace changing an indexed field is seen by the very
/// next filtered read.
#[test]
fn git_sim_external_replace_is_seen_by_next_filtered_read() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());

    replace_external(&registry, "unit-012", toggle_wave);
    let wave7 = check_shape_outcome(
        &registry,
        "replace",
        &Shape::Filtered("planning.wave = 7"),
        true,
    );
    let ids: Vec<_> = wave7.unwrap().iter().map(|u| u["id"].clone()).collect();
    assert_eq!(ids, [serde_json::json!("unit-012")]);

    // Same size, possibly the same mtime: only the file id tells them apart.
    replace_external(&registry, "unit-012", |doc| {
        doc["planning"]["wave"] = 8.into()
    });
    let wave8 = check_shape_outcome(
        &registry,
        "same size",
        &Shape::Filtered("planning.wave = 8"),
        true,
    );
    assert_eq!(wave8.unwrap().len(), 1);

    check_after_each_change(&registry, "replace", true, |registry, round| {
        replace_external(registry, &git_id(round * 7 + 1), toggle_wave);
    });
}

/// (b) An externally added unit file shows up.
#[test]
fn git_sim_external_add() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    check_after_each_change(&registry, "add", true, |registry, round| {
        let id = format!("added-{round:03}");
        let mut unit = make_code_unit(&id, "EXTERNAL", CodeUnitObjectType::View);
        unit.target.as_mut().unwrap().name = Some("EXTERNAL".into());
        unit.planning.get_or_insert_with(Default::default).wave = Some(7 + (round % 2) as i64);
        set_dependency_ids(&mut unit, &[&git_id(round * 3 + 40)]);
        write_raw(registry, &id, &teammate_doc(unit));
    });
}

/// (c) An externally deleted unit file disappears, also from dependency
/// closures that reached it.
#[test]
fn git_sim_external_delete() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    check_after_each_change(&registry, "delete", true, |registry, round| {
        let path = registry.storage.files().path_for(&git_id(round * 7 + 2));
        fs::remove_file(path).unwrap();
    });
}

/// (d) An external rename (`git mv`) changes the key: same inode, size,
/// and mtime, under a different name.
#[test]
fn git_sim_external_rename() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    // Documents without an embedded `id` take theirs from the file name, so
    // a pure rename stays a valid unit.
    let renamed: Vec<String> = (0..change_rounds())
        .map(|round| git_id(round * 7 + 3))
        .collect();
    for id in &renamed {
        replace_external(&registry, id, |doc| {
            doc.as_object_mut().unwrap().remove("id");
        });
    }
    check_shape(
        &registry,
        "id-less",
        &Shape::Filtered("source.objectType = 'view'"),
        true,
    );

    check_after_each_change(&registry, "rename", true, |registry, round| {
        let from = &renamed[round];
        let to = from.replace("unit-", "renamed-");
        let files = registry.storage.files();
        fs::rename(files.path_for(from), files.path_for(&to)).unwrap();
    });
    let ids = check_shape_outcome(
        &registry,
        "renamed",
        &Shape::Filtered("id = 'renamed-010'"),
        true,
    );
    assert_eq!(ids.unwrap().len(), 1, "unit-010 was renamed in round 1");
}

/// (e) Switching branches back and forth: half the files replaced, some
/// deleted, some added on every switch.
#[test]
fn git_sim_branch_checkout() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    let main_dir = temp_dir();
    let main = copy_registry(&registry, main_dir.path());

    // The feature branch: a teammate's library changes on a copy.
    let feature_dir = temp_dir();
    let feature = copy_registry(&registry, feature_dir.path());
    let updates: Vec<(String, Vec<(&str, serde_json::Value)>)> = (0..60)
        .step_by(2)
        .map(|i| {
            let wave = if i % 4 == 0 { 7 } else { 8 };
            (
                git_id(i),
                vec![
                    ("planning.wave", serde_json::json!(wave)),
                    ("target.name", serde_json::json!("EXTERNAL")),
                ],
            )
        })
        .collect();
    let batch: Vec<(&str, Vec<(&str, serde_json::Value)>)> = updates
        .iter()
        .map(|(id, fields)| (id.as_str(), fields.clone()))
        .collect();
    let result = feature.update_batch(&batch, None).unwrap();
    assert!(result.failed.is_empty(), "{:?}", result.failed);
    for i in [5, 11, 17, 23, 29] {
        feature.delete(&git_id(i)).unwrap();
    }
    for n in 0..5 {
        let mut unit = make_code_unit(
            &format!("added-{n:03}"),
            "EXTERNAL",
            CodeUnitObjectType::View,
        );
        unit.planning.get_or_insert_with(Default::default).wave = Some(7);
        set_dependency_ids(&mut unit, &[&git_id(40 + n)]);
        feature.create(&mut unit, None).unwrap();
    }
    let changed = registry
        .storage
        .file_ids()
        .unwrap()
        .iter()
        .filter(|id| {
            !stored(&feature, id) || read_raw_text(&feature, id) != read_raw_text(&registry, id)
        })
        .count();
    assert!(
        changed >= 30,
        "only {changed} files differ between the branches"
    );

    check_after_each_change(&registry, "checkout", true, |registry, round| {
        checkout(registry, if round % 2 == 0 { &feature } else { &main });
    });
}

/// (f) An in-place rewrite (same inode) doesn't change the directory mtime:
/// a read right away may still see the old value (documented limit), but
/// after the periodic sweep interval it must see the new one.
#[test]
fn git_sim_in_place_edit_is_seen_after_periodic_sweep() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    for (round, shape) in git_shapes().iter().enumerate() {
        let label = format!("in-place round {round}");
        let before = read_outcome(test_hooks::without_index(|| shape.run(&registry)));
        // Size changes, so the fingerprint differs whatever the clock tick.
        let id = git_id(round * 7 + 4);
        let mut doc = read_raw_value(&registry, &id);
        toggle_wave(&mut doc);
        doc["source"]["name"] = "EXTERNAL".into();
        doc["target"]["name"] = format!("EXTERNAL_{round}").into();
        let path = registry.storage.files().path_for(&id);
        fs::write(&path, serde_json::to_string_pretty(&doc).unwrap()).unwrap();

        let after = read_outcome(test_hooks::without_index(|| shape.run(&registry)));
        let immediate = read_outcome(shape.run(&registry));
        assert!(
            immediate == before || immediate == after,
            "{label}: {}: neither the old nor the new result",
            shape.label()
        );
        // Each round is another 31 s later than the last.
        let later = std::time::Duration::from_secs(31 * (round as u64 + 1));
        let sweeps = registry.storage.sweeps();
        test_hooks::with_clock_offset(later, || {
            assert_eq!(check_shape_outcome(&registry, &label, shape, true), after);
        });
        if index_enabled() {
            assert!(
                registry.storage.sweeps() > sweeps,
                "{label}: the periodic sweep should have run"
            );
        }
    }
}

/// (f, racy) An in-place, same-size rewrite in the same clock tick as the
/// library write that produced the file leaves size, mtime, and inode all
/// unchanged; the periodic sweep must still not trust the stale row.
#[test]
fn git_sim_same_tick_in_place_edit_is_seen_after_periodic_sweep() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    for round in 0..5usize {
        let id = git_id(round * 11 + 6);
        registry
            .update(&id, &[("planning.wave", serde_json::json!(7))], None)
            .unwrap();
        let path = registry.storage.files().path_for(&id);
        let text = fs::read_to_string(&path).unwrap();
        let edited = text.replacen("\"wave\": 7", "\"wave\": 8", 1);
        assert_ne!(edited, text);
        fs::write(&path, edited).unwrap();

        let later = std::time::Duration::from_secs(31 * (round as u64 + 1));
        test_hooks::with_clock_offset(later, || {
            let label = format!("same-tick in-place round {round}");
            let wave8 = check_shape_outcome(
                &registry,
                &label,
                &Shape::Filtered("planning.wave = 8"),
                true,
            );
            let ids: Vec<_> = wave8.unwrap().iter().map(|u| u["id"].clone()).collect();
            assert!(ids.contains(&serde_json::json!(id)), "{label}: {ids:?}");
        });
    }
}

/// An external replace right after a library write (same clock tick, after
/// the write's own bookkeeping) is seen by the next read.
#[test]
fn git_sim_external_replace_right_after_library_write() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    for round in 0..10usize {
        registry
            .update(
                &git_id(round),
                &[("target.name", serde_json::json!("LIB"))],
                None,
            )
            .unwrap();
        let id = git_id(round * 7 + 30);
        replace_external(&registry, &id, toggle_wave);
        let label = format!("after library write round {round}");
        for shape in [
            Shape::Filtered("planning.wave IN (7, 8)"),
            Shape::Filtered("target.name = 'LIB'"),
        ] {
            check_shape(&registry, &label, &shape, true);
        }
    }
}

/// (g) The index directory deleted while registries are open.
#[cfg(unix)] // Windows can't delete an open database.
#[test]
fn git_sim_index_dir_deleted_while_open() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    let index = index_dir(&registry);
    let _ = fs::remove_dir_all(&index);

    // Another process (here: instance) opening afterwards rebuilds it.
    let other = CodeUnitRegistry::open(dir.path()).unwrap();
    check_shape(
        &other,
        "rebuilt",
        &Shape::Filtered("planning.wave = 2"),
        true,
    );
    if index_enabled() {
        assert!(index.is_dir(), "the index is rebuilt on first use");
    }

    check_after_each_change(&registry, "index deleted", false, |registry, round| {
        if round % 3 == 0 {
            let _ = fs::remove_dir_all(index_dir(registry));
        }
        replace_external(registry, &git_id(round * 7 + 1), toggle_wave);
        if round % 2 == 0 {
            other
                .update(
                    &git_id(round * 7 + 5),
                    &[("target.name", "EXTERNAL".into())],
                    None,
                )
                .unwrap();
        }
    });
    for shape in git_shapes() {
        check_shape(&other, "other instance", &shape, false);
    }
}

fn index_db_files(registry: &CodeUnitRegistry) -> Vec<std::path::PathBuf> {
    let Ok(entries) = fs::read_dir(index_dir(registry)) else {
        return Vec::new();
    };
    entries
        .map(|entry| entry.unwrap().path())
        .filter(|path| {
            let name = path.file_name().unwrap().to_string_lossy();
            name.starts_with('v') && name.ends_with(".db")
        })
        .collect()
}

fn write_garbage_over_index(registry: &CodeUnitRegistry) {
    let dbs = index_db_files(registry);
    if index_enabled() {
        assert!(
            !dbs.is_empty(),
            "no v*.db in {}",
            index_dir(registry).display()
        );
    }
    for db in dbs {
        fs::write(
            &db,
            b"<<<<<<< HEAD\nnot a database\n>>>>>>> theirs\n".repeat(64),
        )
        .unwrap();
    }
}

/// (h) Garbage written over `registry/.index/v*.db`: while closed (rebuilt
/// on open) and while open.
#[test]
fn git_sim_garbage_index_file() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    drop(registry);
    let registry = CodeUnitRegistry::open(dir.path()).unwrap();
    write_garbage_over_index(&registry);
    drop(registry);

    let registry = CodeUnitRegistry::open(dir.path()).unwrap();
    replace_external(&registry, "unit-012", toggle_wave);
    // Rebuilt from the files, so the index serves again.
    check_shape(
        &registry,
        "garbage while closed",
        &Shape::Filtered("planning.wave = 7"),
        true,
    );

    #[cfg(unix)] // Windows may refuse to overwrite an open database.
    {
        write_garbage_over_index(&registry);
        check_after_each_change(&registry, "garbage while open", false, |registry, round| {
            if round % 4 == 0 {
                write_garbage_over_index(registry);
            }
            replace_external(registry, &git_id(round * 7 + 1), toggle_wave);
        });
        let fresh = CodeUnitRegistry::open(dir.path()).unwrap();
        for shape in git_shapes() {
            check_shape(&fresh, "fresh instance", &shape, false);
        }
    }
}

/// (i) A read-only index directory: the index can't be updated, so reads
/// must not trust it (they may come from the files) and stay correct.
#[cfg(unix)]
#[test]
fn git_sim_read_only_index_dir() {
    use std::os::unix::fs::PermissionsExt;

    /// Restores write permission so the temp dir can be cleaned up.
    struct Restore(std::path::PathBuf);
    impl Drop for Restore {
        fn drop(&mut self) {
            if let Ok(entries) = fs::read_dir(&self.0) {
                let _ = fs::set_permissions(&self.0, fs::Permissions::from_mode(0o755));
                for entry in entries.flatten() {
                    let _ = fs::set_permissions(entry.path(), fs::Permissions::from_mode(0o644));
                }
            }
        }
    }

    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    let index = index_dir(&registry);
    let _restore = Restore(index.clone());
    if let Ok(entries) = fs::read_dir(&index) {
        for entry in entries.flatten() {
            fs::set_permissions(entry.path(), fs::Permissions::from_mode(0o444)).unwrap();
        }
        fs::set_permissions(&index, fs::Permissions::from_mode(0o555)).unwrap();
    }

    check_after_each_change(&registry, "read-only index", false, |registry, round| {
        replace_external(registry, &git_id(round * 7 + 1), toggle_wave);
        if round % 3 == 1 {
            registry
                .update(
                    &git_id(round * 7 + 5),
                    &[("target.name", "EXTERNAL".into())],
                    None,
                )
                .unwrap();
        }
    });
    let fresh = CodeUnitRegistry::open(dir.path()).unwrap();
    replace_external(&fresh, "unit-013", toggle_wave);
    for shape in git_shapes() {
        check_shape(&fresh, "fresh instance", &shape, false);
    }
}

/// (j) A library write right after an external change must not record the
/// directory as in sync over the unswept change (`prepare_write` sweeps).
#[test]
fn git_sim_library_write_after_external_change() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    check_after_each_change(&registry, "library write", true, |registry, round| {
        let external = git_id(round * 7 + 1);
        replace_external(registry, &external, toggle_wave);
        if round % 3 == 0 {
            fs::remove_file(registry.storage.files().path_for(&git_id(round * 7 + 2))).unwrap();
        }
        match round % 4 {
            // Another unit.
            0 => registry
                .update(
                    &git_id(round * 7 + 3),
                    &[("target.name", "EXTERNAL".into())],
                    None,
                )
                .unwrap(),
            // The externally changed unit itself: the merge reads the file.
            1 => registry
                .update(&external, &[("source.name", "EXTERNAL".into())], None)
                .unwrap(),
            2 => {
                let mut unit =
                    make_code_unit(&format!("lib-{round:03}"), "LIB", CodeUnitObjectType::Table);
                set_dependency_ids(&mut unit, &[&external]);
                registry.create(&mut unit, None).unwrap();
            }
            _ => {
                let result = registry
                    .update_where(
                        "source.name = 'OBJ_44'",
                        &[("target.name", "EXTERNAL".into())],
                        None,
                    )
                    .unwrap();
                assert!(result.failed.is_empty(), "{:?}", result.failed);
            }
        }
    });
    let wave = read_raw_value(&registry, "unit-001")["planning"]["wave"].clone();
    let shape =
        Shape::ByObject(serde_json::json!({ "id": "unit-001", "planning": { "wave": wave } }));
    assert_eq!(
        check_shape_outcome(&registry, "external value kept", &shape, true)
            .unwrap()
            .len(),
        1
    );
}

/// (k) Two instances in one process (`init` + `open`) writing alternately:
/// each sees the other's writes in filtered reads. A third instance without
/// the index (an older library, or `SCAI_REGISTRY_INDEX=off`) writes too:
/// its writes are external changes to the other two.
#[test]
fn git_sim_two_instances_write_alternately() {
    let dir = temp_dir();
    let first = init_git_registry(dir.path());
    let second = CodeUnitRegistry::open(dir.path()).unwrap();
    let without_index = CodeUnitRegistry::with_storage(
        dir.path().to_path_buf(),
        storage::Storage::open_without_index(&dir.path().join("registry")),
    );
    // (instance, whether its reads are served by the index)
    let instances = [(&first, true), (&second, true), (&without_index, false)];
    for (round, shape) in git_shapes().iter().enumerate() {
        let (writer, writer_indexed) = instances[round % 3];
        let (reader, reader_indexed) = instances[(round + 1) % 3];
        let id = git_id(round * 7 + 1);
        let wave = if round % 2 == 0 { 7 } else { 8 };
        writer
            .update(&id, &[("planning.wave", wave.into())], None)
            .unwrap();
        let mut unit = make_code_unit(
            &format!("added-{round:03}"),
            "EXTERNAL",
            CodeUnitObjectType::View,
        );
        set_dependency_ids(&mut unit, &[&id]);
        writer.create(&mut unit, None).unwrap();
        if round % 3 == 2 {
            writer.delete(&git_id(round * 7 + 2)).unwrap();
        }
        let label = format!("instances round {round}");
        let by_wave = Shape::Filtered(if wave == 7 {
            "planning.wave = 7"
        } else {
            "planning.wave IN (2, 8)"
        });
        let found = check_shape_outcome(reader, &label, &by_wave, reader_indexed).unwrap();
        assert!(
            found.iter().any(|u| u["id"] == id.as_str()),
            "{label}: {id} missing"
        );
        check_shape(reader, &label, shape, reader_indexed);
        check_shape(writer, &label, shape, writer_indexed);
        // The instance that neither wrote nor read yet this round.
        let (third, third_indexed) = instances[(round + 2) % 3];
        check_shape(third, &label, &by_wave, third_indexed);
    }
    check_update_where(&second, "second", "planning.wave = 7", true);
    check_update_where(&first, "first", "target.name = 'UPDATED'", true);
    check_update_where(&without_index, "without index", "planning.wave = 8", false);
    for shape in git_shapes() {
        check_shape(&first, "first settled", &shape, true);
        check_shape(&second, "second settled", &shape, true);
    }
}

/// (l) Strict-load errors introduced externally still fail filtered reads
/// (and `update_where` before it writes anything); fixing the file heals.
#[test]
fn git_sim_external_strict_load_errors() {
    let dir = temp_dir();
    let registry = init_git_registry(dir.path());
    let original = read_raw_text(&registry, "unit-020");
    let conflict = original.replacen(
        "\"wave\": 0",
        "<<<<<<< HEAD\n    \"wave\": 0\n=======\n    \"wave\": 7\n>>>>>>> feature",
        1,
    );
    assert_ne!(conflict, original);
    let mut future: serde_json::Value = serde_json::from_str(&original).unwrap();
    future[SCHEMA_VERSION_FIELD] = serde_json::json!(999);
    let future = serde_json::to_string_pretty(&future).unwrap();

    // (key, text): a merge conflict, a newer library's document, and a
    // copy-pasted file whose embedded id is another unit's.
    let corruptions = [
        ("unit-020", conflict.as_str()),
        ("unit-020", future.as_str()),
        ("unit-020-copy", original.as_str()),
    ];
    for (key, text) in corruptions {
        for (round, shape) in git_shapes().iter().enumerate() {
            let label = format!("{key} round {round}");
            write_raw(&registry, key, text);
            let broken = check_shape_outcome(&registry, &label, shape, true);
            assert!(
                broken.is_err(),
                "{label}: {}: the files-only read rejects it",
                shape.label()
            );
            if key == "unit-020" {
                write_raw(&registry, key, &original);
            } else {
                fs::remove_file(registry.storage.files().path_for(key)).unwrap();
            }
            assert!(check_shape_outcome(&registry, &format!("{label} fixed"), shape, true).is_ok());
        }
        write_raw(&registry, key, text);
        check_update_where(&registry, key, "planning.wave = 2", true);
        if key == "unit-020" {
            write_raw(&registry, key, &original);
        } else {
            fs::remove_file(registry.storage.files().path_for(key)).unwrap();
        }
        check_update_where(&registry, key, "planning.wave = 2", true);
    }
}

/// Many threads writing and reading one registry at once must not deadlock.
///
/// With `SCAI_REGISTRY_THREADS` set, operations run as jobs in a dedicated
/// pool, and a pool thread waiting inside one write can pick up another
/// queued operation. A writer that blocked on the write lock *inside* the
/// pool could then wait on a lock held further down its own stack, so
/// writers take the lock on the calling thread first. Run the suite with
/// `SCAI_REGISTRY_THREADS=2` to exercise the dedicated pool.
#[test]
fn concurrent_writers_and_readers_do_not_deadlock() {
    let dir = temp_dir();
    let registry = std::sync::Arc::new(CodeUnitRegistry::init(dir.path()).unwrap());
    let mut seed: Vec<CodeUnit> = (0..40)
        .map(|i| {
            make_code_unit(
                &format!("u{i:02}"),
                &format!("T{i}"),
                CodeUnitObjectType::Table,
            )
        })
        .collect();
    registry.create_batch(&mut seed, None).unwrap();

    let (done_tx, done_rx) = std::sync::mpsc::channel();
    let handles: Vec<_> = (0..8)
        .map(|t| {
            let registry = registry.clone();
            let done_tx = done_tx.clone();
            std::thread::spawn(move || {
                for round in 0..10 {
                    let id = format!("u{:02}", (t * 5 + round) % 40);
                    registry
                        .update(
                            &id,
                            &[("source.name", serde_json::json!(format!("R{t}-{round}")))],
                            None,
                        )
                        .unwrap();
                    let filter = format!("id = '{id}'");
                    let found = registry
                        .find_all(FindOptions {
                            filter: Some(&filter),
                            ..FindOptions::default()
                        })
                        .unwrap();
                    assert_eq!(found.len(), 1);
                    registry.find_all(FindOptions::default()).unwrap();
                }
                done_tx.send(()).unwrap();
            })
        })
        .collect();
    drop(done_tx);
    for _ in 0..handles.len() {
        done_rx
            .recv_timeout(std::time::Duration::from_secs(120))
            .expect("a writer/reader thread hung: possible lock deadlock");
    }
    for handle in handles {
        handle.join().unwrap();
    }
}

/// Registry calls made from another rayon pool's worker threads must not run
/// (or wait) by executing that pool's other jobs.
///
/// Each job lazily initializes one shared `OnceLock` with a registry query.
/// If the initializing worker waited by stealing — running the registry's
/// parallel work on the caller's pool, or `install`ing into a registry pool
/// from it — it could pick up a sibling job that re-enters the same
/// `OnceLock` on the same thread and deadlocks. Writers run alongside.
#[test]
fn calls_from_another_rayon_pool_do_not_reenter_its_jobs() {
    let dir = temp_dir();
    let registry = std::sync::Arc::new(CodeUnitRegistry::init(dir.path()).unwrap());
    let mut seed: Vec<CodeUnit> = (0..2000)
        .map(|i| {
            make_code_unit(
                &format!("u{i:04}"),
                &format!("T{i}"),
                CodeUnitObjectType::Table,
            )
        })
        .collect();
    registry.create_batch(&mut seed, None).unwrap();

    let (done_tx, done_rx) = std::sync::mpsc::channel();
    let registry_for_pool = registry.clone();
    std::thread::spawn(move || {
        let caller_pool = rayon::ThreadPoolBuilder::new()
            .num_threads(2)
            .build()
            .unwrap();
        let cell = std::sync::OnceLock::new();
        caller_pool.scope(|scope| {
            for job in 0..64 {
                let registry = &registry_for_pool;
                let cell = &cell;
                scope.spawn(move |_| {
                    if job % 8 == 0 {
                        let id = format!("u{:04}", job);
                        registry
                            .update(&id, &[("source.name", serde_json::json!("RENAMED"))], None)
                            .unwrap();
                    }
                    let count: &usize = cell
                        .get_or_init(|| registry.find_all(FindOptions::default()).unwrap().len());
                    assert_eq!(*count, 2000);
                    let found = registry
                        .find_all(FindOptions {
                            filter: Some("source.objectType = 'table'"),
                            fields: Some(&["id"]),
                            ..FindOptions::default()
                        })
                        .unwrap();
                    assert_eq!(found.len(), 2000);
                });
            }
        });
        done_tx.send(()).unwrap();
    });
    done_rx
        .recv_timeout(std::time::Duration::from_secs(120))
        .expect("registry calls from another rayon pool deadlocked");
}
