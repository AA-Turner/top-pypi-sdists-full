//! Trajectory analysis functions.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyfunction, gen_stub_pymethods};

use super::helpers::positions_to_vec3;
use crate::trajectory::{self, MsdCalculator, VacfCalculator};

/// Validate dimension parameter (must be 1, 2, or 3).
fn validate_dim(dim: usize) -> PyResult<()> {
    if dim == 0 || dim > 3 {
        return Err(PyValueError::new_err("dim must be 1, 2, or 3"));
    }
    Ok(())
}

/// Validate origin interval is positive.
fn validate_origin_interval(origin_interval: usize) -> PyResult<()> {
    if origin_interval == 0 {
        return Err(PyValueError::new_err(
            "origin_interval must be a positive integer",
        ));
    }
    Ok(())
}

/// Validate frame count, lag bounds, and consistent atom counts for batch calculations.
fn validate_frames_and_max_lag(frames: &[Vec<[f64; 3]>], max_lag: usize) -> PyResult<()> {
    if frames.len() < 2 {
        return Err(PyValueError::new_err(
            "frames must contain at least 2 frames",
        ));
    }
    let n_atoms = frames[0].len();
    if n_atoms == 0 {
        return Err(PyValueError::new_err("frames must have at least 1 atom"));
    }
    for (idx, frame) in frames.iter().enumerate().skip(1) {
        if frame.len() != n_atoms {
            return Err(PyValueError::new_err(format!(
                "frame {idx} has {} atoms, expected {n_atoms}",
                frame.len()
            )));
        }
    }
    if max_lag == 0 {
        return Err(PyValueError::new_err("max_lag must be at least 1"));
    }
    if max_lag >= frames.len() {
        return Err(PyValueError::new_err(format!(
            "max_lag ({max_lag}) must be less than number of frames ({})",
            frames.len()
        )));
    }
    Ok(())
}

/// Compute MSD from a trajectory of position frames.
#[gen_stub_pyfunction(module = "ferrox._ferrox.trajectory")]
#[pyfunction]
#[pyo3(signature = (frames, max_lag, origin_interval = 1))]
fn compute_msd(
    frames: Vec<Vec<[f64; 3]>>,
    max_lag: usize,
    origin_interval: usize,
) -> PyResult<Vec<f64>> {
    validate_frames_and_max_lag(&frames, max_lag)?;
    validate_origin_interval(origin_interval)?;
    let trajectory_vec: Vec<_> = frames.iter().map(|fr| positions_to_vec3(fr)).collect();
    Ok(trajectory::compute_msd_batch(
        &trajectory_vec,
        max_lag,
        origin_interval,
    ))
}

/// Compute VACF from a trajectory of velocity frames.
#[gen_stub_pyfunction(module = "ferrox._ferrox.trajectory")]
#[pyfunction]
#[pyo3(signature = (frames, max_lag, origin_interval = 1))]
fn compute_vacf(
    frames: Vec<Vec<[f64; 3]>>,
    max_lag: usize,
    origin_interval: usize,
) -> PyResult<Vec<f64>> {
    validate_frames_and_max_lag(&frames, max_lag)?;
    validate_origin_interval(origin_interval)?;
    let trajectory_vec: Vec<_> = frames.iter().map(|fr| positions_to_vec3(fr)).collect();
    Ok(trajectory::compute_vacf_batch(
        &trajectory_vec,
        max_lag,
        origin_interval,
    ))
}

/// Calculate diffusion coefficient from mean squared displacement.
#[gen_stub_pyfunction(module = "ferrox._ferrox.trajectory")]
#[pyfunction]
#[pyo3(signature = (msd, times, dim = 3, start_fraction = 0.2, end_fraction = 0.8))]
fn diffusion_from_msd(
    msd: Vec<f64>,
    times: Vec<f64>,
    dim: usize,
    start_fraction: f64,
    end_fraction: f64,
) -> PyResult<(f64, f64)> {
    if msd.len() < 2 || times.len() < 2 {
        return Err(PyValueError::new_err(
            "MSD and times must have at least 2 points",
        ));
    }
    if msd.len() != times.len() {
        return Err(PyValueError::new_err("MSD and times must have same length"));
    }
    if !(0.0..=1.0).contains(&start_fraction) || !(0.0..=1.0).contains(&end_fraction) {
        return Err(PyValueError::new_err(
            "start_fraction and end_fraction must be in [0.0, 1.0]",
        ));
    }
    if start_fraction >= end_fraction {
        return Err(PyValueError::new_err(
            "start_fraction must be less than end_fraction",
        ));
    }
    validate_dim(dim)?;
    Ok(trajectory::diffusion_coefficient_from_msd(
        &msd,
        &times,
        dim,
        start_fraction,
        end_fraction,
    ))
}

/// Calculate diffusion coefficient from velocity autocorrelation function.
#[gen_stub_pyfunction(module = "ferrox._ferrox.trajectory")]
#[pyfunction]
#[pyo3(signature = (vacf, dt, dim = 3))]
fn diffusion_from_vacf(vacf: Vec<f64>, dt: f64, dim: usize) -> PyResult<f64> {
    if vacf.len() < 2 {
        return Err(PyValueError::new_err("VACF must have at least 2 points"));
    }
    if !dt.is_finite() || dt <= 0.0 {
        return Err(PyValueError::new_err("dt must be a finite positive number"));
    }
    validate_dim(dim)?;
    Ok(trajectory::diffusion_coefficient_from_vacf(&vacf, dt, dim))
}

