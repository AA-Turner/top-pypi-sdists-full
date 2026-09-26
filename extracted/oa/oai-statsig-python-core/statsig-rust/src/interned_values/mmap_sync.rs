use serde::Deserialize;

use crate::{StatsigErr, networking::ResponseData, specs_response::spec_types::SpecsResponseFull};

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

#[derive(Deserialize)]
struct MmapResponseMetadata {
    has_updates: Option<bool>,
    time: Option<u64>,
    checksum: Option<String>,
}

pub(super) fn resolve_json_response(
    data: &mut ResponseData,
    previous: Option<&MmapSyncCursor>,
) -> Result<Option<MmapResolvedUpdate>, StatsigErr> {
    // The body is published before its metadata, so response headers can
    // describe an older generation. Read identity only from the body.
    let metadata = data.deserialize_into::<MmapResponseMetadata>()?;
    match metadata.has_updates {
        Some(false) => {
            validate_no_update(previous, metadata.time, metadata.checksum.as_deref())?;
            return Ok(None);
        }
        Some(true) => {}
        None => {
            return Err(invalid_mmap_response(
                "A config response did not include a valid has_updates value",
            ));
        }
    }
    let cursor = full_body_cursor(metadata.time.unwrap_or_default(), metadata.checksum)?;
    if previous.is_some_and(|previous| cursor_is_stale_or_exact(&cursor, previous)) {
        return Ok(None);
    }
    let specs = data.deserialize_into::<SpecsResponseFull>()?;
    resolve_parsed_response(specs, previous)
}

pub(super) fn resolve_parsed_response(
    specs: SpecsResponseFull,
    previous: Option<&MmapSyncCursor>,
) -> Result<Option<MmapResolvedUpdate>, StatsigErr> {
    if !specs.has_updates {
        validate_no_update(previous, Some(specs.time), specs.checksum.as_deref())?;
        return Ok(None);
    }
    let cursor = full_body_cursor(specs.time, specs.checksum.clone())?;
    if previous.is_some_and(|previous| cursor_is_stale_or_exact(&cursor, previous)) {
        return Ok(None);
    }
    Ok(Some(MmapResolvedUpdate { specs, cursor }))
}

fn full_body_cursor(lcut: u64, checksum: Option<String>) -> Result<MmapSyncCursor, StatsigErr> {
    if lcut == 0 {
        return Err(invalid_mmap_response(
            "A config response did not include a valid time",
        ));
    }
    Ok(MmapSyncCursor {
        lcut,
        checksum: checksum.filter(|checksum| !checksum.is_empty()),
    })
}

fn cursor_is_stale_or_exact(cursor: &MmapSyncCursor, previous: &MmapSyncCursor) -> bool {
    cursor.lcut < previous.lcut
        || (cursor.lcut == previous.lcut && cursor.checksum == previous.checksum)
}

fn validate_no_update(
    previous: Option<&MmapSyncCursor>,
    lcut: Option<u64>,
    checksum: Option<&str>,
) -> Result<(), StatsigErr> {
    let previous = previous.ok_or_else(|| {
        invalid_mmap_response("Received a no-update response before any mmap was published")
    })?;
    let Some(lcut) = lcut else {
        if checksum.is_some() {
            return Err(invalid_mmap_response(
                "A no-update response included checksum without time",
            ));
        }
        return Ok(());
    };
    if lcut > previous.lcut
        || (lcut == previous.lcut
            && checksum.is_some_and(|checksum| {
                Some(checksum).filter(|checksum| !checksum.is_empty())
                    != previous.checksum.as_deref()
            }))
    {
        return Err(invalid_mmap_response(
            "A no-update response advertised a changed config identity",
        ));
    }
    Ok(())
}

fn invalid_mmap_response(message: &str) -> StatsigErr {
    StatsigErr::InvalidOperation(format!("Invalid mmap config response: {message}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn initial_no_update_requires_a_published_artifact() {
        let mut data =
            ResponseData::from_bytes_with_headers(br#"{"has_updates":false}"#.to_vec(), None);
        assert!(matches!(
            resolve_json_response(&mut data, None),
            Err(StatsigErr::InvalidOperation(_))
        ));
    }
}
