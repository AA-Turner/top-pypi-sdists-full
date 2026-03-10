//! Python quantity and unit mode bindings.

use std::str::FromStr;

use pyo3::exceptions::PyTypeError;
use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pyfunction, gen_stub_pymethods};

use crate::units::{self, Dimension, DynQuantity, UnitMode, UnitSymbol, UnitsError};

/// Relative-tolerance equality for SI-base-unit values.
/// Pure relative check: two identical zero values compare equal.
fn approx_eq(lhs: f64, rhs: f64) -> bool {
    let diff = (lhs - rhs).abs();
    let magnitude = lhs.abs().max(rhs.abs());
    diff <= magnitude * 1e-12
}

#[allow(missing_docs)]
mod py_exceptions {
    use pyo3::create_exception;
    use pyo3::exceptions::PyValueError;

    create_exception!(crate::python::units, UnitError, PyValueError);
    create_exception!(crate::python::units, DimensionError, UnitError);
}

pub use py_exceptions::{DimensionError, UnitError};

const EXPORTED_UNIT_CONSTANTS: [(&str, UnitSymbol); 39] = [
    // Energy
    ("EV", UnitSymbol::Electronvolt),
    ("MEV", UnitSymbol::MilliElectronvolt),
    ("KEV", UnitSymbol::KiloElectronvolt),
    ("JOULE", UnitSymbol::Joule),
    ("KJ", UnitSymbol::Kilojoule),
    ("CAL", UnitSymbol::Calorie),
    ("KCAL", UnitSymbol::Kilocalorie),
    ("KJ_PER_MOL", UnitSymbol::KilojoulePerMol),
    ("KCAL_PER_MOL", UnitSymbol::KilocaloriePerMol),
    ("HARTREE", UnitSymbol::Hartree),
    ("RY", UnitSymbol::Rydberg),
    ("INVCM", UnitSymbol::InverseCentimeter),
    // Length
    ("ANGSTROM", UnitSymbol::Angstrom),
    ("BOHR", UnitSymbol::Bohr),
    ("METER", UnitSymbol::Meter),
    ("NM", UnitSymbol::Nanometer),
    ("PM", UnitSymbol::Picometer),
    ("CM", UnitSymbol::Centimeter),
    ("UM", UnitSymbol::Micrometer),
    // Mass
    ("AMU", UnitSymbol::AtomicMassUnit),
    ("KG", UnitSymbol::Kilogram),
    ("GRAM", UnitSymbol::Gram),
    // Time
    ("FS", UnitSymbol::Femtosecond),
    ("PS", UnitSymbol::Picosecond),
    ("NS", UnitSymbol::Nanosecond),
    ("US", UnitSymbol::Microsecond),
    ("MS", UnitSymbol::Millisecond),
    ("SECOND", UnitSymbol::Second),
    // Temperature (Celsius omitted: offset-based unit breaks scalar * UNIT pattern)
    ("KELVIN", UnitSymbol::Kelvin),
    // Pressure
    ("GPA", UnitSymbol::Gigapascal),
    ("MPA", UnitSymbol::Megapascal),
    ("KPA", UnitSymbol::Kilopascal),
    ("PA", UnitSymbol::Pascal),
    ("BAR", UnitSymbol::Bar),
    ("KBAR", UnitSymbol::Kilobar),
    ("MILLIBAR", UnitSymbol::Millibar),
    ("ATM", UnitSymbol::Atmosphere),
    // Force
    ("NEWTON", UnitSymbol::Newton),
    ("EV_PER_ANGSTROM", UnitSymbol::ElectronvoltPerAngstrom),
];

/// Return unit constants exported on `ferrox.units`.
pub fn exported_unit_constants() -> &'static [(&'static str, UnitSymbol)] {
    &EXPORTED_UNIT_CONSTANTS
}

pub(crate) fn map_units_error_to_pyerr(units_error: UnitsError) -> PyErr {
    match units_error {
        UnitsError::DimensionMismatch { .. } | UnitsError::WrongDimension { .. } => {
            DimensionError::new_err(units_error.to_string())
        }
        _ => UnitError::new_err(units_error.to_string()),
    }
}

