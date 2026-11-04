use super::*;

fn proof(index: u64) -> MmapRemoteValueProof {
    MmapRemoteValueProof {
        sha256: format!("{index:064x}"),
        byte_length: 5_000_000,
        compression: "gzip".to_string(),
        returnable_hash: index,
        json_sidecar_reuse_safe: false,
    }
}

fn artifact(directory: &Path) -> (std::path::PathBuf, File) {
    let path = directory.join("v2.mmap");
    let temporary = tempfile::NamedTempFile::new_in(directory).unwrap();
    std::fs::write(temporary.path(), b"writer v2").unwrap();
    let file = temporary.persist(&path).unwrap();
    (path, file)
}

fn expected_sidecar_bytes(
    file: &File,
    project: MmapProjectId,
    values: &[MmapRemoteValueProof],
) -> Vec<u8> {
    let artifact_sha256 = artifact_sha256(file).unwrap();
    let checksum = provenance_checksum(1, &project.sdk_key_hash, &artifact_sha256, values).unwrap();
    serde_json::to_vec(&MmapRemoteValuesSidecarRef {
        v2: &MmapArtifactIdentity::from_file(file).unwrap(),
        remote_values: MmapBlobProvenanceRef {
            version: 1,
            sdk_key_hash: &project.sdk_key_hash,
            artifact_sha256: &artifact_sha256,
            values,
            checksum: &checksum,
        },
    })
    .unwrap()
}

fn replace_sidecar_bytes(manifest: &Path, bytes: &[u8]) {
    let digest: String = Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    std::fs::write(remote_values_sidecar_path(manifest), bytes).unwrap();
    let mut data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(manifest).unwrap()).unwrap();
    data["remote_values_file"]["sha256"] = digest.into();
    std::fs::write(manifest, serde_json::to_vec(&data).unwrap()).unwrap();
}

fn replace_sidecar_json(manifest: &Path, change: impl FnOnce(&mut serde_json::Value)) {
    let mut data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(remote_values_sidecar_path(manifest)).unwrap())
            .unwrap();
    change(&mut data);
    replace_sidecar_bytes(manifest, &serde_json::to_vec(&data).unwrap());
}

fn assert_invalid_sidecar_ignored(change: impl FnOnce(&Path)) {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(1)]).unwrap();

    change(&manifest);

    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert!(provenance.is_none());
}

#[test]
fn remote_values_preserve_legacy_manifest_and_archive_compatibility() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, mut file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    file.seek(SeekFrom::Start(3)).unwrap();
    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(1)]).unwrap();

    assert_eq!(file.stream_position().unwrap(), 3);
    assert_eq!(std::fs::read(&path).unwrap(), b"writer v2");
    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    let provenance = provenance.unwrap();
    assert!(provenance.has_valid_checksum());
    assert_eq!(provenance.version, 1);
    assert_eq!(provenance.sdk_key_hash, project.sdk_key_hash);
    assert_eq!(
        provenance.artifact_sha256,
        Sha256::digest(b"writer v2")
            .iter()
            .map(|byte| format!("{byte:02x}"))
            .collect::<String>()
    );
    assert_eq!(provenance.values.len(), 1);
    assert_eq!(provenance.values[0].sha256, proof(1).sha256);
}

#[test]
fn a_fitting_table_publishes_the_final_sorted_sidecar_bytes() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (_, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    let values: Vec<_> = (0..3).map(proof).collect();

    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        project,
        values.iter().rev().cloned().collect(),
    )
    .unwrap();

    assert_eq!(
        std::fs::read(remote_values_sidecar_path(&manifest)).unwrap(),
        expected_sidecar_bytes(&file, project, &values),
    );
}

#[test]
fn an_exact_byte_limit_prefix_is_retained() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (_, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    let mut first = proof(1);
    first.compression.clear();
    let base_length = expected_sidecar_bytes(&file, project, &[first.clone()]).len();
    first.compression = "x".repeat(MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES - base_length);
    let expected = expected_sidecar_bytes(&file, project, &[first.clone()]);
    assert_eq!(expected.len(), MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES);

    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(2), first])
        .unwrap();

    assert_eq!(
        std::fs::read(remote_values_sidecar_path(&manifest)).unwrap(),
        expected,
    );
}

