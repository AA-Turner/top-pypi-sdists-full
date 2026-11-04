use std::{collections::HashMap, io::Write};

use rusty_fork::rusty_fork_test;

use super::*;
use crate::{
    evaluation::rkyv_value::RkyvValue,
    specs_adapter::remote_config_value_hydrator::MmapRemoteValueProof,
};

const ORIGINAL_VALUE: &str = "original-verified-value-0123456789";
const RETURNABLE_HASH: u64 = 7;
const OTHER_RETURNABLE_HASH: u64 = 8;

fn digest(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn fixture() -> (Vec<u8>, MmapBlobProvenance) {
    let project = MmapProjectId::for_sdk_key("secret-blob-reader-project");
    let body = serde_json::to_vec(&serde_json::json!({"text": ORIGINAL_VALUE})).unwrap();
    let data = MmapDataV2 {
        returnables: vec![
            (
                RETURNABLE_HASH,
                Arc::new(HashMap::from([(
                    "text".to_owned(),
                    RkyvValue::String(ORIGINAL_VALUE.to_owned()),
                )])),
            ),
            (
                OTHER_RETURNABLE_HASH,
                Arc::new(HashMap::from([(
                    "text".to_owned(),
                    RkyvValue::String("a different existing value".to_owned()),
                )])),
            ),
        ],
        ..MmapDataV2::default()
    };
    let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&data)
        .unwrap()
        .to_vec();
    let mut provenance = MmapBlobProvenance {
        version: 1,
        sdk_key_hash: project.sdk_key_hash,
        artifact_sha256: digest(&bytes),
        values: vec![MmapRemoteValueProof {
            sha256: digest(&body),
            byte_length: body.len() as u64,
            compression: "none".to_owned(),
            returnable_hash: RETURNABLE_HASH,
            json_sidecar_reuse_safe: true,
        }],
        checksum: String::new(),
    };
    update_checksum(&mut provenance);
    (bytes, provenance)
}

fn update_checksum(provenance: &mut MmapBlobProvenance) {
    provenance.checksum = digest(
        &serde_json::to_vec(&(
            provenance.version,
            &provenance.sdk_key_hash,
            &provenance.artifact_sha256,
            &provenance.values,
        ))
        .unwrap(),
    );
}

fn project_from_bytes(bytes: &[u8]) -> LoadedMmapProject {
    let mut file = tempfile::tempfile().unwrap();
    file.write_all(bytes).unwrap();
    load_v2_file(
        MmapProjectId::for_sdk_key("secret-blob-reader-project"),
        file,
    )
    .unwrap()
}

fn assert_provenance_ignored(change: impl FnOnce(&mut MmapBlobProvenance)) {
    let (bytes, mut provenance) = fixture();
    let project = project_from_bytes(&bytes);
    change(&mut provenance);
    update_checksum(&mut provenance);
    assert!(
        validate_remote_values(&project, provenance)
            .unwrap()
            .is_none()
    );
}

#[test]
fn matching_artifact_accepts_verified_blob_provenance() {
    let (bytes, provenance) = fixture();
    let expected = provenance.values.clone();
    let project = project_from_bytes(&bytes);
    let accepted = validate_remote_values(&project, provenance)
        .unwrap()
        .unwrap();

    assert_eq!(accepted.values, expected);
    assert_eq!(accepted.artifact_sha256, digest(&bytes));
}

#[test]
fn structurally_valid_content_corruption_rejects_the_mapping() {
    let (mut bytes, provenance) = fixture();
    let offset = bytes
        .windows(ORIGINAL_VALUE.len())
        .position(|window| window == ORIGINAL_VALUE.as_bytes())
        .expect("the archived returnable must contain the fixture string");
    bytes[offset] = b'X';

    // The same-length UTF-8 edit passes archive validation but is no longer
    // the artifact whose verified blob handles the writer committed.
    let project = project_from_bytes(&bytes);
    assert!(matches!(
        validate_remote_values(&project, provenance),
        Err(StatsigErr::SerializationError(_))
    ));
}

