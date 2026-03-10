//! Bulk conversion between LMDB datasets and other formats (extXYZ, Structure).

use crate::element::Element;
use crate::error::Result;
use crate::io::{parse_extxyz_trajectory, structure_to_extxyz};
use crate::structure::Structure;
use std::fmt::Write as FmtWrite;
use std::io::{BufWriter, Write};
use std::path::Path;

use super::LmdbCodec;
use super::dataset::LmdbDataset;
use super::frame::TrainingFrame;

impl LmdbDataset {
    /// Create a new LMDB dataset from an extXYZ file.
    ///
    /// Parses all frames, converts to [`TrainingFrame`]s, and writes to a new LMDB.
    /// Serialization is parallelized when rayon is enabled.
    ///
    /// **Note**: All frames are loaded into memory. For very large files,
    /// consider streaming via [`extend`](LmdbDataset::extend).
    pub fn from_extxyz(xyz_path: &Path, lmdb_path: &Path, codec: LmdbCodec) -> Result<Self> {
        let frames: Vec<TrainingFrame> = parse_extxyz_trajectory(xyz_path)?
            .into_iter()
            .map(|res| res.map(|s| TrainingFrame::from(&s)))
            .collect::<Result<_>>()?;

        let dataset = Self::create(lmdb_path, codec)?;
        dataset.extend(frames)?;
        Ok(dataset)
    }

    /// Export the dataset to an extXYZ file.
    ///
    /// Frames with `cell: Some(...)` are converted via [`Structure`] for full
    /// extXYZ output including all labels. Frames with `cell: None` are written
    /// as minimal XYZ (atom count, pbc, energy, positions only — forces, stress,
    /// and other labels are not included, and these frames cannot be re-imported
    /// via [`from_extxyz`](LmdbDataset::from_extxyz)).
    ///
    /// Returns the number of frames written.
    pub fn to_extxyz(&self, xyz_path: &Path) -> Result<u64> {
        let len = self.len();
        let mut writer = BufWriter::new(std::fs::File::create(xyz_path)?);
        let rtxn = self.env_ref().read_txn()?;

        for idx in 0..len {
            let frame = self.get_in_txn(&rtxn, idx)?;
            let text = if frame.cell.is_some() {
                let structure = Structure::try_from(&frame)?;
                structure_to_extxyz(&structure, None)
            } else {
                frame_to_xyz(&frame)
            };
            writer.write_all(text.as_bytes())?;
        }

        writer.flush()?;
        Ok(len)
    }

    /// Create a new LMDB dataset from a slice of [`Structure`]s.
    pub fn from_structures(
        structures: &[Structure],
        lmdb_path: &Path,
        codec: LmdbCodec,
    ) -> Result<Self> {
        let frames: Vec<TrainingFrame> = structures.iter().map(TrainingFrame::from).collect();
        let dataset = Self::create(lmdb_path, codec)?;
        dataset.extend(frames)?;
        Ok(dataset)
    }
}

/// Format a non-periodic `TrainingFrame` as XYZ text (no `Lattice=` key).
fn frame_to_xyz(frame: &TrainingFrame) -> String {
    let n_atoms = frame.num_atoms();
    let mut out = String::with_capacity(n_atoms * 60 + 40);

    let _ = writeln!(out, "{n_atoms}");

    let pbc_str = frame.pbc.map(|b| if b { "T" } else { "F" }).join(" ");
    let mut comment = format!("pbc=\"{pbc_str}\"");
    if let Some(energy) = frame.energy {
        let _ = write!(comment, " energy={energy}");
    }
    let _ = writeln!(out, "{comment}");

    debug_assert_eq!(frame.atomic_numbers.len(), frame.positions.len());
    for (&atomic_num, pos) in frame.atomic_numbers.iter().zip(&frame.positions) {
        let symbol = Element::from_atomic_number(atomic_num).map_or("X", |el| el.symbol());
        let _ = writeln!(
            out,
            "{} {:20.16} {:20.16} {:20.16}",
            symbol, pos[0], pos[1], pos[2]
        );
    }

    out
}
