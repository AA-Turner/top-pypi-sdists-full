//! File-per-document storage: `registry/{id}.json`.

use std::fs::{self, File};
use std::io::{ErrorKind, Write};
use std::path::{Path, PathBuf};

use rayon::prelude::*;
use serde_json::Value;

use super::{Fingerprint, StorageWrite};
use crate::error::*;
use crate::registry::{paths, LINE_ENDING};

/// What a successful put wrote: the exact file text, and the file's
/// fingerprint taken right after the rename (`None` if that `stat` failed).
#[derive(Debug)]
pub(super) struct Written {
    pub(super) text: String,
    pub(super) fingerprint: Option<Fingerprint>,
}

/// Stores each code unit as pretty-printed JSON in `{dir}/{id}.json`.
#[derive(Debug)]
pub(crate) struct FileStorage {
    dir: PathBuf,
    /// Names the sync engine's listings ([`Self::scan`],
    /// [`Self::list_file_ids`]) leave out, as `readdir` may during a
    /// concurrent rename (see [`Self::hide_from_listings`]).
    #[cfg(test)]
    hidden: std::sync::Mutex<Vec<String>>,
}

impl FileStorage {
    pub(crate) fn new(dir: PathBuf) -> Self {
        Self {
            dir,
            #[cfg(test)]
            hidden: std::sync::Mutex::new(Vec::new()),
        }
    }

    /// Test-only: make the sync engine's listings of this instance omit the
    /// files for `ids` (which still exist), the way a `readdir` racing a
    /// rename can on btrfs. An empty slice restores complete listings.
    #[cfg(test)]
    pub(super) fn hide_from_listings(&self, ids: &[&str]) {
        *self.hidden.lock().unwrap() = ids.iter().map(|id| id.to_string()).collect();
    }

    /// Whether a listing should omit `id` (see [`Self::hide_from_listings`]).
    #[cfg(test)]
    fn hidden(&self, id: &str) -> bool {
        self.hidden.lock().unwrap().iter().any(|h| h == id)
    }

    /// The registry directory holding the files.
    #[cfg(test)]
    pub(crate) fn dir(&self) -> &Path {
        &self.dir
    }

    /// Compute file path from ID.
    /// Returns `{dir}/{id}.json`
    pub(crate) fn path_for(&self, id: &str) -> PathBuf {
        self.dir.join(format!("{}.json", id))
    }

    pub(super) fn exists(&self, id: &str) -> bool {
        self.path_for(id).exists()
    }

    pub(super) fn read_raw(&self, id: &str) -> Result<Option<String>> {
        match fs::read_to_string(self.path_for(id)) {
            Ok(text) => Ok(Some(text)),
            Err(e) if e.kind() == ErrorKind::NotFound => Ok(None),
            Err(e) => Err(e.into()),
        }
    }

    pub(super) fn read_many(&self, ids: &[String]) -> Vec<Result<Option<String>>> {
        ids.par_iter().map(|id| self.read_raw(id)).collect()
    }

    /// Registry directory mtime in ns since the Unix epoch: changes whenever a
    /// file is added, removed, or replaced by rename.
    pub(super) fn dir_mtime_ns(&self) -> Result<i64> {
        Ok(mtime_ns(&fs::metadata(&self.dir)?))
    }

    /// Fingerprint of every `*.json` file, in directory order. A file that
    /// vanishes between listing and `stat` is left out; a name that is not a
    /// valid ID fails the scan (as [`Self::ids`] does).
    ///
    /// Like any listing, it can miss a file that exists throughout, or
    /// list one twice, while the directory is being modified (POSIX allows
    /// it; btrfs does it for a file renamed over mid-listing): a name
    /// missing here is not proof that its file is gone.
    ///
    /// The `stat`s run in parallel: listing is sequential, but at ~2 µs per
    /// file the stats dominate a large directory.
    pub(super) fn scan(&self) -> Result<Vec<(String, Fingerprint)>> {
        let paths = paths::json_file_paths(&self.dir)?;
        #[cfg(test)]
        let paths: Vec<PathBuf> = paths
            .into_iter()
            .filter(|path| !paths::filename_stem(path).is_ok_and(|id| self.hidden(id)))
            .collect();
        let stats: Vec<Result<Option<(String, Fingerprint)>>> = paths
            .par_iter()
            .with_min_len(256)
            .map(|path| {
                let id = paths::filename_stem(path)?;
                match fs::metadata(path) {
                    Ok(meta) => Ok(Some((id.to_string(), fingerprint(&meta)))),
                    Err(e) if e.kind() == ErrorKind::NotFound => Ok(None),
                    Err(e) => Err(e.into()),
                }
            })
            .collect();
        stats.into_iter().filter_map(Result::transpose).collect()
    }

