use super::config_spec_background_sync_metrics::{
    DeltaFallbackReason, DeltaFallbackSource, log_config_sync_full_fallback_count,
    log_config_sync_overall_latency,
};
use super::remote_config_value_hydrator::RemoteConfigValueHydrator;
use super::response_format::{SpecsResponseFormat, get_specs_response_format};
use crate::DEFAULT_INIT_TIMEOUT_MS;
use crate::data_store_interface::ENABLE_DCS_ZSTD_DATASTORE_FLAG;
use crate::networking::{
    DEFAULT_CDN_SPECS_URL, NetworkClient, NetworkError, RequestArgs, ResponseData, api_from_url,
    config_specs_url,
};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::specs_adapter::{SpecsAdapter, SpecsUpdate, SpecsUpdateHydration, SpecsUpdateListener};
use crate::specs_response::spec_types::SpecsResponseNoUpdates;
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
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
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

const TAG: &str = stringify!(StatsigHttpSpecsAdapter);
const STATSIG_NETWORK_FALLBACK_THRESHOLD: u32 = 5;
const DELTA_FALLBACK_REASON_HEADER: &str = "x-statsig-delta-fallback-reason";
const DELTA_FALLBACK_SOURCE_HEADER: &str = "x-statsig-delta-fallback-source";
const INITIAL_DELTA_CURSOR_STATE: &str = "initial";
const INCREMENTAL_DELTA_CURSOR_STATE: &str = "incremental";
const DCS_ZSTD_ACCEPT_ENCODING: &str = "statsig-zstd, statsig-br, gzip, deflate, br";

pub struct StatsigHttpSpecsAdapter {
    listener: RwLock<Option<Arc<dyn SpecsUpdateListener>>>,
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
    background_sync_failure_count: AtomicU32,
}

// OB client -- START
// These types are only for the config_sync_overall.latency observability metric added in this change.

enum NetworkSyncOutcome {
    Success,
    Failure,
}

impl NetworkSyncOutcome {
    fn as_bool(&self) -> bool {
        matches!(self, Self::Success)
    }
}

enum ConfigSyncResponseType {
    Delta,
    Full,
    NoUpdate,
    NetworkError,
}

impl ConfigSyncResponseType {
    fn from_response_data(data: &mut ResponseData) -> Self {
        if is_true_header(data, "x-cache-hit") {
            return Self::NoUpdate;
        }

        if data.get_header_ref("x-deltas-used").is_some() {
            return Self::Delta;
        }

        let response_type = match data.deserialize_into::<SpecsResponseNoUpdates>() {
            Ok(response) if !response.has_updates => Self::NoUpdate,
            _ => Self::Full,
        };
        let _ = data.rewind();
        response_type
    }

    fn as_str(&self) -> &'static str {
        match self {
            Self::Delta => "delta",
            Self::Full => "full",
            Self::NoUpdate => "no_update",
            Self::NetworkError => "network_error",
        }
    }
}

fn is_true_header(data: &ResponseData, key: &str) -> bool {
    data.get_header_ref(key)
        .is_some_and(|value| value.eq_ignore_ascii_case("true"))
}

fn is_process_success(result: &Result<(), StatsigErr>) -> bool {
    result.is_ok()
}

fn get_delta_fallback_reason(data: &ResponseData) -> DeltaFallbackReason {
    DeltaFallbackReason::from_header(
        data.get_header_ref(DELTA_FALLBACK_REASON_HEADER)
            .map(String::as_str),
    )
}

fn get_delta_fallback_source(data: &ResponseData) -> DeltaFallbackSource {
    DeltaFallbackSource::from_header(
        data.get_header_ref(DELTA_FALLBACK_SOURCE_HEADER)
            .map(String::as_str),
    )
}
// OB client -- END

