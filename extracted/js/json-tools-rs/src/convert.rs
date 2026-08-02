//! Automatic type conversion for JSON string values.
//!
//! Detects and converts string representations of booleans, numbers, dates,
//! and null into their native JSON types. Handles locale-aware number formats
//! (EU comma decimals, accounting negatives) with SIMD-accelerated cleaning.

use chrono::{DateTime, Datelike, NaiveDate, NaiveDateTime, Timelike, Utc};
use memchr::{memchr, memchr2, memchr3, memchr_iter};
use smallvec::SmallVec;
use std::borrow::Cow;

use crate::config::{
    BooleanConversionConfig, DateConversionConfig, NullConversionConfig, NumberConversionConfig,
    TypeConversionConfig, TypeConversionMode,
};

#[inline(always)]
fn parse_f64(s: &str) -> Result<f64, std::num::ParseFloatError> {
    s.parse()
}

/// Try to parse a string into a number, handling various formats
/// Returns None if the string cannot be parsed as a valid number
///
/// Supports:
/// - Basic numbers: "123", "45.67", "-10"
/// - Scientific notation: "1e5", "1.23e-4"
/// - Thousands separators: "1,234.56" (US), "1.234,56" (EU), "1 234.56" (FR)
/// - Currency symbols: "$123.45", "99.99", "50.00"
/// - Percentages: "50%" -> 50.0 (not as decimal)
///
/// Optimized version that accepts already-trimmed string and has fast-path for clean numbers
/// Supports: basic numbers, scientific notation, percentages, permille, basis points,
/// suffixed numbers (K/M/B/T), fractions, hex/binary/octal, and various formatting
#[inline]
pub(crate) fn try_parse_number(trimmed: &str) -> Option<f64> {
    // Early exit for empty strings
    if trimmed.is_empty() {
        return None;
    }

    // Every supported format (plain numbers, currency, percentages, fractions, hex/binary/octal,
    // K/M/B/T suffixes) requires at least one ASCII digit. Strings with none -- ordinary
    // capitalized words ("Pending"), non-ASCII text ("café", "日本語"), "Infinity"/"NaN" -- can
    // never parse, so reject them before paying for the suffix checks and clean_number_string's
    // currency-stripping machinery below.
    if !trimmed.bytes().any(|b| b.is_ascii_digit()) {
        return None;
    }

    // Fast path: try direct parse first (handles basic numbers and scientific notation)
    // This catches ~90% of cases with minimal overhead
    // Guard against NaN/Infinity which str::parse may accept but aren't valid JSON numbers
    if let Ok(num) = parse_f64(trimmed) {
        if num.is_finite() {
            return Some(num);
        }
    }

    // Handle percentage strings (e.g., "50%" -> 50.0)
    if let Some(stripped) = trimmed.strip_suffix('%') {
        if let Ok(num) = parse_f64(stripped) {
            if num.is_finite() {
                return Some(num);
            }
        }
    }

    // Handle permille -- per thousand
    if let Some(stripped) = trimmed.strip_suffix('\u{2030}') {
        if let Ok(num) = parse_f64(stripped) {
            return Some(num / 1000.0);
        }
    }

    // Handle per ten-thousand -- basis points symbol
    if let Some(stripped) = trimmed.strip_suffix('\u{2031}') {
        if let Ok(num) = parse_f64(stripped) {
            return Some(num / 10000.0);
        }
    }

    // Byte-level discriminators: skip parsers that cannot possibly match,
    // avoiding function call overhead for the common case (plain numbers).
    let bytes = trimmed.as_bytes();
    let last = bytes[bytes.len() - 1];

    // Handle basis points: 25bp, 25bps, 25 bp, 25 bps -- only if ends with 'p' or 's'
    if matches!(last, b'p' | b's') {
        if let result @ Some(_) = try_parse_basis_points(trimmed) {
            return result;
        }
    }

    // Handle suffixed numbers: 1K, 2.5M, 3B, 1T -- only if last byte is K/M/B/T
    if matches!(last, b'K' | b'k' | b'M' | b'm' | b'B' | b'b' | b'T' | b't') {
        if let result @ Some(_) = try_parse_suffixed_number(trimmed) {
            return result;
        }
    }

    // Handle fractions: 1/2, 3/4, 2 1/2 -- only if '/' present (SIMD via memchr)
    if memchr(b'/', bytes).is_some() {
        if let result @ Some(_) = try_parse_fraction(trimmed) {
            return result;
        }
    }

    // Handle hex, binary, octal -- only if starts with 0x/0b/0o (or -0x etc.)
    let check = if bytes[0] == b'-' && bytes.len() > 1 {
        &bytes[1..]
    } else {
        bytes
    };
    let radix_result = if check.len() >= 2
        && check[0] == b'0'
        && matches!(check[1], b'x' | b'X' | b'b' | b'B' | b'o' | b'O')
    {
        try_parse_radix_number(trimmed)
    } else {
        None
    };
    if radix_result.is_some() {
        return radix_result;
    }

    // Slow path: clean common number formats and try again
    let cleaned = clean_number_string(trimmed);
    parse_f64(cleaned.as_ref()).ok().filter(|n| n.is_finite())
}

/// Configured variant of [`try_parse_number`]: plain numbers/scientific notation and
/// thousands-separator cleanup (via [`clean_number_string_configured`]) are always
/// applied; percent/permille/per-ten-thousand, text basis points, K/M/B/T suffixes,
/// fractions, and hex/binary/octal are each gated on their own
/// [`NumberConversionConfig`] field.
#[inline]
fn try_parse_number_configured(trimmed: &str, cfg: &NumberConversionConfig) -> Option<f64> {
    if trimmed.is_empty() {
        return None;
    }
    if !trimmed.bytes().any(|b| b.is_ascii_digit()) {
        return None;
    }

    if let Ok(num) = parse_f64(trimmed) {
        if num.is_finite() {
            return Some(num);
        }
    }

    if cfg.percent {
        if let Some(stripped) = trimmed.strip_suffix('%') {
            if let Ok(num) = parse_f64(stripped) {
                if num.is_finite() {
                    return Some(num);
                }
            }
        }
        if let Some(stripped) = trimmed.strip_suffix('\u{2030}') {
            if let Ok(num) = parse_f64(stripped) {
                return Some(num / 1000.0);
            }
        }
        if let Some(stripped) = trimmed.strip_suffix('\u{2031}') {
            if let Ok(num) = parse_f64(stripped) {
                return Some(num / 10000.0);
            }
        }
    }

    let bytes = trimmed.as_bytes();
    let last = bytes[bytes.len() - 1];

    if cfg.basis_points && matches!(last, b'p' | b's') {
        if let result @ Some(_) = try_parse_basis_points(trimmed) {
            return result;
        }
    }

    if cfg.suffixes && matches!(last, b'K' | b'k' | b'M' | b'm' | b'B' | b'b' | b'T' | b't') {
        if let result @ Some(_) = try_parse_suffixed_number(trimmed) {
            return result;
        }
    }

    if cfg.fractions && memchr(b'/', bytes).is_some() {
        if let result @ Some(_) = try_parse_fraction(trimmed) {
            return result;
        }
    }

    if cfg.radix {
        let check = if bytes[0] == b'-' && bytes.len() > 1 {
            &bytes[1..]
        } else {
            bytes
        };
        let radix_result = if check.len() >= 2
            && check[0] == b'0'
            && matches!(check[1], b'x' | b'X' | b'b' | b'B' | b'o' | b'O')
        {
            try_parse_radix_number(trimmed)
        } else {
            None
        };
        if radix_result.is_some() {
            return radix_result;
        }
    }

    // Slow path: clean common number formats and try again. Thousands-separator
    // cleanup is always applied; currency stripping is gated on `cfg.currency`.
    let cleaned = clean_number_string_configured(trimmed, cfg.currency);
    parse_f64(cleaned.as_ref()).ok().filter(|n| n.is_finite())
}

