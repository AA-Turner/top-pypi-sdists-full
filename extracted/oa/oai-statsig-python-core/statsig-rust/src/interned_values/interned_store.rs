use std::{
    borrow::Cow,
    collections::{hash_map::Entry, HashMap},
    fs::{create_dir_all, File},
    io::Write,
    path::{Path, PathBuf},
    sync::{Arc, OnceLock},
    time::{Duration, Instant},
};

#[cfg(unix)]
use std::os::unix::fs::PermissionsExt;

use ahash::AHashMap;
use lazy_static::lazy_static;
use memmap2::Mmap;
use ouroboros::self_referencing;
use parking_lot::Mutex;
use rkyv::{
    collections::swiss_table::ArchivedHashMap,
    string::ArchivedString,
    with::{Identity, MapKV, Unshare},
    Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize,
};
use serde_json::value::RawValue;

use crate::{
    evaluation::{
        dynamic_returnable::DynamicReturnableValue,
        evaluator_value::{EvaluatorValue, EvaluatorValueInner, MemoizedEvaluatorValue},
        rkyv_value::{ArchivedRkyvValue, RkyvValue},
    },
    hashing,
    interned_string::{InternedString, InternedStringValue},
    log_d, log_e, log_w,
    networking::ResponseData,
    observability::ops_stats::OpsStatsForInstance,
    specs_adapter::{SpecsInfo, SpecsSyncTrigger, StatsigHttpSpecsAdapter},
    specs_response::{
        proto_specs::deserialize_protobuf,
        spec_types::{Spec, SpecsResponseFull},
        specs_hash_map::{SpecPointer, SpecsHashMap},
    },
    DynamicReturnable, StatsigErr, StatsigOptions,
};

const TAG: &str = "InternedStore";
const MMAP_DIRECTORY: &str = "statsig-interned-store";

static IMMORTAL_DATA: OnceLock<ImmortalData> = OnceLock::new();
static MMAP_DATA: OnceLock<LoadedMmapData> = OnceLock::new();

lazy_static! {
    static ref MUTABLE_DATA: Mutex<MutableData> = Mutex::new(MutableData::default());
}

#[derive(Archive, RkyvDeserialize, RkyvSerialize)]
pub(crate) struct MmapDataV1 {
    format_version: u32,
    #[rkyv(with = MapKV<Identity, Unshare>)]
    strings: HashMap<u64, Arc<String>, ahash::RandomState>,
    #[rkyv(with = MapKV<Identity, Unshare>)]
    returnables: HashMap<u64, Arc<HashMap<String, RkyvValue>>, ahash::RandomState>,
}

impl MmapDataV1 {
    // Create MmapDataV2 and increment this when the archived layout or
    // serialization semantics change.
    pub(crate) const FORMAT_VERSION: u32 = 1;

    #[cfg(test)]
    pub(crate) fn empty_with_format_version(format_version: u32) -> Self {
        Self {
            format_version,
            strings: AHashMap::new().into(),
            returnables: AHashMap::new().into(),
        }
    }
}

impl ArchivedMmapDataV1 {
    pub(crate) fn format_version(&self) -> u32 {
        self.format_version.to_native()
    }

    #[cfg(test)]
    pub(crate) fn string_for_test(&self, hash: u64) -> Option<&str> {
        let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
        self.strings.get(&archived_hash).map(|value| value.as_str())
    }

    #[cfg(test)]
    pub(crate) fn returnable_for_test(&self, hash: u64, key: &str) -> Option<&ArchivedRkyvValue> {
        let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
        self.returnables.get(&archived_hash)?.get(key)
    }

    #[cfg(test)]
    pub(crate) fn find_returnable_value_for_test(&self, key: &str) -> Option<&ArchivedRkyvValue> {
        self.returnables
            .iter()
            .find_map(|(_, returnable)| returnable.get(key))
    }
}

