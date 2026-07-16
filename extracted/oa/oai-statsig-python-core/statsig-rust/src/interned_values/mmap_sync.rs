use serde::Deserialize;

use crate::{
    networking::ResponseData,
    observability::ops_stats::OpsStatsForInstance,
    specs_response::{proto_specs::deserialize_protobuf, spec_types::SpecsResponseFull},
    StatsigErr,
};

/// Identifies the config generation used to build an mmap artifact.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MmapSyncCursor {
    pub lcut: u64,
    pub checksum: Option<String>,
}

/// Reports whether a conditional mmap fetch published a new artifact.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum MmapWriteOutcome {
    Published(MmapSyncCursor),
    NoUpdate,
}

pub(super) struct MmapResolvedUpdate {
    pub(super) specs: SpecsResponseFull,
    pub(super) cursor: MmapSyncCursor,
}

pub(super) struct MmapConfigResponse<'a> {
    data: &'a mut ResponseData,
    headers: MmapResponseHeaders,
    format: MmapResponseFormat,
}

#[derive(Clone, Copy)]
enum MmapResponseFormat {
    Json,
    Protobuf,
}

#[derive(Deserialize)]
struct MmapResponseMetadata {
    has_updates: Option<bool>,
    time: Option<u64>,
    checksum: Option<String>,
}

struct MmapResponseHeaders {
    lcut: Option<u64>,
    checksum: ChecksumHeader,
    cache_hit: bool,
}

enum ChecksumHeader {
    Missing,
    // An explicitly empty header is authoritative `None`; a missing header
    // has no identity information and must not bypass body parsing.
    Present(Option<String>),
}

#[derive(Clone, Copy)]
struct ChecksumIdentity<'a> {
    value: Option<&'a str>,
    is_known: bool,
}

enum MetadataResolution {
    NoUpdate,
    ParseFull(MmapSyncCursor),
}

impl<'a> MmapConfigResponse<'a> {
    pub(super) fn new(data: &'a mut ResponseData) -> Result<Self, StatsigErr> {
        let headers = MmapResponseHeaders::from_response(data)?;
        let format = MmapResponseFormat::from_response(data);

        Ok(Self {
            data,
            headers,
            format,
        })
    }

    pub(super) fn resolve(
        mut self,
        previous: Option<&MmapSyncCursor>,
    ) -> Result<Option<MmapResolvedUpdate>, StatsigErr> {
        if self.headers.cache_hit {
            let previous = previous.ok_or_else(|| {
                invalid_mmap_response("Received a cache-hit response before any mmap was published")
            })?;
            validate_no_update_identity(
                previous,
                self.headers.lcut,
                self.headers.checksum.identity(),
            )?;
            return Ok(None);
        }

        if previous.is_some_and(|previous| self.headers.is_no_update_without_body(previous)) {
            return Ok(None);
        }

        let metadata_cursor = match self.format {
            MmapResponseFormat::Protobuf => {
                if previous.is_some() && self.headers.lcut.is_none() {
                    return Err(invalid_mmap_response(
                        "A conditional protobuf response did not include x-since-time",
                    ));
                }
                None
            }
            MmapResponseFormat::Json => match self.resolve_json_metadata(previous)? {
                MetadataResolution::NoUpdate => return Ok(None),
                MetadataResolution::ParseFull(cursor) => Some(cursor),
            },
        };

        let specs = parse_specs_response_data(&mut *self.data, self.format)?;
        self.resolve_parsed(specs, metadata_cursor, previous)
    }

    fn resolve_json_metadata(
        &mut self,
        previous: Option<&MmapSyncCursor>,
    ) -> Result<MetadataResolution, StatsigErr> {
        let metadata = self.data.deserialize_into::<MmapResponseMetadata>()?;
        if metadata.has_updates == Some(false) {
            let previous = previous.ok_or_else(|| {
                invalid_mmap_response("Received a no-update response before any mmap was published")
            })?;
            validate_json_no_update(&metadata, &self.headers, previous)?;
            return Ok(MetadataResolution::NoUpdate);
        }
        if metadata.has_updates != Some(true) {
            return Err(invalid_mmap_response(
                "A config response did not include a valid has_updates value",
            ));
        }

        let cursor = cursor_from_metadata(&metadata)?;
        self.headers.validate_cursor(&cursor)?;
        if previous.is_some_and(|previous| cursor_is_stale_or_exact(&cursor, previous)) {
            return Ok(MetadataResolution::NoUpdate);
        }

        Ok(MetadataResolution::ParseFull(cursor))
    }