#[test]
fn missing_returnable_handle_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.values[0].returnable_hash = u64::MAX;
    });
}

#[test]
fn invalid_blob_sha_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.values[0].sha256 = "not-a-sha256".to_owned();
    });
}

#[test]
fn unsupported_compression_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.values[0].compression = "unsupported".to_owned();
    });
}

#[test]
fn oversized_blob_length_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.values[0].byte_length = u64::MAX;
    });
}

#[test]
fn duplicate_blob_sha_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.values.push(provenance.values[0].clone());
    });
}

#[test]
fn another_sdk_key_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.sdk_key_hash = MmapProjectId::for_sdk_key("secret-another-project").sdk_key_hash;
    });
}

#[test]
fn unknown_provenance_version_ignores_optional_provenance() {
    assert_provenance_ignored(|provenance| {
        provenance.version += 1;
    });
}

#[test]
fn redirecting_a_proof_to_another_existing_value_ignores_provenance() {
    let (bytes, mut provenance) = fixture();
    let project = project_from_bytes(&bytes);
    provenance.values[0].returnable_hash = OTHER_RETURNABLE_HASH;

    assert!(!provenance.has_valid_checksum());
    assert!(
        validate_remote_values(&project, provenance)
            .unwrap()
            .is_none()
    );
}

#[test]
fn malformed_bundle_checksum_ignores_provenance() {
    let (bytes, mut provenance) = fixture();
    let project = project_from_bytes(&bytes);
    provenance.checksum = "not-a-checksum".to_owned();

    assert!(
        validate_remote_values(&project, provenance)
            .unwrap()
            .is_none()
    );
}

fn add_fixture_to_builder(
    builder: &mut MmapRegistryBuilder,
    id: MmapProjectId,
    bytes: &[u8],
    provenance: Option<MmapBlobProvenance>,
) {
    let mut file = tempfile::tempfile().unwrap();
    file.write_all(bytes).unwrap();
    builder
        .add_file_with_remote_values(id, file, provenance)
        .unwrap();
}

