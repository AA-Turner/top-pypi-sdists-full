//! Structure manipulation and matching functions.

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_stub_gen::derive::gen_stub_pyfunction;

use crate::analysis::structure_matcher::StructureMatcher;
use crate::python::helpers::SpacegroupInput;
use crate::structure::Structure;

use super::helpers::{
    StructureJson, parse_reduction_algo, parse_struct, parse_structure_pair, props_to_pydict,
    py_to_json_value, structure_to_pydict,
};

// === Structure Manipulation Functions ===

/// Create a supercell using a 3x3 transformation matrix.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn make_supercell(
    py: Python<'_>,
    structure: StructureJson,
    matrix: [[i32; 3]; 3],
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let supercell = struc
        .make_supercell(matrix)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &supercell)?.unbind())
}

/// Create a diagonal supercell.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn make_supercell_diag(
    py: Python<'_>,
    structure: StructureJson,
    scaling: [i32; 3],
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let supercell = struc.make_supercell_diag(scaling);
    Ok(structure_to_pydict(py, &supercell)?.unbind())
}

/// Get a reduced cell structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, algorithm = "niggli"))]
fn get_reduced_structure(
    py: Python<'_>,
    structure: StructureJson,
    algorithm: &str,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let algo = parse_reduction_algo(algorithm)?;
    let reduced = struc
        .get_reduced_structure(algo)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &reduced)?.unbind())
}

/// Copy a structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(name = "copy")]
fn copy_structure(py: Python<'_>, structure: StructureJson) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Wrap all sites to the unit cell.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn wrap_to_unit_cell(py: Python<'_>, structure: StructureJson) -> PyResult<Py<PyDict>> {
    let mut struc = parse_struct(&structure)?;
    struc.wrap_to_unit_cell();
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Interpolate between two structures.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (struct1, struct2, n_images, interpolate_lattices = false, use_pbc = true))]
fn interpolate(
    py: Python<'_>,
    struct1: StructureJson,
    struct2: StructureJson,
    n_images: usize,
    interpolate_lattices: bool,
    use_pbc: bool,
) -> PyResult<Vec<Py<PyDict>>> {
    if n_images == 0 {
        return Err(PyValueError::new_err(
            "n_images must be at least 1 to generate interpolated structures",
        ));
    }
    let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
    let images = s1
        .interpolate(&s2, n_images, interpolate_lattices, use_pbc)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    images
        .iter()
        .map(|img| Ok(structure_to_pydict(py, img)?.unbind()))
        .collect()
}

/// Get structure sorted by species.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, reverse = false))]
fn get_sorted_structure(
    py: Python<'_>,
    structure: StructureJson,
    reverse: bool,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let sorted = struc.get_sorted_structure(reverse);
    Ok(structure_to_pydict(py, &sorted)?.unbind())
}

/// Get structure metadata.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_structure_metadata(py: Python<'_>, structure: StructureJson) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let comp = struc.composition();
    let dict = PyDict::new(py);

    // Formula representations
    dict.set_item("formula", comp.formula())?;
    dict.set_item("formula_anonymous", comp.anonymous_formula())?;
    dict.set_item("formula_hill", comp.hill_formula())?;
    dict.set_item("chemical_system", comp.chemical_system())?;

    // Element info (use unique_elements, not species_strings, to get clean symbols
    // even for disordered/partial-occupancy sites)
    let mut elements: Vec<String> = struc
        .unique_elements()
        .iter()
        .map(|el| el.symbol().to_string())
        .collect();
    elements.sort();
    dict.set_item("elements", elements.clone())?;
    dict.set_item("n_elements", elements.len())?;
    dict.set_item("n_sites", struc.num_sites())?;
    dict.set_item("is_ordered", struc.is_ordered())?;

    // Physical properties
    dict.set_item("volume", struc.volume())?;
    dict.set_item("density", struc.density())?;
    dict.set_item("mass", comp.weight())?;

    Ok(dict.unbind())
}

/// Check if two structures match.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (struct1, struct2, anonymous = false))]
fn matches(struct1: StructureJson, struct2: StructureJson, anonymous: bool) -> PyResult<bool> {
    let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
    let matcher = StructureMatcher::new();
    Ok(if anonymous {
        matcher.fit_anonymous(&s1, &s2, None)
    } else {
        matcher.fit(&s1, &s2)
    })
}

