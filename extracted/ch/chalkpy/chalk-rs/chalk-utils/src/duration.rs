/// 100 years in milliseconds — the maximum duration Chalk supports.
/// Must match `CHALK_MAX_TIMEDELTA = timedelta(days=100 * 365)` in Python.
pub const CHALK_MAX_DURATION_MS: i64 = 100 * 365 * 86_400 * 1_000;
pub const CHALK_MAX_DURATION_S: i64 = 100 * 365 * 86_400;

/// Parse a Chalk duration string to total milliseconds.
/// Handles: "10m", "1h30m", "7d", "-3d10m", "500ms", "infinity", "all", etc.
/// Returns an error string (suitable for ValueError) on invalid input.
pub fn parse_duration_ms(s: &str) -> Result<i64, String> {
    // Fast-path lookup for common durations
    match s {
        "" => return Ok(0),
        "infinity" | "all" => return Ok(CHALK_MAX_DURATION_MS),
        "0s" => return Ok(0),
        "1s" => return Ok(1_000),
        "50s" => return Ok(50_000),
        "200s" => return Ok(200_000),
        "1m" => return Ok(60_000),
        "5m" => return Ok(300_000),
        "10m" => return Ok(600_000),
        "15m" => return Ok(900_000),
        "20m" => return Ok(1_200_000),
        "30m" => return Ok(1_800_000),
        "1h" => return Ok(3_600_000),
        "2h" => return Ok(7_200_000),
        "12h" => return Ok(43_200_000),
        "24h" => return Ok(86_400_000),
        "48h" => return Ok(172_800_000),
        "1d" => return Ok(86_400_000),
        "2d" => return Ok(172_800_000),
        "3d" => return Ok(259_200_000),
        "5d" => return Ok(432_000_000),
        "7d" => return Ok(604_800_000),
        "10d" => return Ok(864_000_000),
        "14d" => return Ok(1_209_600_000),
        "30d" => return Ok(2_592_000_000),
        "45d" => return Ok(3_888_000_000),
        "60d" => return Ok(5_184_000_000),
        "90d" => return Ok(7_776_000_000),
        "100d" => return Ok(8_640_000_000),
        "365d" => return Ok(31_536_000_000),
        "1w" => return Ok(604_800_000),
        _ => {}
    }

    parse_duration_ms_slow(s)
}

/// Parse a Chalk duration string to total seconds (truncated toward zero).
pub fn parse_duration_s(s: &str) -> Result<i64, String> {
    let ms = parse_duration_ms(s)?;
    // Truncate toward zero (same as Python int() on positive, floor-div for negative)
    if ms >= 0 {
        Ok(ms / 1000)
    } else {
        // For negative: -3010ms -> -3s (truncate toward zero)
        Ok(-((-ms) / 1000))
    }
}

/// Convert total seconds (as f64 for sub-second precision) to a duration string.
/// e.g. 90061.005 → "1d1h1m1s5ms"
pub fn seconds_to_duration_string(total_seconds: f64) -> String {
    if total_seconds >= CHALK_MAX_DURATION_S as f64 {
        return "infinity".to_string();
    }
    let negative = total_seconds < 0.0;
    let total_seconds = total_seconds.abs();
    let whole_seconds = total_seconds as u64;
    let milliseconds = ((total_seconds - whole_seconds as f64) * 1000.0).round() as u64;

    let days = whole_seconds / 86400;
    let remainder = whole_seconds % 86400;
    let hours = remainder / 3600;
    let remainder = remainder % 3600;
    let minutes = remainder / 60;
    let seconds = remainder % 60;

    let mut result = String::new();
    if negative {
        result.push('-');
    }
    if days > 0 {
        result.push_str(&days.to_string());
        result.push('d');
    }
    if hours > 0 {
        result.push_str(&hours.to_string());
        result.push('h');
    }
    if minutes > 0 {
        result.push_str(&minutes.to_string());
        result.push('m');
    }
    if seconds > 0 {
        result.push_str(&seconds.to_string());
        result.push('s');
    }
    if milliseconds > 0 {
        result.push_str(&milliseconds.to_string());
        result.push_str("ms");
    }
    result
}

// Unit flags for duplicate detection
const UNIT_WEEKS: u8 = 1;
const UNIT_DAYS: u8 = 2;
const UNIT_HOURS: u8 = 4;
const UNIT_MINUTES: u8 = 8;
const UNIT_SECONDS: u8 = 16;
const UNIT_MILLISECONDS: u8 = 32;

fn make_error(original: &str, remainder: &str) -> String {
    format!(
        "The duration '{}' contained a component '{}' that could not be parsed. \
         Please use a valid duration, like '10m', '1h', or '1h30m'. \
         Read more at https://docs.chalk.ai/api-docs#Duration",
        original, remainder
    )
}

