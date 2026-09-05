use chrono::Utc;

use super::network_error::NetworkError;
use super::providers::get_network_provider;
use super::{
    HttpMethod, NetworkProvider, RequestArgs, Response, get_source_service_and_request_path,
    should_log_network_request_latency,
};
use crate::networking::proxy_config::ProxyConfig;
use crate::observability::ErrorBoundaryEvent;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::sdk_diagnostics::marker::{ActionType, Marker, StepType};
use crate::utils::get_loggable_sdk_key;
use crate::{StatsigOptions, log_d, log_i, log_w};
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Weak};
use std::time::{Duration, Instant};

const NON_RETRY_CODES: [u16; 6] = [
    400, // Bad Request
    403, // Forbidden
    413, // Payload Too Large
    405, // Method Not Allowed
    429, // Too Many Requests
    501, // Not Implemented
];
const SHUTDOWN_ERROR: &str = "Request was aborted because the client is shutting down";

const NETWORK_REQUEST_LATENCY_METRIC: &str = "network_request.latency";
const REQUEST_PATH_TAG: &str = "request_path";
const STATUS_CODE_TAG: &str = "status_code";
const IS_SUCCESS_TAG: &str = "is_success";
const SDK_KEY_TAG: &str = "sdk_key";
const SOURCE_SERVICE_TAG: &str = "source_service";
const ID_LIST_FILE_ID_TAG: &str = "id_list_file_id";
const DELTAS_USED_TAG: &str = "deltas_used";

const TAG: &str = stringify!(NetworkClient);

pub struct NetworkClient {
    headers: HashMap<String, String>,
    is_shutdown: Arc<AtomicBool>,
    ops_stats: Arc<OpsStatsForInstance>,
    net_provider: Weak<dyn NetworkProvider>,
    disable_network: bool,
    proxy_config: Option<ProxyConfig>,
    ca_cert_pem: Option<Vec<u8>>,
    silent_on_network_failure: bool,
    disable_file_streaming: bool,
    log_event_connection_reuse: bool,
    loggable_sdk_key: String,
}

impl NetworkClient {
    #[must_use]
    pub fn new(
        sdk_key: &str,
        headers: Option<HashMap<String, String>>,
        options: Option<&StatsigOptions>,
    ) -> Self {
        let net_provider = get_network_provider();
        let (disable_network, proxy_config, ca_cert_pem, log_event_connection_reuse) = options
            .map(|opts| {
                let ca_cert_pem = opts
                    .proxy_config
                    .as_ref()
                    .and_then(|cfg| cfg.ca_cert_path.as_ref())
                    .and_then(|path| {
                        if path.is_empty() {
                            return None;
                        }
                        match std::fs::read(path) {
                            Ok(bytes) => Some(bytes),
                            Err(e) => {
                                log_w!(
                                    TAG,
                                    "Failed to read proxy_config.ca_cert_path '{}': {}",
                                    path,
                                    e
                                );
                                None
                            }
                        }
                    });
                (
                    opts.disable_network.unwrap_or(false),
                    opts.proxy_config.clone(),
                    ca_cert_pem,
                    opts.log_event_connection_reuse.unwrap_or(true),
                )
            })
            .unwrap_or((false, None, None, true));

        let sdk_instance_id = options
            .map(|opts| opts.get_sdk_instance_id(sdk_key))
            .unwrap_or(sdk_key);

        NetworkClient {
            headers: headers.unwrap_or_default(),
            is_shutdown: Arc::new(AtomicBool::new(false)),
            net_provider,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            disable_network,
            proxy_config,
            ca_cert_pem,
            silent_on_network_failure: false,
            disable_file_streaming: options
                .map(|opts| opts.disable_disk_access.unwrap_or(false))
                .unwrap_or(false),
            log_event_connection_reuse,
            loggable_sdk_key: get_loggable_sdk_key(sdk_key),
        }
    }

    pub fn shutdown(&self) {
        self.is_shutdown.store(true, Ordering::SeqCst);
    }

    pub async fn get(&self, request_args: RequestArgs) -> Result<Response, NetworkError> {
        self.make_request(HttpMethod::GET, request_args, None).await
    }

    pub(crate) async fn get_with_response_limit(
        &self,
        request_args: RequestArgs,
        max_response_bytes: u64,
    ) -> Result<Response, NetworkError> {
        self.make_request(HttpMethod::GET, request_args, Some(max_response_bytes))
            .await
    }

