use super::{AMOUNT_TOLERANCE, Composition};
use std::ops::{Add, Div, Mul, Sub};

// === Operator Implementations ===

impl Composition {
    /// Helper for Add/Sub: merge rhs into self with given sign (+1 or -1).
    fn merge_with(self, rhs: Self, sign: f64) -> Self {
        let mut result = self.species.clone();
        for (sp, amt) in rhs.species {
            *result.entry(sp).or_insert(0.0) += sign * amt;
        }
        Self {
            species: result
                .into_iter()
                .filter(|(_, amt)| amt.abs() > AMOUNT_TOLERANCE)
                .collect(),
            allow_negative: self.allow_negative || rhs.allow_negative,
        }
    }

    /// Helper for Mul/Div: scale all amounts.
    fn scale(self, factor: f64) -> Self {
        Self {
            species: self
                .species
                .into_iter()
                .map(|(sp, amt)| (sp, amt * factor))
                .filter(|(_, amt)| amt.abs() > AMOUNT_TOLERANCE)
                .collect(),
            allow_negative: self.allow_negative,
        }
    }
}

impl Add for Composition {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        self.merge_with(rhs, 1.0)
    }
}

impl Sub for Composition {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        self.merge_with(rhs, -1.0)
    }
}

impl Mul<f64> for Composition {
    type Output = Self;
    fn mul(self, scalar: f64) -> Self {
        self.scale(scalar)
    }
}

impl Div<f64> for Composition {
    type Output = Self;
    /// Divide all species amounts by a scalar.
    ///
    /// # Panics
    /// Panics if `scalar` is zero or near-zero (< AMOUNT_TOLERANCE).
    fn div(self, scalar: f64) -> Self {
        assert!(
            scalar.abs() >= AMOUNT_TOLERANCE,
            "Cannot divide Composition by zero or near-zero value"
        );
        self.scale(1.0 / scalar)
    }
}

impl Mul<Composition> for f64 {
    type Output = Composition;

    fn mul(self, rhs: Composition) -> Composition {
        rhs * self
    }
}
