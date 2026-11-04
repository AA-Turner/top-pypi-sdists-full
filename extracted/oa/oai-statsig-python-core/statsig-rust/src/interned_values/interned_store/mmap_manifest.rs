use std::{
    fs::{File, create_dir_all},
    io::{Read, Seek, SeekFrom, Write},
    path::{Path, PathBuf},
    time::UNIX_EPOCH,
};

#[cfg(unix)]
use std::os::unix::fs::{MetadataExt, PermissionsExt};
#[cfg(windows)]
use std::os::windows::io::AsRawHandle;

use sha2::{Digest, Sha256};

use crate::{StatsigErr, log_w, specs_adapter::remote_config_value_hydrator::MmapRemoteValueProof};

use super::{MmapProjectId, TAG};

#[cfg(target_os = "linux")]
mod virtiofs;

const MAX_MMAP_MANIFEST_BYTES: usize = 64 * 1024;
const MAX_LEGACY_MMAP_REMOTE_VALUES: usize = 512;
const MAX_MMAP_REMOTE_VALUES: usize = 65_536;
const MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES: usize = 16 * 1024 * 1024;

#[derive(Clone, serde::Deserialize, serde::Serialize)]
pub(super) struct MmapBlobProvenance {
    pub(super) version: u32,
    pub(super) sdk_key_hash: [u8; 32],
    pub(super) artifact_sha256: String,
    pub(super) values: Vec<MmapRemoteValueProof>,
    pub(super) checksum: String,
}

impl MmapBlobProvenance {
    /// Detect corruption of the SHA-to-handle bindings as well as their scope.
    /// This checksum is not authentication against a malicious local writer.
    pub(super) fn has_valid_checksum(&self) -> bool {
        provenance_checksum(
            self.version,
            &self.sdk_key_hash,
            &self.artifact_sha256,
            &self.values,
        )
        .is_ok_and(|checksum| checksum == self.checksum)
    }
}

fn provenance_checksum(
    version: u32,
    sdk_key_hash: &[u8; 32],
    artifact_sha256: &str,
    values: &[MmapRemoteValueProof],
) -> Result<String, StatsigErr> {
    // A fixed tuple and the proof struct's field order give writer and reader
    // the same encoding, independently of whitespace in the manifest JSON.
    let bytes = serde_json::to_vec(&(version, sdk_key_hash, artifact_sha256, values))
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    Ok(Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect())
}

#[derive(serde::Deserialize, serde::Serialize)]
struct MmapManifest {
    // Serde ignores the retired `v1` identity in previously paired manifests.
    v2: MmapArtifactIdentity,
}

// Borrow the optional field only on the enabled path. The legacy deserializer
// skips it without allocating a provenance table or a captured JSON value.
#[derive(serde::Deserialize)]
struct MmapManifestWithRemoteValues<'a> {
    v2: MmapArtifactIdentity,
    #[serde(default, borrow)]
    remote_values: Option<&'a serde_json::value::RawValue>,
    #[serde(default, borrow)]
    remote_values_file: Option<&'a serde_json::value::RawValue>,
}

#[derive(serde::Serialize)]
struct MmapManifestWithRemoteValuesFileRef<'a> {
    #[serde(flatten)]
    manifest: &'a MmapManifest,
    remote_values_file: MmapRemoteValuesFileRef<'a>,
}

#[derive(serde::Deserialize)]
struct MmapRemoteValuesFile {
    version: u32,
    sha256: String,
}

#[derive(serde::Serialize)]
struct MmapRemoteValuesFileRef<'a> {
    version: u32,
    sha256: &'a str,
}

#[derive(serde::Deserialize)]
struct MmapRemoteValuesSidecar {
    v2: MmapArtifactIdentity,
    remote_values: MmapBlobProvenance,
}

#[derive(serde::Serialize)]
struct MmapRemoteValuesSidecarRef<'a> {
    v2: &'a MmapArtifactIdentity,
    remote_values: MmapBlobProvenanceRef<'a>,
}

#[derive(serde::Serialize)]
struct MmapBlobProvenanceRef<'a> {
    version: u32,
    sdk_key_hash: &'a [u8; 32],
    artifact_sha256: &'a str,
    values: &'a [MmapRemoteValueProof],
    checksum: &'a str,
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

