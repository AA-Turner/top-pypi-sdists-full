use smoldot_light::{
    platform::DefaultPlatform, AddChainConfig, AddChainConfigJsonRpc, Client,
};

use std::fs;
use std::num::NonZeroU32;
use std::path::Path;
use std::sync::Arc;
use std::time::Duration;

use futures_lite::future;
use futures_timer::Delay;

#[test]
#[ignore = "requires network access to the Polkadot live network"]
fn polkadot_chain_spec_responds_to_system_name() {
    let chain_spec_path = Path::new(env!("CARGO_MANIFEST_DIR")).join("chains/polkadot.json");
    let chain_spec = fs::read_to_string(&chain_spec_path)
        .expect("expected chains/polkadot.json from examples/extract_chainspec.py");

    let platform = DefaultPlatform::new("py-smoldot-light".to_string(), "0.1.0".to_string());
    let mut client: Client<Arc<DefaultPlatform>, ()> = Client::new(platform);

    let cfg = AddChainConfig {
        user_data: (),
        specification: &chain_spec,
        database_content: "",
        potential_relay_chains: std::iter::empty(),
        json_rpc: AddChainConfigJsonRpc::Enabled {
            max_pending_requests: NonZeroU32::new(128).unwrap(),
            max_subscriptions: 1024,
        },
    };

    let success = client.add_chain(cfg).expect("add_chain failed");
    let mut responses = success
        .json_rpc_responses
        .expect("json rpc disabled unexpectedly");

    client
        .json_rpc_request(
            r#"{"id":1,"jsonrpc":"2.0","method":"system_name","params":[]}"#.to_string(),
            success.chain_id,
        )
        .expect("json_rpc_request failed");

    let response = future::block_on(async {
        future::or(
            responses.next(),
            async {
                Delay::new(Duration::from_secs(10)).await;
                None
            },
        )
        .await
    })
    .expect("no response received within timeout");

    let value: serde_json::Value =
        serde_json::from_str(&response).expect("invalid json-rpc response");
    assert_eq!(value.get("id").and_then(|v| v.as_i64()), Some(1));
    assert!(
        value.get("result").is_some(),
        "expected JSON-RPC result in response: {response}"
    );
    
}
