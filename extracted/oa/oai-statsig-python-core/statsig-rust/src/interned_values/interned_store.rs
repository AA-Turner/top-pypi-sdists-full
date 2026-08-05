#[cfg(test)]
use std::path::Path;
use std::{
    borrow::Cow,
    collections::{HashMap, hash_map::Entry},
    marker::PhantomData,
    path::PathBuf,
    sync::{
        Arc, OnceLock, Weak,
        atomic::{AtomicBool, Ordering},
    },
    time::Instant,
};

use ahash::AHashMap;
use fancy_regex::Regex as FancyRegex;
use lazy_static::lazy_static;
use parking_lot::RwLock;
use rkyv::{
    Archive, Place, Serialize as RkyvSerialize,
    collections::swiss_table::{ArchivedHashMap, HashMapResolver},
    hash::FxHasher64,
    rancor::{Fallible, Source},
    ser::{Allocator, Writer},
    string::ArchivedString,
    with::{ArchiveWith, DeserializeWith, SerializeWith, With},
};
use serde_json::value::RawValue;
use sha2::{Digest, Sha256};

pub use super::mmap_sync::{MmapSyncCursor, MmapWriteOutcome};

use crate::{
    DynamicReturnable, StatsigErr, StatsigOptions,
    evaluation::{
        dynamic_returnable::DynamicReturnableValue,
        evaluator_value::{EvaluatorValue, EvaluatorValueInner, MemoizedEvaluatorValue},
        rkyv_value::{ArchivedRkyvValue, RkyvValue},
    },
    hashing,
    interned_string::{InternedString, InternedStringValue},
    log_d, log_e,
    networking::ResponseData,
    observability::ops_stats::OpsStatsForInstance,
    specs_adapter::{SpecsInfo, SpecsSyncTrigger, StatsigHttpSpecsAdapter},
    specs_response::{
        proto_specs::deserialize_protobuf,
        spec_types::{Spec, SpecsResponseFull},
        specs_hash_map::{SpecPointer, SpecsHashMap},
    },
    utils::try_release_unused_heap_memory,
};

use super::mmap_data_v2::ArchivedMmapEvaluatorValue;

mod mmap_artifact;
mod mmap_manifest;
mod mmap_reader;
mod mmap_writer;

pub use mmap_artifact::{MmapArtifactSnapshot, MmapArtifactState};
pub use mmap_reader::MmapReaderMemorySnapshot;

use mmap_manifest::open_committed_mmap_v2;
#[cfg(all(test, any(unix, windows)))]
pub(crate) use mmap_manifest::open_committed_mmap_v2_for_test;
#[cfg(test)]
pub(crate) use mmap_manifest::{
    write_mmap_manifest_for_test, write_mmap_v2_only_manifest_for_test,
};
use mmap_reader::{
    MmapRegistryBuilder, MmapSpecKind,
    get_evaluator_value as get_archived_evaluator_value_from_mmap,
    get_returnable as get_returnable_from_mmap, get_spec as get_mmap_spec,
    get_string as get_string_from_mmap,
};
use mmap_writer::{acquire_mmap_write_lock, write_mmap_artifacts};
#[cfg(test)]
pub(crate) use mmap_writer::{acquire_mmap_write_lock_for_test, write_mmap_v2_for_test};

const TAG: &str = "InternedStore";
const MMAP_DIRECTORY: &str = "statsig-interned-store";
pub(crate) const LEGACY_MMAP_FORMAT_VERSION: u32 = 1;
const WEAK_STORE_SWEEP_INTERVAL: usize = 4096;

/// Controls optional work performed while installing an interned mmap reader.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct MmapPreloadOptions {
    /// Precompute stable hashes for archived JSON returnables.
    ///
    /// This trades preload CPU and process heap for predictable checksum-enabled
    /// GCIR latency. It does not change the mmap artifact and is disabled by
    /// default.
    pub precompute_returnable_stable_hashes: bool,
}

#[non_exhaustive]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MmapPreloadReport {
    /// Format version shared by the validated and installed artifacts.
    pub format_version: u32,
    /// Number of artifacts installed.
    pub loaded: usize,
    /// Optional inputs that were skipped, indexed within `optional_sdk_keys`.
    pub skipped_optional: Vec<MmapPreloadFailure>,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) struct MmapProjectId {
    sdk_key_hash: [u8; 32],
    artifact_id: u32,
}

impl MmapProjectId {
    pub(crate) fn for_sdk_key(sdk_key: &str) -> Self {
        Self {
            sdk_key_hash: Sha256::digest(sdk_key.as_bytes()).into(),
            artifact_id: hashing::djb2_number(sdk_key) as u32,
        }
    }

    fn aliases_artifact(self, other: Self) -> bool {
        self.artifact_id == other.artifact_id
    }

    fn artifact_id(self) -> u32 {
        self.artifact_id
    }
}

#[non_exhaustive]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MmapPreloadFailure {
    pub index: usize,
    pub error: String,
}
static IMMORTAL_DATA: OnceLock<ImmortalData> = OnceLock::new();
static MMAP_EVALUATOR_OVERRIDE_EXISTS: AtomicBool = AtomicBool::new(false);

lazy_static! {
    static ref MUTABLE_STRINGS: MutableStore<String> = MutableStore::default();
    static ref MUTABLE_RETURNABLES: MutableStore<HashMap<String, RkyvValue>> =
        MutableStore::default();
    static ref MUTABLE_EVALUATOR_VALUES: MutableStore<MemoizedEvaluatorValue> =
        MutableStore::default();
}

