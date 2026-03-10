//! Python bindings for LMDB dataset storage.

use std::path::Path;
use std::sync::Arc;

use pyo3::exceptions::{PyIndexError, PyValueError};
use pyo3::prelude::*;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use crate::io::lmdb::frame::RkyvFrame;
use crate::io::lmdb::{LmdbCodec, LmdbDataset, TrainingFrame};

fn to_py_err(err: crate::error::FerroxError) -> PyErr {
    PyValueError::new_err(err.to_string())
}

/// Serialize a JSON value to a Python-friendly string.
/// Unwraps string values to avoid double-quoting (`"\"foo\""` -> `"foo"`).
fn json_val_to_string(val: &serde_json::Value) -> String {
    match val {
        serde_json::Value::String(s) => s.clone(),
        other => other.to_string(),
    }
}

fn resolve_index(idx: i64, len: usize) -> PyResult<usize> {
    let len_i64 = len as i64;
    let resolved = if idx < 0 { len_i64 + idx } else { idx };
    if resolved < 0 || resolved >= len_i64 {
        return Err(PyIndexError::new_err(format!(
            "index {idx} out of range for length {len}"
        )));
    }
    Ok(resolved as usize)
}

// === PyTrainingFrame ===

/// A single atomic configuration with ML training labels.
///
/// Contains atomic numbers, Cartesian positions, optional cell/pbc,
/// and training labels (energy, forces, stress).
#[gen_stub_pyclass]
#[pyclass(name = "TrainingFrame", module = "ferrox._ferrox.lmdb")]
#[derive(Clone)]
pub struct PyTrainingFrame {
    inner: TrainingFrame,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyTrainingFrame {
    /// Create a new TrainingFrame.
    #[new]
    #[pyo3(signature = (
        atomic_numbers,
        positions,
        cell = None,
        pbc = None,
        energy = None,
        forces = None,
        stress = None,
        charge = None,
        magnetic_moments = None,
        properties = None,
    ))]
    fn new(
        atomic_numbers: Vec<u8>,
        positions: Vec<[f64; 3]>,
        cell: Option<[[f64; 3]; 3]>,
        pbc: Option<[bool; 3]>,
        energy: Option<f64>,
        forces: Option<Vec<[f64; 3]>>,
        stress: Option<[f64; 6]>,
        charge: Option<f64>,
        magnetic_moments: Option<Vec<f64>>,
        properties: Option<std::collections::HashMap<String, String>>,
    ) -> PyResult<Self> {
        let props = properties
            .unwrap_or_default()
            .into_iter()
            .map(|(key, val)| {
                let json_val = serde_json::from_str(&val).unwrap_or(serde_json::Value::String(val));
                (key, json_val)
            })
            .collect();
        let frame = TrainingFrame {
            atomic_numbers,
            positions,
            cell,
            pbc: pbc.unwrap_or([cell.is_some(); 3]),
            energy,
            forces,
            stress,
            charge,
            magnetic_moments,
            properties: props,
        };
        frame.validate().map_err(to_py_err)?;
        Ok(Self { inner: frame })
    }

    /// Number of atoms.
    #[getter]
    fn num_atoms(&self) -> usize {
        self.inner.num_atoms()
    }

    /// Atomic numbers as a list of integers.
    #[getter]
    fn atomic_numbers(&self) -> Vec<u16> {
        // Return Vec<u16> instead of Vec<u8> so PyO3 produces a list[int],
        // not bytes (PyO3 converts Vec<u8> to Python bytes by default)
        self.inner
            .atomic_numbers
            .iter()
            .map(|&z| z as u16)
            .collect()
    }

    /// Cartesian positions in angstroms as list of [x, y, z].
    #[getter]
    fn positions(&self) -> Vec<[f64; 3]> {
        self.inner.positions.clone()
    }

    /// Lattice vectors as 3x3 list, or None for non-periodic.
    #[getter]
    fn cell(&self) -> Option<[[f64; 3]; 3]> {
        self.inner.cell
    }

    /// Periodic boundary conditions per axis.
    #[getter]
    fn pbc(&self) -> [bool; 3] {
        self.inner.pbc
    }

    /// Total energy in eV, or None.
    #[getter]
    fn energy(&self) -> Option<f64> {
        self.inner.energy
    }

    /// Per-atom forces in eV/A as list of [fx, fy, fz], or None.
    #[getter]
    fn forces(&self) -> Option<Vec<[f64; 3]>> {
        self.inner.forces.clone()
    }

    /// Stress tensor in Voigt notation [xx, yy, zz, yz, xz, xy] (eV/A^3), or None.
    #[getter]
    fn stress(&self) -> Option<[f64; 6]> {
        self.inner.stress
    }

    /// Total system charge, or None.
    #[getter]
    fn charge(&self) -> Option<f64> {
        self.inner.charge
    }

    /// Per-atom magnetic moments, or None.
    #[getter]
    fn magnetic_moments(&self) -> Option<Vec<f64>> {
        self.inner.magnetic_moments.clone()
    }

    fn __repr__(&self) -> String {
        let energy_str = self
            .inner
            .energy
            .map_or("None".to_string(), |e| format!("{e:.6}"));
        format!(
            "TrainingFrame(n_atoms={}, energy={energy_str})",
            self.inner.num_atoms()
        )
    }
}