    pub async fn post(
        &self,
        mut request_args: RequestArgs,
        body: Option<Vec<u8>>,
    ) -> Result<Response, NetworkError> {
        request_args.body = body;
        self.make_request(HttpMethod::POST, request_args, None)
            .await
    }

    async fn make_request(
        &self,
        method: HttpMethod,
        mut request_args: RequestArgs,
        max_response_bytes: Option<u64>,
    ) -> Result<Response, NetworkError> {
        let is_shutdown = if let Some(is_shutdown) = &request_args.is_shutdown {
            is_shutdown.clone()
        } else {
            self.is_shutdown.clone()
        };

        if self.disable_network {
            log_d!(TAG, "Network is disabled, not making requests");
            return Err(NetworkError::DisableNetworkOn(request_args.url));
        }

        request_args.populate_headers(self.headers.clone());

        if request_args.disable_file_streaming.is_none() {
            request_args.disable_file_streaming = Some(self.disable_file_streaming);
        }

        if request_args.ca_cert_pem.is_none() {
            request_args.ca_cert_pem = self.ca_cert_pem.clone();
        }

        if self.log_event_connection_reuse && !request_args.log_event_connection_reuse {
            request_args.log_event_connection_reuse = true;
        }

        let mut merged_headers = request_args.headers.unwrap_or_default();
        if !self.headers.is_empty() {
            merged_headers.extend(self.headers.clone());
        }
        merged_headers.insert(
            "STATSIG-CLIENT-TIME".into(),
            Utc::now().timestamp_millis().to_string(),
        );
        request_args.headers = Some(merged_headers);

        // passing down proxy config through request args
        if let Some(proxy_config) = &self.proxy_config {
            request_args.proxy_config = Some(proxy_config.clone());
        }
        let mut attempt = 0;

        loop {
            if let Some(key) = request_args.diagnostics_key {
                self.ops_stats.add_marker(
                    Marker::new(key, ActionType::Start, Some(StepType::NetworkRequest))
                        .with_attempt(attempt)
                        .with_url(request_args.url.clone()),
                    None,
                );
            }
            if is_shutdown.load(Ordering::SeqCst) {
                log_i!(TAG, "{}", SHUTDOWN_ERROR);
                return Err(NetworkError::ShutdownError(request_args.url));
            }

            let request_start = Instant::now();
            let (mut response, response_size_limit_exceeded, response_limit_unsupported) =
                match self.net_provider.upgrade() {
                    Some(net_provider) => match max_response_bytes {
                        Some(max_response_bytes) => net_provider
                            .send_with_response_limit(&method, &request_args, max_response_bytes)
                            .await
                            .into_parts(),
                        None => (
                            net_provider.send(&method, &request_args).await,
                            false,
                            false,
                        ),
                    },
                    None => {
                        return Err(NetworkError::RequestFailed(
                            request_args.url,
                            None,
                            "Failed to get a NetworkProvider instance".to_string(),
                        ));
                    }
                };

            let status = response.status_code;
            let error_message = response
                .error
                .clone()
                .unwrap_or_else(|| get_error_message_for_status(status, response.data.as_mut()));

            let content_type = response
                .data
                .as_ref()
                .and_then(|data| data.get_header_ref("content-type"));

            log_d!(
                TAG,
                "Response url({}) status({:?}) content-type({:?})",
                &request_args.url,
                response.status_code,
                content_type
            );

            let sdk_region_str = response
                .data
                .as_ref()
                .and_then(|data| data.get_header_ref("x-statsig-region").cloned());
            // Keep existing unlimited request semantics unchanged. Limited blob
            // requests need body-read failures to enter retry handling instead
            // of accepting an empty successful response.
            let success = !response_size_limit_exceeded
                && !response_limit_unsupported
                && (200..300).contains(&status.unwrap_or(0))
                && (max_response_bytes.is_none() || response.error.is_none());
            let duration_ms = request_start.elapsed().as_millis() as f64;
            self.log_network_request_latency_to_ob(&request_args, status, success, duration_ms);

            if let Some(key) = request_args.diagnostics_key {
                let mut end_marker =
                    Marker::new(key, ActionType::End, Some(StepType::NetworkRequest))
                        .with_attempt(attempt)
                        .with_url(request_args.url.clone())
                        .with_is_success(success)
                        .with_content_type(content_type.cloned())
                        .with_sdk_region(sdk_region_str.map(|s| s.to_owned()));

                if let Some(status_code) = status {
                    end_marker = end_marker.with_status_code(status_code);
                }

                let error_map = if !error_message.is_empty() {
                    let mut map = HashMap::new();
                    map.insert("name".to_string(), "NetworkError".to_string());
                    map.insert("message".to_string(), error_message.clone());
                    let status_string = match status {
                        Some(code) => code.to_string(),
                        None => "None".to_string(),
                    };
                    map.insert("code".to_string(), status_string);
                    Some(map)
                } else {
                    None
                };

                if let Some(error_map) = error_map {
                    end_marker = end_marker.with_error(error_map);
                }

                self.ops_stats.add_marker(end_marker, None);
            }

            if success {
                return Ok(response);
            }

            // A non-2xx response can have an error body larger than the expected blob.
            // Keep the body bound, but preserve status-based retry behavior for those responses.
            let limited_response_failure_is_terminal = response_limit_unsupported
                || (response_size_limit_exceeded
                    && status.is_none_or(|status| (200..300).contains(&status)));

            if limited_response_failure_is_terminal {
                let error = NetworkError::RequestNotRetryable(
                    request_args.url.clone(),
                    status,
                    error_message,
                );
                self.log_warning(&error, &request_args);
                return Err(error);
            }

            if NON_RETRY_CODES.contains(&status.unwrap_or(0)) {
                let error = NetworkError::RequestNotRetryable(
                    request_args.url.clone(),
                    status,
                    error_message,
                );
                self.log_warning(&error, &request_args);
                return Err(error);
            }

            if attempt >= request_args.retries {
                let error = NetworkError::RetriesExhausted(
                    request_args.url.clone(),
                    status,
                    attempt + 1,
                    error_message,
                );
                self.log_warning(&error, &request_args);
                return Err(error);
            }

            attempt += 1;
            let backoff_ms = 2_u64.pow(attempt) * 100;

            log_i!(
                TAG,
                "Network request failed with status code {} (attempt {}/{}), will retry after {}ms...\n{}",
                status.map_or("unknown".to_string(), |s| s.to_string()),
                attempt,
                request_args.retries + 1,
                backoff_ms,
                error_message
            );

            tokio::time::sleep(Duration::from_millis(backoff_ms)).await;
        }
    }

