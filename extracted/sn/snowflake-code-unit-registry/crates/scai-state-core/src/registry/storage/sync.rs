//! The index freshness protocol: when the SQLite index may serve a read,
//! the sweeps and verifies that bring it in line with the files, and the
//! index side of library writes. `registry/README.md` ("Storage: JSON Files
//! + SQLite Index") describes the protocol; this module implements it.
//!
//! # Freshness
//!
//! A query first classifies the index ([`Freshness`]) from one `stat` of the
//! registry directory plus the one-row meta table:
//!
//! - **stale**: the directory mtime differs from `meta.dir_mtime_ns`, or a
//!   library writer is mid-batch (`write_in_progress`). Needs a sweep.
//! - **racy**: in line, but the mtime was observed less than
//!   [`racy_window`] after it was set. Directory mtimes come from the
//!   filesystem's coarse clock (4–10 ms ticks on Linux before fine-grained
//!   timestamps, ~15.6 ms on Windows, 1–2 s on FAT/HFS+), so a file added,
//!   removed or replaced later in the same tick left it unchanged. Needs a
//!   *verify*: compare the listing's (name → file id) with the index rows —
//!   one `readdir`, no `stat` per file — and re-record the same mtime with a
//!   fresh observation time when nothing differs (git's "racily clean"
//!   check, applied to the directory). Any difference → sweep.
//! - **expired**: in line and settled, but the last full sweep is older than
//!   [`SWEEP_INTERVAL`] (or in the future). Needs a sweep, which is what
//!   eventually catches in-place edits (those leave the directory alone).
//! - **trusted**: none of the above.
//!
//! Every library write leaves the index racy (its observation precedes its
//! own renames), so the first read at least [`racy_window`] later verifies.
//!
//! # Reader states
//!
//! - trusted → read the index;
//! - this process holds the write lock (any instance, any thread — hooks
//!   inside a write, or a sweep on another thread) → never wait on it: read
//!   the index unless it is stale without a write in progress, else files.
//!   (A locked operation reads as of its `prepare_write`, which verified or
//!   swept; a same-tick change *during* the operation is concurrent with it.)
//! - racy (and the periodic sweep not due) → verify *without* the lock
//!   (below); a match serves this read from the index;
//! - otherwise, or on a mismatch, try the write lock without blocking:
//!   - acquired → re-check; verify or sweep as needed; release; read;
//!   - busy, and a library writer is mid-batch, or the index is merely
//!     expired → read the index as-is (the consistent pre-batch snapshot /
//!     the files as of the last sweep, short only of in-place edits);
//!   - busy with a sweep running (`dir_mtime_ns =` [`SWEEPING_DIR_MTIME`],
//!     which every sweep commits first — the first-open build included) →
//!     wait, polling and re-checking every 5–50 ms, for at most
//!     [`SWEEP_WAIT_LIMIT`]; then read the files. Reading the files costs
//!     what the sweep does, so a crowd of readers waits for the one sweep
//!     instead of each redoing it;
//!   - busy otherwise → wait, polling and re-checking every few ms, for at
//!     most [`WAIT_LIMIT`]; then read the files.
//!
//! Every re-check tries the lock again, so a reader proceeds the moment the
//! sweep commits (the index is then in line) or the lock frees, and a
//! sweeper that died is taken over at once: its sentinel stays behind, but
//! the OS released its lock, which the reader then gets and sweeps itself.
//! A sweep that stops early on an error commits [`ABANDONED_DIR_MTIME`]
//! instead (still stale, not waited for), since its caller may keep the
//! lock for a whole write operation. A reader that waits out a limit
//! records the meta it gave up on; while the index shows exactly that meta
//! and the lock is busy, later reads on the same instance go to the files
//! without waiting again (one query may ask twice: candidates, then all).
//!
//! Any index error, or a sweep that cannot finish, means "read the files":
//! the index never fails an operation.
//!
//! # Lock-free verify
//!
//! A verify only reads, so a reader that finds the index racy runs it
//! without the write lock — a library writer holding the lock through its
//! hooks no longer queues readers. It takes `observed` (wall clock), then
//! checks the directory mtime equals the `m` the racy meta records, lists
//! (name → inode) and reads the rows' file ids, and checks the mtime again.
//! On a match the listing provably equals the rows as of the listing, so
//! this read uses the index; once `observed − m` exceeds the racy window it
//! also settles the index for later readers with a compare-and-set
//! ([`SqliteIndex::settle_dir`]: only if `dir_mtime_ns`, `dir_recorded_ns`
//! are still what classified it racy and no write is in progress). Any
//! mismatch is a real change: the locked path above takes over.
//!
//! Two guards close the races with lock holders, which keep changing the
//! rows while the verify runs:
//!
//! - **A sweep** commits rows taken from *its* listing, which the verify
//!   never compared: if that listing predates a same-tick change the
//!   verify's listing saw (an add and delete of one name within a tick), the
//!   sweep's rows are stale while still racy. So a sweep first commits
//!   `dir_mtime_ns =` [`SWEEPING_DIR_MTIME`], making the index stale while
//!   it runs; the CAS then can't match until the sweep commits a fresh
//!   `dir_recorded_ns`, which also fails the CAS (`IS seen`). And a
//!   lock-free verified read is *confirmed* after reading
//!   ([`IndexRead::confirm`]): if `dir_mtime_ns` or `last_sweep_ns` moved —
//!   a sweep started or finished, or a write recorded a new mtime — the
//!   read is retried (the last attempt without the shortcut).
//! - **A writer** sets `write_in_progress` before its first rename. Its
//!   renames during the listing either change the mtime the verify checks
//!   on both sides of its listing, or (same tick) show up as inodes the rows
//!   lack, unless the listing passed them before they happened — then this
//!   read precedes the batch, and reading the pre-batch rows is correct. Its
//!   flag (or the fresh `dir_recorded_ns` its commit records) makes the CAS
//!   a no-op, so a verify never settles over its batch. A write's rows are
//!   its own files' truth, so a confirm that sees only a same-tick write
//!   commit lets the read stand.
//! - **Smudged rows** carry real file ids (only their mtime is the
//!   sentinel), so a verify, locked or not, compares them correctly. It
//!   never un-smudges them; the next sweep re-reads them as before, and a
//!   settled index still gets the periodic sweep that does.
//!
//! What no verify can see, locked or not: an in-place rewrite (same inode;
//! the documented limit, left to the periodic sweep), and — theoretically —
//! a file replaced in the same tick by one that reuses the row's inode
//! number (ext4 reuses freed inodes; btrfs and APFS don't).
//!
//! # Incomplete listings
//!
//! A directory listing taken while the directory changes may miss entries
//! that exist throughout, or return one twice: POSIX leaves it unspecified,
//! and btrfs does skip a file renamed over (a `git checkout`) mid-listing.
//! So no listing alone ever deletes a row:
//!
//! - **Sweep:** rows whose name the listing lacks are `stat`ed by path (a
//!   rename-over is atomic for the path, so an existing file always
//!   answers). Present → re-read and upserted with that fresh fingerprint,
//!   like any changed file; only `NotFound` deletes the row. Only unlisted
//!   rows are checked, so this is cheap.
//! - **Verify:** compares the listing with the rows as sets
//!   ([`listing_matches`]): a missing name, or a repeated one standing in
//!   for it, is a mismatch, and the locked path sweeps.
//! - **A new file the sweep's listing missed** stays absent from the index,
//!   but the next read catches it. Whatever made the listing incomplete
//!   changed the directory after the sweep's pre-listing `stat`. Either its
//!   mtime moved past the recorded one (the next read finds the index
//!   stale and sweeps), or it landed in the same clock tick as the recorded
//!   mtime — then the pre-listing observation lies within that tick too,
//!   so the recording is racy and the next read verifies, against a new
//!   listing. (That listing could in turn miss the file only if the file is
//!   being renamed again during it, in that same tick: the same race any
//!   verify has with a concurrent change.)
//!
//! # Rows
//!
//! The same tick problem exists per file: an in-place rewrite (same inode)
//! of the same size in the same tick as the version a row was taken from
//! leaves the fingerprint unchanged, so no sweep — periodic or not — would
//! ever see it. Such rows are stored *smudged* (fingerprint mtime
//! [`SMUDGED_MTIME`], which no `stat` returns) and re-read by the next
//! sweep: every row a library write records (its file was just renamed into
//! place) and every swept row whose file changed within [`racy_window`] of
//! the sweep. Re-reading an unchanged file only updates the row's
//! fingerprint columns.

use std::borrow::Cow;
use std::collections::{HashMap, HashSet};
use std::fs::{File, OpenOptions};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex, MutexGuard, Weak};
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

use fs2::FileExt;
use rayon::prelude::*;

use super::file::{FileStorage, Written};
use super::sqlite::{self, SqliteIndex};
use super::{
    Fingerprint, IndexChanges, IndexMeta, IndexRow, LockGuard, StorageWrite, INDEX_DIR,
    INDEX_ENV_VAR, SCAN_CHUNK,
};
use crate::error::*;

/// Longest the index is trusted without a full sweep: bounds how long an
/// in-place edit (which leaves the directory mtime alone) can go unseen.
pub(super) const SWEEP_INTERVAL: Duration = Duration::from_secs(30);

/// How long after a directory mtime was set an observation of it must be
/// to rule out a later same-tick change (see [`racy_window`]).
pub(super) const RACY_WINDOW: Duration = Duration::from_millis(100);

/// [`RACY_WINDOW`] for filesystems with whole-second timestamps.
const COARSE_RACY_WINDOW: Duration = Duration::from_secs(2);

/// Longest a reader waits for another process's lock holder (not
/// sweeping) before reading the files instead.
const WAIT_LIMIT: Duration = Duration::from_secs(1);

/// Polling interval bounds while waiting for the write lock.
const WAIT_MIN: Duration = Duration::from_millis(1);
const WAIT_MAX: Duration = Duration::from_millis(10);

/// Longest a reader waits for another process's sweep (or first-open
/// build) before reading the files instead: reading the files costs about
/// what the sweep does, so a crowd of readers should wait for the one.
const SWEEP_WAIT_LIMIT: Duration = Duration::from_secs(60);

/// Polling interval bounds while waiting for a sweep.
const SWEEP_WAIT_MIN: Duration = Duration::from_millis(5);
const SWEEP_WAIT_MAX: Duration = Duration::from_millis(50);

/// Fingerprint mtime of a smudged row: never equal to a real `stat`, so the
/// next sweep re-reads the file.
pub(super) const SMUDGED_MTIME: i64 = i64::MIN;

/// `meta.dir_mtime_ns` while a sweep runs: never equal to a real `stat`.
pub(super) const SWEEPING_DIR_MTIME: i64 = i64::MIN;

/// `meta.dir_mtime_ns` after a sweep stopped early: stale like
/// [`SWEEPING_DIR_MTIME`], but readers don't wait for it.
const ABANDONED_DIR_MTIME: i64 = i64::MIN + 1;

const NS_PER_SEC: i64 = 1_000_000_000;

/// Whether `SCAI_REGISTRY_INDEX` leaves the index enabled (unset, or
/// anything but `off` / `0` / `false`).
pub(super) fn enabled_by_env() -> bool {
    !matches!(
        std::env::var(INDEX_ENV_VAR)
            .map(|v| v.trim().to_ascii_lowercase())
            .as_deref(),
        Ok("off" | "0" | "false")
    )
}

/// The index of one open registry, plus the write lock and the protocol
/// state around it.
#[derive(Debug)]
pub(super) struct IndexSync {
    /// `registry/.index`.
    index_dir: PathBuf,
    /// `registry/.locks/registry.lock`.
    lock_path: PathBuf,
    /// The index, opened on first use.
    slot: Mutex<Slot>,
    /// How many write-lock guards on this registry directory this process
    /// holds (shared by every instance in the process; see [`held_counter`]).
    held: Arc<AtomicUsize>,
    /// The meta a reader last waited out to its limit with the lock busy.
    /// While the index still shows exactly that, readers on this instance
    /// read the files without waiting again (a query may ask twice: for
    /// candidates, then for everything).
    gave_up_on: Mutex<Option<IndexMeta>>,
    /// Reads served by the index (see [`Self::count_index_read`]).
    index_reads: AtomicU64,
    #[cfg(test)]
    stats: TestStats,
    /// [`SWEEP_WAIT_LIMIT`], shortened by tests.
    #[cfg(test)]
    sweep_wait_limit: Mutex<Duration>,
}

