//! Chemical potential diagram computation.
//!
//! Computes N-dimensional chemical potential diagrams via halfspace intersection
//! and vertex enumeration. For an N-element system, each stable phase defines a
//! halfspace in N-dimensional chemical potential space (formal Δµ_i). The
//! stability region (domain) of each phase is the convex polytope where its
//! halfspace constraint is tight and all competing constraints are satisfied.
//!
//! Algorithm (following pymatgen's `ChemicalPotentialDiagram`):
//! 1. Identify elemental references (lowest energy per atom per element).
//! 2. De-duplicate entries by reduced formula, keeping the lowest-energy polymorph.
//! 3. Express each entry as a halfspace: `Σ(x_i · µ_i) ≤ E_form_per_atom`.
//! 4. Add border halfspaces for the display window (`µ_i ∈ [min_limit, 0]`).
//! 5. Enumerate all vertices of the halfspace arrangement by solving `dim`-sized
//!    linear sub-systems, checking feasibility, and assigning feasible vertices
//!    to the phases whose halfspaces are active.

use crate::analysis::convex_hull::{
    ConvexHullEntry, compute_e_form_per_atom, find_lowest_energy_unary_refs,
};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use std::collections::{BTreeSet, HashMap};

/// (hyperplane_rows, formula_names, formation_energies) for vertex enumeration.
type HyperplaneData = (Vec<Vec<f64>>, Vec<String>, Vec<f64>);

/// Numerical tolerance for singularity checks and feasibility tests.
const CHEMPOT_TOL: f64 = 1e-6;

/// Default lower bound for chemical potential axes (eV).
const DEFAULT_MIN_LIMIT: f64 = -50.0;

// === Public Types ===

/// A stability region for a single phase in chemical potential space.
#[derive(Debug, Clone)]
pub struct ChemPotRegion {
    /// Phase label (reduced formula).
    pub phase_name: String,
    /// Vertices of the stability polytope. Each vertex is a `Vec` of length N
    /// (number of elements), representing formal chemical potentials `[Δµ_0, …, Δµ_{N-1}]`.
    pub vertices: Vec<Vec<f64>>,
    /// Formation energy per atom of this phase (eV/atom).
    pub e_form_per_atom: f64,
}

/// Complete chemical potential diagram.
#[derive(Debug, Clone)]
pub struct ChemPotDiagram {
    /// Element ordering (determines axis mapping).
    pub elements: Vec<Element>,
    /// Stability regions for each stable phase.
    pub regions: Vec<ChemPotRegion>,
    /// Elemental reference energies per atom (eV/atom).
    pub el_refs: HashMap<Element, f64>,
}

// === Core Algorithm ===

/// Compute the chemical potential diagram from a set of convex hull entries.
///
/// The entries must include at least one unary (elemental) reference for every
/// element in the system. The returned diagram contains stability regions in
/// formal chemical potential space (Δµ relative to elemental references).
pub fn compute_chempot_diagram(entries: &[ConvexHullEntry]) -> Result<ChemPotDiagram> {
    let elements = sorted_elements(entries);
    let dim = elements.len();
    if dim < 2 {
        return Err(FerroxError::CompositionError {
            reason: format!("Chemical potential diagram requires 2+ elements, got {dim}"),
        });
    }

    let el_refs = find_lowest_energy_unary_refs(entries)?;
    for element in &elements {
        if !el_refs.contains_key(element) {
            return Err(FerroxError::CompositionError {
                reason: format!("Missing elemental reference for {}", element.symbol()),
            });
        }
    }

    let min_entries = get_min_entries(entries)?;

    let (hyperplanes, hp_formulas, hp_e_forms) =
        build_hyperplanes(&min_entries, &el_refs, &elements)?;

    let lims: Vec<(f64, f64)> = vec![(DEFAULT_MIN_LIMIT, 0.0); dim];
    let border_hps = build_border_hyperplanes(&lims);

    let domains = compute_domains(&hyperplanes, &border_hps, &hp_formulas, dim);

    let mut regions = Vec::new();
    for (formula, vertices) in &domains {
        if vertices.is_empty() {
            continue;
        }
        let e_form = hp_formulas
            .iter()
            .zip(hp_e_forms.iter())
            .find(|(name, _)| *name == formula)
            .map(|(_, e_form)| *e_form)
            .unwrap_or(0.0);
        regions.push(ChemPotRegion {
            phase_name: formula.clone(),
            vertices: vertices.clone(),
            e_form_per_atom: e_form,
        });
    }
    regions.sort_by(|region_a, region_b| region_a.phase_name.cmp(&region_b.phase_name));

    Ok(ChemPotDiagram {
        elements,
        regions,
        el_refs,
    })
}