// === PyLmdbDataset ===

/// An LMDB-backed dataset of TrainingFrames for ML potential training.
///
/// Supports fast random-access reads, sequential writes, and parallel iteration.
/// LMDB files are memory-mapped for zero-copy reads.
#[gen_stub_pyclass]
#[pyclass(name = "LmdbDataset", module = "ferrox._ferrox.lmdb")]
pub struct PyLmdbDataset {
    inner: Arc<LmdbDataset>,
}

fn parse_codec(codec: &str) -> PyResult<LmdbCodec> {
    match codec {
        "rkyv" => Ok(LmdbCodec::Rkyv),
        "json" => Ok(LmdbCodec::Json),
        _ => Err(PyValueError::new_err(format!(
            "unknown codec '{codec}'; expected 'rkyv' or 'json'"
        ))),
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyLmdbDataset {
    /// Open an existing LMDB dataset.
    #[staticmethod]
    fn open(path: &str) -> PyResult<Self> {
        let dataset = LmdbDataset::open(Path::new(path)).map_err(to_py_err)?;
        Ok(Self {
            inner: Arc::new(dataset),
        })
    }

    /// Create a new LMDB dataset.
    #[staticmethod]
    #[pyo3(signature = (path, codec = "rkyv"))]
    fn create(path: &str, codec: &str) -> PyResult<Self> {
        let codec = parse_codec(codec)?;
        let dataset = LmdbDataset::create(Path::new(path), codec).map_err(to_py_err)?;
        Ok(Self {
            inner: Arc::new(dataset),
        })
    }

    /// Number of frames in the dataset.
    fn __len__(&self) -> usize {
        self.inner.len() as usize
    }

    /// Get frame(s) by integer index or slice.
    fn __getitem__<'py>(
        &self,
        key: &Bound<'py, pyo3::types::PyAny>,
    ) -> PyResult<Bound<'py, pyo3::types::PyAny>> {
        let py = key.py();
        if let Ok(slice) = key.cast::<pyo3::types::PySlice>() {
            let len = self.inner.len() as usize;
            let indices = slice.indices(len as isize)?;
            let mut idx_list: Vec<u64> = Vec::new();
            let mut idx = indices.start;
            while (indices.step > 0 && idx < indices.stop)
                || (indices.step < 0 && idx > indices.stop)
            {
                idx_list.push(idx as u64);
                idx += indices.step;
            }
            let frames: Vec<PyTrainingFrame> = self
                .inner
                .get_batch(&idx_list)
                .map_err(to_py_err)?
                .into_iter()
                .map(|frame| PyTrainingFrame { inner: frame })
                .collect();
            return Ok(frames.into_pyobject(py)?.into_any());
        }
        let idx: i64 = key.extract()?;
        let resolved = resolve_index(idx, self.inner.len() as usize)?;
        let frame = self.inner.get(resolved as u64).map_err(to_py_err)?;
        Ok(PyTrainingFrame { inner: frame }
            .into_pyobject(py)?
            .into_any())
    }

    /// Iterate over all frames.
    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<PyLmdbIter> {
        Ok(PyLmdbIter {
            dataset: Arc::clone(&slf.inner),
            idx: 0,
            len: slf.inner.len(),
        })
    }

    /// The serialization codec used by this dataset.
    #[getter]
    fn codec(&self) -> &str {
        match self.inner.codec() {
            LmdbCodec::Rkyv => "rkyv",
            LmdbCodec::Json => "json",
        }
    }

    /// Write a single frame at a given index.
    fn put(&self, idx: u64, frame: &PyTrainingFrame) -> PyResult<()> {
        self.inner.put(idx, &frame.inner).map_err(to_py_err)
    }

    /// Read multiple frames by index in a single transaction.
    fn get_batch(&self, indices: Vec<u64>) -> PyResult<Vec<PyTrainingFrame>> {
        let frames = self.inner.get_batch(&indices).map_err(to_py_err)?;
        Ok(frames
            .into_iter()
            .map(|frame| PyTrainingFrame { inner: frame })
            .collect())
    }

    /// Read a contiguous range of frames `[start, end)` in a single transaction.
    fn get_range(&self, start: u64, end: u64) -> PyResult<Vec<PyTrainingFrame>> {
        let frames = self.inner.get_range(start, end).map_err(to_py_err)?;
        Ok(frames
            .into_iter()
            .map(|frame| PyTrainingFrame { inner: frame })
            .collect())
    }

    /// Read all frames into a list in a single transaction.
    ///
    /// Loads the entire dataset into memory. For large datasets, prefer
    /// `get_range()` with smaller windows.
    fn to_list(&self) -> PyResult<Vec<PyTrainingFrame>> {
        self.get_range(0, self.inner.len())
    }

    /// Read a range of frames as a batch, keeping data in Rust memory.
    ///
    /// For rkyv-encoded datasets, this is essentially free — no data is read
    /// until a field accessor (`.energies`, `.positions`, etc.) is called,
    /// which then reads directly from LMDB's memory-mapped bytes.
    /// For other codecs, frames are fully deserialized upfront.
    fn read_batch(&self, start: u64, end: u64) -> PyResult<PyFrameBatch> {
        let len = self.inner.len();
        if start > end {
            return Err(PyValueError::new_err(format!(
                "start ({start}) must be <= end ({end})"
            )));
        }
        if end > len {
            return Err(PyValueError::new_err(format!(
                "end ({end}) out of range for dataset of length {len}"
            )));
        }
        if self.inner.codec() == LmdbCodec::Rkyv {
            Ok(PyFrameBatch {
                storage: BatchStorage::RkyvLazy {
                    dataset: Arc::clone(&self.inner),
                    start,
                    end,
                },
            })
        } else {
            let frames = self.inner.get_range(start, end).map_err(to_py_err)?;
            Ok(PyFrameBatch {
                storage: BatchStorage::Deserialized(frames),
            })
        }
    }

    /// Remove all frames and reset the dataset length to zero.
    fn clear(&self) -> PyResult<()> {
        self.inner.clear().map_err(to_py_err)
    }

    /// Write multiple frames at specified indices in a single transaction.
    fn put_batch(&self, entries: Vec<(u64, PyTrainingFrame)>) -> PyResult<()> {
        let rust_entries: Vec<(u64, TrainingFrame)> = entries
            .into_iter()
            .map(|(idx, frame)| (idx, frame.inner))
            .collect();
        self.inner.put_batch(&rust_entries).map_err(to_py_err)
    }

    /// Append frames, auto-assigning sequential keys. Returns new length.
    fn extend(&self, frames: Vec<PyTrainingFrame>) -> PyResult<u64> {
        let rust_frames: Vec<TrainingFrame> = frames.into_iter().map(|frame| frame.inner).collect();
        self.inner.extend(rust_frames).map_err(to_py_err)
    }

    /// Create an LMDB dataset from an extXYZ file.
    #[staticmethod]
    #[pyo3(signature = (xyz_path, lmdb_path, codec = "rkyv"))]
    fn from_extxyz(xyz_path: &str, lmdb_path: &str, codec: &str) -> PyResult<Self> {
        let codec = parse_codec(codec)?;
        let dataset = LmdbDataset::from_extxyz(Path::new(xyz_path), Path::new(lmdb_path), codec)
            .map_err(to_py_err)?;
        Ok(Self {
            inner: Arc::new(dataset),
        })
    }

    /// Create an LMDB dataset from a list of Structure objects.
    #[staticmethod]
    #[pyo3(signature = (structures, lmdb_path, codec = "rkyv"))]
    fn from_structures(
        structures: Vec<PyRef<'_, crate::python::classes::PyStructure>>,
        lmdb_path: &str,
        codec: &str,
    ) -> PyResult<Self> {
        let codec = parse_codec(codec)?;
        let rust_structs: Vec<crate::structure::Structure> =
            structures.iter().map(|s| s.inner.clone()).collect();
        let dataset = LmdbDataset::from_structures(&rust_structs, Path::new(lmdb_path), codec)
            .map_err(to_py_err)?;
        Ok(Self {
            inner: Arc::new(dataset),
        })
    }

    /// Export the dataset to an extXYZ file. Returns number of frames written.
    fn to_extxyz(&self, path: &str) -> PyResult<u64> {
        self.inner.to_extxyz(Path::new(path)).map_err(to_py_err)
    }

    fn __repr__(&self) -> String {
        format!(
            "LmdbDataset(len={}, codec='{}')",
            self.inner.len(),
            self.codec()
        )
    }
}

