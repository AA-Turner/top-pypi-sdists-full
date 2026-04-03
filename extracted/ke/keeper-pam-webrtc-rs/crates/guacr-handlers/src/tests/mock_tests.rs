use crate::handler::{HealthStatus, ProtocolHandler};
use crate::mock::MockProtocolHandler;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::mpsc;

#[tokio::test]
async fn test_mock_handler_name() {
    let handler = MockProtocolHandler::new("test-protocol");
    assert_eq!(handler.name(), "test-protocol");
}

#[tokio::test]
async fn test_mock_handler_connect() {
    let handler = MockProtocolHandler::new("ssh");
    let (to_client, _rx) = mpsc::channel(10);
    let (tx, from_client) = mpsc::channel(10);

    assert_eq!(handler.connect_count(), 0);

    // Spawn connect task
    let handler_clone = Arc::new(handler);
    let handler_ref = Arc::clone(&handler_clone);
    let connect_task: tokio::task::JoinHandle<Result<(), crate::error::HandlerError>> =
        tokio::spawn(async move {
            handler_ref
                .connect(HashMap::new(), to_client, from_client, None)
                .await
        });

    // Wait a bit
    tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;

    // Close channel
    drop(tx);

    // Wait for connect to finish
    connect_task.await.unwrap().unwrap();

    assert_eq!(handler_clone.connect_count(), 1);
}

#[tokio::test]
async fn test_mock_handler_health() {
    let handler = MockProtocolHandler::new("test");

    let status = handler.health_check().await.unwrap();
    assert_eq!(status, HealthStatus::Healthy);

    handler.set_health(HealthStatus::Degraded {
        reason: "test degradation".to_string(),
    });

    let status = handler.health_check().await.unwrap();
    assert!(matches!(status, HealthStatus::Degraded { .. }));
}

#[tokio::test]
async fn test_mock_handler_stats() {
    let handler = Arc::new(MockProtocolHandler::new("test"));
    let (to_client, _rx) = mpsc::channel(10);
    let (tx, from_client) = mpsc::channel(10);

    let handler_ref = Arc::clone(&handler);
    let connect_task: tokio::task::JoinHandle<Result<(), crate::error::HandlerError>> =
        tokio::spawn(async move {
            handler_ref
                .connect(HashMap::new(), to_client, from_client, None)
                .await
        });

    tokio::time::sleep(tokio::time::Duration::from_millis(10)).await;
    drop(tx);
    connect_task.await.unwrap().unwrap();

    let stats: crate::handler::HandlerStats = handler.stats().await.unwrap();
    assert_eq!(stats.total_connections, 1);
}
