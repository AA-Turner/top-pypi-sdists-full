//! Molecular dynamics integrators and analysis.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyfunction, gen_stub_pymethods};

use crate::simulation::md::{
    self, LangevinIntegrator, LangevinStepError, MDState, NPTConfig, NPTIntegrator,
    NoseHooverChain, ThermostatStepError, VelocityRescale,
};

use super::helpers::{
    array_to_mat3, default_pbc, mat3_to_array, positions_to_vec3, validate_positive_f64,
    vec3_to_positions,
};

// === Validation Helpers ===

/// Validate temperature is finite and non-negative.
#[inline]
fn validate_temperature(temp: f64) -> PyResult<()> {
    if !temp.is_finite() || temp < 0.0 {
        return Err(PyValueError::new_err(format!(
            "temperature must be finite and non-negative, got {temp}"
        )));
    }
    Ok(())
}

/// Validate degrees of freedom is positive.
#[inline]
fn validate_n_dof(n_dof: usize) -> PyResult<()> {
    if n_dof == 0 {
        return Err(PyValueError::new_err(
            "n_dof must be positive (number of degrees of freedom)",
        ));
    }
    Ok(())
}

/// Convert ThermostatStepError to PyErr.
#[inline]
fn thermostat_step_err_to_pyerr(err: ThermostatStepError<PyErr>) -> PyErr {
    match err {
        ThermostatStepError::Callback(py_err) => py_err,
        ThermostatStepError::ForcesLength(err) => PyValueError::new_err(err.to_string()),
    }
}

/// Convert LangevinStepError to PyErr.
#[inline]
fn langevin_step_err_to_pyerr(err: LangevinStepError<PyErr>) -> PyErr {
    match err {
        LangevinStepError::Callback(py_err) => py_err,
        LangevinStepError::ForcesLength(err) => PyValueError::new_err(err.to_string()),
    }
}

/// Extract and validate forces from Python callback result.
/// Returns an error if the number of forces doesn't match the number of positions.
fn extract_and_validate_forces(
    result: &Bound<'_, PyAny>,
    n_atoms: usize,
) -> PyResult<Vec<nalgebra::Vector3<f64>>> {
    let forces: Vec<[f64; 3]> = result.extract()?;
    if forces.len() != n_atoms {
        return Err(PyValueError::new_err(format!(
            "Force callback returned {} forces for {} atoms",
            forces.len(),
            n_atoms
        )));
    }
    Ok(positions_to_vec3(&forces))
}

/// Validate force-array length against atom count.
#[inline]
fn validate_force_count(forces_len: usize, n_atoms: usize, name: &str) -> PyResult<()> {
    if forces_len != n_atoms {
        return Err(PyValueError::new_err(format!(
            "{name} length ({forces_len}) must match num_atoms ({n_atoms})",
        )));
    }
    Ok(())
}

/// Validate that an NPT state's atom count matches the integrator configuration.
#[inline]
fn validate_npt_atom_count(integrator: &NPTIntegrator, state_n_atoms: usize) -> PyResult<()> {
    let expected = integrator.num_atoms();
    if state_n_atoms != expected {
        return Err(PyValueError::new_err(format!(
            "NPTState has {state_n_atoms} atoms but NPTIntegrator was configured for {expected}"
        )));
    }
    Ok(())
}

// Workaround: pyo3-stub-gen lacks blanket impl for &mut T where T: PyStubType.
// Any pyfunction taking &mut SomePyClass needs this manual impl.
// Track upstream: https://github.com/Jij-Inc/pyo3-stub-gen/issues/169
macro_rules! impl_stub_type_for_mut {
    ($($ty:ty),+ $(,)?) => {
        $(impl pyo3_stub_gen::PyStubType for &mut $ty {
            fn type_input() -> pyo3_stub_gen::TypeInfo { <$ty>::type_input() }
            fn type_output() -> pyo3_stub_gen::TypeInfo { <$ty>::type_output() }
        })+
    };
}

// === MDState ===

