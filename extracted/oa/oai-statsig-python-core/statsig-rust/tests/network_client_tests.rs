use statsig_rust::networking::{NetworkClient, NetworkError, RequestArgs};
use std::{sync::Arc, time::Duration};
use tokio::sync::Notify;
use wiremock::{Mock, MockServer, Request, ResponseTemplate, matchers::method};

async fn setup() -> (MockServer, Arc<Notify>) {
    let server = MockServer::start().await;
    let request_started = Arc::new(Notify::new());
    let started = Arc::clone(&request_started);
    Mock::given(method("POST"))
        .respond_with(move |_: &Request| {
            started.notify_one();
            ResponseTemplate::new(200).set_delay(Duration::from_secs(10))
        })
        .mount(&server)
        .await;
    (server, request_started)
}

#[tokio::test]
async fn test_killing_inflight_requests() {
    let (server, request_started) = setup().await;
    let network_client = Arc::new(NetworkClient::new("inflight_key", None, None));
    let url = format!("{}/v2/download_config_specs", server.uri());

    let network_client_clone = Arc::clone(&network_client);
    let request_url = url.clone();
    let spawned_task = tokio::task::spawn(async move {
        network_client_clone
            .post(
                RequestArgs {
                    url: request_url,
                    ..RequestArgs::new()
                },
                None,
            )
            .await
    });

    // The server must receive the request before shutdown can test cancellation.
    tokio::time::timeout(Duration::from_secs(2), request_started.notified())
        .await
        .expect("request did not reach the server");
    assert!(!spawned_task.is_finished());
    network_client.shutdown();

    let result = tokio::time::timeout(Duration::from_secs(2), spawned_task)
        .await
        .expect("shutdown did not cancel the in-flight request")
        .expect("request task panicked");
    assert_eq!(result.err(), Some(NetworkError::ShutdownError(url)));
}

#[tokio::test]
async fn test_per_request_timeout() {
    let (server, _) = setup().await;
    let network_client = NetworkClient::new("per_req_key", None, None);
    let url = format!("{}/v2/download_config_specs", server.uri());

    let result = tokio::time::timeout(
        Duration::from_secs(2),
        network_client.post(
            RequestArgs {
                url: url.clone(),
                timeout_ms: 100,
                ..RequestArgs::new()
            },
            None,
        ),
    )
    .await
    .expect("per-request timeout did not finish before the server response");
    assert!(matches!(
        result,
        Err(NetworkError::RetriesExhausted(request_url, None, 1, _)) if request_url == url
    ));
    assert_eq!(server.received_requests().await.unwrap().len(), 1);
}