pub(super) enum MmapV2Publication {
    Absent,
    Committed(File),
    Incomplete,
    Invalid(String),
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
        BY_HANDLE_FILE_INFORMATION, GetFileInformationByHandle,
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

pub(super) fn write_mmap_manifest(manifest_path: &Path, v2_file: &File) -> Result<(), StatsigErr> {
    let manifest = MmapManifest {
        v2: MmapArtifactIdentity::from_file(v2_file)?,
    };
    let bytes = serde_json::to_vec(&manifest)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    write_atomic_json_file(manifest_path, &bytes)
}

/// Publishes optional verified-value bindings in a bounded sidecar, preserving
/// the small manifest and V2 archive understood by existing readers.
pub(super) fn write_mmap_manifest_with_remote_values(
    manifest_path: &Path,
    v2_file: &File,
    project: MmapProjectId,
    mut values: Vec<MmapRemoteValueProof>,
) -> Result<(), StatsigErr> {
    if values.is_empty() {
        return write_mmap_manifest(manifest_path, v2_file);
    }

    values.sort_unstable_by(|left, right| left.sha256.cmp(&right.sha256));
    values.truncate(MAX_MMAP_REMOTE_VALUES);
    let artifact_digest = artifact_sha256(v2_file)?;
    let manifest = MmapManifest {
        v2: MmapArtifactIdentity::from_file(v2_file)?,
    };
    let encode = |count: usize, checksum: &str| {
        serde_json::to_vec(&MmapRemoteValuesSidecarRef {
            v2: &manifest.v2,
            remote_values: MmapBlobProvenanceRef {
                version: 1,
                sdk_key_hash: &project.sdk_key_hash,
                artifact_sha256: &artifact_digest,
                values: &values[..count],
                checksum,
            },
        })
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))
    };

    // Bound optional metadata independently of the legacy manifest's 64 KiB
    // limit. Very large tables retain a deterministic fitting prefix.
    let checksum = provenance_checksum(1, &project.sdk_key_hash, &artifact_digest, &values)?;
    let sidecar_bytes = encode(values.len(), &checksum)?;
    // Most tables fit in full; reuse the final encoding on this path.
    let sidecar_bytes = if sidecar_bytes.len() <= MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES {
        sidecar_bytes
    } else {
        drop(sidecar_bytes);
        let mut low = 0;
        let mut high = values.len() - 1;
        while low < high {
            let count = low + (high - low).div_ceil(2);
            // SHA-256 checksums have fixed encoded width, so the full table's
            // checksum gives the exact byte length for every candidate prefix.
            if encode(count, &checksum)?.len() <= MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES {
                low = count;
            } else {
                high = count - 1;
            }
        }
        if low == 0 {
            return write_mmap_manifest(manifest_path, v2_file);
        }
        let checksum =
            provenance_checksum(1, &project.sdk_key_hash, &artifact_digest, &values[..low])?;
        encode(low, &checksum)?
    };
    let sidecar_digest = sha256_hex(&sidecar_bytes);
    let bytes = serde_json::to_vec(&MmapManifestWithRemoteValuesFileRef {
        manifest: &manifest,
        remote_values_file: MmapRemoteValuesFileRef {
            version: 1,
            sha256: &sidecar_digest,
        },
    })
    .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

    // Replace the sidecar before committing its manifest reference. A reader
    // racing this replacement may lose the optimization, but its captured
    // manifest digest and V2 identity prevent using another generation's table.
    // A fixed sibling path also bounds retained metadata to one file per key.
    let sidecar_path = remote_values_sidecar_path(manifest_path);
    if let Err(error) = write_atomic_json_file(&sidecar_path, &sidecar_bytes) {
        log_w!(
            TAG,
            "Ignoring mmap blob provenance sidecar publication failure: {error}"
        );
        return write_mmap_manifest(manifest_path, v2_file);
    }
    write_atomic_json_file(manifest_path, &bytes)
}

fn remote_values_sidecar_path(manifest_path: &Path) -> PathBuf {
    manifest_path.with_extension("blob-proofs.json")
}

