use oai_statsig_grpc::statsig_forward_proxy::{
    ConfigSpecRequest, ConfigSpecResponse,
    statsig_forward_proxy_server::{StatsigForwardProxy, StatsigForwardProxyServer},
};
use oai_statsig_grpc::statsig_grpc_client::StatsigGrpcClient;
use oai_statsig_grpc::statsig_grpc_err::StatsigGrpcErr;
use std::time::Duration;
use tonic::codegen::tokio_stream;
use tonic::transport::server::TcpIncoming;
use tonic::transport::{Certificate, Identity, Server, ServerTlsConfig};
use tonic::{Request, Response, Status};

const CA: &[u8] = include_bytes!("fixtures/test-ca.pem");
const CERT: &[u8] = include_bytes!("fixtures/test-identity.pem");
const KEY: &[u8] = include_bytes!("fixtures/test-identity-key.pem");

fn material() -> [Option<String>; 3] {
    ["test-ca.pem", "test-identity.pem", "test-identity-key.pem"].map(|name| {
        Some(format!(
            "{}/tests/fixtures/{name}",
            env!("CARGO_MANIFEST_DIR")
        ))
    })
}

fn client(url: &str, mode: Option<&str>, paths: [Option<String>; 3]) -> StatsigGrpcClient {
    let [ca, cert, key] = paths;
    StatsigGrpcClient::new(
        "fake-sdk-key",
        url,
        mode.map(str::to_owned),
        ca,
        cert,
        key,
        None,
    )
}

async fn assert_rejected(client: &StatsigGrpcClient, message: &str) {
    // All entry points must reject without sending the key, including after reset.
    tokio::time::timeout(Duration::from_secs(2), async {
        let connect = client.connect_client().await;
        assert!(matches!(connect, Err(StatsigGrpcErr::Authentication(ref m)) if m == message));
        let unary = client.get_specs(None).await;
        assert!(matches!(unary, Err(StatsigGrpcErr::Authentication(ref m)) if m == message));
        client.reset_client();
        let stream = client.get_specs_stream(None).await;
        assert!(matches!(stream, Err(StatsigGrpcErr::Authentication(ref m)) if m == message));
    })
    .await
    .expect("authentication validation should finish without network I/O");
}

#[tokio::test]
async fn missing_or_unreadable_required_material_fails_before_connecting() {
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let roles = ["CA certificate", "client certificate", "client key"];
    for scheme in ["http", "https"] {
        let url = format!("{scheme}://{}", listener.local_addr().unwrap());
        for (mode, required) in [("tls", 1), ("mtls", 3)] {
            for (index, role) in roles.iter().enumerate().take(required) {
                let mut paths = material();
                paths[index] = None;
                assert_rejected(
                    &client(&url, Some(mode), paths),
                    &format!("Missing {role} path"),
                )
                .await;
                // A nonexistent file and a directory both exercise read failures.
                for invalid in ["does-not-exist", ""] {
                    let mut paths = material();
                    paths[index] = Some(format!(
                        "{}/tests/fixtures/{invalid}",
                        env!("CARGO_MANIFEST_DIR")
                    ));
                    assert_rejected(
                        &client(&url, Some(mode), paths),
                        &format!("Failed to read {role}"),
                    )
                    .await;
                }
            }
        }
    }
    assert_eq!(
        listener.accept().unwrap_err().kind(),
        std::io::ErrorKind::WouldBlock
    );
}

#[tokio::test]
async fn explicit_secure_modes_reject_http_even_with_valid_material() {
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let url = format!("http://{}", listener.local_addr().unwrap());
    for mode in ["tls", "mTlS"] {
        assert_rejected(
            &client(&url, Some(mode), material()),
            "TLS authentication requires an HTTPS endpoint",
        )
        .await;
    }
    assert_eq!(
        listener.accept().unwrap_err().kind(),
        std::io::ErrorKind::WouldBlock
    );
}

struct Service;
#[tonic::async_trait]
impl StatsigForwardProxy for Service {
    async fn get_config_spec(
        &self,
        request: Request<ConfigSpecRequest>,
    ) -> Result<Response<ConfigSpecResponse>, Status> {
        assert_eq!(request.into_inner().sdk_key, "fake-sdk-key");
        Ok(Response::new(ConfigSpecResponse {
            spec: "test-specs".into(),
            last_updated: 42,
            zstd_dict_id: None,
        }))
    }
    type StreamConfigSpecStream = tokio_stream::Once<Result<ConfigSpecResponse, Status>>;
    async fn stream_config_spec(
        &self,
        request: Request<ConfigSpecRequest>,
    ) -> Result<Response<Self::StreamConfigSpecStream>, Status> {
        let response = self.get_config_spec(request).await?.into_inner();
        Ok(Response::new(tokio_stream::once(Ok(response))))
    }
}

struct TestServer(tokio::task::JoinHandle<()>);
impl Drop for TestServer {
    fn drop(&mut self) {
        self.0.abort();
    }
}

fn server(mode: Option<&str>) -> (String, TestServer) {
    let incoming = TcpIncoming::bind(([127, 0, 0, 1], 0).into()).unwrap();
    let url = format!(
        "{}://{}",
        if mode.is_some() { "https" } else { "http" },
        incoming.local_addr().unwrap()
    );
    let mut builder = Server::builder();
    if let Some(mode) = mode {
        let mut tls = ServerTlsConfig::new().identity(Identity::from_pem(CERT, KEY));
        if mode == "mtls" {
            tls = tls.client_ca_root(Certificate::from_pem(CA));
        }
        builder = builder.tls_config(tls).unwrap();
    }
    let task = tokio::spawn(async move {
        builder
            .add_service(StatsigForwardProxyServer::new(Service))
            .serve_with_incoming(incoming)
            .await
            .unwrap();
    });
    (url, TestServer(task))
}

async fn assert_specs(client: &StatsigGrpcClient) {
    tokio::time::timeout(Duration::from_secs(5), async {
        client.connect_client().await.unwrap();
        assert_eq!(client.get_specs(None).await.unwrap().spec, "test-specs");
        client.reset_client();
        let mut stream = client.get_specs_stream(Some(42)).await.unwrap();
        assert_eq!(stream.message().await.unwrap().unwrap().last_updated, 42);
    })
    .await
    .expect("loopback request should complete");
}

#[tokio::test]
async fn tls_and_required_mtls_can_fetch_and_stream_over_https() {
    for mode in ["tls", "mtls"] {
        let (url, _server) = server(Some(mode));
        if mode == "mtls" {
            let unauthenticated = client(&url, Some("tls"), material());
            assert!(
                tokio::time::timeout(Duration::from_secs(5), unauthenticated.get_specs(None))
                    .await
                    .expect("mTLS handshake should finish")
                    .is_err()
            );
        }
        assert_specs(&client(&url, Some(mode), material())).await;
    }
}

#[tokio::test]
async fn unauthenticated_http_behavior_is_unchanged() {
    let (url, _server) = server(None);
    for mode in [None, Some("none"), Some("unknown")] {
        // Unused TLS paths must not introduce I/O or rejection in legacy modes.
        assert_specs(&client(&url, mode, [Some("not-a-file".into()), None, None])).await;
    }
}
