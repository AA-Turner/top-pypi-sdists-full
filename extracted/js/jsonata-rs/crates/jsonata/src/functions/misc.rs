//! Misc built-ins: error, assert, eval, datetime. Ported from Java `Functions`.

use crate::error::{JError, JResult};
use crate::evaluator::Evaluator;
use crate::value::JValue;

use chrono::{Duration, Local, LocalResult, NaiveDate, Offset, TimeZone};
use regex::Regex;
use std::sync::OnceLock;

/// Java: `public static void error(String message) throws Throwable`
///
/// ```java
/// throw new JException("D3137", -1, message != null ? message : "$error() function evaluated");
/// ```
/// The signature is `<s?:x>`, so the (optional) argument is already validated to
/// be a string. The dynamic message goes in `.current` (the D3137 template is
/// `{{{message}}}`, substituted from `.current`).
pub fn error(args: &[JValue]) -> JResult<JValue> {
    let message = match args.first().and_then(|v| v.as_str()) {
        Some(s) => s.to_string(),
        None => "$error() function evaluated".to_string(),
    };
    // Java: throw new JException("D3137", -1, message)
    Err(JError::with_current("D3137", -1, JValue::string(message)))
}

/// Java: `public static void assertFn(boolean condition, String message) throws Throwable`
///
/// ```java
/// if (!condition) {
///     throw new JException("D3141", -1, message != null ? message : "$assert() statement failed");
/// }
/// ```
/// Signature `<bs?:x>`: arg0 is the (validated) boolean condition, arg1 the
/// optional string message. Returns undefined when the condition holds.
pub fn assert_fn(args: &[JValue]) -> JResult<JValue> {
    let condition = args.first().and_then(|v| v.as_bool()).unwrap_or(false);
    if !condition {
        let message = match args.get(1).and_then(|v| v.as_str()) {
            Some(s) => s.to_string(),
            None => "$assert() statement failed".to_string(),
        };
        // Java: throw new JException("D3141", -1, message)
        return Err(JError::with_current("D3141", -1, JValue::string(message)));
    }
    Ok(JValue::Undefined)
}

pub fn eval(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let expr = match args.first() {
        Some(JValue::String(s)) => s.to_string(),
        _ => return Ok(JValue::Undefined),
    };
    let focus = args.get(1).cloned().unwrap_or(JValue::Undefined);
    ev.eval_str(&expr, focus)
}

/// Java: `public static String now(String picture, String timezone)`
///
/// ```java
/// long t = Jsonata.current.get().timestamp;
/// return dateTimeFromMillis(t, picture, timezone);
/// ```
/// Signature `<s?s?:s>`. The captured request timestamp is `ev.timestamp`.
pub fn now(ev: &mut Evaluator, args: &[JValue]) -> JResult<JValue> {
    let picture = args.first().and_then(|v| v.as_str());
    let timezone = args.get(1).and_then(|v| v.as_str());
    let s = crate::datetime::format_date_time(ev.timestamp, picture, timezone)?;
    Ok(JValue::string(s))
}

/// Java: `public static String dateTimeFromMillis(Number millis, String picture, String timezone)`
///
/// ```java
/// if (millis == null) return null;          // undefined input -> undefined
/// return DateTimeUtils.formatDateTime(millis.longValue(), picture, timezone);
/// ```
/// Signature `<n-s?s?:s>`. `millis.longValue()` truncates toward zero, matching
/// Rust's `as i64` cast for finite values.
pub fn from_millis(args: &[JValue]) -> JResult<JValue> {
    let arg0 = args.first().cloned().unwrap_or(JValue::Undefined);
    if arg0.is_undefined() {
        return Ok(JValue::Undefined);
    }
    // Signature `n` guarantees a number; defensively default to 0 otherwise.
    let millis = arg0.as_f64().unwrap_or(0.0) as i64;
    let picture = args.get(1).and_then(|v| v.as_str());
    let timezone = args.get(2).and_then(|v| v.as_str());
    let s = crate::datetime::format_date_time(millis, picture, timezone)?;
    Ok(JValue::string(s))
}

