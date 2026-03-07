//! PyStructureMatcher: OOP wrapper for StructureMatcher.

use std::collections::HashMap;

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3_stub_gen::derive::{gen_stub_pyclass, gen_stub_pymethods};

use crate::analysis::structure_matcher::{
    AnonymousClassMapping, AnonymousMatchMode, ComparatorType, StructureMatcher,
};
use crate::element::Element;
use crate::io::structure_to_pymatgen_json;
use crate::python::helpers::{
    StructureJson, parse_struct, parse_structure_pair, to_str_refs, validate_positive_f64,
};
use crate::structure::Structure;

fn format_skipped_indices(skipped_indices: &[usize]) -> String {
    skipped_indices
        .iter()
        .map(|idx| idx.to_string())
        .collect::<Vec<_>>()
        .join(", ")
}

fn ensure_no_skipped_indices(operation_name: &str, skipped_indices: &[usize]) -> PyResult<()> {
    if skipped_indices.is_empty() {
        return Ok(());
    }
    Err(PyValueError::new_err(format!(
        "{operation_name} skipped structure indices [{}]; set on_error=Fail in Rust API or clean inputs",
        format_skipped_indices(skipped_indices)
    )))
}

fn validate_predefined_mapping_coverage(
    struct1: &Structure,
    struct2: &Structure,
    mapping_kind: AnonymousClassMapping,
    mapping_name: &str,
) -> PyResult<()> {
    let missing_elements =
        StructureMatcher::missing_predefined_mapping_elements(struct1, struct2, mapping_kind);
    if missing_elements.is_empty() {
        return Ok(());
    }

    let missing_symbols = missing_elements
        .iter()
        .map(Element::symbol)
        .collect::<Vec<_>>()
        .join(", ");
    Err(PyValueError::new_err(format!(
        "Mapping '{mapping_name}' does not cover elements: {missing_symbols}"
    )))
}

fn parse_class_mapping_by_symbol(
    mapping_by_symbol: HashMap<String, String>,
) -> PyResult<HashMap<Element, String>> {
    let mut class_mapping = HashMap::new();
    for (element_symbol, class_label) in mapping_by_symbol {
        let trimmed_class_label = class_label.trim();
        if trimmed_class_label.is_empty() {
            return Err(PyValueError::new_err(format!(
                "Class label cannot be empty for element '{element_symbol}'"
            )));
        }
        let element = Element::from_symbol(&element_symbol).ok_or_else(|| {
            PyValueError::new_err(format!(
                "Invalid element symbol in mapping: '{element_symbol}'"
            ))
        })?;
        class_mapping.insert(element, trimmed_class_label.to_string());
    }
    Ok(class_mapping)
}

/// Python wrapper for StructureMatcher.
#[gen_stub_pyclass]
#[pyclass(module = "ferrox._ferrox.structure", name = "StructureMatcher")]
pub struct PyStructureMatcher {
    inner: StructureMatcher,
}