    fn resolve_parsed(
        &self,
        specs: SpecsResponseFull,
        metadata_cursor: Option<MmapSyncCursor>,
        previous: Option<&MmapSyncCursor>,
    ) -> Result<Option<MmapResolvedUpdate>, StatsigErr> {
        let cursor = cursor_from_specs_response(&specs)?;
        self.headers.validate_cursor(&cursor)?;
        if metadata_cursor
            .as_ref()
            .is_some_and(|metadata_cursor| metadata_cursor != &cursor)
        {
            return Err(invalid_mmap_response(
                "The parsed config identity did not match its JSON metadata",
            ));
        }
        if !specs.has_updates {
            let previous = previous.ok_or_else(|| {
                invalid_mmap_response("Received a no-update response before any mmap was published")
            })?;
            validate_no_update_identity(
                previous,
                Some(cursor.lcut),
                ChecksumIdentity::known(cursor.checksum.as_deref()),
            )?;
            return Ok(None);
        }
        if previous.is_some_and(|previous| cursor_is_stale_or_exact(&cursor, previous)) {
            return Ok(None);
        }

        Ok(Some(MmapResolvedUpdate { specs, cursor }))
    }
}

impl MmapResponseFormat {
    fn from_response(response_data: &ResponseData) -> Self {
        let is_protobuf = response_data
            .get_header_ref("content-type")
            .is_some_and(|value| value.contains("application/octet-stream"))
            && response_data
                .get_header_ref("content-encoding")
                .is_some_and(|value| value.contains("statsig-br"));

        if is_protobuf {
            Self::Protobuf
        } else {
            Self::Json
        }
    }
}

impl MmapResponseHeaders {
    fn from_response(response_data: &ResponseData) -> Result<Self, StatsigErr> {
        let lcut = response_data
            .get_header_ref("x-since-time")
            .map(|value| {
                value.parse::<u64>().map_err(|_| {
                    invalid_mmap_response("The x-since-time response header was not a valid u64")
                })
            })
            .transpose()?;
        let checksum = match response_data.get_header_ref("x-checksum") {
            Some(value) => ChecksumHeader::Present(normalize_checksum(Some(value.clone()))),
            None => ChecksumHeader::Missing,
        };

        if checksum.identity().value.is_some() && lcut.is_none() {
            return Err(invalid_mmap_response(
                "The response included x-checksum without x-since-time",
            ));
        }

        Ok(Self {
            lcut,
            checksum,
            cache_hit: response_data
                .get_header_ref("x-cache-hit")
                .is_some_and(|value| value.eq_ignore_ascii_case("true")),
        })
    }

    fn is_no_update_without_body(&self, previous: &MmapSyncCursor) -> bool {
        let Some(lcut) = self.lcut else {
            return false;
        };

        lcut < previous.lcut || (lcut == previous.lcut && self.checksum.matches(&previous.checksum))
    }

    fn validate_cursor(&self, cursor: &MmapSyncCursor) -> Result<(), StatsigErr> {
        if self.lcut.is_some_and(|lcut| lcut != cursor.lcut) {
            return Err(invalid_mmap_response(
                "The x-since-time response header did not match the config response time",
            ));
        }
        if self
            .checksum
            .identity()
            .conflicts_with(ChecksumIdentity::known(cursor.checksum.as_deref()))
        {
            return Err(invalid_mmap_response(
                "The x-checksum response header did not match the config response checksum",
            ));
        }

        Ok(())
    }
}

impl ChecksumHeader {
    fn identity(&self) -> ChecksumIdentity<'_> {
        match self {
            Self::Missing => ChecksumIdentity::unknown(),
            Self::Present(checksum) => ChecksumIdentity::known(checksum.as_deref()),
        }
    }

    fn matches(&self, expected: &Option<String>) -> bool {
        let identity = self.identity();
        identity.is_known && identity.value == expected.as_deref()
    }
}

