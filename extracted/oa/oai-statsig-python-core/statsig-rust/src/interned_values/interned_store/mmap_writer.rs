use std::{
    collections::HashMap,
    fs::{File, OpenOptions, create_dir_all},
    io::{self, BufWriter, Write},
    path::Path,
    sync::Arc,
};

use ahash::AHashSet;
use rkyv::ser::{Positional, allocator::Arena, writer::IoWriter};
#[cfg(unix)]
use std::os::unix::fs::PermissionsExt;
use tokio::sync::Mutex;

use crate::{
    StatsigErr, StatsigOptions,
    evaluation::dynamic_string::DynamicString,
    interned_string::InternedString,
    interned_values::{
        mmap_data_v2::{MmapDataV2, MmapEvaluatorValue, MmapSpec},
        mmap_sync::{
            MmapResolvedUpdate, MmapSyncCursor, MmapWriteOutcome, resolve_json_response,
            resolve_parsed_response,
        },
    },
    log_d,
    networking::ResponseData,
    specs_adapter::{
        SpecsInfo, SpecsSyncTrigger, StatsigHttpSpecsAdapter,
        remote_config_value_hydrator::{
            MmapRemoteValueProof, StoreHydrationOptions, VerifiedRemoteValue,
        },
    },
    specs_response::{
        parse_options::{SpecsResponseParseOptions, with_parse_options},
        proto_compression::is_compressed_protobuf_response,
        proto_specs::{
            ProtobufStoreParseBase, ProtobufUpdate, SpecsFieldChecksums,
            VerifiedRemoteConfigValues, prepare_protobuf_store_update,
        },
        spec_types::{Condition, SpecsResponseFull},
        specs_hash_map::SpecsHashMap,
    },
    utils::try_release_unused_heap_memory,
};

use super::{
    IMMORTAL_DATA, MmapProjectId, MutableData, TAG, mmap_lock_path_for_sdk_key,
    mmap_manifest::write_mmap_manifest_with_remote_values, mmap_manifest_path_for_sdk_key,
    mmap_v2_path_for_sdk_key, take_mutable_data,
};

const MMAP_WRITE_BUFFER_CAPACITY: usize = 1024 * 1024;

// Parsing populates process-global intern tables that graph construction drains.
// Take this lock before hydration to avoid waiting for the graph while holding
// hydration admission. Hold it through publication to limit synchronous file
// work to one async runtime worker.
static MMAP_GRAPH_WRITE_LOCK: Mutex<()> = Mutex::const_new(());

pub(super) async fn fetch_and_write_mmap(
    sdk_key: &str,
    options: Option<&StatsigOptions>,
    previous: Option<&MmapSyncCursor>,
) -> Result<MmapWriteOutcome, StatsigErr> {
    let result = {
        // Hold the cross-process per-key lock from fetch through publication so
        // a delayed response cannot overwrite a newer generation.
        let _key_lock = acquire_mmap_write_lock(&mmap_lock_path_for_sdk_key(sdk_key)).await?;
        let adapter = StatsigHttpSpecsAdapter::new(sdk_key, options, None);
        let mut specs_info = SpecsInfo::empty();
        if let Some(previous) = previous {
            specs_info.lcut = Some(previous.lcut);
            specs_info.checksum = previous.checksum.clone();
        }
        let response = adapter
            .fetch_specs_from_network(specs_info, SpecsSyncTrigger::Manual)
            .await
            .map_err(StatsigErr::NetworkError)?;

        let project = MmapProjectId::for_sdk_key(sdk_key);
        let _graph_lock = MMAP_GRAPH_WRITE_LOCK.lock().await;
        match hydrate_and_resolve_mmap_response(
            adapter,
            response.data,
            &response.request_url,
            project,
            previous,
        )
        .await?
        {
            Some((resolved, verified)) => write_mmap_artifact(resolved, verified, sdk_key, project),
            None => Ok(MmapWriteOutcome::NoUpdate),
        }
    };
    // Trim only after successful response resolution and after dropping both locks.
    try_release_unused_heap_memory();
    result
}