    /// The ID and file id (inode) of every `*.json` file, from the listing
    /// alone — no `stat` per file. `None` where the listing carries no file
    /// id (non-Unix): the caller must `stat` instead. Can miss or repeat
    /// names during concurrent changes, as [`Self::scan`] can.
    pub(super) fn list_file_ids(&self) -> Result<Option<Vec<(String, u64)>>> {
        #[cfg(unix)]
        {
            use std::os::unix::fs::DirEntryExt;
            let mut out = Vec::new();
            for entry in fs::read_dir(&self.dir)? {
                let entry = entry?;
                let name = entry.file_name();
                // Same selection and naming as `paths::json_file_paths` /
                // `filename_stem`, without building a path per entry.
                let name = Path::new(&name);
                if name.extension().is_some_and(|e| e == "json") {
                    let id = paths::filename_stem(name)?;
                    #[cfg(test)]
                    if self.hidden(id) {
                        continue;
                    }
                    out.push((id.to_string(), entry.ino()));
                }
            }
            Ok(Some(out))
        }
        #[cfg(not(unix))]
        Ok(None)
    }

    /// Fingerprint of the file for `id`, or `None` if it does not exist.
    pub(super) fn fingerprint_of(&self, id: &str) -> Result<Option<Fingerprint>> {
        match fs::metadata(self.path_for(id)) {
            Ok(meta) => Ok(Some(fingerprint(&meta))),
            Err(e) if e.kind() == ErrorKind::NotFound => Ok(None),
            Err(e) => Err(e.into()),
        }
    }

    pub(super) fn ids(&self) -> Result<Vec<String>> {
        if !self.dir.exists() {
            return Ok(Vec::new());
        }
        paths::json_file_paths(&self.dir)?
            .iter()
            .map(|path| paths::filename_stem(path).map(str::to_string))
            .collect()
    }

