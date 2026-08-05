mod utils;

use std::sync::atomic::Ordering;
use std::sync::{Arc, atomic::AtomicBool};
use std::time::Duration;

use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use statsig_rust::{
    SpecsSource, SpecsUpdate, Statsig, StatsigOptions, StatsigUser, networking::ResponseData,
    sdk_event_emitter::SdkEvent,
};
use utils::mock_event_logging_adapter::MockEventLoggingAdapter;

struct BlockingSpecsUpdatedCallback {
    is_blocked: AtomicBool,
    did_block_callback: AtomicBool,
}

impl BlockingSpecsUpdatedCallback {
    pub fn new() -> Self {
        Self {
            is_blocked: AtomicBool::new(false),
            did_block_callback: AtomicBool::new(false),
        }
    }

    fn block_while_enabled(&self) {
        while self.is_blocked.load(std::sync::atomic::Ordering::SeqCst) {
            self.did_block_callback
                .store(true, std::sync::atomic::Ordering::SeqCst);
            std::thread::sleep(std::time::Duration::from_millis(100));
        }
    }
}

#[tokio::test(flavor = "multi_thread", worker_threads = 4)]
async fn test_spec_store_lock() {
    let specs_adapter = Arc::new(MockSpecsAdapter::with_data("tests/data/eval_proj_dcs.json"));
    let blocking_callback = Arc::new(BlockingSpecsUpdatedCallback::new());

    let options = StatsigOptions {
        specs_adapter: Some(specs_adapter.clone()),
        event_logging_adapter: Some(Arc::new(MockEventLoggingAdapter::new())),
        ..StatsigOptions::default()
    };

    let statsig = Arc::new(Statsig::new("secret-key", Some(Arc::new(options))));
    let _ = statsig.initialize().await;

    let blocking_callback_clone = blocking_callback.clone();
    statsig
        .event_emitter
        .subscribe(SdkEvent::SPECS_UPDATED, move |_| {
            blocking_callback_clone.block_while_enabled();
        });

    blocking_callback.is_blocked.store(true, Ordering::SeqCst);

    let statsig_for_sync = statsig.clone();
    let sync_handle = tokio::task::spawn(async move {
        let mut data: serde_json::Value =
            serde_json::from_str(include_str!("data/eval_proj_dcs.json")).unwrap();
        data["time"] = serde_json::json!(9_999_999_999_999_u64);
        data["checksum"] = serde_json::json!("spec-store-lock-test");

        statsig_for_sync
            .get_context()
            .spec_store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes(serde_json::to_vec(&data).unwrap()),
                source: SpecsSource::Bootstrap,
                received_at: 2000,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
    });

    for _ in 0..20 {
        if blocking_callback.did_block_callback.load(Ordering::SeqCst) {
            break;
        }

        tokio::time::sleep(Duration::from_millis(50)).await;
    }

    assert!(blocking_callback.did_block_callback.load(Ordering::SeqCst));

    let statsig_clone = statsig.clone();
    let check_handle = tokio::task::spawn(async move {
        let user = StatsigUser::with_user_id("user1");

        for _ in 0..1000 {
            let gate = statsig_clone.get_feature_gate(&user, "test_public");
            drop(gate);
        }
    });

    let winner = tokio::select! {
        _ = tokio::time::sleep(Duration::from_secs(1)) => false,
        _ = check_handle => true,
    };

    blocking_callback.is_blocked.store(false, Ordering::SeqCst);

    if !winner {
        panic!("gate checks blocked by long sync times");
    }

    drop(statsig);
    sync_handle.abort();
    std::process::exit(0);
}