// === Streaming MSD calculator ===

/// Streaming MSD calculator for memory-efficient trajectory analysis.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.trajectory", name = "MsdCalculator")]
pub struct PyMsdCalculator {
    inner: MsdCalculator,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyMsdCalculator {
    /// Create a new MSD calculator.
    ///
    /// Args:
    ///     n_atoms: Number of atoms per frame (must be > 0)
    ///     max_lag: Maximum lag time in frames
    ///     origin_interval: Frames between time origins (must be > 0)
    #[new]
    #[pyo3(signature = (n_atoms, max_lag, origin_interval))]
    fn new(n_atoms: usize, max_lag: usize, origin_interval: usize) -> PyResult<Self> {
        if n_atoms == 0 {
            return Err(PyValueError::new_err("n_atoms must be > 0"));
        }
        if max_lag == 0 {
            return Err(PyValueError::new_err("max_lag must be >= 1"));
        }
        validate_origin_interval(origin_interval)?;
        Ok(Self {
            inner: trajectory::MsdCalculator::new(n_atoms, max_lag, origin_interval),
        })
    }

    /// Number of atoms expected per frame.
    #[getter]
    fn n_atoms(&self) -> usize {
        self.inner.n_atoms()
    }

    /// Maximum lag time in frames.
    #[getter]
    fn max_lag(&self) -> usize {
        self.inner.max_lag()
    }

    /// Add a position frame to the MSD calculation.
    fn add_frame(&mut self, positions: Vec<[f64; 3]>) -> PyResult<()> {
        let pos_vec = positions_to_vec3(&positions);
        if pos_vec.len() != self.inner.n_atoms() {
            return Err(PyValueError::new_err(format!(
                "Expected {} positions, got {}",
                self.inner.n_atoms(),
                pos_vec.len()
            )));
        }
        self.inner.add_frame(&pos_vec);
        Ok(())
    }

    /// Compute mean squared displacement (averaged over atoms and time origins).
    fn compute_msd(&self) -> Vec<f64> {
        self.inner.compute_msd()
    }

    /// Compute MSD per atom for each lag time.
    ///
    /// Returns list of length max_lag+1, each element is list of length n_atoms.
    fn compute_msd_per_atom(&self) -> Vec<Vec<f64>> {
        self.inner.compute_msd_per_atom()
    }
}

// === Streaming VACF calculator ===

/// Streaming VACF calculator for memory-efficient trajectory analysis.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.trajectory", name = "VacfCalculator")]
pub struct PyVacfCalculator {
    inner: VacfCalculator,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyVacfCalculator {
    /// Create a new VACF calculator.
    ///
    /// Args:
    ///     n_atoms: Number of atoms per frame (must be > 0)
    ///     max_lag: Maximum lag time in frames
    ///     origin_interval: Frames between time origins (must be > 0)
    #[new]
    #[pyo3(signature = (n_atoms, max_lag, origin_interval))]
    fn new(n_atoms: usize, max_lag: usize, origin_interval: usize) -> PyResult<Self> {
        if n_atoms == 0 {
            return Err(PyValueError::new_err("n_atoms must be > 0"));
        }
        if max_lag == 0 {
            return Err(PyValueError::new_err("max_lag must be >= 1"));
        }
        validate_origin_interval(origin_interval)?;
        Ok(Self {
            inner: trajectory::VacfCalculator::new(n_atoms, max_lag, origin_interval),
        })
    }

    /// Number of atoms expected per frame.
    #[getter]
    fn n_atoms(&self) -> usize {
        self.inner.n_atoms()
    }

    /// Maximum lag time in frames.
    #[getter]
    fn max_lag(&self) -> usize {
        self.inner.max_lag()
    }

    /// Add a velocity frame to the VACF calculation.
    fn add_frame(&mut self, velocities: Vec<[f64; 3]>) -> PyResult<()> {
        let vel_vec = positions_to_vec3(&velocities);
        if vel_vec.len() != self.inner.n_atoms() {
            return Err(PyValueError::new_err(format!(
                "Expected {} velocities, got {}",
                self.inner.n_atoms(),
                vel_vec.len()
            )));
        }
        self.inner.add_frame(&vel_vec);
        Ok(())
    }

    /// Compute velocity autocorrelation function.
    fn compute_vacf(&self) -> Vec<f64> {
        self.inner.compute_vacf()
    }

    /// Compute normalized VACF (VACF(t) / VACF(0)).
    fn compute_normalized_vacf(&self) -> Vec<f64> {
        self.inner.compute_normalized_vacf()
    }
}

/// Register trajectory functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(compute_msd, module)?)?;
    module.add_function(wrap_pyfunction!(compute_vacf, module)?)?;
    module.add_function(wrap_pyfunction!(diffusion_from_msd, module)?)?;
    module.add_function(wrap_pyfunction!(diffusion_from_vacf, module)?)?;
    module.add_class::<PyMsdCalculator>()?;
    module.add_class::<PyVacfCalculator>()?;
    Ok(())
}
