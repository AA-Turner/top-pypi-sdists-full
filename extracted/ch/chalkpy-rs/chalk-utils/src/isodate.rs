#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct IsoDate {
    pub year: i32,
    pub month: u8,
    pub day: u8,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum IsoTimezone {
    Utc,
    Fixed { name: String, seconds: i32 },
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IsoTime {
    pub hour: u8,
    pub minute: u8,
    pub second: u8,
    pub microsecond: u32,
    pub timezone: Option<IsoTimezone>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IsoDateTime {
    pub date: IsoDate,
    pub time: IsoTime,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum IsoDuration {
    Timedelta { total_microseconds: i128 },
    HasYearMonth,
}

const US_PER_SECOND: i128 = 1_000_000;
const US_PER_MINUTE: i128 = 60 * US_PER_SECOND;
const US_PER_HOUR: i128 = 60 * US_PER_MINUTE;
const US_PER_DAY: i128 = 24 * US_PER_HOUR;
const US_PER_WEEK: i128 = 7 * US_PER_DAY;

fn iso_error(kind: &str, value: &str) -> String {
    format!("Unrecognised ISO 8601 {kind} format: {value:?}")
}

fn is_digit(b: u8) -> bool {
    b.is_ascii_digit()
}

fn all_digits(bytes: &[u8]) -> bool {
    bytes.iter().all(|&b| is_digit(b))
}

fn parse_i32_digits(s: &str) -> i32 {
    let mut value = 0i32;
    for b in s.bytes() {
        value = value * 10 + i32::from(b - b'0');
    }
    value
}

fn parse_u8_digits(s: &str) -> u8 {
    let mut value = 0u8;
    for b in s.bytes() {
        value = value * 10 + (b - b'0');
    }
    value
}

fn days_from_civil(year: i32, month: u8, day: u8) -> i64 {
    let year = i64::from(year) - i64::from(month <= 2);
    let era = if year >= 0 { year } else { year - 399 } / 400;
    let yoe = year - era * 400;
    let month = i64::from(month);
    let day = i64::from(day);
    let mp = month + if month > 2 { -3 } else { 9 };
    let doy = (153 * mp + 2) / 5 + day - 1;
    let doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    era * 146_097 + doe - 719_468
}

fn civil_from_days(days: i64) -> IsoDate {
    let days = days + 719_468;
    let era = if days >= 0 { days } else { days - 146_096 } / 146_097;
    let doe = days - era * 146_097;
    let yoe = (doe - doe / 1_460 + doe / 36_524 - doe / 146_096) / 365;
    let year = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = mp + if mp < 10 { 3 } else { -9 };
    IsoDate {
        year: (year + i64::from(month <= 2)) as i32,
        month: month as u8,
        day: day as u8,
    }
}

fn iso_weekday(year: i32, month: u8, day: u8) -> i64 {
    (days_from_civil(year, month, day) + 3).rem_euclid(7) + 1
}

fn add_days(date: IsoDate, days: i64) -> IsoDate {
    civil_from_days(days_from_civil(date.year, date.month, date.day) + days)
}

fn is_leap_year(year: i32) -> bool {
    year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

fn parse_ordinal_date(year: i32, day: i32) -> Option<IsoDate> {
    if day < 1 || day > 365 + i32::from(is_leap_year(year)) {
        return None;
    }
    Some(add_days(
        IsoDate {
            year,
            month: 1,
            day: 1,
        },
        i64::from(day - 1),
    ))
}

fn parse_week_date(year: i32, week: i32, day: Option<i32>) -> Option<IsoDate> {
    let day = day.unwrap_or(1);
    if !(1..54).contains(&week) || !(1..8).contains(&day) {
        return None;
    }
    let jan_1 = IsoDate {
        year,
        month: 1,
        day: 1,
    };
    let jan_1_weekday = iso_weekday(year, 1, 1);
    let jan_1_is_week_1 = jan_1_weekday <= 4;
    let days = i64::from(7 * (week - i32::from(jan_1_is_week_1)) - jan_1_weekday as i32 + day);
    Some(add_days(jan_1, days))
}

pub fn parse_date(datestring: &str) -> Result<IsoDate, String> {
    if !datestring.is_ascii() {
        return Err(iso_error("date", datestring));
    }
    let bytes = datestring.as_bytes();
    let len = bytes.len();

    if len == 10
        && bytes[4] == b'-'
        && bytes[7] == b'-'
        && all_digits(&bytes[0..4])
        && all_digits(&bytes[5..7])
        && all_digits(&bytes[8..10])
    {
        return Ok(IsoDate {
            year: parse_i32_digits(&datestring[0..4]),
            month: parse_u8_digits(&datestring[5..7]),
            day: parse_u8_digits(&datestring[8..10]),
        });
    }
    if len == 8 && all_digits(bytes) {
        return Ok(IsoDate {
            year: parse_i32_digits(&datestring[0..4]),
            month: parse_u8_digits(&datestring[4..6]),
            day: parse_u8_digits(&datestring[6..8]),
        });
    }
    if len == 10
        && bytes[4] == b'-'
        && bytes[5] == b'W'
        && bytes[8] == b'-'
        && all_digits(&bytes[0..4])
        && all_digits(&bytes[6..8])
        && all_digits(&bytes[9..10])
    {
        return parse_week_date(
            parse_i32_digits(&datestring[0..4]),
            i32::from(parse_u8_digits(&datestring[6..8])),
            Some(i32::from(parse_u8_digits(&datestring[9..10]))),
        )
        .ok_or_else(|| iso_error("date", datestring));
    }
    if len == 8
        && bytes[4] == b'W'
        && all_digits(&bytes[0..4])
        && all_digits(&bytes[5..7])
        && all_digits(&bytes[7..8])
    {
        return parse_week_date(
            parse_i32_digits(&datestring[0..4]),
            i32::from(parse_u8_digits(&datestring[5..7])),
            Some(i32::from(parse_u8_digits(&datestring[7..8]))),
        )
        .ok_or_else(|| iso_error("date", datestring));
    }
    if len == 8 && bytes[4] == b'-' && all_digits(&bytes[0..4]) && all_digits(&bytes[5..8]) {
        let year = parse_i32_digits(&datestring[0..4]);
        let day = parse_i32_digits(&datestring[5..8]);
        return parse_ordinal_date(year, day).ok_or_else(|| iso_error("date", datestring));
    }
    if len == 7 && all_digits(bytes) {
        let year = parse_i32_digits(&datestring[0..4]);
        let day = parse_i32_digits(&datestring[4..7]);
        return parse_ordinal_date(year, day).ok_or_else(|| iso_error("date", datestring));
    }
    if len == 8
        && bytes[4] == b'-'
        && bytes[5] == b'W'
        && all_digits(&bytes[0..4])
        && all_digits(&bytes[6..8])
    {
        return parse_week_date(
            parse_i32_digits(&datestring[0..4]),
            i32::from(parse_u8_digits(&datestring[6..8])),
            None,
        )
        .ok_or_else(|| iso_error("date", datestring));
    }
    if len == 7 && bytes[4] == b'W' && all_digits(&bytes[0..4]) && all_digits(&bytes[5..7]) {
        return parse_week_date(
            parse_i32_digits(&datestring[0..4]),
            i32::from(parse_u8_digits(&datestring[5..7])),
            None,
        )
        .ok_or_else(|| iso_error("date", datestring));
    }
    if len == 7 && bytes[4] == b'-' && all_digits(&bytes[0..4]) && all_digits(&bytes[5..7]) {
        return Ok(IsoDate {
            year: parse_i32_digits(&datestring[0..4]),
            month: parse_u8_digits(&datestring[5..7]),
            day: 1,
        });
    }
    if len == 6 && all_digits(bytes) {
        return Ok(IsoDate {
            year: parse_i32_digits(&datestring[0..4]),
            month: parse_u8_digits(&datestring[4..6]),
            day: 1,
        });
    }
    if len == 4 && all_digits(bytes) {
        return Ok(IsoDate {
            year: parse_i32_digits(datestring),
            month: 1,
            day: 1,
        });
    }
    if len == 2 && all_digits(bytes) {
        return Ok(IsoDate {
            year: parse_i32_digits(datestring) * 100 + 1,
            month: 1,
            day: 1,
        });
    }

    Err(iso_error("date", datestring))
}

fn parse_tzinfo(s: &str) -> Option<Option<IsoTimezone>> {
    if s.is_empty() {
        return Some(None);
    }
    if s == "Z" || s == "z" {
        return Some(Some(IsoTimezone::Utc));
    }
    let bytes = s.as_bytes();
    if bytes.len() != 3 && bytes.len() != 5 && bytes.len() != 6 {
        return None;
    }
    if bytes[0] != b'+' && bytes[0] != b'-' {
        return None;
    }
    if !is_digit(bytes[1]) || !is_digit(bytes[2]) {
        return None;
    }
    let hour = i32::from(parse_u8_digits(&s[1..3]));
    let (minute, valid) = match bytes.len() {
        3 => (0, true),
        5 => (
            if is_digit(bytes[3]) && is_digit(bytes[4]) {
                i32::from(parse_u8_digits(&s[3..5]))
            } else {
                0
            },
            is_digit(bytes[3]) && is_digit(bytes[4]),
        ),
        6 => (
            if bytes[3] == b':' && is_digit(bytes[4]) && is_digit(bytes[5]) {
                i32::from(parse_u8_digits(&s[4..6]))
            } else {
                0
            },
            bytes[3] == b':' && is_digit(bytes[4]) && is_digit(bytes[5]),
        ),
        _ => unreachable!(),
    };
    if !valid {
        return None;
    }
    if hour > 23 || minute > 59 {
        return None;
    }
    let sign = if bytes[0] == b'-' { -1 } else { 1 };
    Some(Some(IsoTimezone::Fixed {
        name: s.to_string(),
        seconds: sign * (hour * 3600 + minute * 60),
    }))
}

fn split_fraction(s: &str, whole_len: usize) -> Option<(&str, Option<&str>, &str)> {
    if s.len() < whole_len {
        return None;
    }
    let (whole, rest) = s.split_at(whole_len);
    if !all_digits(whole.as_bytes()) {
        return None;
    }
    let rest_bytes = rest.as_bytes();
    if rest_bytes.first().is_some_and(|b| *b == b'.' || *b == b',') {
        let mut end = 1;
        while end < rest_bytes.len() && is_digit(rest_bytes[end]) {
            end += 1;
        }
        if end == 1 {
            return None;
        }
        Some((whole, Some(&rest[1..end]), &rest[end..]))
    } else {
        Some((whole, None, rest))
    }
}

fn floor_fraction_scaled(digits: &str, scale: u128) -> u128 {
    let mut numerator = 0u128;
    let mut denominator = 1u128;
    for b in digits.bytes().take(38) {
        numerator = numerator * 10 + u128::from(b - b'0');
        denominator *= 10;
    }
    numerator * scale / denominator
}

fn round_half_even(numerator: u128, denominator: u128) -> u128 {
    let quotient = numerator / denominator;
    let remainder = numerator % denominator;
    let twice = remainder * 2;
    if twice < denominator {
        quotient
    } else if twice > denominator || quotient % 2 == 1 {
        quotient + 1
    } else {
        quotient
    }
}

fn parse_second(whole: &str, fraction: Option<&str>) -> (u8, u32) {
    let second = parse_u8_digits(whole);
    let microsecond = fraction
        .map(|digits| floor_fraction_scaled(digits, 1_000_000) as u32)
        .unwrap_or(0);
    (second, microsecond)
}

fn parse_minute(whole: &str, fraction: Option<&str>) -> (u8, u8, u32) {
    let minute = parse_u8_digits(whole);
    let total_us = fraction
        .map(|digits| floor_fraction_scaled(digits, 60_000_000))
        .unwrap_or(0);
    (
        minute,
        (total_us / 1_000_000) as u8,
        (total_us % 1_000_000) as u32,
    )
}

fn parse_hour(whole: &str, fraction: Option<&str>) -> (u8, u8, u8, u32) {
    let hour = parse_u8_digits(whole);
    let Some(digits) = fraction else {
        return (hour, 0, 0, 0);
    };
    let minute_scaled = floor_fraction_scaled(digits, 60);
    let minute = minute_scaled as u8;

    let mut numerator = 0u128;
    let mut denominator = 1u128;
    for b in digits.bytes().take(38) {
        numerator = numerator * 10 + u128::from(b - b'0');
        denominator *= 10;
    }
    let after_minutes = numerator * 60 - minute_scaled * denominator;
    let second = (after_minutes * 60 / denominator) as u8;
    let after_seconds = numerator * 3_600
        - u128::from(minute) * 60 * denominator
        - u128::from(second) * denominator;
    let microsecond = round_half_even(after_seconds * 1_000_000, denominator) as u32;
    (hour, minute, second, microsecond)
}

fn try_parse_complete_extended(s: &str, offset: usize) -> Option<IsoTime> {
    let bytes = s.as_bytes();
    if bytes.len() < offset + 8 || bytes[offset + 2] != b':' || bytes[offset + 5] != b':' {
        return None;
    }
    if !all_digits(&bytes[offset..offset + 2])
        || !all_digits(&bytes[offset + 3..offset + 5])
        || !all_digits(&bytes[offset + 6..offset + 8])
    {
        return None;
    }
    let (second_whole, second_fraction, rest) = split_fraction(&s[offset + 6..], 2)?;
    let timezone = parse_tzinfo(rest)?;
    let (second, microsecond) = parse_second(second_whole, second_fraction);
    Some(IsoTime {
        hour: parse_u8_digits(&s[offset..offset + 2]),
        minute: parse_u8_digits(&s[offset + 3..offset + 5]),
        second,
        microsecond,
        timezone,
    })
}

fn try_parse_complete_basic(s: &str, offset: usize) -> Option<IsoTime> {
    let (whole, fraction, rest) = split_fraction(&s[offset..], 6)?;
    let timezone = parse_tzinfo(rest)?;
    let (second, microsecond) = parse_second(&whole[4..6], fraction);
    Some(IsoTime {
        hour: parse_u8_digits(&whole[0..2]),
        minute: parse_u8_digits(&whole[2..4]),
        second,
        microsecond,
        timezone,
    })
}

fn try_parse_minute_extended(s: &str, offset: usize) -> Option<IsoTime> {
    let bytes = s.as_bytes();
    if bytes.len() < offset + 5 || bytes[offset + 2] != b':' {
        return None;
    }
    if !all_digits(&bytes[offset..offset + 2]) || !all_digits(&bytes[offset + 3..offset + 5]) {
        return None;
    }
    let (minute_whole, minute_fraction, rest) = split_fraction(&s[offset + 3..], 2)?;
    let timezone = parse_tzinfo(rest)?;
    let (minute, second, microsecond) = parse_minute(minute_whole, minute_fraction);
    Some(IsoTime {
        hour: parse_u8_digits(&s[offset..offset + 2]),
        minute,
        second,
        microsecond,
        timezone,
    })
}

fn try_parse_minute_basic(s: &str, offset: usize) -> Option<IsoTime> {
    let (whole, fraction, rest) = split_fraction(&s[offset..], 4)?;
    let timezone = parse_tzinfo(rest)?;
    let (minute, second, microsecond) = parse_minute(&whole[2..4], fraction);
    Some(IsoTime {
        hour: parse_u8_digits(&whole[0..2]),
        minute,
        second,
        microsecond,
        timezone,
    })
}

fn try_parse_hour(s: &str, offset: usize) -> Option<IsoTime> {
    let (whole, fraction, rest) = split_fraction(&s[offset..], 2)?;
    let timezone = parse_tzinfo(rest)?;
    let (hour, minute, second, microsecond) = parse_hour(whole, fraction);
    Some(IsoTime {
        hour,
        minute,
        second,
        microsecond,
        timezone,
    })
}

pub fn parse_time(timestring: &str) -> Result<IsoTime, String> {
    if !timestring.is_ascii() {
        return Err(iso_error("time", timestring));
    }
    let offset = usize::from(timestring.as_bytes().first().is_some_and(|b| *b == b'T'));
    for parser in [
        try_parse_complete_extended,
        try_parse_complete_basic,
        try_parse_minute_extended,
        try_parse_minute_basic,
        try_parse_hour,
    ] {
        if let Some(parsed) = parser(timestring, offset) {
            return Ok(parsed);
        }
    }
    Err(iso_error("time", timestring))
}

fn midnight() -> IsoTime {
    IsoTime {
        hour: 0,
        minute: 0,
        second: 0,
        microsecond: 0,
        timezone: None,
    }
}

fn month_number(month: &str) -> Option<u8> {
    let lower = month.trim_end_matches(',').to_ascii_lowercase();
    match lower.as_str() {
        "jan" | "january" => Some(1),
        "feb" | "february" => Some(2),
        "mar" | "march" => Some(3),
        "apr" | "april" => Some(4),
        "may" => Some(5),
        "jun" | "june" => Some(6),
        "jul" | "july" => Some(7),
        "aug" | "august" => Some(8),
        "sep" | "sept" | "september" => Some(9),
        "oct" | "october" => Some(10),
        "nov" | "november" => Some(11),
        "dec" | "december" => Some(12),
        _ => None,
    }
}

fn ampm_hour(hour: u8, marker: &str) -> Option<u8> {
    if !(1..=12).contains(&hour) {
        return None;
    }
    match marker.to_ascii_lowercase().as_str() {
        "am" => Some(if hour == 12 { 0 } else { hour }),
        "pm" => Some(if hour == 12 { 12 } else { hour + 12 }),
        _ => None,
    }
}

fn parse_ampm_time(time: &str, marker: &str) -> Option<IsoTime> {
    let split = time.find(':')?;
    if split == 0 || split > 2 {
        return None;
    }
    let hour = &time[..split];
    if !all_digits(hour.as_bytes()) {
        return None;
    }
    let mut parsed = parse_time(&format!("{:0>2}{}", hour, &time[split..])).ok()?;
    parsed.hour = ampm_hour(parsed.hour, marker)?;
    Some(parsed)
}

fn parse_month_name_datetime(datetimestring: &str) -> Option<IsoDateTime> {
    let parts: Vec<&str> = datetimestring.split_whitespace().collect();
    if parts.len() < 3 {
        return None;
    }

    let (year, month, day, time_index) = if let Some(month) = month_number(parts[0]) {
        let day = parts[1].trim_end_matches(',');
        let year = parts[2].trim_end_matches(',');
        if !all_digits(day.as_bytes()) || !all_digits(year.as_bytes()) {
            return None;
        }
        (parse_i32_digits(year), month, parse_u8_digits(day), 3usize)
    } else if let Some(month) = month_number(parts[1]) {
        let day = parts[0].trim_end_matches(',');
        let year = parts[2].trim_end_matches(',');
        if !all_digits(day.as_bytes()) || !all_digits(year.as_bytes()) {
            return None;
        }
        (parse_i32_digits(year), month, parse_u8_digits(day), 3usize)
    } else {
        return None;
    };

    let time = if parts.len() == time_index {
        midnight()
    } else if parts.len() == time_index + 1 {
        parse_time(parts[time_index]).ok()?
    } else if parts.len() == time_index + 2 {
        if let Some(time) = parse_ampm_time(parts[time_index], parts[time_index + 1]) {
            time
        } else {
            let mut time_with_tz =
                String::with_capacity(parts[time_index].len() + parts[time_index + 1].len());
            time_with_tz.push_str(parts[time_index]);
            time_with_tz.push_str(parts[time_index + 1]);
            parse_time(&time_with_tz).ok()?
        }
    } else {
        return None;
    };

    Some(IsoDateTime {
        date: IsoDate { year, month, day },
        time,
    })
}

fn looks_like_time_only_datetime(s: &str) -> bool {
    let Some(split) = s.find(':') else {
        return false;
    };
    (split == 1 || split == 2) && all_digits(s[..split].as_bytes())
}

pub fn parse_datetime_with_default_date(
    datetimestring: &str,
    default_date: Option<IsoDate>,
) -> Result<IsoDateTime, String> {
    if !datetimestring.is_ascii() {
        return Err(format!("Unknown string format: {datetimestring}"));
    }
    let trimmed = datetimestring.trim();
    if trimmed.is_empty() {
        return Err(format!("String does not contain a date: {datetimestring}"));
    }

    if let Some((date_part, time_part)) = trimmed.split_once('T') {
        return Ok(IsoDateTime {
            date: parse_date(date_part)
                .map_err(|_| format!("Unknown string format: {datetimestring}"))?,
            time: parse_time(time_part)
                .map_err(|_| format!("Unknown string format: {datetimestring}"))?,
        });
    }

    if let Some((date_part, time_part)) = trimmed.split_once(' ') {
        if date_part
            .as_bytes()
            .first()
            .is_some_and(|b| b.is_ascii_digit())
        {
            if let (Ok(date), Ok(time)) = (parse_date(date_part), parse_time(time_part)) {
                return Ok(IsoDateTime { date, time });
            }
        }
    }

    if let Ok(date) = parse_date(trimmed) {
        return Ok(IsoDateTime {
            date,
            time: midnight(),
        });
    }

    if let Some(parsed) = parse_month_name_datetime(trimmed) {
        return Ok(parsed);
    }

    if looks_like_time_only_datetime(trimmed) {
        if let (Some(date), Ok(time)) = (default_date, parse_time(trimmed)) {
            return Ok(IsoDateTime { date, time });
        }
    }

    Err(format!("Unknown string format: {datetimestring}"))
}

pub fn parse_datetime(datetimestring: &str) -> Result<IsoDateTime, String> {
    parse_datetime_with_default_date(datetimestring, None)
}

fn parse_duration_number(s: &str, pos: usize, designator: u8) -> Option<(usize, &str)> {
    let bytes = s.as_bytes();
    let mut end = pos;
    while end < bytes.len() && is_digit(bytes[end]) {
        end += 1;
    }
    if end == pos {
        return None;
    }
    if end < bytes.len() && (bytes[end] == b'.' || bytes[end] == b',') {
        end += 1;
        let fraction_start = end;
        while end < bytes.len() && is_digit(bytes[end]) {
            end += 1;
        }
        if end == fraction_start {
            return None;
        }
    }
    if end < bytes.len() && bytes[end] == designator {
        Some((end + 1, &s[pos..end]))
    } else {
        None
    }
}

fn decimal_is_zero(value: &str) -> bool {
    value.bytes().all(|b| b == b'0' || b == b'.' || b == b',')
}

fn parse_f64_duration(value: &str) -> Result<f64, String> {
    value
        .replace(',', ".")
        .parse::<f64>()
        .map_err(|_| format!("Unable to parse duration component {value:?}"))
}

fn round_f64_half_even(value: f64) -> Result<i128, String> {
    if !value.is_finite() {
        return Err("Duration value is out of range".to_string());
    }
    let floor = value.floor();
    let fraction = value - floor;
    let rounded = if fraction < 0.5 {
        floor
    } else if fraction > 0.5 {
        floor + 1.0
    } else {
        let floor_i = floor as i128;
        if floor_i % 2 == 0 {
            floor
        } else {
            floor + 1.0
        }
    };
    Ok(rounded as i128)
}

pub fn parse_duration(datestring: &str) -> Result<IsoDuration, String> {
    if !datestring.is_ascii() {
        return Err(format!("Unable to parse duration string {datestring:?}"));
    }
    let bytes = datestring.as_bytes();
    let len = bytes.len();
    let mut pos = 0;
    let mut negative = false;

    if pos < len && (bytes[pos] == b'-' || bytes[pos] == b'+') {
        negative = bytes[pos] == b'-';
        pos += 1;
    }
    if pos >= len || bytes[pos] != b'P' {
        return Err(format!("Unable to parse duration string {datestring:?}"));
    }
    pos += 1;
    if pos >= len || !bytes[pos].is_ascii_alphanumeric() {
        return Err(format!("Unable to parse duration string {datestring:?}"));
    }

    let mut has_year_month = false;
    let mut weeks = 0.0f64;
    let mut days = 0.0f64;
    let mut hours = 0.0f64;
    let mut minutes = 0.0f64;
    let mut seconds = 0.0f64;

    if let Some((next, value)) = parse_duration_number(datestring, pos, b'Y') {
        has_year_month |= !decimal_is_zero(value);
        pos = next;
    }
    if let Some((next, value)) = parse_duration_number(datestring, pos, b'M') {
        has_year_month |= !decimal_is_zero(value);
        pos = next;
    }
    if let Some((next, value)) = parse_duration_number(datestring, pos, b'W') {
        weeks = parse_f64_duration(value)?;
        pos = next;
    }
    if let Some((next, value)) = parse_duration_number(datestring, pos, b'D') {
        days = parse_f64_duration(value)?;
        pos = next;
    }
    if pos < len && bytes[pos] == b'T' {
        pos += 1;
        if let Some((next, value)) = parse_duration_number(datestring, pos, b'H') {
            hours = parse_f64_duration(value)?;
            pos = next;
        }
        if let Some((next, value)) = parse_duration_number(datestring, pos, b'M') {
            minutes = parse_f64_duration(value)?;
            pos = next;
        }
        if let Some((next, value)) = parse_duration_number(datestring, pos, b'S') {
            seconds = parse_f64_duration(value)?;
            pos = next;
        }
    }
    if pos != len {
        return Err(format!("Unable to parse duration string {datestring:?}"));
    }
    if has_year_month {
        return Ok(IsoDuration::HasYearMonth);
    }

    let total = weeks * US_PER_WEEK as f64
        + days * US_PER_DAY as f64
        + hours * US_PER_HOUR as f64
        + minutes * US_PER_MINUTE as f64
        + seconds * US_PER_SECOND as f64;
    let total_microseconds = round_f64_half_even(total)?;
    Ok(IsoDuration::Timedelta {
        total_microseconds: if negative {
            -total_microseconds
        } else {
            total_microseconds
        },
    })
}

pub fn split_timedelta(total_microseconds: i128) -> Result<(i32, i32, i32), String> {
    let days = total_microseconds.div_euclid(US_PER_DAY);
    let remainder = total_microseconds.rem_euclid(US_PER_DAY);
    let seconds = remainder / US_PER_SECOND;
    let microseconds = remainder % US_PER_SECOND;
    if days < i128::from(i32::MIN) || days > i128::from(i32::MAX) {
        return Err("Duration value is out of range".to_string());
    }
    Ok((days as i32, seconds as i32, microseconds as i32))
}

pub fn duration_isoformat(days: i32, seconds: i32, microseconds: i32) -> String {
    let total = (i128::from(days) * 86_400 + i128::from(seconds)) * US_PER_SECOND
        + i128::from(microseconds);
    let mut remaining = total.abs();
    let mut ret = String::new();
    if total < 0 {
        ret.push('-');
    }
    ret.push('P');

    let duration_days = remaining / US_PER_DAY;
    remaining %= US_PER_DAY;
    let hours = remaining / US_PER_HOUR;
    remaining %= US_PER_HOUR;
    let minutes = remaining / US_PER_MINUTE;
    remaining %= US_PER_MINUTE;
    let duration_seconds = remaining / US_PER_SECOND;
    let duration_microseconds = remaining % US_PER_SECOND;

    let mut has_component = false;
    if duration_days != 0 {
        ret.push_str(&duration_days.to_string());
        ret.push('D');
        has_component = true;
    }
    if hours != 0 || minutes != 0 || duration_seconds != 0 || duration_microseconds != 0 {
        ret.push('T');
        if hours != 0 {
            ret.push_str(&hours.to_string());
            ret.push('H');
        }
        if minutes != 0 {
            ret.push_str(&minutes.to_string());
            ret.push('M');
        }
        if duration_seconds != 0 || duration_microseconds != 0 {
            if duration_microseconds != 0 {
                let mut fraction = format!("{duration_microseconds:06}");
                while fraction.ends_with('0') {
                    fraction.pop();
                }
                ret.push_str(&duration_seconds.to_string());
                ret.push('.');
                ret.push_str(&fraction);
            } else {
                ret.push_str(&duration_seconds.to_string());
            }
            ret.push('S');
        }
        has_component = true;
    }
    if !has_component {
        ret.push_str("0D");
    }
    ret
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_isodate_date_formats_used_by_chalk() {
        let cases = [
            (
                "2024-02-29",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 29,
                },
            ),
            (
                "20240229",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 29,
                },
            ),
            (
                "2024-060",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 29,
                },
            ),
            (
                "2024060",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 29,
                },
            ),
            (
                "2024-W01-1",
                IsoDate {
                    year: 2024,
                    month: 1,
                    day: 1,
                },
            ),
            (
                "2024W011",
                IsoDate {
                    year: 2024,
                    month: 1,
                    day: 1,
                },
            ),
            (
                "2024-W01",
                IsoDate {
                    year: 2024,
                    month: 1,
                    day: 1,
                },
            ),
            (
                "2024W01",
                IsoDate {
                    year: 2024,
                    month: 1,
                    day: 1,
                },
            ),
            (
                "2024-02",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 1,
                },
            ),
            (
                "202402",
                IsoDate {
                    year: 2024,
                    month: 2,
                    day: 1,
                },
            ),
            (
                "2024",
                IsoDate {
                    year: 2024,
                    month: 1,
                    day: 1,
                },
            ),
            (
                "20",
                IsoDate {
                    year: 2001,
                    month: 1,
                    day: 1,
                },
            ),
        ];
        for (input, expected) in cases {
            assert_eq!(parse_date(input).unwrap(), expected, "{input}");
        }
    }

    #[test]
    fn parses_isodate_time_formats_used_by_chalk() {
        assert_eq!(
            parse_time("12:34:56.1234569").unwrap(),
            IsoTime {
                hour: 12,
                minute: 34,
                second: 56,
                microsecond: 123_456,
                timezone: None,
            }
        );
        assert_eq!(
            parse_time("12:34.5").unwrap(),
            IsoTime {
                hour: 12,
                minute: 34,
                second: 30,
                microsecond: 0,
                timezone: None,
            }
        );
        assert_eq!(
            parse_time("12.999999999").unwrap(),
            IsoTime {
                hour: 12,
                minute: 59,
                second: 59,
                microsecond: 999_996,
                timezone: None,
            }
        );
        assert_eq!(
            parse_time("T12:34:56Z").unwrap().timezone,
            Some(IsoTimezone::Utc)
        );
        assert_eq!(
            parse_time("12:34:56-0330").unwrap().timezone,
            Some(IsoTimezone::Fixed {
                name: "-0330".to_string(),
                seconds: -(3 * 3600 + 30 * 60),
            })
        );
    }

    #[test]
    fn parses_dateutil_datetime_formats_used_by_chalk() {
        let parsed = parse_datetime("2024-01-15T12:30:45+00:00").unwrap();
        assert_eq!(
            parsed,
            IsoDateTime {
                date: IsoDate {
                    year: 2024,
                    month: 1,
                    day: 15,
                },
                time: IsoTime {
                    hour: 12,
                    minute: 30,
                    second: 45,
                    microsecond: 0,
                    timezone: Some(IsoTimezone::Fixed {
                        name: "+00:00".to_string(),
                        seconds: 0,
                    }),
                },
            }
        );
        assert_eq!(
            parse_datetime("2023-01-25 17:31:40.074654").unwrap(),
            IsoDateTime {
                date: IsoDate {
                    year: 2023,
                    month: 1,
                    day: 25,
                },
                time: IsoTime {
                    hour: 17,
                    minute: 31,
                    second: 40,
                    microsecond: 74_654,
                    timezone: None,
                },
            }
        );
        assert_eq!(
            parse_datetime("January 15 2024 12:30:45").unwrap(),
            IsoDateTime {
                date: IsoDate {
                    year: 2024,
                    month: 1,
                    day: 15,
                },
                time: IsoTime {
                    hour: 12,
                    minute: 30,
                    second: 45,
                    microsecond: 0,
                    timezone: None,
                },
            }
        );
        assert_eq!(
            parse_datetime("Jan 29, 2021 7:10:39 PM").unwrap(),
            IsoDateTime {
                date: IsoDate {
                    year: 2021,
                    month: 1,
                    day: 29,
                },
                time: IsoTime {
                    hour: 19,
                    minute: 10,
                    second: 39,
                    microsecond: 0,
                    timezone: None,
                },
            }
        );
        assert_eq!(
            parse_datetime("4 Jul 1976").unwrap(),
            IsoDateTime {
                date: IsoDate {
                    year: 1976,
                    month: 7,
                    day: 4,
                },
                time: IsoTime {
                    hour: 0,
                    minute: 0,
                    second: 0,
                    microsecond: 0,
                    timezone: None,
                },
            }
        );
        let default_date = IsoDate {
            year: 2024,
            month: 1,
            day: 15,
        };
        let parsed = parse_datetime_with_default_date("12:34:56.789", Some(default_date)).unwrap();
        assert_eq!(parsed.date, default_date);
        assert_eq!(
            parsed.time,
            IsoTime {
                hour: 12,
                minute: 34,
                second: 56,
                microsecond: 789_000,
                timezone: None,
            }
        );
        assert_eq!(
            parse_datetime("2023-01-25").unwrap(),
            IsoDateTime {
                date: IsoDate {
                    year: 2023,
                    month: 1,
                    day: 25,
                },
                time: IsoTime {
                    hour: 0,
                    minute: 0,
                    second: 0,
                    microsecond: 0,
                    timezone: None,
                },
            }
        );
    }

    #[test]
    fn parses_isodate_duration_formats_used_by_chalk() {
        assert_eq!(
            parse_duration("P1W2DT3H4M5.1234567S").unwrap(),
            IsoDuration::Timedelta {
                total_microseconds: 9 * US_PER_DAY
                    + 3 * US_PER_HOUR
                    + 4 * US_PER_MINUTE
                    + 5_123_457,
            }
        );
        assert_eq!(
            parse_duration("-PT0.000001S").unwrap(),
            IsoDuration::Timedelta {
                total_microseconds: -1,
            }
        );
        assert_eq!(
            parse_duration("PT0.0000025S").unwrap(),
            IsoDuration::Timedelta {
                total_microseconds: 2,
            }
        );
        assert_eq!(
            parse_duration("PT").unwrap(),
            IsoDuration::Timedelta {
                total_microseconds: 0
            }
        );
        assert_eq!(parse_duration("P1M").unwrap(), IsoDuration::HasYearMonth);
        assert_eq!(
            parse_duration("P0Y0M1D").unwrap(),
            IsoDuration::Timedelta {
                total_microseconds: US_PER_DAY,
            }
        );
    }

    #[test]
    fn formats_timedelta_like_isodate() {
        assert_eq!(duration_isoformat(0, 0, 0), "P0D");
        assert_eq!(duration_isoformat(1, 0, 0), "P1D");
        assert_eq!(duration_isoformat(0, 90 * 60, 0), "PT1H30M");
        assert_eq!(duration_isoformat(0, 0, 1), "PT0.000001S");
        assert_eq!(duration_isoformat(-1, 86_399, 999_999), "-PT0.000001S");
        assert_eq!(duration_isoformat(-2, 3, 4), "-P1DT23H59M56.999996S");
    }
}
