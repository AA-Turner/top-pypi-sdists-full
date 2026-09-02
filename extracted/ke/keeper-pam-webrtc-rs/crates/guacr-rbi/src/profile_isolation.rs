// Profile isolation for RBI sessions
//
// Provides security mechanisms to ensure RBI sessions are properly isolated:
// 1. Profile lock files - Prevent concurrent use of the same persistent profile
//
// Based on KCM's isolation implementation.

use fs2::FileExt;
use log::{debug, info};
use std::fs::{self, File, OpenOptions};
use std::io;
use std::path::{Path, PathBuf};

/// Name of the lock file placed in profile directories
pub(crate) const PROFILE_LOCK_FILE_NAME: &str = "guacr-rbi-profile.lock";

/// Profile directory creation mode
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum ProfileCreationMode {
    /// Don't create the directory - it must already exist
    #[default]
    MustExist,
    /// Create the directory if it doesn't exist (single level)
    Create,
    /// Recursively create all parent directories as needed
    CreateRecursive,
}

/// Manages an isolated browser profile directory with locking
///
/// When using persistent profile directories, this ensures only one
/// RBI session can use a given profile at a time via advisory file locks.
///
/// # Security
///
/// - Creates a lock file in the profile directory
/// - Uses `fs2::FileExt::try_lock_exclusive()` for exclusive advisory locking
/// - Works on Linux, macOS, and Windows
/// - Prevents data corruption from concurrent browser instances
/// - Lock is automatically released when this struct is dropped
#[derive(Debug)]
pub struct ProfileLock {
    /// The lock file handle (keeps the advisory lock active while held)
    lock_file: Option<File>,
    /// Path to the profile directory
    profile_path: PathBuf,
}

impl ProfileLock {
    /// Acquire an exclusive lock on a profile directory
    ///
    /// # Arguments
    ///
    /// * `profile_directory` - Path to the browser profile directory
    /// * `creation_mode` - How to handle directory creation
    ///
    /// # Returns
    ///
    /// * `Ok(ProfileLock)` - Lock acquired successfully
    /// * `Err(ProfileLockError)` - Failed to acquire lock
    ///
    /// # Security
    ///
    /// This prevents multiple RBI sessions from using the same profile
    /// directory simultaneously, which could lead to:
    /// - Cookie/session data corruption
    /// - localStorage conflicts
    /// - Cache corruption
    /// - Potential data leakage between sessions
    pub fn acquire(
        profile_directory: impl AsRef<Path>,
        creation_mode: ProfileCreationMode,
    ) -> Result<Self, ProfileLockError> {
        let profile_path = profile_directory.as_ref().to_path_buf();
        let lock_file_path = profile_path.join(PROFILE_LOCK_FILE_NAME);

        // Create directory if needed
        match creation_mode {
            ProfileCreationMode::MustExist => {
                if !profile_path.exists() {
                    return Err(ProfileLockError::DirectoryNotFound(profile_path));
                }
                if !profile_path.is_dir() {
                    return Err(ProfileLockError::NotADirectory(profile_path));
                }
            }
            ProfileCreationMode::Create => {
                if !profile_path.exists() {
                    fs::create_dir(&profile_path).map_err(|e| {
                        ProfileLockError::DirectoryCreationFailed(profile_path.clone(), e)
                    })?;
                    debug!("Created profile directory: {}", profile_path.display());
                }
            }
            ProfileCreationMode::CreateRecursive => {
                if !profile_path.exists() {
                    fs::create_dir_all(&profile_path).map_err(|e| {
                        ProfileLockError::DirectoryCreationFailed(profile_path.clone(), e)
                    })?;
                    debug!(
                        "Recursively created profile directory: {}",
                        profile_path.display()
                    );
                }
            }
        }

        // Create/open the lock file and acquire an exclusive advisory lock.
        // fs2::FileExt::try_lock_exclusive() works on Linux, macOS, and Windows.
        // On Linux it uses flock(LOCK_EX | LOCK_NB); on Windows it uses LockFileEx.
        let lock_file = {
            let file = OpenOptions::new()
                .read(true)
                .write(true)
                .create(true)
                .truncate(false)
                .open(&lock_file_path)
                .map_err(|e| ProfileLockError::LockFileCreationFailed(lock_file_path.clone(), e))?;

            match file.try_lock_exclusive() {
                Ok(()) => file,
                Err(e) if e.kind() == io::ErrorKind::WouldBlock => {
                    return Err(ProfileLockError::ProfileInUse(profile_path));
                }
                Err(e) => {
                    return Err(ProfileLockError::LockFailed(lock_file_path, e));
                }
            }
        };

        info!(
            "Acquired exclusive lock on profile: {}",
            profile_path.display()
        );

        Ok(Self {
            lock_file: Some(lock_file),
            profile_path,
        })
    }