#[gen_stub_pymethods]
#[pymethods]
impl PyStructureMatcher {
    #[new]
    #[pyo3(signature = (
        latt_len_tol = 0.2,
        site_pos_tol = 0.3,
        angle_tol = 5.0,
        primitive_cell = true,
        scale = true,
        attempt_supercell = false,
        comparator = "species"
    ))]
    fn new(
        latt_len_tol: f64,
        site_pos_tol: f64,
        angle_tol: f64,
        primitive_cell: bool,
        scale: bool,
        attempt_supercell: bool,
        comparator: &str,
    ) -> PyResult<Self> {
        validate_positive_f64(latt_len_tol, "latt_len_tol")?;
        validate_positive_f64(site_pos_tol, "site_pos_tol")?;
        validate_positive_f64(angle_tol, "angle_tol")?;

        let comparator_type = match comparator {
            "species" => ComparatorType::Species,
            "element" => ComparatorType::Element,
            _ => {
                return Err(PyValueError::new_err(format!(
                    "Invalid comparator: {comparator}. Use 'species' or 'element'"
                )));
            }
        };

        let inner = StructureMatcher::new()
            .with_latt_len_tol(latt_len_tol)
            .with_site_pos_tol(site_pos_tol)
            .with_angle_tol(angle_tol)
            .with_primitive_cell(primitive_cell)
            .with_scale(scale)
            .with_attempt_supercell(attempt_supercell)
            .with_comparator(comparator_type);

        Ok(Self { inner })
    }

    #[pyo3(signature = (struct1, struct2, skip_structure_reduction = false))]
    fn fit(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
        skip_structure_reduction: bool,
    ) -> PyResult<bool> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        Ok(if skip_structure_reduction {
            self.inner.fit_preprocessed(&s1, &s2)
        } else {
            self.inner.fit(&s1, &s2)
        })
    }

    fn get_rms_dist(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
    ) -> PyResult<Option<(f64, f64)>> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        Ok(self.inner.get_rms_dist(&s1, &s2))
    }

    fn get_structure_distance(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
    ) -> PyResult<f64> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        Ok(self.inner.get_structure_distance(&s1, &s2))
    }

    #[pyo3(signature = (struct1, struct2, mapping_name = None, mapping = None))]
    fn fit_anonymous(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
        mapping_name: Option<&str>,
        mapping: Option<HashMap<String, String>>,
    ) -> PyResult<bool> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        if mapping_name.is_some() && mapping.is_some() {
            return Err(PyValueError::new_err(
                "Provide only one of mapping_name or mapping",
            ));
        }
        if let Some(predefined_mapping_name) = mapping_name {
            let mapping_kind =
                AnonymousClassMapping::from_name(predefined_mapping_name).ok_or_else(|| {
                    PyValueError::new_err(format!(
                        "Invalid mapping_name: {predefined_mapping_name}. Use one of: ACX, CEA, Metal/Non-metal"
                    ))
                })?;
            validate_predefined_mapping_coverage(&s1, &s2, mapping_kind, predefined_mapping_name)?;
            Ok(self.inner.fit_anonymous(
                &s1,
                &s2,
                Some(AnonymousMatchMode::Predefined(mapping_kind)),
            ))
        } else if let Some(custom_mapping) = mapping {
            let class_mapping = parse_class_mapping_by_symbol(custom_mapping)?;
            Ok(self
                .inner
                .fit_anonymous(&s1, &s2, Some(AnonymousMatchMode::Custom(&class_mapping))))
        } else {
            Ok(self.inner.fit_anonymous(&s1, &s2, None))
        }
    }

    fn get_structure_distance_anonymous_mapped(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
        mapping: HashMap<String, String>,
    ) -> PyResult<Option<f64>> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        let class_mapping = parse_class_mapping_by_symbol(mapping)?;
        Ok(self
            .inner
            .get_structure_distance_anonymous_mapped(&s1, &s2, &class_mapping))
    }

    fn get_structure_distance_anonymous_predefined(
        &self,
        struct1: StructureJson,
        struct2: StructureJson,
        mapping_name: &str,
    ) -> PyResult<Option<f64>> {
        let (s1, s2) = parse_structure_pair(&struct1, &struct2)?;
        let mapping_kind = AnonymousClassMapping::from_name(mapping_name).ok_or_else(|| {
            PyValueError::new_err(format!(
                "Invalid mapping_name: {mapping_name}. Use one of: ACX, CEA, Metal/Non-metal"
            ))
        })?;
        validate_predefined_mapping_coverage(&s1, &s2, mapping_kind, mapping_name)?;
        Ok(self
            .inner
            .get_structure_distance_anonymous_predefined(&s1, &s2, mapping_kind))
    }

    fn deduplicate(&self, py: Python<'_>, structures: Vec<String>) -> PyResult<Vec<usize>> {
        py.detach(|| {
            let dedup_result = self
                .inner
                .deduplicate_json(&to_str_refs(&structures))
                .map_err(|err| PyValueError::new_err(err.to_string()))?;
            ensure_no_skipped_indices("deduplicate", &dedup_result.skipped)?;
            Ok(dedup_result.parents)
        })
    }

    fn group(
        &self,
        py: Python<'_>,
        structures: Vec<String>,
    ) -> PyResult<HashMap<usize, Vec<usize>>> {
        py.detach(|| {
            let dedup_result = self
                .inner
                .deduplicate_json(&to_str_refs(&structures))
                .map_err(|err| PyValueError::new_err(err.to_string()))?;
            ensure_no_skipped_indices("group", &dedup_result.skipped)?;

            let mut groups: HashMap<usize, Vec<usize>> = HashMap::new();
            for (idx, canonical) in dedup_result.parents.into_iter().enumerate() {
                groups.entry(canonical).or_default().push(idx);
            }
            Ok(groups)
        })
    }

    fn get_unique_indices(&self, py: Python<'_>, structures: Vec<String>) -> PyResult<Vec<usize>> {
        py.detach(|| {
            let dedup_result = self
                .inner
                .deduplicate_json(&to_str_refs(&structures))
                .map_err(|err| PyValueError::new_err(err.to_string()))?;
            ensure_no_skipped_indices("get_unique_indices", &dedup_result.skipped)?;

            Ok(dedup_result
                .parents
                .iter()
                .enumerate()
                .filter_map(|(idx, &canonical)| (idx == canonical).then_some(idx))
                .collect())
        })
    }

    fn find_matches(
        &self,
        py: Python<'_>,
        new_structures: Vec<String>,
        existing_structures: Vec<String>,
    ) -> PyResult<Vec<Option<usize>>> {
        py.detach(|| {
            self.inner
                .find_matches_json(
                    &to_str_refs(&new_structures),
                    &to_str_refs(&existing_structures),
                )
                .map_err(|err| PyValueError::new_err(err.to_string()))
        })
    }

    fn reduce_structure(&self, py: Python<'_>, structure: StructureJson) -> PyResult<String> {
        let struc = parse_struct(&structure)?;
        let reduced = py.detach(|| self.inner.reduce_structure(&struc));
        Ok(structure_to_pymatgen_json(&reduced))
    }

    fn __repr__(&self) -> String {
        let sm = &self.inner;
        let py_bool = |b: bool| if b { "True" } else { "False" };
        format!(
            "StructureMatcher(latt_len_tol={}, site_pos_tol={}, angle_tol={}, \
             primitive_cell={}, scale={}, attempt_supercell={})",
            sm.latt_len_tol,
            sm.site_pos_tol,
            sm.angle_tol,
            py_bool(sm.primitive_cell),
            py_bool(sm.scale),
            py_bool(sm.attempt_supercell)
        )
    }

    #[getter]
    fn latt_len_tol(&self) -> f64 {
        self.inner.latt_len_tol
    }

    #[getter]
    fn site_pos_tol(&self) -> f64 {
        self.inner.site_pos_tol
    }

    #[getter]
    fn angle_tol(&self) -> f64 {
        self.inner.angle_tol
    }

    #[getter]
    fn primitive_cell(&self) -> bool {
        self.inner.primitive_cell
    }

    #[getter]
    fn scale(&self) -> bool {
        self.inner.scale
    }

    #[getter]
    fn attempt_supercell(&self) -> bool {
        self.inner.attempt_supercell
    }
}
