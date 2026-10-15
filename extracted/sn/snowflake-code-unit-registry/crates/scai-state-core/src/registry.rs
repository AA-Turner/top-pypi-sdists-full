//! Code Unit Registry – file operations for the code unit registry
//!
//! CodeUnit files are stored flat in `./registry/{id}.json` where id is a UUID v4.

use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};

use rayon::prelude::*;
use serde_json::Value;

use crate::checksum::{
    apply_checksums, find_sql_file_changes, validate_checksum_report, ChecksumMode,
    ChecksumValidationReport, SourceCodeChanges,
};
use crate::dependency_view;
use crate::error::*;
use crate::filter::Filter;
use crate::generated::types::CodeUnit;
use snafu::IntoError;

mod graph;
mod in_memory;
mod loader;
pub(crate) mod paths;
mod pushdown;
mod query;
pub(crate) mod storage;
#[cfg(test)]
pub(crate) mod test_helpers;
#[cfg(test)]
pub(crate) mod test_hooks;
mod threads;
use in_memory::InMemoryRegistry;
use storage::index::Prefilter;
pub use storage::{LockGuard, INDEX_ENV_VAR};
use storage::{Storage, StorageWrite};
pub use threads::THREADS_ENV_VAR;

/// ID placeholder used in batch operations when a code unit has no ID.
pub const UNKNOWN_ID: &str = "unknown";

/// Subdirectory name where code unit JSON files are stored.
const REGISTRY_DIR: &str = "registry";

/// The kind of write operation that triggered a lifecycle hook.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ChangeType {
    Create,
    Update,
    Upsert,
    Delete,
}

/// A pending write operation with before/after snapshots.
///
/// Hooks receive a mutable slice of these and may transform the `after`
/// field before the data is persisted:
/// - `Some(unit)` in `after` → write this unit to disk
/// - `None` in `after` → no unit should exist on disk for this ID
///   (delete the file if it existed, or skip the create)
#[derive(Debug, Clone)]
pub(crate) struct CodeUnitChange {
    pub(crate) id: String,
    /// Snapshot of the unit before this operation (`None` for creates).
    pub(crate) before: Option<CodeUnit>,
    /// The intended new disk state. Hooks may modify this.
    pub(crate) after: Option<CodeUnit>,
}

/// Options passed to every write operation and forwarded to hooks.
#[derive(Debug, Clone, Copy, Default)]
pub struct WriteOptions {
    pub checksum_mode: ChecksumMode,
}

/// Before-persist hook for registry write operations.
///
/// Hooks are chained: each receives the previous hook's output. They may
/// transform, filter, or append [`CodeUnitChange`] entries. If a hook
/// returns `Err`, the operation is aborted and nothing is written to disk.
pub(crate) trait RegistryHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        Ok(changes)
    }
}

/// Built-in hook that recomputes file checksums based on [`WriteOptions::checksum_mode`].
/// Runs first so downstream hooks see the final checksum values.
pub(crate) struct ChecksumHook;

impl RegistryHook for ChecksumHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        registry: &CodeUnitRegistry,
        options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        if options.checksum_mode.is_none() {
            return Ok(changes);
        }
        let mut result = changes;
        for change in &mut result {
            if let Some(unit) = &mut change.after {
                apply_checksums(unit, &options.checksum_mode, &registry.root)?;
            }
        }
        Ok(result)
    }
}

/// Built-in hook that recomputes dependency-derived fields (topological
/// rank, `requiredBy`, `isMissing`, `hasTransitiveMissingDependencies`)
/// purely in-memory, appending extra [`CodeUnitChange`] entries for any
/// units whose derived fields changed.
///
/// Uses **scoped refresh** when possible: only nodes reachable from the
/// changed units' dependency edges are recomputed. Falls back to a full
/// refresh when any seed unit has `planning == None` (meaning `requiredBy`
/// is not populated yet and upward traversal cannot be trusted).
pub(crate) struct DependencyRefreshHook;

impl DependencyRefreshHook {
    /// Extract dependency edge IDs from a unit for seeding the graph refresh.
    fn dependency_seeds(unit: &CodeUnit) -> Vec<String> {
        dependency_view::dep_blocks(unit)
            .flat_map(|d| {
                d.depends_on
                    .iter()
                    .filter_map(|dep| dep.id.clone())
                    .chain(d.required_by.iter().cloned())
            })
            .collect()
    }

    /// Apply incoming changes to the in-memory store and collect seed IDs
    /// for the graph refresh. Returns a position index mapping change IDs
    /// to their slot in the result vec.
    fn apply_changes(
        changes: &[CodeUnitChange],
        in_memory: &mut InMemoryRegistry,
    ) -> (std::collections::HashMap<String, usize>, Vec<String>) {
        let mut id_to_pos = std::collections::HashMap::new();
        let mut seed_ids = Vec::new();

        for (i, c) in changes.iter().enumerate() {
            seed_ids.push(c.id.clone());

            if let Some(before) = &c.before {
                seed_ids.extend(Self::dependency_seeds(before));
            }
            if let Some(after) = &c.after {
                seed_ids.extend(Self::dependency_seeds(after));
            }

            if let Some(mem_idx) = in_memory.id_to_index(&c.id) {
                match &c.after {
                    Some(unit) => *in_memory.unit_mut(mem_idx) = unit.clone(),
                    None => in_memory.remove_unit(&c.id),
                }
            } else if let Some(unit) = &c.after {
                in_memory.add_unit(unit.clone());
            }
            id_to_pos.insert(c.id.clone(), i);
        }

        (id_to_pos, seed_ids)
    }

    /// Run a scoped or full graph refresh depending on whether all seed
    /// units have `planning` populated.
    fn refresh_graph(seed_ids: &[String], in_memory: &mut InMemoryRegistry) -> Result<Vec<usize>> {
        let needs_full = seed_ids
            .iter()
            .filter_map(|id| in_memory.id_to_index(id))
            .any(|i| in_memory.unit(i).planning.is_none());

        if needs_full {
            in_memory.graph().refresh(false)
        } else {
            let seeds: Vec<usize> = seed_ids
                .iter()
                .filter_map(|id| in_memory.id_to_index(id))
                .collect();
            in_memory.graph().refresh_scoped(&seeds, false)
        }
    }

    /// Merge graph-refreshed units back into the change set.
    ///
    /// Units already in the change set get their `after` updated in place.
    /// Transitively dirtied units are appended with `before` from the
    /// pre-refresh snapshot so downstream hooks see an accurate diff.
    fn merge_refreshed(
        mut result: Vec<CodeUnitChange>,
        id_to_pos: &mut std::collections::HashMap<String, usize>,
        dirty: &[usize],
        in_memory: &InMemoryRegistry,
        pre_refresh: &[CodeUnit],
    ) -> Vec<CodeUnitChange> {
        for &i in dirty {
            let refreshed = in_memory.unit(i);
            let Some(id) = refreshed.id.clone() else {
                continue;
            };
            match id_to_pos.get(&id) {
                Some(&pos) => {
                    if let Some(ref mut after) = result[pos].after {
                        *after = refreshed.clone();
                    }
                }
                None => {
                    let before = pre_refresh.get(i).cloned();
                    id_to_pos.insert(id.clone(), result.len());
                    result.push(CodeUnitChange {
                        id,
                        before,
                        after: Some(refreshed.clone()),
                    });
                }
            }
        }
        result
    }
}

impl RegistryHook for DependencyRefreshHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        let mut in_memory = InMemoryRegistry::build(registry)?;
        let (mut id_to_pos, seed_ids) = Self::apply_changes(&changes, &mut in_memory);

        let pre_refresh = in_memory.snapshot_units();
        let dirty = Self::refresh_graph(&seed_ids, &mut in_memory)?;

        Ok(Self::merge_refreshed(
            changes,
            &mut id_to_pos,
            &dirty,
            &in_memory,
            &pre_refresh,
        ))
    }
}

