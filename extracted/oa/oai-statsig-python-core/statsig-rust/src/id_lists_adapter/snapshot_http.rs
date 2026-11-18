use super::*;
use crate::id_lists_adapter::IdListIds;
use crate::id_lists_adapter::shared_id_list_format::{IdListImage, digest, hex, invalid};
use crate::portable_id_list_ef::{MAX_IMAGE_BYTES, MEDIA_TYPE, RECORD_BYTES};
use std::io::{self, Read};

pub(super) fn supports_snapshots(endpoint: &url::Url) -> bool {
    matches!(endpoint.scheme(), "http" | "https")
        && endpoint.username().is_empty()
        && endpoint.password().is_none()
        && endpoint.query().is_none()
        && endpoint.fragment().is_none()
}

fn is_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

pub(super) fn is_snapshot_response(body: &ResponseData) -> bool {
    body.header_values("content-type").any(|value| {
        media_type_without_parameters(value)
            .eq_ignore_ascii_case(media_type_without_parameters(MEDIA_TYPE))
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

fn read_verified_snapshot(body: &mut ResponseData, expected_digest: &str) -> io::Result<Vec<u8>> {
    let encoding = {
        let mut values = body.header_values("content-encoding");
        let first = values.next().unwrap_or("identity").trim();
        if values.next().is_some() {
            return Err(invalid("multiple snapshot content encodings"));
        }
        first
    };

    // Reqwest strips Content-Encoding if it already decoded the body.
    let reader: &mut dyn Read = match encoding {
        s if s.eq_ignore_ascii_case("identity") => body.get_stream_mut(),
        s if s.eq_ignore_ascii_case("gzip") => {
            &mut flate2::read::MultiGzDecoder::new(body.get_stream_mut())
        }
        s if s.eq_ignore_ascii_case("zstd") => {
            &mut zstd::stream::read::Decoder::new(body.get_stream_mut())?
        }
        s if s.eq_ignore_ascii_case("br") => {
            &mut brotli::Decompressor::new(body.get_stream_mut(), 32 * 1024)
        }
        s if s.eq_ignore_ascii_case("deflate") => {
            &mut flate2::read::ZlibDecoder::new(body.get_stream_mut())
        }
        _ => return Err(invalid("unsupported snapshot content encoding")),
    };

    let mut bytes = Vec::new();
    reader
        .take(MAX_IMAGE_BYTES as u64 + 1)
        .read_to_end(&mut bytes)?;
    if bytes.len() > MAX_IMAGE_BYTES {
        return Err(invalid("snapshot exceeds maximum image size"));
    }
    if hex(&digest(&bytes)) != expected_digest {
        return Err(invalid("snapshot digest mismatch"));
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
        let file_id = header("x-statsig-id-list-file-id")
            .filter(|id| !id.is_empty())
            .ok_or_else(invalid)?;
        if response.status_code != Some(200)
            || header("content-type") != Some(MEDIA_TYPE)
            || body.get_header_ignore_ascii_case("content-range").is_some()
            || Some(file_id) != job.metadata.file_id.as_deref()
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
        let image = tokio::task::spawn_blocking(id_list_load_timing::with_current_timings(
            Phase::BuildWorkerWait,
            move || {
                let _permits = (download_permit, build_permit);
                if stopped.load(Ordering::SeqCst) {
                    return Err(StatsigHttpIdListsAdapter::publication_stopped());
                }
                let image = id_list_load_timing::measure(Phase::Decode, || {
                    read_verified_snapshot(&mut body, &expected)
                        .and_then(|bytes| IdListImage::from_ef_v1_snapshot(bytes, end))
                });
                Ok(image)
            },
        ))
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