/// Get per-element chemical potential bounds for a phase in the diagram.
///
/// Returns `Some(limits)` where `limits[i] = (min_µ_i, max_µ_i)` for the
/// phase's stability region, or `None` if the phase has no stability region.
pub fn get_chempot_limits(diagram: &ChemPotDiagram, phase: &str) -> Option<Vec<(f64, f64)>> {
    let region = diagram
        .regions
        .iter()
        .find(|region| region.phase_name == phase)?;
    if region.vertices.is_empty() {
        return None;
    }
    let dim = diagram.elements.len();
    let mut limits = vec![(f64::INFINITY, f64::NEG_INFINITY); dim];
    for vertex in &region.vertices {
        for (axis_idx, &val) in vertex.iter().enumerate().take(dim) {
            limits[axis_idx].0 = limits[axis_idx].0.min(val);
            limits[axis_idx].1 = limits[axis_idx].1.max(val);
        }
    }
    Some(limits)
}

// === Internal Helpers ===

/// Collect unique elements from entries, sorted by atomic number.
fn sorted_elements(entries: &[ConvexHullEntry]) -> Vec<Element> {
    let mut elements: BTreeSet<(u8, Element)> = BTreeSet::new();
    for entry in entries {
        for element in entry.composition.element_composition().unique_elements() {
            elements.insert((element.atomic_number(), element));
        }
    }
    elements.into_iter().map(|(_, element)| element).collect()
}

/// De-duplicate entries by reduced formula, keeping only the lowest-energy
/// polymorph for each composition.
fn get_min_entries(entries: &[ConvexHullEntry]) -> Result<Vec<ConvexHullEntry>> {
    let mut by_formula: HashMap<String, (ConvexHullEntry, f64)> = HashMap::new();
    for entry in entries {
        let formula = entry.composition.reduced_formula();
        let epa = entry.corrected_energy_per_atom()?;
        let dominated = by_formula
            .get(&formula)
            .is_some_and(|(_, existing_epa)| *existing_epa <= epa);
        if !dominated {
            by_formula.insert(formula, (entry.clone(), epa));
        }
    }
    Ok(by_formula.into_values().map(|(entry, _)| entry).collect())
}

/// Build halfspace rows for stable entries.
///
/// Each row is `[x_1, …, x_n, -E_form]` representing the constraint
/// `Σ(x_i · µ_i) + (-E_form) ≤ 0`, i.e. `Σ(x_i · µ_i) ≤ E_form`.
///
/// Only entries with negative formation energy or elemental references are included.
fn build_hyperplanes(
    min_entries: &[ConvexHullEntry],
    el_refs: &HashMap<Element, f64>,
    elements: &[Element],
) -> Result<HyperplaneData> {
    let dim = elements.len();
    let mut hyperplanes: Vec<Vec<f64>> = Vec::new();
    let mut formulas: Vec<String> = Vec::new();
    let mut e_forms: Vec<f64> = Vec::new();

    for entry in min_entries {
        let atom_count = entry.composition.num_atoms();
        let elem_comp = entry.composition.element_composition();
        let e_form = compute_e_form_per_atom(entry, el_refs)?;
        let is_elemental = entry.is_unary();

        if e_form < -CHEMPOT_TOL || is_elemental {
            let mut row = vec![0.0; dim + 1];
            for (elem_idx, element) in elements.iter().enumerate() {
                row[elem_idx] = elem_comp.get_element_total(*element) / atom_count;
            }
            row[dim] = -e_form;
            hyperplanes.push(row);
            formulas.push(entry.composition.reduced_formula());
            e_forms.push(e_form);
        }
    }

    Ok((hyperplanes, formulas, e_forms))
}

