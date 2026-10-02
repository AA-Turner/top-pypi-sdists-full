//! Individual migration functions, one per schema version transition.
//!
//! Each migration lives in its own file (`v{N}_to_v{N+1}.rs`) and is registered
//! as a [`SchemaMigrationStep`] in [`SCHEMA_MIGRATION_STEPS`].
//!
//! ## Adding a migration
//!
//! 1. Freeze the current schema to `schemas/history/code-unit.v{N}.schema.json` (**before** editing).
//! 2. Create `migration/versions/v{N}_to_v{N+1}.rs` with a `pub fn migrate(...)`.
//! 3. Add `mod v{N}_to_v{N+1};` below and append to [`SCHEMA_MIGRATION_STEPS`].
//! 4. Bump [`CURRENT_SCHEMA_VERSION`](super::CURRENT_SCHEMA_VERSION).
//!
//! For per-file steps, the signature is `fn(&mut Value) -> Result<()>`.
//! For registry-aware steps, use `fn(&mut SchemaMigrationContext) -> Result<()>` — do NOT
//! set `schemaVersion` (the orchestrator bumps it), and keep the function a pure transform
//! (no IO). Each version transition is exactly one kind; split into two bumps if you need both.

use serde_json::Value;

use super::SchemaMigrationContext;
use crate::error::*;

/// Single-document migration. Runs in parallel via rayon.
#[allow(dead_code)]
pub(crate) type PerFileSchemaMigrationFn = fn(&mut Value) -> Result<()>;

/// Cross-document migration via [`SchemaMigrationContext`]. Runs sequentially; on failure
/// all in-memory changes are discarded so the caller can retry from on-disk state.
#[allow(dead_code)]
pub(crate) type RegistryAwareSchemaMigrationFn = fn(&mut SchemaMigrationContext) -> Result<()>;

/// Prefer `PerFile` (parallel, no full-registry load). Use `RegistryAware` only when a step
/// must read or mutate across documents (e.g. denormalization, cross-references).
#[allow(dead_code)]
pub(crate) enum SchemaMigrationStep {
    PerFile(PerFileSchemaMigrationFn),
    RegistryAware(RegistryAwareSchemaMigrationFn),
}

// ── Migration modules ──────────────────────────────────────────────────
// mod v1_to_v2;

/// Ordered migration chain. Each entry is `(from_version, migration)`.
/// A migration from version N always produces version N+1.
pub(crate) const SCHEMA_MIGRATION_STEPS: &[(i64, SchemaMigrationStep)] = &[
    // (1, SchemaMigrationStep::PerFile(v1_to_v2::migrate)),
];
