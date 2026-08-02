//! Units of measurement
//! These are tracked along with data items
use num::Rational64;
use num_traits::Pow;
use std::{
    collections::{HashMap, HashSet},
    fmt::Display,
    ops::{Div, Mul},
};

#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::pyclass;
#[cfg(feature = "all")]
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyclass_complex_enum};

/// allow some standard units
/// to take care of custom string generation
/// and handling of slightly different unit names for the same units
/// and, potentially for some automatic conversion.
#[cfg_attr(feature = "all", gen_stub_pyclass_complex_enum)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, str, hash, eq)
)]
#[derive(Debug, Clone, Hash, Eq, PartialEq)]
pub enum SimpleUnit {
    // default given to channels without a unit
    Counts(),
    // custom type names are identified by their exact string.
    Custom(String),
}

impl Display for SimpleUnit {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Counts() => f.write_str("counts"),
            Self::Custom(n) => f.write_str(n),
        }
    }
}

impl From<String> for SimpleUnit {
    fn from(value: String) -> Self {
        Self::Custom(value)
    }
}

impl Default for SimpleUnit {
    fn default() -> Self {
        Self::Counts()
    }
}

/// map a simple unit to a rational power
#[derive(Debug, Clone, Eq, PartialEq, Default)]
#[cfg_attr(feature = "all", gen_stub_pyclass)]
#[cfg_attr(
    any(feature = "python", feature = "python-pipe"),
    pyclass(frozen, str, eq)
)]
pub struct Unit(HashMap<SimpleUnit, Rational64>);

impl Display for Unit {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for (u, p) in self.0.iter() {
            u.fmt(f)?;
            if *p != Rational64::new(1, 1) {
                write!(f, "^({})", p)?;
            } else {
                f.write_str(" ")?;
            }
        }

        Ok(())
    }
}

impl Mul<&Unit> for &Unit {
    type Output = Unit;

    fn mul(self, rhs: &Unit) -> Self::Output {
        let left_keys: HashSet<_> = self.0.keys().cloned().collect();
        let right_keys: HashSet<_> = rhs.0.keys().cloned().collect();
        let new_map: HashMap<_, _> = left_keys
            .union(&right_keys)
            .map(|x| {
                let p1 = self.0.get(x).unwrap_or(&Rational64::new(0, 1)).clone();
                let p2 = rhs.0.get(x).unwrap_or(&Rational64::new(0, 1)).clone();
                (x.clone(), p1 + p2)
            })
            .filter(|(_x, p)| *p != Rational64::new(0, 1))
            .collect();

        Unit(new_map)
    }
}

impl Mul<Unit> for Unit {
    type Output = Unit;

    fn mul(self, rhs: Unit) -> Self::Output {
        &self * &rhs
    }
}

impl Mul<&Unit> for Unit {
    type Output = Unit;

    fn mul(self, rhs: &Unit) -> Self::Output {
        &self * rhs
    }
}

impl Mul<Unit> for &Unit {
    type Output = Unit;

    fn mul(self, rhs: Unit) -> Self::Output {
        self * &rhs
    }
}

impl Div<&Unit> for &Unit {
    type Output = Unit;

    fn div(self, rhs: &Unit) -> Self::Output {
        self.mul(&rhs.pow(-1))
    }
}

impl Div<Unit> for Unit {
    type Output = Unit;

    fn div(self, rhs: Unit) -> Self::Output {
        &self / &rhs
    }
}

impl Div<&Unit> for Unit {
    type Output = Unit;

    fn div(self, rhs: &Unit) -> Self::Output {
        &self / rhs
    }
}

impl Div<Unit> for &Unit {
    type Output = Unit;

    fn div(self, rhs: Unit) -> Self::Output {
        self / &rhs
    }
}

impl Pow<&Rational64> for &Unit {
    type Output = Unit;

    fn pow(self, rhs: &Rational64) -> Self::Output {
        let new_map = self.0.iter().map(|(u, p)| (u.clone(), p * *rhs)).collect();

        Unit(new_map)
    }
}

impl Pow<i64> for &Unit {
    type Output = Unit;

    fn pow(self, rhs: i64) -> Self::Output {
        self.pow(&Rational64::new(rhs, 1))
    }
}

impl Unit {
    /// make the unit have the nth root
    pub fn root(&self, rhs: i64) -> Self {
        self.pow(&Rational64::new(1, rhs))
    }
}

impl From<SimpleUnit> for Unit {
    fn from(value: SimpleUnit) -> Self {
        let mut new_map = HashMap::with_capacity(1);
        new_map.insert(value, Rational64::new(1, 1));
        Self(new_map)
    }
}

impl<T> From<T> for Unit
where
    T: Into<String>,
{
    fn from(value: T) -> Self {
        let s: String = value.into();
        let su: SimpleUnit = s.into();
        su.into()
    }
}
