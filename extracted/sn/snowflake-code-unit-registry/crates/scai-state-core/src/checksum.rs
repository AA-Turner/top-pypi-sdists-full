//! Checksum computation and update policy for code unit file entries.
//!
//! [`ChecksumMode`] selects which file-entry checksums are (re)computed.
//! [`compute_file_checksum`] is the standalone utility for callers that need a
//! hash without going through the registry.
//!
//! # Algorithm
//!
//! xxHash3-128 – produces a 32-character lowercase hex digest (128 bits),
//! matching the `^[a-f0-9]{32}$` pattern enforced by the JSON schema.
//! Non-cryptographic; chosen purely for speed.
//!
//! # Checksum lifecycle
//!
//! Checksums are **not** recomputed automatically on write operations.
//! Callers must explicitly call `update_checksum` to (re)compute hashes
//! for file entries. The `update_checksum` method uses compare-then-update:
//! only entries whose computed hash differs from the stored one are modified.
//!
//! `validate_checksum` is read-only and never fails for per-field issues;
//! problems are captured in the report (e.g. `MissingFile`, `IoError`).

use std::collections::{BTreeMap, HashSet};
use std::fs::{self, File};
use std::io::ErrorKind;
use std::io::Read;
use std::path::{Path, PathBuf};

use rayon::prelude::*;
use snafu::ResultExt;

use crate::error::*;
use crate::generated::types::{CodeUnit, FileEntry, FileEntryChecksum};

// Shared checksum-bearing field names.
pub(crate) const FILES_SOURCE_FIELD: &str = "files.source";
pub(crate) const FILES_CONVERTED_FIELD: &str = "files.converted";
pub(crate) const FILES_SNAPSHOT_FIELD: &str = "files.snapshot";

pub(crate) const CHECKSUM_MODE_NONE: &str = "none";
pub(crate) const CHECKSUM_MODE_SOURCE: &str = "source";
pub(crate) const CHECKSUM_MODE_CONVERTED: &str = "converted";
pub(crate) const CHECKSUM_MODE_SNAPSHOT: &str = "snapshot";
pub(crate) const CHECKSUM_MODE_ALL: &str = "all";

// ── Public enum ─────────────────────────────────────────────────────────────

/// Selects which checksum-bearing file entries should be examined.
///
/// Used by read-only operations (`validate_checksum`, `find_sql_file_changes`)
/// where selective inspection is useful.
///
/// Callers at the FFI boundary (C#, Python) specify the mode as one of
/// the predefined string values (`"none"`, `"source"`, `"converted"`,
/// `"snapshot"`, `"all"`), parsed via [`std::str::FromStr`]. Internal Rust code
/// can also construct arbitrary combinations via the boolean fields.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct ChecksumMode {
    pub source: bool,
    pub converted: bool,
    pub snapshot: bool,
}

impl ChecksumMode {
    pub const NONE: Self = Self {
        source: false,
        converted: false,
        snapshot: false,
    };
    pub const SOURCE: Self = Self {
        source: true,
        converted: false,
        snapshot: false,
    };
    pub const CONVERTED: Self = Self {
        source: false,
        converted: true,
        snapshot: false,
    };
    pub const SNAPSHOT: Self = Self {
        source: false,
        converted: false,
        snapshot: true,
    };
    pub const ALL: Self = Self {
        source: true,
        converted: true,
        snapshot: true,
    };

    pub fn is_none(&self) -> bool {
        !self.source && !self.converted && !self.snapshot
    }
}

impl std::str::FromStr for ChecksumMode {
    type Err = Error;

    /// Parse from the lowercase string representation used by cross-language bindings:
    /// `"none"`, `"source"`, `"converted"`, `"snapshot"`, `"all"`.
    fn from_str(s: &str) -> Result<Self> {
        match s {
            CHECKSUM_MODE_NONE => Ok(Self::NONE),
            CHECKSUM_MODE_SOURCE => Ok(Self::SOURCE),
            CHECKSUM_MODE_CONVERTED => Ok(Self::CONVERTED),
            CHECKSUM_MODE_SNAPSHOT => Ok(Self::SNAPSHOT),
            CHECKSUM_MODE_ALL => Ok(Self::ALL),
            other => InvalidChecksumModeSnafu { input: other }.fail(),
        }
    }
}

/// Validation status for a single checksum-bearing field.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ChecksumValidationStatus {
    Match,
    Mismatch,
    MissingPath,
    MissingChecksum,
    MissingFile,
    Skipped,
    IoError,
}