fn sha256_hex(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn write_atomic_json_file(path: &Path, bytes: &[u8]) -> Result<(), StatsigErr> {
    let mut file = new_manifest_temp_file(path)?;
    file.write_all(bytes)
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    sync_manifest_temp_file(&file)?;
    file.persist(path)
        .map(|_| ())
        .map_err(|error| StatsigErr::FileError(error.error.to_string()))
}

fn artifact_sha256(file: &File) -> Result<String, StatsigErr> {
    let mut file = file
        .try_clone()
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let position = file
        .stream_position()
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    file.rewind()
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let result: std::io::Result<String> = (|| {
        let mut digest = Sha256::new();
        let mut buffer = [0_u8; 64 * 1024];
        loop {
            let count = file.read(&mut buffer)?;
            if count == 0 {
                return Ok(digest
                    .finalize()
                    .iter()
                    .map(|byte| format!("{byte:02x}"))
                    .collect());
            }
            digest.update(&buffer[..count]);
        }
    })();
    // Cloned file handles share their offset on supported platforms. Restore
    // it even when hashing fails so this helper cannot change publication I/O.
    let restore = file.seek(SeekFrom::Start(position));
    match (result, restore) {
        (Ok(digest), Ok(_)) => Ok(digest),
        (Err(error), _) | (_, Err(error)) => Err(StatsigErr::FileError(error.to_string())),
    }
}

#[cfg(any(unix, windows))]
pub(super) fn inspect_mmap_v2_publication(
    manifest_path: &Path,
    v2_path: &Path,
) -> Result<MmapV2Publication, StatsigErr> {
    inspect_mmap_v2_publication_with_remote_values(manifest_path, v2_path, None)
        .map(|(publication, _)| publication)
}

#[cfg(any(unix, windows))]
fn inspect_mmap_v2_publication_with_remote_values(
    manifest_path: &Path,
    v2_path: &Path,
    project: Option<MmapProjectId>,
) -> Result<(MmapV2Publication, Option<MmapBlobProvenance>), StatsigErr> {
    let v2_file = match File::open(v2_path) {
        Ok(file) => Some(file),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => None,
        Err(error) => return Err(StatsigErr::FileError(error.to_string())),
    };
    let manifest_file = match File::open(manifest_path) {
        Ok(file) => file,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            return if v2_file.is_some() {
                Ok((MmapV2Publication::Incomplete, None))
            } else {
                Ok((MmapV2Publication::Absent, None))
            };
        }
        Err(error) => return Err(StatsigErr::FileError(error.to_string())),
    };
    let mut manifest_bytes = Vec::new();
    (&manifest_file)
        .take((MAX_MMAP_MANIFEST_BYTES + 1) as u64)
        .read_to_end(&mut manifest_bytes)
        .map_err(|error| StatsigErr::FileError(error.to_string()))?;
    if manifest_bytes.len() > MAX_MMAP_MANIFEST_BYTES {
        return Ok((
            MmapV2Publication::Invalid(format!(
                "mmap manifest exceeds {MAX_MMAP_MANIFEST_BYTES} bytes"
            )),
            None,
        ));
    }
    let parsed = if project.is_some() {
        serde_json::from_slice::<MmapManifestWithRemoteValues<'_>>(&manifest_bytes).map(
            |manifest| {
                (
                    MmapManifest { v2: manifest.v2 },
                    manifest.remote_values,
                    manifest.remote_values_file,
                )
            },
        )
    } else {
        serde_json::from_slice::<MmapManifest>(&manifest_bytes)
            .map(|manifest| (manifest, None, None))
    };
    let (manifest, remote_values, remote_values_file) = match parsed {
        Ok(manifest) => manifest,
        Err(error) => {
            return Ok((MmapV2Publication::Invalid(error.to_string()), None));
        }
    };
    let Some(v2_file) = v2_file else {
        return Ok((MmapV2Publication::Incomplete, None));
    };

    let current_v2 = MmapArtifactIdentity::from_file(&v2_file)?;
    let identity_matches = manifest.v2 == current_v2;
    #[cfg(target_os = "linux")]
    let identity_matches = identity_matches
        || virtiofs::matches_published_identity(
            &manifest,
            &manifest_bytes,
            &current_v2,
            &manifest_file,
            &v2_file,
            manifest_path,
            v2_path,
        );
    if !identity_matches {
        return Ok((MmapV2Publication::Incomplete, None));
    }

    let remote_values = project.and_then(|project| {
        if let Some(reference) = remote_values_file {
            // Bind proofs to the accepted publisher identity. Virtiofs may
            // translate its device ID; the reader also verifies archive bytes.
            return read_remote_values_sidecar(manifest_path, &manifest.v2, project, reference);
        }
        let provenance: MmapBlobProvenance = serde_json::from_str(remote_values?.get()).ok()?;
        (provenance.version == 1
            && provenance.sdk_key_hash == project.sdk_key_hash
            && provenance.values.len() <= MAX_LEGACY_MMAP_REMOTE_VALUES)
            .then_some(provenance)
    });
    Ok((MmapV2Publication::Committed(v2_file), remote_values))
}

