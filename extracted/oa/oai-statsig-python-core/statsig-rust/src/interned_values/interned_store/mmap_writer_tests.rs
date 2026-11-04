use memmap2::Mmap;
use rkyv::{collections::swiss_table::ArchivedHashMap, string::ArchivedString};
use serde_json::json;

use crate::{
    DynamicReturnable,
    evaluation::{
        dynamic_returnable::DynamicReturnableValue,
        evaluator_value::{EvaluatorValueType, MemoizedEvaluatorValue},
        rkyv_value::{ArchivedRkyvValue, RkyvValue},
    },
    specs_adapter::remote_config_value_hydrator::VerifiedRemoteValues,
    specs_response::{
        spec_types::{Rule, Spec},
        specs_hash_map::SpecPointer,
    },
};

use super::super::{try_parse_as_json, try_parse_as_proto};
use super::*;

fn write_mmap_v2_specs(
    specs_responses: Vec<SpecsResponseFull>,
    path: &Path,
) -> Result<(), StatsigErr> {
    let mmap_data = mutable_to_mmap_data_v2(specs_responses)?;
    let (file, bytes_written) = serialize_mmap_to_temp_file(mmap_data, path, |data, file| {
        serialize_mmap_v2_data(data, file)
    })?;
    commit_mmap_temp_file(file, path)?;

    log_d!(
        TAG,
        "Wrote {} bytes to mmap v2 file {}",
        bytes_written,
        path.display()
    );

    Ok(())
}

pub(crate) fn acquire_mmap_write_lock_for_test(path: &Path) -> Result<File, StatsigErr> {
    acquire_mmap_write_lock_blocking(path)
}

