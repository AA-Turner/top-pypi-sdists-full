use super::{EvaluationClient, StatsigOptions, tests::TestObservabilityClient};
use std::sync::Arc;

#[tokio::test]
async fn shutdown_prevents_lazy_preload_observer_creation() {
    let observer = Arc::new(TestObservabilityClient::default());
    let client = EvaluationClient::new(tokio::runtime::Handle::current(), Some(observer)).unwrap();
    assert!(client.id_lists_local_ops_stats.get().is_none());
    client.shutdown().await;

    assert!(
        client
            .preload_shared_id_lists(
                "secret-owner",
                "tenant",
                &StatsigOptions {
                    disable_remote_telemetry: Some(true),
                    disable_network: Some(true),
                    ..Default::default()
                }
            )
            .await
            .is_err()
    );
    assert!(client.id_lists_local_ops_stats.get().is_none());
    assert!(
        client
            .id_lists_observability_runtime
            .get_running_task_ids()
            .is_empty()
    );
}
