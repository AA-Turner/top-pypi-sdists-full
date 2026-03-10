use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use moyo::base::Operation as MoyoOperation;
use moyo::data::{
    BravaisClass, Centering, CrystalFamily, GeometricCrystalClass, LatticeSystem, Setting,
    arithmetic_crystal_class_entry, hall_symbol_entry,
};
use nalgebra::{Matrix3, Vector3};
use std::collections::HashMap;
use std::sync::LazyLock;

use super::SymmetryOperation;

// === Symmetry Helper Functions ===

/// Validate symprec parameter for symmetry operations.
pub(super) fn validate_symprec(symprec: f64) -> Result<()> {
    if !symprec.is_finite() || symprec <= 0.0 {
        return Err(FerroxError::InvalidStructure {
            index: 0,
            reason: format!("symprec must be positive and finite, got {symprec}"),
        });
    }
    Ok(())
}

/// Convert nalgebra Matrix3 to a nested `[[f64; 3]; 3]` array.
#[inline]
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn mat3_to_array(mat: &Matrix3<f64>) -> [[f64; 3]; 3] {
    std::array::from_fn(|row| std::array::from_fn(|col| mat[(row, col)]))
}

/// Convert moyo Operations to arrays for easy serialization.
pub(crate) fn moyo_ops_to_arrays(ops: &[MoyoOperation]) -> Vec<SymmetryOperation> {
    ops.iter()
        .map(|op| {
            let rot = std::array::from_fn(|i| std::array::from_fn(|j| op.rotation[(i, j)]));
            let trans = [op.translation.x, op.translation.y, op.translation.z];
            (rot, trans)
        })
        .collect()
}

/// Get crystal system from spacegroup number.
pub(crate) fn spacegroup_to_crystal_system(sg: i32) -> &'static str {
    match sg {
        1..=2 => "triclinic",
        3..=15 => "monoclinic",
        16..=74 => "orthorhombic",
        75..=142 => "tetragonal",
        143..=167 => "trigonal",
        168..=194 => "hexagonal",
        195..=230 => "cubic",
        _ => "unknown",
    }
}

/// Look up the `GeometricCrystalClass` (point group) from a Hall number.
// TODO: uses InvalidStructure with dummy index: 0 -- add a dedicated error variant
pub(crate) fn geometric_crystal_class_from_hall(hall_number: i32) -> Result<GeometricCrystalClass> {
    let hall_entry =
        hall_symbol_entry(hall_number).ok_or_else(|| FerroxError::InvalidStructure {
            index: 0,
            reason: format!("Invalid Hall number: {hall_number}"),
        })?;
    let arith_entry =
        arithmetic_crystal_class_entry(hall_entry.arithmetic_number).ok_or_else(|| {
            FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "Invalid arithmetic crystal class number: {}",
                    hall_entry.arithmetic_number
                ),
            }
        })?;
    Ok(arith_entry.geometric_crystal_class)
}

/// Convert a `BravaisClass` enum variant to its static string representation.
fn bravais_class_str(bravais_class: BravaisClass) -> &'static str {
    match bravais_class {
        BravaisClass::aP => "aP",
        BravaisClass::mP => "mP",
        BravaisClass::mC => "mC",
        BravaisClass::oP => "oP",
        BravaisClass::oS => "oS",
        BravaisClass::oF => "oF",
        BravaisClass::oI => "oI",
        BravaisClass::tP => "tP",
        BravaisClass::tI => "tI",
        BravaisClass::hR => "hR",
        BravaisClass::hP => "hP",
        BravaisClass::cP => "cP",
        BravaisClass::cF => "cF",
        BravaisClass::cI => "cI",
    }
}

/// Convert a `LatticeSystem` enum variant to its static string representation.
fn lattice_system_str(lattice_system: LatticeSystem) -> &'static str {
    match lattice_system {
        LatticeSystem::Triclinic => "triclinic",
        LatticeSystem::Monoclinic => "monoclinic",
        LatticeSystem::Orthorhombic => "orthorhombic",
        LatticeSystem::Tetragonal => "tetragonal",
        LatticeSystem::Rhombohedral => "rhombohedral",
        LatticeSystem::Hexagonal => "hexagonal",
        LatticeSystem::Cubic => "cubic",
    }
}

/// Convert a `CrystalFamily` enum variant to its static string representation.
fn crystal_family_str(crystal_family: CrystalFamily) -> &'static str {
    match crystal_family {
        CrystalFamily::Triclinic => "triclinic",
        CrystalFamily::Monoclinic => "monoclinic",
        CrystalFamily::Orthorhombic => "orthorhombic",
        CrystalFamily::Tetragonal => "tetragonal",
        CrystalFamily::Hexagonal => "hexagonal",
        CrystalFamily::Cubic => "cubic",
    }
}

