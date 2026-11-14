use std::borrow::Cow;
use std::fs::File;
use std::io::{self, BufWriter, Write};
use std::ops::{Deref, Range};
use std::path::Path;
use std::sync::{Arc, OnceLock};

use memmap2::Mmap;
use sha2::{Digest, Sha256};

use super::IdListIds;
use crate::portable_id_list_ef::packed as elias_fano;

const MAGIC: &[u8; 8] = b"STGIDLS\0";
const VERSION: u32 = 2;
const COMPACT_VERSION: u32 = 3;
const HASH_ALGORITHM: u32 = 2;
const EMPTY: u8 = 0x80;
const GROUP: usize = 16;
pub(super) const HEADER_LEN: usize = 128;

/// Capacity is derived from unique members, separately for each key partition.
/// This is a file-build policy, not a public SDK option. The reader uses the
/// capacities in the image and accepts either rounding policy.
#[derive(Clone, Copy)]
pub(super) struct HashTableSizing {
    pub numerator: usize,
    pub denominator: usize,
    pub power_of_two: bool,
}

// Fine rounding avoids power-of-two capacity jumps. At 75% occupancy the
// mapped lookup sweep kept miss probes short while retaining most of the
// shared-memory saving; higher occupancy caused long linear-probe clusters.
const INLINE_SIZING: HashTableSizing = HashTableSizing {
    numerator: 3,
    denominator: 4,
    power_of_two: false,
};
// Fallback strings use multiply-high range reduction. The measured 5/8 load
// balances probe lengths and mapped bytes while retaining fine capacity steps.
const FALLBACK_SIZING: HashTableSizing = HashTableSizing {
    numerator: 5,
    denominator: 8,
    power_of_two: false,
};

impl HashTableSizing {
    pub(super) fn capacity(self, count: usize) -> io::Result<usize> {
        if self.numerator == 0 || self.numerator >= self.denominator {
            return Err(invalid("invalid ID-list table load fraction"));
        }
        if count == 0 {
            return Ok(0);
        }
        let target = checked_add(checked_mul(count, self.denominator)?, self.numerator - 1)?
            / self.numerator;
        if self.power_of_two {
            target
                .max(GROUP)
                .checked_next_power_of_two()
                .ok_or_else(|| invalid("ID-list table capacity overflow"))
        } else {
            checked_mul(checked_add(target, GROUP - 1)? / GROUP, GROUP)
        }
    }
}

#[derive(Clone, Copy)]
struct Table {
    controls: usize,
    slots: usize,
    capacity: usize,
    count: usize,
}

impl Table {
    fn new(
        start: usize,
        count: usize,
        capacity: usize,
        stride: usize,
    ) -> io::Result<(Self, usize)> {
        if (count == 0) != (capacity == 0)
            || (capacity != 0 && (!capacity.is_multiple_of(GROUP) || count >= capacity))
        {
            return Err(invalid("invalid ID-list hash table capacity"));
        }
        let controls_len = if capacity == 0 {
            0
        } else {
            checked_add(capacity, GROUP)?
        };
        let slots = checked_add(start, controls_len)?;
        let end = checked_add(slots, checked_mul(capacity, stride)?)?;
        Ok((
            Self {
                controls: start,
                slots,
                capacity,
                count,
            },
            end,
        ))
    }

    fn home(self, hash: u64, inline: bool) -> usize {
        if !inline {
            // High-half multiplication selects a bucket without division. Its
            // tag uses low bits, avoiding correlation with this range reduction.
            ((hash as u128 * self.capacity as u128) >> 64) as usize
        } else if self.capacity.is_power_of_two() {
            (hash as usize) & (self.capacity - 1)
        } else {
            (hash % self.capacity as u64) as usize
        }
    }

    fn advance(self, slot: usize, distance: usize) -> usize {
        let next = slot + distance;
        if next >= self.capacity {
            next - self.capacity
        } else {
            next
        }
    }
}

/// Both owners expose the same encoded image. A delta borrows its nested
/// hash table from a subregion of the mapping containing the operation bits.
enum ImageBytes {
    Heap(Box<[u8]>),
    Mapped {
        owner: Arc<Mmap>,
        range: Range<usize>,
    },
}

impl Deref for ImageBytes {
    type Target = [u8];
    fn deref(&self) -> &[u8] {
        match self {
            Self::Heap(bytes) => bytes,
            Self::Mapped { owner, range } => &owner[range.clone()],
        }
    }
}

pub(crate) struct IdListImage {
    map: ImageBytes,
    ef: Option<elias_fano::Ef>,
    iter_keys: OnceLock<Box<[[u8; 8]]>>,
    content_digest: OnceLock<String>,
    inline: Table,
    other: Table,
    blob_start: usize,
}