/// Per-field checksum validation result.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ChecksumValidationEntry {
    pub field: String,
    pub status: ChecksumValidationStatus,
    pub stored_checksum: Option<String>,
    pub computed_checksum: Option<String>,
}

/// Checksum validation report.
#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ChecksumValidationReport {
    pub entries: Vec<ChecksumValidationEntry>,
}

// ── Public utility ───────────────────────────────────────────────────────────

/// Hash an in-memory buffer with xxHash3-128; returns a 32-character lowercase hex digest.
///
/// Matches the output format of [`compute_file_checksum`] and the `^[a-f0-9]{32}$`
/// schema constraint.
pub fn compute_buffer_checksum(buf: &[u8]) -> FileEntryChecksum {
    let hex = format!("{:032x}", xxhash_rust::xxh3::xxh3_128(buf));
    hex.parse()
        .expect("xxHash3-128 digest always satisfies ^[a-f0-9]{32}$")
}

/// Hash a file with xxHash3-128 and return the 32-character lowercase hex digest.
///
/// The path must be absolute, or relative to the current working directory.
/// Registry internals resolve repo-relative paths before calling this.
///
/// Reads the file in 64 KiB chunks so that large files never need to be
/// held in memory all at once.
pub fn compute_file_checksum(path: impl AsRef<Path>) -> Result<String> {
    let p = path.as_ref();
    let path_str = p.display().to_string();
    let mut file = File::open(p).context(FileIoSnafu {
        op: "open",
        path: &path_str,
    })?;
    let mut hasher = xxhash_rust::xxh3::Xxh3Default::new();
    let mut buf = [0u8; 65536];
    loop {
        let n = file.read(&mut buf).context(FileIoSnafu {
            op: "read",
            path: &path_str,
        })?;
        if n == 0 {
            break;
        }
        hasher.update(&buf[..n]);
    }
    Ok(format!("{:032x}", hasher.digest128()))
}

/// Recompute checksums for file entries selected by `mode`.
///
/// Only updates the checksum field when the computed value differs from
/// the stored one (compare-then-update). This ensures future `updatedAt`
/// timestamps are only set when the file content actually changed.
///
/// Missing entries are skipped. Missing paths clear the checksum.
pub(crate) fn apply_checksums(
    code_unit: &mut CodeUnit,
    mode: &ChecksumMode,
    base_path: &Path,
) -> Result<()> {
    if mode.is_none() {
        return Ok(());
    }
    if let Some(files) = code_unit.files.as_mut() {
        if mode.source {
            refresh_file_entry_checksum(files.source.as_mut(), base_path)?;
        }
        if mode.converted {
            refresh_file_entry_checksum(files.converted.as_mut(), base_path)?;
        }
        if mode.snapshot {
            refresh_file_entry_checksum(files.snapshot.as_mut(), base_path)?;
        }
    }
    Ok(())
}

/// Validate selected checksums and return detailed per-field status entries.
pub(crate) fn validate_checksum_report(
    code_unit: &CodeUnit,
    mode: &ChecksumMode,
    base_path: &Path,
) -> ChecksumValidationReport {
    let mut report = ChecksumValidationReport::default();
    let files = code_unit.files.as_ref();

    let selected = |field: &str| -> bool {
        match field {
            FILES_SOURCE_FIELD => mode.source,
            FILES_CONVERTED_FIELD => mode.converted,
            FILES_SNAPSHOT_FIELD => mode.snapshot,
            _ => false,
        }
    };

    report.entries.push(validate_file_entry_checksum(
        FILES_SOURCE_FIELD,
        files.and_then(|f| f.source.as_ref()),
        selected(FILES_SOURCE_FIELD),
        base_path,
    ));
    report.entries.push(validate_file_entry_checksum(
        FILES_CONVERTED_FIELD,
        files.and_then(|f| f.converted.as_ref()),
        selected(FILES_CONVERTED_FIELD),
        base_path,
    ));
    report.entries.push(validate_file_entry_checksum(
        FILES_SNAPSHOT_FIELD,
        files.and_then(|f| f.snapshot.as_ref()),
        selected(FILES_SNAPSHOT_FIELD),
        base_path,
    ));

    report
}

// ── Internal ─────────────────────────────────────────────────────────────────