// === Spacegroup resolution and orbit generation ===

/// Resolve a space group identifier (ITA number or Hermann-Mauguin symbol) to a Hall number.
///
/// Accepts either:
/// - An integer string like "225" (ITA number 1-230)
/// - A Hermann-Mauguin symbol like "Fm-3m" or "P 6_3/m m c"
///
/// Returns the standard Hall number for the space group.
pub(crate) fn resolve_spacegroup(sg: &str) -> Result<i32> {
    // Try parsing as integer first
    if let Ok(number) = sg.parse::<i32>() {
        if !(1..=230).contains(&number) {
            return Err(FerroxError::InvalidArgument {
                reason: format!("Space group number must be 1-230, got {number}"),
            });
        }
        return Setting::Spglib
            .hall_number(number)
            .ok_or_else(|| FerroxError::InvalidArgument {
                reason: format!("No Hall number for space group {number}"),
            });
    }

    // Otherwise look up as Hermann-Mauguin symbol
    hm_symbol_to_hall_number(sg)
}

/// Look up a Hermann-Mauguin symbol to find the corresponding Hall number.
///
/// Matches against the `hm_short` field in moyo's Hall symbol database (530 entries).
/// Normalizes whitespace for flexible matching. Returns the first standard-setting
/// match for the ITA number.
fn hm_symbol_to_hall_number(symbol: &str) -> Result<i32> {
    static HM_TO_HALL: LazyLock<HashMap<String, i32>> = LazyLock::new(|| {
        let mut map = HashMap::new();
        for hall_num in 1..=530 {
            if let Some(entry) = hall_symbol_entry(hall_num) {
                let normalized = normalize_hm_symbol(entry.hm_short);
                // Prefer the standard setting (first Hall number per ITA number)
                map.entry(normalized).or_insert(hall_num);

                // Also index the full notation
                let normalized_full = normalize_hm_symbol(entry.hm_full);
                map.entry(normalized_full).or_insert(hall_num);
            }
        }
        map
    });

    let normalized = normalize_hm_symbol(symbol);
    HM_TO_HALL
        .get(&normalized)
        .copied()
        .ok_or_else(|| FerroxError::InvalidArgument {
            reason: format!(
                "Unknown space group symbol '{symbol}'. Use an ITA number (1-230) or \
                 Hermann-Mauguin symbol (e.g. 'Fm-3m', 'P6_3/mmc')."
            ),
        })
}

/// Normalize a Hermann-Mauguin symbol for comparison: strip spaces, lowercase.
fn normalize_hm_symbol(symbol: &str) -> String {
    symbol
        .chars()
        .filter(|ch| !ch.is_whitespace())
        .flat_map(|ch| ch.to_lowercase())
        .collect()
}

