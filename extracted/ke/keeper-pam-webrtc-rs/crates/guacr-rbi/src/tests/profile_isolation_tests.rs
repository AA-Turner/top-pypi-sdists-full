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

    #[cfg(target_os = "linux")]
    {
        let result2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist);
        assert!(matches!(result2, Err(ProfileLockError::ProfileInUse(_))));
    }

    drop(lock);

    let _lock2 = ProfileLock::acquire(&profile_path, ProfileCreationMode::MustExist).unwrap();
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
