//! Port of `software.amazon.kinesis.common.CommonCalculations`.

/// Convenience method for calculating renewer/taker intervals in milliseconds.
///
/// Port of `CommonCalculations.getRenewerTakerIntervalMillis`.
pub fn get_renewer_taker_interval_millis(lease_duration_millis: i64, epsilon_millis: i64) -> i64 {
    lease_duration_millis / 3 - epsilon_millis
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn interval_is_third_minus_epsilon() {
        assert_eq!(get_renewer_taker_interval_millis(30_000, 25), 9_975);
    }
}