/// Built-in hook that sets `updatedAt` timestamps on parent objects
/// whose sibling fields have changed.
///
/// Parent paths are discovered at build time from the JSON Schema
/// (see `generated::updated_at_paths::UPDATED_AT_PARENT_PATHS`).
/// For each path, if any sibling field (excluding `updatedAt` itself)
/// differs between `before` and `after`, the hook writes the current
/// UTC time in ISO 8601 Zulu format (e.g. `2026-03-09T04:58:19Z`).
pub(crate) struct UpdatedAtHook;

impl UpdatedAtHook {
    /// Compare two parent objects excluding the `updatedAt` key.
    /// Returns `true` if any sibling field differs.
    fn siblings_changed(before_parent: Option<&Value>, after_parent: &Value) -> bool {
        let Some(before) = before_parent else {
            return true;
        };

        let (Some(before_obj), Some(after_obj)) = (before.as_object(), after_parent.as_object())
        else {
            return before != after_parent;
        };

        let all_keys: std::collections::HashSet<&String> = before_obj
            .keys()
            .chain(after_obj.keys())
            .filter(|k| k.as_str() != "updatedAt")
            .collect();

        for key in all_keys {
            if before_obj.get(key) != after_obj.get(key) {
                return true;
            }
        }
        false
    }

    fn now_zulu() -> String {
        chrono::Utc::now().to_rfc3339_opts(chrono::SecondsFormat::Secs, true)
    }
}

impl RegistryHook for UpdatedAtHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        use crate::generated::updated_at_paths::UPDATED_AT_PARENT_PATHS;

        let mut result = changes;
        let now = Self::now_zulu();

        for change in &mut result {
            let Some(after) = &change.after else {
                continue;
            };

            let before_json = change
                .before
                .as_ref()
                .map(serde_json::to_value)
                .transpose()?;
            let mut after_json = serde_json::to_value(after)?;

            let mut modified = false;
            for path in UPDATED_AT_PARENT_PATHS {
                let after_parent = paths::navigate_path(&after_json, path);

                let parent_exists_in_after = after_parent
                    .is_some_and(|v| v.is_object() && !v.as_object().unwrap().is_empty());

                if !parent_exists_in_after {
                    continue;
                }

                let before_parent = before_json
                    .as_ref()
                    .and_then(|bj| paths::navigate_path(bj, path));

                if Self::siblings_changed(before_parent, after_parent.unwrap()) {
                    if let Some(parent_mut) = paths::ensure_path(&mut after_json, path) {
                        if let Some(obj) = parent_mut.as_object_mut() {
                            obj.insert("updatedAt".to_string(), Value::String(now.clone()));
                            modified = true;
                        }
                    }
                }
            }

            if modified {
                change.after = Some(serde_json::from_value(after_json)?);
            }
        }

        Ok(result)
    }
}

/// Built-in hook that normalizes file path fields to UNIX-style forward
/// slashes. Runs first in the chain so downstream hooks (checksums, etc.)
/// see canonical paths.
pub(crate) struct PathNormalizationHook;

impl RegistryHook for PathNormalizationHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        let mut result = changes;
        for change in &mut result {
            if let Some(unit) = &mut change.after {
                paths::normalize_code_unit_paths(unit);
            }
        }
        Ok(result)
    }
}

/// Options for `find_all` queries.
#[derive(Debug, Clone, Copy, Default)]
pub struct FindOptions<'a> {
    /// Optional SQL-like filter expression.
    pub filter: Option<&'a str>,
    /// Optional field projection list (dot paths, e.g. `"source.name"`).
    ///
    /// Without a `filter`, a projected read decodes only the top-level keys
    /// the projection needs: every document is still checked for JSON
    /// syntax, `schemaVersion`, and id/key match, but a type error in a
    /// field *outside* the projection no longer fails the read.
    pub fields: Option<&'a [&'a str]>,
    /// When true and a filter is active, include transitive dependencies
    /// of matching units even if they do not match the filter.
    pub include_dependencies: bool,
    /// Literal token → replacement-value map applied to `source.*` and
    /// `target.*` string slots of returned code units.
    ///
    /// CUR is grammar-agnostic: it does not parse `${...}` / `<% ... %>`
    /// or any other wrapper. Whatever string the caller puts in a key is
    /// matched verbatim. Substitution is single-pass — replacement values
    /// are not re-scanned. `dependsOn[].id` and stored data are never
    /// mutated; substitution happens in-memory after projection.
    pub bindings: Option<&'a HashMap<String, String>>,
    /// Path to a `database-bindings.yml`; the read resolves it and returns bound
    /// units, so a caller passes a path instead of parsing and wrapping itself.
    ///
    /// Equivalent to passing [`crate::DatabaseBindings::token_map`] as `bindings`:
    /// both sides at once, which is unambiguous because `${NAME}` and `<%NAME%>`
    /// are disjoint grammars. Parse and IO failures surface from the read instead
    /// of having to be handled in every caller.
    ///
    /// Mutually exclusive with `bindings` — supplying both is an error rather than
    /// a silent precedence rule.
    ///
    /// Two limits, stated because the failure mode is silence:
    /// * it uses the default `${NAME}` source grammar, so a conversion that wrote
    ///   a customer-specific source wrapper still needs the explicit `bindings`
    ///   map — `apply_bindings` leaves an unmatched token alone, so that gap would
    ///   not announce itself;
    /// * a bound read also rewrites `target.name` / `target.canonical_name`, so a
    ///   caller deriving a frozen identity from those — a baseline key, a stage
    ///   path, an on-disk layout — must read **unbound** for that call. The
    ///   convenience does not change that hazard, only how easily it is reached.
    pub bindings_path: Option<&'a Path>,
}

/// Convert dot-notation path to JSON Pointer (RFC 6901)
/// e.g., "source.name" -> "/source/name"
fn to_json_pointer(dot_path: &str) -> String {
    format!("/{}", dot_path.replace('.', "/"))
}

/// Set a value at a dot-notation path, creating intermediate objects as needed.
/// Returns Err if an intermediate segment exists but is not an object.
fn set_path(root: &mut Value, path: &str, val: Value) -> Result<()> {
    let parts: Vec<&str> = path.split('.').collect();
    let mut current = root;

    for part in &parts[..parts.len() - 1] {
        if !current.is_object() {
            return ValidationSnafu {
                message: format!(
                    "Cannot set path '{}': intermediate value is not an object",
                    path
                ),
            }
            .fail();
        }
        current = current
            .as_object_mut()
            .unwrap()
            .entry(*part)
            .or_insert_with(|| Value::Object(serde_json::Map::new()));
    }

    let leaf = parts.last().unwrap();
    match current.as_object_mut() {
        Some(obj) => {
            obj.insert(leaf.to_string(), val);
            Ok(())
        }
        None => ValidationSnafu {
            message: format!("Cannot set path '{}': parent is not an object", path),
        }
        .fail(),
    }
}

/// Project a unit to `fields` (see [`project_fields`]).
fn project_unit(unit: &CodeUnit, fields: &[&str]) -> Result<CodeUnit> {
    let json_value = serde_json::to_value(unit)?;
    let projected = project_fields(&json_value, fields)?;
    Ok(serde_json::from_value(projected)?)
}

/// Project specified fields from a JSON value into a new object.
/// Supports nested paths like "source.name".
fn project_fields(value: &Value, fields: &[&str]) -> Result<Value> {
    let mut result = Value::Object(serde_json::Map::new());

    for field in fields {
        if let Some(v) = value.pointer(&to_json_pointer(field)) {
            set_path(&mut result, field, v.clone())?;
        }
    }

    Ok(result)
}

/// Check if all fields present in `partial` match the corresponding fields in `target`.
/// For objects, recurse into nested keys. For all other types, require exact equality.
fn matches_partial(partial: &Value, target: &Value) -> bool {
    match (partial, target) {
        (Value::Object(partial_map), Value::Object(target_map)) => {
            for (key, partial_val) in partial_map {
                match target_map.get(key) {
                    Some(target_val) => {
                        if !matches_partial(partial_val, target_val) {
                            return false;
                        }
                    }
                    None => return false,
                }
            }
            true
        }
        _ => partial == target,
    }
}

