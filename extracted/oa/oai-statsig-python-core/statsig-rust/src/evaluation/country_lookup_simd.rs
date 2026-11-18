use super::CountryLookup;
use std::arch::x86_64::*;

#[derive(Clone, Copy)]
struct Layout {
    separators: u16,
    shuffle: [u8; 16],
}

// Three dots and a marker at the end distinguish the 3^4 possible octet widths.
// This hash puts all 81 layouts in distinct slots, checked at compile time below.
const fn slot(separators: u16) -> usize {
    ((separators as usize * 3359) >> 7) & 255
}

static LAYOUTS: [Layout; 256] = {
    let mut layouts = [Layout {
        separators: 0,
        shuffle: [0x80; 16],
    }; 256];
    let mut pattern = 0;
    while pattern < 81 {
        let mut widths = pattern;
        let mut shuffle = [0x80; 16];
        let mut separators = 0;
        let mut start = 0;
        let mut octet = 0;
        while octet < 4 {
            let width = widths % 3 + 1;
            widths /= 3;
            let mut digit = 0;
            while digit < width {
                shuffle[4 * octet + 4 - width + digit] = (start + digit) as u8;
                digit += 1;
            }
            separators |= 1 << (start + width);
            start += width + 1;
            octet += 1;
        }
        assert!(layouts[slot(separators)].separators == 0);
        layouts[slot(separators)] = Layout {
            separators,
            shuffle,
        };
        pattern += 1;
    }
    layouts
};

#[target_feature(enable = "avx512bw,avx512vl")]
pub(super) unsafe fn parse(ip: &str) -> Option<u32> {
    let end = 1u16 << ip.len();
    let active = end - 1;
    // SAFETY: each enabled byte lies within ip. Masked-off lanes do not access memory.
    let bytes = unsafe { _mm_maskz_loadu_epi8(active, ip.as_ptr().cast()) };
    let dots = _mm_cmpeq_epi8_mask(bytes, _mm_set1_epi8(b'.' as i8));
    let separators = dots | end;
    let layout = &LAYOUTS[slot(separators)];
    let digits = _mm_sub_epi8(bytes, _mm_set1_epi8(b'0' as i8));
    // u8::from_str also accepts extra leading zeros and a leading plus.
    if layout.separators != separators
        || _mm_mask_cmpgt_epu8_mask(active ^ dots, digits, _mm_set1_epi8(9)) != 0
    {
        return CountryLookup::parse_scalar(ip);
    }
    // Each group of four bytes now contains [0, hundreds, tens, ones].
    // SAFETY: shuffle is exactly 16 initialized bytes and the load permits any alignment.
    let shuffle = unsafe { _mm_loadu_si128(layout.shuffle.as_ptr().cast()) };
    let grouped = _mm_shuffle_epi8(digits, shuffle);
    let weights = _mm_set1_epi32(i32::from_le_bytes([0, 100, 10, 1]));
    let pairs = _mm_maddubs_epi16(grouped, weights);
    let octets = _mm_madd_epi16(pairs, _mm_set1_epi16(1));
    if _mm_cmpgt_epi32_mask(octets, _mm_set1_epi32(255)) != 0 {
        return None;
    }
    let packed = _mm_cvtepi32_epi8(octets);
    Some((_mm_cvtsi128_si32(packed) as u32).swap_bytes())
}
