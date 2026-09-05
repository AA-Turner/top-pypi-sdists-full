use super::remote_config_value_hydrator::RemoteConfigValueHydrator;
use super::{
    SpecsAdapter, SpecsCursorUpdate, SpecsInfo, SpecsSource, SpecsUpdate, SpecsUpdateHydration,
    SpecsUpdateListener,
};
use crate::hashing::ahash_str;
use crate::networking::{DEFAULT_CDN_SPECS_URL, NetworkClient, ResponseData};
use crate::observability::ops_stats::{
    OPS_STATS, OpsStatsForInstance, with_scoped_hydration_observability,
};
use crate::{ObservabilityClient, StatsigErr, StatsigOptions, StatsigRuntime, log_e, log_w};
use async_trait::async_trait;
use chrono::Utc;
use parking_lot::RwLock;
use std::any::Any;
use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, OnceLock};
use std::time::{Duration, Instant};
use tokio::sync::Notify;
use tokio::time::sleep;

const TAG: &str = stringify!(ScopedSourceSpecsAdapter);
const SOURCE_NAME: &str = "ScopedConfigSource";
const SYNC_INTERVAL: Duration = Duration::from_secs(10);
const LEGACY_FETCH_METRIC: &str = "statsig.sdk.evaluation.snapshot.fetch.count";
const LEGACY_UPDATE_METRIC: &str = "statsig.sdk.evaluation.snapshot.update.count";
const LEGACY_UPDATE_DURATION_METRIC: &str = "statsig.sdk.evaluation.snapshot.update.duration_ms";
const LEGACY_UPDATE_PAYLOAD_METRIC: &str =
    "statsig.sdk.evaluation.snapshot.update.encoded_payload_bytes";
const ACTIVE_UPDATE_METRIC: &str = "statsig.sdk.scoped_snapshot.update.active";

static ACTIVE_SNAPSHOT_UPDATES: AtomicUsize = AtomicUsize::new(0);

struct ActiveSnapshotUpdateGuard {
    observer: Arc<dyn ObservabilityClient>,
}

impl ActiveSnapshotUpdateGuard {
    fn new(observer: Arc<dyn ObservabilityClient>) -> Self {
        let active = ACTIVE_SNAPSHOT_UPDATES.fetch_add(1, Ordering::Relaxed) + 1;
        observer.gauge(ACTIVE_UPDATE_METRIC.to_string(), active as f64, None);
        Self { observer }
    }
}

impl Drop for ActiveSnapshotUpdateGuard {
    fn drop(&mut self) {
        let active = ACTIVE_SNAPSHOT_UPDATES.fetch_sub(1, Ordering::Relaxed) - 1;
        self.observer
            .gauge(ACTIVE_UPDATE_METRIC.to_string(), active as f64, None);
    }
}

#[derive(Default)]
struct ScopedRefreshTelemetry {
    metadata_fetch: Option<Duration>,
    payload_fetch: Option<Duration>,
    decode_publish: Option<Duration>,
    payload_bytes: Option<u64>,
    response_type: Option<&'static str>,
    encoding: Option<&'static str>,
    change_reason: Option<&'static str>,
    used_fallback: bool,
}

impl ScopedRefreshTelemetry {
    fn record_payload(&mut self, payload: &ResponseData, used_fallback: bool) {
        self.payload_bytes = payload
            .get_header_ref("content-length")
            .and_then(|length| length.parse().ok());
        let is_protobuf = payload
            .get_header_ref("content-type")
            .is_some_and(|content_type| content_type == "application/octet-stream")
            || payload
                .get_header_ref("content-encoding")
                .is_some_and(|encoding| encoding == "statsig-br");
        self.response_type = Some(if is_protobuf { "protobuf" } else { "json" });
        self.encoding = Some(if is_protobuf { "brotli" } else { "identity" });
        self.used_fallback |= used_fallback;
    }

    fn add_duration(duration: &mut Option<Duration>, started: Option<Instant>) {
        if let Some(started) = started {
            *duration = Some(duration.unwrap_or_default() + started.elapsed());
        }
    }

    fn tags(&self, result: &str, scope_class: Option<&'static str>) -> HashMap<String, String> {
        let mut tags = HashMap::from([("result".to_string(), result.to_string())]);
        if let Some(scope_class) = scope_class {
            tags.insert("scope_class".to_string(), scope_class.to_string());
        }
        if let Some(change_reason) = self.change_reason {
            tags.insert("change_reason".to_string(), change_reason.to_string());
        }
        if let Some(response_type) = self.response_type {
            tags.insert("response_type".to_string(), response_type.to_string());
            tags.insert("fallback".to_string(), self.used_fallback.to_string());
        }
        if let Some(encoding) = self.encoding {
            tags.insert("encoding".to_string(), encoding.to_string());
        }
        tags
    }

    fn legacy_update_tags(&self, scope_class: Option<&'static str>) -> HashMap<String, String> {
        let initial_load = self.change_reason == Some("initial_load");
        let change_reason = match self.change_reason {
            Some("checksum_repair") => "checksum_changed",
            Some("checksum_changed") => "lcut_and_checksum_changed",
            Some(reason) => reason,
            None => "unknown",
        };
        let response_type = match self.response_type {
            Some("json") => "uncompressed_json",
            Some("protobuf") => "brotli_protobuf",
            _ => "unknown",
        };
        let mut tags = HashMap::from([
            (
                "update_kind".to_string(),
                if initial_load {
                    "initial_load"
                } else {
                    "refresh"
                }
                .to_string(),
            ),
            ("change_reason".to_string(), change_reason.to_string()),
            ("response_type".to_string(), response_type.to_string()),
            (
                "used_json_fallback".to_string(),
                self.used_fallback.to_string(),
            ),
        ]);
        if let Some(scope_class) = scope_class {
            tags.insert("scope_class".to_string(), scope_class.to_string());
        }
        tags
    }
}

/// Version metadata and the source-private token needed to fetch the same payload.
#[doc(hidden)]
pub struct ScopedConfigMetadata {
    pub lcut: u64,
    pub checksum: String,
    token: Arc<dyn Any + Send + Sync>,
}

impl ScopedConfigMetadata {
    pub fn new<T: Any + Send + Sync>(lcut: u64, checksum: String, token: T) -> Self {
        Self {
            lcut,
            checksum,
            token: Arc::new(token),
        }
    }

    pub fn token<T: Any>(&self) -> Option<&T> {
        self.token.as_ref().downcast_ref::<T>()
    }
}

/// Supplies scoped metadata and payload I/O while the SDK owns synchronization.
#[doc(hidden)]
#[async_trait]
pub trait ScopedConfigSource: Send + Sync {
    /// Returns a bounded source category for operational telemetry without exposing its identity.
    fn observability_scope_class(&self) -> Option<&'static str> {
        None
    }

    /// Returns the host-approved origin for resolving remote configuration values.
    fn trusted_hydration_source_url(&self) -> Option<&str> {
        None
    }

    async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr>;

    async fn fetch_metadata_with_cursor(
        &self,
        _current: &SpecsInfo,
    ) -> Result<ScopedConfigMetadata, StatsigErr> {
        self.fetch_metadata().await
    }

    async fn fetch_payload(
        &self,
        metadata: &ScopedConfigMetadata,
    ) -> Result<ResponseData, StatsigErr>;

    async fn fetch_fallback_payload(
        &self,
        _metadata: &ScopedConfigMetadata,
    ) -> Result<Option<ResponseData>, StatsigErr> {
        Ok(None)
    }
}