/// Deep-merge `patch` into `base`.
/// For objects, recursively merge keys. For all other types, `patch` wins.
fn deep_merge(base: &mut Value, patch: &Value) {
    match (base, patch) {
        (Value::Object(base_map), Value::Object(patch_map)) => {
            for (key, patch_val) in patch_map {
                let entry = base_map.entry(key.clone()).or_insert_with(|| Value::Null);
                deep_merge(entry, patch_val);
            }
        }
        (base, patch) => {
            *base = patch.clone();
        }
    }
}

/// Always use LF line endings in registry JSON files for cross-platform consistency.
const LINE_ENDING: &str = "\n";

/// RAII guard that records the current thread as running hooks and clears
/// it on drop — even if the guarded scope panics.
struct HookGuard<'a>(&'a HookThread);

impl<'a> HookGuard<'a> {
    fn enter(slot: &'a HookThread) -> Self {
        *slot.lock().unwrap_or_else(|p| p.into_inner()) = Some(std::thread::current().id());
        Self(slot)
    }
}

impl Drop for HookGuard<'_> {
    fn drop(&mut self) {
        *self.0.lock().unwrap_or_else(|p| p.into_inner()) = None;
    }
}

/// The thread currently running this registry's before-persist hooks, if any.
type HookThread = std::sync::Mutex<Option<std::thread::ThreadId>>;

/// Built-in hook that computes `canonicalName` on both `source` and `target`
/// metadata before persisting, delegating to [`crate::canonical_name`].
pub(crate) struct CanonicalNameHook;

impl RegistryHook for CanonicalNameHook {
    fn before_persist(
        &self,
        _kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        _registry: &CodeUnitRegistry,
        _options: &WriteOptions,
    ) -> Result<Vec<CodeUnitChange>> {
        use crate::canonical_name::{self, Side};
        let mut result = changes;
        for change in &mut result {
            let Some(unit) = &mut change.after else {
                continue;
            };
            let source_cn = canonical_name::for_code_unit(unit, Side::Source);
            let target_cn = canonical_name::for_code_unit(unit, Side::Target);
            if let Some(source) = &mut unit.source {
                source.canonical_name = source_cn;
            }
            if let Some(target) = &mut unit.target {
                target.canonical_name = target_cn;
            }
        }
        Ok(result)
    }
}

/// The ordered set of built-in hooks that run on every write operation.
///
/// Order matters: PathNormalizationHook first (so downstream hooks see
/// canonical paths), ChecksumHook second (so checksums are based on
/// resolved paths), then DependencyRefreshHook, CanonicalNameHook,
/// then UpdatedAtHook last.
fn builtin_hooks() -> Vec<Box<dyn RegistryHook + Send + Sync>> {
    vec![
        Box::new(PathNormalizationHook),
        Box::new(ChecksumHook),
        Box::new(DependencyRefreshHook),
        Box::new(CanonicalNameHook),
        Box::new(UpdatedAtHook),
    ]
}

/// A code-unit registry rooted at a project directory.
pub struct CodeUnitRegistry {
    /// Root path of the registry (contains registry/)
    root: PathBuf,
    /// Backend holding the code unit documents.
    storage: Storage,
    /// Before-write hooks that fire before data is persisted.
    hooks: Vec<Box<dyn RegistryHook + Send + Sync>>,
    /// Re-entrancy guard: prevents write methods from being called inside
    /// hooks (on the thread running them).
    in_hook: HookThread,
}

impl CodeUnitRegistry {
    /// Returns `true` if a registry directory structure exists at the given path.
    pub fn exists(path: impl AsRef<Path>) -> bool {
        path.as_ref().join(REGISTRY_DIR).exists()
    }

    /// Initialize a new registry at the given path.
    /// Creates the registry directory structure.
    pub fn init(path: impl AsRef<Path>) -> Result<Self> {
        let root = path.as_ref().to_path_buf();

        if Self::exists(&root) {
            return RegistryAlreadyExistsSnafu {
                path: root.display().to_string(),
            }
            .fail();
        }

        let registry_dir = root.join(REGISTRY_DIR);
        fs::create_dir_all(&registry_dir)?;
        fs::create_dir_all(registry_dir.join(".locks"))?;

        let gitignore = registry_dir.join(".gitignore");
        let gitignore_content = format!(".locks/{}", LINE_ENDING);
        fs::write(&gitignore, gitignore_content)?;

        let storage = Storage::open(&registry_dir)?;
        Ok(Self::with_storage(root, storage))
    }

    /// Open an existing registry at the given path.
    pub fn open(path: impl AsRef<Path>) -> Result<Self> {
        let root = path.as_ref().to_path_buf();

        if !Self::exists(&root) {
            return RegistryNotFoundSnafu {
                path: root.display().to_string(),
            }
            .fail();
        }

        let storage = Storage::open(&root.join(REGISTRY_DIR))?;
        Ok(Self::with_storage(root, storage))
    }

    fn with_storage(root: PathBuf, storage: Storage) -> Self {
        Self {
            root,
            storage,
            hooks: builtin_hooks(),
            in_hook: HookThread::default(),
        }
    }

    /// How many reads on this instance were answered from the SQLite index
    /// rather than the files. A diagnostic for benchmarks, which must not
    /// time the files-only fallback while labelled "index on"; not part of
    /// the stable API and not exposed to the bindings.
    #[doc(hidden)]
    pub fn index_reads_served(&self) -> u64 {
        self.storage.index_reads()
    }

    /// Get the root path of the registry
    pub fn root(&self) -> &Path {
        &self.root
    }

    /// Get the source directory path (`root/source`).
    pub fn source_dir(&self) -> PathBuf {
        self.root.join("source")
    }

    /// Get the snowflake (converted output) directory path (`root/snowflake`).
    pub fn snowflake_dir(&self) -> PathBuf {
        self.root.join("snowflake")
    }

    /// Acquire an exclusive lock for write operations.
    pub fn acquire_lock(&self) -> Result<LockGuard> {
        self.storage.lock()
    }

    // ── Hooks ────────────────────────────────────────────────────────────

    #[cfg(test)]
    fn add_hook(&mut self, hook: impl RegistryHook + Send + Sync + 'static) {
        self.hooks.push(Box::new(hook));
    }

    /// Reject a write issued from inside this registry's hooks *on the hook
    /// thread itself* (it would wait forever on the lock its caller holds).
    /// Other threads writing concurrently are fine: they queue on the lock.
    fn guard_reentrant(&self) -> Result<()> {
        let hook_thread = *self.in_hook.lock().unwrap_or_else(|p| p.into_inner());
        if hook_thread == Some(std::thread::current().id()) {
            return HookReentrantSnafu.fail();
        }
        Ok(())
    }

    /// Run all registered hooks in order, allowing each to inspect and
    /// transform the change set. Hooks may append additional changes for
    /// units affected by side effects (e.g. transitive dependency updates),
    /// so the returned vec can be larger than the input.
    fn fire_before_persist(
        &self,
        kind: ChangeType,
        changes: Vec<CodeUnitChange>,
        options: Option<&WriteOptions>,
    ) -> Result<Vec<CodeUnitChange>> {
        let default_opts = WriteOptions::default();
        let options = options.unwrap_or(&default_opts);
        let _guard = HookGuard::enter(&self.in_hook);
        self.hooks.iter().try_fold(changes, |acc, hook| {
            hook.before_persist(kind, acc, self, options)
        })
    }

    fn persist_changes(&self, lock: &LockGuard, changes: &[CodeUnitChange]) -> Result<()> {
        for outcome in self.persist_units(lock, &Self::change_items(changes), true) {
            outcome?;
        }
        self.sync()
    }

