//! Physical property Python bindings.

use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pyfunction;
use rayon::prelude::*;
use std::time::Instant;

use super::helpers::{StructureJson, parse_struct};

#[derive(Clone, Copy)]
enum BenchmarkWorkload {
    Clone,
    Analysis,
}

impl BenchmarkWorkload {
    fn parse(workload: &str) -> PyResult<Self> {
        match workload {
            "clone" => Ok(Self::Clone),
            "analysis" => Ok(Self::Analysis),
            _ => Err(pyo3::exceptions::PyValueError::new_err(format!(
                "Invalid workload '{workload}'. Expected one of: 'clone', 'analysis'."
            ))),
        }
    }

    fn as_str(self) -> &'static str {
        match self {
            Self::Clone => "clone",
            Self::Analysis => "analysis",
        }
    }
}

/// Get the volume of a structure in Angstrom^3.
#[gen_stub_pyfunction(module = "ferrox._ferrox.properties")]
#[pyfunction]
fn get_volume(structure: StructureJson) -> PyResult<f64> {
    let struc = parse_struct(&structure)?;
    Ok(struc.volume())
}

/// Get the total mass of a structure in atomic mass units (amu).
#[gen_stub_pyfunction(module = "ferrox._ferrox.properties")]
#[pyfunction]
fn get_total_mass(structure: StructureJson) -> PyResult<f64> {
    let struc = parse_struct(&structure)?;
    Ok(struc.total_mass())
}

/// Get the density of a structure in g/cm^3.
///
/// Returns None for non-periodic or zero-volume structures.
#[gen_stub_pyfunction(module = "ferrox._ferrox.properties")]
#[pyfunction]
fn get_density(structure: StructureJson) -> PyResult<Option<f64>> {
    let struc = parse_struct(&structure)?;
    Ok(struc.density())
}

/// Get basic structure metadata (volume, density, lattice params).
#[gen_stub_pyfunction(module = "ferrox._ferrox.properties")]
#[pyfunction]
#[pyo3(name = "get_structure_metadata")]
fn properties_get_structure_metadata(
    py: Python<'_>,
    structure: StructureJson,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let comp = struc.composition();
    let lengths = struc.lattice.lengths();
    let angles = struc.lattice.angles();

    let dict = PyDict::new(py);
    dict.set_item("n_sites", struc.num_sites())?;
    dict.set_item("formula", comp.reduced_formula())?;
    dict.set_item("formula_anonymous", comp.anonymous_formula())?;
    dict.set_item("formula_hill", comp.hill_formula())?;
    dict.set_item("volume", struc.volume())?;
    dict.set_item("density", struc.density())?;
    dict.set_item("lattice_params", [lengths.x, lengths.y, lengths.z])?;
    dict.set_item("lattice_angles", [angles.x, angles.y, angles.z])?;
    dict.set_item("is_ordered", struc.is_ordered())?;
    dict.set_item(
        "elements",
        struc
            .species()
            .into_iter()
            .map(|s| s.element.symbol().to_string())
            .collect::<Vec<_>>(),
    )?;
    Ok(dict.into())
}

