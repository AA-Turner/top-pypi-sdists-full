//! WASM quantity bindings with runtime unit checks.

use wasm_bindgen::prelude::*;

use crate::units::{DynQuantity, UnitsError};

fn to_js_err(err: UnitsError) -> JsError {
    JsError::new(&err.to_string())
}

/// JavaScript quantity wrapper.
#[wasm_bindgen(js_name = "Quantity")]
#[derive(Clone)]
pub struct JsQuantity {
    inner: DynQuantity,
}

#[wasm_bindgen(js_class = "Quantity")]
impl JsQuantity {
    /// Create a quantity from value and unit string.
    #[wasm_bindgen(constructor)]
    pub fn new(value: f64, unit: &str) -> Result<JsQuantity, JsError> {
        DynQuantity::new(value, unit)
            .map(|inner| Self { inner })
            .map_err(to_js_err)
    }

    /// Convenience constructor in eV.
    #[wasm_bindgen(js_name = "ev")]
    pub fn ev(value: f64) -> Result<JsQuantity, JsError> {
        Self::new(value, "eV")
    }

    /// Convenience constructor in angstrom.
    #[wasm_bindgen(js_name = "angstrom")]
    pub fn angstrom(value: f64) -> Result<JsQuantity, JsError> {
        Self::new(value, "angstrom")
    }

    /// Convenience constructor in amu.
    #[wasm_bindgen(js_name = "amu")]
    pub fn amu(value: f64) -> Result<JsQuantity, JsError> {
        Self::new(value, "amu")
    }

    /// Convenience constructor in femtoseconds.
    #[wasm_bindgen(js_name = "fs")]
    pub fn fs(value: f64) -> Result<JsQuantity, JsError> {
        Self::new(value, "fs")
    }

    /// Convenience constructor in Kelvin.
    #[wasm_bindgen(js_name = "kelvin")]
    pub fn kelvin(value: f64) -> Result<JsQuantity, JsError> {
        Self::new(value, "K")
    }

    /// Convert quantity to target unit.
    pub fn to(&self, unit: &str) -> Result<f64, JsError> {
        self.inner.to_unit(unit).map_err(to_js_err)
    }

    /// Quantity dimension label.
    #[wasm_bindgen(getter)]
    pub fn dimension(&self) -> String {
        self.inner.dimension().as_str().to_string()
    }

    /// Display unit label.
    #[wasm_bindgen(getter)]
    pub fn unit(&self) -> String {
        self.inner.display_unit().as_str().to_string()
    }

    /// Numeric value in display unit.
    #[wasm_bindgen(getter)]
    pub fn value(&self) -> Result<f64, JsError> {
        self.inner.value().map_err(to_js_err)
    }

    /// Add two quantities with matching dimensions.
    pub fn add(&self, other: &JsQuantity) -> Result<JsQuantity, JsError> {
        self.inner
            .try_add(other.inner)
            .map(|inner| Self { inner })
            .map_err(to_js_err)
    }

    /// Subtract two quantities with matching dimensions.
    pub fn sub(&self, other: &JsQuantity) -> Result<JsQuantity, JsError> {
        self.inner
            .try_sub(other.inner)
            .map(|inner| Self { inner })
            .map_err(to_js_err)
    }

    /// Multiply by scalar.
    #[wasm_bindgen(js_name = "mulScalar")]
    pub fn mul_scalar(&self, scalar: f64) -> Result<JsQuantity, JsError> {
        self.inner
            .try_mul_scalar(scalar)
            .map(|inner| Self { inner })
            .map_err(to_js_err)
    }

    /// Divide by scalar.
    #[wasm_bindgen(js_name = "divScalar")]
    pub fn div_scalar(&self, scalar: f64) -> Result<JsQuantity, JsError> {
        self.inner
            .try_div_scalar(scalar)
            .map(|inner| Self { inner })
            .map_err(to_js_err)
    }
}

// === WASM unit constant factories ===
// wasm-bindgen cannot export pre-constructed instances as module-level
// constants, so each "constant" is a factory that returns Quantity(1.0, unit).
// Callers should hoist: `const EV = EV_UNIT();` then reuse `EV`.

