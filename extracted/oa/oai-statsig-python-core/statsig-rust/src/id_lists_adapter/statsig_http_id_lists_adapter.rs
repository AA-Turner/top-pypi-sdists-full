use super::IdListMetadata;
use crate::id_lists_adapter::{IdListUpdate, IdListsAdapter, IdListsUpdateListener};
use crate::networking::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, NetworkClient, NetworkError, RequestArgs, Response,
    ResponseData, default_cdn_id_lists_manifest_url, is_default_cdn_id_lists_manifest_url,
    is_default_cdn_url, normalize_default_cdn_id_lists_manifest_url, replace_url_base,
};
use crate::observability::observability_client_adapter::{MetricType, ObservabilityEvent};
use crate::observability::ops_stats::{OPS_STATS, OpsStatsForInstance};
use crate::observability::sdk_errors_observer::ErrorBoundaryEvent;
use crate::sdk_diagnostics::diagnostics::ContextType;
use crate::sdk_diagnostics::marker::{ActionType, KeyType, Marker, StepType};
use crate::statsig_metadata::StatsigMetadata;
use crate::{
    StatsigErr, StatsigOptions, StatsigRuntime, log_d, log_e, log_error_to_statsig_and_console,
};
use async_trait::async_trait;
use chrono::Utc;
use futures::{StreamExt, stream};
use parking_lot::RwLock;
use std::collections::HashMap;
use std::sync::{Arc, Weak};
use std::time::Duration;
use tokio::sync::Notify;
use tokio::time::sleep;

const DEFAULT_ID_LIST_SYNC_INTERVAL_MS: u32 = 60_000;
const ID_LIST_DOWNLOAD_CONCURRENCY: usize = 4;

type IdListsResponse = HashMap<String, IdListMetadata>;

const TAG: &str = stringify!(StatsigHttpIdListsAdapter);
const ID_LISTS_SYNC_OVERALL_LATENCY_METRIC: &str = "id_lists_sync_overall.latency";
const ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG: &str = "id_list_manifest_success";
const ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG: &str =
    "succeed_single_id_list_number";

pub struct StatsigHttpIdListsAdapter {
    output_policy: crate::output_policy::OutputPolicy,
    id_lists_manifest_url: String,
    download_id_list_file_api: Option<String>,
    fallback_url: Option<String>,
    fallback_to_statsig_api: bool,
    listener: RwLock<Option<Arc<dyn IdListsUpdateListener>>>,
    network: NetworkClient,
    sync_interval_duration: Duration,
    ops_stats: Arc<OpsStatsForInstance>,
    shutdown_notify: Arc<Notify>,
    download_retry_count: u32,
}

impl StatsigHttpIdListsAdapter {
    #[must_use]
    pub fn new(sdk_key: &str, options: &StatsigOptions) -> Self {
        let output_policy = crate::output_policy::OutputPolicy::from_options(Some(options));
        let _output_scope = output_policy.enter();
        let id_lists_manifest_url =
            normalize_default_cdn_id_lists_manifest_url(options.id_lists_url.as_deref());

        let mut fallback_url = None;
        if options.fallback_to_statsig_api == Some(true)
            && !id_lists_manifest_url.contains(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX)
        {
            fallback_url = Some(default_cdn_id_lists_manifest_url());
        }

        let sync_interval_duration = Duration::from_millis(u64::from(
            options
                .id_lists_sync_interval_ms
                .unwrap_or(DEFAULT_ID_LIST_SYNC_INTERVAL_MS),
        ));

        let headers =
            StatsigMetadata::get_constant_request_headers(sdk_key, options.service_name.as_deref());
        let network = NetworkClient::new(sdk_key, Some(headers), Some(options));

        let sdk_instance_id = options.get_sdk_instance_id(sdk_key);

        Self {
            output_policy,
            id_lists_manifest_url,
            download_id_list_file_api: options.download_id_list_file_api.clone(),
            fallback_url,
            fallback_to_statsig_api: options.fallback_to_statsig_api == Some(true),
            listener: RwLock::new(None),
            network,
            sync_interval_duration,
            ops_stats: OPS_STATS.get_for_instance(sdk_instance_id),
            shutdown_notify: Arc::new(Notify::new()),
            download_retry_count: 2,
        }
    }

    pub fn force_shutdown(&self) {
        let _output_scope = self.output_policy.enter();
        self.shutdown_notify.notify_one();
    }

