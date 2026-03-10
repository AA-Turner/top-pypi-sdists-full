//! LMDB-backed dataset for fast random-access storage of [`TrainingFrame`]s.
//!
//! Uses two named databases within a single LMDB environment:
//! - `"data"` — sequential `u64` keys → serialized frame bytes
//! - `"meta"` — string keys → JSON metadata (codec, length, version)

use crate::error::{FerroxError, Result};
use heed::byteorder::BigEndian;
use heed::types::{Bytes, Str, U64};
use heed::{Database, Env, EnvOpenOptions};
use std::path::Path;
use std::sync::atomic::AtomicU64;
use std::sync::atomic::Ordering::{Acquire, Release};

use super::frame::TrainingFrame;
use super::{LmdbCodec, deserialize_frame, serialize_frame};

/// Default LMDB map size: 1 TiB virtual (only used pages consume physical memory).
const DEFAULT_MAP_SIZE: usize = 1 << 40;

/// Current format version for forwards-compatibility checks.
const FORMAT_VERSION: u32 = 1;

/// Metadata stored in the `"meta"` database.
#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct DatasetMeta {
    length: u64,
    codec: LmdbCodec,
    version: u32,
}

/// An LMDB-backed dataset providing fast random-access reads and sequential writes
/// for ML interatomic potential training data.
///
/// LMDB supports concurrent reads from multiple threads but only one writer at
/// a time. Use [`par_iter`](LmdbDataset::par_iter) for parallel reads via rayon.
pub struct LmdbDataset {
    env: Env,
    data_db: Database<U64<BigEndian>, Bytes>,
    meta_db: Database<Str, Bytes>,
    codec: LmdbCodec,
    length: AtomicU64,
}

impl std::fmt::Debug for LmdbDataset {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt.debug_struct("LmdbDataset")
            .field("len", &self.len())
            .field("codec", &self.codec)
            .finish()
    }
}

fn open_env(path: &Path, map_size: usize) -> Result<Env> {
    unsafe {
        EnvOpenOptions::new()
            .max_dbs(2)
            .map_size(map_size)
            .open(path)
            .map_err(|err| FerroxError::LmdbError {
                reason: format!("failed to open LMDB env at {}: {err}", path.display()),
            })
    }
}

impl LmdbDataset {
    /// Open an existing LMDB dataset, reading codec and length from stored metadata.
    pub fn open(path: &Path) -> Result<Self> {
        let env = open_env(path, DEFAULT_MAP_SIZE)?;

        let rtxn = env.read_txn()?;
        let data_db: Database<U64<BigEndian>, Bytes> = env
            .open_database(&rtxn, Some("data"))?
            .ok_or_else(|| FerroxError::LmdbError {
                reason: "missing 'data' database in LMDB env".to_string(),
            })?;
        let meta_db: Database<Str, Bytes> =
            env.open_database(&rtxn, Some("meta"))?
                .ok_or_else(|| FerroxError::LmdbError {
                    reason: "missing 'meta' database in LMDB env".to_string(),
                })?;
        let meta = read_meta(&meta_db, &rtxn)?;
        rtxn.commit()?;

        if meta.version > FORMAT_VERSION {
            return Err(FerroxError::LmdbError {
                reason: format!(
                    "dataset version {} is newer than supported version {FORMAT_VERSION}",
                    meta.version
                ),
            });
        }

        Ok(Self {
            env,
            data_db,
            meta_db,
            codec: meta.codec,
            length: AtomicU64::new(meta.length),
        })
    }

    /// Create a new LMDB dataset with the default map size (1 TiB).
    pub fn create(path: &Path, codec: LmdbCodec) -> Result<Self> {
        Self::create_with_map_size(path, codec, DEFAULT_MAP_SIZE)
    }

    /// Create a new LMDB dataset with a custom map size in bytes.
    pub fn create_with_map_size(path: &Path, codec: LmdbCodec, map_size: usize) -> Result<Self> {
        std::fs::create_dir_all(path).map_err(|err| FerroxError::LmdbError {
            reason: format!("failed to create directory {}: {err}", path.display()),
        })?;

        let env = open_env(path, map_size)?;

        let mut wtxn = env.write_txn()?;
        let data_db: Database<U64<BigEndian>, Bytes> =
            env.create_database(&mut wtxn, Some("data"))?;
        let meta_db: Database<Str, Bytes> = env.create_database(&mut wtxn, Some("meta"))?;

        // Clear any pre-existing data so create() on an existing path
        // doesn't leave orphaned records or stale metadata
        data_db.clear(&mut wtxn)?;
        meta_db.clear(&mut wtxn)?;

        let meta = DatasetMeta {
            length: 0,
            codec,
            version: FORMAT_VERSION,
        };
        write_meta(&meta_db, &mut wtxn, &meta)?;
        wtxn.commit()?;

        Ok(Self {
            env,
            data_db,
            meta_db,
            codec,
            length: AtomicU64::new(0),
        })
    }