    fn persist_changes_batch(
        &self,
        lock: &LockGuard,
        changes: &[CodeUnitChange],
        result: &mut BatchResult,
    ) {
        let outcomes = self.persist_units(lock, &Self::change_items(changes), true);
        for (change, outcome) in changes.iter().zip(outcomes) {
            match outcome {
                Ok(()) => result.success(change.id.clone()),
                Err(e) => result.failure(change.id.clone(), &e),
            }
        }
        if let Err(e) = self.sync() {
            result.failure("_sync".to_string(), &e);
        }
    }

    fn change_items(changes: &[CodeUnitChange]) -> Vec<(&str, Option<&CodeUnit>)> {
        changes
            .iter()
            .map(|c| (c.id.as_str(), c.after.as_ref()))
            .collect()
    }

    /// Write (`Some`) or delete (`None`) each unit, returning one outcome per
    /// item in input order. Does not sync.
    ///
    /// Each written unit is deep-merged on top of the document currently
    /// stored under its ID, so fields present in storage but absent from the
    /// `CodeUnit` struct (e.g. fields added by a newer schema version)
    /// survive the round-trip.
    fn persist_units(
        &self,
        lock: &LockGuard,
        items: &[(&str, Option<&CodeUnit>)],
        durable: bool,
    ) -> Vec<Result<()>> {
        let put_ids: Vec<String> = items
            .iter()
            .filter(|(_, unit)| unit.is_some())
            .map(|(id, _)| (*id).to_string())
            .collect();
        let mut stored = self.storage.read_many(&put_ids).into_iter();
        let stored: Vec<Option<String>> = items
            .iter()
            .map(|(_, unit)| unit.and_then(|_| stored.next().and_then(|raw| raw.ok().flatten())))
            .collect();

        let values: Vec<Result<Option<Value>>> = items
            .par_iter()
            .zip(stored.into_par_iter())
            .map(|((_, unit), raw)| unit.map(|u| merge_onto_stored(u, raw)).transpose())
            .collect();

        let writes: Vec<StorageWrite<'_>> = items
            .iter()
            .zip(&values)
            .filter_map(|((id, _), value)| match value {
                Ok(Some(value)) => Some(StorageWrite::Put { id, value }),
                Ok(None) => Some(StorageWrite::Delete { id }),
                Err(_) => None,
            })
            .collect();
        let mut written = self.storage.write_batch(lock, &writes, durable).into_iter();

        values
            .into_iter()
            .map(|value| match value {
                Err(e) => Err(e),
                Ok(_) => written.next().expect("one outcome per storage write"),
            })
            .collect()
    }

    // ── Write pipeline helpers ────────────────────────────────────────────

    /// Take the write lock on the calling thread, then run `f` in the
    /// registry thread pool.
    ///
    /// The order matters with a dedicated pool (`SCAI_REGISTRY_THREADS`): a
    /// pool thread waiting inside one operation may pick up another queued
    /// operation, and if that one blocked on the lock there, it would wait
    /// for a lock held further down its own stack. Blocking on the caller's
    /// thread keeps a waiting writer out of the pool entirely.
    fn locked<T: Send>(&self, f: impl FnOnce(&LockGuard) -> Result<T> + Send) -> Result<T> {
        let lock = self.acquire_lock()?;
        threads::run(|| f(&lock))
    }

    fn write_protected<T: Send>(
        &self,
        kind: ChangeType,
        options: Option<&WriteOptions>,
        prepare: impl FnOnce() -> Result<(Vec<CodeUnitChange>, T)> + Send,
    ) -> Result<T> {
        self.guard_reentrant()?;
        self.locked(|lock| {
            self.storage.prepare_write(lock)?;
            let (changes, value) = prepare()?;
            let changes = self.fire_before_persist(kind, changes, options)?;
            self.persist_changes(lock, &changes)?;
            Ok(value)
        })
    }

    fn write_protected_batch(
        &self,
        kind: ChangeType,
        options: Option<&WriteOptions>,
        prepare: impl FnOnce(&mut BatchResult) -> Result<Vec<CodeUnitChange>> + Send,
    ) -> Result<BatchResult> {
        self.guard_reentrant()?;
        self.locked(|lock| self.write_protected_batch_locked(lock, kind, options, prepare))
    }

    fn write_protected_batch_locked(
        &self,
        lock: &LockGuard,
        kind: ChangeType,
        options: Option<&WriteOptions>,
        prepare: impl FnOnce(&mut BatchResult) -> Result<Vec<CodeUnitChange>>,
    ) -> Result<BatchResult> {
        self.storage.prepare_write(lock)?;
        let mut result = BatchResult::new();
        let changes = prepare(&mut result)?;
        let input_ids = Self::check_duplicate_ids(&changes)?;
        let changes = self.fire_before_persist(kind, changes, options)?;

        result.side_effect_ids = changes
            .iter()
            .filter(|c| !input_ids.contains(&c.id))
            .map(|c| c.id.clone())
            .collect();

        self.persist_changes_batch(lock, &changes, &mut result);
        Ok(result)
    }

    /// Reject batches containing the same ID more than once.
    /// On success returns the set of input IDs for downstream side-effect detection.
    fn check_duplicate_ids(
        changes: &[CodeUnitChange],
    ) -> Result<std::collections::HashSet<String>> {
        let mut seen = std::collections::HashMap::with_capacity(changes.len());
        for (idx, change) in changes.iter().enumerate() {
            if let Some(&first_index) = seen.get(&change.id) {
                return DuplicateBatchIdSnafu {
                    id: change.id.clone(),
                    first_index,
                    duplicate_index: idx,
                    batch_size: changes.len(),
                }
                .fail();
            }
            seen.insert(change.id.clone(), idx);
        }
        Ok(seen.into_keys().collect())
    }

    // ── Create ───────────────────────────────────────────────────────────

    /// Create a new code unit on disk.
    /// If code_unit.id is None, generates a new ID.
    /// Returns the ID of the created code unit.
    /// Errors if the code unit already exists.
    pub fn create(
        &self,
        code_unit: &mut CodeUnit,
        options: Option<&WriteOptions>,
    ) -> Result<String> {
        self.write_protected(ChangeType::Create, options, || {
            let id = self.prepare_create(code_unit)?;
            let changes = vec![CodeUnitChange {
                id: id.clone(),
                before: None,
                after: Some(code_unit.clone()),
            }];
            Ok((changes, id))
        })
    }

    /// Batch create multiple code units efficiently.
    /// All creates are written without sync, then a single sync at the end.
    /// If a code_unit.id is None, generates a new ID for it.
    /// Skips entries that fail (e.g., duplicate IDs) and continues with the rest.
    ///
    /// The returned `BatchResult` may include IDs beyond those in `batch`
    /// when lifecycle hooks trigger side effects (e.g. dependency graph updates).
    pub fn create_batch(
        &self,
        batch: &mut [CodeUnit],
        options: Option<&WriteOptions>,
    ) -> Result<BatchResult> {
        self.write_protected_batch(ChangeType::Create, options, |result| {
            let mut changes = Vec::new();
            for code_unit in batch.iter_mut() {
                match self.prepare_create(code_unit) {
                    Ok(id) => {
                        changes.push(CodeUnitChange {
                            id,
                            before: None,
                            after: Some(code_unit.clone()),
                        });
                    }
                    Err(e) => {
                        let id = code_unit
                            .id
                            .clone()
                            .unwrap_or_else(|| UNKNOWN_ID.to_string());
                        result.failure(id, &e);
                    }
                }
            }
            Ok(changes)
        })
    }

    /// Prepare a code unit for creation: assign ID if needed, validate no conflict.
    /// Does NOT write to disk.
    fn prepare_create(&self, code_unit: &mut CodeUnit) -> Result<String> {
        let id = match &code_unit.id {
            Some(id) => id.clone(),
            None => {
                let new_id = crate::generate_id();
                code_unit.id = Some(new_id.clone());
                new_id
            }
        };

        if self.storage.exists(&id)? {
            return CodeUnitAlreadyExistsSnafu { id }.fail();
        }

        Ok(id)
    }

    // ── Read ─────────────────────────────────────────────────────────────

