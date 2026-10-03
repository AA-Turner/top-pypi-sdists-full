use std::sync::{
    Arc, Mutex,
    atomic::{AtomicBool, AtomicUsize, Ordering},
};

use async_trait::async_trait;
use statsig_rust::{
    StatsigErr,
    data_store_interface::{
        DataStoreBytesResponse, DataStoreGetBytesRequest, DataStoreResponse, DataStoreTrait,
        RequestPath,
    },
};
use tokio::sync::Semaphore;

#[derive(Default)]
struct MockDataStoreByteCache {
    brotli_proto: Option<Vec<u8>>,
    zstd_proto: Option<Vec<u8>>,
    json: Option<Vec<u8>>,
}

pub struct MockDataStore {
    response: Mutex<Option<DataStoreResponse>>,
    byte_cache: Mutex<MockDataStoreByteCache>,
    get_bytes_error: Mutex<Option<String>>,
    supports_polling: bool,
    byte_cache_enabled: bool,
    read_only: bool,
    write_once: bool,
    set_bytes_failures: AtomicUsize,
    set_bytes_gate: Option<Semaphore>,
    set_bytes_started: Semaphore,
    set_bytes_payloads: Mutex<Vec<Vec<u8>>>,
    read_only_once: AtomicBool,
    read_only_after_first_check: bool,
    read_only_call_count: AtomicUsize,
    get_call_count: Arc<AtomicUsize>,
    get_bytes_call_count: Arc<AtomicUsize>,
    zstd_get_bytes_call_count: Arc<AtomicUsize>,
    set_call_count: Arc<AtomicUsize>,
    set_bytes_call_count: Arc<AtomicUsize>,
}

impl MockDataStore {
    pub fn new(supports_polling: bool) -> Self {
        Self {
            response: Mutex::new(None),
            byte_cache: Mutex::new(MockDataStoreByteCache::default()),
            get_bytes_error: Mutex::new(None),
            supports_polling,
            byte_cache_enabled: false,
            read_only: false,
            write_once: false,
            set_bytes_failures: AtomicUsize::new(0),
            set_bytes_gate: None,
            set_bytes_started: Semaphore::new(0),
            set_bytes_payloads: Mutex::new(Vec::new()),
            read_only_once: AtomicBool::new(false),
            read_only_after_first_check: false,
            read_only_call_count: AtomicUsize::new(0),
            get_call_count: Arc::new(AtomicUsize::new(0)),
            get_bytes_call_count: Arc::new(AtomicUsize::new(0)),
            zstd_get_bytes_call_count: Arc::new(AtomicUsize::new(0)),
            set_call_count: Arc::new(AtomicUsize::new(0)),
            set_bytes_call_count: Arc::new(AtomicUsize::new(0)),
        }
    }

    pub fn new_with_byte_cache(supports_polling: bool) -> Self {
        Self {
            byte_cache_enabled: true,
            ..Self::new(supports_polling)
        }
    }

    pub fn with_read_only(mut self, read_only: bool) -> Self {
        self.read_only = read_only;
        self
    }

    pub fn with_write_once(mut self) -> Self {
        self.write_once = true;
        self
    }

    pub fn with_set_bytes_failures(mut self, count: usize) -> Self {
        self.set_bytes_failures = AtomicUsize::new(count);
        self
    }

    pub fn with_blocked_set_bytes(mut self) -> Self {
        self.set_bytes_gate = Some(Semaphore::new(0));
        self
    }

    pub async fn wait_for_set_bytes_call(&self) {
        tokio::time::timeout(
            std::time::Duration::from_secs(5),
            self.set_bytes_started.acquire(),
        )
        .await
        .expect("datastore publication should start")
        .unwrap()
        .forget();
    }

    pub fn release_set_bytes_calls(&self, count: usize) {
        self.set_bytes_gate.as_ref().unwrap().add_permits(count);
    }

    pub fn set_bytes_payloads(&self) -> Vec<Vec<u8>> {
        self.set_bytes_payloads.lock().unwrap().clone()
    }

    pub fn with_read_only_once(mut self) -> Self {
        self.read_only_once = AtomicBool::new(true);
        self
    }

    pub fn with_read_only_after_first_check(mut self) -> Self {
        self.read_only_after_first_check = true;
        self
    }

    pub fn with_proto_cache(proto: &[u8]) -> Self {
        let store = Self::new_with_byte_cache(false);
        store.mock_proto_bytes(proto);
        store
    }

    pub fn with_json_cache(json: &str) -> Self {
        let store = Self::new_with_byte_cache(false);
        store.mock_json_bytes(json);
        store
    }

    pub fn with_zstd_proto_cache(proto: &[u8]) -> Self {
        let store = Self::new_with_byte_cache(false);
        store.mock_zstd_proto_bytes(proto);
        store
    }

    pub async fn mock_response(&self, response: DataStoreResponse) {
        let mut lock = self.response.lock().unwrap();
        *lock = Some(response);
    }

    pub fn mock_proto_bytes(&self, proto: &[u8]) {
        self.byte_cache.lock().unwrap().brotli_proto = Some(proto.to_vec());
    }

    pub fn mock_zstd_proto_bytes(&self, proto: &[u8]) {
        self.byte_cache.lock().unwrap().zstd_proto = Some(proto.to_vec());
    }

    pub fn mock_json_bytes(&self, json: &str) {
        self.byte_cache.lock().unwrap().json = Some(json.as_bytes().to_vec());
    }

    pub fn mock_get_bytes_error(&self, message: &str) {
        *self.get_bytes_error.lock().unwrap() = Some(message.to_string());
    }

