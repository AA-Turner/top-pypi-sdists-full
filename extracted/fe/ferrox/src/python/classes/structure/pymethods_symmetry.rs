use std::collections::HashSet;

use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3_stub_gen::derive::gen_stub_pymethods;

use crate::cell_ops;
use crate::python::helpers::mat3_to_array;
use crate::structure::{
    geometric_crystal_class_from_hall, point_group_symbol, spacegroup_to_crystal_system,
    spacegroup_type_from_number,
};

use super::{PyStructure, ferrox_err, set_none_keys, write_mag_analysis, wyckoff_histogram};

#[gen_stub_pymethods]
#[pymethods]
impl PyStructure {
    // === Symmetry (using cached dataset) ===

    /// Space group number (1-230).
    #[pyo3(signature = (symprec = 0.01))]
    fn get_spacegroup_number(&self, symprec: f64) -> PyResult<i32> {
        Ok(self._dataset(symprec)?.number)
    }

    /// Hermann-Mauguin short symbol.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_spacegroup_symbol(&self, symprec: f64) -> PyResult<String> {
        Ok(self._dataset(symprec)?.hm_symbol.clone())
    }

    /// Hall number (1-530).
    #[pyo3(signature = (symprec = 0.01))]
    fn get_hall_number(&self, symprec: f64) -> PyResult<i32> {
        Ok(self._dataset(symprec)?.hall_number)
    }

    /// Crystal system string.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_crystal_system(&self, symprec: f64) -> PyResult<String> {
        let ds = self._dataset(symprec)?;
        Ok(spacegroup_to_crystal_system(ds.number).to_string())
    }

    /// Pearson symbol (e.g. "cF8").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_pearson_symbol(&self, symprec: f64) -> PyResult<String> {
        Ok(self._dataset(symprec)?.pearson_symbol.clone())
    }

    /// Bravais class (e.g. "cF", "tI", "oP").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_bravais_class(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.bravais_class.to_string())
    }

    /// Lattice system (e.g. "cubic", "hexagonal").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_lattice_system(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.lattice_system.to_string())
    }

    /// Crystal family (e.g. "cubic", "hexagonal").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_crystal_family(&self, symprec: f64) -> PyResult<String> {
        Ok(self._spg_type_info(symprec)?.crystal_family.to_string())
    }

    /// Whether centrosymmetric.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_centrosymmetric(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_centrosymmetric)
    }

    /// Whether polar.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_polar(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_polar)
    }

    /// Whether chiral (Sohncke group).
    #[pyo3(signature = (symprec = 0.01))]
    fn is_chiral(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_chiral)
    }

    /// Whether piezoelectricity is symmetry-allowed.
    /// Non-centrosymmetric except point group 432 (O), whose high symmetry
    /// forces all piezoelectric tensor coefficients to zero.
    #[pyo3(signature = (symprec = 0.01))]
    fn is_piezoelectric_allowed(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_piezoelectric_allowed)
    }

    /// Whether SHG is symmetry-allowed (non-centrosymmetric).
    #[pyo3(signature = (symprec = 0.01))]
    fn is_shg_allowed(&self, symprec: f64) -> PyResult<bool> {
        Ok(self._spg_type_info(symprec)?.is_shg_allowed)
    }

    /// Number of symmetry operations.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_num_symmetry_operations(&self, symprec: f64) -> PyResult<usize> {
        Ok(self._dataset(symprec)?.operations.len())
    }

    /// Number of symmetry-unique sites.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_num_unique_sites(&self, symprec: f64) -> PyResult<usize> {
        let ds = self._dataset(symprec)?;
        Ok(ds.orbits.iter().collect::<HashSet<_>>().len())
    }

    /// Wyckoff letters for each site.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_wyckoff_letters(&self, symprec: f64) -> PyResult<Vec<String>> {
        let ds = self._dataset(symprec)?;
        Ok(ds.wyckoffs.iter().map(|ch| ch.to_string()).collect())
    }

    /// Wyckoff histogram: {letter: count}.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_wyckoff_histogram(&self, py: Python<'_>, symprec: f64) -> PyResult<Py<PyDict>> {
        let ds = self._dataset(symprec)?;
        Ok(wyckoff_histogram(&ds.wyckoffs).into_pyobject(py)?.unbind())
    }

    /// Site symmetry symbols.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_site_symmetry_symbols(&self, symprec: f64) -> PyResult<Vec<String>> {
        let ds = self._dataset(symprec)?;
        Ok(ds.site_symmetry_symbols.clone())
    }

    // === Magnetism ===

    /// Magnetic analysis results as a dict.
    #[pyo3(signature = (threshold = 0.05, symprec = 0.01))]
    fn get_magnetic_analysis(
        &self,
        py: Python<'_>,
        threshold: f64,
        symprec: f64,
    ) -> PyResult<Py<PyDict>> {
        let dataset = self._dataset(symprec).ok();
        let analysis = self
            .inner
            .magnetic_analysis(threshold, dataset.as_ref().map(|ds| &ds.orbits[..]));
        let dict = PyDict::new(py);
        write_mag_analysis(&dict, &analysis)?;
        Ok(dict.unbind())
    }

    // === Batch metadata ===

    /// Get all structure metadata as a comprehensive dict.
    ///
    /// Computes the symmetry dataset once and extracts all fields in a single pass.
    #[pyo3(signature = (symprec = 0.01, reduce_tol = 1e-5, mag_threshold = 0.05, disorder_tol = 1e-3))]
    fn get_all_metadata(
        &self,
        py: Python<'_>,
        symprec: f64,
        reduce_tol: f64,
        mag_threshold: f64,
        disorder_tol: f64,
    ) -> PyResult<Py<PyDict>> {
        let dict = PyDict::new(py);
        let comp = self.inner.composition();
        let species_comp = self.inner.species_composition();

        // Core
        dict.set_item("is_ordered", self.inner.is_ordered())?;
        dict.set_item("num_sites", self.inner.num_sites())?;
        dict.set_item("num_formula_units", comp.num_formula_units())?;

        // Composition
        dict.set_item("reduced_formula", comp.reduced_formula())?;
        dict.set_item("anonymized_formula", comp.anonymous_formula())?;
        dict.set_item("formula_unit_cell", comp.formula())?;
        dict.set_item("chemical_system", comp.chemical_system())?;
        dict.set_item("num_elements", comp.num_elements())?;
        dict.set_item("mean_atomic_mass", comp.mean_atomic_mass())?;
        dict.set_item("mean_atomic_number", comp.mean_atomic_number())?;
        dict.set_item("molar_mass_reduced", comp.molar_mass_reduced())?;
        dict.set_item("molar_mass_unit_cell", comp.weight())?;
        dict.set_item("anx_formula", species_comp.anx_formula())?;

        // Elements
        let mut elems: Vec<String> = comp
            .unique_elements()
            .iter()
            .map(|elem| elem.symbol().to_string())
            .collect();
        elems.sort_unstable();
        dict.set_item("elements", elems)?;

        // Composition maps
        dict.set_item("atomic_fractions", comp.atomic_fractions_map())?;
        dict.set_item("composition_unit_cell", comp.composition_unit_cell_map())?;
        dict.set_item("composition_reduced", comp.composition_reduced_map())?;

        // Disorder
        dict.set_item(
            "has_substitutional_disorder",
            self.inner.has_substitutional_disorder(),
        )?;
        dict.set_item(
            "has_vacancy_disorder",
            self.inner.has_vacancy_disorder(disorder_tol),
        )?;
        dict.set_item("max_species_per_site", self.inner.max_species_per_site())?;
        dict.set_item(
            "min_total_occupancy_per_site",
            self.inner.min_total_occupancy_per_site(),
        )?;
        dict.set_item(
            "num_disordered_sites",
            self.inner.num_disordered_sites(disorder_tol),
        )?;

        // Oxidation (reuse species_comp from above)
        let has_oxi = self.inner.has_oxidation_states();
        dict.set_item("has_oxidation_states", has_oxi)?;
        if has_oxi {
            dict.set_item("composition_charge", species_comp.charge())?;
            dict.set_item("is_charge_neutral", species_comp.is_charge_balanced())?;
        } else {
            dict.set_item("composition_charge", py.None())?;
            dict.set_item("is_charge_neutral", py.None())?;
        }

        // Lattice
        let lengths = self.inner.lattice.lengths();
        let angles = self.inner.lattice.angles();
        dict.set_item("volume", self.inner.volume())?;
        dict.set_item("density", self.inner.density())?;
        dict.set_item("atomic_density", self.inner.atomic_density())?;
        dict.set_item("volume_per_site", self.inner.volume_per_site())?;
        dict.set_item("lattice_a", lengths.x)?;
        dict.set_item("lattice_b", lengths.y)?;
        dict.set_item("lattice_c", lengths.z)?;
        dict.set_item("lattice_alpha", angles.x)?;
        dict.set_item("lattice_beta", angles.y)?;
        dict.set_item("lattice_gamma", angles.z)?;

        dict.set_item("lattice_matrix", mat3_to_array(self.inner.lattice.matrix()))?;

        // Niggli G6
        let g6_keys = [
            "niggli_g6_a2",
            "niggli_g6_b2",
            "niggli_g6_c2",
            "niggli_g6_2bc",
            "niggli_g6_2ac",
            "niggli_g6_2ab",
        ];
        match cell_ops::niggli_g6(&self.inner.lattice, reduce_tol) {
            Ok(g6) => {
                for (key, val) in g6_keys.iter().zip(g6.as_array()) {
                    dict.set_item(*key, val)?;
                }
            }
            Err(_) => set_none_keys(&dict, &g6_keys)?,
        }

        // Selling S6
        let s6_keys = [
            "selling_s6_bc",
            "selling_s6_ac",
            "selling_s6_ab",
            "selling_s6_ad",
            "selling_s6_bd",
            "selling_s6_cd",
        ];
        match cell_ops::selling_s6(&self.inner.lattice, reduce_tol) {
            Ok(s6) => {
                for (key, val) in s6_keys.iter().zip(s6.as_array()) {
                    dict.set_item(*key, val)?;
                }
            }
            Err(_) => set_none_keys(&dict, &s6_keys)?,
        }

        // Symmetry (single dataset computation, reuse for magnetism + prototype).
        // SYM_KEYS enumerates every key this block writes so the fallback path
        // can set them all to None in one call.
        const SYM_KEYS: &[&str] = &[
            "spacegroup_number",
            "spacegroup_hm_short",
            "hall_number",
            "pearson_symbol",
            "crystal_system",
            "num_symmetry_operations",
            "wyckoffs",
            "site_symmetry_symbols",
            "num_unique_sites",
            "wyckoff_histogram",
            "point_group",
            "laue_group",
            "is_centrosymmetric",
            "is_polar",
            "is_chiral",
            "is_piezoelectric_allowed",
            "is_shg_allowed",
            "hall_symbol",
            "arithmetic_crystal_class_number",
            "arithmetic_crystal_class_symbol",
            "bravais_class",
            "lattice_system",
            "crystal_family",
            "std_linear",
            "std_origin_shift",
            "std_rotation_matrix",
            "mapping_std_prim",
        ];
        let dataset = self._dataset(symprec).ok();
        if let Some(ref ds) = dataset {
            dict.set_item("spacegroup_number", ds.number)?;
            dict.set_item("spacegroup_hm_short", &ds.hm_symbol)?;
            dict.set_item("hall_number", ds.hall_number)?;
            dict.set_item("pearson_symbol", &ds.pearson_symbol)?;
            dict.set_item("crystal_system", spacegroup_to_crystal_system(ds.number))?;
            dict.set_item("num_symmetry_operations", ds.operations.len())?;

            // Wyckoff
            let wyckoff_strs: Vec<String> = ds.wyckoffs.iter().map(|ch| ch.to_string()).collect();
            dict.set_item("wyckoffs", &wyckoff_strs)?;
            dict.set_item("site_symmetry_symbols", &ds.site_symmetry_symbols)?;

            let unique_sites = ds.orbits.iter().collect::<HashSet<_>>().len();
            dict.set_item("num_unique_sites", unique_sites)?;

            // Wyckoff histogram
            dict.set_item("wyckoff_histogram", wyckoff_histogram(&ds.wyckoffs))?;

            // Point group + SpacegroupTypeInfo
            if let Ok(info) = spacegroup_type_from_number(ds.number) {
                dict.set_item("point_group", info.point_group)?;
                dict.set_item("laue_group", info.laue_group)?;
                dict.set_item("is_centrosymmetric", info.is_centrosymmetric)?;
                dict.set_item("is_polar", info.is_polar)?;
                dict.set_item("is_chiral", info.is_chiral)?;
                dict.set_item("is_piezoelectric_allowed", info.is_piezoelectric_allowed)?;
                dict.set_item("is_shg_allowed", info.is_shg_allowed)?;
                dict.set_item("hall_symbol", info.hall_symbol)?;
                dict.set_item(
                    "arithmetic_crystal_class_number",
                    info.arithmetic_crystal_class_number,
                )?;
                dict.set_item(
                    "arithmetic_crystal_class_symbol",
                    info.arithmetic_crystal_class_symbol,
                )?;
                dict.set_item("bravais_class", info.bravais_class)?;
                dict.set_item("lattice_system", info.lattice_system)?;
                dict.set_item("crystal_family", info.crystal_family)?;
            }

            // Transformation matrices
            dict.set_item("std_linear", mat3_to_array(&ds.std_linear))?;
            let shift = &ds.std_origin_shift;
            dict.set_item("std_origin_shift", [shift.x, shift.y, shift.z])?;
            dict.set_item(
                "std_rotation_matrix",
                mat3_to_array(&ds.std_rotation_matrix),
            )?;
            dict.set_item("mapping_std_prim", &ds.mapping_std_prim)?;
        } else {
            set_none_keys(&dict, SYM_KEYS)?;
        }

        // Magnetism (reuse orbits from symmetry dataset above)
        let orbits = dataset.as_ref().map(|ds| &ds.orbits[..]);
        let mag = self.inner.magnetic_analysis(mag_threshold, orbits);
        write_mag_analysis(&dict, &mag)?;

        // Prototype label (reuse dataset to avoid recomputing symmetry)
        const PROTO_KEYS: &[&str] = &[
            "protostructure_label",
            "prototype_method",
            "prototype_symprec",
        ];
        let pre_proto_count = dict.len();
        if let Some(label) = dataset
            .as_ref()
            .and_then(|ds| self.inner.protostructure_label_from_dataset(ds).ok())
        {
            dict.set_item("protostructure_label", &label)?;
            dict.set_item("prototype_method", "moyo")?;
            dict.set_item("prototype_symprec", symprec)?;
        } else {
            set_none_keys(&dict, PROTO_KEYS)?;
        }
        debug_assert_eq!(
            dict.len() - pre_proto_count,
            PROTO_KEYS.len(),
            "PROTO_KEYS has {} entries but {} keys were written",
            PROTO_KEYS.len(),
            dict.len() - pre_proto_count,
        );

        Ok(dict.unbind())
    }

    // === Prototype labels ===

    /// Get AFLOW-style protostructure label.
    #[pyo3(signature = (symprec = 0.01))]
    fn get_protostructure_label(&self, symprec: f64) -> PyResult<String> {
        self.inner
            .get_protostructure_label(symprec)
            .map_err(ferrox_err)
    }

    /// Point group symbol (e.g. "m-3m", "4/mmm").
    #[pyo3(signature = (symprec = 0.01))]
    fn get_point_group(&self, symprec: f64) -> PyResult<&'static str> {
        let ds = self._dataset(symprec)?;
        let gcc = geometric_crystal_class_from_hall(ds.hall_number).map_err(ferrox_err)?;
        Ok(point_group_symbol(gcc))
    }
}