rusty_fork_test! {
    #[test]
    fn preload_builds_the_shared_verified_index_before_any_lookup() {
        let (bytes, provenance) = fixture();
        let id = MmapProjectId::for_sdk_key("secret-blob-reader-project");
        let sha = provenance.values[0].sha256.clone();
        let mut builder = MmapRegistryBuilder::new();
        add_fixture_to_builder(&mut builder, id, &bytes, Some(provenance));
        builder.install(&MmapPreloadOptions::default()).unwrap();

        // Preload, not the first SDK lookup in each worker, must build this map.
        let project = &MMAP_DATA.get().unwrap().projects[0];
        let prepared = project.verified_remote_values.get().unwrap();
        assert_eq!(prepared.len(), 1);
        assert!(prepared[&sha].value.get_json_archived_ref().is_some());
        assert_eq!(prepared[&sha].value.get_json().unwrap()["text"], ORIGINAL_VALUE);
        assert!(std::ptr::eq(verified_remote_values(id).unwrap(), prepared));

        std::thread::scope(|scope| {
            for _ in 0..2 {
                let sha = &sha;
                scope.spawn(move || {
                    let actual = verified_remote_values(id).unwrap();
                    assert!(std::ptr::eq(actual, prepared));
                    assert!(Arc::ptr_eq(&actual[sha], &prepared[sha]));
                });
            }
        });
    }

    #[test]
    fn eager_proof_indexes_keep_project_association_after_ignored_provenance() {
        let (bytes, first) = fixture();
        let first_id = MmapProjectId::for_sdk_key("secret-blob-reader-project");
        let ignored_id = MmapProjectId::for_sdk_key("secret-ignored-reader-project");
        let last_id = MmapProjectId::for_sdk_key("secret-last-reader-project");
        let first_sha = first.values[0].sha256.clone();
        let mut ignored = first.clone();
        ignored.version += 1;
        ignored.sdk_key_hash = ignored_id.sdk_key_hash;
        update_checksum(&mut ignored);

        let mut last = first.clone();
        last.sdk_key_hash = last_id.sdk_key_hash;
        let body = br#"{"text":"a different existing value"}"#;
        last.values[0].sha256 = digest(body);
        last.values[0].byte_length = body.len() as u64;
        last.values[0].returnable_hash = OTHER_RETURNABLE_HASH;
        update_checksum(&mut last);
        let last_sha = last.values[0].sha256.clone();
        let mut builder = MmapRegistryBuilder::new();
        add_fixture_to_builder(&mut builder, first_id, &bytes, Some(first));
        add_fixture_to_builder(&mut builder, ignored_id, &bytes, Some(ignored));
        add_fixture_to_builder(&mut builder, last_id, &bytes, Some(last));
        builder.install(&MmapPreloadOptions::default()).unwrap();

        assert!(verified_remote_values(ignored_id).is_none());
        let first_values = verified_remote_values(first_id).unwrap();
        let last_values = verified_remote_values(last_id).unwrap();
        assert_eq!(first_values.len(), 1);
        assert_eq!(last_values.len(), 1);
        assert!(!first_values.contains_key(&last_sha));
        assert!(!last_values.contains_key(&first_sha));
        assert_eq!(first_values[&first_sha].value.get_json().unwrap()["text"], ORIGINAL_VALUE);
        assert_eq!(
            last_values[&last_sha].value.get_json().unwrap()["text"],
            "a different existing value"
        );
    }

    #[test]
    fn eager_proof_indexes_preserve_empty_and_missing_provenance() {
        let (bytes, mut empty) = fixture();
        let empty_id = MmapProjectId::for_sdk_key("secret-empty-reader-project");
        let missing_id = MmapProjectId::for_sdk_key("secret-proofless-reader-project");
        empty.sdk_key_hash = empty_id.sdk_key_hash;
        empty.values.clear();
        update_checksum(&mut empty);
        let mut builder = MmapRegistryBuilder::new();
        add_fixture_to_builder(&mut builder, empty_id, &bytes, Some(empty));
        add_fixture_to_builder(&mut builder, missing_id, &bytes, None);
        builder.install(&MmapPreloadOptions::default()).unwrap();

        assert!(verified_remote_values(empty_id).unwrap().is_empty());
        assert!(verified_remote_values(missing_id).is_none());
        assert!(verified_remote_values(MmapProjectId::for_sdk_key("unknown-project")).is_none());
    }

    #[test]
    fn failed_reinstall_preserves_the_existing_verified_index() {
        let (bytes, provenance) = fixture();
        let id = MmapProjectId::for_sdk_key("secret-blob-reader-project");
        let sha = provenance.values[0].sha256.clone();
        let mut first = MmapRegistryBuilder::new();
        add_fixture_to_builder(&mut first, id, &bytes, Some(provenance.clone()));
        first.install(&MmapPreloadOptions::default()).unwrap();
        let existing = verified_remote_values(id).unwrap();

        let other_id = MmapProjectId::for_sdk_key("secret-second-install-project");
        let mut other = provenance;
        other.sdk_key_hash = other_id.sdk_key_hash;
        update_checksum(&mut other);
        let mut second = MmapRegistryBuilder::new();
        add_fixture_to_builder(&mut second, other_id, &bytes, Some(other));
        assert!(matches!(
            second.install(&MmapPreloadOptions::default()),
            Err(StatsigErr::LockFailure(_))
        ));

        let current = verified_remote_values(id).unwrap();
        assert!(std::ptr::eq(current, existing));
        assert!(Arc::ptr_eq(&current[&sha], &existing[&sha]));
        assert_eq!(current[&sha].value.get_json().unwrap()["text"], ORIGINAL_VALUE);
        assert!(verified_remote_values(other_id).is_none());
    }
}
