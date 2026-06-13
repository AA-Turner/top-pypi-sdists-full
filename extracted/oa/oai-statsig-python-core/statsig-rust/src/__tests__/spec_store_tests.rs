use std::collections::HashMap;
use std::sync::{mpsc, Arc};
use std::time::Duration;

use async_trait::async_trait;
use parking_lot::Mutex;
use serial_test::serial;

use crate::{
    data_store_interface::{DataStoreResponse, DataStoreTrait, RequestPath},
    networking::ResponseData,
    output_logger::{
        initialize_output_logger, shutdown_output_logger, LogLevel, OutputLogProvider,
    },
    sdk_event_emitter::{SdkEvent, SdkEventEmitter},
    SpecStore, SpecsSource, SpecsUpdate, StatsigErr, StatsigOptions, StatsigRuntime,
};

struct TestDataStore {
    get_response: Mutex<Option<DataStoreResponse>>,
    supports_polling: bool,
    set_bytes_error: Option<&'static str>,
    calls: Mutex<Vec<(String, Option<String>)>>,
}

#[derive(Clone, Debug, PartialEq)]
enum RecordedLog {
    Warn(String, String),
    Init,
    Shutdown,
}

struct TestLogProvider {
    logs: Mutex<Vec<RecordedLog>>,
}

impl TestLogProvider {
    fn new() -> Self {
        Self {
            logs: Mutex::new(Vec::new()),
        }
    }
}

impl TestDataStore {
    fn new(supports_polling: bool) -> Self {
        Self {
            get_response: Mutex::new(None),
            supports_polling,
            set_bytes_error: None,
            calls: Mutex::new(vec![]),
        }
    }

    fn new_with_set_bytes_failure(supports_polling: bool) -> Self {
        Self {
            set_bytes_error: Some("set_bytes failed"),
            ..Self::new(supports_polling)
        }
    }
}

#[async_trait]
impl DataStoreTrait for TestDataStore {
    async fn initialize(&self) -> Result<(), StatsigErr> {
        self.calls.lock().push(("initialize".to_string(), None));
        Ok(())
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        self.calls.lock().push(("shutdown".to_string(), None));
        Ok(())
    }

    async fn get(&self, key: &str) -> Result<DataStoreResponse, StatsigErr> {
        self.calls
            .lock()
            .push(("get".to_string(), Some(key.to_string())));

        let mut lock = self.get_response.lock();
        lock.take()
            .ok_or(StatsigErr::DataStoreFailure("Failed to get".to_string()))
    }

    async fn set(&self, key: &str, value: &str, time: Option<u64>) -> Result<(), StatsigErr> {
        self.calls
            .lock()
            .push(("set".to_string(), Some(format!("{key}:{value}:{time:?}"))));
        Ok(())
    }

    async fn set_bytes(
        &self,
        key: &str,
        value: &[u8],
        time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<(), StatsigErr> {
        self.calls.lock().push((
            "set_bytes".to_string(),
            Some(format!("{key}:{}:{time:?}:{checksum:?}", value.len())),
        ));

        match self.set_bytes_error {
            Some(message) => Err(StatsigErr::DataStoreFailure(message.to_string())),
            None => Err(StatsigErr::BytesNotImplemented),
        }
    }

    async fn support_polling_updates_for(&self, path: RequestPath) -> bool {
        self.calls.lock().push((
            "support_polling_updates_for".to_string(),
            Some(path.to_string()),
        ));
        self.supports_polling
    }
}

impl OutputLogProvider for TestLogProvider {
    fn initialize(&self) {
        self.logs.lock().push(RecordedLog::Init);
    }

    fn debug(&self, _tag: &str, _msg: String) {}

    fn info(&self, _tag: &str, _msg: String) {}

    fn warn(&self, tag: &str, msg: String) {
        self.logs
            .lock()
            .push(RecordedLog::Warn(tag.to_string(), msg));
    }

    fn error(&self, _tag: &str, _msg: String) {}