/// Recompute and set checksum for one optional entry (compare-then-update).
///
/// Missing entry is skipped. Missing path clears any existing checksum.
/// Only writes the new checksum when it differs from the stored value.
fn refresh_file_entry_checksum(entry: Option<&mut FileEntry>, base_path: &Path) -> Result<()> {
    let Some(entry) = entry else {
        return Ok(());
    };

    let Some(path_str) = entry.path.as_deref() else {
        entry.checksum = None;
        return Ok(());
    };

    let joined = base_path.join(path_str);
    let digest = compute_file_checksum(&joined)?;
    let new_checksum: FileEntryChecksum = digest
        .parse()
        .expect("xxHash3-128 digest always satisfies ^[a-f0-9]{32}$");

    let changed = entry
        .checksum
        .as_ref()
        .is_none_or(|old| old.as_str() != new_checksum.as_str());

    if changed {
        entry.checksum = Some(new_checksum);
    }
    Ok(())
}

fn validate_file_entry_checksum(
    field: &str,
    entry: Option<&FileEntry>,
    selected: bool,
    base_path: &Path,
) -> ChecksumValidationEntry {
    if !selected {
        return ChecksumValidationEntry {
            field: field.to_string(),
            status: ChecksumValidationStatus::Skipped,
            stored_checksum: None,
            computed_checksum: None,
        };
    }

    let Some(entry) = entry else {
        return ChecksumValidationEntry {
            field: field.to_string(),
            status: ChecksumValidationStatus::MissingPath,
            stored_checksum: None,
            computed_checksum: None,
        };
    };

    let stored_checksum = entry.checksum.as_ref().map(|c| c.to_string());
    let Some(path_str) = entry.path.as_deref() else {
        return ChecksumValidationEntry {
            field: field.to_string(),
            status: ChecksumValidationStatus::MissingPath,
            stored_checksum,
            computed_checksum: None,
        };
    };

    match compute_file_checksum(base_path.join(path_str)) {
        Ok(computed) => {
            let status = match stored_checksum.as_ref() {
                None => ChecksumValidationStatus::MissingChecksum,
                Some(stored) if *stored == computed => ChecksumValidationStatus::Match,
                Some(_) => ChecksumValidationStatus::Mismatch,
            };
            ChecksumValidationEntry {
                field: field.to_string(),
                status,
                stored_checksum,
                computed_checksum: Some(computed),
            }
        }
        Err(e) => {
            // `NotFound` is reported as the more specific `MissingFile` status.
            let status = match io_error_kind(&e) {
                Some(ErrorKind::NotFound) => ChecksumValidationStatus::MissingFile,
                _ => ChecksumValidationStatus::IoError,
            };
            ChecksumValidationEntry {
                field: field.to_string(),
                status,
                stored_checksum,
                computed_checksum: None,
            }
        }
    }
}

/// Extract the underlying [`std::io::ErrorKind`] from any error variant that
/// wraps an `io::Error`. Returns `None` for non-I/O variants.
fn io_error_kind(err: &Error) -> Option<ErrorKind> {
    match err {
        Error::IoError { source, .. } | Error::FileIoError { source, .. } => Some(source.kind()),
        _ => None,
    }
}

// ── Source-code change detection ─────────────────────────────────────────────

/// Whether a file change refers to a source or converted file.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum FileType {
    Source,
    Converted,
}

impl FileType {
    fn as_field_name(&self) -> &'static str {
        match self {
            Self::Source => "source",
            Self::Converted => "converted",
        }
    }
}

/// The kind of change detected for a file.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ChangeType {
    Modified,
    Removed,
    Added,
}

/// A single file-level change: path, whether it's source or converted,
/// and whether it was modified, removed, or added (untracked).
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct FileChange {
    pub path: String,
    pub file_type: FileType,
    pub change_type: ChangeType,
}

/// A file entry that could not be checked due to an I/O error (e.g. permission
/// denied). Distinguished from `Removed` which means the file simply does not
/// exist.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct ChecksumScanError {
    /// Code unit ID.
    pub id: String,
    /// Which file entry failed (e.g. `"source"`, `"converted"`).
    pub field: String,
    /// Human-readable error message.
    pub message: String,
}

/// Result of scanning the project for source-code changes.
///
/// * `code_unit_changes` maps code-unit IDs to the list of file-level
///   changes detected for that unit (modified or removed files).
/// * `untracked_files` lists files found under `source/` or `snowflake/`
///   that are not referenced by any code unit.
/// * `errors` lists file entries that could not be checked due to I/O
///   errors (permission denied, disk failure, etc.).
#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct SourceCodeChanges {
    pub code_unit_changes: BTreeMap<String, Vec<FileChange>>,
    pub untracked_files: Vec<FileChange>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub errors: Vec<ChecksumScanError>,
}

