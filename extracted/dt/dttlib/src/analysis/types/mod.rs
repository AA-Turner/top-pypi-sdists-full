//! Pipeline data types

use pipelines::complex::c128;
use std::ops::{AddAssign, DivAssign, SubAssign};

#[cfg(any(feature = "python-pipe", feature = "python"))]
use pyo3::pyclass;

pub mod frequency_domain_array;
pub mod linear;
pub(crate) mod math_traits;
pub mod time_domain_array;

/// Allows some math operations on TimeDomain array types
pub trait Scalar:
    Default + Copy + Clone + AddAssign<Self> + DivAssign<Self> + From<f64> + SubAssign<Self> + 'static
{
}

impl Scalar for f64 {}
impl Scalar for c128 {}

/// Allows a value to track some accumulation statistics
#[derive(Clone, Copy, Debug)]
#[cfg_attr(
    any(feature = "python-pipe", feature = "python"),
    pyclass(get_all, frozen)
)]
pub struct AccumulationStats {
    /// size of accumulation
    pub n: f64,
    pub sequence_index: usize,
    pub sequence_size: usize,
}

impl Default for AccumulationStats {
    fn default() -> Self {
        Self {
            n: 1.0,
            sequence_index: 0,
            sequence_size: 0,
        }
    }
}

pub trait Accumulation: Sized {
    fn set_accumulation_stats(&self, stats: AccumulationStats) -> Self;

    fn get_accumulation_stats(&self) -> &AccumulationStats;

    fn set_sequence_values(&mut self, sequence_index: usize, sequence_size: usize) -> Self {
        let mut stats = self.get_accumulation_stats().clone();
        stats.sequence_index = sequence_index;
        stats.sequence_size = sequence_size;
        self.set_accumulation_stats(stats)
    }
}

pub trait MutableAccumulation: Accumulation {
    fn set_mut_accumulation_stats(&mut self, stats: AccumulationStats);

    fn set_mut_sequence_values(&mut self, sequence_index: usize, sequence_size: usize) {
        let mut stats = self.get_accumulation_stats().clone();
        stats.sequence_index = sequence_index;
        stats.sequence_size = sequence_size;
        self.set_mut_accumulation_stats(stats)
    }
}