/// Validate that lattice parameters are compatible with the crystal system
/// implied by the space group.
pub(crate) fn validate_lattice_compatibility(
    lattice: &Lattice,
    sg_number: i32,
    centering: Centering,
) -> Result<()> {
    let crystal_system = spacegroup_to_crystal_system(sg_number);
    let lengths = lattice.lengths();
    let angles = lattice.angles();
    let (a, b, c) = (lengths[0], lengths[1], lengths[2]);
    let (alpha, beta, gamma) = (angles[0], angles[1], angles[2]);

    // Tolerance for floating-point comparison of lattice parameters
    let len_tol = 1e-4;
    let ang_tol = 0.1; // degrees

    let is_right = |angle: f64| (angle - 90.0).abs() < ang_tol;
    let all_right = is_right(alpha) && is_right(beta) && is_right(gamma);

    let err = |msg: &str| {
        Err(FerroxError::InvalidArgument {
            reason: format!(
                "Lattice parameters (a={a:.4}, b={b:.4}, c={c:.4}, \
                 alpha={alpha:.2}, beta={beta:.2}, gamma={gamma:.2}) \
                 incompatible with {crystal_system} crystal system: {msg}"
            ),
        })
    };

    match crystal_system {
        "cubic" => {
            if (a - b).abs() > len_tol || (a - c).abs() > len_tol {
                return err("a = b = c required");
            }
            if !all_right {
                return err("alpha = beta = gamma = 90° required");
            }
        }
        "hexagonal" => {
            if (a - b).abs() > len_tol {
                return err("a = b required");
            }
            if !is_right(alpha) || !is_right(beta) || (gamma - 120.0).abs() > ang_tol {
                return err("alpha = beta = 90°, gamma = 120° required");
            }
        }
        "trigonal" => {
            let hex_ok = (a - b).abs() < len_tol
                && is_right(alpha)
                && is_right(beta)
                && (gamma - 120.0).abs() < ang_tol;

            // R centering translations assume a hexagonal conventional cell, so a
            // primitive rhombohedral cell would produce wrong multiplicities.
            if matches!(centering, Centering::R) && !hex_ok {
                return err(
                    "the resolved Hall symbol uses R centering (hexagonal setting), \
                     so the lattice must be hexagonal (a=b, alpha=beta=90°, gamma=120°)",
                );
            } else if !matches!(centering, Centering::R) {
                // Rhombohedral: a=b=c, alpha=beta=gamma, not 90° and not 120°
                let rhomb_ok = (a - b).abs() < len_tol
                    && (a - c).abs() < len_tol
                    && (alpha - beta).abs() < ang_tol
                    && (alpha - gamma).abs() < ang_tol
                    && !is_right(alpha)
                    && (alpha - 120.0).abs() > ang_tol;
                if !hex_ok && !rhomb_ok {
                    return err("requires hexagonal (a=b, gamma=120°) or rhombohedral \
                         (a=b=c, alpha=beta=gamma ≠ 90°/120°) setting");
                }
            }
        }
        "tetragonal" => {
            if (a - b).abs() > len_tol {
                return err("a = b required");
            }
            if !all_right {
                return err("alpha = beta = gamma = 90° required");
            }
        }
        "orthorhombic" => {
            if !all_right {
                return err("alpha = beta = gamma = 90° required");
            }
        }
        "monoclinic" => {
            let axis_a_ok = is_right(beta) && is_right(gamma);
            let axis_b_ok = is_right(alpha) && is_right(gamma);
            let axis_c_ok = is_right(alpha) && is_right(beta);
            if !axis_a_ok && !axis_b_ok && !axis_c_ok {
                return err(
                    "requires two right angles: beta=gamma=90° (unique axis a), \
                     alpha=gamma=90° (unique axis b), or alpha=beta=90° (unique axis c)",
                );
            }
        }
        // Triclinic: no constraints
        _ => {}
    }
    Ok(())
}

/// Build the full set of conventional cell operations from coset representatives
/// and centering lattice points (including identity).
///
/// Uses the same algorithm as moyopy: for each lattice point `c` and each
/// coset representative `(R, t)`, creates `(R, (c + t) mod 1)`.
pub(crate) fn build_conventional_operations(
    coset_ops: &[moyo::base::Operation],
    lattice_points: &[Vector3<f64>],
) -> Vec<moyo::base::Operation> {
    use moyo::base::Operation;

    let mut operations = Vec::with_capacity(coset_ops.len() * lattice_points.len());
    for lp in lattice_points {
        for op in coset_ops {
            let new_translation = (lp + op.translation).map(|elem| elem.rem_euclid(1.0));
            operations.push(Operation::new(op.rotation, new_translation));
        }
    }
    operations
}

/// Generate the orbit of a fractional coordinate under a set of symmetry operations.
///
/// Applies each operation, wraps to [0,1), and deduplicates within `tol`.
pub(crate) fn generate_orbit(
    coord: &Vector3<f64>,
    operations: &[moyo::base::Operation],
    tol: f64,
) -> Vec<Vector3<f64>> {
    use crate::pbc::wrap_frac_coords;

    let mut orbit = Vec::new();

    for op in operations {
        let rot = op.rotation.map(|elem| elem as f64);
        let new_coord = wrap_frac_coords(&(rot * coord + op.translation));

        let is_duplicate = orbit.iter().any(|existing: &Vector3<f64>| {
            let mut diff = new_coord - existing;
            // Wrap differences to [-0.5, 0.5) for periodic comparison
            diff -= diff.map(|elem| elem.round());
            diff.iter().all(|&elem| elem.abs() < tol)
        });

        if !is_duplicate {
            orbit.push(new_coord);
        }
    }

    orbit
}

