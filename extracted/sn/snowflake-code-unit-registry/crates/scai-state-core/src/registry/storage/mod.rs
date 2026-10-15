//! Registry storage: the JSON files (the record) plus a SQLite index.
//!
//! The registry layer (`registry.rs`) owns all document semantics — schema
//! migration on read, typed/raw deep-merge on write, hooks. [`Storage`] maps
//! a code unit ID to its raw JSON text:
//!
//! - [`FileStorage`]: one pretty-printed `registry/{id}.json` per unit — the
//!   only record, synced through git exactly as before.
//! - The SQLite index (`sqlite.rs`, `registry/.index/`): a git-ignored,
//!   always-rebuildable cache of the files with indexed columns
//!   ([`index`]), kept current by the freshness protocol described in
//!   `registry/README.md`.
//!
//! Reads that want the whole registry or a filtered subset go through the
//! index when it is trusted, and fall back to the files otherwise; reads of
//! the record itself (`read_raw`, `read_many`, `*_files`) always hit the
//! files. Writes go to the files, then to the index.
//!
//! IDs are storage keys (file stems): a document whose embedded `id`
//! disagrees with its key is reported by the loader/validator, never
//! silently re-keyed here.

mod file;
pub(crate) mod index;
mod sqlite;
mod sync;

pub(crate) use file::FileStorage;

use std::fs::File;
use std::path::Path;
use std::sync::atomic::AtomicUsize;
use std::sync::Arc;

use rayon::prelude::*;
use serde_json::Value;

use crate::error::*;
use sync::IndexSync;

/// Environment variable that disables the SQLite index when set to `off`,
/// `0`, or `false`: the process then reads and writes only the JSON files
/// (a diagnostic escape hatch and benchmark baseline).
pub const INDEX_ENV_VAR: &str = "SCAI_REGISTRY_INDEX";

/// Index directory inside the registry directory.
pub(crate) const INDEX_DIR: &str = ".index";

/// Number of documents read per chunk by full scans. Bounds peak memory:
/// raw text for at most one chunk is held alongside the parsed output.
const SCAN_CHUNK: usize = 4096;

/// Index reads a query attempts before reading the files: a read vouched
/// for by a lock-free verify is retried when its confirmation fails, the
/// last attempt without the lock-free shortcut.
const READ_ATTEMPTS: usize = 3;

/// A single document write.
#[derive(Debug, Clone, Copy)]
pub(crate) enum StorageWrite<'a> {
    /// Store `value` as the full document for `id`, replacing any existing one.
    Put { id: &'a str, value: &'a Value },
    /// Remove the document for `id`; a no-op if it does not exist.
    Delete { id: &'a str },
}

// ── Index contract (shared by the sync engine and `sqlite.rs`) ───────────

/// Identity of one version of a registry file, as seen by `stat`.
///
/// `file_id` is the inode on Unix (0 where unavailable): replacing a file by
/// rename — as git and the library do — always changes it, even when size
/// and mtime happen to match. A stored row's `mtime_ns` may instead be the
/// "smudged" sentinel (see `sync.rs`), which no `stat` returns, so the next
/// sweep re-reads that file.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) struct Fingerprint {
    pub(crate) size: u64,
    pub(crate) mtime_ns: i64,
    pub(crate) file_id: u64,
}

/// The index's bookkeeping row (see the freshness protocol).
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub(crate) struct IndexMeta {
    /// Registry directory mtime the index was last brought in line with;
    /// `None` = never (a new or reset index).
    pub(crate) dir_mtime_ns: Option<i64>,
    /// Wall-clock time at which `dir_mtime_ns` was observed (see
    /// [`IndexChanges::dir_recorded_ns`]). Less than the racy window after
    /// `dir_mtime_ns` means a later change in the same filesystem clock
    /// tick could have left the mtime unchanged, so the index must be
    /// verified against a listing before it is trusted.
    pub(crate) dir_recorded_ns: Option<i64>,
    /// Wall-clock time of the last full sweep.
    pub(crate) last_sweep_ns: Option<i64>,
    /// A library writer holding the write lock is mid-batch.
    pub(crate) write_in_progress: bool,
}

/// One index row: a document's text — exactly the file's text, whether a
/// sweep read it or a library write produced it — and the fingerprint of
/// the file it came from.
#[derive(Debug, Clone)]
pub(crate) struct IndexRow<'a> {
    pub(crate) id: &'a str,
    pub(crate) doc: std::borrow::Cow<'a, str>,
    pub(crate) fingerprint: Fingerprint,
}

