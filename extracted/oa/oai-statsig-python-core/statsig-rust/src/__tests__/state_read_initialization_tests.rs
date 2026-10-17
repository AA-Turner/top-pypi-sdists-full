use crate::id_lists_adapter::{IdListsAdapter, IdListsUpdateListener};
use crate::{SpecsAdapter, SpecsUpdateListener};
use crate::{Statsig, StatsigErr, StatsigOptions, StatsigRuntime};
use async_trait::async_trait;
use std::sync::{
    Arc,
    atomic::{AtomicBool, Ordering},
};
use std::time::Duration;
struct DelayedSpecs;
#[async_trait]
impl SpecsAdapter for DelayedSpecs {
    fn initialize(&self, _: Arc<dyn SpecsUpdateListener>) {}
    async fn start(self: Arc<Self>, _: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        tokio::time::sleep(Duration::from_millis(1800)).await;
        Ok(())
    }
    async fn schedule_background_sync(
        self: Arc<Self>,
        _: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        Ok(())
    }
    async fn shutdown(&self, _: Duration, _: &Arc<StatsigRuntime>) -> Result<(), StatsigErr> {
        Ok(())
    }
    fn get_type_name(&self) -> String {
        "DelayedSpecs".into()
    }
}

struct DelayedLists(AtomicBool);
#[async_trait]
impl IdListsAdapter for DelayedLists {
    async fn start(
        self: Arc<Self>,
        _: &Arc<StatsigRuntime>,
        _: Arc<dyn IdListsUpdateListener + Send + Sync>,
    ) -> Result<(), StatsigErr> {
        self.0.store(true, Ordering::SeqCst);
        tokio::time::sleep(Duration::from_millis(1800)).await;
        Ok(())
    }
    async fn shutdown(&self, _: Duration) -> Result<(), StatsigErr> {
        Ok(())
    }
    async fn schedule_background_sync(
        self: Arc<Self>,
        _: &Arc<StatsigRuntime>,
    ) -> Result<(), StatsigErr> {
        Ok(())
    }
    fn get_type_name(&self) -> String {
        "DelayedLists".into()
    }
}

#[cfg(not(feature = "custom_network_provider"))]
#[tokio::test]
async fn built_in_adapters_recover_after_timeout_before_id_list_start() {
    use wiremock::{
        Mock, MockServer, ResponseTemplate,
        matchers::{method, path},
    };
    for timeout in [Some(0), Some(20)] {
        let server = MockServer::start().await;
        Mock::given(method("GET"))
            .and(path("/v2/download_config_specs"))
            .respond_with(ResponseTemplate::new(200).set_delay(Duration::from_secs(5)))
            .mount(&server)
            .await;
        let statsig = Statsig::new(
            "secret-recovery",
            Some(Arc::new(StatsigOptions {
                specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
                id_lists_url: Some(format!("{}/manifest", server.uri())),
                specs_sync_interval_ms: Some(1000),
                id_lists_sync_interval_ms: Some(1000),
                init_timeout_ms: timeout,
                enable_id_lists: Some(true),
                disable_all_logging: Some(true),
                disable_country_lookup: Some(true),
                ..Default::default()
            })),
        );
        assert!(
            !statsig
                .initialize_with_details()
                .await
                .unwrap()
                .init_success
        );
        server.reset().await;
        Mock::given(method("GET"))
            .and(path("/v2/download_config_specs"))
            .respond_with(
                ResponseTemplate::new(200)
                    .set_body_bytes(include_bytes!("../../tests/data/eval_proj_dcs.json")),
            )
            .mount(&server)
            .await;
        Mock::given(method("POST")).and(path("/manifest"))
            .respond_with(ResponseTemplate::new(200).set_body_json(serde_json::json!({"a": {
                "name": "a", "url": format!("{}/file", server.uri()), "size": 3, "fileID": "v1", "creationTime": 1
            }}))).mount(&server).await;
        Mock::given(method("GET"))
            .and(path("/file"))
            .respond_with(ResponseTemplate::new(200).set_body_string("+a\n"))
            .mount(&server)
            .await;
        tokio::time::timeout(Duration::from_secs(4), async {
            while !statsig
                .spec_store
                .get_current_id_list_metadata()
                .contains_key("a")
                || !statsig.is_config_spec_ready()
            {
                tokio::time::sleep(Duration::from_millis(20)).await;
            }
        })
        .await
        .expect("both built-in adapters must publish after timeout");
        statsig.shutdown().await.unwrap();
    }
}

#[tokio::test(start_paused = true)]
async fn explicit_initialization_deadline_is_shared_across_sequential_adapters() {
    let lists = Arc::new(DelayedLists(AtomicBool::new(false)));
    let statsig = Statsig::new(
        "secret-deadline",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(DelayedSpecs)),
            id_lists_adapter: Some(lists.clone()),
            enable_id_lists: Some(true),
            init_timeout_ms: Some(3000),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            ..Default::default()
        })),
    );
    let start = tokio::time::Instant::now();
    let details = statsig.initialize_with_details().await.unwrap();
    assert!(!details.init_success);
    assert!(lists.0.load(Ordering::SeqCst));
    assert_eq!(start.elapsed(), Duration::from_secs(3));
    statsig.shutdown().await.unwrap();
}

#[tokio::test(start_paused = true)]
async fn explicit_zero_does_not_become_the_default_deadline() {
    let statsig = Statsig::new(
        "secret-zero",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(DelayedSpecs)),
            init_timeout_ms: Some(0),
            disable_all_logging: Some(true),
            disable_country_lookup: Some(true),
            ..Default::default()
        })),
    );
    let start = tokio::time::Instant::now();
    assert!(
        !statsig
            .initialize_with_details()
            .await
            .unwrap()
            .init_success
    );
    assert!(start.elapsed() < Duration::from_millis(10));
    statsig.shutdown().await.unwrap();
}