impl StatsigHttpSpecsAdapter {
    #[must_use]
    pub fn new(
        sdk_key: &str,
        options: Option<&StatsigOptions>,
        override_url: Option<String>,
    ) -> Self {
        let default_options = StatsigOptions::default();
        let options_ref = options.unwrap_or(&default_options);

        let init_timeout_ms = options_ref
            .init_timeout_ms
            .unwrap_or(DEFAULT_INIT_TIMEOUT_MS);

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
            background_sync_failure_count: AtomicU32::new(0),
        }
    }

    pub fn force_shutdown(&self) {
        self.shutdown_notify.notify_one();
    }

    pub async fn fetch_specs_from_network(
        &self,
        current_specs_info: SpecsInfo,
        trigger: SpecsSyncTrigger,
    ) -> Result<NetworkResponse, NetworkError> {
        self.fetch_specs_from_network_with_proto_support(current_specs_info, trigger, true)
            .await
    }

    async fn fetch_specs_from_network_with_proto_support(
        &self,
        current_specs_info: SpecsInfo,
        trigger: SpecsSyncTrigger,
        supports_proto: bool,
    ) -> Result<NetworkResponse, NetworkError> {
        let request_args = self.get_request_args(&current_specs_info, trigger, supports_proto);
        let url = request_args.url.clone();
        let requested_deltas = request_args.deltas_enabled;
        match self.handle_specs_request(request_args).await {
            Ok(response) => Ok(NetworkResponse {
                data: response,
                loggable_api: api_from_url(&url),
                requested_deltas,
                request_url: url,
            }),
            Err(e) => Err(e),
        }
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
        let mut response = self
            .fetch_specs_from_network_with_proto_support(current_specs_info, trigger, false)
            .await
            .map_err(StatsigErr::NetworkError)?;
        self.hydrate_network_response(&mut response).await?;
        Ok(response)
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
            retries: match trigger {
                SpecsSyncTrigger::Initial | SpecsSyncTrigger::Manual => 0,
                SpecsSyncTrigger::Background => 3,
            },
            query_params: Some(params),
            deltas_enabled: use_deltas_next_req,
            accept_gzip_response: true,
            diagnostics_key: Some(KeyType::DownloadConfigSpecs),
            timeout_ms,
            headers,
            ..RequestArgs::new()
        }
    }

    async fn handle_fallback_request(
        &self,
        mut request_args: RequestArgs,
    ) -> Result<NetworkResponse, NetworkError> {
        let requested_deltas = request_args.deltas_enabled;
        let fallback_url = match &self.fallback_url {
            Some(url) => config_specs_url(url.as_str()),
            None => {
                return Err(NetworkError::RequestFailed(
                    request_args.url.clone(),
                    None,
                    "No fallback URL".to_string(),
                ));
            }
        };

        request_args.url = fallback_url.clone();

        // TODO logging

        let response = self.handle_specs_request(request_args).await?;
        Ok(NetworkResponse {
            data: response,
            loggable_api: api_from_url(&fallback_url),
            requested_deltas,
            request_url: fallback_url,
        })
    }

    async fn handle_specs_request(
        &self,
        request_args: RequestArgs,
    ) -> Result<ResponseData, NetworkError> {
        let url = request_args.url.clone();
        let response = self.network.get(request_args).await?;
        match response.data {
            Some(data) => Ok(data),
            None => Err(NetworkError::RequestFailed(
                url,
                None,
                response.error.unwrap_or("No data in response".to_string()),
            )),
        }
    }

    fn should_attempt_fallback(
        &self,
        trigger: SpecsSyncTrigger,
        result: &Result<(), StatsigErr>,
    ) -> bool {
        if result.is_ok() || self.fallback_url.is_none() {
            return false;
        }

        if trigger != SpecsSyncTrigger::Background {
            return true;
        }

        let failure_count = self
            .background_sync_failure_count
            .fetch_add(1, Ordering::SeqCst)
            + 1;

        if failure_count.is_multiple_of(STATSIG_NETWORK_FALLBACK_THRESHOLD) {
            return true;
        }

        log_d!(
            TAG,
            "Skipping fallback on background sync failure {}. Retrying fallback every {} failures.",
            failure_count,
            STATSIG_NETWORK_FALLBACK_THRESHOLD
        );

        false
    }

    pub async fn run_background_sync(self: Arc<Self>) {
        let specs_info = match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => listener.get_current_specs_info(),
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
        let mut deltas_used = self.use_deltas_next_request.load(Ordering::SeqCst);
        let mut response = self
            .fetch_specs_from_network(current_specs_info.clone(), trigger)
            .await;
        let mut response_type = response
            .as_mut()
            .map_or(ConfigSyncResponseType::NetworkError, |response| {
                ConfigSyncResponseType::from_response_data(&mut response.data)
            });
        let mut delta_fallback_reason = response
            .as_ref()
            .map_or(DeltaFallbackReason::MissingHeader, |response| {
                get_delta_fallback_reason(&response.data)
            });
        let mut delta_fallback_source = response
            .as_ref()
            .map_or(DeltaFallbackSource::MissingHeader, |response| {
                get_delta_fallback_source(&response.data)
            });
        let (mut source_api, mut response_format, mut network_success) = match &response {
            Ok(response) => (
                response.loggable_api.clone(),
                get_specs_response_format(&response.data),
                NetworkSyncOutcome::Success,
            ),
            Err(_) => (
                api_from_url(&config_specs_url(self.specs_url.as_str())),
                SpecsResponseFormat::Unknown,
                NetworkSyncOutcome::Failure,
            ),
        };
        if let Ok(response) = &response {
            deltas_used = response.requested_deltas;
        }

        let mut result = self.process_spec_data(response).await;

        if self.should_attempt_fallback(trigger, &result) {
            log_d!(TAG, "Falling back to DCS CDN");
            let fallback_args = self.get_request_args(&current_specs_info, trigger, true);
            deltas_used = fallback_args.deltas_enabled;
            let mut response = self.handle_fallback_request(fallback_args).await;
            response_type = response
                .as_mut()
                .map_or(ConfigSyncResponseType::NetworkError, |response| {
                    ConfigSyncResponseType::from_response_data(&mut response.data)
                });
            delta_fallback_reason = response
                .as_ref()
                .map_or(DeltaFallbackReason::MissingHeader, |response| {
                    get_delta_fallback_reason(&response.data)
                });
            delta_fallback_source = response
                .as_ref()
                .map_or(DeltaFallbackSource::MissingHeader, |response| {
                    get_delta_fallback_source(&response.data)
                });
            match &response {
                Ok(response) => {
                    source_api = response.loggable_api.clone();
                    response_format = get_specs_response_format(&response.data);
                    network_success = NetworkSyncOutcome::Success;
                    deltas_used = response.requested_deltas;
                }
                Err(_) => {
                    // Backup request failed, so no successful network payload was returned.
                    if let Some(fallback_url) = self.fallback_url.as_ref() {
                        source_api = api_from_url(&config_specs_url(fallback_url.as_str()));
                    }
                    network_success = NetworkSyncOutcome::Failure;
                }
            }
            result = self.process_spec_data(response).await;
        }

        let process_success = is_process_success(&result);
        log_config_sync_overall_latency(
            &self.ops_stats,
            sync_start_ms,
            source_api.as_str(),
            response_format.as_str(),
            network_success.as_bool(),
            process_success,
            result
                .as_ref()
                .err()
                .map_or_else(String::new, |e| e.to_string()),
            deltas_used,
            response_type.as_str(),
        );
        log_config_sync_full_fallback_count(
            &self.ops_stats,
            source_api.as_str(),
            deltas_used,
            response_type.as_str(),
            delta_fallback_reason,
            delta_fallback_source,
            delta_cursor_state,
        );

        result
    }

    async fn process_spec_data(
        &self,
        response: Result<NetworkResponse, NetworkError>,
    ) -> Result<(), StatsigErr> {
        let resp = response.map_err(StatsigErr::NetworkError)?;
        let requested_deltas = resp.requested_deltas;
        let hydration = SpecsUpdateHydration::new(
            self.remote_config_value_hydrator.clone(),
            self.hydration_source_url(&resp.request_url).to_string(),
        );

        let update = SpecsUpdate {
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
                let err =
                    StatsigErr::LockFailure("Failed to acquire read lock on listener".to_string());
                log_error_to_statsig_and_console!(&self.ops_stats, TAG, err.clone());
                Err(err)
            }
        };
        let result = match listener {
            Ok(listener) => {
                listener
                    .did_receive_specs_update_async(update, Some(hydration))
                    .await
            }
            Err(error) => Err(error),
        };

        if matches!(&result, Err(StatsigErr::ChecksumFailure(_))) {
            let was_deltas_used = self.use_deltas_next_request.swap(false, Ordering::SeqCst);
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
    }

    pub(crate) async fn hydrate_network_response(
        &self,
        response: &mut NetworkResponse,
    ) -> Result<(), StatsigErr> {
        self.remote_config_value_hydrator
            .hydrate_response(
                &mut response.data,
                self.hydration_source_url(&response.request_url),
            )
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
        self.remote_config_value_hydrator
            .hydrate_response(data, source_url)
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
        let specs_info = match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => listener.get_current_specs_info(),
                None => SpecsInfo::empty(),
            },
            None => SpecsInfo::error(),
        };
        self.manually_sync_specs(specs_info, SpecsSyncTrigger::Initial)
            .await
    }

    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        match self
            .listener
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut lock) => *lock = Some(listener),
            None => {
                log_e!(TAG, "Failed to acquire write lock on listener");
            }
        }
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
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
    }

    async fn shutdown(
        &self,
        _timeout: Duration,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.shutdown_notify.notify_one();
        Ok(())
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
            .process_spec_data(Ok(NetworkResponse {
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
                request_url: "https://example.com/v2/download_config_specs/key.json".to_string(),
            }))
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
            .process_spec_data(Ok(NetworkResponse {
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
                request_url: "https://example.com/v2/download_config_specs/key.json".to_string(),
            }))
            .await;

        assert!(
            result.is_ok(),
            "statsig-zstd delta was rejected: {result:?}"
        );
        assert_eq!(listener.calls.load(Ordering::SeqCst), 1);
    }

    #[tokio::test]
    async fn test_disable_accept_deltas_after_checksum_failure() {
        let options = StatsigOptions {
            enable_dcs_deltas: Some(true),
            ..StatsigOptions::default()
        };
        let adapter = StatsigHttpSpecsAdapter::new(
            "secret-key",
            Some(&options),
            Some("https://example.com/v2/download_config_specs".to_string()),
        );
        let specs_info = SpecsInfo::empty();

        let request_before = adapter.get_request_args(&specs_info, SpecsSyncTrigger::Manual, true);
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
            .process_spec_data(Ok(NetworkResponse {
                data: ResponseData::from_bytes(b"{}".to_vec()),
                loggable_api: "test-api".to_string(),
                requested_deltas: true,
                request_url: "https://example.com/v2/download_config_specs/key.json".to_string(),
            }))
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

    #[tokio::test]
    async fn test_reenable_accept_deltas_after_successful_non_delta_update() {
        let options = StatsigOptions {
            enable_dcs_deltas: Some(true),
            ..StatsigOptions::default()
        };
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
            .process_spec_data(Ok(NetworkResponse {
                data: ResponseData::from_bytes(b"{}".to_vec()),
                loggable_api: "test-api".to_string(),
                requested_deltas: true,
                request_url: "https://example.com/v2/download_config_specs/key.json".to_string(),
            }))
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
            .process_spec_data(Ok(NetworkResponse {
                data: ResponseData::from_bytes(b"{}".to_vec()),
                loggable_api: "test-api".to_string(),
                requested_deltas: false,
                request_url: "https://example.com/v2/download_config_specs/key.json".to_string(),
            }))
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
    fn test_config_sync_response_type_delta() {
        let mut headers = HashMap::new();
        headers.insert("x-deltas-used".to_string(), "true".to_string());
        let mut data = ResponseData::from_bytes_with_headers(
            b"{\"has_updates\": false}".to_vec(),
            Some(headers),
        );

        let response_type = ConfigSyncResponseType::from_response_data(&mut data);

        assert_eq!(response_type.as_str(), "delta");
    }

    #[test]
    fn test_config_sync_response_type_no_update() {
        let mut data = ResponseData::from_bytes(b"{\"has_updates\": false}".to_vec());

        let response_type = ConfigSyncResponseType::from_response_data(&mut data);

        assert_eq!(response_type.as_str(), "no_update");
        let response = data.deserialize_into::<SpecsResponseNoUpdates>().unwrap();
        assert!(!response.has_updates);
    }

    #[test]
    fn test_config_sync_response_type_no_update_with_delta_header() {
        let mut headers = HashMap::new();
        headers.insert("x-cache-hit".to_string(), "true".to_string());
        headers.insert("x-deltas-used".to_string(), "true".to_string());
        let mut data = ResponseData::from_bytes_with_headers(
            b"{\"has_updates\": false}".to_vec(),
            Some(headers),
        );

        let response_type = ConfigSyncResponseType::from_response_data(&mut data);

        assert_eq!(response_type.as_str(), "no_update");
    }

    #[test]
    fn test_config_sync_response_type_full() {
        let mut data = ResponseData::from_bytes(b"{\"has_updates\": true}".to_vec());

        let response_type = ConfigSyncResponseType::from_response_data(&mut data);

        assert_eq!(response_type.as_str(), "full");
    }

    #[test]
    fn test_config_sync_response_type_full_for_non_json_payload() {
        let mut data = ResponseData::from_bytes(vec![0, 1, 2]);

        let response_type = ConfigSyncResponseType::from_response_data(&mut data);

        assert_eq!(response_type.as_str(), "full");
        let mut first_byte = [1];
        data.get_stream_mut().read_exact(&mut first_byte).unwrap();
        assert_eq!(first_byte, [0]);
    }

    #[test]
    fn test_delta_fallback_headers_parse_to_typed_values() {
        let data = ResponseData::from_bytes_with_headers(
            vec![],
            Some(HashMap::from([
                (
                    DELTA_FALLBACK_REASON_HEADER.to_string(),
                    "before_earliest_lcut".to_string(),
                ),
                (
                    DELTA_FALLBACK_SOURCE_HEADER.to_string(),
                    "local_compute".to_string(),
                ),
            ])),
        );

        assert_eq!(
            get_delta_fallback_reason(&data),
            DeltaFallbackReason::BeforeEarliestLcut
        );
        assert_eq!(
            get_delta_fallback_source(&data),
            DeltaFallbackSource::LocalCompute
        );
    }

    #[test]
    fn test_delta_fallback_headers_preserve_missing_and_invalid() {
        let missing = ResponseData::from_bytes(vec![]);
        assert_eq!(
            get_delta_fallback_reason(&missing),
            DeltaFallbackReason::MissingHeader
        );
        assert_eq!(
            get_delta_fallback_source(&missing),
            DeltaFallbackSource::MissingHeader
        );

        let invalid = ResponseData::from_bytes_with_headers(
            vec![],
            Some(HashMap::from([
                (
                    DELTA_FALLBACK_REASON_HEADER.to_string(),
                    "free_form_reason".to_string(),
                ),
                (
                    DELTA_FALLBACK_SOURCE_HEADER.to_string(),
                    "raw-unbounded-source".to_string(),
                ),
            ])),
        );
        assert_eq!(
            get_delta_fallback_reason(&invalid),
            DeltaFallbackReason::InvalidHeader
        );
        assert_eq!(
            get_delta_fallback_source(&invalid),
            DeltaFallbackSource::InvalidHeader
        );
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
