// RBI network isolation check (T-007, T-008)
//
// Verifies that the RBI process is running inside a network-isolated
// environment before any browser process is launched.
//
// On Linux the check reads /proc filesystem namespace symlinks:
//   - /proc/1/ns/net  — init process (PID 1), always in the host network namespace
//   - /proc/self/ns/net — current process namespace
// If they differ the current process is in an isolated network namespace.
//
// On non-Linux platforms the check falls back to an environment variable:
//   GUACR_NETWORK_ISOLATED=1   → isolation confirmed
//   (absent or 0)               → isolation not detected
//
// This design makes the check testable on macOS developer machines while
// enforcing the requirement in production Linux containers.
//
// AC-4 and AC-5 are covered by the deployment documentation in
// crates/guacr-rbi/docs/DEPLOYMENT_SECURITY.md.

use log::info;

/// Check whether the RBI process is running in a network-isolated environment.
///
/// Returns `Ok(())` if isolation is confirmed.
/// Returns `Err(String)` with a descriptive message if isolation cannot be verified.
pub fn check_network_isolation() -> Result<(), String> {
    #[cfg(target_os = "linux")]
    {
        check_linux_network_namespace()
    }
    #[cfg(not(target_os = "linux"))]
    {
        check_env_fallback()
    }
}

/// Linux: compare /proc/1/ns/net with /proc/self/ns/net.
///
/// If they resolve to different inode paths, the current process is in a
/// network namespace distinct from the host (AC-3).
#[cfg(target_os = "linux")]
fn check_linux_network_namespace() -> Result<(), String> {
    use std::fs;

    // Allow override for integration tests in CI that run without real namespacing.
    if std::env::var("GUACR_SKIP_NETWORK_ISOLATION_CHECK").as_deref() == Ok("1") {
        info!("RBI: Network isolation check skipped (GUACR_SKIP_NETWORK_ISOLATION_CHECK=1)");
        return Ok(());
    }

    // Check env var override first (useful in container environments where
    // /proc/1/ns/net is the same inode but network policy is enforced externally).
    if std::env::var("GUACR_NETWORK_ISOLATED").as_deref() == Ok("1") {
        info!("RBI: Network isolation confirmed via GUACR_NETWORK_ISOLATED=1");
        return Ok(());
    }

    let host_ns = fs::read_link("/proc/1/ns/net")
        .map_err(|e| format!("RBI: Cannot read host network namespace (/proc/1/ns/net): {e}"))?;

    let self_ns = fs::read_link("/proc/self/ns/net")
        .map_err(|e| format!("RBI: Cannot read own network namespace (/proc/self/ns/net): {e}"))?;

    if host_ns == self_ns {
        let msg = format!(
            "RBI: Network namespace isolation not detected. \
             The RBI process is in the host network namespace ({host_ns:?}). \
             Deploy inside a network-namespaced container with egress restrictions. \
             Set GUACR_SKIP_NETWORK_ISOLATION_CHECK=1 to bypass in dev/test environments. \
             See crates/guacr-rbi/docs/DEPLOYMENT_SECURITY.md for requirements."
        );
        log::warn!("{msg}");
        return Err(msg);
    }

    info!("RBI: Network namespace isolation confirmed (self={self_ns:?}, host={host_ns:?})");
    Ok(())
}

/// Non-Linux: check GUACR_NETWORK_ISOLATED environment variable.
#[cfg(not(target_os = "linux"))]
fn check_env_fallback() -> Result<(), String> {
    if std::env::var("GUACR_SKIP_NETWORK_ISOLATION_CHECK").as_deref() == Ok("1") {
        info!("RBI: Network isolation check skipped (GUACR_SKIP_NETWORK_ISOLATION_CHECK=1)");
        return Ok(());
    }

    if std::env::var("GUACR_NETWORK_ISOLATED").as_deref() == Ok("1") {
        info!("RBI: Network isolation confirmed via GUACR_NETWORK_ISOLATED=1");
        return Ok(());
    }

    Err("RBI: Network namespace isolation not detected. \
         Set GUACR_NETWORK_ISOLATED=1 when the container provides network isolation, \
         or set GUACR_SKIP_NETWORK_ISOLATION_CHECK=1 for development. \
         See crates/guacr-rbi/docs/DEPLOYMENT_SECURITY.md for production requirements."
        .to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    // std::env::set_var / remove_var are not thread-safe. Serialize all tests
    // in this module that touch env vars through a single mutex.
    static ENV_MUTEX: std::sync::Mutex<()> = std::sync::Mutex::new(());

    #[test]
    fn test_isolation_skip_override() {
        let _guard = ENV_MUTEX.lock().unwrap();
        std::env::set_var("GUACR_SKIP_NETWORK_ISOLATION_CHECK", "1");
        let result = check_network_isolation();
        std::env::remove_var("GUACR_SKIP_NETWORK_ISOLATION_CHECK");
        assert!(result.is_ok(), "skip override must succeed: {result:?}");
    }

    #[test]
    fn test_isolation_env_confirmed() {
        let _guard = ENV_MUTEX.lock().unwrap();
        std::env::remove_var("GUACR_SKIP_NETWORK_ISOLATION_CHECK");
        std::env::set_var("GUACR_NETWORK_ISOLATED", "1");
        let result = check_network_isolation();
        std::env::remove_var("GUACR_NETWORK_ISOLATED");
        assert!(result.is_ok(), "env confirmed must succeed: {result:?}");
    }
}