// Own the source response and adapter so both are dropped before archive construction.
async fn hydrate_and_resolve_mmap_response(
    adapter: StatsigHttpSpecsAdapter,
    mut data: ResponseData,
    source_url: &str,
    project: MmapProjectId,
    previous: Option<&MmapSyncCursor>,
) -> Result<Option<(MmapResolvedUpdate, VerifiedRemoteConfigValues)>, StatsigErr> {
    let hydration_options = StoreHydrationOptions::new(source_url, project)
        .with_sync_trigger(Some(SpecsSyncTrigger::Manual));
    let (specs, verified) = if is_compressed_protobuf_response(&data) {
        hydrate_protobuf_mmap_response(&adapter, &mut data, hydration_options).await?
    } else {
        let hydrated = adapter
            .remote_config_value_hydrator()
            .prepare_json_store_update(
                &mut data,
                hydration_options,
                &VerifiedRemoteConfigValues::new(),
                None,
            )
            .await?;
        let Some(hydrated) = hydrated else {
            let parse_options = SpecsResponseParseOptions::for_store(false);
            return Ok(with_parse_options(parse_options, || {
                resolve_json_response(&mut data, previous)
            })?
            .map(|resolved| (resolved, VerifiedRemoteConfigValues::new())));
        };
        (*hydrated.values, hydrated.verified_remote_values)
    };
    Ok(resolve_parsed_response(specs, previous)?.map(|resolved| (resolved, verified)))
}

async fn hydrate_protobuf_mmap_response(
    adapter: &StatsigHttpSpecsAdapter,
    data: &mut ResponseData,
    hydration_options: StoreHydrationOptions<'_>,
) -> Result<(SpecsResponseFull, VerifiedRemoteConfigValues), StatsigErr> {
    let current = SpecsResponseFull::default();
    let mut specs = SpecsResponseFull::default();
    let hydrated = prepare_protobuf_store_update(
        adapter.ops_stats(),
        ProtobufStoreParseBase::new(
            &current,
            Default::default(),
            &SpecsFieldChecksums::from_specs(&current),
            &VerifiedRemoteConfigValues::new(),
        ),
        &mut specs,
        data,
        adapter.remote_config_value_hydrator(),
        hydration_options,
    )
    .await?;
    if !matches!(hydrated.update, ProtobufUpdate::Materialized { .. }) {
        return Err(StatsigErr::InvalidOperation(
            "Mmap protobuf fetch did not produce a full snapshot".to_string(),
        ));
    }
    Ok((specs, hydrated.verified_remote_values))
}

fn write_mmap_artifact(
    MmapResolvedUpdate { specs, cursor }: MmapResolvedUpdate,
    verified: VerifiedRemoteConfigValues,
    sdk_key: &str,
    project: MmapProjectId,
) -> Result<MmapWriteOutcome, StatsigErr> {
    let proofs = mmap_remote_value_proofs(&specs, verified);
    let mmap_v2 = mutable_to_mmap_data_v2(vec![specs])?;
    let proofs = proofs_referenced_by_archive(proofs, &mmap_v2);
    let path = mmap_v2_path_for_sdk_key(sdk_key);
    let (file, bytes_written) = serialize_mmap_to_temp_file(mmap_v2, &path, |data, file| {
        serialize_mmap_v2_data(data, file)
    })?;
    let file = commit_mmap_temp_file(file, &path)?;
    write_mmap_manifest_with_remote_values(
        &mmap_manifest_path_for_sdk_key(sdk_key),
        &file,
        project,
        proofs,
    )?;
    log_d!(TAG, "Wrote {bytes_written} bytes to {}", path.display());
    Ok(MmapWriteOutcome::Published(cursor))
}

