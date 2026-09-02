use crate::profile_isolation::{
    ProfileCreationMode, ProfileLock, ProfileLockError, PROFILE_LOCK_FILE_NAME,
};

#[test]
fn test_profile_lock_temp_dir() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("test_profile");

    let result = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist);
    assert!(matches!(
        result,
        Err(ProfileLockError::DirectoryNotFound(_))
    ));

    let lock = ProfileLock::acquire(&profile_path, ProfileCreationMode::Create).unwrap();
    assert!(profile_path.exists());
    assert!(profile_path.join(PROFILE_LOCK_FILE_NAME).exists());

    // A second concurrent acquire must fail on all platforms (fs2 advisory lock).
    let result2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist);
    assert!(matches!(result2, Err(ProfileLockError::ProfileInUse(_))));

    drop(lock);

    let _lock2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist).unwrap();
}

// ---------------------------------------------------------------------------
// ProfileLock::release() explicit release path
//
// The lock supports two release mechanisms:
// 1. drop(lock) — the Drop impl calls release_internal().
// 2. lock.release() — explicit release, consumes self.
//
// Both must allow a subsequent acquisition on the same profile.
// This test was absent from the original suite; it catches any regression
// where release() fails to unlock before the handle is dropped.
// ---------------------------------------------------------------------------

/// Explicit release() must allow immediate re-acquisition.
#[test]
fn test_explicit_release_allows_reacquire() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("explicit_release_profile");

    let lock = ProfileLock::acquire(&profile_path, ProfileCreationMode::Create).unwrap();
    assert!(profile_path.exists());

    // Explicitly release — this is the non-drop path.
    lock.release();

    // Must be able to acquire again immediately.
    let lock2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist);
    assert!(
        lock2.is_ok(),
        "re-acquisition after explicit release() should succeed"
    );
}

/// ProfileLock::path() must return the directory path used at acquisition.
#[test]
fn test_profile_lock_path_matches_acquired_directory() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("path_check_profile");

    let lock = ProfileLock::acquire(&profile_path, ProfileCreationMode::Create).unwrap();
    assert_eq!(
        lock.path(),
        profile_path.as_path(),
        "lock.path() must equal the directory passed to acquire()"
    );
}

// ---------------------------------------------------------------------------
// Concurrent lock semantics (fs2 advisory locking — all platforms)
//
// fs2::FileExt::try_lock_exclusive() uses kernel advisory locks on all
// platforms (flock on Unix, LockFileEx on Windows).  A second acquire()
// must fail while the first lock is held, regardless of OS.
// ---------------------------------------------------------------------------

/// A second concurrent acquire must fail on all platforms.
#[test]
fn test_concurrent_lock_all_platforms() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("concurrent_all_platforms");

    let lock1 = ProfileLock::acquire(&profile_path, ProfileCreationMode::Create).unwrap();

    // Extract the error without unwrap_err() — ProfileLock does not impl Debug,
    // so unwrap_err() (which requires T: Debug) would not compile.
    let err = match ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist) {
        Err(e) => e,
        Ok(_) => panic!("second acquire while lock is held must fail"),
    };
    let msg = err.to_string();
    assert!(
        msg.to_lowercase().contains("use") || msg.to_lowercase().contains("already"),
        "error message should indicate the profile is in use: {}",
        msg
    );

    drop(lock1);
}

/// Lock file persists on disk after release (fs2 does not delete it — the
/// kernel lock is what guards concurrent access, not file existence).
#[test]
fn test_lock_file_persists_after_release() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("lock_persist_test");

    let lock = ProfileLock::acquire(&profile_path, ProfileCreationMode::Create).unwrap();
    let lock_file = profile_path.join(PROFILE_LOCK_FILE_NAME);

    assert!(
        lock_file.exists(),
        "lock file must exist while lock is held"
    );

    drop(lock);

    // The lock file remains on disk; the kernel advisory lock was released.
    // A subsequent acquire must succeed (the file is re-opened and re-locked).
    assert!(
        lock_file.exists(),
        "lock file is allowed to persist after release — kernel lock guards access"
    );

    let _lock2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist)
        .expect("re-acquisition after release must succeed");
}

#[test]
fn test_profile_creation_modes() {
    let temp = tempfile::tempdir().unwrap();

    let nested_path = temp.path().join("a/b/c/profile");
    let lock = ProfileLock::acquire(&nested_path, ProfileCreationMode::CreateRecursive).unwrap();
    assert!(nested_path.exists());
    drop(lock);

    let single_path = temp.path().join("single_profile");
    let lock = ProfileLock::acquire(&single_path, ProfileCreationMode::Create).unwrap();
    assert!(single_path.exists());
    drop(lock);

    let nested_fail = temp.path().join("x/y/z");
    let result = ProfileLock::acquire(&nested_fail, ProfileCreationMode::Create);
    assert!(matches!(
        result,
        Err(ProfileLockError::DirectoryCreationFailed(_, _))
    ));
}