type MutableEntries<T> = AHashMap<u64, Weak<T>>;

struct MutableTable<T> {
    entries: MutableEntries<T>,
    insertions: usize,
    next_sweep_at: usize,
}

impl<T> Default for MutableTable<T> {
    fn default() -> Self {
        Self {
            entries: AHashMap::new(),
            insertions: 0,
            next_sweep_at: WEAK_STORE_SWEEP_INTERVAL,
        }
    }
}

struct MutableStore<T> {
    table: RwLock<MutableTable<T>>,
}

impl<T> Default for MutableStore<T> {
    fn default() -> Self {
        Self {
            table: RwLock::new(MutableTable::default()),
        }
    }
}

impl<T> MutableStore<T> {
    fn get(&self, hash: u64) -> Option<Arc<T>> {
        let table = self.table.read();
        let value = table.entries.get(&hash)?.upgrade();
        value
    }

    fn get_or_insert(&self, hash: u64, candidate: Arc<T>) -> Arc<T> {
        let mut table = self.table.write();
        let (value, inserted) = match table.entries.entry(hash) {
            Entry::Occupied(mut entry) => match entry.get().upgrade() {
                Some(value) => (value, false),
                None => {
                    entry.insert(Arc::downgrade(&candidate));
                    (candidate, true)
                }
            },
            Entry::Vacant(entry) => {
                entry.insert(Arc::downgrade(&candidate));
                (candidate, true)
            }
        };

        if inserted {
            Self::maybe_sweep(&mut table);
        }
        value
    }

    fn replace(&self, hash: u64, value: &Arc<T>) {
        let mut table = self.table.write();
        table.entries.insert(hash, Arc::downgrade(value));
        Self::maybe_sweep(&mut table);
    }

    #[cfg(test)]
    fn live_len(&self) -> usize {
        self.table
            .read()
            .entries
            .iter()
            .filter(|(_, value)| value.strong_count() > 0)
            .count()
    }

    #[cfg(test)]
    fn stored_len(&self) -> usize {
        self.table.read().entries.len()
    }

    #[cfg(test)]
    fn stored_capacity(&self) -> usize {
        self.table.read().entries.capacity()
    }

    fn take_live(&self) -> Vec<(u64, Arc<T>)> {
        let detached = {
            let mut table = self.table.write();
            std::mem::take(&mut *table)
        };

        let mut values = Vec::with_capacity(detached.entries.len());
        for (hash, value) in detached.entries {
            if let Some(value) = value.upgrade() {
                values.push((hash, value));
            }
        }
        values
    }

    fn maybe_sweep(table: &mut MutableTable<T>) {
        table.insertions += 1;
        if table.insertions == table.next_sweep_at {
            table.entries.retain(|_, value| value.strong_count() > 0);
            table.next_sweep_at = table
                .insertions
                .saturating_add(table.entries.len().max(WEAK_STORE_SWEEP_INTERVAL));
        }
    }
}

// Archives compact live-entry vectors directly as ArchivedHashMaps, avoiding
// intermediate owned hash tables and rehashing.
pub(super) struct MapKVVec<A, B>(PhantomData<(A, B)>);

struct WithKey<'a, K, A> {
    key: &'a K,
    _adapter: PhantomData<A>,
}

impl<K, A> Copy for WithKey<'_, K, A> {}

impl<K, A> Clone for WithKey<'_, K, A> {
    fn clone(&self) -> Self {
        *self
    }
}

impl<K: PartialEq, A> PartialEq for WithKey<'_, K, A> {
    fn eq(&self, other: &Self) -> bool {
        self.key == other.key
    }
}

impl<K: Eq, A> Eq for WithKey<'_, K, A> {}

impl<K: std::hash::Hash, A> std::hash::Hash for WithKey<'_, K, A> {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.key.hash(state);
    }
}

impl<K, A> Archive for WithKey<'_, K, A>
where
    A: ArchiveWith<K>,
{
    type Archived = A::Archived;
    type Resolver = A::Resolver;

    fn resolve(&self, resolver: Self::Resolver, out: Place<Self::Archived>) {
        A::resolve_with(self.key, resolver, out);
    }
}

impl<K, A, S> RkyvSerialize<S> for WithKey<'_, K, A>
where
    S: Fallible + ?Sized,
    A: SerializeWith<K, S>,
{
    fn serialize(&self, serializer: &mut S) -> Result<Self::Resolver, S::Error> {
        A::serialize_with(self.key, serializer)
    }
}

impl<A, B, K, V> ArchiveWith<Vec<(K, V)>> for MapKVVec<A, B>
where
    A: ArchiveWith<K>,
    B: ArchiveWith<V>,
{
    type Archived = ArchivedHashMap<A::Archived, B::Archived>;
    type Resolver = HashMapResolver;

    fn resolve_with(field: &Vec<(K, V)>, resolver: Self::Resolver, out: Place<Self::Archived>) {
        ArchivedHashMap::resolve_from_len(field.len(), (7, 8), resolver, out);
    }
}

