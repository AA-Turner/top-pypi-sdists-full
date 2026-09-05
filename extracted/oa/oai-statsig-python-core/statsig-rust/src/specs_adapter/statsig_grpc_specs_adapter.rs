use super::{SpecsInfo, StatsigHttpSpecsAdapter};
use crate::networking::{DEFAULT_CDN_SPECS_URL, ResponseData, config_specs_url};
use crate::observability::ErrorBoundaryEvent;
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::{
    SpecAdapterConfig, SpecsAdapter, SpecsSource, SpecsUpdate, SpecsUpdateListener, StatsigErr,
    StatsigOptions, StatsigRuntime, log_d, log_e, log_error_to_statsig_and_console, log_w,
};
use async_trait::async_trait;
use chrono::Utc;
use oai_statsig_grpc::statsig_grpc_client::StatsigGrpcClient;
use parking_lot::{Mutex, RwLock};
use std::cmp;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::time::Duration;
use tokio::sync::{Notify, broadcast};
use tokio::time::{sleep, timeout};

// Todo make those configurable
const DEFAULT_BACKOFF_INTERVAL_MS: u64 = 3000;
const DEFAULT_BACKOFF_MULTIPLIER: u64 = 2;
const MAX_BACKOFF_INTERVAL_MS: u64 = 60 * 1000;
const RETRY_LIMIT: u64 = 10 * 24 * 60 * 60;
const FALL_BACK_TO_POLLING_THREASHOLD: u64 = 30; //Fallback after 30 minutes
struct StreamingRetryState {
    backoff_interval_ms: AtomicU64,
    retry_attempts: AtomicU64,
    is_retrying: AtomicBool,
}

const TAG: &str = stringify!(StatsigGrpcSpecsAdapter);
const BG_TASK_TAG: &str = "grpc_streaming";

pub struct StatsigGrpcSpecsAdapter {
    listener: RwLock<Option<Arc<dyn SpecsUpdateListener>>>,
    shutdown_notify: Arc<Notify>,
    initialization_tx: Arc<broadcast::Sender<Result<(), StatsigErr>>>,
    task_handle_id: Mutex<Option<tokio::task::Id>>,
    grpc_client: StatsigGrpcClient,
    retry_state: StreamingRetryState,
    init_timeout: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    // For fallback to poll job behavior
    http_specs_adapter: Arc<StatsigHttpSpecsAdapter>,
    hydration_source_url: String,
    cancel_poll_notify: Arc<Notify>,
}

#[async_trait]
impl SpecsAdapter for StatsigGrpcSpecsAdapter {
    async fn start(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        let handle_id = self
            .clone()
            .spawn_grpc_streaming_thread(statsig_runtime, self.ops_stats.clone())
            .await?;

        self.set_task_handle_id(handle_id)?;
        let mut rx = self.initialization_tx.subscribe();
        match timeout(self.init_timeout, rx.recv()).await {
            Ok(res) => match res {
                Ok(Ok(())) => Ok(()),
                Ok(Err(err)) => Err(StatsigErr::GrpcError(format!(
                    "Failed to initialize from streaming: {err}"
                ))),
                Err(_) => Err(StatsigErr::GrpcError("Failed to get a ".to_string())),
            },
            Err(_) => Err(StatsigErr::GrpcError(
                "Start Timeout to get a response".to_string(),
            )),
        }
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        match self.task_handle_id.try_lock_for(Duration::from_secs(5)) {
            Some(lock) => {
                if lock.is_some() {
                    return Ok(());
                }
            }
            None => {
                log_w!(TAG, "Failed to lock task_handle_id");
                return Err(StatsigErr::LockFailure(
                    "Failed to lock task_handle_id".to_string(),
                ));
            }
        };

        let task_id = self
            .clone()
            .spawn_grpc_streaming_thread(statsig_runtime, self.ops_stats.clone())
            .await?;

        match self.task_handle_id.try_lock_for(Duration::from_secs(5)) {
            Some(mut lock) => {
                *lock = Some(task_id);
            }
            None => {
                log_w!(TAG, "Failed to lock task_handle_id");
            }
        }

        Ok(())
    }

