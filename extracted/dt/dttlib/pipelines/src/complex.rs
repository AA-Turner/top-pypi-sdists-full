//! complex numbers defined here, because they must be made PipeData

use num_complex::{Complex32, Complex64};

/// # Complex type aliases
/// c128 is 128 bits long, represented by two 64-bit floats
/// c64 is 64 bits long, represented by two 32-bit floats
/// These names, c128 and c64, are used to match the names Complex128 and Complex64 used in
/// DAQ data type enumerations
#[allow(non_camel_case_types)]
pub type c128 = Complex64;
#[allow(non_camel_case_types)]
pub type c64 = Complex32;
