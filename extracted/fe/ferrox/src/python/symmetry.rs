//! Symmetry and space group functions.

use nalgebra::{Matrix3, Vector3};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pyfunction;

use crate::structure::{
    SymmOp, geometric_crystal_class_from_hall, laue_group_from_point_group,
    point_group_is_centrosymmetric, point_group_is_chiral, point_group_is_polar,
    point_group_symbol, spacegroup_to_crystal_system, spacegroup_type_from_number,
};
use moyo::data::GeometricCrystalClass;

use super::helpers::{StructureJson, mat3_to_array, parse_struct, structure_to_pydict};

/// Parse structure and look up the geometric crystal class (shared by point group functions).
fn parse_gcc(structure: &StructureJson, symprec: f64) -> PyResult<GeometricCrystalClass> {
    let struc = parse_struct(structure)?;
    struc
        .get_geometric_crystal_class(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the space group number.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_spacegroup_number(structure: StructureJson, symprec: f64) -> PyResult<i32> {
    let struc = parse_struct(&structure)?;
    struc
        .get_spacegroup_number(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the space group symbol.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_spacegroup_symbol(structure: StructureJson, symprec: f64) -> PyResult<String> {
    let struc = parse_struct(&structure)?;
    struc
        .get_spacegroup_symbol(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the Hall number.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_hall_number(structure: StructureJson, symprec: f64) -> PyResult<i32> {
    let struc = parse_struct(&structure)?;
    struc
        .get_hall_number(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the crystal system.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_crystal_system(structure: StructureJson, symprec: f64) -> PyResult<String> {
    let struc = parse_struct(&structure)?;
    let spg = struc
        .get_spacegroup_number(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(spacegroup_to_crystal_system(spg).to_string())
}

/// Get the Pearson symbol.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_pearson_symbol(structure: StructureJson, symprec: f64) -> PyResult<String> {
    let struc = parse_struct(&structure)?;
    struc
        .get_pearson_symbol(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the point group (geometric crystal class) Hermann-Mauguin symbol.
///
/// Uses the ITA primary symbol convention (e.g. "-42m" for D2d, "-6m2" for D3h).
/// pymatgen/spglib may use the alternative ITA setting ("-4m2", "-62m").
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_point_group(structure: StructureJson, symprec: f64) -> PyResult<&'static str> {
    Ok(point_group_symbol(parse_gcc(&structure, symprec)?))
}

/// Get the Laue group symbol.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_laue_group(structure: StructureJson, symprec: f64) -> PyResult<&'static str> {
    Ok(laue_group_from_point_group(parse_gcc(&structure, symprec)?))
}

/// Whether the structure's point group is centrosymmetric (contains inversion).
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn is_centrosymmetric(structure: StructureJson, symprec: f64) -> PyResult<bool> {
    Ok(point_group_is_centrosymmetric(parse_gcc(
        &structure, symprec,
    )?))
}

/// Whether the structure's point group is polar (has a unique polar direction).
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn is_polar(structure: StructureJson, symprec: f64) -> PyResult<bool> {
    Ok(point_group_is_polar(parse_gcc(&structure, symprec)?))
}

/// Whether the structure's point group is chiral (contains only proper rotations).
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn is_chiral(structure: StructureJson, symprec: f64) -> PyResult<bool> {
    Ok(point_group_is_chiral(parse_gcc(&structure, symprec)?))
}

/// Get Wyckoff letters for all sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_wyckoff_letters(structure: StructureJson, symprec: f64) -> PyResult<Vec<String>> {
    let struc = parse_struct(&structure)?;
    let letters = struc
        .get_wyckoff_letters(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(letters.into_iter().map(|c| c.to_string()).collect())
}

/// Get symmetry operations.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_symmetry_operations(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
) -> PyResult<Vec<Py<PyDict>>> {
    let struc = parse_struct(&structure)?;
    let ops = struc
        .get_symmetry_operations(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    ops.iter()
        .map(|(rot, trans)| {
            let dict = PyDict::new(py);
            dict.set_item("rotation", rot.to_vec())?;
            dict.set_item("translation", trans.to_vec())?;
            Ok(dict.unbind())
        })
        .collect()
}

/// Get equivalent sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_equivalent_sites(structure: StructureJson, symprec: f64) -> PyResult<Vec<usize>> {
    let struc = parse_struct(&structure)?;
    struc
        .get_equivalent_sites(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the primitive cell.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_primitive(py: Python<'_>, structure: StructureJson, symprec: f64) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let primitive = struc
        .get_primitive(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &primitive)?.unbind())
}

/// Get the conventional cell.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_conventional(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let conventional = struc
        .get_conventional_structure(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &conventional)?.unbind())
}

/// Get the ITA-standardized structure with transformation matrix.
///
/// Returns a dict with "structure" (the standardized cell) and
/// "transformation" (3x3 matrix from input to standardized cell).
/// Set primitive=True for the primitive standardized cell.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01, primitive = false))]
fn get_standardized(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
    primitive: bool,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let (std_struc, transformation) = struc
        .get_standardized_structure(symprec, primitive)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let dict = PyDict::new(py);
    dict.set_item("structure", structure_to_pydict(py, &std_struc)?)?;
    dict.set_item("transformation", mat3_to_array(&transformation))?;
    Ok(dict.unbind())
}

/// Symmetrize a structure by averaging equivalent atomic positions.
///
/// Enforces exact space group symmetry on a distorted structure by
/// averaging coordinates of symmetry-equivalent sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_symmetrized(py: Python<'_>, structure: StructureJson, symprec: f64) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let symmetrized = struc
        .get_symmetrized_structure(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    Ok(structure_to_pydict(py, &symmetrized)?.unbind())
}

/// Get all site indices symmetry-equivalent to the given site.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, site_idx, symprec = 0.01))]
fn get_symmetry_equivalent_sites(
    structure: StructureJson,
    site_idx: usize,
    symprec: f64,
) -> PyResult<Vec<usize>> {
    let struc = parse_struct(&structure)?;
    struc
        .get_symmetry_equivalent_sites(site_idx, symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Look up space group type information from an ITA number (1-230).
///
/// Returns a dict with number, hm_short, hm_full, hall_symbol, crystal_system,
/// point_group, laue_group, is_centrosymmetric, is_polar, is_chiral.
/// No structure input needed -- pure database lookup.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
fn get_spacegroup_type(py: Python<'_>, number: i32) -> PyResult<Py<PyDict>> {
    let info = spacegroup_type_from_number(number)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let dict = PyDict::new(py);
    dict.set_item("number", info.number)?;
    for (key, value) in [
        ("hm_short", info.hm_short),
        ("hm_full", info.hm_full),
        ("hall_symbol", info.hall_symbol),
        ("crystal_system", info.crystal_system),
        ("point_group", info.point_group),
        ("laue_group", info.laue_group),
        (
            "arithmetic_crystal_class_symbol",
            info.arithmetic_crystal_class_symbol,
        ),
        ("bravais_class", info.bravais_class),
        ("lattice_system", info.lattice_system),
        ("crystal_family", info.crystal_family),
    ] {
        dict.set_item(key, value)?;
    }
    dict.set_item(
        "arithmetic_crystal_class_number",
        info.arithmetic_crystal_class_number,
    )?;
    dict.set_item("is_centrosymmetric", info.is_centrosymmetric)?;
    dict.set_item("is_polar", info.is_polar)?;
    dict.set_item("is_chiral", info.is_chiral)?;
    dict.set_item("is_piezoelectric_allowed", info.is_piezoelectric_allowed)?;
    dict.set_item("is_shg_allowed", info.is_shg_allowed)?;
    Ok(dict.unbind())
}

/// Get the magnetic symmetry dataset for a structure with magnetic moments.
///
/// Extracts magmom from site properties and determines the magnetic space group.
/// Supports collinear (scalar magmom per site) and non-collinear (3-vector) moments.
///
/// Returns a dict with uni_number (UNI magnetic space group number),
/// num_magnetic_operations, orbits, and the actual symprec/mag_symprec used.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01, mag_symprec = None, is_axial = true))]
fn get_magnetic_symmetry_dataset(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
    mag_symprec: Option<f64>,
    is_axial: bool,
) -> PyResult<Py<PyDict>> {
    use moyo::MoyoMagneticDataset;
    use moyo::base::{Collinear, MagneticCell, NonCollinear, RotationMagneticMomentAction};

    let struc = parse_struct(&structure)?;
    let moyo_cell = struc.to_moyo_cell();
    let action = if is_axial {
        RotationMagneticMomentAction::Axial
    } else {
        RotationMagneticMomentAction::Polar
    };

    // Extract magmom from site properties
    let magmoms_raw: Vec<Option<&serde_json::Value>> = struc
        .site_occupancies
        .iter()
        .map(|occ| occ.properties.get("magmom"))
        .collect();

    // Detect collinear vs non-collinear by checking the first non-None magmom
    let first_magmom = magmoms_raw.iter().find_map(|m| *m).ok_or_else(|| {
        PyValueError::new_err(
            "No 'magmom' found in site properties. Add magmom to each site's properties dict.",
        )
    })?;

    let is_collinear = first_magmom.is_number();

    // Validate all magmom values are consistent (all scalar or all 3-vector)
    for (idx, m) in magmoms_raw.iter().enumerate() {
        if let Some(val) = m {
            let site_is_scalar = val.is_number();
            if site_is_scalar != is_collinear {
                let expected = if is_collinear { "scalar" } else { "3-vector" };
                let got = if site_is_scalar { "scalar" } else { "array" };
                return Err(PyValueError::new_err(format!(
                    "Site {idx}: mixed magmom types — expected {expected} (matching site 0) but got {got}. \
                     All sites must use the same format (all scalars for collinear, all 3-vectors for non-collinear)."
                )));
            }
        }
    }

    // Serialize shared fields from a MoyoMagneticDataset into the result dict
    macro_rules! serialize_mag_dataset {
        ($dict:expr, $dataset:expr, $is_col:expr) => {{
            $dict.set_item("uni_number", $dataset.uni_number)?;
            $dict.set_item(
                "num_magnetic_operations",
                $dataset.magnetic_operations.len(),
            )?;
            $dict.set_item("orbits", &$dataset.orbits)?;
            $dict.set_item("symprec", $dataset.symprec)?;
            $dict.set_item("mag_symprec", $dataset.mag_symprec)?;
            $dict.set_item("is_collinear", $is_col)?;
            let ops: Vec<_> = $dataset
                .magnetic_operations
                .iter()
                .map(|op| {
                    let rot: [[i32; 3]; 3] = std::array::from_fn(|row| {
                        std::array::from_fn(|col| op.operation.rotation[(row, col)])
                    });
                    let t = &op.operation.translation;
                    (rot, [t.x, t.y, t.z], op.time_reversal)
                })
                .collect();
            $dict.set_item("magnetic_operations", ops)?;
        }};
    }

    let moyo_err = |e| PyValueError::new_err(format!("Magnetic symmetry search failed: {e:?}"));
    let dict = PyDict::new(py);

    if is_collinear {
        let moments: Vec<Collinear> = magmoms_raw
            .iter()
            .enumerate()
            .map(|(idx, m)| match m.and_then(|v| v.as_f64()) {
                Some(val) if val.is_finite() => Ok(Collinear(val)),
                Some(val) => Err(PyValueError::new_err(format!(
                    "Site {idx}: magmom must be finite, got {val}"
                ))),
                None => Ok(Collinear(0.0)),
            })
            .collect::<PyResult<_>>()?;

        let mag_cell = MagneticCell::from_cell(moyo_cell, moments);
        let dataset = MoyoMagneticDataset::new(
            &mag_cell,
            symprec,
            moyo::base::AngleTolerance::Default,
            mag_symprec,
            action,
            false,
        )
        .map_err(moyo_err)?;
        serialize_mag_dataset!(dict, dataset, true);
        let std_moments: Vec<f64> = dataset
            .std_mag_cell
            .magnetic_moments
            .iter()
            .map(|m| m.0)
            .collect();
        dict.set_item("std_magmoms", std_moments)?;
    } else {
        let moments: Vec<NonCollinear> = magmoms_raw
            .iter()
            .enumerate()
            .map(|(idx, m)| {
                let Some(val) = m else {
                    return Ok(NonCollinear(Vector3::new(0.0, 0.0, 0.0)));
                };
                let arr = val.as_array().ok_or_else(|| {
                    PyValueError::new_err(format!(
                        "Site {idx}: expected 3-vector magmom, got {val:?}"
                    ))
                })?;
                if arr.len() != 3 {
                    return Err(PyValueError::new_err(format!(
                        "Site {idx}: magmom must be 3-vector, got length {}",
                        arr.len()
                    )));
                }
                let parse_component = |comp_idx: usize| {
                    arr[comp_idx].as_f64().ok_or_else(|| {
                        PyValueError::new_err(format!(
                            "Site {idx}: magmom component {comp_idx} must be numeric"
                        ))
                    })
                };
                Ok(NonCollinear(Vector3::new(
                    parse_component(0)?,
                    parse_component(1)?,
                    parse_component(2)?,
                )))
            })
            .collect::<PyResult<_>>()?;

        let mag_cell = MagneticCell::from_cell(moyo_cell, moments);
        let dataset = MoyoMagneticDataset::new(
            &mag_cell,
            symprec,
            moyo::base::AngleTolerance::Default,
            mag_symprec,
            action,
            false,
        )
        .map_err(moyo_err)?;
        serialize_mag_dataset!(dict, dataset, false);
        let std_moments: Vec<[f64; 3]> = dataset
            .std_mag_cell
            .magnetic_moments
            .iter()
            .map(|m| [m.0.x, m.0.y, m.0.z])
            .collect();
        dict.set_item("std_magmoms", std_moments)?;
    }

    Ok(dict.unbind())
}

/// Get the full symmetry dataset.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_symmetry_dataset(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let dataset = struc
        .get_symmetry_dataset(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;

    let dict = PyDict::new(py);
    dict.set_item("spacegroup_number", dataset.number)?;
    dict.set_item("spacegroup_symbol", &dataset.hm_symbol)?;
    dict.set_item("hall_number", dataset.hall_number)?;
    dict.set_item("pearson_symbol", &dataset.pearson_symbol)?;
    dict.set_item("num_operations", dataset.operations.len())?;
    dict.set_item(
        "crystal_system",
        spacegroup_to_crystal_system(dataset.number),
    )?;

    // Point group and Laue group from Hall number classification
    let gcc = geometric_crystal_class_from_hall(dataset.hall_number)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    dict.set_item("point_group", point_group_symbol(gcc))?;
    dict.set_item("laue_group", laue_group_from_point_group(gcc))?;
    dict.set_item("is_centrosymmetric", point_group_is_centrosymmetric(gcc))?;
    dict.set_item("is_polar", point_group_is_polar(gcc))?;
    dict.set_item("is_chiral", point_group_is_chiral(gcc))?;

    // Use fields directly from the already-computed dataset (avoids redundant symmetry runs)
    let wyckoff_strs: Vec<String> = dataset.wyckoffs.iter().map(|c| c.to_string()).collect();
    dict.set_item("wyckoff_letters", wyckoff_strs)?;
    dict.set_item("equivalent_sites", &dataset.orbits)?;
    dict.set_item("site_symmetry_symbols", &dataset.site_symmetry_symbols)?;

    let ops: Vec<_> = dataset
        .operations
        .iter()
        .map(|op| {
            let rot: [[i32; 3]; 3] =
                std::array::from_fn(|row| std::array::from_fn(|col| op.rotation[(row, col)]));
            let trans = [op.translation.x, op.translation.y, op.translation.z];
            (rot, trans)
        })
        .collect();
    dict.set_item("symmetry_operations", ops)?;

    // Transformation matrices (input cell -> standardized cells)
    dict.set_item("std_linear", mat3_to_array(&dataset.std_linear))?;
    let shift = &dataset.std_origin_shift;
    dict.set_item("std_origin_shift", [shift.x, shift.y, shift.z])?;
    dict.set_item(
        "std_rotation_matrix",
        mat3_to_array(&dataset.std_rotation_matrix),
    )?;
    dict.set_item("mapping_std_prim", &dataset.mapping_std_prim)?;

    Ok(dict.unbind())
}

/// Apply a symmetry operation (rotation + translation) to a structure.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, rotation, translation, fractional = true))]
fn apply_operation(
    py: Python<'_>,
    structure: StructureJson,
    rotation: [[f64; 3]; 3],
    translation: [f64; 3],
    fractional: bool,
) -> PyResult<Py<PyDict>> {
    let mut struc = parse_struct(&structure)?;
    let rot = Matrix3::from_row_slice(&rotation.concat());
    let op = SymmOp::new(rot, Vector3::from(translation));
    struc.apply_operation(&op, fractional);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Apply inversion through the origin.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, fractional = true))]
fn apply_inversion(
    py: Python<'_>,
    structure: StructureJson,
    fractional: bool,
) -> PyResult<Py<PyDict>> {
    let mut struc = parse_struct(&structure)?;
    struc.apply_operation(&SymmOp::inversion(), fractional);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Apply a translation to all sites.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, translation, fractional = true))]
fn apply_translation(
    py: Python<'_>,
    structure: StructureJson,
    translation: [f64; 3],
    fractional: bool,
) -> PyResult<Py<PyDict>> {
    let mut struc = parse_struct(&structure)?;
    struc.apply_operation(&SymmOp::translation(Vector3::from(translation)), fractional);
    Ok(structure_to_pydict(py, &struc)?.unbind())
}

/// Parse structure and look up SpacegroupTypeInfo (shared by classification functions).
fn parse_spg_type_info(
    structure: &StructureJson,
    symprec: f64,
) -> PyResult<crate::structure::SpacegroupTypeInfo> {
    let struc = parse_struct(structure)?;
    let spg = struc
        .get_spacegroup_number(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    spacegroup_type_from_number(spg).map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the Bravais class of a structure (e.g. "cF", "tI", "oP").
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_bravais_class(structure: StructureJson, symprec: f64) -> PyResult<String> {
    Ok(parse_spg_type_info(&structure, symprec)?
        .bravais_class
        .to_string())
}

/// Get the lattice system of a structure (e.g. "cubic", "hexagonal").
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_lattice_system(structure: StructureJson, symprec: f64) -> PyResult<String> {
    Ok(parse_spg_type_info(&structure, symprec)?
        .lattice_system
        .to_string())
}

/// Get the crystal family of a structure (e.g. "cubic", "hexagonal").
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_crystal_family(structure: StructureJson, symprec: f64) -> PyResult<String> {
    Ok(parse_spg_type_info(&structure, symprec)?
        .crystal_family
        .to_string())
}

/// Whether piezoelectricity is symmetry-allowed.
/// Non-centrosymmetric except point group 432 (O), whose high symmetry
/// forces all piezoelectric tensor coefficients to zero.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn is_piezoelectric_allowed(structure: StructureJson, symprec: f64) -> PyResult<bool> {
    Ok(parse_spg_type_info(&structure, symprec)?.is_piezoelectric_allowed)
}

/// Whether the structure's point group allows second harmonic generation (non-centrosymmetric).
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn is_shg_allowed(structure: StructureJson, symprec: f64) -> PyResult<bool> {
    Ok(parse_spg_type_info(&structure, symprec)?.is_shg_allowed)
}

/// Get the number of symmetry operations in the structure's space group.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_num_symmetry_operations(structure: StructureJson, symprec: f64) -> PyResult<usize> {
    let struc = parse_struct(&structure)?;
    struc
        .num_symmetry_operations(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get the number of symmetry-inequivalent sites (Wyckoff orbits).
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_num_unique_sites(structure: StructureJson, symprec: f64) -> PyResult<usize> {
    let struc = parse_struct(&structure)?;
    struc
        .num_unique_sites(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))
}

/// Get a histogram of Wyckoff letters mapping each letter to its count.
#[gen_stub_pyfunction(module = "ferrox._ferrox.symmetry")]
#[pyfunction]
#[pyo3(signature = (structure, symprec = 0.01))]
fn get_wyckoff_histogram(
    py: Python<'_>,
    structure: StructureJson,
    symprec: f64,
) -> PyResult<Py<PyDict>> {
    let struc = parse_struct(&structure)?;
    let hist = struc
        .wyckoff_histogram(symprec)
        .map_err(|err| PyValueError::new_err(err.to_string()))?;
    let dict = PyDict::new(py);
    for (letter, count) in &hist {
        dict.set_item(letter.to_string(), count)?;
    }
    Ok(dict.unbind())
}

/// Register symmetry functions and classes on the given module.
pub fn register(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(get_spacegroup_number, module)?)?;
    module.add_function(wrap_pyfunction!(get_spacegroup_symbol, module)?)?;
    module.add_function(wrap_pyfunction!(get_hall_number, module)?)?;
    module.add_function(wrap_pyfunction!(get_crystal_system, module)?)?;
    module.add_function(wrap_pyfunction!(get_pearson_symbol, module)?)?;
    module.add_function(wrap_pyfunction!(get_point_group, module)?)?;
    module.add_function(wrap_pyfunction!(get_laue_group, module)?)?;
    module.add_function(wrap_pyfunction!(is_centrosymmetric, module)?)?;
    module.add_function(wrap_pyfunction!(is_polar, module)?)?;
    module.add_function(wrap_pyfunction!(is_chiral, module)?)?;
    module.add_function(wrap_pyfunction!(get_wyckoff_letters, module)?)?;
    module.add_function(wrap_pyfunction!(get_symmetry_operations, module)?)?;
    module.add_function(wrap_pyfunction!(get_equivalent_sites, module)?)?;
    module.add_function(wrap_pyfunction!(get_primitive, module)?)?;
    module.add_function(wrap_pyfunction!(get_conventional, module)?)?;
    module.add_function(wrap_pyfunction!(get_standardized, module)?)?;
    module.add_function(wrap_pyfunction!(get_symmetrized, module)?)?;
    module.add_function(wrap_pyfunction!(get_symmetry_equivalent_sites, module)?)?;
    module.add_function(wrap_pyfunction!(get_spacegroup_type, module)?)?;
    module.add_function(wrap_pyfunction!(get_magnetic_symmetry_dataset, module)?)?;
    module.add_function(wrap_pyfunction!(get_symmetry_dataset, module)?)?;
    module.add_function(wrap_pyfunction!(apply_operation, module)?)?;
    module.add_function(wrap_pyfunction!(apply_inversion, module)?)?;
    module.add_function(wrap_pyfunction!(apply_translation, module)?)?;
    module.add_function(wrap_pyfunction!(get_bravais_class, module)?)?;
    module.add_function(wrap_pyfunction!(get_lattice_system, module)?)?;
    module.add_function(wrap_pyfunction!(get_crystal_family, module)?)?;
    module.add_function(wrap_pyfunction!(is_piezoelectric_allowed, module)?)?;
    module.add_function(wrap_pyfunction!(is_shg_allowed, module)?)?;
    module.add_function(wrap_pyfunction!(get_num_symmetry_operations, module)?)?;
    module.add_function(wrap_pyfunction!(get_num_unique_sites, module)?)?;
    module.add_function(wrap_pyfunction!(get_wyckoff_histogram, module)?)?;
    Ok(())
}