/// Benchmark-only API for Rust-side structure cloning from a parsed template.
///
/// Parse the input structure once, then clone and optionally analyze `n_structures`
/// copies in Rust. This avoids Python-loop overhead in benchmark hot paths.
///
/// Returns a dictionary with keys:
/// - n_structures, retain, workload, parallel, retained_count
/// - elapsed_seconds, throughput_structures_per_second
/// - scalar_checksum, site_checksum
#[gen_stub_pyfunction(module = "ferrox._ferrox.properties")]
#[pyfunction]
#[pyo3(signature = (
    structure,
    n_structures,
    retain = true,
    workload = "clone",
    parallel = true
))]
fn clone_template(
    py: Python<'_>,
    structure: StructureJson,
    n_structures: usize,
    retain: bool,
    workload: &str,
    parallel: bool,
) -> PyResult<Py<PyDict>> {
    if n_structures == 0 {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "clone_template requires n_structures >= 1.",
        ));
    }
    let workload_mode = BenchmarkWorkload::parse(workload)?;
    let template = parse_struct(&structure)?;

    let (elapsed_seconds, retained_count, scalar_checksum, site_checksum) = py.detach(|| {
        let start_time = Instant::now();
        let analyze = |struc: &crate::structure::Structure| -> (f64, usize) {
            match workload_mode {
                BenchmarkWorkload::Clone => (struc.volume(), struc.num_sites()),
                BenchmarkWorkload::Analysis => {
                    // Include common property pathways for a less synthetic benchmark.
                    let volume = struc.volume();
                    let mass = struc.total_mass();
                    let density = struc.density().unwrap_or(0.0);
                    let n_species = struc.species().len() as f64;
                    (
                        volume + mass + density + 1e-3 * n_species,
                        struc.num_sites(),
                    )
                }
            }
        };

        if retain {
            let structures = if parallel {
                (0..n_structures)
                    .into_par_iter()
                    .map(|_idx| template.clone())
                    .collect::<Vec<_>>()
            } else {
                (0..n_structures)
                    .map(|_idx| template.clone())
                    .collect::<Vec<_>>()
            };
            // Retained mode keeps all structures in memory; analysis runs after materialization.
            let (scalar_sum, sites_sum) =
                structures
                    .iter()
                    .fold((0.0_f64, 0_usize), |(scalar_acc, site_acc), struc| {
                        let (scalar_value, site_value) = analyze(struc);
                        (scalar_acc + scalar_value, site_acc + site_value)
                    });
            let retained_len = structures.len();
            let elapsed = start_time.elapsed().as_secs_f64();
            // Keep retained_len/materialized structures in-scope until timer is captured.
            (elapsed, retained_len, scalar_sum, sites_sum)
        } else {
            let (scalar_sum, sites_sum) = if parallel {
                (0..n_structures)
                    .into_par_iter()
                    .map(|_idx| {
                        let cloned = template.clone();
                        analyze(&cloned)
                    })
                    .reduce(
                        || (0.0_f64, 0_usize),
                        |(scalar_a, sites_a), (scalar_b, sites_b)| {
                            (scalar_a + scalar_b, sites_a + sites_b)
                        },
                    )
            } else {
                (0..n_structures).fold((0.0_f64, 0_usize), |(scalar_acc, site_acc), _idx| {
                    let cloned = template.clone();
                    let (scalar_value, site_value) = analyze(&cloned);
                    (scalar_acc + scalar_value, site_acc + site_value)
                })
            };
            let elapsed = start_time.elapsed().as_secs_f64();
            (elapsed, 0, scalar_sum, sites_sum)
        }
    });

    let throughput = (n_structures as f64) / elapsed_seconds.max(f64::EPSILON);
    let dict = PyDict::new(py);
    dict.set_item("n_structures", n_structures)?;
    dict.set_item("retain", retain)?;
    dict.set_item("workload", workload_mode.as_str())?;
    dict.set_item("parallel", parallel)?;
    dict.set_item("retained_count", retained_count)?;
    dict.set_item("elapsed_seconds", elapsed_seconds)?;
    dict.set_item("throughput_structures_per_second", throughput)?;
    dict.set_item("scalar_checksum", scalar_checksum)?;
    dict.set_item("site_checksum", site_checksum)?;
    Ok(dict.into())
}

/// Register properties functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(get_volume, module)?)?;
    module.add_function(wrap_pyfunction!(get_total_mass, module)?)?;
    module.add_function(wrap_pyfunction!(get_density, module)?)?;
    module.add_function(wrap_pyfunction!(clone_template, module)?)?;
    module.add_function(wrap_pyfunction!(properties_get_structure_metadata, module)?)?;
    Ok(())
}