pub(crate) fn write_mmap_v2_for_test(data: &[u8], path: &Path) -> Result<(), StatsigErr> {
    let specs = try_parse_as_json(data).or_else(|_| try_parse_as_proto(data))?;
    write_mmap_v2_specs(vec![specs], path)
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

fn arc_backed_v2_source() -> MmapDataV2 {
    let returnable = HashMap::from([("enabled".to_string(), RkyvValue::Bool(true))]);
    MmapDataV2 {
        strings: vec![(7, Arc::new("v2-string".to_string()))],
        returnables: vec![(11, Arc::new(returnable))],
        ..MmapDataV2::default()
    }
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

    let mmap_data = detached_mutable_to_mmap_data_v2(mutable_data, Vec::new()).unwrap();

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

    let _mmap_data = detached_mutable_to_mmap_data_v2(mutable_data, Vec::new()).unwrap();

    assert!(evaluator_weak.upgrade().is_none());
}

#[test]
fn v2_archive_is_streamed_to_file() {
    let mut file = tempfile::NamedTempFile::new().unwrap();

    let archived_len = serialize_mmap_v2_data(&arc_backed_v2_source(), file.as_file_mut()).unwrap();

    assert_eq!(
        archived_len,
        file.as_file().metadata().unwrap().len() as usize
    );
    let mmap = unsafe { Mmap::map(file.as_file()).unwrap() };
    let archived = rkyv::access::<
        crate::interned_values::mmap_data_v2::ArchivedMmapDataV2,
        rkyv::rancor::Error,
    >(&mmap)
    .unwrap();

    assert_eq!(
        archived.format_version.to_native(),
        MmapDataV2::FORMAT_VERSION
    );
    assert_eq!(
        archived
            .strings
            .get(&rkyv::primitive::ArchivedU64::from_native(7))
            .map(|value| value.as_str()),
        Some("v2-string")
    );
    assert!(matches!(
        archived
            .returnables
            .get(&rkyv::primitive::ArchivedU64::from_native(11))
            .and_then(|returnable| returnable.get("enabled")),
        Some(ArchivedRkyvValue::Bool(true))
    ));
}

#[test]
fn write_failure_is_file_error_and_preserves_published_artifact() {
    let directory = tempfile::tempdir().unwrap();
    let path = directory.path().join("published.mmap");
    std::fs::write(&path, b"previous artifact").unwrap();
    let mmap_data = MmapDataV2 {
        strings: vec![(1, Arc::new("x".repeat(MMAP_WRITE_BUFFER_CAPACITY * 2)))],
        ..MmapDataV2::default()
    };

    let result = serialize_mmap_to_temp_file(mmap_data, &path, |data, file| {
        serialize_mmap_v2_data(data, FailAfterWriter::new(file, 4096))
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

    let result = serialize_mmap_to_temp_file(MmapDataV2::default(), &path, |data, file| {
        serialize_mmap_v2_data(data, FailOnFlushWriter::new(file))
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
    let mmap_data = MmapDataV2 {
        strings: vec![(1, Arc::new("x".repeat(MMAP_WRITE_BUFFER_CAPACITY * 2)))],
        ..MmapDataV2::default()
    };

    let result = serialize_mmap_v2_data(&mmap_data, WriteZeroWriter);

    assert!(matches!(result, Err(StatsigErr::FileError(_))));
}

fn archived_value(hash: u64) -> DynamicReturnable {
    let values = HashMap::from([("id".to_string(), RkyvValue::String(hash.to_string()))]);
    let bytes = Box::leak(Box::new(
        rkyv::to_bytes::<rkyv::rancor::Error>(&values).unwrap(),
    ));
    let archived = rkyv::access::<
        ArchivedHashMap<ArchivedString, ArchivedRkyvValue>,
        rkyv::rancor::Error,
    >(bytes)
    .unwrap();
    DynamicReturnable::from_archived_value(hash, archived)
}

fn verified_value(index: u64, value: DynamicReturnable) -> Arc<VerifiedRemoteValue> {
    Arc::new(
        VerifiedRemoteValue::from_verified_mmap(
            &MmapRemoteValueProof {
                sha256: format!("{index:064x}"),
                byte_length: 20,
                compression: "none".to_string(),
                returnable_hash: value.hash,
                json_sidecar_reuse_safe: true,
            },
            value,
        )
        .unwrap(),
    )
}

fn spec(default_value: DynamicReturnable, rule_values: Vec<DynamicReturnable>) -> Spec {
    let mut spec: Spec = serde_json::from_value(json!({
        "type": "dynamic_config", "salt": "writer-proof", "enabled": true,
        "defaultValue": false, "rules": [], "idType": "userID", "entity": "dynamic_config",
    }))
    .unwrap();
    spec.default_value = default_value;
    spec.rules = rule_values
        .into_iter()
        .map(|return_value| {
            let mut rule: Rule = serde_json::from_value(json!({
                "name": "remote", "id": "remote", "passPercentage": 100,
                "returnValue": false, "conditions": [], "idType": "userID",
            }))
            .unwrap();
            rule.return_value = return_value;
            rule
        })
        .collect();
    spec
}

fn specs_with_config(spec: Spec) -> SpecsResponseFull {
    let mut specs = SpecsResponseFull::default();
    specs.dynamic_configs.insert(
        InternedString::from_str_ref("remote_config"),
        SpecPointer::from_spec(spec),
    );
    specs
}

fn verified_config(values: VerifiedRemoteValues) -> VerifiedRemoteConfigValues {
    HashMap::from([(
        InternedString::from_str_ref("remote_config"),
        Arc::new(values),
    )])
}

#[test]
fn updates_without_exportable_proofs_produce_no_candidates() {
    let specs = specs_with_config(spec(DynamicReturnable::empty(), Vec::new()));
    for verified in [HashMap::new(), verified_config(HashMap::new())] {
        assert!(mmap_remote_value_proofs(&specs, verified).is_empty());
    }

    let unreferenced = verified_value(1, archived_value(1));
    let verified = verified_config(HashMap::from([("unreferenced".to_string(), unreferenced)]));
    assert!(mmap_remote_value_proofs(&specs, verified).is_empty());

    let missing = HashMap::from([(
        InternedString::from_str_ref("missing_config"),
        Arc::new(HashMap::from([(
            "missing".to_string(),
            verified_value(2, archived_value(2)),
        )])),
    )]);
    assert!(mmap_remote_value_proofs(&specs, missing).is_empty());
}

#[test]
fn one_config_exports_all_distinct_remote_rule_values() {
    const RULE_COUNT: u64 = 4096;
    let default = archived_value(1);
    let rules: Vec<_> = (2..RULE_COUNT + 2).map(archived_value).collect();
    let verified = std::iter::once(&default)
        .chain(&rules)
        .map(|value| {
            (
                value.hash.to_string(),
                verified_value(value.hash, value.clone()),
            )
        })
        .collect();
    let specs = specs_with_config(spec(default, rules));
    let proofs = mmap_remote_value_proofs(&specs, verified_config(verified));
    assert_eq!(proofs.len(), RULE_COUNT as usize + 1);
    for index in 1..RULE_COUNT + 2 {
        assert_eq!(proofs[&format!("{index:064x}")].returnable_hash, index);
    }
}

#[test]
fn equal_hash_and_content_do_not_export_a_replaced_backing() {
    let installed = archived_value(7);
    let replaced = archived_value(7);
    assert_eq!(installed, replaced);
    let candidates = HashMap::from([
        (
            "installed".to_string(),
            verified_value(1, installed.clone()),
        ),
        ("replaced".to_string(), verified_value(2, replaced)),
        (
            "unreferenced".to_string(),
            verified_value(3, archived_value(8)),
        ),
    ]);
    let specs = specs_with_config(spec(installed, Vec::new()));
    let proofs = mmap_remote_value_proofs(&specs, verified_config(candidates));

    assert_eq!(proofs.len(), 1);
    assert!(proofs.contains_key(&format!("{:064x}", 1)));
}

#[test]
fn backing_identity_preserves_arc_static_archived_and_scalar_semantics() {
    let map = HashMap::from([("enabled".to_string(), RkyvValue::Bool(true))]);
    let shared = Arc::new(map.clone());
    let owned = DynamicReturnable::from_interned_value(
        1,
        DynamicReturnableValue::JsonPointer(Arc::clone(&shared)),
    );
    let leaked_shared: &'static Arc<HashMap<String, RkyvValue>> = Box::leak(Box::new(shared));
    let same_address_static = DynamicReturnable::from_interned_value(
        1,
        DynamicReturnableValue::JsonStatic(leaked_shared.as_ref()),
    );
    assert!(
        VerifiedRemoteValue::backing_identity(&owned)
            != VerifiedRemoteValue::backing_identity(&same_address_static)
    );
    let independent_owned = DynamicReturnable::from_interned_value(
        1,
        DynamicReturnableValue::JsonPointer(Arc::new(map.clone())),
    );
    let static_value = DynamicReturnable::from_interned_value(
        1,
        DynamicReturnableValue::JsonStatic(Box::leak(Box::new(map.clone()))),
    );
    let independent_static = DynamicReturnable::from_interned_value(
        1,
        DynamicReturnableValue::JsonStatic(Box::leak(Box::new(map))),
    );
    let archived = archived_value(1);
    let independent_archived = archived_value(1);
    let installed = [
        &owned,
        &static_value,
        &archived,
        &DynamicReturnable::empty(),
        &DynamicReturnable::from_bool(true),
    ]
    .into_iter()
    .map(VerifiedRemoteValue::backing_identity)
    .collect::<AHashSet<_>>();

    for value in [
        &owned.clone(),
        &static_value.clone(),
        &archived.clone(),
        &DynamicReturnable::empty(),
        &DynamicReturnable::from_bool(true),
    ] {
        assert!(installed.contains(&VerifiedRemoteValue::backing_identity(value)));
    }
    for value in [
        &independent_owned,
        &independent_static,
        &independent_archived,
        &DynamicReturnable::from_bool(false),
    ] {
        assert!(!installed.contains(&VerifiedRemoteValue::backing_identity(value)));
    }
}
