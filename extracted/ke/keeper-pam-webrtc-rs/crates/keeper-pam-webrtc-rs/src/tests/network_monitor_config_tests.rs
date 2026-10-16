// Connectivity-check endpoint selection (KEEPER_WEBRTC_DISABLE_CONNECTIVITY_CHECK and
// KEEPER_WEBRTC_CONNECTIVITY_ENDPOINTS), tested through the pure resolver so no test
// touches the process environment.

use crate::config::resolve_connectivity_endpoints;
use crate::webrtc_network_monitor::{NetworkMonitor, NetworkMonitorConfig};
use std::time::{Duration, Instant};

const DEFAULTS: [&str; 3] = ["8.8.8.8:53", "1.1.1.1:53", "208.67.222.222:53"];

#[test]
fn unset_uses_public_dns_defaults() {
    assert_eq!(resolve_connectivity_endpoints(None, None), DEFAULTS);
}

#[test]
fn disable_true_or_1_turns_checks_off() {
    for value in ["true", "TRUE", "True", "1", " true "] {
        assert!(
            resolve_connectivity_endpoints(Some(value), None).is_empty(),
            "{value:?} must disable"
        );
    }
}

#[test]
fn disable_wins_over_custom_endpoints() {
    assert!(resolve_connectivity_endpoints(Some("true"), Some("10.0.1.1:53")).is_empty());
}

#[test]
fn disable_false_still_honours_custom_endpoints() {
    assert_eq!(
        resolve_connectivity_endpoints(Some("false"), Some("10.0.1.1:53,10.0.1.2:53")),
        ["10.0.1.1:53", "10.0.1.2:53"],
        "a non-true disable value must not send traffic to public DNS instead"
    );
}

#[test]
fn custom_endpoints_are_trimmed_and_blanks_dropped() {
    assert_eq!(
        resolve_connectivity_endpoints(None, Some(" dns.internal.corp:53 , ,10.0.1.1:53,")),
        ["dns.internal.corp:53", "10.0.1.1:53"]
    );
}

#[test]
fn empty_custom_endpoints_disable_checks() {
    assert!(resolve_connectivity_endpoints(None, Some("")).is_empty());
    assert!(resolve_connectivity_endpoints(None, Some(" , ")).is_empty());
}

#[tokio::test]
async fn disabled_check_reports_connected_without_probing() {
    let monitor = NetworkMonitor::new(NetworkMonitorConfig {
        test_endpoints: vec![],
        ..NetworkMonitorConfig::default()
    });

    let started = Instant::now();
    assert!(
        monitor.check_connectivity().await,
        "with no endpoints the check is skipped, which must not read as the network being down"
    );
    assert!(started.elapsed() < Duration::from_millis(100));
}