#[cfg(any(unix, windows))]
fn read_remote_values_sidecar(
    manifest_path: &Path,
    expected_v2: &MmapArtifactIdentity,
    project: MmapProjectId,
    reference: &serde_json::value::RawValue,
) -> Option<MmapBlobProvenance> {
    let reference: MmapRemoteValuesFile = serde_json::from_str(reference.get()).ok()?;
    if reference.version != 1
        || reference.sha256.len() != 64
        || !reference
            .sha256
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return None;
    }

    // The manifest never supplies a filesystem path. Sidecar reads are bounded
    // and optional, so absence, corruption, and publication races preserve the
    // normal archive load and verified-download fallback.
    let file = File::open(remote_values_sidecar_path(manifest_path)).ok()?;
    let mut bytes = Vec::new();
    file.take((MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES + 1) as u64)
        .read_to_end(&mut bytes)
        .ok()?;
    if bytes.len() > MAX_MMAP_REMOTE_VALUES_SIDECAR_BYTES || sha256_hex(&bytes) != reference.sha256
    {
        return None;
    }
    let sidecar: MmapRemoteValuesSidecar = serde_json::from_slice(&bytes).ok()?;
    let provenance = sidecar.remote_values;
    (&sidecar.v2 == expected_v2
        && provenance.version == 1
        && provenance.sdk_key_hash == project.sdk_key_hash
        && provenance.values.len() <= MAX_MMAP_REMOTE_VALUES)
        .then_some(provenance)
}

#[cfg(all(test, any(unix, windows)))]
pub(super) fn open_committed_mmap_v2(
    manifest_path: &Path,
    v2_path: &Path,
) -> Result<Option<File>, StatsigErr> {
    committed_file(inspect_mmap_v2_publication(manifest_path, v2_path)?)
}

#[cfg(any(unix, windows))]
pub(super) fn open_committed_mmap_v2_with_remote_values(
    manifest_path: &Path,
    v2_path: &Path,
    project: MmapProjectId,
) -> Result<Option<(File, Option<MmapBlobProvenance>)>, StatsigErr> {
    let (publication, provenance) =
        inspect_mmap_v2_publication_with_remote_values(manifest_path, v2_path, Some(project))?;
    Ok(committed_file(publication)?.map(|file| (file, provenance)))
}

#[cfg(any(unix, windows))]
fn committed_file(publication: MmapV2Publication) -> Result<Option<File>, StatsigErr> {
    match publication {
        MmapV2Publication::Committed(file) => Ok(Some(file)),
        MmapV2Publication::Absent => Ok(None),
        MmapV2Publication::Invalid(error) => {
            log_w!(TAG, "Ignoring invalid mmap manifest: {error}");
            Ok(None)
        }
        MmapV2Publication::Incomplete => Err(incomplete_v2_publication()),
    }
}

#[cfg(any(unix, windows))]
fn incomplete_v2_publication() -> StatsigErr {
    StatsigErr::InvalidOperation(
        "Interned mmap V2 publication is incomplete; retry preload".to_string(),
    )
}

#[cfg(not(any(unix, windows)))]
pub(super) fn inspect_mmap_v2_publication(
    _manifest_path: &Path,
    _v2_path: &Path,
) -> Result<MmapV2Publication, StatsigErr> {
    Ok(MmapV2Publication::Absent)
}

#[cfg(not(any(unix, windows)))]

pub(super) fn open_committed_mmap_v2_with_remote_values(
    _manifest_path: &Path,
    _v2_path: &Path,
    _project: MmapProjectId,
) -> Result<Option<(File, Option<MmapBlobProvenance>)>, StatsigErr> {
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
    v2_path: &Path,
) -> Result<(), StatsigErr> {
    let v2_file = File::open(v2_path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    write_mmap_manifest(manifest_path, &v2_file)
}

#[cfg(all(test, any(unix, windows)))]
pub(crate) fn open_committed_mmap_v2_for_test(
    manifest_path: &Path,
    v2_path: &Path,
) -> Result<Option<File>, StatsigErr> {
    open_committed_mmap_v2(manifest_path, v2_path)
}

#[cfg(all(test, any(unix, windows)))]
#[path = "mmap_manifest_tests.rs"]
mod tests;