// === Structure Transformation Functions ===

/// Substitute one species with another.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn substitute_species(
    py: Python<'_>,
    structure: StructureJson,
    old_species: &str,
    new_species: &str,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;

    let old_elem = crate::element::Element::from_symbol(old_species)
        .ok_or_else(|| PyValueError::new_err(format!("Unknown element: {old_species}")))?;
    let new_elem = crate::element::Element::from_symbol(new_species)
        .ok_or_else(|| PyValueError::new_err(format!("Unknown element: {new_species}")))?;

    let old_sp = crate::species::Species::neutral(old_elem);
    let new_sp = crate::species::Species::neutral(new_elem);

    let result = struc
        .substitute(old_sp, new_sp)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &result)?.unbind())
}

/// Remove all sites of specified species.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn remove_species(
    py: Python<'_>,
    structure: StructureJson,
    species_list: Vec<String>,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;

    // Validate all species symbols first
    let mut species = Vec::with_capacity(species_list.len());
    for sym in &species_list {
        match crate::element::Element::from_symbol(sym) {
            Some(elem) => species.push(crate::species::Species::neutral(elem)),
            None => {
                return Err(PyValueError::new_err(format!(
                    "Unknown species symbol: {sym}"
                )));
            }
        }
    }

    let result = struc
        .remove_species(&species)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &result)?.unbind())
}

/// Remove sites at specified indices.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn remove_sites(
    py: Python<'_>,
    structure: StructureJson,
    indices: Vec<usize>,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let result = struc
        .remove_sites(&indices)
        .map_err(|err| pyo3::exceptions::PyIndexError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &result)?.unbind())
}

/// Apply a deformation gradient to the structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn deform(
    py: Python<'_>,
    structure: StructureJson,
    gradient: [[f64; 3]; 3],
) -> PyResult<Py<PyDict>> {
    if gradient.iter().flatten().any(|v| !v.is_finite()) {
        return Err(PyValueError::new_err("gradient must be finite"));
    }
    let struc = parse_struct(&structure)?;
    let grad_matrix = nalgebra::Matrix3::from_row_slice(&[
        gradient[0][0],
        gradient[0][1],
        gradient[0][2],
        gradient[1][0],
        gradient[1][1],
        gradient[1][2],
        gradient[2][0],
        gradient[2][1],
        gradient[2][2],
    ]);
    let result = struc
        .deform(grad_matrix)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &result)?.unbind())
}

/// Compute Ewald energy for a structure with oxidation states.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, eta = None, real_cutoff = None, accuracy = None))]
fn ewald_energy(
    structure: StructureJson,
    eta: Option<f64>,
    real_cutoff: Option<f64>,
    accuracy: Option<f64>,
) -> PyResult<f64> {
    let struc = parse_struct(&structure)?;

    // Validate optional parameters
    if let Some(acc) = accuracy.filter(|&a| a <= 0.0 || !a.is_finite()) {
        return Err(PyValueError::new_err(format!(
            "accuracy must be positive and finite, got {acc}"
        )));
    }
    if let Some(rc) = real_cutoff.filter(|&r| r <= 0.0 || !r.is_finite()) {
        return Err(PyValueError::new_err(format!(
            "real_cutoff must be positive and finite, got {rc}"
        )));
    }

    let mut ewald = crate::algorithms::ewald::Ewald::new();
    if let Some(eta_val) = eta {
        if eta_val <= 0.0 || !eta_val.is_finite() {
            return Err(PyValueError::new_err("eta must be positive and finite"));
        }
        ewald = ewald.with_eta(eta_val);
    }
    if let Some(rc) = real_cutoff {
        ewald = ewald.with_real_cutoff(rc);
    }
    if let Some(acc) = accuracy {
        ewald = ewald.with_accuracy(acc);
    }

    ewald
        .energy(&struc)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Generate ordered structures from a disordered structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, max_structures = 100))]
fn order_disordered(
    py: Python<'_>,
    structure: StructureJson,
    max_structures: usize,
) -> PyResult<Vec<Py<PyDict>>> {
    let struc = parse_struct(&structure)?;
    let config = crate::transformations::OrderDisorderedConfig {
        max_structures: Some(max_structures),
        ..Default::default()
    };
    let results = struc
        .order_disordered(config)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    results
        .iter()
        .map(|s| Ok(structure_to_pydict(py, s)?.unbind()))
        .collect()
}

