use crate::compression::compression_helper::{
    compress_data, compress_zstd_data, get_compression_format,
};
use crate::event_logging_adapter::EventLoggingAdapter;
use crate::log_event_payload::{LogEventRequest, SerializedLogEventRequest};
use crate::networking::{NetworkClient, NetworkError, RequestArgs};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::statsig_metadata::StatsigMetadata;
use crate::{StatsigErr, StatsigOptions, StatsigRuntime, log_d};
use async_trait::async_trait;
use serde::Deserialize;
use std::collections::HashMap;
use std::sync::Arc;

const DEFAULT_LOG_EVENT_URL: &str = "https://api.oaistatsig.com/v1/log_event";
const DIRECT_EVENT_SERIALIZATION_FLAG: &str = "direct_event_serialization";
const EVENT_COMPRESSION_ZSTD_FLAG: &str = "event_compression_zstd";

#[derive(Deserialize)]
struct LogEventResult {
    success: Option<bool>,
}

const TAG: &str = stringify!(StatsigHttpEventLoggingAdapter);

pub struct StatsigHttpEventLoggingAdapter {
    direct_event_serialization_enabled: bool,
    event_compression_zstd_enabled: bool,
    event_compression_format: String,
    log_event_url: String,
    network: NetworkClient,
    ops_stats: Arc<OpsStatsForInstance>,
}

impl StatsigHttpEventLoggingAdapter {
    #[must_use]
    pub fn new(sdk_key: &str, options: Option<&StatsigOptions>) -> Self {
        let headers = StatsigMetadata::get_constant_request_headers(
            sdk_key,
            options.and_then(|opts| opts.service_name.as_deref()),
        );

        let log_event_url = options
            .and_then(|opts| opts.log_event_url.as_ref())
            .map(|u| u.to_string())
            .unwrap_or_else(|| DEFAULT_LOG_EVENT_URL.to_string());

        let sdk_instance_id = options
            .map(|opts| opts.get_sdk_instance_id(sdk_key))
            .unwrap_or(sdk_key);

        let direct_event_serialization_enabled = options
            .and_then(|opts| opts.experimental_flags.as_ref())
            .is_some_and(|flags| flags.contains(DIRECT_EVENT_SERIALIZATION_FLAG));

        // This feature is compiled only into the PyO3 wheel. The per-instance
        // flag keeps gzip as the default and gives callers an immediate kill
        // switch without changing custom EventLoggingAdapter behavior.
        let event_compression_zstd_enabled = cfg!(feature = "pyo3_event_zstd")
            && options
                .and_then(|opts| opts.experimental_flags.as_ref())
                .is_some_and(|flags| flags.contains(EVENT_COMPRESSION_ZSTD_FLAG));
        let event_compression_format = if event_compression_zstd_enabled {
            "zstd".to_string()
        } else {
            get_compression_format()
        };

        Self {
            direct_event_serialization_enabled,
            event_compression_zstd_enabled,
            event_compression_format,
            log_event_url,
            network: NetworkClient::new(sdk_key, Some(headers), options),
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
        }
    }

    pub async fn send_events_over_http(&self, request: &LogEventRequest) -> Result<(), StatsigErr> {
        let payload = serde_json::to_vec(&request.payload)
            .map_err(|e| StatsigErr::SerializationError(e.to_string()))?;
        self.send_serialized_events_over_http(SerializedLogEventRequest {
            payload,
            event_count: request.event_count,
            retries: request.retries,
            flush_type: get_request_flush_type(request),
        })
        .await
    }

