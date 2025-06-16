#[expect(unused_imports, reason = "This is a test file.")]
use crate::commands::self_info::compare_versions;
#[expect(unused_imports, reason = "This is a test file.")]
use crate::tests::shared::TestResult;

#[test]
/// special test which makes sure uvenv uses a custom home directory
/// to prevent breaking normal installed uvenv packages on host system.
fn test_is_latest() -> TestResult {
    assert!(compare_versions("1.2.3", "1.2.3"));
    assert!(compare_versions("1.3.3", "1.2.3"));
    assert!(compare_versions("1.2.10", "1.2.3"));
    assert!(!compare_versions("1.2.3", "1.3.3"));
    assert!(!compare_versions("1.3.3", "1.3.13"));

    Ok(())
}