    async fn fetch_id_list_manifests_from_network(&self) -> Result<IdListsResponse, StatsigErr> {
        let request_args = RequestArgs {
            url: self.id_lists_manifest_url.clone(),
            accept_gzip_response: true,
            diagnostics_key: Some(KeyType::GetIDListSources),
            ..RequestArgs::new()
        };

        let result = if self.is_cdn_url() {
            self.network.get(request_args.clone()).await
        } else {
            self.network.post(request_args.clone(), None).await
        };

        let result = match result {
            Ok(response) => self.parse_response(response.data),
            Err(initial_err) => {
                self.handle_manifest_network_error(request_args, initial_err)
                    .await
            }
        };

        let (metric_name, metric_value) = if result.is_ok() {
            ("id_list_manifest_download_success", 1.0)
        } else {
            ("id_list_manifest_download_failure", 1.0)
        };
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Increment,
            metric_name.to_string(),
            metric_value,
            None,
        ));

        result
    }

    async fn download_id_list(&self, job: &IdListDownloadJob) -> Result<String, StatsigErr> {
        let mut download_url = job.url.as_str();
        let mut using_fallback = false;
        for attempt in 1..=self.download_retry_count + 1 {
            let request = Self::id_list_file_request_args(
                download_url,
                job.range_start,
                job.metadata.size,
                job.metadata.file_id.clone(),
            );
            let response = if using_fallback {
                // Only the captured default CDN is trusted with SDK credentials.
                // Never forward those credentials through a fallback redirect.
                self.network.get_without_redirects(request).await
            } else {
                self.network.get(request).await
            };
            let can_fallback = !using_fallback
                && self.fallback_to_statsig_api
                && job.url != job.metadata.url
                && is_default_cdn_url(&job.metadata.url)
                && matches!(&response, Err(NetworkError::RetriesExhausted(_, status, _, _)) if *status != Some(401));
            self.add_diagnostics_start_marker(
                KeyType::GetIDList,
                StepType::Process,
                None,
                Some(download_url.to_owned()),
            );
            let result = match response {
                Err(error) => Err(StatsigErr::NetworkError(error)),
                Ok(response) => {
                    if let Some(error) = response.error {
                        Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                            download_url.to_owned(),
                            response.status_code,
                            error,
                        )))
                    } else if let Some(mut body) = response.data {
                        // I/O failures are retryable; malformed UTF-8 is terminal.
                        body.read_to_string()
                    } else {
                        Err(StatsigErr::NetworkError(NetworkError::RequestFailed(
                            download_url.to_owned(),
                            response.status_code,
                            "Missing ID list body".into(),
                        )))
                    }
                }
            };
            self.add_diagnostics_end_marker(
                KeyType::GetIDList,
                StepType::Process,
                result.is_ok(),
                None,
                Some(download_url.to_owned()),
            );
            match result {
                Ok(body) => return Ok(body),
                Err(mut error) if !is_retryable_download_error(&error) => {
                    if let StatsigErr::NetworkError(NetworkError::RetriesExhausted(
                        _,
                        _,
                        count,
                        _,
                    )) = &mut error
                    {
                        *count = attempt;
                    }
                    return Err(error);
                }
                Err(error) if attempt > self.download_retry_count => {
                    let status = match &error {
                        StatsigErr::NetworkError(error) => error.status_code(),
                        _ => None,
                    };
                    return Err(StatsigErr::NetworkError(NetworkError::RetriesExhausted(
                        download_url.to_owned(),
                        status,
                        attempt,
                        error.to_string(),
                    )));
                }
                Err(_) => {
                    // Fallback consumes the same per-file retry budget. Explicit zero
                    // retries means one SDK attempt, including when fallback is enabled.
                    if can_fallback {
                        download_url = &job.metadata.url;
                        using_fallback = true;
                    }
                    sleep(Duration::from_millis(100 * 2_u64.pow(attempt))).await;
                }
            }
        }
        unreachable!("the initial download attempt always runs")
    }

    fn id_list_file_request_args(
        list_url: &str,
        start_index: u64,
        new_file_size: u64,
        id_list_file_id: Option<String>,
    ) -> RequestArgs {
        let (headers, query_params) = if is_default_cdn_url(list_url) {
            (
                None,
                Some(HashMap::from([("range".into(), format!("{start_index}-"))])),
            )
        } else {
            (
                Some(HashMap::from([
                    ("Range".into(), format!("bytes={start_index}-")),
                    (
                        "statsig-id-list-file-size".into(),
                        new_file_size.to_string(),
                    ),
                ])),
                None,
            )
        };

        RequestArgs {
            url: list_url.to_string(),
            headers,
            query_params,
            id_list_file_id,
            // Each request is one attempt in the adapter-owned retry budget.
            diagnostics_key: Some(KeyType::GetIDList),
            retries: 0,
            ..RequestArgs::new()
        }
    }

    fn get_override_id_list_download_url(&self, list_url: &str) -> String {
        let Some(override_api) = &self.download_id_list_file_api else {
            return list_url.to_string();
        };

        replace_url_base(override_api, list_url)
    }

    async fn handle_fallback_request(
        &self,
        fallback_url: &str,
        mut request_args: RequestArgs,
    ) -> Result<Response, StatsigErr> {
        request_args.url = fallback_url.to_owned();

        // TODO add log

        // fallback to cdn, it's a get request
        match self.network.get(request_args.clone()).await {
            Ok(response) => Ok(response),
            Err(e) => Err(StatsigErr::NetworkError(e)),
        }
    }

    async fn handle_manifest_network_error(
        &self,
        request_args: RequestArgs,
        initial_err: NetworkError,
    ) -> Result<IdListsResponse, StatsigErr> {
        if !matches!(initial_err, NetworkError::RetriesExhausted(_, _, _, _)) {
            return Err(StatsigErr::NetworkError(initial_err));
        }

        if let Some(fallback_url) = &self.fallback_url {
            return match self
                .handle_fallback_request(fallback_url, request_args)
                .await
            {
                Ok(response) => self.parse_response(response.data),
                Err(e) => Err(e),
            };
        }

        Err(StatsigErr::NetworkError(initial_err))
    }

    async fn run_background_sync(weak_self: &Weak<Self>) {
        let strong_self = match weak_self.upgrade() {
            Some(s) => s,
            None => return,
        };

        strong_self
            .ops_stats
            .set_diagnostics_context(ContextType::ConfigSync);

        if let Err(e) = strong_self.sync_id_lists().await {
            if let StatsigErr::NetworkError(NetworkError::DisableNetworkOn(_)) = e {
                return;
            }
            log_e!(TAG, "IDList background sync failed {}", e);
        }

        strong_self.ops_stats.enqueue_diagnostics_event(
            Some(KeyType::GetIDListSources),
            Some(ContextType::ConfigSync),
        );
    }

    fn is_cdn_url(&self) -> bool {
        is_default_cdn_id_lists_manifest_url(&self.id_lists_manifest_url)
    }

    fn parse_response(
        &self,
        response: Option<ResponseData>,
    ) -> Result<IdListsResponse, StatsigErr> {
        let mut data = match response {
            Some(r) => r,
            None => {
                let msg = "No ID List results from network".to_string();
                return Err(StatsigErr::JsonParseError(
                    "IdListsResponse".to_owned(),
                    msg,
                ));
            }
        };

        data.deserialize_into::<IdListsResponse>()
            .map_err(|parse_err| {
                let msg = format!("Failed to parse JSON: {parse_err}");
                StatsigErr::JsonParseError(stringify!(IdListsResponse).to_string(), msg)
            })
    }

    fn set_listener(&self, listener: Arc<dyn IdListsUpdateListener>) {
        match self
            .listener
            .try_write_for(std::time::Duration::from_secs(5))
        {
            Some(mut lock) => *lock = Some(listener),
            None => {
                log_error_to_statsig_and_console!(
                    self.ops_stats.clone(),
                    TAG,
                    StatsigErr::LockFailure("Failed to acquire write lock on listener".to_string())
                );
            }
        }
    }

    fn get_current_id_list_metadata(&self) -> Result<HashMap<String, IdListMetadata>, StatsigErr> {
        let lock = match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => lock,
            None => {
                return Err(StatsigErr::LockFailure(
                    "Failed to acquire read lock on listener".to_string(),
                ));
            }
        };

        match lock.as_ref() {
            Some(listener) => Ok(listener.get_current_id_list_metadata()),
            None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
        }
    }

    async fn sync_id_lists(&self) -> Result<(), StatsigErr> {
        let sync_start_ms = Utc::now().timestamp_millis() as u64;
        let mut manifest_success = false;
        let mut successful_downloads = 0;
        let result = self
            .fetch_and_process_id_lists(&mut manifest_success, &mut successful_downloads)
            .await;
        self.log_id_lists_sync_overall_latency(
            sync_start_ms,
            manifest_success,
            successful_downloads,
            result.is_ok(),
        );
        result
    }

    async fn fetch_and_process_id_lists(
        &self,
        manifest_success: &mut bool,
        successful_downloads: &mut u64,
    ) -> Result<(), StatsigErr> {
        let new_manifest = self.fetch_id_list_manifests_from_network().await?;
        *manifest_success = true;
        // Capture both manifests once; retries never reread committed metadata.
        let curr_manifest = self.get_current_id_list_metadata()?;
        self.add_diagnostics_start_marker(
            KeyType::GetIDListSources,
            StepType::Process,
            Some(new_manifest.len()),
            None,
        );
        let result = self
            .process_id_lists(new_manifest, curr_manifest, successful_downloads)
            .await;
        self.add_diagnostics_end_marker(
            KeyType::GetIDListSources,
            StepType::Process,
            result.is_ok(),
            None,
            None,
        );
        result
    }

    async fn process_id_lists(
        &self,
        new_manifest: IdListsResponse,
        curr_manifest: IdListsResponse,
        successful_downloads: &mut u64,
    ) -> Result<(), StatsigErr> {
        let mut jobs = Vec::new();
        let mut updates = HashMap::new();
        for (name, metadata) in new_manifest {
            let range_start = match curr_manifest.get(&name) {
                Some(current)
                    if metadata.creation_time > current.creation_time
                        || metadata.file_id != current.file_id =>
                {
                    Some(0)
                }
                Some(current) if metadata.size > current.size => Some(current.size),
                Some(_) => None,
                None => Some(0),
            };
            if let Some(range_start) = range_start {
                jobs.push(IdListDownloadJob {
                    name,
                    url: self.get_override_id_list_download_url(&metadata.url),
                    metadata,
                    range_start,
                });
            } else {
                updates.insert(
                    name,
                    IdListUpdate {
                        raw_changeset: None,
                        new_metadata: metadata,
                    },
                );
            }
        }
        // Stable launch order also makes failures reproducible across manifest map orderings.
        jobs.sort_by(|a, b| a.name.cmp(&b.name));
        let mut downloads = stream::iter(jobs.into_iter().map(|job| async move {
            let result = self.download_id_list(&job).await;
            (job, result)
        }))
        .buffer_unordered(ID_LIST_DOWNLOAD_CONCURRENCY);
        let mut failures = Vec::new();
        while let Some((job, result)) = downloads.next().await {
            match result {
                Ok(raw_changeset) => {
                    *successful_downloads += 1;
                    updates.insert(
                        job.name,
                        IdListUpdate {
                            raw_changeset: Some(raw_changeset),
                            new_metadata: job.metadata,
                        },
                    );
                }
                Err(error) => {
                    // Drain every job so independent downloads can finish their retry budgets.
                    failures.push((job.name, error));
                }
            }
        }
        if !failures.is_empty() {
            let summary = failures
                .iter()
                .map(|(name, error)| format!("{name}: {error}"))
                .collect::<Vec<_>>()
                .join("; ");
            log_e!(TAG, "ID list refresh failed: {}", summary);
            return Err(failures.swap_remove(0).1);
        }
        match self
            .listener
            .try_read_for(std::time::Duration::from_secs(5))
        {
            Some(lock) => match lock.as_ref() {
                Some(listener) => {
                    listener.did_receive_id_list_updates(updates);
                    Ok(())
                }
                None => Err(StatsigErr::UnstartedAdapter("Listener not set".to_string())),
            },
            None => {
                let error = "Failed to acquire read lock on listener".to_string();
                log_error_to_statsig_and_console!(
                    self.ops_stats.clone(),
                    TAG,
                    StatsigErr::LockFailure(error.clone())
                );
                Err(StatsigErr::LockFailure(error))
            }
        }
    }

    // ---- Helper functions for monioring ID List ----
    fn add_diagnostics_start_marker(
        &self,
        key: KeyType,
        step: StepType,
        id_list_count: Option<usize>,
        url: Option<String>,
    ) {
        let mut marker = Marker::new(key, ActionType::Start, Some(step));
        if let Some(count) = id_list_count {
            marker = marker.with_id_list_count(count);
        }
        if let Some(url) = url {
            marker = marker.with_url(url);
        }
        self.ops_stats.add_marker(marker, None);
    }

    fn add_diagnostics_end_marker(
        &self,
        key: KeyType,
        step: StepType,
        success: bool,
        status_code: Option<u16>,
        url: Option<String>,
    ) {
        let mut marker = Marker::new(key, ActionType::End, Some(step)).with_is_success(success);
        if let Some(status_code) = status_code {
            marker = marker.with_status_code(status_code);
        }
        if let Some(url) = url {
            marker = marker.with_url(url);
        }
        self.ops_stats.add_marker(marker, None);
    }

    fn log_id_lists_sync_overall_latency(
        &self,
        sync_start_ms: u64,
        id_list_manifest_success: bool,
        successful_single_id_list_number: u64,
        success: bool,
    ) {
        let latency_ms =
            (Utc::now().timestamp_millis() as u64).saturating_sub(sync_start_ms) as f64;
        self.ops_stats.log(ObservabilityEvent::new_event(
            MetricType::Dist,
            ID_LISTS_SYNC_OVERALL_LATENCY_METRIC.to_string(),
            latency_ms,
            Some(HashMap::from([
                ("id_lists_sync_success".into(), success.to_string()),
                (
                    ID_LISTS_SYNC_OVERALL_MANIFEST_SUCCESS_TAG.to_string(),
                    id_list_manifest_success.to_string(),
                ),
                (
                    ID_LISTS_SYNC_OVERALL_SUCCEED_SINGLE_ID_LIST_NUMBER_TAG.to_string(),
                    successful_single_id_list_number.to_string(),
                ),
            ])),
        ));
    }
}

