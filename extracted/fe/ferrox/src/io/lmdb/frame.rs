//! Training frame data model for ML interatomic potentials.
//!
//! [`TrainingFrame`] is a streamlined representation of an atomic configuration
//! with typed ML-specific fields (energy, forces, stress). It is intentionally
//! simpler than [`Structure`](crate::structure::Structure) -- no oxidation states,
//! no disordered sites, no fractional coordinates.

use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::lattice::Lattice;
use crate::species::{SiteOccupancy, Species};
use crate::structure::Structure;
use nalgebra::{Matrix3, Vector3};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// An atomic configuration with typed ML training labels.
///
/// Stores positions in Cartesian coordinates (angstroms), energy in eV,
/// forces in eV/A, and stress in Voigt notation (eV/A^3).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct TrainingFrame {
    /// Atomic numbers for each atom.
    pub atomic_numbers: Vec<u8>,
    /// Cartesian positions in angstroms, one `[x, y, z]` per atom.
    pub positions: Vec<[f64; 3]>,
    /// Lattice vectors as a row-major 3x3 matrix, `None` for non-periodic systems.
    pub cell: Option<[[f64; 3]; 3]>,
    /// Periodic boundary conditions per axis.
    pub pbc: [bool; 3],
    /// Total energy in eV.
    pub energy: Option<f64>,
    /// Per-atom forces in eV/A, one `[fx, fy, fz]` per atom.
    pub forces: Option<Vec<[f64; 3]>>,
    /// Stress tensor in Voigt notation `[xx, yy, zz, yz, xz, xy]`, units eV/A^3.
    pub stress: Option<[f64; 6]>,
    /// Total system charge.
    pub charge: Option<f64>,
    /// Per-atom magnetic moments.
    pub magnetic_moments: Option<Vec<f64>>,
    /// Arbitrary additional properties.
    pub properties: HashMap<String, serde_json::Value>,
}

impl TrainingFrame {
    /// Number of atoms in this frame.
    pub fn num_atoms(&self) -> usize {
        self.atomic_numbers.len()
    }

    /// Validate internal consistency (positions length matches atomic_numbers, etc.).
    ///
    /// Called automatically by the Python constructor. Should also be called after
    /// manual construction or when building frames from untrusted/external data.
    pub fn validate(&self) -> Result<()> {
        let n_atoms = self.atomic_numbers.len();
        let check = |field_name: &str, field_len: usize| -> Result<()> {
            if field_len != n_atoms {
                return Err(FerroxError::InvalidArgument {
                    reason: format!(
                        "{field_name} length ({field_len}) != atomic_numbers length ({n_atoms})"
                    ),
                });
            }
            Ok(())
        };
        check("positions", self.positions.len())?;
        if let Some(ref forces) = self.forces {
            check("forces", forces.len())?;
        }
        if let Some(ref mag_mom) = self.magnetic_moments {
            check("magnetic_moments", mag_mom.len())?;
        }
        for &z in &self.atomic_numbers {
            if Element::from_atomic_number(z).is_none() {
                return Err(FerroxError::InvalidArgument {
                    reason: format!("invalid atomic number: {z}"),
                });
            }
        }
        if self.cell.is_none() && self.pbc.iter().any(|&p| p) {
            return Err(FerroxError::PbcWithoutCell);
        }
        Ok(())
    }
}

/// Extract a JSON array of 3-vectors (e.g. forces) from a serde_json::Value.
/// Returns `None` if the value isn't an array or any entry is malformed.
fn json_to_vec3_array(val: &serde_json::Value) -> Option<Vec<[f64; 3]>> {
    val.as_array()?.iter().map(json_to_f64_array::<3>).collect()
}

/// Extract a fixed-length f64 array from a JSON array.
fn json_to_f64_array<const N: usize>(val: &serde_json::Value) -> Option<[f64; N]> {
    let arr = val.as_array()?;
    if arr.len() != N {
        return None;
    }
    let mut result = [0.0; N];
    for (idx, item) in arr.iter().enumerate() {
        result[idx] = item.as_f64()?;
    }
    Some(result)
}

/// ML-specific property keys that are promoted to typed fields on TrainingFrame.
const ML_PROPERTY_KEYS: [&str; 4] = ["energy", "forces", "stress", "magnetic_moments"];

impl From<&Structure> for TrainingFrame {
    /// Convert a [`Structure`] to a [`TrainingFrame`].
    ///
    /// - Lattice matrix -> `cell`
    /// - Dominant species at each site -> `atomic_numbers`
    /// - Fractional coords -> Cartesian `positions`
    /// - `"energy"`, `"forces"`, `"stress"` extracted from `Structure.properties`
    /// - Remaining properties passed through
    fn from(structure: &Structure) -> Self {
        let atomic_numbers = structure
            .species()
            .iter()
            .map(|sp| sp.element.atomic_number())
            .collect();

        let positions = structure
            .cart_coords()
            .iter()
            .map(|coord| [coord.x, coord.y, coord.z])
            .collect();

        let mat = structure.lattice.matrix();
        let cell = Some(std::array::from_fn(|row| {
            std::array::from_fn(|col| mat[(row, col)])
        }));

        let energy = structure
            .properties
            .get("energy")
            .and_then(|val| val.as_f64());
        let forces = structure
            .properties
            .get("forces")
            .and_then(json_to_vec3_array);
        let stress = structure
            .properties
            .get("stress")
            .and_then(json_to_f64_array::<6>);
        let magnetic_moments = structure
            .properties
            .get("magnetic_moments")
            .and_then(|val| {
                val.as_array()?
                    .iter()
                    .map(|v| v.as_f64())
                    .collect::<Option<Vec<_>>>()
            });

        let charge = if structure.charge.abs() > 1e-10 {
            Some(structure.charge)
        } else {
            None
        };

        let properties = structure
            .properties
            .iter()
            .filter(|(key, _)| !ML_PROPERTY_KEYS.contains(&key.as_str()))
            .map(|(key, val)| (key.clone(), val.clone()))
            .collect();

        let frame = TrainingFrame {
            atomic_numbers,
            positions,
            cell,
            pbc: structure.pbc,
            energy,
            forces,
            stress,
            charge,
            magnetic_moments,
            properties,
        };
        debug_assert!(
            frame.validate().is_ok(),
            "Structure -> TrainingFrame produced invalid frame: {:?}",
            frame.validate().unwrap_err()
        );
        frame
    }
}

