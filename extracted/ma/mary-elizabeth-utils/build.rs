// use anyhow::{Context, Result};
// use flate2::read::GzDecoder;
// use reqwest::blocking::get;
// use std::env;
// use std::fs;
// use std::io::Cursor;
// use std::path::Path;
// use tar::Archive;

// fn main() -> Result<()> {
//     // Download and extract ReadStat binary
//     download_and_extract_readstat()?;

//     // Tell cargo to re-run this if the build script changes
//     println!("cargo:rerun-if-changed=build.rs");

//     Ok(())
// }

// fn download_and_extract_readstat() -> Result<()> {
//     // Determine architecture and platform
//     let target_arch = env::var("CARGO_CFG_TARGET_ARCH")?;
//     let target_os = env::var("CARGO_CFG_TARGET_OS")?;
//     let target = format!("{}-{}", target_arch, target_os);

//     println!("Debug: target_arch = {}", target_arch);
//     println!("Debug: target_os = {}", target_os);
//     println!("Debug: target = {}", target);

//     // Match the correct binary based on platform
//     let (url, archive_ext) = match (target_arch.as_str(), target_os.as_str()) {
//         ("x86_64", "macos") | ("x86_64", "darwin") =>
//             ("https://github.com/curtisalexander/readstat-rs/releases/download/v0.12.2/readstat-v0.12.2-x86_64-apple-darwin.tar.gz", "tar.gz"),
//         ("aarch64", "macos") | ("aarch64", "darwin") =>
//             ("https://github.com/curtisalexander/readstat-rs/releases/download/v0.12.2/readstat-v0.12.2-aarch64-apple-darwin.tar.gz", "tar.gz"),
//         ("x86_64", "windows") =>
//             ("https://github.com/curtisalexander/readstat-rs/releases/download/v0.12.2/readstat-v0.12.2-x86_64-pc-windows-msvc.zip", "zip"),
//         ("x86_64", "linux") =>
//             ("https://github.com/curtisalexander/readstat-rs/releases/download/v0.12.2/readstat-v0.12.2-x86_64-unknown-linux-gnu.tar.gz", "tar.gz"),
//         _ => return Err(anyhow::anyhow!("Unsupported target platform: {}", target)),
//     };

//     // Download the binary
//     let response = get(url).context("Failed to download ReadStat binary")?;
//     let out_dir = env::var("OUT_DIR")?;
//     let dest_path = Path::new(&out_dir).join("readstat_binary");

//     fs::create_dir_all(&dest_path)?;

//     // Extract the archive
//     if archive_ext == "tar.gz" {
//         let tar = GzDecoder::new(Cursor::new(response.bytes()?));
//         let mut archive = Archive::new(tar);
//         archive
//             .unpack(&dest_path)
//             .context("Failed to extract ReadStat binary")?;
//     } else if archive_ext == "zip" {
//         let mut zip = zip::ZipArchive::new(Cursor::new(response.bytes()?))
//             .context("Failed to open ZIP archive")?;
//         zip.extract(&dest_path)
//             .context("Failed to extract ZIP archive")?;
//     }

//     // Copy the binary to the final location
//     let binary_name = if target_os == "windows" {
//         "readstat.exe"
//     } else {
//         "readstat"
//     };

//     // Define the path for the Python package bin directory
//     let package_binary_path = Path::new("python")
//         .join("mary_elizabeth_utils")
//         .join("bin")
//         .join(binary_name);

//     // Create the directory if it doesn't exist
//     fs::create_dir_all(package_binary_path.parent().unwrap())?;

//     // Copy the binary to the Python package bin directory
//     fs::copy(dest_path.join(binary_name), &package_binary_path)?;

//     // Set the READSTAT_BINARY environment variable
//     println!(
//         "cargo:rustc-env=READSTAT_BINARY={}",
//         package_binary_path.display()
//     );

//     Ok(())
// }

fn main() {
    println!("Hello, world!")
}