fn parse_duration_ms_slow(s: &str) -> Result<i64, String> {
    let bytes = s.as_bytes();
    let len = bytes.len();

    if len == 0 || s.trim().is_empty() {
        return Err(make_error(s, s));
    }

    let mut pos: usize = 0;

    // Handle optional negative prefix
    let negative = bytes[0] == b'-';
    if negative {
        pos = 1;
    }

    let mut total_ms: i64 = 0;
    let mut seen: u8 = 0;
    let mut parsed_any = false;

    // We track consumed ranges so we can compute the remainder for error messages.
    // Strategy: walk through input, skip whitespace, parse number+unit pairs.
    // If anything is left over, that's the remainder for the error.
    let mut consumed = vec![false; len];
    if negative {
        consumed[0] = true;
    }

    while pos < len {
        // Skip whitespace
        if bytes[pos] == b' ' {
            consumed[pos] = true;
            pos += 1;
            continue;
        }

        // Expect a digit
        if !bytes[pos].is_ascii_digit() {
            // Build remainder from unconsumed bytes
            let remainder: String = bytes
                .iter()
                .zip(consumed.iter())
                .filter(|(_, &c)| !c)
                .map(|(&b, _)| b as char)
                .collect::<String>()
                .trim()
                .to_string();
            return Err(make_error(s, &remainder));
        }

        // Parse digit run
        let num_start = pos;
        while pos < len && bytes[pos].is_ascii_digit() {
            pos += 1;
        }
        let num_str = &s[num_start..pos];
        let value: i64 = num_str.parse().map_err(|_| make_error(s, num_str))?;

        // Parse unit suffix
        if pos >= len {
            // Number with no unit
            let remainder: String = bytes
                .iter()
                .zip(consumed.iter())
                .filter(|(_, &c)| !c)
                .map(|(&b, _)| b as char)
                .collect::<String>()
                .trim()
                .to_string();
            return Err(make_error(s, &remainder));
        }

        let (multiplier, unit_flag, unit_len) = match bytes[pos] {
            b'w' => (604_800_000i64, UNIT_WEEKS, 1),
            b'd' => (86_400_000, UNIT_DAYS, 1),
            b'h' => (3_600_000, UNIT_HOURS, 1),
            b'm' => {
                // Check for "ms"
                if pos + 1 < len && bytes[pos + 1] == b's' {
                    (1, UNIT_MILLISECONDS, 2)
                } else {
                    (60_000, UNIT_MINUTES, 1)
                }
            }
            b's' => (1_000, UNIT_SECONDS, 1),
            _ => {
                let remainder: String = bytes
                    .iter()
                    .zip(consumed.iter())
                    .filter(|(_, &c)| !c)
                    .map(|(&b, _)| b as char)
                    .collect::<String>()
                    .trim()
                    .to_string();
                return Err(make_error(s, &remainder));
            }
        };

        // Check for duplicate unit
        if seen & unit_flag != 0 {
            // Mark everything up to here as consumed, remainder is current number+unit onward
            let remainder: String = bytes
                .iter()
                .zip(consumed.iter())
                .filter(|(_, &c)| !c)
                .map(|(&b, _)| b as char)
                .collect::<String>()
                .trim()
                .to_string();
            return Err(make_error(s, &remainder));
        }
        seen |= unit_flag;

        // Check that unit suffix isn't followed by more alpha (e.g. "10daily" should fail)
        let unit_end = pos + unit_len;
        if unit_end < len && bytes[unit_end].is_ascii_alphabetic() {
            let remainder: String = bytes
                .iter()
                .zip(consumed.iter())
                .filter(|(_, &c)| !c)
                .map(|(&b, _)| b as char)
                .collect::<String>()
                .trim()
                .to_string();
            return Err(make_error(s, &remainder));
        }

        total_ms += value * multiplier;
        for i in num_start..unit_end {
            consumed[i] = true;
        }
        pos = unit_end;
        parsed_any = true;
    }

    if !parsed_any {
        return Err(make_error(s, s));
    }

    // Check for any unconsumed non-whitespace
    let remainder: String = bytes
        .iter()
        .zip(consumed.iter())
        .filter(|(_, &c)| !c)
        .map(|(&b, _)| b as char)
        .collect::<String>()
        .trim()
        .to_string();
    if !remainder.is_empty() {
        return Err(make_error(s, &remainder));
    }

    Ok(if negative { -total_ms } else { total_ms })
}

#[cfg(test)]
mod tests {
    use super::*;

    // Millisecond multipliers for readable assertions
    const MS: i64 = 1;
    const S: i64 = 1_000;
    const M: i64 = 60 * S;
    const H: i64 = 60 * M;
    const D: i64 = 24 * H;
    const W: i64 = 7 * D;