impl From<Structure> for TrainingFrame {
    fn from(structure: Structure) -> Self {
        TrainingFrame::from(&structure)
    }
}

impl TryFrom<&TrainingFrame> for Structure {
    type Error = FerroxError;

    /// Convert a [`TrainingFrame`] back to a [`Structure`].
    ///
    /// Forces, stress, and magnetic moments are stored in `Structure.properties`
    /// as JSON arrays (matching the extXYZ convention).
    fn try_from(frame: &TrainingFrame) -> Result<Self> {
        let cell = frame.cell.ok_or(FerroxError::InvalidArgument {
            reason: "TrainingFrame has no cell; cannot convert to Structure".to_string(),
        })?;

        let lattice = Lattice::new(Matrix3::from_row_slice(cell.as_flattened()));

        let species: Vec<Species> = frame
            .atomic_numbers
            .iter()
            .map(|&z| {
                Element::from_atomic_number(z)
                    .ok_or_else(|| FerroxError::InvalidArgument {
                        reason: format!("Unknown atomic number: {z}"),
                    })
                    .map(Species::neutral)
            })
            .collect::<Result<_>>()?;

        let cart_coords: Vec<Vector3<f64>> = frame
            .positions
            .iter()
            .map(|pos| Vector3::new(pos[0], pos[1], pos[2]))
            .collect();
        let frac_coords = lattice.get_fractional_coords(&cart_coords);

        let mut properties = frame.properties.clone();
        if let Some(energy) = frame.energy {
            properties.insert("energy".to_string(), serde_json::json!(energy));
        }
        if let Some(ref forces) = frame.forces {
            properties.insert("forces".to_string(), serde_json::json!(forces));
        }
        if let Some(stress) = frame.stress {
            properties.insert("stress".to_string(), serde_json::json!(stress));
        }
        if let Some(ref mag_mom) = frame.magnetic_moments {
            properties.insert("magnetic_moments".to_string(), serde_json::json!(mag_mom));
        }

        Structure::try_new_full(
            lattice,
            species.into_iter().map(SiteOccupancy::ordered).collect(),
            frac_coords,
            frame.pbc,
            frame.charge.unwrap_or(0.0),
            properties,
        )
    }
}

impl TryFrom<TrainingFrame> for Structure {
    type Error = FerroxError;

    fn try_from(frame: TrainingFrame) -> Result<Self> {
        Structure::try_from(&frame)
    }
}

// === rkyv-archivable representation ===

/// Internal representation of a training frame for rkyv zero-copy serialization.
///
/// Identical to [`TrainingFrame`] except `properties` is stored as pre-serialized
/// JSON bytes (`Vec<u8>`), since `serde_json::Value` doesn't implement rkyv's
/// `Archive` trait.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
#[rkyv(derive(Debug))]
pub struct RkyvFrame {
    pub atomic_numbers: Vec<u8>,
    pub positions: Vec<[f64; 3]>,
    pub cell: Option<[[f64; 3]; 3]>,
    pub pbc: [bool; 3],
    pub energy: Option<f64>,
    pub forces: Option<Vec<[f64; 3]>>,
    pub stress: Option<[f64; 6]>,
    pub charge: Option<f64>,
    pub magnetic_moments: Option<Vec<f64>>,
    pub properties_json: Vec<u8>,
}

impl From<&TrainingFrame> for RkyvFrame {
    fn from(frame: &TrainingFrame) -> Self {
        let properties_json = serde_json::to_vec(&frame.properties).unwrap_or_else(|err| {
            tracing::warn!("failed to serialize TrainingFrame properties: {err}");
            b"{}".to_vec()
        });
        RkyvFrame {
            atomic_numbers: frame.atomic_numbers.clone(),
            positions: frame.positions.clone(),
            cell: frame.cell,
            pbc: frame.pbc,
            energy: frame.energy,
            forces: frame.forces.clone(),
            stress: frame.stress,
            charge: frame.charge,
            magnetic_moments: frame.magnetic_moments.clone(),
            properties_json,
        }
    }
}

impl From<RkyvFrame> for TrainingFrame {
    fn from(rkyv_frame: RkyvFrame) -> Self {
        let properties =
            serde_json::from_slice(&rkyv_frame.properties_json).unwrap_or_else(|err| {
                tracing::warn!("failed to deserialize RkyvFrame properties_json: {err}");
                HashMap::new()
            });
        TrainingFrame {
            atomic_numbers: rkyv_frame.atomic_numbers,
            positions: rkyv_frame.positions,
            cell: rkyv_frame.cell,
            pbc: rkyv_frame.pbc,
            energy: rkyv_frame.energy,
            forces: rkyv_frame.forces,
            stress: rkyv_frame.stress,
            charge: rkyv_frame.charge,
            magnetic_moments: rkyv_frame.magnetic_moments,
            properties,
        }
    }
}