#[test]
fn remote_value_count_limit_retains_the_full_deterministic_prefix() {
    const { assert!(MAX_MMAP_REMOTE_VALUES >= 40_960) };
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    let expected_proof = |index| MmapRemoteValueProof {
        returnable_hash: u64::MAX - index,
        json_sidecar_reuse_safe: true,
        ..proof(index)
    };
    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        project,
        (0..=MAX_MMAP_REMOTE_VALUES as u64)
            .rev()
            .map(expected_proof)
            .collect(),
    )
    .unwrap();

    let manifest_bytes = std::fs::read(&manifest).unwrap();
    assert!(manifest_bytes.len() <= MAX_MMAP_MANIFEST_BYTES);
    let _: MmapManifest = serde_json::from_slice(&manifest_bytes).unwrap();
    let sidecar_bytes = std::fs::metadata(remote_values_sidecar_path(&manifest))
        .unwrap()
        .len();
    assert!(sidecar_bytes > MAX_MMAP_MANIFEST_BYTES as u64);
    assert!(sidecar_bytes <= MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES as u64);
    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    let provenance = provenance.unwrap();
    assert!(provenance.has_valid_checksum());
    assert_eq!(provenance.values.len(), MAX_MMAP_REMOTE_VALUES);
    for (index, value) in provenance.values.iter().enumerate() {
        assert_eq!(*value, expected_proof(index as u64));
    }
}

#[test]
fn remote_value_byte_limit_retains_the_largest_fitting_prefix() {
    const PROOF_COUNT: usize = 300;
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    // Oversized fixture fields exercise the serialized metadata budget without
    // allocating blob payloads or invoking SDK hydration.
    let compression_bytes = MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES / PROOF_COUNT + 1;
    let large_proof = |index| {
        let mut value = proof(index);
        value.compression = "x".repeat(compression_bytes);
        value
    };
    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        project,
        (0..PROOF_COUNT as u64).rev().map(large_proof).collect(),
    )
    .unwrap();

    assert!(std::fs::metadata(&manifest).unwrap().len() <= MAX_MMAP_MANIFEST_BYTES as u64);
    let bytes = std::fs::read(remote_values_sidecar_path(&manifest)).unwrap();
    assert!(bytes.len() <= MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES);
    let mut sidecar: MmapRemoteValuesSidecar = serde_json::from_slice(&bytes).unwrap();
    drop(bytes);
    let count = sidecar.remote_values.values.len();
    assert!(count > 0 && count < PROOF_COUNT);
    assert!(sidecar.remote_values.has_valid_checksum());
    for (index, value) in sidecar.remote_values.values.iter().enumerate() {
        assert_eq!(value.sha256, proof(index as u64).sha256);
        assert_eq!(value.compression.len(), compression_bytes);
    }
    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert_eq!(provenance.unwrap().values.len(), count);

    sidecar.remote_values.values.push(large_proof(count as u64));
    let provenance = &sidecar.remote_values;
    // A recalculated checksum has the same fixed width, so keeping the old
    // checksum is sufficient when checking only the next prefix's byte size.
    let next_bytes = serde_json::to_vec(&MmapRemoteValuesSidecarRef {
        v2: &sidecar.v2,
        remote_values: MmapBlobProvenanceRef {
            version: provenance.version,
            sdk_key_hash: &provenance.sdk_key_hash,
            artifact_sha256: &provenance.artifact_sha256,
            values: &provenance.values,
            checksum: &provenance.checksum,
        },
    })
    .unwrap();
    assert!(next_bytes.len() > MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES);
}

#[test]
fn missing_optional_sidecar_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        std::fs::remove_file(remote_values_sidecar_path(manifest)).unwrap();
    });
}

#[test]
fn unreadable_optional_sidecar_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        let sidecar = remote_values_sidecar_path(manifest);
        std::fs::remove_file(&sidecar).unwrap();
        std::fs::create_dir(sidecar).unwrap();
    });
}

#[test]
fn sidecar_publication_failure_preserves_a_proofless_commit() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    std::fs::create_dir(remote_values_sidecar_path(&manifest)).unwrap();

    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(1)]).unwrap();

    let data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(&manifest).unwrap()).unwrap();
    assert!(data.get("remote_values_file").is_none());
    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert!(provenance.is_none());
}

#[test]
fn corrupted_optional_sidecar_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        let path = remote_values_sidecar_path(manifest);
        let mut bytes = std::fs::read(&path).unwrap();
        // Still valid JSON, but no longer matches the manifest's file digest.
        bytes.push(b' ');
        std::fs::write(path, bytes).unwrap();
    });
}

#[test]
fn malformed_sidecar_with_matching_digest_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        replace_sidecar_bytes(manifest, b"not-json");
    });
}

