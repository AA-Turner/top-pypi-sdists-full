use std::{
    env,
    error::Error,
    io,
    path::{Path, PathBuf},
    process::Command,
};

const VERSION_ENV: &str = "CHALK_LSP_VERSION";

fn main() -> Result<(), Box<dyn Error>> {
    configure_version();
    generate_cheapo_supported_funcs()?;
    Ok(())
}

fn configure_version() {
    println!("cargo:rerun-if-env-changed={VERSION_ENV}");
    println!("cargo:rerun-if-changed=../../.git/HEAD");
    println!("cargo:rerun-if-changed=../../.git/refs/heads");
    println!("cargo:rerun-if-changed=../../.git/refs/tags");
    println!("cargo:rerun-if-changed=../../.git/packed-refs");

    let version = std::env::var(VERSION_ENV)
        .ok()
        .filter(|version| !version.is_empty())
        .unwrap_or_else(local_git_version);

    println!("cargo:rustc-env={VERSION_ENV}={version}");
}

fn generate_cheapo_supported_funcs() -> Result<(), Box<dyn Error>> {
    let manifest_dir = PathBuf::from(env::var("CARGO_MANIFEST_DIR")?);
    let out_path = PathBuf::from(env::var("OUT_DIR")?).join("cheapo_supported_funcs.rs");
    let generator = manifest_dir.join("scripts/generate_supported_funcs.py");
    let supported_funcs = manifest_dir.join("scripts/SUPPORTED_FUNCS.data");

    println!("cargo:rerun-if-changed={}", generator.display());
    println!("cargo:rerun-if-changed={}", supported_funcs.display());

    run_generator(&generator, &supported_funcs, &out_path)
}

fn run_generator(
    generator: &Path,
    supported_funcs: &Path,
    out_path: &Path,
) -> Result<(), Box<dyn Error>> {
    let output = Command::new("python3")
        .arg(generator)
        .arg(supported_funcs)
        .arg("-o")
        .arg(out_path)
        .output()
        .map_err(|err| {
            io::Error::new(
                err.kind(),
                format!(
                    "failed to run supported-function generator {}: {err}",
                    generator.display()
                ),
            )
        })?;

    if output.status.success() {
        return Ok(());
    }

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);
    Err(io::Error::new(
        io::ErrorKind::Other,
        format!(
            "supported-function generator failed with status {}: stdout={stdout:?} stderr={stderr:?}",
            output.status
        ),
    )
    .into())
}

fn local_git_version() -> String {
    let output = Command::new("git").args(["describe", "--tags"]).output();

    match output {
        Ok(output) if output.status.success() => {
            let version = String::from_utf8_lossy(&output.stdout).trim().to_owned();
            if !version.is_empty() {
                return version;
            }
        }
        _ => {}
    }

    env::var("CARGO_PKG_VERSION").unwrap_or_else(|_| "unknown".to_owned())
}