/// Enumerate derivative structures within a size range.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, min_size = 1, max_size = 4))]
fn enumerate_derivatives(
    py: Python<'_>,
    structure: StructureJson,
    min_size: usize,
    max_size: usize,
) -> PyResult<Vec<Py<PyDict>>> {
    if min_size > max_size {
        return Err(PyValueError::new_err("min_size must be <= max_size"));
    }
    let struc = parse_struct(&structure)?;
    let results = struc
        .enumerate_derivatives(min_size, max_size)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    results
        .iter()
        .map(|s| Ok(structure_to_pydict(py, s)?.unbind()))
        .collect()
}

/// Translate selected sites by a vector.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, indices, vector, fractional = true))]
fn translate_sites(
    py: Python<'_>,
    structure: StructureJson,
    indices: Vec<usize>,
    vector: [f64; 3],
    fractional: bool,
) -> PyResult<Py<PyDict>> {
    if vector.iter().any(|v| !v.is_finite()) {
        return Err(PyValueError::new_err("vector must be finite"));
    }
    let mut struc = parse_struct(&structure)?;
    let num_sites = struc.num_sites();
    if let Some(&idx) = indices.iter().find(|&&idx| idx >= num_sites) {
        return Err(pyo3::exceptions::PyIndexError::new_err(format!(
            "Site index {idx} out of bounds (num_sites={num_sites})"
        )));
    }
    struc.translate_sites(&indices, nalgebra::Vector3::from(vector), fractional);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Perturb all sites by random vectors.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, distance, min_distance = None, seed = None))]
fn perturb(
    py: Python<'_>,
    structure: StructureJson,
    distance: f64,
    min_distance: Option<f64>,
    seed: Option<u64>,
) -> PyResult<Py<PyDict>> {
    if !distance.is_finite() || distance < 0.0 {
        return Err(PyValueError::new_err(
            "distance must be finite and non-negative",
        ));
    }
    if let Some(min_dist) = min_distance {
        if !min_dist.is_finite() || min_dist < 0.0 {
            return Err(PyValueError::new_err(
                "min_distance must be finite and non-negative",
            ));
        }
        if min_dist > distance {
            return Err(PyValueError::new_err("min_distance must be <= distance"));
        }
    }
    let mut struc = parse_struct(&structure)?;
    struc.perturb(distance, min_distance, seed);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Get labels for all sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn site_labels(structure: StructureJson) -> PyResult<Vec<String>> {
    Ok(parse_struct(&structure)?.site_labels())
}

/// Get species strings for all sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn species_strings(structure: StructureJson) -> PyResult<Vec<String>> {
    Ok(parse_struct(&structure)?.species_strings())
}

/// Get structure with reduced lattice using custom parameters.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (structure, algorithm = "niggli", niggli_tol = 1e-5, lll_delta = 0.75))]
fn get_reduced_structure_with_params(
    py: Python<'_>,
    structure: StructureJson,
    algorithm: &str,
    niggli_tol: f64,
    lll_delta: f64,
) -> PyResult<Py<PyDict>> {
    if !niggli_tol.is_finite() || niggli_tol <= 0.0 {
        return Err(PyValueError::new_err(
            "niggli_tol must be finite and positive",
        ));
    }
    if !lll_delta.is_finite() || lll_delta <= 0.25 || lll_delta > 1.0 {
        return Err(PyValueError::new_err(
            "lll_delta must be finite and in range (0.25, 1.0]",
        ));
    }
    let struc = parse_struct(&structure)?;
    let algo = parse_reduction_algo(algorithm)?;
    let reduced = struc
        .get_reduced_structure_with_params(algo, niggli_tol, lll_delta)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &reduced)?.unbind())
}

/// Get structure sorted by electronegativity.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_sorted_by_electronegativity(
    py: Python<'_>,
    structure: StructureJson,
    reverse: Option<bool>,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let sorted = struc.get_sorted_by_electronegativity(reverse.unwrap_or(false));
    Ok(structure_to_pydict(py, &sorted)?.unbind())
}

