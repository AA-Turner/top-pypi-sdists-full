use chrono::{DateTime, Utc};
use pyo3::prelude::*;
use taskchampion::Annotation as TCAnnotation;

#[pyclass(from_py_object, frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq)]
/// An annotation for the task
pub struct Annotation(TCAnnotation);

impl std::hash::Hash for Annotation {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.0.entry.hash(state);
        self.0.description.hash(state);
    }
}

#[pymethods]
impl Annotation {
    #[new]
    pub fn new(entry: DateTime<Utc>, description: String) -> Self {
        Annotation(TCAnnotation { entry, description })
    }

    pub fn __repr__(&self) -> String {
        format!(
            "Annotation(entry={:?}, description={:?})",
            self.0.entry.to_rfc3339(),
            self.0.description,
        )
    }

    #[getter]
    pub fn entry(&self) -> DateTime<Utc> {
        self.0.entry
    }

    #[getter]
    pub fn description(&self) -> String {
        self.0.description.clone()
    }
}

impl AsRef<TCAnnotation> for Annotation {
    fn as_ref(&self) -> &TCAnnotation {
        &self.0
    }
}

impl From<TCAnnotation> for Annotation {
    fn from(value: TCAnnotation) -> Self {
        Annotation(value)
    }
}

impl From<Annotation> for TCAnnotation {
    fn from(value: Annotation) -> Self {
        value.0
    }
}
