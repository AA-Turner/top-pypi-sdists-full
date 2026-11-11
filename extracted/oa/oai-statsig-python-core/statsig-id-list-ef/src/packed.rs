//! Eight characters from the standard Base64 alphabet encode one exact 48-bit key.
//! The compact section stores the member count, a restart directory, packed low
//! bits in sorted order, and a unary high-bit stream. Each high bucket contributes
//! one set bit per member followed by a zero separator. Directory entries are
//! bit offsets into that stream. Both bit arrays have eight bytes of read padding.
use super::{checked_add, checked_mul, invalid, read_u32, read_u64};
use std::io;

const RESTART_BUCKETS: usize = 32;
// Includes each bucket's zero separator. Starting at its restart, lookup
// reads at most about ten high-bit words (including an unaligned start and
// a repeated word at the target bucket). This bounds scanning, not latency.
const MAX_SPAN_BITS: usize = 512;
const U: u64 = 1 << 48;
const ABC: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const LUT: [u8; 256] = {
    let mut tbl = [255; 256];
    let mut i = 0;
    while i < 64 {
        tbl[ABC[i] as usize] = i as u8;
        i += 1;
    }
    tbl
};

pub fn decode(raw: &[u8; 8]) -> Option<u64> {
    let mut value = 0u64;
    let mut bad = 0;
    for c in raw {
        let d = LUT[*c as usize];
        bad |= d;
        value = (value << 6) | u64::from(d);
    }
    (bad < 64).then_some(value)
}

/// Sorts by the 48-bit rank, with the operation in the spare low bit.
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct RankEdit(u64);

impl RankEdit {
    pub fn new(rank: u64, present: bool) -> Self {
        debug_assert!(rank < U);
        Self((rank << 1) | u64::from(present))
    }

    pub fn rank(self) -> u64 {
        self.0 >> 1
    }

    pub fn present(self) -> bool {
        self.0 & 1 != 0
    }
}

#[derive(Clone, Copy)]
pub struct Ef {
    pub count: usize,
    low_bits: usize,
    buckets: usize,
    directory: usize,
    lows: usize,
    highs: usize,
    pub end: usize,
}

pub fn encode(value: u64) -> [u8; 8] {
    std::array::from_fn(|c| ABC[((value >> (42 - 6 * c)) & 63) as usize])
}

impl Ef {
    pub fn supports_count(count: usize) -> bool {
        (1..=u32::MAX as usize / 3).contains(&count)
    }

    pub fn layout(count: usize, start: usize) -> io::Result<Self> {
        if !Self::supports_count(count) {
            return Err(invalid("unsupported EF count"));
        }
        let low_bits = (U / count as u64).ilog2() as usize;
        let buckets = (U >> low_bits) as usize;
        let directory = start;
        let lows = checked_add(
            directory,
            checked_mul(buckets.div_ceil(RESTART_BUCKETS), 4)?,
        )?;
        // Padding permits a single unaligned little-endian word read at the end.
        let highs = checked_add(
            lows,
            checked_add(checked_mul(count, low_bits)?.div_ceil(8), 8)?,
        )?;
        let end = checked_add(
            highs,
            checked_add(checked_add(buckets, count)?.div_ceil(8), 8)?,
        )?;
        Ok(Self {
            count,
            low_bits,
            buckets,
            directory,
            lows,
            highs,
            end,
        })
    }
    pub fn prepare(keys: &mut Vec<[u8; 8]>) -> io::Result<Option<(Self, Vec<[u8; 8]>)>> {
        let mut numbers = Vec::new();
        keys.retain(|key| match decode(key) {
            Some(rank) => {
                numbers.push(rank.to_ne_bytes());
                false
            }
            None => true,
        });
        if Self::supports_count(numbers.len()) {
            numbers.sort_unstable_by_key(|word| u64::from_ne_bytes(*word));
            if let Some(ef) = Self::for_sorted_ranks(&numbers)? {
                return Ok(Some((ef, numbers)));
            }
        }
        keys.extend(
            numbers
                .into_iter()
                .map(|word| encode(u64::from_ne_bytes(word))),
        );
        Ok(None)
    }

