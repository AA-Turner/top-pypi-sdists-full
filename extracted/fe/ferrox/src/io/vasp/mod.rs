//! VASP file format support.
//!
//! This module provides parsers and analysis tools for VASP output files.
//! POSCAR/CONTCAR parsing lives in [`crate::io`]; this module covers volumetric
//! data formats that require domain-specific post-processing.
//!
//! - [`chgcar`] — CHGCAR parsing and Fourier coefficient extraction.

pub mod chgcar;