    /// Number of frames in the dataset.
    pub fn len(&self) -> u64 {
        self.length.load(Acquire)
    }

    /// Whether the dataset contains no frames.
    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    /// The serialization codec used by this dataset.
    pub fn codec(&self) -> LmdbCodec {
        self.codec
    }

    /// Access the underlying LMDB environment (for zero-copy batch reads).
    pub fn env_ref(&self) -> &Env {
        &self.env
    }

    /// Access the data database handle (for zero-copy batch reads).
    pub fn data_db_ref(&self) -> &Database<U64<BigEndian>, Bytes> {
        &self.data_db
    }

    /// Read a single frame by index.
    pub fn get(&self, idx: u64) -> Result<TrainingFrame> {
        let rtxn = self.env.read_txn()?;
        self.get_in_txn(&rtxn, idx)
    }

    /// Write a single frame at a given index.
    ///
    /// If the index is >= the current length, the length is updated to `idx + 1`.
    pub fn put(&self, idx: u64, frame: &TrainingFrame) -> Result<()> {
        let bytes = serialize_frame(frame, self.codec)?;
        let mut wtxn = self.env.write_txn()?;
        self.data_db.put(&mut wtxn, &idx, &bytes)?;
        self.commit_with_len_update(idx.saturating_add(1), wtxn)
    }

    /// Read multiple frames by index.
    pub fn get_batch(&self, indices: &[u64]) -> Result<Vec<TrainingFrame>> {
        let rtxn = self.env.read_txn()?;
        indices
            .iter()
            .map(|&idx| self.get_in_txn(&rtxn, idx))
            .collect()
    }

    /// Read a contiguous range of frames `[start, end)` in a single transaction.
    ///
    /// More efficient than individual `get()` calls for sequential reads since
    /// only one LMDB read transaction is opened for the entire range.
    pub fn get_range(&self, start: u64, end: u64) -> Result<Vec<TrainingFrame>> {
        let rtxn = self.env.read_txn()?;
        (start..end)
            .map(|idx| self.get_in_txn(&rtxn, idx))
            .collect()
    }

    /// Write multiple frames. Each entry is `(index, frame)`.
    ///
    /// Serialization is parallelized when the `rayon` feature is enabled.
    /// All LMDB writes happen in a single transaction for atomicity.
    pub fn put_batch(&self, frames: &[(u64, TrainingFrame)]) -> Result<()> {
        if frames.is_empty() {
            return Ok(());
        }

        let just_frames: Vec<&TrainingFrame> = frames.iter().map(|(_, frame)| frame).collect();
        let serialized_bytes = serialize_frame_refs(&just_frames, self.codec)?;

        let mut wtxn = self.env.write_txn()?;
        let mut new_len = self.length.load(Acquire);
        for ((idx, _), bytes) in frames.iter().zip(&serialized_bytes) {
            self.data_db.put(&mut wtxn, idx, bytes)?;
            new_len = new_len.max(idx.saturating_add(1));
        }
        self.commit_with_len_update(new_len, wtxn)?;
        Ok(())
    }

    /// Append frames, auto-assigning sequential keys starting from the current length.
    ///
    /// Serialization is parallelized via rayon when the `rayon` feature is enabled.
    /// Returns the new dataset length after insertion.
    pub fn extend(&self, frames: impl IntoIterator<Item = TrainingFrame>) -> Result<u64> {
        let frames: Vec<TrainingFrame> = frames.into_iter().collect();
        if frames.is_empty() {
            return Ok(self.len());
        }

        // Serialize outside the write lock for parallelism
        let frame_refs: Vec<&TrainingFrame> = frames.iter().collect();
        let serialized_bytes = serialize_frame_refs(&frame_refs, self.codec)?;

        // Assign indices under the write lock to avoid races between
        // concurrent extend() calls reading the same start_idx
        let mut wtxn = self.env.write_txn()?;
        let start_idx = self.length.load(Acquire);
        let new_len = start_idx.saturating_add(serialized_bytes.len() as u64);
        for (offset, bytes) in serialized_bytes.iter().enumerate() {
            let idx = start_idx.saturating_add(offset as u64);
            self.data_db.put(&mut wtxn, &idx, bytes)?;
        }
        self.commit_with_len_update(new_len, wtxn)?;
        Ok(new_len)
    }