impl IdListImage {
    /// Adopt a fully validated portable EF section. It contains only canonical
    /// keys, so the local hash partitions are empty and no replay is needed.
    pub(super) fn from_ef_v1_snapshot(bytes: Vec<u8>, raw_end: u64) -> io::Result<Self> {
        let ef = crate::portable_id_list_ef::validate_v1(&bytes)?;
        if ef.count as u64 > raw_end / crate::portable_id_list_ef::RECORD_BYTES as u64 {
            return Err(invalid("ID-list snapshot count exceeds its raw prefix"));
        }
        let (empty, end) = Table::new(bytes.len(), 0, 0, 8)?;
        Ok(Self {
            map: ImageBytes::Heap(bytes.into_boxed_slice()),
            ef: Some(ef),
            iter_keys: OnceLock::new(),
            content_digest: OnceLock::new(),
            inline: empty,
            other: empty,
            blob_start: end,
        })
    }

    pub(super) fn packed_ef_section(&self) -> Option<&[u8]> {
        if self.inline.count != 0 || self.other.count != 0 {
            return None;
        }
        self.ef?.encoded_section(&self.map)
    }

    pub(super) fn open(path: &Path, namespace: &[u8; 32], name: &str) -> io::Result<Self> {
        let file = File::open(path)?;
        if file.metadata()?.len() < HEADER_LEN as u64 {
            return Err(invalid("truncated ID-list header"));
        }
        // Published inodes are immutable. Unlinking an old file keeps live maps valid.
        let map = Arc::new(unsafe { Mmap::map(&file)? });
        let range = 0..map.len();
        Self::from_region(map, range, namespace, name)
    }

    // A delta's operation bit refers to a physical hash slot. EF ordinals
    // have no such slot, so a delta must contain exactly the v2 hash format.
    pub(super) fn from_delta_region(
        owner: Arc<Mmap>,
        range: Range<usize>,
        namespace: &[u8; 32],
        name: &str,
    ) -> io::Result<Self> {
        let bytes = owner
            .get(range.clone())
            .ok_or_else(|| invalid("invalid delta table region"))?;
        if bytes.len() < HEADER_LEN || read_u32(bytes, 8) != VERSION {
            return Err(invalid("delta requires a version-2 hash table"));
        }
        Self::from_region(owner, range, namespace, name)
    }

    fn from_region(
        owner: Arc<Mmap>,
        range: Range<usize>,
        namespace: &[u8; 32],
        name: &str,
    ) -> io::Result<Self> {
        let view = Self::parse(ImageBytes::Mapped { owner, range }, namespace, name)?;
        if let Some(ef) = view.ef {
            ef.walk(&view.map, |_| true)?;
        }
        let blob_len = view.map.len() - view.blob_start;
        view.validate_table(view.inline, true, blob_len)?;
        view.validate_table(view.other, false, blob_len)?;
        Ok(view)
    }

    pub(super) fn build_heap(
        namespace: &[u8; 32],
        name: &str,
        ids: &IdListIds,
    ) -> io::Result<Self> {
        let mut bytes = Vec::new();
        encode_image(
            &mut bytes,
            namespace,
            name,
            ids.collect_image_keys(),
            INLINE_SIZING,
            FALLBACK_SIZING,
            true,
        )?;
        // The encoder just constructed these tables. Only external mappings
        // need the full walk and content digest before use.
        Self::parse(ImageBytes::Heap(bytes.into_boxed_slice()), namespace, name)
    }

