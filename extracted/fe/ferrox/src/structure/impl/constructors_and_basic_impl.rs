use crate::composition::Composition;
use crate::element::Element;
use crate::error::{FerroxError, Result, check_positive};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use moyo::base::{Cell as MoyoCell, Lattice as MoyoLattice};
use moyo::data::{HallSymbol, hall_symbol_entry};
use nalgebra::Vector3;
use std::collections::{BTreeMap, HashMap};

use super::Structure;
use super::symmetry_helpers::{
    build_conventional_operations, generate_orbit, resolve_spacegroup,
    validate_lattice_compatibility,
};

impl Structure {
    /// Try to create a new structure from site occupancies.
    pub fn try_new_from_occupancies(
        lattice: Lattice,
        site_occupancies: Vec<SiteOccupancy>,
        frac_coords: Vec<Vector3<f64>>,
    ) -> Result<Self> {
        Self::try_new_from_occupancies_with_properties(
            lattice,
            site_occupancies,
            frac_coords,
            HashMap::new(),
        )
    }

    /// Create a structure with site occupancies and properties.
    /// Uses the lattice's pbc field for periodicity.
    pub fn try_new_from_occupancies_with_properties(
        lattice: Lattice,
        site_occupancies: Vec<SiteOccupancy>,
        frac_coords: Vec<Vector3<f64>>,
        properties: HashMap<String, serde_json::Value>,
    ) -> Result<Self> {
        let pbc = lattice.pbc;
        Self::try_new_full(lattice, site_occupancies, frac_coords, pbc, 0.0, properties)
    }