/// Per-unit result from parallel checksum scanning.
struct UnitScanResult {
    id: String,
    changes: Vec<FileChange>,
    tracked_source: Option<String>,
    tracked_converted: Option<String>,
    errors: Vec<ChecksumScanError>,
}

/// Scan `code_units` for modified/removed files and walk `source_dir` /
/// `snowflake_dir` for untracked files.
///
/// `mode` selects which file entries to check: `source`, `converted`, or
/// both. Snapshot entries are ignored by this function.
///
/// Per-unit checksum verification runs in parallel via rayon.
pub(crate) fn find_sql_file_changes(
    code_units: &[CodeUnit],
    mode: &ChecksumMode,
    base_path: &Path,
    source_dir: &Path,
    snowflake_dir: &Path,
) -> SourceCodeChanges {
    let per_unit: Vec<UnitScanResult> = code_units
        .par_iter()
        .filter_map(|unit| {
            let id = unit.id.as_ref()?.clone();
            let files = unit.files.as_ref()?;
            let mut changes = Vec::new();
            let mut errors = Vec::new();
            let mut tracked_source = None;
            let mut tracked_converted = None;

            let entries: [(bool, Option<&FileEntry>, FileType); 2] = [
                (mode.source, files.source.as_ref(), FileType::Source),
                (
                    mode.converted,
                    files.converted.as_ref(),
                    FileType::Converted,
                ),
            ];
            for (enabled, entry, file_type) in entries {
                if !enabled {
                    continue;
                }
                let is_source = matches!(file_type, FileType::Source);
                let check = check_file_entry(entry, base_path, file_type, &id);
                if let Some(path) = check.tracked_path {
                    if is_source {
                        tracked_source = Some(path);
                    } else {
                        tracked_converted = Some(path);
                    }
                }
                match check.outcome {
                    FileEntryOutcome::Changed(c) => changes.push(c),
                    FileEntryOutcome::Error(e) => errors.push(e),
                    FileEntryOutcome::NoEntry | FileEntryOutcome::Unchanged => {}
                }
            }

            Some(UnitScanResult {
                id,
                changes,
                tracked_source,
                tracked_converted,
                errors,
            })
        })
        .collect();

    let mut code_unit_changes: BTreeMap<String, Vec<FileChange>> = BTreeMap::new();
    let mut tracked_source_paths: HashSet<String> = HashSet::new();
    let mut tracked_converted_paths: HashSet<String> = HashSet::new();
    let mut errors: Vec<ChecksumScanError> = Vec::new();

    for r in per_unit {
        if let Some(p) = r.tracked_source {
            tracked_source_paths.insert(p);
        }
        if let Some(p) = r.tracked_converted {
            tracked_converted_paths.insert(p);
        }
        errors.extend(r.errors);
        if !r.changes.is_empty() {
            code_unit_changes.insert(r.id, r.changes);
        }
    }

    let untracked_files = collect_untracked_files(
        mode,
        base_path,
        source_dir,
        snowflake_dir,
        &tracked_source_paths,
        &tracked_converted_paths,
    );

    SourceCodeChanges {
        code_unit_changes,
        untracked_files,
        errors,
    }
}

fn collect_untracked_files(
    mode: &ChecksumMode,
    base_path: &Path,
    source_dir: &Path,
    snowflake_dir: &Path,
    tracked_source_paths: &HashSet<String>,
    tracked_converted_paths: &HashSet<String>,
) -> Vec<FileChange> {
    let mut untracked = Vec::new();

    let scan_targets: &[(bool, &Path, &HashSet<String>, FileType)] = &[
        (
            mode.source,
            source_dir,
            tracked_source_paths,
            FileType::Source,
        ),
        (
            mode.converted,
            snowflake_dir,
            tracked_converted_paths,
            FileType::Converted,
        ),
    ];
    for &(enabled, dir, tracked, ref file_type) in scan_targets {
        if !enabled || !dir.exists() {
            continue;
        }
        let mut disk_files = Vec::new();
        walk_files(dir, &mut disk_files);
        for abs_path in disk_files {
            if let Ok(rel_path) = abs_path.strip_prefix(base_path) {
                let rel_str = normalize_path(rel_path);
                if !tracked.contains(&rel_str) {
                    untracked.push(FileChange {
                        path: rel_str,
                        file_type: file_type.clone(),
                        change_type: ChangeType::Added,
                    });
                }
            }
        }
    }

    untracked.sort_by(|a, b| a.path.cmp(&b.path));
    untracked
}