    fn shutdown(&self) {
        self.logs.lock().push(RecordedLog::Shutdown);
    }
}

#[tokio::test]
async fn test_spec_store_data_store_updates_forwarded_to_data_store() {
    let data_store = Arc::new(TestDataStore::new(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(contents.to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    // data store updates are async, so we need to wait for them to complete
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert_eq!(calls.len(), 2);
    assert_eq!(calls[0].0, "set_bytes");
    assert_eq!(calls[1].0, "set");

    let bytes_call_value = calls[0].1.as_ref().unwrap();
    assert!(bytes_call_value.starts_with("test:"));

    let call_value = calls[1].1.as_ref().unwrap();
    assert!(call_value.len() > 100);
    assert!(call_value.contains("\"feature_gates\""));
}

#[tokio::test]
async fn test_spec_store_data_store_string_fallback_requires_bytes_not_implemented() {
    let data_store = Arc::new(TestDataStore::new_with_set_bytes_failure(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(contents.to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert_eq!(calls.len(), 1);
    assert_eq!(calls[0].0, "set_bytes");
}

#[tokio::test]
async fn test_spec_store_skips_data_store_write_for_delta_responses() {
    let data_store = Arc::new(TestDataStore::new(true));

    let options = StatsigOptions {
        data_store: Some(data_store.clone()),
        ..StatsigOptions::default()
    };

    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        Some(&options),
    );

    let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes_with_headers(
            contents.to_vec(),
            Some(HashMap::from([(
                "x-deltas-used".to_string(),
                "true".to_string(),
            )])),
        ),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok());

    tokio::time::sleep(std::time::Duration::from_millis(100)).await;

    let calls = data_store.calls.lock();

    assert!(calls.is_empty());
}

#[tokio::test]
#[serial]
async fn test_spec_store_proto_bytes_warning_requires_polling_support() {
    let provider = Arc::new(TestLogProvider::new());
    initialize_output_logger(&Some(LogLevel::Debug), Some(provider.clone()));

    for supports_polling in [false, true] {
        provider.logs.lock().clear();

        let data_store = Arc::new(TestDataStore::new(supports_polling));
        let options = StatsigOptions {
            data_store: Some(data_store),
            ..StatsigOptions::default()
        };

        let spec_store = SpecStore::new(
            "test",
            "test".to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            Some(&options),
        );

        let contents = include_bytes!("../../tests/data/eval_proj_dcs.pb.br");
        let update_result = spec_store.set_values(SpecsUpdate {
            data: ResponseData::from_bytes_with_headers(
                contents.to_vec(),
                Some(HashMap::from([
                    (
                        "content-type".to_string(),
                        "application/octet-stream".to_string(),
                    ),
                    ("content-encoding".to_string(), "statsig-br".to_string()),
                ])),
            ),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        });

        assert!(update_result.is_ok());
        tokio::time::sleep(std::time::Duration::from_millis(100)).await;

        let logged_warning = provider.logs.lock().iter().any(|log| {
            matches!(
                log,
                RecordedLog::Warn(_, msg)
                    if msg.contains(
                        "Failed to write protobuf specs to data store as bytes. Protobuf specs cannot fall back to string writes"
                    )
            )
        });

        assert_eq!(logged_warning, supports_polling);
    }

    shutdown_output_logger();
}

#[test]
fn test_failure_to_update() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"test".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_err())
}

#[test]
fn test_no_updates() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"{\"has_updates\": false}".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: None,
    });

    assert!(update_result.is_ok())
}

#[test]
fn test_no_updates_update_field_short_circuit_parse() {
    let spec_store = SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    );

    let update_result = spec_store.set_values(SpecsUpdate {
        data: ResponseData::from_bytes(b"invalid".to_vec()),
        source: SpecsSource::Network,
        received_at: 2000,
        source_api: None,
        has_updates: Some(false),
    });

    assert!(update_result.is_ok())
}

#[test]
fn test_specs_updated_callback_runs_without_holding_store_lock() {
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let spec_store = Arc::new(SpecStore::new(
        "test",
        "test".to_string(),
        StatsigRuntime::get_runtime(),
        event_emitter.clone(),
        None,
    ));
    let callback_store = spec_store.clone();

    event_emitter.subscribe(SdkEvent::SPECS_UPDATED, move |event| {
        let SdkEvent::SpecsUpdated { source, values, .. } = event else {
            panic!("expected a specs updated event");
        };
        assert_eq!(source, &SpecsSource::Network);
        assert!(values.time > 0);

        callback_store.set_source(SpecsSource::Bootstrap);
    });

    let (completed_tx, completed_rx) = mpsc::channel();
    std::thread::spawn(move || {
        let contents = include_bytes!("../../tests/data/eval_proj_dcs.json");
        let result = spec_store.set_values(SpecsUpdate {
            data: ResponseData::from_bytes(contents.to_vec()),
            source: SpecsSource::Network,
            received_at: 2000,
            source_api: None,
            has_updates: None,
        });
        completed_tx.send(result).unwrap();
    });

    let result = completed_rx
        .recv_timeout(Duration::from_millis(500))
        .expect("specs updated callback deadlocked while re-entering the spec store");
    assert!(result.is_ok());
}
