//! Runtime-typed physical quantity helpers for Python/WASM boundary layers.
//!
//! [`DynQuantity`] wraps SI quantities from [`uom`] with runtime dimension checks,
//! unit conversion, and string-based unit parsing — suitable for dynamic contexts
//! like Python bindings where compile-time unit types are impractical.
//!
//! ```
//! use ferrox::units::{DynQuantity, Dimension};
//!
//! let length = DynQuantity::new(5.43, "angstrom").unwrap();
//! assert_eq!(length.dimension(), Dimension::Length);
//! assert!((length.to_unit("nm").unwrap() - 0.543).abs() < 1e-10);
//!
//! let doubled = length.try_mul_scalar(2.0).unwrap();
//! assert!((doubled.to_unit("angstrom").unwrap() - 10.86).abs() < 1e-10);
//! ```

use std::fmt;
use std::str::FromStr;
use std::sync::atomic::{AtomicU8, Ordering};

use uom::si::electric_charge::coulomb;
use uom::si::energy::{calorie, electronvolt, hartree, joule, kilocalorie, kilojoule};
use uom::si::f64 as si;
use uom::si::force::{nanonewton, newton};
use uom::si::length::{angstrom, bohr_radius, centimeter, meter, micrometer, nanometer, picometer};
use uom::si::mass::{dalton, gram, kilogram};
use uom::si::pressure::{atmosphere, bar, gigapascal, kilopascal, megapascal, pascal};
use uom::si::thermodynamic_temperature::{degree_celsius, kelvin};
use uom::si::time::{femtosecond, microsecond, millisecond, nanosecond, picosecond, second};

// === Physical Constants for Manual Conversions ===

/// Avogadro constant (2019 SI, exact).
const AVOGADRO: f64 = 6.022_140_76e23;

/// 1 eV in joules (2019 SI, exact).
const EV_IN_JOULES: f64 = 1.602_176_634e-19;

/// h*c in J·m for wavenumber (cm⁻¹) → energy conversion.
/// h = 6.62607015e-34 J·s, c = 299792458 m/s  →  h*c = 1.98644568...e-25 J·m
/// Per cm⁻¹: h*c * 100 (cm→m) = 1.98644568...e-23 J
const HC_IN_JOULE_CM: f64 = 1.986_445_857_148_12e-23;

/// 1 eV/Å in newtons: (1.602176634e-19 J) / (1e-10 m).
const EV_PER_ANGSTROM_IN_NEWTON: f64 = EV_IN_JOULES / 1e-10;

/// Physical dimension tracked by [`DynQuantity`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Dimension {
    /// Distance.
    Length,
    /// Energy.
    Energy,
    /// Mass.
    Mass,
    /// Time.
    Time,
    /// Temperature.
    Temperature,
    /// Pressure.
    Pressure,
    /// Force.
    Force,
    /// Electric charge.
    Charge,
    /// Unitless scalar.
    Dimensionless,
}

impl Dimension {
    /// Lowercase human-readable name.
    #[must_use]
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Length => "length",
            Self::Energy => "energy",
            Self::Mass => "mass",
            Self::Time => "time",
            Self::Temperature => "temperature",
            Self::Pressure => "pressure",
            Self::Force => "force",
            Self::Charge => "charge",
            Self::Dimensionless => "dimensionless",
        }
    }
}

