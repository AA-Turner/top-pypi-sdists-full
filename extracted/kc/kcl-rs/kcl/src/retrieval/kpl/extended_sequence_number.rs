//! Port of `software.amazon.kinesis.retrieval.kpl.ExtendedSequenceNumber`.

use std::cmp::Ordering;

use num_bigint::BigInt;

use crate::checkpoint::SentinelCheckpoint;

/// Represents a two-part sequence number for records aggregated by the Kinesis
/// Producer Library (KPL).
///
/// The KPL combines multiple user records into a single Kinesis record; each
/// user record therefore has an integer sub-sequence number in addition to the
/// Kinesis record's sequence number.
///
/// # Ordering vs. equality
///
/// Like the Java class, [`Ord`] (`compareTo`) and [`PartialEq`] (`equals`) are
/// **intentionally inconsistent**: equality compares the raw
/// `(sequence_number, sub_sequence_number)` fields, while ordering compares the
/// numeric ([`BigInt`]) value of the sequence number. Thus `"007"` and `"7"`
/// are *ordered* equal but *not* equal. This matches Java exactly.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ExtendedSequenceNumber {
    sequence_number: String,
    sub_sequence_number: i64,
}

// Sentinel numeric values: defined to be less than all real sequence numbers.
fn trim_horizon_value() -> BigInt {
    BigInt::from(-2)
}
fn latest_value() -> BigInt {
    BigInt::from(-1)
}
fn at_timestamp_value() -> BigInt {
    BigInt::from(-3)
}

impl ExtendedSequenceNumber {
    /// Construct with an explicit sub-sequence number.
    ///
    /// Mirrors the Java `ExtendedSequenceNumber(String, Long)` constructor: a
    /// `None` sub-sequence number defaults to `0`.
    pub fn new(sequence_number: impl Into<String>, sub_sequence_number: Option<i64>) -> Self {
        Self {
            sequence_number: sequence_number.into(),
            sub_sequence_number: sub_sequence_number.unwrap_or(0),
        }
    }

    /// Construct with a sub-sequence number of `0`.
    ///
    /// Mirrors the Java `ExtendedSequenceNumber(String)` constructor.
    pub fn from_sequence_number(sequence_number: impl Into<String>) -> Self {
        Self::new(sequence_number, None)
    }

    /// Special value for `LATEST`.
    pub fn latest() -> Self {
        Self::from_sequence_number(SentinelCheckpoint::Latest.as_str())
    }

    /// Special value for `SHARD_END`.
    pub fn shard_end() -> Self {
        Self::from_sequence_number(SentinelCheckpoint::ShardEnd.as_str())
    }

    /// Special value for `TRIM_HORIZON`.
    pub fn trim_horizon() -> Self {
        Self::from_sequence_number(SentinelCheckpoint::TrimHorizon.as_str())
    }

    /// Special value for `AT_TIMESTAMP`.
    pub fn at_timestamp() -> Self {
        Self::from_sequence_number(SentinelCheckpoint::AtTimestamp.as_str())
    }

    /// The sequence number of the Kinesis record.
    pub fn sequence_number(&self) -> &str {
        &self.sequence_number
    }

    /// The sub-sequence number of the user record within the enclosing Kinesis record.
    pub fn sub_sequence_number(&self) -> i64 {
        self.sub_sequence_number
    }

    /// Whether this refers to the end of the shard.
    pub fn is_shard_end(&self) -> bool {
        self.sequence_number == SentinelCheckpoint::ShardEnd.as_str()
    }

    /// Whether the sequence number is a [`SentinelCheckpoint`]. Sub-sequence
    /// numbers are ignored when making this determination.
    pub fn is_sentinel_checkpoint(&self) -> bool {
        SentinelCheckpoint::is_sentinel(&self.sequence_number)
    }

    /// Compares this with another using the KCL rules (Java `compareTo`).
    ///
    /// * `SHARD_END` is greatest.
    /// * `TRIM_HORIZON`, `LATEST`, `AT_TIMESTAMP` are less than all real numbers.
    /// * real sequence numbers compare by their [`BigInt`] value, ties broken by
    ///   sub-sequence number.
    ///
    /// # Panics
    /// Panics (mirroring Java's `IllegalArgumentException`) if either value's
    /// sequence number is neither all-digits nor a sentinel value.
    pub fn compare_to(&self, other: &ExtendedSequenceNumber) -> Ordering {
        let first = &self.sequence_number;
        let second = &other.sequence_number;

        if !is_digits_or_sentinel(self) || !is_digits_or_sentinel(other) {
            panic!(
                "Expected a sequence number or a sentinel checkpoint value but received: first={} and second={}",
                first, second
            );
        }

        let shard_end = SentinelCheckpoint::ShardEnd.as_str();
        // SHARD_END is the greatest.
        if first == shard_end && second == shard_end {
            return Ordering::Equal;
        } else if second == shard_end {
            return Ordering::Less;
        } else if first == shard_end {
            return Ordering::Greater;
        }

        let result = big_integer_value(first).cmp(&big_integer_value(second));
        if result == Ordering::Equal {
            self.sub_sequence_number.cmp(&other.sub_sequence_number)
        } else {
            result
        }
    }
}