    /// Load a code unit from disk by ID.
    pub fn get_by_id(&self, id: &str, fields: Option<&[&str]>) -> Result<CodeUnit> {
        threads::run(|| {
            let code_unit = self.load_existing(id)?;
            match fields {
                Some(f) => {
                    let json_value = serde_json::to_value(&code_unit)?;
                    let projected = project_fields(&json_value, f)?;
                    Ok(serde_json::from_value(projected)?)
                }
                None => Ok(code_unit),
            }
        })
    }

    /// List code units, optionally filtered and with field projection.
    ///
    /// If `options.filter` is `None`, returns all code units.
    /// If `options.filter` is `Some`, only returns code units matching the expression.
    /// If `options.fields` is `Some`, returns only the specified fields.
    ///
    /// Uses strict loading and returns an error if any registry JSON is malformed
    /// or has an ID/filename mismatch.
    pub fn find_all(&self, options: FindOptions<'_>) -> Result<Vec<CodeUnit>> {
        threads::run(|| {
            let parsed_filter = options.filter.map(Filter::parse).transpose()?;
            let mut units = match (parsed_filter, options.fields) {
                // Unfiltered projected read: decode only what the projection needs.
                (None, Some(fields)) if fast_projection_enabled() => {
                    loader::RegistryLoader::new(self).read_all_projected(fields)
                }
                (None, fields) => InMemoryRegistry::build(self)?.all_units(fields),
                (Some(parsed_filter), fields) => {
                    let prefilter = prefilter_for_filter(&parsed_filter);
                    let in_memory = if options.include_dependencies {
                        self.load_for_query_with_dependencies(prefilter)?
                    } else {
                        self.load_for_query(prefilter)?
                    };
                    let selected = {
                        let query = in_memory.query();
                        let mut selected =
                            query.matching_indices(|json| parsed_filter.matches(json))?;
                        if options.include_dependencies {
                            query.include_transitive_dependencies(&mut selected);
                        }
                        selected
                    };
                    in_memory.selected_units(selected, fields)
                }
            }?;
            // A path is resolved into the same literal map `bindings` carries, so there
            // is exactly one substitution path whichever input the caller used.
            let from_path = match (options.bindings, options.bindings_path) {
                (Some(_), Some(_)) => {
                    return ValidationSnafu {
                        message: "FindOptions: pass either `bindings` or `bindings_path`, not both"
                            .to_string(),
                    }
                    .fail();
                }
                (None, Some(path)) => {
                    Some(crate::database_bindings::read_database_bindings(path)?.token_map())
                }
                _ => None,
            };
            if let Some(bindings) = options.bindings.or(from_path.as_ref()) {
                for unit in &mut units {
                    crate::bindings::apply_bindings(unit, bindings);
                }
            }
            Ok(units)
        })
    }

    /// Find code units matching all non-null fields of a partial code unit.
    ///
    /// `partial` is a JSON value representing a partial code unit – only the
    /// keys present in the object are compared. For nested objects, the
    /// comparison recurses: a stored code unit matches when every key in
    /// `partial` exists in the stored document and carries the same value.
    ///
    /// If `fields` is `Some`, only the specified fields are returned
    /// (field projection).
    ///
    /// Uses strict loading and returns an error if any registry JSON is malformed
    /// or has an ID/filename mismatch.
    pub fn find_by_object(
        &self,
        partial: &Value,
        fields: Option<&[&str]>,
    ) -> Result<Vec<CodeUnit>> {
        threads::run(|| {
            let in_memory = self.load_for_query(prefilter_for_partial(partial))?;
            let selected = {
                let query = in_memory.query();
                query.matching_indices(|json| matches_partial(partial, json))?
            };
            in_memory.selected_units(selected, fields)
        })
    }

    // ── Update (PATCH) ───────────────────────────────────────────────────

    /// Update specific fields in a code unit by dot-notation paths.
    /// Always syncs to disk after the update.
    pub fn update(
        &self,
        id: &str,
        updates: &[(&str, Value)],
        options: Option<&WriteOptions>,
    ) -> Result<()> {
        self.write_protected(ChangeType::Update, options, || {
            let existing = self.load_existing(id)?;
            let patched = self.prepare_update(&existing, updates)?;
            let changes = vec![CodeUnitChange {
                id: id.to_string(),
                before: Some(existing),
                after: Some(patched),
            }];
            Ok((changes, ()))
        })
    }

    /// Update all code units matching a filter with the same updates.
    ///
    /// Matching uses strict loading: if any registry JSON is malformed or has an
    /// ID/filename mismatch, this method returns an error before applying updates.
    ///
    /// After the match set is loaded, per-item update failures are recorded in
    /// `BatchResult.failed` and processing continues for the remaining matches.
    ///
    /// The returned `BatchResult` may include IDs beyond the matched set
    /// when lifecycle hooks trigger side effects (e.g. dependency graph updates).
    pub fn update_where(
        &self,
        filter: &str,
        updates: &[(&str, Value)],
        options: Option<&WriteOptions>,
    ) -> Result<BatchResult> {
        self.write_protected_batch(ChangeType::Update, options, |result| {
            let matches = self.find_all(FindOptions {
                filter: Some(filter),
                ..FindOptions::default()
            })?;
            let mut changes = Vec::new();
            for existing in matches {
                if let Some(id) = existing.id.clone() {
                    match self.prepare_update(&existing, updates) {
                        Ok(patched) => {
                            changes.push(CodeUnitChange {
                                id,
                                before: Some(existing),
                                after: Some(patched),
                            });
                        }
                        Err(e) => result.failure(id, &e),
                    }
                }
            }
            Ok(changes)
        })
    }

    /// Batch update multiple code units efficiently.
    /// All updates are written to temp files first, then renamed, with a single sync at the end.
    /// Skips entries that fail (e.g., not found) and continues with the rest.
    ///
    /// The returned `BatchResult` may include IDs beyond those in `batch`
    /// when lifecycle hooks trigger side effects (e.g. dependency graph updates).
    pub fn update_batch(
        &self,
        batch: &[(&str, Vec<(&str, Value)>)],
        options: Option<&WriteOptions>,
    ) -> Result<BatchResult> {
        self.write_protected_batch(ChangeType::Update, options, |result| {
            let mut changes = Vec::new();
            for (id, updates) in batch {
                match self.load_existing(id).and_then(|existing| {
                    let patched = self.prepare_update(&existing, updates)?;
                    Ok((existing, patched))
                }) {
                    Ok((existing, patched)) => {
                        changes.push(CodeUnitChange {
                            id: id.to_string(),
                            before: Some(existing),
                            after: Some(patched),
                        });
                    }
                    Err(e) => result.failure(id.to_string(), &e),
                }
            }
            Ok(changes)
        })
    }

    /// Produce the patched CodeUnit from applying updates to an existing unit.
    /// Does NOT write to disk or apply checksums.
    fn prepare_update(&self, existing: &CodeUnit, updates: &[(&str, Value)]) -> Result<CodeUnit> {
        let mut json_value = serde_json::to_value(existing)?;
        for (path, value) in updates {
            set_path(&mut json_value, path, value.clone())?;
        }
        Ok(serde_json::from_value(json_value)?)
    }

    // ── Upsert (merge) ──────────────────────────────────────────────────

    /// Create-or-merge a single code unit.
    ///
    /// * If the code unit does **not** exist on disk, it is created (like `create`).
    /// * If it **does** exist, the incoming fields are deep-merged into the
    ///   existing document -- fields present in `code_unit` overwrite the
    ///   corresponding fields on disk, but fields **not** present in `code_unit`
    ///   (i.e. serialised as `None` / absent) are left untouched.
    ///
    /// Returns the ID of the upserted code unit.
    pub fn upsert(
        &self,
        code_unit: &mut CodeUnit,
        options: Option<&WriteOptions>,
    ) -> Result<String> {
        self.write_protected(ChangeType::Upsert, options, || {
            let existing = self.load_optional(code_unit.id.as_deref().unwrap_or(""))?;
            let (id, merged) = self.prepare_upsert(code_unit, existing.as_ref())?;
            let changes = vec![CodeUnitChange {
                id: id.clone(),
                before: existing,
                after: Some(merged),
            }];
            Ok((changes, id))
        })
    }

