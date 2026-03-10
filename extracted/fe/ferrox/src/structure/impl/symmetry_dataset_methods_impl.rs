use crate::error::{FerroxError, Result};
use moyo::MoyoDataset;
use moyo::base::AngleTolerance;
use moyo::data::{GeometricCrystalClass, Setting};
use nalgebra::{Matrix3, Vector3};
use std::collections::{HashMap, HashSet};

use super::symmetry_helpers::{
    geometric_crystal_class_from_hall, laue_group_from_point_group, moyo_ops_to_arrays,
    point_group_symbol, spacegroup_to_crystal_system, validate_symprec,
};
use super::{Structure, SymmetryOperation, WyckoffSite};

impl Structure {
    /// Get the primitive cell using moyo symmetry analysis.
    pub fn get_primitive(&self, symprec: f64) -> Result<Self> {
        validate_symprec(symprec)?;
        let moyo_cell = self.to_moyo_cell();
        let dataset = MoyoDataset::new(
            &moyo_cell,
            symprec,
            AngleTolerance::Default,
            Setting::Standard,
            false,
        )
        .map_err(|e| FerroxError::MoyoError {
            index: 0,
            reason: format!("{e:?}"),
        })?;
        Self::from_moyo_cell(&dataset.prim_std_cell)
    }

    /// Get the conventional (standardized) cell using moyo symmetry analysis.
    pub fn get_conventional_structure(&self, symprec: f64) -> Result<Self> {
        validate_symprec(symprec)?;
        let moyo_cell = self.to_moyo_cell();
        let dataset = MoyoDataset::new(
            &moyo_cell,
            symprec,
            AngleTolerance::Default,
            Setting::Standard,
            false,
        )
        .map_err(|e| FerroxError::MoyoError {
            index: 0,
            reason: format!("{e:?}"),
        })?;
        Self::from_moyo_cell(&dataset.std_cell)
    }

    /// Get the spacegroup number using moyo.
    pub fn get_spacegroup_number(&self, symprec: f64) -> Result<i32> {
        // symprec validated by get_symmetry_dataset
        Ok(self.get_symmetry_dataset(symprec)?.number)
    }