    /// The caller has an empty base. A rejected changeset goes through the ordinary parser.
    pub(super) fn try_heap_from_adds<'a>(
        namespace: &[u8; 32],
        name: &str,
        body: Cow<'a, str>,
    ) -> Result<Self, Cow<'a, str>> {
        const RECORD_BYTES: usize = 10; // '+' + eight Base64 bytes + LF
        const MIN_DIRECT_ADDS: usize = 1_000;
        let (records, tail) = body.as_bytes().as_chunks::<RECORD_BYTES>();
        let count = records.len();
        // Check the whole stream before reordering anything: a later deletion must
        // still see all earlier edits in their original order.
        if count < MIN_DIRECT_ADDS || !tail.is_empty() || !records.iter().all(|record| {
            matches!(record, [b'+', key @ .., b'\n'] if elias_fano::decode(key).is_some())
        }) {
            return Err(body);
        }
        // Eight-byte ranks fit behind the next unread ten-byte record.
        let mut bytes = body.into_owned().into_bytes();
        for i in 0..count {
            let start = i * RECORD_BYTES + 1;
            let key = bytes[start..start + 8].try_into().unwrap();
            let rank = elias_fano::decode(key).expect("validated canonical key");
            bytes[i * 8..i * 8 + 8].copy_from_slice(&rank.to_ne_bytes());
        }
        let (numbers, _) = bytes[..count * 8].as_chunks_mut::<8>();
        numbers.sort_unstable_by_key(|word| u64::from_ne_bytes(*word));
        let mut distinct = 1;
        for i in 1..count {
            if numbers[i] != numbers[distinct - 1] {
                numbers[distinct] = numbers[i];
                distinct += 1;
            }
        }
        if let Ok(image) = Self::heap_from_sorted_ranks(namespace, name, &numbers[..distinct]) {
            return Ok(image);
        }
        // Encoding failed. Expand backwards to recover a replay of the same set.
        // The adapter advances the cursor by the original download length.
        bytes.truncate(distinct * RECORD_BYTES);
        for i in (0..distinct).rev() {
            let rank = u64::from_ne_bytes(bytes[i * 8..i * 8 + 8].try_into().unwrap());
            let line = &mut bytes[i * RECORD_BYTES..(i + 1) * RECORD_BYTES];
            line[0] = b'+';
            line[1..9].copy_from_slice(&elias_fano::encode(rank));
            line[9] = b'\n';
        }
        Err(Cow::Owned(
            String::from_utf8(bytes).expect("canonical add records"),
        ))
    }

    /// Compact a canonical private EF base using only the normalized edits as scratch.
    /// A mixed or overly dense result goes through the general image builder.
    pub(super) fn try_merge_heap<'a>(
        &self,
        name: &str,
        count: usize,
        changes: impl ExactSizeIterator<Item = (&'a [u8; 8], bool)>,
    ) -> Option<Self> {
        let base = self.ef?;
        if self.is_mapped() || self.inline.count != 0 || self.other.count != 0 {
            return None;
        }
        let layout = elias_fano::Ef::layout(count, 8).ok()?;
        let mut edits = Vec::new();
        edits.try_reserve_exact(changes.len()).ok()?;
        for (key, present) in changes {
            edits.push(elias_fano::RankEdit::new(elias_fano::decode(key)?, present));
        }
        edits.sort_unstable();
        if base.density_rejects_edits(&self.map, layout, &edits) {
            return None;
        }

        let namespace = &[0; 32];
        let length = checked_add(HEADER_LEN, layout.end).ok()?;
        let mut bytes = Vec::new();
        bytes.try_reserve_exact(length).ok()?;
        write_header(&mut bytes, namespace, name, COMPACT_VERSION, [0; 5]).ok()?;
        bytes.resize(length, 0);
        let mut output = layout.stream(&mut bytes[HEADER_LEN..]);
        let mut edits = edits.into_iter().peekable();
        let walked = base
            .walk(&self.map, |rank| {
                while let Some(edit) = edits.next_if(|edit| edit.rank() <= rank) {
                    // A normalized edit at an existing rank is a removal. Ranks
                    // between consecutive base members can only be insertions.
                    if edit.rank() == rank {
                        return !edit.present();
                    }
                    if !edit.present() || !output.push(edit.rank()) {
                        return false;
                    }
                }
                output.push(rank)
            })
            .ok()?;
        if walked && edits.all(|edit| edit.present() && output.push(edit.rank())) && output.finish()
        {
            Self::parse(ImageBytes::Heap(bytes.into_boxed_slice()), namespace, name).ok()
        } else {
            None
        }
    }

    fn heap_from_sorted_ranks(
        namespace: &[u8; 32],
        name: &str,
        ranks: &[[u8; 8]],
    ) -> io::Result<Self> {
        let mut map = Vec::new();
        if let Some(ef) = elias_fano::Ef::for_sorted_ranks(ranks)? {
            write_header(&mut map, namespace, name, COMPACT_VERSION, [0; 5])?;
            map.write_ef(ef, ranks, 0)?;
        } else {
            // Use the ordinary v2 hash image when the EF density guard rejects the set.
            let keys = ranks
                .iter()
                .map(|word| elias_fano::encode(u64::from_ne_bytes(*word)))
                .collect();
            encode_image(
                &mut map,
                namespace,
                name,
                (keys, Vec::new()),
                INLINE_SIZING,
                FALLBACK_SIZING,
                false,
            )?;
        }
        Self::parse(ImageBytes::Heap(map.into_boxed_slice()), namespace, name)
    }

    fn parse(map: ImageBytes, namespace: &[u8; 32], name: &str) -> io::Result<Self> {
        let length = map.len();
        if length < HEADER_LEN {
            return Err(invalid("truncated ID-list header"));
        }
        let ef = match read_u32(&map, 8) {
            VERSION => None,
            COMPACT_VERSION if length >= HEADER_LEN + 8 => Some(elias_fano::Ef::layout(
                to_usize(read_u64(&map, HEADER_LEN))?,
                HEADER_LEN + 8,
            )?),
            _ => return Err(invalid("unsupported ID-list file version")),
        };
        let tables_start = ef.map_or(HEADER_LEN, |e| e.end);
        if &map[..8] != MAGIC
            || read_u32(&map, 12) != 0
            || read_u32(&map, 120) != HASH_ALGORITHM
            || read_u32(&map, 124) != 0
        {
            return Err(invalid("unsupported ID-list file format"));
        }
        if &map[16..48] != namespace || map[48..80] != digest(name.as_bytes()) {
            return Err(invalid("ID-list file identity mismatch"));
        }
        let inline_count = to_usize(read_u64(&map, 80))?;
        let other_count = to_usize(read_u64(&map, 88))?;
        checked_add(
            checked_add(inline_count, other_count)?,
            ef.map_or(0, |e| e.count),
        )?;
        let blob_len = to_usize(read_u64(&map, 96))?;
        let (inline, end) = Table::new(
            tables_start,
            inline_count,
            to_usize(read_u64(&map, 104))?,
            8,
        )?;
        let (other, blob_start) = Table::new(end, other_count, to_usize(read_u64(&map, 112))?, 16)?;
        checked_add(inline.capacity, other.capacity)?;
        if checked_add(blob_start, blob_len)? != map.len() {
            return Err(invalid("ID-list file length does not match its header"));
        }
        let view = Self {
            map,
            content_digest: OnceLock::new(),
            ef,
            iter_keys: OnceLock::new(),
            inline,
            other,
            blob_start,
        };
        Ok(view)
    }

    /// Verifies the writer's semantic invariants in construction tests.
    #[cfg(test)]
    pub(super) fn validate_membership(&self) -> io::Result<()> {
        for (table, is_inline) in [(self.inline, true), (self.other, false)] {
            for slot in 0..table.capacity {
                let control = self.map[table.controls + slot];
                if control == EMPTY {
                    continue;
                }
                let value = self.slot_bytes(table, slot, is_inline);
                if control != fingerprint(stable_hash(value), is_inline) {
                    return Err(invalid("ID-list fingerprint does not match its key"));
                }
                if self.find_slot(table, value, is_inline) != Some(slot) {
                    return Err(invalid("duplicate or unreachable ID-list hash entry"));
                }
            }
        }
        Ok(())
    }

    fn validate_table(&self, table: Table, inline: bool, blob_len: usize) -> io::Result<()> {
        if table.capacity == 0 {
            return Ok(());
        }
        if self.map[table.controls..table.controls + GROUP]
            != self.map[table.controls + table.capacity..table.controls + table.capacity + GROUP]
        {
            return Err(invalid("invalid ID-list mirrored controls"));
        }
        let mut count = 0;
        for slot in 0..table.capacity {
            let control = self.map[table.controls + slot];
            if control == EMPTY {
                continue;
            }
            if control & EMPTY != 0 {
                return Err(invalid("invalid ID-list control byte"));
            }
            if !inline {
                let start = to_usize(read_u64(&self.map, table.slots + slot * 16))?;
                let len = to_usize(read_u64(&self.map, table.slots + slot * 16 + 8))?;
                if len == 8 || checked_add(start, len)? > blob_len {
                    return Err(invalid("invalid ID-list string bounds"));
                }
            }
            let bytes = self.slot_bytes(table, slot, inline);
            if inline
                && self.ef.is_some()
                && bytes.try_into().ok().and_then(elias_fano::decode).is_some()
            {
                return Err(invalid("canonical EF key found in raw-eight fallback"));
            }
            std::str::from_utf8(bytes).map_err(|_| invalid("invalid ID-list UTF-8"))?;
            count += 1;
        }
        if count != table.count {
            return Err(invalid("ID-list occupied count mismatch"));
        }
        Ok(())
    }

    #[cfg(test)]
    pub(super) fn has_cached_iter_keys(&self) -> bool {
        self.iter_keys.get().is_some()
    }

    #[cfg(test)]
    pub(super) fn is_compact(&self) -> bool {
        self.ef.is_some()
    }

    pub(crate) fn len(&self) -> usize {
        let (a, b) = self.partition_counts();
        a + b
    }
    pub(super) fn partition_counts(&self) -> (usize, usize) {
        let n = self.ef.map_or(0, |ef| ef.count);
        (self.inline.count + n, self.other.count)
    }
    pub(super) fn is_mapped(&self) -> bool {
        matches!(self.map, ImageBytes::Mapped { .. })
    }

    pub(crate) fn mapped_bytes(&self) -> usize {
        if self.is_mapped() { self.map.len() } else { 0 }
    }
    pub(super) fn content_digest(&self) -> String {
        self.content_digest
            .get_or_init(|| hex(&digest(&self.map)))
            .clone()
    }

    /// Test keys by value, stopping at the first mismatch without filling the spelling cache.
    pub(super) fn all_image_keys<'a>(
        &'a self,
        mut inline: impl FnMut([u8; 8]) -> bool,
        mut other: impl FnMut(&'a str) -> bool,
    ) -> bool {
        if self.ef.is_some_and(|ef| {
            !ef.walk(&self.map, |v| inline(elias_fano::encode(v)))
                .expect("validated EF view")
        }) {
            return false;
        }
        let controls = &self.map[self.inline.controls..self.inline.controls + self.inline.capacity];
        let slots = &self.map[self.inline.slots..self.inline.slots + self.inline.capacity * 8];
        for (control, bytes) in controls.iter().zip(slots.chunks_exact(8)) {
            if *control != EMPTY && !inline(bytes.try_into().expect("fixed-size inline slot")) {
                return false;
            }
        }
        for slot in 0..self.other.capacity {
            if self.map[self.other.controls + slot] != EMPTY {
                let key = std::str::from_utf8(self.slot_bytes(self.other, slot, false))
                    .expect("mapped ID-list UTF-8 was validated");
                if !other(key) {
                    return false;
                }
            }
        }
        true
    }

    pub(super) fn slot_capacity(&self) -> usize {
        self.inline.capacity + self.other.capacity
    }

    pub(super) fn lookup_index_hashed(&self, value: &str, hash: u64) -> Option<usize> {
        let inline = value.len() == 8;
        self.find_slot_hashed(
            if inline { self.inline } else { self.other },
            value.as_bytes(),
            inline,
            hash,
        )
        .map(|slot| {
            if inline {
                slot
            } else {
                self.inline.capacity + slot
            }
        })
    }

    fn compact_membership(&self, value: &str) -> Option<bool> {
        let ef = self.ef?;
        let x = elias_fano::decode(value.as_bytes().try_into().ok()?)?;
        Some(ef.contains(&self.map, x))
    }

    pub(super) fn contains_hashed(&self, value: &str, hash: u64) -> bool {
        if let Some(present) = self.compact_membership(value) {
            return present;
        }
        self.lookup_index_hashed(value, hash).is_some()
    }

    /// The cursor addresses physical slots, not a dense member ordinal. This
    /// keeps iteration linear without retaining an ordinal-to-slot index.
    pub(crate) fn next<'a>(&'a self, cursor: &mut usize) -> Option<&'a str> {
        while *cursor < self.inline.capacity + self.other.capacity {
            let current = *cursor;
            *cursor += 1;
            let (table, slot, inline) = if current < self.inline.capacity {
                (self.inline, current, true)
            } else {
                (self.other, current - self.inline.capacity, false)
            };
            if self.map[table.controls + slot] != EMPTY {
                return Some(
                    std::str::from_utf8(self.slot_bytes(table, slot, inline))
                        .expect("mapped ID-list UTF-8 was validated"),
                );
            }
        }
        if let Some(ef) = self.ef {
            let i = *cursor - self.slot_capacity();
            if i < ef.count {
                *cursor += 1;
                // The public iterator borrows strings. Only that API needs a stable
                // spelling for each packed key; image writing walks EF directly.
                let key = &self.iter_keys.get_or_init(|| {
                    let mut keys = Vec::with_capacity(ef.count);
                    ef.walk(&self.map, |v| {
                        keys.push(elias_fano::encode(v));
                        true
                    })
                    .expect("validated EF view");
                    keys.into_boxed_slice()
                })[i];
                return Some(std::str::from_utf8(key).expect("canonical EF key"));
            }
        }
        None
    }

    pub(crate) fn contains(&self, value: &str) -> bool {
        if let Some(present) = self.compact_membership(value) {
            return present;
        }
        let inline = value.len() == 8;
        self.find_slot(
            if inline { self.inline } else { self.other },
            value.as_bytes(),
            inline,
        )
        .is_some()
    }

    fn slot_bytes(&self, table: Table, slot: usize, inline: bool) -> &[u8] {
        if inline {
            &self.map[table.slots + slot * 8..table.slots + (slot + 1) * 8]
        } else {
            let start = self.blob_start + read_u64(&self.map, table.slots + slot * 16) as usize;
            let len = read_u64(&self.map, table.slots + slot * 16 + 8) as usize;
            &self.map[start..start + len]
        }
    }

    fn find_slot(&self, table: Table, value: &[u8], inline: bool) -> Option<usize> {
        self.find_slot_hashed(table, value, inline, stable_hash(value))
    }

    fn find_slot_hashed(
        &self,
        table: Table,
        value: &[u8],
        inline: bool,
        hash: u64,
    ) -> Option<usize> {
        if table.capacity == 0 {
            return None;
        }
        let mut group = table.home(hash, inline);
        for _ in 0..table.capacity / GROUP {
            let (mut matches, empty) =
                group_masks(&self.map, table.controls + group, fingerprint(hash, inline));
            while matches != 0 {
                let slot = table.advance(group, matches.trailing_zeros() as usize);
                if self.slot_bytes(table, slot, inline) == value {
                    return Some(slot);
                }
                matches &= matches - 1;
            }
            if empty != 0 {
                return None;
            }
            group = table.advance(group, GROUP);
        }
        None
    }
}