/// Build border halfspaces from per-axis limits.
///
/// For axis `i` with limits `[lo, hi]`:
/// - Lower bound: `−µ_i + lo ≤ 0` → `µ_i ≥ lo` → row `[-1, 0, …, lo]`
/// - Upper bound: `µ_i − hi ≤ 0` → `µ_i ≤ hi` → row `[1, 0, …, -hi]`
fn build_border_hyperplanes(lims: &[(f64, f64)]) -> Vec<Vec<f64>> {
    let dim = lims.len();
    let mut borders = Vec::with_capacity(dim * 2);
    for (idx, (lo, hi)) in lims.iter().enumerate() {
        let mut lower = vec![0.0; dim + 1];
        lower[idx] = -1.0;
        lower[dim] = *lo;
        borders.push(lower);

        let mut upper = vec![0.0; dim + 1];
        upper[idx] = 1.0;
        upper[dim] = -*hi;
        borders.push(upper);
    }
    borders
}

/// Compute chemical potential domains via vertex enumeration.
///
/// For each combination of `dim` halfspaces from the combined set (entry + border),
/// solves the linear system for the intersection vertex, checks feasibility against
/// all remaining halfspaces, and assigns feasible vertices to entry domains.
fn compute_domains(
    hyperplanes: &[Vec<f64>],
    border_hyperplanes: &[Vec<f64>],
    entry_formulas: &[String],
    dim: usize,
) -> HashMap<String, Vec<Vec<f64>>> {
    let n_entries = hyperplanes.len();
    let all_hs: Vec<&Vec<f64>> = hyperplanes
        .iter()
        .chain(border_hyperplanes.iter())
        .collect();
    let n_total = all_hs.len();

    let mut domains: HashMap<String, Vec<Vec<f64>>> = HashMap::new();
    for formula in entry_formulas {
        domains.entry(formula.clone()).or_default();
    }

    let mut combo: Vec<usize> = (0..dim).collect();

    loop {
        let has_entry = combo.iter().any(|&idx| idx < n_entries);
        if has_entry {
            let matrix: Vec<Vec<f64>> = combo
                .iter()
                .map(|&idx| all_hs[idx][..dim].to_vec())
                .collect();
            let rhs: Vec<f64> = combo.iter().map(|&idx| -all_hs[idx][dim]).collect();

            if let Some(mu) = solve_linear_system(&matrix, &rhs) {
                let feasible = (0..n_total).all(|idx| {
                    if combo.contains(&idx) {
                        return true;
                    }
                    let hs = all_hs[idx];
                    let val: f64 = (0..dim).map(|jdx| hs[jdx] * mu[jdx]).sum::<f64>() + hs[dim];
                    val <= CHEMPOT_TOL
                });

                if feasible {
                    for &hs_idx in &combo {
                        if hs_idx < n_entries {
                            domains
                                .get_mut(&entry_formulas[hs_idx])
                                .unwrap()
                                .push(mu.clone());
                        }
                    }
                }
            }
        }

        if !advance_combination(&mut combo, n_total) {
            break;
        }
    }

    domains.retain(|_, verts| !verts.is_empty());
    domains
}

/// Advance a combination to the next lexicographic order.
/// Returns `false` when all combinations are exhausted.
fn advance_combination(combo: &mut [usize], n_total: usize) -> bool {
    let dim = combo.len();
    let mut pos = dim;
    loop {
        if pos == 0 {
            return false;
        }
        pos -= 1;
        if combo[pos] < n_total - dim + pos {
            break;
        }
    }
    combo[pos] += 1;
    for idx in (pos + 1)..dim {
        combo[idx] = combo[idx - 1] + 1;
    }
    true
}