/// Parse basis points: 25bp, 25bps, 25 bp, 25 bps -> 0.0025
#[inline]
fn try_parse_basis_points(s: &str) -> Option<f64> {
    let s = s.trim();

    // Try "25bps" or "25bp" (no space)
    if let Some(num_str) = s.strip_suffix("bps").or_else(|| s.strip_suffix("bp")) {
        if let Ok(num) = parse_f64(num_str.trim()) {
            return Some(num / 10000.0);
        }
    }

    // Try "25 bps" or "25 bp" (with space)
    if let Some(num_str) = s.strip_suffix(" bps").or_else(|| s.strip_suffix(" bp")) {
        if let Ok(num) = parse_f64(num_str.trim()) {
            return Some(num / 10000.0);
        }
    }

    None
}

/// Parse suffixed numbers: 1K, 2.5M, 3B, 1T, 1k, 2.5m (case-insensitive)
/// K = thousand (1,000), M = million (1,000,000), B = billion (1,000,000,000), T = trillion
#[inline]
fn try_parse_suffixed_number(s: &str) -> Option<f64> {
    let s = s.trim();
    if s.len() < 2 {
        return None;
    }

    // Get the last character and check if it's a magnitude suffix
    let last_char = s.chars().last()?;
    let multiplier = match last_char {
        'k' | 'K' => 1_000.0,
        'm' | 'M' => 1_000_000.0,
        'b' | 'B' => 1_000_000_000.0,
        't' | 'T' => 1_000_000_000_000.0,
        _ => return None,
    };

    // Parse the number part (everything except the last character)
    let num_str = &s[..s.len() - 1];
    if let Ok(num) = parse_f64(num_str.trim()) {
        return Some(num * multiplier);
    }

    None
}

/// Parse simple fractions: 1/2, 3/4, -1/4
/// Parse mixed fractions: 2 1/2, 3 3/4, -1 1/2
#[inline]
fn try_parse_fraction(s: &str) -> Option<f64> {
    let s = s.trim();

    // Must contain a slash to be a fraction
    if !s.contains('/') {
        return None;
    }

    // Check for mixed fraction (has space before the fraction part)
    if let Some(space_pos) = s.rfind(' ') {
        // Mixed fraction: "2 1/2" or "-1 1/2"
        let whole_part = s[..space_pos].trim();
        let fraction_part = s[space_pos + 1..].trim();

        if let (Ok(whole), Some(frac_value)) =
            (parse_f64(whole_part), parse_simple_fraction(fraction_part))
        {
            // Handle negative mixed fractions: -1 1/2 = -1.5, not -0.5
            if whole < 0.0 {
                return Some(whole - frac_value);
            } else {
                return Some(whole + frac_value);
            }
        }
    }

    // Simple fraction: "1/2", "3/4", "-1/4"
    parse_simple_fraction(s)
}

/// Parse a simple fraction like "1/2" or "3/4"
#[inline]
fn parse_simple_fraction(s: &str) -> Option<f64> {
    let (num_str, den_str) = s.split_once('/')?;

    let numerator: f64 = parse_f64(num_str.trim()).ok()?;
    let denominator: f64 = parse_f64(den_str.trim()).ok()?;

    if denominator == 0.0 {
        return None;
    }

    Some(numerator / denominator)
}

/// Parse radix numbers: hex (0x...), binary (0b...), octal (0o...)
#[inline]
fn try_parse_radix_number(s: &str) -> Option<f64> {
    let s = s.trim();

    // Handle negative prefix
    let (is_negative, num_str) = if let Some(rest) = s.strip_prefix('-') {
        (true, rest.trim())
    } else {
        (false, s)
    };

    let result = if let Some(hex) = num_str
        .strip_prefix("0x")
        .or_else(|| num_str.strip_prefix("0X"))
    {
        // Hexadecimal: 0x1A2B, 0xFF
        i64::from_str_radix(hex, 16).ok().map(|n| n as f64)
    } else if let Some(bin) = num_str
        .strip_prefix("0b")
        .or_else(|| num_str.strip_prefix("0B"))
    {
        // Binary: 0b1010, 0B1111
        i64::from_str_radix(bin, 2).ok().map(|n| n as f64)
    } else if let Some(oct) = num_str
        .strip_prefix("0o")
        .or_else(|| num_str.strip_prefix("0O"))
    {
        // Octal: 0o777, 0O755
        i64::from_str_radix(oct, 8).ok().map(|n| n as f64)
    } else {
        None
    };

    result.map(|n| if is_negative { -n } else { n })
}

/// Attempt to parse and normalize a date/datetime string to UTC
///
/// Supported formats (ISO-8601 and common variants):
///
/// **ISO-8601 Standard:**
/// - Date only: YYYY-MM-DD (e.g., "2024-01-15")
/// - Compact date: YYYYMMDD (e.g., "20240115")
/// - DateTime with T: YYYY-MM-DDTHH:MM:SS (e.g., "2024-01-15T10:30:00")
/// - Compact datetime: YYYYMMDDTHHMMSS (e.g., "20240115T103000")
/// - Fractional seconds: YYYY-MM-DDTHH:MM:SS.sss
/// - UTC suffix (Z): YYYY-MM-DDTHH:MM:SSZ
/// - Timezone offset: YYYY-MM-DDTHH:MM:SS+HH:MM or -HH:MM
/// - Compact offset: YYYY-MM-DDTHH:MM:SS+HHMM (no colon)
/// - Space separator: YYYY-MM-DD HH:MM:SS
/// - Ordinal date: YYYY-DDD (e.g., "2024-015" for Jan 15)
/// - Week date: YYYY-Www-D (e.g., "2024-W03-1" for Monday of week 3)
///
/// **Common Variants:**
/// - Slash separators: YYYY/MM/DD (e.g., "2024/01/15")
/// - Dot separators: YYYY.MM.DD (e.g., "2024.01.15")
/// - Time with offset no colon: +0530 or -0800
/// - Hour-only offset: +05 or -08
///
/// Returns Some(normalized_string) if valid date, None otherwise
/// Normalizes to UTC with Z suffix for datetime, keeps YYYY-MM-DD for date-only
#[inline]
fn try_parse_and_normalize_iso8601(s: &str) -> Option<String> {
    let trimmed = s.trim();
    let len = trimmed.len();

    // Quick rejection: minimum length is 8 for YYYYMMDD
    if len < 8 {
        return None;
    }

    let bytes = trimmed.as_bytes();
    let first_byte = bytes[0];

    // Must start with a digit (for year)
    if !first_byte.is_ascii_digit() {
        return None;
    }

    // Try compact date format first: YYYYMMDD (exactly 8 digits)
    // Year must start with 1 or 2 to be a plausible date (1000-2999)
    if len == 8 && matches!(first_byte, b'1' | b'2') && bytes.iter().all(|b| b.is_ascii_digit()) {
        return try_parse_compact_date(trimmed);
    }

    // Try compact datetime format: YYYYMMDDTHHMMSS or YYYYMMDDTHHMMSSZ
    if len >= 15 && bytes[8] == b'T' {
        if let Some(result) = try_parse_compact_datetime(trimmed) {
            return Some(result);
        }
    }

    // Ordinal date format: YYYY-DDD (8 chars with dash at position 4)
    if len == 8 && bytes[4] == b'-' {
        return try_parse_ordinal_date(trimmed);
    }

    // Week date format: YYYY-Www or YYYY-Www-D
    if len >= 8 && bytes[4] == b'-' && bytes[5] == b'W' {
        return try_parse_week_date(trimmed);
    }

    // Standard format detection: check for separators at expected positions
    // YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
    if len >= 10 {
        let sep = bytes[4];
        if (sep == b'-' || sep == b'/' || sep == b'.') && bytes[7] == sep {
            return try_parse_standard_date(trimmed, sep);
        }
    }

    None
}

