mod config;
mod fs;
mod inode;
mod s3;

use crate::config::Config;
use crate::fs::LazyDvcFs;
use crate::inode::InodeTree;
use crate::s3::S3Downloader;
use fuser::MountOption;
use log::info;
use std::path::PathBuf;

fn main() {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info")).init();

    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <config_path>", args[0]);
        std::process::exit(1);
    }

    let config = Config::from_file(&args[1]).unwrap_or_else(|e| {
        eprintln!("Failed to parse config: {}", e);
        std::process::exit(1);
    });

    let overlay_dir = PathBuf::from(&config.cache_dir).join("overlay");
    let cache_dir = PathBuf::from(&config.cache_dir);
    let mountpoint = PathBuf::from(&config.mountpoint);

    std::fs::create_dir_all(&overlay_dir).unwrap_or_else(|e| {
        eprintln!(
            "Failed to create overlay dir {}: {}",
            overlay_dir.display(),
            e
        );
        std::process::exit(1);
    });
    std::fs::create_dir_all(&cache_dir.join("cache")).unwrap_or_else(|e| {
        eprintln!("Failed to create cache dir: {}", e);
        std::process::exit(1);
    });

    // Build inode tree
    let mut tree = InodeTree::new();
    tree.build_from_manifest(&config.manifest.entries);
    tree.scan_overlay(&overlay_dir);

    // S3 downloader (only if bucket is non-empty)
    let s3 = if !config.s3_config.bucket.is_empty() {
        Some(S3Downloader::new(config.s3_config))
    } else {
        None
    };

    let filesystem = LazyDvcFs::new(tree, overlay_dir, cache_dir, s3);

    info!(
        "Mounting FUSE at {} ({} manifest entries)",
        mountpoint.display(),
        config.manifest.entries.len()
    );

    let options = vec![
        MountOption::FSName("lazydvc".to_string()),
        MountOption::AllowOther,
        MountOption::RW,
    ];

    fuser::mount2(filesystem, &mountpoint, &options).unwrap_or_else(|e| {
        eprintln!("FUSE mount failed: {}", e);
        std::process::exit(1);
    });
}
