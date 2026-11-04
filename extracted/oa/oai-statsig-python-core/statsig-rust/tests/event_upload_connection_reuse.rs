#![cfg(not(feature = "custom_network_provider"))]

use serde_json::json;
use statsig_rust::log_event_payload::{LogEventPayload, LogEventRequest};
use statsig_rust::networking::proxy_config::ProxyConfig;
use statsig_rust::statsig_global::StatsigGlobal;
use statsig_rust::{StatsigHttpEventLoggingAdapter, StatsigOptions};
use std::net::SocketAddr;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::mpsc::{UnboundedReceiver, unbounded_channel};
use tokio::task::{JoinHandle, JoinSet};
use wiremock::matchers::method;
use wiremock::{Mock, MockServer, ResponseTemplate};

struct ConnectionRecorder {
    server: MockServer,
    address: SocketAddr,
    accepted: Arc<AtomicUsize>,
    closed: UnboundedReceiver<usize>,
    relay: JoinHandle<()>,
}

fn event_request() -> LogEventRequest {
    LogEventRequest {
        payload: LogEventPayload {
            events: json!([{ "eventName": "test" }]),
            statsig_metadata: json!({}),
        },
        event_count: 1,
        retries: 0,
    }
}

impl ConnectionRecorder {
    async fn start() -> Self {
        let server = MockServer::start().await;
        Mock::given(method("POST"))
            .respond_with(ResponseTemplate::new(200).set_body_json(json!({ "success": true })))
            .mount(&server)
            .await;

        let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
        let address = listener.local_addr().unwrap();
        let upstream_address = *server.address();
        let accepted = Arc::new(AtomicUsize::new(0));
        let relay_accepted = Arc::clone(&accepted);
        let (notify_closed, closed) = unbounded_channel();
        let relay = tokio::spawn(async move {
            let mut relays = JoinSet::new();
            loop {
                let (mut downstream, _) = listener.accept().await.unwrap();
                let connection_id = relay_accepted.fetch_add(1, Ordering::SeqCst) + 1;
                let notify_closed = notify_closed.clone();
                relays.spawn(async move {
                    let mut upstream = TcpStream::connect(upstream_address).await.unwrap();
                    let _ = tokio::io::copy_bidirectional(&mut downstream, &mut upstream).await;
                    let _ = notify_closed.send(connection_id);
                });
            }
        });

        Self {
            server,
            address,
            accepted,
            closed,
            relay,
        }
    }

    async fn upload(&self, sdk_key: &str, options: StatsigOptions, expected_connections: usize) {
        let adapter = StatsigHttpEventLoggingAdapter::new(sdk_key, Some(&options));
        adapter
            .send_events_over_http(&event_request())
            .await
            .unwrap();
        assert_eq!(
            self.accepted.load(Ordering::SeqCst),
            expected_connections,
            "{sdk_key}"
        );
    }

    async fn wait_for_close(&mut self, connection_id: usize) {
        tokio::time::timeout(Duration::from_secs(5), async {
            while self.closed.recv().await.unwrap() != connection_id {}
        })
        .await
        .expect("the old client should release its connection at reset");
    }
}

impl Drop for ConnectionRecorder {
    fn drop(&mut self) {
        self.relay.abort();
    }
}

