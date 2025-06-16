use pyo3::prelude::*;
use serde::{Serialize, Deserialize};

/// Unit‐only Distance enum for simple metrics.
#[pyclass]
#[derive(Clone, Copy, Serialize, Deserialize, Debug)]
pub enum Distance {
    /// Euclidean (L2)
    Euclidean,
    /// Cosine
    Cosine,
    /// Manhattan (L1)
    Manhattan,
    /// Chebyshev (L∞)
    Chebyshev,
}

#[pymethods]
impl Distance {
    #[classattr] pub const EUCLIDEAN: Distance = Distance::Euclidean;
    #[classattr] pub const COSINE:    Distance = Distance::Cosine;
    #[classattr] pub const MANHATTAN: Distance = Distance::Manhattan;
    #[classattr] pub const CHEBYSHEV: Distance = Distance::Chebyshev;

    fn __repr__(&self) -> &'static str {
        match self {
            Distance::Euclidean => "Distance.EUCLIDEAN",
            Distance::Cosine    => "Distance.COSINE",
            Distance::Manhattan => "Distance.MANHATTAN",
            Distance::Chebyshev => "Distance.CHEBYSHEV",
        }
    }
}