    async fn send_serialized_events_over_http(
        &self,
        request: SerializedLogEventRequest,
    ) -> Result<(), StatsigErr> {
        let SerializedLogEventRequest {
            payload,
            event_count,
            retries,
            flush_type,
        } = request;

        log_d!(
            TAG,
            "Logging Events ({}): {}",
            event_count,
            String::from_utf8_lossy(&payload)
        );

        // Set headers
        let headers = HashMap::from([
            ("statsig-event-count".to_string(), event_count.to_string()),
            ("statsig-retry-count".to_string(), retries.to_string()),
            (
                "Content-Encoding".to_owned(),
                self.event_compression_format.clone(),
            ),
            ("Content-Type".to_owned(), "application/json".to_owned()),
        ]);

        // Compress data before sending it
        self.ops_stats
            .log_event_request_uncompressed_body_size_bytes(
                payload.len(),
                flush_type,
                self.get_observability_tags(),
            );

        let compressed = match self.compress_event_payload(&payload) {
            Ok(c) => c,
            Err(e) => return Err(e),
        };
        // The request body may stay in flight for a while. Once compression is done,
        // retain only the compressed bytes instead of holding both full buffers.
        drop(payload);

        // Make request
        let response = self
            .network
            .post(
                RequestArgs {
                    url: self.log_event_url.clone(),
                    headers: Some(headers),
                    accept_gzip_response: true,
                    ..RequestArgs::new()
                },
                Some(compressed),
            )
            .await
            .map_err(StatsigErr::NetworkError)?;

        let mut res_data = match response.data {
            Some(data) => data,
            None => {
                return Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                    self.log_event_url.clone(),
                    response.status_code,
                    "Empty response from network".to_string(),
                )));
            }
        };

        let result = res_data
            .deserialize_into::<LogEventResult>()
            .map(|result| result.success != Some(false))
            .map_err(|e| {
                StatsigErr::JsonParseError(stringify!(LogEventResult).to_string(), e.to_string())
            })?;

        if result {
            Ok(())
        } else {
            Err(StatsigErr::LogEventError(
                "Unsuccessful response from network".into(),
            ))
        }
    }

    fn compress_event_payload(&self, payload: &[u8]) -> Result<Vec<u8>, StatsigErr> {
        if self.event_compression_zstd_enabled {
            compress_zstd_data(payload)
        } else {
            compress_data(payload)
        }
    }
}

fn get_request_flush_type(request: &LogEventRequest) -> String {
    request
        .payload
        .statsig_metadata
        .get("flushType")
        .and_then(|value| value.as_str())
        .unwrap_or("unknown")
        .to_string()
}

