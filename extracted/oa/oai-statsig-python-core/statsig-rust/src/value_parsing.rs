use chrono::{DateTime, NaiveDate, NaiveDateTime};

pub(crate) fn try_parse_timestamp(value: &str, parsed_i64: Option<i64>) -> Option<i64> {
    let first = *value.as_bytes().first()?;
    if !(first.is_ascii_digit() || matches!(first, b'+' | b'-')) {
        return None;
    }

    if let Some(value) = parsed_i64 {
        return Some(value);
    }

    if value.len() < 8
        || value.len() > 20
        || (!value.contains('-') && !value.contains('T') && !value.contains(':'))
    {
        return None;
    }

    if let Ok(value) = DateTime::parse_from_rfc3339(value) {
        return Some(value.timestamp_millis());
    }

    if let Ok(value) = NaiveDateTime::parse_from_str(value, "%Y-%m-%d %H:%M:%S") {
        return Some(value.and_utc().timestamp_millis());
    }

    if let Ok(value) = NaiveDate::parse_from_str(value, "%Y-%m-%d") {
        return value
            .and_hms_opt(0, 0, 0)
            .map(|value| value.and_utc().timestamp_millis());
    }

    None
}

pub(crate) fn maybe_parse_i64(value: &str) -> Option<i64> {
    let first = *value.as_bytes().first()?;
    if !(first.is_ascii_digit() || matches!(first, b'+' | b'-')) {
        return None;
    }

    value.parse().ok()
}

pub(crate) fn maybe_parse_f64(value: &str) -> Option<f64> {
    let first = *value.as_bytes().first()?;
    if !(first.is_ascii_digit() || matches!(first, b'+' | b'-' | b'.' | b'i' | b'I' | b'n' | b'N'))
    {
        return None;
    }

    value.parse().ok()
}