fn add_unit_constant(module: &Bound<'_, PyModule>, name: &str, unit: UnitSymbol) -> PyResult<()> {
    let quantity = PyQuantity::new_internal(1.0, unit).map_err(map_units_error_to_pyerr)?;
    let py_quantity = Py::new(module.py(), quantity)?;
    module.add(name, py_quantity)?;
    Ok(())
}

fn extract_quantity_operand(
    other: &Bound<'_, PyAny>,
    operation_name: &str,
) -> PyResult<DynQuantity> {
    other
        .extract::<PyRef<'_, PyQuantity>>()
        .map(|quantity_ref| quantity_ref.inner)
        .map_err(|_| PyTypeError::new_err(format!("{operation_name} expects another Quantity")))
}

/// Python quantity wrapper with runtime dimension checks.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.units", name = "Quantity")]
#[derive(Clone)]
pub struct PyQuantity {
    /// Inner runtime-typed quantity.
    pub inner: DynQuantity,
}

impl PyQuantity {
    fn new_internal(value: f64, unit_symbol: UnitSymbol) -> Result<Self, UnitsError> {
        DynQuantity::from_unit_symbol(value, unit_symbol).map(|inner| Self { inner })
    }

    fn scalar_op(
        &self,
        other: &Bound<'_, PyAny>,
        op_fn: fn(DynQuantity, f64) -> Result<DynQuantity, UnitsError>,
        op_name: &str,
        op_symbol: &str,
    ) -> PyResult<Self> {
        if let Ok(scalar) = other.extract::<f64>() {
            return op_fn(self.inner, scalar)
                .map(|inner| Self { inner })
                .map_err(map_units_error_to_pyerr);
        }
        if other.extract::<PyRef<'_, PyQuantity>>().is_ok() {
            return Err(UnitError::new_err(format!(
                "Quantity{op_symbol}Quantity is not supported in v1; use scalar only"
            )));
        }
        Err(PyTypeError::new_err(format!(
            "Quantity {op_name} expects a scalar float"
        )))
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl PyQuantity {
    /// Create a quantity from value and unit string.
    #[new]
    fn new(value: f64, unit: &str) -> PyResult<Self> {
        DynQuantity::new(value, unit)
            .map(|inner| Self { inner })
            .map_err(map_units_error_to_pyerr)
    }

    /// Convert value to a requested unit.
    fn to(&self, unit: &str) -> PyResult<f64> {
        self.inner.to_unit(unit).map_err(map_units_error_to_pyerr)
    }

    /// Quantity value in its display unit.
    #[getter]
    fn value(&self) -> PyResult<f64> {
        self.inner.value().map_err(map_units_error_to_pyerr)
    }

    /// Display unit symbol for this quantity.
    #[getter]
    fn unit(&self) -> String {
        self.inner.display_unit().as_str().to_string()
    }

    /// Dimension label.
    #[getter]
    fn dimension(&self) -> String {
        self.inner.dimension().as_str().to_string()
    }

    fn __add__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        let other_quantity = extract_quantity_operand(other, "Quantity addition")?;
        self.inner
            .try_add(other_quantity)
            .map(|inner| Self { inner })
            .map_err(map_units_error_to_pyerr)
    }