/// Outcome of [`try_parse_and_normalize_iso8601_configured`].
enum DateMatch {
    /// Not recognized as a date/datetime at all -- caller should fall through to
    /// number parsing.
    NotADate,
    /// Recognized as a date/datetime, but the configured knobs mean it should be
    /// left byte-for-byte unchanged. Still counts as a match: the caller must NOT
    /// fall through to number parsing (a date string like `"20240115"` would
    /// otherwise be misread as the number `20240115`).
    Unchanged,
    /// Recognized as a date/datetime and normalized per the configured knobs.
    Normalized(String),
}

/// Detect whether a datetime string already carries explicit timezone info (a
/// trailing `Z`/`z`, or a `+`/`-` offset at one of the positions a full ISO-8601
/// timestamp's offset can appear in the separator-delimited formats, reusing the
/// exact position table `try_parse_with_offset_variants` itself scans -- or, for the
/// separator-free compact format, any `-` at an index past the fixed
/// `YYYYMMDDTHHMMSS` prefix, since compact dates/times never otherwise contain a
/// `-`). Pure detection, not extraction -- used only to decide which
/// [`DateConversionConfig`] knob (`normalize_to_utc` vs `assume_utc_for_naive`)
/// governs a given input, without duplicating the parsers themselves.
#[inline]
fn has_explicit_timezone(trimmed: &str) -> bool {
    let bytes = trimmed.as_bytes();
    if matches!(bytes.last(), Some(b'Z') | Some(b'z')) {
        return true;
    }
    if memchr(b'+', bytes).is_some() {
        return true;
    }
    let len = bytes.len();
    for pos in [16, 19, 22, 23, 26] {
        if pos < len && bytes[pos] == b'-' {
            return true;
        }
    }
    // Compact format (YYYYMMDDTHHMMSS...) has no separators at all before an
    // offset, so any '-' past the fixed 15-char prefix is an offset sign.
    if len > 15 && bytes[8] == b'T' && memchr(b'-', &bytes[15..]).is_some() {
        return true;
    }
    false
}

/// Configured variant of [`try_parse_and_normalize_iso8601`]: reuses the untouched
/// original parser entirely (no duplicated date-format logic), then decides what to
/// do with its result based on `cfg`. A recognized date/datetime whose normalized
/// form differs from the input is either kept (per [`DateConversionConfig::
/// normalize_to_utc`] for inputs with explicit timezone info, or
/// [`DateConversionConfig::assume_utc_for_naive`] for timezone-less inputs) or
/// reported as [`DateMatch::Unchanged`] -- which still blocks number-parsing
/// fallthrough, matching the always-on behavior documented on those two fields.
#[inline]
fn try_parse_and_normalize_iso8601_configured(s: &str, cfg: &DateConversionConfig) -> DateMatch {
    let trimmed = s.trim();
    match try_parse_and_normalize_iso8601(trimmed) {
        None => DateMatch::NotADate,
        Some(normalized) => {
            if normalized == trimmed {
                return DateMatch::Unchanged;
            }
            let allow_rewrite = if has_explicit_timezone(trimmed) {
                cfg.normalize_to_utc
            } else {
                cfg.assume_utc_for_naive
            };
            if allow_rewrite {
                DateMatch::Normalized(normalized)
            } else {
                DateMatch::Unchanged
            }
        }
    }
}

/// Parse `n` ASCII digit bytes into a `u32`. Caller guarantees the slice is all digits.
#[inline(always)]
fn digits_to_u32(bytes: &[u8]) -> u32 {
    bytes
        .iter()
        .fold(0u32, |acc, &b| acc * 10 + (b - b'0') as u32)
}

/// Format a UTC datetime as this crate's fixed normalized-datetime shape
/// (`YYYY-MM-DDTHH:MM:SSZ`) without going through `DateTime::format` --
/// chrono's generic formatter re-interprets the strftime-style format string
/// (via `StrftimeItems`) on every call, the same avoidable cost
/// `try_parse_compact_date` below already documents for the parse direction.
/// Every normalized-datetime output in this file uses this exact fixed
/// shape (never fractional seconds -- `%S` truncates them, matched here by
/// reading whole-second fields only), so a plain integer-formatted
/// `format!` is a direct, correct replacement, not an approximation.
#[inline]
fn format_utc_datetime_z(dt: DateTime<Utc>) -> String {
    format!(
        "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}Z",
        dt.year(),
        dt.month(),
        dt.day(),
        dt.hour(),
        dt.minute(),
        dt.second()
    )
}

/// Parse compact date format: YYYYMMDD
///
/// Hand-rolled instead of `NaiveDate::parse_from_str(s, "%Y%m%d")`: chrono's generic
/// parser re-interprets the format string on every call. `could_be_date`'s prefilter
/// can't distinguish a real compact date from an 8-digit numeric ID/zip+4/order number
/// starting with 1 or 2 (a very common shape once `auto_convert_types` is enabled), so
/// this function is reached for plenty of non-dates -- `NaiveDate::from_ymd_opt` is a
/// direct, cheap validator (no string re-scanning) and correctly rejects those the same
/// way the format-string parser would (invalid month/day, non-leap Feb 29, etc.).
#[inline]
fn try_parse_compact_date(s: &str) -> Option<String> {
    let bytes = s.as_bytes();
    let year = digits_to_u32(&bytes[0..4]);
    let month = digits_to_u32(&bytes[4..6]);
    let day = digits_to_u32(&bytes[6..8]);
    NaiveDate::from_ymd_opt(year as i32, month, day)?;
    Some(format!("{year:04}-{month:02}-{day:02}"))
}

/// Parse compact datetime format: YYYYMMDDTHHMMSS with optional Z or offset
#[inline]
fn try_parse_compact_datetime(s: &str) -> Option<String> {
    let bytes = s.as_bytes();
    let len = s.len();

    // Basic format: YYYYMMDDTHHMMSS (15 chars)
    // With Z: YYYYMMDDTHHMMSSZ (16 chars)
    // With offset: YYYYMMDDTHHMMSS+HHMM (20 chars) or +HH:MM (21 chars)

    // Try with Z suffix
    if len == 16 && bytes[15] == b'Z' {
        if let Ok(naive) = NaiveDateTime::parse_from_str(&s[..15], "%Y%m%dT%H%M%S") {
            let utc = naive.and_utc();
            return Some(format_utc_datetime_z(utc));
        }
    }

    // Try with offset (+HHMM or -HHMM)
    if len >= 19 && (bytes[15] == b'+' || bytes[15] == b'-') {
        // Convert to ISO format and parse
        let date_part = &s[0..8];
        let time_part = &s[9..15];
        let offset_part = &s[15..];

        // Format offset properly. `is_char_boundary(3)` guards the slice below --
        // a multi-byte UTF-8 character straddling byte offset 3 (e.g. an offset
        // of "+1Á2") would otherwise panic here. A real +HHMM offset is always
        // pure ASCII, so failing the check just means this isn't a valid offset;
        // the malformed string falls through to `parse_from_rfc3339` below and
        // is correctly rejected as not a date, instead of panicking.
        let formatted_offset = if offset_part.len() == 5 && offset_part.is_char_boundary(3) {
            // +HHMM -> +HH:MM
            format!("{}:{}", &offset_part[..3], &offset_part[3..])
        } else {
            offset_part.to_string()
        };

        let iso_str = format!(
            "{}-{}-{}T{}:{}:{}{}",
            &date_part[0..4],
            &date_part[4..6],
            &date_part[6..8],
            &time_part[0..2],
            &time_part[2..4],
            &time_part[4..6],
            formatted_offset
        );

        if let Ok(dt) = DateTime::parse_from_rfc3339(&iso_str) {
            let utc: DateTime<Utc> = dt.into();
            return Some(format_utc_datetime_z(utc));
        }
    }

    // Try basic compact format (assume UTC)
    if len == 15 {
        if let Ok(naive) = NaiveDateTime::parse_from_str(s, "%Y%m%dT%H%M%S") {
            let utc = naive.and_utc();
            return Some(format_utc_datetime_z(utc));
        }
    }

    None
}