    pub fn mute_network_error_log(mut self) -> Self {
        self.silent_on_network_failure = true;
        self
    }

    // Logging helpers
    fn log_warning(&self, error: &NetworkError, args: &RequestArgs) {
        let exception = error.name();

        log_w!(TAG, "{}", error);
        if !self.silent_on_network_failure {
            let dedupe_key = format!("{:?}", args.diagnostics_key);
            self.ops_stats.log_error(ErrorBoundaryEvent {
                tag: TAG.to_string(),
                exception: exception.to_string(),
                bypass_dedupe: false,
                info: serde_json::to_string(error).unwrap_or_default(),
                dedupe_key: Some(dedupe_key),
                extra: Some(get_network_error_extra_tags(error, args)),
            });
        }
    }

    // ------------------------------------------------------------
    // Observability Logging Helpers (OB only) - START
    // ------------------------------------------------------------
    fn log_network_request_latency_to_ob(
        &self,
        request_args: &RequestArgs,
        status: Option<u16>,
        success: bool,
        duration_ms: f64,
    ) {
        let url = request_args.url.as_str();
        if !should_log_network_request_latency(url) {
            return;
        }

        let status_code = status
            .map(|code| code.to_string())
            .unwrap_or("none".to_string());
        let tags = get_network_request_latency_tags(
            request_args,
            status_code,
            success,
            self.loggable_sdk_key.clone(),
        );

        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            NETWORK_REQUEST_LATENCY_METRIC.to_string(),
            duration_ms,
            Some(tags),
        ));
    }
}

fn get_network_error_extra_tags(
    error: &NetworkError,
    request_args: &RequestArgs,
) -> HashMap<String, String> {
    let (_, request_path) = get_source_service_and_request_path(&request_args.url);
    HashMap::from([
        (REQUEST_PATH_TAG.to_string(), request_path),
        (
            STATUS_CODE_TAG.to_string(),
            error
                .status_code()
                .map(|code| code.to_string())
                .unwrap_or("none".to_string()),
        ),
    ])
}