    /// Parallel: writes are independent and syscall-bound. Callers guarantee
    /// unique IDs per batch, so no two threads touch the same unit's `.tmp`.
    ///
    /// With `record`, each successful put reports what it wrote (see
    /// [`Written`]); otherwise, and for deletes, the outcome is `Ok(None)`.
    pub(super) fn write_batch(
        &self,
        writes: &[StorageWrite<'_>],
        durable: bool,
        record: bool,
    ) -> Vec<Result<Option<Written>>> {
        writes
            .par_iter()
            .map(|write| match *write {
                StorageWrite::Put { id, value } => {
                    let path = self.path_for(id);
                    let text = Self::render(value)?;
                    Self::write_text(&path, &text, durable)?;
                    Ok(record.then(|| Written {
                        fingerprint: fs::metadata(&path).ok().map(|m| fingerprint(&m)),
                        text,
                    }))
                }
                StorageWrite::Delete { id } => {
                    let path = self.path_for(id);
                    if path.exists() {
                        fs::remove_file(path)?;
                    }
                    Ok(None)
                }
            })
            .collect()
    }

    pub(super) fn sync(&self) -> Result<()> {
        // fsync-ing the directory handle makes the temp-file→rename in
        // `write_text` durable on POSIX. Windows can't open a directory
        // as a `File` (returns ERROR_ACCESS_DENIED / os error 5) and doesn't
        // need it — NTFS journals the rename — so skip the flush there.
        #[cfg(not(windows))]
        {
            if self.dir.exists() {
                let dir = File::open(&self.dir)?;
                dir.sync_all()?;
            }
        }
        Ok(())
    }

    /// The file text stored for `value`: pretty JSON plus a line ending.
    fn render(value: &Value) -> Result<String> {
        let mut text = serde_json::to_string_pretty(value)?;
        text.push_str(LINE_ENDING);
        Ok(text)
    }

    /// Low-level atomic file write: write `text` to a temp file, then rename
    /// into place. `durable` requests a crash-durable rename (see
    /// [`Self::durable_rename`]).
    fn write_text(path: &Path, text: &str, durable: bool) -> Result<()> {
        let temp_path = path.with_extension("json.tmp");
        {
            let mut file = File::create(&temp_path)?;
            file.write_all(text.as_bytes())?;
        }
        Self::durable_rename(&temp_path, path, durable)?;
        Ok(())
    }

    /// Rename `from`→`to`, making the rename itself crash-durable when `durable`.
    ///
    /// POSIX ignores `durable`: the single directory fsync in [`Self::sync`]
    /// already flushes the rename metadata for the whole batch cheaply. Windows
    /// has no directory-fsync (see `sync`), so a durable rename must be
    /// write-through — `MoveFileExW` with `MOVEFILE_WRITE_THROUGH` does not
    /// return until the move is on disk. That flush is per-rename, so only
    /// user-initiated writes request it; derived/bulk writes pass `false` and
    /// rely on NTFS journaling, keeping the large refresh path fast.
    fn durable_rename(from: &Path, to: &Path, durable: bool) -> Result<()> {
        #[cfg(windows)]
        if durable {
            return Self::write_through_rename(from, to);
        }
        #[cfg(not(windows))]
        let _ = durable;
        fs::rename(from, to)?;
        Ok(())
    }

    #[cfg(windows)]
    fn write_through_rename(from: &Path, to: &Path) -> Result<()> {
        use std::os::windows::ffi::OsStrExt;
        use windows_sys::Win32::Storage::FileSystem::{
            MoveFileExW, MOVEFILE_REPLACE_EXISTING, MOVEFILE_WRITE_THROUGH,
        };
        fn wide(p: &Path) -> Vec<u16> {
            p.as_os_str()
                .encode_wide()
                .chain(std::iter::once(0))
                .collect()
        }
        let from_w = wide(from);
        let to_w = wide(to);
        // SAFETY: both pointers reference NUL-terminated UTF-16 buffers that
        // outlive the call; flags are valid MOVE_FILE_FLAGS constants.
        let ok = unsafe {
            MoveFileExW(
                from_w.as_ptr(),
                to_w.as_ptr(),
                MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH,
            )
        };
        if ok == 0 {
            return Err(std::io::Error::last_os_error().into());
        }
        Ok(())
    }
}

/// The fingerprint `stat` gives a file (see [`Fingerprint`]).
pub(super) fn fingerprint(meta: &fs::Metadata) -> Fingerprint {
    #[cfg(unix)]
    let file_id = std::os::unix::fs::MetadataExt::ino(meta);
    #[cfg(not(unix))]
    let file_id = 0;
    Fingerprint {
        size: meta.len(),
        mtime_ns: mtime_ns(meta),
        file_id,
    }
}

/// Modification time in ns since the Unix epoch (negative before it; 0 when
/// the platform reports none).
fn mtime_ns(meta: &fs::Metadata) -> i64 {
    #[cfg(unix)]
    {
        use std::os::unix::fs::MetadataExt;
        meta.mtime()
            .saturating_mul(1_000_000_000)
            .saturating_add(meta.mtime_nsec())
    }
    #[cfg(not(unix))]
    {
        use std::time::UNIX_EPOCH;
        match meta.modified() {
            Ok(t) => match t.duration_since(UNIX_EPOCH) {
                Ok(d) => i64::try_from(d.as_nanos()).unwrap_or(i64::MAX),
                Err(e) => -i64::try_from(e.duration().as_nanos()).unwrap_or(i64::MAX),
            },
            Err(_) => 0,
        }
    }
}