#[derive(Debug)]
enum Slot {
    /// Not opened yet; `false` = disabled (`SCAI_REGISTRY_INDEX=off`).
    Unopened {
        enabled: bool,
    },
    Open(Arc<SqliteIndex>),
    /// Disabled, or it could not be opened: serve from the files.
    Off,
}

#[cfg(test)]
#[derive(Debug, Default)]
struct TestStats {
    sweeps: std::sync::atomic::AtomicU64,
    verifies: std::sync::atomic::AtomicU64,
    lock_free_verifies: std::sync::atomic::AtomicU64,
    /// Reads that waited out a wait limit on the lock.
    give_ups: std::sync::atomic::AtomicU64,
    /// Sleeps while polling the lock (timing-free "did it wait?").
    waits: std::sync::atomic::AtomicU64,
}

/// How far the index can be relied on (see the module docs).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Freshness {
    Trusted,
    /// In line and settled; the last full sweep is too old.
    Expired,
    /// In line, but a same-tick change may hide behind the directory mtime.
    /// `expired`: the periodic sweep is due as well.
    Racy {
        expired: bool,
    },
    /// Not in line with the directory (or unreadable). `write_in_progress`:
    /// a library writer is mid-batch over a consistent pre-batch index.
    Stale {
        write_in_progress: bool,
    },
}

type SweepResult = std::result::Result<(), SweepError>;

/// Why a sweep stopped.
enum SweepError {
    /// The files could not be listed or read; the files path reports it.
    Files,
    /// The index failed; repairing it may help.
    Index,
}

impl IndexSync {
    /// The protocol state for the registry directory `dir`; the index itself
    /// is opened on first use, if `enabled`.
    pub(super) fn new(dir: &Path, enabled: bool) -> Self {
        Self {
            index_dir: dir.join(INDEX_DIR),
            lock_path: dir.join(".locks").join("registry.lock"),
            slot: Mutex::new(Slot::Unopened { enabled }),
            held: held_counter(dir),
            gave_up_on: Mutex::new(None),
            index_reads: AtomicU64::new(0),
            #[cfg(test)]
            stats: TestStats::default(),
            #[cfg(test)]
            sweep_wait_limit: Mutex::new(SWEEP_WAIT_LIMIT),
        }
    }

    // ── Write lock ──────────────────────────────────────────────────────

    /// Acquire the exclusive registry write lock (blocking).
    pub(super) fn lock(&self) -> Result<LockGuard> {
        if let Some(parent) = self.lock_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        let file = File::create(&self.lock_path)?;
        file.lock_exclusive().map_err(|e| {
            LockSnafu {
                message: e.to_string(),
            }
            .build()
        })?;
        Ok(self.guard(file))
    }

    /// Acquire the write lock if it is free: `None` when another holder has it.
    fn try_lock(&self) -> std::io::Result<Option<LockGuard>> {
        if let Some(parent) = self.lock_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        let file = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(false)
            .open(&self.lock_path)
            // A read-only registry: flock works on a read-only descriptor.
            .or_else(|_| File::open(&self.lock_path))?;
        match file.try_lock_exclusive() {
            Ok(()) => Ok(Some(self.guard(file))),
            Err(e) if e.raw_os_error() == fs2::lock_contended_error().raw_os_error() => Ok(None),
            Err(e) => Err(e),
        }
    }

    fn guard(&self, file: File) -> LockGuard {
        self.held.fetch_add(1, Ordering::SeqCst);
        LockGuard {
            file,
            held: Arc::clone(&self.held),
        }
    }

    /// Whether this process holds the write lock on this registry.
    fn held_here(&self) -> bool {
        self.held.load(Ordering::SeqCst) > 0
    }

    // ── The index handle ────────────────────────────────────────────────

    fn slot(&self) -> MutexGuard<'_, Slot> {
        lock_ignoring_poison(&self.slot)
    }

    /// The index, opening it on first use; `None` = serve from the files.
    fn index(&self) -> Option<Arc<SqliteIndex>> {
        let mut slot = self.slot();
        if let Slot::Unopened { enabled } = *slot {
            *slot = self.open(enabled);
        }
        match &*slot {
            Slot::Open(index) => Some(Arc::clone(index)),
            _ => None,
        }
    }

    fn open(&self, enabled: bool) -> Slot {
        if !enabled {
            return Slot::Off;
        }
        match SqliteIndex::open(&self.index_dir) {
            Ok(index) => Slot::Open(Arc::new(index)),
            Err(_) => Slot::Off,
        }
    }

    /// Replace a broken or deleted index with a freshly opened one (which
    /// moves a corrupt database aside). Called with the write lock held.
    fn reopen(&self) -> Option<Arc<SqliteIndex>> {
        let mut slot = self.slot();
        *slot = self.open(true);
        match &*slot {
            Slot::Open(index) => Some(Arc::clone(index)),
            _ => None,
        }
    }

    fn db_path(&self) -> PathBuf {
        sqlite::db_path(&self.index_dir)
    }

    // ── Reads ───────────────────────────────────────────────────────────

    /// The index to serve a query from, or `None` to read the files. With
    /// `lock_free`, a racy index may be verified without the write lock; the
    /// caller must then [`IndexRead::confirm`] after reading.
    pub(super) fn for_read(&self, files: &FileStorage, lock_free: bool) -> Option<IndexRead> {
        #[cfg(test)]
        if super::super::test_hooks::index_disabled() {
            return None;
        }
        let index = self.index()?;
        let start = Instant::now();
        let mut delay = WAIT_MIN;
        // The meta a lock-free verify last found not to match, so a waiting
        // reader retries it only after the index changed.
        let mut mismatched: Option<IndexMeta> = None;
        loop {
            let (freshness, meta) = observe(files, &index);
            if freshness == Freshness::Trusted {
                return Some(IndexRead::plain(index));
            }
            if self.held_here() {
                // This process holds the lock (a write's hooks, or a sweep
                // on another thread): never wait on ourselves. A racy or
                // expired index is the operation's own view — its
                // `prepare_write` verified it — so only a stale one sends
                // the read to the files.
                let usable = freshness
                    != Freshness::Stale {
                        write_in_progress: false,
                    };
                return usable.then(|| IndexRead::plain(index));
            }
            if let (Freshness::Racy { expired: false }, Some(meta)) = (freshness, meta) {
                if lock_free && mismatched != Some(meta) {
                    if let Some(read) = self.verify_lock_free(files, &index, &meta) {
                        return Some(read);
                    }
                    mismatched = Some(meta);
                }
            }
            let readable_as_is = matches!(
                freshness,
                Freshness::Expired
                    | Freshness::Stale {
                        write_in_progress: true
                    }
            );
            // Taking the lock is how a reader takes over from a sweeper
            // that died: its sentinel stays, but the OS released its lock.
            match self.try_lock() {
                Ok(Some(lock)) => return self.refresh(files, index, &lock).map(IndexRead::plain),
                Ok(None) if readable_as_is => return Some(IndexRead::plain(index)),
                Ok(None) => {
                    if meta.is_some() && *lock_ignoring_poison(&self.gave_up_on) == meta {
                        return None;
                    }
                    // A sweep (or first-open build) commits soon and serves
                    // everyone; any other holder gets the short wait.
                    let sweeping = meta.is_some_and(|m| m.dir_mtime_ns == Some(SWEEPING_DIR_MTIME));
                    let (limit, min, max) = if sweeping {
                        (self.sweep_wait_limit(), SWEEP_WAIT_MIN, SWEEP_WAIT_MAX)
                    } else {
                        (WAIT_LIMIT, WAIT_MIN, WAIT_MAX)
                    };
                    let Some(left) = limit.checked_sub(start.elapsed()).filter(|d| !d.is_zero())
                    else {
                        if meta.is_some() {
                            *lock_ignoring_poison(&self.gave_up_on) = meta;
                        }
                        #[cfg(test)]
                        self.stats.give_ups.fetch_add(1, Ordering::Relaxed);
                        return None;
                    };
                    delay = delay.clamp(min, max);
                    #[cfg(test)]
                    self.stats.waits.fetch_add(1, Ordering::Relaxed);
                    std::thread::sleep(delay.min(left));
                    delay = (delay * 2).min(max);
                }
                Err(_) => return None,
            }
        }
    }

    /// How long a reader waits for another process's sweep.
    fn sweep_wait_limit(&self) -> Duration {
        #[cfg(test)]
        return *lock_ignoring_poison(&self.sweep_wait_limit);
        #[cfg(not(test))]
        SWEEP_WAIT_LIMIT
    }

    /// Verify a racy index without the write lock (see "Lock-free verify"
    /// in the module docs). `meta` is what classified it racy. `Some` = the
    /// listing matched: serve this read from the index, confirming after.
    fn verify_lock_free(
        &self,
        files: &FileStorage,
        index: &Arc<SqliteIndex>,
        meta: &IndexMeta,
    ) -> Option<IndexRead> {
        #[cfg(test)]
        self.stats
            .lock_free_verifies
            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        let observed = wall_clock_ns();
        let m = meta.dir_mtime_ns?;
        if files.dir_mtime_ns().ok()? != m {
            return None;
        }
        let (listed, stored) = rayon::join(|| files.list_file_ids(), || index.file_ids());
        let listed = listed.ok()??;
        let stored = stored.ok()?;
        let matches = listing_matches(&listed, &stored) && files.dir_mtime_ns().ok()? == m;
        if !matches {
            return None;
        }
        // Settle it for later readers once the observation is past the tick.
        if !is_racy(m, observed) {
            let _ = index.settle_dir(m, meta.dir_recorded_ns, observed);
        }
        Some(IndexRead {
            index: Arc::clone(index),
            verified: Some((m, meta.last_sweep_ns)),
        })
    }

    /// Bring the index in line with the files unless it already is. Called
    /// with the write lock held; `None` = the files must serve this read.
    fn refresh(
        &self,
        files: &FileStorage,
        index: Arc<SqliteIndex>,
        _lock: &LockGuard,
    ) -> Option<Arc<SqliteIndex>> {
        // Deleted under us: rebuild it in a new file rather than keep
        // caching into an unlinked one.
        let index = if self.db_path().exists() {
            index
        } else {
            self.reopen()?
        };
        let outcome = match freshness(files, &index) {
            Freshness::Trusted => return Some(index),
            Freshness::Racy { expired: false } => self.verify(files, &index),
            _ => self.sweep(files, &index),
        };
        match outcome {
            Ok(()) => Some(index),
            Err(SweepError::Files) => None,
            Err(SweepError::Index) => {
                // Damaged: reset in place, or (not even a database) reopen,
                // which moves the file aside; then rebuild.
                let index = if index.reset().is_ok() {
                    index
                } else {
                    self.reopen()?
                };
                self.sweep(files, &index).ok().map(|()| index)
            }
        }
    }

    /// Settle a racy index: if the listing still matches the rows (by name
    /// and file id) and the directory did not change meanwhile, re-record
    /// its mtime with a fresh observation time; otherwise sweep.
    fn verify(&self, files: &FileStorage, index: &SqliteIndex) -> SweepResult {
        #[cfg(test)]
        self.stats
            .verifies
            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        let observed = wall_clock_ns();
        let before = files.dir_mtime_ns().map_err(|_| SweepError::Files)?;
        let recorded = index.meta().map_err(|_| SweepError::Index)?.dir_mtime_ns;
        // The listing and the index read are independent: overlap them.
        let (listed, stored) = rayon::join(|| files.list_file_ids(), || index.file_ids());
        let Some(listed) = listed.map_err(|_| SweepError::Files)? else {
            return self.sweep(files, index);
        };
        let stored = stored.map_err(|_| SweepError::Index)?;
        let unchanged = recorded == Some(before)
            && listing_matches(&listed, &stored)
            && files.dir_mtime_ns().ok() == Some(before);
        if !unchanged {
            return self.sweep(files, index);
        }
        index
            .apply(&IndexChanges {
                dir_mtime_ns: Some(before),
                dir_recorded_ns: Some(observed),
                ..IndexChanges::default()
            })
            .map_err(|_| SweepError::Index)
    }

    /// Sweep: bring every row in line with its file (see the README).
    fn sweep(&self, files: &FileStorage, index: &SqliteIndex) -> SweepResult {
        #[cfg(test)]
        self.stats
            .sweeps
            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        // Untrusted while it runs: a lock-free verify that overlaps it can't
        // settle the index, nor confirm a read, over rows from this sweep.
        // The sentinel also tells readers in other processes to wait for it.
        index
            .apply(&IndexChanges {
                dir_mtime_ns: Some(SWEEPING_DIR_MTIME),
                ..IndexChanges::default()
            })
            .map_err(|_| SweepError::Index)?;
        let outcome = self.sweep_rows(files, index);
        if outcome.is_err() {
            // Still stale, but no longer worth waiting for (the caller may
            // keep the lock for a whole write operation). Best effort: an
            // index failure is repaired by the caller.
            let _ = index.apply(&IndexChanges {
                dir_mtime_ns: Some(ABANDONED_DIR_MTIME),
                ..IndexChanges::default()
            });
        }
        outcome
    }

    /// The body of [`Self::sweep`], after the sentinel is committed.
    fn sweep_rows(&self, files: &FileStorage, index: &SqliteIndex) -> SweepResult {
        let observed = wall_clock_ns();
        let dir_mtime = files.dir_mtime_ns().map_err(|_| SweepError::Files)?;
        let (listed, stored) = rayon::join(|| files.scan(), || index.fingerprints());
        let listed = listed.map_err(|_| SweepError::Files)?;
        let mut stored = stored.map_err(|_| SweepError::Index)?;
        let mut changed = Vec::new();
        for (id, fingerprint) in listed {
            if stored.remove(&id) != Some(fingerprint) {
                changed.push((id, fingerprint));
            }
        }
        // Rows the listing did not show. A listing racing a rename can miss
        // a file that exists throughout, so only a `stat` saying it's gone
        // deletes a row; a file that is there is re-read like a changed one.
        let unlisted: Vec<String> = stored.into_keys().collect();
        let mut gone = Vec::new();
        for (id, fingerprint) in unlisted
            .into_par_iter()
            .map(|id| files.fingerprint_of(&id).map(|fp| (id, fp)))
            .collect::<Result<Vec<_>>>()
            .map_err(|_| SweepError::Files)?
        {
            match fingerprint {
                Some(fingerprint) => changed.push((id, fingerprint)),
                None => gone.push(id),
            }
        }

        // Read and commit in chunks to bound memory; meta goes with the last.
        let chunks: Vec<&[(String, Fingerprint)]> = if changed.is_empty() {
            vec![&[]]
        } else {
            changed.chunks(SCAN_CHUNK).collect()
        };
        let mut deletes: Vec<&str> = gone.iter().map(String::as_str).collect();
        let last = chunks.len() - 1;
        for (n, chunk) in chunks.into_iter().enumerate() {
            let ids: Vec<String> = chunk.iter().map(|(id, _)| id.clone()).collect();
            let mut changes = IndexChanges {
                deletes: std::mem::take(&mut deletes),
                ..IndexChanges::default()
            };
            for ((id, fingerprint), text) in chunk.iter().zip(files.read_many(&ids)) {
                match text {
                    Ok(Some(text)) => changes.upserts.push(IndexRow {
                        id: id.as_str(),
                        doc: Cow::Owned(text),
                        fingerprint: if is_racy(fingerprint.mtime_ns, observed) {
                            smudged(*fingerprint)
                        } else {
                            *fingerprint
                        },
                    }),
                    // Vanished since the listing.
                    Ok(None) => changes.deletes.push(id.as_str()),
                    Err(_) => return Err(SweepError::Files),
                }
            }
            if n == last {
                changes.dir_mtime_ns = Some(dir_mtime);
                changes.dir_recorded_ns = Some(observed);
                changes.swept_at_ns = Some(clock_ns());
            }
            index.apply(&changes).map_err(|_| SweepError::Index)?;
        }
        Ok(())
    }

    // ── Writes (caller holds the write lock) ────────────────────────────

    /// Sweep (or verify) first if the index is not trusted, so a write never
    /// records a directory mtime over unswept external changes. Uses the
    /// caller's lock.
    pub(super) fn prepare_write(&self, files: &FileStorage, lock: &LockGuard) {
        if let Some(index) = self.index() {
            self.refresh(files, index, lock);
        }
    }

    /// Write the files, keeping the index current (see the README). Index
    /// failures never fail a write; they leave the index untrusted.
    pub(super) fn write_batch(
        &self,
        files: &FileStorage,
        _lock: &LockGuard,
        writes: &[StorageWrite<'_>],
        durable: bool,
    ) -> Vec<Result<()>> {
        let index = if writes.is_empty() {
            None
        } else {
            self.index()
        };
        let Some(index) = index else {
            return files
                .write_batch(writes, durable, false)
                .into_iter()
                .map(|outcome| outcome.map(drop))
                .collect();
        };

        // Only an index in line with the directory is a consistent pre-batch
        // snapshot that readers may use while the files change, and only then
        // may the batch record the directory mtime afterwards. That record
        // vouches for the directory only as of *before* the batch (an
        // external change landing during it is hidden behind our renames),
        // so it is always racy: the next read verifies.
        let in_line = match (files.dir_mtime_ns(), index.meta()) {
            (Ok(dir), Ok(meta)) => !meta.write_in_progress && meta.dir_mtime_ns == Some(dir),
            _ => false,
        };
        let marked = in_line && index.set_write_in_progress().is_ok();
        let observed = wall_clock_ns();
        let outcomes = files.write_batch(writes, durable, true);
        let dir_after = files.dir_mtime_ns().ok();

        let mut complete = true;
        let mut changes = IndexChanges::default();
        let results: Vec<Result<()>> = writes
            .iter()
            .zip(outcomes)
            .map(|(write, outcome)| {
                match (*write, outcome) {
                    (
                        StorageWrite::Put { id, .. },
                        Ok(Some(Written {
                            text,
                            fingerprint: Some(fingerprint),
                        })),
                    ) => changes.upserts.push(IndexRow {
                        id,
                        doc: Cow::Owned(text),
                        // Just renamed into place: racy by definition.
                        fingerprint: smudged(fingerprint),
                    }),
                    (StorageWrite::Delete { id }, Ok(_)) => changes.deletes.push(id),
                    // Failed, or written without a fingerprint: the next
                    // sweep sorts it out.
                    (_, Err(e)) => {
                        complete = false;
                        return Err(e);
                    }
                    (StorageWrite::Put { .. }, Ok(_)) => complete = false,
                }
                Ok(())
            })
            .collect();
        if marked && complete {
            if let Some(dir_after) = dir_after {
                changes.dir_mtime_ns = Some(dir_after);
                changes.dir_recorded_ns = Some(observed);
            }
        }
        if index.apply(&changes).is_err() {
            // Leave it untrusted (the directory changed, the mtime was not
            // recorded) and clear `write_in_progress`, so readers don't take
            // the stale index for a pre-batch snapshot.
            if index.apply(&IndexChanges::default()).is_err() {
                let _ = index.reset();
            }
        }
        results
    }

    // ── Counters ────────────────────────────────────────────────────────

    /// Record a query served by the index (a relaxed increment).
    pub(super) fn count_index_read(&self) {
        self.index_reads.fetch_add(1, Ordering::Relaxed);
    }

    /// How many queries the index served on this instance.
    pub(super) fn index_reads(&self) -> u64 {
        self.index_reads.load(Ordering::Relaxed)
    }

    // ── Test support ────────────────────────────────────────────────────

    #[cfg(test)]
    pub(super) fn sweeps(&self) -> u64 {
        self.stats.sweeps.load(std::sync::atomic::Ordering::Relaxed)
    }

    #[cfg(test)]
    pub(super) fn verifies(&self) -> u64 {
        self.stats
            .verifies
            .load(std::sync::atomic::Ordering::Relaxed)
    }

    #[cfg(test)]
    pub(super) fn give_ups(&self) -> u64 {
        self.stats.give_ups.load(Ordering::Relaxed)
    }

    #[cfg(test)]
    pub(super) fn waits(&self) -> u64 {
        self.stats.waits.load(Ordering::Relaxed)
    }

    #[cfg(test)]
    pub(super) fn lock_free_verifies(&self) -> u64 {
        self.stats
            .lock_free_verifies
            .load(std::sync::atomic::Ordering::Relaxed)
    }

    /// The open index, if any (without opening it).
    #[cfg(test)]
    pub(super) fn open_index(&self) -> Option<Arc<SqliteIndex>> {
        match &*self.slot() {
            Slot::Open(index) => Some(Arc::clone(index)),
            _ => None,
        }
    }
}

