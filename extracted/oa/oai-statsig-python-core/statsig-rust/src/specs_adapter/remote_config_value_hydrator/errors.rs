use crate::StatsigErr;

// The checkpoint detecting expiry, not necessarily where the budget was consumed.
#[derive(Clone, Copy, Debug)]
pub(super) enum HydrationTimeoutStep {
    Response,
    PermitPrecheck,
    PermitWait,
    DownloadPrecheck,
    DownloadWait,
}

impl HydrationTimeoutStep {
    pub(super) fn as_str(self) -> &'static str {
        match self {
            Self::Response => "response",
            Self::PermitPrecheck => "permit_precheck",
            Self::PermitWait => "permit_wait",
            Self::DownloadPrecheck => "download_precheck",
            Self::DownloadWait => "download_wait",
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(super) enum HydrationFailureReason {
    TotalTimeout,
    DownloadFailed,
    BodyReadFailed,
    EmptyResponse,
    MissingResponseContentType,
    MissingProtoData,
    MetadataWithoutValue,
    MetadataConflict,
    TooManyValues,
    TotalBytesExceeded,
    InvalidDefaultMetadata,
    InvalidMetadata,
    InvalidPlaceholder,
    InvalidSha256,
    InvalidContentType,
    InvalidCompression,
    InvalidSourceUrl,
    InvalidDownloadUrl,
    InvalidDownloadScheme,
    UntrustedDownloadOrigin,
    DownloadPathMismatch,
    ByteLengthMismatch,
    ResponseContentTypeMismatch,
    ChecksumMismatch,
    InvalidJson,
    InvalidProtoWireType,
    MissingHydratedValue,
}

impl HydrationFailureReason {
    // Keep metric labels bounded even though StatsigErr carries a diagnostic string.
    pub(super) fn from_error(error: &StatsigErr) -> Option<Self> {
        let StatsigErr::CustomError(message) = error else {
            return None;
        };
        let (reason, _) = message
            .strip_prefix("Dynamic config hydration failure: ")?
            .split_once(": ")?;
        [
            Self::TotalTimeout,
            Self::DownloadFailed,
            Self::BodyReadFailed,
            Self::EmptyResponse,
            Self::MissingResponseContentType,
            Self::MissingProtoData,
            Self::MetadataWithoutValue,
            Self::MetadataConflict,
            Self::TooManyValues,
            Self::TotalBytesExceeded,
            Self::InvalidDefaultMetadata,
            Self::InvalidMetadata,
            Self::InvalidPlaceholder,
            Self::InvalidSha256,
            Self::InvalidContentType,
            Self::InvalidCompression,
            Self::InvalidSourceUrl,
            Self::InvalidDownloadUrl,
            Self::InvalidDownloadScheme,
            Self::UntrustedDownloadOrigin,
            Self::DownloadPathMismatch,
            Self::ByteLengthMismatch,
            Self::ResponseContentTypeMismatch,
            Self::ChecksumMismatch,
            Self::InvalidJson,
            Self::InvalidProtoWireType,
            Self::MissingHydratedValue,
        ]
        .into_iter()
        .find(|candidate| candidate.as_str() == reason)
    }

    pub(super) const fn as_str(self) -> &'static str {
        match self {
            Self::TotalTimeout => "total_timeout",
            Self::DownloadFailed => "download_failed",
            Self::BodyReadFailed => "body_read_failed",
            Self::EmptyResponse => "empty_response",
            Self::MissingResponseContentType => "missing_response_content_type",
            Self::MissingProtoData => "missing_proto_data",
            Self::MetadataWithoutValue => "metadata_without_value",
            Self::MetadataConflict => "metadata_conflict",
            Self::TooManyValues => "too_many_values",
            Self::TotalBytesExceeded => "total_bytes_exceeded",
            Self::InvalidDefaultMetadata => "invalid_default_metadata",
            Self::InvalidMetadata => "invalid_metadata",
            Self::InvalidPlaceholder => "invalid_placeholder",
            Self::InvalidSha256 => "invalid_sha256",
            Self::InvalidContentType => "invalid_content_type",
            Self::InvalidCompression => "invalid_compression",
            Self::InvalidSourceUrl => "invalid_source_url",
            Self::InvalidDownloadUrl => "invalid_download_url",
            Self::InvalidDownloadScheme => "invalid_download_scheme",
            Self::UntrustedDownloadOrigin => "untrusted_download_origin",
            Self::DownloadPathMismatch => "download_path_mismatch",
            Self::ByteLengthMismatch => "byte_length_mismatch",
            Self::ResponseContentTypeMismatch => "response_content_type_mismatch",
            Self::ChecksumMismatch => "checksum_mismatch",
            Self::InvalidJson => "invalid_json",
            Self::InvalidProtoWireType => "invalid_proto_wire_type",
            Self::MissingHydratedValue => "missing_hydrated_value",
        }
    }
}

pub(super) fn hydration_error(reason: HydrationFailureReason, message: &str) -> StatsigErr {
    StatsigErr::CustomError(format!(
        "Dynamic config hydration failure: {}: {message}",
        reason.as_str()
    ))
}
