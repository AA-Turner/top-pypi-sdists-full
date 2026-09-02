// Unit tests for chrome_sandbox (Linux user-namespace sandbox).
//
// All tests run without root, without spawning Chrome, and without Docker.
// They verify:
//   1. sandbox_available() returns a bool without panicking
//   2. The uid_map / gid_map format strings are correct
//   3. Chrome args contain --no-sandbox only when sandbox is unavailable

#[cfg(target_os = "linux")]
mod linux {
    use crate::chrome_sandbox::{gid_map_line, sandbox_available, uid_map_line};

    /// sandbox_available() must return a bool without panicking.
    /// We cannot assert true/false here because the result depends on
    /// kernel config (unprivileged_userns_clone) and the test runner environment.
    #[test]
    fn test_sandbox_available_returns_bool() {
        // The only contract is "does not panic".
        let _ = sandbox_available();
    }

    /// uid_map_line(1000, 65534) must produce the correct format.
    ///
    /// Format is: "<child_uid> <host_uid> 1\n"
    /// This maps child UID 1000 to the host UID 65534 with a range of 1.
    #[test]
    fn test_uid_map_format_correctness() {
        let line = uid_map_line(1000, 65534);
        assert_eq!(
            line, "1000 65534 1\n",
            "uid_map line format must be '<child> <host> 1\\n'"
        );
    }

    /// gid_map_line(1000, 65534) must produce the correct format.
    #[test]
    fn test_gid_map_format_correctness() {
        let line = gid_map_line(1000, 65534);
        assert_eq!(
            line, "1000 65534 1\n",
            "gid_map line format must be '<child> <host> 1\\n'"
        );
    }

    /// uid_map_line with the actual current uid must include that uid.
    #[test]
    fn test_uid_map_uses_provided_host_uid() {
        let host_uid = 500u32;
        let line = uid_map_line(1000, host_uid);
        assert!(
            line.contains(&host_uid.to_string()),
            "uid_map line must embed the host uid"
        );
    }
}

// Chrome arg tests are platform-independent: we test the logic that decides
// whether to add --no-sandbox by reading build_chrome_args() output.
#[cfg(target_os = "linux")]
mod chrome_args {
    use crate::chrome_sandbox::{build_chrome_launch_args, sandbox_available};

    /// When sandbox is available, --no-sandbox must not be present in the base args.
    ///
    /// This is the main security invariant: if we successfully establish a user
    /// namespace, Chrome must not be told to disable its own sandbox.
    #[test]
    fn test_no_sandbox_flag_absent_when_sandbox_available() {
        if !sandbox_available() {
            // Cannot test the positive case in this environment.
            // The absence-of-flag when sandbox IS available is what matters
            // in production; skip rather than false-fail in CI containers
            // where unprivileged_userns_clone=0.
            return;
        }
        let args = build_chrome_launch_args(true /* use_sandbox */);
        assert!(
            !args.iter().any(|a| a == "--no-sandbox"),
            "--no-sandbox must not appear when user-namespace sandbox is active"
        );
    }

    /// When sandbox is NOT requested (use_sandbox=false), --no-sandbox must be present.
    ///
    /// This covers the fallback path where the kernel does not support
    /// unprivileged user namespaces.
    #[test]
    fn test_no_sandbox_flag_present_when_sandbox_unavailable() {
        let args = build_chrome_launch_args(false /* use_sandbox */);
        assert!(
            args.iter().any(|a| a == "--no-sandbox"),
            "--no-sandbox must appear in the fallback (no sandbox) arg list"
        );
    }

    /// --disable-setuid-sandbox must accompany --no-sandbox in the fallback path.
    #[test]
    fn test_disable_setuid_sandbox_accompanies_no_sandbox() {
        let args = build_chrome_launch_args(false /* use_sandbox */);
        assert!(
            args.iter().any(|a| a == "--disable-setuid-sandbox"),
            "--disable-setuid-sandbox must accompany --no-sandbox"
        );
    }
}
