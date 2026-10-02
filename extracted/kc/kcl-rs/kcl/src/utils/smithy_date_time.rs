//! SDK `DateTime` ↔ `chrono` conversions.
//!
//! Replaces the `aws-smithy-types-convert` crate (its `DateTimeExt` trait was
//! the only thing we used). The implementations mirror that crate exactly so
//! the conversion semantics are unchanged.

use aws_smithy_types::DateTime;
use chrono::Utc;

/// SDK `DateTime` → `chrono::DateTime<Utc>`.
///
/// Mirrors `aws_smithy_types_convert::date_time::DateTimeExt::to_chrono_utc`
/// (modulo the error type): `None` when the seconds are out of chrono's range
/// or the nanoseconds are invalid.
pub(crate) fn to_chrono_utc(value: &DateTime) -> Option<chrono::DateTime<Utc>> {
    chrono::DateTime::from_timestamp(value.secs(), value.subsec_nanos())
}

/// `chrono::DateTime<Utc>` → SDK `DateTime`.
///
/// Mirrors `aws_smithy_types_convert::date_time::DateTimeExt::from_chrono_utc`.
pub(crate) fn from_chrono_utc(value: chrono::DateTime<Utc>) -> DateTime {
    DateTime::from_secs_and_nanos(value.timestamp(), value.timestamp_subsec_nanos())
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn round_trips_with_subsecond_precision() {
        let chrono_ts = Utc.with_ymd_and_hms(2024, 5, 17, 12, 34, 56).unwrap()
            + chrono::Duration::nanoseconds(123_456_789);
        let smithy = from_chrono_utc(chrono_ts);
        assert_eq!(smithy.secs(), chrono_ts.timestamp());
        assert_eq!(smithy.subsec_nanos(), 123_456_789);
        assert_eq!(to_chrono_utc(&smithy), Some(chrono_ts));
    }

    #[test]
    fn pre_epoch_round_trip() {
        let smithy = DateTime::from_secs_and_nanos(-1, 500_000_000);
        let chrono_ts = to_chrono_utc(&smithy).unwrap();
        assert_eq!(from_chrono_utc(chrono_ts), smithy);
    }

    #[test]
    fn out_of_range_seconds_is_none() {
        // chrono::DateTime cannot represent i64::MAX seconds.
        assert_eq!(to_chrono_utc(&DateTime::from_secs(i64::MAX)), None);
    }
}