impl fmt::Display for Dimension {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

macro_rules! define_unit_symbols {
    ($($(#[$meta:meta])* $variant:ident),+ $(,)?) => {
        /// Unit symbol used for display/conversion.
        #[derive(Debug, Clone, Copy, PartialEq, Eq)]
        pub enum UnitSymbol {
            $($(#[$meta])* $variant,)+
        }

        impl UnitSymbol {
            /// Every variant. Auto-kept in sync by the `define_unit_symbols!` macro.
            pub const ALL: &[Self] = &[$(Self::$variant,)+];
        }
    };
}

define_unit_symbols! {
    // Energy
    /// Electronvolt.
    Electronvolt,
    /// Millielectronvolt.
    MilliElectronvolt,
    /// Kiloelectronvolt.
    KiloElectronvolt,
    /// Joule.
    Joule,
    /// Kilojoule.
    Kilojoule,
    /// Calorie (thermochemical).
    Calorie,
    /// Kilocalorie (thermochemical).
    Kilocalorie,
    /// Kilojoule per mole (energy per particle).
    KilojoulePerMol,
    /// Kilocalorie per mole (energy per particle).
    KilocaloriePerMol,
    /// Hartree (atomic unit of energy).
    Hartree,
    /// Rydberg (0.5 Hartree).
    Rydberg,
    /// Inverse centimeter / wavenumber (spectroscopic energy).
    InverseCentimeter,
    // Length
    /// Angstrom.
    Angstrom,
    /// Bohr radius.
    Bohr,
    /// Meter.
    Meter,
    /// Nanometer.
    Nanometer,
    /// Picometer.
    Picometer,
    /// Centimeter.
    Centimeter,
    /// Micrometer.
    Micrometer,
    // Mass
    /// Atomic mass unit / dalton.
    AtomicMassUnit,
    /// Kilogram.
    Kilogram,
    /// Gram.
    Gram,
    // Time
    /// Femtosecond.
    Femtosecond,
    /// Picosecond.
    Picosecond,
    /// Nanosecond.
    Nanosecond,
    /// Microsecond.
    Microsecond,
    /// Millisecond.
    Millisecond,
    /// Second.
    Second,
    // Temperature
    /// Kelvin.
    Kelvin,
    /// Degree Celsius.
    Celsius,
    // Pressure
    /// Gigapascal.
    Gigapascal,
    /// Megapascal.
    Megapascal,
    /// Kilopascal.
    Kilopascal,
    /// Pascal.
    Pascal,
    /// Bar.
    Bar,
    /// Millibar (0.001 bar = 100 Pa).
    Millibar,
    /// Kilobar.
    Kilobar,
    /// Megabar.
    Megabar,
    /// Standard atmosphere.
    Atmosphere,
    // Force
    /// Newton.
    Newton,
    /// Nanonewton.
    NanoNewton,
    /// Electronvolt per angstrom (common in atomistic simulation).
    ElectronvoltPerAngstrom,
    // Charge
    /// Elementary charge.
    ElementaryCharge,
    /// Coulomb.
    Coulomb,
    // Dimensionless
    /// Unitless ratio.
    Ratio,
}

impl UnitSymbol {
    /// Return the corresponding physical dimension.
    #[must_use]
    pub fn dimension(self) -> Dimension {
        match self {
            Self::Electronvolt
            | Self::MilliElectronvolt
            | Self::KiloElectronvolt
            | Self::Joule
            | Self::Kilojoule
            | Self::Calorie
            | Self::Kilocalorie
            | Self::KilojoulePerMol
            | Self::KilocaloriePerMol
            | Self::Hartree
            | Self::Rydberg
            | Self::InverseCentimeter => Dimension::Energy,

            Self::Angstrom
            | Self::Bohr
            | Self::Meter
            | Self::Nanometer
            | Self::Picometer
            | Self::Centimeter
            | Self::Micrometer => Dimension::Length,

            Self::AtomicMassUnit | Self::Kilogram | Self::Gram => Dimension::Mass,

            Self::Femtosecond
            | Self::Picosecond
            | Self::Nanosecond
            | Self::Microsecond
            | Self::Millisecond
            | Self::Second => Dimension::Time,

            Self::Kelvin | Self::Celsius => Dimension::Temperature,

            Self::Gigapascal
            | Self::Megapascal
            | Self::Kilopascal
            | Self::Pascal
            | Self::Bar
            | Self::Millibar
            | Self::Kilobar
            | Self::Megabar
            | Self::Atmosphere => Dimension::Pressure,

            Self::Newton | Self::NanoNewton | Self::ElectronvoltPerAngstrom => Dimension::Force,

            Self::ElementaryCharge | Self::Coulomb => Dimension::Charge,

            Self::Ratio => Dimension::Dimensionless,
        }
    }

    /// Canonical text representation.
    #[must_use]
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Electronvolt => "eV",
            Self::MilliElectronvolt => "meV",
            Self::KiloElectronvolt => "keV",
            Self::Joule => "J",
            Self::Kilojoule => "kJ",
            Self::Calorie => "cal",
            Self::Kilocalorie => "kcal",
            Self::KilojoulePerMol => "kJ/mol",
            Self::KilocaloriePerMol => "kcal/mol",
            Self::Hartree => "Ha",
            Self::Rydberg => "Ry",
            Self::InverseCentimeter => "cm^-1",
            Self::Angstrom => "angstrom",
            Self::Bohr => "bohr",
            Self::Meter => "m",
            Self::Nanometer => "nm",
            Self::Picometer => "pm",
            Self::Centimeter => "cm",
            Self::Micrometer => "um",
            Self::AtomicMassUnit => "amu",
            Self::Kilogram => "kg",
            Self::Gram => "g",
            Self::Femtosecond => "fs",
            Self::Picosecond => "ps",
            Self::Nanosecond => "ns",
            Self::Microsecond => "us",
            Self::Millisecond => "ms",
            Self::Second => "s",
            Self::Kelvin => "K",
            Self::Celsius => "degC",
            Self::Gigapascal => "GPa",
            Self::Megapascal => "MPa",
            Self::Kilopascal => "kPa",
            Self::Pascal => "Pa",
            Self::Bar => "bar",
            Self::Millibar => "mbar",
            Self::Kilobar => "kbar",
            Self::Megabar => "megabar",
            Self::Atmosphere => "atm",
            Self::Newton => "N",
            Self::NanoNewton => "nN",
            Self::ElectronvoltPerAngstrom => "eV/A",
            Self::ElementaryCharge => "e",
            Self::Coulomb => "C",
            Self::Ratio => "1",
        }
    }
}

/// Unit parse/operation failures.
#[derive(Debug, Clone, PartialEq)]
pub enum UnitsError {
    /// Unknown unit string.
    UnknownUnit(String),
    /// Unit does not match quantity dimension.
    WrongDimension {
        /// Expected physical dimension.
        expected: Dimension,
        /// Received physical dimension.
        got: Dimension,
    },
    /// Arithmetic with incompatible dimensions.
    DimensionMismatch {
        /// Left-hand-side dimension.
        lhs: Dimension,
        /// Right-hand-side dimension.
        rhs: Dimension,
    },
    /// Operation is not implemented in v1.
    UnsupportedOperation(&'static str),
    /// Value is not finite.
    NonFiniteValue(f64),
}

impl fmt::Display for UnitsError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnknownUnit(unit_name) => write!(formatter, "unknown unit: {unit_name}"),
            Self::WrongDimension { expected, got } => {
                write!(
                    formatter,
                    "wrong unit dimension: expected {expected}, got {got}"
                )
            }
            Self::DimensionMismatch { lhs, rhs } => {
                write!(formatter, "dimension mismatch: {lhs} vs {rhs}")
            }
            Self::UnsupportedOperation(operation_name) => {
                write!(
                    formatter,
                    "unsupported quantity operation: {operation_name}"
                )
            }
            Self::NonFiniteValue(raw_value) => {
                write!(formatter, "quantity value must be finite, got {raw_value}")
            }
        }
    }
}

impl std::error::Error for UnitsError {}

/// Runtime-typed quantity wrapper.
#[derive(Debug, Clone, Copy, PartialEq)]
#[allow(missing_docs)]
pub enum DynQuantity {
    /// Length.
    Length {
        quantity: si::Length,
        display_unit: UnitSymbol,
    },
    /// Energy.
    Energy {
        quantity: si::Energy,
        display_unit: UnitSymbol,
    },
    /// Mass.
    Mass {
        quantity: si::Mass,
        display_unit: UnitSymbol,
    },
    /// Time.
    Time {
        quantity: si::Time,
        display_unit: UnitSymbol,
    },
    /// Temperature.
    Temperature {
        quantity: si::ThermodynamicTemperature,
        display_unit: UnitSymbol,
    },
    /// Pressure.
    Pressure {
        quantity: si::Pressure,
        display_unit: UnitSymbol,
    },
    /// Force.
    Force {
        quantity: si::Force,
        display_unit: UnitSymbol,
    },
    /// Electric charge.
    Charge {
        quantity: si::ElectricCharge,
        display_unit: UnitSymbol,
    },
    /// Unitless scalar.
    Dimensionless { value: f64 },
}

impl DynQuantity {
    /// Verify the value is finite in its display unit, rejecting overflow from arithmetic.
    fn check_finite(self) -> Result<Self, UnitsError> {
        self.value()?;
        Ok(self)
    }