/// Parse ordinal date format: YYYY-DDD
///
/// Hand-rolled for the same reason as `try_parse_compact_date`; ordinal-to-month/day
/// conversion (leap-year-aware) is left to `NaiveDate`'s getters rather than
/// re-implemented, since that's the part actually worth trusting chrono for.
#[inline]
fn try_parse_ordinal_date(s: &str) -> Option<String> {
    let bytes = s.as_bytes();
    if !bytes[0..4].iter().all(|b| b.is_ascii_digit())
        || !bytes[5..8].iter().all(|b| b.is_ascii_digit())
    {
        return None;
    }
    let year = digits_to_u32(&bytes[0..4]);
    let ordinal = digits_to_u32(&bytes[5..8]);
    let date = NaiveDate::from_yo_opt(year as i32, ordinal)?;
    Some(format!(
        "{:04}-{:02}-{:02}",
        date.year(),
        date.month(),
        date.day()
    ))
}

/// Parse ISO week date format: YYYY-Www or YYYY-Www-D
#[inline]
fn try_parse_week_date(s: &str) -> Option<String> {
    // YYYY-Www (8 chars) - Monday of that week
    // YYYY-Www-D (10 chars) - specific day
    let formats = ["%G-W%V-%u", "%G-W%V"];

    for fmt in &formats {
        if let Ok(d) = NaiveDate::parse_from_str(s, fmt) {
            return Some(format!("{:04}-{:02}-{:02}", d.year(), d.month(), d.day()));
        }
    }
    None
}

/// Parse standard date formats with various separators
#[inline]
fn try_parse_standard_date(s: &str, sep: u8) -> Option<String> {
    let bytes = s.as_bytes();
    let len = s.len();

    // Normalize to dashes for parsing
    let normalized: Cow<'_, str> = if sep != b'-' {
        let sep_char = sep as char;
        Cow::Owned(s.replace(sep_char, "-"))
    } else {
        Cow::Borrowed(s)
    };

    // Validate basic structure: YYYY-MM-DD
    if len >= 10
        && (!bytes[0..4].iter().all(|b| b.is_ascii_digit())
            || !bytes[5..7].iter().all(|b| b.is_ascii_digit())
            || !bytes[8..10].iter().all(|b| b.is_ascii_digit()))
    {
        return None;
    }

    // Date-only (exactly 10 chars). Hand-rolled for the same reason as
    // try_parse_compact_date: positions 0..4, 5..7, 8..10 are already confirmed all
    // ASCII digits above, so NaiveDate::from_ymd_opt validates just as correctly as
    // the format-string parser without re-scanning the string a second time. The
    // original (already-normalized, separator-unified) string is returned unchanged
    // on success -- this call only needs to validate, not reformat.
    if len == 10 {
        let year = digits_to_u32(&bytes[0..4]);
        let month = digits_to_u32(&bytes[5..7]);
        let day = digits_to_u32(&bytes[8..10]);
        NaiveDate::from_ymd_opt(year as i32, month, day)?;
        return Some(normalized.into_owned());
    }

    // Must have datetime separator at position 10 (T or space)
    if len < 11 {
        return None;
    }
    let datetime_sep = bytes[10];
    if datetime_sep != b'T' && datetime_sep != b' ' {
        return None;
    }

    // Normalize datetime separator to T
    let normalized = if datetime_sep == b' ' {
        let mut s = normalized.into_owned();
        // Safe because position 10 is single-byte ASCII
        unsafe {
            s.as_bytes_mut()[10] = b'T';
        }
        Cow::Owned(s)
    } else {
        normalized
    };

    // Try RFC3339 first (handles timezone)
    if let Ok(dt) = DateTime::parse_from_rfc3339(&normalized) {
        let utc: DateTime<Utc> = dt.into();
        return Some(format_utc_datetime_z(utc));
    }

    // Try parsing with various timezone offset formats
    if let Some(result) = try_parse_with_offset_variants(&normalized) {
        return Some(result);
    }

    // Handle Z suffix for formats without full seconds (e.g., "2024-01-15T10:30Z")
    let time_part = normalized.strip_suffix('Z').unwrap_or(normalized.as_ref());

    // Try naive datetime formats
    let naive_formats = [
        "%Y-%m-%dT%H:%M:%S%.f", // With fractional seconds
        "%Y-%m-%dT%H:%M:%S",    // Standard
        "%Y-%m-%dT%H:%M",       // Without seconds
        "%Y-%m-%dT%H",          // Hour only
    ];

    for fmt in &naive_formats {
        if let Ok(naive_dt) = NaiveDateTime::parse_from_str(time_part, fmt) {
            // Always output as UTC (Z suffix)
            let utc_dt = naive_dt.and_utc();
            return Some(format_utc_datetime_z(utc_dt));
        }
    }

    None
}

/// Try parsing datetime with various timezone offset formats
#[inline]
fn try_parse_with_offset_variants(s: &str) -> Option<String> {
    let len = s.len();
    if len < 14 {
        return None;
    }

    // Look for offset indicator (+/-) after time portion
    // Minimum position: YYYY-MM-DDTHH:MM+... = position 16
    // Or: YYYY-MM-DDTHH:MM:SS+... = position 19

    for pos in [16, 19, 22, 23, 26] {
        if pos >= len {
            continue;
        }
        let byte = s.as_bytes()[pos];
        if byte == b'+' || byte == b'-' {
            let offset_part = &s[pos..];
            let time_part = &s[..pos];

            // Try to normalize offset
            if let Some(normalized_offset) = normalize_offset(offset_part) {
                let full = format!("{}{}", time_part, normalized_offset);
                if let Ok(dt) = DateTime::parse_from_rfc3339(&full) {
                    let utc: DateTime<Utc> = dt.into();
                    return Some(format_utc_datetime_z(utc));
                }
            }
        }
    }

    None
}

/// Normalize timezone offset to RFC3339 format (+HH:MM or -HH:MM)
#[inline]
fn normalize_offset(offset: &str) -> Option<String> {
    let bytes = offset.as_bytes();
    let len = bytes.len();

    if len < 2 {
        return None;
    }

    let sign = bytes[0];
    if sign != b'+' && sign != b'-' {
        return None;
    }

    let sign_char = sign as char;
    let rest = &offset[1..];

    match rest.len() {
        // +HH -> +HH:00
        2 if rest.as_bytes().iter().all(|b| b.is_ascii_digit()) => {
            Some(format!("{}{}:00", sign_char, rest))
        }
        // +HHMM -> +HH:MM
        4 if rest.as_bytes().iter().all(|b| b.is_ascii_digit()) => {
            Some(format!("{}{}:{}", sign_char, &rest[..2], &rest[2..]))
        }
        // +HH:MM -> already correct
        5 if rest.as_bytes()[2] == b':' => Some(offset.to_string()),
        _ => None,
    }
}

/// Check if a string looks like it could be a date (fast pre-filter)
/// Used to avoid expensive parsing for obviously non-date strings
#[inline(always)]
fn could_be_date(s: &str) -> bool {
    let len = s.len();
    // Minimum 8 chars for YYYYMMDD or YYYY-DDD
    if len < 8 {
        return false;
    }

    let bytes = s.as_bytes();

    // First 4 chars must be digits (year)
    if !bytes[0..4].iter().all(|b| b.is_ascii_digit()) {
        return false;
    }

    // Check for various date patterns:
    // YYYYMMDD (compact), YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD, YYYY-DDD, YYYY-Www
    let fifth = bytes[4];
    match fifth {
        // Compact format: next char is also a digit
        b'0'..=b'9' => len == 8 || (len >= 15 && bytes[8] == b'T'),
        // Standard separators - len 8 for YYYY-DDD ordinal, >= 10 for YYYY-MM-DD
        b'-' | b'/' | b'.' => len >= 8,
        _ => false,
    }
}