fn get_network_request_latency_tags(
    request_args: &RequestArgs,
    status_code: String,
    success: bool,
    loggable_sdk_key: String,
) -> HashMap<String, String> {
    let (source_service, request_path) = get_source_service_and_request_path(&request_args.url);
    let mut tags = HashMap::from([
        (REQUEST_PATH_TAG.to_string(), request_path),
        (STATUS_CODE_TAG.to_string(), status_code),
        (IS_SUCCESS_TAG.to_string(), success.to_string()),
        (SDK_KEY_TAG.to_string(), loggable_sdk_key),
        (SOURCE_SERVICE_TAG.to_string(), source_service),
        (
            DELTAS_USED_TAG.to_string(),
            request_args.deltas_enabled.to_string(),
        ),
    ]);
    if let Some(id_list_file_id) = request_args
        .id_list_file_id
        .as_ref()
        .filter(|id| !id.is_empty())
    {
        tags.insert(ID_LIST_FILE_ID_TAG.to_string(), id_list_file_id.clone());
    }

    tags
}

#[cfg(test)]
fn get_request_path(url: &str) -> String {
    crate::networking::get_source_service_and_request_path(url).1
}

// ------------------------------------------------------------
// Observability Logging Helpers (OB only) - END
// ------------------------------------------------------------

fn get_error_message_for_status(
    status: Option<u16>,
    data: Option<&mut super::ResponseData>,
) -> String {
    if (200..300).contains(&status.unwrap_or(0)) {
        return String::new();
    }

    let mut message = String::new();
    if let Some(data) = data {
        let lossy_str = data.read_to_string().unwrap_or_default();
        if lossy_str.is_ascii() {
            message = lossy_str.to_string();
        }
    }

    let status_value = match status {
        Some(code) => code,
        None => return format!("HTTP Error None: {message}"),
    };

    let generic_message = match status_value {
        400 => "Bad Request",
        401 => "Unauthorized",
        403 => "Forbidden",
        404 => "Not Found",
        405 => "Method Not Allowed",
        406 => "Not Acceptable",
        408 => "Request Timeout",
        500 => "Internal Server Error",
        502 => "Bad Gateway",
        503 => "Service Unavailable",
        504 => "Gateway Timeout",
        0 => "Unknown Error",
        _ => return format!("HTTP Error {status_value}: {message}"),
    };

    if message.is_empty() {
        return generic_message.to_string();
    }

    format!("{generic_message}: {message}")
}

