//! Brillouin zone WASM bindings.

use wasm_bindgen::prelude::*;

use crate::analysis::brillouin;
use crate::wasm_types::{
    JsBrillouinFace, JsBrillouinZone, JsCrystal, JsHighSymmetryPoint, WasmResult,
};

/// Compute the first Brillouin zone for a crystal structure's lattice.
///
/// Returns vertex positions, face polygons, and volume of the Wigner-Seitz
/// cell in reciprocal space.
#[wasm_bindgen]
pub fn compute_brillouin_zone(structure: JsCrystal) -> WasmResult<JsBrillouinZone> {
    structure
        .to_structure()
        .map(|struc| {
            let bz = brillouin::compute_brillouin_zone(&struc.lattice);
            JsBrillouinZone {
                vertices: bz.vertices.iter().map(|v| [v.x, v.y, v.z]).collect(),
                faces: bz
                    .faces
                    .iter()
                    .map(|face| JsBrillouinFace {
                        vertices: face.vertices.clone(),
                        normal: [face.normal.x, face.normal.y, face.normal.z],
                        miller_index: face.miller_index,
                    })
                    .collect(),
                volume: bz.volume,
            }
        })
        .into()
}

/// Get labeled high-symmetry k-points for a crystal structure's lattice.
///
/// Returns standard Setyawan-Curtarolo k-path points based on the
/// detected lattice type (cubic, hexagonal, tetragonal, etc.).
#[wasm_bindgen]
pub fn get_high_symmetry_points(structure: JsCrystal) -> WasmResult<Vec<JsHighSymmetryPoint>> {
    structure
        .to_structure()
        .map(|struc| {
            brillouin::get_high_symmetry_points(&struc.lattice)
                .into_iter()
                .map(|(label, pos)| JsHighSymmetryPoint {
                    label,
                    position: [pos.x, pos.y, pos.z],
                })
                .collect()
        })
        .into()
}