struct FileEntryCheck {
    tracked_path: Option<String>,
    outcome: FileEntryOutcome,
}

enum FileEntryOutcome {
    NoEntry,
    Unchanged,
    Changed(FileChange),
    Error(ChecksumScanError),
}

fn check_file_entry(
    entry: Option<&FileEntry>,
    base_path: &Path,
    file_type: FileType,
    code_unit_id: &str,
) -> FileEntryCheck {
    let Some(fe) = entry else {
        return FileEntryCheck {
            tracked_path: None,
            outcome: FileEntryOutcome::NoEntry,
        };
    };
    let Some(path_str) = fe.path.as_deref() else {
        return FileEntryCheck {
            tracked_path: None,
            outcome: FileEntryOutcome::NoEntry,
        };
    };
    let tracked_path = Some(path_str.to_string());

    let Some(stored) = fe.checksum.as_ref() else {
        return FileEntryCheck {
            tracked_path,
            outcome: FileEntryOutcome::Unchanged,
        };
    };

    let outcome = match compute_file_checksum(base_path.join(path_str)) {
        Ok(computed) if *stored.to_string() == computed => FileEntryOutcome::Unchanged,
        Ok(_) => FileEntryOutcome::Changed(FileChange {
            path: path_str.to_string(),
            file_type,
            change_type: ChangeType::Modified,
        }),
        Err(e) if io_error_kind(&e) == Some(std::io::ErrorKind::NotFound) => {
            FileEntryOutcome::Changed(FileChange {
                path: path_str.to_string(),
                file_type,
                change_type: ChangeType::Removed,
            })
        }
        Err(e) => FileEntryOutcome::Error(ChecksumScanError {
            id: code_unit_id.to_string(),
            field: file_type.as_field_name().to_string(),
            message: e.to_string(),
        }),
    };

    FileEntryCheck {
        tracked_path,
        outcome,
    }
}

fn walk_files(dir: &Path, out: &mut Vec<PathBuf>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.is_dir() {
            walk_files(&path, out);
        } else if path.is_file() {
            out.push(path);
        }
    }
}

fn normalize_path(path: &Path) -> String {
    crate::registry::paths::normalize_os_path(path)
}