    pub fn stored_proto_bytes(&self) -> Option<Vec<u8>> {
        self.byte_cache.lock().unwrap().brotli_proto.clone()
    }

    pub fn stored_zstd_proto_bytes(&self) -> Option<Vec<u8>> {
        self.byte_cache.lock().unwrap().zstd_proto.clone()
    }

    pub fn stored_json_bytes(&self) -> Option<Vec<u8>> {
        self.byte_cache.lock().unwrap().json.clone()
    }

    pub fn num_get_calls(&self) -> usize {
        self.get_call_count.load(Ordering::SeqCst)
    }

    pub fn num_read_only_calls(&self) -> usize {
        self.read_only_call_count.load(Ordering::SeqCst)
    }

    pub fn num_get_bytes_calls(&self) -> usize {
        self.get_bytes_call_count.load(Ordering::SeqCst)
    }

    pub fn num_zstd_get_bytes_calls(&self) -> usize {
        self.zstd_get_bytes_call_count.load(Ordering::SeqCst)
    }

    pub fn num_set_calls(&self) -> usize {
        self.set_call_count.load(Ordering::SeqCst)
    }

    pub fn num_set_bytes_calls(&self) -> usize {
        self.set_bytes_call_count.load(Ordering::SeqCst)
    }

    fn get_bytes_cache_for_key(&self, key: &str) -> Option<Vec<u8>> {
        let cache = self.byte_cache.lock().unwrap();
        if key.contains("|statsig-zstd|") {
            cache.zstd_proto.clone()
        } else if key.contains("|statsig-br|") {
            cache.brotli_proto.clone()
        } else {
            cache.json.clone()
        }
    }
}

#[async_trait]
impl DataStoreTrait for MockDataStore {
    fn write_once(&self) -> bool {
        self.write_once
    }

    fn is_read_only(&self) -> bool {
        let prior_checks = self.read_only_call_count.fetch_add(1, Ordering::SeqCst);
        self.read_only
            || self.read_only_once.swap(false, Ordering::SeqCst)
            || (self.read_only_after_first_check && prior_checks > 0)
    }

    async fn initialize(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        Ok(())
    }

    async fn get(&self, key: &str) -> Result<DataStoreResponse, StatsigErr> {
        self.get_call_count.fetch_add(1, Ordering::SeqCst);
        let response = self.response.lock().unwrap().take();
        if let Some(response) = response {
            return Ok(response);
        }

        let Some(bytes) = self.get_bytes_cache_for_key(key) else {
            return Err(StatsigErr::DataStoreFailure("Failed to get".to_string()));
        };

        Ok(DataStoreResponse {
            result: Some(String::from_utf8(bytes).map_err(|e| {
                StatsigErr::DataStoreFailure(format!("Cached value is not UTF-8: {e}"))
            })?),
            time: Some(1),
            checksum: None,
            has_updates: None,
        })
    }

    async fn set(&self, key: &str, value: &str, _time: Option<u64>) -> Result<(), StatsigErr> {
        self.set_call_count.fetch_add(1, Ordering::SeqCst);
        if self.byte_cache_enabled && !is_proto_cache_key(key) {
            self.byte_cache.lock().unwrap().json = Some(value.as_bytes().to_vec());
        }
        Ok(())
    }

    async fn get_bytes(
        &self,
        key: &str,
        _request: DataStoreGetBytesRequest,
    ) -> Result<DataStoreBytesResponse, StatsigErr> {
        self.get_bytes_call_count.fetch_add(1, Ordering::SeqCst);
        if key.contains("|statsig-zstd|") {
            self.zstd_get_bytes_call_count
                .fetch_add(1, Ordering::SeqCst);
        }
        if !self.byte_cache_enabled {
            return Err(StatsigErr::BytesNotImplemented);
        }

        if let Some(message) = self.get_bytes_error.lock().unwrap().as_ref() {
            return Err(StatsigErr::DataStoreFailure(message.clone()));
        }

        Ok(DataStoreBytesResponse {
            result: self.get_bytes_cache_for_key(key),
            time: Some(1),
            checksum: None,
            has_updates: None,
        })
    }

    async fn set_bytes(
        &self,
        key: &str,
        value: &[u8],
        _time: Option<u64>,
        _checksum: Option<String>,
    ) -> Result<(), StatsigErr> {
        self.set_bytes_call_count.fetch_add(1, Ordering::SeqCst);
        self.set_bytes_payloads.lock().unwrap().push(value.to_vec());
        self.set_bytes_started.add_permits(1);
        if let Some(gate) = &self.set_bytes_gate {
            gate.acquire().await.unwrap().forget();
        }
        if self
            .set_bytes_failures
            .fetch_update(Ordering::SeqCst, Ordering::SeqCst, |remaining| {
                remaining.checked_sub(1)
            })
            .is_ok()
        {
            return Err(StatsigErr::DataStoreFailure(
                "Publication failed".to_string(),
            ));
        }
        if !self.byte_cache_enabled {
            return Err(StatsigErr::BytesNotImplemented);
        }

        let mut cache = self.byte_cache.lock().unwrap();
        if key.contains("|statsig-zstd|") {
            cache.zstd_proto = Some(value.to_vec());
        } else if key.contains("|statsig-br|") {
            cache.brotli_proto = Some(value.to_vec());
        } else {
            cache.json = Some(value.to_vec());
        }

        Ok(())
    }

    async fn support_polling_updates_for(&self, _path: RequestPath) -> bool {
        self.supports_polling
    }
}

fn is_proto_cache_key(key: &str) -> bool {
    key.contains("|statsig-br|") || key.contains("|statsig-zstd|")
}
