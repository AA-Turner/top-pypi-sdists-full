use std::{
    collections::HashMap,
    fs::{create_dir_all, File, OpenOptions},
    io::{self, BufWriter, Write},
    path::Path,
    sync::Arc,
};

use ahash::AHashSet;
use lazy_static::lazy_static;
use parking_lot::Mutex;
use rkyv::ser::{allocator::Arena, writer::IoWriter, Positional};
#[cfg(unix)]
use std::os::unix::fs::PermissionsExt;

use crate::{
    evaluation::dynamic_string::DynamicString,
    interned_string::InternedString,
    interned_values::{
        mmap_data_v2::{MmapDataV2, MmapEvaluatorValue, MmapSpec},
        mmap_sync::{MmapConfigResponse, MmapResolvedUpdate, MmapSyncCursor, MmapWriteOutcome},
    },
    log_d,
    networking::ResponseData,
    specs_response::{
        spec_types::{Condition, SpecsResponseFull},
        specs_hash_map::SpecsHashMap,
    },
    StatsigErr,
};

use super::{
    mmap_manifest::write_mmap_manifest, take_mutable_data, MmapDataV1, MutableData, IMMORTAL_DATA,
    TAG,
};
#[cfg(test)]
use super::{try_parse_as_json, try_parse_as_proto};

const MMAP_WRITE_BUFFER_CAPACITY: usize = 1024 * 1024;

lazy_static! {
    static ref MMAP_WRITE_LOCK: Mutex<()> = Mutex::new(());
}

#[allow(dead_code)]
pub(super) fn write_mmap_specs(
    specs_responses: Vec<SpecsResponseFull>,
    path: &Path,
) -> Result<(), StatsigErr> {
    if let Some(parent) = path.parent() {
        create_dir_all(parent).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    }

    let mmap_data = mutable_to_mmap_data(specs_responses);
    publish_mmap_data(mmap_data, path, |data, file| {
        serialize_mmap_data(data, file)
    })
}

fn publish_mmap_data(
    mmap_data: MmapDataV1,
    path: &Path,
    serialize: impl FnOnce(&MmapDataV1, &mut File) -> Result<usize, StatsigErr>,
) -> Result<(), StatsigErr> {
    let mut file = new_mmap_temp_file(path)?;
    let archived_len = serialize(&mmap_data, file.as_file_mut())?;
    drop(mmap_data);
    sync_mmap_temp_file(&file)?;
    persist_mmap_temp_file(file, path)?;

    log_d!(
        TAG,
        "Wrote {} bytes to mmap file {}",
        archived_len,
        path.display()
    );

    Ok(())
}

pub(super) fn write_mmap_artifacts(
    response_data: &mut ResponseData,
    previous: Option<&MmapSyncCursor>,
    v1_path: &Path,
    v2_path: &Path,
    manifest_path: &Path,
) -> Result<MmapWriteOutcome, StatsigErr> {
    let _write_guard = MMAP_WRITE_LOCK.lock();
    let Some(MmapResolvedUpdate { specs, cursor }) =
        MmapConfigResponse::new(response_data)?.resolve(previous)?
    else {
        return Ok(MmapWriteOutcome::NoUpdate);
    };

    let mmap_v2 = mutable_to_mmap_data_v2(vec![specs])?;

    let mut v2_file = new_mmap_temp_file(v2_path)?;
    let v2_bytes_written = serialize_mmap_v2_data(&mmap_v2, v2_file.as_file_mut())?;
    sync_mmap_temp_file(&v2_file)?;

    let MmapDataV2 {
        strings,
        returnables,
        ..
    } = mmap_v2;
    let mmap_v1 = MmapDataV1 {
        format_version: MmapDataV1::FORMAT_VERSION,
        strings,
        returnables,
    };
    let mut v1_file = new_mmap_temp_file(v1_path)?;
    let v1_bytes_written = serialize_mmap_data(&mmap_v1, v1_file.as_file_mut())?;
    drop(mmap_v1);
    sync_mmap_temp_file(&v1_file)?;

    let v1_file = persist_mmap_temp_file(v1_file, v1_path)?;
    let v2_file = persist_mmap_temp_file(v2_file, v2_path)?;
    // The manifest commits the pair. Missing or mismatched manifests make
    // readers fall back to V1, including after a V1-only rollback.
    write_mmap_manifest(manifest_path, Some(&v1_file), &v2_file)?;

    log_d!(
        TAG,
        "Wrote {v1_bytes_written} bytes to {}",
        v1_path.display()
    );
    log_d!(
        TAG,
        "Wrote {v2_bytes_written} bytes to {}",
        v2_path.display()
    );

    Ok(MmapWriteOutcome::Published(cursor))
}

