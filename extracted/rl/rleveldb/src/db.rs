use std::collections::HashMap;
use std::fmt;
use std::path::{Path, PathBuf};

use crate::ldb_file::LdbFile;
use crate::log_file::LogFile;
use crate::manifest::ManifestFile;
use crate::types::Record;

#[derive(Debug)]
pub enum DbError {
    NotADirectory(PathBuf),
    Io(std::io::Error),
    Ldb(crate::ldb_file::LdbError),
    Log(crate::log_file::LogError),
    Manifest(crate::manifest::ManifestError),
}

impl fmt::Display for DbError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            DbError::NotADirectory(p) => write!(f, "Not a directory: {}", p.display()),
            DbError::Io(e) => write!(f, "IO error: {e}"),
            DbError::Ldb(e) => write!(f, "LDB error: {e}"),
            DbError::Log(e) => write!(f, "Log error: {e}"),
            DbError::Manifest(e) => write!(f, "Manifest error: {e}"),
        }
    }
}

impl std::error::Error for DbError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            DbError::Io(e) => Some(e),
            DbError::Ldb(e) => Some(e),
            DbError::Log(e) => Some(e),
            DbError::Manifest(e) => Some(e),
            DbError::NotADirectory(_) => None,
        }
    }
}

impl From<std::io::Error> for DbError {
    fn from(e: std::io::Error) -> Self {
        DbError::Io(e)
    }
}

impl From<crate::ldb_file::LdbError> for DbError {
    fn from(e: crate::ldb_file::LdbError) -> Self {
        DbError::Ldb(e)
    }
}

impl From<crate::log_file::LogError> for DbError {
    fn from(e: crate::log_file::LogError) -> Self {
        DbError::Log(e)
    }
}

impl From<crate::manifest::ManifestError> for DbError {
    fn from(e: crate::manifest::ManifestError) -> Self {
        DbError::Manifest(e)
    }
}

enum DataFile {
    Ldb(LdbFile),
    Log(LogFile),
}

impl DataFile {
    fn file_no(&self) -> u64 {
        match self {
            DataFile::Ldb(f) => f.file_no,
            DataFile::Log(f) => f.file_no,
        }
    }

    fn records(&self) -> Vec<Record> {
        match self {
            DataFile::Ldb(f) => f.records(),
            DataFile::Log(f) => f.records(),
        }
    }
}

pub struct RawLevelDb {
    in_dir: PathBuf,
    files: Vec<DataFile>,
    pub manifest: Option<ManifestFile>,
}

impl RawLevelDb {
    pub fn open(in_dir: &Path) -> Result<Self, DbError> {
        if !in_dir.is_dir() {
            return Err(DbError::NotADirectory(in_dir.to_path_buf()));
        }

        let mut files = Vec::new();
        let mut latest_manifest: Option<(u64, PathBuf)> = None;

        for entry in std::fs::read_dir(in_dir).map_err(DbError::Io)? {
            let entry = entry.map_err(DbError::Io)?;
            let path = entry.path();
            if !path.is_file() {
                continue;
            }

            let name = match path.file_name().and_then(|n| n.to_str()) {
                Some(n) => n.to_string(),
                None => continue,
            };

            // Check data files: 6 decimal digits + .ldb/.log/.sst extension
            if let Some(ext) = path.extension().and_then(|e| e.to_str()) {
                let stem = path.file_stem().and_then(|s| s.to_str()).unwrap_or("");
                if stem.len() == 6 && stem.chars().all(|c| c.is_ascii_digit()) {
                    match ext.to_lowercase().as_str() {
                        "log" => {
                            if let Ok(f) = LogFile::open(&path) {
                                files.push(DataFile::Log(f));
                            }
                        }
                        "ldb" | "sst" => {
                            if let Ok(f) = LdbFile::open(&path) {
                                files.push(DataFile::Ldb(f));
                            }
                        }
                        _ => {}
                    }
                }
            }

            // Check manifest files (MANIFEST-{hex_number})
            if let Some(hex_part) = name.strip_prefix("MANIFEST-") {
                if let Ok(no) = u64::from_str_radix(hex_part, 16) {
                    match &latest_manifest {
                        Some((current_no, _)) if *current_no >= no => {}
                        _ => latest_manifest = Some((no, path)),
                    }
                }
            }
        }

        let manifest = if let Some((_, path)) = latest_manifest {
            ManifestFile::open(&path).ok()
        } else {
            None
        };

        Ok(Self {
            in_dir: in_dir.to_path_buf(),
            files,
            manifest,
        })
    }

    pub fn in_dir_path(&self) -> &Path {
        &self.in_dir
    }

    /// Get the file-to-level mapping from the manifest, if available.
    pub fn file_to_level(&self) -> Option<&HashMap<u64, u64>> {
        self.manifest.as_ref().map(|m| &m.file_to_level)
    }

    /// Iterate all records, sorted by file number.
    pub fn iterate_records_raw(&self, reverse: bool) -> Vec<Record> {
        let mut sorted_indices: Vec<usize> = (0..self.files.len()).collect();
        sorted_indices.sort_by_key(|&i| self.files[i].file_no());
        if reverse {
            sorted_indices.reverse();
        }

        let mut records = Vec::new();
        for i in sorted_indices {
            records.extend(self.files[i].records());
        }
        records
    }
}
