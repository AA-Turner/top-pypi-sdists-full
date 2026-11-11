use super::*;
use crate::id_lists_adapter::IdListIds;
use crate::id_lists_adapter::shared_id_list_format::{IdListImage, digest, hex};
use crate::portable_id_list_ef::{MAX_IMAGE_BYTES, RECORD_BYTES};
use std::io::{self, Read};

#[derive(Clone, Copy)]
enum SnapshotFormat {
    EliasFanoV1,
}

const SUPPORTED_FORMATS: [SnapshotFormat; 1] = [SnapshotFormat::EliasFanoV1];

impl SnapshotFormat {
    fn media_type(self) -> &'static str {
        match self {
            Self::EliasFanoV1 => crate::portable_id_list_ef::MEDIA_TYPE,
        }
    }

    fn from_content_type(value: &str) -> Option<Self> {
        SUPPORTED_FORMATS
            .into_iter()
            .find(|format| format.media_type() == value)
    }

    fn decode(self, bytes: Vec<u8>, raw_end: u64) -> io::Result<IdListImage> {
        match self {
            Self::EliasFanoV1 => IdListImage::from_ef_v1_snapshot(bytes, raw_end),
        }
    }
}

pub(super) fn accept_header_value() -> String {
    SUPPORTED_FORMATS.map(SnapshotFormat::media_type).join(", ")
}

#[cfg(not(feature = "custom_network_provider"))]
pub(crate) fn accepts_snapshot(value: &str) -> bool {
    value
        .split(',')
        .any(|entry| SnapshotFormat::from_content_type(entry.trim()).is_some())
}

pub(super) fn supports_snapshots(endpoint: &url::Url) -> bool {
    matches!(endpoint.scheme(), "http" | "https")
        && endpoint.username().is_empty()
        && endpoint.password().is_none()
        && endpoint.query().is_none()
        && endpoint.fragment().is_none()
}

pub(super) fn source_changed(
    current: Option<&IdListMetadata>,
    target: &IdListMetadata,
    private_target: bool,
) -> bool {
    current.is_some_and(|old| old.url != target.url && (private_target || private_generation(old)))
}

fn is_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

pub(super) fn private_generation(metadata: &IdListMetadata) -> bool {
    metadata
        .file_id
        .as_deref()
        .is_some_and(|id| private_generation_url(&metadata.url, id))
}

pub(super) fn is_snapshot_response(body: &ResponseData) -> bool {
    body.header_values("content-type").any(|value| {
        let name = media_type_without_parameters(value);
        SUPPORTED_FORMATS.iter().any(|format| {
            name.eq_ignore_ascii_case(media_type_without_parameters(format.media_type()))
        })
    }) || [
        "x-statsig-id-list-raw-end",
        "x-statsig-id-list-file-id",
        "x-statsig-id-list-sha256",
    ]
    .iter()
    .any(|key| body.get_header_ignore_ascii_case(key).is_some())
}

fn media_type_without_parameters(value: &str) -> &str {
    value.split_once(';').map_or(value, |(name, _)| name).trim()
}

fn private_generation_url(raw: &str, generation: &str) -> bool {
    let Ok(url) = url::Url::parse(raw) else {
        return false;
    };
    let Some(encoded) = url.path().strip_prefix("/v1/download_id_list_file/") else {
        return false;
    };
    let Some((scope, file)) = encoded.split_once("%2F") else {
        return false;
    };
    let valid_segment = |s: &str| {
        !s.is_empty()
            && !matches!(s, "." | "..")
            && s.bytes()
                .all(|b| b.is_ascii_alphanumeric() || matches!(b, b'-' | b'_' | b'.'))
    };
    let Some((base, account)) = file.split_once(".regional.") else {
        return false;
    };
    valid_segment(scope)
        && !scope.contains(".regional.")
        && valid_segment(base)
        && (3..=24).contains(&account.len())
        && account
            .bytes()
            .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit())
        && file == generation
        && matches!(url.scheme(), "http" | "https")
        && url.username().is_empty()
        && url.password().is_none()
        && url.query() == Some("private=true")
        && url.fragment().is_none()
}

fn read_verified_snapshot(body: &mut ResponseData, expected_digest: &str) -> io::Result<Vec<u8>> {
    let mut bytes = Vec::new();
    body.get_stream_mut()
        .take(MAX_IMAGE_BYTES as u64 + 1)
        .read_to_end(&mut bytes)?;
    if bytes.len() > MAX_IMAGE_BYTES {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "snapshot exceeds maximum image size",
        ));
    }
    if hex(&digest(&bytes)) != expected_digest {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "snapshot digest mismatch",
        ));
    }
    Ok(bytes)
}

impl StatsigHttpIdListsAdapter {
    pub(super) async fn validate_snapshot(
        &self,
        job: &IdListDownloadJob,
        response: Response,
        download_permit: tokio::sync::OwnedSemaphorePermit,
        build: Option<&PrivateBuildAttempt>,
    ) -> Result<IdList, StatsigErr> {
        // Retry invalid encoded data as raw on the next authorized primary attempt.
        let invalid_response = |reason: String| {
            StatsigErr::NetworkError(NetworkError::RequestFailed(
                job.primary_url.clone(),
                response.status_code,
                reason,
            ))
        };
        let invalid = || invalid_response("invalid ID-list snapshot".into());
        let mut body = response.data.ok_or_else(invalid)?;
        let header = |key| {
            let mut values = body.header_values(key);
            let first = values.next()?;
            values.next().is_none().then_some(first)
        };
        let format = header("content-type")
            .and_then(SnapshotFormat::from_content_type)
            .ok_or_else(invalid)?;
        if response.status_code != Some(200)
            || body.get_header_ignore_ascii_case("content-range").is_some()
            || body
                .get_header_ignore_ascii_case("content-encoding")
                .is_some()
            || header("x-statsig-id-list-file-id") != job.metadata.file_id.as_deref()
        {
            return Err(invalid());
        }
        let end = header("x-statsig-id-list-raw-end")
            .filter(|s| s.bytes().all(|b| b.is_ascii_digit()))
            .and_then(|s| s.parse::<u64>().ok())
            .filter(|&end| {
                end > 0 && end <= job.metadata.size && end.is_multiple_of(RECORD_BYTES as u64)
            })
            .ok_or_else(invalid)?;
        let expected = header("x-statsig-id-list-sha256")
            .filter(|s| is_sha256(s))
            .ok_or_else(invalid)?
            .to_owned();
        // Keep the download slot while the body is live. The build slot covers only
        // validation and is released before a raw retry.
        let build_permit = match build {
            Some(build) => Some(build.admit_worker().await),
            None => None,
        };
        let stopped = Arc::clone(self.network.shutdown_flag());
        let image = tokio::task::spawn_blocking(move || {
            let _permits = (download_permit, build_permit);
            if stopped.load(Ordering::SeqCst) {
                return Err(StatsigHttpIdListsAdapter::publication_stopped());
            }
            let image = read_verified_snapshot(&mut body, &expected)
                .and_then(|bytes| format.decode(bytes, end));
            Ok(image)
        })
        .await
        .map_err(|e| StatsigErr::ThreadFailure(e.to_string()))??
        .map_err(|error| invalid_response(error.to_string()))?;
        let mut metadata = job.metadata.clone();
        metadata.size = end;
        Ok(IdList {
            metadata,
            ids: Arc::new(IdListIds::from_image(image)),
        })
    }
}
