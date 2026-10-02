//! Port of `software.amazon.kinesis.utils.ExponentialMovingAverage`.

/// Simple [exponential moving average][ema].
///
/// Values of `alpha` close to `1` have less of a smoothing effect and give
/// greater weight to recent changes in the data, while values closer to `0`
/// have a greater smoothing effect and are less responsive to recent changes.
///
/// The first value added seeds the average verbatim; subsequent values are
/// blended as `alpha * new + (1 - alpha) * previous`.
///
/// [ema]: https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
#[derive(Debug, Clone)]
pub struct ExponentialMovingAverage {
    alpha: f64,
    value: f64,
    initialized: bool,
}

impl ExponentialMovingAverage {
    /// Create an EMA with the given smoothing factor (Java
    /// `@RequiredArgsConstructor` over `alpha`; `value` defaults to `0.0` and
    /// `initialized` to `false`).
    pub fn new(alpha: f64) -> Self {
        Self {
            alpha,
            value: 0.0,
            initialized: false,
        }
    }

    /// Add a new sample, updating the current average.
    pub fn add(&mut self, new_value: f64) {
        if !self.initialized {
            self.value = new_value;
            self.initialized = true;
        } else {
            self.value = self.alpha * new_value + (1.0 - self.alpha) * self.value;
        }
    }

    /// The current smoothed value (Java `@Getter double value`).
    pub fn value(&self) -> f64 {
        self.value
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn first_value_seeds_average() {
        let mut ema = ExponentialMovingAverage::new(0.5);
        assert_eq!(ema.value(), 0.0);
        ema.add(10.0);
        assert_eq!(ema.value(), 10.0);
    }

    #[test]
    fn subsequent_values_are_blended_alpha_half() {
        let mut ema = ExponentialMovingAverage::new(0.5);
        ema.add(10.0);
        ema.add(20.0);
        // 0.5 * 20 + 0.5 * 10 = 15
        assert_eq!(ema.value(), 15.0);
        ema.add(0.0);
        // 0.5 * 0 + 0.5 * 15 = 7.5
        assert_eq!(ema.value(), 7.5);
    }

    #[test]
    fn alpha_close_to_one_tracks_recent() {
        let mut ema = ExponentialMovingAverage::new(0.9);
        ema.add(100.0);
        ema.add(0.0);
        // 0.9 * 0 + 0.1 * 100 = 10
        assert!((ema.value() - 10.0).abs() < 1e-9);
    }
}
