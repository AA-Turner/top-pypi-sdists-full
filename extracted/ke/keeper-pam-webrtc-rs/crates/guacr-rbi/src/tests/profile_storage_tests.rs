use crate::profile_storage::{acquire_lock, ProfileStorageConfig};
use std::collections::HashMap;

// ---------------------------------------------------------------------------
// from_params tests
// ---------------------------------------------------------------------------

#[test]
fn test_no_profile_path_uses_temp_dir() {
    let params = HashMap::new();
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    assert!(config.path.is_none());
    assert!(!config.create_if_missing);

    // validate_and_prepare with no path returns something under the system
    // temp directory.
    let dir = config.validate_and_prepare().unwrap();
    let temp_root = std::env::temp_dir();
    assert!(dir.starts_with(temp_root), "expected a path under temp dir");
}

#[test]
fn test_path_traversal_rejected() {
    let mut params = HashMap::new();
    params.insert("profile-path".to_string(), "../etc/passwd".to_string());
    let result = ProfileStorageConfig::from_params(&params);
    assert!(result.is_err(), "path traversal must be rejected");
    let msg = result.unwrap_err();
    assert!(msg.contains("'..'"), "error should mention '..': {}", msg);
}

#[test]
fn test_deeply_nested_path_traversal_rejected() {
    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        "/safe/path/../../../etc/passwd".to_string(),
    );
    let result = ProfileStorageConfig::from_params(&params);
    assert!(result.is_err(), "embedded .. must be rejected");
}

#[test]
fn test_empty_path_rejected() {
    let mut params = HashMap::new();
    params.insert("profile-path".to_string(), "".to_string());
    let result = ProfileStorageConfig::from_params(&params);
    assert!(result.is_err(), "empty profile-path must be rejected");
}

#[test]
fn test_create_if_missing_true_parsed() {
    let mut params = HashMap::new();
    params.insert("profile-path".to_string(), "/tmp/test-profile".to_string());
    params.insert("profile-create".to_string(), "true".to_string());
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    assert!(config.create_if_missing);
}

#[test]
fn test_create_if_missing_default_false() {
    let mut params = HashMap::new();
    params.insert("profile-path".to_string(), "/tmp/test-profile".to_string());
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    assert!(!config.create_if_missing);
}

// ---------------------------------------------------------------------------
// validate_and_prepare tests
// ---------------------------------------------------------------------------

#[test]
fn test_existing_dir_ok() {
    let temp = tempfile::tempdir().unwrap();
    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        temp.path().to_string_lossy().to_string(),
    );
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    let result = config.validate_and_prepare();
    assert!(result.is_ok(), "existing directory should be accepted");
    assert_eq!(result.unwrap(), temp.path());
}

#[test]
fn test_missing_dir_without_create_fails() {
    let temp = tempfile::tempdir().unwrap();
    let nonexistent = temp.path().join("does_not_exist");

    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        nonexistent.to_string_lossy().to_string(),
    );
    // create_if_missing defaults to false
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    let result = config.validate_and_prepare();
    assert!(result.is_err(), "missing dir without create-flag must fail");
    let msg = result.unwrap_err();
    assert!(
        msg.contains("profile-create=true"),
        "error should suggest profile-create=true: {}",
        msg
    );
}

#[test]
fn test_missing_dir_with_create_succeeds() {
    let temp = tempfile::tempdir().unwrap();
    let new_dir = temp.path().join("new_profile_dir");
    assert!(!new_dir.exists());

    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        new_dir.to_string_lossy().to_string(),
    );
    params.insert("profile-create".to_string(), "true".to_string());

    let config = ProfileStorageConfig::from_params(&params).unwrap();
    let result = config.validate_and_prepare();
    assert!(result.is_ok(), "create=true should create the directory");
    assert!(
        new_dir.is_dir(),
        "directory should have been created on disk"
    );
}

#[test]
fn test_file_path_rejected() {
    let temp = tempfile::tempdir().unwrap();
    let file_path = temp.path().join("not_a_directory.txt");
    std::fs::write(&file_path, b"hello").unwrap();

    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        file_path.to_string_lossy().to_string(),
    );
    let config = ProfileStorageConfig::from_params(&params).unwrap();
    let result = config.validate_and_prepare();
    assert!(result.is_err(), "file path must be rejected");
    let msg = result.unwrap_err();
    assert!(
        msg.contains("is a file"),
        "error should say 'is a file': {}",
        msg
    );
}

// ---------------------------------------------------------------------------
// Lock tests
// ---------------------------------------------------------------------------

#[test]
#[cfg(target_os = "linux")]
fn test_lock_prevents_second_session() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("locked_profile");
    std::fs::create_dir(&profile_path).unwrap();

    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        profile_path.to_string_lossy().to_string(),
    );
    let config = ProfileStorageConfig::from_params(&params).unwrap();

    // First acquisition succeeds.
    let lock1 = acquire_lock(&config, &profile_path);
    assert!(lock1.is_ok(), "first lock should succeed");
    let lock1 = lock1.unwrap();
    assert!(lock1.is_some(), "persistent profile should return a lock");

    // Second acquisition on the same path must fail (profile in use).
    let lock2 = acquire_lock(&config, &profile_path);
    assert!(lock2.is_err(), "second lock should fail on Linux");
    let msg = lock2.unwrap_err();
    assert!(
        msg.contains("PROFILE_IN_USE"),
        "error should start with PROFILE_IN_USE: {}",
        msg
    );

    drop(lock1);
}

#[test]
#[cfg(target_os = "linux")]
fn test_lock_released_on_drop() {
    let temp = tempfile::tempdir().unwrap();
    let profile_path = temp.path().join("release_test");
    std::fs::create_dir(&profile_path).unwrap();

    let mut params = HashMap::new();
    params.insert(
        "profile-path".to_string(),
        profile_path.to_string_lossy().to_string(),
    );
    let config = ProfileStorageConfig::from_params(&params).unwrap();

    // Acquire and immediately drop.
    {
        let lock = acquire_lock(&config, &profile_path).unwrap();
        assert!(lock.is_some());
        // lock dropped here
    }

    // Should be able to acquire again.
    let lock2 = acquire_lock(&config, &profile_path);
    assert!(
        lock2.is_ok(),
        "re-acquisition after drop should succeed: {:?}",
        lock2.err()
    );
}

#[test]
fn test_no_lock_for_temp_dir() {
    // When no profile-path is given, acquire_lock should return None (no lock needed).
    let temp = tempfile::tempdir().unwrap();
    let config = ProfileStorageConfig::default(); // path is None

    let result = acquire_lock(&config, temp.path());
    assert!(result.is_ok());
    assert!(result.unwrap().is_none(), "temp dir sessions need no lock");
}
