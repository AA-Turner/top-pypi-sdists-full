//! Schema version detection and document migration.
//!
//! Each code unit JSON file carries a `schemaVersion` integer. This module provides the migration
//! pipeline that upgrades old documents to [`CURRENT_SCHEMA_VERSION`] using `Value`-level transforms.
//! See [`versions`] for the step registry, migration kinds, and how to add new migrations.

mod versions;

use std::collections::{HashMap, HashSet};

use serde_json::Value;

use crate::error::*;

pub(crate) use versions::{
    PerFileSchemaMigrationFn, RegistryAwareSchemaMigrationFn, SchemaMigrationStep,
    SCHEMA_MIGRATION_STEPS,
};

/// JSON field name for the schema version indicator on every code unit document.
pub const SCHEMA_VERSION_FIELD: &str = "schemaVersion";

/// Current schema version. Must match `schemaVersion.const` in `schemas/code-unit.schema.json`.
/// Guarded by `test_version_constant_matches_schema`.
pub const CURRENT_SCHEMA_VERSION: i64 = 1;

/// Extract the schema version from a raw JSON document. Returns `Ok(version)` for valid integers
/// >= 1, `Ok(1)` when absent (missing = v1), or `Err(SchemaMigrationError)` when present but invalid.
pub fn extract_version(doc: &Value) -> Result<i64> {
    match doc.get(SCHEMA_VERSION_FIELD) {
        None => Ok(1),
        Some(v) => {
            let version = v.as_i64().ok_or_else(|| {
                schema_migration_err(format!(
                    "schemaVersion must be a positive integer, got: {}",
                    truncated_display(v),
                ))
            })?;
            if version < 1 {
                return Err(schema_migration_err(format!(
                    "schemaVersion must be >= 1, got: {version}"
                )));
            }
            Ok(version)
        }
    }
}

/// Migrate a document from its current version to [`CURRENT_SCHEMA_VERSION`]. Returns it unchanged
/// if already current. Errors: 1020 if newer than supported, 1021 if migration fails or chain is
/// incomplete, 1022 if a registry-aware step is required (use `migrate_schema_all` instead).
pub fn migrate(doc: Value) -> Result<Value> {
    migrate_with(doc, CURRENT_SCHEMA_VERSION, SCHEMA_MIGRATION_STEPS)
}

/// Like [`migrate`] but with an externally supplied step chain and target version.
/// Used by the per-file-only optimized path in `registry.rs`.
pub(crate) fn migrate_with(
    mut doc: Value,
    target_version: i64,
    migrations: &[(i64, SchemaMigrationStep)],
) -> Result<Value> {
    let version = extract_version(&doc)?;

    if version > target_version {
        return SchemaVersionNewerThanSupportedSnafu {
            document_version: version,
            supported_version: target_version,
        }
        .fail();
    }

    if version == target_version {
        return Ok(doc);
    }

    for &(from_ver, ref step) in migrations {
        if extract_version(&doc)? == from_ver {
            match step {
                SchemaMigrationStep::PerFile(f) => {
                    f(&mut doc).map_err(|e| {
                        schema_migration_err(format!("v{} to v{}: {e}", from_ver, from_ver + 1))
                    })?;
                    set_version(&mut doc, from_ver + 1)?;
                }
                SchemaMigrationStep::RegistryAware(_) => {
                    return RegistrySchemaMigrationRequiredSnafu {
                        document_version: from_ver,
                        target_version: from_ver + 1,
                    }
                    .fail();
                }
            }
        }
    }

    let final_version = extract_version(&doc)?;
    if final_version != target_version {
        return Err(schema_migration_err(format!(
            "Migration chain incomplete: document at v{version}, reached v{final_version}, \
             expected v{target_version}. Add missing migration functions.",
        )));
    }

    Ok(doc)
}

/// The sandbox passed to [`RegistryAwareSchemaMigrationFn`] during `migrate_schema_all`.
///
/// Holds every registry document as raw [`Value`]s (pre-migration, so not yet valid `CodeUnit`s).
/// Read access spans all documents; mutable access is restricted to "targets" — those at the
/// step's source version. On success the orchestrator bumps versions and writes to disk; on
/// failure everything is discarded and the caller can retry from on-disk state.
pub(crate) struct SchemaMigrationContext {
    docs: Vec<(String, Value)>,
    #[allow(dead_code)] // Used by migration functions (none registered yet)
    id_to_index: HashMap<String, usize>,
    #[allow(dead_code)] // Used by migration functions (none registered yet)
    target_ids: HashSet<String>,
}