#[cfg_attr(not(test), allow(dead_code))]
fn write_mmap_v2_specs(
    specs_responses: Vec<SpecsResponseFull>,
    path: &Path,
) -> Result<(), StatsigErr> {
    let mmap_data = mutable_to_mmap_data_v2(specs_responses)?;
    let mut file = new_mmap_temp_file(path)?;
    let bytes_written = serialize_mmap_v2_data(&mmap_data, file.as_file_mut())?;
    drop(mmap_data);
    sync_mmap_temp_file(&file)?;
    persist_mmap_temp_file(file, path)?;

    log_d!(
        TAG,
        "Wrote {} bytes to mmap v2 file {}",
        bytes_written,
        path.display()
    );

    Ok(())
}

fn new_mmap_temp_file(path: &Path) -> Result<tempfile::NamedTempFile, StatsigErr> {
    let parent = path
        .parent()
        .ok_or_else(|| StatsigErr::FileError("Mmap path has no parent".to_string()))?;
    create_dir_all(parent).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    tempfile::NamedTempFile::new_in(parent)
        .map_err(|error| StatsigErr::FileError(error.to_string()))
}

fn sync_mmap_temp_file(file: &tempfile::NamedTempFile) -> Result<(), StatsigErr> {
    #[cfg(unix)]
    file.as_file()
        .set_permissions(std::fs::Permissions::from_mode(0o644))
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    file.as_file()
        .sync_all()
        .map_err(|error| StatsigErr::FileError(error.to_string()))
}

fn persist_mmap_temp_file(file: tempfile::NamedTempFile, path: &Path) -> Result<File, StatsigErr> {
    file.persist(path)
        .map_err(|error| StatsigErr::FileError(error.error.to_string()))
}