/// Polls a scoped source without fetching unchanged configuration payloads.
#[doc(hidden)]
pub struct ScopedSourceSpecsAdapter {
    source: Arc<dyn ScopedConfigSource>,
    scope_identity: String,
    hydration_source_url: String,
    listener: RwLock<Option<Arc<dyn SpecsUpdateListener>>>,
    shutdown_notify: Arc<Notify>,
    observability: OnceLock<Arc<dyn ObservabilityClient>>,
}

impl ScopedSourceSpecsAdapter {
    pub fn new(source: Arc<dyn ScopedConfigSource>, scope_identity: &str) -> Self {
        let hydration_source_url = source
            .trusted_hydration_source_url()
            .unwrap_or(DEFAULT_CDN_SPECS_URL)
            .to_string();
        Self {
            source,
            scope_identity: scope_identity.to_string(),
            hydration_source_url,
            listener: RwLock::new(None),
            shutdown_notify: Arc::new(Notify::new()),
            observability: OnceLock::new(),
        }
    }

    pub(crate) fn bind_observability_client(&self, client: Arc<dyn ObservabilityClient>) {
        let _ = self.observability.set(client);
    }

    fn listener(&self) -> Result<Arc<dyn SpecsUpdateListener>, StatsigErr> {
        self.listener
            .try_read_for(Duration::from_secs(5))
            .ok_or_else(|| StatsigErr::LockFailure("Failed to lock scoped source listener".into()))?
            .as_ref()
            .cloned()
            .ok_or_else(|| StatsigErr::UnstartedAdapter("Scoped source listener not set".into()))
    }

    async fn sync(&self) -> Result<(), StatsigErr> {
        let started = Instant::now();
        let mut telemetry = self
            .observability
            .get()
            .map(|_| ScopedRefreshTelemetry::default());
        let result = self.sync_impl(&mut telemetry).await;
        if let (Some(observer), Some(telemetry)) = (self.observability.get(), telemetry) {
            let scope_class = self.source.observability_scope_class();
            let legacy_result = match &result {
                Ok(true) => "updated",
                Ok(false) => "unchanged",
                Err(_) if telemetry.change_reason.is_some() => "payload_error",
                Err(_) => "metadata_error",
            };
            let mut legacy_fetch_tags =
                HashMap::from([("result".to_string(), legacy_result.to_string())]);
            if let Some(scope_class) = scope_class {
                legacy_fetch_tags.insert("scope_class".to_string(), scope_class.to_string());
            }
            observer.increment(
                LEGACY_FETCH_METRIC.to_string(),
                1.0,
                Some(legacy_fetch_tags),
            );
            let status = match &result {
                Ok(true) => Some("updated"),
                Ok(false) => None,
                Err(_) => Some("error"),
            };
            if let Some(status) = status {
                let tags = telemetry.tags(status, scope_class);
                let legacy_update_tags =
                    (status == "updated").then(|| telemetry.legacy_update_tags(scope_class));
                observer.increment(
                    "statsig.sdk.scoped_snapshot.refresh.count".to_string(),
                    1.0,
                    Some(tags.clone()),
                );
                observer.dist(
                    "statsig.sdk.scoped_snapshot.refresh.duration_ms".to_string(),
                    started.elapsed().as_secs_f64() * 1_000.0,
                    Some(tags.clone()),
                );
                if let Some(legacy_tags) = legacy_update_tags.as_ref() {
                    observer.increment(
                        LEGACY_UPDATE_METRIC.to_string(),
                        1.0,
                        Some(legacy_tags.clone()),
                    );
                    let mut total_tags = legacy_tags.clone();
                    total_tags.insert("phase".to_string(), "total".to_string());
                    observer.dist(
                        LEGACY_UPDATE_DURATION_METRIC.to_string(),
                        started.elapsed().as_secs_f64() * 1_000.0,
                        Some(total_tags),
                    );
                }
                for (phase, duration) in [
                    ("metadata_fetch", telemetry.metadata_fetch),
                    ("payload_fetch", telemetry.payload_fetch),
                    ("decode_publish", telemetry.decode_publish),
                ] {
                    if let Some(duration) = duration {
                        let mut phase_tags = tags.clone();
                        phase_tags.insert("phase".to_string(), phase.to_string());
                        observer.dist(
                            "statsig.sdk.scoped_snapshot.refresh.phase.duration_ms".to_string(),
                            duration.as_secs_f64() * 1_000.0,
                            Some(phase_tags),
                        );
                        if let Some(legacy_tags) = legacy_update_tags.as_ref() {
                            let mut legacy_phase_tags = legacy_tags.clone();
                            let legacy_phase = if phase == "decode_publish" {
                                "decode"
                            } else {
                                phase
                            };
                            legacy_phase_tags.insert("phase".to_string(), legacy_phase.to_string());
                            observer.dist(
                                LEGACY_UPDATE_DURATION_METRIC.to_string(),
                                duration.as_secs_f64() * 1_000.0,
                                Some(legacy_phase_tags),
                            );
                        }
                    }
                }
                if let ("updated", Some(bytes)) = (status, telemetry.payload_bytes) {
                    observer.dist(
                        "statsig.sdk.scoped_snapshot.refresh.payload_bytes".to_string(),
                        bytes as f64,
                        None,
                    );
                    if let Some(legacy_tags) = legacy_update_tags {
                        observer.dist(
                            LEGACY_UPDATE_PAYLOAD_METRIC.to_string(),
                            bytes as f64,
                            Some(legacy_tags),
                        );
                    }
                }
            }
        }
        result.map(|_| ())
    }

