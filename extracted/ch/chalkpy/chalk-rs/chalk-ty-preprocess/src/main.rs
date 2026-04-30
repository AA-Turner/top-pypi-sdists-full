use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{bail, Context, Result};
use clap::Parser;
use walkdir::WalkDir;

use chalk_ty_preprocess::transform::{generate_feature_stubs, transform_source};
use chalk_ty_preprocess::type_map::{
    build_type_map, load_graph_from_bytes, load_graph_from_export_bytes, load_type_map_from_json,
    TypeMap,
};

#[derive(Parser, Debug)]
#[command(
    name = "chalk-ty-preprocess",
    about = "Pre-process Chalk Python code for type checking with ty"
)]
struct Args {
    /// Path to the Chalk project directory containing Python source files.
    #[arg(long)]
    project_dir: PathBuf,

    /// Path to a serialized protograph (Export or Graph protobuf).
    /// If not provided, runs `chalk apply --export` to generate one.
    #[arg(long)]
    protograph: Option<PathBuf>,

    /// Output directory for transformed files. Defaults to <project_dir>/.chalk-ty-check/
    #[arg(long)]
    output_dir: Option<PathBuf>,

    /// Skip running `ty check` after transformation.
    #[arg(long)]
    no_check: bool,

    /// Extra arguments to pass to `ty check`.
    #[arg(long)]
    ty_args: Vec<String>,

    /// Treat the protograph as a raw Graph message instead of an Export wrapper.
    #[arg(long)]
    raw_graph: bool,

    /// Path to a Python environment or venv to use for module resolution.
    /// If not provided, auto-detects .venv or venv in the project directory.
    #[arg(long)]
    python: Option<PathBuf>,
}

fn main() -> Result<()> {
    let args = Args::parse();

    let project_dir = args
        .project_dir
        .canonicalize()
        .context("project_dir does not exist")?;

    let output_dir = args
        .output_dir
        .unwrap_or_else(|| project_dir.join(".chalk-ty-check"));

    // Step 1: Load the protograph.
    let type_map = load_type_map(&args.protograph, &project_dir, args.raw_graph)?;

    eprintln!(
        "Loaded protograph: {} feature classes, {} features",
        type_map.class_fields.len(),
        type_map.features.len()
    );

    // Step 2: Create output directory.
    if output_dir.exists() {
        fs::remove_dir_all(&output_dir).context("failed to clean output directory")?;
    }
    fs::create_dir_all(&output_dir).context("failed to create output directory")?;

    // Step 3: Generate feature class stubs.
    let stubs = generate_feature_stubs(&type_map);
    let stubs_path = output_dir.join("_chalk_stubs.py");
    fs::write(&stubs_path, &stubs).context("failed to write stubs file")?;
    eprintln!("Wrote feature stubs to {}", stubs_path.display());

    // Step 4: Transform Python source files.
    let mut transformed_count = 0u32;
    let mut copied_count = 0u32;

    for entry in WalkDir::new(&project_dir)
        .into_iter()
        .filter_entry(|e| !is_hidden_or_output(e, &output_dir))
    {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let path = entry.path();
        let Some(ext) = path.extension() else {
            continue;
        };
        if ext != "py" {
            continue;
        }

        let relative = path
            .strip_prefix(&project_dir)
            .context("file not under project_dir")?;
        let dest = output_dir.join(relative);
        if let Some(parent) = dest.parent() {
            fs::create_dir_all(parent)?;
        }

        let source = fs::read_to_string(path)
            .with_context(|| format!("failed to read {}", path.display()))?;

        match transform_source(&source, &type_map) {
            Some(transformed) => {
                fs::write(&dest, &transformed)?;
                transformed_count += 1;
                eprintln!("  transformed: {}", relative.display());
            }
            None => {
                // Copy unmodified — ty needs all files to resolve imports.
                fs::write(&dest, &source)?;
                copied_count += 1;
            }
        }
    }

    eprintln!(
        "\nTransformed {transformed_count} files, copied {copied_count} files to {}",
        output_dir.display()
    );

    // Step 5: Optionally run ty check.
    if !args.no_check {
        eprintln!("\nRunning ty check...\n");
        let mut cmd = Command::new("ty");
        cmd.arg("check");
        cmd.arg(&output_dir);

        // Point ty at the project's Python environment for module resolution.
        let python_env = args.python.clone().or_else(|| {
            // Auto-detect venv in project directory.
            let venv = project_dir.join(".venv");
            if venv.exists() {
                return Some(venv);
            }
            let venv = project_dir.join("venv");
            if venv.exists() {
                return Some(venv);
            }
            None
        });
        if let Some(ref env_path) = python_env {
            cmd.arg("--python").arg(env_path);
            eprintln!("Using Python environment: {}", env_path.display());
        }

        // Add the output directory as an extra search path so stubs are found.
        cmd.arg("--extra-search-path").arg(&output_dir);

        for arg in &args.ty_args {
            cmd.arg(arg);
        }
        let status = cmd
            .status()
            .context("failed to run `ty check` — is ty installed?")?;
        if !status.success() {
            std::process::exit(status.code().unwrap_or(1));
        }
    }

    Ok(())
}

fn load_type_map(
    protograph_path: &Option<PathBuf>,
    project_dir: &Path,
    raw_graph: bool,
) -> Result<TypeMap> {
    match protograph_path {
        Some(path) => {
            let bytes = fs::read(path)
                .with_context(|| format!("failed to read protograph at {}", path.display()))?;

            // Try protobuf first, then JSON as fallback.
            if let Ok(graph) = if raw_graph {
                load_graph_from_bytes(&bytes)
            } else {
                load_graph_from_export_bytes(&bytes).or_else(|_| load_graph_from_bytes(&bytes))
            } {
                return Ok(build_type_map(&graph));
            }

            // Try JSON (Go-style proto JSON).
            if let Ok(type_map) = load_type_map_from_json(&bytes) {
                eprintln!("Loaded graph from JSON format");
                return Ok(type_map);
            }

            bail!(
                "failed to decode protograph as protobuf or JSON from {}",
                path.display()
            );
        }
        None => {
            // Try to run `chalk apply --export` to get the protograph.
            eprintln!("No protograph provided, running `chalk apply --export`...");
            let output = Command::new("chalk")
                .args([
                    "apply",
                    "--dir",
                    &project_dir.to_string_lossy(),
                    "--export-graph-path",
                    "/dev/stdout",
                ])
                .output()
                .context("failed to run `chalk apply` — is chalk installed?")?;
            if !output.status.success() {
                let stderr = String::from_utf8_lossy(&output.stderr);
                bail!("chalk apply failed:\n{stderr}");
            }
            let graph = load_graph_from_export_bytes(&output.stdout)
                .or_else(|_| load_graph_from_bytes(&output.stdout))?;
            Ok(build_type_map(&graph))
        }
    }
}

fn is_hidden_or_output(entry: &walkdir::DirEntry, output_dir: &Path) -> bool {
    let path = entry.path();
    // Skip the output directory itself.
    if path.starts_with(output_dir) {
        return true;
    }
    // Skip hidden directories and common non-source directories.
    if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
        if name.starts_with('.')
            || name == "__pycache__"
            || name == "node_modules"
            || name == ".venv"
            || name == "venv"
        {
            return true;
        }
    }
    false
}
