use super::NetworkClient;
use crate::networking::{NetworkError, RequestArgs};
use crate::observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance};
use serde_json::{Value, json};
use std::sync::Arc;

#[test]
fn published_network_error_masks_keys_and_preserves_diagnostic_json() {
    let mut client = NetworkClient::new("secret-FAKECLIENTONLY", None, None);
    client.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut events = client.ops_stats.subscribe_for_test();

    for (key, masked) in [
        ("secret-FAKE123456789ONLY", "secret-FAKE1*****"),
        // Deliberately malformed fake tokens must not panic while logging an error.
        ("secret-FAKEéééé", "secret-FAKEé*****"),
        ("secret-é", "secret-é*****"),
    ] {
        let args = RequestArgs {
            url: format!("https://example.invalid/v2/download_config_specs/{key}.json"),
            ..RequestArgs::new()
        };
        let error = NetworkError::RetriesExhausted(
            args.url.clone(),
            Some(503),
            3,
            format!("failed \"{key}\"; café; retry={key}"),
        );

        client.log_warning(&error, &args);

        let OpsStatsEvent::SDKError(event) = events.try_recv().expect("network error event") else {
            panic!("expected SDKError event");
        };
        assert_eq!(
            serde_json::from_str::<Value>(&event.info).unwrap(),
            json!({"RetriesExhausted": [
                format!("https://example.invalid/v2/download_config_specs/{masked}.json"),
                503,
                3,
                format!("failed \"{masked}\"; café; retry={masked}")
            ]})
        );
    }
}