    /// Batch upsert multiple code units.
    ///
    /// The returned `BatchResult` may include IDs beyond those in `batch`
    /// when lifecycle hooks trigger side effects (e.g. dependency graph updates).
    pub fn upsert_batch(
        &self,
        batch: &mut [CodeUnit],
        options: Option<&WriteOptions>,
    ) -> Result<BatchResult> {
        self.write_protected_batch(ChangeType::Upsert, options, |result| {
            let mut changes = Vec::new();
            for code_unit in batch.iter_mut() {
                let existing = match code_unit.id.as_deref() {
                    Some(id) => self.load_optional(id)?,
                    None => None,
                };
                match self.prepare_upsert(code_unit, existing.as_ref()) {
                    Ok((id, merged)) => {
                        changes.push(CodeUnitChange {
                            id,
                            before: existing,
                            after: Some(merged),
                        });
                    }
                    Err(e) => {
                        let id = code_unit
                            .id
                            .clone()
                            .unwrap_or_else(|| UNKNOWN_ID.to_string());
                        result.failure(id, &e);
                    }
                }
            }
            Ok(changes)
        })
    }

    /// Prepare an upsert: merge incoming into existing (or use as-is for create).
    /// Returns (id, merged_unit). Does NOT write to disk.
    fn prepare_upsert(
        &self,
        code_unit: &mut CodeUnit,
        existing: Option<&CodeUnit>,
    ) -> Result<(String, CodeUnit)> {
        let id = match &code_unit.id {
            Some(id) => id.clone(),
            None => {
                let new_id = crate::generate_id();
                code_unit.id = Some(new_id.clone());
                new_id
            }
        };

        if let Some(existing) = existing {
            let mut base_value = serde_json::to_value(existing)?;
            let patch_value = serde_json::to_value(&*code_unit)?;
            deep_merge(&mut base_value, &patch_value);
            let merged: CodeUnit = serde_json::from_value(base_value)?;
            Ok((id, merged))
        } else {
            Ok((id, code_unit.clone()))
        }
    }

    /// Recompute checksums for file entries selected by `mode` on an
    /// existing code unit.
    ///
    /// Reads the unit from disk, re-hashes selected file entries
    /// (compare-then-update), and persists through the standard changes
    /// pipeline (before-persist hooks fire with `ChangeType::Update`).
    pub fn update_checksum(&self, id: &str, mode: ChecksumMode) -> Result<()> {
        self.write_protected(ChangeType::Update, None, || {
            let existing = self.load_existing(id)?;
            let mut updated = existing.clone();
            apply_checksums(&mut updated, &mode, &self.root)?;
            let changes = vec![CodeUnitChange {
                id: id.to_string(),
                before: Some(existing),
                after: Some(updated),
            }];
            Ok((changes, ()))
        })
    }

    /// Validate checksums for an existing code unit using the explicit mode.
    pub fn validate_checksum(
        &self,
        id: &str,
        mode: ChecksumMode,
    ) -> Result<ChecksumValidationReport> {
        threads::run(|| {
            let code_unit = self.load_existing(id)?;
            Ok(validate_checksum_report(&code_unit, &mode, &self.root))
        })
    }

    // ── Change detection ─────────────────────────────────────────────────

    /// Detect source-code changes across the project.
    ///
    /// Returns a [`SourceCodeChanges`] report containing:
    /// * **code_unit_changes** — code units whose tracked files have been
    ///   modified or removed from disk.
    /// * **untracked_files** — files found under `source/` or `snowflake/`
    ///   that are not referenced by any code unit.
    ///
    /// `mode` selects which file entries to check (`source`, `converted`,
    /// or both). `filter` optionally restricts the scan to code units
    /// matching a SQL WHERE expression.
    pub fn find_sql_file_changes(
        &self,
        mode: ChecksumMode,
        filter: Option<&str>,
    ) -> Result<SourceCodeChanges> {
        threads::run(|| {
            let parsed_filter = filter.map(Filter::parse).transpose()?;
            let in_memory =
                self.load_for_query(parsed_filter.as_ref().and_then(prefilter_for_filter))?;
            let units = match parsed_filter {
                None => in_memory.all_units(None)?,
                Some(parsed_filter) => {
                    let selected = {
                        let query = in_memory.query();
                        query.matching_indices(|json| parsed_filter.matches(json))?
                    };
                    in_memory.selected_units(selected, None)?
                }
            };
            Ok(find_sql_file_changes(
                &units,
                &mode,
                &self.root,
                &self.source_dir(),
                &self.snowflake_dir(),
            ))
        })
    }

    // ── Delete ───────────────────────────────────────────────────────────

    /// Delete a code unit by ID.
    ///
    /// Before-write hooks fire with `before` = existing unit and `after` = `None`.
    /// If a hook sets `after` to `Some(unit)`, the delete is cancelled and the
    /// unit is written instead.
    pub fn delete(&self, id: &str) -> Result<()> {
        self.write_protected(ChangeType::Delete, None, || {
            let existing = self.load_existing(id)?;
            let changes = vec![CodeUnitChange {
                id: id.to_string(),
                before: Some(existing),
                after: None,
            }];
            Ok((changes, ()))
        })
    }

    // ── Refresh ──────────────────────────────────────────────────────────

    /// Recompute dependency-derived fields across the entire registry.
    ///
    /// Uses strict cycle detection: returns `CycleDetected(1014)` if any
    /// dependency cycle is found.
    pub fn refresh_dependencies(&self) -> Result<()> {
        self.locked(|lock| {
            self.storage.prepare_write(lock)?;
            self.refresh_and_sync(lock, true)
        })
    }

    // ── Validation ────────────────────────────────────────────────────────

    /// Migrate all registry documents on disk to the current schema version.
    ///
    /// Acquires the lock internally — callers must **not** already hold it.
    /// Best-effort for per-file steps: per-document failures are recorded in
    /// [`BatchResult::failed`] and processing continues. Registry-aware steps
    /// are all-or-nothing: if one fails, `migrate_schema_all` returns a hard
    /// `Err` and no documents from that run are written to disk.
    ///
    /// When no registry-aware steps exist in the chain, the method
    /// short-circuits to the existing file-at-a-time parallel code path
    /// (no bulk load, no snapshot clone).
    ///
    /// Returns `Err` only for batch-level failures (lock, enumeration, sync,
    /// or a registry-aware step failure).
    pub fn migrate_schema_all(&self) -> Result<BatchResult> {
        use crate::migration::{CURRENT_SCHEMA_VERSION, SCHEMA_MIGRATION_STEPS};

        self.migrate_schema_all_with_steps(SCHEMA_MIGRATION_STEPS, CURRENT_SCHEMA_VERSION)
    }

    /// Internal coordinator for schema migration, parameterized on the
    /// migration chain. The public `migrate_schema_all` delegates here
    /// with the production chain; tests inject custom steps.
    ///
    /// Acquires the lock internally — callers must **not** already hold it.
    #[allow(clippy::needless_pass_by_value)]
    fn migrate_schema_all_with_steps(
        &self,
        steps: &[(i64, crate::migration::SchemaMigrationStep)],
        target_version: i64,
    ) -> Result<BatchResult> {
        use crate::migration::SchemaMigrationStep;

        self.locked(|lock| {
            self.storage.prepare_write(lock)?;

            let has_registry_aware = steps
                .iter()
                .any(|(_, step)| matches!(step, SchemaMigrationStep::RegistryAware(_)));
            if !has_registry_aware {
                return self.migrate_schema_all_per_file_only(lock, steps, target_version);
            }

            let mut result = BatchResult::new();
            let mut docs = self.load_all_schema_docs(&mut result)?;
            let originals: HashMap<String, Value> =
                docs.iter().map(|(id, v)| (id.clone(), v.clone())).collect();

            for &(from_ver, ref step) in steps {
                match step {
                    SchemaMigrationStep::PerFile(f) => {
                        Self::apply_per_file_schema_migration_step(
                            &mut docs,
                            from_ver,
                            *f,
                            &mut result,
                        );
                    }
                    SchemaMigrationStep::RegistryAware(f) => {
                        Self::apply_registry_aware_schema_migration_step(
                            &mut docs, from_ver, *f, &result,
                        )?;
                    }
                }
            }

            Self::validate_schema_migration_results(&docs, target_version, &mut result);
            self.write_changed_schema_docs(lock, &docs, &originals, &mut result);

            if !result.succeeded.is_empty() {
                self.sync()?;
            }
            Ok(result)
        })
    }