/// Strip all trailing occurrences of a fixed 2-byte ASCII suffix, matching
/// `s.trim_end_matches("xy")`'s exact semantics (repeats until the suffix no
/// longer matches) without going through std's generic `Pattern`/`StrSearcher`
/// machinery -- see the call site's comment for why that matters here.
#[inline]
fn strip_trailing_ascii_pair(s: &str, pair: [u8; 2]) -> &str {
    let mut s = s;
    while s.len() >= 2
        && s.as_bytes()[s.len() - 2] == pair[0]
        && s.as_bytes()[s.len() - 1] == pair[1]
    {
        s = &s[..s.len() - 2];
    }
    s
}

/// Clean a number string by removing common formatting characters
/// Handles: currencies, thousands separators, negative formats, and more
/// Supports: $, EUR, GBP, JPY, INR, RUB, KRW, TRY, BRL, AUD, CAD, CHF, SEK, PLN, CZK codes
/// Negative formats: -123, (123), [123], 123-, 123 CR/DR
/// Separators: comma, dot, space, apostrophe, underscore
/// Optimized with single-pass filtering and comprehensive format detection
/// OPTIMIZATION: Returns Cow to avoid allocation when number is already clean
#[inline(always)] // Called per-value during type conversion; force inline to avoid call overhead
pub(crate) fn clean_number_string(s: &str) -> Cow<'_, str> {
    let (is_negative, working_str) = match strip_sign(s) {
        None => return Cow::Borrowed(""),
        Some(SignStrip::AlreadyClean(trimmed)) => return Cow::Borrowed(trimmed),
        Some(SignStrip::Stripped {
            is_negative,
            working_str,
            ..
        }) => (is_negative, working_str),
    };

    let without_currency = strip_currency_indicators(working_str);

    clean_number_core(without_currency, is_negative)
}

/// Configured variant of [`clean_number_string`]: thousands-separator cleanup and
/// negative-sign handling always apply; currency symbol/code/credit-debit-suffix
/// stripping is skipped entirely when `currency` is false.
#[inline]
fn clean_number_string_configured(s: &str, currency: bool) -> Cow<'_, str> {
    let (is_negative, working_str) = match strip_sign(s) {
        None => return Cow::Borrowed(""),
        Some(SignStrip::AlreadyClean(trimmed)) => return Cow::Borrowed(trimmed),
        Some(SignStrip::Stripped {
            is_negative,
            working_str,
            ..
        }) => (is_negative, working_str),
    };

    let without_currency = if currency {
        strip_currency_indicators(working_str)
    } else {
        working_str
    };

    clean_number_core(without_currency, is_negative)
}

/// Result of [`strip_sign`]'s negative/leading-plus handling.
enum SignStrip<'a> {
    /// Already in canonical number form -- return as-is (borrowed, no allocation).
    AlreadyClean(&'a str),
    /// Sign indicators stripped; ready for currency/separator cleanup.
    Stripped {
        is_negative: bool,
        working_str: &'a str,
    },
}

/// Trim, fast-path-detect already-clean numbers, and strip negative-format/leading-
/// plus indicators. Shared by [`clean_number_string`] and
/// [`clean_number_string_configured`] -- identical in both (sign handling isn't
/// gated by any `NumberConversionConfig` field). Returns `None` for empty input
/// (caller should return `Cow::Borrowed("")`).
#[inline(always)]
fn strip_sign(s: &str) -> Option<SignStrip<'_>> {
    let trimmed = s.trim();

    if trimmed.is_empty() {
        return None;
    }

    // OPTIMIZATION: Fast path for already-clean numbers (10-30% speedup)
    // Check if string only contains valid number characters AND has proper format
    let is_clean = trimmed.bytes().all(|b| matches!(b, b'0'..=b'9' | b'.' | b'-' | b'+' | b'e' | b'E'))
        && !trimmed.ends_with('-')  // Trailing minus needs processing
        && !trimmed.starts_with('+'); // Leading plus needs removal
    if is_clean {
        return Some(SignStrip::AlreadyClean(trimmed));
    }

    // Detect negative number formats
    let is_negative = trimmed.starts_with('-')
        || trimmed.starts_with('(') && trimmed.ends_with(')') // Accounting format: (123.45)
        || trimmed.starts_with('[') && trimmed.ends_with(']') // Bracket format: [123.45]
        || trimmed.ends_with('-'); // Trailing minus: 123.45-

    // Remove negative indicators temporarily for processing
    let working_str = if is_negative {
        // Handle bracketed negatives: (123) or [123]
        if let Some(s) = trimmed.strip_prefix('(').and_then(|s| s.strip_suffix(')')) {
            s
        } else if let Some(s) = trimmed.strip_prefix('[').and_then(|s| s.strip_suffix(']')) {
            s
        } else if let Some(s) = trimmed.strip_suffix('-') {
            // Handle trailing minus: 123-
            s
        } else {
            // Remove leading minus
            &trimmed[1..]
        }
    } else {
        trimmed
    }
    .trim();

    // Remove leading plus sign if present
    let working_str = working_str.strip_prefix('+').unwrap_or(working_str).trim();

    Some(SignStrip::Stripped {
        is_negative,
        working_str,
    })
}

/// Remove currency symbols and codes and credit/debit suffixes.
/// Extended currency support: $, EUR, GBP, JPY, INR, RUB, KRW, TRY, BRL, AUD, CAD, CHF, SEK, PLN, CZK
///
/// Extracted from `clean_number_string` so it can be conditionally skipped by
/// `clean_number_string_configured` (when `NumberConversionConfig::currency` is
/// false) while `clean_number_string` itself keeps calling it unconditionally --
/// `#[inline(always)]` so this extraction doesn't add call overhead to the existing
/// hot path.
#[inline(always)]
fn strip_currency_indicators(working_str: &str) -> &str {
    let mut without_currency = working_str;

    // Remove multi-character currency prefixes first (R$, A$, C$, AU$, CA$, US$)
    if without_currency.len() > 2 {
        if let Some(rest) = without_currency
            .strip_prefix("R$")
            .or_else(|| without_currency.strip_prefix("A$"))
            .or_else(|| without_currency.strip_prefix("C$"))
            .or_else(|| without_currency.strip_prefix("AU$"))
            .or_else(|| without_currency.strip_prefix("CA$"))
            .or_else(|| without_currency.strip_prefix("US$"))
            .or_else(|| without_currency.strip_prefix("Fr"))
            .or_else(|| without_currency.strip_prefix("kr"))
            .or_else(|| without_currency.strip_prefix("z\u{142}"))
            .or_else(|| without_currency.strip_prefix("K\u{10d}"))
        {
            without_currency = rest.trim();
        }
    }

    // Remove single-character currency symbols from start
    without_currency = without_currency
        .trim_start_matches(
            &[
                '$', '\u{20ac}', '\u{00a3}', '\u{00a5}', '\u{20b9}', '\u{20bd}', '\u{20a9}',
                '\u{20ba}',
            ][..],
        )
        .trim();

    // Remove currency codes (USD, EUR, GBP, etc.) - 3 letter codes at start
    // Only remove if followed by a space to avoid false positives like "ABC123"
    // `is_char_boundary(3)` guards the slice below: a multi-byte UTF-8 character
    // straddling byte offset 3 (e.g. "5xÁ1000") would otherwise panic here -- a
    // real production crash, not a hypothetical (see the regression tests). A
    // real 3-letter currency code is always pure ASCII, so byte offset 3 is
    // guaranteed a valid boundary for every genuine match; failing the check
    // just means "not a currency-code prefix", which is the correct outcome.
    if without_currency.len() > 4 && without_currency.is_char_boundary(3) {
        let first_three = &without_currency[..3];
        if first_three.bytes().all(|b| b.is_ascii_uppercase()) {
            let potential_code = &without_currency[3..];
            // Only strip if followed by space (USD 123, EUR 45.67)
            if potential_code.starts_with(' ') {
                without_currency = potential_code.trim();
            }
        }
    }

    // Remove trailing currency indicators and credit/debit markers
    without_currency = without_currency.trim_end_matches(
        &[
            '$', '\u{20ac}', '\u{00a3}', '\u{00a5}', '\u{20b9}', '\u{20bd}', '\u{20a9}', '\u{20ba}',
        ][..],
    );
    // Hand-rolled instead of chained `.trim_end_matches("CR")` etc.: a `&str` pattern
    // makes std construct a generic `StrSearcher` (the same machinery used for
    // arbitrary substring search) on every call, which is wasteful overhead for a
    // fixed 2-byte suffix check. Validated with an isolated benchmark before
    // adopting: ~20-28x faster. Kept as 4 sequential exhaustive-strip passes (not one
    // combined loop) to match `trim_end_matches`'s exact semantics: each call strips
    // *all* trailing repeats of its own pattern before the next pattern is tried, so
    // e.g. "CRDR" strips only the trailing "DR" (leaving "CR", which the later
    // lowercase-only "cr"/"dr" passes don't match) -- a combined loop checking all
    // four patterns each iteration would strip both and give a different result.
    without_currency = strip_trailing_ascii_pair(without_currency, *b"CR"); // Credit
    without_currency = strip_trailing_ascii_pair(without_currency, *b"DR"); // Debit
    without_currency = strip_trailing_ascii_pair(without_currency, *b"cr");
    without_currency = strip_trailing_ascii_pair(without_currency, *b"dr");
    without_currency.trim()
}

