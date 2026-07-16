use std::{
    fs::{create_dir_all, File},
    path::Path,
    time::UNIX_EPOCH,
};

#[cfg(unix)]
use std::os::unix::fs::{MetadataExt, PermissionsExt};
#[cfg(windows)]
use std::os::windows::io::AsRawHandle;

use crate::{log_w, StatsigErr};

use super::TAG;

#[derive(serde::Deserialize, serde::Serialize)]
struct MmapManifest {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    v1: Option<MmapArtifactIdentity>,
    v2: MmapArtifactIdentity,
}

#[derive(Eq, PartialEq, serde::Deserialize, serde::Serialize)]
struct MmapArtifactIdentity {
    len: u64,
    modified_secs: u64,
    modified_nanos: u32,
    #[cfg(unix)]
    device: u64,
    #[cfg(unix)]
    inode: u64,
    #[cfg(windows)]
    volume_serial_number: Option<u32>,
    #[cfg(windows)]
    file_index: Option<u64>,
}

impl MmapArtifactIdentity {
    fn from_file(file: &File) -> Result<Self, StatsigErr> {
        let metadata = file
            .metadata()
            .map_err(|error| StatsigErr::FileError(error.to_string()))?;
        let modified = metadata
            .modified()
            .map_err(|error| StatsigErr::FileError(error.to_string()))?
            .duration_since(UNIX_EPOCH)
            .map_err(|error| StatsigErr::FileError(error.to_string()))?;
        #[cfg(windows)]
        let (volume_serial_number, file_index) = windows_file_identity(file)?;

        Ok(Self {
            len: metadata.len(),
            modified_secs: modified.as_secs(),
            modified_nanos: modified.subsec_nanos(),
            #[cfg(unix)]
            device: metadata.dev(),
            #[cfg(unix)]
            inode: metadata.ino(),
            #[cfg(windows)]
            volume_serial_number: Some(volume_serial_number),
            #[cfg(windows)]
            file_index: Some(file_index),
        })
    }
}

#[cfg(windows)]
fn windows_file_identity(file: &File) -> Result<(u32, u64), StatsigErr> {
    use windows_sys::Win32::Storage::FileSystem::{
        GetFileInformationByHandle, BY_HANDLE_FILE_INFORMATION,
    };

    let mut information = unsafe { std::mem::zeroed::<BY_HANDLE_FILE_INFORMATION>() };
    let succeeded = unsafe { GetFileInformationByHandle(file.as_raw_handle(), &mut information) };
    if succeeded == 0 {
        return Err(StatsigErr::FileError(
            std::io::Error::last_os_error().to_string(),
        ));
    }

    let file_index =
        (u64::from(information.nFileIndexHigh) << 32) | u64::from(information.nFileIndexLow);
    Ok((information.dwVolumeSerialNumber, file_index))
}

pub(super) fn write_mmap_manifest(
    manifest_path: &Path,
    v1_file: Option<&File>,
    v2_file: &File,
) -> Result<(), StatsigErr> {
    let manifest = MmapManifest {
        v1: v1_file.map(MmapArtifactIdentity::from_file).transpose()?,
        v2: MmapArtifactIdentity::from_file(v2_file)?,
    };
    let mut file = new_manifest_temp_file(manifest_path)?;
    serde_json::to_writer(file.as_file_mut(), &manifest)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    sync_manifest_temp_file(&file)?;
    file.persist(manifest_path)
        .map(|_| ())
        .map_err(|error| StatsigErr::FileError(error.error.to_string()))
}

#[cfg(any(unix, windows))]
pub(super) fn open_committed_mmap_v2(
    manifest_path: &Path,
    v1_path: &Path,
    v2_path: &Path,
) -> Result<Option<File>, StatsigErr> {
    let v2_file = match File::open(v2_path) {
        Ok(file) => Some(file),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => None,
        Err(error) => return Err(StatsigErr::FileError(error.to_string())),
    };
    let manifest_bytes = match std::fs::read(manifest_path) {
        Ok(bytes) => bytes,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            return if v2_file.is_some() {
                Err(incomplete_v2_publication())
            } else {
                Ok(None)
            };
        }
        Err(error) => return Err(StatsigErr::FileError(error.to_string())),
    };
    let manifest: MmapManifest = match serde_json::from_slice(&manifest_bytes) {
        Ok(manifest) => manifest,
        Err(error) => {
            log_w!(TAG, "Ignoring invalid mmap manifest: {error}");
            return Ok(None);
        }
    };
    let Some(v2_file) = v2_file else {
        return if manifest.v1.is_none() {
            Err(incomplete_v2_publication())
        } else {
            Ok(None)
        };
    };

    let current_v2 = MmapArtifactIdentity::from_file(&v2_file)?;
    if manifest.v2 != current_v2 {
        return if manifest.v1.is_none() {
            Err(incomplete_v2_publication())
        } else {
            Ok(None)
        };
    }

    if let Some(expected_v1) = manifest.v1 {
        let v1_file = match File::open(v1_path) {
            Ok(file) => file,
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(None),
            Err(error) => return Err(StatsigErr::FileError(error.to_string())),
        };
        if expected_v1 != MmapArtifactIdentity::from_file(&v1_file)? {
            return Ok(None);
        }
    }

    Ok(Some(v2_file))
}

#[cfg(any(unix, windows))]
fn incomplete_v2_publication() -> StatsigErr {
    StatsigErr::InvalidOperation(
        "Interned mmap V2 publication is incomplete; retry preload".to_string(),
    )
}

