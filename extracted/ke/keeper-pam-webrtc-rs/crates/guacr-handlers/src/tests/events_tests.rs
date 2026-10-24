use crate::error::HandlerError;
use crate::events::{connect_with_event_adapter, EventCallback, HandlerEvent, InstructionSender};
use bytes::Bytes;
use std::sync::{Arc, Mutex};

struct TestCallback {
    events: Arc<Mutex<Vec<HandlerEvent>>>,
    instructions: Arc<Mutex<Vec<Bytes>>>,
}

#[async_trait::async_trait]
impl EventCallback for TestCallback {
    fn on_event(&self, event: HandlerEvent) {
        self.events.lock().unwrap().push(event);
    }

    async fn send_instruction(&self, instruction: Bytes) -> Result<(), HandlerError> {
        self.instructions.lock().unwrap().push(instruction);
        Ok(())
    }
}

#[tokio::test]
async fn test_event_callback() {
    let events = Arc::new(Mutex::new(Vec::new()));
    let instructions = Arc::new(Mutex::new(Vec::new()));

    let callback = Arc::new(TestCallback {
        events: events.clone(),
        instructions: instructions.clone(),
    });

    let sender = InstructionSender::new(callback.clone());

    // Send instruction
    sender.send(Bytes::from("test")).await.unwrap();
    assert_eq!(instructions.lock().unwrap().len(), 1);

    // Send error
    sender.send_error("test error".to_string(), Some(1));
    assert_eq!(events.lock().unwrap().len(), 1);

    // Send threat
    sender.send_threat("critical".to_string(), "threat detected".to_string());
    assert_eq!(events.lock().unwrap().len(), 2);
}

struct ControlledCallback {
    started: tokio::sync::mpsc::UnboundedSender<Bytes>,
    release: Arc<tokio::sync::Semaphore>,
    fail: bool,
    panic: bool,
}

#[async_trait::async_trait]
impl EventCallback for ControlledCallback {
    fn on_event(&self, _: HandlerEvent) {}

    async fn send_instruction(&self, instruction: Bytes) -> Result<(), HandlerError> {
        self.started.send(instruction).unwrap();
        self.release.acquire().await.unwrap().forget();
        assert!(!self.panic, "forwarder panic");
        if self.fail {
            Err(HandlerError::ChannelError(
                "forwarding rejected".to_string(),
            ))
        } else {
            Ok(())
        }
    }
}

#[tokio::test]
async fn adapter_waits_for_blocked_final_output() {
    let (started_tx, mut started_rx) = tokio::sync::mpsc::unbounded_channel();
    let release = Arc::new(tokio::sync::Semaphore::new(0));
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: release.clone(),
        fail: false,
        panic: false,
    });
    let (_, input) = tokio::sync::mpsc::channel(1);
    let adapter = tokio::spawn(connect_with_event_adapter(
        |_, output, _, _, _| async move {
            output
                .send(Bytes::from_static(b"final output"))
                .await
                .unwrap();
            Ok(())
        },
        Default::default(),
        callback,
        input,
        None,
        Default::default(),
        1,
    ));
    assert_eq!(
        started_rx.recv().await.unwrap(),
        Bytes::from_static(b"final output")
    );
    assert!(
        !adapter.is_finished(),
        "completion must join the blocked final send"
    );
    release.add_permits(1);
    adapter.await.unwrap().unwrap();
}

#[tokio::test]
async fn adapter_drains_fifo_even_after_producer_error() {
    let (started_tx, mut started_rx) = tokio::sync::mpsc::unbounded_channel();
    let release = Arc::new(tokio::sync::Semaphore::new(0));
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: release.clone(),
        fail: false,
        panic: false,
    });
    let (_, input) = tokio::sync::mpsc::channel(1);
    let adapter = tokio::spawn(connect_with_event_adapter(
        |_, output, _, _, _| async move {
            output.send(Bytes::from_static(b"first")).await.unwrap();
            output.send(Bytes::from_static(b"final")).await.unwrap();
            Err(HandlerError::RecordingFailed("producer failed".to_string()))
        },
        Default::default(),
        callback,
        input,
        None,
        Default::default(),
        2,
    ));
    assert_eq!(
        started_rx.recv().await.unwrap(),
        Bytes::from_static(b"first")
    );
    assert!(!adapter.is_finished());
    release.add_permits(1);
    assert_eq!(
        started_rx.recv().await.unwrap(),
        Bytes::from_static(b"final")
    );
    assert!(!adapter.is_finished());
    release.add_permits(1);
    assert!(matches!(
        adapter.await.unwrap(),
        Err(HandlerError::RecordingFailed(_))
    ));
}

#[tokio::test]
async fn producer_error_takes_precedence_over_forwarder_error() {
    let (started_tx, _started_rx) = tokio::sync::mpsc::unbounded_channel();
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: Arc::new(tokio::sync::Semaphore::new(1)),
        fail: true,
        panic: false,
    });
    let (_, input) = tokio::sync::mpsc::channel(1);
    let result = connect_with_event_adapter(
        |_, output, _, _, _| async move {
            output.send(Bytes::from_static(b"final")).await.unwrap();
            Err(HandlerError::RecordingFailed("producer failed".to_string()))
        },
        Default::default(),
        callback,
        input,
        None,
        Default::default(),
        1,
    )
    .await;
    assert!(matches!(result, Err(HandlerError::RecordingFailed(_))));
}