macro_rules! wasm_unit_constant {
    ($rust_name:ident, $js_name:literal, $unit_str:literal, $doc:literal) => {
        #[doc = $doc]
        #[wasm_bindgen(js_name = $js_name)]
        pub fn $rust_name() -> Result<JsQuantity, JsError> {
            JsQuantity::new(1.0, $unit_str)
        }
    };
}

// Energy
wasm_unit_constant!(ev_constant, "EV", "eV", "1 electronvolt.");
wasm_unit_constant!(mev_constant, "MEV", "meV", "1 millielectronvolt.");
wasm_unit_constant!(kev_constant, "KEV", "keV", "1 kiloelectronvolt.");
wasm_unit_constant!(joule_constant, "JOULE", "J", "1 joule.");
wasm_unit_constant!(kj_constant, "KJ", "kJ", "1 kilojoule.");
wasm_unit_constant!(cal_constant, "CAL", "cal", "1 calorie.");
wasm_unit_constant!(kcal_constant, "KCAL", "kcal", "1 kilocalorie.");
wasm_unit_constant!(kj_per_mol_constant, "KJ_PER_MOL", "kJ/mol", "1 kJ/mol.");
wasm_unit_constant!(
    kcal_per_mol_constant,
    "KCAL_PER_MOL",
    "kcal/mol",
    "1 kcal/mol."
);
wasm_unit_constant!(hartree_constant, "HARTREE", "Ha", "1 hartree.");
wasm_unit_constant!(ry_constant, "RY", "Ry", "1 rydberg.");
wasm_unit_constant!(invcm_constant, "INVCM", "cm^-1", "1 inverse centimeter.");
// Length
wasm_unit_constant!(angstrom_constant, "ANGSTROM", "angstrom", "1 angstrom.");
wasm_unit_constant!(bohr_constant, "BOHR", "bohr", "1 bohr radius.");
wasm_unit_constant!(meter_constant, "METER", "m", "1 meter.");
wasm_unit_constant!(nm_constant, "NM", "nm", "1 nanometer.");
wasm_unit_constant!(pm_constant, "PM", "pm", "1 picometer.");
wasm_unit_constant!(cm_constant, "CM", "cm", "1 centimeter.");
wasm_unit_constant!(um_constant, "UM", "um", "1 micrometer.");
// Mass
wasm_unit_constant!(amu_constant, "AMU", "amu", "1 atomic mass unit.");
wasm_unit_constant!(kg_constant, "KG", "kg", "1 kilogram.");
wasm_unit_constant!(gram_constant, "GRAM", "g", "1 gram.");
// Time
wasm_unit_constant!(fs_constant, "FS", "fs", "1 femtosecond.");
wasm_unit_constant!(ps_constant, "PS", "ps", "1 picosecond.");
wasm_unit_constant!(ns_constant, "NS", "ns", "1 nanosecond.");
wasm_unit_constant!(us_constant, "US", "us", "1 microsecond.");
wasm_unit_constant!(ms_constant, "MS", "ms", "1 millisecond.");
wasm_unit_constant!(second_constant, "SECOND", "s", "1 second.");
// Temperature (Celsius omitted: offset-based unit breaks scalar * UNIT pattern)
wasm_unit_constant!(kelvin_constant, "KELVIN", "K", "1 kelvin.");
// Pressure
wasm_unit_constant!(gpa_constant, "GPA", "GPa", "1 gigapascal.");
wasm_unit_constant!(mpa_constant, "MPA", "MPa", "1 megapascal.");
wasm_unit_constant!(kpa_constant, "KPA", "kPa", "1 kilopascal.");
wasm_unit_constant!(pa_constant, "PA", "Pa", "1 pascal.");
wasm_unit_constant!(bar_constant, "BAR", "bar", "1 bar.");
wasm_unit_constant!(kbar_constant, "KBAR", "kbar", "1 kilobar.");
wasm_unit_constant!(millibar_constant, "MILLIBAR", "mbar", "1 millibar.");
wasm_unit_constant!(atm_constant, "ATM", "atm", "1 atmosphere.");
// Force
wasm_unit_constant!(newton_constant, "NEWTON", "N", "1 newton.");
wasm_unit_constant!(
    ev_per_angstrom_constant,
    "EV_PER_ANGSTROM",
    "eV/A",
    "1 eV/angstrom."
);