    /// Create a quantity from a value and unit string.
    ///
    /// The `unit_name` is parsed case-insensitively and supports common aliases
    /// (e.g. `"Å"`, `"angstrom"`, `"A"` all map to [`UnitSymbol::Angstrom`]).
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::units::DynQuantity;
    ///
    /// let energy = DynQuantity::new(1.5, "eV").unwrap();
    /// let joules = energy.to_unit("J").unwrap();
    /// assert!((joules - 1.5 * 1.602_176_634e-19).abs() < 1e-30);
    ///
    /// // Unknown unit names produce an error
    /// assert!(DynQuantity::new(1.0, "foobar").is_err());
    /// ```
    pub fn new(value: f64, unit_name: &str) -> Result<Self, UnitsError> {
        let unit_symbol = UnitSymbol::from_str(unit_name)?;
        Self::from_unit_symbol(value, unit_symbol)
    }

    pub(crate) fn from_unit_symbol(
        value: f64,
        unit_symbol: UnitSymbol,
    ) -> Result<Self, UnitsError> {
        if !value.is_finite() {
            return Err(UnitsError::NonFiniteValue(value));
        }
        let quantity = match unit_symbol {
            // === Energy ===
            UnitSymbol::Electronvolt => Self::Energy {
                quantity: si::Energy::new::<electronvolt>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::MilliElectronvolt => Self::Energy {
                quantity: si::Energy::new::<electronvolt>(value * 1e-3),
                display_unit: unit_symbol,
            },
            UnitSymbol::KiloElectronvolt => Self::Energy {
                quantity: si::Energy::new::<electronvolt>(value * 1e3),
                display_unit: unit_symbol,
            },
            UnitSymbol::Joule => Self::Energy {
                quantity: si::Energy::new::<joule>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Kilojoule => Self::Energy {
                quantity: si::Energy::new::<kilojoule>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Calorie => Self::Energy {
                quantity: si::Energy::new::<calorie>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Kilocalorie => Self::Energy {
                quantity: si::Energy::new::<kilocalorie>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::KilojoulePerMol => Self::Energy {
                quantity: si::Energy::new::<joule>(value * 1e3 / AVOGADRO),
                display_unit: unit_symbol,
            },
            UnitSymbol::KilocaloriePerMol => Self::Energy {
                quantity: si::Energy::new::<joule>(value * 4184.0 / AVOGADRO),
                display_unit: unit_symbol,
            },
            UnitSymbol::Hartree => Self::Energy {
                quantity: si::Energy::new::<hartree>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Rydberg => Self::Energy {
                quantity: si::Energy::new::<hartree>(value * 0.5),
                display_unit: unit_symbol,
            },
            UnitSymbol::InverseCentimeter => Self::Energy {
                quantity: si::Energy::new::<joule>(value * HC_IN_JOULE_CM),
                display_unit: unit_symbol,
            },

            // === Length ===
            UnitSymbol::Angstrom => Self::Length {
                quantity: si::Length::new::<angstrom>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Bohr => Self::Length {
                quantity: si::Length::new::<bohr_radius>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Meter => Self::Length {
                quantity: si::Length::new::<meter>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Nanometer => Self::Length {
                quantity: si::Length::new::<nanometer>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Picometer => Self::Length {
                quantity: si::Length::new::<picometer>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Centimeter => Self::Length {
                quantity: si::Length::new::<centimeter>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Micrometer => Self::Length {
                quantity: si::Length::new::<micrometer>(value),
                display_unit: unit_symbol,
            },

            // === Mass ===
            UnitSymbol::AtomicMassUnit => Self::Mass {
                quantity: si::Mass::new::<dalton>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Kilogram => Self::Mass {
                quantity: si::Mass::new::<kilogram>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Gram => Self::Mass {
                quantity: si::Mass::new::<gram>(value),
                display_unit: unit_symbol,
            },

            // === Time ===
            UnitSymbol::Femtosecond => Self::Time {
                quantity: si::Time::new::<femtosecond>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Picosecond => Self::Time {
                quantity: si::Time::new::<picosecond>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Nanosecond => Self::Time {
                quantity: si::Time::new::<nanosecond>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Microsecond => Self::Time {
                quantity: si::Time::new::<microsecond>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Millisecond => Self::Time {
                quantity: si::Time::new::<millisecond>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Second => Self::Time {
                quantity: si::Time::new::<second>(value),
                display_unit: unit_symbol,
            },

            // === Temperature ===
            UnitSymbol::Kelvin => Self::Temperature {
                quantity: si::ThermodynamicTemperature::new::<kelvin>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Celsius => Self::Temperature {
                quantity: si::ThermodynamicTemperature::new::<degree_celsius>(value),
                display_unit: unit_symbol,
            },

            // === Pressure ===
            UnitSymbol::Gigapascal => Self::Pressure {
                quantity: si::Pressure::new::<gigapascal>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Megapascal => Self::Pressure {
                quantity: si::Pressure::new::<megapascal>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Kilopascal => Self::Pressure {
                quantity: si::Pressure::new::<kilopascal>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Pascal => Self::Pressure {
                quantity: si::Pressure::new::<pascal>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Bar => Self::Pressure {
                quantity: si::Pressure::new::<bar>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::Millibar => Self::Pressure {
                quantity: si::Pressure::new::<bar>(value * 1e-3),
                display_unit: unit_symbol,
            },
            UnitSymbol::Kilobar => Self::Pressure {
                quantity: si::Pressure::new::<bar>(value * 1e3),
                display_unit: unit_symbol,
            },
            UnitSymbol::Megabar => Self::Pressure {
                quantity: si::Pressure::new::<bar>(value * 1e6),
                display_unit: unit_symbol,
            },
            UnitSymbol::Atmosphere => Self::Pressure {
                quantity: si::Pressure::new::<atmosphere>(value),
                display_unit: unit_symbol,
            },

            // === Force ===
            UnitSymbol::Newton => Self::Force {
                quantity: si::Force::new::<newton>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::NanoNewton => Self::Force {
                quantity: si::Force::new::<nanonewton>(value),
                display_unit: unit_symbol,
            },
            UnitSymbol::ElectronvoltPerAngstrom => Self::Force {
                quantity: si::Force::new::<newton>(value * EV_PER_ANGSTROM_IN_NEWTON),
                display_unit: unit_symbol,
            },

            // === Charge ===
            UnitSymbol::ElementaryCharge => Self::Charge {
                quantity: si::ElectricCharge::new::<coulomb>(value * EV_IN_JOULES),
                display_unit: unit_symbol,
            },
            UnitSymbol::Coulomb => Self::Charge {
                quantity: si::ElectricCharge::new::<coulomb>(value),
                display_unit: unit_symbol,
            },

            // === Dimensionless ===
            UnitSymbol::Ratio => Self::Dimensionless { value },
        };
        quantity.check_finite()
    }

    /// Return quantity dimension.
    #[must_use]
    pub fn dimension(self) -> Dimension {
        match self {
            Self::Length { .. } => Dimension::Length,
            Self::Energy { .. } => Dimension::Energy,
            Self::Mass { .. } => Dimension::Mass,
            Self::Time { .. } => Dimension::Time,
            Self::Temperature { .. } => Dimension::Temperature,
            Self::Pressure { .. } => Dimension::Pressure,
            Self::Force { .. } => Dimension::Force,
            Self::Charge { .. } => Dimension::Charge,
            Self::Dimensionless { .. } => Dimension::Dimensionless,
        }
    }

    /// Return display unit.
    #[must_use]
    pub fn display_unit(self) -> UnitSymbol {
        match self {
            Self::Length { display_unit, .. }
            | Self::Energy { display_unit, .. }
            | Self::Mass { display_unit, .. }
            | Self::Time { display_unit, .. }
            | Self::Temperature { display_unit, .. }
            | Self::Pressure { display_unit, .. }
            | Self::Force { display_unit, .. }
            | Self::Charge { display_unit, .. } => display_unit,
            Self::Dimensionless { .. } => UnitSymbol::Ratio,
        }
    }

    /// Raw value in SI base units (J, m, kg, s, K, Pa, N, C).
    ///
    /// This is the internal `uom` representation — no rescaling, so it cannot
    /// overflow for a validly-constructed quantity. Useful for equality
    /// comparisons that must never error.
    #[must_use]
    pub fn si_value(self) -> f64 {
        match self {
            Self::Energy { quantity, .. } => quantity.get::<joule>(),
            Self::Length { quantity, .. } => quantity.get::<meter>(),
            Self::Mass { quantity, .. } => quantity.get::<kilogram>(),
            Self::Time { quantity, .. } => quantity.get::<second>(),
            Self::Temperature { quantity, .. } => quantity.get::<kelvin>(),
            Self::Pressure { quantity, .. } => quantity.get::<pascal>(),
            Self::Force { quantity, .. } => quantity.get::<newton>(),
            Self::Charge { quantity, .. } => quantity.get::<coulomb>(),
            Self::Dimensionless { value } => value,
        }
    }

    /// Convert to a specific unit.
    ///
    /// Returns the numeric value in the target unit. Fails if the target unit
    /// has a different [`Dimension`] than `self`.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::units::DynQuantity;
    ///
    /// let temp = DynQuantity::new(300.0, "K").unwrap();
    /// let celsius = temp.to_unit("celsius").unwrap();
    /// assert!((celsius - 26.85).abs() < 0.01);
    ///
    /// // Dimension mismatch → error
    /// assert!(temp.to_unit("eV").is_err());
    /// ```
    pub fn to_unit(self, unit_name: &str) -> Result<f64, UnitsError> {
        let unit_symbol = UnitSymbol::from_str(unit_name)?;
        self.to_unit_symbol(unit_symbol)
    }

    /// Convert to the quantity's current display unit.
    pub fn value(self) -> Result<f64, UnitsError> {
        self.to_unit_symbol(self.display_unit())
    }

    /// Convert to canonical default unit for this dimension.
    pub fn to_default(self) -> Result<f64, UnitsError> {
        self.to_unit_symbol(default_unit_for_dimension(self.dimension()))
    }

    /// Checked addition with same-dimension quantity.
    ///
    /// For `Temperature`, this performs arithmetic addition of Kelvin values.
    /// Physically, adding two absolute temperatures is not meaningful, but this
    /// operation is intentionally supported so that `try_sub` can work via
    /// negate-then-add, and for general user arithmetic (e.g. temperature offsets).
    pub fn try_add(self, rhs_quantity: Self) -> Result<Self, UnitsError> {
        if self.dimension() != rhs_quantity.dimension() {
            return Err(UnitsError::DimensionMismatch {
                lhs: self.dimension(),
                rhs: rhs_quantity.dimension(),
            });
        }
        let unit = self.display_unit();
        let result = match (self, rhs_quantity) {
            (Self::Length { quantity: l, .. }, Self::Length { quantity: r, .. }) => Self::Length {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Energy { quantity: l, .. }, Self::Energy { quantity: r, .. }) => Self::Energy {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Mass { quantity: l, .. }, Self::Mass { quantity: r, .. }) => Self::Mass {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Time { quantity: l, .. }, Self::Time { quantity: r, .. }) => Self::Time {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Temperature { quantity: l, .. }, Self::Temperature { quantity: r, .. }) => {
                // Arithmetic on temperatures always yields Kelvin display because
                // Celsius is offset-based: a sum/difference of absolute Celsius
                // values is only meaningful as a Kelvin delta.
                Self::Temperature {
                    quantity: si::ThermodynamicTemperature::new::<kelvin>(
                        l.get::<kelvin>() + r.get::<kelvin>(),
                    ),
                    display_unit: UnitSymbol::Kelvin,
                }
            }
            (Self::Pressure { quantity: l, .. }, Self::Pressure { quantity: r, .. }) => {
                Self::Pressure {
                    quantity: l + r,
                    display_unit: unit,
                }
            }
            (Self::Force { quantity: l, .. }, Self::Force { quantity: r, .. }) => Self::Force {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Charge { quantity: l, .. }, Self::Charge { quantity: r, .. }) => Self::Charge {
                quantity: l + r,
                display_unit: unit,
            },
            (Self::Dimensionless { value: l }, Self::Dimensionless { value: r }) => {
                Self::Dimensionless { value: l + r }
            }
            _ => unreachable!("dimension equality pre-checked in try_add"),
        };
        result.check_finite()
    }

    /// Checked subtraction with same-dimension quantity.
    pub fn try_sub(self, rhs_quantity: Self) -> Result<Self, UnitsError> {
        self.try_add(rhs_quantity.try_mul_scalar(-1.0)?)
    }

    /// Multiply by scalar.
    ///
    /// For `Temperature`, this multiplies the Kelvin value directly. Physically
    /// questionable for absolute temperatures, but required for `try_sub`
    /// (which negates via `try_mul_scalar(-1.0)`) and for constructing quantities
    /// like `300.0 * KELVIN`.
    pub fn try_mul_scalar(self, scalar: f64) -> Result<Self, UnitsError> {
        if !scalar.is_finite() {
            return Err(UnitsError::NonFiniteValue(scalar));
        }
        let result = match self {
            Self::Length {
                quantity: q,
                display_unit: u,
            } => Self::Length {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Energy {
                quantity: q,
                display_unit: u,
            } => Self::Energy {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Mass {
                quantity: q,
                display_unit: u,
            } => Self::Mass {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Time {
                quantity: q,
                display_unit: u,
            } => Self::Time {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Temperature {
                quantity: q,
                display_unit: u,
            } => Self::Temperature {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Pressure {
                quantity: q,
                display_unit: u,
            } => Self::Pressure {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Force {
                quantity: q,
                display_unit: u,
            } => Self::Force {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Charge {
                quantity: q,
                display_unit: u,
            } => Self::Charge {
                quantity: q * scalar,
                display_unit: u,
            },
            Self::Dimensionless { value } => Self::Dimensionless {
                value: value * scalar,
            },
        };
        result.check_finite()
    }

    /// Divide by scalar.
    pub fn try_div_scalar(self, scalar: f64) -> Result<Self, UnitsError> {
        if !scalar.is_finite() {
            return Err(UnitsError::NonFiniteValue(scalar));
        }
        if scalar == 0.0 {
            return Err(UnitsError::UnsupportedOperation("division by zero"));
        }
        let reciprocal = 1.0 / scalar;
        if !reciprocal.is_finite() {
            return Err(UnitsError::UnsupportedOperation(
                "division by near-zero value would overflow",
            ));
        }
        self.try_mul_scalar(reciprocal)
    }

    /// Convert to a specific unit symbol (pre-parsed version of [`Self::to_unit`]).
    pub fn to_unit_symbol(self, unit_symbol: UnitSymbol) -> Result<f64, UnitsError> {
        if self.dimension() != unit_symbol.dimension() {
            return Err(UnitsError::WrongDimension {
                expected: unit_symbol.dimension(),
                got: self.dimension(),
            });
        }
        let value = match self {
            Self::Energy { quantity, .. } => match unit_symbol {
                UnitSymbol::Electronvolt => quantity.get::<electronvolt>(),
                UnitSymbol::MilliElectronvolt => quantity.get::<electronvolt>() * 1e3,
                UnitSymbol::KiloElectronvolt => quantity.get::<electronvolt>() * 1e-3,
                UnitSymbol::Joule => quantity.get::<joule>(),
                UnitSymbol::Kilojoule => quantity.get::<kilojoule>(),
                UnitSymbol::Calorie => quantity.get::<calorie>(),
                UnitSymbol::Kilocalorie => quantity.get::<kilocalorie>(),
                UnitSymbol::KilojoulePerMol => quantity.get::<joule>() * AVOGADRO / 1e3,
                UnitSymbol::KilocaloriePerMol => quantity.get::<joule>() * AVOGADRO / 4184.0,
                UnitSymbol::Hartree => quantity.get::<hartree>(),
                UnitSymbol::Rydberg => quantity.get::<hartree>() * 2.0,
                UnitSymbol::InverseCentimeter => quantity.get::<joule>() / HC_IN_JOULE_CM,
                _ => unreachable!(),
            },
            Self::Length { quantity, .. } => match unit_symbol {
                UnitSymbol::Angstrom => quantity.get::<angstrom>(),
                UnitSymbol::Bohr => quantity.get::<bohr_radius>(),
                UnitSymbol::Meter => quantity.get::<meter>(),
                UnitSymbol::Nanometer => quantity.get::<nanometer>(),
                UnitSymbol::Picometer => quantity.get::<picometer>(),
                UnitSymbol::Centimeter => quantity.get::<centimeter>(),
                UnitSymbol::Micrometer => quantity.get::<micrometer>(),
                _ => unreachable!(),
            },
            Self::Mass { quantity, .. } => match unit_symbol {
                UnitSymbol::AtomicMassUnit => quantity.get::<dalton>(),
                UnitSymbol::Kilogram => quantity.get::<kilogram>(),
                UnitSymbol::Gram => quantity.get::<gram>(),
                _ => unreachable!(),
            },
            Self::Time { quantity, .. } => match unit_symbol {
                UnitSymbol::Femtosecond => quantity.get::<femtosecond>(),
                UnitSymbol::Picosecond => quantity.get::<picosecond>(),
                UnitSymbol::Nanosecond => quantity.get::<nanosecond>(),
                UnitSymbol::Microsecond => quantity.get::<microsecond>(),
                UnitSymbol::Millisecond => quantity.get::<millisecond>(),
                UnitSymbol::Second => quantity.get::<second>(),
                _ => unreachable!(),
            },
            Self::Temperature { quantity, .. } => match unit_symbol {
                UnitSymbol::Kelvin => quantity.get::<kelvin>(),
                UnitSymbol::Celsius => quantity.get::<degree_celsius>(),
                _ => unreachable!(),
            },
            Self::Pressure { quantity, .. } => match unit_symbol {
                UnitSymbol::Gigapascal => quantity.get::<gigapascal>(),
                UnitSymbol::Megapascal => quantity.get::<megapascal>(),
                UnitSymbol::Kilopascal => quantity.get::<kilopascal>(),
                UnitSymbol::Pascal => quantity.get::<pascal>(),
                UnitSymbol::Bar => quantity.get::<bar>(),
                UnitSymbol::Millibar => quantity.get::<bar>() * 1e3,
                UnitSymbol::Kilobar => quantity.get::<bar>() / 1e3,
                UnitSymbol::Megabar => quantity.get::<bar>() / 1e6,
                UnitSymbol::Atmosphere => quantity.get::<atmosphere>(),
                _ => unreachable!(),
            },
            Self::Force { quantity, .. } => match unit_symbol {
                UnitSymbol::Newton => quantity.get::<newton>(),
                UnitSymbol::NanoNewton => quantity.get::<nanonewton>(),
                UnitSymbol::ElectronvoltPerAngstrom => {
                    quantity.get::<newton>() / EV_PER_ANGSTROM_IN_NEWTON
                }
                _ => unreachable!(),
            },
            Self::Charge { quantity, .. } => match unit_symbol {
                UnitSymbol::ElementaryCharge => quantity.get::<coulomb>() / EV_IN_JOULES,
                UnitSymbol::Coulomb => quantity.get::<coulomb>(),
                _ => unreachable!(),
            },
            Self::Dimensionless { value } => match unit_symbol {
                UnitSymbol::Ratio => value,
                _ => unreachable!(),
            },
        };
        if !value.is_finite() {
            return Err(UnitsError::NonFiniteValue(value));
        }
        Ok(value)
    }
}

impl FromStr for UnitSymbol {
    type Err = UnitsError;

    fn from_str(raw_unit: &str) -> Result<Self, Self::Err> {
        let normalized = normalize_unit_name(raw_unit);
        let parsed = match normalized.as_str() {
            // Energy
            "ev" | "electronvolt" | "electronvolts" => Self::Electronvolt,
            "mev" | "millielectronvolt" | "millielectronvolts" => Self::MilliElectronvolt,
            "kev" | "kiloelectronvolt" | "kiloelectronvolts" => Self::KiloElectronvolt,
            "j" | "joule" | "joules" => Self::Joule,
            "kj" | "kilojoule" | "kilojoules" => Self::Kilojoule,
            "cal" | "calorie" | "calories" => Self::Calorie,
            "kcal" | "kilocalorie" | "kilocalories" => Self::Kilocalorie,
            "kj/mol" | "kjpermol" | "kjmol" | "kilojoule/mol" | "kilojoulepermol" => {
                Self::KilojoulePerMol
            }
            "kcal/mol" | "kcalpermol" | "kcalmol" | "kilocalorie/mol" | "kilocaloriepermol" => {
                Self::KilocaloriePerMol
            }
            "ha" | "hartree" | "hartrees" => Self::Hartree,
            "ry" | "rydberg" | "rydbergs" => Self::Rydberg,
            "cm1" | "cm^1" | "invcm" | "wavenumber" | "wavenumbers" | "kayser" => {
                Self::InverseCentimeter
            }

            // Length
            "a" | "ang" | "angstrom" | "angstroms" => Self::Angstrom,
            "bohr" | "bohrradius" | "a0" => Self::Bohr,
            "m" | "meter" | "meters" | "metre" | "metres" => Self::Meter,
            "nm" | "nanometer" | "nanometers" | "nanometre" | "nanometres" => Self::Nanometer,
            "pm" | "picometer" | "picometers" | "picometre" | "picometres" => Self::Picometer,
            "cm" | "centimeter" | "centimeters" | "centimetre" | "centimetres" => Self::Centimeter,
            "um" | "micrometer" | "micrometers" | "micrometre" | "micrometres" | "micron"
            | "microns" => Self::Micrometer,

            // Mass
            "amu" | "u" | "dalton" | "daltons" | "atomicmassunit" => Self::AtomicMassUnit,
            "kg" | "kilogram" | "kilograms" => Self::Kilogram,
            "g" | "gram" | "grams" => Self::Gram,

            // Time
            "fs" | "femtosecond" | "femtoseconds" => Self::Femtosecond,
            "ps" | "picosecond" | "picoseconds" => Self::Picosecond,
            "ns" | "nanosecond" | "nanoseconds" => Self::Nanosecond,
            "us" | "microsecond" | "microseconds" => Self::Microsecond,
            "ms" | "millisecond" | "milliseconds" => Self::Millisecond,
            "s" | "sec" | "second" | "seconds" => Self::Second,

            // Temperature
            "k" | "kelvin" => Self::Kelvin,
            "degc" | "celsius" | "degreec" | "degreecelsius" | "degreescelsius" => Self::Celsius,

            // Pressure
            "gpa" | "gigapascal" | "gigapascals" => Self::Gigapascal,
            "mpa" | "megapascal" | "megapascals" => Self::Megapascal,
            "kpa" | "kilopascal" | "kilopascals" => Self::Kilopascal,
            "pa" | "pascal" | "pascals" => Self::Pascal,
            "bar" => Self::Bar,
            "mbar" | "millibar" | "millibars" => Self::Millibar,
            "kbar" | "kilobar" | "kilobars" => Self::Kilobar,
            "megabar" | "megabars" => Self::Megabar,
            "atm" | "atmosphere" | "atmospheres" => Self::Atmosphere,

            // Force
            "n" | "newton" | "newtons" => Self::Newton,
            "nn" | "nanonewton" | "nanonewtons" => Self::NanoNewton,
            "ev/a" | "ev/ang" | "ev/angstrom" | "evperangstrom" => Self::ElectronvoltPerAngstrom,

            // Charge
            "e" | "elementarycharge" => Self::ElementaryCharge,
            "c" | "coulomb" | "coulombs" => Self::Coulomb,

            // Dimensionless
            "1" | "ratio" | "dimensionless" => Self::Ratio,

            _ => return Err(UnitsError::UnknownUnit(raw_unit.to_string())),
        };
        Ok(parsed)
    }
}

/// Handling mode for bare raw floats at language boundaries.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum UnitMode {
    /// Accept raw floats silently.
    Auto = 0,
    /// Accept raw floats and emit warning.
    Warn = 1,
    /// Reject raw floats.
    Strict = 2,
}

impl UnitMode {
    /// Stable lowercase mode name.
    #[must_use]
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Auto => "auto",
            Self::Warn => "warn",
            Self::Strict => "strict",
        }
    }
}

impl FromStr for UnitMode {
    type Err = UnitsError;

    fn from_str(raw_mode: &str) -> Result<Self, Self::Err> {
        let normalized_mode = raw_mode.trim().to_ascii_lowercase();
        match normalized_mode.as_str() {
            "auto" => Ok(Self::Auto),
            "warn" => Ok(Self::Warn),
            "strict" => Ok(Self::Strict),
            _ => Err(UnitsError::UnsupportedOperation(
                "unknown unit mode (expected auto, warn, or strict)",
            )),
        }
    }
}

static UNIT_MODE: AtomicU8 = AtomicU8::new(UnitMode::Auto as u8);

/// Set global unit mode.
pub fn set_unit_mode(mode: UnitMode) {
    UNIT_MODE.store(mode as u8, Ordering::SeqCst);
}

/// Read global unit mode.
#[must_use]
pub fn get_unit_mode() -> UnitMode {
    match UNIT_MODE.load(Ordering::SeqCst) {
        0 => UnitMode::Auto,
        1 => UnitMode::Warn,
        2 => UnitMode::Strict,
        other => unreachable!("UNIT_MODE contains invalid value {other}"),
    }
}

/// Default display unit for a physical dimension.
#[must_use]
pub fn default_unit_for_dimension(dimension: Dimension) -> UnitSymbol {
    match dimension {
        Dimension::Length => UnitSymbol::Angstrom,
        Dimension::Energy => UnitSymbol::Electronvolt,
        Dimension::Mass => UnitSymbol::AtomicMassUnit,
        Dimension::Time => UnitSymbol::Femtosecond,
        Dimension::Temperature => UnitSymbol::Kelvin,
        Dimension::Pressure => UnitSymbol::Gigapascal,
        Dimension::Force => UnitSymbol::ElectronvoltPerAngstrom,
        Dimension::Charge => UnitSymbol::ElementaryCharge,
        Dimension::Dimensionless => UnitSymbol::Ratio,
    }
}

fn normalize_unit_name(raw_unit: &str) -> String {
    raw_unit
        .trim()
        .replace('Å', "A")
        // Handle decomposed ring-above forms (e.g., "A◌̊").
        .replace(['\u{030A}', '_', '-', ' '], "")
        .to_ascii_lowercase()
}