    // ── parse_duration_ms: fast-path lookups ──────────────────────────

    #[test]
    fn test_lookup_fast_path_cases() {
        let cases: [(&str, i64); 10] = [
            ("1m", 1 * M),
            ("1d", 1 * D),
            ("30m", 30 * M),
            ("1h", 1 * H),
            ("7d", 7 * D),
            ("90d", 90 * D),
            ("0s", 0),
            ("1w", 1 * W),
            ("infinity", CHALK_MAX_DURATION_MS),
            ("all", CHALK_MAX_DURATION_MS),
        ];

        for (input, expected_ms) in cases {
            assert_eq!(
                parse_duration_ms(input).unwrap(),
                expected_ms,
                "fast-path lookup mismatch for '{input}'"
            );
        }
    }

    // ── parse_duration_ms: slow-path multi-component ─────────────────

    #[test]
    fn test_multi_component_cases() {
        let cases: [(&str, i64); 6] = [
            ("10d 04s", 10 * D + 4 * S),
            ("1h30m", 1 * H + 30 * M),
            ("1w 2m", 1 * W + 2 * M),
            ("10m 40s 4ms", 10 * M + 40 * S + 4 * MS),
            ("-3d10m", -(3 * D + 10 * M)),
            ("", 0),
        ];

        for (input, expected_ms) in cases {
            assert_eq!(
                parse_duration_ms(input).unwrap(),
                expected_ms,
                "multi-component parse mismatch for '{input}'"
            );
        }
    }

    // ── parse_duration_ms: error cases ───────────────────────────────

    #[test]
    fn test_duplicate_unit_error() {
        let err = parse_duration_ms("10d 4d").unwrap_err();
        assert_eq!(
            err,
            "The duration '10d 4d' contained a component '4d' that could not be parsed. \
             Please use a valid duration, like '10m', '1h', or '1h30m'. \
             Read more at https://docs.chalk.ai/api-docs#Duration"
        );
    }

    #[test]
    fn test_unknown_unit_error() {
        let err = parse_duration_ms("10b").unwrap_err();
        assert_eq!(
            err,
            "The duration '10b' contained a component '10b' that could not be parsed. \
             Please use a valid duration, like '10m', '1h', or '1h30m'. \
             Read more at https://docs.chalk.ai/api-docs#Duration"
        );
    }

    #[test]
    fn test_whitespace_only_error() {
        assert!(parse_duration_ms("  ").is_err());
    }

    // ── parse_duration_s ─────────────────────────────────────────────

    #[test]
    fn test_parse_duration_s_cases() {
        let cases: [(&str, i64); 7] = [
            ("1m", 60),
            ("1h30m", 90 * 60),
            ("7d", 7 * 86_400),
            // 10m 40s 4ms = 640004ms -> 640s (truncate toward zero)
            ("10m 40s 4ms", 10 * 60 + 40),
            ("-3d10m", -(3 * 86_400 + 10 * 60)),
            ("infinity", CHALK_MAX_DURATION_S),
            ("all", CHALK_MAX_DURATION_S),
        ];

        for (input, expected_s) in cases {
            assert_eq!(
                parse_duration_s(input).unwrap(),
                expected_s,
                "parse_duration_s mismatch for '{input}'"
            );
        }
    }

    // ── seconds_to_duration_string ───────────────────────────────────

    #[test]
    fn test_seconds_to_duration_string_cases() {
        let cases: [(f64, &str); 10] = [
            (4.0, "4s"),
            (30.0 * 60.0 + 4.0, "30m4s"),
            (86_400.0 + 4.0, "1d4s"),
            (2.0 * 86_400.0, "2d"),
            (86_400.0 + 3_600.0 + 60.0 + 1.0 + 0.005, "1d1h1m1s5ms"),
            (-(3.0 * 86_400.0 + 10.0 * 60.0 + 0.005), "-3d10m5ms"),
            (0.0, ""),
            (0.042, "42ms"),
            (CHALK_MAX_DURATION_S as f64, "infinity"),
            (CHALK_MAX_DURATION_S as f64 + 1.0, "infinity"),
        ];

        for (input_s, expected) in cases {
            assert_eq!(
                seconds_to_duration_string(input_s),
                expected,
                "seconds_to_duration_string mismatch for {input_s}"
            );
        }
    }

    // ── roundtrip tests ──────────────────────────────────────────────

    #[test]
    fn test_roundtrip() {
        let cases = vec!["1d", "1h", "30m", "1h30m", "1d4s", "2d", "30m4s"];
        for case in cases {
            let ms = parse_duration_ms(case).unwrap();
            let back = seconds_to_duration_string(ms as f64 / 1000.0);
            assert_eq!(back, case, "roundtrip failed for '{}'", case);
        }
    }
}