/// Static lookup of space group type information from an ITA number (1-230).
///
/// Returns point group, Laue group, crystal system, HM symbol, Hall symbol,
/// and symmetry predicates without needing a structure.
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn spacegroup_type_from_number(number: i32) -> Result<SpacegroupTypeInfo> {
    if !(1..=230).contains(&number) {
        return Err(FerroxError::InvalidArgument {
            reason: format!("Space group number must be 1-230, got {number}"),
        });
    }
    // O(1) lookup via static table: space group number → first Hall number
    static FIRST_HALL: LazyLock<[i32; 231]> = LazyLock::new(|| {
        let mut table = [0i32; 231];
        for hall_num in 1..=530 {
            if let Some(entry) = hall_symbol_entry(hall_num) {
                let sg = entry.number as usize;
                if sg <= 230 && table[sg] == 0 {
                    table[sg] = hall_num;
                }
            }
        }
        table
    });
    let first_hall = FIRST_HALL[number as usize];
    let hall_entry = hall_symbol_entry(first_hall).ok_or_else(|| FerroxError::InvalidArgument {
        reason: format!("No Hall entry for space group {number}"),
    })?;
    let arith_entry =
        arithmetic_crystal_class_entry(hall_entry.arithmetic_number).ok_or_else(|| {
            FerroxError::InvalidArgument {
                reason: format!(
                    "Invalid arithmetic crystal class number: {}",
                    hall_entry.arithmetic_number
                ),
            }
        })?;
    let gcc = arith_entry.geometric_crystal_class;
    let is_centrosymmetric = point_group_is_centrosymmetric(gcc);

    Ok(SpacegroupTypeInfo {
        number,
        hm_short: hall_entry.hm_short,
        hm_full: hall_entry.hm_full,
        hall_symbol: hall_entry.hall_symbol,
        crystal_system: spacegroup_to_crystal_system(number),
        point_group: point_group_symbol(gcc),
        laue_group: laue_group_from_point_group(gcc),
        is_centrosymmetric,
        is_polar: point_group_is_polar(gcc),
        is_chiral: point_group_is_chiral(gcc),
        arithmetic_crystal_class_number: arith_entry.arithmetic_number,
        arithmetic_crystal_class_symbol: arith_entry.symbol,
        bravais_class: bravais_class_str(arith_entry.bravais_class),
        lattice_system: lattice_system_str(arith_entry.lattice_system()),
        crystal_family: crystal_family_str(CrystalFamily::from_lattice_system(
            arith_entry.lattice_system(),
        )),
        is_piezoelectric_allowed: point_group_is_piezoelectric(gcc),
        is_shg_allowed: !is_centrosymmetric,
    })
}

/// Space group type information from a static lookup.
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) struct SpacegroupTypeInfo {
    pub number: i32,
    pub hm_short: &'static str,
    pub hm_full: &'static str,
    pub hall_symbol: &'static str,
    pub crystal_system: &'static str,
    pub point_group: &'static str,
    pub laue_group: &'static str,
    pub is_centrosymmetric: bool,
    pub is_polar: bool,
    pub is_chiral: bool,
    pub arithmetic_crystal_class_number: i32,
    pub arithmetic_crystal_class_symbol: &'static str,
    pub bravais_class: &'static str,
    pub lattice_system: &'static str,
    pub crystal_family: &'static str,
    pub is_piezoelectric_allowed: bool,
    pub is_shg_allowed: bool,
}

/// Get the Laue group Hermann-Mauguin symbol from a point group.
///
/// Maps each `GeometricCrystalClass` to its corresponding Laue class symbol
/// (the centrosymmetric supergroup of the point group).
pub(crate) fn laue_group_from_point_group(gcc: GeometricCrystalClass) -> &'static str {
    match gcc {
        // Triclinic
        GeometricCrystalClass::C1 | GeometricCrystalClass::Ci => "-1",
        // Monoclinic
        GeometricCrystalClass::C2 | GeometricCrystalClass::C1h | GeometricCrystalClass::C2h => {
            "2/m"
        }
        // Orthorhombic
        GeometricCrystalClass::D2 | GeometricCrystalClass::C2v | GeometricCrystalClass::D2h => {
            "mmm"
        }
        // Tetragonal
        GeometricCrystalClass::C4 | GeometricCrystalClass::S4 | GeometricCrystalClass::C4h => "4/m",
        GeometricCrystalClass::D4
        | GeometricCrystalClass::C4v
        | GeometricCrystalClass::D2d
        | GeometricCrystalClass::D4h => "4/mmm",
        // Trigonal
        GeometricCrystalClass::C3 | GeometricCrystalClass::C3i => "-3",
        GeometricCrystalClass::D3 | GeometricCrystalClass::C3v | GeometricCrystalClass::D3d => {
            "-3m"
        }
        // Hexagonal
        GeometricCrystalClass::C6 | GeometricCrystalClass::C3h | GeometricCrystalClass::C6h => {
            "6/m"
        }
        GeometricCrystalClass::D6
        | GeometricCrystalClass::C6v
        | GeometricCrystalClass::D3h
        | GeometricCrystalClass::D6h => "6/mmm",
        // Cubic
        GeometricCrystalClass::T | GeometricCrystalClass::Th => "m-3",
        GeometricCrystalClass::O | GeometricCrystalClass::Td | GeometricCrystalClass::Oh => "m-3m",
    }
}