    /// Optimized path for chains containing only per-file steps.
    /// Processes documents chunk by chunk in parallel, no bulk load.
    fn migrate_schema_all_per_file_only(
        &self,
        lock: &LockGuard,
        steps: &[(i64, crate::migration::SchemaMigrationStep)],
        target_version: i64,
    ) -> Result<BatchResult> {
        let mut result = BatchResult::new();
        self.storage.for_each_file_chunk(|ids, texts| {
            let outcomes: Vec<Result<Option<Value>>> = texts
                .into_par_iter()
                .map(|text| match text? {
                    Some(text) => Self::migrate_schema_text(&text, steps, target_version),
                    None => Ok(None),
                })
                .collect();

            let writes: Vec<StorageWrite<'_>> = ids
                .iter()
                .zip(&outcomes)
                .filter_map(|(id, outcome)| match outcome {
                    Ok(Some(value)) => Some(StorageWrite::Put { id, value }),
                    _ => None,
                })
                .collect();
            let mut written = self.storage.write_batch(lock, &writes, false).into_iter();

            for (id, outcome) in ids.iter().zip(outcomes) {
                match outcome {
                    Ok(Some(_)) => match written.next().expect("one outcome per storage write") {
                        Ok(()) => result.success(id.clone()),
                        Err(e) => result.failure(id.clone(), &e),
                    },
                    Ok(None) => {}
                    Err(e) => result.failure(id.clone(), &e),
                }
            }
            Ok(())
        })?;

        if !result.succeeded.is_empty() {
            self.sync()?;
        }
        Ok(result)
    }

    /// Migrate a single stored document using the given per-file-only chain.
    /// Returns the migrated document, or `None` when it is already current.
    fn migrate_schema_text(
        text: &str,
        steps: &[(i64, crate::migration::SchemaMigrationStep)],
        target_version: i64,
    ) -> Result<Option<Value>> {
        let value = Self::parse_raw_json(text)?;
        let migrated = crate::migration::migrate_with(value.clone(), target_version, steps)?;

        if migrated == value {
            return Ok(None);
        }

        let _validated: CodeUnit = serde_json::from_value(migrated.clone())?;
        Ok(Some(migrated))
    }

    /// Load all JSON documents from storage into memory.
    /// Parse/IO failures are recorded in `result` and the document is
    /// skipped (not added to the returned vec).
    fn load_all_schema_docs(&self, result: &mut BatchResult) -> Result<Vec<(String, Value)>> {
        let loaded = self.storage.load_all_files(|id, text| {
            (
                id.to_string(),
                text.and_then(|text| Self::parse_raw_json(&text)),
            )
        })?;
        let mut docs = Vec::with_capacity(loaded.len());
        for (id, value) in loaded {
            match value {
                Ok(value) => docs.push((id, value)),
                Err(e) => result.failure(id, &e),
            }
        }
        Ok(docs)
    }

    fn parse_raw_json(text: &str) -> Result<Value> {
        Ok(serde_json::from_str(text)?)
    }

    /// Run a per-file migration step over in-memory documents.
    fn apply_per_file_schema_migration_step(
        docs: &mut [(String, Value)],
        from_ver: i64,
        step_fn: crate::migration::PerFileSchemaMigrationFn,
        result: &mut BatchResult,
    ) {
        for (id, doc) in docs.iter_mut() {
            if result.has_failed(id) {
                continue;
            }
            let version = match crate::migration::extract_version(doc) {
                Ok(v) => v,
                Err(e) => {
                    if !result.has_failed(id) {
                        result.failure(id.clone(), &e);
                    }
                    continue;
                }
            };
            if version == from_ver {
                if let Err(e) = step_fn(doc) {
                    let wrapped_err = SchemaMigrationSnafu {
                        message: format!("v{} to v{}: {e}", from_ver, from_ver + 1),
                        context: None,
                    }
                    .build();
                    result.failure(id.clone(), &wrapped_err);
                } else if let Err(e) = crate::migration::set_version(doc, from_ver + 1) {
                    result.failure(id.clone(), &e);
                }
            }
        }
    }

    /// Run a registry-aware migration step. On failure, returns a hard `Err`.
    ///
    /// Uses `std::mem::take` to move the docs Vec into a
    /// [`SchemaMigrationContext`], then **always** restores it via
    /// `into_inner()` — even if the step returns `Err`.
    ///
    /// On success, bumps `schemaVersion` to `from_ver + 1` on all target
    /// documents (orchestrator owns the version bump).
    fn apply_registry_aware_schema_migration_step(
        docs: &mut Vec<(String, Value)>,
        from_ver: i64,
        step_fn: crate::migration::RegistryAwareSchemaMigrationFn,
        prior_result: &BatchResult,
    ) -> Result<()> {
        let target_ids: HashSet<String> = docs
            .iter()
            .filter(|(id, doc)| {
                if prior_result.has_failed(id) {
                    return false;
                }
                crate::migration::extract_version(doc)
                    .map(|v| v == from_ver)
                    .unwrap_or(false)
            })
            .map(|(id, _)| id.clone())
            .collect();

        if target_ids.is_empty() {
            return Ok(());
        }

        let taken = std::mem::take(docs);
        let doc_count = taken.len();
        let mut ctx = crate::migration::SchemaMigrationContext::new(taken, target_ids.clone());

        let step_result = step_fn(&mut ctx);
        let restored = ctx.into_inner();
        debug_assert_eq!(
            restored.len(),
            doc_count,
            "registry-aware migration must not add or remove documents"
        );
        *docs = restored;

        if let Err(e) = step_result {
            let context = serde_json::json!({
                "fromVersion": from_ver,
                "toVersion": from_ver + 1,
                "stepError": e.to_string(),
                "priorFailures": serde_json::to_value(&prior_result.failed)
                    .expect("BatchFailure is always serializable"),
            });
            return SchemaMigrationSnafu {
                message: format!(
                    "Registry-aware migration v{} to v{} failed: {e}",
                    from_ver,
                    from_ver + 1,
                ),
                context: Some(context),
            }
            .fail();
        }

        for (id, doc) in docs.iter_mut() {
            if target_ids.contains(id.as_str()) {
                crate::migration::set_version(doc, from_ver + 1)?;
            }
        }

        Ok(())
    }

    /// Post-chain validation: check that all non-failed documents are at
    /// `target_version`. Documents with invalid or future versions are
    /// recorded as failures (deduped via `has_failed`).
    fn validate_schema_migration_results(
        docs: &[(String, Value)],
        target_version: i64,
        result: &mut BatchResult,
    ) {
        for (id, doc) in docs {
            if result.has_failed(id) {
                continue;
            }
            match crate::migration::extract_version(doc) {
                Ok(v) if v == target_version => {}
                Ok(v) if v > target_version => {
                    let err = SchemaVersionNewerThanSupportedSnafu {
                        document_version: v,
                        supported_version: target_version,
                    }
                    .build();
                    result.failure(id.clone(), &err);
                }
                Ok(v) => {
                    let err = SchemaMigrationSnafu {
                        message: format!(
                            "document still at v{v} after migration chain, expected v{target_version}",
                        ),
                        context: None,
                    }
                    .build();
                    result.failure(id.clone(), &err);
                }
                Err(e) => {
                    result.failure(id.clone(), &e);
                }
            }
        }
    }

