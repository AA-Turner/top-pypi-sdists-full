//! Port of `software.amazon.kinesis.worker.metric.OperatingRange`.

/// Immutable value object holding the max utilization percentage (0-100) allowed
/// for a [`WorkerMetric`](crate::worker::metric::WorkerMetric) before it is
/// considered overloaded.
///
/// Java's Lombok `@Builder` invokes a private constructor that validates the
/// range via `Preconditions.checkArgument`. The port enforces the same
/// invariant in [`OperatingRange::new`] / [`OperatingRange::builder`], which
/// **panic** with the exact Java message `"Invalid maxUtilization value"` on an
/// out-of-range value (Java `IllegalArgumentException`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct OperatingRange {
    max_utilization: i32,
}

impl OperatingRange {
    /// Construct an operating range with the given max utilization percentage.
    ///
    /// # Panics
    /// Panics with `"Invalid maxUtilization value"` if `max_utilization` is not
    /// in `0..=100` (Java `IllegalArgumentException`).
    pub fn new(max_utilization: i32) -> Self {
        if !(0..=100).contains(&max_utilization) {
            panic!("Invalid maxUtilization value");
        }
        Self { max_utilization }
    }

    /// A builder mirroring Java `OperatingRange.builder()`. `build()` runs the
    /// same range validation as [`OperatingRange::new`].
    pub fn builder() -> OperatingRangeBuilder {
        OperatingRangeBuilder::default()
    }

    /// Max utilization percentage allowed for the worker metric (Java
    /// `getMaxUtilization`).
    pub fn max_utilization(&self) -> i32 {
        self.max_utilization
    }
}

/// Builder for [`OperatingRange`], mirroring the Lombok `@Builder`.
#[derive(Debug, Default)]
pub struct OperatingRangeBuilder {
    max_utilization: i32,
}

impl OperatingRangeBuilder {
    /// Set the max utilization percentage.
    pub fn max_utilization(mut self, v: i32) -> Self {
        self.max_utilization = v;
        self
    }

    /// Build the [`OperatingRange`], validating the range (panics on failure).
    pub fn build(self) -> OperatingRange {
        OperatingRange::new(self.max_utilization)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_ranges_build() {
        assert_eq!(
            OperatingRange::builder()
                .max_utilization(0)
                .build()
                .max_utilization(),
            0
        );
        assert_eq!(
            OperatingRange::builder()
                .max_utilization(100)
                .build()
                .max_utilization(),
            100
        );
        assert_eq!(
            OperatingRange::builder()
                .max_utilization(80)
                .build()
                .max_utilization(),
            80
        );
    }

    #[test]
    #[should_panic(expected = "Invalid maxUtilization value")]
    fn negative_panics() {
        OperatingRange::builder().max_utilization(-1).build();
    }

    #[test]
    #[should_panic(expected = "Invalid maxUtilization value")]
    fn over_hundred_panics() {
        OperatingRange::builder().max_utilization(101).build();
    }
}