impl<A, B, K, V, S> SerializeWith<Vec<(K, V)>, S> for MapKVVec<A, B>
where
    A: ArchiveWith<K> + SerializeWith<K, S>,
    B: ArchiveWith<V> + SerializeWith<V, S>,
    K: std::hash::Hash + Eq,
    A::Archived: std::hash::Hash + Eq,
    S: Fallible + Allocator + Writer + ?Sized,
    S::Error: Source,
{
    fn serialize_with(field: &Vec<(K, V)>, serializer: &mut S) -> Result<Self::Resolver, S::Error> {
        ArchivedHashMap::<_, _, FxHasher64>::serialize_from_iter::<
            _,
            _,
            _,
            WithKey<'_, K, A>,
            With<V, B>,
            S,
        >(
            field.iter().map(|(key, value)| {
                (
                    WithKey {
                        key,
                        _adapter: PhantomData,
                    },
                    With::<V, B>::cast(value),
                )
            }),
            (7, 8),
            serializer,
        )
    }
}

impl<A, B, K, V, D> DeserializeWith<ArchivedHashMap<A::Archived, B::Archived>, Vec<(K, V)>, D>
    for MapKVVec<A, B>
where
    A: ArchiveWith<K> + DeserializeWith<A::Archived, K, D>,
    B: ArchiveWith<V> + DeserializeWith<B::Archived, V, D>,
    D: Fallible + ?Sized,
{
    fn deserialize_with(
        field: &ArchivedHashMap<A::Archived, B::Archived>,
        deserializer: &mut D,
    ) -> Result<Vec<(K, V)>, D::Error> {
        let mut result = Vec::with_capacity(field.len());
        for (key, value) in field.iter() {
            result.push((
                A::deserialize_with(key, deserializer)?,
                B::deserialize_with(value, deserializer)?,
            ));
        }
        Ok(result)
    }
}

/// Immortal vs Mutable Data
/// ------------------------------------------------------------
/// -`ImmortalData` is static and never changes. It will only exist if a successful call to `preload` is made. It is intentionally
///  leaked so that it can be accessed across forks without incrementing the reference count.
/// -Mutable stores are sharded weak maps. Handles own the values, so dropping a
///  handle never takes a global lock. Dead weak entries are swept periodically.
/// ------------------------------------------------------------
/// In all cases, we first check if there is an ImmortalData entry and then fall back to a mutable store.
#[derive(Default)]
struct ImmortalData {
    strings: AHashMap<u64, &'static str>,
    returnables: AHashMap<u64, &'static HashMap<String, RkyvValue>>,
    evaluator_values: AHashMap<u64, &'static MemoizedEvaluatorValue>,
    feature_gates: AHashMap<u64, &'static Spec>,
    dynamic_configs: AHashMap<u64, &'static Spec>,
    layer_configs: AHashMap<u64, &'static Spec>,
}
#[derive(Default)]
struct MutableData {
    strings: Vec<(u64, Arc<String>)>,
    returnables: Vec<(u64, Arc<HashMap<String, RkyvValue>>)>,
    evaluator_values: Vec<(u64, Arc<MemoizedEvaluatorValue>)>,
}

pub trait Internable: Sized {
    type Input<'a>;
    fn intern(input: Self::Input<'_>) -> Self;
}

pub struct InternedStore;

impl InternedStore {
    pub fn preload(data: &[u8]) -> Result<(), StatsigErr> {
        Self::preload_multi(&[data])
    }

    pub fn preload_multi(data: &[&[u8]]) -> Result<(), StatsigErr> {
        let start_time = Instant::now();

        if IMMORTAL_DATA.get().is_some() {
            log_e!(TAG, "Already preloaded");
            return Err(StatsigErr::InvalidOperation(
                "Already preloaded".to_string(),
            ));
        }

        let specs_responses = data
            .iter()
            .map(|data| try_parse_as_json(data).or_else(|_| try_parse_as_proto(data)))
            .collect::<Result<Vec<SpecsResponseFull>, StatsigErr>>()?;

        let immortal = mutable_to_immortal(specs_responses)?;

        if IMMORTAL_DATA.set(immortal).is_err() {
            return Err(StatsigErr::LockFailure(
                "Failed to set IMMORTAL_DATA".to_string(),
            ));
        }

        let end_time = Instant::now();
        log_d!(
            TAG,
            "Preload took {}ms",
            end_time.duration_since(start_time).as_millis()
        );

        Ok(())
    }

    /// Publishes a V2 mmap artifact selected by `sdk_key`.
    ///
    /// On Unix, the finalized artifact is atomically published with mode `0644`
    /// so readers with unrelated UIDs can consume a read-only shared mount.
    pub async fn fetch_and_write_mmap(sdk_key: &str) -> Result<(), StatsigErr> {
        Self::fetch_and_write_mmap_with_options(sdk_key, None).await
    }

    pub async fn fetch_and_write_mmap_with_specs_url(
        sdk_key: &str,
        specs_url: &str,
    ) -> Result<(), StatsigErr> {
        let options = StatsigOptions {
            specs_url: Some(specs_url.to_string()),
            ..StatsigOptions::default()
        };

        Self::fetch_and_write_mmap_with_options(sdk_key, Some(&options)).await
    }

    pub async fn fetch_and_write_mmap_with_specs_url_if_changed(
        sdk_key: &str,
        specs_url: &str,
        previous: Option<&MmapSyncCursor>,
    ) -> Result<MmapWriteOutcome, StatsigErr> {
        let options = StatsigOptions {
            specs_url: Some(specs_url.to_string()),
            ..StatsigOptions::default()
        };

        Self::fetch_and_write_mmap_with_options_if_changed(sdk_key, Some(&options), previous).await
    }

