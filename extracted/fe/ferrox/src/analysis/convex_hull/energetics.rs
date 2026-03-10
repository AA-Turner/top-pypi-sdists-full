use super::interpolation::compute_e_above_hull_nd;
use super::quickhull::{compute_lower_hull_nd, compute_quickhull_nd};
use super::{ConvexHullEntry, HULL_EPSILON, LowerHullND};
use crate::composition::Composition;
use crate::element::Element;
use crate::error::{FerroxError, Result};
use std::collections::{BTreeSet, HashMap, HashSet};

/// Find the lowest-energy unary references for each element.
pub fn find_lowest_energy_unary_refs(entries: &[ConvexHullEntry]) -> Result<HashMap<Element, f64>> {
    let mut lowest_refs: HashMap<Element, f64> = HashMap::new();
    for entry in entries {
        if !entry.is_unary() {
            continue;
        }
        let element_composition = entry.composition.element_composition();
        let Some(element) = element_composition.unique_elements().iter().next().copied() else {
            continue;
        };
        let entry_energy = entry.corrected_energy_per_atom()?;
        lowest_refs
            .entry(element)
            .and_modify(|current_energy| {
                if entry_energy < *current_energy {
                    *current_energy = entry_energy;
                }
            })
            .or_insert(entry_energy);
    }
    Ok(lowest_refs)
}

/// Compute formation energy per atom for an entry.
pub fn compute_e_form_per_atom(
    entry: &ConvexHullEntry,
    unary_refs: &HashMap<Element, f64>,
) -> Result<f64> {
    if let Some(precomputed_e_form) = entry.e_form_per_atom
        && precomputed_e_form.is_finite()
    {
        return Ok(precomputed_e_form);
    }

    let atom_count = entry.composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Entry {} has non-positive atom count ({atom_count})",
                entry.id_or_formula()
            ),
        });
    }

    let elemental_composition = entry.composition.element_composition();
    let mut composition_elements: Vec<Element> = elemental_composition
        .unique_elements()
        .into_iter()
        .collect();
    composition_elements.sort_unstable_by_key(Element::atomic_number);
    let mut ref_energy_sum = 0.0;
    for element in composition_elements {
        let amount = elemental_composition.get_element_total(element);
        let Some(unary_ref_energy) = unary_refs.get(&element).copied() else {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Missing unary reference for element {} while computing formation energy of {}",
                    element.symbol(),
                    entry.id_or_formula()
                ),
            });
        };
        ref_energy_sum += (amount / atom_count) * unary_ref_energy;
    }
    Ok(entry.corrected_energy_per_atom()? - ref_energy_sum)
}

fn has_finite_precomputed_e_form(entry: &ConvexHullEntry) -> bool {
    entry.e_form_per_atom.is_some_and(f64::is_finite)
}

fn compute_entry_e_form(
    entry: &ConvexHullEntry,
    unary_refs: Option<&HashMap<Element, f64>>,
) -> Result<f64> {
    if let Some(precomputed_e_form) = entry.e_form_per_atom
        && precomputed_e_form.is_finite()
    {
        return Ok(precomputed_e_form);
    }
    let Some(unary_refs) = unary_refs else {
        return Err(FerroxError::CompositionError {
            reason: format!(
                "Entry {} requires absolute energy inputs because e_form_per_atom is missing",
                entry.id_or_formula()
            ),
        });
    };
    compute_e_form_per_atom(entry, unary_refs)
}

pub(crate) fn sorted_elements_from_entries(entries: &[ConvexHullEntry]) -> Vec<Element> {
    let mut elements: BTreeSet<(u8, Element)> = BTreeSet::new();
    for entry in entries {
        for element in entry.composition.element_composition().unique_elements() {
            elements.insert((element.atomic_number(), element));
        }
    }
    elements.into_iter().map(|(_, element)| element).collect()
}

fn composition_to_spatial_coords(
    composition: &Composition,
    element_order: &[Element],
) -> Result<Vec<f64>> {
    if element_order.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Cannot build coordinates for an empty element set".to_string(),
        });
    }
    let atom_count = composition.num_atoms();
    if !atom_count.is_finite() || atom_count <= 0.0 {
        return Err(FerroxError::CompositionError {
            reason: format!("Invalid composition atom count: {atom_count}"),
        });
    }

    let elemental_composition = composition.element_composition();
    let element_set: HashSet<Element> = element_order.iter().copied().collect();
    for present_element in elemental_composition.unique_elements() {
        if !element_set.contains(&present_element) {
            return Err(FerroxError::CompositionError {
                reason: format!(
                    "Composition includes element {} outside reference element set",
                    present_element.symbol()
                ),
            });
        }
    }

    if element_order.len() == 1 {
        return Ok(vec![]);
    }
    let spatial_dim = element_order.len() - 1;
    let mut coords = Vec::with_capacity(spatial_dim);
    for element in &element_order[..spatial_dim] {
        coords.push(elemental_composition.get_element_total(*element) / atom_count);
    }
    Ok(coords)
}