/// Java: `public static Long dateTimeToMillis(String timestamp, String picture) throws ParseException`
///
/// ```java
/// if (timestamp == null) return null;       // undefined input -> undefined
/// if (picture == null) {
///     // ... ISO 8601 parse ...
/// } else {
///     return DateTimeUtils.parseDateTime(timestamp, picture);
/// }
/// ```
/// Signature `<s-s?:n>`.
///
/// PORT-NOTE: with no picture, jsonata-java runs a lenient `java.time` fallback
/// chain (see `date_time_to_millis` below) instead of jsonata-js's ISO-8601
/// regex gate + `Date.parse`. We replicate the Java chain — see COMPAT.md
/// ("`$toMillis` default (no-picture) parsing") for the catalogued divergences
/// from jsonata-js (e.g. `'123'` parses as year 123 here, and `'2018-01'` is
/// rejected). The one deliberate softening: where Java lets a raw
/// `DateTimeParseException`/`ParseException` escape (crashing the caller), we
/// raise the clean JSONata error D3110 with the timestamp as `current` — the
/// accept/reject split is identical, only the failure surface differs.
pub fn to_millis(args: &[JValue]) -> JResult<JValue> {
    let arg0 = args.first().cloned().unwrap_or(JValue::Undefined);
    if arg0.is_undefined() {
        return Ok(JValue::Undefined);
    }
    let timestamp = arg0.as_str().unwrap_or("").to_string();

    match args.get(1).and_then(|v| v.as_str()) {
        None => match date_time_to_millis(&timestamp) {
            Some(m) => Ok(JValue::Number(m as f64)),
            // Java: the DateTimeParseException escapes raw; we surface the
            // clean D3110 ("timestamp does not match ISO 8601") instead.
            None => Err(JError::with_current("D3110", -1, JValue::string(timestamp))),
        },
        Some(picture) => {
            // Java: return DateTimeUtils.parseDateTime(timestamp, picture);
            match crate::datetime::parse_date_time(&timestamp, picture)? {
                Some(m) => Ok(JValue::Number(m as f64)),
                None => Ok(JValue::Undefined),
            }
        }
    }
}

/// Java `Functions.dateTimeToMillis`, picture == null branch — the fallback
/// chain, replicated step by step (each step's accept/reject and value
/// verified differentially against jsonata-java in multiple timezones):
///
/// 1. all-digit string (`Character.isDigit` — Unicode `Nd`): lenient
///    `SimpleDateFormat("yyyy")` year parse in UTC.
/// 2. `OffsetDateTime.parse` after the `+HHMM` → `+HH:MM` colon fixup.
/// 3. `LocalDate.parse(ts, "yyyy-MM-dd")` (SMART resolver) → UTC midnight.
/// 4. `LocalDateTime.parse` (strict ISO, no offset) → system local timezone.
///
/// Returns `None` where Java would throw (`ParseException` from step 1,
/// `DateTimeParseException` from step 4, or `ArithmeticException` on epoch
/// overflow) — the caller maps that to D3110.
fn date_time_to_millis(timestamp: &str) -> Option<i64> {
    // Step 1: Java isNumeric(): non-empty, every char Character.isDigit.
    if !timestamp.is_empty() && timestamp.chars().all(is_unicode_digit) {
        return Some(lenient_year_to_millis(timestamp));
    }

    // Java mutates its local `timestamp` var with the offset-colon fixup before
    // OffsetDateTime.parse, so steps 2-4 all see the fixed-up string.
    let ts = fixup_offset_colon(timestamp);

    // Step 2: OffsetDateTime.parse (strict ISO_OFFSET_DATE_TIME).
    if let Some(m) = parse_offset_date_time(&ts) {
        return Some(m);
    }
    // Step 3: LocalDate.parse with pattern "yyyy-MM-dd" (SMART: day-of-month
    // clamps to the month length, e.g. 2018-02-31 -> 2018-02-28).
    if let Some(m) = parse_local_date_smart(&ts) {
        return Some(m);
    }
    // Step 4: LocalDateTime.parse (strict ISO_LOCAL_DATE_TIME), interpreted in
    // the system local timezone (ZoneId.systemDefault()).
    parse_local_date_time(&ts)
}

/// Java `Character.isDigit`: true exactly for Unicode general category `Nd`.
/// (`char::is_numeric` is broader — it also matches Nl/No — so test `\p{Nd}`.)
fn is_unicode_digit(c: char) -> bool {
    if c.is_ascii() {
        return c.is_ascii_digit();
    }
    static RE: OnceLock<Regex> = OnceLock::new();
    let re = RE.get_or_init(|| Regex::new(r"\A\p{Nd}\z").expect("valid Nd regex"));
    re.is_match(c.encode_utf8(&mut [0u8; 4]))
}