#[async_trait]
impl EventLoggingAdapter for StatsigHttpEventLoggingAdapter {
    async fn start(&self, _statsig_runtime: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn log_events(&self, request: LogEventRequest) -> Result<bool, StatsigErr> {
        match self.send_events_over_http(&request).await {
            Ok(()) => Ok(true),
            Err(e) => Err(e),
        }
    }

    fn supports_serialized_events(&self) -> bool {
        self.direct_event_serialization_enabled
    }

    async fn log_serialized_events(
        &self,
        request: SerializedLogEventRequest,
    ) -> Result<bool, StatsigErr> {
        match self.send_serialized_events_over_http(request).await {
            Ok(()) => Ok(true),
            Err(e) => Err(e),
        }
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    fn should_schedule_background_flush(&self) -> bool {
        true
    }

    fn get_observability_tags(&self) -> Option<HashMap<String, String>> {
        Some(HashMap::from([(
            "source_api".to_string(),
            self.log_event_url.clone(),
        )]))
    }
}

#[test]
fn direct_event_serialization_is_opt_in() {
    use std::collections::HashSet;

    let default_adapter = StatsigHttpEventLoggingAdapter::new("secret-test", None);
    assert!(!default_adapter.supports_serialized_events());

    let unrelated_options = StatsigOptions {
        experimental_flags: Some(HashSet::from(["other_flag".to_string()])),
        ..StatsigOptions::default()
    };
    let unrelated_flag_adapter =
        StatsigHttpEventLoggingAdapter::new("secret-test", Some(&unrelated_options));
    assert!(!unrelated_flag_adapter.supports_serialized_events());

    let enabled_options = StatsigOptions {
        experimental_flags: Some(HashSet::from([DIRECT_EVENT_SERIALIZATION_FLAG.to_string()])),
        ..StatsigOptions::default()
    };
    let enabled_adapter =
        StatsigHttpEventLoggingAdapter::new("secret-test", Some(&enabled_options));
    assert!(enabled_adapter.supports_serialized_events());
}

#[test]
fn event_compression_zstd_is_feature_gated_and_opt_in() {
    use std::collections::HashSet;

    let default_adapter = StatsigHttpEventLoggingAdapter::new("secret-test", None);
    assert!(!default_adapter.event_compression_zstd_enabled);

    let options = StatsigOptions {
        experimental_flags: Some(HashSet::from([EVENT_COMPRESSION_ZSTD_FLAG.to_string()])),
        ..StatsigOptions::default()
    };
    let adapter = StatsigHttpEventLoggingAdapter::new("secret-test", Some(&options));
    assert_eq!(
        adapter.event_compression_zstd_enabled,
        cfg!(feature = "pyo3_event_zstd")
    );
}

#[cfg(not(feature = "with_zstd"))]
#[tokio::test]
async fn test_event_logging() {
    use crate::log_event_payload::{LogEventPayload, LogEventRequest};
    use std::env;

    let sdk_key = env::var("test_api_key").expect("test_api_key environment variable not set");

    let adapter = StatsigHttpEventLoggingAdapter::new(&sdk_key, None);

    let payload_str = r#"{"events":[{"eventName":"statsig::config_exposure","metadata":{"config":"running_exp_in_unlayered_with_holdout","ruleID":"5suobe8yyvznqasn9Ph1dI"},"secondaryExposures":[{"gate":"global_holdout","gateValue":"false","ruleID":"3QoA4ncNdVGBaMt3N1KYjz:0.50:1"},{"gate":"exp_holdout","gateValue":"false","ruleID":"1rEqLOpCROaRafv7ubGgax"}],"time":1722386636538,"user":{"appVersion":null,"country":null,"custom":null,"customIDs":null,"email":"daniel@statsig.com","ip":null,"locale":null,"privateAttributes":null,"statsigEnvironment":null,"userAgent":null,"userID":"a-user"},"value":null}],"statsigMetadata":{"sdk_type":"statsig-server-core","sdk_version":"0.0.1"}}"#;
    let payload = serde_json::from_str::<LogEventPayload>(payload_str).unwrap();

    let request = LogEventRequest {
        payload,
        event_count: 1,
        retries: 0,
    };

    let result = adapter.log_events(request).await;

    assert!(result.is_ok(), "Error logging events: {:?}", result.err());
}

#[cfg(not(feature = "with_zstd"))]
#[tokio::test]
async fn serialized_event_path_preserves_http_payload_and_headers() {
    use crate::log_event_payload::SerializedLogEventRequest;
    use flate2::read::GzDecoder;
    use serde_json::json;
    use std::io::Read;
    use wiremock::{
        Mock, MockServer, Request, ResponseTemplate,
        matchers::{method, path},
    };

    let server = MockServer::start().await;
    let payload = serde_json::to_vec(&json!({
        "events": [{"eventName": "statsig::config_exposure"}],
        "statsigMetadata": {"flushType": "scheduled_max_time"},
    }))
    .unwrap();
    let expected_payload = payload.clone();

    Mock::given(method("POST"))
        .and(path("/v1/log_event"))
        .respond_with(move |request: &Request| {
            assert_eq!(request.headers.get("statsig-event-count").unwrap(), "3");
            assert_eq!(request.headers.get("statsig-retry-count").unwrap(), "2");
            assert_eq!(request.headers.get("content-encoding").unwrap(), "gzip");
            assert_eq!(
                request.headers.get("content-type").unwrap(),
                "application/json"
            );

            let mut decoded = Vec::new();
            GzDecoder::new(request.body.as_slice())
                .read_to_end(&mut decoded)
                .unwrap();
            assert_eq!(decoded, expected_payload);

            ResponseTemplate::new(200).set_body_json(json!({"success": true}))
        })
        .mount(&server)
        .await;

    let options = StatsigOptions {
        log_event_url: Some(format!("{}/v1/log_event", server.uri())),
        ..StatsigOptions::default()
    };
    let adapter = StatsigHttpEventLoggingAdapter::new("secret-test", Some(&options));

    assert!(
        adapter
            .log_serialized_events(SerializedLogEventRequest {
                payload,
                event_count: 3,
                retries: 2,
                flush_type: "scheduled_max_time".to_string(),
            })
            .await
            .unwrap()
    );
}

#[cfg(all(feature = "pyo3_event_zstd", not(feature = "with_zstd")))]
#[tokio::test]
async fn event_compression_zstd_repeated_adapter_calls_preserve_payload_and_update_retry_header() {
    use crate::log_event_payload::SerializedLogEventRequest;
    use serde_json::json;
    use std::collections::HashSet;
    use std::sync::Mutex;
    use wiremock::{
        Mock, MockServer, Request, ResponseTemplate,
        matchers::{method, path},
    };

    let server = MockServer::start().await;
    let payload = serde_json::to_vec(&json!({
        "events": [
            {"eventName": "first", "time": 1},
            {"eventName": "second", "time": 2}
        ],
        "statsigMetadata": {"flushType": "scheduled_max_time"},
    }))
    .unwrap();
    let expected_payload = payload.clone();
    let observed_requests = Arc::new(Mutex::new(Vec::new()));
    let response_observations = observed_requests.clone();

    Mock::given(method("POST"))
        .and(path("/v1/log_event"))
        .respond_with(move |request: &Request| {
            assert_eq!(request.headers.get("statsig-event-count").unwrap(), "2");
            assert_eq!(request.headers.get("content-encoding").unwrap(), "zstd");
            assert_eq!(
                request.headers.get("content-type").unwrap(),
                "application/json"
            );

            let decoded =
                zstd::bulk::decompress(request.body.as_slice(), expected_payload.len()).unwrap();
            assert_eq!(decoded, expected_payload);
            response_observations.lock().unwrap().push((
                request
                    .headers
                    .get("statsig-retry-count")
                    .unwrap()
                    .to_str()
                    .unwrap()
                    .to_string(),
                request.body.clone(),
            ));

            ResponseTemplate::new(200).set_body_json(json!({"success": true}))
        })
        .expect(2)
        .mount(&server)
        .await;

    let options = StatsigOptions {
        log_event_url: Some(format!("{}/v1/log_event", server.uri())),
        experimental_flags: Some(HashSet::from([
            DIRECT_EVENT_SERIALIZATION_FLAG.to_string(),
            EVENT_COMPRESSION_ZSTD_FLAG.to_string(),
        ])),
        ..StatsigOptions::default()
    };
    let adapter = StatsigHttpEventLoggingAdapter::new("secret-test", Some(&options));

    // This exercises two direct adapter calls with the same serialized request
    // payload. EventLogger retries may reserialize changing Statsig metadata.
    for retries in [0, 1] {
        assert!(
            adapter
                .log_serialized_events(SerializedLogEventRequest {
                    payload: payload.clone(),
                    event_count: 2,
                    retries,
                    flush_type: "scheduled_max_time".to_string(),
                })
                .await
                .unwrap()
        );
    }

    let observed_requests = observed_requests.lock().unwrap();
    assert_eq!(observed_requests.len(), 2);
    assert_eq!(observed_requests[0].0, "0");
    assert_eq!(observed_requests[1].0, "1");
    assert_eq!(observed_requests[0].1, observed_requests[1].1);
}