impl SchemaMigrationContext {
    pub(crate) fn new(docs: Vec<(String, Value)>, target_ids: HashSet<String>) -> Self {
        let id_to_index = docs
            .iter()
            .enumerate()
            .map(|(idx, (id, _))| (id.clone(), idx))
            .collect();
        Self {
            docs,
            id_to_index,
            target_ids,
        }
    }

    // The following methods are the API for `RegistryAwareSchemaMigrationFn` authors.
    // Unused until a real registry-aware migration is registered.

    /// Look up any document by ID (read-only). Covers the full registry.
    #[allow(dead_code)]
    pub(crate) fn get(&self, id: &str) -> Option<&Value> {
        self.id_to_index.get(id).map(|&idx| &self.docs[idx].1)
    }

    /// Look up a target document by ID for mutation. Returns `None` for non-target IDs.
    #[allow(dead_code)]
    pub(crate) fn get_target_mut(&mut self, id: &str) -> Option<&mut Value> {
        if !self.target_ids.contains(id) {
            return None;
        }
        let idx = *self.id_to_index.get(id)?;
        Some(&mut self.docs[idx].1)
    }

    /// Iterate over all `(id, doc)` pairs (read-only).
    #[allow(dead_code)]
    pub(crate) fn iter(&self) -> impl Iterator<Item = (&str, &Value)> + '_ {
        self.docs.iter().map(|(id, v)| (id.as_str(), v))
    }

    /// Iterate over the IDs that are valid mutation targets for this step.
    #[allow(dead_code)]
    pub(crate) fn target_ids(&self) -> impl Iterator<Item = &str> + '_ {
        self.target_ids.iter().map(|id| id.as_str())
    }

    /// Total number of documents (targets + non-targets).
    #[allow(dead_code)]
    pub(crate) fn len(&self) -> usize {
        self.docs.len()
    }

    /// Consume the context and return the (potentially mutated) documents.
    pub(crate) fn into_inner(self) -> Vec<(String, Value)> {
        self.docs
    }
}

pub(crate) fn set_version(doc: &mut Value, version: i64) -> Result<()> {
    let obj = doc
        .as_object_mut()
        .ok_or_else(|| schema_migration_err("document root must be a JSON object".to_string()))?;
    obj.insert(SCHEMA_VERSION_FIELD.to_string(), Value::from(version));
    Ok(())
}

fn schema_migration_err(message: String) -> Error {
    SchemaMigrationSnafu {
        message,
        context: None,
    }
    .build()
}

