use std::collections::HashMap;

use async_trait::async_trait;
use serde::Serialize;
use serde_json::Value;
use tokio::sync::RwLock;

use crate::{
    OpsStatsEventObserver, StatsigOptions, log_d, log_e,
    networking::{NetworkClient, RequestArgs},
    statsig_metadata::StatsigMetadata,
};

use super::ops_stats::OpsStatsEvent;

static STATSIG_SDK_EXCEPTION_URL: &str = "https://api.oaistatsig.com/v1/sdk_exception";

fn get_sdk_exception_endpoint() -> String {
    #[cfg(feature = "testing")]
    if let Ok(url) = std::env::var("STATSIG_SDK_EXCEPTION_URL") {
        return url;
    }

    STATSIG_SDK_EXCEPTION_URL.to_string()
}

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ErrorBoundaryEvent {
    pub tag: String,
    pub info: String,
    pub exception: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub dedupe_key: Option<String>,

    pub bypass_dedupe: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub extra: Option<HashMap<String, String>>,
}

const TAG: &str = stringify!(SDKErrorsObserver);
const MAX_SEEN_ERRORS: usize = 1000;

// Observer to post to scrapi when exception happened
// If we never see the exception, log to sdk exception
// TODO: By session end, we flush stats
pub struct SDKErrorsObserver {
    output_policy: crate::output_policy::OutputPolicy,
    errors_aggregator: RwLock<HashMap<String, u32>>,
    network_client: NetworkClient,
    statsig_options_logging_copy: String,
    sdk_exception_url: String,
}

impl SDKErrorsObserver {
    pub fn new(sdk_key: &str, options: &StatsigOptions) -> Self {
        let mut headers =
            StatsigMetadata::get_constant_request_headers(sdk_key, options.service_name.as_deref());
        headers.insert("Content-Type".to_string(), "application/json".to_string());
        let output_policy = crate::output_policy::OutputPolicy::from_options(Some(options));
        let options_logging_copy = if output_policy.is_silent() {
            String::new()
        } else {
            serde_json::to_string(options).unwrap_or_default()
        };
        SDKErrorsObserver {
            output_policy,
            network_client: NetworkClient::new(sdk_key, Some(headers), Some(options))
                .mute_network_error_log(),
            errors_aggregator: RwLock::new(HashMap::new()),
            statsig_options_logging_copy: options_logging_copy,
            sdk_exception_url: get_sdk_exception_endpoint(),
        }
    }

    async fn handle_eb_event(&self, eb_event: ErrorBoundaryEvent) {
        let key = eb_event
            .dedupe_key
            .clone()
            .unwrap_or(format!("{}:{}", eb_event.tag, eb_event.exception));

        let write_guard_result = tokio::time::timeout(
            std::time::Duration::from_secs(5),
            self.errors_aggregator.write(),
        )
        .await;

        let mut write_guard = match write_guard_result {
            Ok(guard) => guard,
            Err(_) => {
                log_e!(TAG, "Failed to acquire write lock on errors_aggregator");
                return;
            }
        };

        if write_guard.len() >= MAX_SEEN_ERRORS {
            write_guard.clear();
        }

        let count = write_guard.entry(key).or_default();
        *count += 1;
        if *count > 1 && !eb_event.bypass_dedupe {
            return;
        }

        self.log_exception(eb_event).await;
    }

    async fn log_exception(&self, e: ErrorBoundaryEvent) {
        let mut body_obj = serde_json::to_value(e).unwrap_or_default();
        if let Value::Object(ref mut map) = body_obj {
            map.insert(
                "statsigOptions".to_string(),
                Value::String(self.statsig_options_logging_copy.clone()),
            );
        }
        let body = serde_json::to_string_pretty(&body_obj).unwrap_or_default();

        log_d!(TAG, "Caught SDK Exception: {}", body);

        let request_args = RequestArgs {
            url: self.sdk_exception_url.clone(),
            retries: 0,
            ..RequestArgs::new()
        };
        let _ = self
            .network_client
            .post(request_args, Some(body.into()))
            .await;
    }
}

#[async_trait]
impl OpsStatsEventObserver for SDKErrorsObserver {
    async fn handle_event(&self, event: OpsStatsEvent) {
        if self.output_policy.is_silent() {
            return;
        }
        if let OpsStatsEvent::SDKError(e) = event {
            self.handle_eb_event(e).await;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::networking::{HttpMethod, NetworkProvider, Response};
    use std::sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
    };

    struct RecordingTransport(AtomicUsize);

    #[async_trait]
    impl NetworkProvider for RecordingTransport {
        async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
            self.0.fetch_add(1, Ordering::SeqCst);
            Response {
                status_code: Some(200),
                data: None,
                error: None,
            }
        }
    }

    #[tokio::test]
    async fn silent_observer_never_posts_exception_or_disables_same_id_ordinary_observer() {
        let transport = Arc::new(RecordingTransport(AtomicUsize::new(0)));
        let network: Arc<dyn NetworkProvider> = transport.clone();
        for silent in [true, false] {
            let options = StatsigOptions {
                sdk_instance_id: Some("same-instance".into()),
                ..StatsigOptions::default()
            }
            .suppress_diagnostic_output(silent);
            let mut observer = SDKErrorsObserver::new("secret-FAKE_ONLY", &options);
            observer
                .network_client
                .set_network_provider_for_test(Arc::downgrade(&network));
            observer
                .handle_event(OpsStatsEvent::SDKError(ErrorBoundaryEvent {
                    tag: "fake".into(),
                    info: "secret-FAKE_ONLY payload".into(),
                    exception: "fixture".into(),
                    dedupe_key: None,
                    bypass_dedupe: false,
                    extra: None,
                }))
                .await;
            assert_eq!(transport.0.load(Ordering::SeqCst), usize::from(!silent));
            if silent {
                assert!(observer.statsig_options_logging_copy.is_empty());
                assert!(observer.errors_aggregator.read().await.is_empty());
            }
        }
    }
}
