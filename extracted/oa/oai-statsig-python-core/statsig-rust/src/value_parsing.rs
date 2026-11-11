use chrono::{DateTime, NaiveDate, NaiveDateTime};

#[inline]
pub(crate) fn parse_string_values(value: &str) -> (Option<i64>, Option<f64>, Option<i64>) {
    match value.as_bytes().first() {
        Some(b'0'..=b'9' | b'+' | b'-') => parse_number_or_date(value),
        Some(b'.' | b'i' | b'I' | b'n' | b'N') => (None, value.parse().ok(), None),
        _ => (None, None, None),
    }
}

// Keep numeric and date parser setup off the common text path.
#[inline(never)]
fn parse_number_or_date(value: &str) -> (Option<i64>, Option<f64>, Option<i64>) {
    let int_value = value.parse().ok();
    let timestamp_value = int_value.or_else(|| parse_date(value));
    (int_value, value.parse().ok(), timestamp_value)
}

fn parse_date(value: &str) -> Option<i64> {
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
