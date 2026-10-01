use super::{NETWORK_REQUEST_LATENCY_METRIC, REQUEST_PATH_TAG};
use crate::observability::{
    observability_client_adapter::{MetricType, ObservabilityEvent},
    ops_stats::OpsStatsEvent,
};

#[tokio::test]
async fn unsupported_limited_blob_request_does_not_record_network_latency() {
    use super::NetworkClient;
    use crate::networking::{HttpMethod, NetworkError, NetworkProvider, RequestArgs, Response};
    use crate::observability::ops_stats::OpsStatsForInstance;
    use async_trait::async_trait;
    use std::sync::Arc;

    struct SendOnlyProvider;

    #[async_trait]
    impl NetworkProvider for SendOnlyProvider {
        async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
            panic!("unsupported limited requests must not fall back to send");
        }
    }

    let network_provider: Arc<dyn NetworkProvider> = Arc::new(SendOnlyProvider);
    let mut client = NetworkClient::new("secret-test", None, None);
    client.net_provider = Arc::downgrade(&network_provider);
    client.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut metrics = client.ops_stats.subscribe_for_test();

    let result = client
        .get_with_response_limit(
            RequestArgs {
                url: "https://statsigcdn.openai.com/v1/dynamic_config_value/blob-sha".to_string(),
                ..RequestArgs::new()
            },
            1024,
        )
        .await;

    assert!(matches!(
        result,
        Err(NetworkError::RequestNotRetryable(_, None, _))
    ));
    assert!(take_network_latencies(&mut metrics).is_empty());
}

pub(super) fn take_network_latencies(
    receiver: &mut tokio::sync::broadcast::Receiver<OpsStatsEvent>,
) -> Vec<ObservabilityEvent> {
    let mut latencies = Vec::new();
    while let Ok(event) = receiver.try_recv() {
        if let OpsStatsEvent::Observability(event) = event {
            if event.metric_name == NETWORK_REQUEST_LATENCY_METRIC {
                assert!(matches!(event.metric_type, MetricType::Dist));
                assert!(event.value.is_finite() && event.value >= 0.0);
                assert_eq!(
                    event.tags.as_ref().unwrap()[REQUEST_PATH_TAG],
                    "/v1/dynamic_config_value"
                );
                latencies.push(event);
            }
        }
    }
    latencies
}

#[cfg(not(feature = "custom_network_provider"))]
crate::networking::__tests__::http2_test_helpers::isolated_http2_test! {
async fn blob_request_latency_includes_complete_response_body() {
    use super::{IS_SUCCESS_TAG, NetworkClient};
    use crate::networking::{
        NetworkProvider, RequestArgs, providers::net_provider_reqwest::NetworkProviderReqwest,
    };
    use crate::observability::ops_stats::OpsStatsForInstance;
    use std::{sync::Arc, time::Duration};

    let mut server = mockito::Server::new_async().await;
    let mock = server
        .mock("GET", "/v1/dynamic_config_value/slow-body")
        .with_chunked_body(|writer| {
            writer.write_all(b"first")?;
            std::thread::sleep(Duration::from_millis(100));
            writer.write_all(b"last")
        })
        .expect(1)
        .create_async()
        .await;
    let network_provider: Arc<dyn NetworkProvider> = Arc::new(NetworkProviderReqwest::new());
    let mut client = NetworkClient::new("secret-test", None, None);
    client.net_provider = Arc::downgrade(&network_provider);
    client.ops_stats = Arc::new(OpsStatsForInstance::new());
    let mut metrics = client.ops_stats.subscribe_for_test();

    let response = client
        .get_with_response_limit(
            RequestArgs {
                url: format!("{}/v1/dynamic_config_value/slow-body", server.url()),
                timeout_ms: 5000,
                ..RequestArgs::new()
            },
            9,
        )
        .await
        .unwrap();
    let mut data = response.data.unwrap();
    assert_eq!(data.read_to_bytes().unwrap(), b"firstlast");
    mock.assert_async().await;

    let latencies = take_network_latencies(&mut metrics);
    assert_eq!(latencies.len(), 1);
    assert!(latencies[0].value >= 100.0);
    assert_eq!(latencies[0].tags.as_ref().unwrap()[IS_SUCCESS_TAG], "true");
}
}
