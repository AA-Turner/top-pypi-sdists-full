#[path = "utils/synthetic_specs_fixture.rs"]
mod synthetic_specs_fixture;

use std::fs;

use serde_json::json;
use sha2::{Digest, Sha256};
use synthetic_specs_fixture::{load_inline_json, load_inline_protobuf};

fn sha256(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn fixture() -> (tempfile::TempDir, serde_json::Value) {
    let dir = tempfile::tempdir().unwrap();
    let source = br#"{"schema_version":2,"product":"chatgpt","seed":-723}"#;
    fs::write(dir.path().join("source.json"), source).unwrap();
    fs::write(dir.path().join("inline.pb.zst"), b"fixture").unwrap();
    let manifest = json!({
        "schema_version": 1,
        "source_manifest": {
            "path": "source.json",
            "sha256": sha256(source),
        },
        "artifacts": [{
            "state": "inline", "file": "inline.pb.zst",
            "encoding": "protobuf_full", "content_encoding": "statsig-zstd",
            "bytes": 7, "sha256": sha256(b"fixture"),
        }],
    });
    (dir, manifest)
}

fn write_manifest(dir: &tempfile::TempDir, manifest: &serde_json::Value) -> std::path::PathBuf {
    let path = dir.path().join("manifest.json");
    fs::write(&path, serde_json::to_vec(manifest).unwrap()).unwrap();
    path
}

#[test]
fn reads_verified_inline_artifact_and_identity() {
    let (dir, mut manifest) = fixture();
    let loaded = load_inline_protobuf(&write_manifest(&dir, &manifest)).unwrap();
    assert_eq!(loaded.bytes, b"fixture");
    assert_eq!(loaded.content_encoding, "statsig-zstd");
    assert_eq!(loaded.product, "chatgpt");
    assert_eq!(loaded.seed, serde_json::Number::from(-723));
    assert_eq!(loaded.sha256, manifest["artifacts"][0]["sha256"]);
    manifest["artifacts"][0]["content_encoding"] = json!("statsig-br");
    let legacy = load_inline_protobuf(&write_manifest(&dir, &manifest)).unwrap();
    assert_eq!(legacy.content_encoding, "statsig-br");
    manifest["artifacts"][0]["content_encoding"] = json!("gzip");
    assert!(
        load_inline_protobuf(&write_manifest(&dir, &manifest))
            .err()
            .unwrap()
            .contains("unsupported protobuf content encoding")
    );
}

#[test]
fn rejects_changed_source_manifest_and_artifact() {
    let (dir, manifest) = fixture();
    let path = write_manifest(&dir, &manifest);
    fs::write(dir.path().join("inline.pb.zst"), b"changed").unwrap();
    assert!(
        load_inline_protobuf(&path)
            .err()
            .unwrap()
            .contains("SHA-256 mismatch")
    );
    fs::write(dir.path().join("inline.pb.zst"), b"short").unwrap();
    assert!(
        load_inline_protobuf(&path)
            .err()
            .unwrap()
            .contains("length mismatch")
    );
    fs::write(dir.path().join("source.json"), b"changed").unwrap();
    assert!(
        load_inline_protobuf(&path)
            .err()
            .unwrap()
            .contains("source manifest SHA-256 mismatch")
    );
}

#[test]
fn rejects_remote_delta_and_missing_artifacts() {
    let (dir, manifest) = fixture();
    for (field, value) in [("state", "remote_observed"), ("encoding", "protobuf_delta")] {
        let mut unsupported = manifest.clone();
        unsupported["artifacts"][0][field] = json!(value);
        assert!(
            load_inline_protobuf(&write_manifest(&dir, &unsupported))
                .err()
                .unwrap()
                .contains("remote/delta inputs are unsupported")
        );
    }
    fs::remove_file(dir.path().join("inline.pb.zst")).unwrap();
    assert!(
        load_inline_protobuf(&write_manifest(&dir, &manifest))
            .err()
            .unwrap()
            .contains("protobuf artifact:")
    );
}

#[test]
fn rejects_nonregular_source_manifest() {
    let (dir, mut manifest) = fixture();
    manifest["source_manifest"]["path"] = json!(".");
    assert!(
        load_inline_protobuf(&write_manifest(&dir, &manifest))
            .err()
            .unwrap()
            .contains("regular source manifest file")
    );
}

#[test]
fn rejects_artifact_outside_encoding_bundle() {
    let (dir, mut manifest) = fixture();
    let other = tempfile::tempdir().unwrap();
    let file = other.path().join("external.pb");
    fs::write(&file, b"fixture").unwrap();
    manifest["artifacts"][0]["file"] = json!(file);
    assert!(
        load_inline_protobuf(&write_manifest(&dir, &manifest))
            .err()
            .unwrap()
            .contains("inside the bundle")
    );
}

fn json_fixture() -> (tempfile::TempDir, serde_json::Value) {
    let dir = tempfile::tempdir().unwrap();
    fs::write(dir.path().join("inline.json"), b"{\"time\":1}").unwrap();
    let manifest = json!({
        "schema_version": 2, "product": "model_lab", "seed": 17,
        "scenarios": [{
            "name": "display name", "state_id": "inline", "encoding": "json_full", "file": "inline.json",
            "bytes": 10, "sha256": sha256(b"{\"time\":1}"),
        }],
    });
    (dir, manifest)
}

#[test]
fn reads_verified_inline_json_and_identity() {
    let (dir, manifest) = json_fixture();
    let loaded = load_inline_json(&write_manifest(&dir, &manifest)).unwrap();
    assert_eq!(loaded.bytes, b"{\"time\":1}");
    assert_eq!(loaded.product, "model_lab");
    assert_eq!(loaded.seed, serde_json::Number::from(17));
    assert_eq!(loaded.sha256, manifest["scenarios"][0]["sha256"]);
}

#[test]
fn rejects_json_artifacts_outside_the_declaring_bundle() {
    let (dir, mut manifest) = json_fixture();
    let bundle = tempfile::tempdir_in(dir.path()).unwrap();
    let outside = dir.path().join("inline.json");
    for file in [outside.to_str().unwrap(), "../inline.json"] {
        manifest["scenarios"][0]["file"] = json!(file);
        assert!(
            load_inline_json(&write_manifest(&bundle, &manifest))
                .err()
                .unwrap()
                .contains("inside the bundle")
        );
    }
}

#[test]
fn rejects_modified_missing_or_wrong_length_json() {
    let (dir, manifest) = json_fixture();
    let path = write_manifest(&dir, &manifest);
    fs::write(dir.path().join("inline.json"), b"{\"time\":2}").unwrap();
    assert!(
        load_inline_json(&path)
            .err()
            .unwrap()
            .contains("SHA-256 mismatch")
    );
    fs::write(dir.path().join("inline.json"), b"{}").unwrap();
    assert!(
        load_inline_json(&path)
            .err()
            .unwrap()
            .contains("length mismatch")
    );
    fs::remove_file(dir.path().join("inline.json")).unwrap();
    assert!(
        load_inline_json(&path)
            .err()
            .unwrap()
            .contains("JSON artifact:")
    );
}

#[test]
fn rejects_unsupported_or_ambiguous_json_selection() {
    let (dir, manifest) = json_fixture();
    for (field, value) in [("state_id", "remote_observed"), ("encoding", "json_delta")] {
        let mut unsupported = manifest.clone();
        unsupported["scenarios"][0][field] = json!(value);
        assert!(
            load_inline_json(&write_manifest(&dir, &unsupported))
                .err()
                .unwrap()
                .contains("remote/delta inputs are unsupported")
        );
    }
    let mut duplicate = manifest.clone();
    duplicate["scenarios"]
        .as_array_mut()
        .unwrap()
        .push(manifest["scenarios"][0].clone());
    assert!(
        load_inline_json(&write_manifest(&dir, &duplicate))
            .err()
            .unwrap()
            .contains("multiple full inline JSON artifacts")
    );
    let mut old_version = manifest;
    old_version["schema_version"] = json!(1);
    assert!(
        load_inline_json(&write_manifest(&dir, &old_version))
            .err()
            .unwrap()
            .contains("unsupported synthetic bundle manifest version")
    );
}