impl Drop for LockGuard {
    fn drop(&mut self) {
        // Release before un-counting, so a reader in this process that sees
        // the count drop to zero never waits on a lock about to be freed.
        let _ = FileExt::unlock(&self.file);
        self.held.fetch_sub(1, Ordering::SeqCst);
    }
}

/// An index chosen to serve one read.
pub(super) struct IndexRead {
    pub(super) index: Arc<SqliteIndex>,
    /// Set when a lock-free verify vouched for it: the `dir_mtime_ns` and
    /// `last_sweep_ns` it verified against.
    verified: Option<(i64, Option<i64>)>,
}

impl IndexRead {
    fn plain(index: Arc<SqliteIndex>) -> Self {
        Self {
            index,
            verified: None,
        }
    }

    /// After reading: whether the result stands. A lock-free verified read
    /// fails if a sweep started or committed meanwhile (its rows come from a
    /// listing the verify never compared), or the directory mtime it
    /// verified was replaced; the caller then reads again.
    pub(super) fn confirm(&self) -> bool {
        let Some((m, swept)) = self.verified else {
            return true;
        };
        self.index
            .meta()
            .is_ok_and(|meta| meta.dir_mtime_ns == Some(m) && meta.last_sweep_ns == swept)
    }
}

/// Whether a listing's (name, file id) pairs are exactly the stored rows'.
/// Compared as sets: a listing racing a rename may repeat a name as well as
/// miss one, and a repeat must not make up for a miss. A file id of 0 (none
/// known) never matches.
fn listing_matches(listed: &[(String, u64)], stored: &HashMap<String, u64>) -> bool {
    if listed.len() != stored.len() {
        return false;
    }
    let mut seen = HashSet::with_capacity(listed.len());
    listed.iter().all(|(id, file_id)| {
        *file_id != 0 && stored.get(id) == Some(file_id) && seen.insert(id.as_str())
    })
}

/// Classify the index against the directory: one `stat` plus one meta read.
fn freshness(files: &FileStorage, index: &SqliteIndex) -> Freshness {
    observe(files, index).0
}

/// [`freshness`], plus the meta it was judged on.
fn observe(files: &FileStorage, index: &SqliteIndex) -> (Freshness, Option<IndexMeta>) {
    match (files.dir_mtime_ns(), index.meta()) {
        (Ok(dir), Ok(meta)) => (classify(&meta, dir, clock_ns()), Some(meta)),
        _ => (
            Freshness::Stale {
                write_in_progress: false,
            },
            None,
        ),
    }
}

fn classify(meta: &IndexMeta, dir_mtime_ns: i64, now_ns: i64) -> Freshness {
    if meta.write_in_progress || meta.dir_mtime_ns != Some(dir_mtime_ns) {
        return Freshness::Stale {
            write_in_progress: meta.write_in_progress,
        };
    }
    let interval = i64::try_from(SWEEP_INTERVAL.as_nanos()).unwrap_or(i64::MAX);
    let expired = !meta
        .last_sweep_ns
        .is_some_and(|swept| (0..interval).contains(&now_ns.saturating_sub(swept)));
    let settled = meta
        .dir_recorded_ns
        .is_some_and(|observed| !is_racy(dir_mtime_ns, observed));
    match (settled, expired) {
        (false, expired) => Freshness::Racy { expired },
        (true, true) => Freshness::Expired,
        (true, false) => Freshness::Trusted,
    }
}

/// How long after an mtime was set an observation must be to rule out a
/// later change in the same filesystem clock tick: [`RACY_WINDOW`], or
/// [`COARSE_RACY_WINDOW`] when the mtime falls on a whole second (a
/// filesystem with 1–2 s timestamps, such as FAT or HFS+).
fn racy_window(mtime_ns: i64) -> i64 {
    let window = if mtime_ns % NS_PER_SEC == 0 {
        COARSE_RACY_WINDOW
    } else {
        RACY_WINDOW
    };
    i64::try_from(window.as_nanos()).unwrap_or(i64::MAX)
}

/// Whether a change after an observation at `observed_ns` (wall clock)
/// could still carry the same `mtime_ns`.
fn is_racy(mtime_ns: i64, observed_ns: i64) -> bool {
    observed_ns.saturating_sub(mtime_ns) < racy_window(mtime_ns)
}

fn smudged(fingerprint: Fingerprint) -> Fingerprint {
    Fingerprint {
        mtime_ns: SMUDGED_MTIME,
        ..fingerprint
    }
}

fn wall_clock_ns() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |d| i64::try_from(d.as_nanos()).unwrap_or(i64::MAX))
}