    async fn sync_impl(
        &self,
        telemetry: &mut Option<ScopedRefreshTelemetry>,
    ) -> Result<bool, StatsigErr> {
        let listener = self.listener()?;
        let current = listener.get_current_specs_info();
        let metadata_started = telemetry.as_ref().map(|_| Instant::now());
        let metadata = self.source.fetch_metadata_with_cursor(&current).await;
        if let Some(telemetry) = telemetry.as_mut() {
            ScopedRefreshTelemetry::add_duration(&mut telemetry.metadata_fetch, metadata_started);
        }
        let metadata = metadata?;

        if current.checksum.as_deref() == Some(metadata.checksum.as_str()) {
            if current.lcut.is_none_or(|lcut| metadata.lcut > lcut) {
                listener.did_advance_specs_cursor(SpecsCursorUpdate {
                    lcut: metadata.lcut,
                    checksum: metadata.checksum,
                    source: SpecsSource::Adapter(SOURCE_NAME.to_string()),
                    source_api: Some(SOURCE_NAME.to_string()),
                })?;
            }
            return Ok(false);
        }

        if current.lcut.is_some_and(|lcut| metadata.lcut < lcut) {
            return Ok(false);
        }

        if let Some(telemetry) = telemetry.as_mut() {
            telemetry.change_reason = Some(if current.checksum.is_none() {
                "initial_load"
            } else if current.lcut == Some(metadata.lcut) {
                "checksum_repair"
            } else {
                "checksum_changed"
            });
        }
        let _active_update = self
            .observability
            .get()
            .cloned()
            .map(ActiveSnapshotUpdateGuard::new);
        let payload_started = telemetry.as_ref().map(|_| Instant::now());
        let payload = self.source.fetch_payload(&metadata).await;
        if let Some(telemetry) = telemetry.as_mut() {
            ScopedRefreshTelemetry::add_duration(&mut telemetry.payload_fetch, payload_started);
        }
        let update_result = match payload {
            Ok(payload) => {
                if let Some(telemetry) = telemetry.as_mut() {
                    telemetry.record_payload(&payload, false);
                }
                let decode_started = telemetry.as_ref().map(|_| Instant::now());
                let result = self
                    .publish_payload(listener.as_ref(), payload, &metadata)
                    .await;
                if let Some(telemetry) = telemetry.as_mut() {
                    ScopedRefreshTelemetry::add_duration(
                        &mut telemetry.decode_publish,
                        decode_started,
                    );
                }
                result
            }
            Err(error) => Err(error),
        };
        if let Err(error) = update_result {
            let fallback_started = telemetry.as_ref().map(|_| Instant::now());
            let fallback = self.source.fetch_fallback_payload(&metadata).await;
            if let Some(telemetry) = telemetry.as_mut() {
                ScopedRefreshTelemetry::add_duration(
                    &mut telemetry.payload_fetch,
                    fallback_started,
                );
            }
            let Some(fallback) = fallback? else {
                return Err(error);
            };
            if let Some(telemetry) = telemetry.as_mut() {
                telemetry.record_payload(&fallback, true);
            }
            log_w!(
                TAG,
                "Preferred scoped configuration payload failed; retrying fallback: {}",
                error
            );
            let fallback_decode_started = telemetry.as_ref().map(|_| Instant::now());
            let fallback_result = self
                .publish_payload(listener.as_ref(), fallback, &metadata)
                .await;
            if let Some(telemetry) = telemetry.as_mut() {
                ScopedRefreshTelemetry::add_duration(
                    &mut telemetry.decode_publish,
                    fallback_decode_started,
                );
            }
            fallback_result?;
        }

        let applied = listener.get_current_specs_info();
        if applied.checksum.as_deref() == Some(metadata.checksum.as_str())
            && applied.lcut.is_some_and(|lcut| metadata.lcut > lcut)
        {
            listener.did_advance_specs_cursor(SpecsCursorUpdate {
                lcut: metadata.lcut,
                checksum: metadata.checksum,
                source: SpecsSource::Adapter(SOURCE_NAME.to_string()),
                source_api: Some(SOURCE_NAME.to_string()),
            })?;
        }

        Ok(true)
    }

    async fn publish_payload(
        &self,
        listener: &dyn SpecsUpdateListener,
        payload: ResponseData,
        metadata: &ScopedConfigMetadata,
    ) -> Result<(), StatsigErr> {
        let hydration = SpecsUpdateHydration::new(
            Self::capability_hydrator(),
            self.hydration_source_url.clone(),
        );
        with_scoped_hydration_observability(
            self.observability.get().cloned(),
            listener.did_receive_specs_update_async(
                Self::specs_update(payload, metadata),
                Some(hydration),
            ),
        )
        .await?;
        Self::validate_published_specs(listener, metadata)
    }

    fn capability_hydrator() -> Arc<RemoteConfigValueHydrator> {
        static HYDRATOR: OnceLock<Arc<RemoteConfigValueHydrator>> = OnceLock::new();
        const INSTANCE_ID: &str = "scoped:remote-value-capability";

        Arc::clone(HYDRATOR.get_or_init(|| {
            let observer = Arc::new(OpsStatsForInstance::disabled());
            let _disabled_observability =
                OPS_STATS.enter_instance_scope(INSTANCE_ID, Some(Arc::clone(&observer)));
            let options = StatsigOptions {
                sdk_instance_id: Some(INSTANCE_ID.to_string()),
                disable_network: Some(false),
                disable_disk_access: Some(true),
                ..StatsigOptions::default()
            };
            let network = Arc::new(NetworkClient::new(INSTANCE_ID, None, Some(&options)));
            Arc::new(RemoteConfigValueHydrator::new_with_ops_stats(
                network, observer,
            ))
        }))
    }

    fn validate_published_specs(
        listener: &dyn SpecsUpdateListener,
        metadata: &ScopedConfigMetadata,
    ) -> Result<(), StatsigErr> {
        let applied = listener.get_current_specs_info();
        if applied.checksum.as_deref() != Some(metadata.checksum.as_str()) {
            return Err(StatsigErr::ChecksumFailure(
                "Scoped configuration payload checksum does not match its metadata".to_string(),
            ));
        }
        match applied.lcut {
            Some(lcut) if lcut > metadata.lcut => {
                return Err(StatsigErr::ChecksumFailure(
                    "Scoped configuration payload LCUT is newer than its metadata".to_string(),
                ));
            }
            None => {
                return Err(StatsigErr::InitializationError(
                    "Scoped configuration payload did not publish a ready snapshot".to_string(),
                ));
            }
            Some(_) => {}
        }
        Ok(())
    }

    fn specs_update(mut data: ResponseData, metadata: &ScopedConfigMetadata) -> SpecsUpdate {
        data.set_scoped_expected_checksum(&metadata.checksum);
        data.set_scoped_expected_lcut(metadata.lcut);
        SpecsUpdate {
            data,
            source: SpecsSource::Adapter(SOURCE_NAME.to_string()),
            received_at: Utc::now().timestamp_millis() as u64,
            source_api: Some(SOURCE_NAME.to_string()),
            has_updates: None,
        }
    }

    fn first_sync_delay(&self) -> Duration {
        static PROCESS_SALT: OnceLock<String> = OnceLock::new();
        let salt = PROCESS_SALT.get_or_init(|| uuid::Uuid::new_v4().to_string());
        let interval_ms = SYNC_INTERVAL.as_millis() as u64;
        let minimum_delay_ms = interval_ms / 2;
        let jitter_window_ms = interval_ms - minimum_delay_ms + 1;
        Duration::from_millis(
            minimum_delay_ms
                + (ahash_str(&format!("{salt}:{}", self.scope_identity)) % jitter_window_ms),
        )
    }
}

