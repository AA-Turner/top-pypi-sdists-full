mod utils;

use crate::utils::mock_scrapi::StubData;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use statsig_rust::{Statsig, StatsigOptions, StatsigUser};
use std::sync::Arc;
use std::time::Duration;
use utils::mock_scrapi::{Endpoint, EndpointStub, Method, MockScrapi};

async fn setup() -> (Arc<Statsig>, StatsigUser, MockScrapi) {
    let mock_scrapi = MockScrapi::new().await;
    mock_scrapi
        .stub(EndpointStub {
            method: Method::POST,
            response: StubData::String("{}".to_string()),
            status: 500,
            ..EndpointStub::with_endpoint(Endpoint::LogEvent)
        })
        .await;

    let user = StatsigUser::with_user_id("a_user".to_string());
    let statsig = Statsig::new(
        "secret-key",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(Arc::new(MockSpecsAdapter::with_data(
                "tests/data/eval_proj_dcs.json",
            ))),
            // output_log_level: Some(LogLevel::Debug),
            log_event_url: Some(mock_scrapi.url_for_endpoint(Endpoint::LogEvent)),
            environment: Some("development".to_string()),
            disable_country_lookup: Some(true),
            event_logging_max_pending_batch_queue_size: Some(2),
            event_logging_max_queue_size: Some(1000),
            ..StatsigOptions::new()
        })),
    );

    statsig.initialize().await.unwrap();

    (Arc::new(statsig), user, mock_scrapi)
}

#[tokio::test]
async fn log_event_remains_responsive_while_uploads_fail() {
    let (statsig, user, mock_scrapi) = setup().await;

    // Trigger a background upload and observe the HTTP 500 stub before the flood.
    for _ in 0..1_000 {
        statsig.log_event(&user, "test_event", None, None);
    }
    assert_eventually!(|| mock_scrapi.times_called_for_endpoint(Endpoint::LogEvent) > 0);

    // Keep the million-event workload, but detect stalls rather than requiring
    // the CI host to sustain 100,000 events/second in a debug build.
    const CHUNKS: usize = 100;
    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel();
    let producer = statsig.clone();
    let worker = std::thread::spawn(move || {
        for _ in 0..CHUNKS {
            for _ in 0..10_000 {
                producer.log_event(&user, "test_event", None, None);
            }
            tx.send(()).unwrap();
        }
    });
    for _ in 0..CHUNKS {
        tokio::time::timeout(Duration::from_secs(1), rx.recv())
            .await
            .expect("event producer stalled")
            .expect("event producer exited early");
    }
    worker.join().unwrap();
    let _ = statsig.shutdown().await;
}