/// Decimal value of a Unicode `Nd` digit (Java `Character.digit(c, 10)`).
/// Unicode encodes each decimal-digit run as a contiguous 0..9 block, so scan
/// down to the start of the (possibly chained) run and take the offset mod 10.
fn unicode_digit_value(c: char) -> u32 {
    if let Some(d) = c.to_digit(10) {
        return d;
    }
    let mut start = c as u32;
    while start > 0 {
        match char::from_u32(start - 1) {
            Some(p) if is_unicode_digit(p) => start -= 1,
            _ => break,
        }
    }
    (c as u32 - start) % 10
}

/// Step 1: Java `new SimpleDateFormat("yyyy")` (lenient, UTC) applied to an
/// all-digit string. DecimalFormat yields a Long when the digits fit in a
/// long (otherwise a Double), and SimpleDateFormat takes `.intValue()` of it —
/// so the year wraps like `(int)(long)` in range and saturates to
/// `Integer.MAX_VALUE` beyond. The lenient GregorianCalendar then resolves
/// Jan 1 of that year using Julian rules up to 1582 and Gregorian rules from
/// 1583, with plain (wrapping) long arithmetic for the epoch millis.
fn lenient_year_to_millis(digits: &str) -> i64 {
    let mut acc: u128 = 0;
    let mut overflow = false;
    for c in digits.chars() {
        let d = unicode_digit_value(c) as u128;
        match acc.checked_mul(10).and_then(|a| a.checked_add(d)) {
            Some(a) => acc = a,
            None => {
                overflow = true;
                break;
            }
        }
    }
    let year: i32 = if overflow || acc > i64::MAX as u128 {
        i32::MAX // Double.intValue() saturates
    } else {
        (acc as i64) as i32 // Long.intValue() wraps
    };
    let y = year as i64;
    let epoch_days = if y >= 1583 {
        // Gregorian Jan 1 (days since 1970-01-01).
        let y1 = y - 1;
        365 * y1 + y1.div_euclid(4) - y1.div_euclid(100) + y1.div_euclid(400) + 1 - 719_163
    } else {
        // GregorianCalendar cutover: proleptic Julian Jan 1 up to 1582.
        365 * y + (y - 1).div_euclid(4) - 719_529
    };
    epoch_days.wrapping_mul(86_400_000)
}

/// The Java colon fixup ahead of `OffsetDateTime.parse`: if the 5th-from-last
/// char is `+`/`-` and the last four are digits (`Character.isDigit`), insert a
/// colon — `...+0000` becomes `...+00:00`.
fn fixup_offset_colon(ts: &str) -> String {
    let chars: Vec<char> = ts.chars().collect();
    let len = chars.len();
    if len > 5
        && (chars[len - 5] == '+' || chars[len - 5] == '-')
        && chars[len - 4..].iter().all(|&c| is_unicode_digit(c))
    {
        let mut fixed: String = chars[..len - 2].iter().collect();
        fixed.push(':');
        fixed.extend(&chars[len - 2..]);
        return fixed;
    }
    ts.to_string()
}

/// Regex for strict `java.time` ISO_OFFSET_DATE_TIME. Notes on fidelity:
/// - the ISO formatters parse case-insensitively, so `t`/`z` are accepted;
/// - year (field YEAR, SignStyle.EXCEEDS_PAD): exactly 4 digits unsigned, or a
///   sign with `-` ≥ 4 / `+` ≥ 5 digits, max 10;
/// - seconds are optional; the fraction needs seconds and takes 0-9 digits
///   (a bare trailing `.` is valid — appendFraction min width is 0);
/// - offset `Z` or `±HH[:MM[:SS]]`.
fn offset_date_time_regex() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(
            r"(?x)^
            (?P<y>-[0-9]{4,10}|\+[0-9]{5,10}|[0-9]{4})
            -(?P<mo>[0-9]{2})-(?P<d>[0-9]{2})
            [Tt](?P<h>[0-9]{2}):(?P<mi>[0-9]{2})
            (?::(?P<s>[0-9]{2})(?:\.(?P<f>[0-9]{0,9}))?)?
            (?:[Zz]|(?P<osign>[+-])(?P<oh>[0-9]{2})(?::(?P<om>[0-9]{2})(?::(?P<os>[0-9]{2}))?)?)
            $",
        )
        .expect("valid offset date-time regex")
    })
}

/// Strict ISO_LOCAL_DATE_TIME (same as above, minus the offset designator).
fn local_date_time_regex() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(
            r"(?x)^
            (?P<y>-[0-9]{4,10}|\+[0-9]{5,10}|[0-9]{4})
            -(?P<mo>[0-9]{2})-(?P<d>[0-9]{2})
            [Tt](?P<h>[0-9]{2}):(?P<mi>[0-9]{2})
            (?::(?P<s>[0-9]{2})(?:\.(?P<f>[0-9]{0,9}))?)?
            $",
        )
        .expect("valid local date-time regex")
    })
}

