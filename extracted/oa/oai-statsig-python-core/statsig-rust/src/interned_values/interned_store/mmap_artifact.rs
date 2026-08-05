use std::{fs::Metadata, path::Path, time::UNIX_EPOCH};

use crate::StatsigErr;

use super::{
    InternedStore, LEGACY_MMAP_FORMAT_VERSION, legacy_mmap_v1_path_for_sdk_key,
    mmap_manifest::{MmapV2Publication, inspect_mmap_v2_publication},
    mmap_manifest_path_for_sdk_key, mmap_v2_path_for_sdk_key,
};

/// Describes the interned mmap artifacts linked at the SDK-owned location.
///
/// This intentionally omits the SDK key, filesystem path, and platform-specific
/// file identity used to validate publication. V1 states are informational;
/// the V2-only reader rejects them.
#[non_exhaustive]
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum MmapArtifactState {
    /// No V1 artifact or V2 publication is linked at the SDK-owned location.
    Missing,
    /// A legacy V1 artifact is linked and no V2 publication was observed.
    LegacyV1,
    /// A V2 publication failed manifest identity validation while a legacy V1
    /// artifact remains linked.
    FallbackV1,
    /// The V2 artifact and manifest identities match.
    CommittedV2,
    /// A V2-only artifact and manifest do not form a committed identity, so
    /// readers must retry rather than fall back.
    IncompleteV2,
    /// V2 publication validation failed and no V1 fallback is linked.
    Invalid,
}

impl MmapArtifactState {
    /// Returns a stable, bounded label suitable for telemetry.
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Missing => "missing",
            Self::LegacyV1 => "legacy_v1",
            Self::FallbackV1 => "fallback_v1",
            Self::CommittedV2 => "committed_v2",
            Self::IncompleteV2 => "incomplete_v2",
            Self::Invalid => "invalid",
        }
    }
}

/// Safe metadata for an SDK-owned interned mmap artifact.
///
/// Byte counts cover only currently linked V1, V2, and manifest files. They do
/// not include unlinked generations that remain mapped by readers or transient
/// writer files. State and format reflect a reader-selectable publication
/// observed during inspection. Linked file sizes and modification times are
/// best-effort and may span a concurrent atomic publication. Filesystem
/// capacity is best-effort and is omitted on unsupported platforms or when the
/// backing filesystem cannot be inspected. A reported V1 format is not
/// selectable by the V2-only reader.
#[non_exhaustive]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MmapArtifactSnapshot {
    pub state: MmapArtifactState,
    /// Format of the linked legacy or committed artifact. Unavailable or
    /// invalid artifacts report `None`.
    pub format_version: Option<u32>,
    pub v1_bytes: Option<u64>,
    pub v2_bytes: Option<u64>,
    pub manifest_bytes: Option<u64>,
    pub total_linked_bytes: u64,
    pub linked_file_count: u64,
    /// Newest whole-second modification timestamp among the linked files.
    pub newest_linked_modified_unix_seconds: Option<u64>,
    pub filesystem_capacity_bytes: Option<u64>,
    pub filesystem_available_bytes: Option<u64>,
}

impl InternedStore {
    /// Inspects the SDK-owned artifact without exposing its derived path or file
    /// identity.
    ///
    /// V2 state uses the same committed-manifest identity validation as
    /// `preload_mmap`. The snapshot is informational and does not map or parse
    /// either archived config payload.
    pub fn inspect_mmap_artifact(sdk_key: &str) -> Result<MmapArtifactSnapshot, StatsigErr> {
        let v1_path = legacy_mmap_v1_path_for_sdk_key(sdk_key);
        let v2_path = mmap_v2_path_for_sdk_key(sdk_key);
        let manifest_path = mmap_manifest_path_for_sdk_key(sdk_key);

        let publication = inspect_mmap_v2_publication(&manifest_path, &v1_path, &v2_path)?;
        let v1_metadata = metadata_if_linked(&v1_path)?;
        let manifest_metadata = metadata_if_linked(&manifest_path)?;

        let (state, format_version, committed_v2_metadata) = match publication {
            MmapV2Publication::Absent if v1_metadata.is_some() => (
                MmapArtifactState::LegacyV1,
                Some(LEGACY_MMAP_FORMAT_VERSION),
                None,
            ),
            MmapV2Publication::Absent => (MmapArtifactState::Missing, None, None),
            MmapV2Publication::Committed(file) => {
                let metadata = file
                    .metadata()
                    .map_err(|error| StatsigErr::FileError(error.to_string()))?;
                (
                    MmapArtifactState::CommittedV2,
                    Some(crate::interned_values::INTERNED_MMAP_FORMAT_VERSION),
                    Some(metadata),
                )
            }
            MmapV2Publication::Incomplete => (MmapArtifactState::IncompleteV2, None, None),
            MmapV2Publication::Invalid(_) if v1_metadata.is_some() => (
                MmapArtifactState::FallbackV1,
                Some(LEGACY_MMAP_FORMAT_VERSION),
                None,
            ),
            MmapV2Publication::Invalid(_) => (MmapArtifactState::Invalid, None, None),
        };

        let v2_metadata = match committed_v2_metadata {
            Some(metadata) => Some(metadata),
            None => metadata_if_linked(&v2_path)?,
        };
        let v1_bytes = v1_metadata.as_ref().map(Metadata::len);
        let v2_bytes = v2_metadata.as_ref().map(Metadata::len);
        let manifest_bytes = manifest_metadata.as_ref().map(Metadata::len);
        let total_linked_bytes = [v1_bytes, v2_bytes, manifest_bytes]
            .into_iter()
            .flatten()
            .fold(0_u64, u64::saturating_add);
        let linked_file_count = [v1_bytes, v2_bytes, manifest_bytes]
            .into_iter()
            .filter(Option::is_some)
            .count() as u64;
        let newest_linked_modified_unix_seconds = [
            v1_metadata.as_ref(),
            v2_metadata.as_ref(),
            manifest_metadata.as_ref(),
        ]
        .into_iter()
        .flatten()
        .filter_map(modified_unix_seconds)
        .max();
        let (filesystem_capacity_bytes, filesystem_available_bytes) = manifest_path
            .parent()
            .map(filesystem_space)
            .unwrap_or((None, None));

        Ok(MmapArtifactSnapshot {
            state,
            format_version,
            v1_bytes,
            v2_bytes,
            manifest_bytes,
            total_linked_bytes,
            linked_file_count,
            newest_linked_modified_unix_seconds,
            filesystem_capacity_bytes,
            filesystem_available_bytes,
        })
    }
}

fn metadata_if_linked(path: &Path) -> Result<Option<Metadata>, StatsigErr> {
    match path.metadata() {
        Ok(metadata) => Ok(Some(metadata)),
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => Ok(None),
        Err(error) => Err(StatsigErr::FileError(error.to_string())),
    }
}

fn modified_unix_seconds(metadata: &Metadata) -> Option<u64> {
    metadata
        .modified()
        .ok()?
        .duration_since(UNIX_EPOCH)
        .ok()
        .map(|duration| duration.as_secs())
}

#[cfg(any(unix, windows))]
fn filesystem_space(path: &Path) -> (Option<u64>, Option<u64>) {
    fs4::statvfs(path)
        .map(|stats| (Some(stats.total_space()), Some(stats.available_space())))
        .unwrap_or((None, None))
}

#[cfg(not(any(unix, windows)))]
fn filesystem_space(_path: &Path) -> (Option<u64>, Option<u64>) {
    (None, None)
}
