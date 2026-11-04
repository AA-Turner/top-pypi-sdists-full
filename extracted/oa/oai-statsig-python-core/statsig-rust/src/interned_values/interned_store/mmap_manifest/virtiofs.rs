use std::{fs::File, io::Read, os::fd::AsRawFd, os::unix::fs::MetadataExt, path::Path};

use super::{MmapArtifactIdentity, MmapManifest};

const ALLOW_DEVICE_TRANSLATION: &str = "STATSIG_MMAP_ALLOW_VIRTIOFS_DEVICE_TRANSLATION";
const MAX_PROC_FILE_BYTES: u64 = 1024 * 1024;

/// A virtiofs guest sees a different device ID from the host. Operators must
/// verify that both files are direct children of one host directory on the same
/// filesystem: guest device IDs cannot reveal host-side per-file mounts.
pub(super) fn matches_published_identity(
    manifest: &MmapManifest,
    manifest_bytes: &[u8],
    current: &MmapArtifactIdentity,
    manifest_file: &File,
    artifact_file: &File,
    manifest_path: &Path,
    artifact_path: &Path,
) -> bool {
    if !is_translation_candidate(
        std::env::var(ALLOW_DEVICE_TRANSLATION).as_deref().ok(),
        manifest,
        current,
        manifest_path,
        artifact_path,
    ) || !is_v2_only_manifest(manifest_bytes)
    {
        return false;
    }

    let (Ok(manifest_metadata), Ok(artifact_metadata)) =
        (manifest_file.metadata(), artifact_file.metadata())
    else {
        return false;
    };
    manifest_metadata.is_file()
        && artifact_metadata.is_file()
        && manifest_metadata.dev() == artifact_metadata.dev()
        && is_virtiofs_file(artifact_file).unwrap_or(false)
}

fn is_translation_candidate(
    setting: Option<&str>,
    manifest: &MmapManifest,
    current: &MmapArtifactIdentity,
    manifest_path: &Path,
    artifact_path: &Path,
) -> bool {
    setting == Some("1")
        && manifest_path.parent() == artifact_path.parent()
        && manifest.v2.device != current.device
        && manifest.v2
            == MmapArtifactIdentity {
                device: manifest.v2.device,
                ..*current
            }
}

fn is_v2_only_manifest(bytes: &[u8]) -> bool {
    #[derive(serde::Deserialize)]
    struct LegacyIdentity {
        v1: Option<serde::de::IgnoredAny>,
    }

    // The V2 reader ignores legacy identities, but translation is limited to V2-only manifests.
    serde_json::from_slice::<LegacyIdentity>(bytes).is_ok_and(|identity| identity.v1.is_none())
}

fn is_virtiofs_file(file: &File) -> Option<bool> {
    let fdinfo = read_proc_text(format!("/proc/self/fdinfo/{}", file.as_raw_fd()))?;
    let mount_id = fdinfo
        .lines()
        .find_map(|line| line.strip_prefix("mnt_id:"))?
        .trim()
        .parse::<u64>()
        .ok()?;
    let mountinfo = read_proc_text("/proc/self/mountinfo")?;
    Some(
        mountinfo
            .lines()
            .any(|line| is_virtiofs_mount(line, mount_id)),
    )
}

fn is_virtiofs_mount(line: &str, mount_id: u64) -> bool {
    let Some((mount, filesystem)) = line.split_once(" - ") else {
        return false;
    };
    mount
        .split_whitespace()
        .next()
        .and_then(|id| id.parse::<u64>().ok())
        == Some(mount_id)
        && filesystem.split_whitespace().next() == Some("virtiofs")
}

fn read_proc_text(path: impl AsRef<Path>) -> Option<String> {
    let mut text = String::new();
    File::open(path)
        .ok()?
        .take(MAX_PROC_FILE_BYTES + 1)
        .read_to_string(&mut text)
        .ok()?;
    (text.len() <= MAX_PROC_FILE_BYTES as usize).then_some(text)
}

#[cfg(test)]
mod tests;