/// Get distance between two sites with a specific periodic image.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_distance_with_image(
    structure: StructureJson,
    idx1: usize,
    idx2: usize,
    jimage: [i32; 3],
) -> PyResult<f64> {
    let struc = parse_struct(&structure)?;
    let num_sites = struc.num_sites();
    if idx1 >= num_sites || idx2 >= num_sites {
        return Err(pyo3::exceptions::PyIndexError::new_err(format!(
            "Site index out of bounds (num_sites={num_sites})"
        )));
    }
    Ok(struc.get_distance_with_image(idx1, idx2, jimage))
}

/// Get site properties for a specific site.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_site_properties(
    py: Python<'_>,
    structure: StructureJson,
    idx: usize,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    if idx >= struc.num_sites() {
        return Err(pyo3::exceptions::PyIndexError::new_err(format!(
            "Site index {idx} out of bounds for structure with {} sites",
            struc.num_sites()
        )));
    }
    Ok(props_to_pydict(py, struc.site_properties(idx))?.unbind())
}

/// Get all site properties for a structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_all_site_properties(py: Python<'_>, structure: StructureJson) -> PyResult<Py<PyList>> {
    let struc = parse_struct(&structure)?;
    let result: Vec<_> = (0..struc.num_sites())
        .map(|idx| props_to_pydict(py, struc.site_properties(idx)))
        .collect::<PyResult<_>>()?;
    Ok(PyList::new(py, result)?.unbind())
}

