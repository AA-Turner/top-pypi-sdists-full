use crate::exception::InvalidNzbError;
use crate::file::File;
use crate::meta::Meta;
use crate::repr::PyRepr;
use crate::tuple::Tuple;
use pyo3::exceptions::PyFileNotFoundError;
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::io;
use std::path::PathBuf;

#[pyclass(module = "rnzb", frozen, eq, hash)]
#[derive(Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct Nzb(nzb_rs::Nzb);

impl PyRepr for Nzb {
    fn pyrepr(&self) -> String {
        format!(
            "Nzb(meta={}, files={})",
            self.meta().pyrepr(),
            self.files().pyrepr(),
        )
    }
}

#[pymethods]
impl Nzb {
    #[new]
    #[pyo3(signature = (*, meta, files))]
    pub fn __new__(meta: Meta, files: Vec<File>) -> Self {
        Self(nzb_rs::Nzb {
            meta: meta.into(),
            files: files.into_iter().map(Into::into).collect(),
        })
    }

    fn __repr__(&self) -> String {
        self.pyrepr()
    }

    #[getter]
    pub fn meta(&self) -> Meta {
        self.0.meta.clone().into()
    }

    #[getter]
    pub fn files(&self) -> Tuple<File> {
        self.0
            .files
            .clone()
            .into_iter()
            .map(Into::into)
            .collect::<Vec<File>>()
            .into()
    }

    #[staticmethod]
    #[pyo3(signature = (nzb, /))]
    pub fn from_str(nzb: &str) -> PyResult<Self> {
        match nzb_rs::Nzb::parse(nzb) {
            Ok(nzb) => Ok(Self(nzb)),
            Err(e) => Err(InvalidNzbError::new_err(e.to_string())),
        }
    }

    #[staticmethod]
    #[pyo3(signature = (nzb, /))]
    pub fn from_file(nzb: PathBuf) -> PyResult<Self> {
        match nzb_rs::Nzb::parse_file(nzb) {
            Ok(nzb) => Ok(Self(nzb)),
            Err(err) => match err {
                nzb_rs::ParseNzbFileError::Io { source, file }
                    if source.kind() == io::ErrorKind::NotFound =>
                {
                    Err(PyFileNotFoundError::new_err(file))
                }
                _ => Err(InvalidNzbError::new_err(err.to_string())),
            },
        }
    }

    #[staticmethod]
    #[pyo3(signature = (data, /))]
    pub fn from_json(data: &str) -> PyResult<Self> {
        let nzb: nzb_rs::Nzb =
            serde_json::from_str(data).map_err(|e| InvalidNzbError::new_err(e.to_string()))?;
        Ok(Self(nzb))
    }

    #[pyo3(signature = (*, pretty=false))]
    pub fn to_json(&self, pretty: bool) -> PyResult<String> {
        if pretty {
            serde_json::to_string_pretty(&self).map_err(|e| InvalidNzbError::new_err(e.to_string()))
        } else {
            serde_json::to_string(&self).map_err(|e| InvalidNzbError::new_err(e.to_string()))
        }
    }

    #[getter]
    pub fn file(&self) -> File {
        self.0.file().clone().into()
    }

    #[getter]
    pub fn size(&self) -> u64 {
        self.0.size()
    }

    #[getter]
    pub fn filenames(&self) -> Tuple<&str> {
        self.0.filenames().into()
    }

    #[getter]
    pub fn posters(&self) -> Tuple<&str> {
        self.0.posters().into()
    }

    #[getter]
    pub fn groups(&self) -> Tuple<&str> {
        self.0.groups().into()
    }

    #[getter]
    pub fn par2_files(&self) -> Tuple<File> {
        self.0
            .par2_files()
            .clone()
            .into_iter()
            .map(|f| f.clone().into())
            .collect::<Vec<File>>()
            .into()
    }

    #[getter]
    pub fn par2_size(&self) -> u64 {
        self.0.par2_size()
    }

    #[getter]
    pub fn par2_percentage(&self) -> f64 {
        self.0.par2_percentage()
    }

    #[pyo3(signature = (ext, /))]
    pub fn has_extension(&self, ext: &str) -> bool {
        self.0.has_extension(ext)
    }

    pub fn has_par2(&self) -> bool {
        self.0.has_par2()
    }

    pub fn has_rar(&self) -> bool {
        self.0.has_rar()
    }

    pub fn is_rar(&self) -> bool {
        self.0.is_rar()
    }

    pub fn is_obfuscated(&self) -> bool {
        self.0.is_obfuscated()
    }
}