    pub(crate) async fn fetch_and_write_mmap_with_options(
        sdk_key: &str,
        options: Option<&StatsigOptions>,
    ) -> Result<(), StatsigErr> {
        match Self::fetch_and_write_mmap_with_options_if_changed(sdk_key, options, None).await? {
            MmapWriteOutcome::Published(_) => Ok(()),
            MmapWriteOutcome::NoUpdate => Err(StatsigErr::InvalidOperation(
                "An unconditional mmap fetch did not return a publishable config snapshot"
                    .to_string(),
            )),
        }
    }

    pub(crate) async fn fetch_and_write_mmap_with_options_if_changed(
        sdk_key: &str,
        options: Option<&StatsigOptions>,
        previous: Option<&MmapSyncCursor>,
    ) -> Result<MmapWriteOutcome, StatsigErr> {
        // Serialize the full same-key refresh so a delayed response cannot
        // overwrite a newer generation published by another writer.
        let write_lock = acquire_mmap_write_lock(&mmap_lock_path_for_sdk_key(sdk_key)).await?;
        let adapter = StatsigHttpSpecsAdapter::new(sdk_key, options, None);
        let mut specs_info = SpecsInfo::empty();
        if let Some(previous) = previous {
            specs_info.lcut = Some(previous.lcut);
            specs_info.checksum = previous.checksum.clone();
        }

        let mut response = adapter
            .fetch_specs_from_network(specs_info, SpecsSyncTrigger::Manual)
            .await
            .map_err(StatsigErr::NetworkError)?;
        let result = write_mmap_artifacts(
            &mut response.data,
            previous,
            &mmap_v2_path_for_sdk_key(sdk_key),
            &mmap_manifest_path_for_sdk_key(sdk_key),
        );

        drop(response);
        drop(adapter);
        drop(write_lock);
        try_release_unused_heap_memory();
        result
    }

    pub fn preload_mmap(sdk_key: &str) -> Result<(), StatsigErr> {
        Self::preload_mmap_with_options(sdk_key, &MmapPreloadOptions::default()).map(|_| ())
    }

    /// Reports memory accounting for the currently loaded mmap reader.
    ///
    /// Returns `None` before a reader has been installed. Linux reports RSS,
    /// PSS, private dirty, deleted mapping bytes, and VMA segment count for the
    /// exact retained mapping by reading `/proc/self/smaps`, so callers should
    /// sample infrequently. Other platforms leave those optional fields unset.
    pub fn mmap_reader_memory_snapshot() -> Result<Option<MmapReaderMemorySnapshot>, StatsigErr> {
        mmap_reader::memory_snapshot()
    }

    /// Preloads the committed artifact with optional eager reader work and
    /// reports the selected compatibility-reader format.
    pub fn preload_mmap_with_options(
        sdk_key: &str,
        options: &MmapPreloadOptions,
    ) -> Result<MmapPreloadReport, StatsigErr> {
        Self::preload_mmap_multi_with_options(&[sdk_key], &[], options)
    }

    /// Preloads committed V2 mmap artifacts for multiple SDK keys in one atomic install.
    ///
    /// Required keys fail the whole operation. Optional keys that cannot be opened,
    /// validated, or safely combined are returned in `skipped_optional`. Call this once
    /// before creating SDK instances or forking worker processes.
    pub fn preload_mmap_multi(
        required_sdk_keys: &[&str],
        optional_sdk_keys: &[&str],
    ) -> Result<MmapPreloadReport, StatsigErr> {
        Self::preload_mmap_multi_with_options(
            required_sdk_keys,
            optional_sdk_keys,
            &MmapPreloadOptions::default(),
        )
    }

    /// Preloads multiple committed V2 artifacts with shared reader options.
    ///
    /// Options apply to every required and successfully loaded optional project.
    pub fn preload_mmap_multi_with_options(
        required_sdk_keys: &[&str],
        optional_sdk_keys: &[&str],
        options: &MmapPreloadOptions,
    ) -> Result<MmapPreloadReport, StatsigErr> {
        if required_sdk_keys.is_empty() {
            return Err(StatsigErr::InvalidOperation(
                "At least one required interned mmap SDK key must be provided".to_string(),
            ));
        }
        if mmap_reader::is_installed() {
            return Err(StatsigErr::InvalidOperation(
                "Interned mmap data is already preloaded".to_string(),
            ));
        }

        let mut builder = MmapRegistryBuilder::new();
        for sdk_key in required_sdk_keys {
            let file = open_committed_mmap_for_sdk_key(sdk_key)?;
            builder.add_file(MmapProjectId::for_sdk_key(sdk_key), file)?;
        }

        let mut report = MmapPreloadReport {
            format_version: super::mmap_data_v2::MmapDataV2::FORMAT_VERSION,
            loaded: required_sdk_keys.len(),
            skipped_optional: Vec::new(),
        };
        for (index, sdk_key) in optional_sdk_keys.iter().enumerate() {
            let result = open_committed_mmap_for_sdk_key(sdk_key)
                .and_then(|file| builder.add_file(MmapProjectId::for_sdk_key(sdk_key), file));
            match result {
                Ok(()) => report.loaded += 1,
                Err(error) => report.skipped_optional.push(MmapPreloadFailure {
                    index,
                    error: error.to_string(),
                }),
            }
        }

        builder.install(options)?;
        Ok(report)
    }