    fn initialize(&self, listener: Arc<dyn SpecsUpdateListener>) {
        self.http_specs_adapter.initialize(listener.clone());
        match self
            .listener
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut lock) => *lock = Some(listener),
            None => {
                log_error_to_statsig_and_console!(
                    self.ops_stats,
                    TAG,
                    StatsigErr::LockFailure("Failed to acquire write lock on listener".to_string())
                );
            }
        }
    }

    async fn shutdown(
        &self,
        timeout: Duration,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.shutdown_notify.notify_one();

        let opt_handle_id = match self.task_handle_id.try_lock_for(Duration::from_secs(5)) {
            Some(mut lock) => lock.take(),
            None => {
                log_w!(TAG, "Failed to lock task_handle_id");
                return Err(StatsigErr::LockFailure(
                    "Failed to lock task_handle_id".to_string(),
                ));
            }
        };

        let handle_id = match opt_handle_id {
            Some(handle_id) => handle_id,
            None => {
                return Err(StatsigErr::ThreadFailure(
                    "No running task found".to_string(),
                ));
            }
        };

        if tokio::time::timeout(
            timeout,
            statsig_runtime.await_join_handle(BG_TASK_TAG, &handle_id),
        )
        .await
        .is_err()
        {
            return Err(StatsigErr::GrpcError(
                "Failed to gracefully shutdown StatsigGrpcSpecsAdapter.".to_string(),
            ));
        }

        Ok(())
    }

    fn get_type_name(&self) -> String {
        stringify!(StatsigGrpcSpecsAdapter).to_string()
    }
}

impl StatsigGrpcSpecsAdapter {
    pub fn new(
        sdk_key: &str,
        config: &SpecAdapterConfig,
        options: Option<&StatsigOptions>,
    ) -> Self {
        let grpc_source_url = config.specs_url.clone().unwrap_or("INVALID".to_owned());
        let default_options = StatsigOptions::default();
        let options_ref = options.unwrap_or(&default_options);
        let hydration_source_url = config_specs_url(
            options_ref
                .remote_config_value_source_url
                .as_deref()
                .or(options_ref.specs_url.as_deref())
                .unwrap_or(DEFAULT_CDN_SPECS_URL),
        );
        let fallback_adapter = StatsigHttpSpecsAdapter::new(sdk_key, options, None);
        let sdk_instance_id = options_ref.get_sdk_instance_id(sdk_key);
        let (init_tx, _) = broadcast::channel(1);
        Self {
            listener: RwLock::new(None),
            shutdown_notify: Arc::new(Notify::new()),
            task_handle_id: Mutex::new(None),
            grpc_client: StatsigGrpcClient::new(
                sdk_key,
                &grpc_source_url,
                config.authentication_mode.clone(),
                config.ca_cert_path.clone(),
                config.client_cert_path.clone(),
                config.client_key_path.clone(),
                config.domain_name.clone(),
            ),
            initialization_tx: Arc::new(init_tx),
            retry_state: StreamingRetryState {
                backoff_interval_ms: DEFAULT_BACKOFF_INTERVAL_MS.into(),
                retry_attempts: 0.into(),
                is_retrying: false.into(),
            },
            init_timeout: Duration::from_millis(config.init_timeout_ms),
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            http_specs_adapter: Arc::new(fallback_adapter),
            hydration_source_url,
            cancel_poll_notify: Arc::new(Notify::new()),
        }
    }

    fn spawn_poll_from_statsig_thread(
        http_spec_adapter: Arc<StatsigHttpSpecsAdapter>,
        cancel_notify: Arc<Notify>,
        shutdown_notify: Arc<Notify>,
    ) {
        let weak_http_adapter = Arc::downgrade(&http_spec_adapter);
        tokio::task::spawn(async move {
            loop {
                tokio::select! {
                    _ = sleep(Duration::from_millis(3000)) => {
                        if let Some(strong_http_adapter) = weak_http_adapter.upgrade() {
                            StatsigHttpSpecsAdapter::run_background_sync(strong_http_adapter).await;
                        } else {
                            log_e!(TAG, "GRPC adapter lost strong reference to StatsigHttpSpecsAdapter. Stopping polling thread");
                            break;
                        }
                    }
                    _ = cancel_notify.notified() => {
                        log_d!(TAG, "Cancel grpc fallback background specs sync");
                        break;
                    }
                    _ = shutdown_notify.notified() => {
                        log_d!(TAG, "Shutting down grpc fallback specs background sync");
                        break;
                    }
                }
            }
        });
    }