    /// Write migrated documents back to storage. Skips documents that match
    /// their original snapshot and documents already recorded as failed.
    /// Writes the migrated value as-is (no deep-merge) to avoid
    /// re-injecting pre-migration data.
    fn write_changed_schema_docs(
        &self,
        lock: &LockGuard,
        docs: &[(String, Value)],
        originals: &HashMap<String, Value>,
        result: &mut BatchResult,
    ) {
        let mut writes = Vec::new();
        for (id, doc) in docs {
            if result.has_failed(id) {
                continue;
            }
            let changed = originals.get(id) != Some(doc);
            if !changed {
                continue;
            }
            match serde_json::from_value::<CodeUnit>(doc.clone()) {
                Ok(_) => writes.push(StorageWrite::Put { id, value: doc }),
                Err(e) => result.failure(id.clone(), &e.into()),
            }
        }
        let outcomes = self.storage.write_batch(lock, &writes, false);
        for (write, outcome) in writes.iter().zip(outcomes) {
            let StorageWrite::Put { id, .. } = *write else {
                unreachable!("schema migration only writes puts");
            };
            match outcome {
                Ok(()) => result.success(id.to_string()),
                Err(e) => result.failure(id.to_string(), &e),
            }
        }
    }

    /// Validate all code units in the registry.
    ///
    /// Performs JSON syntax checks, JSON Schema validation, serde
    /// deserialization, ID/filename consistency, duplicate ID detection,
    /// referential integrity, and checksum validation (controlled by
    /// `checksum_mode`).
    ///
    /// Returns a [`ValidationReport`] with `is_valid == true` when no
    /// issues are found. All issues are collected (no fail-fast) so callers
    /// get a complete picture in a single invocation — ideal for CI/build
    /// pipelines.
    pub fn validate(
        &self,
        checksum_mode: ChecksumMode,
    ) -> Result<crate::validation::ValidationReport> {
        threads::run(|| {
            crate::validation::validate_registry(&self.storage, &checksum_mode, &self.root)
        })
    }

    /// Validate a single code unit by ID.
    ///
    /// Performs per-file checks (JSON, schema, deserialization, ID/filename,
    /// checksums) but not cross-unit checks (duplicates, referential
    /// integrity).
    pub fn validate_unit(
        &self,
        id: &str,
        checksum_mode: ChecksumMode,
    ) -> Result<crate::validation::ValidationReport> {
        threads::run(|| {
            crate::validation::validate_single(&self.storage, id, &checksum_mode, &self.root)
        })
    }

    /// Full refresh: recompute dependency-derived fields for all units,
    /// then sync to disk (assumes lock held).
    ///
    /// Loads all units, runs the graph refresh algorithm, and writes back
    /// only the units whose dependency-derived fields changed. Always syncs
    /// even if refresh fails, so any preceding writes are durable. The refresh
    /// error (if any) is returned after the sync succeeds.
    ///
    /// In best-effort mode (`strict=false`), cycles silently receive
    /// `topological_rank = -1`.
    fn refresh_and_sync(&self, lock: &LockGuard, strict: bool) -> Result<()> {
        let wrote_any = std::sync::atomic::AtomicBool::new(false);
        let refresh_result = (|| {
            let mut in_memory = InMemoryRegistry::build(self)?;
            let dirty = in_memory.graph().refresh(strict)?;
            #[cfg(test)]
            test_hooks::run_after_load_hook();
            // `dirty` is unique (HashSet scope, see `refresh_scope`), so the
            // batch never writes the same ID twice.
            let items: Vec<(&str, Option<&CodeUnit>)> = dirty
                .iter()
                .map(|&i| {
                    let unit = in_memory.unit(i);
                    let id = unit.id.as_deref().expect("loader guarantees id");
                    (id, Some(unit))
                })
                .collect();
            let mut first_err = None;
            for outcome in self.persist_units(lock, &items, false) {
                match outcome {
                    Ok(()) => wrote_any.store(true, std::sync::atomic::Ordering::Relaxed),
                    Err(e) => {
                        first_err.get_or_insert(e);
                    }
                }
            }
            first_err.map_or(Ok(()), Err)
        })();
        self.sync()?;
        match refresh_result {
            Ok(()) => Ok(()),
            Err(err) if wrote_any.load(std::sync::atomic::Ordering::Relaxed) => {
                Err(WriteSucceededRefreshFailedSnafu.into_error(Box::new(err)))
            }
            Err(err) => Err(err),
        }
    }

    // ── Internal helpers ─────────────────────────────────────────────────

    /// Load the units a query needs: the index-selected candidates when the
    /// backend can push `prefilter` down, otherwise every unit.
    ///
    /// Candidates are a superset of the matches (see `storage::index`), so
    /// callers must still apply the query's predicate to the result.
    fn load_for_query(&self, prefilter: Option<Prefilter>) -> Result<InMemoryRegistry> {
        if let Some(prefilter) = prefilter {
            if let Some(in_memory) = InMemoryRegistry::build_candidates(self, &prefilter)? {
                return Ok(in_memory);
            }
        }
        InMemoryRegistry::build(self)
    }

    /// [`Self::load_for_query`] plus the candidates' transitive dependency
    /// closure, so `include_dependencies` expansion sees every unit it would
    /// reach in a full load.
    fn load_for_query_with_dependencies(
        &self,
        prefilter: Option<Prefilter>,
    ) -> Result<InMemoryRegistry> {
        if let Some(prefilter) = prefilter {
            if let Some(in_memory) =
                InMemoryRegistry::build_candidates_with_dependencies(self, &prefilter)?
            {
                return Ok(in_memory);
            }
        }
        InMemoryRegistry::build(self)
    }

    /// Sync all pending writes to storage (internal use only).
    fn sync(&self) -> Result<()> {
        self.storage.sync()
    }

    /// Load an existing code unit by ID, returning `CodeUnitNotFound` if absent.
    fn load_existing(&self, id: &str) -> Result<CodeUnit> {
        match self.load_optional(id)? {
            Some(unit) => Ok(unit),
            None => CodeUnitNotFoundSnafu { id }.fail(),
        }
    }

    /// Load a code unit by ID, or `None` if absent.
    fn load_optional(&self, id: &str) -> Result<Option<CodeUnit>> {
        self.storage
            .read_raw(id)?
            .map(|text| Self::parse_unit(&text))
            .transpose()
    }

    /// Parse stored JSON as CodeUnit, migrating to the current schema
    /// version and normalizing paths to UNIX-style.
    fn parse_unit(text: &str) -> Result<CodeUnit> {
        let value = Self::parse_raw_json(text)?;
        let mut value = crate::migration::migrate(value)?;
        paths::normalize_value_paths(&mut value);
        Ok(serde_json::from_value(value)?)
    }
}

/// Whether unfiltered projected reads take the decode-only-what's-needed
/// path (see `RegistryLoader::read_all_projected`). Disabled only by tests,
/// to compute the reference result.
fn fast_projection_enabled() -> bool {
    #[cfg(test)]
    if test_hooks::fast_projection_disabled() {
        return false;
    }
    true
}

fn prefilter_for_filter(filter: &Filter) -> Option<Prefilter> {
    pushdown::from_filter(filter)
}

fn prefilter_for_partial(partial: &Value) -> Option<Prefilter> {
    pushdown::from_partial(partial)
}

/// Deep-merge a typed unit on top of its currently stored document (if any
/// parses), so unknown fields in storage survive the write.
fn merge_onto_stored(unit: &CodeUnit, stored: Option<String>) -> Result<Value> {
    let typed = serde_json::to_value(unit)?;
    Ok(
        match stored.and_then(|s| serde_json::from_str::<Value>(&s).ok()) {
            Some(mut raw) => {
                deep_merge(&mut raw, &typed);
                raw
            }
            None => typed,
        },
    )
}

#[cfg(test)]
mod tests;