    pub(crate) fn with_mmap_project<T>(id: MmapProjectId, callback: impl FnOnce() -> T) -> T {
        mmap_reader::with_project(id, callback)
    }
}

fn open_committed_mmap_for_sdk_key(sdk_key: &str) -> Result<std::fs::File, StatsigErr> {
    // TODO: Bind the manifest to the full SDK-key digest and verify it here. These
    // paths use a 32-bit hash, so colliding keys can overwrite each other's artifact.
    let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
    let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);
    open_committed_mmap_v2(
        &manifest_path,
        &legacy_mmap_v1_path_for_sdk_key(sdk_key),
        &v2_path,
    )?
    .ok_or_else(|| {
        StatsigErr::InvalidOperation("No committed interned mmap V2 artifact was found".to_string())
    })
}

#[cfg(test)]
pub(crate) fn preload_mmap_v2_for_test(path: &Path) -> Result<(), StatsigErr> {
    mmap_reader::preload_v2(path, &MmapPreloadOptions::default())
}

#[cfg(test)]
pub(crate) fn preload_mmap_v2_multi_for_test(projects: &[(&str, &Path)]) -> Result<(), StatsigErr> {
    preload_mmap_v2_multi_with_options_for_test(projects, &MmapPreloadOptions::default())
}

#[cfg(test)]
pub(crate) fn preload_mmap_v2_multi_with_options_for_test(
    projects: &[(&str, &Path)],
    options: &MmapPreloadOptions,
) -> Result<(), StatsigErr> {
    let mut builder = MmapRegistryBuilder::new();
    for (sdk_key, path) in projects {
        let file =
            std::fs::File::open(path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
        builder.add_file(MmapProjectId::for_sdk_key(sdk_key), file)?;
    }
    builder.install(options)
}

#[cfg(test)]
pub(crate) fn validate_mmap_v2_for_test(path: &Path) -> Result<(), StatsigErr> {
    mmap_reader::validate_v2(path)
}

pub(crate) fn legacy_mmap_v1_path_for_sdk_key(sdk_key: &str) -> PathBuf {
    mmap_path_for_sdk_key_version(sdk_key, 1)
}

pub(crate) fn mmap_v2_path_for_sdk_key(sdk_key: &str) -> PathBuf {
    mmap_path_for_sdk_key_version(sdk_key, super::mmap_data_v2::MmapDataV2::FORMAT_VERSION)
}

pub(crate) fn mmap_manifest_path_for_sdk_key(sdk_key: &str) -> PathBuf {
    std::env::temp_dir().join(MMAP_DIRECTORY).join(format!(
        "{}_interned_store_manifest.json",
        hashing::djb2(sdk_key),
    ))
}

pub(crate) fn mmap_lock_path_for_sdk_key(sdk_key: &str) -> PathBuf {
    std::env::temp_dir()
        .join(MMAP_DIRECTORY)
        .join(format!("{}_interned_store.lock", hashing::djb2(sdk_key)))
}

fn mmap_path_for_sdk_key_version(sdk_key: &str, version: u32) -> PathBuf {
    std::env::temp_dir().join(MMAP_DIRECTORY).join(format!(
        "{}_v{version}_interned_store.mmap",
        hashing::djb2(sdk_key),
    ))
}

impl InternedStore {
    pub(crate) fn get_mmap_returnable_stable_hash(hash: u64) -> Option<u64> {
        mmap_reader::get_returnable_stable_hash(hash)
    }

    pub fn get_or_intern_string<T: AsRef<str> + ToString>(value: T) -> InternedString {
        let hash = hashing::hash_one(value.as_ref().as_bytes());

        if let Some(string) = get_string_from_mmap(hash) {
            return InternedString::from_static(hash, string);
        }

        if let Some(string) = get_string_from_shared(hash) {
            return InternedString::from_static(hash, string);
        }

        let ptr = get_string_from_local(hash, value);
        InternedString::from_pointer(hash, ptr)
    }

    pub fn get_or_intern_owned_string(value: String) -> InternedString {
        let hash = hashing::hash_one(value.as_bytes());

        if let Some(string) = get_string_from_mmap(hash) {
            return InternedString::from_static(hash, string);
        }

        if let Some(string) = get_string_from_shared(hash) {
            return InternedString::from_static(hash, string);
        }

        let ptr = get_owned_string_from_local(hash, value);
        InternedString::from_pointer(hash, ptr)
    }

    pub fn get_or_intern_returnable(value: Cow<'_, RawValue>) -> DynamicReturnable {
        let raw_string = value.get();
        match raw_string {
            "true" => return DynamicReturnable::from_bool(true),
            "false" => return DynamicReturnable::from_bool(false),
            "null" => return DynamicReturnable::empty(),
            _ => {}
        }

        let hash = hashing::hash_one(raw_string.as_bytes());

        if let Some(returnable) = get_returnable_from_mmap(hash) {
            return DynamicReturnable::from_archived(hash, returnable);
        }

        if let Some(returnable) = get_returnable_from_shared(hash) {
            return DynamicReturnable::from_static(hash, returnable);
        }

        let ptr = get_returnable_from_local(hash, value);
        DynamicReturnable::from_pointer(hash, ptr)
    }

    pub fn get_or_intern_evaluator_value(value: Cow<'_, RawValue>) -> EvaluatorValue {
        let raw_string = value.get();
        let hash = hashing::hash_one(raw_string.as_bytes());

        if let Some(evaluator_value) = get_evaluator_value_from_mmap(hash) {
            return evaluator_value;
        }

        if let Some(evaluator_value) = get_evaluator_value_from_shared(hash) {
            return EvaluatorValue::from_static(hash, evaluator_value);
        }

        let ptr = get_or_create_evaluator_value_from_local(hash, value);
        EvaluatorValue::from_pointer(hash, ptr)
    }

    pub fn replace_evaluator_value(hash: u64, evaluator_value: Arc<MemoizedEvaluatorValue>) {
        MUTABLE_EVALUATOR_VALUES.replace(hash, &evaluator_value);
    }

    pub(crate) fn replace_mmap_evaluator_value(
        hash: u64,
        evaluator_value: Arc<MemoizedEvaluatorValue>,
    ) {
        let has_regex = evaluator_value.regex_value.is_some();
        MUTABLE_EVALUATOR_VALUES.replace(hash, &evaluator_value);
        if has_regex {
            MMAP_EVALUATOR_OVERRIDE_EXISTS.store(true, Ordering::Release);
        }
    }

    pub fn try_get_preloaded_evaluator_value(bytes: &[u8]) -> Option<EvaluatorValue> {
        let hash = hashing::hash_one(bytes);
        if let Some(evaluator_value) = get_evaluator_value_from_mmap(hash) {
            return Some(evaluator_value);
        }

        if let Some(evaluator_value) = get_evaluator_value_from_shared(hash) {
            return Some(EvaluatorValue::from_static(hash, evaluator_value));
        }

        None
    }

    pub fn try_get_preloaded_returnable(bytes: &[u8]) -> Option<DynamicReturnable> {
        match bytes {
            b"true" => return Some(DynamicReturnable::from_bool(true)),
            b"false" => return Some(DynamicReturnable::from_bool(false)),
            b"null" => return Some(DynamicReturnable::empty()),
            _ => {}
        }

        let hash = hashing::hash_one(bytes);

        if let Some(returnable) = get_returnable_from_mmap(hash) {
            return Some(DynamicReturnable::from_archived(hash, returnable));
        }

        if let Some(returnable) = get_returnable_from_shared(hash) {
            return Some(DynamicReturnable::from_static(hash, returnable));
        }

        None
    }

    pub fn try_get_preloaded_dynamic_config(name: &InternedString) -> Option<SpecPointer> {
        if let Some(spec) = get_mmap_spec(MmapSpecKind::DynamicConfig, name.hash) {
            return Some(SpecPointer::from_mmap(spec));
        }

        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .dynamic_configs
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub fn try_get_preloaded_layer_config(name: &InternedString) -> Option<SpecPointer> {
        if let Some(spec) = get_mmap_spec(MmapSpecKind::LayerConfig, name.hash) {
            return Some(SpecPointer::from_mmap(spec));
        }

        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .layer_configs
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub fn try_get_preloaded_feature_gate(name: &InternedString) -> Option<SpecPointer> {
        if let Some(spec) = get_mmap_spec(MmapSpecKind::FeatureGate, name.hash) {
            return Some(SpecPointer::from_mmap(spec));
        }

        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .feature_gates
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub(crate) fn try_get_preloaded_spec(
        name: &InternedString,
        entity: &str,
    ) -> Option<SpecPointer> {
        [
            MmapSpecKind::FeatureGate,
            MmapSpecKind::DynamicConfig,
            MmapSpecKind::LayerConfig,
        ]
        .into_iter()
        .find_map(|kind| {
            let spec = get_mmap_spec(kind, name.hash)?;
            (get_string_from_mmap(spec.entity.to_native()) == Some(entity))
                .then(|| SpecPointer::from_mmap(spec))
        })
    }

    pub(crate) fn has_preloaded_mmap_v2() -> bool {
        mmap_reader::has_v2()
    }
    pub(crate) fn get_mmap_string(hash: u64) -> Option<&'static str> {
        get_string_from_mmap(hash)
    }

    #[cfg(test)]
    pub fn get_memoized_len() -> (
        /* strings */ usize,
        /* returnables */ usize,
        /* evaluator values */ usize,
    ) {
        (
            MUTABLE_STRINGS.live_len(),
            MUTABLE_RETURNABLES.live_len(),
            MUTABLE_EVALUATOR_VALUES.live_len(),
        )
    }
}

// ------------------------------------------------------------------------------- [ Preloading ]

fn try_parse_as_json(data: &[u8]) -> Result<SpecsResponseFull, StatsigErr> {
    serde_json::from_slice(data)
        .map_err(|e| StatsigErr::JsonParseError(TAG.to_string(), e.to_string()))
}

fn try_parse_as_proto(data: &[u8]) -> Result<SpecsResponseFull, StatsigErr> {
    let current = SpecsResponseFull::default();
    let mut next = SpecsResponseFull::default();

    let mut response_data = ResponseData::from_bytes_with_headers(
        data.to_vec(),
        Some(std::collections::HashMap::from([(
            "content-encoding".to_string(),
            "statsig-br".to_string(),
        )])),
    );

    let ops_stats = OpsStatsForInstance::new();

    deserialize_protobuf(&ops_stats, &current, &mut next, &mut response_data)?;

    Ok(next)
}

// ------------------------------------------------------------------------------- [ String ]

fn get_string_from_shared(hash: u64) -> Option<&'static str> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.strings.get(&hash).copied(),
        None => None,
    }
}

fn get_string_from_local<T: ToString>(hash: u64, value: T) -> Arc<String> {
    if let Some(string) = MUTABLE_STRINGS.get(hash) {
        return string;
    }

    MUTABLE_STRINGS.get_or_insert(hash, Arc::new(value.to_string()))
}

fn get_owned_string_from_local(hash: u64, value: String) -> Arc<String> {
    if let Some(string) = MUTABLE_STRINGS.get(hash) {
        return string;
    }

    MUTABLE_STRINGS.get_or_insert(hash, Arc::new(value))
}

// ------------------------------------------------------------------------------- [ Returnable ]

fn get_returnable_from_shared(hash: u64) -> Option<&'static HashMap<String, RkyvValue>> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.returnables.get(&hash).copied(),
        None => None,
    }
}