impl Default for MmapDataV1 {
    fn default() -> Self {
        Self {
            format_version: Self::FORMAT_VERSION,
            strings: AHashMap::new().into(),
            returnables: AHashMap::new().into(),
        }
    }
}

#[self_referencing]
struct LoadedMmapData {
    file: File,
    mmap: Mmap,

    #[borrows(mmap)]
    archived: &'this ArchivedMmapDataV1,
}

/// Immortal vs Mutable Data
/// ------------------------------------------------------------
/// -`ImmortalData` is static and never changes. It will only exist if a successful call to `preload` is made. It is intentionally
///  leaked so that it can be accessed across forks without incrementing the reference count.
/// -`MutableData` is dynamic and changes over time as values are added and removed.
/// ------------------------------------------------------------
/// In all cases, we first check if there is a ImmortalData entry and then fallback to MutableData.
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
    strings: AHashMap<u64, Arc<String>>,
    returnables: AHashMap<u64, Arc<HashMap<String, RkyvValue>>>,
    evaluator_values: AHashMap<u64, Arc<MemoizedEvaluatorValue>>,
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

    /// Publishes an mmap artifact selected by `sdk_key`.
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

    pub(crate) async fn fetch_and_write_mmap_with_options(
        sdk_key: &str,
        options: Option<&StatsigOptions>,
    ) -> Result<(), StatsigErr> {
        let adapter = StatsigHttpSpecsAdapter::new(sdk_key, options, None);
        let mut response = adapter
            .fetch_specs_from_network(SpecsInfo::empty(), SpecsSyncTrigger::Manual)
            .await
            .map_err(StatsigErr::NetworkError)?;
        let specs_response = parse_specs_response_data(&mut response.data)?;

        write_mmap_specs(vec![specs_response], &mmap_path_for_sdk_key(sdk_key))
    }

    pub fn preload_mmap(sdk_key: &str) -> Result<(), StatsigErr> {
        preload_mmap_from_path(&mmap_path_for_sdk_key(sdk_key))
    }
}

fn write_mmap_specs(
    specs_responses: Vec<SpecsResponseFull>,
    path: &Path,
) -> Result<(), StatsigErr> {
    if let Some(parent) = path.parent() {
        create_dir_all(parent).map_err(|e| StatsigErr::FileError(e.to_string()))?;
    }

    let parent = path
        .parent()
        .ok_or_else(|| StatsigErr::FileError("Mmap path has no parent".to_string()))?;
    let mut file = tempfile::NamedTempFile::new_in(parent)
        .map_err(|e| StatsigErr::FileError(e.to_string()))?;

    let mmap_data = mutable_to_mmap_data(specs_responses)?;
    let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&mmap_data)
        .map_err(|e| StatsigErr::SerializationError(e.to_string()))?;

    file.write_all(&archived)
        .map_err(|e| StatsigErr::FileError(e.to_string()))?;
    #[cfg(unix)]
    file.as_file()
        .set_permissions(std::fs::Permissions::from_mode(0o644))
        .map_err(|e| StatsigErr::FileError(e.to_string()))?;
    file.as_file()
        .sync_all()
        .map_err(|e| StatsigErr::FileError(e.to_string()))?;
    file.persist(path)
        .map_err(|e| StatsigErr::FileError(e.error.to_string()))?;

    log_d!(
        TAG,
        "Wrote {} bytes to mmap file {}",
        archived.len(),
        path.display()
    );

    Ok(())
}

fn preload_mmap_from_path(path: &Path) -> Result<(), StatsigErr> {
    let file = File::open(path).map_err(|e| StatsigErr::FileError(e.to_string()))?;
    let mmap = unsafe { Mmap::map(&file).map_err(|e| StatsigErr::FileError(e.to_string()))? };

    let loaded_result = LoadedMmapDataTryBuilder {
        file,
        mmap,
        archived_builder: |mmap| rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(mmap),
    }
    .try_build();

    let loaded = match loaded_result {
        Ok(loaded) => loaded,
        Err(e) => {
            return Err(StatsigErr::SerializationError(e.to_string()));
        }
    };

    let format_version = loaded.borrow_archived().format_version();
    if format_version != MmapDataV1::FORMAT_VERSION {
        return Err(StatsigErr::SerializationError(format!(
            "Unsupported interned mmap format version {format_version}; expected {}",
            MmapDataV1::FORMAT_VERSION
        )));
    }

    MMAP_DATA
        .set(loaded)
        .map_err(|_| StatsigErr::LockFailure("Failed to set MMAP_DATA".to_string()))
}

