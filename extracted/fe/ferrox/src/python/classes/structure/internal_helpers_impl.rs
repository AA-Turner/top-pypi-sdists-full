use std::sync::{Arc, Mutex};

use moyo::MoyoDataset;
use pyo3::prelude::*;

use crate::python::helpers::parse_element;
use crate::structure::spacegroup_type_from_number;

use super::{PyStructure, ferrox_err};

// === Internal helpers (not exposed to Python) ===

impl PyStructure {
    /// Wrap a Rust Structure into a PyStructure (fresh symmetry cache).
    pub(crate) fn wrap(inner: crate::structure::Structure) -> Self {
        Self {
            inner,
            cached_dataset: Mutex::new(None),
        }
    }

    pub(crate) fn wrap_many(structures: Vec<crate::structure::Structure>) -> Vec<Self> {
        structures.into_iter().map(Self::wrap).collect()
    }

    pub(crate) fn parse_neutral_species_list(
        species_symbols: &[String],
    ) -> PyResult<Vec<crate::species::Species>> {
        species_symbols
            .iter()
            .map(|symbol| Ok(crate::species::Species::neutral(parse_element(symbol)?)))
            .collect()
    }

    /// Get or compute the cached symmetry dataset (cheap Arc clone on hit).
    pub(crate) fn _dataset(&self, symprec: f64) -> PyResult<Arc<MoyoDataset>> {
        let mut cache = self.cached_dataset.lock().map_err(ferrox_err)?;
        if let Some((cached_prec, ref ds)) = *cache
            && (cached_prec - symprec).abs() < 1e-12
        {
            return Ok(Arc::clone(ds));
        }
        let ds = Arc::new(
            self.inner
                .get_symmetry_dataset(symprec)
                .map_err(ferrox_err)?,
        );
        *cache = Some((symprec, Arc::clone(&ds)));
        Ok(ds)
    }

    /// Look up SpacegroupTypeInfo from the cached dataset.
    pub(crate) fn _spg_type_info(
        &self,
        symprec: f64,
    ) -> PyResult<crate::structure::SpacegroupTypeInfo> {
        let ds = self._dataset(symprec)?;
        spacegroup_type_from_number(ds.number).map_err(ferrox_err)
    }
}