/// Pattern `"yyyy-MM-dd"`: field YEAR_OF_ERA (positive, ≤ 999,999,999 — so a
/// parsed `-` year fails the range check later), 4-19 digit width.
fn local_date_regex() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(
            r"(?x)^
            (?P<y>-[0-9]{4,19}|\+[0-9]{5,19}|[0-9]{4})
            -(?P<mo>[0-9]{2})-(?P<d>[0-9]{2})
            $",
        )
        .expect("valid local date regex")
    })
}

/// ISO proleptic-Gregorian leap year (java.time / chrono agree).
fn is_leap_year(y: i64) -> bool {
    y % 4 == 0 && (y % 100 != 0 || y % 400 == 0)
}

fn days_in_month(y: i64, m: u32) -> u32 {
    match m {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 => {
            if is_leap_year(y) {
                29
            } else {
                28
            }
        }
        _ => 0,
    }
}

/// Days from the epoch (1970-01-01) for a proleptic-Gregorian date, valid for
/// any year (Howard Hinnant's `days_from_civil`).
fn days_from_civil(y: i64, m: u32, d: u32) -> i64 {
    let y = if m <= 2 { y - 1 } else { y };
    let era = y.div_euclid(400);
    let yoe = y - era * 400; // [0, 399]
    let mp = if m > 2 { m - 3 } else { m + 9 } as i64; // [0, 11]
    let doy = (153 * mp + 2) / 5 + d as i64 - 1;
    let doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    era * 146_097 + doe - 719_468
}

/// Parse a captured year field to i64, respecting the range java.time enforces
/// for YEAR / YEAR_OF_ERA (±999,999,999).
fn parse_year_field(y: &str) -> Option<i64> {
    let v: i64 = y.trim_start_matches('+').parse().ok()?;
    (-999_999_999..=999_999_999).contains(&v).then_some(v)
}

/// First three fraction digits, right-padded — java.time keeps nanoseconds but
/// `toEpochMilli` only surfaces milliseconds.
fn frac_field_millis(f: &str) -> i64 {
    let mut digits: String = f.chars().take(3).collect();
    while digits.len() < 3 {
        digits.push('0');
    }
    digits.parse().unwrap_or(0)
}

/// Step 2: `OffsetDateTime.parse(ts).toInstant().toEpochMilli()`. Strict
/// validation (month 1-12, real day-of-month, HH ≤ 23, offset ≤ ±18:00);
/// epoch overflow returns None like Java's ArithmeticException (which is
/// caught as a RuntimeException and falls through to the next steps, where
/// an offset-bearing string can never parse — same net reject).
fn parse_offset_date_time(ts: &str) -> Option<i64> {
    let caps = offset_date_time_regex().captures(ts)?;
    let y = parse_year_field(&caps["y"])?;
    let mo: u32 = caps["mo"].parse().ok()?;
    let d: u32 = caps["d"].parse().ok()?;
    let h: i64 = caps["h"].parse().ok()?;
    let mi: i64 = caps["mi"].parse().ok()?;
    let s: i64 = caps.name("s").map_or(Ok(0), |m| m.as_str().parse()).ok()?;
    let frac = caps.name("f").map_or(0, |m| frac_field_millis(m.as_str()));
    if !(1..=12).contains(&mo) || d < 1 || d > days_in_month(y, mo) || h > 23 || mi > 59 || s > 59 {
        return None;
    }
    let offset_secs = match caps.name("osign") {
        None => 0, // Z
        Some(sign) => {
            let oh: i64 = caps["oh"].parse().ok()?;
            let om: i64 = caps.name("om").map_or(Ok(0), |m| m.as_str().parse()).ok()?;
            let os: i64 = caps.name("os").map_or(Ok(0), |m| m.as_str().parse()).ok()?;
            if om > 59 || os > 59 {
                return None;
            }
            let total = oh * 3600 + om * 60 + os;
            if total > 18 * 3600 {
                return None; // ZoneOffset range is ±18:00
            }
            if sign.as_str() == "-" {
                -total
            } else {
                total
            }
        }
    };
    let secs = days_from_civil(y, mo, d)
        .checked_mul(86_400)?
        .checked_add(h * 3600 + mi * 60 + s)?
        .checked_sub(offset_secs)?;
    secs.checked_mul(1000)?.checked_add(frac)
}