/// Set a site property.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn set_site_property(
    py: Python<'_>,
    structure: StructureJson,
    idx: usize,
    key: &str,
    value: Bound<'_, pyo3::PyAny>,
) -> PyResult<Py<PyDict>> {
    let mut struc = parse_struct(&structure)?;
    if idx >= struc.num_sites() {
        return Err(pyo3::exceptions::PyIndexError::new_err(format!(
            "Site index {idx} out of bounds for structure with {} sites",
            struc.num_sites()
        )));
    }
    let json_val = py_to_json_value(&value)?;
    struc.set_site_property(idx, key, json_val);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Get Cartesian coordinates for all sites in a structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn get_cart_coords(structure: StructureJson) -> PyResult<Vec<[f64; 3]>> {
    let struc = parse_struct(&structure)?;
    Ok(struc
        .cart_coords()
        .iter()
        .map(|c| [c.x, c.y, c.z])
        .collect())
}

/// Count the number of Wyckoff positions in an AFLOW protostructure label.
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
fn count_wyckoff_positions(protostructure_label: &str) -> PyResult<usize> {
    crate::analysis::prototype::count_wyckoff_positions(protostructure_label)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Create a structure from a space group, lattice, and asymmetric unit.
///
/// Generates all symmetry-equivalent sites from the space group operations.
///
/// Args:
///     sg: Space group as ITA number (1-230) or Hermann-Mauguin symbol (e.g. "Fm-3m")
///     lattice: 3x3 lattice matrix (rows = lattice vectors) or [[a, b, c, alpha, beta, gamma]]
///     species: Element symbols for each symmetrically distinct site (e.g. ["Na", "Cl"])
///     coords: Fractional coordinates of each distinct site (Nx3 list)
///     tol: Tolerance for deduplicating equivalent sites (default: 1e-5)
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (sg, lattice, species, coords, tol = None))]
fn from_spacegroup(
    py: Python<'_>,
    sg: SpacegroupInput,
    lattice: Vec<Vec<f64>>,
    species: Vec<String>,
    coords: Vec<[f64; 3]>,
    tol: Option<f64>,
) -> PyResult<Py<PyDict>> {
    let lat = parse_lattice_input(&lattice)?;
    let site_occs = crate::species::SiteOccupancy::parse_symbols(&species)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let frac_coords: Vec<nalgebra::Vector3<f64>> = coords
        .iter()
        .map(|c| nalgebra::Vector3::new(c[0], c[1], c[2]))
        .collect();

    let struc = Structure::from_spacegroup(&sg.0, lat, site_occs, frac_coords, tol)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Create a structure from a named prototype (e.g. "fcc", "rocksalt", "perovskite").
///
/// Supported prototypes: sc, fcc, bcc, hcp, diamond, rocksalt, perovskite,
/// cscl, fluorite, antifluorite, zincblende, wurtzite.
///
/// Args:
///     prototype: Name of the prototype structure
///     species: Element symbols for each symmetrically distinct site
///     a: Lattice parameter a (required for all prototypes)
///     b: Lattice parameter b (optional)
///     c: Lattice parameter c (required for hcp, wurtzite)
#[gen_stub_pyfunction(module = "ferrox._ferrox.structure")]
#[pyfunction]
#[pyo3(signature = (prototype, species, a, b = None, c = None))]
fn from_prototype(
    py: Python<'_>,
    prototype: &str,
    species: Vec<String>,
    a: f64,
    b: Option<f64>,
    c: Option<f64>,
) -> PyResult<Py<PyDict>> {
    let site_occs = crate::species::SiteOccupancy::parse_symbols(&species)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let struc = Structure::from_prototype(prototype, site_occs, a, b, c)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Parse lattice input: either 3x3 matrix or [[a, b, c, alpha, beta, gamma]].
pub fn parse_lattice_input(lattice: &[Vec<f64>]) -> PyResult<crate::lattice::Lattice> {
    if lattice.len() == 3 && lattice.iter().all(|row| row.len() == 3) {
        let matrix = nalgebra::Matrix3::new(
            lattice[0][0],
            lattice[0][1],
            lattice[0][2],
            lattice[1][0],
            lattice[1][1],
            lattice[1][2],
            lattice[2][0],
            lattice[2][1],
            lattice[2][2],
        );
        Ok(crate::lattice::Lattice::new(matrix))
    } else if lattice.len() == 1 && lattice[0].len() == 6 {
        let p = &lattice[0];
        Ok(crate::lattice::Lattice::from_parameters(
            p[0], p[1], p[2], p[3], p[4], p[5],
        ))
    } else {
        Err(PyValueError::new_err(
            "lattice must be a 3x3 matrix (rows = lattice vectors) or a single row \
             [a, b, c, alpha, beta, gamma]",
        ))
    }
}

/// Register structure functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_class::<super::classes::PyStructureMatcher>()?;
    module.add_class::<super::classes::PyStructure>()?;
    module.add_function(wrap_pyfunction!(make_supercell, module)?)?;
    module.add_function(wrap_pyfunction!(make_supercell_diag, module)?)?;
    module.add_function(wrap_pyfunction!(get_reduced_structure, module)?)?;
    module.add_function(wrap_pyfunction!(get_reduced_structure_with_params, module)?)?;
    module.add_function(wrap_pyfunction!(copy_structure, module)?)?;
    module.add_function(wrap_pyfunction!(wrap_to_unit_cell, module)?)?;
    module.add_function(wrap_pyfunction!(interpolate, module)?)?;
    module.add_function(wrap_pyfunction!(get_sorted_structure, module)?)?;
    module.add_function(wrap_pyfunction!(get_sorted_by_electronegativity, module)?)?;
    module.add_function(wrap_pyfunction!(get_structure_metadata, module)?)?;
    module.add_function(wrap_pyfunction!(matches, module)?)?;
    module.add_function(wrap_pyfunction!(substitute_species, module)?)?;
    module.add_function(wrap_pyfunction!(remove_species, module)?)?;
    module.add_function(wrap_pyfunction!(remove_sites, module)?)?;
    module.add_function(wrap_pyfunction!(deform, module)?)?;
    module.add_function(wrap_pyfunction!(ewald_energy, module)?)?;
    module.add_function(wrap_pyfunction!(order_disordered, module)?)?;
    module.add_function(wrap_pyfunction!(enumerate_derivatives, module)?)?;
    module.add_function(wrap_pyfunction!(translate_sites, module)?)?;
    module.add_function(wrap_pyfunction!(perturb, module)?)?;
    module.add_function(wrap_pyfunction!(site_labels, module)?)?;
    module.add_function(wrap_pyfunction!(species_strings, module)?)?;
    module.add_function(wrap_pyfunction!(get_distance_with_image, module)?)?;
    module.add_function(wrap_pyfunction!(get_site_properties, module)?)?;
    module.add_function(wrap_pyfunction!(get_all_site_properties, module)?)?;
    module.add_function(wrap_pyfunction!(set_site_property, module)?)?;
    module.add_function(wrap_pyfunction!(get_cart_coords, module)?)?;
    module.add_function(wrap_pyfunction!(count_wyckoff_positions, module)?)?;
    module.add_function(wrap_pyfunction!(from_spacegroup, module)?)?;
    module.add_function(wrap_pyfunction!(from_prototype, module)?)?;
    Ok(())
}