#[async_trait]
impl SpecsAdapter for ScopedSourceSpecsAdapter {
    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        match self.listener.try_write_for(Duration::from_secs(5)) {
            Some(mut current) => *current = Some(listener),
            None => log_e!(TAG, "Failed to lock scoped source listener"),
        }
    }

    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.sync().await
    }

    async fn shutdown(
        &self,
        _timeout: Duration,
        _statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.shutdown_notify.notify_waiters();
        Ok(())
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        let weak_self = Arc::downgrade(&self);
        let shutdown_notify = Arc::clone(&self.shutdown_notify);
        let mut next_delay = self.first_sync_delay();

        statsig_runtime.spawn(
            "scoped_source_specs_sync",
            move |runtime_shutdown| async move {
                loop {
                    tokio::select! {
                        () = sleep(next_delay) => {
                            next_delay = SYNC_INTERVAL;
                            let Some(adapter) = weak_self.upgrade() else {
                                break;
                            };
                            if let Err(error) = adapter.sync().await {
                                log_e!(TAG, "Scoped source background sync failed: {}", error);
                            }
                        }
                        () = runtime_shutdown.notified() => break,
                        () = shutdown_notify.notified() => break,
                    }
                }
            },
        )?;

        Ok(())
    }

    fn get_type_name(&self) -> String {
        TAG.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::{
        SYNC_INTERVAL, ScopedConfigMetadata, ScopedConfigSource, ScopedSourceSpecsAdapter,
    };
    use crate::interned_string::InternedString;
    use crate::networking::ResponseData;
    use crate::observability::ops_stats::OPS_STATS;
    use crate::sdk_event_emitter::SdkEventEmitter;
    use crate::specs_response::spec_types::SpecsResponseFull;
    use crate::statsig_options::SnapshotEvaluationSessionInitOptions;
    use crate::{
        ObservabilityClient, OpsStatsEventObserver, SpecStore, SpecsAdapter, SpecsCursorUpdate,
        SpecsInfo, SpecsSource, SpecsUpdate, SpecsUpdateListener, StatsigErr, StatsigRuntime,
    };
    use async_trait::async_trait;
    use parking_lot::Mutex;
    use sha2::{Digest, Sha256};
    use std::collections::HashMap;
    use std::sync::Arc;
    use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    struct CountingSource {
        lcut: u64,
        checksum: String,
        scope_class: Option<&'static str>,
        payload_fetches: AtomicUsize,
        fallback_fetches: AtomicUsize,
        has_fallback: bool,
        include_content_length: bool,
        content_encoding: Option<&'static str>,
    }

    struct CursorRecordingSource {
        source: Arc<CountingSource>,
        cursors: Mutex<Vec<SpecsInfo>>,
    }

    #[async_trait]
    impl ScopedConfigSource for CountingSource {
        fn observability_scope_class(&self) -> Option<&'static str> {
            self.scope_class
        }

        async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
            Ok(ScopedConfigMetadata::new(
                self.lcut,
                self.checksum.clone(),
                "source-private-token".to_string(),
            ))
        }

        async fn fetch_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<ResponseData, StatsigErr> {
            assert_eq!(
                metadata.token::<String>().map(String::as_str),
                Some("source-private-token")
            );
            self.payload_fetches.fetch_add(1, Ordering::Relaxed);
            let payload = format!(
                r#"{{"has_updates":true,"time":{},"checksum":"{}"}}"#,
                self.lcut, self.checksum
            )
            .into_bytes();
            let mut headers = HashMap::new();
            if self.include_content_length {
                headers.insert("content-length".to_string(), payload.len().to_string());
            }
            if let Some(encoding) = self.content_encoding {
                headers.insert("content-encoding".to_string(), encoding.to_string());
            }
            let headers = (!headers.is_empty()).then_some(headers);
            Ok(ResponseData::from_bytes_with_headers(payload, headers))
        }

        async fn fetch_fallback_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<Option<ResponseData>, StatsigErr> {
            self.fallback_fetches.fetch_add(1, Ordering::Relaxed);
            Ok(self.has_fallback.then(|| {
                ResponseData::from_bytes(
                    format!(
                        r#"{{"has_updates":true,"time":{},"checksum":"{}"}}"#,
                        self.lcut, metadata.checksum
                    )
                    .into_bytes(),
                )
            }))
        }
    }

    #[async_trait]
    impl ScopedConfigSource for CursorRecordingSource {
        async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
            Err(StatsigErr::InvalidOperation(
                "cursor-aware metadata fetch was not used".to_string(),
            ))
        }

        async fn fetch_metadata_with_cursor(
            &self,
            current: &SpecsInfo,
        ) -> Result<ScopedConfigMetadata, StatsigErr> {
            self.cursors.lock().push(current.clone());
            self.source.fetch_metadata().await
        }

        async fn fetch_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<ResponseData, StatsigErr> {
            self.source.fetch_payload(metadata).await
        }
    }

    struct FailingPreferredSource(Arc<CountingSource>);

    struct FutureLcutSource(Arc<CountingSource>);

    struct RemotePayloadSource {
        payload: Arc<[u8]>,
        trusted_source_url: String,
    }

    fn remote_payload(download_url: &str, digest: &str, byte_length: usize) -> Arc<[u8]> {
        Arc::from(
            serde_json::to_vec(&serde_json::json!({
                "dynamic_configs": {
                    "remote_config": {
                        "type": "dynamic_config",
                        "salt": "salt",
                        "enabled": true,
                        "defaultValue": { "value": download_url },
                        "remoteConfigMetadata": {
                            "sha256": digest,
                            "byteLength": byte_length,
                            "contentType": "application/json",
                            "compression": "none"
                        },
                        "rules": [],
                        "idType": "userID",
                        "entity": "dynamic_config"
                    }
                },
                "feature_gates": {},
                "experiment_to_layer": {},
                "layer_configs": {},
                "condition_map": {},
                "has_updates": true,
                "time": 123,
                "checksum": "hydrated-checksum",
                "company_id": "company",
                "response_format": "dcs-v2"
            }))
            .expect("remote configuration snapshot should serialize"),
        )
    }

    #[async_trait]
    impl ScopedConfigSource for RemotePayloadSource {
        fn trusted_hydration_source_url(&self) -> Option<&str> {
            Some(&self.trusted_source_url)
        }

        async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
            Ok(ScopedConfigMetadata::new(
                123,
                "hydrated-checksum".to_string(),
                (),
            ))
        }

        async fn fetch_payload(
            &self,
            _metadata: &ScopedConfigMetadata,
        ) -> Result<ResponseData, StatsigErr> {
            Ok(ResponseData::from_shared_bytes_with_headers(
                Arc::clone(&self.payload),
                None,
            ))
        }
    }

    #[async_trait]
    impl ScopedConfigSource for FailingPreferredSource {
        async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
            self.0.fetch_metadata().await
        }

        async fn fetch_payload(
            &self,
            _metadata: &ScopedConfigMetadata,
        ) -> Result<ResponseData, StatsigErr> {
            self.0.payload_fetches.fetch_add(1, Ordering::Relaxed);
            Err(StatsigErr::DataStoreFailure(
                "preferred payload transport failed".to_string(),
            ))
        }

        async fn fetch_fallback_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<Option<ResponseData>, StatsigErr> {
            self.0.fetch_fallback_payload(metadata).await
        }
    }

    #[async_trait]
    impl ScopedConfigSource for FutureLcutSource {
        async fn fetch_metadata(&self) -> Result<ScopedConfigMetadata, StatsigErr> {
            self.0.fetch_metadata().await
        }

        async fn fetch_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<ResponseData, StatsigErr> {
            self.0.fetch_payload(metadata).await?;
            Ok(full_specs_payload(metadata.lcut + 1, &metadata.checksum))
        }

        async fn fetch_fallback_payload(
            &self,
            metadata: &ScopedConfigMetadata,
        ) -> Result<Option<ResponseData>, StatsigErr> {
            Ok(self
                .0
                .fetch_fallback_payload(metadata)
                .await?
                .map(|_| full_specs_payload(metadata.lcut, &metadata.checksum)))
        }
    }

    struct RecordingListener {
        current: Mutex<SpecsInfo>,
        updates: AtomicUsize,
        cursor_updates: AtomicUsize,
        reject_next_update: AtomicBool,
        ignore_next_update: AtomicBool,
    }

    type RecordedTags = Option<HashMap<String, String>>;
    type RecordedDistribution = (String, f64, RecordedTags);

    #[derive(Default)]
    struct RecordingObserver {
        increments: Mutex<Vec<(String, RecordedTags)>>,
        gauges: Mutex<Vec<RecordedDistribution>>,
        distributions: Mutex<Vec<RecordedDistribution>>,
    }

    impl ObservabilityClient for RecordingObserver {
        fn init(&self) {}

        fn increment(&self, name: String, _value: f64, tags: Option<HashMap<String, String>>) {
            self.increments.lock().push((name, tags));
        }

        fn gauge(&self, name: String, value: f64, tags: Option<HashMap<String, String>>) {
            self.gauges.lock().push((name, value, tags));
        }

        fn dist(&self, name: String, value: f64, tags: Option<HashMap<String, String>>) {
            self.distributions.lock().push((name, value, tags));
        }

        fn error(&self, _tag: String, _error: String) {}

        fn should_enable_high_cardinality_for_this_tag(&self, _tag: String) -> Option<bool> {
            Some(false)
        }

        fn to_ops_stats_event_observer(self: Arc<Self>) -> Arc<dyn OpsStatsEventObserver> {
            self
        }
    }

    impl RecordingListener {
        fn new(lcut: Option<u64>, checksum: Option<&str>) -> Self {
            Self {
                current: Mutex::new(SpecsInfo {
                    lcut,
                    checksum: checksum.map(str::to_string),
                    source: SpecsSource::NoValues,
                    source_api: None,
                }),
                updates: AtomicUsize::new(0),
                cursor_updates: AtomicUsize::new(0),
                reject_next_update: AtomicBool::new(false),
                ignore_next_update: AtomicBool::new(false),
            }
        }
    }

    impl SpecsUpdateListener for RecordingListener {
        fn did_receive_specs_update(&self, mut update: SpecsUpdate) -> Result<(), StatsigErr> {
            self.updates.fetch_add(1, Ordering::Relaxed);
            if self.reject_next_update.swap(false, Ordering::Relaxed) {
                return Err(StatsigErr::ProtobufParseError(
                    "SpecsResponse".to_string(),
                    "invalid preferred payload".to_string(),
                ));
            }
            if self.ignore_next_update.swap(false, Ordering::Relaxed) {
                return Ok(());
            }

            let payload = update.data.deserialize_into::<serde_json::Value>()?;
            let mut current = self.current.lock();
            current.lcut = payload.get("time").and_then(serde_json::Value::as_u64);
            current.checksum = payload
                .get("checksum")
                .and_then(serde_json::Value::as_str)
                .map(str::to_string);
            Ok(())
        }

        fn did_advance_specs_cursor(&self, update: SpecsCursorUpdate) -> Result<(), StatsigErr> {
            self.cursor_updates.fetch_add(1, Ordering::Relaxed);
            let mut current = self.current.lock();
            current.lcut = Some(update.lcut);
            current.checksum = Some(update.checksum);
            Ok(())
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            self.current.lock().clone()
        }
    }

    fn source(lcut: u64, checksum: &str) -> Arc<CountingSource> {
        source_with(lcut, checksum, false, true, None)
    }

    fn full_specs_payload(lcut: u64, checksum: &str) -> ResponseData {
        ResponseData::from_bytes(
            serde_json::to_vec(&SpecsResponseFull {
                has_updates: true,
                time: lcut,
                checksum: Some(checksum.to_string()),
                ..SpecsResponseFull::default()
            })
            .expect("scoped test snapshot should serialize"),
        )
    }

    fn source_with(
        lcut: u64,
        checksum: &str,
        has_fallback: bool,
        include_content_length: bool,
        content_encoding: Option<&'static str>,
    ) -> Arc<CountingSource> {
        Arc::new(CountingSource {
            lcut,
            checksum: checksum.to_string(),
            scope_class: None,
            payload_fetches: AtomicUsize::new(0),
            fallback_fetches: AtomicUsize::new(0),
            has_fallback,
            include_content_length,
            content_encoding,
        })
    }

    fn adapter_fixture(
        source: Arc<dyn ScopedConfigSource>,
        lcut: Option<u64>,
        checksum: Option<&str>,
        scope: &str,
    ) -> (Arc<ScopedSourceSpecsAdapter>, Arc<RecordingListener>) {
        let adapter = Arc::new(ScopedSourceSpecsAdapter::new(source, scope));
        let listener = Arc::new(RecordingListener::new(lcut, checksum));
        adapter.initialize(listener.clone());
        (adapter, listener)
    }

    fn observed_fixture(
        source: Arc<dyn ScopedConfigSource>,
        lcut: Option<u64>,
        checksum: Option<&str>,
        scope: &str,
    ) -> (
        Arc<ScopedSourceSpecsAdapter>,
        Arc<RecordingListener>,
        Arc<RecordingObserver>,
    ) {
        let (adapter, listener) = adapter_fixture(source, lcut, checksum, scope);
        let observer = Arc::new(RecordingObserver::default());
        adapter.bind_observability_client(observer.clone());
        (adapter, listener, observer)
    }

    #[tokio::test]
    async fn metadata_requests_receive_the_listener_owned_cursor() {
        for (initial_lcut, initial_checksum) in [(None, None), (Some(123), Some("same-checksum"))] {
            let source = Arc::new(CursorRecordingSource {
                source: source(123, "same-checksum"),
                cursors: Mutex::new(Vec::new()),
            });
            let (adapter, _) =
                adapter_fixture(source.clone(), initial_lcut, initial_checksum, "scope");

            adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

            let cursors = source.cursors.lock();
            assert_eq!(cursors.len(), 1);
            assert_eq!(cursors[0].lcut, initial_lcut);
            assert_eq!(cursors[0].checksum.as_deref(), initial_checksum);
        }
    }

    #[tokio::test]
    async fn unchanged_checksum_advances_cursor_without_fetching_payload() {
        let source = source(124, "same-checksum");
        let (adapter, listener) =
            adapter_fixture(source.clone(), Some(123), Some("same-checksum"), "scope");

        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime())
            .await
            .unwrap();

        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 0);
        assert_eq!(listener.updates.load(Ordering::Relaxed), 0);
        assert_eq!(listener.cursor_updates.load(Ordering::Relaxed), 1);
        assert_eq!(listener.get_current_specs_info().lcut, Some(124));
    }

    #[tokio::test]
    async fn scoped_remote_values_are_hydrated_without_credentials_or_per_scope_observers() {
        let server = MockServer::start().await;
        let body = br#"{"answer":"hydrated"}"#;
        let digest = format!("{:x}", Sha256::digest(body));
        let download_path = format!("/v1/dynamic_config_value/{digest}");

        Mock::given(method("GET"))
            .and(path(download_path.clone()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(body.to_vec()),
            )
            .expect(1)
            .mount(&server)
            .await;

        let source = Arc::new(RemotePayloadSource {
            payload: remote_payload(&download_path, &digest, body.len()),
            trusted_source_url: format!("{}/v2/download_config_specs", server.uri()),
        });
        let adapter = Arc::new(ScopedSourceSpecsAdapter::new(
            source,
            "company:app:production",
        ));
        let observer = Arc::new(RecordingObserver::default());
        adapter.bind_observability_client(observer.clone());
        let store = Arc::new(SpecStore::new(
            "scoped-hydration-test",
            "scoped-hydration-test".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
        ));
        adapter.initialize(store.clone());

        adapter
            .start(&StatsigRuntime::get_runtime())
            .await
            .expect("scoped remote values should hydrate before snapshot publication");

        let values = store.get_current_values().unwrap();
        let value = values
            .dynamic_configs
            .get(&InternedString::from_string("remote_config".to_string()))
            .unwrap()
            .as_spec_ref()
            .default_value
            .get_json()
            .unwrap();
        assert_eq!(value.get("answer"), Some(&serde_json::json!("hydrated")));

        let requests = server.received_requests().await.unwrap();
        assert_eq!(requests.len(), 1);
        assert!(requests[0].headers.get("statsig-api-key").is_none());
        assert!(!OPS_STATS.has_instance_for_test("scoped:remote-value-capability"));

        let increments = observer.increments.lock();
        let (_, tags) = increments
            .iter()
            .find(|(name, _)| name == "statsig.sdk.remote_config_hydration.count")
            .expect("successful scoped hydration should reach its bound observer");
        let tags = tags.as_ref().expect("hydration metrics should carry tags");
        assert_eq!(tags.get("outcome").map(String::as_str), Some("success"));
        assert!(tags.contains_key("sdk_type"));
        assert!(tags.contains_key("sdk_version"));

        let distributions = observer.distributions.lock();
        assert!(distributions.iter().any(|(name, value, tags)| {
            name == "statsig.sdk.remote_config_hydration.bytes"
                && *value == body.len() as f64
                && tags.as_ref().is_some_and(|tags| {
                    tags.contains_key("sdk_type") && tags.contains_key("sdk_version")
                })
        }));
        assert!(distributions.iter().any(|(name, _, tags)| {
            name == "statsig.sdk.remote_config_hydration.latency"
                && tags
                    .as_ref()
                    .and_then(|tags| tags.get("outcome"))
                    .is_some_and(|outcome| outcome == "success")
        }));
    }

    #[tokio::test]
    async fn trusted_hydration_origin_rejects_foreign_values_and_reports_failure() {
        let body = br#"{}"#;
        let digest = format!("{:x}", Sha256::digest(body));
        let source = Arc::new(RemotePayloadSource {
            payload: remote_payload(
                &format!("https://untrusted.example/v1/dynamic_config_value/{digest}"),
                &digest,
                body.len(),
            ),
            trusted_source_url: "https://trusted.example/v2/download_config_specs".to_string(),
        });
        let adapter = Arc::new(ScopedSourceSpecsAdapter::new(source, "trusted-origin"));
        let observer = Arc::new(RecordingObserver::default());
        adapter.bind_observability_client(observer.clone());
        let store = Arc::new(SpecStore::new(
            "trusted-origin",
            "trusted-origin".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
        ));
        adapter.initialize(store);

        let result = adapter.start(&StatsigRuntime::get_runtime()).await;

        assert!(matches!(
            result,
            Err(StatsigErr::CustomError(message))
                if message.contains("untrusted_download_origin")
        ));
        let increments = observer.increments.lock();
        assert!(increments.iter().any(|(name, tags)| {
            name == "statsig.sdk.remote_config_hydration.count"
                && tags
                    .as_ref()
                    .and_then(|tags| tags.get("outcome"))
                    .is_some_and(|outcome| outcome == "failure")
        }));
        let distributions = observer.distributions.lock();
        assert!(distributions.iter().any(|(name, _, tags)| {
            name == "statsig.sdk.remote_config_hydration.latency"
                && tags
                    .as_ref()
                    .and_then(|tags| tags.get("outcome"))
                    .is_some_and(|outcome| outcome == "failure")
        }));
        assert!(
            !distributions
                .iter()
                .any(|(name, _, _)| { name == "statsig.sdk.remote_config_hydration.bytes" })
        );
    }

    #[tokio::test]
    async fn accepted_payload_must_publish_the_metadata_checksum() {
        let source = source(124, "new-checksum");
        let (adapter, listener) =
            adapter_fixture(source.clone(), Some(123), Some("old-checksum"), "scope");
        listener.ignore_next_update.store(true, Ordering::Relaxed);

        let result = adapter.start(&StatsigRuntime::get_runtime()).await;

        assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(source.fallback_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(
            listener.get_current_specs_info().checksum.as_deref(),
            Some("old-checksum")
        );
    }

    #[tokio::test]
    async fn future_payload_lcut_never_publishes_and_valid_fallback_can_recover() {
        for has_fallback in [false, true] {
            let source = source_with(124, "new-checksum", has_fallback, true, None);
            let adapter = Arc::new(ScopedSourceSpecsAdapter::new(
                Arc::new(FutureLcutSource(Arc::clone(&source))),
                "future-lcut-scope",
            ));
            let store = Arc::new(SpecStore::new_with_snapshot_evaluation_session_options(
                "future-lcut-scope",
                "future-lcut-scope".to_string(),
                StatsigRuntime::get_runtime(),
                Arc::new(SdkEventEmitter::default()),
                None,
                &SnapshotEvaluationSessionInitOptions {
                    config_only_mode: true,
                    ..SnapshotEvaluationSessionInitOptions::default()
                },
            ));
            store
                .set_values(SpecsUpdate {
                    data: full_specs_payload(123, "old-checksum"),
                    source: SpecsSource::Network,
                    received_at: 1,
                    source_api: None,
                    has_updates: None,
                })
                .expect("previous scoped snapshot should initialize");
            let previous = store.load_data();
            adapter.initialize(store.clone());

            let result = adapter.start(&StatsigRuntime::get_runtime()).await;

            assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
            assert_eq!(source.fallback_fetches.load(Ordering::Relaxed), 1);
            let current = store.load_data();
            if has_fallback {
                result.expect("valid fallback should recover a future preferred LCUT");
                assert!(!Arc::ptr_eq(&previous, &current));
                assert_eq!(current.lcut(), 124);
                assert_eq!(current.snapshot.checksum.as_deref(), Some("new-checksum"));
            } else {
                assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
                assert!(Arc::ptr_eq(&previous, &current));
                assert_eq!(current.lcut(), 123);
                assert_eq!(current.snapshot.checksum.as_deref(), Some("old-checksum"));
            }
        }
    }

    #[tokio::test]
    async fn initial_payload_cannot_succeed_without_publishing_a_snapshot() {
        let source = source(124, "initial-checksum");
        let (adapter, listener) = adapter_fixture(source.clone(), None, None, "scope");
        listener.ignore_next_update.store(true, Ordering::Relaxed);

        let result = adapter.start(&StatsigRuntime::get_runtime()).await;

        assert!(matches!(result, Err(StatsigErr::ChecksumFailure(_))));
        assert!(listener.get_current_specs_info().lcut.is_none());
        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
    }

    #[tokio::test]
    async fn older_metadata_never_rewinds_the_snapshot() {
        let source = source(122, "older-checksum");
        let (adapter, listener) =
            adapter_fixture(source.clone(), Some(123), Some("current-checksum"), "scope");

        adapter
            .clone()
            .start(&StatsigRuntime::get_runtime())
            .await
            .unwrap();

        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 0);
        assert_eq!(listener.updates.load(Ordering::Relaxed), 0);
    }

    #[tokio::test]
    async fn preferred_payload_failures_are_retried_with_valid_fallback() {
        for (failure, expected_updates) in [("rejected", 2), ("unpublished", 2), ("transport", 1)] {
            let source = source_with(124, "new-checksum", true, true, None);
            let preferred: Arc<dyn ScopedConfigSource> = if failure == "transport" {
                Arc::new(FailingPreferredSource(source.clone()))
            } else {
                source.clone()
            };
            let (adapter, listener) =
                adapter_fixture(preferred, Some(123), Some("old-checksum"), "scope");
            if failure == "rejected" {
                listener.reject_next_update.store(true, Ordering::Relaxed);
            } else if failure == "unpublished" {
                listener.ignore_next_update.store(true, Ordering::Relaxed);
            }

            adapter
                .start(&StatsigRuntime::get_runtime())
                .await
                .expect("JSON fallback should recover every preferred payload failure");

            assert_eq!(
                source.payload_fetches.load(Ordering::Relaxed),
                1,
                "{failure}"
            );
            assert_eq!(
                source.fallback_fetches.load(Ordering::Relaxed),
                1,
                "{failure}"
            );
            assert_eq!(
                listener.updates.load(Ordering::Relaxed),
                expected_updates,
                "{failure}"
            );
            assert_eq!(
                listener.get_current_specs_info().checksum.as_deref(),
                Some("new-checksum"),
                "{failure}"
            );
        }
    }

    #[tokio::test]
    async fn changed_refresh_reports_outcome_duration_and_encoded_payload_size() {
        let mut source = source(124, "new-checksum");
        Arc::get_mut(&mut source)
            .expect("source should not be shared before the adapter is created")
            .scope_class = Some("target_app_and_environment");
        let (adapter, listener, observer) = observed_fixture(
            source.clone(),
            Some(123),
            Some("old-checksum"),
            "private-company:private-app:private-environment",
        );

        adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(listener.updates.load(Ordering::Relaxed), 1);
        assert_eq!(
            listener.get_current_specs_info().checksum.as_deref(),
            Some("new-checksum")
        );

        let increments = observer.increments.lock();
        assert_eq!(increments.len(), 3);
        for metric in [
            super::LEGACY_FETCH_METRIC,
            super::LEGACY_UPDATE_METRIC,
            "statsig.sdk.scoped_snapshot.refresh.count",
        ] {
            let tags = increments
                .iter()
                .find(|(name, _)| name == metric)
                .and_then(|(_, tags)| tags.as_ref())
                .expect("snapshot metric should preserve bounded scope classification");
            assert_eq!(
                tags.get("scope_class").map(String::as_str),
                Some("target_app_and_environment")
            );
            assert!(!tags.values().any(|value| value.contains("private-")));
        }
        let refresh = increments
            .iter()
            .find(|(name, _)| name == "statsig.sdk.scoped_snapshot.refresh.count")
            .expect("modern refresh outcome should be preserved");
        assert_eq!(
            refresh.1.as_ref().and_then(|tags| tags.get("result")),
            Some(&"updated".to_string())
        );
        let tags = refresh.1.as_ref().unwrap();
        assert_eq!(
            tags.get("change_reason").map(String::as_str),
            Some("checksum_changed")
        );
        assert_eq!(tags.get("response_type").map(String::as_str), Some("json"));
        assert_eq!(tags.get("encoding").map(String::as_str), Some("identity"));
        assert_eq!(tags.get("fallback").map(String::as_str), Some("false"));
        let legacy_update = increments
            .iter()
            .find(|(name, _)| name == super::LEGACY_UPDATE_METRIC)
            .expect("legacy refresh dashboards should continue receiving updates");
        let legacy_tags = legacy_update.1.as_ref().unwrap();
        assert_eq!(
            legacy_tags.get("response_type").map(String::as_str),
            Some("uncompressed_json")
        );
        assert_eq!(
            legacy_tags.get("used_json_fallback").map(String::as_str),
            Some("false")
        );
        assert!(!legacy_tags.contains_key("scope"));
        let distributions = observer.distributions.lock();
        let modern_distributions: Vec<_> = distributions
            .iter()
            .filter(|(name, _, _)| name.starts_with("statsig.sdk.scoped_snapshot.refresh."))
            .collect();
        assert_eq!(modern_distributions.len(), 5);
        let phases: Vec<_> = modern_distributions
            .iter()
            .filter(|(name, _, _)| name == "statsig.sdk.scoped_snapshot.refresh.phase.duration_ms")
            .map(|(name, _, tags)| {
                assert_eq!(
                    name,
                    "statsig.sdk.scoped_snapshot.refresh.phase.duration_ms"
                );
                tags.as_ref().unwrap().get("phase").unwrap().as_str()
            })
            .collect();
        assert_eq!(
            phases,
            ["metadata_fetch", "payload_fetch", "decode_publish"]
        );
        let payload = modern_distributions
            .iter()
            .find(|(name, _, _)| name == "statsig.sdk.scoped_snapshot.refresh.payload_bytes")
            .expect("modern payload metric should remain available");
        assert_eq!(
            payload.1,
            br#"{"has_updates":true,"time":124,"checksum":"new-checksum"}"#.len() as f64
        );
        assert!(
            distributions
                .iter()
                .any(|(name, _, _)| name == super::LEGACY_UPDATE_PAYLOAD_METRIC)
        );
        assert!(distributions.iter().any(|(name, _, tags)| {
            name == super::LEGACY_UPDATE_DURATION_METRIC
                && tags
                    .as_ref()
                    .and_then(|tags| tags.get("phase"))
                    .is_some_and(|phase| phase == "decode")
        }));

        let gauges = observer.gauges.lock();
        assert_eq!(gauges.len(), 2);
        assert!(
            gauges
                .iter()
                .all(|(name, _, tags)| { name == super::ACTIVE_UPDATE_METRIC && tags.is_none() })
        );
    }

    #[tokio::test]
    async fn unchanged_refresh_preserves_legacy_poll_liveness_without_modern_update_metrics() {
        let source = source(123, "same-checksum");
        let (adapter, listener, observer) =
            observed_fixture(source.clone(), Some(123), Some("same-checksum"), "scope");

        adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 0);
        assert_eq!(listener.updates.load(Ordering::Relaxed), 0);
        assert_eq!(listener.cursor_updates.load(Ordering::Relaxed), 0);

        let increments = observer.increments.lock();
        assert_eq!(increments.len(), 1);
        assert_eq!(increments[0].0, super::LEGACY_FETCH_METRIC);
        assert_eq!(
            increments[0]
                .1
                .as_ref()
                .and_then(|tags| tags.get("result"))
                .map(String::as_str),
            Some("unchanged")
        );
        assert!(observer.distributions.lock().is_empty());
    }

    #[tokio::test]
    async fn changed_refresh_without_content_length_omits_payload_metric() {
        let source = source_with(124, "new-checksum", false, false, None);
        let (adapter, _listener, observer) =
            observed_fixture(source, Some(123), Some("old-checksum"), "scope");

        adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

        let distributions = observer.distributions.lock();
        assert_eq!(
            distributions
                .iter()
                .filter(|(name, _, _)| name.starts_with("statsig.sdk.scoped_snapshot.refresh."))
                .count(),
            4
        );
        assert!(
            distributions
                .iter()
                .all(|(name, _, _)| name != super::LEGACY_UPDATE_PAYLOAD_METRIC)
        );
    }

    #[tokio::test]
    async fn failed_refresh_reports_outcome_and_duration_without_payload_metric() {
        let source = source(124, "new-checksum");
        let (adapter, listener, observer) =
            observed_fixture(source.clone(), Some(123), Some("old-checksum"), "scope");
        listener.reject_next_update.store(true, Ordering::Relaxed);

        let result = adapter.start(&StatsigRuntime::get_runtime()).await;

        assert!(matches!(result, Err(StatsigErr::ProtobufParseError(_, _))));
        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(source.fallback_fetches.load(Ordering::Relaxed), 1);
        let increments = observer.increments.lock();
        assert_eq!(increments.len(), 2);
        let refresh = increments
            .iter()
            .find(|(name, _)| name == "statsig.sdk.scoped_snapshot.refresh.count")
            .expect("modern failure metric should remain available");
        assert_eq!(
            refresh.1.as_ref().and_then(|tags| tags.get("result")),
            Some(&"error".to_string())
        );
        let legacy = increments
            .iter()
            .find(|(name, _)| name == super::LEGACY_FETCH_METRIC)
            .expect("legacy failure metric should remain available");
        assert_eq!(
            legacy.1.as_ref().and_then(|tags| tags.get("result")),
            Some(&"payload_error".to_string())
        );
        let distributions = observer.distributions.lock();
        assert_eq!(distributions.len(), 4);
        assert_eq!(
            distributions[0].0,
            "statsig.sdk.scoped_snapshot.refresh.duration_ms"
        );
        let gauges = observer.gauges.lock();
        assert_eq!(gauges.len(), 2);
        assert!(
            gauges
                .iter()
                .all(|(name, _, _)| name == super::ACTIVE_UPDATE_METRIC)
        );
    }

    #[tokio::test]
    async fn protobuf_fallback_refresh_reports_low_cardinality_phase_context() {
        let source = source_with(124, "repaired-checksum", true, true, Some("statsig-br"));
        let (adapter, listener, observer) = observed_fixture(
            source.clone(),
            Some(124),
            Some("old-checksum"),
            "private-scope",
        );
        listener.reject_next_update.store(true, Ordering::Relaxed);

        adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

        assert_eq!(source.payload_fetches.load(Ordering::Relaxed), 1);
        assert_eq!(source.fallback_fetches.load(Ordering::Relaxed), 1);
        let increments = observer.increments.lock();
        let tags = increments
            .iter()
            .find(|(name, _)| name == "statsig.sdk.scoped_snapshot.refresh.count")
            .and_then(|(_, tags)| tags.as_ref())
            .expect("modern refresh tags should remain available");
        assert_eq!(tags.get("result").map(String::as_str), Some("updated"));
        assert_eq!(
            tags.get("change_reason").map(String::as_str),
            Some("checksum_repair")
        );
        assert_eq!(tags.get("response_type").map(String::as_str), Some("json"));
        assert_eq!(tags.get("encoding").map(String::as_str), Some("identity"));
        assert_eq!(tags.get("fallback").map(String::as_str), Some("true"));
        assert!(!tags.contains_key("scope"));
        assert!(!tags.contains_key("sdk_key"));

        let distributions = observer.distributions.lock();
        let modern_distributions: Vec<_> = distributions
            .iter()
            .filter(|(name, _, _)| name.starts_with("statsig.sdk.scoped_snapshot.refresh."))
            .collect();
        assert_eq!(modern_distributions.len(), 4);
        assert!(modern_distributions.iter().skip(1).all(|(_, _, tags)| {
            tags.as_ref()
                .and_then(|tags| tags.get("fallback"))
                .is_some_and(|fallback| fallback == "true")
        }));
        let legacy = increments
            .iter()
            .find(|(name, _)| name == super::LEGACY_UPDATE_METRIC)
            .and_then(|(_, tags)| tags.as_ref())
            .expect("legacy fallback tags should remain available");
        assert_eq!(
            legacy.get("used_json_fallback").map(String::as_str),
            Some("true")
        );
    }

    #[tokio::test]
    async fn protobuf_refresh_reports_brotli_response_encoding() {
        let source = source_with(124, "new-checksum", false, true, Some("statsig-br"));
        let (adapter, _listener, observer) =
            observed_fixture(source, Some(123), Some("old-checksum"), "private-scope");

        adapter.start(&StatsigRuntime::get_runtime()).await.unwrap();

        let increments = observer.increments.lock();
        let tags = increments
            .iter()
            .find(|(name, _)| name == "statsig.sdk.scoped_snapshot.refresh.count")
            .and_then(|(_, tags)| tags.as_ref())
            .expect("modern protobuf tags should remain available");
        assert_eq!(
            tags.get("response_type").map(String::as_str),
            Some("protobuf")
        );
        assert_eq!(tags.get("encoding").map(String::as_str), Some("brotli"));
        assert_eq!(tags.get("fallback").map(String::as_str), Some("false"));
        let legacy = increments
            .iter()
            .find(|(name, _)| name == super::LEGACY_UPDATE_METRIC)
            .and_then(|(_, tags)| tags.as_ref())
            .expect("legacy protobuf tags should remain available");
        assert_eq!(
            legacy.get("response_type").map(String::as_str),
            Some("brotli_protobuf")
        );
    }

    #[test]
    fn first_sync_is_stable_per_scope_and_jittered_within_second_half_of_polling_interval() {
        let source = source(1, "checksum");
        let first = ScopedSourceSpecsAdapter::new(source.clone(), "scope");
        let second = ScopedSourceSpecsAdapter::new(source.clone(), "scope");

        assert_eq!(first.first_sync_delay(), second.first_sync_delay());

        let delays = (0..64)
            .map(|index| {
                ScopedSourceSpecsAdapter::new(source.clone(), &format!("scope-{index}"))
                    .first_sync_delay()
            })
            .collect::<std::collections::HashSet<_>>();

        assert!(delays.len() > 1);
        assert!(
            delays
                .iter()
                .all(|delay| *delay >= SYNC_INTERVAL / 2 && *delay <= SYNC_INTERVAL)
        );
    }
}
