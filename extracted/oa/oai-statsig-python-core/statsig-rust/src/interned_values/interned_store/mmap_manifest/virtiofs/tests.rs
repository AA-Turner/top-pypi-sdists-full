use std::{fs::File, path::Path};

use super::super::{MmapV2Publication, inspect_mmap_v2_publication};
use super::{
    MmapArtifactIdentity, MmapManifest, is_translation_candidate, is_v2_only_manifest,
    is_virtiofs_mount,
};

fn identity() -> MmapArtifactIdentity {
    MmapArtifactIdentity {
        len: 100,
        modified_secs: 200,
        modified_nanos: 300,
        device: 400,
        inode: 500,
    }
}

#[test]
fn device_translation_preserves_generation_checks() {
    let manifest = MmapManifest { v2: identity() };
    let mut current = identity();
    fn matches(
        setting: Option<&str>,
        manifest: &MmapManifest,
        current: &MmapArtifactIdentity,
        artifact_path: &Path,
    ) -> bool {
        is_translation_candidate(
            setting,
            manifest,
            current,
            Path::new("/data/manifest.json"),
            artifact_path,
        )
    }
    let artifact_path = Path::new("/data/v2");

    assert!(!matches(Some("1"), &manifest, &current, artifact_path));
    current.device += 1;
    assert!(matches(Some("1"), &manifest, &current, artifact_path));
    assert!(!matches(None, &manifest, &current, artifact_path));
    assert!(!matches(Some("0"), &manifest, &current, artifact_path));
    assert!(!matches(Some("true"), &manifest, &current, artifact_path));
    assert!(!matches(
        Some("1"),
        &manifest,
        &current,
        Path::new("/other/v2")
    ));

    current.inode += 1;
    assert!(!matches(Some("1"), &manifest, &current, artifact_path));
    current.inode -= 1;
    current.len += 1;
    assert!(!matches(Some("1"), &manifest, &current, artifact_path));
    current.len -= 1;
    current.modified_secs += 1;
    assert!(!matches(Some("1"), &manifest, &current, artifact_path));
    current.modified_secs -= 1;
    current.modified_nanos += 1;
    assert!(!matches(Some("1"), &manifest, &current, artifact_path));
}

#[test]
fn device_translation_rejects_legacy_paired_manifests() {
    assert!(is_v2_only_manifest(br#"{"v2":{}}"#));
    assert!(is_v2_only_manifest(br#"{"v1":null,"v2":{}}"#));
    assert!(!is_v2_only_manifest(br#"{"v1":{},"v2":{}}"#));
}

#[test]
fn mount_check_requires_the_exact_virtiofs_mount() {
    let virtiofs = "42 24 0:58 / /data rw,relatime - virtiofs shared rw";
    assert!(is_virtiofs_mount(virtiofs, 42));
    assert!(!is_virtiofs_mount(virtiofs, 41));
    assert!(!is_virtiofs_mount(
        "42 24 0:58 / /data rw - fuse shared rw",
        42
    ));
    assert!(!is_virtiofs_mount(
        "42 24 0:58 / /data rw - ext4 shared rw",
        42
    ));
    assert!(!is_virtiofs_mount("malformed", 42));
}

#[test]
#[ignore = "requires TMPDIR on writable virtiofs and STATSIG_MMAP_ALLOW_VIRTIOFS_DEVICE_TRANSLATION=1"]
fn translated_virtiofs_publication_is_committed() {
    let directory = tempfile::tempdir().unwrap();
    let artifact_path = directory.path().join("v2.mmap");
    let manifest_path = directory.path().join("manifest.json");
    std::fs::write(&artifact_path, b"writer v2").unwrap();
    let mut identity =
        MmapArtifactIdentity::from_file(&File::open(&artifact_path).unwrap()).unwrap();
    // Emulate the host device ID recorded in the manifest.
    identity.device ^= 1;
    std::fs::write(
        &manifest_path,
        serde_json::to_vec(&MmapManifest { v2: identity }).unwrap(),
    )
    .unwrap();

    let publication = inspect_mmap_v2_publication(&manifest_path, &artifact_path).unwrap();
    assert!(matches!(publication, MmapV2Publication::Committed(_)));
}
