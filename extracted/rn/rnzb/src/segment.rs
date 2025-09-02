use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

use crate::repr::PyRepr;

#[pyclass(module = "rnzb", frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct Segment(nzb_rs::Segment);

impl From<nzb_rs::Segment> for Segment {
    fn from(s: nzb_rs::Segment) -> Self {
        Self(s)
    }
}

impl From<Segment> for nzb_rs::Segment {
    fn from(s: Segment) -> Self {
        Self {
            size: s.size(),
            number: s.number(),
            message_id: s.message_id().to_owned(),
        }
    }
}

impl PyRepr for Segment {
    fn pyrepr(&self) -> String {
        format!(
            "Segment(size={}, number={}, message_id={})",
            self.size().pyrepr(),
            self.number().pyrepr(),
            self.message_id().pyrepr()
        )
    }
}

#[pymethods]
impl Segment {
    #[new]
    #[pyo3(signature = (*, size, number, message_id))]
    pub fn __new__(size: u32, number: u32, message_id: String) -> Self {
        Self(nzb_rs::Segment {
            size,
            number,
            message_id,
        })
    }

    #[getter]
    pub fn size(&self) -> u32 {
        self.0.size
    }

    #[getter]
    pub fn number(&self) -> u32 {
        self.0.number
    }

    #[getter]
    pub fn message_id(&self) -> &str {
        &self.0.message_id
    }

    pub fn __repr__(&self) -> String {
        self.pyrepr()
    }
}