/// Thousands-separator cleanup and negative-sign handling, applied after currency
/// stripping (or after skipping it, when `NumberConversionConfig::currency` is
/// false). Extracted from `clean_number_string` so `clean_number_string_configured`
/// can share it -- this part of the cleanup is always-on "core" behavior, never
/// gated by any `NumberConversionConfig` field. `#[inline(always)]` so this
/// extraction doesn't add call overhead to the existing hot path.
#[inline(always)]
fn clean_number_core(without_currency: &str, is_negative: bool) -> Cow<'_, str> {
    // Early exit for simple cases (no special characters)
    // SIMD: 2 SIMD passes (memchr3 + memchr2) are faster than std::str::contains with a char slice
    {
        let b = without_currency.as_bytes();
        if memchr3(b',', b'.', b' ', b).is_none() && memchr2(b'\'', b'_', b).is_none() {
            return if is_negative {
                Cow::Owned(format!("-{}", without_currency))
            } else {
                Cow::Owned(without_currency.to_string())
            };
        }
    }

    // SIMD byte scan: compute last_comma_pos, last_dot_pos, comma_count, dot_count
    // memchr_iter uses AVX2/SSE2/NEON to process 32+ bytes per cycle -- faster than
    // a sequential single-pass loop for inputs where SIMD amortizes the call overhead.
    let bytes = without_currency.as_bytes();
    let (last_comma_pos, comma_count) =
        memchr_iter(b',', bytes).fold((None, 0usize), |(_, c), pos| (Some(pos), c + 1));
    let (last_dot_pos, dot_count) =
        memchr_iter(b'.', bytes).fold((None, 0usize), |(_, c), pos| (Some(pos), c + 1));

    // Stack-allocated buffer for short numbers (most are under 64 bytes),
    // avoiding heap allocation entirely
    let mut buffer: SmallVec<[u8; 64]> = SmallVec::new();

    // Add negative sign if needed
    if is_negative {
        buffer.push(b'-');
    }

    match (last_comma_pos, last_dot_pos, comma_count, dot_count) {
        // Both comma and dot present
        (Some(comma_pos), Some(dot_pos), _, _) => {
            if dot_pos > comma_pos {
                // US format: 1,234.56 - keep dot, remove commas and separators
                // SIMD: find skip bytes with memchr3+memchr, bulk-copy clean segments
                extend_skipping_4(&mut buffer, bytes, b',', b' ', b'\'', b'_');
            } else {
                // European format: 1.234,56 - remove dots, then convert commas to dots
                // Phase 1: copy all except '.', ' ', '\'', '_'  (commas kept)
                extend_skipping_4(&mut buffer, bytes, b'.', b' ', b'\'', b'_');
                // Phase 2: convert decimal commas to dots (auto-vectorized by LLVM)
                for b in buffer.iter_mut() {
                    if *b == b',' {
                        *b = b'.';
                    }
                }
            }
        }
        // Only comma present
        (Some(_), None, 1, 0) => {
            // Single comma - likely decimal separator (European format: 12,34)
            // Phase 1: copy all except ' ', '\'', '_'  (comma kept)
            extend_skipping_3(&mut buffer, bytes, b' ', b'\'', b'_');
            // Phase 2: convert the single decimal comma to a dot
            for b in buffer.iter_mut() {
                if *b == b',' {
                    *b = b'.';
                }
            }
        }
        (Some(_), None, _, 0) => {
            // Multiple commas - could be:
            // 1. US format thousands separators: 1,234,567 (3-digit groups)
            // 2. Indian numbering system: 1,00,000 (lakhs) or 1,00,00,000 (crores)
            let segments: SmallVec<[&str; 8]> = without_currency.split(',').collect();

            // Check US format: all segments after first have exactly 3 digits
            let is_us_thousands = segments.len() > 1
                && segments[1..]
                    .iter()
                    .all(|seg| seg.len() == 3 && seg.bytes().all(|b| b.is_ascii_digit()));

            // Check Indian format: first segment 1-3 digits, then 2-digit groups, last 3 digits
            // Examples: 1,00,000 (1 lakh) -> [1, 00, 000]
            //           12,34,567 -> [12, 34, 567]
            //           1,23,45,678 -> [1, 23, 45, 678]
            let is_indian_format = segments.len() >= 2 && {
                let last_seg = segments
                    .last()
                    .expect("segments non-empty: len >= 2 checked above");
                let middle_segs = &segments[1..segments.len() - 1];

                // Last segment must be 3 digits (or 2 for lakhs like 1,00,000)
                let last_valid = (last_seg.len() == 3 || last_seg.len() == 2)
                    && last_seg.bytes().all(|b| b.is_ascii_digit());

                // Middle segments (if any) must be 2 digits
                let middle_valid = middle_segs
                    .iter()
                    .all(|seg| seg.len() == 2 && seg.bytes().all(|b| b.is_ascii_digit()));

                // First segment can be 1-3 digits
                let first_valid = !segments[0].is_empty()
                    && segments[0].len() <= 3
                    && segments[0].bytes().all(|b| b.is_ascii_digit());

                first_valid && middle_valid && last_valid
            };

            if is_us_thousands || is_indian_format {
                // Valid thousands separators - remove commas
                // SIMD: bulk-copy digit segments between separator positions
                extend_skipping_4(&mut buffer, bytes, b',', b' ', b'\'', b'_');
            } else {
                // Invalid format (like "12,34,56") - keep as-is and let it fail to parse
                return Cow::Owned(without_currency.to_string());
            }
        }
        // Only dot present (multiple dots means thousands separators in EU format)
        (None, Some(_), 0, count) if count > 1 => {
            // Multiple dots - could be thousands separators (European format: 1.234.567)
            // But need to validate the format - dots should be every 3 digits from right
            // Split by dots and check if all segments (except first) have 3 digits
            let segments: SmallVec<[&str; 8]> = without_currency.split('.').collect();
            let is_valid_thousands = segments.len() > 1
                && segments[1..]
                    .iter()
                    .all(|seg| seg.len() == 3 && seg.bytes().all(|b| b.is_ascii_digit()));

            if is_valid_thousands {
                // Valid thousands separators - remove dots
                // SIMD: bulk-copy digit segments between dot positions
                extend_skipping_4(&mut buffer, bytes, b'.', b' ', b'\'', b'_');
            } else {
                // Invalid format (like "12.34.56") - keep as-is and let it fail to parse
                return Cow::Owned(without_currency.to_string());
            }
        }
        // Default case: just remove spaces, apostrophes, and underscores
        _ => {
            // SIMD: memchr3 finds skip positions, extend_from_slice bulk-copies segments
            extend_skipping_3(&mut buffer, bytes, b' ', b'\'', b'_');
        }
    }

    // Convert SmallVec buffer to String - this is safe because we only pushed ASCII bytes
    // SAFETY: buffer only contains ASCII digits, '.', '-', 'e', 'E' which are valid UTF-8
    Cow::Owned(unsafe { String::from_utf8_unchecked(buffer.into_vec()) })
}