/// Solve a `dim × dim` linear system `Ax = b` via Gaussian elimination with
/// partial pivoting. Returns `None` if the matrix is singular.
fn solve_linear_system(matrix_a: &[Vec<f64>], vector_b: &[f64]) -> Option<Vec<f64>> {
    let dim = matrix_a.len();
    if dim == 0 {
        return Some(vec![]);
    }
    if vector_b.len() != dim || matrix_a.iter().any(|row| row.len() != dim) {
        return None;
    }

    let mut augmented: Vec<Vec<f64>> = matrix_a
        .iter()
        .zip(vector_b.iter())
        .map(|(row, &rhs)| {
            let mut merged = row.clone();
            merged.push(rhs);
            merged
        })
        .collect();

    for pivot_col in 0..dim {
        let mut pivot_row = pivot_col;
        for row_idx in (pivot_col + 1)..dim {
            if augmented[row_idx][pivot_col].abs() > augmented[pivot_row][pivot_col].abs() {
                pivot_row = row_idx;
            }
        }
        if augmented[pivot_row][pivot_col].abs() < CHEMPOT_TOL {
            return None;
        }
        if pivot_row != pivot_col {
            augmented.swap(pivot_row, pivot_col);
        }

        let pivot_row_values = augmented[pivot_col].clone();
        for row_idx in (pivot_col + 1)..dim {
            let factor = augmented[row_idx][pivot_col] / augmented[pivot_col][pivot_col];
            for col_idx in pivot_col..=dim {
                augmented[row_idx][col_idx] -= factor * pivot_row_values[col_idx];
            }
        }
    }

    let mut solution = vec![0.0; dim];
    for row_idx in (0..dim).rev() {
        let mut rhs_val = augmented[row_idx][dim];
        for col_idx in (row_idx + 1)..dim {
            rhs_val -= augmented[row_idx][col_idx] * solution[col_idx];
        }
        solution[row_idx] = rhs_val / augmented[row_idx][row_idx];
    }
    Some(solution)
}

