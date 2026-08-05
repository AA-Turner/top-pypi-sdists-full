use std::fs::File;

use memmap2::Mmap;

use crate::StatsigErr;

/// Process-local memory accounting for the currently loaded interned mmap
/// reader generation.
///
/// The snapshot contains no SDK key, filesystem path, inode, device, or virtual
/// address. Linux residency fields are derived from the exact address range of
/// the retained mapping. Platforms without an equivalent implementation leave
/// optional residency fields unset while still reporting format and mapped
/// bytes. A failed Linux probe likewise leaves only its optional fields unset.
#[non_exhaustive]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct MmapReaderMemorySnapshot {
    pub format_version: u32,
    pub mapped_bytes: u64,
    pub resident_bytes: Option<u64>,
    pub proportional_set_bytes: Option<u64>,
    pub private_dirty_bytes: Option<u64>,
    pub deleted_mapped_bytes: Option<u64>,
    /// Number of reader artifact mappings retained by this process.
    pub loaded_generation_count: u64,
    pub vma_segment_count: Option<u64>,
}

pub(super) fn snapshot(
    file: &File,
    mmap: &Mmap,
    format_version: u32,
) -> Result<MmapReaderMemorySnapshot, StatsigErr> {
    let mapped_bytes = u64::try_from(mmap.len()).map_err(|_| {
        StatsigErr::InvalidOperation("Loaded mmap length does not fit in u64".to_string())
    })?;

    #[cfg(target_os = "linux")]
    {
        use std::os::unix::fs::MetadataExt;

        let residency = linux_residency(mmap.as_ptr() as usize, mmap.len()).ok();
        let link_count = file.metadata().ok().map(|metadata| metadata.nlink());

        Ok(linux_snapshot(
            format_version,
            mapped_bytes,
            residency,
            link_count,
        ))
    }

    #[cfg(not(target_os = "linux"))]
    {
        let _ = file;
        Ok(MmapReaderMemorySnapshot {
            format_version,
            mapped_bytes,
            resident_bytes: None,
            proportional_set_bytes: None,
            private_dirty_bytes: None,
            deleted_mapped_bytes: None,
            loaded_generation_count: 1,
            vma_segment_count: None,
        })
    }
}

pub(super) fn aggregate<'a>(
    mappings: impl IntoIterator<Item = (&'a File, &'a Mmap)>,
    format_version: u32,
) -> Result<Option<MmapReaderMemorySnapshot>, StatsigErr> {
    let mut mappings = mappings.into_iter();
    let Some((file, mmap)) = mappings.next() else {
        return Ok(None);
    };
    let mut total = snapshot(file, mmap, format_version)?;

    for (file, mmap) in mappings {
        let next = snapshot(file, mmap, format_version)?;
        total.mapped_bytes = add_snapshot_value(total.mapped_bytes, next.mapped_bytes)?;
        total.resident_bytes =
            add_optional_snapshot_value(total.resident_bytes, next.resident_bytes)?;
        total.proportional_set_bytes =
            add_optional_snapshot_value(total.proportional_set_bytes, next.proportional_set_bytes)?;
        total.private_dirty_bytes =
            add_optional_snapshot_value(total.private_dirty_bytes, next.private_dirty_bytes)?;
        total.deleted_mapped_bytes =
            add_optional_snapshot_value(total.deleted_mapped_bytes, next.deleted_mapped_bytes)?;
        total.loaded_generation_count =
            add_snapshot_value(total.loaded_generation_count, next.loaded_generation_count)?;
        total.vma_segment_count =
            add_optional_snapshot_value(total.vma_segment_count, next.vma_segment_count)?;
    }

    Ok(Some(total))
}

fn add_snapshot_value(left: u64, right: u64) -> Result<u64, StatsigErr> {
    left.checked_add(right).ok_or_else(|| {
        StatsigErr::InvalidOperation("Loaded mmap memory snapshot overflowed".to_string())
    })
}

fn add_optional_snapshot_value(
    left: Option<u64>,
    right: Option<u64>,
) -> Result<Option<u64>, StatsigErr> {
    match (left, right) {
        (Some(left), Some(right)) => add_snapshot_value(left, right).map(Some),
        _ => Ok(None),
    }
}

#[cfg(target_os = "linux")]
fn linux_snapshot(
    format_version: u32,
    mapped_bytes: u64,
    residency: Option<LinuxMmapResidency>,
    link_count: Option<u64>,
) -> MmapReaderMemorySnapshot {
    let (resident_bytes, proportional_set_bytes, private_dirty_bytes, vma_segment_count) =
        match residency {
            Some(residency) => (
                Some(residency.resident_bytes),
                Some(residency.proportional_set_bytes),
                Some(residency.private_dirty_bytes),
                Some(residency.vma_segment_count),
            ),
            None => (None, None, None, None),
        };

    MmapReaderMemorySnapshot {
        format_version,
        mapped_bytes,
        resident_bytes,
        proportional_set_bytes,
        private_dirty_bytes,
        deleted_mapped_bytes: link_count.map(|count| if count == 0 { mapped_bytes } else { 0 }),
        loaded_generation_count: 1,
        vma_segment_count,
    }
}