#[test]
fn oversized_sidecar_with_matching_digest_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        let mut bytes = std::fs::read(remote_values_sidecar_path(manifest)).unwrap();
        // Keep the proof table valid so the byte limit, rather than JSON or
        // proof validation, must reject this otherwise usable sidecar.
        bytes.resize(MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES + 1, b' ');
        replace_sidecar_bytes(manifest, &bytes);
    });
}

#[test]
fn sidecar_for_another_archive_generation_is_ignored() {
    assert_invalid_sidecar_ignored(|manifest| {
        replace_sidecar_json(manifest, |data| {
            let len = data["v2"]["len"].as_u64().unwrap();
            data["v2"]["len"] = (len + 1).into();
        });
    });
}

#[test]
fn sidecar_with_another_project_is_ignored() {
    assert_invalid_sidecar_ignored(|manifest| {
        replace_sidecar_json(manifest, |data| {
            let mut provenance: MmapBlobProvenance =
                serde_json::from_value(data["remote_values"].clone()).unwrap();
            provenance.sdk_key_hash =
                MmapProjectId::for_sdk_key("secret-other-project").sdk_key_hash;
            provenance.checksum = provenance_checksum(
                provenance.version,
                &provenance.sdk_key_hash,
                &provenance.artifact_sha256,
                &provenance.values,
            )
            .unwrap();
            data["remote_values"] = serde_json::to_value(provenance).unwrap();
        });
    });
}

#[test]
fn unknown_sidecar_reference_version_is_ignored() {
    assert_invalid_sidecar_ignored(|manifest| {
        let mut data: serde_json::Value =
            serde_json::from_slice(&std::fs::read(manifest).unwrap()).unwrap();
        data["remote_values_file"]["version"] = 2.into();
        std::fs::write(manifest, serde_json::to_vec(&data).unwrap()).unwrap();
    });
}

#[test]
fn malformed_sidecar_reference_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        let mut data: serde_json::Value =
            serde_json::from_slice(&std::fs::read(manifest).unwrap()).unwrap();
        data["remote_values_file"] = "not-a-reference".into();
        std::fs::write(manifest, serde_json::to_vec(&data).unwrap()).unwrap();
    });
}

#[test]
fn too_many_sidecar_proofs_with_matching_digest_are_ignored() {
    assert_invalid_sidecar_ignored(|manifest| {
        let mut sidecar: MmapRemoteValuesSidecar =
            serde_json::from_slice(&std::fs::read(remote_values_sidecar_path(manifest)).unwrap())
                .unwrap();
        let provenance = &mut sidecar.remote_values;
        provenance.values = (0..=MAX_MMAP_REMOTE_VALUES as u64).map(proof).collect();
        provenance.checksum = provenance_checksum(
            provenance.version,
            &provenance.sdk_key_hash,
            &provenance.artifact_sha256,
            &provenance.values,
        )
        .unwrap();
        // Serialize borrowed typed records directly instead of materializing
        // a second JSON object tree for tens of thousands of proof entries.
        let bytes = serde_json::to_vec(&MmapRemoteValuesSidecarRef {
            v2: &sidecar.v2,
            remote_values: MmapBlobProvenanceRef {
                version: provenance.version,
                sdk_key_hash: &provenance.sdk_key_hash,
                artifact_sha256: &provenance.artifact_sha256,
                values: &provenance.values,
                checksum: &provenance.checksum,
            },
        })
        .unwrap();
        replace_sidecar_bytes(manifest, &bytes);
        assert!(
            std::fs::metadata(remote_values_sidecar_path(manifest))
                .unwrap()
                .len()
                <= MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES as u64
        );
    });
}

#[test]
fn mismatched_manifest_and_sidecar_generations_only_disable_reuse() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    let sidecar = remote_values_sidecar_path(&manifest);
    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(1)]).unwrap();
    let old_manifest = std::fs::read(&manifest).unwrap();
    let old_sidecar = std::fs::read(&sidecar).unwrap();
    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(2)]).unwrap();
    let new_manifest = std::fs::read(&manifest).unwrap();
    let new_sidecar = std::fs::read(&sidecar).unwrap();

    // A reader can capture either manifest before opening the independently
    // replaced sidecar. Neither mismatch may authorize an unbound proof table.
    for (manifest_bytes, sidecar_bytes) in
        [(&old_manifest, &new_sidecar), (&new_manifest, &old_sidecar)]
    {
        std::fs::write(&manifest, manifest_bytes).unwrap();
        std::fs::write(&sidecar, sidecar_bytes).unwrap();
        assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
        let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
            .unwrap()
            .unwrap();
        assert!(provenance.is_none());
    }

    std::fs::write(&manifest, new_manifest).unwrap();
    std::fs::write(&sidecar, new_sidecar).unwrap();
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert_eq!(provenance.unwrap().values, vec![proof(2)]);
}

