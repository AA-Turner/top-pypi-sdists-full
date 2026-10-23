use super::config_spec_background_sync_metrics::{
    ConfigSyncMetrics, ConfigSyncResponseType, log_config_sync_full_fallback_count,
    log_config_sync_overall_latency,
};
use super::remote_config_value_hydrator::RemoteConfigValueHydrator;
#[cfg(test)]
use super::response_format::{SpecsResponseFormat, get_specs_response_format};
use crate::data_store_interface::ENABLE_DCS_ZSTD_DATASTORE_FLAG;
use crate::networking::HttpMethod;
use crate::networking::retry::{
    PrimaryOutcome, RefreshFailureTracker, RetryPolicy, retryable_network_error,
};
use crate::networking::{
    DEFAULT_CDN_SPECS_URL, NetworkClient, NetworkError, RequestArgs, ResponseData, api_from_url,
    config_specs_url,
};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::spec_store::SpecStore;
use crate::specs_adapter::{SpecsAdapter, SpecsUpdate, SpecsUpdateHydration, SpecsUpdateListener};
use crate::statsig_err::StatsigErr;
use crate::statsig_metadata::StatsigMetadata;
use crate::{
    SpecsSource, StatsigOptions, StatsigRuntime, log_d, log_e, log_error_to_statsig_and_console,
};
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::RwLock;
use percent_encoding::percent_encode;
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Weak};
use std::time::Duration;
use tokio::sync::Notify;
use tokio::time::sleep;

use super::SpecsInfo;

pub struct NetworkResponse {
    pub data: ResponseData,
    pub loggable_api: String,
    pub requested_deltas: bool,
    pub request_url: String,
}

pub const DEFAULT_SYNC_INTERVAL_MS: u32 = 10_000;
const DEFAULT_INIT_REQUEST_TIMEOUT_MS: u64 = 5_000;

#[cfg(test)]
#[path = "__tests__/state_read_retry_tests.rs"]
mod state_read_retry_tests;

#[cfg(test)]
#[path = "__tests__/response_metrics_reuse_tests.rs"]
mod response_metrics_reuse_tests;

const FOREGROUND_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 2,
    jitter: true,
};
const BACKGROUND_RETRY_POLICY: RetryPolicy = RetryPolicy {
    attempts: 4,
    ..FOREGROUND_RETRY_POLICY
};

const TAG: &str = stringify!(StatsigHttpSpecsAdapter);
const INITIAL_DELTA_CURSOR_STATE: &str = "initial";
const INCREMENTAL_DELTA_CURSOR_STATE: &str = "incremental";
const DCS_ZSTD_ACCEPT_ENCODING: &str = "statsig-zstd, statsig-br, gzip, deflate, br";

#[derive(Clone)]
enum HttpSpecsListener {
    External(Arc<dyn SpecsUpdateListener>),
    Store(Arc<SpecStore>),
}

impl HttpSpecsListener {
    fn as_listener(&self) -> &dyn SpecsUpdateListener {
        match self {
            Self::External(listener) => listener.as_ref(),
            Self::Store(store) => store.as_ref(),
        }
    }
}

pub struct StatsigHttpSpecsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    foreground_retry_policy: RetryPolicy,
    background_retry_policy: RetryPolicy,
    listener: RwLock<Option<HttpSpecsListener>>,
    network: Arc<NetworkClient>,
    remote_config_value_hydrator: Arc<RemoteConfigValueHydrator>,
    specs_url: String,
    remote_config_value_source_url: Option<String>,
    fallback_url: Option<String>,
    init_timeout_ms: u64,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown_notify: Arc<Notify>,
    allow_dcs_deltas: bool,
    // Datastore-backed adapters stay on Brotli until a follow-up rollout opts
    // them into the codec-aware datastore path. The same statsig-zstd token
    // covers both full and delta protobuf responses.
    allow_dcs_zstd: bool,
    use_deltas_next_request: AtomicBool,
    background_sync_failure_count: RefreshFailureTracker,
}

fn is_process_success(result: &Result<(), StatsigErr>) -> bool {
    result.is_ok()
}

impl StatsigHttpSpecsAdapter {
    pub(crate) fn initialize_spec_store(&self, store: Arc<SpecStore>) {
        self.set_listener(HttpSpecsListener::Store(store));
    }

    fn set_listener(&self, listener: HttpSpecsListener) {
        let _output_scope = self.output_policy.enter();
        match self.listener.try_write_for(Duration::from_secs(5)) {
            Some(mut lock) => *lock = Some(listener),
            None => log_e!(TAG, "Failed to acquire write lock on listener"),
        }
    }

    fn retry_policy(&self, trigger: SpecsSyncTrigger) -> RetryPolicy {
        if trigger == SpecsSyncTrigger::Background {
            self.background_retry_policy
        } else {
            self.foreground_retry_policy
        }
    }

    fn network_retry_limit(&self, error: &NetworkError) -> Option<u32> {
        // A successful status with a failed body read had no primary retry before this policy.
        retryable_network_error(error).then_some(
            if error
                .status_code()
                .is_some_and(|status| (200..300).contains(&status))
            {
                self.foreground_retry_policy.attempts
            } else {
                u32::MAX
            },
        )
    }

