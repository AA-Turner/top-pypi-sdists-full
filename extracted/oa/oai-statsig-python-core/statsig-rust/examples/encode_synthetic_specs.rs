//! Encode a generated bundle offline. Fixture setup belongs outside benchmark timing.
#[path = "support/synthetic_specs.rs"]
mod synthetic_specs;

use serde::Deserialize;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs,
    io::Read,
    path::{Component, Path, PathBuf},
};

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Deserialize)]
struct Artifact {
    file: String,
    bytes: u64,
    sha256: String,
}

#[derive(Deserialize)]
struct Scenario {
    state_id: String,
    encoding: String,
    #[serde(flatten)]
    artifact: Artifact,
}

#[derive(Deserialize)]
struct Transition {
    before: String,
    after: String,
}

#[derive(Deserialize)]
struct Manifest {
    schema_version: u32,
    profile: String,
    profile_sha256: String,
    scenarios: Vec<Scenario>,
    blobs: Vec<Artifact>,
    next_states: Vec<Transition>,
}

fn local_path(root: &Path, file: &str) -> Result<PathBuf> {
    if file.is_empty()
        || !Path::new(file)
            .components()
            .all(|part| matches!(part, Component::Normal(_)))
    {
        return Err(format!("expected a relative bundle file: {file}").into());
    }
    let path = root.join(file).canonicalize()?;
    if !path.starts_with(root) {
        return Err(format!("file escapes bundle directory: {file}").into());
    }
    Ok(path)
}

fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|byte| format!("{byte:02x}")).collect()
}

fn hash_file(path: &Path) -> Result<(u64, String)> {
    let mut file = fs::File::open(path)?;
    let mut hash = Sha256::new();
    let mut length = 0;
    let mut buffer = [0u8; 65536];
    loop {
        let count = file.read(&mut buffer)?;
        if count == 0 {
            break;
        }
        length += count as u64;
        hash.update(&buffer[..count]);
    }
    Ok((length, hex(&hash.finalize())))
}

fn load(root: &Path, scenario: &Scenario) -> Result<Value> {
    let bytes = fs::read(local_path(root, &scenario.artifact.file)?)?;
    // Check the same bytes we parse, even if an input changed since preflight.
    if bytes.len() as u64 != scenario.artifact.bytes
        || hex(&Sha256::digest(&bytes)) != scenario.artifact.sha256
    {
        return Err(format!("artifact hash/length mismatch: {}", scenario.artifact.file).into());
    }
    Ok(serde_json::from_slice(&bytes)?)
}

fn write_artifact(out: &Path, state: &str, base: Option<&str>, bytes: Vec<u8>) -> Result<Value> {
    let file = match base {
        Some(base) => format!("{base}--{state}.delta.pb.zst"),
        None => format!("{state}.full.pb.zst"),
    };
    let mut entry = json!({
        "state": state, "file": file,
        "encoding": if base.is_some() { "protobuf_delta" } else { "protobuf_full" },
        "content_encoding": "statsig-zstd", "bytes": bytes.len(),
        "sha256": hex(&Sha256::digest(&bytes)),
    });
    if let Some(base) = base {
        entry["base"] = json!(base);
    }
    fs::write(out.join(file), bytes)?;
    Ok(entry)
}

fn main() -> Result<()> {
    let mut manifest_path = None;
    let mut output = None;
    let mut args = std::env::args().skip(1);
    while let Some(flag) = args.next() {
        let slot = match flag.as_str() {
            "--manifest" => &mut manifest_path,
            "--out" => &mut output,
            _ => {
                return Err("usage: encode_synthetic_specs --manifest PATH --out EMPTY_DIR".into());
            }
        };
        if slot.is_some() {
            return Err(format!("duplicate argument {flag}").into());
        }
        *slot = Some(PathBuf::from(args.next().ok_or("missing argument value")?));
    }
    let manifest_path = manifest_path.ok_or("missing --manifest")?.canonicalize()?;
    let output = output.ok_or("missing --out")?;
    if output.exists() && fs::read_dir(&output)?.next().is_some() {
        return Err("output directory must be empty".into());
    }
    let source = fs::read(&manifest_path)?;
    let manifest: Manifest = serde_json::from_slice(&source)?;
    if manifest.schema_version != 2 {
        return Err("expected synthetic bundle schema_version 2".into());
    }
    let root = manifest_path.parent().ok_or("manifest has no parent")?;
    if hash_file(&local_path(root, &manifest.profile)?)?.1 != manifest.profile_sha256 {
        return Err("profile hash mismatch".into());
    }
    // Validate every source artifact before creating any encoded output.
    for artifact in manifest
        .scenarios
        .iter()
        .map(|scenario| &scenario.artifact)
        .chain(&manifest.blobs)
    {
        let (length, hash) = hash_file(&local_path(root, &artifact.file)?)?;
        if length != artifact.bytes || hash != artifact.sha256 {
            return Err(format!("artifact hash/length mismatch: {}", artifact.file).into());
        }
    }
    let mut states = BTreeMap::new();
    for scenario in &manifest.scenarios {
        if scenario.state_id.is_empty()
            || !scenario
                .state_id
                .bytes()
                .all(|byte| byte.is_ascii_alphanumeric() || byte == b'_')
        {
            return Err("state IDs must contain only letters, digits, or underscores".into());
        }
        if scenario.encoding != "json_full"
            || states
                .insert(scenario.state_id.as_str(), scenario)
                .is_some()
        {
            return Err("expected unique json_full scenarios".into());
        }
    }
    for transition in &manifest.next_states {
        if !states.contains_key(transition.before.as_str())
            || !states.contains_key(transition.after.as_str())
        {
            return Err("transition references an unknown state".into());
        }
    }
    fs::create_dir_all(&output)?;
    let mut artifacts = Vec::new();
    for scenario in &manifest.scenarios {
        let state = load(root, scenario)?;
        artifacts.push(write_artifact(
            &output,
            &scenario.state_id,
            None,
            synthetic_specs::encode_full(&state)?,
        )?);
    }
    for transition in &manifest.next_states {
        let before = load(root, states[transition.before.as_str()])?;
        let after = load(root, states[transition.after.as_str()])?;
        artifacts.push(write_artifact(
            &output,
            &transition.after,
            Some(&transition.before),
            synthetic_specs::encode_delta(&before, &after)?,
        )?);
    }
    let result = json!({
        "schema_version": 1,
        "source_manifest": { "path": manifest_path, "sha256": hex(&Sha256::digest(&source)) },
        "artifacts": artifacts,
    });
    fs::write(
        output.join("manifest.json"),
        serde_json::to_vec_pretty(&result)?,
    )?;
    println!(
        "Encoded {} artifacts in {}",
        artifacts.len(),
        output.display()
    );
    Ok(())
}