/// Get the point group Hermann-Mauguin symbol from a `GeometricCrystalClass`.
pub(crate) fn point_group_symbol(gcc: GeometricCrystalClass) -> &'static str {
    match gcc {
        GeometricCrystalClass::C1 => "1",
        GeometricCrystalClass::Ci => "-1",
        GeometricCrystalClass::C2 => "2",
        GeometricCrystalClass::C1h => "m",
        GeometricCrystalClass::C2h => "2/m",
        GeometricCrystalClass::D2 => "222",
        GeometricCrystalClass::C2v => "mm2",
        GeometricCrystalClass::D2h => "mmm",
        GeometricCrystalClass::C4 => "4",
        GeometricCrystalClass::S4 => "-4",
        GeometricCrystalClass::C4h => "4/m",
        GeometricCrystalClass::D4 => "422",
        GeometricCrystalClass::C4v => "4mm",
        GeometricCrystalClass::D2d => "-42m",
        GeometricCrystalClass::D4h => "4/mmm",
        GeometricCrystalClass::C3 => "3",
        GeometricCrystalClass::C3i => "-3",
        GeometricCrystalClass::D3 => "32",
        GeometricCrystalClass::C3v => "3m",
        GeometricCrystalClass::D3d => "-3m",
        GeometricCrystalClass::C6 => "6",
        GeometricCrystalClass::C3h => "-6",
        GeometricCrystalClass::C6h => "6/m",
        GeometricCrystalClass::D6 => "622",
        GeometricCrystalClass::C6v => "6mm",
        GeometricCrystalClass::D3h => "-6m2",
        GeometricCrystalClass::D6h => "6/mmm",
        GeometricCrystalClass::T => "23",
        GeometricCrystalClass::Th => "m-3",
        GeometricCrystalClass::O => "432",
        GeometricCrystalClass::Td => "-43m",
        GeometricCrystalClass::Oh => "m-3m",
    }
}

/// Whether the point group is centrosymmetric (contains inversion).
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn point_group_is_centrosymmetric(gcc: GeometricCrystalClass) -> bool {
    matches!(
        gcc,
        GeometricCrystalClass::Ci
            | GeometricCrystalClass::C2h
            | GeometricCrystalClass::D2h
            | GeometricCrystalClass::C4h
            | GeometricCrystalClass::D4h
            | GeometricCrystalClass::C3i
            | GeometricCrystalClass::D3d
            | GeometricCrystalClass::C6h
            | GeometricCrystalClass::D6h
            | GeometricCrystalClass::Th
            | GeometricCrystalClass::Oh
    )
}

/// Whether the point group is polar (has a unique polar direction).
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn point_group_is_polar(gcc: GeometricCrystalClass) -> bool {
    matches!(
        gcc,
        GeometricCrystalClass::C1
            | GeometricCrystalClass::C2
            | GeometricCrystalClass::C1h
            | GeometricCrystalClass::C2v
            | GeometricCrystalClass::C4
            | GeometricCrystalClass::C4v
            | GeometricCrystalClass::C3
            | GeometricCrystalClass::C3v
            | GeometricCrystalClass::C6
            | GeometricCrystalClass::C6v
    )
}

/// Whether the point group is chiral (contains only proper rotations).
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn point_group_is_chiral(gcc: GeometricCrystalClass) -> bool {
    matches!(
        gcc,
        GeometricCrystalClass::C1
            | GeometricCrystalClass::C2
            | GeometricCrystalClass::D2
            | GeometricCrystalClass::C3
            | GeometricCrystalClass::D3
            | GeometricCrystalClass::C4
            | GeometricCrystalClass::D4
            | GeometricCrystalClass::C6
            | GeometricCrystalClass::D6
            | GeometricCrystalClass::T
            | GeometricCrystalClass::O
    )
}

/// Whether the point group allows piezoelectricity.
///
/// This is `!centrosymmetric` with one exception: point group 432 (O) is
/// non-centrosymmetric but its high symmetry (combined 4-fold and 3-fold axes)
/// forces all piezoelectric tensor coefficients to zero.
#[allow(dead_code)] // used by python + wasm feature gates
pub(crate) fn point_group_is_piezoelectric(gcc: GeometricCrystalClass) -> bool {
    !point_group_is_centrosymmetric(gcc) && gcc != GeometricCrystalClass::O
}

// === Slab Generation ===