#[tokio::test]
#[serial_test::serial(event_upload_transport)]
async fn event_upload_connection_reuse_obeys_opt_in_and_transport_policy() {
    let mut recorder = ConnectionRecorder::start().await;
    let mut expected_keys = Vec::new();

    for (index, (reuse, path, connections)) in [
        (None, "/v1/log_custom_event", 1),
        (None, "/v1/log_custom_event", 2),
        (Some(false), "/v1/log_custom_event", 3),
        (Some(false), "/v1/log_custom_event", 4),
        (Some(false), "/v1/sdk_exception", 5),
        (Some(false), "/v1/sdk_exception", 6),
        (Some(true), "/v1/log_event", 7),
        (Some(true), "/v1/log_custom_event", 7),
        (Some(true), "/arbitrary/event/upload", 7),
    ]
    .into_iter()
    .enumerate()
    {
        let key = format!("secret-direct-{index}");
        recorder
            .upload(
                &key,
                StatsigOptions {
                    log_event_url: Some(format!("http://{}{path}", recorder.address)),
                    log_event_connection_reuse: reuse,
                    disable_disk_access: Some(true),
                    ..StatsigOptions::default()
                },
                connections,
            )
            .await;
        expected_keys.push(key);
    }

    let temporary_directory = tempfile::tempdir().unwrap();
    let missing_ca = temporary_directory.path().join("missing-ca.pem");
    let first_ca = temporary_directory.path().join("first-ca.pem");
    let equivalent_ca = temporary_directory.path().join("equivalent-ca.pem");
    for path in [&first_ca, &equivalent_ca] {
        std::fs::write(path, include_bytes!("data/event_upload_test_ca.pem")).unwrap();
    }
    for (index, (reuse, auth, ca, connections)) in [
        (Some(true), "alice:one", None, 8),
        (Some(true), "alice:one", None, 8),
        (Some(true), "bob:two", None, 9),
        (Some(true), "alice:one", None, 9),
        (Some(false), "alice:one", None, 10),
        (None, "alice:one", None, 11),
        (Some(true), "alice:one", Some(&missing_ca), 12),
        (Some(true), "alice:one", Some(&missing_ca), 13),
        (Some(true), "alice:one", Some(&first_ca), 14),
        (Some(true), "alice:one", Some(&equivalent_ca), 14),
    ]
    .into_iter()
    .enumerate()
    {
        let key = format!("secret-proxy-{index}");
        recorder
            .upload(
                &key,
                StatsigOptions {
                    log_event_url: Some("http://events.test/v1/log_custom_event".to_owned()),
                    log_event_connection_reuse: reuse,
                    proxy_config: Some(ProxyConfig {
                        proxy_host: Some(recorder.address.ip().to_string()),
                        proxy_port: Some(recorder.address.port()),
                        proxy_auth: Some(auth.to_owned()),
                        proxy_protocol: Some("http".to_owned()),
                        ca_cert_path: ca.map(|path| path.to_string_lossy().into_owned()),
                    }),
                    disable_disk_access: Some(true),
                    ..StatsigOptions::default()
                },
                connections,
            )
            .await;
        expected_keys.push(key);
    }

    StatsigGlobal::reset();
    recorder.wait_for_close(7).await;
    recorder
        .upload(
            "secret-after-reset",
            StatsigOptions {
                log_event_url: Some(format!("http://{}/v1/log_custom_event", recorder.address)),
                log_event_connection_reuse: Some(true),
                disable_disk_access: Some(true),
                ..StatsigOptions::default()
            },
            15,
        )
        .await;
    expected_keys.push("secret-after-reset".to_owned());

    let requests = recorder.server.received_requests().await.unwrap();
    assert_eq!(requests.len(), expected_keys.len());
    for (request, expected_key) in requests.iter().zip(expected_keys) {
        assert_eq!(
            request.headers["statsig-api-key"].to_str().unwrap(),
            expected_key
        );
    }
    for (key, authorization) in [
        ("secret-proxy-0", "Basic YWxpY2U6b25l"),
        ("secret-proxy-2", "Basic Ym9iOnR3bw=="),
    ] {
        let request = requests
            .iter()
            .find(|request| request.headers["statsig-api-key"] == key)
            .unwrap();
        assert_eq!(request.headers["proxy-authorization"], authorization);
    }
}

#[tokio::test]
#[serial_test::serial(event_upload_transport)]
async fn event_uploads_never_reuse_a_connection_driven_by_another_runtime() {
    let recorder = ConnectionRecorder::start().await;
    let options = StatsigOptions {
        log_event_url: Some(format!("http://{}/v1/log_custom_event", recorder.address)),
        log_event_connection_reuse: Some(true),
        disable_disk_access: Some(true),
        ..StatsigOptions::default()
    };
    let first_options = options.clone();
    let (ready, first_upload) = tokio::sync::oneshot::channel();
    let (stop, wait_for_stop) = std::sync::mpsc::channel::<()>();
    let first_runtime = std::thread::spawn(move || {
        let runtime = tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap();
        let adapter =
            StatsigHttpEventLoggingAdapter::new("secret-first-runtime", Some(&first_options));
        let result = runtime
            .block_on(adapter.send_events_over_http(&event_request()))
            .map_err(|error| error.to_string());
        ready.send(result).unwrap();
        let _ = wait_for_stop.recv();
    });

    tokio::time::timeout(Duration::from_secs(5), first_upload)
        .await
        .unwrap()
        .unwrap()
        .unwrap();
    tokio::time::timeout(
        Duration::from_secs(2),
        recorder.upload("secret-second-runtime", options, 2),
    )
    .await
    .expect("the second runtime must not wait for the dormant first runtime");
    stop.send(()).unwrap();
    first_runtime.join().unwrap();
}
