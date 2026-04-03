use crate::browser_client::BrowserClient;
use crate::handler::RbiConfig;
use guacr_handlers::RecordingConfig;
use std::collections::HashMap;

#[test]
fn test_browser_client_new() {
    let config = RbiConfig::default();
    let recording_config = RecordingConfig::default();
    let params = HashMap::new();
    let client = BrowserClient::new(1920, 1080, config, &recording_config, &params, None);
    assert_eq!(client.width, 1920);
    assert_eq!(client.height, 1080);
}