#[tokio::test]
async fn forwarder_failure_allows_live_producer_finalization() {
    for panic in [false, true] {
        let (started_tx, _started_rx) = tokio::sync::mpsc::unbounded_channel();
        let callback = Arc::new(ControlledCallback {
            started: started_tx,
            release: Arc::new(tokio::sync::Semaphore::new(1)),
            fail: !panic,
            panic,
        });
        let (finalized_tx, finalized_rx) = tokio::sync::oneshot::channel();
        let (_, input) = tokio::sync::mpsc::channel(1);
        let result = tokio::time::timeout(
            std::time::Duration::from_secs(1),
            connect_with_event_adapter(
                |_, output, _, _, _| async move {
                    output.send(Bytes::from_static(b"output")).await.unwrap();
                    tokio::time::sleep(std::time::Duration::from_millis(20)).await;
                    finalized_tx.send(()).unwrap();
                    Ok(())
                },
                Default::default(),
                callback,
                input,
                None,
                Default::default(),
                1,
            ),
        )
        .await
        .expect("failed forwarder must not wait beyond its finalize deadline");
        assert!(matches!(result, Err(HandlerError::ChannelError(_))));
        finalized_rx.await.expect("producer finalization must run");
    }
}

#[tokio::test]
async fn completed_producer_seals_retained_senders_and_drains_admitted_output() {
    let (started_tx, mut started_rx) = tokio::sync::mpsc::unbounded_channel();
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: Arc::new(tokio::sync::Semaphore::new(1)),
        fail: false,
        panic: false,
    });
    let (retained_tx, retained_rx) = tokio::sync::oneshot::channel();
    let (_, input) = tokio::sync::mpsc::channel(1);
    tokio::time::timeout(
        std::time::Duration::from_secs(1),
        connect_with_event_adapter(
            |_, output, _, _, _| async move {
                output.send(Bytes::from_static(b"admitted")).await.unwrap();
                retained_tx.send(output).unwrap();
                Ok(())
            },
            Default::default(),
            callback,
            input,
            None,
            Default::default(),
            1,
        ),
    )
    .await
    .expect("retained sender must not keep completion alive")
    .unwrap();
    assert_eq!(
        started_rx.recv().await.unwrap(),
        Bytes::from_static(b"admitted")
    );
    let retained = retained_rx.await.unwrap();
    assert!(retained
        .send(Bytes::from_static(b"too late"))
        .await
        .is_err());
}

#[tokio::test(start_paused = true)]
async fn adapter_honors_configured_finalization_deadline() {
    let (started_tx, _started_rx) = tokio::sync::mpsc::unbounded_channel();
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: Arc::new(tokio::sync::Semaphore::new(1)),
        fail: true,
        panic: false,
    });
    let finalized = Arc::new(std::sync::atomic::AtomicBool::new(false));
    let producer_finalized = finalized.clone();
    let (_, input) = tokio::sync::mpsc::channel(1);
    let started = tokio::time::Instant::now();
    let result = connect_with_event_adapter(
        |_, output, _, _, _| async move {
            output.send(Bytes::from_static(b"output")).await.unwrap();
            tokio::time::sleep(std::time::Duration::from_secs(15)).await;
            producer_finalized.store(true, std::sync::atomic::Ordering::Release);
            Ok(())
        },
        Default::default(),
        callback,
        input,
        None,
        crate::hooks::SessionHooks {
            handler_finalization_timeout: std::time::Duration::from_secs(16),
            ..Default::default()
        },
        1,
    )
    .await;
    assert!(started.elapsed() >= std::time::Duration::from_secs(15));
    assert!(finalized.load(std::sync::atomic::Ordering::Acquire));
    assert!(matches!(result, Err(HandlerError::ChannelError(_))));
}

#[tokio::test(start_paused = true)]
async fn adapter_aborts_hung_producer_at_configured_backstop() {
    let (started_tx, _started_rx) = tokio::sync::mpsc::unbounded_channel();
    let callback = Arc::new(ControlledCallback {
        started: started_tx,
        release: Arc::new(tokio::sync::Semaphore::new(1)),
        fail: true,
        panic: false,
    });
    let dropped = Arc::new(std::sync::atomic::AtomicBool::new(false));
    let producer_dropped = dropped.clone();
    let (_, input) = tokio::sync::mpsc::channel(1);
    let started = tokio::time::Instant::now();
    let result = connect_with_event_adapter(
        |_, output, _, _, _| async move {
            let _guard = DropFlag(producer_dropped);
            output.send(Bytes::from_static(b"output")).await.unwrap();
            std::future::pending::<Result<(), HandlerError>>().await
        },
        Default::default(),
        callback,
        input,
        None,
        crate::hooks::SessionHooks {
            handler_finalization_timeout: std::time::Duration::from_millis(20),
            ..Default::default()
        },
        1,
    )
    .await;
    assert!(started.elapsed() >= std::time::Duration::from_millis(20));
    assert!(dropped.load(std::sync::atomic::Ordering::Acquire));
    assert!(matches!(result, Err(HandlerError::ChannelError(_))));
}

struct DropFlag(Arc<std::sync::atomic::AtomicBool>);

impl Drop for DropFlag {
    fn drop(&mut self) {
        self.0.store(true, std::sync::atomic::Ordering::Release);
    }
}