fn get_returnable_from_local(hash: u64, value: Cow<RawValue>) -> Arc<HashMap<String, RkyvValue>> {
    if let Some(returnable) = MUTABLE_RETURNABLES.get(hash) {
        return returnable;
    }

    let owned: HashMap<String, RkyvValue> = match serde_json::from_str(value.get()) {
        Ok(owned) => owned,
        Err(e) => {
            log_e!(TAG, "Failed to parse returnable from local: {}", e);
            return Arc::new(HashMap::new());
        }
    };

    MUTABLE_RETURNABLES.get_or_insert(hash, Arc::new(owned))
}

// ------------------------------------------------------------------------------- [ Evaluator Value ]

fn get_evaluator_value_from_mmap(hash: u64) -> Option<EvaluatorValue> {
    let (value, regex) = get_archived_evaluator_value_from_mmap(hash)?;

    if regex.is_none() && MMAP_EVALUATOR_OVERRIDE_EXISTS.load(Ordering::Acquire) {
        if let Some(value) =
            get_evaluator_value_from_local(hash).filter(|value| value.regex_value.is_some())
        {
            return Some(EvaluatorValue::from_pointer(hash, value));
        }
    }

    Some(EvaluatorValue::from_mmap(hash, value, regex))
}

fn get_evaluator_value_from_shared(hash: u64) -> Option<&'static MemoizedEvaluatorValue> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.evaluator_values.get(&hash).copied(),
        None => None,
    }
}