// === FrameBatch ===

/// Internal storage for FrameBatch: either a lazy reference to an rkyv dataset
/// (reads fields directly from mmap inside a fresh txn) or deserialized frames.
enum BatchStorage {
    /// Lazy rkyv: holds a dataset reference + range. Field accessors read
    /// directly from the memory-mapped LMDB inside a read transaction —
    /// no per-frame byte copies, no allocation until the user requests a field.
    RkyvLazy {
        dataset: Arc<LmdbDataset>,
        start: u64,
        end: u64,
    },
    /// Fallback for non-rkyv codecs: fully deserialized frames.
    Deserialized(Vec<TrainingFrame>),
}

impl BatchStorage {
    fn len(&self) -> usize {
        match self {
            BatchStorage::RkyvLazy { start, end, .. } => end.saturating_sub(*start) as usize,
            BatchStorage::Deserialized(frames) => frames.len(),
        }
    }

    fn map_field<T>(
        &self,
        deser_fn: impl Fn(&TrainingFrame) -> T,
        rkyv_fn: impl Fn(&ArchivedFrame) -> T,
    ) -> PyResult<Vec<T>> {
        match self {
            BatchStorage::Deserialized(frames) => Ok(frames.iter().map(deser_fn).collect()),
            BatchStorage::RkyvLazy {
                dataset,
                start,
                end,
            } => rkyv_map_range(dataset, *start, *end, rkyv_fn),
        }
    }
}