#[cfg(test)]
mod tests {
    use super::{
        DELTAS_USED_TAG, ID_LIST_FILE_ID_TAG, NetworkClient, REQUEST_PATH_TAG, STATUS_CODE_TAG,
        get_network_error_extra_tags, get_network_request_latency_tags, get_request_path,
    };
    use crate::StatsigOptions;
    use crate::networking::{
        HttpMethod, NetworkError, NetworkProvider, RequestArgs, Response, ResponseData,
        ResponseLimitOutcome, get_source_service_and_request_path,
        should_log_network_request_latency,
    };
    use async_trait::async_trait;
    use std::sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
    };

    struct RetryableBodyReadFailureProvider {
        attempts: AtomicUsize,
    }

    struct UnsupportedSuccessProvider {
        limited_calls: AtomicUsize,
    }

    #[async_trait]
    impl NetworkProvider for UnsupportedSuccessProvider {
        async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
            panic!("unsupported limited requests must not fall back to send")
        }

        async fn send_with_response_limit(
            &self,
            _method: &HttpMethod,
            _args: &RequestArgs,
            _max_response_bytes: u64,
        ) -> ResponseLimitOutcome {
            self.limited_calls.fetch_add(1, Ordering::SeqCst);
            ResponseLimitOutcome::Unsupported(Response {
                status_code: Some(200),
                data: Some(ResponseData::from_bytes(b"looks-successful".to_vec())),
                error: None,
            })
        }
    }

    impl RetryableBodyReadFailureProvider {
        fn next_response(&self) -> Response {
            if self.attempts.fetch_add(1, Ordering::SeqCst) == 0 {
                return Response {
                    status_code: Some(200),
                    data: None,
                    error: Some("body read interrupted".to_string()),
                };
            }

            Response {
                status_code: Some(200),
                data: Some(ResponseData::from_bytes(b"ok".to_vec())),
                error: None,
            }
        }
    }

    #[async_trait]
    impl NetworkProvider for RetryableBodyReadFailureProvider {
        async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
            self.next_response()
        }

        async fn send_with_response_limit(
            &self,
            _method: &HttpMethod,
            _args: &RequestArgs,
            _max_response_bytes: u64,
        ) -> ResponseLimitOutcome {
            ResponseLimitOutcome::Response(self.next_response())
        }
    }

    #[tokio::test]
    async fn retries_success_status_response_with_body_read_error() {
        let provider = Arc::new(RetryableBodyReadFailureProvider {
            attempts: AtomicUsize::new(0),
        });
        let network_provider: Arc<dyn NetworkProvider> = provider.clone();
        let mut client = NetworkClient::new("secret-test", None, None);
        client.net_provider = Arc::downgrade(&network_provider);

        let response = client
            .get_with_response_limit(
                RequestArgs {
                    url: "https://example.com/remote-value".to_string(),
                    retries: 1,
                    ..RequestArgs::new()
                },
                1024,
            )
            .await
            .unwrap();

        assert!(response.data.is_some());
        assert_eq!(provider.attempts.load(Ordering::SeqCst), 2);
    }

    #[tokio::test]
    async fn unsupported_response_limit_outcome_is_terminal_even_with_status_200() {
        let provider = Arc::new(UnsupportedSuccessProvider {
            limited_calls: AtomicUsize::new(0),
        });
        let network_provider: Arc<dyn NetworkProvider> = provider.clone();
        let mut client = NetworkClient::new("secret-test", None, None);
        client.net_provider = Arc::downgrade(&network_provider);

        let result = client
            .get_with_response_limit(
                RequestArgs {
                    url: "https://example.com/remote-value".to_string(),
                    retries: 2,
                    ..RequestArgs::new()
                },
                1024,
            )
            .await;

        assert!(matches!(
            result,
            Err(NetworkError::RequestNotRetryable(_, Some(200), _))
        ));
        assert_eq!(provider.limited_calls.load(Ordering::SeqCst), 1);
    }

    #[cfg(not(feature = "custom_network_provider"))]
    #[tokio::test]
    async fn response_limited_blob_urls_retry_oversized_errors() {
        use crate::networking::providers::net_provider_reqwest::NetworkProviderReqwest;
        use wiremock::matchers::{method, path};
        use wiremock::{Mock, MockServer, ResponseTemplate};

        let server = MockServer::start().await;
        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/retry"))
            .respond_with(ResponseTemplate::new(500).set_body_bytes(b"temporary upstream failure"))
            .up_to_n_times(1)
            .with_priority(1)
            .expect(1)
            .mount(&server)
            .await;
        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/retry"))
            .respond_with(ResponseTemplate::new(200).set_body_bytes(b"retry"))
            .with_priority(2)
            .expect(1)
            .mount(&server)
            .await;
        let network_provider: Arc<dyn NetworkProvider> = Arc::new(NetworkProviderReqwest::new());
        let mut client = NetworkClient::new("secret-test", None, None);
        client.net_provider = Arc::downgrade(&network_provider);

        let retry_response = client
            .get_with_response_limit(
                RequestArgs {
                    url: format!("{}/v1/dynamic_config_value/retry", server.uri()),
                    retries: 1,
                    ..RequestArgs::new()
                },
                5,
            )
            .await
            .expect("retrying blob request should succeed");
        assert_eq!(retry_response.status_code, Some(200));

        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/oversized-success"))
            .respond_with(ResponseTemplate::new(200).set_body_bytes(b"too-large"))
            .expect(1)
            .mount(&server)
            .await;

        let oversized_success = client
            .get_with_response_limit(
                RequestArgs {
                    url: format!("{}/v1/dynamic_config_value/oversized-success", server.uri()),
                    retries: 1,
                    ..RequestArgs::new()
                },
                5,
            )
            .await;
        assert!(matches!(
            oversized_success,
            Err(NetworkError::RequestNotRetryable(_, Some(200), _))
        ));

        server.verify().await;
    }

    #[test]
    fn test_log_event_connection_reuse_defaults_to_true() {
        assert!(NetworkClient::new("secret-test", None, None).log_event_connection_reuse);
        assert!(
            NetworkClient::new("secret-test", None, Some(&StatsigOptions::default()))
                .log_event_connection_reuse
        );

        let options = StatsigOptions {
            log_event_connection_reuse: Some(false),
            ..StatsigOptions::default()
        };
        assert!(
            !NetworkClient::new("secret-test", None, Some(&options)).log_event_connection_reuse
        );
    }

    #[test]
    fn test_get_request_path_with_sample_urls() {
        assert_eq!(
            get_request_path(
                "https://statsigcdn.openai.com/v1/download_id_list_file/3wHgh0FhoQH0p"
            ),
            "/v1/download_id_list_file"
        );
        assert_eq!(
            get_request_path(
                "https://statsigcdn.openai.com/v1/download_id_list_file/Q9mXcz7L1P43tRb8kV2dHyw%2FM6nJf0Ae5uTqsrC4Gp9KZ?foo=bar"
            ),
            "/v1/download_id_list_file"
        );
        assert_eq!(
            get_request_path("https://api.oaistatsig.com/v1/get_id_lists/secret-abcdef"),
            "/v1/get_id_lists"
        );
        assert_eq!(
            get_request_path(
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-123456"
            ),
            "/v2/download_config_specs"
        );
        assert_eq!(
            get_request_path("https://api.oaistatsig.com/v1/log_event"),
            "/v1/log_event"
        );
    }

    #[test]
    fn test_should_log_network_request_latency_for_supported_endpoints() {
        assert!(should_log_network_request_latency(
            "https://api.oaistatsig.com/v1/log_event"
        ));
        assert!(!should_log_network_request_latency(
            "https://api.oaistatsig.com/v1/sdk_exception"
        ));
        assert!(should_log_network_request_latency(
            "https://api.oaistatsig.com/v1/get_id_lists/secret-abcdef"
        ));
        assert!(should_log_network_request_latency(
            "https://statsigcdn.openai.com/v2/download_config_specs/secret-123456"
        ));
        assert!(should_log_network_request_latency(
            "https://statsigcdn.openai.com/v1/download_id_list_file/3wHgh0FhoQH0p"
        ));
    }

    #[test]
    fn test_get_source_service_and_request_path() {
        let (source_service, request_path) = get_source_service_and_request_path(
            "http://127.0.0.1:12345/mock-uuid/v2/download_config_specs/secret-key.json?x=1",
        );
        assert_eq!(source_service, "http://127.0.0.1:12345/mock-uuid");
        assert_eq!(request_path, "/v2/download_config_specs");
    }

    #[test]
    fn test_network_latency_tags_include_id_list_file_id_only_when_present() {
        let mut request_args = RequestArgs {
            url: "https://statsigcdn.openai.com/v1/download_id_list_file/file-123".to_string(),
            id_list_file_id: Some("file-123".to_string()),
            ..RequestArgs::new()
        };

        let tags = get_network_request_latency_tags(
            &request_args,
            "200".to_string(),
            true,
            "client-key-123".to_string(),
        );
        assert_eq!(tags.get(ID_LIST_FILE_ID_TAG), Some(&"file-123".to_string()));
        assert_eq!(tags.get(DELTAS_USED_TAG), Some(&"false".to_string()));
        assert_eq!(
            tags.get(REQUEST_PATH_TAG),
            Some(&"/v1/download_id_list_file".to_string())
        );

        request_args.id_list_file_id = Some(String::new());
        request_args.deltas_enabled = true;
        let tags_without_id = get_network_request_latency_tags(
            &request_args,
            "200".to_string(),
            true,
            "client-key-123".to_string(),
        );
        assert!(!tags_without_id.contains_key(ID_LIST_FILE_ID_TAG));
        assert_eq!(
            tags_without_id.get(DELTAS_USED_TAG),
            Some(&"true".to_string())
        );
    }

    #[test]
    fn test_network_error_extra_tags_include_request_path_and_status_code() {
        let request_args = RequestArgs {
            url: "https://prodregistryv2.org/v1/log_event".to_string(),
            ..RequestArgs::new()
        };
        let error = NetworkError::RequestNotRetryable(
            request_args.url.clone(),
            Some(429),
            "Too Many Requests".to_string(),
        );

        let tags = get_network_error_extra_tags(&error, &request_args);

        assert_eq!(
            tags.get(REQUEST_PATH_TAG),
            Some(&"/v1/log_event".to_string())
        );
        assert_eq!(tags.get(STATUS_CODE_TAG), Some(&"429".to_string()));
    }
}