    async fn spawn_grpc_streaming_thread(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
        ops_stats: Arc<OpsStatsForInstance>,
    ) -> Result<tokio::task::Id, StatsigErr> {
        let weak_self = Arc::downgrade(&self);

        statsig_runtime.spawn(BG_TASK_TAG, |_shutdown_notify| async move {
            if let Some(strong_self) = weak_self.upgrade() {
                if let Err(e) = strong_self.run_retryable_grpc_stream().await {
                    log_error_to_statsig_and_console!(
                        &ops_stats,
                        TAG,
                        StatsigErr::GrpcError(format!("gRPC streaming thread failed: {e}"))
                    );
                }
            } else {
                log_error_to_statsig_and_console!(
                    &ops_stats,
                    TAG,
                    StatsigErr::GrpcError(
                        "Failed to upgrade weak reference to strong reference".to_string()
                    )
                );
            }
        })
    }

    async fn run_retryable_grpc_stream(&self) -> Result<(), StatsigErr> {
        loop {
            tokio::select! {
                result = self.handle_grpc_request_stream() => {
                    if let Err(err) = result {
                        let attempt = self.retry_state.retry_attempts.fetch_add(1, Ordering::SeqCst);
                        if attempt > RETRY_LIMIT {
                            log_error_to_statsig_and_console!(&self.ops_stats, TAG, StatsigErr::GrpcError(format!("gRPC stream failure, exhaust retry limit: {err:?}")));
                           break;
                        }
                        if attempt == FALL_BACK_TO_POLLING_THREASHOLD {
                            log_d!(TAG, "SFP is not reachable after {} tries: Falling back to polling from statsig", FALL_BACK_TO_POLLING_THREASHOLD);
                            Self::spawn_poll_from_statsig_thread(self.http_specs_adapter.clone(), self.cancel_poll_notify.clone(), self.shutdown_notify.clone());
                        }
                        self.grpc_client.reset_client();

                        // Update retry state
                        let curr_backoff = self.retry_state.backoff_interval_ms.load(Ordering::SeqCst);
                        let new_backoff = if curr_backoff < MAX_BACKOFF_INTERVAL_MS {
                            cmp::min(curr_backoff * DEFAULT_BACKOFF_MULTIPLIER, MAX_BACKOFF_INTERVAL_MS)
                        } else  {
                            MAX_BACKOFF_INTERVAL_MS
                        };
                        self.retry_state.backoff_interval_ms.store(new_backoff,Ordering::SeqCst);
                        self.retry_state.is_retrying.store(true, Ordering::SeqCst);
                        self.log_streaming_err(err, attempt, curr_backoff);
                        tokio::time::sleep(Duration::from_millis(curr_backoff)).await;
                    }
                },
                _ = self.shutdown_notify.notified() => {
                    log_d!(TAG, "Received shutdown signal, stopping stream listener.");
                    break;
                }
            }
        }
        Ok(())
    }