/// A batch of training frames kept in Rust memory for efficient bulk access.
///
/// For rkyv-encoded datasets, field accessors (`.energies`, `.positions`, etc.)
/// read directly from LMDB's memory-mapped bytes via zero-copy rkyv access —
/// no deserialization and no per-frame allocation.
/// For other codecs, falls back to deserialized frames.
#[gen_stub_pyclass]
#[pyclass(name = "FrameBatch", module = "ferrox._ferrox.lmdb")]
pub struct PyFrameBatch {
    storage: BatchStorage,
}

type ArchivedFrame = <RkyvFrame as rkyv::Archive>::Archived;

/// Convert a rkyv little-endian f64 array to native.
fn rkyv_f64_array<const N: usize>(arr: &[rkyv::rend::f64_le; N]) -> [f64; N] {
    std::array::from_fn(|idx| arr[idx].to_native())
}

fn rkyv_f64x3x3(arr: &[[rkyv::rend::f64_le; 3]; 3]) -> [[f64; 3]; 3] {
    std::array::from_fn(|idx| rkyv_f64_array(&arr[idx]))
}

/// Access an archived rkyv frame from raw bytes.
fn access_archived(bytes: &[u8]) -> PyResult<&ArchivedFrame> {
    rkyv::access::<ArchivedFrame, rkyv::rancor::Error>(bytes)
        .map_err(|err| PyValueError::new_err(format!("rkyv access failed: {err}")))
}

/// Helper: open a read txn and iterate over a range, applying `f` to each
/// archived frame's mmap bytes. This is the core zero-copy read path.
fn rkyv_map_range<T>(
    dataset: &LmdbDataset,
    start: u64,
    end: u64,
    extract_fn: impl Fn(&ArchivedFrame) -> T,
) -> PyResult<Vec<T>> {
    let rtxn = dataset
        .env_ref()
        .read_txn()
        .map_err(|err| PyValueError::new_err(format!("failed to open read txn: {err}")))?;
    (start..end)
        .map(|idx| {
            let bytes = dataset
                .data_db_ref()
                .get(&rtxn, &idx)
                .map_err(|err| PyValueError::new_err(format!("LMDB get failed: {err}")))?
                .ok_or_else(|| {
                    PyValueError::new_err(format!("key {idx} not found in LMDB dataset"))
                })?;
            let archived = access_archived(bytes)?;
            Ok(extract_fn(archived))
        })
        .collect()
}