    /// Ranks are native-endian words so a download buffer need not be aligned for u64.
    pub fn for_sorted_ranks(numbers: &[[u8; 8]]) -> io::Result<Option<Self>> {
        if !Self::supports_count(numbers.len()) {
            return Ok(None);
        }
        let ef = Self::layout(numbers.len(), 8)?;
        let block =
            |word: [u8; 8]| (u64::from_ne_bytes(word) >> ef.low_bits) as usize / RESTART_BUCKETS;
        for members in numbers.chunk_by(|a, b| block(*a) == block(*b)) {
            let first_bucket = block(members[0]) * RESTART_BUCKETS;
            let separators = RESTART_BUCKETS.min(ef.buckets - first_bucket);
            if members.len() > MAX_SPAN_BITS - separators {
                return Ok(None);
            }
        }
        Ok(Some(ef))
    }

    /// An unchanged bucket width lets us check density before walking the base.
    /// Each sorted edit must add an absent rank or remove a present rank.
    pub fn density_rejects_edits(self, base: &[u8], next: Self, edits: &[RankEdit]) -> bool {
        if self.low_bits != next.low_bits {
            return false; // The streaming packer checks density in the new layout.
        }
        let block = |edit: RankEdit| (edit.rank() >> self.low_bits) as usize / RESTART_BUCKETS;
        edits
            .chunk_by(|a, b| block(*a) == block(*b))
            .any(|changes| {
                let bucket = block(changes[0]) * RESTART_BUCKETS;
                let (start, end) = self.restart_span(base, bucket);
                // The old span includes this block's zero separators. A normalized
                // addition contributes one high bit; a removal takes one away.
                let additions = changes.iter().filter(|edit| edit.present()).count() as i64;
                end as i64 - start as i64 + 2 * additions - changes.len() as i64
                    > MAX_SPAN_BITS as i64
            })
    }

    fn restart_span(self, bytes: &[u8], bucket: usize) -> (usize, usize) {
        let offset = self.directory + 4 * (bucket / RESTART_BUCKETS);
        let start = read_u32(bytes, offset) as usize;
        let end = if bucket + RESTART_BUCKETS < self.buckets {
            read_u32(bytes, offset + 4) as usize
        } else {
            self.buckets + self.count
        };
        (start, end)
    }

    fn write_restart(self, bytes: &mut [u8], bucket: usize, ordinal: usize) {
        let offset = self.directory + 4 * (bucket / RESTART_BUCKETS);
        bytes[offset..offset + 4].copy_from_slice(&((bucket + ordinal) as u32).to_le_bytes());
    }

    fn write_rank(self, bytes: &mut [u8], bucket: usize, ordinal: usize, rank: u64) {
        let high = bucket + ordinal;
        bytes[self.highs + high / 8] |= 1 << (high % 8);
        let bit = ordinal * self.low_bits;
        let offset = self.lows + bit / 8;
        let low = rank & ((1u64 << self.low_bits) - 1);
        let word = read_u64(bytes, offset) | (low << (bit % 8));
        bytes[offset..offset + 8].copy_from_slice(&word.to_le_bytes());
    }

    /// Pack sorted, density-checked ranks directly into a zeroed EF section.
    pub fn pack(self, numbers: &[[u8; 8]], bytes: &mut [u8]) {
        bytes[..8].copy_from_slice(&(self.count as u64).to_le_bytes());
        let mut i = 0;
        for k in 0..self.buckets {
            if k % RESTART_BUCKETS == 0 {
                self.write_restart(bytes, k, i);
            }
            while i < numbers.len() && (u64::from_ne_bytes(numbers[i]) >> self.low_bits) == k as u64
            {
                self.write_rank(bytes, k, i, u64::from_ne_bytes(numbers[i]));
                i += 1;
            }
        }
    }

