use super::*;

#[test]
fn exception_reporter_state_is_created_only_when_reporting_is_enabled() {
    for disabled in [None, Some(false), Some(true)] {
        let options = StatsigOptions {
            disable_remote_telemetry: disabled,
            ..StatsigOptions::default()
        };
        let observer = SDKErrorsObserver::new("secret-state-fixture", &options);
        // None means no network client, options snapshot, or error aggregator.
        assert_eq!(observer.state.is_none(), disabled == Some(true));
    }
}