pub(crate) fn mmap_path_for_sdk_key(sdk_key: &str) -> PathBuf {
    std::env::temp_dir().join(MMAP_DIRECTORY).join(format!(
        "{}_v{}_interned_store.mmap",
        hashing::djb2(sdk_key),
        MmapDataV1::FORMAT_VERSION
    ))
}

fn parse_specs_response_data(
    response_data: &mut ResponseData,
) -> Result<SpecsResponseFull, StatsigErr> {
    if is_protobuf_specs_response(response_data) {
        let current = SpecsResponseFull::default();
        let mut next = SpecsResponseFull::default();
        deserialize_protobuf(
            &OpsStatsForInstance::new(),
            &current,
            &mut next,
            response_data,
        )?;
        return Ok(next);
    }

    response_data.deserialize_into::<SpecsResponseFull>()
}

fn is_protobuf_specs_response(response_data: &ResponseData) -> bool {
    let content_type = response_data.get_header_ref("content-type");
    if content_type.map(|s| s.as_str().contains("application/octet-stream")) != Some(true) {
        return false;
    }

    let content_encoding = response_data.get_header_ref("content-encoding");
    content_encoding.map(|s| s.as_str().contains("statsig-br")) == Some(true)
}

impl InternedStore {
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

        if let Some(evaluator_value) = get_evaluator_value_from_shared(hash) {
            return EvaluatorValue::from_static(hash, evaluator_value);
        }

        let ptr = get_evaluator_value_from_local(hash, value);
        EvaluatorValue::from_pointer(hash, ptr)
    }

    pub fn replace_evaluator_value(hash: u64, evaluator_value: Arc<MemoizedEvaluatorValue>) {
        let old = use_mutable_data("replace_evaluator_value", |data| {
            data.evaluator_values.insert(hash, evaluator_value)
        });
        drop(old);
    }

    pub fn try_get_preloaded_evaluator_value(bytes: &[u8]) -> Option<EvaluatorValue> {
        let hash = hashing::hash_one(bytes);
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
        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .dynamic_configs
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub fn try_get_preloaded_layer_config(name: &InternedString) -> Option<SpecPointer> {
        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .layer_configs
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub fn try_get_preloaded_feature_gate(name: &InternedString) -> Option<SpecPointer> {
        match IMMORTAL_DATA.get() {
            Some(shared) => shared
                .feature_gates
                .get(&name.hash)
                .map(|s| SpecPointer::Static(s)),
            None => None,
        }
    }

    pub fn release_returnable(hash: u64) {
        let ptr = use_mutable_data("release_returnable", |data| {
            try_release_entry(&mut data.returnables, hash)
        });
        drop(ptr);
    }

    pub fn release_string(hash: u64) {
        let ptr = use_mutable_data("release_string", |data| {
            try_release_entry(&mut data.strings, hash)
        });
        drop(ptr);
    }

    pub fn release_evaluator_value(hash: u64) {
        let ptr = use_mutable_data("release_eval_value", |data| {
            try_release_entry(&mut data.evaluator_values, hash)
        });
        drop(ptr);
    }

    #[cfg(test)]
    pub fn get_memoized_len() -> (
        /* strings */ usize,
        /* returnables */ usize,
        /* evaluator values */ usize,
    ) {
        match MUTABLE_DATA.try_lock() {
            Some(memo) => (
                memo.strings.len(),
                memo.returnables.len(),
                memo.evaluator_values.len(),
            ),
            None => (0, 0, 0),
        }
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

fn get_string_from_mmap(hash: u64) -> Option<&'static str> {
    let data = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let found = data.borrow_archived().strings.get(&archived_hash);
    found.map(|s| s.as_str())
}

fn get_string_from_shared(hash: u64) -> Option<&'static str> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.strings.get(&hash).copied(),
        None => None,
    }
}