/// Changes committed to the index in one transaction. Every `apply` also
/// clears `write_in_progress`.
#[derive(Debug, Clone, Default)]
pub(crate) struct IndexChanges<'a> {
    pub(crate) upserts: Vec<IndexRow<'a>>,
    pub(crate) deletes: Vec<&'a str>,
    /// New `meta.dir_mtime_ns`.
    pub(crate) dir_mtime_ns: Option<i64>,
    /// New `meta.dir_recorded_ns`: the wall-clock time *before* the
    /// observation that `dir_mtime_ns` vouches for — the stat before a
    /// sweep's or verify's listing, or the start of a write batch — not the
    /// time of `apply`. Always given together with `dir_mtime_ns`.
    pub(crate) dir_recorded_ns: Option<i64>,
    /// New `meta.last_sweep_ns` (set by sweeps only).
    pub(crate) swept_at_ns: Option<i64>,
}

// ── Write lock ──────────────────────────────────────────────────────────

/// Exclusive registry write lock (`registry/.locks/registry.lock`); released
/// when dropped.
///
/// While any guard on a registry is alive, readers in the same process never
/// wait on the lock (see `sync.rs`): an flock taken through a second
/// descriptor would deadlock against it.
pub struct LockGuard {
    file: File,
    /// The process-wide holder count this guard is part of (see `sync.rs`).
    held: Arc<AtomicUsize>,
}

// ── Storage ─────────────────────────────────────────────────────────────

/// The storage of an open registry.
#[derive(Debug)]
pub(crate) struct Storage {
    files: FileStorage,
    index: IndexSync,
}

impl Storage {
    /// Storage for the registry directory `dir`. Never fails because of the
    /// index: an unusable index only means reads come from the files. The
    /// index is opened on first use, unless [`INDEX_ENV_VAR`] disables it.
    pub(crate) fn open(dir: &Path) -> Result<Self> {
        Ok(Self::with_index(dir, sync::enabled_by_env()))
    }

    fn with_index(dir: &Path, enabled: bool) -> Self {
        Self {
            files: FileStorage::new(dir.to_path_buf()),
            index: IndexSync::new(dir, enabled),
        }
    }

    /// Storage that never uses the index, as with `SCAI_REGISTRY_INDEX=off`.
    #[cfg(test)]
    pub(crate) fn open_without_index(dir: &Path) -> Self {
        Self::with_index(dir, false)
    }

    /// The file store (for file-layout tests).
    #[cfg(test)]
    pub(crate) fn files(&self) -> &FileStorage {
        &self.files
    }

    // ── Locking ─────────────────────────────────────────────────────────

    /// Acquire the exclusive registry write lock (blocking).
    pub(crate) fn lock(&self) -> Result<LockGuard> {
        self.index.lock()
    }

    // ── The record (always the files) ───────────────────────────────────

    /// Whether a document is stored under `id`.
    pub(crate) fn exists(&self, id: &str) -> Result<bool> {
        Ok(self.files.exists(id))
    }

    /// Raw JSON text stored under `id`, or `None` if absent.
    pub(crate) fn read_raw(&self, id: &str) -> Result<Option<String>> {
        self.files.read_raw(id)
    }

    /// Raw JSON text for each of `ids`, in the same order.
    pub(crate) fn read_many(&self, ids: &[String]) -> Vec<Result<Option<String>>> {
        self.files.read_many(ids)
    }

    /// All stored IDs (file stems), in directory order.
    #[cfg(test)]
    pub(crate) fn file_ids(&self) -> Result<Vec<String>> {
        self.files.ids()
    }

    /// Visit every file in chunks of up to [`SCAN_CHUNK`]. `f` receives the
    /// chunk's IDs and their read outcomes (`Ok(None)` when a file vanished
    /// between listing and reading). `f` may write to this storage.
    pub(crate) fn for_each_file_chunk(
        &self,
        mut f: impl FnMut(&[String], Vec<Result<Option<String>>>) -> Result<()>,
    ) -> Result<()> {
        let ids = self.files.ids()?;
        for chunk in ids.chunks(SCAN_CHUNK) {
            f(chunk, self.files.read_many(chunk))?;
        }
        Ok(())
    }

    /// Map every file through `f` in parallel, in directory order. Files
    /// that vanish mid-scan are skipped.
    pub(crate) fn load_all_files<T: Send>(
        &self,
        f: impl Fn(&str, Result<String>) -> T + Sync,
    ) -> Result<Vec<T>> {
        let mut out = Vec::new();
        self.for_each_file_chunk(|ids, texts| {
            out.par_extend(
                ids.par_iter()
                    .zip(texts.into_par_iter())
                    .filter_map(|(id, text)| text.transpose().map(|text| f(id, text))),
            );
            Ok(())
        })?;
        Ok(out)
    }