struct IdListDownloadJob {
    name: String,
    url: String,
    metadata: IdListMetadata,
    range_start: u64,
}

fn is_retryable_download_error(error: &StatsigErr) -> bool {
    match error {
        StatsigErr::SerializationError(_) => true,
        StatsigErr::NetworkError(
            NetworkError::RequestFailed(_, status, _)
            | NetworkError::RetriesExhausted(_, status, _, _),
        ) => !matches!(status, Some(400 | 401 | 403 | 405 | 413 | 429 | 501)),
        _ => false,
    }
}

#[async_trait]
impl IdListsAdapter for StatsigHttpIdListsAdapter {
    async fn start(
        self: Arc<Self>,
        _statsig_runtime: &Arc<StatsigRuntime>,
        listener: Arc<dyn IdListsUpdateListener + Send + Sync>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.set_listener(listener);
                self.ops_stats
                    .set_diagnostics_context(ContextType::Initialize);
                let result = self.sync_id_lists().await;
                result?;
                Ok(())
            })
            .await
    }

    async fn shutdown(&self, _timeout: Duration) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                self.shutdown_notify.notify_one();
                Ok(())
            })
            .await
    }

    async fn schedule_background_sync(
        self: Arc<Self>,
        statsig_runtime: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        self.output_policy
            .scope(async {
                let weak_self = Arc::downgrade(&self);
                let interval_duration = self.sync_interval_duration;

                statsig_runtime.spawn(
            "http_id_list_bg_sync",
            move |rt_shutdown_notify| async move {
                loop {
                    tokio::select! {
                        () = sleep(interval_duration) => {
                            Self::run_background_sync(&weak_self).await;
                        }
                        () = rt_shutdown_notify.notified() => {
                            log_d!(TAG, "Runtime shutdown. Shutting down id list background sync");
                            break;
                        },
                        () = self.shutdown_notify.notified() => {
                            log_d!(TAG, "Shutting down id list background sync");
                            break;
                        }
                    }
                }
            },
        )?;

                Ok(())
            })
            .await
    }

    fn get_type_name(&self) -> String {
        TAG.to_string()
    }
}