fn get_evaluator_value_from_local(hash: u64) -> Option<Arc<MemoizedEvaluatorValue>> {
    MUTABLE_EVALUATOR_VALUES.get(hash)
}

fn get_or_create_evaluator_value_from_local(
    hash: u64,
    value: Cow<'_, RawValue>,
) -> Arc<MemoizedEvaluatorValue> {
    if let Some(evaluator_value) = MUTABLE_EVALUATOR_VALUES.get(hash) {
        return evaluator_value;
    }

    let ptr = Arc::new(MemoizedEvaluatorValue::from_raw_value(value));
    MUTABLE_EVALUATOR_VALUES.get_or_insert(hash, ptr)
}

// ------------------------------------------------------------------------------- [ Helpers ]

fn mutable_to_immortal(
    specs_responses: Vec<SpecsResponseFull>,
) -> Result<ImmortalData, StatsigErr> {
    let mutable_data = take_mutable_data();
    let mut immortal = ImmortalData::default();

    for (hash, arc) in mutable_data.strings.into_iter() {
        let raw = Arc::into_raw(arc);
        let leaked: &'static str = unsafe { &*raw };
        immortal.strings.insert(hash, leaked);
    }

    for (hash, returnable) in mutable_data.returnables.into_iter() {
        let raw_returnable = Arc::into_raw(returnable);
        let leaked = unsafe { &*raw_returnable };
        immortal.returnables.insert(hash, leaked);
    }

    for (hash, evaluator_value) in mutable_data.evaluator_values.into_iter() {
        let raw_evaluator_value = Arc::into_raw(evaluator_value);
        let leaked = unsafe { &*raw_evaluator_value };
        immortal.evaluator_values.insert(hash, leaked);
    }

    for response in specs_responses {
        try_insert_specs(response.feature_gates, &mut immortal.feature_gates);
        try_insert_specs(response.dynamic_configs, &mut immortal.dynamic_configs);
        try_insert_specs(response.layer_configs, &mut immortal.layer_configs);
    }

    Ok(immortal)
}

fn take_mutable_data() -> MutableData {
    MutableData {
        strings: MUTABLE_STRINGS.take_live(),
        returnables: MUTABLE_RETURNABLES.take_live(),
        evaluator_values: MUTABLE_EVALUATOR_VALUES.take_live(),
    }
}

fn try_insert_specs(source: SpecsHashMap, destination: &mut AHashMap<u64, &'static Spec>) {
    for (name, spec_ptr) in source.0.into_iter() {
        let Some(spec) = spec_ptr.into_pointer() else {
            continue;
        };

        if spec.checksum.is_none() {
            // no point doint this if there is no checksum field to verify against later
            continue;
        }

        let raw_spec = Arc::into_raw(spec);
        let spec = unsafe { &*raw_spec };
        destination.insert(name.hash, spec);
    }
}

