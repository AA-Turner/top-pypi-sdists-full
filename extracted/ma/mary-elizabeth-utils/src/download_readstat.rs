use anyhow::{Context, Result};
use flate2::read::GzDecoder;
use reqwest::Client;
use serde::Deserialize;
use std::fs::{create_dir_all, File};
use std::io::{copy, Read};
use std::path::{Path, PathBuf};
use tar::Archive;
use zip::ZipArchive;

#[derive(Deserialize)]
struct Asset {
    name: String,
    browser_download_url: String,
}

#[derive(Deserialize)]
struct Release {
    assets: Vec<Asset>,
}

const TARGET_ASSET_NAMES: &[(&str, &str)] = &[
    (
        "aarch64-apple-darwin",
        "readstat-v0.12.2-aarch64-apple-darwin.tar.gz",
    ),
    (
        "x86_64-apple-darwin",
        "readstat-v0.12.2-x86_64-apple-darwin.tar.gz",
    ),
    (
        "x86_64-pc-windows-msvc",
        "readstat-v0.12.2-x86_64-pc-windows-msvc.zip",
    ),
    (
        "x86_64-unknown-linux-gnu",
        "readstat-v0.12.2-x86_64-unknown-linux-gnu.tar.gz",
    ),
    (
        "x86_64-unknown-linux-musl",
        "readstat-v0.12.2-x86_64-unknown-linux-musl.tar.gz",
    ),
];

fn get_target_asset_name() -> &'static str {
    let target = std::env::consts::ARCH.to_owned() + "-" + std::env::consts::OS;
    TARGET_ASSET_NAMES
        .iter()
        .find(|&&(t, _)| t == target)
        .map(|&(_, name)| name)
        .unwrap_or_else(|| panic!("Unsupported target platform: {}", target))
}

fn get_binary_name() -> &'static str {
    if cfg!(target_os = "windows") {
        "readstat.exe"
    } else {
        "readstat"
    }
}

fn get_installation_dir() -> Result<PathBuf> {
    dirs::home_dir()
        .context("Could not determine home directory")
        .map(|mut path| {
            path.push(".mary_elizabeth_utils");
            path
        })
}

async fn download_and_extract_readstat() -> Result<()> {
    let client = Client::new();
    let release: Release = client
        .get("https://api.github.com/repos/curtisalexander/readstat-rs/releases/latest")
        .header("User-Agent", "readstat-downloader")
        .send()
        .await?
        .json()
        .await?;

    let target_asset_name = get_target_asset_name();
    let asset = release
        .assets
        .iter()
        .find(|a| a.name == target_asset_name)
        .context("No suitable asset found for this platform")?;

    let content = client
        .get(&asset.browser_download_url)
        .send()
        .await?
        .bytes()
        .await?;
    let install_dir = get_installation_dir()?;
    create_dir_all(&install_dir)?;

    match Path::new(&asset.name)
        .extension()
        .and_then(std::ffi::OsStr::to_str)
    {
        Some("gz") => extract_tar_gz(&content, &install_dir),
        Some("zip") => extract_zip(&content, &install_dir),
        _ => anyhow::bail!("Unsupported archive format"),
    }
}

fn write_binary<R: Read>(source: &mut R, install_dir: &Path) -> Result<()> {
    let dest_path = install_dir.join(get_binary_name());
    let mut dest = File::create(&dest_path)?;
    copy(source, &mut dest)?;

    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        dest.set_permissions(std::fs::Permissions::from_mode(0o755))?;
    }

    Ok(())
}

fn extract_tar_gz(content: &[u8], install_dir: &Path) -> Result<()> {
    let tar = GzDecoder::new(content);
    let mut archive = Archive::new(tar);

    for entry in archive.entries()? {
        let mut entry = entry?;
        if entry.path()?.file_name() == Some(get_binary_name().as_ref().into()) {
            return write_binary(&mut entry, install_dir);
        }
    }

    anyhow::bail!("Binary not found in archive")
}

fn extract_zip(content: &[u8], install_dir: &Path) -> Result<()> {
    let reader = std::io::Cursor::new(content);
    let mut archive = ZipArchive::new(reader)?;

    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        if file.name() == get_binary_name() {
            return write_binary(&mut file, install_dir);
        }
    }

    anyhow::bail!("Binary not found in archive")
}

pub fn ensure_readstat_binary() -> Result<()> {
    tokio::runtime::Runtime::new()?.block_on(download_and_extract_readstat())
}