#[gen_stub_pymethods]
#[pymethods]
impl PyFrameBatch {
    /// Number of frames in the batch.
    fn __len__(&self) -> usize {
        self.storage.len()
    }

    /// Get a single frame by index (full deserialization for rkyv, clone for others).
    fn __getitem__(&self, idx: i64) -> PyResult<PyTrainingFrame> {
        let resolved = resolve_index(idx, self.storage.len())?;
        match &self.storage {
            BatchStorage::Deserialized(frames) => Ok(PyTrainingFrame {
                inner: frames[resolved as usize].clone(),
            }),
            BatchStorage::RkyvLazy { dataset, start, .. } => {
                let frame = dataset.get(start + resolved as u64).map_err(to_py_err)?;
                Ok(PyTrainingFrame { inner: frame })
            }
        }
    }

    /// Energies for all frames (zero-copy for rkyv — reads directly from mmap).
    #[getter]
    fn energies(&self) -> PyResult<Vec<Option<f64>>> {
        self.storage.map_field(
            |frame| frame.energy,
            |archived| archived.energy.as_ref().map(|e| e.to_native()),
        )
    }

    /// Atomic numbers for all frames (zero-copy for rkyv).
    #[getter]
    fn atomic_numbers(&self) -> PyResult<Vec<Vec<u16>>> {
        self.storage.map_field(
            |frame| frame.atomic_numbers.iter().map(|&z| z as u16).collect(),
            |archived| archived.atomic_numbers.iter().map(|&z| z as u16).collect(),
        )
    }

    /// Positions for all frames (zero-copy for rkyv).
    #[getter]
    fn positions(&self) -> PyResult<Vec<Vec<[f64; 3]>>> {
        self.storage.map_field(
            |frame| frame.positions.clone(),
            |archived| archived.positions.iter().map(rkyv_f64_array).collect(),
        )
    }

    /// Forces for all frames (zero-copy for rkyv).
    #[getter]
    fn forces(&self) -> PyResult<Vec<Option<Vec<[f64; 3]>>>> {
        self.storage.map_field(
            |frame| frame.forces.clone(),
            |archived| {
                archived
                    .forces
                    .as_ref()
                    .map(|forces| forces.iter().map(rkyv_f64_array).collect())
            },
        )
    }

    /// Stress tensors for all frames (zero-copy for rkyv).
    #[getter]
    fn stresses(&self) -> PyResult<Vec<Option<[f64; 6]>>> {
        self.storage.map_field(
            |frame| frame.stress,
            |archived| archived.stress.as_ref().map(rkyv_f64_array),
        )
    }

    /// Cell matrices for all frames (zero-copy for rkyv).
    #[getter]
    fn cells(&self) -> PyResult<Vec<Option<[[f64; 3]; 3]>>> {
        self.storage.map_field(
            |frame| frame.cell,
            |archived| archived.cell.as_ref().map(rkyv_f64x3x3),
        )
    }

    /// Properties for all frames (lazy JSON deserialization).
    #[getter]
    fn properties(&self) -> PyResult<Vec<std::collections::HashMap<String, String>>> {
        self.storage.map_field(
            |frame| {
                frame
                    .properties
                    .iter()
                    .map(|(key, val)| (key.clone(), json_val_to_string(val)))
                    .collect()
            },
            |archived| {
                let map: std::collections::HashMap<String, serde_json::Value> =
                    serde_json::from_slice(&archived.properties_json).unwrap_or_default();
                map.into_iter()
                    .map(|(key, val)| (key, json_val_to_string(&val)))
                    .collect()
            },
        )
    }

    fn __repr__(&self) -> String {
        format!("FrameBatch(n_frames={})", self.storage.len())
    }
}

// === Iterator ===

/// Python iterator over LMDB dataset frames.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.lmdb")]
pub struct PyLmdbIter {
    dataset: Arc<LmdbDataset>,
    idx: u64,
    len: u64,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyLmdbIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }

    fn __next__(&mut self) -> PyResult<Option<PyTrainingFrame>> {
        if self.idx >= self.len {
            return Ok(None);
        }
        let frame = self.dataset.get(self.idx).map_err(to_py_err)?;
        self.idx += 1;
        Ok(Some(PyTrainingFrame { inner: frame }))
    }
}

/// Register lmdb functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<PyTrainingFrame>()?;
    module.add_class::<PyLmdbDataset>()?;
    module.add_class::<PyFrameBatch>()?;
    module.add_class::<PyLmdbIter>()?;
    Ok(())
}