// ------------------------------------------------------------------------------- [ Helper Implementations ]

impl EvaluatorValue {
    fn from_mmap(
        hash: u64,
        evaluator_value: &'static ArchivedMmapEvaluatorValue,
        regex: Option<&'static FancyRegex>,
    ) -> Self {
        Self {
            hash,
            inner: EvaluatorValueInner::Mmap(
                crate::evaluation::evaluator_value::MmapEvaluatorValueHandle::new(
                    evaluator_value,
                    regex,
                ),
            ),
        }
    }

    fn from_static(hash: u64, evaluator_value: &'static MemoizedEvaluatorValue) -> Self {
        Self {
            hash,
            inner: EvaluatorValueInner::Static(evaluator_value),
        }
    }

    fn from_pointer(hash: u64, pointer: Arc<MemoizedEvaluatorValue>) -> Self {
        Self {
            hash,
            inner: EvaluatorValueInner::Pointer(pointer),
        }
    }
}

impl DynamicReturnable {
    fn from_static(hash: u64, returnable: &'static HashMap<String, RkyvValue>) -> Self {
        Self::from_interned_value(hash, DynamicReturnableValue::JsonStatic(returnable))
    }

    fn from_archived(
        hash: u64,
        returnable: &'static ArchivedHashMap<ArchivedString, ArchivedRkyvValue>,
    ) -> Self {
        Self::from_archived_value(hash, returnable)
    }

    fn from_pointer(hash: u64, pointer: Arc<HashMap<String, RkyvValue>>) -> Self {
        Self::from_interned_value(hash, DynamicReturnableValue::JsonPointer(pointer))
    }
}

impl InternedString {
    pub(crate) fn from_static(hash: u64, string: &'static str) -> Self {
        Self {
            hash,
            value: InternedStringValue::Static(string),
        }
    }

    fn from_pointer(hash: u64, pointer: Arc<String>) -> Self {
        Self {
            hash,
            value: InternedStringValue::Pointer(pointer),
        }
    }
}

#[cfg(test)]
mod mutable_store_tests {
    use super::MutableStore;
    use std::sync::{Arc, Barrier};

    #[test]
    fn concurrent_insertions_share_one_live_value() {
        const THREAD_COUNT: usize = 16;
        let store = Arc::new(MutableStore::<String>::default());
        let start = Arc::new(Barrier::new(THREAD_COUNT));

        let threads = (0..THREAD_COUNT)
            .map(|_| {
                let store = Arc::clone(&store);
                let start = Arc::clone(&start);
                std::thread::spawn(move || {
                    start.wait();
                    store.get_or_insert(42, Arc::new("shared".to_owned()))
                })
            })
            .collect::<Vec<_>>();
        let handles = threads
            .into_iter()
            .map(|thread| thread.join().expect("interner thread should finish"))
            .collect::<Vec<_>>();

        assert!(handles.iter().all(|value| Arc::ptr_eq(value, &handles[0])));
    }

    #[test]
    fn dead_value_is_replaced() {
        let store = MutableStore::<String>::default();
        let first = store.get_or_insert(42, Arc::new("first".to_owned()));
        let weak_first = Arc::downgrade(&first);
        drop(first);

        assert!(store.get(42).is_none());

        let second = store.get_or_insert(42, Arc::new("second".to_owned()));
        assert!(weak_first.upgrade().is_none());
        assert_eq!(second.as_str(), "second");
        assert_eq!(store.live_len(), 1);
    }

    #[test]
    fn dead_entries_are_bounded_by_periodic_sweeps() {
        let store = MutableStore::<String>::default();

        for hash in 0..super::WEAK_STORE_SWEEP_INTERVAL as u64 {
            drop(store.get_or_insert(hash, Arc::new(hash.to_string())));
        }

        assert_eq!(store.live_len(), 0);
        assert_eq!(store.stored_len(), 1);
    }

    #[test]
    fn take_live_retires_the_old_table() {
        let store = MutableStore::<String>::default();
        let live = store.get_or_insert(1, Arc::new("live".to_owned()));
        drop(store.get_or_insert(2, Arc::new("dead".to_owned())));

        assert!(store.stored_capacity() > 0);
        let taken = store.take_live();

        assert!(Arc::ptr_eq(
            &taken.iter().find(|(hash, _)| *hash == 1).unwrap().1,
            &live
        ));
        assert!(!taken.iter().any(|(hash, _)| *hash == 2));
        assert_eq!(store.stored_len(), 0);
        assert_eq!(store.stored_capacity(), 0);
    }

    #[test]
    fn take_live_releases_weak_metadata_before_a_batch_drop() {
        const BATCH_SIZE: u64 = 1024;

        let store = MutableStore::<String>::default();
        let handles = (0..BATCH_SIZE)
            .map(|hash| store.get_or_insert(hash, Arc::new(hash.to_string())))
            .collect::<Vec<_>>();
        assert!(store.stored_capacity() >= BATCH_SIZE as usize);

        let taken = store.take_live();

        assert_eq!(taken.len(), BATCH_SIZE as usize);
        assert_eq!(store.stored_len(), 0);
        assert_eq!(store.stored_capacity(), 0);

        drop(handles);
        assert!(taken.iter().all(|(_, value)| Arc::strong_count(value) == 1));
        drop(taken);
        assert_eq!(store.stored_len(), 0);
    }
}