/// Step 3: `LocalDate.parse(ts, ofPattern("yyyy-MM-dd"))` (SMART resolver) at
/// UTC midnight. SMART validates month 1-12 and day 1-31 at parse time, then
/// clamps the day to the month length (2018-02-31 -> 2018-02-28). Year-of-era
/// must be ≥ 1. Epoch overflow (year ≈ 300M+) returns None — in Java that is
/// a raw uncaught ArithmeticException, another crash we turn into D3110.
fn parse_local_date_smart(ts: &str) -> Option<i64> {
    let caps = local_date_regex().captures(ts)?;
    let y: i64 = caps["y"].trim_start_matches('+').parse().ok()?;
    if !(1..=999_999_999).contains(&y) {
        return None; // YEAR_OF_ERA range
    }
    let mo: u32 = caps["mo"].parse().ok()?;
    let d: u32 = caps["d"].parse().ok()?;
    if !(1..=12).contains(&mo) || !(1..=31).contains(&d) {
        return None;
    }
    let d = d.min(days_in_month(y, mo)); // SMART clamp
    days_from_civil(y, mo, d).checked_mul(86_400_000)
}

/// Step 4: `LocalDateTime.parse(ts).atZone(ZoneId.systemDefault())`. The naive
/// local time resolves against the system zone with `ZonedDateTime.ofLocal`
/// semantics: overlaps take the earlier offset (= earlier instant) and DST
/// gaps shift forward by the gap — equivalent to applying the pre-gap offset.
fn parse_local_date_time(ts: &str) -> Option<i64> {
    let caps = local_date_time_regex().captures(ts)?;
    let y = parse_year_field(&caps["y"])?;
    let mo: u32 = caps["mo"].parse().ok()?;
    let d: u32 = caps["d"].parse().ok()?;
    let h: u32 = caps["h"].parse().ok()?;
    let mi: u32 = caps["mi"].parse().ok()?;
    let s: u32 = caps.name("s").map_or(Ok(0), |m| m.as_str().parse()).ok()?;
    let frac = caps.name("f").map_or(0, |m| frac_field_millis(m.as_str()));
    if !(1..=12).contains(&mo) || d < 1 || d > days_in_month(y, mo) || h > 23 || mi > 59 || s > 59 {
        return None;
    }

    // chrono's NaiveDate only spans years ±262143, but java.time accepts up to
    // ±999,999,999 here. Zone rules repeat over the 400-year Gregorian cycle
    // (identical leap pattern and weekday alignment), so resolve the offset in
    // a congruent year within range and shift the result by whole days.
    let mut cy = y;
    while cy > 200_000 {
        cy -= 400;
    }
    while cy < -200_000 {
        cy += 400;
    }
    let ndt = NaiveDate::from_ymd_opt(cy as i32, mo, d)?.and_hms_opt(h, mi, s)?;
    let base = match Local.from_local_datetime(&ndt) {
        LocalResult::Single(dt) => dt.timestamp_millis(),
        // Overlap: Java picks the pre-transition offset, i.e. the earlier
        // instant. chrono's overlap range is endpoint-inclusive (java.time's
        // is half-open), so first drop any candidate whose offset is not
        // actually in effect at the instant it denotes.
        LocalResult::Ambiguous(a, b) => {
            let valid = |dt: &chrono::DateTime<Local>| {
                Local.offset_from_utc_datetime(&dt.naive_utc()).fix() == dt.offset().fix()
            };
            match (valid(&a), valid(&b)) {
                (true, false) => a.timestamp_millis(),
                (false, true) => b.timestamp_millis(),
                _ => a.timestamp_millis().min(b.timestamp_millis()),
            }
        }
        // Gap: interpret with the pre-gap offset (== Java's shift-forward-by-
        // the-gap). Walk back to the nearest resolvable local time and undo
        // the walk on the instant; the offset there is the pre-gap offset as
        // long as the walk lands before the transition (gaps are ≤ 1h except
        // for exotic zone hops like Pacific/Apia 2011, which the loop covers).
        LocalResult::None => {
            let mut k = 1i64;
            loop {
                if k > 48 {
                    return None;
                }
                let probe = ndt.checked_sub_signed(Duration::hours(k))?;
                match Local.from_local_datetime(&probe).earliest() {
                    Some(dt) => break dt.timestamp_millis() + k * 3_600_000,
                    None => k += 1,
                }
            }
        }
    };
    let day_shift = days_from_civil(y, mo, d)
        .checked_sub(days_from_civil(cy, mo, d))?
        .checked_mul(86_400_000)?;
    base.checked_add(day_shift)?.checked_add(frac)
}