#[inline(always)]
fn try_parse_bool(s: &str) -> Option<bool> {
    match s {
        "true" | "TRUE" | "True" | "yes" | "YES" | "Yes" | "y" | "Y" | "on" | "ON" | "On" => {
            Some(true)
        }
        "false" | "FALSE" | "False" | "no" | "NO" | "No" | "n" | "N" | "off" | "OFF" | "Off" => {
            Some(false)
        }
        _ => None,
    }
}

/// Fast version that accepts already-trimmed string (no trim() overhead)
#[inline(always)]
fn is_null_string(s: &str) -> bool {
    matches!(
        s,
        "null"
            | "NULL"
            | "Null"
            | "nil"
            | "NIL"
            | "Nil"
            | "none"
            | "NONE"
            | "None"
            | "N/A"
            | "n/a"
            | "NA"
            | "na"
    )
}

/// Configured variant of [`try_parse_bool`]: checks the built-in list first, then any
/// caller-supplied extra tokens.
#[inline]
fn try_parse_bool_configured(s: &str, cfg: &BooleanConversionConfig) -> Option<bool> {
    if let Some(b) = try_parse_bool(s) {
        return Some(b);
    }
    if cfg.extra_true_tokens.iter().any(|t| t == s) {
        return Some(true);
    }
    if cfg.extra_false_tokens.iter().any(|t| t == s) {
        return Some(false);
    }
    None
}

/// Configured variant of [`is_null_string`]: checks the built-in list first, then any
/// caller-supplied extra tokens.
#[inline]
fn is_null_string_configured(s: &str, cfg: &NullConversionConfig) -> bool {
    is_null_string(s) || cfg.extra_tokens.iter().any(|t| t == s)
}

/// Try to convert a string value to its native JSON representation.
/// Returns `Some(json_bytes)` if the string can be converted (e.g., "123" → "123", "true" → "true",
/// "null" → "null"), or `None` if the string should remain as-is.
/// The returned string is valid JSON (NOT quoted — e.g., `123` not `"123"`).
#[inline]
pub(crate) fn try_convert_string_to_json_bytes(s: &str) -> Option<Cow<'_, str>> {
    if s.is_empty() {
        return None;
    }

    let trimmed = s.trim();
    if trimmed.is_empty() {
        return None;
    }

    let first_byte = trimmed.as_bytes()[0];
    match first_byte {
        // Null patterns
        b'n' | b'N' => {
            if is_null_string(trimmed) {
                return Some(Cow::Borrowed("null"));
            }
            if let Some(b) = try_parse_bool(trimmed) {
                return Some(Cow::Borrowed(if b { "true" } else { "false" }));
            }
            None
        }
        // Boolean patterns
        b't' | b'T' | b'f' | b'F' | b'y' | b'Y' | b'o' | b'O' => {
            try_parse_bool(trimmed).map(|b| Cow::Borrowed(if b { "true" } else { "false" }))
        }
        // Number/date patterns
        b'0'..=b'9' | b'-' | b'+' | b'.' | b'$' | b'(' | b'[' => {
            // Boolean for "0", "1"
            if first_byte == b'0' || first_byte == b'1' {
                if let Some(b) = try_parse_bool(trimmed) {
                    return Some(Cow::Borrowed(if b { "true" } else { "false" }));
                }
            }
            // Date detection before number
            if could_be_date(trimmed) {
                if let Some(normalized_date) = try_parse_and_normalize_iso8601(trimmed) {
                    if normalized_date != trimmed {
                        // Return as JSON string (quoted)
                        return Some(Cow::Owned(format!("\"{}\"", normalized_date)));
                    }
                    return None; // Date but no normalization needed — keep original
                }
            }
            // Number conversion -- fast path first (see `canonical_json_integer`'s
            // doc comment): skips the float round-trip entirely for the common case.
            if let Some(fast) = canonical_json_integer(trimmed) {
                return Some(Cow::Borrowed(fast));
            }
            if let Some(num) = try_parse_number(trimmed) {
                return f64_to_json_bytes(num);
            }
            None
        }
        // Currency codes
        b'A'..=b'Z' | b'\xc2'..=b'\xf4' => {
            if let Some(num) = try_parse_number(trimmed) {
                return f64_to_json_bytes(num);
            }
            None
        }
        _ => None,
    }
}

/// Configured variant of [`try_convert_string_to_json_bytes`]: mirrors its exact
/// byte-dispatch structure and dates -> nulls -> booleans -> numbers priority order,
/// but each category is short-circuited when disabled, and each category's own
/// `_configured` helper is used so per-category customization (extra null/boolean
/// tokens, date UTC-normalization knobs, number sub-format toggles) takes effect.
///
/// Extra null/boolean tokens can start with any byte (unlike the built-in lists,
/// which the byte-dispatch below is shaped around), so they're re-checked in a
/// fallback pass at the end regardless of which arm above ran -- cheap even when
/// redundant with an arm's own built-in-list check (a handful of string-literal
/// comparisons).
#[inline]
pub(crate) fn try_convert_string_to_json_bytes_configured<'a>(
    s: &'a str,
    cfg: &TypeConversionConfig,
) -> Option<Cow<'a, str>> {
    if s.is_empty() {
        return None;
    }

    let trimmed = s.trim();
    if trimmed.is_empty() {
        return None;
    }

    let first_byte = trimmed.as_bytes()[0];
    let result: Option<Cow<'a, str>> = match first_byte {
        // Null patterns
        b'n' | b'N' => {
            if cfg.nulls.enabled && is_null_string(trimmed) {
                Some(Cow::Borrowed("null"))
            } else if cfg.booleans.enabled {
                try_parse_bool(trimmed).map(|b| Cow::Borrowed(if b { "true" } else { "false" }))
            } else {
                None
            }
        }
        // Boolean patterns
        b't' | b'T' | b'f' | b'F' | b'y' | b'Y' | b'o' | b'O' => {
            if cfg.booleans.enabled {
                try_parse_bool(trimmed).map(|b| Cow::Borrowed(if b { "true" } else { "false" }))
            } else {
                None
            }
        }
        // Number/date patterns
        b'0'..=b'9' | b'-' | b'+' | b'.' | b'$' | b'(' | b'[' => {
            // Boolean for "0", "1"
            if cfg.booleans.enabled && (first_byte == b'0' || first_byte == b'1') {
                if let Some(b) = try_parse_bool(trimmed) {
                    return Some(Cow::Borrowed(if b { "true" } else { "false" }));
                }
            }
            // Date detection before number
            if cfg.dates.enabled && could_be_date(trimmed) {
                match try_parse_and_normalize_iso8601_configured(trimmed, &cfg.dates) {
                    DateMatch::Normalized(normalized) => {
                        return Some(Cow::Owned(format!("\"{}\"", normalized)));
                    }
                    DateMatch::Unchanged => return None,
                    DateMatch::NotADate => {}
                }
            }
            if cfg.numbers.enabled {
                if let Some(fast) = canonical_json_integer(trimmed) {
                    Some(Cow::Borrowed(fast))
                } else {
                    try_parse_number_configured(trimmed, &cfg.numbers).and_then(f64_to_json_bytes)
                }
            } else {
                None
            }
        }
        // Currency codes
        b'A'..=b'Z' | b'\xc2'..=b'\xf4' => {
            if cfg.numbers.enabled {
                try_parse_number_configured(trimmed, &cfg.numbers).and_then(f64_to_json_bytes)
            } else {
                None
            }
        }
        _ => None,
    };
    if result.is_some() {
        return result;
    }

    if cfg.nulls.enabled && is_null_string_configured(trimmed, &cfg.nulls) {
        return Some(Cow::Borrowed("null"));
    }
    if cfg.booleans.enabled {
        if let Some(b) = try_parse_bool_configured(trimmed, &cfg.booleans) {
            return Some(Cow::Borrowed(if b { "true" } else { "false" }));
        }
    }
    None
}