    /// Get the profile directory path
    pub fn path(&self) -> &Path {
        &self.profile_path
    }

    /// Release the lock explicitly (also happens on drop)
    pub fn release(mut self) {
        self.release_internal();
    }

    fn release_internal(&mut self) {
        if let Some(file) = self.lock_file.take() {
            // Explicitly unlock before dropping so the OS releases the advisory lock
            // immediately (fs2 unlocks on drop too, but being explicit is clearer).
            let _ = file.unlock();
            drop(file);
            debug!("Released lock on profile: {}", self.profile_path.display());
        }
    }
}

impl Drop for ProfileLock {
    fn drop(&mut self) {
        self.release_internal();
    }
}

/// Errors that can occur during profile locking
#[derive(Debug)]
pub enum ProfileLockError {
    /// Profile directory does not exist
    DirectoryNotFound(PathBuf),
    /// Path exists but is not a directory
    NotADirectory(PathBuf),
    /// Failed to create the profile directory
    DirectoryCreationFailed(PathBuf, io::Error),
    /// Failed to create the lock file
    LockFileCreationFailed(PathBuf, io::Error),
    /// Failed to acquire lock on the file
    LockFailed(PathBuf, io::Error),
    /// Profile is already in use by another session
    ProfileInUse(PathBuf),
}

impl std::fmt::Display for ProfileLockError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProfileLockError::DirectoryNotFound(p) => {
                write!(f, "Profile directory does not exist: {}", p.display())
            }
            ProfileLockError::NotADirectory(p) => {
                write!(f, "Profile path is not a directory: {}", p.display())
            }
            ProfileLockError::DirectoryCreationFailed(p, e) => {
                write!(
                    f,
                    "Failed to create profile directory {}: {}",
                    p.display(),
                    e
                )
            }
            ProfileLockError::LockFileCreationFailed(p, e) => {
                write!(f, "Failed to create lock file {}: {}", p.display(), e)
            }
            ProfileLockError::LockFailed(p, e) => {
                write!(f, "Failed to lock {}: {}", p.display(), e)
            }
            ProfileLockError::ProfileInUse(p) => {
                write!(f, "Profile is already in use: {}", p.display())
            }
        }
    }
}

impl std::error::Error for ProfileLockError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            ProfileLockError::DirectoryCreationFailed(_, e)
            | ProfileLockError::LockFileCreationFailed(_, e)
            | ProfileLockError::LockFailed(_, e) => Some(e),
            _ => None,
        }
    }
}

// ============================================================================
// DBus Isolation (Not needed for Chrome CDP)
// ============================================================================

/// DBus isolation is not needed for Chrome CDP backend
///
/// Chrome/Chromium via CDP doesn't require DBus isolation since each
/// session runs in its own isolated profile directory.
pub struct DbusIsolation;

impl DbusIsolation {
    pub fn setup() -> Result<Self, String> {
        debug!("DBus isolation not needed for Chrome CDP");
        Ok(Self)
    }

    pub fn cleanup(&mut self) {}
}