fn entry_to_hull_point(
    entry: &ConvexHullEntry,
    element_order: &[Element],
    e_form_per_atom: f64,
) -> Result<Vec<f64>> {
    let mut point = composition_to_spatial_coords(&entry.composition, element_order)?;
    point.push(e_form_per_atom);
    Ok(point)
}

fn should_inject_synthetic_corners(
    reference_entries: &[ConvexHullEntry],
    unary_refs: Option<&HashMap<Element, f64>>,
) -> bool {
    unary_refs.is_some() || !reference_entries.iter().any(ConvexHullEntry::is_unary)
}

/// Build lower hull from reference entries.
pub fn build_lower_hull(reference_entries: &[ConvexHullEntry]) -> Result<LowerHullND> {
    if reference_entries.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Reference entries cannot be empty".to_string(),
        });
    }

    let element_order = sorted_elements_from_entries(reference_entries);
    if element_order.is_empty() {
        return Err(FerroxError::CompositionError {
            reason: "Reference entries contain no valid elements".to_string(),
        });
    }

    let needs_unary_refs = reference_entries
        .iter()
        .any(|entry| !has_finite_precomputed_e_form(entry));
    let unary_refs = if needs_unary_refs {
        Some(find_lowest_energy_unary_refs(reference_entries)?)
    } else {
        None
    };
    let mut reference_points = Vec::with_capacity(reference_entries.len() + element_order.len());

    for entry in reference_entries {
        let e_form_per_atom = compute_entry_e_form(entry, unary_refs.as_ref())?;
        reference_points.push(entry_to_hull_point(entry, &element_order, e_form_per_atom)?);
    }

    if should_inject_synthetic_corners(reference_entries, unary_refs.as_ref()) {
        let n_elements = element_order.len();
        let spatial_dim = n_elements.saturating_sub(1);
        for element_idx in 0..n_elements {
            let mut corner_point = vec![0.0; spatial_dim + 1];
            if n_elements > 1 && element_idx < spatial_dim {
                corner_point[element_idx] = 1.0;
            }
            let corner_exists = reference_points.iter().any(|point| {
                point.len() == corner_point.len()
                    && point
                        .iter()
                        .zip(corner_point.iter())
                        .all(|(coord, corner_coord)| (coord - corner_coord).abs() < HULL_EPSILON)
            });
            if !corner_exists {
                reference_points.push(corner_point);
            }
        }
    }

    let all_facets = compute_quickhull_nd(&reference_points)?;
    let lower_facets = compute_lower_hull_nd(&all_facets);

    Ok(LowerHullND {
        element_order,
        reference_points,
        lower_facets,
    })
}

/// Compute `e_above_hull` values for entries against a reference hull.
pub fn calculate_e_above_hull(
    entries: &[ConvexHullEntry],
    reference_entries: &[ConvexHullEntry],
) -> Result<Vec<f64>> {
    if entries.is_empty() {
        return Ok(vec![]);
    }
    let hull_model = build_lower_hull(reference_entries)?;
    let needs_unary_refs = entries
        .iter()
        .chain(reference_entries.iter())
        .any(|entry| !has_finite_precomputed_e_form(entry));
    let unary_refs = if needs_unary_refs {
        Some(find_lowest_energy_unary_refs(reference_entries)?)
    } else {
        None
    };
    if hull_model.element_order.len() == 1 || hull_model.lower_facets.is_empty() {
        let reference_min_e_form =
            reference_entries
                .iter()
                .try_fold(f64::INFINITY, |current_min, entry| {
                    compute_entry_e_form(entry, unary_refs.as_ref())
                        .map(|value| current_min.min(value))
                })?;
        return entries
            .iter()
            .map(|entry| {
                compute_entry_e_form(entry, unary_refs.as_ref())
                    .map(|value| (value - reference_min_e_form).max(0.0))
            })
            .collect();
    }

    let query_points: Vec<Vec<f64>> = entries
        .iter()
        .map(|entry| {
            let e_form_per_atom = compute_entry_e_form(entry, unary_refs.as_ref())?;
            entry_to_hull_point(entry, &hull_model.element_order, e_form_per_atom)
        })
        .collect::<Result<Vec<_>>>()?;

    Ok(compute_e_above_hull_nd(
        &query_points,
        &hull_model.lower_facets,
        &hull_model.reference_points,
    ))
}