/// Central dispatch used by all per-string call sites in `flatten.rs`/
/// `unflatten.rs`/`transform.rs`: routes to the untouched original fast-path
/// function for `AllDefault` (zero behavior/perf change from before per-category
/// config existed), the configured function for `Custom`, and returns `None`
/// immediately for `Disabled` (defensive -- callers already guard on `mode !=
/// Disabled` before reaching here on the hot path, but this keeps the function
/// total). `#[inline]` so this adds no call overhead beyond the match itself.
#[inline]
pub(crate) fn convert_string_for_mode<'a>(
    s: &'a str,
    mode: TypeConversionMode,
    cfg: &TypeConversionConfig,
) -> Option<Cow<'a, str>> {
    match mode {
        TypeConversionMode::Disabled => None,
        TypeConversionMode::AllDefault => try_convert_string_to_json_bytes(s),
        TypeConversionMode::Custom => try_convert_string_to_json_bytes_configured(s, cfg),
    }
}

/// i64::MIN's magnitude (2^63) and u64::MAX as digit strings -- used to
/// bounds-check 19- and 20-digit integers exactly, where digit count alone can't
/// decide whether the value fits (see `canonical_json_integer`). A 19-digit
/// negative number needs `I64_MIN_MAGNITUDE` (i64 is the only signed option);
/// a 19-digit positive number always fits `u64` (whose max is 20 digits) so
/// needs no comparison; a 20-digit positive number needs `U64_MAX_DIGITS`.
const I64_MIN_MAGNITUDE: &[u8] = b"9223372036854775808";
const U64_MAX_DIGITS: &[u8] = b"18446744073709551615";

/// Returns `Some(s)` unchanged when `s` is already the exact canonical JSON
/// integer we would otherwise reconstruct via a full float round-trip
/// (`try_parse_number` + `f64_to_json_bytes`): an optional leading '-', no
/// leading zeros (other than a bare "0"), digits only, and exactly
/// representable as an i64 or u64 (checked precisely below rather than via a
/// blanket digit-count cutoff, so this covers the *entire* range the float
/// round-trip claims to support).
///
/// This isn't just a speed optimization: `f64` only has ~15-17 significant
/// decimal digits of exact precision, so the float round-trip silently
/// corrupts the last few digits of any exact i64/u64-representable integer
/// string longer than that (e.g. "999999999999999999" -> "1000000000000000000",
/// confirmed via a byte-for-byte A/B comparison against the pre-existing
/// code). Real-world 64-bit IDs (Snowflake/Discord/database bigint IDs
/// commonly stored as JSON strings specifically *to avoid* this exact class
/// of precision loss in other JSON parsers) are typically 17-19 digits, so
/// this was a live correctness bug for `auto_convert_types`, not just a
/// hypothetical one.
///
/// Deliberately excludes "-0": the float round-trip collapses it to "0"
/// (casting `-0.0f64 as i64` drops the sign), so falling through to the slow
/// path preserves that existing behavior instead of silently changing it.
///
/// Validated with an isolated benchmark before adopting: ~8x faster than the
/// float round-trip for a realistic mix of mostly-clean integer strings (the
/// common case for `auto_convert_types` on numeric-ID/count fields stored as
/// strings) -- skips a full float parse and a heap-allocating reformat when
/// the input is already the output.
#[inline]
fn canonical_json_integer(s: &str) -> Option<&str> {
    let bytes = s.as_bytes();
    let (neg, digits) = match bytes.first() {
        Some(b'-') => (true, &bytes[1..]),
        _ => (false, bytes),
    };
    if digits.is_empty() || digits.len() > 20 || !digits.iter().all(u8::is_ascii_digit) {
        return None;
    }
    if digits[0] == b'0' {
        // "0" itself is fine; "00"/"007" (leading zero) and "-0" (negative
        // zero) are not -- both must fall through to match existing behavior.
        return if digits.len() == 1 && !neg {
            Some(s)
        } else {
            None
        };
    }
    let fits = match digits.len() {
        1..=18 => true,                         // always fits i64 and u64
        19 if !neg => true,                     // any 19-digit positive < u64::MAX (20 digits)
        19 => digits <= I64_MIN_MAGNITUDE,      // negative: must fit i64::MIN
        20 if !neg => digits <= U64_MAX_DIGITS, // 20-digit negative can never fit i64
        _ => false,
    };
    fits.then_some(s)
}

/// Convert f64 to a JSON number string representation.
/// Returns None for NaN or Infinity. Converts to integer representation when possible.
#[inline]
fn f64_to_json_bytes(num: f64) -> Option<Cow<'static, str>> {
    if num.is_finite() && num.fract() == 0.0 {
        if num >= i64::MIN as f64 && num <= i64::MAX as f64 {
            return Some(Cow::Owned((num as i64).to_string()));
        }
        if num >= 0.0 && num <= u64::MAX as f64 {
            return Some(Cow::Owned((num as u64).to_string()));
        }
    }
    // Use serde_json for correct float formatting (uses ryu internally)
    serde_json::Number::from_f64(num).map(|n| Cow::Owned(n.to_string()))
}

/// SIMD-accelerated copy skipping exactly 4 specified bytes.
///
/// Uses memchr3 (3 bytes) + memchr (1 byte) to locate skip positions with AVX2/SSE2/NEON,
/// then bulk-copies the clean segments between them via extend_from_slice (hardware memcpy).
/// Faster than byte-by-byte filtering once input exceeds ~16 bytes.
#[inline]
pub(crate) fn extend_skipping_4(
    dst: &mut SmallVec<[u8; 64]>,
    src: &[u8],
    s1: u8,
    s2: u8,
    s3: u8,
    s4: u8,
) {
    let mut start = 0usize;
    while start < src.len() {
        let rest = &src[start..];
        let next = {
            let a = memchr3(s1, s2, s3, rest);
            let b = memchr(s4, rest);
            match (a, b) {
                (Some(x), Some(y)) => Some(x.min(y) + start),
                (Some(x), None) | (None, Some(x)) => Some(x + start),
                (None, None) => None,
            }
        };
        match next {
            Some(sep_pos) => {
                dst.extend_from_slice(&src[start..sep_pos]);
                start = sep_pos + 1;
            }
            None => {
                dst.extend_from_slice(&src[start..]);
                break;
            }
        }
    }
}

/// SIMD-accelerated copy skipping exactly 3 specified bytes.
#[inline]
pub(crate) fn extend_skipping_3(dst: &mut SmallVec<[u8; 64]>, src: &[u8], s1: u8, s2: u8, s3: u8) {
    let mut start = 0usize;
    while start < src.len() {
        let rest = &src[start..];
        match memchr3(s1, s2, s3, rest) {
            Some(pos) => {
                dst.extend_from_slice(&src[start..start + pos]);
                start += pos + 1;
            }
            None => {
                dst.extend_from_slice(&src[start..]);
                break;
            }
        }
    }
}
