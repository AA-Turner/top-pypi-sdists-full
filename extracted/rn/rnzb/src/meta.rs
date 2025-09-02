use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

use crate::{repr::PyRepr, tuple::Tuple};

#[pyclass(module = "rnzb", frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct Meta(nzb_rs::Meta);

impl From<nzb_rs::Meta> for Meta {
    fn from(m: nzb_rs::Meta) -> Self {
        Self(m)
    }
}

impl From<Meta> for nzb_rs::Meta {
    fn from(m: Meta) -> Self {
        Self {
            title: m.title(),
            passwords: m.passwords().into(),
            tags: m.tags().into(),
            category: m.category(),
        }
    }
}

impl PyRepr for Meta {
    fn pyrepr(&self) -> String {
        format!(
            "Meta(title={}, passwords={}, tags={}, category={})",
            self.title().pyrepr(),
            self.passwords().pyrepr(),
            self.tags().pyrepr(),
            self.category().pyrepr()
        )
    }
}

#[pymethods]
impl Meta {
    #[new]
    #[pyo3(signature = (*, title=None, passwords=Vec::new(), tags=Vec::new(), category=None))]
    pub fn __new__(
        title: Option<String>,
        passwords: Vec<String>,
        tags: Vec<String>,
        category: Option<String>,
    ) -> Self {
        Self(nzb_rs::Meta {
            title,
            passwords,
            tags,
            category,
        })
    }

    #[getter]
    pub fn title(&self) -> Option<String> {
        self.0.title.clone()
    }

    #[getter]
    pub fn passwords(&self) -> Tuple<String> {
        self.0.passwords.clone().into()
    }

    #[getter]
    pub fn tags(&self) -> Tuple<String> {
        self.0.tags.clone().into()
    }

    #[getter]
    pub fn category(&self) -> Option<String> {
        self.0.category.clone()
    }

    pub fn __repr__(&self) -> String {
        self.pyrepr()
    }
}
