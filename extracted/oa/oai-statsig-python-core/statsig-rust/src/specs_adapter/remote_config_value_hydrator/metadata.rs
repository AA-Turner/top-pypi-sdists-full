use std::collections::HashMap;
use std::sync::Arc;

use serde::Deserialize;
use serde_json::value::RawValue;
use url::Url;

use crate::StatsigErr;

use super::TAG;
use super::errors::{HydrationFailureReason, hydration_error};

const DEFAULT_DOWNLOAD_ORIGIN: &str = "https://statsigcdn.openai.com";
pub(super) const DOWNLOAD_PATH_PREFIX: &str = "/v1/dynamic_config_value/";

pub(super) const MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC: usize = 16 * 1024 * 1024;
pub(super) const MAX_REMOTE_VALUE_BYTES: usize = 10 * 1024 * 1024;

// Keep the checksum and byte length independent of the untrusted placeholder
// URL, and keep the format fields explicit so future content types or
// compression modes do not require another metadata-envelope change.
#[derive(Clone, Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct RemoteConfigValueMetadataWire {
    pub(super) sha256: String,
    pub(super) byte_length: u64,
    pub(super) content_type: String,
    pub(super) compression: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub(super) struct RemoteConfigValueMetadata {
    pub(super) sha256: Sha256Digest,
    pub(super) byte_length: u64,
    pub(super) content_type: RemoteContentType,
    pub(super) compression: RemoteCompression,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub(super) struct Sha256Digest(String);

impl Sha256Digest {
    pub(super) fn as_str(&self) -> &str {
        &self.0
    }
}

impl std::fmt::Display for Sha256Digest {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(self.as_str())
    }
}

impl TryFrom<String> for Sha256Digest {
    type Error = StatsigErr;

    fn try_from(value: String) -> Result<Self, Self::Error> {
        if value.len() != 64
            || !value
                .bytes()
                .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        {
            return Err(hydration_error(
                HydrationFailureReason::InvalidSha256,
                "remote value sha256 must be 64 lowercase hexadecimal characters",
            ));
        }
        Ok(Self(value))
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub(super) enum RemoteContentType {
    ApplicationJson,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
pub(super) enum RemoteCompression {
    None,
    Gzip,
    Zstd,
}

impl RemoteContentType {
    pub(super) const fn as_str(self) -> &'static str {
        match self {
            Self::ApplicationJson => "application/json",
        }
    }
}

impl TryFrom<RemoteConfigValueMetadataWire> for RemoteConfigValueMetadata {
    type Error = StatsigErr;

    fn try_from(wire: RemoteConfigValueMetadataWire) -> Result<Self, Self::Error> {
        let sha256 = Sha256Digest::try_from(wire.sha256)?;
        if wire.byte_length > MAX_REMOTE_VALUE_BYTES as u64 {
            return Err(hydration_error(
                HydrationFailureReason::TotalBytesExceeded,
                &format!(
                    "remote value {sha256} declared {} bytes; maximum is {MAX_REMOTE_VALUE_BYTES}",
                    wire.byte_length
                ),
            ));
        }
        let content_type = if wire.content_type == RemoteContentType::ApplicationJson.as_str() {
            RemoteContentType::ApplicationJson
        } else {
            return Err(hydration_error(
                HydrationFailureReason::InvalidContentType,
                &format!(
                    "remote value {} declared unsupported content type {}",
                    sha256, wire.content_type
                ),
            ));
        };
        let compression = match wire.compression.as_str() {
            "none" => RemoteCompression::None,
            "gzip" => RemoteCompression::Gzip,
            "zstd" => RemoteCompression::Zstd,
            _ => {
                return Err(hydration_error(
                    HydrationFailureReason::InvalidCompression,
                    &format!(
                        "remote value {} declared unsupported compression {}",
                        sha256, wire.compression
                    ),
                ));
            }
        };
        Ok(Self {
            sha256,
            byte_length: wire.byte_length,
            content_type,
            compression,
        })
    }
}

#[derive(Clone, Debug)]
pub(super) struct RemoteValueReference {
    pub(super) download_url: Url,
    pub(super) metadata: RemoteConfigValueMetadata,
    pub(super) occurrences: usize,
}

pub(super) fn add_raw_value_reference(
    references: &mut HashMap<String, RemoteValueReference>,
    placeholder: Option<&RawValue>,
    metadata: RemoteConfigValueMetadata,
    source_url: &str,
) -> Result<(), StatsigErr> {
    let raw_url = raw_placeholder_url(placeholder.ok_or_else(|| {
        hydration_error(
            HydrationFailureReason::MetadataWithoutValue,
            &format!("remote metadata {} had no matching value", metadata.sha256),
        )
    })?)?;
    let download_url =
        resolve_and_validate_download_url(&raw_url, metadata.sha256.as_str(), source_url)?;
    let sha256 = metadata.sha256.to_string();
    insert_reference(
        references,
        sha256,
        RemoteValueReference {
            download_url,
            metadata,
            occurrences: 1,
        },
    )
}

fn raw_placeholder_url(value: &RawValue) -> Result<String, StatsigErr> {
    if let Ok(url) = serde_json::from_str::<String>(value.get()) {
        return Ok(url);
    }
    if !value.get().trim_start().starts_with('{') {
        return Err(hydration_error(
            HydrationFailureReason::InvalidPlaceholder,
            "remote metadata was attached to a non-URL value",
        ));
    }
    let object: HashMap<String, Box<RawValue>> = serde_json::from_str(value.get())
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_string(), error.to_string()))?;
    if object.len() != 1 {
        return Err(hydration_error(
            HydrationFailureReason::InvalidPlaceholder,
            "remote value placeholder must contain only the value field",
        ));
    }
    object
        .get("value")
        .and_then(|value| serde_json::from_str::<String>(value.get()).ok())
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::InvalidPlaceholder,
                "remote value placeholder did not contain a string value field",
            )
        })
}