    fn retry_limit(&self, error: &StatsigErr) -> Option<u32> {
        match error {
            StatsigErr::NetworkError(error) => self.network_retry_limit(error),
            StatsigErr::SerializationError(_) => Some(self.foreground_retry_policy.attempts),
            _ => None,
        }
    }

    #[must_use]
    pub fn new(
        sdk_key: &str,
        options: Option<&StatsigOptions>,
        override_url: Option<String>,
    ) -> Self {
        let output_policy = crate::output_policy::OutputPolicy::from_options(options);
        let _output_scope = output_policy.enter();
        let default_options = StatsigOptions::default();
        let options_ref = options.unwrap_or(&default_options);
        let retry_override =
            RetryPolicy::state_read_override(options_ref.state_read_primary_attempts);

        let init_timeout_ms = options_ref
            .init_timeout_ms
            .unwrap_or(DEFAULT_INIT_REQUEST_TIMEOUT_MS);

        let specs_url = match override_url {
            Some(url) => url,
            None => options_ref
                .specs_url
                .as_ref()
                .map(|u| u.to_string())
                .unwrap_or(DEFAULT_CDN_SPECS_URL.to_string()),
        };

        // only fallback when the spec_url is not the default CDN specs URL
        let fallback_url = if options_ref.fallback_to_statsig_api.unwrap_or(false)
            && specs_url != DEFAULT_CDN_SPECS_URL
        {
            Some(DEFAULT_CDN_SPECS_URL.to_string())
        } else {
            None
        };

        let headers = StatsigMetadata::get_constant_request_headers(
            sdk_key,
            options_ref.service_name.as_deref(),
        );
        let enable_dcs_deltas = options_ref.enable_dcs_deltas.unwrap_or(false);
        let allow_dcs_zstd = options_ref.data_store.is_none()
            || options_ref
                .experimental_flags
                .as_ref()
                .is_some_and(|flags| flags.contains(ENABLE_DCS_ZSTD_DATASTORE_FLAG));

        let sdk_instance_id = options_ref.get_sdk_instance_id(sdk_key);
        let ops_stats = OPS_STATS.get_for_instance(sdk_instance_id);
        let network = Arc::new(NetworkClient::new(
            sdk_key,
            Some(headers),
            Some(options_ref),
        ));

        Self {
            output_policy,
            foreground_retry_policy: retry_override.unwrap_or(FOREGROUND_RETRY_POLICY),
            background_retry_policy: retry_override.unwrap_or(BACKGROUND_RETRY_POLICY),
            listener: RwLock::new(None),
            network: network.clone(),
            remote_config_value_hydrator: Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
                network,
                ops_stats.clone(),
            )),
            specs_url,
            remote_config_value_source_url: options_ref.remote_config_value_source_url.clone(),
            fallback_url,
            init_timeout_ms,
            sync_interval_duration: Duration::from_millis(u64::from(
                options_ref
                    .specs_sync_interval_ms
                    .unwrap_or(DEFAULT_SYNC_INTERVAL_MS),
            )),
            ops_stats,
            shutdown_notify: Arc::new(Notify::new()),
            allow_dcs_deltas: enable_dcs_deltas,
            allow_dcs_zstd,
            use_deltas_next_request: AtomicBool::new(enable_dcs_deltas),
            background_sync_failure_count: RefreshFailureTracker::default(),
        }
    }

    pub fn force_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.network.shutdown();
        self.shutdown_notify.notify_one();
    }

    pub async fn fetch_specs_from_network(
        &self,
        current_specs_info: SpecsInfo,
        trigger: SpecsSyncTrigger,
    ) -> Result<NetworkResponse, NetworkError> {
        self.output_policy
            .scope(async {
                self.network
                    .retry_executor(self.retry_policy(trigger))
                    .run(
                        |_, index| {
                            let current_specs_info = &current_specs_info;
                            async move {
                                self.fetch_specs_once(
                                    current_specs_info,
                                    trigger,
                                    true,
                                    false,
                                    index,
                                )
                                .await
                                .map_err(|(error, _)| error)
                            }
                        },
                        |error| self.network_retry_limit(error),
                        |_| false,
                        || NetworkError::ShutdownError(self.specs_url.clone()),
                    )
                    .await
            })
            .await
    }

    async fn fetch_specs_once(
        &self,
        current_specs_info: &SpecsInfo,
        trigger: SpecsSyncTrigger,
        supports_proto: bool,
        fallback: bool,
        index: u32,
    ) -> Result<NetworkResponse, (NetworkError, bool)> {
        let mut request_args = self.get_request_args(current_specs_info, trigger, supports_proto);
        if fallback {
            self.network.log_fallback("config_specs", true);
            request_args.url = config_specs_url(self.fallback_url.as_deref().unwrap());
        }
        let url = request_args.url.clone();
        let requested_deltas = request_args.deltas_enabled;
        let response = self
            .network
            .request_once(HttpMethod::GET, request_args, None, false, true, index)
            .await
            .map_err(|error| (error, requested_deltas))?;
        Ok(NetworkResponse {
            data: response.data.ok_or_else(|| {
                (
                    NetworkError::RequestFailed(
                        url.clone(),
                        response.status_code,
                        "No data in response".into(),
                    ),
                    requested_deltas,
                )
            })?,
            loggable_api: api_from_url(&url),
            requested_deltas,
            request_url: url,
        })
    }

    /// Fetches JSON specs and resolves any blob-backed dynamic config values
    /// before returning the response to a caller that consumes text bytes
    /// directly. A statsig-br response cannot be returned through the FFI
    /// string/local-file contracts.
    pub async fn fetch_hydrated_specs_from_network(
        &self,
        current_specs_info: SpecsInfo,
        trigger: SpecsSyncTrigger,
    ) -> Result<NetworkResponse, StatsigErr> {
        self.output_policy
            .scope(async {
                self.network
                    .retry_executor(self.retry_policy(trigger))
                    .run(
                        |_, index| {
                            let current_specs_info = &current_specs_info;
                            async move {
                                let mut response = self
                                    .fetch_specs_once(
                                        current_specs_info,
                                        trigger,
                                        false,
                                        false,
                                        index,
                                    )
                                    .await
                                    .map_err(|(error, _)| StatsigErr::NetworkError(error))?;
                                self.hydrate_network_response(&mut response, trigger)
                                    .await?;
                                Ok(response)
                            }
                        },
                        |error| self.retry_limit(error),
                        |_| false,
                        || {
                            StatsigErr::NetworkError(NetworkError::ShutdownError(
                                self.specs_url.clone(),
                            ))
                        },
                    )
                    .await
            })
            .await
    }

    fn get_request_args(
        &self,
        current_specs_info: &SpecsInfo,
        trigger: SpecsSyncTrigger,
        supports_proto: bool,
    ) -> RequestArgs {
        let mut params = HashMap::new();

        if supports_proto {
            params.insert("supports_proto".to_string(), "true".to_string());
        }
        if let Some(lcut) = current_specs_info.lcut {
            if lcut > 0 {
                params.insert("sinceTime".to_string(), lcut.to_string());
            }
        }

        let is_init_request = trigger == SpecsSyncTrigger::Initial;

        let timeout_ms = if is_init_request && self.init_timeout_ms > 0 {
            self.init_timeout_ms
        } else {
            0
        };

        if let Some(cs) = &current_specs_info.checksum {
            params.insert(
                "checksum".to_string(),
                percent_encode(cs.as_bytes(), percent_encoding::NON_ALPHANUMERIC).to_string(),
            );
        }

        let use_deltas_next_req = self.use_deltas_next_request.load(Ordering::SeqCst);
        if use_deltas_next_req {
            params.insert("accept_deltas".to_string(), "true".to_string());
        }
        let headers = if supports_proto {
            let accept_encoding = if self.allow_dcs_zstd {
                DCS_ZSTD_ACCEPT_ENCODING
            } else {
                "statsig-br, gzip, deflate, br"
            };
            Some(HashMap::from([
                ("statsig-supports-proto".to_string(), "true".to_string()),
                ("accept-encoding".to_string(), accept_encoding.to_string()),
            ]))
        } else {
            None
        };

        RequestArgs {
            url: config_specs_url(self.specs_url.as_str()),
            retries: self.retry_policy(trigger).attempts - 1,
            query_params: Some(params),
            deltas_enabled: use_deltas_next_req,
            accept_gzip_response: true,
            diagnostics_key: Some(KeyType::DownloadConfigSpecs),
            timeout_ms,
            headers,
            ..RequestArgs::new()
        }
    }

    pub async fn run_background_sync(self: Arc<Self>) {
        self.output_policy
            .scope(async {
                let specs_info = match self
                    .listener
                    .try_read_for(std::time::Duration::from_secs(5))
                {
                    Some(lock) => match lock.as_ref() {
                        Some(listener) => listener.as_listener().get_current_specs_info(),
                        None => SpecsInfo::empty(),
                    },
                    None => SpecsInfo::error(),
                };

                self.ops_stats
                    .set_diagnostics_context(ContextType::ConfigSync);
                if let Err(e) = self
                    .manually_sync_specs(specs_info, SpecsSyncTrigger::Background)
                    .await
                {
                    if let StatsigErr::NetworkError(NetworkError::DisableNetworkOn(_)) = e {
                        return;
                    }
                    log_e!(TAG, "Background specs sync failed: {}", e);
                }
                self.ops_stats.enqueue_diagnostics_event(
                    Some(KeyType::DownloadConfigSpecs),
                    Some(ContextType::ConfigSync),
                );
            })
            .await
    }

    async fn manually_sync_specs(
        &self,
        current_specs_info: SpecsInfo,
        trigger: SpecsSyncTrigger,
    ) -> Result<(), StatsigErr> {
        if let Some(lock) = self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            if lock.is_none() {
                return Err(StatsigErr::UnstartedAdapter("Listener not set".to_string()));
            }
        }

        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let delta_cursor_state = if current_specs_info.lcut.unwrap_or(0) > 0 {
            INCREMENTAL_DELTA_CURSOR_STATE
        } else {
            INITIAL_DELTA_CURSOR_STATE
        };
        let metrics = parking_lot::Mutex::new(None);
        let result = self
            .network
            .retry_executor(self.retry_policy(trigger))
            .run(
                |fallback, index| {
                    let metrics = &metrics;
                    let current_specs_info = &current_specs_info;
                    async move {
                        let mut response = self
                            .fetch_specs_once(current_specs_info, trigger, true, fallback, index)
                            .await;
                        let source_url = if fallback {
                            self.fallback_url.as_ref().unwrap()
                        } else {
                            &self.specs_url
                        };
                        let attempt_metrics = match &mut response {
                            Ok(response) => ConfigSyncMetrics::from_response_headers(
                                &response.data,
                                &response.loggable_api,
                                response.requested_deltas,
                            ),
                            Err((_, requested_deltas)) => {
                                ConfigSyncMetrics::from_network_error(source_url, *requested_deltas)
                            }
                        };
                        let requested_deltas = response.as_ref().is_ok_and(|r| r.requested_deltas);
                        *metrics.lock() = Some(attempt_metrics);
                        let result = self
                            .process_spec_data_with_metrics(
                                trigger,
                                response.map_err(|(error, _)| error),
                                Some(metrics),
                            )
                            .await;
                        match result {
                            // A bad delta spends the next remaining attempt on a full primary response.
                            Err(StatsigErr::ChecksumFailure(message)) if requested_deltas => {
                                Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                                    source_url.clone(),
                                    None,
                                    message,
                                )))
                            }
                            result => result,
                        }
                    }
                },
                |error| self.retry_limit(error),
                |outcome| {
                    let eligible = self
                        .background_sync_failure_count
                        .record(outcome, trigger == SpecsSyncTrigger::Background);
                    if outcome == PrimaryOutcome::Exhausted
                        && self.fallback_url.is_some()
                        && !eligible
                    {
                        self.network.log_fallback("config_specs", false);
                    }
                    eligible && self.fallback_url.is_some()
                },
                || StatsigErr::NetworkError(NetworkError::ShutdownError(self.specs_url.clone())),
            )
            .await;
        let Some(metrics) = metrics.into_inner() else {
            return result;
        };

        let process_success = is_process_success(&result);
        log_config_sync_overall_latency(
            &self.ops_stats,
            sync_start_ms,
            metrics.source_api.as_str(),
            metrics.response_format.as_str(),
            metrics.network_success,
            process_success,
            result
                .as_ref()
                .err()
                .map_or_else(String::new, |e| e.to_string()),
            metrics.deltas_used,
            metrics.response_type.as_str(),
        );
        log_config_sync_full_fallback_count(
            &self.ops_stats,
            metrics.source_api.as_str(),
            metrics.deltas_used,
            metrics.response_type.as_str(),
            metrics.delta_fallback_reason,
            metrics.delta_fallback_source,
            delta_cursor_state,
        );

        result
    }

    #[cfg(test)]
    async fn process_spec_data(
        &self,
        trigger: SpecsSyncTrigger,
        response: Result<NetworkResponse, NetworkError>,
    ) -> Result<(), StatsigErr> {
        self.process_spec_data_with_metrics(trigger, response, None)
            .await
    }

    async fn process_spec_data_with_metrics(
        &self,
        trigger: SpecsSyncTrigger,
        response: Result<NetworkResponse, NetworkError>,
        metrics: Option<&parking_lot::Mutex<Option<ConfigSyncMetrics>>>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                let resp = response.map_err(StatsigErr::NetworkError)?;
                let requested_deltas = resp.requested_deltas;
                let hydration = SpecsUpdateHydration::new(
                    self.remote_config_value_hydrator.clone(),
                    self.hydration_source_url(&resp.request_url).to_string(),
                )
                .with_sync_trigger(trigger);

                let mut update = SpecsUpdate {
                    data: resp.data,
                    source: SpecsSource::Network,
                    received_at: Utc::now().timestamp_millis() as u64,
                    source_api: Some(resp.loggable_api),
                    has_updates: None,
                };

                self.ops_stats.add_marker(
                    Marker::new(
                        KeyType::DownloadConfigSpecs,
                        ActionType::Start,
                        Some(StepType::Process),
                    ),
                    None,
                );

                let listener = match self
                    .listener
                    .try_read_for(std::time::Duration::from_secs(5))
                {
                    Some(lock) => match lock.as_ref() {
                        Some(listener) => Ok(listener.clone()),
                        None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
                    },
                    None => {
                        let err = StatsigErr::LockFailure(
                            "Failed to acquire read lock on listener".to_string(),
                        );
                        log_error_to_statsig_and_console!(&self.ops_stats, TAG, err.clone());
                        Err(err)
                    }
                };
                let body_metrics = metrics.filter(|_| {
                    ConfigSyncResponseType::from_headers(&update.data).is_none()
                });
                let result = match (listener, body_metrics) {
                    (Ok(HttpSpecsListener::Store(store)), Some(metrics))
                        if !crate::specs_response::proto_compression::is_compressed_protobuf_response(
                            &update.data,
                        ) =>
                    {
                        let has_updates = Arc::new(AtomicBool::new(true));
                        if let Some(metrics) = metrics.lock().as_mut() {
                            metrics.response_type = ConfigSyncResponseType::JsonBody(has_updates.clone());
                        }
                        store
                            .set_values_with_json_hydration_metrics(
                                update,
                                hydration,
                                &has_updates,
                            )
                            .await
                    }
                    (listener, metrics) => {
                        if let Some(metrics) = metrics {
                            let response_type = ConfigSyncResponseType::from_response_data(&mut update.data);
                            if let Some(metrics) = metrics.lock().as_mut() {
                                metrics.response_type = response_type;
                            }
                        }
                        match listener {
                            Ok(listener) => listener
                                .as_listener()
                                .did_receive_specs_update_async(update, Some(hydration))
                                .await,
                            Err(error) => Err(error),
                        }
                    }
                };

                if matches!(&result, Err(StatsigErr::ChecksumFailure(_))) {
                    let was_deltas_used =
                        self.use_deltas_next_request.swap(false, Ordering::SeqCst);
                    if was_deltas_used {
                        log_d!(TAG, "Disabling delta requests after checksum failure");
                    }
                } else if result.is_ok() && !requested_deltas && self.allow_dcs_deltas {
                    let was_deltas_used = self.use_deltas_next_request.swap(true, Ordering::SeqCst);
                    if !was_deltas_used {
                        log_d!(
                            TAG,
                            "Re-enabling delta requests after successful non-delta specs update"
                        );
                    }
                }

                self.ops_stats.add_marker(
                    Marker::new(
                        KeyType::DownloadConfigSpecs,
                        ActionType::End,
                        Some(StepType::Process),
                    )
                    .with_is_success(result.is_ok()),
                    None,
                );

                result
            })
            .await
    }

    pub(crate) async fn hydrate_network_response(
        &self,
        response: &mut NetworkResponse,
        trigger: SpecsSyncTrigger,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.remote_config_value_hydrator
                    .hydrate_response_with_trigger(
                        &mut response.data,
                        self.hydration_source_url(&response.request_url),
                        Some(trigger),
                    )
                    .await
            })
            .await
    }

    fn hydration_source_url<'a>(&'a self, request_url: &'a str) -> &'a str {
        self.remote_config_value_source_url
            .as_deref()
            .unwrap_or(request_url)
    }

    pub(crate) async fn hydrate_response_data(
        &self,
        data: &mut ResponseData,
        source_url: &str,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.remote_config_value_hydrator
                    .hydrate_response(data, source_url)
                    .await
            })
            .await
    }

    pub(crate) fn remote_config_value_hydrator(&self) -> &RemoteConfigValueHydrator {
        self.remote_config_value_hydrator.as_ref()
    }

    pub(crate) fn ops_stats(&self) -> &OpsStatsForInstance {
        self.ops_stats.as_ref()
    }
}