    /// Human-readable location of a document, for error messages.
    pub(crate) fn location(&self, id: &str) -> String {
        self.files.path_for(id).display().to_string()
    }

    // ── Queries (index when trusted, else files) ────────────────────────

    /// Map every stored document through `f` in parallel. Served by the
    /// index when it is trusted, otherwise by the files.
    pub(crate) fn load_all<T: Send>(
        &self,
        f: impl Fn(&str, Result<String>) -> T + Sync,
    ) -> Result<Vec<T>> {
        for attempt in 0..READ_ATTEMPTS {
            let Some(read) = self
                .index
                .for_read(&self.files, attempt + 1 < READ_ATTEMPTS)
            else {
                break;
            };
            let mut out = Vec::new();
            let scanned = read.index.for_each_chunk(SCAN_CHUNK, |ids, texts| {
                out.par_extend(
                    ids.par_iter()
                        .zip(texts.into_par_iter())
                        .filter_map(|(id, text)| text.transpose().map(|text| f(id, text))),
                );
                Ok(())
            });
            // An index failure mid-scan: start over from the files.
            if scanned.is_err() {
                break;
            }
            if read.confirm() {
                self.index.count_index_read();
                return Ok(out);
            }
        }
        self.load_all_files(f)
    }

    /// Map the documents that may satisfy `prefilter` through `f`, or
    /// `None` when the index can't serve it (untrusted, disabled, or a full
    /// scan is cheaper) — the caller then uses [`Self::load_all`].
    ///
    /// The result is a superset of the matches (see [`index`]): callers must
    /// still apply the original predicate to each document.
    pub(crate) fn load_candidates<T: Send>(
        &self,
        prefilter: &index::Prefilter,
        f: impl Fn(&str, Result<String>) -> T + Sync,
    ) -> Result<Option<Vec<T>>> {
        for attempt in 0..READ_ATTEMPTS {
            let Some(read) = self
                .index
                .for_read(&self.files, attempt + 1 < READ_ATTEMPTS)
            else {
                break;
            };
            match read.index.load_candidates(prefilter, &f) {
                Ok(Some(candidates)) if read.confirm() => {
                    self.index.count_index_read();
                    return Ok(Some(candidates));
                }
                Ok(Some(_)) => {}
                // Not servable, or an index failure: the caller scans instead.
                Ok(None) | Err(_) => break,
            }
        }
        Ok(None)
    }

    // ── Writes (caller holds the write lock) ────────────────────────────

    /// Called once at the start of a locked write operation, before any
    /// read the operation's hooks make: brings an untrusted index up to date
    /// (see the freshness protocol).
    pub(crate) fn prepare_write(&self, lock: &LockGuard) -> Result<()> {
        self.index.prepare_write(&self.files, lock);
        Ok(())
    }

    /// Apply `writes` to the files, then to the index, returning one
    /// outcome per write in input order. Index failures never fail a write.
    ///
    /// `durable` requests that user-initiated writes survive a crash once
    /// this returns (together with [`Self::sync`]); derived and bulk writes
    /// pass `false`.
    pub(crate) fn write_batch(
        &self,
        lock: &LockGuard,
        writes: &[StorageWrite<'_>],
        durable: bool,
    ) -> Vec<Result<()>> {
        self.index.write_batch(&self.files, lock, writes, durable)
    }

    /// Make all preceding file writes durable.
    pub(crate) fn sync(&self) -> Result<()> {
        self.files.sync()
    }

    /// How many `load_all` / `load_candidates` calls on this instance were
    /// served by the index (so tests and benchmarks can prove the index path
    /// actually ran). A relaxed counter: cheap, and exact once the calls
    /// returned.
    pub(crate) fn index_reads(&self) -> u64 {
        self.index.index_reads()
    }

    /// Test-only: how many sweeps this instance ran.
    #[cfg(test)]
    pub(crate) fn sweeps(&self) -> u64 {
        self.index.sweeps()
    }

    /// Test-only: write arbitrary raw text (possibly invalid JSON) as the
    /// file for `id` the way an external writer such as git does — temp file
    /// plus rename, so the directory mtime changes.
    #[cfg(test)]
    pub(crate) fn put_raw_text(&self, id: &str, text: &str) -> Result<()> {
        let path = self.files.path_for(id);
        let temp = path.with_extension("json.external-tmp");
        std::fs::write(&temp, text)?;
        std::fs::rename(&temp, &path)?;
        Ok(())
    }
}
