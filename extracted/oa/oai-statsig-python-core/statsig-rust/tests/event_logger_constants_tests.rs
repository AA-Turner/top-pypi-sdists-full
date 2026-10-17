use statsig_rust::event_logging::event_logger_constants::EventLoggerConstants;
use std::process::Command;

const OVERRIDE_NAMES: [&str; 4] = [
    "STATSIG_TEST_OVERRIDE_TICK_INTERVAL_MS",
    "STATSIG_TEST_OVERRIDE_MIN_FLUSH_INTERVAL_MS",
    "STATSIG_TEST_OVERRIDE_MAX_FLUSH_INTERVAL_MS",
    "STATSIG_TEST_OVERRIDE_MAX_LOG_EVENT_RETRIES",
];
const EXPECTED_VALUES: &str = "STATSIG_CONSTANTS_TEST_EXPECTED_VALUES";
const DEFAULTS: [u64; 4] = [1000, 1000, 60_000, 5];

#[test]
fn event_logger_overrides_are_feature_gated() {
    for (value, testing_values) in [
        (None, DEFAULTS),
        (Some(""), DEFAULTS),
        (Some("invalid"), DEFAULTS),
        (Some("-1"), DEFAULTS),
        (Some("18446744073709551616"), DEFAULTS),
        (Some("17"), [17, 17, 17, 17]),
        (Some("0"), [0, 0, 0, 0]),
        (Some("256"), [256, 256, 256, 5]),
    ] {
        let expected = if cfg!(feature = "testing") {
            testing_values
        } else {
            DEFAULTS
        };
        let mut command = Command::new(std::env::current_exe().unwrap());
        command
            .args(["--exact", "event_logger_constants_in_child", "--nocapture"])
            .env(EXPECTED_VALUES, format!("{expected:?}"));
        for name in OVERRIDE_NAMES {
            command.env_remove(name);
            if let Some(value) = value {
                command.env(name, value);
            }
        }
        let output = command.output().unwrap();
        assert!(
            output.status.success(),
            "override {value:?}:\n{}\n{}",
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr),
        );
    }
}

#[test]
fn event_logger_constants_in_child() {
    let Ok(expected) = std::env::var(EXPECTED_VALUES) else {
        return;
    };
    let actual = [
        EventLoggerConstants::tick_interval_ms(),
        EventLoggerConstants::min_flush_interval_ms(),
        EventLoggerConstants::max_flush_interval_ms(),
        u64::from(EventLoggerConstants::max_log_event_retries()),
    ];
    assert_eq!(format!("{actual:?}"), expected);
}