/// Sequence numbers are converted to their numeric value; sentinels map to
/// negative numbers so they sort before real sequence numbers.
///
/// This is only called after the `SHARD_END` / two-sentinel cases have been
/// handled, matching the Java control flow.
fn big_integer_value(sequence_number: &str) -> BigInt {
    if is_digits(sequence_number) {
        sequence_number
            .parse::<BigInt>()
            .expect("checked by is_digits")
    } else if sequence_number == SentinelCheckpoint::Latest.as_str() {
        latest_value()
    } else if sequence_number == SentinelCheckpoint::TrimHorizon.as_str() {
        trim_horizon_value()
    } else if sequence_number == SentinelCheckpoint::AtTimestamp.as_str() {
        at_timestamp_value()
    } else {
        panic!(
            "Expected a string of digits, TRIM_HORIZON, LATEST or AT_TIMESTAMP but received {}",
            sequence_number
        );
    }
}

fn is_digits_or_sentinel(esn: &ExtendedSequenceNumber) -> bool {
    is_digits(&esn.sequence_number) || esn.is_sentinel_checkpoint()
}

/// True for a non-empty string of only ASCII digits (Java `Character.isDigit`
/// on ASCII sequence numbers). False for empty input.
fn is_digits(s: &str) -> bool {
    !s.is_empty() && s.bytes().all(|b| b.is_ascii_digit())
}

impl Ord for ExtendedSequenceNumber {
    fn cmp(&self, other: &Self) -> Ordering {
        self.compare_to(other)
    }
}

impl PartialOrd for ExtendedSequenceNumber {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl std::fmt::Display for ExtendedSequenceNumber {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        // Mirrors Java toString(): sequence number always non-null here, and
        // sub-sequence number is always >= 0 for constructed values.
        write!(
            f,
            "{{SequenceNumber: {},SubsequenceNumber: {}}}",
            self.sequence_number, self.sub_sequence_number
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_sub_sequence_is_zero() {
        let esn = ExtendedSequenceNumber::from_sequence_number("123");
        assert_eq!(esn.sequence_number(), "123");
        assert_eq!(esn.sub_sequence_number(), 0);
    }

    #[test]
    fn shard_end_is_greatest() {
        let shard_end = ExtendedSequenceNumber::shard_end();
        let big = ExtendedSequenceNumber::from_sequence_number("99999999999999999999999999");
        assert_eq!(shard_end.compare_to(&big), Ordering::Greater);
        assert_eq!(big.compare_to(&shard_end), Ordering::Less);
        assert_eq!(
            shard_end.compare_to(&ExtendedSequenceNumber::shard_end()),
            Ordering::Equal
        );
    }

    #[test]
    fn sentinels_sort_below_real_numbers_in_defined_order() {
        let at_ts = ExtendedSequenceNumber::at_timestamp(); // -3
        let trim = ExtendedSequenceNumber::trim_horizon(); // -2
        let latest = ExtendedSequenceNumber::latest(); // -1
        let zero = ExtendedSequenceNumber::from_sequence_number("0");
        assert_eq!(at_ts.compare_to(&trim), Ordering::Less);
        assert_eq!(trim.compare_to(&latest), Ordering::Less);
        assert_eq!(latest.compare_to(&zero), Ordering::Less);
    }

    #[test]
    fn big_integer_comparison_beyond_u128() {
        let a = ExtendedSequenceNumber::from_sequence_number(
            "100000000000000000000000000000000000000000",
        );
        let b = ExtendedSequenceNumber::from_sequence_number(
            "99999999999999999999999999999999999999999",
        );
        assert_eq!(a.compare_to(&b), Ordering::Greater);
    }

    #[test]
    fn ties_broken_by_sub_sequence_number() {
        let a = ExtendedSequenceNumber::new("100", Some(1));
        let b = ExtendedSequenceNumber::new("100", Some(2));
        assert_eq!(a.compare_to(&b), Ordering::Less);
    }

    #[test]
    fn ordering_and_equality_are_intentionally_inconsistent() {
        let a = ExtendedSequenceNumber::from_sequence_number("007");
        let b = ExtendedSequenceNumber::from_sequence_number("7");
        assert_eq!(a.compare_to(&b), Ordering::Equal); // numeric
        assert_ne!(a, b); // field equality
    }

    #[test]
    #[should_panic(expected = "Expected a sequence number or a sentinel checkpoint value")]
    fn invalid_sequence_number_panics() {
        let bad = ExtendedSequenceNumber::from_sequence_number("not-a-number");
        let good = ExtendedSequenceNumber::from_sequence_number("1");
        let _ = bad.compare_to(&good);
    }

    /// Port of `ExtendedSequenceNumberTest.testSentinelCheckpoints`. Every
    /// sentinel-name sequence number is recognized as a sentinel checkpoint, and
    /// (for backwards-compatibility) a sub-sequence number is ignored when making
    /// that determination.
    #[test]
    fn sentinel_checkpoints() {
        for sentinel in SentinelCheckpoint::ALL {
            let esn = ExtendedSequenceNumber::from_sequence_number(sentinel.as_str());
            assert!(esn.is_sentinel_checkpoint(), "{}", sentinel.as_str());

            let esn_with_subsequence = ExtendedSequenceNumber::new(sentinel.as_str(), Some(42));
            assert!(
                esn_with_subsequence.is_sentinel_checkpoint(),
                "{}",
                sentinel.as_str()
            );
        }
    }
}
