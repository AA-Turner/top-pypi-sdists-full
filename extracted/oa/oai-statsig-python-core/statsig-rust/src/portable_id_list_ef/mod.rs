//! The forward proxy can copy this directory and declare `mod portable_id_list_ef;`.
//! The codec depends only on the Rust standard library.
//!
//! Version 1 is a little-endian unique-member count followed by its packed EF
//! section. The number of low bits is floor(log2(2^48 / count)). Each group of
//! 32 high buckets begins at a u32 bit offset in the restart directory. The
//! low stream holds count packed values; the high stream has a one per member
//! and a zero per bucket. Both streams end in eight bytes of read padding.
use std::io;
#[doc(hidden)]
pub mod packed;
#[cfg(test)]
mod tests;

pub const MEDIA_TYPE: &str = "application/vnd.statsig.id-list-ef;version=1";
pub const MAX_IMAGE_BYTES: usize = 64 * 1024 * 1024;
pub const RECORD_BYTES: usize = 10;
pub const V1_COUNT_BYTES: usize = size_of::<u64>();
// At most 32 MiB of eight-byte ranks, including duplicates, before in-place sorting.
pub const MAX_PREFIX_RECORDS: usize = 1 << 22;

/// Encode the initial run of canonical, LF-terminated additions. The returned
/// cursor counts original bytes including duplicates, independently of EF size.
/// Callers pin the supplied bytes to one authorized, append-only generation.
pub fn encode_prefix_v1(raw: &[u8], min_raw_bytes: usize) -> io::Result<Option<(usize, Vec<u8>)>> {
    let mut ranks = Vec::new();
    for record in raw.chunks_exact(RECORD_BYTES).take(MAX_PREFIX_RECORDS) {
        let [b'+', key @ .., b'\n'] = record else {
            break;
        };
        let Some(rank) = packed::decode(key.try_into().unwrap()) else {
            break;
        };
        ranks.push(rank.to_ne_bytes());
    }
    let raw_end = ranks.len() * RECORD_BYTES;
    if raw_end == 0 || raw_end < min_raw_bytes {
        return Ok(None);
    }
    ranks.sort_unstable_by_key(|rank| u64::from_ne_bytes(*rank));
    ranks.dedup();
    let Some(ef) = packed::Ef::for_sorted_ranks(&ranks)? else {
        return Ok(None);
    };
    if ef.end > MAX_IMAGE_BYTES {
        return Ok(None);
    }
    let mut image = vec![0; ef.end];
    ef.pack(&ranks, &mut image);
    Ok(Some((raw_end, image)))
}

/// Validate length, directory, occupancy, strict order and final count in
/// place, without allocating a decoded membership table.
pub fn validate_v1(image: &[u8]) -> io::Result<packed::Ef> {
    let ef = v1_layout(image, image.len() as u64)?;
    ef.walk(image, |_| true)?;
    Ok(ef)
}

/// A complete v1 count must fit in its low four bytes and imply the given image size.
pub fn matches_v1_prefix(prefix: &[u8], total: u64) -> bool {
    prefix.get(4..V1_COUNT_BYTES) == Some(&[0; 4]) && v1_layout(prefix, total).is_ok()
}

/// For a split count, check whether its available bytes could describe an image
/// of this size. The v1 layout grows with the member count.
pub fn matches_partial_v1_count(prefix: &[u8], total: u64) -> bool {
    if prefix.is_empty() || prefix.len() >= V1_COUNT_BYTES || total > MAX_IMAGE_BYTES as u64 {
        return false;
    }
    let mut low = 1;
    let mut high = total as usize; // V1 needs at least one byte per member within this cap.
    while low <= high {
        let count = low + (high - low) / 2;
        let Ok(layout) = packed::Ef::layout(count, V1_COUNT_BYTES) else {
            return false;
        };
        match (layout.end as u64).cmp(&total) {
            std::cmp::Ordering::Less => low = count + 1,
            std::cmp::Ordering::Greater => high = count - 1,
            std::cmp::Ordering::Equal => return (count as u64).to_le_bytes().starts_with(prefix),
        }
    }
    false
}

fn v1_layout(prefix: &[u8], total: u64) -> io::Result<packed::Ef> {
    if prefix.len() < V1_COUNT_BYTES
        || !(V1_COUNT_BYTES as u64..=MAX_IMAGE_BYTES as u64).contains(&total)
    {
        return Err(invalid("invalid EF snapshot length"));
    }
    let count = usize::try_from(read_u64(prefix, 0)).map_err(|_| invalid("invalid EF count"))?;
    let ef = packed::Ef::layout(count, V1_COUNT_BYTES)?;
    if ef.end as u64 != total {
        return Err(invalid("EF snapshot length mismatch"));
    }
    Ok(ef)
}

fn invalid(message: &str) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, message)
}
fn read_u32(bytes: &[u8], offset: usize) -> u32 {
    u32::from_le_bytes(bytes[offset..offset + 4].try_into().unwrap())
}
fn read_u64(bytes: &[u8], offset: usize) -> u64 {
    u64::from_le_bytes(bytes[offset..offset + 8].try_into().unwrap())
}
fn checked_add(a: usize, b: usize) -> io::Result<usize> {
    a.checked_add(b)
        .ok_or_else(|| invalid("EF offset overflow"))
}
fn checked_mul(a: usize, b: usize) -> io::Result<usize> {
    a.checked_mul(b)
        .ok_or_else(|| invalid("EF offset overflow"))
}