/// "Now" for the periodic-sweep check (tests may shift it).
fn clock_ns() -> i64 {
    let now = wall_clock_ns();
    #[cfg(test)]
    let now = now.saturating_add(
        i64::try_from(super::super::test_hooks::clock_offset().as_nanos()).unwrap_or(i64::MAX),
    );
    now
}

fn lock_ignoring_poison<T>(mutex: &Mutex<T>) -> MutexGuard<'_, T> {
    mutex.lock().unwrap_or_else(|p| p.into_inner())
}

/// The process-wide count of write-lock guards held on registry directory
/// `dir`, shared by every [`IndexSync`] for it. An flock on a second
/// descriptor conflicts with one this process already holds, so a reader
/// must know about every in-process holder — not just its own instance's —
/// to never wait on itself.
fn held_counter(dir: &Path) -> Arc<AtomicUsize> {
    static COUNTERS: Mutex<Vec<(PathBuf, Weak<AtomicUsize>)>> = Mutex::new(Vec::new());
    let key = dir.canonicalize().unwrap_or_else(|_| dir.to_path_buf());
    let mut counters = COUNTERS.lock().unwrap_or_else(|p| p.into_inner());
    counters.retain(|(_, counter)| counter.strong_count() > 0);
    if let Some(counter) = counters
        .iter()
        .find(|(path, _)| *path == key)
        .and_then(|(_, counter)| counter.upgrade())
    {
        return counter;
    }
    let counter = Arc::new(AtomicUsize::new(0));
    counters.push((key, Arc::downgrade(&counter)));
    counter
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::types::{CodeUnit, Kind, ObjectType, SourceMetadata, TargetMetadata};
    use crate::registry::storage::Storage;
    use crate::registry::{test_hooks, ChangeType, CodeUnitChange, CodeUnitRegistry};
    use crate::registry::{FindOptions, RegistryHook, WriteOptions};
    use serde_json::{json, Value};
    use std::sync::atomic::AtomicU64;

    // ── Fixtures ────────────────────────────────────────────────────────

    fn unit(id: &str, schema: &str) -> CodeUnit {
        CodeUnit {
            id: Some(id.to_string()),
            kind: Some(Kind::DatabaseObject),
            source: Some(SourceMetadata {
                object_type: Some(ObjectType::Table),
                database: Some("DB".into()),
                schema: Some(schema.into()),
                name: Some(id.to_uppercase()),
                ..Default::default()
            }),
            target: Some(TargetMetadata {
                object_type: Some(ObjectType::Table),
                name: Some(id.to_uppercase()),
                ..Default::default()
            }),
            ..Default::default()
        }
    }

    /// A document as an external tool (git) would write it.
    fn doc_text(id: &str, schema: &str) -> String {
        serde_json::to_string_pretty(&unit(id, schema)).unwrap() + "\n"
    }

    /// The registry at `root`, with the index enabled whatever
    /// `SCAI_REGISTRY_INDEX` says (these tests are about the index).
    fn open_indexed(root: &Path) -> CodeUnitRegistry {
        let dir = root.join(crate::registry::REGISTRY_DIR);
        CodeUnitRegistry::with_storage(root.to_path_buf(), Storage::with_index(&dir, true))
    }

    /// A new registry at a temp dir, with the index enabled.
    fn new_registry() -> (tempfile::TempDir, CodeUnitRegistry) {
        let dir = tempfile::tempdir().unwrap();
        drop(CodeUnitRegistry::init(dir.path()).unwrap());
        let registry = open_indexed(dir.path());
        (dir, registry)
    }

    /// A registry with `n` units spread over schemas `S0`..`S3`.
    fn registry_with(n: usize) -> (tempfile::TempDir, CodeUnitRegistry) {
        let (dir, registry) = new_registry();
        let mut units: Vec<CodeUnit> = (0..n)
            .map(|i| unit(&format!("u{i:03}"), &format!("S{}", i % 4)))
            .collect();
        let result = registry.create_batch(&mut units, None).unwrap();
        assert!(result.failed.is_empty(), "{:?}", result.failed);
        (dir, registry)
    }

    fn sync(registry: &CodeUnitRegistry) -> &IndexSync {
        &registry.storage.index
    }

    fn files(registry: &CodeUnitRegistry) -> &FileStorage {
        &registry.storage.files
    }

    fn index(registry: &CodeUnitRegistry) -> Arc<SqliteIndex> {
        sync(registry).index().expect("index enabled")
    }

    fn current(registry: &CodeUnitRegistry) -> Freshness {
        freshness(files(registry), &index(registry))
    }

    fn put_external(registry: &CodeUnitRegistry, id: &str, schema: &str) {
        registry
            .storage
            .put_raw_text(id, &doc_text(id, schema))
            .unwrap();
    }

    fn find(registry: &CodeUnitRegistry, filter: Option<&str>) -> Vec<Value> {
        let options = FindOptions {
            filter,
            ..FindOptions::default()
        };
        let mut found: Vec<Value> = registry
            .find_all(options)
            .unwrap()
            .into_iter()
            .map(|u| serde_json::to_value(u).unwrap())
            .collect();
        found.sort_by_key(|v| v["id"].as_str().unwrap_or_default().to_string());
        found
    }

    fn ids(found: &[Value]) -> Vec<&str> {
        found.iter().map(|v| v["id"].as_str().unwrap()).collect()
    }

    /// Read through the index (asserting it served the read) and compare
    /// with a files-only read.
    fn check(registry: &CodeUnitRegistry, filter: Option<&str>, label: &str) -> Vec<Value> {
        let before = sync(registry).index_reads();
        let got = find(registry, filter);
        assert!(
            sync(registry).index_reads() > before,
            "{label}: the index did not serve {filter:?}"
        );
        let expected = test_hooks::without_index(|| find(registry, filter));
        assert_eq!(ids(&got), ids(&expected), "{label}: {filter:?}");
        assert_eq!(got, expected, "{label}: {filter:?}");
        got
    }

    /// Let the racy window pass, then read once: the index is trusted after.
    fn settle(registry: &CodeUnitRegistry) {
        std::thread::sleep(RACY_WINDOW + Duration::from_millis(20));
        find(registry, None);
        assert_eq!(current(registry), Freshness::Trusted);
    }

    fn set_mtime(path: &Path, mtime_ns: i64) {
        let time = UNIX_EPOCH + Duration::from_nanos(u64::try_from(mtime_ns).unwrap());
        File::open(path).unwrap().set_modified(time).unwrap();
    }

    // ── Classification ──────────────────────────────────────────────────

    #[test]
    fn classify_states() {
        let ms = 1_000_000;
        let m = 1_700_000_000_123_456_789; // not on a whole second
        let now = m + 5_000 * ms;
        let meta =
            |dir: Option<i64>, observed: Option<i64>, swept: Option<i64>, wip: bool| IndexMeta {
                dir_mtime_ns: dir,
                dir_recorded_ns: observed,
                last_sweep_ns: swept,
                write_in_progress: wip,
            };
        let settled = Some(m + 150 * ms);
        let swept = Some(now - 1_000 * ms);
        assert_eq!(
            classify(&meta(Some(m), settled, swept, false), m, now),
            Freshness::Trusted
        );
        assert_eq!(
            classify(&IndexMeta::default(), m, now),
            Freshness::Stale {
                write_in_progress: false
            }
        );
        assert_eq!(
            classify(&meta(Some(m - 1), settled, swept, false), m, now),
            Freshness::Stale {
                write_in_progress: false
            }
        );
        assert_eq!(
            classify(&meta(Some(m), settled, swept, true), m, now),
            Freshness::Stale {
                write_in_progress: true
            }
        );
        // Observed within the racy window of the mtime, or never.
        for observed in [Some(m), Some(m + 99 * ms), Some(m - ms), None] {
            assert_eq!(
                classify(&meta(Some(m), observed, swept, false), m, now),
                Freshness::Racy { expired: false },
                "{observed:?}"
            );
        }
        assert_eq!(
            classify(&meta(Some(m), Some(m), None, false), m, now),
            Freshness::Racy { expired: true }
        );
        // The periodic sweep: due after the interval, or for a sweep "in the future".
        let interval = SWEEP_INTERVAL.as_nanos() as i64;
        for swept in [None, Some(now - interval), Some(now + ms)] {
            assert_eq!(
                classify(&meta(Some(m), settled, swept, false), m, now),
                Freshness::Expired,
                "{swept:?}"
            );
        }
        // Whole-second mtimes (FAT, HFS+) get a 2 s window.
        let whole = 1_700_000_000 * NS_PER_SEC;
        assert_eq!(
            classify(
                &meta(Some(whole), Some(whole + 1_500 * ms), Some(whole), false),
                whole,
                whole + 1_600 * ms
            ),
            Freshness::Racy { expired: false }
        );
    }

    // ── Reader paths ────────────────────────────────────────────────────

    #[test]
    fn trusted_reads_do_no_sweep_or_verify() {
        let (_dir, registry) = registry_with(20);
        settle(&registry);
        let s = sync(&registry);
        let (sweeps, verifies, reads) = (s.sweeps(), s.verifies(), s.index_reads());
        for _ in 0..20 {
            check(&registry, Some("source.schema = 'S1'"), "trusted");
            check(&registry, None, "trusted");
        }
        assert_eq!((s.sweeps(), s.verifies()), (sweeps, verifies));
        assert!(s.index_reads() >= reads + 40);
    }

    #[test]
    fn a_library_write_is_verified_once_then_trusted() {
        let (_dir, registry) = registry_with(8);
        settle(&registry);
        registry.create(&mut unit("new", "S1"), None).unwrap();
        assert_eq!(current(&registry), Freshness::Racy { expired: false });
        let s = sync(&registry);
        std::thread::sleep(RACY_WINDOW + Duration::from_millis(20));
        let (sweeps, verifies, lock_free) = (s.sweeps(), s.verifies(), s.lock_free_verifies());
        assert!(ids(&check(
            &registry,
            Some("source.schema = 'S1'"),
            "after write"
        ))
        .contains(&"new"));
        assert_eq!(
            (s.sweeps(), s.verifies(), s.lock_free_verifies()),
            (sweeps, verifies, lock_free + 1)
        );
        assert_eq!(current(&registry), Freshness::Trusted);
        check(&registry, None, "settled");
        assert_eq!(
            (s.sweeps(), s.verifies(), s.lock_free_verifies()),
            (sweeps, verifies, lock_free + 1)
        );
    }

    #[test]
    fn external_add_replace_delete_and_rename_are_detected() {
        let (_dir, registry) = registry_with(12);
        let path = |id: &str| files(&registry).path_for(id);
        // Each change right after a library write, and again on a settled index.
        for settled in [false, true] {
            let tag = if settled { "settled" } else { "fresh" };
            let touch = |registry: &CodeUnitRegistry| {
                if settled {
                    settle(registry);
                } else {
                    registry
                        .update("u000", &[("target.name", json!(tag))], None)
                        .unwrap();
                }
            };
            touch(&registry);
            put_external(&registry, &format!("add-{tag}"), "S1");
            let found = check(&registry, Some("source.schema = 'S1'"), "add");
            assert!(ids(&found).contains(&format!("add-{tag}").as_str()));

            touch(&registry);
            put_external(&registry, &format!("add-{tag}"), "S2");
            let found = check(&registry, Some("source.schema = 'S2'"), "replace");
            assert!(ids(&found).contains(&format!("add-{tag}").as_str()));

            touch(&registry);
            std::fs::remove_file(path(&format!("add-{tag}"))).unwrap();
            let found = check(&registry, None, "delete");
            assert!(!ids(&found).contains(&format!("add-{tag}").as_str()));

            // A pure rename (`git mv`): same inode, size and mtime, new key.
            let id_free = serde_json::to_string_pretty(&json!({
                "kind": "databaseObject",
                "source": { "schema": "S3", "name": "MOVED" }
            }))
            .unwrap();
            registry
                .storage
                .put_raw_text(&format!("before-{tag}"), &id_free)
                .unwrap();
            touch(&registry);
            std::fs::rename(
                path(&format!("before-{tag}")),
                path(&format!("after-{tag}")),
            )
            .unwrap();
            let found = check(&registry, Some("source.schema = 'S3'"), "rename");
            assert!(ids(&found).contains(&format!("after-{tag}").as_str()));
            assert!(!ids(&found).contains(&format!("before-{tag}").as_str()));
        }
    }

    /// The race behind the racy window: a file added in the same clock tick
    /// as a library write's bookkeeping leaves the directory mtime as
    /// recorded. Forced here by setting the directory mtime back.
    #[test]
    fn same_tick_add_after_a_write_is_seen_by_the_next_read() {
        let (_dir, registry) = registry_with(6);
        let dir = files(&registry).dir().to_path_buf();
        registry.create(&mut unit("lib", "S1"), None).unwrap();
        let recorded = index(&registry).meta().unwrap().dir_mtime_ns.unwrap();
        put_external(&registry, "sneaky", "S1");
        set_mtime(&dir, recorded);
        assert_eq!(files(&registry).dir_mtime_ns().unwrap(), recorded);

        let s = sync(&registry);
        let (sweeps, verifies) = (s.sweeps(), s.verifies());
        let found = check(&registry, Some("source.schema = 'S1'"), "same tick");
        assert!(ids(&found).contains(&"sneaky"), "{:?}", ids(&found));
        assert!(s.verifies() > verifies, "a racy index is verified");
        assert!(s.sweeps() > sweeps, "the verify found the difference");

        // Control: had the mtime been observed well after it was set, the
        // same masked add would be invisible until the periodic sweep.
        settle(&registry);
        let recorded = index(&registry).meta().unwrap().dir_mtime_ns.unwrap();
        put_external(&registry, "masked", "S1");
        set_mtime(&dir, recorded);
        let found = find(&registry, Some("source.schema = 'S1'"));
        assert!(!ids(&found).contains(&"masked"));
        let found = test_hooks::with_clock_offset(SWEEP_INTERVAL + Duration::from_secs(1), || {
            find(&registry, Some("source.schema = 'S1'"))
        });
        assert!(ids(&found).contains(&"masked"));
    }

    #[test]
    fn in_place_edit_is_seen_by_the_periodic_sweep_only() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        let path = files(&registry).path_for("u001");
        std::fs::write(&path, doc_text("u001", "EDITED")).unwrap();
        let filter = Some("source.schema = 'EDITED'");
        assert!(find(&registry, filter).is_empty(), "not seen immediately");
        let sweeps = sync(&registry).sweeps();
        let found = test_hooks::with_clock_offset(SWEEP_INTERVAL + Duration::from_secs(1), || {
            check(&registry, filter, "periodic")
        });
        assert_eq!(ids(&found), ["u001"]);
        assert_eq!(sync(&registry).sweeps(), sweeps + 1);
    }

    /// An in-place edit of the same size in the same tick as a library
    /// write leaves the file's fingerprint as stat'd after the write; only
    /// the smudged row makes the periodic sweep re-read it.
    #[test]
    fn same_tick_in_place_edit_after_a_write_is_caught_by_smudging() {
        let (_dir, registry) = registry_with(6);
        registry.create(&mut unit("lib", "S1"), None).unwrap();
        let fingerprint = files(&registry).fingerprint_of("lib").unwrap().unwrap();
        let path = files(&registry).path_for("lib");
        let edited = std::fs::read_to_string(&path)
            .unwrap()
            .replace("\"S1\"", "\"S9\"");
        std::fs::write(&path, edited).unwrap();
        set_mtime(&path, fingerprint.mtime_ns);
        assert_eq!(
            files(&registry).fingerprint_of("lib").unwrap().unwrap(),
            fingerprint
        );
        settle(&registry);
        let found = test_hooks::with_clock_offset(SWEEP_INTERVAL + Duration::from_secs(1), || {
            check(&registry, Some("source.schema = 'S9'"), "smudged")
        });
        assert_eq!(ids(&found), ["lib"]);
    }

    #[test]
    fn crash_mid_write_leaves_the_next_reader_to_sweep() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        {
            // A writer that died after marking its batch and renaming a file.
            let _lock = registry.acquire_lock().unwrap();
            index(&registry).set_write_in_progress().unwrap();
            put_external(&registry, "half", "S1");
        }
        assert_eq!(
            current(&registry),
            Freshness::Stale {
                write_in_progress: true
            }
        );
        let sweeps = sync(&registry).sweeps();
        let found = check(&registry, Some("source.schema = 'S1'"), "after crash");
        assert!(ids(&found).contains(&"half"));
        assert_eq!(sync(&registry).sweeps(), sweeps + 1);
        assert!(!index(&registry).meta().unwrap().write_in_progress);
    }

    /// The write lock taken the way another process would: a separate
    /// descriptor this process's guard count knows nothing about.
    fn foreign_lock(registry: &CodeUnitRegistry) -> File {
        let file = File::create(&sync(registry).lock_path).unwrap();
        file.lock_exclusive().unwrap();
        file
    }

    #[test]
    fn reader_during_a_writers_batch_reads_the_pre_batch_snapshot() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        let before = find(&registry, Some("source.schema = 'S1'"));
        let lock = foreign_lock(&registry);
        index(&registry).set_write_in_progress().unwrap();
        put_external(&registry, "mid-batch", "S1");

        let (reads, sweeps) = (sync(&registry).index_reads(), sync(&registry).sweeps());
        let waits = sync(&registry).waits();
        let during = find(&registry, Some("source.schema = 'S1'"));
        assert_eq!(sync(&registry).waits(), waits, "must not wait");
        assert_eq!(during, before, "the pre-batch snapshot");
        assert!(sync(&registry).index_reads() > reads);
        assert_eq!(sync(&registry).sweeps(), sweeps);

        drop(lock);
        let after = check(&registry, Some("source.schema = 'S1'"), "after batch");
        assert!(ids(&after).contains(&"mid-batch"));
    }

    #[test]
    fn reader_waits_for_a_busy_lock_then_falls_back_to_files() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        put_external(&registry, "pending", "S1");

        // Held for good: the reader gives up after the wait limit.
        let lock = foreign_lock(&registry);
        let s = sync(&registry);
        let (reads, give_ups) = (s.index_reads(), s.give_ups());
        let start = Instant::now();
        let found = find(&registry, Some("source.schema = 'S1'"));
        let waited = start.elapsed();
        assert!(ids(&found).contains(&"pending"), "files are the truth");
        assert!(waited >= WAIT_LIMIT, "{waited:?}");
        // Once: the query's fallback from candidates to a full load does
        // not wait a second time.
        assert_eq!(s.give_ups(), give_ups + 1);
        assert_eq!(s.index_reads(), reads, "served by files");
        // Nothing changed since: this instance doesn't wait again.
        let waits = s.waits();
        find(&registry, Some("source.schema = 'S1'"));
        assert_eq!(s.waits(), waits, "no new wait");
        assert_eq!(s.index_reads(), reads, "served by files");

        // Released while waiting: the reader takes the lock and sweeps. (A
        // new instance, which has not given up on this state yet.)
        let other = open_indexed(registry.root());
        let release = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(100));
            drop(lock);
        });
        let found = check(&other, Some("source.schema = 'S1'"), "after release");
        assert!(ids(&found).contains(&"pending"));
        release.join().unwrap();
        check(&registry, Some("source.schema = 'S1'"), "lock free again");
    }

    /// Commit the sweep sentinel, as another process's sweep (or first-open
    /// build) does first.
    fn mark_sweeping(registry: &CodeUnitRegistry) {
        index(registry)
            .apply(&IndexChanges {
                dir_mtime_ns: Some(SWEEPING_DIR_MTIME),
                ..IndexChanges::default()
            })
            .unwrap();
    }

    /// A reader meeting another process's sweep waits past [`WAIT_LIMIT`]
    /// for it, and is served by the index as soon as it commits — before
    /// the sweeper even releases the lock.
    #[test]
    fn reader_waits_for_another_processs_sweep_and_reads_the_index() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        put_external(&registry, "pending", "S1");
        let lock = foreign_lock(&registry);
        mark_sweeping(&registry);
        let s = sync(&registry);
        let (reads, sweeps) = (s.index_reads(), s.sweeps());
        let sweep_for = WAIT_LIMIT + Duration::from_millis(500);
        let released = std::sync::atomic::AtomicBool::new(false);
        let (found, waited) = std::thread::scope(|scope| {
            scope.spawn(|| {
                // The other process's sweep (no guard: this process doesn't
                // count as holding the lock), then a slow release.
                std::thread::sleep(sweep_for);
                assert!(s.sweep_rows(files(&registry), &index(&registry)).is_ok());
                std::thread::sleep(Duration::from_secs(1));
                released.store(true, Ordering::SeqCst);
                drop(lock);
            });
            let start = Instant::now();
            let found = find(&registry, Some("source.schema = 'S1'"));
            assert!(
                !released.load(Ordering::SeqCst),
                "served before the release"
            );
            (found, start.elapsed())
        });
        assert!(waited >= sweep_for, "{waited:?}");
        assert!(ids(&found).contains(&"pending"), "{:?}", ids(&found));
        assert_eq!(s.index_reads(), reads + 1, "served by the index");
        assert_eq!(s.sweeps(), sweeps, "the reader did not sweep itself");
    }

    /// A sentinel left by a sweeper that died: its lock is gone, so the
    /// next reader takes over at once rather than wait for it.
    #[test]
    fn stale_sweep_sentinel_without_a_lock_holder_is_taken_over() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        put_external(&registry, "pending", "S1");
        mark_sweeping(&registry);
        let s = sync(&registry);
        let (sweeps, waits) = (s.sweeps(), s.waits());
        let found = check(&registry, Some("source.schema = 'S1'"), "taken over");
        assert!(ids(&found).contains(&"pending"));
        assert_eq!(s.sweeps(), sweeps + 1, "the reader swept");
        assert_eq!(s.waits(), waits, "without waiting");
    }

    /// A sweep that never commits: readers wait [`SWEEP_WAIT_LIMIT`] (here
    /// shortened), once per state, then read the files.
    #[test]
    fn sweep_wait_is_capped() {
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        let limit = WAIT_LIMIT + Duration::from_millis(500);
        *sync(&registry).sweep_wait_limit.lock().unwrap() = limit;
        put_external(&registry, "pending", "S1");
        let lock = foreign_lock(&registry);
        mark_sweeping(&registry);
        let s = sync(&registry);
        let (reads, give_ups) = (s.index_reads(), s.give_ups());
        let start = Instant::now();
        let found = find(&registry, Some("source.schema = 'S1'"));
        let waited = start.elapsed();
        assert!(ids(&found).contains(&"pending"), "files are the truth");
        assert!(waited >= limit, "{waited:?}");
        assert_eq!(s.give_ups(), give_ups + 1, "one wait per query");
        assert_eq!(s.index_reads(), reads, "served by files");
        // Still the same sweep: later reads don't wait for it again.
        let waits = s.waits();
        find(&registry, None);
        assert_eq!(s.waits(), waits, "no new wait");
        assert_eq!(s.index_reads(), reads, "served by files");
        drop(lock);
        check(&registry, Some("source.schema = 'S1'"), "lock free again");
    }

    /// A sweep that stops early (here: an unreadable file) clears the
    /// sentinel, so readers don't wait for a sweep nobody is running while
    /// the stopped sweeper keeps the lock (a write operation would).
    #[cfg(unix)]
    #[test]
    fn a_sweep_that_stops_early_is_not_waited_for() {
        use std::os::unix::fs::PermissionsExt;
        let (_dir, registry) = registry_with(6);
        settle(&registry);
        put_external(&registry, "locked-out", "S1");
        let path = files(&registry).path_for("locked-out");
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o000)).unwrap();
        if std::fs::read(&path).is_ok() {
            return; // running as root: permissions are not enforced
        }
        let lock = registry.acquire_lock().unwrap();
        assert!(sync(&registry)
            .sweep(files(&registry), &index(&registry))
            .is_err());
        assert_eq!(
            index(&registry).meta().unwrap().dir_mtime_ns,
            Some(ABANDONED_DIR_MTIME)
        );
        drop(lock);
        // Were it still marked as sweeping, the reader would wait 20 s.
        *sync(&registry).sweep_wait_limit.lock().unwrap() = Duration::from_secs(20);
        let lock = foreign_lock(&registry);
        let start = Instant::now();
        assert!(sync(&registry).for_read(files(&registry), true).is_none());
        let waited = start.elapsed();
        assert!(
            waited >= WAIT_LIMIT && waited < Duration::from_secs(10),
            "{waited:?}"
        );
        drop(lock);
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o644)).unwrap();
        check(&registry, Some("source.schema = 'S1'"), "readable again");
    }

    /// A racy index read while another process's writer holds the lock in
    /// its hooks phase is verified without the lock and served at once.
    #[test]
    fn racy_index_is_verified_lock_free_while_a_writer_holds_the_lock() {
        let (_dir, registry) = registry_with(6);
        let written = Instant::now(); // no later than the write's mtime
        registry.create(&mut unit("lib", "S1"), None).unwrap();
        assert_eq!(current(&registry), Freshness::Racy { expired: false });
        let lock = foreign_lock(&registry);
        let s = sync(&registry);
        let (reads, lock_free, verifies, sweeps) = (
            s.index_reads(),
            s.lock_free_verifies(),
            s.verifies(),
            s.sweeps(),
        );

        // Within the racy window: served, but not settled.
        let waits = s.waits();
        let found = check(&registry, Some("source.schema = 'S1'"), "racy, lock busy");
        assert_eq!(s.waits(), waits, "must not wait");
        assert!(ids(&found).contains(&"lib"));
        assert!(s.index_reads() > reads);
        assert!(s.lock_free_verifies() > lock_free);
        assert_eq!(
            (s.verifies(), s.sweeps()),
            (verifies, sweeps),
            "no locked work"
        );
        // (A loaded registry thread pool can delay the read past the window.)
        if written.elapsed() < RACY_WINDOW {
            assert_eq!(current(&registry), Freshness::Racy { expired: false });
        }

        // Past the window: the compare-and-set settles it, lock still busy.
        std::thread::sleep(RACY_WINDOW + Duration::from_millis(20));
        check(&registry, None, "settling");
        assert_eq!(current(&registry), Freshness::Trusted);
        let lock_free = s.lock_free_verifies();
        check(&registry, None, "settled");
        assert_eq!(s.lock_free_verifies(), lock_free, "trusted: no verify");
        drop(lock);
    }

    /// A same-tick external add behind a racy index, with the lock busy: the
    /// lock-free verify sees the new name and hands over to the locked path.
    #[test]
    fn lock_free_verify_detects_an_external_add_while_the_lock_is_busy() {
        let (_dir, registry) = registry_with(6);
        let dir = files(&registry).dir().to_path_buf();
        registry.create(&mut unit("lib", "S1"), None).unwrap();
        let recorded = index(&registry).meta().unwrap().dir_mtime_ns.unwrap();
        put_external(&registry, "sneaky", "S1");
        set_mtime(&dir, recorded);
        assert_eq!(current(&registry), Freshness::Racy { expired: false });

        let lock = foreign_lock(&registry);
        let release = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(150));
            drop(lock);
        });
        let s = sync(&registry);
        let (lock_free, sweeps) = (s.lock_free_verifies(), s.sweeps());
        let found = check(
            &registry,
            Some("source.schema = 'S1'"),
            "same tick, lock busy",
        );
        assert!(ids(&found).contains(&"sneaky"), "{:?}", ids(&found));
        assert_eq!(
            s.lock_free_verifies(),
            lock_free + 1,
            "verified once, then waited"
        );
        assert!(
            s.sweeps() > sweeps,
            "the locked path swept once the lock was free"
        );
        release.join().unwrap();
    }

    /// The compare-and-set and the read confirmation refuse anything a
    /// sweep or write committed since the verify's meta was read.
    #[test]
    fn settle_and_confirm_refuse_concurrent_commits() {
        let (_dir, registry) = registry_with(4);
        settle(&registry);
        let index = index(&registry);
        let meta = index.meta().unwrap();
        let m = meta.dir_mtime_ns.unwrap();
        let later = meta.dir_recorded_ns.unwrap() + 1;
        let read = || IndexRead {
            index: Arc::clone(&index),
            verified: Some((m, meta.last_sweep_ns)),
        };
        assert!(read().confirm());

        // A write in progress, or a newer observation, blocks the CAS.
        index.set_write_in_progress().unwrap();
        assert!(!index.settle_dir(m, meta.dir_recorded_ns, later).unwrap());
        index.apply(&IndexChanges::default()).unwrap();
        assert!(!index.settle_dir(m, Some(later - 2), later).unwrap());
        assert!(!index
            .settle_dir(m + 1, meta.dir_recorded_ns, later)
            .unwrap());
        assert!(index.settle_dir(m, meta.dir_recorded_ns, later).unwrap());
        assert_eq!(index.meta().unwrap().dir_recorded_ns, Some(later));
        assert!(read().confirm(), "a settle is not a change");

        // A sweep, running or done, fails the confirmation.
        let lock = registry.acquire_lock().unwrap();
        index
            .apply(&IndexChanges {
                dir_mtime_ns: Some(SWEEPING_DIR_MTIME),
                ..IndexChanges::default()
            })
            .unwrap();
        assert!(!read().confirm(), "sweep running");
        assert!(sync(&registry).sweep(files(&registry), &index).is_ok());
        assert_eq!(index.meta().unwrap().dir_mtime_ns, Some(m));
        assert!(!read().confirm(), "sweep committed");
        drop(lock);
    }

    #[cfg(unix)] // Windows can't delete an open database.
    #[test]
    fn index_deleted_while_open_is_rebuilt() {
        let (_dir, registry) = registry_with(8);
        settle(&registry);
        let db = sync(&registry).db_path();
        std::fs::remove_dir_all(db.parent().unwrap()).unwrap();
        check(&registry, Some("source.schema = 'S1'"), "deleted");

        // The next untrusted read rebuilds it in a new file.
        put_external(&registry, "later", "S1");
        let found = check(&registry, Some("source.schema = 'S1'"), "rebuilt");
        assert!(ids(&found).contains(&"later"));
        assert!(db.is_file(), "rebuilt at {}", db.display());

        // Another instance shares the rebuilt file.
        let other = open_indexed(registry.root());
        check(&other, Some("source.schema = 'S1'"), "other instance");
    }

    #[test]
    fn index_replaced_with_garbage_while_open_is_rebuilt() {
        let (_dir, registry) = registry_with(8);
        settle(&registry);
        let db = sync(&registry).db_path();
        std::fs::write(&db, "this is not a database".repeat(500)).unwrap();
        put_external(&registry, "after-garbage", "S1");
        for round in 0..3 {
            let found = find(&registry, Some("source.schema = 'S1'"));
            let expected =
                test_hooks::without_index(|| find(&registry, Some("source.schema = 'S1'")));
            assert_eq!(found, expected, "round {round}");
        }
        // Repaired: the index serves again.
        put_external(&registry, "after-repair", "S1");
        let found = check(&registry, Some("source.schema = 'S1'"), "repaired");
        assert!(ids(&found).contains(&"after-repair"));
        let other = open_indexed(registry.root());
        check(&other, Some("source.schema = 'S1'"), "other instance");
    }

    #[cfg(unix)]
    #[test]
    fn unusable_index_dir_falls_back_to_files() {
        use std::os::unix::fs::PermissionsExt;
        let (_dir, registry) = new_registry();
        let index_dir = files(&registry).dir().join(INDEX_DIR);
        std::fs::create_dir(&index_dir).unwrap();
        std::fs::set_permissions(&index_dir, std::fs::Permissions::from_mode(0o500)).unwrap();
        if std::fs::write(index_dir.join("probe"), "").is_ok() {
            return; // running as root: permissions are not enforced
        }
        registry.create(&mut unit("a", "S1"), None).unwrap();
        put_external(&registry, "b", "S1");
        assert_eq!(
            ids(&find(&registry, Some("source.schema = 'S1'"))),
            ["a", "b"]
        );
        assert_eq!(sync(&registry).index_reads(), 0);
        assert!(sync(&registry).open_index().is_none());
        std::fs::set_permissions(&index_dir, std::fs::Permissions::from_mode(0o700)).unwrap();
    }

    #[test]
    fn disabled_index_uses_only_files_and_its_writes_are_swept_by_others() {
        let (dir, enabled) = registry_with(4);
        settle(&enabled);
        let registry_dir = files(&enabled).dir().to_path_buf();
        let disabled = CodeUnitRegistry::with_storage(
            dir.path().to_path_buf(),
            Storage::open_without_index(&registry_dir),
        );
        disabled.create(&mut unit("off-1", "S1"), None).unwrap();
        disabled
            .update("u001", &[("target.name", json!("OFF"))], None)
            .unwrap();
        let found = find(&disabled, Some("source.schema = 'S1'"));
        assert!(ids(&found).contains(&"off-1"));
        assert_eq!(sync(&disabled).index_reads(), 0);
        assert!(sync(&disabled).open_index().is_none());

        let found = check(
            &enabled,
            Some("source.schema = 'S1'"),
            "enabled sees off writes",
        );
        assert!(ids(&found).contains(&"off-1"));
        let renamed = check(&enabled, Some("target.name = 'OFF'"), "enabled");
        assert_eq!(ids(&renamed), ["u001"]);
    }

    #[test]
    fn prepare_write_sweeps_external_changes_first() {
        let (_dir, registry) = registry_with(4);
        settle(&registry);
        put_external(&registry, "ext", "S1");
        let sweeps = sync(&registry).sweeps();
        registry.create(&mut unit("lib", "S2"), None).unwrap();
        assert!(sync(&registry).sweeps() > sweeps, "the write swept first");
        // No read since: the write path itself brought `ext` into the index.
        let rows = index(&registry).read_many(&["ext".to_string(), "lib".to_string()]);
        assert!(rows.iter().all(|r| matches!(r, Ok(Some(_)))), "{rows:?}");
        check(&registry, Some("source.schema = 'S1'"), "after write");
    }

    /// A hook that reads while its write holds the lock — through this
    /// instance and through a second one in the same process — after an
    /// external change made the index stale: both read the files rather than
    /// wait on the lock their own process holds.
    struct ReadingHook {
        calls: AtomicU64,
    }

    impl RegistryHook for ReadingHook {
        fn before_persist(
            &self,
            _kind: ChangeType,
            changes: Vec<CodeUnitChange>,
            registry: &CodeUnitRegistry,
            _options: &WriteOptions,
        ) -> crate::error::Result<Vec<CodeUnitChange>> {
            let n = self.calls.fetch_add(1, Ordering::Relaxed);
            let id = format!("hook-ext-{n}");
            // In a later clock tick than the write's own bookkeeping, so the
            // index is stale (not merely racy, which a locked operation
            // reads as of its `prepare_write`).
            std::thread::sleep(Duration::from_millis(25));
            registry.storage.put_raw_text(&id, &doc_text(&id, "S1"))?;
            let options = FindOptions {
                filter: Some("source.schema = 'S1'"),
                ..FindOptions::default()
            };
            let found = registry.find_all(options)?;
            assert!(found.iter().any(|u| u.id.as_deref() == Some(id.as_str())));
            let other = open_indexed(registry.root());
            let found = other.find_all(options)?;
            assert!(found.iter().any(|u| u.id.as_deref() == Some(id.as_str())));
            Ok(changes)
        }
    }

    #[test]
    fn hooks_reading_during_a_write_never_deadlock() {
        let (_dir, mut registry) = registry_with(6);
        registry.add_hook(ReadingHook {
            calls: AtomicU64::new(0),
        });
        let (done, finished) = std::sync::mpsc::channel();
        let worker = std::thread::spawn(move || {
            registry.create(&mut unit("c1", "S1"), None).unwrap();
            registry
                .update("u001", &[("target.name", json!("HOOKED"))], None)
                .unwrap();
            let mut batch = vec![unit("c2", "S2"), unit("c3", "S2")];
            assert!(registry
                .create_batch(&mut batch, None)
                .unwrap()
                .failed
                .is_empty());
            done.send(()).unwrap();
            registry
        });
        finished
            .recv_timeout(Duration::from_secs(60))
            .expect("a write whose hooks read deadlocked");
        let registry = worker.join().unwrap();
        let found = check(&registry, Some("source.schema = 'S1'"), "after hooks");
        for id in ["c1", "hook-ext-0", "hook-ext-1", "hook-ext-2"] {
            assert!(ids(&found).contains(&id), "{id}");
        }
        check(&registry, None, "after hooks");
    }

    // ── Listings that miss files ────────────────────────────────────────

    /// A sweep whose listing omits files that still exist (as `readdir`
    /// may while a rename runs): their rows survive, re-read from the file;
    /// only a file `stat` reports gone loses its row.
    #[test]
    fn sweep_keeps_rows_of_existing_files_its_listing_missed() {
        let (_dir, registry) = registry_with(8);
        settle(&registry);
        let rows = |ids: &[&str]| {
            let ids: Vec<String> = ids.iter().map(|id| id.to_string()).collect();
            index(&registry)
                .read_many(&ids)
                .into_iter()
                .map(|row| row.unwrap().is_some())
                .collect::<Vec<bool>>()
        };
        // u001 unchanged, u002 replaced, u003 deleted: all three unlisted.
        files(&registry).hide_from_listings(&["u001", "u002", "u003"]);
        put_external(&registry, "u002", "S9");
        std::fs::remove_file(files(&registry).path_for("u003")).unwrap();
        let sweeps = sync(&registry).sweeps();
        let found = check(&registry, None, "listing misses");
        assert!(sync(&registry).sweeps() > sweeps, "swept");
        let found = ids(&found);
        assert!(
            found.contains(&"u001") && found.contains(&"u002"),
            "{found:?}"
        );
        assert!(!found.contains(&"u003"), "{found:?}");
        assert_eq!(rows(&["u001", "u002", "u003"]), [true, true, false]);
        let replaced = check(&registry, Some("source.schema = 'S9'"), "re-read");
        assert_eq!(ids(&replaced), ["u002"]);
        assert_eq!(
            files(&registry)
                .fingerprint_of("u002")
                .unwrap()
                .unwrap()
                .file_id,
            index(&registry).fingerprints().unwrap()["u002"].file_id,
            "the row carries the fresh fingerprint"
        );

        // A lock-free verify missing a name is a mismatch, never a delete.
        files(&registry).hide_from_listings(&[]);
        registry.create(&mut unit("lib", "S1"), None).unwrap();
        files(&registry).hide_from_listings(&["u004"]);
        std::thread::sleep(RACY_WINDOW + Duration::from_millis(20));
        let lock_free = sync(&registry).lock_free_verifies();
        check(&registry, Some("source.schema = 'S0'"), "verify misses");
        assert!(sync(&registry).lock_free_verifies() > lock_free);
        assert_eq!(rows(&["u004"]), [true]);
        files(&registry).hide_from_listings(&[]);
        check(&registry, None, "complete listings again");
    }

    /// The verify compares the listing with the rows as a set: a name
    /// listed twice (possible mid-rename) can't stand in for a missing one.
    #[test]
    fn listing_comparison_rejects_repeats_and_misses() {
        let stored: HashMap<String, u64> = [("a".to_string(), 1), ("b".to_string(), 2)]
            .into_iter()
            .collect();
        let listed = |names: &[(&str, u64)]| {
            names
                .iter()
                .map(|(n, i)| (n.to_string(), *i))
                .collect::<Vec<_>>()
        };
        assert!(listing_matches(&listed(&[("b", 2), ("a", 1)]), &stored));
        assert!(!listing_matches(&listed(&[("a", 1), ("a", 1)]), &stored));
        assert!(!listing_matches(&listed(&[("a", 1)]), &stored));
        assert!(!listing_matches(&listed(&[("a", 1), ("b", 3)]), &stored));
        assert!(!listing_matches(&listed(&[("a", 1), ("b", 0)]), &stored));
        assert!(!listing_matches(
            &listed(&[("a", 1), ("b", 2), ("c", 3)]),
            &stored
        ));
    }

    /// The real thing: files replaced by rename (as `git checkout` does) in
    /// a loop while filtered reads run; every read must return every unit.
    /// On btrfs, `readdir` misses files renamed over mid-listing.
    ///
    /// `SCAI_SYNC_RENAME_SECS` (default 5) bounds it; the registry lives in
    /// `$TMPDIR`, so run it there on the filesystem of interest.
    #[test]
    #[ignore = "timing-based; runs for several seconds"]
    fn reads_stay_complete_while_files_are_renamed_over() {
        const UNITS: usize = 400;
        let (_dir, registry) = registry_with(UNITS);
        settle(&registry);
        let dir = files(&registry).dir().to_path_buf();
        let run_for = Duration::from_secs(env_or("SCAI_SYNC_RENAME_SECS", 5) as u64);
        let stop = std::sync::atomic::AtomicBool::new(false);
        let (renames, reads, short) = std::thread::scope(|scope| {
            let renamer = scope.spawn(|| {
                let mut n = 0usize;
                while !stop.load(Ordering::Relaxed) {
                    let id = format!("u{:03}", n % UNITS);
                    let temp = dir.join(format!(".{id}.json.rename-tmp"));
                    std::fs::write(&temp, doc_text(&id, &format!("S{}", (n % UNITS) % 4))).unwrap();
                    std::fs::rename(&temp, dir.join(format!("{id}.json"))).unwrap();
                    n += 1;
                }
                n
            });
            let start = Instant::now();
            let (mut reads, mut short) = (0usize, Vec::new());
            while start.elapsed() < run_for {
                let found = find(&registry, Some("source.schema = 'S1'"));
                if found.len() != UNITS / 4 {
                    short.push(found.len());
                }
                reads += 1;
            }
            stop.store(true, Ordering::Relaxed);
            (renamer.join().unwrap(), reads, short)
        });
        let s = sync(&registry);
        println!(
            "{renames} renames, {reads} reads ({} from the index, {} sweeps): {} short",
            s.index_reads(),
            s.sweeps(),
            short.len()
        );
        assert!(
            short.is_empty(),
            "short reads (expected {}): {short:?}",
            UNITS / 4
        );
        check(&registry, None, "quiet");
    }

    // ── Multi-process stress ────────────────────────────────────────────

    const STRESS_ROLE_ENV: &str = "SCAI_SYNC_STRESS_ROLE";
    const STRESS_DIR_ENV: &str = "SCAI_SYNC_STRESS_DIR";
    /// Units per library writer (each writer owns schema `S{writer}`).
    const STRESS_UNITS: usize = 40;
    /// Units owned by the "git" process (schema `G`).
    const STRESS_GIT_UNITS: usize = 40;

    fn env_or(name: &str, default: usize) -> usize {
        std::env::var(name)
            .ok()
            .and_then(|v| v.parse().ok())
            .unwrap_or(default)
    }

    fn writer_id(writer: usize, n: usize) -> String {
        format!("w{writer:02}-{n:02}")
    }

    /// Replace (temp + rename, like git) or create `id`'s file.
    fn git_put(dir: &Path, id: &str, name: &str) {
        let mut doc = unit(id, "G");
        doc.target.as_mut().unwrap().name = Some(name.to_string());
        let path = dir.join(format!("{id}.json"));
        let temp = dir.join(format!(".{id}.json.git-tmp"));
        std::fs::write(&temp, serde_json::to_string_pretty(&doc).unwrap() + "\n").unwrap();
        std::fs::rename(&temp, &path).unwrap();
    }

    /// One line of per-process statistics for the parent to aggregate.
    fn print_stats(role: &str, registry: &CodeUnitRegistry, extra: &str) {
        let s = sync(registry);
        println!(
            "STATS {role} index_reads={} sweeps={} verifies={} lock_free={} {extra}",
            s.index_reads(),
            s.sweeps(),
            s.verifies(),
            s.lock_free_verifies()
        );
    }

    /// Child process body for [`multiprocess_stress`]; a no-op unless spawned by it.
    #[test]
    #[ignore = "child process of multiprocess_stress"]
    fn stress_worker() {
        let (Ok(role), Ok(root)) = (
            std::env::var(STRESS_ROLE_ENV),
            std::env::var(STRESS_DIR_ENV),
        ) else {
            return;
        };
        let root = PathBuf::from(root);
        let registry = CodeUnitRegistry::open(&root).unwrap();
        let (kind, index) = role.split_once(':').unwrap();
        let index: usize = index.parse().unwrap();
        match kind {
            "writer" => {
                let writes = env_or("SCAI_SYNC_STRESS_WRITES", 40);
                let start = Instant::now();
                for k in 0..writes {
                    let tag = json!(format!("w{index}-{k}"));
                    if k % 5 == 4 {
                        let batch: Vec<(String, Vec<(&str, Value)>)> = (0..5)
                            .map(|j| {
                                let id = writer_id(index, (k * 3 + j) % STRESS_UNITS);
                                (id, vec![("target.name", tag.clone())])
                            })
                            .collect();
                        let batch: Vec<(&str, Vec<(&str, Value)>)> = batch
                            .iter()
                            .map(|(id, updates)| (id.as_str(), updates.clone()))
                            .collect();
                        let result = registry.update_batch(&batch, None).unwrap();
                        assert!(result.failed.is_empty(), "{:?}", result.failed);
                    } else {
                        let id = writer_id(index, (k * 7) % STRESS_UNITS);
                        registry
                            .update(&id, &[("target.name", tag.clone())], None)
                            .unwrap();
                    }
                }
                let elapsed = start.elapsed().as_secs_f64() * 1000.0;
                print_stats(
                    &role,
                    &registry,
                    &format!("writes={writes} ms={elapsed:.0}"),
                );
            }
            "git" => {
                let rounds = env_or("SCAI_SYNC_STRESS_GIT_ROUNDS", 150);
                let dir = files(&registry).dir().to_path_buf();
                for r in 0..rounds {
                    git_put(
                        &dir,
                        &format!("git-{:03}", r % STRESS_GIT_UNITS),
                        &format!("r{r}"),
                    );
                    git_put(&dir, &format!("gitnew-{r:03}"), "NEW");
                    if r >= 3 {
                        std::fs::remove_file(dir.join(format!("gitnew-{:03}.json", r - 3)))
                            .unwrap();
                    }
                    std::thread::sleep(Duration::from_millis(2));
                }
                print_stats(&role, &registry, &format!("rounds={rounds}"));
            }
            "reader" => {
                let writers = env_or("SCAI_SYNC_STRESS_WRITERS", 8);
                let stop = root.join("stop");
                let pause_ms = env_or("SCAI_SYNC_STRESS_READER_PAUSE_MS", 0) as u64;
                let (mut ops, mut fallbacks) = (0usize, 0usize);
                let mut first_fallback = false;
                let mut first_gave_up = false;
                let mut latencies: Vec<f64> = Vec::new();
                // Opening the index is part of the first read; timed apart.
                let opening = Instant::now();
                sync(&registry).index();
                let open_ms = opening.elapsed().as_secs_f64() * 1000.0;
                while !stop.exists() || ops < 20 {
                    let start = Instant::now();
                    let served_before = sync(&registry).index_reads();
                    match ops % 3 {
                        0 | 1 => {
                            let schema = if ops % 3 == 0 {
                                format!("S{}", (index + ops) % writers)
                            } else {
                                "G".to_string()
                            };
                            let filter = format!("source.schema = '{schema}'");
                            let found = registry
                                .find_all(FindOptions {
                                    filter: Some(&filter),
                                    ..FindOptions::default()
                                })
                                .unwrap();
                            for u in &found {
                                let got = u.source.as_ref().and_then(|s| s.schema.as_deref());
                                assert_eq!(got, Some(schema.as_str()));
                            }
                            if schema != "G" {
                                assert_eq!(found.len(), STRESS_UNITS, "{filter}");
                            }
                        }
                        _ => {
                            let found = registry
                                .find_all(FindOptions {
                                    fields: Some(&["id", "target.name"]),
                                    ..FindOptions::default()
                                })
                                .unwrap();
                            assert!(
                                found.len() >= writers * STRESS_UNITS + STRESS_GIT_UNITS,
                                "{} units",
                                found.len()
                            );
                        }
                    }
                    if sync(&registry).index_reads() == served_before {
                        fallbacks += 1;
                        first_fallback |= ops == 0;
                    }
                    first_gave_up |= ops == 0 && sync(&registry).give_ups() > 0;
                    latencies.push(start.elapsed().as_secs_f64() * 1000.0);
                    ops += 1;
                    // Think time between reads (0 = a closed loop).
                    std::thread::sleep(Duration::from_millis(pause_ms));
                }
                let text: Vec<String> = latencies.iter().map(|ms| format!("{ms:.3}")).collect();
                std::fs::write(root.join(format!("latency-{index}.txt")), text.join("\n")).unwrap();
                print_stats(
                    &role,
                    &registry,
                    &format!(
                        "ops={ops} fallbacks={fallbacks} first_fallback={} first_gave_up={} \
                         open_ms={open_ms:.1} first_ms={:.1}",
                        u8::from(first_fallback),
                        u8::from(first_gave_up),
                        latencies.first().copied().unwrap_or(0.0)
                    ),
                );
            }
            other => panic!("unknown role {other}"),
        }
    }

    /// Many processes sharing one registry: library writers, filtered
    /// readers, and a "git" process replacing, adding and deleting files
    /// behind the library's back. No error may reach a caller, and once
    /// quiet, an index read must equal a files-only read.
    ///
    /// `cargo test --release -p scai-state-core multiprocess_stress -- --ignored --nocapture`
    /// (`SCAI_SYNC_STRESS_PROCS`, `_WRITERS`, `_WRITES`, `_GIT_ROUNDS`,
    /// `_READER_PAUSE_MS` tune it). `SCAI_SYNC_STRESS_FILLER=N` adds `N`
    /// more units (schema `X`, written as files); `SCAI_SYNC_STRESS_COLD=1`
    /// deletes the index before the children start, so they all meet the
    /// first-open build.
    #[test]
    #[ignore = "stress test; spawns many processes"]
    fn multiprocess_stress() {
        use std::process::{Command, Stdio};

        if !enabled_by_env() {
            // Files-only reads are not consistent under concurrent renames
            // (a listing can miss a file replaced mid-`readdir`), so the
            // readers' exact counts would fail; the test is about the index.
            println!("multiprocess_stress: skipped, {INDEX_ENV_VAR} disables the index");
            return;
        }
        let procs = env_or("SCAI_SYNC_STRESS_PROCS", 24);
        let writers = env_or("SCAI_SYNC_STRESS_WRITERS", 8).min(procs - 2);
        let readers = procs - writers - 1;
        let root = tempfile::tempdir().unwrap();
        let registry = CodeUnitRegistry::init(root.path()).unwrap();
        let mut seed: Vec<CodeUnit> = (0..writers)
            .flat_map(|w| (0..STRESS_UNITS).map(move |n| unit(&writer_id(w, n), &format!("S{w}"))))
            .chain((0..STRESS_GIT_UNITS).map(|n| unit(&format!("git-{n:03}"), "G")))
            .collect();
        assert!(registry
            .create_batch(&mut seed, None)
            .unwrap()
            .failed
            .is_empty());
        let filler = env_or("SCAI_SYNC_STRESS_FILLER", 0);
        for n in 0..filler {
            let id = format!("x{n:06}");
            registry
                .storage
                .put_raw_text(&id, &doc_text(&id, "X"))
                .unwrap();
        }
        let cold = env_or("SCAI_SYNC_STRESS_COLD", 0) != 0;
        if cold {
            drop(registry);
            let index_dir = root
                .path()
                .join(crate::registry::REGISTRY_DIR)
                .join(INDEX_DIR);
            std::fs::remove_dir_all(index_dir).unwrap();
        }

        let test_name = format!(
            "{}::stress_worker",
            module_path!().split_once("::").unwrap().1
        );
        let spawn = |role: String| {
            let child = Command::new(std::env::current_exe().unwrap())
                .args([
                    test_name.as_str(),
                    "--exact",
                    "--ignored",
                    "--nocapture",
                    "--test-threads=1",
                ])
                .env(STRESS_ROLE_ENV, &role)
                .env(STRESS_DIR_ENV, root.path())
                .env("SCAI_SYNC_STRESS_WRITERS", writers.to_string())
                .stdout(Stdio::piped())
                .stderr(Stdio::piped())
                .spawn()
                .unwrap();
            (role, child)
        };
        let start = Instant::now();
        let reader_children: Vec<_> = (0..readers).map(|i| spawn(format!("reader:{i}"))).collect();
        let mut busy: Vec<_> = (0..writers).map(|i| spawn(format!("writer:{i}"))).collect();
        busy.push(spawn("git:0".to_string()));

        let mut failures = Vec::new();
        let mut stats: Vec<String> = Vec::new();
        let mut collect = |(role, child): (String, std::process::Child)| {
            let out = child.wait_with_output().unwrap();
            let stdout = String::from_utf8_lossy(&out.stdout);
            stats.extend(
                stdout
                    .lines()
                    // libtest may print "test … ... " on the same line.
                    .filter_map(|l| l.split_once("STATS ").map(|(_, stats)| stats.to_string())),
            );
            if !out.status.success() {
                failures.push(format!(
                    "{role} failed ({}):\n{stdout}\n{}",
                    out.status,
                    String::from_utf8_lossy(&out.stderr)
                ));
            }
        };
        busy.into_iter().for_each(&mut collect);
        let writes_done = start.elapsed();
        std::fs::write(root.path().join("stop"), "").unwrap();
        reader_children.into_iter().for_each(&mut collect);
        let wall = start.elapsed();
        assert!(failures.is_empty(), "{}", failures.join("\n\n"));

        // Quiescent: the index must say exactly what the files say.
        let registry = CodeUnitRegistry::open(root.path()).unwrap();
        let settle_start = Instant::now();
        let all = check(&registry, None, "final");
        let settle_time = settle_start.elapsed();
        for w in 0..writers {
            let found = check(&registry, Some(&format!("source.schema = 'S{w}'")), "final");
            assert_eq!(found.len(), STRESS_UNITS);
        }
        let git = check(&registry, Some("source.schema = 'G'"), "final");
        assert_eq!(
            git.len(),
            STRESS_GIT_UNITS + env_or("SCAI_SYNC_STRESS_GIT_ROUNDS", 150).min(3),
            "git units plus the last three added"
        );

        let sum = |role: &str, key: &str| -> f64 {
            stats
                .iter()
                .filter(|l| l.starts_with(role))
                .filter_map(|l| {
                    l.split_whitespace()
                        .find_map(|kv| kv.strip_prefix(&format!("{key}=")))
                        .and_then(|v| v.parse::<f64>().ok())
                })
                .sum()
        };
        let max = |role: &str, key: &str| -> f64 {
            stats
                .iter()
                .filter(|l| l.starts_with(role))
                .filter_map(|l| {
                    l.split_whitespace()
                        .find_map(|kv| kv.strip_prefix(&format!("{key}=")))
                        .and_then(|v| v.parse::<f64>().ok())
                })
                .fold(0.0, f64::max)
        };
        let reader_ops = sum("reader", "ops");
        let mut latencies: Vec<f64> = (0..readers)
            .flat_map(|i| {
                std::fs::read_to_string(root.path().join(format!("latency-{i}.txt")))
                    .unwrap_or_default()
                    .lines()
                    .filter_map(|l| l.parse::<f64>().ok())
                    .collect::<Vec<_>>()
            })
            .collect();
        latencies.sort_by(f64::total_cmp);
        let pct = |p: f64| {
            latencies
                .get(((latencies.len() as f64 * p) as usize).min(latencies.len().saturating_sub(1)))
                .copied()
                .unwrap_or(0.0)
        };
        let mean = latencies.iter().sum::<f64>() / latencies.len().max(1) as f64;
        println!(
            "{procs} processes ({writers} writers x {} writes, {readers} readers, 1 git): \
             writers+git done in {writes_done:.2?}, wall {wall:.2?}; {} units at the end; \
             final read (incl. settle) {settle_time:.2?}",
            env_or("SCAI_SYNC_STRESS_WRITES", 40),
            all.len(),
        );
        println!(
            "readers: {reader_ops:.0} ops, mean {mean:.2} ms, p50 {:.2} ms, p99 {:.1} ms, \
             max {:.1} ms; file fallbacks {:.0} ({:.2}%); sweeps {:.0}, verifies {:.0} locked \
             + {:.0} lock-free",
            pct(0.5),
            pct(0.99),
            latencies.last().copied().unwrap_or(0.0),
            sum("reader", "fallbacks"),
            100.0 * sum("reader", "fallbacks") / reader_ops.max(1.0),
            sum("reader", "sweeps"),
            sum("reader", "verifies"),
            sum("reader", "lock_free"),
        );
        println!(
            "first reads ({}{filler} filler units): {:.0} of {readers} readers stopped waiting \
             for the lock, {:.0} fell back to the files; slowest index open {:.0} ms, slowest \
             first read after it {:.0} ms",
            if cold { "cold index, " } else { "" },
            sum("reader", "first_gave_up"),
            sum("reader", "first_fallback"),
            max("reader", "open_ms"),
            max("reader", "first_ms"),
        );
        let total_writes = (writers * env_or("SCAI_SYNC_STRESS_WRITES", 40)) as f64;
        println!(
            "writer throughput: {:.0} write ops/s ({total_writes:.0} in {:.2} s)",
            total_writes / max("writer", "ms") * 1000.0,
            max("writer", "ms") / 1000.0,
        );
        println!(
            "writers: max {:.0} ms for all their writes; sweeps {:.0}, verifies {:.0}",
            max("writer", "ms"),
            sum("writer", "sweeps"),
            sum("writer", "verifies"),
        );
    }

    /// Cost of the protocol's pieces on a real registry: first build, the
    /// per-operation freshness check, sweeps with no / 1% changes.
    ///
    /// `SCAI_SYNC_PERF_DIR=/tmp/r cargo test --release -p scai-state-core
    /// perf_sync_costs -- --ignored --nocapture`, where `/tmp/r/registry`
    /// holds the files (the index there is deleted first; 1% of the files
    /// are rewritten).
    #[test]
    #[ignore = "perf; needs SCAI_SYNC_PERF_DIR"]
    fn perf_sync_costs() {
        let Ok(root) = std::env::var("SCAI_SYNC_PERF_DIR") else {
            return;
        };
        let dir = Path::new(&root).join("registry");
        let _ = std::fs::remove_dir_all(dir.join(INDEX_DIR));
        let storage = Storage::open(&dir).unwrap();
        let (files, sync) = (&storage.files, &storage.index);
        let time = |label: &str, f: &mut dyn FnMut()| {
            let start = Instant::now();
            f();
            let elapsed = start.elapsed();
            println!("{label}: {elapsed:.2?}");
            elapsed
        };

        let lock = storage.lock().unwrap();
        time("first-open build (open + full sweep)", &mut || {
            storage.prepare_write(&lock).unwrap()
        });
        let index = sync.open_index().unwrap();
        drop(lock);
        // A fresh copy's directory was just written: let the racy window pass.
        std::thread::sleep(RACY_WINDOW);
        storage.load_all(|_, _| ()).unwrap();
        assert_eq!(freshness(files, &index), Freshness::Trusted);

        let n = 2000;
        let per_op = time("freshness check x2000", &mut || {
            for _ in 0..n {
                assert_eq!(freshness(files, &index), Freshness::Trusted);
            }
        }) / n;
        println!("  per check: {per_op:.2?}");
        let per_op = time("for_read (trusted) x2000", &mut || {
            for _ in 0..n {
                assert!(sync.for_read(files, true).is_some());
            }
        }) / n;
        println!("  per for_read: {per_op:.2?}");
        time("dir stat x2000", &mut || {
            for _ in 0..n {
                files.dir_mtime_ns().unwrap();
            }
        });
        time("meta read x2000", &mut || {
            for _ in 0..n {
                index.meta().unwrap();
            }
        });

        let lock = storage.lock().unwrap();
        time("scan (list + stat all)", &mut || {
            files.scan().unwrap();
        });
        time("index fingerprints()", &mut || {
            index.fingerprints().unwrap();
        });
        time("sweep, no changes", &mut || {
            assert!(sync.sweep(files, &index).is_ok())
        });
        time("listing with file ids (readdir only)", &mut || {
            files.list_file_ids().unwrap().unwrap();
        });
        time("index file_ids()", &mut || {
            index.file_ids().unwrap();
        });
        let (sweeps, verifies) = (sync.sweeps(), sync.verifies());
        time("verify, no changes", &mut || {
            assert!(sync.verify(files, &index).is_ok())
        });
        assert_eq!(
            (sync.sweeps(), sync.verifies()),
            (sweeps, verifies + 1),
            "settled without a sweep"
        );

        // Twice: the first apply after the build may also pay for emptying
        // the build's WAL.
        let ids = files.ids().unwrap();
        let mut changed: Vec<&String> = Vec::new();
        for round in 0..2 {
            changed = ids.iter().skip(round).step_by(100).collect();
            for id in &changed {
                let text = std::fs::read_to_string(files.path_for(id)).unwrap();
                storage.put_raw_text(id, &format!("{text} ")).unwrap();
            }
            time(
                &format!("sweep, {} files replaced (round {round})", changed.len()),
                &mut || assert!(sync.sweep(files, &index).is_ok()),
            );
        }

        let values: Vec<(String, serde_json::Value)> = changed
            .iter()
            .map(|id| {
                let text = std::fs::read_to_string(files.path_for(id)).unwrap();
                ((*id).clone(), serde_json::from_str(&text).unwrap())
            })
            .collect();
        let writes: Vec<StorageWrite<'_>> = values
            .iter()
            .map(|(id, value)| StorageWrite::Put { id, value })
            .collect();
        time(
            &format!("library write_batch of {}", writes.len()),
            &mut || {
                assert!(storage
                    .write_batch(&lock, &writes, false)
                    .iter()
                    .all(|r| r.is_ok()))
            },
        );
        time("sweep re-verifying those (smudged) rows", &mut || {
            assert!(sync.sweep(files, &index).is_ok())
        });
        drop(lock);

        time("load_all via index", &mut || {
            storage.load_all(|_, t| t.map(|t| t.len())).unwrap();
        });
        time("load_all via files", &mut || {
            storage.load_all_files(|_, t| t.map(|t| t.len())).unwrap();
        });
        let _ = std::fs::remove_dir_all(dir.join(INDEX_DIR));
    }
}