/// De-duplicate vertices within tolerance.
pub fn dedup_vertices(vertices: &[Vec<f64>], tol: f64) -> Vec<Vec<f64>> {
    let mut unique: Vec<Vec<f64>> = Vec::new();
    for vertex in vertices {
        let is_dup = unique.iter().any(|existing| {
            existing.len() == vertex.len()
                && existing
                    .iter()
                    .zip(vertex.iter())
                    .all(|(val_a, val_b)| (val_a - val_b).abs() < tol)
        });
        if !is_dup {
            unique.push(vertex.clone());
        }
    }
    unique
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::composition::Composition;
    use approx::assert_abs_diff_eq;

    fn make_entry(formula: &str, e_form_per_atom: f64) -> ConvexHullEntry {
        let composition =
            Composition::from_formula(formula).expect("formula should parse in tests");
        let n_atoms = composition.num_atoms();
        ConvexHullEntry {
            entry_id: None,
            composition,
            energy: e_form_per_atom * n_atoms,
            energy_per_atom: Some(e_form_per_atom),
            e_form_per_atom: Some(e_form_per_atom),
            correction: None,
        }
    }

    #[test]
    fn test_binary_diagram_has_three_regions() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        assert_eq!(diagram.elements.len(), 2);
        assert_eq!(diagram.regions.len(), 3);
    }

    #[test]
    fn test_binary_elemental_ref_energies() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        assert_abs_diff_eq!(diagram.el_refs[&Element::Li], 0.0, epsilon = 1e-12);
        assert_abs_diff_eq!(diagram.el_refs[&Element::O], 0.0, epsilon = 1e-12);
    }

    #[test]
    fn test_binary_li2o_vertices() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        let li2o_region = diagram
            .regions
            .iter()
            .find(|region| region.phase_name == "Li2O")
            .expect("Li2O region must exist");

        let verts = dedup_vertices(&li2o_region.vertices, 1e-8);
        assert_eq!(verts.len(), 2, "Li2O should have 2 unique vertices");

        // Li2O: x_Li=2/3, x_O=1/3, e_form=-0.5
        // H(Li)∩H(Li2O): µ_Li=0, (1/3)µ_O = -0.5 → µ_O = -1.5 → (0, -1.5)
        // H(O)∩H(Li2O): µ_O=0, (2/3)µ_Li = -0.5 → µ_Li = -0.75 → (-0.75, 0)
        let has_vertex_a = verts
            .iter()
            .any(|v| (v[0]).abs() < 1e-6 && (v[1] + 1.5).abs() < 1e-6);
        let has_vertex_b = verts
            .iter()
            .any(|v| (v[0] + 0.75).abs() < 1e-6 && (v[1]).abs() < 1e-6);
        assert!(has_vertex_a, "expected vertex (0, -1.5), got {verts:?}");
        assert!(has_vertex_b, "expected vertex (-0.75, 0), got {verts:?}");
    }

    #[test]
    fn test_unstable_phase_has_no_region() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
            make_entry("LiO", 0.3), // unstable
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        let lio_region = diagram
            .regions
            .iter()
            .find(|region| region.phase_name == "LiO");
        assert!(lio_region.is_none(), "unstable LiO should have no region");
    }

    #[test]
    fn test_get_chempot_limits_binary() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();

        let li2o_limits = get_chempot_limits(&diagram, "Li2O").expect("Li2O must have limits");
        // µ_Li ranges from -0.75 to 0, µ_O ranges from -1.5 to 0
        assert_abs_diff_eq!(li2o_limits[0].0, -0.75, epsilon = 1e-6);
        assert_abs_diff_eq!(li2o_limits[0].1, 0.0, epsilon = 1e-6);
        assert_abs_diff_eq!(li2o_limits[1].0, -1.5, epsilon = 1e-6);
        assert_abs_diff_eq!(li2o_limits[1].1, 0.0, epsilon = 1e-6);
    }

    #[test]
    fn test_missing_phase_returns_none() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        assert!(get_chempot_limits(&diagram, "NaCl").is_none());
    }

    #[test]
    fn test_requires_at_least_two_elements() {
        let entries = vec![make_entry("Li", 0.0)];
        let result = compute_chempot_diagram(&entries);
        assert!(result.is_err());
    }

    #[test]
    fn test_requires_elemental_references() {
        let entries = vec![make_entry("Li2O", -0.5)];
        let result = compute_chempot_diagram(&entries);
        assert!(result.is_err());
    }

    #[test]
    fn test_ternary_diagram_produces_regions() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("Fe", 0.0),
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
            make_entry("Fe2O3", -0.8),
            make_entry("LiFeO2", -1.0),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        assert_eq!(diagram.elements.len(), 3);

        // All stable phases should have regions
        for phase_name in &["Li", "Fe", "O", "Li2O", "Fe2O3", "LiFeO2"] {
            let region = diagram
                .regions
                .iter()
                .find(|region| region.phase_name == *phase_name);
            assert!(
                region.is_some(),
                "phase {phase_name} should have a stability region"
            );
            let region = region.unwrap();
            let unique = dedup_vertices(&region.vertices, 1e-8);
            assert!(
                unique.len() >= 2,
                "phase {phase_name} should have ≥2 unique vertices, got {}",
                unique.len()
            );
        }
    }

    #[test]
    fn test_dedup_vertices_removes_near_duplicates() {
        let vertices = vec![vec![0.0, 1.0], vec![1e-10, 1.0 + 1e-10], vec![2.0, 3.0]];
        let unique = dedup_vertices(&vertices, 1e-4);
        assert_eq!(unique.len(), 2);
    }

    #[test]
    fn test_elemental_ref_selects_lowest_polymorph() {
        let entries = vec![
            make_entry("Li", 0.0),
            make_entry("Li", 0.2), // higher-energy polymorph
            make_entry("O", 0.0),
            make_entry("Li2O", -0.5),
        ];
        let diagram = compute_chempot_diagram(&entries).unwrap();
        assert_abs_diff_eq!(diagram.el_refs[&Element::Li], 0.0, epsilon = 1e-12);
    }

    #[test]
    fn test_solve_linear_system_2x2() {
        let matrix = vec![vec![1.0, 0.0], vec![0.0, 1.0]];
        let rhs = vec![3.0, 4.0];
        let solution = solve_linear_system(&matrix, &rhs).unwrap();
        assert_abs_diff_eq!(solution[0], 3.0, epsilon = 1e-12);
        assert_abs_diff_eq!(solution[1], 4.0, epsilon = 1e-12);
    }

    #[test]
    fn test_solve_linear_system_singular_returns_none() {
        let matrix = vec![vec![1.0, 1.0], vec![1.0, 1.0]];
        let rhs = vec![1.0, 2.0];
        assert!(solve_linear_system(&matrix, &rhs).is_none());
    }
}