#[cfg(unix)]
#[test]
fn sidecar_binds_to_publisher_identity_not_translated_device() {
    let directory = tempfile::tempdir().unwrap();
    let manifest_path = directory.path().join("manifest.json");
    let (_, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-translated-sidecar-project");
    write_mmap_manifest_with_remote_values(&manifest_path, &file, project, vec![proof(1)]).unwrap();
    let bytes = std::fs::read(&manifest_path).unwrap();
    let manifest: MmapManifestWithRemoteValues<'_> = serde_json::from_slice(&bytes).unwrap();
    let reference = manifest.remote_values_file.unwrap();

    // Model identities after device translation has been accepted; this does
    // not invoke the mount detector or require an actual virtiofs filesystem.
    let guest = MmapArtifactIdentity {
        device: manifest.v2.device.wrapping_add(1),
        ..MmapArtifactIdentity::from_file(&file).unwrap()
    };
    let accepted =
        read_remote_values_sidecar(&manifest_path, &manifest.v2, project, reference).unwrap();
    assert_eq!(accepted.values, vec![proof(1)]);
    assert!(accepted.has_valid_checksum());
    assert!(read_remote_values_sidecar(&manifest_path, &guest, project, reference).is_none());

    // Device translation must not relax the remaining generation identity.
    let another_generation = MmapArtifactIdentity {
        inode: manifest.v2.inode.wrapping_add(1),
        ..MmapArtifactIdentity::from_file(&file).unwrap()
    };
    assert!(
        read_remote_values_sidecar(&manifest_path, &another_generation, project, reference)
            .is_none()
    );
}

#[test]
fn sidecar_path_is_derived_only_from_the_manifest_path() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let sidecar = remote_values_sidecar_path(&manifest);
    assert_eq!(sidecar, manifest.with_extension("blob-proofs.json"));
    assert_eq!(sidecar.parent(), manifest.parent());
}

#[test]
fn invalid_sidecar_reference_preserves_a_valid_artifact() {
    assert_invalid_sidecar_ignored(|manifest| {
        let mut data: serde_json::Value =
            serde_json::from_slice(&std::fs::read(manifest).unwrap()).unwrap();
        data["remote_values_file"]["sha256"] = "../outside.json".into();
        std::fs::write(manifest, serde_json::to_vec(&data).unwrap()).unwrap();
    });
}

#[test]
fn a_new_reader_still_accepts_legacy_inline_provenance() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    write_mmap_manifest(&manifest, &file).unwrap();
    let mut provenance = MmapBlobProvenance {
        version: 1,
        sdk_key_hash: project.sdk_key_hash,
        artifact_sha256: artifact_sha256(&file).unwrap(),
        values: vec![proof(1)],
        checksum: String::new(),
    };
    provenance.checksum = provenance_checksum(
        provenance.version,
        &provenance.sdk_key_hash,
        &provenance.artifact_sha256,
        &provenance.values,
    )
    .unwrap();
    let mut data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(&manifest).unwrap()).unwrap();
    data["remote_values"] = serde_json::to_value(provenance).unwrap();
    std::fs::write(&manifest, serde_json::to_vec(&data).unwrap()).unwrap();

    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    let provenance = provenance.unwrap();
    assert!(provenance.has_valid_checksum());
    assert_eq!(provenance.values, vec![proof(1)]);
}

#[test]
fn a_new_reader_loads_an_archive_without_any_proofs() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    write_mmap_manifest(&manifest, &file).unwrap();

    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert!(provenance.is_none());
}

#[test]
fn another_project_cannot_use_manifest_remote_values() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        MmapProjectId::for_sdk_key("secret-writer"),
        vec![proof(1)],
    )
    .unwrap();

    let (_, provenance) = open_committed_mmap_v2_with_remote_values(
        &manifest,
        &path,
        MmapProjectId::for_sdk_key("secret-other-project"),
    )
    .unwrap()
    .unwrap();
    assert!(provenance.is_none());
}

