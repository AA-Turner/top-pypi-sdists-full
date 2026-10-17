use crate::hashing::HashUtil;
use crate::id_lists_adapter::IdList;
use crate::networking::Response;

use super::*;
// todo: update to use wiremock instead of mockito
use mockito::{Mock, Server, ServerGuard};
use std::fs;
use std::path::PathBuf;

pub(super) struct TestIdListsUpdateListener {
    pub(super) id_lists: RwLock<HashMap<String, IdList>>,
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
    let delta = "+2Tv4fIVX\n";
    let new_list_size = existing_list_size + delta.len() as u64;
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
        .with_status(206)
        .with_header(
            "content-range",
            &format!(
                "bytes {existing_list_size}-{}/{new_list_size}",
                new_list_size - 1
            ),
        )
        .with_header("content-type", "application/json")
        .with_body(delta)
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
    let manifest_download_url = "https://fake-id-list-host/v1/download_id_list_file/3wHgh0FhoQH0p";

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
        let job = IdListDownloadJob {
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
        };
        self.network
            .retry_executor(DEFAULT_RETRY_POLICY)
            .run(
                |fallback, index| self.download_id_list(&job, fallback, index),
                |error| retryable_state_error(error).then_some(u32::MAX),
                |outcome| outcome == PrimaryOutcome::Exhausted && self.file_can_fallback(&job),
                || StatsigErr::TaskShutdownFailure,
            )
            .await
            .map(|(body, _)| body)
    }
}

const TEST_CDN_BASE: &str = "https://statsigcdn.openai.com";
const TEST_CDN_FILE: &str = "https://statsigcdn.openai.com/file";

pub(super) struct LocalCdnProvider {
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
    async fn send(&self, method: &crate::networking::HttpMethod, args: &RequestArgs) -> Response {
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
pub(super) fn with_local_cdn(
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
async fn test_id_list_file_fallback_requires_explicit_opt_in() {
    for enabled in [None, Some(false)] {
        let mut proxy = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let primary = proxy
            .mock("GET", "/file")
            .with_status(503)
            .expect(2)
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
async fn test_id_list_file_exhausts_primary_before_one_fallback() {
    let mut proxy = Server::new_async().await;
    let mut origin = Server::new_async().await;
    let primary = proxy
        .mock("GET", "/file")
        .with_status(503)
        .expect(2)
        .create();
    let fallback = origin
        .mock("GET", "/file")
        .with_status(502)
        .expect(1)
        .create();
    let adapter = StatsigHttpIdListsAdapter::new(
        "secret-key",
        &StatsigOptions {
            download_id_list_file_api: Some(proxy.url()),
            fallback_to_statsig_api: Some(true),
            ..StatsigOptions::default()
        },
    );
    let (adapter, provider) = with_local_cdn(adapter, &origin);
    assert!(
        adapter
            .fetch_individual_id_list_changes_from_network(TEST_CDN_FILE, 0, 10, None)
            .await
            .is_err()
    );
    primary.assert();
    fallback.assert();
    let requests = provider.requests.read();
    assert_eq!(requests.len(), 3);
    assert!(
        requests[..2]
            .iter()
            .all(|r| r.url == format!("{}/file", proxy.url()) && r.retries == 0)
    );
    assert_eq!(requests[2].url, TEST_CDN_FILE);
    assert_eq!(requests[2].retries, 0);
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
            .mock("GET", "/file")
            .match_header("range", "bytes=0-")
            .with_status(503)
            .expect(2)
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
        .expect(2)
        .create();
    let fallback = origin
        .mock("GET", "/file")
        .with_status(502)
        .expect(1)
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

#[tokio::test]
async fn test_id_list_file_fallback_does_not_follow_redirects() {
    for status in [301, 302, 303, 307, 308] {
        let mut proxy = Server::new_async().await;
        let mut origin = Server::new_async().await;
        let mut foreign = Server::new_async().await;
        let primary = proxy
            .mock("GET", "/file")
            .with_status(503)
            .expect(2)
            .create();
        let fallback = origin
            .mock("GET", "/file")
            .match_header("statsig-api-key", "secret-key")
            .with_status(status)
            .with_header("location", &format!("{}/escaped", foreign.url()))
            .expect(1)
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
            .expect(2)
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
            StatsigErr::NetworkError(NetworkError::RetriesExhausted(ref failed_url, Some(503), 2, _))
                if failed_url == &proxy_url
        ));
        primary.assert();
        foreign_request.assert();
        let requests = provider.requests.read();
        assert_eq!(requests.len(), 2, "unexpected fallback to {url}");
        assert_eq!(requests[0].url, proxy_url);
    }
}