fn truncated_display(v: &Value) -> String {
    let s = v.to_string();
    if s.len() > 50 {
        format!("{}...", &s[..50])
    } else {
        s
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_constant_matches_schema() {
        let schema_str = include_str!("../../schemas/code-unit.schema.json");
        let schema: Value = serde_json::from_str(schema_str).unwrap();
        let schema_version = schema["properties"][SCHEMA_VERSION_FIELD]["const"]
            .as_i64()
            .expect("schemaVersion.const must be an integer in the schema");
        assert_eq!(
            CURRENT_SCHEMA_VERSION, schema_version,
            "CURRENT_SCHEMA_VERSION ({CURRENT_SCHEMA_VERSION}) does not match \
             schema's schemaVersion.const ({schema_version}). Update the constant.",
        );
    }

    #[test]
    fn test_extract_version_present() {
        let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): 2});
        assert_eq!(extract_version(&doc).unwrap(), 2);
    }

    #[test]
    fn test_extract_version_missing_defaults_to_1() {
        let doc: Value = serde_json::json!({"id": "test"});
        assert_eq!(extract_version(&doc).unwrap(), 1);
    }

    #[test]
    fn test_extract_version_non_integer_rejects_with_error() {
        let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): "not_a_number"});
        let err = extract_version(&doc).unwrap_err();
        assert_eq!(err.error_code_i32(), 1021);
        assert!(err.to_string().contains("must be a positive integer"));
    }

    #[test]
    fn test_extract_version_float_rejects_with_error() {
        let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): 1.5});
        let err = extract_version(&doc).unwrap_err();
        assert_eq!(err.error_code_i32(), 1021);
    }

    #[test]
    fn test_extract_version_non_positive_rejects_with_error() {
        for &v in &[0, -5] {
            let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): v});
            let err = extract_version(&doc).unwrap_err();
            assert_eq!(err.error_code_i32(), 1021, "schemaVersion={v}");
            assert!(
                err.to_string().contains("must be >= 1"),
                "schemaVersion={v}"
            );
        }
    }

    #[test]
    fn test_migrate_current_version_is_noop() {
        let doc: Value =
            serde_json::json!({(SCHEMA_VERSION_FIELD): CURRENT_SCHEMA_VERSION, "id": "test"});
        let result = migrate(doc.clone()).unwrap();
        assert_eq!(result, doc);
    }

    #[test]
    fn test_migrate_future_version_rejected() {
        let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): CURRENT_SCHEMA_VERSION + 1});
        let err = migrate(doc).unwrap_err();
        assert_eq!(err.error_code_i32(), 1020);
        let msg = err.to_string();
        assert!(
            msg.contains("newer"),
            "error message should mention 'newer': {msg}"
        );
    }

    #[test]
    fn test_migrate_non_integer_version_rejected() {
        let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): "bad"});
        let err = migrate(doc).unwrap_err();
        assert_eq!(err.error_code_i32(), 1021);
    }

    #[test]
    fn test_migrate_non_positive_version_rejected() {
        for &v in &[0, -3] {
            let doc: Value = serde_json::json!({(SCHEMA_VERSION_FIELD): v});
            let err = migrate(doc).unwrap_err();
            assert_eq!(err.error_code_i32(), 1021, "schemaVersion={v}");
            assert!(
                err.to_string().contains("must be >= 1"),
                "schemaVersion={v}"
            );
        }
    }

    // ── Pipeline tests using test-only migration functions ─────────────
    //
    // Test schema versions:
    //   v1 → v2: adds "addedInV2": "hello"
    //   v2 → v3: renames "legacyField" → "renamedField"

    /// v1→v2: adds a new field.
    fn fake_v1_to_v2(doc: &mut Value) -> Result<()> {
        if let Some(obj) = doc.as_object_mut() {
            obj.insert("addedInV2".to_string(), Value::from("hello"));
        }
        Ok(())
    }

    /// v2→v3: renames a field.
    fn fake_v2_to_v3(doc: &mut Value) -> Result<()> {
        if let Some(obj) = doc.as_object_mut() {
            if let Some(old) = obj.remove("legacyField") {
                obj.insert("renamedField".to_string(), old);
            }
        }
        Ok(())
    }

    /// Always fails — used to test error propagation.
    fn fake_failing_migration(doc: &mut Value) -> Result<()> {
        let _ = doc;
        Err(schema_migration_err("simulated failure".to_string()))
    }

    use versions::SchemaMigrationStep;

    /// Full v1→v2→v3 chain.
    fn full_chain() -> &'static [(i64, SchemaMigrationStep)] {
        &[
            (1, SchemaMigrationStep::PerFile(fake_v1_to_v2)),
            (2, SchemaMigrationStep::PerFile(fake_v2_to_v3)),
        ]
    }

    /// Minimal document at a given schema version.
    fn doc_at_version(version: i64) -> Value {
        serde_json::json!({
            (SCHEMA_VERSION_FIELD): version,
            "id": "unit-1"
        })
    }

    /// v1 document with a field that v2→v3 will rename.
    fn v1_doc_with_legacy_field() -> Value {
        serde_json::json!({
            (SCHEMA_VERSION_FIELD): 1,
            "id": "unit-1",
            "legacyField": "keep-me"
        })
    }

    /// v1 document with extra fields to verify they survive migration.
    fn v1_doc_with_extra_fields() -> Value {
        serde_json::json!({
            (SCHEMA_VERSION_FIELD): 1,
            "id": "unit-1",
            "customData": {"nested": true},
            "tags": ["a", "b"]
        })
    }

    #[test]
    fn test_pipeline_single_step_v1_to_v2() {
        let doc = doc_at_version(1);

        let result =
            migrate_with(doc, 2, &[(1, SchemaMigrationStep::PerFile(fake_v1_to_v2))]).unwrap();

        assert_eq!(result[SCHEMA_VERSION_FIELD], 2);
        assert_eq!(result["addedInV2"], "hello");
        assert_eq!(result["id"], "unit-1");
    }

    #[test]
    fn test_pipeline_two_steps_v1_to_v3() {
        let doc = v1_doc_with_legacy_field();

        let result = migrate_with(doc, 3, full_chain()).unwrap();

        assert_eq!(result[SCHEMA_VERSION_FIELD], 3);
        assert_eq!(result["addedInV2"], "hello");
        assert_eq!(result["renamedField"], "keep-me");
        assert!(result.get("legacyField").is_none());
    }

    #[test]
    fn test_pipeline_starts_from_middle_version() {
        let doc = doc_at_version(2);

        let result = migrate_with(doc, 3, full_chain()).unwrap();

        assert_eq!(result[SCHEMA_VERSION_FIELD], 3);
        assert!(
            result.get("addedInV2").is_none(),
            "v1→v2 should not have run"
        );
    }

    #[test]
    fn test_pipeline_incomplete_chain_reports_error() {
        let doc = doc_at_version(1);

        let err =
            migrate_with(doc, 3, &[(1, SchemaMigrationStep::PerFile(fake_v1_to_v2))]).unwrap_err();

        assert_eq!(err.error_code_i32(), 1021);
        assert!(err.to_string().contains("Migration chain incomplete"));
        assert!(err.to_string().contains("reached v2"));
        assert!(err.to_string().contains("expected v3"));
    }

    #[test]
    fn test_pipeline_migration_failure_stops_chain() {
        let chain: &[(i64, SchemaMigrationStep)] = &[
            (1, SchemaMigrationStep::PerFile(fake_failing_migration)),
            (2, SchemaMigrationStep::PerFile(fake_v2_to_v3)),
        ];
        let doc = doc_at_version(1);

        let err = migrate_with(doc, 3, chain).unwrap_err();

        assert_eq!(err.error_code_i32(), 1021);
        assert!(err.to_string().contains("v1 to v2"));
        assert!(err.to_string().contains("simulated failure"));
    }

    #[test]
    fn test_pipeline_already_at_target_is_noop() {
        let doc = doc_at_version(2);

        let result = migrate_with(
            doc.clone(),
            2,
            &[(1, SchemaMigrationStep::PerFile(fake_v1_to_v2))],
        )
        .unwrap();

        assert_eq!(result, doc);
    }

    #[test]
    fn test_set_version_rejects_non_object_root() {
        let mut doc = Value::from("not-an-object");
        let err = set_version(&mut doc, 2).unwrap_err();
        assert_eq!(err.error_code_i32(), 1021);
        assert!(err.to_string().contains("must be a JSON object"));
    }

    #[test]
    fn test_pipeline_preserves_unrelated_fields() {
        let doc = v1_doc_with_extra_fields();

        let result = migrate_with(doc, 3, full_chain()).unwrap();

        assert_eq!(result["customData"]["nested"], true);
        assert_eq!(result["tags"][0], "a");
        assert_eq!(result["tags"][1], "b");
    }

    // ── Registry-aware step: error 1022 from single-document path ──────

    fn fake_registry_aware_noop(_ctx: &mut SchemaMigrationContext) -> Result<()> {
        Ok(())
    }

    #[test]
    fn test_migrate_with_registry_aware_step_returns_error_1022() {
        let chain: &[(i64, SchemaMigrationStep)] = &[(
            1,
            SchemaMigrationStep::RegistryAware(fake_registry_aware_noop),
        )];
        let doc = doc_at_version(1);

        let err = migrate_with(doc, 2, chain).unwrap_err();

        assert_eq!(err.error_code_i32(), 1022);
        let msg = err.to_string();
        assert!(
            msg.contains("registry-aware migration"),
            "error message should mention registry-aware: {msg}"
        );
        assert!(
            msg.contains("migrate_schema_all()"),
            "error message should suggest migrate_schema_all(): {msg}"
        );
    }

    #[test]
    fn test_migrate_with_per_file_then_registry_aware_errors_at_registry_step() {
        let chain: &[(i64, SchemaMigrationStep)] = &[
            (1, SchemaMigrationStep::PerFile(fake_v1_to_v2)),
            (
                2,
                SchemaMigrationStep::RegistryAware(fake_registry_aware_noop),
            ),
        ];
        let doc = doc_at_version(1);

        let err = migrate_with(doc, 3, chain).unwrap_err();

        assert_eq!(err.error_code_i32(), 1022);
        let details = err.details().expect("should have details");
        assert_eq!(details["documentVersion"], 2);
        assert_eq!(details["targetVersion"], 3);
    }

    #[test]
    fn test_migrate_with_registry_aware_skipped_when_already_past() {
        let chain: &[(i64, SchemaMigrationStep)] = &[(
            1,
            SchemaMigrationStep::RegistryAware(fake_registry_aware_noop),
        )];
        let doc = doc_at_version(2);

        let result = migrate_with(doc.clone(), 2, chain).unwrap();
        assert_eq!(result, doc);
    }

    // ── SchemaMigrationContext tests ───────────────────────────────────

    fn make_context_docs() -> Vec<(String, Value)> {
        vec![
            (
                "a".to_string(),
                serde_json::json!({(SCHEMA_VERSION_FIELD): 1, "id": "a", "data": "alpha"}),
            ),
            (
                "b".to_string(),
                serde_json::json!({(SCHEMA_VERSION_FIELD): 1, "id": "b", "data": "bravo"}),
            ),
            (
                "c".to_string(),
                serde_json::json!({(SCHEMA_VERSION_FIELD): 2, "id": "c", "data": "charlie"}),
            ),
        ]
    }

    #[test]
    fn test_schema_migration_context_get_and_get_target_mut() {
        let target_ids: HashSet<String> = ["a".to_string(), "b".to_string()].into();
        let mut ctx = SchemaMigrationContext::new(make_context_docs(), target_ids);

        assert_eq!(ctx.get("a").unwrap()["data"], "alpha");
        assert_eq!(ctx.get("b").unwrap()["data"], "bravo");
        assert_eq!(ctx.get("c").unwrap()["data"], "charlie");
        assert!(ctx.get("nonexistent").is_none());

        let a_mut = ctx.get_target_mut("a").unwrap();
        a_mut["data"] = Value::from("modified-alpha");
        assert_eq!(ctx.get("a").unwrap()["data"], "modified-alpha");

        assert!(
            ctx.get_target_mut("c").is_none(),
            "non-target documents must not be mutable"
        );
    }

    #[test]
    fn test_schema_migration_context_iter() {
        let target_ids: HashSet<String> = ["a".to_string()].into();
        let ctx = SchemaMigrationContext::new(make_context_docs(), target_ids);

        let pairs: Vec<(&str, &Value)> = ctx.iter().collect();
        assert_eq!(pairs.len(), 3);

        let ids: Vec<&str> = pairs.iter().map(|(id, _)| *id).collect();
        assert!(ids.contains(&"a"));
        assert!(ids.contains(&"b"));
        assert!(ids.contains(&"c"));
    }

    #[test]
    fn test_schema_migration_context_non_target_mutation_blocked() {
        let target_ids: HashSet<String> = ["a".to_string()].into();
        let mut ctx = SchemaMigrationContext::new(make_context_docs(), target_ids);

        assert!(ctx.get_target_mut("b").is_none());
        assert!(ctx.get_target_mut("c").is_none());

        let a_doc = ctx.get_target_mut("a").unwrap();
        a_doc["mutated"] = Value::from(true);

        let docs = ctx.into_inner();
        let b_doc = docs.iter().find(|(id, _)| id == "b").unwrap();
        assert!(
            b_doc.1.get("mutated").is_none(),
            "non-target document 'b' must not be modified"
        );
        let c_doc = docs.iter().find(|(id, _)| id == "c").unwrap();
        assert!(
            c_doc.1.get("mutated").is_none(),
            "non-target document 'c' must not be modified"
        );
    }

    #[test]
    fn test_schema_migration_context_target_ids() {
        let target_ids: HashSet<String> = ["a".to_string(), "b".to_string()].into();
        let ctx = SchemaMigrationContext::new(make_context_docs(), target_ids);

        let mut tids: Vec<&str> = ctx.target_ids().collect();
        tids.sort();
        assert_eq!(tids, vec!["a", "b"]);
    }

    #[test]
    fn test_schema_migration_context_into_inner_round_trip() {
        let target_ids: HashSet<String> = ["a".to_string()].into();
        let original_docs = make_context_docs();
        let ctx = SchemaMigrationContext::new(original_docs.clone(), target_ids);

        let restored = ctx.into_inner();
        assert_eq!(restored.len(), original_docs.len());
        for (i, (id, doc)) in restored.iter().enumerate() {
            assert_eq!(id, &original_docs[i].0);
            assert_eq!(doc, &original_docs[i].1);
        }
    }
}
