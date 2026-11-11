// Shared by benchmark targets that each use only one input format.
#![allow(dead_code)]

use std::{fs, path::Path};

use serde::Deserialize;
use sha2::{Digest, Sha256};

pub struct SyntheticSpecsFixture {
    pub bytes: Vec<u8>,
    pub content_encoding: String,
    pub product: String,
    pub seed: serde_json::Number,
    pub sha256: String,
}

#[derive(Deserialize)]
struct SourceManifest {
    path: String,
    sha256: String,
}

#[derive(Deserialize)]
struct Artifact {
    state: String,
    file: String,
    encoding: String,
    content_encoding: String,
    bytes: u64,
    sha256: String,
}

#[derive(Deserialize)]
struct EncodingManifest {
    schema_version: u64,
    source_manifest: SourceManifest,
    artifacts: Vec<Artifact>,
}

#[derive(Deserialize)]
struct BundleIdentity {
    schema_version: u64,
    product: String,
    seed: serde_json::Number,
}

fn verify_sha256(bytes: &[u8], expected: &str, label: &str) -> Result<(), String> {
    let actual: String = Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    if actual != expected {
        return Err(format!(
            "{label} SHA-256 mismatch: expected {expected}, got {actual}"
        ));
    }
    Ok(())
}

fn read_bundle_artifact(root: &Path, file: &str) -> Result<Vec<u8>, String> {
    let relative = Path::new(file);
    let root = root.join(".").canonicalize().map_err(|e| e.to_string())?;
    let path = root
        .join(relative)
        .canonicalize()
        .map_err(|e| e.to_string())?;
    if !relative
        .components()
        .all(|c| matches!(c, std::path::Component::Normal(_)))
        || !path.starts_with(&root)
        || !path.is_file()
    {
        return Err("expected a regular artifact file inside the bundle".into());
    }
    fs::read(path).map_err(|e| e.to_string())
}

fn read_verified_artifact(
    root: &Path,
    file: &str,
    expected_bytes: u64,
    expected_sha256: &str,
    label: &str,
) -> Result<Vec<u8>, String> {
    let bytes = read_bundle_artifact(root, file).map_err(|error| format!("{label}: {error}"))?;
    if bytes.len() as u64 != expected_bytes {
        return Err(format!(
            "{label} length mismatch: expected {expected_bytes}, got {}",
            bytes.len()
        ));
    }
    verify_sha256(&bytes, expected_sha256, label)?;
    Ok(bytes)
}

/// Verify the full inline protobuf artifact before any measured work.
pub fn load_inline_protobuf(manifest_path: &Path) -> Result<SyntheticSpecsFixture, String> {
    let manifest_bytes = fs::read(manifest_path).map_err(|error| error.to_string())?;
    let manifest: EncodingManifest =
        serde_json::from_slice(&manifest_bytes).map_err(|error| error.to_string())?;
    if manifest.schema_version != 1 {
        return Err("unsupported protobuf encoding manifest version".into());
    }
    let root = manifest_path.parent().unwrap_or_else(|| Path::new("."));
    let source_path = root.join(&manifest.source_manifest.path);
    if !source_path.is_file() {
        return Err(format!(
            "expected a regular source manifest file: {}",
            source_path.display()
        ));
    }
    let source_bytes =
        fs::read(source_path).map_err(|error| format!("source manifest: {error}"))?;
    verify_sha256(
        &source_bytes,
        &manifest.source_manifest.sha256,
        "source manifest",
    )?;
    let identity: BundleIdentity =
        serde_json::from_slice(&source_bytes).map_err(|error| error.to_string())?;
    if identity.schema_version != 2 {
        return Err("unsupported synthetic bundle manifest version".into());
    }
    let mut candidates = manifest
        .artifacts
        .into_iter()
        .filter(|artifact| artifact.state == "inline" && artifact.encoding == "protobuf_full");
    let artifact = candidates.next().ok_or(
        "manifest must contain a full inline protobuf artifact; remote/delta inputs are unsupported",
    )?;
    if candidates.next().is_some() {
        return Err("manifest contains multiple full inline protobuf artifacts".into());
    }
    if !matches!(
        artifact.content_encoding.as_str(),
        "statsig-zstd" | "statsig-br"
    ) {
        return Err(format!(
            "unsupported protobuf content encoding: {}",
            artifact.content_encoding
        ));
    }
    let bytes = read_verified_artifact(
        root,
        &artifact.file,
        artifact.bytes,
        &artifact.sha256,
        "protobuf artifact",
    )?;
    Ok(SyntheticSpecsFixture {
        bytes,
        content_encoding: artifact.content_encoding,
        product: identity.product,
        seed: identity.seed,
        sha256: artifact.sha256,
    })
}

#[derive(Deserialize)]
struct JsonScenario {
    state_id: String,
    encoding: String,
    file: String,
    bytes: u64,
    sha256: String,
}

#[derive(Deserialize)]
struct JsonManifest {
    #[serde(flatten)]
    identity: BundleIdentity,
    scenarios: Vec<JsonScenario>,
}

/// Resolve only the complete inline JSON state, before any measured work.
pub fn load_inline_json(manifest_path: &Path) -> Result<SyntheticSpecsFixture, String> {
    let manifest_bytes = fs::read(manifest_path).map_err(|error| error.to_string())?;
    let manifest: JsonManifest =
        serde_json::from_slice(&manifest_bytes).map_err(|error| error.to_string())?;
    if manifest.identity.schema_version != 2 {
        return Err("unsupported synthetic bundle manifest version".into());
    }
    let mut candidates = manifest
        .scenarios
        .iter()
        .filter(|scenario| scenario.state_id == "inline" && scenario.encoding == "json_full");
    let artifact = candidates.next().ok_or(
        "manifest must contain a full inline JSON artifact; remote/delta inputs are unsupported",
    )?;
    if candidates.next().is_some() {
        return Err("manifest contains multiple full inline JSON artifacts".into());
    }
    let root = manifest_path.parent().unwrap_or_else(|| Path::new("."));
    let bytes = read_verified_artifact(
        root,
        &artifact.file,
        artifact.bytes,
        &artifact.sha256,
        "JSON artifact",
    )?;
    Ok(SyntheticSpecsFixture {
        bytes,
        content_encoding: "identity".into(),
        product: manifest.identity.product,
        seed: manifest.identity.seed,
        sha256: artifact.sha256.clone(),
    })
}

pub fn evaluation_json() -> String {
    let Some(path) = std::env::var_os("STATSIG_BENCH_MANIFEST") else {
        println!("population fixture: statsig-rust/tests/data/perf_proj_dcs.json");
        return include_str!("../data/perf_proj_dcs.json").to_owned();
    };
    let fixture = load_inline_json(Path::new(&path))
        .unwrap_or_else(|error| panic!("invalid STATSIG_BENCH_MANIFEST: {error}"));
    println!(
        "population fixture: synthetic-inline product={} seed={} sha256={} bytes={}",
        fixture.product,
        fixture.seed,
        fixture.sha256,
        fixture.bytes.len()
    );
    String::from_utf8(fixture.bytes).expect("inline JSON must be UTF-8")
}