    /// Full constructor with all fields.
    /// Syncs lattice.pbc with the provided pbc argument.
    pub fn try_new_full(
        mut lattice: Lattice,
        site_occupancies: Vec<SiteOccupancy>,
        frac_coords: Vec<Vector3<f64>>,
        pbc: [bool; 3],
        charge: f64,
        properties: HashMap<String, serde_json::Value>,
    ) -> Result<Self> {
        lattice.pbc = pbc;
        if !charge.is_finite() {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!("charge must be finite, got {charge}"),
            });
        }
        if site_occupancies.len() != frac_coords.len() {
            return Err(FerroxError::InvalidStructure {
                index: 0,
                reason: format!(
                    "site_occupancies and frac_coords must have same length: {} vs {}",
                    site_occupancies.len(),
                    frac_coords.len()
                ),
            });
        }
        // Validate that each site has at least one species (required by dominant_species(),
        // species(), to_moyo_cell(), etc.)
        for (idx, site_occ) in site_occupancies.iter().enumerate() {
            if site_occ.species.is_empty() {
                return Err(FerroxError::InvalidStructure {
                    index: idx,
                    reason: "SiteOccupancy must have at least one species".to_string(),
                });
            }
        }
        Ok(Self {
            lattice,
            site_occupancies,
            frac_coords,
            pbc,
            charge,
            properties,
        })
    }

    /// Try to create a new structure from ordered species (convenience constructor).
    pub fn try_new(
        lattice: Lattice,
        species: Vec<Species>,
        frac_coords: Vec<Vector3<f64>>,
    ) -> Result<Self> {
        Self::try_new_with_properties(lattice, species, frac_coords, HashMap::new())
    }

    /// Create a structure from ordered species with properties (convenience constructor).
    pub fn try_new_with_properties(
        lattice: Lattice,
        species: Vec<Species>,
        frac_coords: Vec<Vector3<f64>>,
        properties: HashMap<String, serde_json::Value>,
    ) -> Result<Self> {
        let site_occupancies = species.into_iter().map(SiteOccupancy::ordered).collect();
        Self::try_new_from_occupancies_with_properties(
            lattice,
            site_occupancies,
            frac_coords,
            properties,
        )
    }

    /// Create a new structure from ordered species (convenience constructor).
    ///
    /// Panics if `species` and `frac_coords` have different lengths. Use
    /// [`Structure::try_new`] for a fallible alternative.
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::structure::Structure;
    /// use ferrox::lattice::Lattice;
    /// use ferrox::species::Species;
    /// use ferrox::element::Element;
    /// use nalgebra::Vector3;
    ///
    /// let structure = Structure::new(
    ///     Lattice::cubic(4.0),
    ///     vec![Species::neutral(Element::Si)],
    ///     vec![Vector3::new(0.0, 0.0, 0.0)],
    /// );
    /// assert_eq!(structure.num_sites(), 1);
    /// ```
    pub fn new(lattice: Lattice, species: Vec<Species>, frac_coords: Vec<Vector3<f64>>) -> Self {
        Self::try_new(lattice, species, frac_coords)
            .expect("species and frac_coords must have same length")
    }

    /// Create a new structure from site occupancies.
    pub fn new_from_occupancies(
        lattice: Lattice,
        site_occupancies: Vec<SiteOccupancy>,
        frac_coords: Vec<Vector3<f64>>,
    ) -> Self {
        Self::try_new_from_occupancies(lattice, site_occupancies, frac_coords)
            .expect("site_occupancies and frac_coords must have same length")
    }

    // === Non-periodic (molecule) constructors ===

    /// Create a non-periodic structure (molecule) from Cartesian coordinates.
    ///
    /// Uses a unit cubic lattice where fractional coords equal Cartesian coords,
    /// ensuring exact coordinate preservation. Sets `pbc = [false, false, false]`.
    pub fn try_new_molecule(
        species: Vec<Species>,
        cart_coords: Vec<Vector3<f64>>,
        charge: f64,
        properties: HashMap<String, serde_json::Value>,
    ) -> Result<Self> {
        let site_occupancies: Vec<SiteOccupancy> =
            species.into_iter().map(SiteOccupancy::ordered).collect();
        Self::try_new_molecule_from_occupancies(site_occupancies, cart_coords, charge, properties)
    }

    /// Create a non-periodic structure (molecule) from site occupancies and Cartesian coordinates.
    ///
    /// Uses an identity lattice (1 Å cubic) so that `frac_coords == cart_coords`.
    /// This ensures exact coordinate preservation through roundtrips.
    ///
    /// Note: For molecules, `frac_coords` may exceed [0, 1) which is intentional -
    /// molecules are non-periodic so coordinate wrapping would be incorrect.
    pub fn try_new_molecule_from_occupancies(
        site_occupancies: Vec<SiteOccupancy>,
        cart_coords: Vec<Vector3<f64>>,
        charge: f64,
        properties: HashMap<String, serde_json::Value>,
    ) -> Result<Self> {
        // Use identity lattice so frac_coords == cart_coords
        let lattice = Lattice::cubic(1.0);
        Self::try_new_full(
            lattice,
            site_occupancies,
            cart_coords, // stored directly as frac_coords
            [false, false, false],
            charge,
            properties,
        )
    }

    // === Periodicity helpers ===

    /// Check if the structure is periodic in any dimension.
    pub fn is_periodic(&self) -> bool {
        self.pbc.iter().any(|&p| p)
    }

    /// Check if the structure is a molecule (non-periodic in all dimensions).
    pub fn is_molecule(&self) -> bool {
        !self.is_periodic()
    }

    /// Set periodic boundary conditions, keeping Structure.pbc and Lattice.pbc in sync.
    ///
    /// Always use this method instead of direct field assignment to prevent desync
    /// between the structure and lattice PBC settings.
    pub fn set_pbc(&mut self, pbc: [bool; 3]) {
        self.pbc = pbc;
        self.lattice.pbc = pbc;
    }

    /// Get the number of sites in the structure.
    pub fn num_sites(&self) -> usize {
        self.site_occupancies.len()
    }

    /// Check if all sites are ordered (single species at full occupancy per site).
    pub fn is_ordered(&self) -> bool {
        self.site_occupancies.iter().all(|so| so.is_ordered())
    }

    /// True if any site contains more than one species (substitutional disorder).
    pub fn has_substitutional_disorder(&self) -> bool {
        self.site_occupancies.iter().any(|so| so.species.len() > 1)
    }

    /// True if any site has total occupancy < 1 - tol (vacancy disorder).
    pub fn has_vacancy_disorder(&self, tol: f64) -> bool {
        self.site_occupancies
            .iter()
            .any(|so| so.total_occupancy() < 1.0 - tol)
    }

    /// Maximum number of distinct species on any single site.
    pub fn max_species_per_site(&self) -> usize {
        self.site_occupancies
            .iter()
            .map(|so| so.species.len())
            .max()
            .unwrap_or(0)
    }

    /// Minimum total occupancy across all sites. Returns 1.0 for empty structures
    /// (vacuously, all zero sites are fully occupied).
    pub fn min_total_occupancy_per_site(&self) -> f64 {
        self.site_occupancies
            .iter()
            .map(|so| so.total_occupancy())
            .reduce(f64::min)
            .unwrap_or(1.0)
    }

    /// Number of sites with disorder (multiple species or partial occupancy).
    pub fn num_disordered_sites(&self, tol: f64) -> usize {
        self.site_occupancies
            .iter()
            .filter(|so| so.species.len() > 1 || so.total_occupancy() < 1.0 - tol)
            .count()
    }

    /// True if any species has an explicit oxidation state annotation.
    pub fn has_oxidation_states(&self) -> bool {
        self.site_occupancies.iter().any(|so| {
            so.species
                .iter()
                .any(|(sp, _)| sp.oxidation_state.is_some())
        })
    }

    /// Atomic site density in sites/ų.
    pub fn atomic_density(&self) -> Option<f64> {
        let vol = self.volume();
        if vol < 1e-12 {
            return None;
        }
        Some(self.num_sites() as f64 / vol)
    }

    /// Volume per atomic site in ų.
    pub fn volume_per_site(&self) -> Option<f64> {
        let vol = self.volume();
        if vol < 1e-12 || self.num_sites() == 0 {
            return None;
        }
        Some(vol / self.num_sites() as f64)
    }

    /// Get the dominant species at each site.
    ///
    /// Note: This allocates a new Vec on each call. For performance-critical
    /// code that iterates once, consider using `site_occupancies` directly.
    pub fn species(&self) -> Vec<&Species> {
        self.site_occupancies
            .iter()
            .map(|so| so.dominant_species())
            .collect()
    }

    /// Get the element composition (oxidation states ignored, weighted by occupancy).
    pub fn composition(&self) -> Composition {
        let mut counts: BTreeMap<Element, f64> = BTreeMap::new();
        for site_occ in &self.site_occupancies {
            for (sp, occ) in &site_occ.species {
                *counts.entry(sp.element).or_insert(0.0) += occ;
            }
        }
        Composition::from_elements(counts)
    }

    /// Get the species composition (preserves oxidation states, weighted by occupancy).
    pub fn species_composition(&self) -> Composition {
        let mut counts: Vec<(Species, f64)> = Vec::new();
        for site_occ in &self.site_occupancies {
            for (sp, occ) in &site_occ.species {
                if let Some(entry) = counts.iter_mut().find(|(s, _)| s == sp) {
                    entry.1 += occ;
                } else {
                    counts.push((*sp, *occ));
                }
            }
        }
        Composition::new(counts)
    }

    /// Get species strings for all sites.
    ///
    /// Returns a vector of human-readable species strings, one per site.
    /// For ordered sites: "Fe" or "Fe2+". For disordered: "Fe:0.5, Co:0.5"
    /// (sorted by electronegativity, matching pymatgen).
    pub fn species_strings(&self) -> Vec<String> {
        self.site_occupancies
            .iter()
            .map(|so| so.species_string())
            .collect()
    }

    /// Get Cartesian coordinates.
    pub fn cart_coords(&self) -> Vec<Vector3<f64>> {
        self.lattice.get_cartesian_coords(&self.frac_coords)
    }

    /// Convert to moyo::base::Cell for symmetry analysis (uses dominant species).
    pub fn to_moyo_cell(&self) -> MoyoCell {
        // ferrox stores lattice vectors as rows, and moyo::Lattice::new expects that
        // same row-vector convention before transposing into its internal column storage.
        let moyo_lattice = MoyoLattice::new(*self.lattice.matrix());
        let positions: Vec<Vector3<f64>> = self.frac_coords.clone();
        let numbers: Vec<i32> = self
            .site_occupancies
            .iter()
            .map(|so| so.dominant_species().element.atomic_number() as i32)
            .collect();
        MoyoCell::new(moyo_lattice, positions, numbers)
    }

    /// Create Structure from moyo::base::Cell (creates ordered sites).
    pub fn from_moyo_cell(cell: &MoyoCell) -> Result<Self> {
        // moyo stores basis vectors as columns in `cell.lattice.basis`, while ferrox
        // stores them as rows, so transpose when converting back.
        let lattice = Lattice::new(cell.lattice.basis.transpose());
        let site_occupancies: Vec<SiteOccupancy> = cell
            .numbers
            .iter()
            .enumerate()
            .map(|(idx, &n)| {
                let z = u8::try_from(n).ok().filter(|&z| z > 0 && z <= 118);
                let elem = z.and_then(Element::from_atomic_number).ok_or_else(|| {
                    FerroxError::InvalidStructure {
                        index: idx,
                        reason: format!("Invalid atomic number: {n}"),
                    }
                })?;
                Ok(SiteOccupancy::ordered(Species::neutral(elem)))
            })
            .collect::<Result<Vec<_>>>()?;
        let frac_coords = cell.positions.clone();
        Structure::try_new_from_occupancies(lattice, site_occupancies, frac_coords)
    }

    /// Create a structure from a space group, lattice, asymmetric-unit species and
    /// fractional coordinates. All symmetry-equivalent sites are generated by applying
    /// the space group operations.
    ///
    /// # Arguments
    ///
    /// * `sg` - Space group as ITA number (1-230) or Hermann-Mauguin symbol (e.g. "Fm-3m")
    /// * `lattice` - The lattice for the structure
    /// * `species` - Species for each symmetrically distinct site
    /// * `coords` - Fractional coordinates of each symmetrically distinct site
    /// * `tol` - Tolerance for deduplicating equivalent sites (default: 1e-5)
    ///
    /// # Examples
    ///
    /// ```
    /// use ferrox::structure::Structure;
    /// use ferrox::lattice::Lattice;
    /// use ferrox::species::{Species, SiteOccupancy};
    /// use ferrox::element::Element;
    /// use nalgebra::Vector3;
    ///
    /// // Build FCC copper (Fm-3m, 1 atom in asymmetric unit → 4 in conventional cell)
    /// let structure = Structure::from_spacegroup(
    ///     "Fm-3m",
    ///     Lattice::cubic(3.61),
    ///     vec![SiteOccupancy::ordered(Species::neutral(Element::Cu))],
    ///     vec![Vector3::new(0.0, 0.0, 0.0)],
    ///     None,
    /// ).unwrap();
    /// assert_eq!(structure.num_sites(), 4);
    /// ```
    pub fn from_spacegroup(
        sg: &str,
        lattice: Lattice,
        species: Vec<SiteOccupancy>,
        coords: Vec<Vector3<f64>>,
        tol: Option<f64>,
    ) -> Result<Self> {
        if species.len() != coords.len() {
            return Err(FerroxError::InvalidArgument {
                reason: format!(
                    "species and coords must have same length: {} vs {}",
                    species.len(),
                    coords.len()
                ),
            });
        }

        let tol = tol.unwrap_or(1e-5);
        check_positive(tol, "tol")?;
        let hall_number = resolve_spacegroup(sg)?;

        // Validate lattice compatibility with space group
        let entry = hall_symbol_entry(hall_number).ok_or_else(|| FerroxError::InvalidArgument {
            reason: format!("No Hall entry for hall number {hall_number}"),
        })?;
        validate_lattice_compatibility(&lattice, entry.number, entry.centering)?;

        let hall_sym =
            HallSymbol::new(entry.hall_symbol).ok_or_else(|| FerroxError::InvalidArgument {
                reason: format!(
                    "Failed to parse Hall symbol '{}' for hall number {hall_number}",
                    entry.hall_symbol
                ),
            })?;

        // Build all conventional cell operations using the same algorithm as moyopy:
        // For each centering lattice point c and each coset representative (R, t),
        // create operation (R, (c + t) mod 1).
        let coset_ops = hall_sym.traverse();
        let lattice_points = hall_sym.centering.lattice_points();
        let full_ops = build_conventional_operations(&coset_ops, &lattice_points);

        let mut all_species = Vec::new();
        let mut all_coords = Vec::new();

        for (sp, basis_coord) in species.into_iter().zip(coords.into_iter()) {
            let orbit = generate_orbit(&basis_coord, &full_ops, tol);
            all_species.extend(std::iter::repeat_n(sp, orbit.len()));
            all_coords.extend(orbit);
        }

        Structure::try_new_from_occupancies(lattice, all_species, all_coords)
    }

    /// Create a structure from a named prototype (e.g. "fcc", "rocksalt", "perovskite").
    ///
    /// This is a convenience wrapper around `from_spacegroup` with pre-defined space groups
    /// and Wyckoff positions for common crystal structure types.
    ///
    /// # Supported prototypes
    ///
    /// | Name | Required species | Required lattice params |
    /// |------|-----------------|------------------------|
    /// | `sc` | 1 | `a` |
    /// | `fcc` | 1 | `a` |
    /// | `bcc` | 1 | `a` |
    /// | `hcp` | 1 | `a`, `c` |
    /// | `diamond` | 1 | `a` |
    /// | `rocksalt` | 2 | `a` |
    /// | `perovskite` | 3 | `a` |
    /// | `cscl` | 2 | `a` |
    /// | `fluorite` | 2 | `a` |
    /// | `antifluorite` | 2 | `a` |
    /// | `zincblende` | 2 | `a` |
    /// | `wurtzite` | 2 | `a`, `c` |
    pub fn from_prototype(
        prototype: &str,
        species: Vec<SiteOccupancy>,
        a: f64,
        b: Option<f64>,
        c: Option<f64>,
    ) -> Result<Self> {
        check_positive(a, "a")?;
        if let Some(c_val) = c {
            check_positive(c_val, "c")?;
        }
        if b.is_some() {
            return Err(FerroxError::InvalidArgument {
                reason: format!("Prototype '{prototype}' does not use lattice parameter b"),
            });
        }

        let proto = prototype.to_lowercase();

        let (sg, lattice, coords) = match proto.as_str() {
            "sc" => ("Pm-3m", Lattice::cubic(a), vec![Vector3::zeros()]),
            "fcc" => ("Fm-3m", Lattice::cubic(a), vec![Vector3::zeros()]),
            "bcc" => ("Im-3m", Lattice::cubic(a), vec![Vector3::zeros()]),
            "hcp" => {
                let c_val = c.ok_or_else(|| FerroxError::InvalidArgument {
                    reason: "hcp prototype requires lattice parameter c".to_string(),
                })?;
                (
                    "P6_3/mmc",
                    Lattice::hexagonal(a, c_val),
                    vec![Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.25)],
                )
            }
            "diamond" => ("Fd-3m", Lattice::cubic(a), vec![Vector3::zeros()]),
            "rocksalt" => (
                "Fm-3m",
                Lattice::cubic(a),
                vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
            ),
            "perovskite" => (
                "Pm-3m",
                Lattice::cubic(a),
                vec![
                    Vector3::zeros(),
                    Vector3::new(0.5, 0.5, 0.5),
                    Vector3::new(0.5, 0.5, 0.0),
                ],
            ),
            "cscl" => (
                "Pm-3m",
                Lattice::cubic(a),
                vec![Vector3::zeros(), Vector3::new(0.5, 0.5, 0.5)],
            ),
            "fluorite" | "caf2" => (
                "Fm-3m",
                Lattice::cubic(a),
                vec![Vector3::zeros(), Vector3::new(0.25, 0.25, 0.25)],
            ),
            "antifluorite" => (
                "Fm-3m",
                Lattice::cubic(a),
                vec![Vector3::new(0.25, 0.25, 0.25), Vector3::zeros()],
            ),
            "zincblende" => (
                "F-43m",
                Lattice::cubic(a),
                vec![Vector3::zeros(), Vector3::new(0.25, 0.25, 0.25)],
            ),
            "wurtzite" => {
                let c_val = c.ok_or_else(|| FerroxError::InvalidArgument {
                    reason: "wurtzite prototype requires lattice parameter c".to_string(),
                })?;
                (
                    "P6_3mc",
                    Lattice::hexagonal(a, c_val),
                    vec![
                        Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.0),
                        Vector3::new(1.0 / 3.0, 2.0 / 3.0, 0.375),
                    ],
                )
            }
            _ => {
                return Err(FerroxError::InvalidArgument {
                    reason: format!(
                        "Unknown prototype '{prototype}'. Supported: sc, fcc, bcc, hcp, diamond, \
                         rocksalt, perovskite, cscl, fluorite, antifluorite, zincblende, wurtzite"
                    ),
                });
            }
        };

        let uses_c = matches!(proto.as_str(), "hcp" | "wurtzite");
        if !uses_c && c.is_some() {
            return Err(FerroxError::InvalidArgument {
                reason: format!("Prototype '{prototype}' does not use lattice parameter c"),
            });
        }

        if species.len() != coords.len() {
            return Err(FerroxError::InvalidArgument {
                reason: format!(
                    "Prototype '{prototype}' requires {} species, got {}",
                    coords.len(),
                    species.len()
                ),
            });
        }

        Self::from_spacegroup(sg, lattice, species, coords, None)
    }
}