pub(super) async fn acquire_mmap_write_lock(path: &Path) -> Result<File, StatsigErr> {
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

#[cfg(test)]
pub(crate) fn acquire_mmap_write_lock_for_test(path: &Path) -> Result<File, StatsigErr> {
    acquire_mmap_write_lock_blocking(path)
}

#[cfg(test)]
pub(crate) fn write_mmap_v2_for_test(data: &[u8], path: &Path) -> Result<(), StatsigErr> {
    let specs = try_parse_as_json(data).or_else(|_| try_parse_as_proto(data))?;
    write_mmap_v2_specs(vec![specs], path)
}

fn serialize_mmap_data<W: Write>(mmap_data: &MmapDataV1, output: W) -> Result<usize, StatsigErr> {
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

#[allow(dead_code)]
fn mutable_to_mmap_data(specs_responses: Vec<SpecsResponseFull>) -> MmapDataV1 {
    detached_mutable_to_mmap_data(take_mutable_data(), specs_responses)
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

    MmapDataV1 {
        format_version: MmapDataV1::FORMAT_VERSION,
        strings,
        returnables,
    }
}

#[cfg_attr(not(test), allow(dead_code))]
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
            layer_configs,
            ..
        } = response;
        insert_mmap_specs(feature_gates, &mut mmap_data.feature_gates);
        insert_mmap_specs(dynamic_configs, &mut mmap_data.dynamic_configs);
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
            let Some(value) = immortal.returnables.get(hash) else {
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
mod tests {
    use memmap2::Mmap;
    use rkyv::{Archive, Serialize as RkyvSerialize};

    use crate::evaluation::{
        evaluator_value::{EvaluatorValueType, MemoizedEvaluatorValue},
        rkyv_value::{ArchivedRkyvValue, RkyvValue},
    };

    use super::*;

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

    struct FailAfterWriter<W> {
        inner: W,
        remaining: usize,
    }

    impl<W> FailAfterWriter<W> {
        fn new(inner: W, remaining: usize) -> Self {
            Self { inner, remaining }
        }
    }

    impl<W: Write> Write for FailAfterWriter<W> {
        fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
            if self.remaining == 0 {
                return Err(io::Error::other("injected mmap write failure"));
            }

            let limit = self.remaining.min(buffer.len());
            let written = self.inner.write(&buffer[..limit])?;
            self.remaining -= written;
            Ok(written)
        }

        fn flush(&mut self) -> io::Result<()> {
            self.inner.flush()
        }
    }

    struct FailOnFlushWriter<W> {
        inner: W,
    }

    struct WriteZeroWriter;

    impl Write for WriteZeroWriter {
        fn write(&mut self, _buffer: &[u8]) -> io::Result<usize> {
            Ok(0)
        }

        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }

    impl<W> FailOnFlushWriter<W> {
        fn new(inner: W) -> Self {
            Self { inner }
        }
    }

    impl<W: Write> Write for FailOnFlushWriter<W> {
        fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
            self.inner.write(buffer)
        }

        fn flush(&mut self) -> io::Result<()> {
            Err(io::Error::other("injected mmap flush failure"))
        }
    }

    fn arc_backed_v1_source() -> MmapDataV1 {
        let returnable = HashMap::from([("enabled".to_string(), RkyvValue::Bool(true))]);
        MmapDataV1 {
            format_version: MmapDataV1::FORMAT_VERSION,
            strings: vec![(7, Arc::new("v1-string".to_string()))],
            returnables: vec![(11, Arc::new(returnable))],
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
        let current =
            rkyv::access::<super::super::ArchivedMmapDataV1, rkyv::rancor::Error>(&bytes).unwrap();

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
            strings: vec![(7, string)],
            returnables: vec![(11, returnable)],
            evaluator_values: Vec::new(),
        };

        let mmap_data = detached_mutable_to_mmap_data(mutable_data, Vec::new());

        assert!(Arc::ptr_eq(
            &mmap_data
                .strings
                .iter()
                .find(|(hash, _)| *hash == 7)
                .unwrap()
                .1,
            &other_string_owner
        ));
        assert!(Arc::ptr_eq(
            &mmap_data
                .returnables
                .iter()
                .find(|(hash, _)| *hash == 11)
                .unwrap()
                .1,
            &other_returnable_owner
        ));
    }

    #[test]
    fn conversion_releases_evaluator_cache_before_returning_archive_input() {
        let evaluator = Arc::new(MemoizedEvaluatorValue::new(EvaluatorValueType::Null));
        let evaluator_weak = Arc::downgrade(&evaluator);
        let mutable_data = MutableData {
            strings: Vec::new(),
            returnables: Vec::new(),
            evaluator_values: vec![(13, evaluator)],
        };

        let _mmap_data = detached_mutable_to_mmap_data(mutable_data, Vec::new());

        assert!(evaluator_weak.upgrade().is_none());
    }

    #[test]
    fn previous_v1_reader_reads_streamed_arc_backed_archive() {
        let mut file = tempfile::NamedTempFile::new().unwrap();

        let archived_len =
            serialize_mmap_data(&arc_backed_v1_source(), file.as_file_mut()).unwrap();

        assert_eq!(
            archived_len,
            file.as_file().metadata().unwrap().len() as usize
        );
        let mmap = unsafe { Mmap::map(file.as_file()).unwrap() };
        let previous =
            rkyv::access::<PreviousArchivedMmapDataV1, rkyv::rancor::Error>(&mmap).unwrap();

        assert_eq!(previous.format_version(), MmapDataV1::FORMAT_VERSION);
        assert_eq!(previous.string(7), Some("v1-string"));
        assert!(matches!(
            previous.returnable(11, "enabled"),
            Some(ArchivedRkyvValue::Bool(true))
        ));
    }

    #[test]
    fn write_failure_is_file_error_and_preserves_published_artifact() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("published.mmap");
        std::fs::write(&path, b"previous artifact").unwrap();
        let mmap_data = MmapDataV1 {
            format_version: MmapDataV1::FORMAT_VERSION,
            strings: vec![(1, Arc::new("x".repeat(MMAP_WRITE_BUFFER_CAPACITY * 2)))],
            returnables: Vec::new(),
        };

        let result = publish_mmap_data(mmap_data, &path, |data, file| {
            serialize_mmap_data(data, FailAfterWriter::new(file, 4096))
        });

        assert!(matches!(
            result,
            Err(StatsigErr::FileError(message))
                if message.contains("injected mmap write failure")
        ));
        assert_eq!(std::fs::read(&path).unwrap(), b"previous artifact");
        assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
    }

    #[test]
    fn flush_failure_is_file_error_and_preserves_published_artifact() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("published.mmap");
        std::fs::write(&path, b"previous artifact").unwrap();

        let result = publish_mmap_data(MmapDataV1::default(), &path, |data, file| {
            serialize_mmap_data(data, FailOnFlushWriter::new(file))
        });

        assert!(matches!(
            result,
            Err(StatsigErr::FileError(message))
                if message.contains("injected mmap flush failure")
        ));
        assert_eq!(std::fs::read(&path).unwrap(), b"previous artifact");
        assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
    }

    #[test]
    fn write_zero_during_serialization_is_a_file_error() {
        let mmap_data = MmapDataV1 {
            format_version: MmapDataV1::FORMAT_VERSION,
            strings: vec![(1, Arc::new("x".repeat(MMAP_WRITE_BUFFER_CAPACITY * 2)))],
            returnables: Vec::new(),
        };

        let result = serialize_mmap_data(&mmap_data, WriteZeroWriter);

        assert!(matches!(result, Err(StatsigErr::FileError(_))));
    }
}