/// Algorithm 2 is fixed for this file format: SplitMix64's avalanche on an
/// eight-byte little-endian key. Other lengths use a length-dependent initial
/// state and, for keys of at least 32 bytes, four independent lanes for 32-byte
/// stripes, initialized directly from the length and fixed seed. Remaining
/// full words feed successive lanes; the partial tail has an independent mix
/// and rotation before the final merge. This avoids a serial tail dependency.
/// Do not substitute a platform-selected or random hasher.
pub(super) fn stable_hash(bytes: &[u8]) -> u64 {
    const SEED: u64 = 0x9e37_79b9_7f4a_7c15;
    if bytes.len() == 8 {
        return mix(read_u64(bytes, 0) ^ SEED);
    }
    let mut hash = bytes.len() as u64 ^ SEED;
    if bytes.len() < 32 {
        hash = mix(hash);
        let mut chunks = bytes.chunks_exact(8);
        for chunk in &mut chunks {
            hash = mix(hash ^ read_u64(chunk, 0));
        }
        let tail_len = chunks.remainder().len();
        let tail = if tail_len == 0 {
            0
        } else if bytes.len() >= 8 {
            // The final word is entirely inside the input. Discard its already
            // consumed prefix to obtain the same zero-padded little-endian tail.
            read_u64(bytes, bytes.len() - 8) >> ((8 - tail_len) * 8)
        } else if tail_len >= 4 {
            // Overlapping bytes occupy the same bit positions and agree, so OR
            // reconstructs the zero-padded word using only in-bounds scalar loads.
            u64::from(read_u32(bytes, 0))
                | (u64::from(read_u32(bytes, tail_len - 4)) << ((tail_len - 4) * 8))
        } else if tail_len >= 2 {
            u64::from(u16::from_le_bytes([bytes[0], bytes[1]]))
                | (u64::from(u16::from_le_bytes([
                    bytes[tail_len - 2],
                    bytes[tail_len - 1],
                ])) << ((tail_len - 2) * 8))
        } else {
            u64::from(bytes[0])
        };
        return mix(hash ^ tail);
    }

    let mut lanes = [
        hash,
        hash ^ 0xbf58_476d_1ce4_e5b9,
        hash ^ 0x94d0_49bb_1331_11eb,
        hash ^ 0xd6e8_feb8_6659_fd93,
    ];
    let mut stripes = bytes.chunks_exact(32);
    for stripe in &mut stripes {
        lanes[0] = mix(lanes[0] ^ read_u64(stripe, 0));
        lanes[1] = mix(lanes[1] ^ read_u64(stripe, 8));
        lanes[2] = mix(lanes[2] ^ read_u64(stripe, 16));
        lanes[3] = mix(lanes[3] ^ read_u64(stripe, 24));
    }
    let remainder = stripes.remainder();
    let words = remainder.len() / 8;
    if words >= 1 {
        lanes[0] = mix(lanes[0] ^ read_u64(remainder, 0));
    }
    if words >= 2 {
        lanes[1] = mix(lanes[1] ^ read_u64(remainder, 8));
    }
    if words >= 3 {
        lanes[2] = mix(lanes[2] ^ read_u64(remainder, 16));
    }
    let tail_len = remainder.len() % 8;
    let tail_hash = if tail_len != 0 {
        let tail = read_u64(bytes, bytes.len() - 8) >> ((8 - tail_len) * 8);
        // Independent partial-word lane; reuse an existing fixed domain constant.
        mix(hash ^ tail ^ 0xd6e8_feb8_6659_fd93)
    } else {
        0
    };
    mix(hash
        ^ lanes[0]
        ^ lanes[1].rotate_left(13)
        ^ lanes[2].rotate_left(29)
        ^ lanes[3].rotate_left(47)
        ^ tail_hash.rotate_left(37))
}