    /// Get the full symmetry dataset from moyo.
    ///
    /// This is more efficient when you need multiple symmetry properties,
    /// as it only runs the symmetry analysis once.
    pub fn get_symmetry_dataset(&self, symprec: f64) -> Result<MoyoDataset> {
        validate_symprec(symprec)?;
        if self.num_sites() == 0 {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: "Cannot compute symmetry for empty structure (0 sites)".to_string(),
            });
        }
        let moyo_cell = self.to_moyo_cell();
        MoyoDataset::new(
            &moyo_cell,
            symprec,
            AngleTolerance::Default,
            Setting::Standard,
            false,
        )
        .map_err(|e| FerroxError::MoyoError {
            index: 0,
            reason: format!("{e:?}"),
        })
    }

    /// Get the Hermann-Mauguin spacegroup symbol (e.g., "F m -3 m", "P 2_1/c").
    ///
    /// Note: Returns space-separated tokens as provided by the underlying
    /// symmetry library (moyo). For condensed symbols, post-process by removing spaces.
    pub fn get_spacegroup_symbol(&self, symprec: f64) -> Result<String> {
        Ok(self.get_symmetry_dataset(symprec)?.hm_symbol)
    }

    /// Get the Hall number (1-530) identifying the specific spacegroup setting.
    pub fn get_hall_number(&self, symprec: f64) -> Result<i32> {
        Ok(self.get_symmetry_dataset(symprec)?.hall_number)
    }

    /// Get the Pearson symbol (e.g., "cF8" for FCC Cu).
    ///
    /// The Pearson symbol encodes the crystal system, centering type, and
    /// number of atoms in the conventional cell.
    pub fn get_pearson_symbol(&self, symprec: f64) -> Result<String> {
        Ok(self.get_symmetry_dataset(symprec)?.pearson_symbol)
    }

    /// Get Wyckoff letters for each site in the structure.
    ///
    /// Wyckoff positions describe the site symmetry and multiplicity of each
    /// atomic position. Sites with the same letter have equivalent positions
    /// under the space group symmetry.
    pub fn get_wyckoff_letters(&self, symprec: f64) -> Result<Vec<char>> {
        Ok(self.get_symmetry_dataset(symprec)?.wyckoffs)
    }

    /// Get site symmetry symbols for each site (e.g., "m..", "-1", "4mm").
    ///
    /// The site symmetry describes the point group symmetry at each atomic site,
    /// oriented with respect to the standardized cell.
    pub fn get_site_symmetry_symbols(&self, symprec: f64) -> Result<Vec<String>> {
        Ok(self.get_symmetry_dataset(symprec)?.site_symmetry_symbols)
    }

    /// Number of symmetry operations in the structure's space group.
    pub fn num_symmetry_operations(&self, symprec: f64) -> Result<usize> {
        Ok(self.get_symmetry_dataset(symprec)?.operations.len())
    }

    /// Number of symmetry-inequivalent sites (Wyckoff orbits).
    pub fn num_unique_sites(&self, symprec: f64) -> Result<usize> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        Ok(dataset.orbits.iter().collect::<HashSet<_>>().len())
    }

    /// Histogram of Wyckoff letters: maps letter to count of sites with that letter.
    pub fn wyckoff_histogram(&self, symprec: f64) -> Result<HashMap<char, usize>> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        let mut hist = HashMap::new();
        for wyk in &dataset.wyckoffs {
            *hist.entry(*wyk).or_insert(0) += 1;
        }
        Ok(hist)
    }

    /// Get Wyckoff site information for all sites in the structure.
    ///
    /// Uses symmetry analysis to identify equivalent sites and their
    /// Wyckoff positions within the space group.
    ///
    /// **Note:** The returned multiplicities and labels are computed relative to
    /// the **input cell**, not the standardized/conventional cell. For example,
    /// a primitive cell will show multiplicities of 1 for sites that would have
    /// higher multiplicity in the conventional cell. To get conventional Wyckoff
    /// multiplicities, first transform the structure to its conventional cell.
    ///
    /// # Arguments
    ///
    /// * `symprec` - Symmetry precision (typical values: 0.01 to 0.1)
    ///
    /// # Returns
    ///
    /// Vector of `WyckoffSite` for each site, containing the Wyckoff label
    /// (input-cell multiplicity + letter), site symmetry, and representative coordinates.
    pub fn get_wyckoff_sites(&self, symprec: f64) -> Result<Vec<WyckoffSite>> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        let orbits = &dataset.orbits;
        let wyckoffs = &dataset.wyckoffs;
        let site_symmetry = &dataset.site_symmetry_symbols;

        // Count multiplicity for each unique orbit
        let mut orbit_multiplicity: HashMap<usize, usize> = HashMap::new();
        for &orbit_idx in orbits {
            *orbit_multiplicity.entry(orbit_idx).or_insert(0) += 1;
        }

        // Build WyckoffSite for each site
        let sites: Vec<WyckoffSite> = (0..self.num_sites())
            .map(|idx| {
                let orbit_idx = orbits[idx];
                let multiplicity = orbit_multiplicity[&orbit_idx];
                let wyckoff_letter = wyckoffs[idx];
                let label = format!("{multiplicity}{wyckoff_letter}");
                WyckoffSite {
                    label,
                    multiplicity,
                    site_symmetry: site_symmetry[idx].clone(),
                    representative_coords: self.frac_coords[orbit_idx],
                }
            })
            .collect();

        Ok(sites)
    }

    /// Get symmetry operations in the input cell.
    ///
    /// Returns a vector of (rotation_matrix, translation_vector) pairs.
    /// The rotation is a 3x3 integer matrix in fractional coordinates,
    /// and the translation is a 3-vector in fractional coordinates.
    ///
    /// A symmetry operation transforms a point r to: R @ r + t
    pub fn get_symmetry_operations(&self, symprec: f64) -> Result<Vec<SymmetryOperation>> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        Ok(moyo_ops_to_arrays(&dataset.operations))
    }

    /// Get equivalent sites (crystallographic orbits).
    ///
    /// Returns a vector where orbits[i] is the index of the representative site
    /// that site i is equivalent to. Sites with the same orbit index are
    /// related by space group symmetry.
    ///
    /// For example, orbits=[0, 0, 2, 2, 2, 2] means sites 0-1 are equivalent
    /// to site 0, and sites 2-5 are equivalent to site 2.
    pub fn get_equivalent_sites(&self, symprec: f64) -> Result<Vec<usize>> {
        Ok(self.get_symmetry_dataset(symprec)?.orbits)
    }

    /// Get the crystal system based on the spacegroup number.
    ///
    /// Returns one of: "triclinic", "monoclinic", "orthorhombic",
    /// "tetragonal", "trigonal", "hexagonal", "cubic".
    pub fn get_crystal_system(&self, symprec: f64) -> Result<String> {
        Ok(spacegroup_to_crystal_system(self.get_symmetry_dataset(symprec)?.number).to_string())
    }

    /// Get the geometric crystal class (point group enum) for this structure.
    pub fn get_geometric_crystal_class(&self, symprec: f64) -> Result<GeometricCrystalClass> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        geometric_crystal_class_from_hall(dataset.hall_number)
    }

    /// Get the point group (geometric crystal class) symbol.
    ///
    /// Returns the Hermann-Mauguin symbol for the point group, e.g. "m-3m", "-1",
    /// "mmm", "4mm", "32". Uses the ITA primary symbol convention from moyo
    /// (e.g. "-42m" for D2d, "-6m2" for D3h). Note that pymatgen/spglib may use
    /// the alternative setting ("-4m2", "-62m") -- both are valid ITA orientations.
    pub fn get_point_group(&self, symprec: f64) -> Result<&'static str> {
        Ok(point_group_symbol(
            self.get_geometric_crystal_class(symprec)?,
        ))
    }

    /// Get the Laue group symbol.
    ///
    /// The Laue group is the point group augmented with inversion symmetry.
    /// Returns the Hermann-Mauguin symbol, e.g. "m-3m", "-1", "mmm", "4/mmm".
    pub fn get_laue_group(&self, symprec: f64) -> Result<&'static str> {
        Ok(laue_group_from_point_group(
            self.get_geometric_crystal_class(symprec)?,
        ))
    }

    /// Get the ITA-standardized structure (conventional or primitive).
    ///
    /// Returns the structure in the standard ITA setting with proper origin
    /// choice, plus the transformation matrix from the input cell.
    ///
    /// If `primitive` is true, returns the primitive standardized cell;
    /// otherwise returns the conventional standardized cell.
    pub fn get_standardized_structure(
        &self,
        symprec: f64,
        primitive: bool,
    ) -> Result<(Self, Matrix3<f64>)> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        let (cell, linear) = if primitive {
            (&dataset.prim_std_cell, &dataset.prim_std_linear)
        } else {
            (&dataset.std_cell, &dataset.std_linear)
        };
        let struc = Self::from_moyo_cell(cell)?;
        Ok((struc, *linear))
    }

    /// Symmetrize the structure by averaging equivalent atomic positions.
    ///
    /// Identifies symmetry-equivalent sites and averages their fractional
    /// coordinates to enforce exact space group symmetry. Useful for cleaning
    /// up DFT-relaxed structures.
    pub fn get_symmetrized_structure(&self, symprec: f64) -> Result<Self> {
        let dataset = self.get_symmetry_dataset(symprec)?;
        let orbits = &dataset.orbits;
        let operations = &dataset.operations;

        let mut averaged_coords = self.frac_coords.clone();

        // Group sites by orbit representative
        let mut orbit_groups: HashMap<usize, Vec<usize>> = HashMap::new();
        for (site_idx, &orbit_rep) in orbits.iter().enumerate() {
            orbit_groups.entry(orbit_rep).or_default().push(site_idx);
        }

        // For each orbit, apply all operations to the representative and average
        let lat_mat = self.lattice.matrix().transpose();
        for (&rep_idx, site_indices) in &orbit_groups {
            if site_indices.len() <= 1 {
                continue;
            }
            let rep_coord = self.frac_coords[rep_idx];
            let mut sym_coords: HashMap<usize, Vec<Vector3<f64>>> = HashMap::new();

            for op in operations.iter() {
                let rot = op.rotation.map(|e| e as f64);
                let mapped = rot * rep_coord + op.translation;
                for &site_idx in site_indices {
                    let diff = mapped - self.frac_coords[site_idx];
                    let wrapped = Vector3::new(
                        diff.x - diff.x.round(),
                        diff.y - diff.y.round(),
                        diff.z - diff.z.round(),
                    );
                    // Convert fractional diff to Cartesian for proper Å comparison
                    let cart_diff = lat_mat * wrapped;
                    if cart_diff.norm() < symprec {
                        sym_coords.entry(site_idx).or_default().push(mapped);
                        break;
                    }
                }
            }

            // Average mapped coordinates for each site (PBC-aware)
            for (&site_idx, coords) in &sym_coords {
                if coords.is_empty() {
                    continue;
                }
                let ref_coord = coords[0];
                let mut diff_sum = Vector3::zeros();
                for coord in &coords[1..] {
                    let mut diff = coord - ref_coord;
                    diff.x -= diff.x.round();
                    diff.y -= diff.y.round();
                    diff.z -= diff.z.round();
                    diff_sum += diff;
                }
                let avg = ref_coord + diff_sum / coords.len() as f64;
                averaged_coords[site_idx] = Vector3::new(
                    avg.x - avg.x.floor(),
                    avg.y - avg.y.floor(),
                    avg.z - avg.z.floor(),
                );
            }
        }

        Structure::try_new_from_occupancies(
            self.lattice.clone(),
            self.site_occupancies.clone(),
            averaged_coords,
        )
    }

    /// Get all site indices that are symmetry-equivalent to the given site.
    pub fn get_symmetry_equivalent_sites(
        &self,
        site_idx: usize,
        symprec: f64,
    ) -> Result<Vec<usize>> {
        if site_idx >= self.num_sites() {
            return Err(FerroxError::InvalidStructure {
                index: site_idx,
                reason: format!(
                    "Site index {site_idx} out of bounds (num_sites={})",
                    self.num_sites()
                ),
            });
        }
        let orbits = self.get_equivalent_sites(symprec)?;
        let target_orbit = orbits[site_idx];
        Ok(orbits
            .iter()
            .enumerate()
            .filter(|&(_, &orbit)| orbit == target_orbit)
            .map(|(idx, _)| idx)
            .collect())
    }
}
