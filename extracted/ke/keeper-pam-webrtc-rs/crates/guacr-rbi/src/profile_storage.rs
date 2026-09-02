// Profile storage configuration for RBI persistent Chrome profiles.
//
// This module is the configuration and validation layer on top of
// `profile_isolation::ProfileLock`. Callers parse `ProfileStorageConfig`
// from connection parameters, call `validate_and_prepare` to get a resolved
// directory path, and then use the re-exported `acquire_lock` to hold the
// exclusive lock for the session lifetime.
//
// Locking mechanism
// -----------------
// On Linux: `libc::flock(LOCK_EX | LOCK_NB)` — kernel-level advisory lock that
//   survives process crashes (the OS releases it when the fd is closed).
//   Implemented in `profile_isolation::ProfileLock`.
// On non-Linux: `OpenOptions::create_new` atomically creates a lock file;
//   lock release deletes the file.  Only partially crash-safe (stale file
//   on hard crash) — intended primarily for dev/macOS use.
//   Also implemented in `profile_isolation::ProfileLock`.
//
// The lock is cross-platform in that it compiles everywhere; the strength
// of the guarantee differs between Linux (kernel flock) and non-Linux
// (file existence check).

use crate::profile_isolation::{ProfileCreationMode, ProfileLock, ProfileLockError};
use std::collections::HashMap;
use std::path::{Component, PathBuf};

// Re-export so callers can hold the lock without importing profile_isolation.
pub(crate) use crate::profile_isolation::ProfileLock as ProfileLockHandle;

/// Configuration for Chrome profile directory storage.
///
/// Parsed from connection parameters:
/// - `profile-path` — absolute path to the Chrome user-data-dir to persist.
///   When absent the session uses a temporary directory discarded on session end.
/// - `profile-create` — `"true"` to create the directory if it does not exist;
///   defaults to `false`.
#[derive(Debug, Clone, Default)]
pub struct ProfileStorageConfig {
    /// Path to the Chrome user-data-dir.  `None` = use a fresh temp dir.
    pub path: Option<PathBuf>,
    /// Create the directory if it does not exist (default: false).
    pub create_if_missing: bool,
}

impl ProfileStorageConfig {
    /// Parse a `ProfileStorageConfig` from connection parameters.
    ///
    /// Validation rules applied here (before any filesystem access):
    /// - Empty `profile-path` string → `Err`.
    /// - Any `..` component in the path → `Err` (path traversal rejected).
    pub fn from_params(params: &HashMap<String, String>) -> Result<Self, String> {
        let path = match params.get("profile-path") {
            None => None,
            Some(s) if s.is_empty() => {
                return Err("profile-path must not be an empty string".to_string());
            }
            Some(s) => {
                let p = PathBuf::from(s);
                // Reject any path that contains a `..` component to prevent
                // path-traversal attacks (e.g. "../../../etc/passwd").
                for component in p.components() {
                    if component == Component::ParentDir {
                        return Err(format!(
                            "profile-path must not contain '..' components: {}",
                            s
                        ));
                    }
                }
                Some(p)
            }
        };

        let create_if_missing = params
            .get("profile-create")
            .map(|v| v.eq_ignore_ascii_case("true") || v == "1")
            .unwrap_or(false);

        Ok(Self {
            path,
            create_if_missing,
        })
    }

    /// Resolve the profile directory that Chrome should use.
    ///
    /// Rules:
    /// - `path` is `None` → returns a new path under `std::env::temp_dir()`
    ///   with a unique session identifier (UUID v4).
    /// - `path` is `Some` and the directory exists → returns the path as-is.
    /// - `path` is `Some`, directory does not exist, `create_if_missing = true`
    ///   → creates it with `std::fs::create_dir_all` and returns the path.
    /// - `path` is `Some`, directory does not exist, `create_if_missing = false`
    ///   → returns `Err` with a hint to set `profile-create=true`.
    /// - `path` is `Some` but points to a file (not a directory) → returns `Err`.
    ///
    /// Note: directory creation is done here so that callers receive a concrete
    /// path they can immediately pass to `acquire_lock`.  The lock itself is
    /// not acquired here — call `acquire_lock` separately.
    pub fn validate_and_prepare(&self) -> Result<PathBuf, String> {
        match &self.path {
            None => {
                // Generate a unique temp directory path.  We do NOT create it here
                // because Chrome creates its own user-data-dir on first launch, and
                // some platforms' temp directories are cleaned between sessions.
                // The caller passes this path to ChromeSession which creates it.
                let session_id = uuid::Uuid::new_v4().to_string();
                let dir = std::env::temp_dir().join(format!("guacr-rbi-profile-{}", session_id));
                Ok(dir)
            }
            Some(p) => {
                if p.is_file() {
                    return Err(format!(
                        "profile-path exists but is a file, not a directory: {}",
                        p.display()
                    ));
                }

                if p.is_dir() {
                    return Ok(p.clone());
                }

                // Does not exist.
                if self.create_if_missing {
                    std::fs::create_dir_all(p).map_err(|e| {
                        format!("Failed to create profile directory {}: {}", p.display(), e)
                    })?;
                    Ok(p.clone())
                } else {
                    Err(format!(
                        "Profile directory does not exist: {}. \
                         Set profile-create=true to create it automatically.",
                        p.display()
                    ))
                }
            }
        }
    }
}

/// Acquire an exclusive lock on the given profile directory.
///
/// The lock is held until the returned `ProfileLockHandle` is dropped.
/// Returns `Err` if the directory is already locked by another session.
///
/// The `profile_path` here is the value returned by
/// `ProfileStorageConfig::validate_and_prepare()`, so the directory is
/// guaranteed to exist (or to be a fresh temp path that Chrome will create).
/// For the temp-path case (`ProfileStorageConfig::path == None`) we skip
/// locking entirely — temp directories are session-unique by construction.
pub(crate) fn acquire_lock(
    config: &ProfileStorageConfig,
    profile_path: &std::path::Path,
) -> Result<Option<ProfileLockHandle>, String> {
    // Temp-dir sessions (no configured path) do not need a lock: each session
    // gets a UUID-named directory that no other session will ever choose.
    if config.path.is_none() {
        return Ok(None);
    }

    let lock =
        ProfileLock::acquire(profile_path, ProfileCreationMode::MustExist).map_err(
            |e| match e {
                ProfileLockError::ProfileInUse(ref _p) => {
                    "PROFILE_IN_USE: Profile is already in use by another session. \
                 Close the existing session first."
                        .to_string()
                }
                other => format!("Failed to lock profile directory: {}", other),
            },
        )?;

    Ok(Some(lock))
}
