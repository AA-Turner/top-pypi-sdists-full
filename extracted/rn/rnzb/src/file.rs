use crate::{segment::Segment, tuple::Tuple};
use chrono::{DateTime, Utc};
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

use crate::repr::PyRepr;

// Python wrapper class for File
#[pyclass(module = "rnzb", frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct File(nzb_rs::File);

impl From<nzb_rs::File> for File {
    fn from(f: nzb_rs::File) -> Self {
        Self(f)
    }
}

impl From<File> for nzb_rs::File {
    fn from(f: File) -> Self {
        Self {
            poster: f.poster().to_owned(),
            posted_at: f.posted_at(),
            subject: f.subject().to_owned(),
            groups: f.groups().into(),
            segments: f.segments().0.into_iter().map(Into::into).collect(),
        }
    }
}

impl PyRepr for File {
    fn pyrepr(&self) -> String {
        format!(
            "File(poster={}, posted_at={}, subject={}, groups={}, segments={})",
            self.poster().pyrepr(),
            self.posted_at().pyrepr(),
            self.subject().pyrepr(),
            self.groups().pyrepr(),
            self.segments().pyrepr(),
        )
    }
}

#[pymethods]
impl File {
    #[new]
    #[pyo3(signature = (*, poster, posted_at, subject, groups, segments))]
    pub fn __new__(
        poster: String,
        posted_at: DateTime<Utc>,
        subject: String,
        groups: Vec<String>,
        segments: Vec<Segment>,
    ) -> Self {
        Self(nzb_rs::File {
            poster,
            posted_at,
            subject,
            groups,
            segments: segments.into_iter().map(Into::into).collect(),
        })
    }

    fn __repr__(&self) -> String {
        self.pyrepr()
    }

    #[getter]
    pub fn poster(&self) -> &str {
        &self.0.poster
    }

    #[getter]
    pub fn posted_at(&self) -> DateTime<Utc> {
        self.0.posted_at
    }

    #[getter]
    pub fn subject(&self) -> &str {
        &self.0.subject
    }

    #[getter]
    pub fn groups(&self) -> Tuple<String> {
        self.0.groups.clone().into()
    }

    #[getter]
    pub fn segments(&self) -> Tuple<Segment> {
        self.0
            .segments
            .clone()
            .into_iter()
            .map(Into::into)
            .collect::<Vec<Segment>>()
            .into()
    }

    #[getter]
    pub fn size(&self) -> u64 {
        self.0.size()
    }

    #[getter]
    pub fn name(&self) -> Option<&str> {
        self.0.name()
    }

    #[getter]
    pub fn stem(&self) -> Option<&str> {
        self.0.stem()
    }

    #[getter]
    pub fn extension(&self) -> Option<&str> {
        self.0.extension()
    }

    #[pyo3(signature = (ext, /))]
    pub fn has_extension(&self, ext: &str) -> bool {
        self.0.has_extension(ext)
    }

    pub fn is_par2(&self) -> bool {
        self.0.is_par2()
    }

    pub fn is_rar(&self) -> bool {
        self.0.is_rar()
    }

    pub fn is_obfuscated(&self) -> bool {
        self.0.is_obfuscated()
    }
}