fn get_string_from_local<T: ToString>(hash: u64, value: T) -> Arc<String> {
    let result = use_mutable_data("intern_string", |data| {
        if let Some(string) = data.strings.get(&hash) {
            return Some(string.clone());
        }

        let ptr = Arc::new(value.to_string());
        data.strings.insert(hash, ptr.clone());
        Some(ptr)
    });

    result.unwrap_or_else(|| {
        log_w!(TAG, "Failed to get string from local");
        Arc::new(value.to_string())
    })
}

// ------------------------------------------------------------------------------- [ Returnable ]

fn get_returnable_from_mmap(
    hash: u64,
) -> Option<&'static ArchivedHashMap<ArchivedString, ArchivedRkyvValue>> {
    let data = MMAP_DATA.get()?;

    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let found = data.borrow_archived().returnables.get(&archived_hash)?;
    Some(found)
}

fn get_returnable_from_shared(hash: u64) -> Option<&'static HashMap<String, RkyvValue>> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.returnables.get(&hash).copied(),
        None => None,
    }
}

fn get_returnable_from_local(hash: u64, value: Cow<RawValue>) -> Arc<HashMap<String, RkyvValue>> {
    let result = use_mutable_data("intern_returnable", |data| {
        if let Some(returnable) = data.returnables.get(&hash) {
            return Some(returnable.clone());
        }

        None
    });

    if let Some(returnable) = result {
        return returnable;
    }

    let owned: HashMap<String, RkyvValue> = match serde_json::from_str(value.get()) {
        Ok(owned) => owned,
        Err(e) => {
            log_e!(TAG, "Failed to parse returnable from local: {}", e);
            return Arc::new(HashMap::new());
        }
    };

    let ptr = Arc::new(owned);

    use_mutable_data("intern_returnable", |data| {
        data.returnables.insert(hash, ptr.clone());
        Some(())
    });

    ptr
}

// ------------------------------------------------------------------------------- [ Evaluator Value ]

fn get_evaluator_value_from_shared(hash: u64) -> Option<&'static MemoizedEvaluatorValue> {
    match IMMORTAL_DATA.get() {
        Some(shared) => shared.evaluator_values.get(&hash).copied(),
        None => None,
    }
}

fn get_evaluator_value_from_local(
    hash: u64,
    value: Cow<'_, RawValue>,
) -> Arc<MemoizedEvaluatorValue> {
    let result = use_mutable_data("eval_value_lookup", |data| {
        if let Some(evaluator_value) = data.evaluator_values.get(&hash) {
            return Some(evaluator_value.clone());
        }

        None
    });

    if let Some(evaluator_value) = result {
        return evaluator_value;
    }

    // intentinonally done across two locks to avoid deadlock with InternedString creation
    let ptr = Arc::new(MemoizedEvaluatorValue::from_raw_value(value));
    let _ = use_mutable_data("intern_evaluator_value", |data| {
        data.evaluator_values.insert(hash, ptr.clone());
        Some(())
    });

    ptr
}

// ------------------------------------------------------------------------------- [ Helpers ]

fn try_release_entry<T>(data: &mut AHashMap<u64, Arc<T>>, hash: u64) -> Option<Arc<T>> {
    let found = match data.entry(hash) {
        Entry::Occupied(entry) => entry,
        Entry::Vacant(_) => return None,
    };

    let strong_count = Arc::strong_count(found.get());
    if strong_count == 1 {
        let value = found.remove();
        // return the value so it isn't dropped while holding the lock
        return Some(value);
    }

    None
}