    fn __sub__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        let other_quantity = extract_quantity_operand(other, "Quantity subtraction")?;
        self.inner
            .try_sub(other_quantity)
            .map(|inner| Self { inner })
            .map_err(map_units_error_to_pyerr)
    }

    fn __mul__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        self.scalar_op(other, DynQuantity::try_mul_scalar, "multiplication", "*")
    }

    fn __rmul__(&self, scalar: f64) -> PyResult<Self> {
        self.inner
            .try_mul_scalar(scalar)
            .map(|inner| Self { inner })
            .map_err(map_units_error_to_pyerr)
    }

    fn __truediv__(&self, other: &Bound<'_, PyAny>) -> PyResult<Self> {
        self.scalar_op(other, DynQuantity::try_div_scalar, "division", "/")
    }

    fn __neg__(&self) -> PyResult<Self> {
        self.inner
            .try_mul_scalar(-1.0)
            .map(|inner| Self { inner })
            .map_err(map_units_error_to_pyerr)
    }

    /// Approximate equality via SI base-unit values with relative tolerance 1e-12.
    /// Uses `si_value()` instead of `to_default()` to avoid overflow when the
    /// default unit scales up (e.g. J -> eV for large magnitudes).
    /// Intentionally unhashable: approx equality prevents a consistent `__hash__`.
    fn __eq__(&self, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        let other_quantity = match other.extract::<PyRef<'_, PyQuantity>>() {
            Ok(quantity_ref) => quantity_ref.inner,
            Err(_) => return Ok(false),
        };
        if self.inner.dimension() != other_quantity.dimension() {
            return Ok(false);
        }
        Ok(approx_eq(self.inner.si_value(), other_quantity.si_value()))
    }

    fn __repr__(&self) -> PyResult<String> {
        let value = self.inner.value().map_err(map_units_error_to_pyerr)?;
        Ok(format!(
            "Quantity({value}, \"{}\")",
            self.inner.display_unit().as_str()
        ))
    }
}

/// Set global unit mode.
#[gen_stub_pyfunction(module = "ferrox._ferrox.units")]
#[pyfunction]
pub fn set_unit_mode(mode: &str) -> PyResult<()> {
    let parsed_mode = UnitMode::from_str(mode)
        .map_err(|_| UnitError::new_err(format!("invalid unit mode: {mode}")))?;
    units::set_unit_mode(parsed_mode);
    Ok(())
}

/// Get current global unit mode.
#[gen_stub_pyfunction(module = "ferrox._ferrox.units")]
#[pyfunction]
pub fn get_unit_mode() -> String {
    units::get_unit_mode().as_str().to_string()
}

/// Top-level mode setter alias (`ferrox.set_unit_mode(...)`).
#[gen_stub_pyfunction(module = "ferrox._ferrox")]
#[pyfunction(name = "set_unit_mode")]
pub fn set_unit_mode_top_level(mode: &str) -> PyResult<()> {
    set_unit_mode(mode)
}

/// Top-level mode getter alias (`ferrox.get_unit_mode()`).
#[gen_stub_pyfunction(module = "ferrox._ferrox")]
#[pyfunction(name = "get_unit_mode")]
pub fn get_unit_mode_top_level() -> String {
    get_unit_mode()
}

/// Coerce a raw float according to unit mode.
pub fn coerce_raw_float(
    py: Python<'_>,
    value: f64,
    expected_dimension: Dimension,
    parameter_name: &str,
) -> PyResult<f64> {
    match units::get_unit_mode() {
        UnitMode::Auto => Ok(value),
        UnitMode::Warn => {
            let warnings_module = py.import("warnings")?;
            warnings_module.call_method1(
                "warn",
                (format!(
                    "{parameter_name} received raw float without units; assuming default {} for {expected_dimension}",
                    units::default_unit_for_dimension(expected_dimension).as_str()
                ),),
            )?;
            Ok(value)
        }
        UnitMode::Strict => Err(UnitError::new_err(format!(
            "{parameter_name} requires Quantity in strict mode (expected {expected_dimension})"
        ))),
    }
}

/// Register units submodule contents.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add("UnitError", module.py().get_type::<UnitError>())?;
    module.add("DimensionError", module.py().get_type::<DimensionError>())?;
    module.add_class::<PyQuantity>()?;
    module.add_function(wrap_pyfunction!(set_unit_mode, module)?)?;
    module.add_function(wrap_pyfunction!(get_unit_mode, module)?)?;
    for &(constant_name, unit_symbol) in exported_unit_constants() {
        add_unit_constant(module, constant_name, unit_symbol)?;
    }
    Ok(())
}

/// Register top-level mode aliases on the root module.
pub fn register_top_level(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(set_unit_mode_top_level, module)?)?;
    module.add_function(wrap_pyfunction!(get_unit_mode_top_level, module)?)?;
    Ok(())
}