pub(super) fn insert_reference(
    references: &mut HashMap<String, RemoteValueReference>,
    sha256: String,
    reference: RemoteValueReference,
) -> Result<(), StatsigErr> {
    let Some(existing) = references.get_mut(&sha256) else {
        references.insert(sha256, reference);
        return Ok(());
    };
    if existing.metadata != reference.metadata {
        return Err(hydration_error(
            HydrationFailureReason::MetadataConflict,
            &format!("remote value {sha256} had conflicting metadata"),
        ));
    }
    existing.occurrences = existing
        .occurrences
        .checked_add(reference.occurrences)
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::TooManyValues,
                "DCS remote value reference count overflowed",
            )
        })?;
    Ok(())
}

pub(super) fn validate_reference_limits<'a>(
    references: impl IntoIterator<Item = &'a RemoteValueReference>,
) -> Result<(usize, u64), StatsigErr> {
    let mut reference_count = 0usize;
    let mut total_metadata_bytes = 0usize;
    let mut total_bytes = 0u64;

    for reference in references {
        reference_count = reference_count
            .checked_add(reference.occurrences)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value reference count overflowed",
                )
            })?;
        let reference_metadata_bytes = std::mem::size_of::<RemoteValueReference>()
            .checked_add(reference.download_url.as_str().len())
            .and_then(|bytes| bytes.checked_add(reference.metadata.sha256.as_str().len()))
            .and_then(|bytes| bytes.checked_add(reference.metadata.content_type.as_str().len()))
            .and_then(|bytes| bytes.checked_mul(reference.occurrences))
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value metadata byte count overflowed",
                )
            })?;
        total_metadata_bytes = total_metadata_bytes
            .checked_add(reference_metadata_bytes)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TooManyValues,
                    "DCS remote value metadata byte count overflowed",
                )
            })?;
        if total_metadata_bytes > MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC {
            return Err(hydration_error(
                HydrationFailureReason::TooManyValues,
                &format!(
                    "DCS remote value metadata totaled {total_metadata_bytes} bytes; maximum is {MAX_REMOTE_VALUE_METADATA_BYTES_PER_SYNC}"
                ),
            ));
        }

        let reference_bytes = reference
            .metadata
            .byte_length
            .checked_mul(reference.occurrences as u64)
            .ok_or_else(|| {
                hydration_error(
                    HydrationFailureReason::TotalBytesExceeded,
                    "DCS remote value byte count overflowed",
                )
            })?;
        total_bytes = total_bytes.checked_add(reference_bytes).ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::TotalBytesExceeded,
                "DCS remote value byte count overflowed",
            )
        })?;
    }

    Ok((reference_count, total_bytes))
}

pub(super) fn resolve_and_validate_download_url(
    raw_url: &str,
    sha256: &str,
    source_url: &str,
) -> Result<Url, StatsigErr> {
    let source = Url::parse(source_url).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidSourceUrl,
            &format!("DCS source URL was invalid: {error}"),
        )
    })?;
    let url = source.join(raw_url).map_err(|error| {
        hydration_error(
            HydrationFailureReason::InvalidDownloadUrl,
            &format!("remote value download URL was invalid: {error}"),
        )
    })?;

    if !matches!(url.scheme(), "http" | "https") {
        return Err(hydration_error(
            HydrationFailureReason::InvalidDownloadScheme,
            "remote value download URL must use HTTP or HTTPS",
        ));
    }
    let source_origin = source.origin().ascii_serialization();
    let default_origin = Url::parse(DEFAULT_DOWNLOAD_ORIGIN)
        .expect("default remote value origin must be valid")
        .origin()
        .ascii_serialization();
    let download_origin = url.origin().ascii_serialization();
    if download_origin != source_origin && download_origin != default_origin {
        return Err(hydration_error(
            HydrationFailureReason::UntrustedDownloadOrigin,
            "remote value download URL used an unexpected origin",
        ));
    }

    let expected_path = format!("{DOWNLOAD_PATH_PREFIX}{sha256}");
    if url.path() != expected_path {
        return Err(hydration_error(
            HydrationFailureReason::DownloadPathMismatch,
            &format!(
                "remote value download path did not match metadata {}",
                sha256
            ),
        ));
    }
    if url.query().is_some() || url.fragment().is_some() {
        return Err(hydration_error(
            HydrationFailureReason::InvalidDownloadUrl,
            "remote value download URL must not include a query or fragment",
        ));
    }
    Ok(url)
}

pub(super) fn hydrated_value<'a>(
    hydrated: &'a HashMap<String, Arc<Vec<u8>>>,
    sha256: &str,
) -> Result<&'a [u8], StatsigErr> {
    hydrated
        .get(sha256)
        .map(|value| value.as_slice())
        .ok_or_else(|| {
            hydration_error(
                HydrationFailureReason::MissingHydratedValue,
                &format!("remote value {sha256} was not downloaded"),
            )
        })
}
