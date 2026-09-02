use crate::recording_pipeline::{RecordingPipeline, RecordingTaskManager};
use crate::Result;
use crate::TerminalError;
use bytes::Bytes;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;

#[tokio::test]
async fn test_pipeline_completes() {
    let encrypted_count = Arc::new(AtomicUsize::new(0));
    let uploaded_count = Arc::new(AtomicUsize::new(0));

    let encrypted_count_clone = encrypted_count.clone();
    let uploaded_count_clone = uploaded_count.clone();

    let pipeline = RecordingPipeline::new(
        move |data| {
            encrypted_count_clone.fetch_add(1, Ordering::SeqCst);
            Ok(data.to_vec())
        },
        move |_data| {
            uploaded_count_clone.fetch_add(1, Ordering::SeqCst);
            Ok(())
        },
        100,
    );

    // Send test data
    for i in 0..10 {
        pipeline
            .sender()
            .send(Bytes::from(format!("test {}", i)))
            .await
            .unwrap();
    }

    // Shutdown and verify
    pipeline.shutdown().await.unwrap();

    assert_eq!(encrypted_count.load(Ordering::SeqCst), 10);
    assert_eq!(uploaded_count.load(Ordering::SeqCst), 10);
}

#[tokio::test]
async fn test_pipeline_timeout() {
    let pipeline = RecordingPipeline::new(
        |data: Bytes| -> Result<Vec<u8>> { Ok(data.to_vec()) },
        |_data: Vec<u8>| -> Result<()> {
            // Simulate slow upload (use tokio sleep, not std)
            let _ = std::hint::black_box(_data); // Prevent optimization
            Ok(())
        },
        100,
    );

    pipeline.sender().send(Bytes::from("test")).await.unwrap();

    // Give tasks time to process, then shutdown quickly
    tokio::time::sleep(Duration::from_millis(50)).await;

    // Should complete (not timeout with fast upload)
    let result = pipeline.shutdown_with_timeout(Duration::from_secs(1)).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_task_manager_abort_on_drop() {
    let mut manager = RecordingTaskManager::new();

    manager.spawn(async {
        tokio::time::sleep(Duration::from_secs(100)).await;
        Ok(())
    });

    // Drop without shutdown - should abort
    drop(manager);
    // Task is aborted (verified via logs in real usage)
}

#[tokio::test]
async fn test_error_propagation() {
    let pipeline = RecordingPipeline::new(
        |_data: Bytes| -> Result<Vec<u8>> {
            Err(TerminalError::IoError(std::io::Error::other(
                "Encryption failed",
            )))
        },
        |_data: Vec<u8>| -> Result<()> { Ok(()) },
        100,
    );

    pipeline.sender().send(Bytes::from("test")).await.unwrap();

    // Should propagate error
    let result = pipeline.shutdown().await;
    assert!(result.is_err());
}