fn use_mutable_data<T>(reason: &str, f: impl FnOnce(&mut MutableData) -> Option<T>) -> Option<T> {
    let mut data = match MUTABLE_DATA.try_lock_for(Duration::from_secs(5)) {
        Some(data) => data,
        None => {
            #[cfg(test)]
            panic!("Failed to acquire lock for mutable data ({reason})");

            #[cfg(not(test))]
            {
                log_e!(TAG, "Failed to acquire lock for mutable data ({reason})");
                return None;
            }
        }
    };

    f(&mut data)
}

fn mutable_to_immortal(
    specs_responses: Vec<SpecsResponseFull>,
) -> Result<ImmortalData, StatsigErr> {
    let mutable_data: MutableData = {
        let mut mutable_data_lock = MUTABLE_DATA.lock();
        std::mem::take(&mut *mutable_data_lock)
    };
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

fn mutable_to_mmap_data(specs_responses: Vec<SpecsResponseFull>) -> Result<MmapDataV1, StatsigErr> {
    let mutable_data: MutableData = {
        let mut mutable_data_lock = MUTABLE_DATA.lock();
        std::mem::take(&mut *mutable_data_lock)
    };

    Ok(detached_mutable_to_mmap_data(mutable_data, specs_responses))
}

fn detached_mutable_to_mmap_data(
    mutable_data: MutableData,
    specs_responses: Vec<SpecsResponseFull>,
) -> MmapDataV1 {
    let MutableData {
        strings,
        returnables,
        evaluator_values,
    } = mutable_data;

    // Specs and evaluator values can retain interned strings and returnables.
    // Drop them only after detaching MUTABLE_DATA so their destructors cannot
    // remove entries that still need to be archived.
    drop(specs_responses);
    drop(evaluator_values);

    // TODO: Add evaluator values to mmap data
    // for (hash, evaluator_value) in evaluator_values.into_iter() {
    //     let raw_evaluator_value = Arc::into_raw(evaluator_value);
    //     let leaked = unsafe { &*raw_evaluator_value };
    //     mmap_data.evaluator_values.insert(hash, leaked);
    // }

    MmapDataV1 {
        format_version: MmapDataV1::FORMAT_VERSION,
        // AHashMap wraps this exact std HashMap type, so these conversions move
        // the existing tables without allocating, iterating, or rehashing.
        strings: strings.into(),
        returnables: returnables.into(),
    }
}

fn try_insert_specs(source: SpecsHashMap, destination: &mut AHashMap<u64, &'static Spec>) {
    for (name, spec_ptr) in source.0.into_iter() {
        let spec = match spec_ptr {
            SpecPointer::Pointer(spec) => spec,
            _ => continue,
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
        Self {
            hash,
            value: DynamicReturnableValue::JsonStatic(returnable),
        }
    }

    fn from_archived(
        hash: u64,
        returnable: &'static ArchivedHashMap<ArchivedString, ArchivedRkyvValue>,
    ) -> Self {
        Self {
            hash,
            value: DynamicReturnableValue::JsonArchived(returnable),
        }
    }

    fn from_pointer(hash: u64, pointer: Arc<HashMap<String, RkyvValue>>) -> Self {
        Self {
            hash,
            value: DynamicReturnableValue::JsonPointer(pointer),
        }
    }
}

impl InternedString {
    fn from_static(hash: u64, string: &'static str) -> Self {
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
mod mmap_arc_archive_tests {
    use super::*;
    use crate::evaluation::evaluator_value::EvaluatorValueType;

    // Freeze the exact source shape used before the Arc-backed archive input.
    // This models the previous V1 reader and must not be refactored alongside
    // MmapDataV1: new writer bytes have to remain readable through this type.
    #[derive(Archive, RkyvSerialize)]
    #[rkyv(archived = PreviousArchivedMmapDataV1)]
    struct PreviousOwnedMmapDataV1 {
        format_version: u32,
        strings: HashMap<u64, String>,
        returnables: HashMap<u64, HashMap<String, RkyvValue>>,
    }

    impl PreviousArchivedMmapDataV1 {
        fn format_version(&self) -> u32 {
            self.format_version.to_native()
        }

        fn string(&self, hash: u64) -> Option<&str> {
            let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
            self.strings.get(&archived_hash).map(|value| value.as_str())
        }

        fn returnable(&self, hash: u64, key: &str) -> Option<&ArchivedRkyvValue> {
            let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
            self.returnables.get(&archived_hash)?.get(key)
        }
    }

    fn arc_backed_v1_source() -> MmapDataV1 {
        let returnable = HashMap::from([("enabled".to_string(), RkyvValue::Bool(true))]);
        MmapDataV1 {
            format_version: MmapDataV1::FORMAT_VERSION,
            strings: AHashMap::from_iter([(7, Arc::new("v1-string".to_string()))]).into(),
            returnables: AHashMap::from_iter([(11, Arc::new(returnable))]).into(),
        }
    }

    fn previous_owned_v1_source() -> PreviousOwnedMmapDataV1 {
        PreviousOwnedMmapDataV1 {
            format_version: MmapDataV1::FORMAT_VERSION,
            strings: HashMap::from([(7, "v1-string".to_string())]),
            returnables: HashMap::from([(
                11,
                HashMap::from([("enabled".to_string(), RkyvValue::Bool(true))]),
            )]),
        }
    }

    #[test]
    fn previous_owned_v1_reader_reads_arc_backed_writer_bytes() {
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&arc_backed_v1_source()).unwrap();
        let previous =
            rkyv::access::<PreviousArchivedMmapDataV1, rkyv::rancor::Error>(&bytes).unwrap();

        assert_eq!(previous.format_version(), MmapDataV1::FORMAT_VERSION);
        assert_eq!(previous.string(7), Some("v1-string"));
        assert!(matches!(
            previous.returnable(11, "enabled"),
            Some(ArchivedRkyvValue::Bool(true))
        ));
    }

    #[test]
    fn current_v1_reader_reads_previous_owned_writer_bytes() {
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&previous_owned_v1_source()).unwrap();
        let current = rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(&bytes).unwrap();

        assert_eq!(current.format_version(), MmapDataV1::FORMAT_VERSION);
        assert_eq!(current.string_for_test(7), Some("v1-string"));
        assert!(matches!(
            current.returnable_for_test(11, "enabled"),
            Some(ArchivedRkyvValue::Bool(true))
        ));
    }

    #[test]
    fn conversion_keeps_shared_arc_allocations() {
        let string = Arc::new("shared string".to_string());
        let other_string_owner = Arc::clone(&string);
        let returnable = Arc::new(HashMap::from([(
            "enabled".to_string(),
            RkyvValue::Bool(true),
        )]));
        let other_returnable_owner = Arc::clone(&returnable);
        let mutable_data = MutableData {
            strings: AHashMap::from_iter([(7, string)]),
            returnables: AHashMap::from_iter([(11, returnable)]),
            evaluator_values: AHashMap::new(),
        };

        let mmap_data = detached_mutable_to_mmap_data(mutable_data, Vec::new());

        assert!(Arc::ptr_eq(
            mmap_data.strings.get(&7).unwrap(),
            &other_string_owner
        ));
        assert!(Arc::ptr_eq(
            mmap_data.returnables.get(&11).unwrap(),
            &other_returnable_owner
        ));
    }

    #[test]
    fn conversion_releases_evaluator_cache_before_returning_archive_input() {
        let evaluator = Arc::new(MemoizedEvaluatorValue::new(EvaluatorValueType::Null));
        let evaluator_weak = Arc::downgrade(&evaluator);
        let mutable_data = MutableData {
            strings: AHashMap::new(),
            returnables: AHashMap::new(),
            evaluator_values: AHashMap::from_iter([(13, evaluator)]),
        };

        let _mmap_data = detached_mutable_to_mmap_data(mutable_data, Vec::new());

        assert!(evaluator_weak.upgrade().is_none());
    }
}
