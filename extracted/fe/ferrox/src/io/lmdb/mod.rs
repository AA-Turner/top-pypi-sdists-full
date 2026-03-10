//! LMDB-backed dataset storage for ML interatomic potential training data.
//!
//! Provides [`LmdbDataset`] for high-performance random-access reads and
//! sequential writes. Uses rkyv zero-copy serialization by default for
//! fastest reads; JSON is available for debugging/inspection.
//!
//! # Example
//!
//! ```rust,ignore
//! use ferrox::io::lmdb::{LmdbCodec, LmdbDataset, TrainingFrame};
//! use std::path::Path;
//!
//! // Create a new dataset (rkyv by default)
//! let dataset = LmdbDataset::create(Path::new("train.lmdb"), LmdbCodec::default())?;
//!
//! // Append frames
//! dataset.extend(vec![frame1, frame2, frame3])?;
//!
//! // Random access
//! let frame = dataset.get(42)?;
//!
//! // Parallel iteration
//! dataset.par_iter().for_each(|result| { /* ... */ });
//! ```

mod convert;
mod dataset;
pub(crate) mod frame;

pub use dataset::LmdbDataset;
pub use frame::TrainingFrame;

use crate::error::{FerroxError, Result};
use frame::RkyvFrame;
use serde::{Deserialize, Serialize};

/// Serialization codec for LMDB values.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq, Serialize, Deserialize)]
pub enum LmdbCodec {
    /// rkyv — zero-copy deserialization, fastest reads. Default.
    #[default]
    Rkyv,
    /// JSON via serde_json — human-readable, useful for debugging/inspection.
    Json,
}

/// Serialize a [`TrainingFrame`] to bytes using the given codec.
pub fn serialize_frame(frame: &TrainingFrame, codec: LmdbCodec) -> Result<Vec<u8>> {
    match codec {
        LmdbCodec::Rkyv => {
            let rkyv_frame = RkyvFrame::from(frame);
            let aligned = rkyv::to_bytes::<rkyv::rancor::Error>(&rkyv_frame).map_err(|err| {
                FerroxError::LmdbError {
                    reason: format!("rkyv serialization failed: {err}"),
                }
            })?;
            Ok(aligned.to_vec())
        }
        LmdbCodec::Json => serde_json::to_vec(frame).map_err(|err| FerroxError::LmdbError {
            reason: format!("json serialization failed: {err}"),
        }),
    }
}

/// Deserialize a [`TrainingFrame`] from bytes using the given codec.
pub fn deserialize_frame(bytes: &[u8], codec: LmdbCodec) -> Result<TrainingFrame> {
    match codec {
        LmdbCodec::Rkyv => {
            let rkyv_frame: RkyvFrame = rkyv::from_bytes::<RkyvFrame, rkyv::rancor::Error>(bytes)
                .map_err(|err| FerroxError::LmdbError {
                reason: format!("rkyv deserialization failed: {err}"),
            })?;
            Ok(TrainingFrame::from(rkyv_frame))
        }
        LmdbCodec::Json => serde_json::from_slice(bytes).map_err(|err| FerroxError::LmdbError {
            reason: format!("json deserialization failed: {err}"),
        }),
    }
}