fn mmap_remote_value_proofs(
    specs: &SpecsResponseFull,
    verified: VerifiedRemoteConfigValues,
) -> HashMap<String, MmapRemoteValueProof> {
    let mut proofs = HashMap::new();
    for (name, values) in verified {
        if values.is_empty() {
            continue;
        }
        let Some(spec) = specs.dynamic_configs.get(&name) else {
            continue;
        };
        let spec = spec.as_spec_ref();
        // Index each installed backing allocation once, including the variant,
        // so candidate filtering is linear in the rules plus verified values.
        let installed = std::iter::once(&spec.default_value)
            .chain(spec.rules.iter().map(|rule| &rule.return_value))
            .map(VerifiedRemoteValue::backing_identity)
            .collect::<AHashSet<_>>();
        for value in values.values() {
            // Export only values actually installed in the published config,
            // never an unreferenced or replaced hydration candidate.
            if installed.contains(&VerifiedRemoteValue::backing_identity(&value.value)) {
                if let Some(proof) = value.mmap_proof() {
                    proofs.insert(proof.sha256.clone(), proof);
                }
            }
        }
    }
    proofs
}

fn proofs_referenced_by_archive(
    proofs: HashMap<String, MmapRemoteValueProof>,
    archive: &MmapDataV2,
) -> Vec<MmapRemoteValueProof> {
    if proofs.is_empty() {
        return Vec::new();
    }
    let handles = archive
        .returnables
        .iter()
        .map(|(hash, _)| *hash)
        .collect::<AHashSet<_>>();
    proofs
        .into_values()
        .filter(|proof| handles.contains(&proof.returnable_hash))
        .collect()
}

fn serialize_mmap_to_temp_file(
    mmap_data: MmapDataV2,
    path: &Path,
    serialize: impl FnOnce(&MmapDataV2, &mut File) -> Result<usize, StatsigErr>,
) -> Result<(tempfile::NamedTempFile, usize), StatsigErr> {
    let mut file = new_mmap_temp_file(path)?;
    let bytes_written = serialize(&mmap_data, file.as_file_mut())?;
    Ok((file, bytes_written))
}

fn new_mmap_temp_file(path: &Path) -> Result<tempfile::NamedTempFile, StatsigErr> {
    let parent = path
        .parent()
        .ok_or_else(|| StatsigErr::FileError("Mmap path has no parent".to_string()))?;
    create_dir_all(parent).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    tempfile::NamedTempFile::new_in(parent)
        .map_err(|error| StatsigErr::FileError(error.to_string()))
}

fn commit_mmap_temp_file(file: tempfile::NamedTempFile, path: &Path) -> Result<File, StatsigErr> {
    #[cfg(unix)]
    file.as_file()
        .set_permissions(std::fs::Permissions::from_mode(0o644))
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    file.as_file()
        .sync_all()
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    file.persist(path)
        .map_err(|error| StatsigErr::FileError(error.error.to_string()))
}

async fn acquire_mmap_write_lock(path: &Path) -> Result<File, StatsigErr> {
    let path = path.to_path_buf();
    tokio::task::spawn_blocking(move || acquire_mmap_write_lock_blocking(&path))
        .await
        .map_err(|error| StatsigErr::LockFailure(error.to_string()))?
}

fn acquire_mmap_write_lock_blocking(path: &Path) -> Result<File, StatsigErr> {
    let parent = path
        .parent()
        .ok_or_else(|| StatsigErr::FileError("Mmap lock path has no parent".to_string()))?;
    create_dir_all(parent).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let file = OpenOptions::new()
        .create(true)
        .truncate(false)
        .read(true)
        .write(true)
        .open(path)
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    fs4::FileExt::lock(&file).map_err(|error| StatsigErr::LockFailure(error.to_string()))?;
    Ok(file)
}