fn mix(mut value: u64) -> u64 {
    value = (value ^ (value >> 30)).wrapping_mul(0xbf58_476d_1ce4_e5b9);
    value = (value ^ (value >> 27)).wrapping_mul(0x94d0_49bb_1331_11eb);
    value ^ (value >> 31)
}
fn fingerprint(hash: u64, inline: bool) -> u8 {
    if inline {
        (hash >> 57) as u8
    } else {
        (hash & 0x7f) as u8
    }
}

#[cfg(target_arch = "x86_64")]
fn group_masks(bytes: &[u8], start: usize, fingerprint: u8) -> (u16, u16) {
    use std::arch::x86_64::{_mm_cmpeq_epi8, _mm_loadu_si128, _mm_movemask_epi8, _mm_set1_epi8};
    // SSE2 is part of x86_64. Every caller supplies a full group, including the
    // mirrored suffix when the probe straddles the table's end.
    let group = &bytes[start..start + GROUP];
    unsafe {
        let values = _mm_loadu_si128(group.as_ptr().cast());
        let matches = _mm_movemask_epi8(_mm_cmpeq_epi8(values, _mm_set1_epi8(fingerprint as i8)));
        let empty = _mm_movemask_epi8(_mm_cmpeq_epi8(values, _mm_set1_epi8(EMPTY as i8)));
        (matches as u16, empty as u16)
    }
}
#[cfg(not(target_arch = "x86_64"))]
fn group_masks(bytes: &[u8], start: usize, fingerprint: u8) -> (u16, u16) {
    let mut matches = 0;
    let mut empty = 0;
    for (bit, control) in bytes[start..start + GROUP].iter().enumerate() {
        matches |= u16::from(*control == fingerprint) << bit;
        empty |= u16::from(*control == EMPTY) << bit;
    }
    (matches, empty)
}