impl<'a> ChecksumIdentity<'a> {
    fn unknown() -> Self {
        Self {
            value: None,
            is_known: false,
        }
    }

    fn known(value: Option<&'a str>) -> Self {
        Self {
            value,
            is_known: true,
        }
    }

    fn prefer(self, fallback: Self) -> Self {
        if self.is_known {
            self
        } else {
            fallback
        }
    }

    fn conflicts_with(self, other: Self) -> bool {
        self.is_known && other.is_known && self.value != other.value
    }
}

fn cursor_from_metadata(metadata: &MmapResponseMetadata) -> Result<MmapSyncCursor, StatsigErr> {
    let lcut = metadata
        .time
        .filter(|lcut| *lcut > 0)
        .ok_or_else(|| invalid_mmap_response("A config response did not include a valid time"))?;

    Ok(MmapSyncCursor {
        lcut,
        checksum: normalize_checksum(metadata.checksum.clone()),
    })
}

fn cursor_from_specs_response(
    specs_response: &SpecsResponseFull,
) -> Result<MmapSyncCursor, StatsigErr> {
    if specs_response.time == 0 {
        return Err(invalid_mmap_response(
            "A config response did not include a valid time",
        ));
    }

    Ok(MmapSyncCursor {
        lcut: specs_response.time,
        checksum: normalize_checksum(specs_response.checksum.clone()),
    })
}

fn normalize_checksum(checksum: Option<String>) -> Option<String> {
    checksum.filter(|checksum| !checksum.is_empty())
}

fn cursor_is_stale_or_exact(cursor: &MmapSyncCursor, previous: &MmapSyncCursor) -> bool {
    cursor.lcut < previous.lcut
        || (cursor.lcut == previous.lcut && cursor.checksum == previous.checksum)
}

fn validate_json_no_update(
    metadata: &MmapResponseMetadata,
    headers: &MmapResponseHeaders,
    previous: &MmapSyncCursor,
) -> Result<(), StatsigErr> {
    let body_checksum = match metadata.checksum.as_deref() {
        Some(checksum) => ChecksumIdentity::known((!checksum.is_empty()).then_some(checksum)),
        None => ChecksumIdentity::unknown(),
    };
    if body_checksum.is_known && metadata.time.is_none() {
        return Err(invalid_mmap_response(
            "A no-update response included checksum without time",
        ));
    }
    if let (Some(header_lcut), Some(body_lcut)) = (headers.lcut, metadata.time) {
        if header_lcut != body_lcut {
            return Err(invalid_mmap_response(
                "The x-since-time response header did not match the JSON response time",
            ));
        }
    }

    let header_checksum = headers.checksum.identity();
    if header_checksum.conflicts_with(body_checksum) {
        return Err(invalid_mmap_response(
            "The x-checksum response header did not match the JSON response checksum",
        ));
    }

    let lcut = metadata.time.or(headers.lcut);
    validate_no_update_identity(previous, lcut, body_checksum.prefer(header_checksum))
}

fn validate_no_update_identity(
    previous: &MmapSyncCursor,
    lcut: Option<u64>,
    checksum: ChecksumIdentity<'_>,
) -> Result<(), StatsigErr> {
    let Some(lcut) = lcut else {
        return Ok(());
    };

    if lcut > previous.lcut
        || (lcut == previous.lcut
            && checksum.is_known
            && previous.checksum.as_deref() != checksum.value)
    {
        return Err(invalid_mmap_response(
            "A no-update response advertised a changed config identity",
        ));
    }

    Ok(())
}

fn parse_specs_response_data(
    response_data: &mut ResponseData,
    format: MmapResponseFormat,
) -> Result<SpecsResponseFull, StatsigErr> {
    if matches!(format, MmapResponseFormat::Protobuf) {
        let current = SpecsResponseFull::default();
        let mut next = SpecsResponseFull::default();
        deserialize_protobuf(
            &OpsStatsForInstance::new(),
            &current,
            &mut next,
            response_data,
        )?;
        return Ok(next);
    }

    response_data.deserialize_into::<SpecsResponseFull>()
}

fn invalid_mmap_response(message: &str) -> StatsigErr {
    StatsigErr::InvalidOperation(format!("Invalid mmap config response: {message}"))
}