#[cfg(target_os = "linux")]
#[derive(Debug, Default, Eq, PartialEq)]
struct LinuxMmapResidency {
    resident_bytes: u64,
    proportional_set_bytes: u64,
    private_dirty_bytes: u64,
    vma_segment_count: u64,
}

#[cfg(target_os = "linux")]
fn linux_residency(
    mapping_start: usize,
    mapping_len: usize,
) -> Result<LinuxMmapResidency, StatsigErr> {
    use std::io::BufReader;

    let smaps =
        File::open("/proc/self/smaps").map_err(|error| StatsigErr::FileError(error.to_string()))?;
    parse_smaps(BufReader::new(smaps), mapping_start, mapping_len)
}

#[cfg(target_os = "linux")]
fn parse_smaps(
    mut reader: impl std::io::BufRead,
    mapping_start: usize,
    mapping_len: usize,
) -> Result<LinuxMmapResidency, StatsigErr> {
    let mapping_end = mapping_start.checked_add(mapping_len).ok_or_else(|| {
        StatsigErr::InvalidOperation("Loaded mmap address range overflowed".to_string())
    })?;
    if mapping_start == mapping_end {
        return Err(StatsigErr::InvalidOperation(
            "Loaded mmap address range is empty".to_string(),
        ));
    }

    let mut totals = LinuxMmapResidency::default();
    let mut overlaps_mapping = false;
    let mut line = String::new();
    loop {
        line.clear();
        let bytes_read = reader
            .read_line(&mut line)
            .map_err(|error| StatsigErr::FileError(error.to_string()))?;
        if bytes_read == 0 {
            break;
        }

        if let Some((vma_start, vma_end)) = parse_vma_header(&line)? {
            if vma_start >= mapping_end {
                break;
            }
            overlaps_mapping = vma_start < mapping_end && mapping_start < vma_end;
            if overlaps_mapping {
                totals.vma_segment_count =
                    checked_add(totals.vma_segment_count, 1, "VMA segment count overflowed")?;
            }
            continue;
        }
        if !overlaps_mapping {
            continue;
        }

        for (field, destination) in [
            ("Rss:", &mut totals.resident_bytes),
            ("Pss:", &mut totals.proportional_set_bytes),
            ("Private_Dirty:", &mut totals.private_dirty_bytes),
        ] {
            if let Some(value) = parse_kibibyte_field(&line, field)? {
                *destination = checked_add(*destination, value, "smaps byte count overflowed")?;
                break;
            }
        }
    }

    if totals.vma_segment_count == 0 {
        return Err(StatsigErr::FileError(
            "Loaded mmap range was not present in process smaps".to_string(),
        ));
    }
    Ok(totals)
}

#[cfg(target_os = "linux")]
fn parse_vma_header(line: &str) -> Result<Option<(usize, usize)>, StatsigErr> {
    let mut fields = line.split_ascii_whitespace();
    let Some(range) = fields.next() else {
        return Ok(None);
    };
    let Some(permissions) = fields.next() else {
        return Ok(None);
    };
    let permissions = permissions.as_bytes();
    if permissions.len() != 4
        || !matches!(permissions[0], b'r' | b'-')
        || !matches!(permissions[1], b'w' | b'-')
        || !matches!(permissions[2], b'x' | b'-')
        || !matches!(permissions[3], b'p' | b's')
    {
        return Ok(None);
    }
    let Some((start, end)) = range.split_once('-') else {
        return Err(StatsigErr::FileError(
            "Invalid VMA range in process smaps".to_string(),
        ));
    };
    let parse_address = |value: &str| {
        usize::from_str_radix(value, 16)
            .map_err(|_| StatsigErr::FileError("Invalid VMA range in process smaps".to_string()))
    };
    let start = parse_address(start)?;
    let end = parse_address(end)?;
    if start >= end {
        return Err(StatsigErr::FileError(
            "Invalid VMA range in process smaps".to_string(),
        ));
    }
    Ok(Some((start, end)))
}

#[cfg(target_os = "linux")]
fn parse_kibibyte_field(line: &str, expected_field: &str) -> Result<Option<u64>, StatsigErr> {
    const KIBIBYTE: u64 = 1024;

    let mut fields = line.split_ascii_whitespace();
    if fields.next() != Some(expected_field) {
        return Ok(None);
    }
    let value = fields
        .next()
        .ok_or_else(|| invalid_smaps_field(expected_field))?
        .parse::<u64>()
        .map_err(|_| invalid_smaps_field(expected_field))?;
    if fields.next() != Some("kB") {
        return Err(invalid_smaps_field(expected_field));
    }
    value
        .checked_mul(KIBIBYTE)
        .map(Some)
        .ok_or_else(|| invalid_smaps_field(expected_field))
}