/// A canonical insertion order gives unchanged contents the same image digest.
/// Build scratch consists of sorted key references/inline keys and hash slots;
/// readers retain only the mapping and its fixed-size header metadata.
#[cfg(test)]
pub(super) fn write_list(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    ids: &IdListIds,
) -> io::Result<String> {
    write_list_with_format(file, namespace, name, ids, false)
}

pub(super) fn write_list_with_format(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    ids: &IdListIds,
    compact: bool,
) -> io::Result<String> {
    let mut hashed = HashingWriter {
        file,
        digest: Sha256::new(),
    };
    let mut writer = BufWriter::with_capacity(64 * 1024, &mut hashed);
    if let Some(section) = ids.packed_ef_section().filter(|_| compact) {
        // A v3 base with empty hash partitions is the local header followed by
        // exactly the validated wire section, including its count and read padding.
        write_header(&mut writer, namespace, name, COMPACT_VERSION, [0; 5])?;
        writer.write_all(section)?;
    } else {
        encode_image(
            &mut writer,
            namespace,
            name,
            ids.collect_image_keys(),
            INLINE_SIZING,
            FALLBACK_SIZING,
            compact,
        )?;
    }
    writer.flush()?;
    drop(writer);
    Ok(hex(&hashed.digest.finalize()))
}