#[cfg(not(any(unix, windows)))]
pub(super) fn open_committed_mmap_v2(
    _manifest_path: &Path,
    _v1_path: &Path,
    _v2_path: &Path,
) -> Result<Option<File>, StatsigErr> {
    Ok(None)
}

fn new_manifest_temp_file(path: &Path) -> Result<tempfile::NamedTempFile, StatsigErr> {
    let parent = path
        .parent()
        .ok_or_else(|| StatsigErr::FileError("Mmap manifest path has no parent".to_string()))?;
    create_dir_all(parent).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    tempfile::NamedTempFile::new_in(parent)
        .map_err(|error| StatsigErr::FileError(error.to_string()))
}

fn sync_manifest_temp_file(file: &tempfile::NamedTempFile) -> Result<(), StatsigErr> {
    #[cfg(unix)]
    file.as_file()
        .set_permissions(std::fs::Permissions::from_mode(0o644))
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    file.as_file()
        .sync_all()
        .map_err(|error| StatsigErr::FileError(error.to_string()))
}

#[cfg(test)]
pub(crate) fn write_mmap_manifest_for_test(
    manifest_path: &Path,
    v1_path: &Path,
    v2_path: &Path,
) -> Result<(), StatsigErr> {
    let v1_file = File::open(v1_path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let v2_file = File::open(v2_path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    write_mmap_manifest(manifest_path, Some(&v1_file), &v2_file)
}

#[cfg(test)]
pub(crate) fn write_mmap_v2_only_manifest_for_test(
    manifest_path: &Path,
    v2_path: &Path,
) -> Result<(), StatsigErr> {
    let v2_file = File::open(v2_path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    write_mmap_manifest(manifest_path, None, &v2_file)
}

#[cfg(all(test, any(unix, windows)))]
pub(crate) fn open_committed_mmap_v2_for_test(
    manifest_path: &Path,
    v1_path: &Path,
    v2_path: &Path,
) -> Result<Option<File>, StatsigErr> {
    open_committed_mmap_v2(manifest_path, v1_path, v2_path)
}

#[cfg(all(test, any(unix, windows)))]
mod tests {
    use super::*;

    #[test]
    fn manifest_from_persisted_handles_rejects_replaced_path() {
        let directory = tempfile::tempdir().unwrap();
        let v1_path = directory.path().join("v1.mmap");
        let v2_path = directory.path().join("v2.mmap");
        let manifest_path = directory.path().join("manifest.json");

        let v1_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(v1_temp.path(), b"writer v1").unwrap();
        let v1_file = v1_temp.persist(&v1_path).unwrap();
        let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(v2_temp.path(), b"writer v2").unwrap();
        let v2_file = v2_temp.persist(&v2_path).unwrap();

        let replacement = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(replacement.path(), b"legacy writer v1").unwrap();
        replacement.persist(&v1_path).unwrap();

        write_mmap_manifest(&manifest_path, Some(&v1_file), &v2_file).unwrap();
        assert!(open_committed_mmap_v2(&manifest_path, &v1_path, &v2_path)
            .unwrap()
            .is_none());
    }

    #[test]
    fn v2_only_manifest_does_not_require_v1_artifact() {
        let directory = tempfile::tempdir().unwrap();
        let v1_path = directory.path().join("missing-v1.mmap");
        let v2_path = directory.path().join("v2.mmap");
        let manifest_path = directory.path().join("manifest.json");

        let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(v2_temp.path(), b"writer v2").unwrap();
        let v2_file = v2_temp.persist(&v2_path).unwrap();
        write_mmap_manifest(&manifest_path, None, &v2_file).unwrap();

        assert!(open_committed_mmap_v2(&manifest_path, &v1_path, &v2_path)
            .unwrap()
            .is_some());
    }

    #[test]
    fn v2_only_manifest_rejects_replaced_v2_artifact() {
        let directory = tempfile::tempdir().unwrap();
        let v1_path = directory.path().join("stale-v1.mmap");
        let v2_path = directory.path().join("v2.mmap");
        let manifest_path = directory.path().join("manifest.json");

        std::fs::write(&v1_path, b"stale v1").unwrap();
        let v2_temp = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(v2_temp.path(), b"writer v2").unwrap();
        let v2_file = v2_temp.persist(&v2_path).unwrap();
        write_mmap_manifest(&manifest_path, None, &v2_file).unwrap();

        let replacement = tempfile::NamedTempFile::new_in(directory.path()).unwrap();
        std::fs::write(replacement.path(), b"next writer v2").unwrap();
        replacement.persist(&v2_path).unwrap();

        assert!(matches!(
            open_committed_mmap_v2(&manifest_path, &v1_path, &v2_path),
            Err(StatsigErr::InvalidOperation(message))
                if message == "Interned mmap V2 publication is incomplete; retry preload"
        ));
    }

    #[test]
    fn v2_without_manifest_requires_retry() {
        let directory = tempfile::tempdir().unwrap();
        let v1_path = directory.path().join("stale-v1.mmap");
        let v2_path = directory.path().join("v2.mmap");
        let manifest_path = directory.path().join("missing-manifest.json");
        std::fs::write(&v1_path, b"stale v1").unwrap();
        std::fs::write(&v2_path, b"writer v2").unwrap();

        assert!(matches!(
            open_committed_mmap_v2(&manifest_path, &v1_path, &v2_path),
            Err(StatsigErr::InvalidOperation(message))
                if message == "Interned mmap V2 publication is incomplete; retry preload"
        ));
    }
}