#[test]
fn malformed_optional_provenance_preserves_a_valid_artifact() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    write_mmap_manifest(&manifest, &file).unwrap();
    let mut data: serde_json::Value =
        serde_json::from_slice(&std::fs::read(&manifest).unwrap()).unwrap();
    data["remote_values"] = serde_json::json!({"version": "malformed"});
    std::fs::write(&manifest, serde_json::to_vec(&data).unwrap()).unwrap();

    assert!(open_committed_mmap_v2(&manifest, &path).unwrap().is_some());
    let (_, provenance) = open_committed_mmap_v2_with_remote_values(&manifest, &path, project)
        .unwrap()
        .unwrap();
    assert!(provenance.is_none());
}

#[test]
fn provenance_is_never_returned_for_a_replaced_archive() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (path, file) = artifact(directory.path());
    let project = MmapProjectId::for_sdk_key("secret-manifest-project");
    write_mmap_manifest_with_remote_values(&manifest, &file, project, vec![proof(1)]).unwrap();
    let replacement = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(replacement.path(), b"next writer v2").unwrap();
    replacement.persist(&path).unwrap();

    assert!(matches!(
        open_committed_mmap_v2_with_remote_values(&manifest, &path, project),
        Err(StatsigErr::InvalidOperation(_))
    ));
}

#[test]
fn empty_remote_values_write_the_original_manifest_shape() {
    let directory = tempfile::tempdir().unwrap();
    let manifest = directory.path().join("manifest.json");
    let (_, file) = artifact(directory.path());
    write_mmap_manifest(&manifest, &file).unwrap();
    let original = std::fs::read(&manifest).unwrap();
    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        MmapProjectId::for_sdk_key("secret-manifest-project"),
        vec![proof(1)],
    )
    .unwrap();
    write_mmap_manifest_with_remote_values(
        &manifest,
        &file,
        MmapProjectId::for_sdk_key("secret-manifest-project"),
        Vec::new(),
    )
    .unwrap();
    assert_eq!(std::fs::read(&manifest).unwrap(), original);
}

#[test]
fn manifest_from_persisted_handles_rejects_replaced_path() {
    let directory = tempfile::tempdir().unwrap();
    let v2_path = directory.path().join("v2.mmap");
    let manifest_path = directory.path().join("manifest.json");

    let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(v2_temp.path(), b"writer v2").unwrap();
    let v2_file = v2_temp.persist(&v2_path).unwrap();

    let replacement = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(replacement.path(), b"next writer v2").unwrap();
    replacement.persist(&v2_path).unwrap();

    write_mmap_manifest(&manifest_path, &v2_file).unwrap();
    assert!(matches!(
        open_committed_mmap_v2(&manifest_path, &v2_path),
        Err(StatsigErr::InvalidOperation(message))
            if message == "Interned mmap V2 publication is incomplete; retry preload"
    ));
}

#[test]
fn manifest_accepts_committed_v2_artifact() {
    let directory = tempfile::tempdir().unwrap();
    let v2_path = directory.path().join("v2.mmap");
    let manifest_path = directory.path().join("manifest.json");

    let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(v2_temp.path(), b"writer v2").unwrap();
    let v2_file = v2_temp.persist(&v2_path).unwrap();
    write_mmap_manifest(&manifest_path, &v2_file).unwrap();

    assert!(
        open_committed_mmap_v2(&manifest_path, &v2_path)
            .unwrap()
            .is_some()
    );
}

#[test]
fn manifest_rejects_replaced_v2_artifact() {
    let directory = tempfile::tempdir().unwrap();
    let v2_path = directory.path().join("v2.mmap");
    let manifest_path = directory.path().join("manifest.json");

    let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(v2_temp.path(), b"writer v2").unwrap();
    let v2_file = v2_temp.persist(&v2_path).unwrap();
    write_mmap_manifest(&manifest_path, &v2_file).unwrap();

    let replacement = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
    std::fs::write(replacement.path(), b"next writer v2").unwrap();
    replacement.persist(&v2_path).unwrap();

    assert!(matches!(
        open_committed_mmap_v2(&manifest_path, &v2_path),
        Err(StatsigErr::InvalidOperation(message))
            if message == "Interned mmap V2 publication is incomplete; retry preload"
    ));
}

#[test]
fn v2_without_manifest_requires_retry() {
    let directory = tempfile::tempdir().unwrap();
    let v2_path = directory.path().join("v2.mmap");
    let manifest_path = directory.path().join("missing-manifest.json");
    std::fs::write(&v2_path, b"writer v2").unwrap();

    assert!(matches!(
        open_committed_mmap_v2(&manifest_path, &v2_path),
        Err(StatsigErr::InvalidOperation(message))
            if message == "Interned mmap V2 publication is incomplete; retry preload"
    ));
}
