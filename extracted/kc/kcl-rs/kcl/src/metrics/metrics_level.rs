//! Port of `software.amazon.kinesis.metrics.MetricsLevel`.

/// Standard metrics levels controlling which metrics get emitted.
///
/// Levels are ordered by an integer `value`. Enabling metrics at a given level
/// also enables all *higher* levels. Critically, the numeric ordering is
/// **inverted** relative to verbosity: `DETAILED(9000) < SUMMARY(10000) <
/// NONE(i32::MAX)`. Filtering elsewhere uses `data_level.value() <
/// enabled_level.value()` to decide to drop, so enabling `SUMMARY` drops
/// `DETAILED` data (9000 < 10000) but keeps `SUMMARY`, and `NONE` drops
/// everything (nothing has `value >= i32::MAX` except another `NONE` datum).
///
/// Port of the Java `enum` with `(name, value)`; `NONE` uses `Integer.MAX_VALUE`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MetricsLevel {
    /// Turns off all metrics.
    None,
    /// Only the most significant metrics.
    Summary,
    /// All metrics.
    Detailed,
}

impl MetricsLevel {
    /// The name of the metrics level (Java `getName`).
    pub fn name(&self) -> &'static str {
        match self {
            MetricsLevel::None => "NONE",
            MetricsLevel::Summary => "SUMMARY",
            MetricsLevel::Detailed => "DETAILED",
        }
    }

    /// The integer value of the metrics level (Java `getValue`).
    ///
    /// `NONE` maps to `i32::MAX` (Java `Integer.MAX_VALUE`).
    pub fn value(&self) -> i32 {
        match self {
            MetricsLevel::None => i32::MAX,
            MetricsLevel::Summary => 10000,
            MetricsLevel::Detailed => 9000,
        }
    }

    /// Returns the metrics level associated with the given name (Java
    /// `fromName`).
    ///
    /// The lookup is case-insensitive (the input is upper-cased first) and then
    /// matched exactly against an enum name, mirroring Java's
    /// `Enum.valueOf(toUpperCase(name))`. Java throws
    /// `IllegalArgumentException` on an unknown name (and `NullPointerException`
    /// on `null`); the Rust port returns `None` so callers can decide, and a
    /// panicking convenience is provided by [`from_name`](Self::from_name).
    pub fn try_from_name(name: &str) -> Option<MetricsLevel> {
        match name.to_uppercase().as_str() {
            "NONE" => Some(MetricsLevel::None),
            "SUMMARY" => Some(MetricsLevel::Summary),
            "DETAILED" => Some(MetricsLevel::Detailed),
            _ => None,
        }
    }

    /// Returns the metrics level for `name`, panicking on an unknown name.
    ///
    /// Mirrors Java `fromName`, which throws `IllegalArgumentException` via
    /// `Enum.valueOf` for an unrecognized name.
    pub fn from_name(name: &str) -> MetricsLevel {
        MetricsLevel::try_from_name(name)
            .unwrap_or_else(|| panic!("No enum constant MetricsLevel.{}", name.to_uppercase()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ordering_is_inverted_relative_to_verbosity() {
        assert!(MetricsLevel::Detailed.value() < MetricsLevel::Summary.value());
        assert!(MetricsLevel::Summary.value() < MetricsLevel::None.value());
        assert_eq!(MetricsLevel::None.value(), i32::MAX);
        assert_eq!(MetricsLevel::Summary.value(), 10000);
        assert_eq!(MetricsLevel::Detailed.value(), 9000);
    }

    #[test]
    fn names_round_trip() {
        assert_eq!(MetricsLevel::None.name(), "NONE");
        assert_eq!(MetricsLevel::Summary.name(), "SUMMARY");
        assert_eq!(MetricsLevel::Detailed.name(), "DETAILED");
    }

    #[test]
    fn from_name_is_case_insensitive() {
        assert_eq!(MetricsLevel::from_name("detailed"), MetricsLevel::Detailed);
        assert_eq!(MetricsLevel::from_name("Summary"), MetricsLevel::Summary);
        assert_eq!(MetricsLevel::from_name("NONE"), MetricsLevel::None);
    }

    #[test]
    #[should_panic(expected = "No enum constant MetricsLevel.BOGUS")]
    fn from_name_panics_on_unknown() {
        MetricsLevel::from_name("bogus");
    }
}