#[cfg(test)]
pub(super) fn write_list_with_sizing(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    ids: &IdListIds,
    sizing: HashTableSizing,
) -> io::Result<()> {
    let mut writer = BufWriter::new(file);
    encode_image(
        &mut writer,
        namespace,
        name,
        ids.collect_image_keys(),
        sizing,
        sizing,
        false,
    )?;
    writer.flush()
}

pub(super) fn write_image_keys(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    keys: (Vec<[u8; 8]>, Vec<&str>),
) -> io::Result<()> {
    let mut writer = BufWriter::with_capacity(64 * 1024, file);
    encode_image(
        &mut writer,
        namespace,
        name,
        keys,
        INLINE_SIZING,
        FALLBACK_SIZING,
        false,
    )?;
    writer.flush()
}

/// Heap images pack directly into their final allocation. Files buffer only
/// the EF section and stream the remaining tables to the existing writer.
trait ImageWriter: Write {
    fn write_ef(
        &mut self,
        ef: elias_fano::Ef,
        numbers: &[[u8; 8]],
        table_bytes: usize,
    ) -> io::Result<()>;
}

impl ImageWriter for Vec<u8> {
    fn write_ef(
        &mut self,
        ef: elias_fano::Ef,
        numbers: &[[u8; 8]],
        table_bytes: usize,
    ) -> io::Result<()> {
        let start = self.len();
        self.try_reserve_exact(checked_add(ef.end, table_bytes)?)
            .map_err(io::Error::other)?;
        self.resize(checked_add(start, ef.end)?, 0);
        ef.pack(numbers, &mut self[start..]);
        Ok(())
    }
}

impl<W: Write> ImageWriter for BufWriter<W> {
    fn write_ef(
        &mut self,
        ef: elias_fano::Ef,
        numbers: &[[u8; 8]],
        _table_bytes: usize,
    ) -> io::Result<()> {
        let mut section = vec![0; ef.end];
        ef.pack(numbers, &mut section);
        self.write_all(&section)
    }
}