    async fn handle_grpc_request_stream(&self) -> Result<(), StatsigErr> {
        self.grpc_client
            .connect_client()
            .await
            .map_err(|e| StatsigErr::GrpcError(format!("{e}")))?;
        let specs_info = self.get_current_specs_info();
        let mut stream = self
            .grpc_client
            .get_specs_stream(specs_info.as_ref().and_then(|s| s.lcut))
            .await
            .map_err(|e| StatsigErr::GrpcError(format!("{e}")))?;
        loop {
            match stream.message().await {
                Ok(Some(config_spec)) => {
                    let data = match self.hydrate_spec_update(config_spec.spec).await {
                        Ok(data) => data,
                        Err(error) => {
                            let _ = self.initialization_tx.send(Err(error.clone()));
                            self.log_received_message();
                            return Err(error);
                        }
                    };

                    self.cancel_poll_notify.notify_one();
                    if self.retry_state.is_retrying.load(Ordering::SeqCst) {
                        // Reset retry state
                        self.retry_state.is_retrying.store(false, Ordering::SeqCst);
                        self.retry_state.retry_attempts.store(0, Ordering::SeqCst);
                        self.retry_state
                            .backoff_interval_ms
                            .store(DEFAULT_BACKOFF_INTERVAL_MS, Ordering::SeqCst);
                        self.ops_stats.log(ObservabilityEvent::new_event(
                            MetricType::Increment,
                            "grpc_reconnected".to_string(),
                            1.0,
                            None,
                        ));
                    }

                    let update_result = self.send_hydrated_spec_update_to_listener(data);
                    let _ = self.initialization_tx.send(update_result);
                    self.log_received_message();
                }
                err => {
                    return Err(StatsigErr::GrpcError(format!(
                        "Error while receiving stream: {err:?}"
                    )));
                }
            }
        }
    }

    fn set_task_handle_id(&self, handle_id: tokio::task::Id) -> Result<(), StatsigErr> {
        match self.task_handle_id.try_lock_for(Duration::from_secs(5)) {
            Some(mut lock) => {
                *lock = Some(handle_id);
                Ok(())
            }
            None => {
                log_w!(TAG, "Failed to lock task_handle_id");
                Err(StatsigErr::LockFailure(
                    "Failed to lock task_handle_id".to_string(),
                ))
            }
        }
    }

    async fn hydrate_spec_update(&self, data: String) -> Result<ResponseData, StatsigErr> {
        let mut data = ResponseData::from_bytes(data.into_bytes());
        self.http_specs_adapter
            .hydrate_response_data(&mut data, &self.hydration_source_url)
            .await?;
        Ok(data)
    }

    fn send_hydrated_spec_update_to_listener(&self, data: ResponseData) -> Result<(), StatsigErr> {
        let listener = self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
            .ok_or_else(|| {
                StatsigErr::LockFailure("Failed to acquire read lock on listener".to_string())
            })?;

        if let Some(listener) = listener.as_ref() {
            let update = SpecsUpdate {
                data,
                source: SpecsSource::Adapter("GRPC".to_string()),
                received_at: Utc::now().timestamp_millis() as u64,
                source_api: None,
                has_updates: None,
            };

            listener.did_receive_specs_update(update)
        } else {
            Err(StatsigErr::UnstartedAdapter("Listener not set".to_string()))
        }
    }

