use crate::output_logger::{LogLevel, initialize_output_logger};
use std::{env, process::Command};

#[test]
fn no_malloc_trim_controls_heap_trimming() {
    const CHILD: &str = "STATSIG_TEST_HEAP_TRIM_CHILD";
    if env::var_os(CHILD).is_some() {
        initialize_output_logger(&Some(LogLevel::Debug), None);
        super::try_release_unused_heap_memory();
        return;
    }

    for (value, expected_calls) in [
        (None, 1),
        (Some("1"), 0),
        (Some("true"), 0),
        (Some("0"), 1),
        (Some("false"), 1),
        (Some(""), 1),
        (Some("TRUE"), 1),
        (Some(" true "), 1),
    ] {
        let mut cmd = Command::new(env::current_exe().unwrap());
        cmd.args([
            "--exact",
            "utils::heap_trim_tests::no_malloc_trim_controls_heap_trimming",
            "--nocapture",
        ])
        .env(CHILD, "1")
        .env_remove("LD_PRELOAD")
        .env_remove("NO_MALLOC_TRIM");
        if let Some(value) = value {
            cmd.env("NO_MALLOC_TRIM", value);
        }
        let output = cmd.output().unwrap();
        let logs = format!(
            "{}{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
        assert!(output.status.success(), "{logs}");
        // Both possible glibc return values produce a debug message after the call.
        assert_eq!(
            logs.matches("by malloc_trim.").count(),
            expected_calls,
            "{value:?}: {logs}"
        );
    }
}