#[async_trait]
impl SpecsAdapter for StatsigHttpSpecsAdapter {
    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                let specs_info = match self
                    .listener
                    .try_read_for(std::time::Duration::from_secs(5))
                {
                    Some(lock) => match lock.as_ref() {
                        Some(listener) => listener.as_listener().get_current_specs_info(),
                        None => SpecsInfo::empty(),
                    },
                    None => SpecsInfo::error(),
                };
                self.manually_sync_specs(specs_info, SpecsSyncTrigger::Initial)
                    .await
            })
            .await
    }

    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        self.set_listener(HttpSpecsListener::External(listener));
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.output_policy.scope(async {
        let weak_self: Weak<StatsigHttpSpecsAdapter> = Arc::downgrade(&self);
        let interval_duration = self.sync_interval_duration;
        let shutdown_notify = self.shutdown_notify.clone();

        statsig_runtime.spawn("http_specs_bg_sync", move |rt_shutdown_notify| async move {
            loop {
                tokio::select! {
                    () = sleep(interval_duration) => {
                        if let Some(strong_self) = weak_self.upgrade() {
                            Self::run_background_sync(strong_self).await;
                        } else {
                            log_e!(TAG, "Strong reference to StatsigHttpSpecsAdapter lost. Stopping background sync");
                            break;
                        }
                    }
                    () = rt_shutdown_notify.notified() => {
                        log_d!(TAG, "Runtime shutdown. Shutting down specs background sync");
                        break;
                    },
                    () = shutdown_notify.notified() => {
                        log_d!(TAG, "Shutting down specs background sync");
                        break;
                    }
                }
            }
        })?;

        Ok(())
            }).await
    }

    async fn shutdown(
        &self,
        _timeout: Duration,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.network.shutdown();
                self.shutdown_notify.notify_one();
                Ok(())
            })
            .await
    }

    fn get_type_name(&self) -> String {
        stringify!(StatsigHttpSpecsAdapter).to_string()
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SpecsSyncTrigger {
    Initial,
    Background,
    Manual,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        StatsigOptions,
        data_store_interface::{DataStoreResponse, DataStoreTrait, RequestPath},
        networking::ResponseData,
        specs_adapter::SpecsUpdate,
        specs_response::statsig_config_specs as pb,
    };
    use async_trait::async_trait;
    use prost::Message;
    use std::collections::{HashMap, HashSet};
    use std::sync::atomic::AtomicUsize;

    struct NoopDataStore;

    #[async_trait]
    impl DataStoreTrait for NoopDataStore {
        async fn initialize(&self) -> Result<(), StatsigErr> {
            Ok(())
        }

        async fn shutdown(&self) -> Result<(), StatsigErr> {
            Ok(())
        }

        async fn get(&self, _key: &str) -> Result<DataStoreResponse, StatsigErr> {
            unreachable!("request-header tests never read the data store")
        }

        async fn set(
            &self,
            _key: &str,
            _value: &str,
            _time: Option<u64>,
        ) -> Result<(), StatsigErr> {
            unreachable!("request-header tests never write the data store")
        }

        async fn support_polling_updates_for(&self, _path: RequestPath) -> bool {
            false
        }
    }

    struct ChecksumFailingListener;

    impl SpecsUpdateListener for ChecksumFailingListener {
        fn did_receive_specs_update(&self, _update: SpecsUpdate) -> Result<(), StatsigErr> {
            Err(StatsigErr::ChecksumFailure(
                "simulated checksum failure".to_string(),
            ))
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    struct ChecksumFailingThenSuccessListener {
        calls: AtomicUsize,
    }

    impl SpecsUpdateListener for ChecksumFailingThenSuccessListener {
        fn did_receive_specs_update(&self, _update: SpecsUpdate) -> Result<(), StatsigErr> {
            let curr = self.calls.fetch_add(1, Ordering::SeqCst);
            if curr == 0 {
                Err(StatsigErr::ChecksumFailure(
                    "simulated checksum failure".to_string(),
                ))
            } else {
                Ok(())
            }
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    struct RecordingNoUpdateListener {
        calls: AtomicUsize,
    }

    impl SpecsUpdateListener for RecordingNoUpdateListener {
        fn did_receive_specs_update(&self, mut update: SpecsUpdate) -> Result<(), StatsigErr> {
            assert_eq!(
                update.data.read_to_string().unwrap(),
                r#"{"has_updates":false}"#
            );
            self.calls.fetch_add(1, Ordering::SeqCst);
            Ok(())
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    struct RecordingProtobufDeltaListener {
        calls: AtomicUsize,
        expected_data: Vec<u8>,
    }

    impl SpecsUpdateListener for RecordingProtobufDeltaListener {
        fn did_receive_specs_update(&self, mut update: SpecsUpdate) -> Result<(), StatsigErr> {
            assert_eq!(
                update
                    .data
                    .get_header_ref("content-encoding")
                    .map(String::as_str),
                Some("statsig-zstd")
            );
            assert_eq!(
                update
                    .data
                    .get_header_ref("x-deltas-used")
                    .map(String::as_str),
                Some("true")
            );
            assert_eq!(update.data.read_to_bytes().unwrap(), self.expected_data);
            self.calls.fetch_add(1, Ordering::SeqCst);
            Ok(())
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    #[test]
    fn test_text_byte_fetches_do_not_negotiate_protobuf() {
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            None,
            Some("https://example.com/v2/download_config_specs".to_string()),
        );
        let specs_info = SpecsInfo::empty();

        let protobuf_request =
            adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, true);
        assert_eq!(
            protobuf_request
                .query_params
                .as_ref()
                .and_then(|params| params.get("supports_proto"))
                .map(String::as_str),
            Some("true")
        );
        assert_eq!(
            protobuf_request
                .headers
                .as_ref()
                .and_then(|headers| headers.get("statsig-supports-proto"))
                .map(String::as_str),
            Some("true")
        );

        let text_request = adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, false);
        assert!(
            text_request
                .query_params
                .as_ref()
                .is_none_or(|params| !params.contains_key("supports_proto"))
        );
        assert!(text_request.headers.is_none());
    }

    #[test]
    fn test_zstd_advertisement_stays_off_for_legacy_datastore_backed_instances() {
        let options = StatsigOptions {
            data_store: Some(Arc::new(NoopDataStore)),
            enable_dcs_deltas: Some(true),
            ..StatsigOptions::default()
        };
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            Some(&options),
            Some("https://example.com/v2/download_config_specs".to_string()),
        );

        let initial_request =
            adapter.get_request_args(&SpecsInfo::empty(), SpecsSyncTrigger::Manual, true);
        assert_eq!(
            initial_request
                .headers
                .as_ref()
                .and_then(|headers| headers.get("accept-encoding"))
                .map(String::as_str),
            Some("statsig-br, gzip, deflate, br")
        );

        let mut incremental_specs_info = SpecsInfo::empty();
        incremental_specs_info.lcut = Some(1);
        let incremental_request =
            adapter.get_request_args(&incremental_specs_info, SpecsSyncTrigger::Manual, true);
        assert_eq!(
            incremental_request
                .headers
                .as_ref()
                .and_then(|headers| headers.get("accept-encoding"))
                .map(String::as_str),
            Some("statsig-br, gzip, deflate, br")
        );
    }

    #[test]
    fn test_zstd_advertisement_can_be_enabled_for_datastore_backed_instances() {
        let options = StatsigOptions {
            data_store: Some(Arc::new(NoopDataStore)),
            experimental_flags: Some(HashSet::from([ENABLE_DCS_ZSTD_DATASTORE_FLAG.to_string()])),
            ..StatsigOptions::default()
        };
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            Some(&options),
            Some("https://example.com/v2/download_config_specs".to_string()),
        );

        let request = adapter.get_request_args(&SpecsInfo::empty(), SpecsSyncTrigger::Manual, true);
        assert_eq!(
            request
                .headers
                .as_ref()
                .and_then(|headers| headers.get("accept-encoding"))
                .map(String::as_str),
            Some(DCS_ZSTD_ACCEPT_ENCODING)
        );
    }

    #[tokio::test]
    async fn test_default_listener_preserves_legacy_no_update_under_protobuf_headers() {
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            None,
            Some("https://example.com/v2/download_config_specs".to_string()),
        );
        let listener = Arc::new(RecordingNoUpdateListener {
            calls: AtomicUsize::new(0),
        });
        adapter.initialize(listener.clone());

        let result = adapter
            .process_spec_data(
                SpecsSyncTrigger::Initial,
                Ok(NetworkResponse {
                    data: ResponseData::from_bytes_with_headers(
                        br#"{"has_updates":false}"#.to_vec(),
                        Some(HashMap::from([
                            (
                                "content-type".to_string(),
                                "application/octet-stream".to_string(),
                            ),
                            ("content-encoding".to_string(), "statsig-br".to_string()),
                        ])),
                    ),
                    loggable_api: "test-api".to_string(),
                    requested_deltas: false,
                    request_url: "https://example.com/v2/download_config_specs/key.json"
                        .to_string(),
                }),
            )
            .await;

        assert!(result.is_ok());
        assert_eq!(listener.calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn test_default_listener_receives_marker_false_statsig_zstd_delta() {
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            None,
            Some("https://example.com/v2/download_config_specs".to_string()),
        );
        let envelopes = [
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
                ..Default::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::TopLevel as i32,
                data: Some(
                    pb::SpecsTopLevel {
                        has_updates: true,
                        time: 2,
                        rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                        may_have_remote_config_metadata: Some(false),
                        ..Default::default()
                    }
                    .encode_to_vec(),
                ),
                ..Default::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Checksums as i32,
                data: Some(pb::RulesetsChecksums::default().encode_to_vec()),
                ..Default::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Done as i32,
                ..Default::default()
            },
        ];
        let mut encoded = Vec::new();
        for envelope in envelopes {
            envelope.encode_length_delimited(&mut encoded).unwrap();
        }
        let compressed = zstd::stream::encode_all(encoded.as_slice(), 3).unwrap();
        let listener = Arc::new(RecordingProtobufDeltaListener {
            calls: AtomicUsize::new(0),
            expected_data: compressed.clone(),
        });
        adapter.initialize(listener.clone());

        let result = adapter
            .process_spec_data(
                SpecsSyncTrigger::Initial,
                Ok(NetworkResponse {
                    data: ResponseData::from_bytes_with_headers(
                        compressed,
                        Some(HashMap::from([
                            (
                                "content-type".to_string(),
                                "application/octet-stream".to_string(),
                            ),
                            ("content-encoding".to_string(), "statsig-zstd".to_string()),
                            ("x-deltas-used".to_string(), "true".to_string()),
                        ])),
                    ),
                    loggable_api: "test-api".to_string(),
                    requested_deltas: true,
                    request_url: "https://example.com/v2/download_config_specs/key.json"
                        .to_string(),
                }),
            )
            .await;

        assert!(
            result.is_ok(),
            "statsig-zstd delta was rejected: {result:?}"
        );
        assert_eq!(listener.calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn test_disable_accept_deltas_after_checksum_failure() {
        for silent in [false, true] {
            let options = StatsigOptions {
                enable_dcs_deltas: Some(true),
                ..StatsigOptions::default()
            }
            .suppress_diagnostic_output(silent);
            let adapter = StatsigHttpSpecsAdapter::new(
                "secret-key",
                Some(&options),
                Some("https://example.com/v2/download_config_specs".to_string()),
            );
            let specs_info = SpecsInfo::empty();

            let request_before =
                adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, true);
            assert_eq!(
                request_before
                    .query_params
                    .as_ref()
                    .and_then(|p| p.get("accept_deltas"))
                    .map(String::as_str),
                Some("true")
            );
            assert_eq!(
                request_before
                    .headers
                    .as_ref()
                    .and_then(|headers| headers.get("accept-encoding"))
                    .map(String::as_str),
                Some(DCS_ZSTD_ACCEPT_ENCODING)
            );

            let mut incremental_specs_info = SpecsInfo::empty();
            incremental_specs_info.lcut = Some(1);
            let incremental_request =
                adapter.get_request_args(&incremental_specs_info, SpecsSyncTrigger::Manual, true);
            assert_eq!(
                incremental_request
                    .headers
                    .as_ref()
                    .and_then(|headers| headers.get("accept-encoding"))
                    .map(String::as_str),
                Some(DCS_ZSTD_ACCEPT_ENCODING)
            );

            adapter.initialize(Arc::new(ChecksumFailingListener));
            let result = adapter
                .process_spec_data(
                    SpecsSyncTrigger::Initial,
                    Ok(NetworkResponse {
                        data: ResponseData::from_bytes(b"{}".to_vec()),
                        loggable_api: "test-api".to_string(),
                        requested_deltas: true,
                        request_url: "https://example.com/v2/download_config_specs/key.json"
                            .to_string(),
                    }),
                )
                .await;

            assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));

            let request_after =
                adapter.get_request_args(&incremental_specs_info, SpecsSyncTrigger::Manual, true);
            assert!(
                request_after
                    .query_params
                    .as_ref()
                    .is_none_or(|p| !p.contains_key("accept_deltas"))
            );
            assert_eq!(
                request_after
                    .headers
                    .as_ref()
                    .and_then(|headers| headers.get("accept-encoding"))
                    .map(String::as_str),
                Some(DCS_ZSTD_ACCEPT_ENCODING)
            );
        }
    }

    #[tokio::test]
    async fn test_reenable_accept_deltas_after_successful_non_delta_update() {
        for silent in [false, true] {
            let options = StatsigOptions {
                enable_dcs_deltas: Some(true),
                ..StatsigOptions::default()
            }
            .suppress_diagnostic_output(silent);
            let adapter = StatsigHttpSpecsAdapter::new(
                "secret-key",
                Some(&options),
                Some("https://example.com/v2/download_config_specs".to_string()),
            );
            let specs_info = SpecsInfo::empty();

            adapter.initialize(Arc::new(ChecksumFailingThenSuccessListener {
                calls: AtomicUsize::new(0),
            }));

            let first_result = adapter
                .process_spec_data(
                    SpecsSyncTrigger::Initial,
                    Ok(NetworkResponse {
                        data: ResponseData::from_bytes(b"{}".to_vec()),
                        loggable_api: "test-api".to_string(),
                        requested_deltas: true,
                        request_url: "https://example.com/v2/download_config_specs/key.json"
                            .to_string(),
                    }),
                )
                .await;

            assert!(matches!(first_result, Err(StatsigErr::ChecksumFailure(_))));

            let request_after_failure =
                adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, true);
            assert!(
                request_after_failure
                    .query_params
                    .as_ref()
                    .is_none_or(|p| !p.contains_key("accept_deltas"))
            );

            let second_result = adapter
                .process_spec_data(
                    SpecsSyncTrigger::Initial,
                    Ok(NetworkResponse {
                        data: ResponseData::from_bytes(b"{}".to_vec()),
                        loggable_api: "test-api".to_string(),
                        requested_deltas: false,
                        request_url: "https://example.com/v2/download_config_specs/key.json"
                            .to_string(),
                    }),
                )
                .await;

            assert!(second_result.is_ok());

            let request_after_success =
                adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, true);
            assert_eq!(
                request_after_success
                    .query_params
                    .as_ref()
                    .and_then(|p| p.get("accept_deltas"))
                    .map(String::as_str),
                Some("true")
            );
        }
    }

    #[test]
    fn test_checksum_failure_is_not_process_success() {
        let result = Err(StatsigErr::ChecksumFailure(
            "simulated checksum failure".to_string(),
        ));

        assert!(!is_process_success(&result));
        assert!(is_process_success(&Ok(())));
    }

    #[test]
    fn test_fallback_uses_openai_cdn_for_non_default_specs_url() {
        let options = StatsigOptions {
            fallback_to_statsig_api: Some(true),
            ..StatsigOptions::default()
        };
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            Some(&options),
            Some("https://example.com/v2/download_config_specs".to_string()),
        );

        assert_eq!(adapter.fallback_url.as_deref(), Some(DEFAULT_CDN_SPECS_URL));
    }

    #[test]
    fn test_get_response_format_json() {
        let mut headers = HashMap::new();
        headers.insert("content-type".to_string(), "application/json".to_string());
        let data = ResponseData::from_bytes_with_headers(vec![], Some(headers));
        assert!(matches!(
            get_specs_response_format(&data),
            SpecsResponseFormat::Json
        ));
    }

    #[test]
    fn test_get_response_format_plain_text() {
        let mut headers = HashMap::new();
        headers.insert(
            "content-type".to_string(),
            "text/plain; charset=utf-8".to_string(),
        );
        let data = ResponseData::from_bytes_with_headers(vec![], Some(headers));
        assert!(matches!(
            get_specs_response_format(&data),
            SpecsResponseFormat::PlainText
        ));
    }

    #[test]
    fn test_get_response_format_protobuf() {
        let mut headers = HashMap::new();
        headers.insert(
            "content-type".to_string(),
            "application/octet-stream".to_string(),
        );
        headers.insert("content-encoding".to_string(), "statsig-br".to_string());
        let data = ResponseData::from_bytes_with_headers(vec![], Some(headers));
        assert!(matches!(
            get_specs_response_format(&data),
            SpecsResponseFormat::Protobuf
        ));
    }

    #[test]
    fn test_get_response_format_unknown_without_content_type() {
        let data = ResponseData::from_bytes(vec![]);
        assert!(matches!(
            get_specs_response_format(&data),
            SpecsResponseFormat::Unknown
        ));
    }
}