    fn log_received_message(&self) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            "grpc_received_message".to_string(),
            1.0,
            None,
        ));
    }

    fn get_current_specs_info(&self) -> Option<SpecsInfo> {
        match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => Some(listener.get_current_specs_info()),
                None => {
                    log_w!(TAG, "Failed to get current lcut");
                    None
                }
            },
            None => {
                log_w!(TAG, "Failed to get current lcut");
                None
            }
        }
    }

    fn log_streaming_err(&self, err: StatsigErr, retry_attempts: u64, backoff: u64) {
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            "grpc_streaming_failed_with_retry_ct".to_string(),
            retry_attempts as f64,
            None,
        ));
        log_w!(
            TAG,
            "gRPC stream failure ({}). Will wait {} ms and retry. Error: {:?}",
            retry_attempts,
            backoff,
            err
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oai_statsig_grpc::mock_forward_proxy::{MockForwardProxy, api::ConfigSpecResponse};
    use serde_json::json;
    use sha2::{Digest, Sha256};
    use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    #[derive(Default)]
    struct RecordingListener {
        received_update: AtomicBool,
    }

    impl SpecsUpdateListener for RecordingListener {
        fn did_receive_specs_update(&self, _update: SpecsUpdate) -> Result<(), StatsigErr> {
            self.received_update.store(true, Ordering::SeqCst);
            Ok(())
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    #[derive(Default)]
    struct FailingListener {
        received_updates: AtomicUsize,
    }

    impl SpecsUpdateListener for FailingListener {
        fn did_receive_specs_update(&self, _update: SpecsUpdate) -> Result<(), StatsigErr> {
            self.received_updates.fetch_add(1, Ordering::SeqCst);
            Err(StatsigErr::CustomError(
                "intentional listener failure".to_string(),
            ))
        }

        fn get_current_specs_info(&self) -> SpecsInfo {
            SpecsInfo::empty()
        }
    }

    #[tokio::test]
    async fn hydration_failure_returns_without_cancelling_polling() {
        let mock_proxy = MockForwardProxy::spawn().await;
        let config = grpc_config(format!("http://{}", mock_proxy.proxy_address));
        let adapter = Arc::new(StatsigGrpcSpecsAdapter::new("secret-key", &config, None));
        let listener = Arc::new(RecordingListener::default());
        adapter.initialize(listener.clone());
        mock_proxy
            .send_stream_update(Ok(ConfigSpecResponse {
                spec: r#"{"dynamic_configs":{"config":{"defaultValue":"https://statsigcdn.openai.com/v1/dynamic_config_value/not-a-sha","remoteConfigMetadata":{"sha256":"not-a-sha","byteLength":1,"contentType":"application/json","compression":"none"},"rules":[]}}}"#.to_string(),
                last_updated: 123,
                zstd_dict_id: None,
            }))
            .await;

        let result = timeout(Duration::from_secs(2), adapter.handle_grpc_request_stream())
            .await
            .expect("hydration failure should return from the stream loop");

        assert!(matches!(
            result,
            Err(StatsigErr::CustomError(message))
                if message.starts_with("Dynamic config hydration failure: invalid_sha256:")
        ));
        assert!(!listener.received_update.load(Ordering::SeqCst));
        assert!(
            timeout(
                Duration::from_millis(50),
                adapter.cancel_poll_notify.notified()
            )
            .await
            .is_err()
        );

        mock_proxy.stop().await;
    }

    #[tokio::test]
    async fn listener_failure_without_remote_metadata_keeps_stream_open() {
        let mock_proxy = MockForwardProxy::spawn().await;
        let config = grpc_config(format!("http://{}", mock_proxy.proxy_address));
        let adapter = Arc::new(StatsigGrpcSpecsAdapter::new("secret-key", &config, None));
        let listener = Arc::new(FailingListener::default());
        adapter.initialize(listener.clone());

        for last_updated in [123, 124] {
            mock_proxy
                .send_stream_update(Ok(ConfigSpecResponse {
                    spec: r#"{"dynamic_configs":{}}"#.to_string(),
                    last_updated,
                    zstd_dict_id: None,
                }))
                .await;
        }

        let stream_adapter = adapter.clone();
        let stream_task =
            tokio::spawn(async move { stream_adapter.handle_grpc_request_stream().await });
        timeout(Duration::from_secs(2), async {
            while listener.received_updates.load(Ordering::SeqCst) < 2 {
                tokio::time::sleep(Duration::from_millis(10)).await;
            }
        })
        .await
        .expect("the stream should process a second update after a listener failure");
        assert!(
            !stream_task.is_finished(),
            "an ordinary listener failure should not close the gRPC stream"
        );

        stream_task.abort();
        let _ = stream_task.await;
        mock_proxy.stop().await;
    }

    #[tokio::test]
    async fn relative_remote_value_url_uses_http_specs_source() {
        assert_hydrates_from_http_specs_source(false).await;
    }

    #[tokio::test]
    async fn absolute_remote_value_url_uses_http_specs_source() {
        assert_hydrates_from_http_specs_source(true).await;
    }

    #[tokio::test]
    async fn configured_remote_value_source_overrides_http_specs_source() {
        let grpc_source = MockForwardProxy::spawn().await;
        let http_specs_source = MockServer::start().await;
        let blob_source = MockServer::start().await;
        let remote_value = br#"{"from":"configured-blob-source"}"#;
        let sha = lowercase_hex(&Sha256::digest(remote_value));
        let download_path = format!("/v1/dynamic_config_value/{sha}");

        Mock::given(method("GET"))
            .and(path(download_path.clone()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(remote_value),
            )
            .expect(1)
            .mount(&blob_source)
            .await;
        Mock::given(method("GET"))
            .and(path(download_path.clone()))
            .respond_with(ResponseTemplate::new(500))
            .expect(0)
            .mount(&http_specs_source)
            .await;

        let config = grpc_config(format!("http://{}", grpc_source.proxy_address));
        let options = StatsigOptions {
            specs_url: Some(http_specs_source.uri()),
            remote_config_value_source_url: Some(blob_source.uri()),
            ..StatsigOptions::new()
        };
        let adapter = StatsigGrpcSpecsAdapter::new("secret-key", &config, Some(&options));
        let listener = Arc::new(RecordingListener::default());
        adapter.initialize(listener.clone());

        let data = adapter
            .hydrate_spec_update(
                json!({
                    "dynamic_configs": {
                        "config": {
                            "defaultValue": download_path,
                            "remoteConfigMetadata": {
                                "sha256": sha,
                                "byteLength": remote_value.len(),
                                "contentType": "application/json",
                                "compression": "none"
                            },
                            "rules": []
                        }
                    }
                })
                .to_string(),
            )
            .await
            .unwrap();
        adapter.send_hydrated_spec_update_to_listener(data).unwrap();

        assert!(listener.received_update.load(Ordering::SeqCst));
        blob_source.verify().await;
        http_specs_source.verify().await;
        grpc_source.stop().await;
    }

    async fn assert_hydrates_from_http_specs_source(use_absolute_url: bool) {
        let grpc_source = MockForwardProxy::spawn().await;
        let http_source = MockServer::start().await;
        let remote_value = br#"{"from":"http-source"}"#;
        let sha = lowercase_hex(&Sha256::digest(remote_value));
        let download_path = format!("/v1/dynamic_config_value/{sha}");
        let placeholder = if use_absolute_url {
            format!("{}{download_path}", http_source.uri())
        } else {
            download_path.clone()
        };

        Mock::given(method("GET"))
            .and(path(download_path))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(remote_value),
            )
            .expect(1)
            .mount(&http_source)
            .await;

        let config = grpc_config(format!("http://{}", grpc_source.proxy_address));
        let options = StatsigOptions {
            specs_url: Some(http_source.uri()),
            ..StatsigOptions::new()
        };
        let adapter = StatsigGrpcSpecsAdapter::new("secret-key", &config, Some(&options));
        let listener = Arc::new(RecordingListener::default());
        adapter.initialize(listener.clone());

        let data = adapter
            .hydrate_spec_update(
                json!({
                    "dynamic_configs": {
                        "config": {
                            "defaultValue": placeholder,
                            "remoteConfigMetadata": {
                                "sha256": sha,
                                "byteLength": remote_value.len(),
                                "contentType": "application/json",
                                "compression": "none"
                            },
                            "rules": []
                        }
                    }
                })
                .to_string(),
            )
            .await
            .unwrap();
        adapter.send_hydrated_spec_update_to_listener(data).unwrap();

        assert!(listener.received_update.load(Ordering::SeqCst));
        http_source.verify().await;
        grpc_source.stop().await;
    }

    fn grpc_config(specs_url: String) -> SpecAdapterConfig {
        SpecAdapterConfig {
            adapter_type: crate::SpecsAdapterType::NetworkGrpcWebsocket,
            specs_url: Some(specs_url),
            init_timeout_ms: 3_000,
            authentication_mode: None,
            ca_cert_path: None,
            client_cert_path: None,
            client_key_path: None,
            domain_name: None,
        }
    }

    fn lowercase_hex(bytes: &[u8]) -> String {
        const HEX: &[u8; 16] = b"0123456789abcdef";
        let mut result = String::with_capacity(bytes.len() * 2);
        for byte in bytes {
            result.push(HEX[(byte >> 4) as usize] as char);
            result.push(HEX[(byte & 0x0f) as usize] as char);
        }
        result
    }
}