fn encode_image(
    writer: &mut impl ImageWriter,
    namespace: &[u8; 32],
    name: &str,
    keys: (Vec<[u8; 8]>, Vec<&str>),
    inline_sizing: HashTableSizing,
    fallback_sizing: HashTableSizing,
    compact: bool,
) -> io::Result<()> {
    let (mut inline, mut other) = keys;
    let packed = if compact {
        elias_fano::Ef::prepare(&mut inline)?
    } else {
        None
    };
    let inline_count = inline.len();
    inline.sort_unstable();
    other.sort_unstable();
    let inline_capacity = inline_sizing.capacity(inline.len())?;
    let other_capacity = fallback_sizing.capacity(other.len())?;
    let blob_len = other
        .iter()
        .try_fold(0, |len, key| checked_add(len, key.len()))?;
    write_header(
        writer,
        namespace,
        name,
        if packed.is_some() {
            COMPACT_VERSION
        } else {
            VERSION
        },
        [
            inline_count as u64,
            other.len() as u64,
            blob_len as u64,
            inline_capacity as u64,
            other_capacity as u64,
        ],
    )?;
    if let Some((ef, numbers)) = packed {
        // Table offsets are relative to the end of the EF section.
        let (_, end) = Table::new(0, inline_count, inline_capacity, 8)?;
        let (_, end) = Table::new(end, other.len(), other_capacity, 16)?;
        writer.write_ef(ef, &numbers, checked_add(end, blob_len)?)?;
    }

    let mut inline_controls = controls(inline_capacity)?;
    let mut inline_slots = vec![[0u8; 8]; inline_capacity];
    for value in inline {
        let slot = insert_slot(
            &mut inline_controls,
            inline_capacity,
            stable_hash(&value),
            true,
        )?;
        inline_slots[slot] = value;
    }
    let mut other_controls = controls(other_capacity)?;
    let mut other_slots = vec![[0u64; 2]; other_capacity];
    let mut offset = 0u64;
    for value in &other {
        let slot = insert_slot(
            &mut other_controls,
            other_capacity,
            stable_hash(value.as_bytes()),
            false,
        )?;
        other_slots[slot] = [offset, value.len() as u64];
        offset += value.len() as u64;
    }
    writer.write_all(&inline_controls)?;
    for value in inline_slots {
        writer.write_all(&value)?;
    }
    writer.write_all(&other_controls)?;
    for [offset, len] in other_slots {
        writer.write_all(&offset.to_le_bytes())?;
        writer.write_all(&len.to_le_bytes())?;
    }
    for value in other {
        writer.write_all(value.as_bytes())?;
    }
    Ok(())
}

fn write_header(
    writer: &mut impl Write,
    namespace: &[u8; 32],
    name: &str,
    version: u32,
    counts: [u64; 5],
) -> io::Result<()> {
    writer.write_all(MAGIC)?;
    writer.write_all(&version.to_le_bytes())?;
    writer.write_all(&0u32.to_le_bytes())?;
    writer.write_all(namespace)?;
    writer.write_all(&digest(name.as_bytes()))?;
    for number in counts {
        writer.write_all(&number.to_le_bytes())?;
    }
    writer.write_all(&HASH_ALGORITHM.to_le_bytes())?;
    writer.write_all(&0u32.to_le_bytes())
}

fn controls(capacity: usize) -> io::Result<Vec<u8>> {
    Ok(vec![
        EMPTY;
        if capacity == 0 {
            0
        } else {
            checked_add(capacity, GROUP)?
        }
    ])
}
fn insert_slot(controls: &mut [u8], capacity: usize, hash: u64, inline: bool) -> io::Result<usize> {
    let table = Table {
        controls: 0,
        slots: 0,
        capacity,
        count: 0,
    };
    let mut group = table.home(hash, inline);
    for _ in 0..capacity / GROUP {
        let (_, empty) = group_masks(controls, group, fingerprint(hash, inline));
        if empty != 0 {
            let slot = table.advance(group, empty.trailing_zeros() as usize);
            controls[slot] = fingerprint(hash, inline);
            if slot < GROUP {
                controls[capacity + slot] = fingerprint(hash, inline);
            }
            return Ok(slot);
        }
        group = table.advance(group, GROUP);
    }
    Err(invalid("ID-list hash table is full"))
}

struct HashingWriter<'a> {
    file: &'a mut File,
    digest: Sha256,
}
impl Write for HashingWriter<'_> {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        let written = self.file.write(bytes)?;
        self.digest.update(&bytes[..written]);
        Ok(written)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.file.flush()
    }
}
pub(super) fn digest(bytes: &[u8]) -> [u8; 32] {
    Sha256::digest(bytes).into()
}
pub(super) fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|byte| format!("{byte:02x}")).collect()
}
pub(super) fn invalid(message: &str) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, message)
}
fn read_u32(bytes: &[u8], offset: usize) -> u32 {
    u32::from_le_bytes(bytes[offset..offset + 4].try_into().unwrap())
}
fn read_u64(bytes: &[u8], offset: usize) -> u64 {
    u64::from_le_bytes(bytes[offset..offset + 8].try_into().unwrap())
}
fn to_usize(value: u64) -> io::Result<usize> {
    usize::try_from(value).map_err(|_| invalid("ID-list offset exceeds platform bounds"))
}
pub(super) fn checked_add(a: usize, b: usize) -> io::Result<usize> {
    a.checked_add(b)
        .ok_or_else(|| invalid("ID-list offset overflow"))
}
fn checked_mul(a: usize, b: usize) -> io::Result<usize> {
    a.checked_mul(b)
        .ok_or_else(|| invalid("ID-list offset overflow"))
}

#[cfg(test)]
#[path = "shared_id_list_collection_tests.rs"]
mod collection_tests;

#[cfg(test)]
#[path = "elias_fano_tests.rs"]
mod elias_fano_tests;