// ── Tests ────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    use std::fs;
    use test_case::test_case;

    fn write_temp_file(name: &str, content: &[u8]) -> std::path::PathBuf {
        let path = env::temp_dir().join(format!("scai-checksum-test-{}", name));
        fs::write(&path, content).unwrap();
        path
    }

    // ── ChecksumMode parsing (via FromStr) ──────────────────────────────

    #[test_case("none"      => ChecksumMode::NONE      ; "none")]
    #[test_case("source"    => ChecksumMode::SOURCE    ; "source")]
    #[test_case("converted" => ChecksumMode::CONVERTED ; "converted")]
    #[test_case("snapshot"  => ChecksumMode::SNAPSHOT  ; "snapshot")]
    #[test_case("all"       => ChecksumMode::ALL       ; "all")]
    fn parse_valid_mode(input: &str) -> ChecksumMode {
        input.parse().unwrap()
    }

    #[test]
    fn parse_invalid_mode_returns_error() {
        let err = "sha256".parse::<ChecksumMode>().unwrap_err();
        assert_eq!(err.error_code_i32(), 1013);
        assert!(err.to_string().contains("sha256"));
    }

    #[test]
    fn default_mode_is_none() {
        let mode = ChecksumMode::default();
        assert_eq!(mode, ChecksumMode::NONE);
        assert!(mode.is_none());
    }

    #[test_case(ChecksumMode::SOURCE    ; "source")]
    #[test_case(ChecksumMode::CONVERTED ; "converted")]
    #[test_case(ChecksumMode::SNAPSHOT  ; "snapshot")]
    #[test_case(ChecksumMode::ALL       ; "all")]
    fn is_none_returns_false(mode: ChecksumMode) {
        assert!(!mode.is_none());
    }

    // ── compute_file_checksum ────────────────────────────────────────────

    #[test]
    fn checksum_is_32_hex_chars() {
        let path = write_temp_file("hex-chars.txt", b"hello");
        let digest = compute_file_checksum(&path).unwrap();
        assert_eq!(digest.len(), 32);
        assert!(digest.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn checksum_is_deterministic() {
        let path = write_temp_file("deterministic.txt", b"deterministic content");
        let a = compute_file_checksum(&path).unwrap();
        let b = compute_file_checksum(&path).unwrap();
        assert_eq!(a, b);
    }

    #[test]
    fn different_content_produces_different_checksum() {
        let p1 = write_temp_file("diff-a.txt", b"content A");
        let p2 = write_temp_file("diff-b.txt", b"content B");
        assert_ne!(
            compute_file_checksum(&p1).unwrap(),
            compute_file_checksum(&p2).unwrap(),
        );
    }

    #[test]
    fn checksum_missing_file_returns_file_io_error() {
        let missing = "/nonexistent/path/file.sql";
        let err = compute_file_checksum(missing).unwrap_err();
        assert_eq!(err.error_code_i32(), 1023); // FileIoError
        let msg = err.to_string();
        assert!(
            msg.contains(missing),
            "error message should include the attempted path for debuggability, got: {msg}"
        );
        assert!(
            msg.contains("open"),
            "error message should identify the failing operation (open), got: {msg}"
        );

        // The structured `details` payload must surface op + path as separate
        // fields so cross-language callers can react without parsing strings.
        let details = err
            .info()
            .details
            .expect("FileIoError carries op + path in details");
        assert_eq!(details["op"], "open");
        assert_eq!(details["path"], missing);
    }

    /// When the filename on disk literally contains a backslash (as happens
    /// when a Windows-sourced archive is extracted on macOS without
    /// translating path separators), Rust's [`File::open`] handles the
    /// backslash as a regular byte and reads the file normally.
    ///
    /// This test guards against any future regression that would treat `\` as
    /// a path separator on Unix platforms.
    #[cfg(unix)]
    #[test]
    fn checksum_handles_literal_backslash_in_filename() {
        let dir = tempfile::TempDir::new().unwrap();
        let file_path = dir.path().join("brg\\bcis.sql");
        std::fs::write(&file_path, b"SELECT 1").unwrap();

        let digest = compute_file_checksum(&file_path)
            .expect("compute_file_checksum must handle '\\' in Unix filenames");
        assert_eq!(digest.len(), 32);
    }

    #[test]
    fn known_xxhash3_digest_via_file() {
        let path = write_temp_file("empty.bin", b"");
        let digest = compute_file_checksum(&path).unwrap();
        let expected = format!("{:032x}", xxhash_rust::xxh3::xxh3_128(b""));
        assert_eq!(digest, expected);
    }

    // ── find_sql_file_changes ─────────────────────────────────────────

    mod source_code_changes {
        use super::*;
        use crate::generated::types::{FileEntry, FileEntryChecksum, Files};
        use tempfile::TempDir;

        fn temp_dir() -> TempDir {
            TempDir::new().unwrap()
        }

        fn write_file(base: &std::path::Path, rel: &str, content: &[u8]) {
            let path = base.join(rel);
            fs::create_dir_all(path.parent().unwrap()).unwrap();
            fs::write(&path, content).unwrap();
        }

        fn checksum_of(content: &[u8]) -> FileEntryChecksum {
            let hex = format!("{:032x}", xxhash_rust::xxh3::xxh3_128(content));
            hex.parse().unwrap()
        }

        fn make_unit(
            id: &str,
            source_path: Option<&str>,
            source_checksum: Option<FileEntryChecksum>,
            converted_path: Option<&str>,
            converted_checksum: Option<FileEntryChecksum>,
        ) -> CodeUnit {
            let make_entry = |path: Option<&str>, cksum: Option<FileEntryChecksum>| {
                path.map(|p| FileEntry {
                    path: Some(p.to_string()),
                    checksum: cksum,
                })
            };
            CodeUnit {
                id: Some(id.to_string()),
                files: Some(Files {
                    artifacts: None,
                    source: make_entry(source_path, source_checksum),
                    converted: make_entry(converted_path, converted_checksum),
                    snapshot: None,
                }),
                ..Default::default()
            }
        }

        #[test]
        fn no_changes_when_checksums_match() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/a.sql", b"SELECT 1");
            write_file(base, "snowflake/a.sql", b"SELECT 1 /* converted */");

            let units = vec![make_unit(
                "u1",
                Some("source/a.sql"),
                Some(checksum_of(b"SELECT 1")),
                Some("snowflake/a.sql"),
                Some(checksum_of(b"SELECT 1 /* converted */")),
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::ALL,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
            assert!(result.untracked_files.is_empty());
        }

        #[test]
        fn detects_modified_source() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/a.sql", b"SELECT 2 -- modified");

            let units = vec![make_unit(
                "u1",
                Some("source/a.sql"),
                Some(checksum_of(b"SELECT 1")),
                None,
                None,
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            let changes = &result.code_unit_changes["u1"];
            assert_eq!(changes.len(), 1);
            assert_eq!(changes[0].file_type, FileType::Source);
            assert_eq!(changes[0].change_type, ChangeType::Modified);
            assert_eq!(changes[0].path, "source/a.sql");
        }

        #[test]
        fn detects_modified_converted() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "snowflake/b.sql", b"new content");

            let units = vec![make_unit(
                "u1",
                None,
                None,
                Some("snowflake/b.sql"),
                Some(checksum_of(b"old content")),
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::CONVERTED,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            let changes = &result.code_unit_changes["u1"];
            assert_eq!(changes.len(), 1);
            assert_eq!(changes[0].file_type, FileType::Converted);
            assert_eq!(changes[0].change_type, ChangeType::Modified);
        }

        #[test]
        fn detects_removed_source() {
            let dir = temp_dir();
            let base = dir.path();
            // file does NOT exist on disk

            let units = vec![make_unit(
                "u1",
                Some("source/gone.sql"),
                Some(checksum_of(b"was here")),
                None,
                None,
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            let changes = &result.code_unit_changes["u1"];
            assert_eq!(changes.len(), 1);
            assert_eq!(changes[0].change_type, ChangeType::Removed);
            assert_eq!(changes[0].path, "source/gone.sql");
        }

        #[test]
        fn detects_removed_converted() {
            let dir = temp_dir();
            let base = dir.path();

            let units = vec![make_unit(
                "u1",
                None,
                None,
                Some("snowflake/gone.sql"),
                Some(checksum_of(b"was here")),
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::CONVERTED,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            let changes = &result.code_unit_changes["u1"];
            assert_eq!(changes.len(), 1);
            assert_eq!(changes[0].file_type, FileType::Converted);
            assert_eq!(changes[0].change_type, ChangeType::Removed);
        }

        #[test]
        fn detects_untracked_source_files() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/tracked.sql", b"ok");
            write_file(base, "source/extra.sql", b"surprise");
            write_file(base, "source/sub/deep.sql", b"nested");

            let units = vec![make_unit(
                "u1",
                Some("source/tracked.sql"),
                Some(checksum_of(b"ok")),
                None,
                None,
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
            assert_eq!(result.untracked_files.len(), 2);
            assert!(result
                .untracked_files
                .iter()
                .all(|f| f.file_type == FileType::Source && f.change_type == ChangeType::Added));
            let paths: Vec<&str> = result
                .untracked_files
                .iter()
                .map(|f| f.path.as_str())
                .collect();
            assert!(paths.contains(&"source/extra.sql"));
            assert!(paths.contains(&"source/sub/deep.sql"));
        }

        #[test]
        fn detects_untracked_converted_files() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "snowflake/orphan.sql", b"no code unit");

            let units: Vec<CodeUnit> = vec![];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::CONVERTED,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert_eq!(result.untracked_files.len(), 1);
            assert_eq!(result.untracked_files[0].path, "snowflake/orphan.sql");
            assert_eq!(result.untracked_files[0].file_type, FileType::Converted);
            assert_eq!(result.untracked_files[0].change_type, ChangeType::Added);
        }

        #[test]
        fn mode_source_ignores_converted() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/a.sql", b"SELECT 1");
            write_file(base, "snowflake/a.sql", b"modified!");

            let units = vec![make_unit(
                "u1",
                Some("source/a.sql"),
                Some(checksum_of(b"SELECT 1")),
                Some("snowflake/a.sql"),
                Some(checksum_of(b"original")),
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
        }

        #[test]
        fn mode_converted_ignores_source() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/a.sql", b"modified!");
            write_file(base, "snowflake/a.sql", b"SELECT 1");

            let units = vec![make_unit(
                "u1",
                Some("source/a.sql"),
                Some(checksum_of(b"original")),
                Some("snowflake/a.sql"),
                Some(checksum_of(b"SELECT 1")),
            )];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::CONVERTED,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
        }

        #[test]
        fn mixed_changes_across_multiple_units() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/a.sql", b"changed");
            // source/b.sql does NOT exist (removed)
            write_file(base, "source/c.sql", b"unchanged");

            let units = vec![
                make_unit(
                    "u1",
                    Some("source/a.sql"),
                    Some(checksum_of(b"original")),
                    None,
                    None,
                ),
                make_unit(
                    "u2",
                    Some("source/b.sql"),
                    Some(checksum_of(b"was here")),
                    None,
                    None,
                ),
                make_unit(
                    "u3",
                    Some("source/c.sql"),
                    Some(checksum_of(b"unchanged")),
                    None,
                    None,
                ),
            ];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert_eq!(result.code_unit_changes.len(), 2);
            assert_eq!(
                result.code_unit_changes["u1"][0].change_type,
                ChangeType::Modified
            );
            assert_eq!(
                result.code_unit_changes["u2"][0].change_type,
                ChangeType::Removed
            );
            assert!(!result.code_unit_changes.contains_key("u3"));
        }

        #[test]
        fn nonexistent_dirs_produce_no_untracked() {
            let dir = temp_dir();
            let base = dir.path();

            let result = find_sql_file_changes(
                &[],
                &ChecksumMode::ALL,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
            assert!(result.untracked_files.is_empty());
        }

        #[test]
        fn untracked_files_are_sorted_by_path() {
            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/z.sql", b"z");
            write_file(base, "source/a.sql", b"a");
            write_file(base, "source/m.sql", b"m");

            let result = find_sql_file_changes(
                &[],
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            let paths: Vec<&str> = result
                .untracked_files
                .iter()
                .map(|f| f.path.as_str())
                .collect();
            assert_eq!(paths, vec!["source/a.sql", "source/m.sql", "source/z.sql"]);
        }

        #[test]
        fn unit_without_files_is_skipped() {
            let dir = temp_dir();
            let base = dir.path();

            let unit = CodeUnit {
                id: Some("no-files".to_string()),
                files: None,
                ..Default::default()
            };

            let result = find_sql_file_changes(
                &[unit],
                &ChecksumMode::ALL,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            assert!(result.code_unit_changes.is_empty());
        }

        #[cfg(unix)]
        #[test]
        fn io_error_reported_separately_from_removed() {
            use std::os::unix::fs::PermissionsExt;

            let dir = temp_dir();
            let base = dir.path();
            write_file(base, "source/readable.sql", b"ok");
            write_file(base, "source/unreadable.sql", b"secret");

            let unreadable_path = base.join("source/unreadable.sql");
            fs::set_permissions(&unreadable_path, fs::Permissions::from_mode(0o000)).unwrap();

            let readable_checksum = checksum_of(b"ok");
            let stale_checksum: FileEntryChecksum = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1"
                .to_string()
                .try_into()
                .unwrap();

            let units = vec![
                CodeUnit {
                    id: Some("u-readable".to_string()),
                    files: Some(Files {
                        source: Some(FileEntry {
                            path: Some("source/readable.sql".to_string()),
                            checksum: Some(readable_checksum),
                        }),
                        ..Default::default()
                    }),
                    ..Default::default()
                },
                CodeUnit {
                    id: Some("u-unreadable".to_string()),
                    files: Some(Files {
                        source: Some(FileEntry {
                            path: Some("source/unreadable.sql".to_string()),
                            checksum: Some(stale_checksum),
                        }),
                        ..Default::default()
                    }),
                    ..Default::default()
                },
                CodeUnit {
                    id: Some("u-missing".to_string()),
                    files: Some(Files {
                        source: Some(FileEntry {
                            path: Some("source/gone.sql".to_string()),
                            checksum: Some(
                                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2"
                                    .to_string()
                                    .try_into()
                                    .unwrap(),
                            ),
                        }),
                        ..Default::default()
                    }),
                    ..Default::default()
                },
            ];

            let result = find_sql_file_changes(
                &units,
                &ChecksumMode::SOURCE,
                base,
                &base.join("source"),
                &base.join("snowflake"),
            );

            // Restore permissions so temp dir cleanup works
            fs::set_permissions(&unreadable_path, fs::Permissions::from_mode(0o644)).unwrap();

            // Missing file → Removed in code_unit_changes
            assert!(result.code_unit_changes.contains_key("u-missing"));
            assert_eq!(
                result.code_unit_changes["u-missing"][0].change_type,
                ChangeType::Removed
            );

            // Unreadable file → error, NOT in code_unit_changes
            assert!(!result.code_unit_changes.contains_key("u-unreadable"));
            assert_eq!(result.errors.len(), 1);
            assert_eq!(result.errors[0].id, "u-unreadable");
            assert_eq!(result.errors[0].field, "source");
            assert!(
                result.errors[0].message.contains("ermission denied")
                    || result.errors[0].message.contains("denied")
            );

            // Readable + matching checksum → no change, no error
            assert!(!result.code_unit_changes.contains_key("u-readable"));
        }
    }
}