fn serialize_mmap_v2_data<W: Write>(
    mmap_data: &MmapDataV2,
    output: W,
) -> Result<usize, StatsigErr> {
    let buffered = BufWriter::with_capacity(MMAP_WRITE_BUFFER_CAPACITY, output);
    let mut recording = ErrorRecordingWriter::new(buffered);
    let mut arena = Arena::new();

    let (archive_result, archived_len) = {
        let mut writer = IoWriter::new(&mut recording);
        let archive_result = rkyv::api::high::to_bytes_in_with_alloc::<_, _, rkyv::rancor::Error>(
            mmap_data,
            &mut writer,
            arena.acquire(),
        )
        .map(|_| ());
        let archived_len = writer.pos();
        (archive_result, archived_len)
    };

    if let Err(error) = archive_result {
        let mapped = match recording.take_error() {
            Some(io_error) => StatsigErr::FileError(io_error.to_string()),
            None => StatsigErr::SerializationError(error.to_string()),
        };
        drop(recording);
        drop(arena);
        return Err(mapped);
    }

    recording
        .flush()
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    drop(recording);
    drop(arena);
    Ok(archived_len)
}

struct ErrorRecordingWriter<W> {
    inner: W,
    error: Option<io::Error>,
}

impl<W> ErrorRecordingWriter<W> {
    fn new(inner: W) -> Self {
        Self { inner, error: None }
    }

    fn take_error(&mut self) -> Option<io::Error> {
        self.error.take()
    }

    fn record(&mut self, error: &io::Error) {
        if self.error.is_none() {
            self.error = Some(io::Error::new(error.kind(), error.to_string()));
        }
    }
}

impl<W: Write> Write for ErrorRecordingWriter<W> {
    fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
        match self.inner.write(buffer) {
            Ok(written) => Ok(written),
            Err(error) => {
                self.record(&error);
                Err(error)
            }
        }
    }

    fn write_all(&mut self, buffer: &[u8]) -> io::Result<()> {
        match self.inner.write_all(buffer) {
            Ok(()) => Ok(()),
            Err(error) => {
                self.record(&error);
                Err(error)
            }
        }
    }

    fn flush(&mut self) -> io::Result<()> {
        match self.inner.flush() {
            Ok(()) => Ok(()),
            Err(error) => {
                self.record(&error);
                Err(error)
            }
        }
    }
}

pub(super) fn mutable_to_mmap_data_v2(
    specs_responses: Vec<SpecsResponseFull>,
) -> Result<MmapDataV2, StatsigErr> {
    let mutable_data = take_mutable_data();

    detached_mutable_to_mmap_data_v2(mutable_data, specs_responses)
}

fn detached_mutable_to_mmap_data_v2(
    mutable_data: MutableData,
    specs_responses: Vec<SpecsResponseFull>,
) -> Result<MmapDataV2, StatsigErr> {
    let MutableData {
        strings,
        returnables,
        evaluator_values,
    } = mutable_data;
    let mut mmap_data = MmapDataV2::default();
    mmap_data.evaluator_values.reserve(evaluator_values.len());
    let mut referenced_string_hashes = AHashSet::new();
    let mut referenced_returnable_hashes = AHashSet::new();
    let mut referenced_evaluator_values = Vec::new();

    for response in specs_responses {
        collect_condition_references(
            &response,
            &mut referenced_string_hashes,
            &mut referenced_evaluator_values,
        )?;
        let SpecsResponseFull {
            feature_gates,
            dynamic_configs,
            mut layer_configs,
            ..
        } = response;
        insert_mmap_specs(feature_gates, &mut mmap_data.feature_gates);
        insert_mmap_specs(dynamic_configs, &mut mmap_data.dynamic_configs);
        layer_configs.0.retain(|_, spec| {
            spec.as_spec_ref()
                .rules
                .iter()
                .all(|rule| rule.shared_control_experiments.is_none())
        });
        insert_mmap_specs(layer_configs, &mut mmap_data.layer_configs);
    }

    for (hash, value) in evaluator_values {
        mmap_data
            .evaluator_values
            .insert(hash, MmapEvaluatorValue::from_owned(value.as_ref())?);
    }
    for (hash, value) in referenced_evaluator_values {
        mmap_data.evaluator_values.entry(hash).or_insert(value);
    }

    mmap_data.returnables = returnables;
    mmap_data.strings = strings;
    collect_mmap_references(
        &mmap_data,
        &mut referenced_string_hashes,
        &mut referenced_returnable_hashes,
    );
    append_immortal_entries(
        &mut mmap_data,
        &referenced_string_hashes,
        &referenced_returnable_hashes,
    );

    Ok(mmap_data)
}