    /// Start an image whose final count is known. The EF section must be zeroed.
    pub fn stream(self, bytes: &mut [u8]) -> StreamPacker<'_> {
        bytes[..8].copy_from_slice(&(self.count as u64).to_le_bytes());
        StreamPacker {
            layout: self,
            bytes,
            ordinal: 0,
            next_restart: 0,
            block_start: 0,
            last_rank: 0,
        }
    }
    fn word(self, m: &[u8], b: usize) -> u64 {
        read_u64(m, self.highs + b / 8) >> (b % 8)
    }
    fn low(self, m: &[u8], i: usize) -> u64 {
        let b = i * self.low_bits;
        (read_u64(m, self.lows + b / 8) >> (b % 8)) & ((1u64 << self.low_bits) - 1)
    }
    pub fn contains(self, m: &[u8], x: u64) -> bool {
        let k = (x >> self.low_bits) as usize;
        let mut bit = read_u32(m, self.directory + 4 * (k / RESTART_BUCKETS)) as usize;
        let mut skip = k % RESTART_BUCKETS;
        while skip > 0 {
            let shift = bit % 8;
            let len = 64 - shift;
            let mask = u64::MAX >> shift;
            let mut zeros = (!self.word(m, bit)) & mask;
            let pop = zeros.count_ones() as usize;
            if skip > pop {
                bit += len;
                skip -= pop;
                continue;
            }
            for _ in 1..skip {
                zeros &= zeros - 1;
            }
            bit += zeros.trailing_zeros() as usize + 1;
            break;
        }
        let start = bit - k;
        let needle = x & ((1u64 << self.low_bits) - 1);
        let mut end = bit;
        loop {
            let available = 64 - end % 8;
            let run = self.word(m, end).trailing_ones() as usize;
            end += run;
            if run < available {
                break;
            }
        }
        let n = end - bit;
        if n < 8 {
            return (start..start + n).any(|i| self.low(m, i) == needle);
        }
        let mut a = start;
        let mut b = start + n;
        while a < b {
            let mid = a + (b - a) / 2;
            if self.low(m, mid) < needle {
                a = mid + 1
            } else {
                b = mid
            }
        }
        a < start + n && self.low(m, a) == needle
    }
    // Validate restart offsets, occupancy and member order as we walk. A predicate
    // may stop a trusted traversal early; validation at open always visits every member.
    pub fn walk(self, m: &[u8], mut visit: impl FnMut(u64) -> bool) -> io::Result<bool> {
        let mut i = 0;
        for k in 0..self.buckets {
            if k % RESTART_BUCKETS == 0 {
                let (start, end) = self.restart_span(m, k);
                if start != k + i
                    || end
                        .checked_sub(start)
                        .is_none_or(|span| span > MAX_SPAN_BITS)
                {
                    return Err(invalid("bad EF restart or density"));
                }
            }
            let mut prev = None;
            while self.word(m, k + i) & 1 != 0 {
                if i == self.count {
                    return Err(invalid("bad EF occupancy"));
                }
                let value = ((k as u64) << self.low_bits) | self.low(m, i);
                if prev.is_some_and(|p| p >= value) {
                    return Err(invalid("bad EF member"));
                }
                if !visit(value) {
                    return Ok(false);
                }
                prev = Some(value);
                i += 1;
            }
        }
        if i != self.count {
            return Err(invalid("bad EF count"));
        }
        Ok(true)
    }
}

pub struct StreamPacker<'a> {
    layout: Ef,
    bytes: &'a mut [u8],
    ordinal: usize,
    next_restart: usize,
    block_start: usize,
    last_rank: u64,
}

impl StreamPacker<'_> {
    // Empty blocks still need directory entries. They all begin at the same
    // member ordinal but have different offsets in the unary stream.
    fn write_restarts_before(&mut self, limit: usize) {
        while self.next_restart < limit {
            self.layout
                .write_restart(self.bytes, self.next_restart, self.ordinal);
            self.next_restart += RESTART_BUCKETS;
            self.block_start = self.ordinal;
        }
    }

    /// Returns false if this rank cannot be appended to the candidate image.
    pub fn push(&mut self, rank: u64) -> bool {
        if self.ordinal == self.layout.count
            || rank >= U
            || (self.ordinal > 0 && rank <= self.last_rank)
        {
            return false;
        }
        let bucket = (rank >> self.layout.low_bits) as usize;
        self.write_restarts_before(bucket + 1);
        let first_bucket = self.next_restart - RESTART_BUCKETS;
        let separators = RESTART_BUCKETS.min(self.layout.buckets - first_bucket);
        if self.ordinal - self.block_start >= MAX_SPAN_BITS - separators {
            return false;
        }
        self.layout
            .write_rank(self.bytes, bucket, self.ordinal, rank);
        self.last_rank = rank;
        self.ordinal += 1;
        true
    }

    pub fn finish(mut self) -> bool {
        if self.ordinal != self.layout.count {
            return false;
        }
        self.write_restarts_before(self.layout.buckets);
        true
    }
}