    /// Remove all frames and reset the dataset length to zero.
    pub fn clear(&self) -> Result<()> {
        let mut wtxn = self.env.write_txn()?;
        self.data_db.clear(&mut wtxn)?;
        let meta = DatasetMeta {
            length: 0,
            codec: self.codec,
            version: FORMAT_VERSION,
        };
        write_meta(&self.meta_db, &mut wtxn, &meta)?;
        let old_len = self.length.load(Acquire);
        self.length.store(0, Release);
        if let Err(err) = wtxn.commit() {
            self.length.store(old_len, Release);
            return Err(err.into());
        }
        Ok(())
    }

    /// Iterate over all frames sequentially within a single read transaction.
    pub fn iter(&self) -> Result<impl Iterator<Item = Result<(u64, TrainingFrame)>> + '_> {
        let rtxn = self.env.read_txn()?;
        let len = self.len();
        Ok((0..len).map(move |idx| Ok((idx, self.get_in_txn(&rtxn, idx)?))))
    }

    /// Iterate over all frames in parallel using rayon.
    ///
    /// Each rayon task opens its own lightweight read transaction from the
    /// shared `Env` (which is `Send + Sync`).
    #[cfg(feature = "rayon")]
    pub fn par_iter(
        &self,
    ) -> impl rayon::iter::ParallelIterator<Item = Result<(u64, TrainingFrame)>> + '_ {
        use rayon::iter::{IntoParallelIterator, ParallelIterator};
        let len = self.len();
        (0..len).into_par_iter().map(move |idx| {
            let frame = self.get(idx)?;
            Ok((idx, frame))
        })
    }

    /// Read and deserialize a single frame within an existing read transaction.
    pub(super) fn get_in_txn(&self, rtxn: &heed::RoTxn<'_>, idx: u64) -> Result<TrainingFrame> {
        let bytes = self
            .data_db
            .get(rtxn, &idx)?
            .ok_or_else(|| FerroxError::LmdbError {
                reason: format!("key {idx} not found in LMDB dataset"),
            })?;
        deserialize_frame(bytes, self.codec)
    }

    /// Update persisted metadata, update the in-memory length, then commit.
    ///
    /// The in-memory atomic is updated BEFORE `commit()` so that concurrent
    /// writers (blocked on `write_txn()`) see the correct length as soon as
    /// they acquire the lock. On commit failure, the atomic is rolled back
    /// so subsequent writes don't skip indices.
    fn commit_with_len_update(&self, new_len: u64, mut wtxn: heed::RwTxn<'_>) -> Result<()> {
        let cur_len = self.length.load(Acquire);
        if new_len > cur_len {
            let meta = DatasetMeta {
                length: new_len,
                codec: self.codec,
                version: FORMAT_VERSION,
            };
            write_meta(&self.meta_db, &mut wtxn, &meta)?;
            self.length.store(new_len, Release);
        }
        if let Err(err) = wtxn.commit() {
            self.length.store(cur_len, Release);
            return Err(err.into());
        }
        Ok(())
    }
}

// === Internal helpers ===

/// Serialize frame references to bytes, parallelized via rayon when available.
fn serialize_frame_refs(frames: &[&TrainingFrame], codec: LmdbCodec) -> Result<Vec<Vec<u8>>> {
    #[cfg(feature = "rayon")]
    {
        use rayon::iter::{IntoParallelIterator, ParallelIterator};
        frames
            .into_par_iter()
            .map(|frame| serialize_frame(frame, codec))
            .collect()
    }

    #[cfg(not(feature = "rayon"))]
    {
        frames
            .iter()
            .map(|frame| serialize_frame(frame, codec))
            .collect()
    }
}

fn read_meta(meta_db: &Database<Str, Bytes>, rtxn: &heed::RoTxn<'_>) -> Result<DatasetMeta> {
    let bytes = meta_db
        .get(rtxn, "info")?
        .ok_or_else(|| FerroxError::LmdbError {
            reason: "missing 'info' key in meta database".to_string(),
        })?;
    serde_json::from_slice(bytes).map_err(|err| FerroxError::LmdbError {
        reason: format!("failed to parse dataset metadata: {err}"),
    })
}

fn write_meta(
    meta_db: &Database<Str, Bytes>,
    wtxn: &mut heed::RwTxn<'_>,
    meta: &DatasetMeta,
) -> Result<()> {
    let bytes = serde_json::to_vec(meta).map_err(|err| FerroxError::LmdbError {
        reason: format!("failed to serialize dataset metadata: {err}"),
    })?;
    meta_db.put(wtxn, "info", &bytes)?;
    Ok(())
}
