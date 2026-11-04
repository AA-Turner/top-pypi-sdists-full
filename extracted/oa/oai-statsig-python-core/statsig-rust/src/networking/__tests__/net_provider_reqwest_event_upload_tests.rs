use super::EventUploadTransport;
use crate::StatsigOptions;
use crate::networking::__tests__::http2_test_helpers::isolated_http2_test;
use crate::networking::http_types::NetworkRequest;
use crate::networking::{HttpMethod, NetworkClient, RequestArgs};
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{TcpListener, TcpStream};
use tokio::task::JoinSet;
use wiremock::matchers::method;
use wiremock::{Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn event_upload_does_not_probe_file_access_when_disk_is_disabled() {
    let server = MockServer::start().await;
    Mock::given(method("POST"))
        .respond_with(ResponseTemplate::new(200).set_body_string("{}"))
        .mount(&server)
        .await;

    let transport = EventUploadTransport::new();
    let response = transport
        .send(NetworkRequest::new(
            &HttpMethod::POST,
            &RequestArgs {
                url: server.uri(),
                log_event_connection_reuse: true,
                disable_file_streaming: Some(true),
                ..RequestArgs::new()
            },
        ))
        .await
        .into_parts()
        .0;

    assert_eq!(response.status_code, Some(200));
    assert!(transport.transport.has_file_write_access.get().is_none());
}

isolated_http2_test! {
async fn event_upload_http2_obeys_connection_reuse_policy() {
    let server = MockServer::start().await;
    Mock::given(method("POST"))
        .respond_with(ResponseTemplate::new(200).set_body_string("{}"))
        .expect(5)
        .mount(&server)
        .await;

    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let url = format!(
        "http://{}/v1/log_custom_event",
        listener.local_addr().unwrap()
    );
    let upstream = *server.address();
    let accepted = Arc::new(AtomicUsize::new(0));
    let count = accepted.clone();
    let relay = tokio::spawn(async move {
        let mut connections = JoinSet::new();
        loop {
            let (mut downstream, _) = listener.accept().await.unwrap();
            count.fetch_add(1, Ordering::SeqCst);
            connections.spawn(async move {
                let mut preface = [0; 24];
                downstream.read_exact(&mut preface).await.unwrap();
                assert_eq!(&preface, b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n");
                let mut upstream = TcpStream::connect(upstream).await.unwrap();
                upstream.write_all(&preface).await.unwrap();
                let _ = tokio::io::copy_bidirectional(&mut downstream, &mut upstream).await;
            });
        }
    });

    // Each transport makes one discovery connection before its first payload connection.
    for (reuse, expected_connections) in [(true, 2), (true, 2), (false, 4), (false, 5), (true, 5)] {
        let options = StatsigOptions {
            prefer_http2: Some(true),
            log_event_connection_reuse: Some(reuse),
            disable_disk_access: Some(true),
            ..Default::default()
        };
        let client = NetworkClient::new_for_event_upload("secret-test", None, Some(&options));
        let response = client
            .post(
                RequestArgs {
                    url: url.clone(),
                    ..RequestArgs::new()
                },
                None,
            )
            .await
            .unwrap();
        assert_eq!(response.status_code, Some(200));
        assert_eq!(accepted.load(Ordering::SeqCst), expected_connections, "reuse={reuse}");
    }
    server.verify().await;
    relay.abort();
    assert!(relay.await.unwrap_err().is_cancelled());
}
}