#[cfg(target_os = "linux")]
fn checked_add(left: u64, right: u64, message: &str) -> Result<u64, StatsigErr> {
    left.checked_add(right)
        .ok_or_else(|| StatsigErr::FileError(message.to_string()))
}

#[cfg(target_os = "linux")]
fn invalid_smaps_field(field: &str) -> StatsigErr {
    StatsigErr::FileError(format!("Invalid {field} field in process smaps"))
}

#[cfg(all(test, target_os = "linux"))]
mod tests {
    use std::io::Cursor;

    use super::*;

    const SMAPS: &str = "\
00000000-00001000 r--p 00000000 00:00 0\n\
Rss:                 100 kB\n\
Pss:                  90 kB\n\
Private_Dirty:        80 kB\n\
00001000-00002000 r--s 00000000 00:00 0\n\
Rss:                   4 kB\n\
Pss:                   2 kB\n\
Private_Dirty:         1 kB\n\
00002000-00003000 r--s 00001000 00:00 0\n\
Rss:                   8 kB\n\
Pss:                   5 kB\n\
Private_Dirty:         3 kB\n\
00003000-00004000 r--p 00000000 00:00 0\n\
Rss:                 200 kB\n\
Pss:                 190 kB\n\
Private_Dirty:       180 kB\n";

    #[test]
    fn smaps_parser_sums_only_overlapping_vmas() {
        let result = parse_smaps(Cursor::new(SMAPS), 0x1800, 0x1000).unwrap();
        assert_eq!(
            result,
            LinuxMmapResidency {
                resident_bytes: 12 * 1024,
                proportional_set_bytes: 7 * 1024,
                private_dirty_bytes: 4 * 1024,
                vma_segment_count: 2,
            }
        );
    }

    #[test]
    fn smaps_parser_treats_vma_boundaries_as_non_overlapping() {
        let result = parse_smaps(Cursor::new(SMAPS), 0x2000, 0x1000).unwrap();
        assert_eq!(result.resident_bytes, 8 * 1024);
        assert_eq!(result.vma_segment_count, 1);
    }

    #[test]
    fn smaps_parser_stops_after_the_target_range() {
        let smaps = "\
00001000-00002000 r--p 00000000 00:00 0\n\
Rss:                   4 kB\n\
00002000-00003000 r--p 00000000 00:00 0\n\
not-a-range r--p 00000000 00:00 0\n";
        let result = parse_smaps(Cursor::new(smaps), 0x1000, 0x1000).unwrap();
        assert_eq!(result.resident_bytes, 4 * 1024);
        assert_eq!(result.vma_segment_count, 1);
    }

    #[test]
    fn smaps_parser_rejects_malformed_metrics_and_missing_mapping() {
        let malformed = "1000-2000 r--s 00000000 00:00 0\nRss: nope kB\n";
        assert!(matches!(
            parse_smaps(Cursor::new(malformed), 0x1000, 0x1000),
            Err(StatsigErr::FileError(message)) if message.contains("Rss:")
        ));
        assert!(matches!(
            parse_smaps(Cursor::new(SMAPS), 0x5000, 0x1000),
            Err(StatsigErr::FileError(message))
                if message == "Loaded mmap range was not present in process smaps"
        ));
    }

    #[test]
    fn snapshot_retains_baseline_when_smaps_probe_fails() {
        let snapshot = linux_snapshot(2, 4096, None, Some(0));

        assert_eq!(snapshot.format_version, 2);
        assert_eq!(snapshot.mapped_bytes, 4096);
        assert_eq!(snapshot.loaded_generation_count, 1);
        assert_eq!(snapshot.resident_bytes, None);
        assert_eq!(snapshot.proportional_set_bytes, None);
        assert_eq!(snapshot.private_dirty_bytes, None);
        assert_eq!(snapshot.vma_segment_count, None);
        assert_eq!(snapshot.deleted_mapped_bytes, Some(4096));
    }

    #[test]
    fn snapshot_retains_residency_when_fstat_probe_fails() {
        let snapshot = linux_snapshot(
            2,
            4096,
            Some(LinuxMmapResidency {
                resident_bytes: 2048,
                proportional_set_bytes: 1024,
                private_dirty_bytes: 512,
                vma_segment_count: 1,
            }),
            None,
        );

        assert_eq!(snapshot.format_version, 2);
        assert_eq!(snapshot.mapped_bytes, 4096);
        assert_eq!(snapshot.loaded_generation_count, 1);
        assert_eq!(snapshot.resident_bytes, Some(2048));
        assert_eq!(snapshot.proportional_set_bytes, Some(1024));
        assert_eq!(snapshot.private_dirty_bytes, Some(512));
        assert_eq!(snapshot.vma_segment_count, Some(1));
        assert_eq!(snapshot.deleted_mapped_bytes, None);
    }
}