#[cfg(test)]
mod tests {
    use crate::hashing::HashUtil;
    use crate::id_lists_adapter::IdList;

    use super::*;
    // todo: update to use wiremock instead of mockito
    use mockito::{Mock, Server, ServerGuard};
    use std::fs;
    use std::path::PathBuf;

    struct TestIdListsUpdateListener {
        id_lists: RwLock<HashMap<String, IdList>>,
    }

    impl TestIdListsUpdateListener {
        fn does_list_contain_id(&self, list_name: &str, id: &str) -> bool {
            let id_lists = self
                .id_lists
                .try_read_for(std::time::Duration::from_secs(5))
                .unwrap();
            if let Some(list) = id_lists.get(list_name) {
                list.ids.contains(id)
            } else {
                false
            }
        }

        async fn does_list_contain_id_eventually(
            &self,
            list_name: &str,
            id: &str,
            timeout_duration: Duration,
        ) -> bool {
            let start = tokio::time::Instant::now();
            loop {
                if self.does_list_contain_id(list_name, id) {
                    return true;
                }

                if start.elapsed() >= timeout_duration {
                    return false;
                }

                sleep(Duration::from_millis(10)).await;
            }
        }
    }

    impl IdListsUpdateListener for TestIdListsUpdateListener {
        fn get_current_id_list_metadata(&self) -> HashMap<String, IdListMetadata> {
            self.id_lists
                .try_read_for(std::time::Duration::from_secs(5))
                .unwrap()
                .iter()
                .map(|(key, list)| (key.clone(), list.metadata.clone()))
                .collect()
        }

        fn did_receive_id_list_updates(&self, updates: HashMap<String, IdListUpdate>) {
            let mut id_lists = self
                .id_lists
                .try_write_for(std::time::Duration::from_secs(5))
                .unwrap();

            // delete any id_lists that are not in the changesets
            id_lists.retain(|list_name, _| updates.contains_key(list_name));

            for (list_name, update) in updates {
                if let Some(entry) = id_lists.get_mut(&list_name) {
                    // update existing
                    entry.apply_update(update);
                } else {
                    // add new
                    let mut list = IdList::new(update.new_metadata.clone());
                    list.apply_update(update);
                    id_lists.insert(list_name.clone(), list);
                }
            }
        }
    }

    fn get_hashed_marcos() -> String {
        let hashed = HashUtil::new().sha256("Marcos");
        hashed.chars().take(8).collect()
    }