/// Python wrapper for MD state.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "MDState")]
pub struct PyMDState {
    /// The inner MDState from the core library.
    pub inner: MDState,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyMDState {
    /// Create a new MD state.
    ///
    /// Args:
    ///     positions: Nx3 array of atomic positions in Angstrom
    ///     masses: N-element array of atomic masses in amu
    ///     velocities: Optional Nx3 array of velocities (default: zeros)
    #[new]
    #[pyo3(signature = (positions, masses, velocities = None))]
    fn new(
        positions: Vec<[f64; 3]>,
        masses: Vec<f64>,
        velocities: Option<Vec<[f64; 3]>>,
    ) -> PyResult<Self> {
        if positions.len() != masses.len() {
            return Err(PyValueError::new_err(format!(
                "Masses length ({}) must match positions length ({})",
                masses.len(),
                positions.len()
            )));
        }

        // Validate masses before passing to core library (which panics on invalid)
        for (idx, &mass) in masses.iter().enumerate() {
            if !mass.is_finite() || mass <= 0.0 {
                return Err(PyValueError::new_err(format!(
                    "Mass at index {idx} must be positive and finite, got {mass}"
                )));
            }
        }

        let pos_vec = positions_to_vec3(&positions);
        let mut state = MDState::new(pos_vec, masses);

        if let Some(vels) = velocities {
            if vels.len() != state.num_atoms() {
                return Err(PyValueError::new_err(format!(
                    "Velocities length ({}) must match positions length ({})",
                    vels.len(),
                    state.num_atoms()
                )));
            }
            state.velocities = positions_to_vec3(&vels);
        }

        Ok(Self { inner: state })
    }

    /// Initialize velocities from Maxwell-Boltzmann distribution.
    #[pyo3(signature = (temperature_k, seed = None))]
    fn init_velocities(&mut self, temperature_k: f64, seed: Option<u64>) -> PyResult<()> {
        validate_temperature(temperature_k)?;
        self.inner.init_velocities(temperature_k, seed);
        Ok(())
    }

    /// Get kinetic energy in eV.
    fn kinetic_energy(&self) -> f64 {
        self.inner.kinetic_energy()
    }

    /// Get temperature in Kelvin.
    fn temperature(&self) -> f64 {
        self.inner.temperature()
    }

    /// Get number of atoms.
    fn num_atoms(&self) -> usize {
        self.inner.num_atoms()
    }

    /// Get positions as Nx3 array.
    #[getter]
    fn positions(&self) -> Vec<[f64; 3]> {
        vec3_to_positions(&self.inner.positions)
    }

    /// Set positions from Nx3 array.
    #[setter]
    fn set_positions(&mut self, positions: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(positions.len(), self.inner.num_atoms(), "positions")?;
        self.inner.positions = positions_to_vec3(&positions);
        Ok(())
    }

    /// Get velocities as Nx3 array.
    #[getter]
    fn velocities(&self) -> Vec<[f64; 3]> {
        vec3_to_positions(&self.inner.velocities)
    }

    /// Set velocities from Nx3 array.
    #[setter]
    fn set_velocities(&mut self, velocities: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(velocities.len(), self.inner.num_atoms(), "velocities")?;
        self.inner.velocities = positions_to_vec3(&velocities);
        Ok(())
    }

    /// Get forces as Nx3 array.
    #[getter]
    fn forces(&self) -> Vec<[f64; 3]> {
        vec3_to_positions(&self.inner.forces)
    }

    /// Set forces from Nx3 array.
    #[setter]
    fn set_forces(&mut self, forces: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(forces.len(), self.inner.num_atoms(), "forces")?;
        let force_vec = positions_to_vec3(&forces);
        self.inner.set_forces(&force_vec);
        Ok(())
    }
}

// === LangevinIntegrator ===

/// Python wrapper for Langevin integrator.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "LangevinIntegrator")]
pub struct PyLangevinIntegrator {
    inner: LangevinIntegrator,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyLangevinIntegrator {
    /// Create a new Langevin integrator.
    ///
    /// Args:
    ///     temperature_k: Target temperature in Kelvin (must be non-negative)
    ///     friction: Friction coefficient in 1/fs (must be positive, typical: 0.001 to 0.01)
    ///     dt: Time step in fs (must be positive)
    ///     seed: Optional random seed for reproducibility
    #[new]
    #[pyo3(signature = (temperature_k, friction, dt, seed = None))]
    fn new(temperature_k: f64, friction: f64, dt: f64, seed: Option<u64>) -> PyResult<Self> {
        validate_temperature(temperature_k)?;
        validate_positive_f64(friction, "friction")?;
        validate_positive_f64(dt, "timestep dt")?;
        Ok(Self {
            inner: LangevinIntegrator::new(temperature_k, friction, dt, seed),
        })
    }

    /// Perform one Langevin dynamics step.
    ///
    /// Raises:
    ///     RuntimeError: If force computation fails. State is restored to its
    ///         original value before the step when this happens.
    fn step(
        &mut self,
        state: &mut PyMDState,
        compute_forces: Py<PyAny>,
        py: Python<'_>,
    ) -> PyResult<()> {
        self.inner
            .try_step(&mut state.inner, |positions| {
                let n_atoms = positions.len();
                let pos_arr = vec3_to_positions(positions);
                let result = compute_forces.call1(py, (pos_arr,))?;
                extract_and_validate_forces(result.bind(py), n_atoms)
            })
            .map_err(langevin_step_err_to_pyerr)
    }

    /// Set target temperature.
    fn set_temperature(&mut self, temperature_k: f64) -> PyResult<()> {
        validate_temperature(temperature_k)?;
        self.inner.set_temperature(temperature_k);
        Ok(())
    }

    /// Set friction coefficient.
    fn set_friction(&mut self, friction: f64) -> PyResult<()> {
        validate_positive_f64(friction, "friction")?;
        self.inner.set_friction(friction);
        Ok(())
    }

    /// Set time step.
    fn set_dt(&mut self, dt: f64) -> PyResult<()> {
        validate_positive_f64(dt, "timestep dt")?;
        self.inner.set_dt(dt);
        Ok(())
    }
}

/// First half of Langevin step (B-A-O-A: velocity half-step, position update, thermostat).
///
/// Set state.forces before calling, or pass forces. After calling, compute forces at
/// state.positions and call langevin_step_finalize.
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
fn langevin_step_init(
    integrator: &mut PyLangevinIntegrator,
    state: &mut PyMDState,
    forces: Vec<[f64; 3]>,
) -> PyResult<()> {
    validate_force_count(forces.len(), state.inner.num_atoms(), "forces")?;
    state.inner.set_forces(&positions_to_vec3(&forces));
    integrator.inner.step_init(&mut state.inner);
    Ok(())
}

/// Complete Langevin step after langevin_step_init (final velocity half-step with new forces).
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
fn langevin_step_finalize(
    integrator: &PyLangevinIntegrator,
    state: &mut PyMDState,
    new_forces: Vec<[f64; 3]>,
) -> PyResult<()> {
    validate_force_count(new_forces.len(), state.inner.num_atoms(), "new_forces")?;
    integrator
        .inner
        .step_finalize(&mut state.inner, &positions_to_vec3(&new_forces))
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Perform one complete Langevin step with pre-computed forces (convenience wrapper).
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
fn langevin_step_with_forces(
    integrator: &mut PyLangevinIntegrator,
    state: &mut PyMDState,
    forces: Vec<[f64; 3]>,
    new_forces: Vec<[f64; 3]>,
) -> PyResult<()> {
    langevin_step_init(integrator, state, forces)?;
    langevin_step_finalize(integrator, state, new_forces)
}

/// First half of velocity Verlet: update velocities and positions.
///
/// Expects state.forces to contain current forces. After calling, compute
/// new forces at state.positions and call velocity_verlet_step_finalize.
///
/// Args:
///     state: MD state (forces must be set)
///     dt: Time step in fs (must be positive)
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
fn velocity_verlet_step_init(state: &mut PyMDState, dt: f64) -> PyResult<()> {
    validate_positive_f64(dt, "timestep dt")?;
    state.inner = md::velocity_verlet_init(std::mem::take(&mut state.inner), dt);
    Ok(())
}

/// Complete velocity Verlet step with new forces.
///
/// Call after velocity_verlet_step_init with forces computed at updated positions.
///
/// Args:
///     state: MD state (from velocity_verlet_step_init)
///     dt: Time step in fs (must match step_init)
///     new_forces: Nx3 array of forces at updated positions
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
#[pyo3(name = "velocity_verlet_step_finalize")]
fn velocity_verlet_finalize(
    state: &mut PyMDState,
    dt: f64,
    new_forces: Vec<[f64; 3]>,
) -> PyResult<()> {
    validate_positive_f64(dt, "timestep dt")?;
    validate_force_count(new_forces.len(), state.inner.num_atoms(), "new_forces")?;
    let force_vec = positions_to_vec3(&new_forces);
    state.inner = md::velocity_verlet_finalize(std::mem::take(&mut state.inner), dt, &force_vec);
    Ok(())
}

/// Perform one velocity Verlet step (NVE ensemble).
///
/// Args:
///     state: MD state to update
///     dt: Time step in fs (must be positive)
///     compute_forces: Callback to compute forces
///
/// Raises:
///     ValueError: If dt is not positive and finite.
///     RuntimeError: If force computation fails. State is restored to its
///         original value before the step when this happens.
#[gen_stub_pyfunction(module = "ferrox._ferrox.md")]
#[pyfunction]
fn velocity_verlet_step(
    state: &mut PyMDState,
    dt: f64,
    compute_forces: Py<PyAny>,
    py: Python<'_>,
) -> PyResult<()> {
    validate_positive_f64(dt, "timestep dt")?;
    match md::try_velocity_verlet_step(std::mem::take(&mut state.inner), dt, |positions| {
        let n_atoms = positions.len();
        let pos_arr = vec3_to_positions(positions);
        let result = compute_forces.call1(py, (pos_arr,))?;
        extract_and_validate_forces(result.bind(py), n_atoms)
    }) {
        Ok(new_state) => {
            state.inner = new_state;
            Ok(())
        }
        Err((original_state, err)) => {
            state.inner = original_state;
            Err(err)
        }
    }
}

// === Nose-Hoover Chain ===

/// Nosé-Hoover chain thermostat for NVT molecular dynamics.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "NoseHooverChain")]
pub struct PyNoseHooverChain {
    inner: NoseHooverChain,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyNoseHooverChain {
    /// Create a new Nosé-Hoover chain thermostat.
    ///
    /// Args:
    ///     target_temp: Target temperature in Kelvin (must be positive)
    ///     tau: Coupling time constant in fs (must be positive)
    ///     dt: Time step in fs (must be positive)
    ///     n_dof: Number of degrees of freedom (must be positive)
    #[new]
    fn new(target_temp: f64, tau: f64, dt: f64, n_dof: usize) -> PyResult<Self> {
        validate_positive_f64(target_temp, "target_temp")?;
        validate_positive_f64(tau, "coupling time constant tau")?;
        validate_positive_f64(dt, "timestep dt")?;
        validate_n_dof(n_dof)?;
        Ok(Self {
            inner: NoseHooverChain::new(target_temp, tau, dt, n_dof),
        })
    }

    /// Perform one NVT step.
    fn step(&mut self, state: &mut PyMDState, compute_forces: &Bound<'_, PyAny>) -> PyResult<()> {
        self.inner
            .try_step(&mut state.inner, |positions| {
                let n_atoms = positions.len();
                let result = compute_forces.call1((vec3_to_positions(positions),))?;
                extract_and_validate_forces(&result, n_atoms)
            })
            .map_err(thermostat_step_err_to_pyerr)
    }

    /// Set target temperature.
    fn set_temperature(&mut self, target_temp: f64) -> PyResult<()> {
        validate_positive_f64(target_temp, "target_temp")?;
        self.inner.set_temperature(target_temp);
        Ok(())
    }

    /// First half of Nosé-Hoover step. Call step_finalize after computing new forces.
    fn step_init(&mut self, state: &mut PyMDState, forces: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(forces.len(), state.inner.num_atoms(), "forces")?;
        state.inner.set_forces(&positions_to_vec3(&forces));
        self.inner.step_init(&mut state.inner);
        Ok(())
    }

    /// Complete Nosé-Hoover step after step_init.
    fn step_finalize(&mut self, state: &mut PyMDState, new_forces: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(new_forces.len(), state.inner.num_atoms(), "new_forces")?;
        self.inner
            .step_finalize(&mut state.inner, &positions_to_vec3(&new_forces))
            .map_err(|err| PyValueError::new_err(err.to_string()))
    }

    /// Perform one complete Nosé-Hoover step with pre-computed forces.
    fn step_with_forces(
        &mut self,
        state: &mut PyMDState,
        forces: Vec<[f64; 3]>,
        new_forces: Vec<[f64; 3]>,
    ) -> PyResult<()> {
        self.step_init(state, forces)?;
        self.step_finalize(state, new_forces)
    }
}

// === Velocity Rescaling ===

/// Velocity rescaling (Bussi) thermostat for NVT molecular dynamics.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "VelocityRescale")]
pub struct PyVelocityRescale {
    inner: VelocityRescale,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyVelocityRescale {
    /// Create a new velocity rescaling thermostat.
    ///
    /// Args:
    ///     target_temp: Target temperature in Kelvin (must be positive)
    ///     tau: Coupling time constant in fs (must be positive)
    ///     dt: Time step in fs (must be positive)
    ///     n_dof: Number of degrees of freedom (must be positive)
    ///     seed: Optional random seed for reproducibility
    #[new]
    #[pyo3(signature = (target_temp, tau, dt, n_dof, seed = None))]
    fn new(target_temp: f64, tau: f64, dt: f64, n_dof: usize, seed: Option<u64>) -> PyResult<Self> {
        validate_positive_f64(target_temp, "target_temp")?;
        validate_positive_f64(tau, "coupling time constant tau")?;
        validate_positive_f64(dt, "timestep dt")?;
        validate_n_dof(n_dof)?;
        Ok(Self {
            inner: VelocityRescale::new(target_temp, tau, dt, n_dof, seed),
        })
    }

    /// Perform one NVT step.
    fn step(&mut self, state: &mut PyMDState, compute_forces: &Bound<'_, PyAny>) -> PyResult<()> {
        self.inner
            .try_step(&mut state.inner, |positions| {
                let n_atoms = positions.len();
                let result = compute_forces.call1((vec3_to_positions(positions),))?;
                extract_and_validate_forces(&result, n_atoms)
            })
            .map_err(thermostat_step_err_to_pyerr)
    }

    /// Set target temperature.
    fn set_temperature(&mut self, target_temp: f64) -> PyResult<()> {
        validate_positive_f64(target_temp, "target_temp")?;
        self.inner.set_temperature(target_temp);
        Ok(())
    }

    /// First half of velocity rescale step (position update). Call step_finalize after computing new forces.
    fn step_init(&mut self, state: &mut PyMDState, forces: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(forces.len(), state.inner.num_atoms(), "forces")?;
        state.inner.set_forces(&positions_to_vec3(&forces));
        self.inner.step_init(&mut state.inner);
        Ok(())
    }

    /// Complete velocity rescale step after step_init.
    fn step_finalize(&mut self, state: &mut PyMDState, new_forces: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(new_forces.len(), state.inner.num_atoms(), "new_forces")?;
        self.inner
            .step_finalize(&mut state.inner, &positions_to_vec3(&new_forces))
            .map_err(|err| PyValueError::new_err(err.to_string()))
    }

    /// Perform one complete velocity rescale step with pre-computed forces.
    fn step_with_forces(
        &mut self,
        state: &mut PyMDState,
        forces: Vec<[f64; 3]>,
        new_forces: Vec<[f64; 3]>,
    ) -> PyResult<()> {
        self.step_init(state, forces)?;
        self.step_finalize(state, new_forces)
    }
}

// === NPT State ===

/// State for NPT molecular dynamics.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "NPTState")]
pub struct PyNPTState {
    inner: md::NPTState,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyNPTState {
    /// Create a new NPT state.
    #[new]
    #[pyo3(signature = (positions, masses, cell, pbc = None))]
    fn new(
        positions: Vec<[f64; 3]>,
        masses: Vec<f64>,
        cell: [[f64; 3]; 3],
        pbc: Option<[bool; 3]>,
    ) -> PyResult<Self> {
        if positions.len() != masses.len() {
            return Err(PyValueError::new_err(format!(
                "Masses length ({}) must match positions length ({})",
                masses.len(),
                positions.len()
            )));
        }

        // Validate masses before passing to core library (which panics on invalid)
        for (idx, &mass) in masses.iter().enumerate() {
            if !mass.is_finite() || mass <= 0.0 {
                return Err(PyValueError::new_err(format!(
                    "Mass at index {idx} must be positive and finite, got {mass}"
                )));
            }
        }

        // Validate cell matrix for finiteness
        for (row_idx, row) in cell.iter().enumerate() {
            for (col_idx, &val) in row.iter().enumerate() {
                if !val.is_finite() {
                    return Err(PyValueError::new_err(format!(
                        "Cell matrix element [{row_idx}][{col_idx}] must be finite, got {val}"
                    )));
                }
            }
        }

        let pos_vec = positions_to_vec3(&positions);
        let cell_mat = array_to_mat3(cell);
        // NPT always has a cell, so default pbc to true
        let pbc_arr = default_pbc(pbc, true);

        Ok(Self {
            inner: md::NPTState::new(pos_vec, masses, cell_mat, pbc_arr),
        })
    }

    #[getter]
    fn positions(&self) -> Vec<[f64; 3]> {
        vec3_to_positions(&self.inner.positions)
    }

    #[setter]
    fn set_positions(&mut self, positions: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(positions.len(), self.inner.num_atoms(), "positions")?;
        self.inner.positions = positions_to_vec3(&positions);
        Ok(())
    }

    #[getter]
    fn velocities(&self) -> Vec<[f64; 3]> {
        vec3_to_positions(&self.inner.velocities)
    }

    #[setter]
    fn set_velocities(&mut self, velocities: Vec<[f64; 3]>) -> PyResult<()> {
        validate_force_count(velocities.len(), self.inner.num_atoms(), "velocities")?;
        self.inner.velocities = positions_to_vec3(&velocities);
        Ok(())
    }

    #[getter]
    fn cell(&self) -> [[f64; 3]; 3] {
        mat3_to_array(&self.inner.cell)
    }

    /// Cell volume in Angstrom³.
    fn volume(&self) -> f64 {
        self.inner.volume()
    }

    /// Kinetic energy in eV.
    fn kinetic_energy(&self) -> f64 {
        self.inner.kinetic_energy()
    }

    /// Instantaneous temperature in Kelvin.
    fn temperature(&self) -> f64 {
        self.inner.temperature()
    }

    /// Number of atoms.
    fn num_atoms(&self) -> usize {
        self.inner.num_atoms()
    }
}

// === NPT Integrator ===

/// NPT integrator using Nosé-Hoover thermostat and isotropic barostat.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.md", name = "NPTIntegrator")]
pub struct PyNPTIntegrator {
    inner: NPTIntegrator,
}

impl_stub_type_for_mut!(PyMDState, PyLangevinIntegrator, PyNPTState, PyNPTIntegrator);

#[gen_stub_pymethods]
#[pymethods]
impl PyNPTIntegrator {
    /// Create a new NPT integrator.
    ///
    /// Args:
    ///     temperature: Target temperature in Kelvin (must be positive)
    ///     pressure: Target pressure in GPa
    ///     tau_t: Thermostat time constant in fs (must be positive)
    ///     tau_p: Barostat time constant in fs (must be positive)
    ///     dt: Time step in fs (must be positive)
    ///     n_atoms: Number of atoms (must be >= 2)
    ///     total_mass: Total system mass in amu (must be positive)
    #[new]
    fn new(
        temperature: f64,
        pressure: f64,
        tau_t: f64,
        tau_p: f64,
        dt: f64,
        n_atoms: usize,
        total_mass: f64,
    ) -> PyResult<Self> {
        validate_positive_f64(temperature, "temperature")?;
        if !pressure.is_finite() {
            return Err(PyValueError::new_err(format!(
                "pressure must be finite, got {pressure}"
            )));
        }
        validate_positive_f64(tau_t, "thermostat time constant tau_t")?;
        validate_positive_f64(tau_p, "barostat time constant tau_p")?;
        validate_positive_f64(dt, "timestep dt")?;
        validate_positive_f64(total_mass, "total_mass")?;
        if n_atoms < 2 {
            return Err(PyValueError::new_err(
                "NPTIntegrator requires n_atoms >= 2 for meaningful NPT dynamics",
            ));
        }
        let config = NPTConfig::new(temperature, pressure, tau_t, tau_p, dt);
        Ok(Self {
            inner: NPTIntegrator::new(config, n_atoms, total_mass),
        })
    }

    /// Instantaneous pressure in GPa from stress tensor.
    ///
    /// Args:
    ///     stress: 3x3 stress tensor in eV/Å³ (row-major)
    fn pressure(&self, stress: [[f64; 3]; 3]) -> f64 {
        self.inner.pressure(&array_to_mat3(stress))
    }

    /// First half of NPT step. Call step_finalize after computing new forces and stress.
    fn step_init(
        &mut self,
        state: &mut PyNPTState,
        forces: Vec<[f64; 3]>,
        stress: [[f64; 3]; 3],
    ) -> PyResult<()> {
        validate_npt_atom_count(&self.inner, state.inner.num_atoms())?;
        validate_force_count(forces.len(), state.inner.num_atoms(), "forces")?;
        state.inner.forces = positions_to_vec3(&forces);
        let stress_mat = array_to_mat3(stress);
        self.inner.step_init(&mut state.inner, &stress_mat);
        Ok(())
    }

    /// Complete NPT step after step_init.
    fn step_finalize(
        &mut self,
        state: &mut PyNPTState,
        new_forces: Vec<[f64; 3]>,
        new_stress: [[f64; 3]; 3],
    ) -> PyResult<()> {
        validate_npt_atom_count(&self.inner, state.inner.num_atoms())?;
        validate_force_count(new_forces.len(), state.inner.num_atoms(), "new_forces")?;
        let force_vec = positions_to_vec3(&new_forces);
        let stress_mat = array_to_mat3(new_stress);
        self.inner
            .step_finalize(&mut state.inner, &force_vec, &stress_mat);
        Ok(())
    }

    /// Perform one complete NPT step with pre-computed forces and stress.
    fn step_with_forces_and_stress(
        &mut self,
        state: &mut PyNPTState,
        forces: Vec<[f64; 3]>,
        stress: [[f64; 3]; 3],
        new_forces: Vec<[f64; 3]>,
        new_stress: [[f64; 3]; 3],
    ) -> PyResult<()> {
        self.step_init(state, forces, stress)?;
        self.step_finalize(state, new_forces, new_stress)
    }
}

/// Register md functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<PyMDState>()?;
    module.add_class::<PyLangevinIntegrator>()?;
    module.add_class::<PyNoseHooverChain>()?;
    module.add_class::<PyVelocityRescale>()?;
    module.add_class::<PyNPTState>()?;
    module.add_class::<PyNPTIntegrator>()?;
    module.add_function(wrap_pyfunction!(velocity_verlet_step_init, module)?)?;
    module.add_function(wrap_pyfunction!(velocity_verlet_finalize, module)?)?;
    module.add_function(wrap_pyfunction!(velocity_verlet_step, module)?)?;
    module.add_function(wrap_pyfunction!(langevin_step_init, module)?)?;
    module.add_function(wrap_pyfunction!(langevin_step_finalize, module)?)?;
    module.add_function(wrap_pyfunction!(langevin_step_with_forces, module)?)?;
    Ok(())
}