fn collect_condition_references(
    response: &SpecsResponseFull,
    string_hashes: &mut AHashSet<u64>,
    evaluator_values: &mut Vec<(u64, MmapEvaluatorValue)>,
) -> Result<(), StatsigErr> {
    for (name, condition) in &response.condition_map {
        collect_string(name, string_hashes);
        collect_condition_strings(condition, string_hashes);
        if let Some(value) = &condition.target_value {
            evaluator_values.push((value.hash, MmapEvaluatorValue::from_owned(value.as_ref())?));
        }
    }
    Ok(())
}

fn collect_condition_strings(condition: &Condition, hashes: &mut AHashSet<u64>) {
    collect_string(&condition.condition_type, hashes);
    if let Some(value) = &condition.operator {
        collect_string(value, hashes);
    }
    if let Some(value) = &condition.field {
        collect_dynamic_string(value, hashes);
    }
    if let Some(values) = &condition.additional_values {
        for (key, value) in values {
            collect_string(key, hashes);
            collect_string(value, hashes);
        }
    }
    collect_dynamic_string(&condition.id_type, hashes);
    if let Some(value) = &condition.checksum {
        collect_string(value, hashes);
    }
}

fn collect_string(value: &InternedString, hashes: &mut AHashSet<u64>) {
    hashes.insert(value.hash);
}

fn collect_dynamic_string(value: &DynamicString, hashes: &mut AHashSet<u64>) {
    collect_string(&value.value, hashes);
    collect_string(&value.lowercased_value, hashes);
}

fn collect_mmap_references(
    mmap_data: &MmapDataV2,
    string_hashes: &mut AHashSet<u64>,
    returnable_hashes: &mut AHashSet<u64>,
) {
    for values in [
        &mmap_data.feature_gates,
        &mmap_data.dynamic_configs,
        &mmap_data.layer_configs,
    ] {
        string_hashes.extend(values.keys());
        for spec in values.values() {
            spec.collect_references(string_hashes, returnable_hashes);
        }
    }
    for value in mmap_data.evaluator_values.values() {
        value.collect_string_hashes(string_hashes);
    }
}

fn append_immortal_entries(
    mmap_data: &mut MmapDataV2,
    referenced_string_hashes: &AHashSet<u64>,
    referenced_returnable_hashes: &AHashSet<u64>,
) {
    let Some(immortal) = IMMORTAL_DATA.get() else {
        return;
    };

    let mut string_hashes = mmap_data
        .strings
        .iter()
        .map(|(hash, _)| *hash)
        .collect::<AHashSet<_>>();
    for hash in referenced_string_hashes {
        if string_hashes.insert(*hash) {
            let Some(value) = immortal.strings.get(hash) else {
                continue;
            };
            mmap_data
                .strings
                .push((*hash, Arc::new((*value).to_owned())));
        }
    }

    let mut returnable_hashes = mmap_data
        .returnables
        .iter()
        .map(|(hash, _)| *hash)
        .collect::<AHashSet<_>>();
    for hash in referenced_returnable_hashes {
        if returnable_hashes.insert(*hash) {
            let Some((value, _)) = immortal.returnables.get(hash) else {
                continue;
            };
            mmap_data
                .returnables
                .push((*hash, Arc::new((*value).clone())));
        }
    }
}

fn insert_mmap_specs(source: SpecsHashMap, destination: &mut HashMap<u64, MmapSpec>) {
    destination.reserve(source.0.len());
    for (name, spec) in source.0 {
        destination.insert(name.hash, MmapSpec::from_owned(spec.as_spec_ref()));
    }
}

#[cfg(test)]
#[path = "mmap_writer_tests.rs"]
pub(super) mod tests;