    async fn setup_mock_server() -> (ServerGuard, Mock, Mock) {
        let mut server = Server::new_async().await;
        let mock_server_url = server.url();

        let id_lists_response_path = PathBuf::from(format!(
            "{}/tests/data/get_id_lists.json",
            env!("CARGO_MANIFEST_DIR")
        ));

        let id_lists_response = fs::read_to_string(id_lists_response_path)
            .unwrap()
            .replace("URL_REPLACE", &format!("{mock_server_url}/id_lists"));

        let mocked_get_id_lists = server
            .mock("POST", "/get_id_lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(id_lists_response)
            .create();

        let company_ids_response_path = PathBuf::from(format!(
            "{}/tests/data/company_id_list",
            env!("CARGO_MANIFEST_DIR")
        ));

        let company_ids_response = fs::read_to_string(company_ids_response_path)
            .unwrap()
            .replace("URL_REPLACE", &format!("{mock_server_url}/id_lists"));

        let mocked_individual_id_list = server
            .mock("GET", "/id_lists/company_id_list")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(company_ids_response)
            .create();

        (server, mocked_get_id_lists, mocked_individual_id_list)
    }

    async fn setup(
        id_lists_sync_interval_ms: Option<u32>,
    ) -> (
        ServerGuard,
        Arc<StatsigHttpIdListsAdapter>,
        Arc<TestIdListsUpdateListener>,
        Arc<StatsigRuntime>,
    ) {
        let (server, _, _) = setup_mock_server().await;

        let options = StatsigOptions {
            id_lists_url: Some(format!("{}/get_id_lists", server.url())),
            id_lists_sync_interval_ms,
            wait_for_country_lookup_init: Some(true),
            wait_for_user_agent_init: Some(true),
            ..StatsigOptions::default()
        };

        let adapter = Arc::new(StatsigHttpIdListsAdapter::new("secret-key", &options));
        let listener = Arc::new(TestIdListsUpdateListener {
            id_lists: RwLock::new(HashMap::new()),
        });

        let statsig_rt = StatsigRuntime::get_runtime();
        adapter
            .clone()
            .start(&statsig_rt, listener.clone())
            .await
            .unwrap();

        (server, adapter, listener, statsig_rt)
    }

    #[tokio::test]
    async fn test_id_list_download_uses_override_api() {
        let mut manifest_server = Server::new_async().await;
        let mut download_server = Server::new_async().await;

        let id_lists_response_path = PathBuf::from(format!(
            "{}/tests/data/get_id_lists.json",
            env!("CARGO_MANIFEST_DIR")
        ));
        let id_lists_response = fs::read_to_string(id_lists_response_path).unwrap().replace(
            "URL_REPLACE",
            "https://fake-id-list-host/v1/download_id_list_file",
        );

        let mocked_get_id_lists = manifest_server
            .mock("POST", "/get_id_lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(id_lists_response)
            .create();

        let company_ids_response_path = PathBuf::from(format!(
            "{}/tests/data/company_id_list",
            env!("CARGO_MANIFEST_DIR")
        ));
        let company_ids_response = fs::read_to_string(company_ids_response_path)
            .unwrap()
            .replace(
                "URL_REPLACE",
                "https://fake-id-list-host/v1/download_id_list_file",
            );

        let mocked_individual_id_list = download_server
            .mock("GET", "/v1/download_id_list_file/company_id_list")
            .match_header("range", "bytes=0-")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(company_ids_response)
            .create();

        let options = StatsigOptions {
            id_lists_url: Some(format!("{}/get_id_lists", manifest_server.url())),
            download_id_list_file_api: Some(download_server.url()),
            wait_for_country_lookup_init: Some(true),
            wait_for_user_agent_init: Some(true),
            ..StatsigOptions::default()
        };

        let adapter = Arc::new(StatsigHttpIdListsAdapter::new("secret-key", &options));
        let listener = Arc::new(TestIdListsUpdateListener {
            id_lists: RwLock::new(HashMap::new()),
        });

        let statsig_rt = StatsigRuntime::get_runtime();
        adapter
            .clone()
            .start(&statsig_rt, listener.clone())
            .await
            .unwrap();

        mocked_get_id_lists.assert();
        mocked_individual_id_list.assert();
        assert!(listener.does_list_contain_id("company_id_list", &get_hashed_marcos()));
    }

    #[tokio::test]
    async fn test_id_list_download_passes_file_size_with_range_header() {
        let mut manifest_server = Server::new_async().await;
        let mut download_server = Server::new_async().await;

        let existing_list_size = 10_u64;
        let new_list_size = existing_list_size + 1;
        let existing_creation_time = 1721417546000_i64;
        let file_id = "4t0BEqak3w1UcidsPcpQXN".to_string();
        let manifest_download_url = "https://fake-id-list-host/v1/download_id_list_file";
        let expected_range_start = existing_list_size;
        let expected_file_size = new_list_size.to_string();
        let expected_range_header = format!("bytes={expected_range_start}-");

        let manifest_response = format!(
            r#"{{
  "company_id_list": {{
    "name": "company_id_list",
    "size": {},
    "url": "{}/company_id_list",
    "creationTime": {},
    "fileID": "{}"
  }}
}}"#,
            new_list_size, manifest_download_url, existing_creation_time, file_id
        );

        let mocked_get_id_lists = manifest_server
            .mock("POST", "/get_id_lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(manifest_response)
            .create();

        let mocked_individual_id_list = download_server
            .mock("GET", "/v1/download_id_list_file/company_id_list")
            .match_header("range", expected_range_header.as_str())
            .match_header("statsig-id-list-file-size", expected_file_size.as_str())
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body("+2Tv4fIVX\n")
            .create();

        let options = StatsigOptions {
            id_lists_url: Some(format!("{}/get_id_lists", manifest_server.url())),
            download_id_list_file_api: Some(download_server.url()),
            wait_for_country_lookup_init: Some(true),
            wait_for_user_agent_init: Some(true),
            ..StatsigOptions::default()
        };

        let adapter = Arc::new(StatsigHttpIdListsAdapter::new("secret-key", &options));
        let listener = Arc::new(TestIdListsUpdateListener {
            id_lists: RwLock::new(HashMap::new()),
        });

        {
            let mut existing_lists = listener
                .id_lists
                .try_write_for(std::time::Duration::from_secs(5))
                .unwrap();

            let mut local_list = IdList::new(IdListMetadata {
                name: "company_id_list".to_string(),
                url: format!("{}/company_id_list", manifest_download_url),
                file_id: Some(file_id),
                size: existing_list_size,
                creation_time: existing_creation_time,
            });
            local_list.metadata.size = existing_list_size;
            existing_lists.insert("company_id_list".to_string(), local_list);
        }

        let statsig_rt = StatsigRuntime::get_runtime();
        adapter
            .clone()
            .start(&statsig_rt, listener.clone())
            .await
            .unwrap();

        mocked_get_id_lists.assert();
        mocked_individual_id_list.assert();
        assert!(listener.does_list_contain_id("company_id_list", "2Tv4fIVX"));
    }

    #[test]
    fn test_override_id_list_download_url_preserves_manifest_path_suffix() {
        let options = StatsigOptions {
            download_id_list_file_api: Some("https://download-proxy.example".to_string()),
            ..StatsigOptions::default()
        };

        let adapter = StatsigHttpIdListsAdapter::new("secret-key", &options);
        let manifest_download_url =
            "https://fake-id-list-host/v1/download_id_list_file/3wHgh0FhoQH0p";

        let actual = adapter.get_override_id_list_download_url(manifest_download_url);

        assert_eq!(
            actual,
            "https://download-proxy.example/v1/download_id_list_file/3wHgh0FhoQH0p"
        );
    }

    #[test]
    fn test_normalizes_default_cdn_manifest_url_prefix() {
        for id_lists_url in [
            DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX,
            "https://statsigcdn.openai.com/v1/get_id_lists/",
            "https://statsigcdn.openai.com:443/v1/get_id_lists",
            "https://statsigcdn.openai.com:443/v1/get_id_lists/",
        ] {
            let options = StatsigOptions {
                id_lists_url: Some(id_lists_url.to_string()),
                ..StatsigOptions::default()
            };

            let adapter = StatsigHttpIdListsAdapter::new("secret-key", &options);

            assert_eq!(
                adapter.id_lists_manifest_url, DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX,
                "failed to normalize {id_lists_url}"
            );
            assert!(adapter.is_cdn_url());
        }
    }

    #[test]
    fn test_default_manifest_url_is_keyless() {
        let adapter = StatsigHttpIdListsAdapter::new("secret-key", &StatsigOptions::default());

        assert_eq!(
            adapter.id_lists_manifest_url,
            DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX
        );
        assert!(adapter.is_cdn_url());
    }

    #[test]
    fn test_preserves_custom_id_lists_manifest_urls() {
        for id_lists_url in [
            "https://statsigcdn.openai.com/v1/get_id_lists/secret-existing.json",
            "https://statsigcdn.openai.com/v1/get_id_lists?token=example",
            "https://statsigcdn.openai.com:8443/v1/get_id_lists",
            "https://statsigcdn.openai.com:443@proxy.example/v1/get_id_lists",
            "https://api.oaistatsig.com/v1/get_id_lists",
            "https://proxy.example/v1/get_id_lists",
        ] {
            let options = StatsigOptions {
                id_lists_url: Some(id_lists_url.to_string()),
                ..StatsigOptions::default()
            };

            let adapter = StatsigHttpIdListsAdapter::new("secret-key", &options);

            assert_eq!(
                adapter.id_lists_manifest_url, id_lists_url,
                "unexpectedly rewrote {id_lists_url}"
            );
        }
    }

    #[test]
    fn test_preserves_custom_proxy_id_lists_fallback_behavior() {
        let id_lists_url = "https://proxy.example/v1/get_id_lists?upstream=https://statsigcdn.openai.com/v1/get_id_lists";
        let options = StatsigOptions {
            id_lists_url: Some(id_lists_url.to_string()),
            fallback_to_statsig_api: Some(true),
            ..StatsigOptions::default()
        };

        let adapter = StatsigHttpIdListsAdapter::new("secret-key", &options);

        assert_eq!(adapter.id_lists_manifest_url, id_lists_url);
        assert!(!adapter.is_cdn_url());
        assert!(adapter.fallback_url.is_none());
    }

    #[test]
    fn test_custom_id_lists_manifest_can_fall_back_to_default_cdn() {
        let options = StatsigOptions {
            id_lists_url: Some("https://proxy.example/v1/get_id_lists".to_string()),
            fallback_to_statsig_api: Some(true),
            ..StatsigOptions::default()
        };

        let adapter = StatsigHttpIdListsAdapter::new("secret-key", &options);
        let expected_fallback = DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX;

        assert_eq!(adapter.fallback_url.as_deref(), Some(expected_fallback));
    }

    #[tokio::test]
    async fn test_syncing_new_id_lists() {
        let (_server, adapter, listener, _statsig_rt) = setup(None).await;

        adapter.sync_id_lists().await.unwrap();

        let result = listener.does_list_contain_id("company_id_list", &get_hashed_marcos());
        assert!(result);
    }

    #[tokio::test]
    async fn test_syncing_deleting_id_lists() {
        let (mut server, adapter, listener, _statsig_rt) = setup(None).await;

        adapter.sync_id_lists().await.unwrap();

        server
            .mock("POST", "/get_id_lists")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body("{}")
            .create();

        adapter.sync_id_lists().await.unwrap();

        let result = listener.does_list_contain_id("company_id_list", &get_hashed_marcos());
        assert!(!result);
    }

    #[tokio::test]
    async fn test_bg_syncing() {
        let (_server, _adapter, listener, _statsig_rt) = setup(Some(1)).await;

        let result = listener
            .does_list_contain_id_eventually(
                "company_id_list",
                &get_hashed_marcos(),
                Duration::from_millis(100),
            )
            .await;
        assert!(result);
    }

    #[tokio::test]
    async fn test_bg_sync_shutdown() {
        let (_server, adapter, listener, statsig_rt) = setup(Some(10)).await;

        statsig_rt.shutdown();
        let _ = adapter.shutdown(Duration::from_millis(1)).await;

        let result = listener
            .does_list_contain_id_eventually(
                "company_id_list",
                &get_hashed_marcos(),
                Duration::from_millis(100),
            )
            .await;

        assert!(result);
    }

    impl StatsigHttpIdListsAdapter {
        async fn fetch_individual_id_list_changes_from_network(
            &self,
            url: &str,
            range_start: u64,
            size: u64,
            file_id: Option<String>,
        ) -> Result<String, StatsigErr> {
            self.download_id_list(&IdListDownloadJob {
                name: "test-list".into(),
                url: self.get_override_id_list_download_url(url),
                metadata: IdListMetadata {
                    name: "test-list".into(),
                    url: url.into(),
                    size,
                    file_id,
                    creation_time: 0,
                },
                range_start,
            })
            .await
        }
    }

    const TEST_CDN_BASE: &str = "https://statsigcdn.openai.com";
    const TEST_CDN_FILE: &str = "https://statsigcdn.openai.com/file";

    struct LocalCdnProvider {
        origin: String,
        delegate: Arc<dyn crate::networking::NetworkProvider>,
        requests: RwLock<Vec<RequestArgs>>,
    }

    impl LocalCdnProvider {
        fn local_args(&self, args: &RequestArgs) -> RequestArgs {
            self.requests.write().push(args.clone());
            let mut local_args = args.clone();
            if let Some(path) = args.url.strip_prefix(&format!("{TEST_CDN_BASE}/")) {
                local_args.url = format!("{}/{path}", self.origin);
            }
            let local_url = url::Url::parse(&local_args.url).unwrap();
            assert_eq!(local_url.scheme(), "http");
            assert_eq!(local_url.host_str(), Some("127.0.0.1"));
            assert!(local_url.port().is_some());
            local_args
        }
    }

    #[async_trait]
    impl crate::networking::NetworkProvider for LocalCdnProvider {
        async fn send(
            &self,
            method: &crate::networking::HttpMethod,
            args: &RequestArgs,
        ) -> Response {
            self.delegate.send(method, &self.local_args(args)).await
        }

        async fn send_without_redirects(
            &self,
            method: &crate::networking::HttpMethod,
            args: &RequestArgs,
        ) -> Response {
            self.delegate
                .send_without_redirects(method, &self.local_args(args))
                .await
        }
    }

    // Retain the provider beside the adapter: NetworkClient holds only a Weak reference.
    fn with_local_cdn(
        mut adapter: StatsigHttpIdListsAdapter,
        origin: &ServerGuard,
    ) -> (StatsigHttpIdListsAdapter, Arc<LocalCdnProvider>) {
        let provider = Arc::new(LocalCdnProvider {
            origin: origin.url(),
            delegate: crate::networking::providers::get_network_provider()
                .upgrade()
                .unwrap(),
            requests: RwLock::new(Vec::new()),
        });
        let network_provider: Arc<dyn crate::networking::NetworkProvider> = provider.clone();
        adapter
            .network
            .set_network_provider_for_test(Arc::downgrade(&network_provider));
        (adapter, provider)
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_preserves_initial_and_incremental_membership() {
        let mut manifest_server = Server::new_async().await;
        let mut proxy = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let path = "/v1/download_id_list_file/company%2Fids?token=a%2Bb";
        let url = format!("{TEST_CDN_BASE}{path}");
        let adapter = StatsigHttpIdListsAdapter::new(
            "secret-key",
            &StatsigOptions {
                id_lists_url: Some(format!("{}/get_id_lists", manifest_server.url())),
                download_id_list_file_api: Some(proxy.url()),
                fallback_to_statsig_api: Some(true),
                ..StatsigOptions::default()
            },
        );
        let (adapter, provider) = with_local_cdn(adapter, &origin);
        let listener = Arc::new(TestIdListsUpdateListener {
            id_lists: RwLock::new(HashMap::new()),
        });
        adapter.set_listener(listener.clone());
        let marcos = get_hashed_marcos();
        let initial = format!("+{marcos}\n+retained\n");
        let delta = format!("-{marcos}\n+new-id\n");
        let mut size = 0;
        for body in [&initial, &delta] {
            let start = size;
            size += body.len() as u64;
            let manifest = manifest_server
                .mock("POST", "/get_id_lists")
                .with_status(200)
                .with_body(
                    serde_json::json!({"company_id_list": {
                        "name": "company_id_list", "size": size, "url": url,
                        "creationTime": 1, "fileID": "stable-file"
                    }})
                    .to_string(),
                )
                .expect(1)
                .create();
            let primary = proxy
                .mock("GET", path)
                .match_header("range", format!("bytes={start}-").as_str())
                .match_header("statsig-id-list-file-size", size.to_string().as_str())
                .match_header("statsig-api-key", "secret-key")
                .with_status(503)
                .expect(1)
                .create();
            let fallback = origin
                .mock("GET", format!("{path}&range={start}-").as_str())
                .match_header("range", mockito::Matcher::Missing)
                .match_header("statsig-id-list-file-size", mockito::Matcher::Missing)
                .match_header("statsig-api-key", "secret-key")
                .with_status(200)
                .with_body(body)
                .expect(1)
                .create();
            adapter.sync_id_lists().await.unwrap();
            manifest.assert();
            primary.assert();
            fallback.assert();
            let requests = provider.requests.read();
            let cdn_request = requests.last().unwrap();
            assert_eq!(cdn_request.url, url);
            assert_eq!(cdn_request.id_list_file_id.as_deref(), Some("stable-file"));
            assert_eq!(
                cdn_request.query_params.as_ref().unwrap()["range"],
                format!("{start}-")
            );
            assert_eq!(cdn_request.diagnostics_key, Some(KeyType::GetIDList));
            assert!(listener.does_list_contain_id("company_id_list", "retained"));
            assert_eq!(
                listener.does_list_contain_id("company_id_list", &marcos),
                start == 0
            );
            assert_eq!(
                listener.does_list_contain_id("company_id_list", "new-id"),
                start != 0
            );
            assert_eq!(
                listener.get_current_id_list_metadata()["company_id_list"].size,
                size
            );
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_requires_explicit_opt_in() {
        for enabled in [None, Some(false)] {
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let primary = proxy
                .mock("GET", "/file")
                .with_status(503)
                .expect(3)
                .create();
            let fallback = origin.mock("GET", mockito::Matcher::Any).expect(0).create();
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: Some(proxy.url()),
                    fallback_to_statsig_api: enabled,
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            assert!(
                adapter
                    .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None,)
                    .await
                    .is_err()
            );
            primary.assert();
            fallback.assert();
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_shares_total_attempt_budget_including_zero() {
        for retries in [0, 1, 2] {
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let primary = proxy
                .mock("GET", "/file")
                .with_status(503)
                .expect(1)
                .create();
            let fallback = origin
                .mock("GET", "/file?range=0-")
                .with_status(502)
                .expect(retries as usize)
                .create();
            let mut adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: Some(proxy.url()),
                    fallback_to_statsig_api: Some(true),
                    ..StatsigOptions::default()
                },
            );
            adapter.download_retry_count = retries;
            let (adapter, provider) = with_local_cdn(adapter, &origin);
            let error = adapter
                .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None)
                .await
                .unwrap_err();
            assert!(
                matches!(error, StatsigErr::NetworkError(NetworkError::RetriesExhausted(_, _, attempts, _)) if attempts == retries + 1)
            );
            primary.assert();
            fallback.assert();
            let requests = provider.requests.read();
            assert_eq!(requests.len(), retries as usize + 1);
            assert_eq!(requests[0].url, format!("{}/file", proxy.url()));
            assert!(
                requests[1..]
                    .iter()
                    .all(|request| request.url == TEST_CDN_FILE && request.retries == 0)
            );
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_skips_success_and_terminal_http_statuses() {
        for status in [200, 401, 403, 400, 429] {
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let primary = proxy
                .mock("GET", "/file")
                .with_status(status)
                .with_body("+proxy-id\n")
                .expect(1)
                .create();
            let fallback = origin.mock("GET", mockito::Matcher::Any).expect(0).create();
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: Some(proxy.url()),
                    fallback_to_statsig_api: Some(true),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            let result = adapter
                .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None)
                .await;
            if status == 200 {
                assert_eq!(result.unwrap(), "+proxy-id\n");
            } else {
                assert!(result.is_err(), "status {status} must remain terminal");
            }
            primary.assert();
            fallback.assert();
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_skips_invalid_response_body() {
        let mut proxy = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let primary = proxy
            .mock("GET", "/file")
            .with_status(200)
            .with_body([0xff])
            .expect(1)
            .create();
        let fallback = origin.mock("GET", mockito::Matcher::Any).expect(0).create();
        let adapter = StatsigHttpIdListsAdapter::new(
            "secret-key",
            &StatsigOptions {
                download_id_list_file_api: Some(proxy.url()),
                fallback_to_statsig_api: Some(true),
                ..StatsigOptions::default()
            },
        );
        let (adapter, _provider) = with_local_cdn(adapter, &origin);
        let error = adapter
            .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None)
            .await
            .unwrap_err();
        assert!(matches!(error, StatsigErr::JsonParseError(_, _)));
        primary.assert();
        fallback.assert();
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_does_not_repeat_original_destination() {
        for has_override in [false, true] {
            let mut origin = Server::new_async().await;
            let request = origin
                .mock("GET", "/file?range=0-")
                .with_status(503)
                .expect(3)
                .create();
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: has_override.then(|| TEST_CDN_BASE.to_string()),
                    fallback_to_statsig_api: Some(true),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            assert!(
                adapter
                    .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None,)
                    .await
                    .is_err()
            );
            request.assert();
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_failure_is_bounded_and_returns_origin_error() {
        let mut proxy = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let primary = proxy
            .mock("GET", "/file")
            .with_status(503)
            .expect(1)
            .create();
        let fallback = origin
            .mock("GET", "/file?range=0-")
            .with_status(502)
            .expect(2)
            .create();
        let url = TEST_CDN_FILE.to_string();
        let adapter = StatsigHttpIdListsAdapter::new(
            "secret-key",
            &StatsigOptions {
                download_id_list_file_api: Some(proxy.url()),
                fallback_to_statsig_api: Some(true),
                ..StatsigOptions::default()
            },
        );
        let (adapter, _provider) = with_local_cdn(adapter, &origin);
        let error = adapter
            .fetch_individual_id_list_changes_from_network(&url, 0, 10, None)
            .await
            .unwrap_err();
        assert!(matches!(error,
            StatsigErr::NetworkError(NetworkError::RetriesExhausted(ref failed_url, Some(502), 3, _))
                if failed_url == &url
        ));
        primary.assert();
        fallback.assert();
    }

    #[test]
    fn test_id_list_file_fallback_rebuilds_cdn_range_arguments() {
        let url =
            "https://statsigcdn.openai.com/v1/download_id_list_file/company%2Fids?token=a%2Bb";
        let adapter = StatsigHttpIdListsAdapter::new(
            "secret-key",
            &StatsigOptions {
                download_id_list_file_api: Some("https://proxy.example".to_string()),
                ..StatsigOptions::default()
            },
        );
        let proxy_url = adapter.get_override_id_list_download_url(url);
        assert_eq!(
            proxy_url,
            "https://proxy.example/v1/download_id_list_file/company%2Fids?token=a%2Bb"
        );
        let primary = StatsigHttpIdListsAdapter::id_list_file_request_args(
            &proxy_url,
            17,
            42,
            Some("stable-file".to_string()),
        );
        assert!(primary.query_params.is_none());
        let headers = primary.headers.as_ref().unwrap();
        assert_eq!(headers["Range"], "bytes=17-");
        assert_eq!(headers["statsig-id-list-file-size"], "42");
        let fallback = StatsigHttpIdListsAdapter::id_list_file_request_args(
            url,
            17,
            42,
            primary.id_list_file_id.clone(),
        );
        assert_eq!(fallback.url, url);
        assert!(fallback.headers.is_none());
        assert_eq!(fallback.query_params.as_ref().unwrap()["range"], "17-");
        for args in [primary, fallback] {
            assert_eq!(args.id_list_file_id.as_deref(), Some("stable-file"));
            assert_eq!(args.diagnostics_key, Some(KeyType::GetIDList));
            assert_eq!(args.retries, 0);
        }
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_does_not_follow_redirects() {
        for status in [301, 302, 303, 307, 308] {
            let mut proxy = Server::new_async().await;
            let mut origin = Server::new_async().await;
            let mut foreign = Server::new_async().await;
            let primary = proxy
                .mock("GET", "/file")
                .with_status(503)
                .expect(1)
                .create();
            let fallback = origin
                .mock("GET", "/file?range=17-")
                .match_header("statsig-api-key", "secret-key")
                .with_status(status)
                .with_header("location", &format!("{}/escaped", foreign.url()))
                .expect(2)
                .create();
            let foreign_request = foreign
                .mock("GET", mockito::Matcher::Any)
                .with_status(200)
                .with_body("+foreign-id\n")
                .expect(0)
                .create();
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: Some(proxy.url()),
                    fallback_to_statsig_api: Some(true),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, _provider) = with_local_cdn(adapter, &origin);
            let result = adapter
                .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 17, 42, None)
                .await;

            primary.assert();
            fallback.assert();
            foreign_request.assert();
            assert!(matches!(result,
                Err(StatsigErr::NetworkError(NetworkError::RetriesExhausted(ref url, Some(code), 3, _)))
                    if url == TEST_CDN_FILE && code == status as u16
            ));
        }
    }

    #[tokio::test]
    async fn test_id_list_file_primary_keeps_redirect_behavior() {
        let mut proxy = Server::new_async().await;
        let mut target = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let primary = proxy
            .mock("GET", "/file")
            .with_status(302)
            .with_header("location", &format!("{}/file", target.url()))
            .expect(1)
            .create();
        let redirected = target
            .mock("GET", "/file")
            .with_status(200)
            .with_body("+proxy-id\n")
            .expect(1)
            .create();
        let fallback = origin.mock("GET", mockito::Matcher::Any).expect(0).create();
        let adapter = StatsigHttpIdListsAdapter::new(
            "secret-key",
            &StatsigOptions {
                download_id_list_file_api: Some(proxy.url()),
                fallback_to_statsig_api: Some(true),
                ..StatsigOptions::default()
            },
        );
        let (adapter, _provider) = with_local_cdn(adapter, &origin);
        let body = adapter
            .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None)
            .await
            .unwrap();

        assert_eq!(body, "+proxy-id\n");
        primary.assert();
        redirected.assert();
        fallback.assert();
    }

    #[tokio::test]
    async fn test_id_list_file_fallback_rejects_untrusted_manifest_destinations() {
        let mut proxy = Server::new_async().await;
        let mut foreign = Server::new_async().await;
        let foreign_request = foreign
            .mock("GET", mockito::Matcher::Any)
            .expect(0)
            .create();
        for url in [
            format!("{}/file", foreign.url()),
            "http://statsigcdn.openai.com/file".to_string(),
            "https://statsigcdn.openai.com:8443/file".to_string(),
            "https://statsigcdn.openai.com@foreign.example/file".to_string(),
        ] {
            let primary = proxy
                .mock("GET", "/file")
                .with_status(503)
                .expect(3)
                .create();
            let adapter = StatsigHttpIdListsAdapter::new(
                "secret-key",
                &StatsigOptions {
                    download_id_list_file_api: Some(proxy.url()),
                    fallback_to_statsig_api: Some(true),
                    ..StatsigOptions::default()
                },
            );
            let (adapter, provider) = with_local_cdn(adapter, &foreign);
            let error = adapter
                .fetch_individual_id_list_changes_from_network(&url, 0, 10, None)
                .await
                .unwrap_err();
            let proxy_url = format!("{}/file", proxy.url());
            assert!(matches!(error,
                StatsigErr::NetworkError(NetworkError::RetriesExhausted(ref failed_url, Some(503), _, _))
                    if failed_url == &proxy_url
            ));
            primary.assert();
            foreign_request.assert();
            let requests = provider.requests.read();
            assert_eq!(requests.len(), 3, "unexpected fallback to {url}");
            assert_eq!(requests[0].url, proxy_url);
        }
    }
}

#[cfg(test)]
#[path = "id_list_download_concurrency_tests.rs"]
mod concurrency_tests;

#[cfg(all(test, feature = "custom_network_provider"))]
#[path = "id_lists_refresh_tests.rs"]
mod refresh_tests;
