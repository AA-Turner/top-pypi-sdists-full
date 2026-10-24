use super::*;
use std::sync::atomic::{AtomicBool, Ordering};
use tokio::sync::{oneshot, Semaphore};

type Fixture = (
    Arc<WebRtcEventCallback>,
    mpsc::Receiver<Bytes>,
    tokio::sync::watch::Sender<HandlerTermination>,
    HandlerOutput,
    mpsc::UnboundedReceiver<(u32, String)>,
);

fn fixture() -> Fixture {
    let (tx, rx) = mpsc::channel(8);
    let (terminal, _) = tokio::sync::watch::channel(HandlerTermination::default());
    let (closed_tx, closed_rx) = mpsc::unbounded_channel();
    let handler_senders = Arc::new(dashmap::DashMap::new());
    let (input, _) = mpsc::channel(1);
    handler_senders.insert(7, input);
    let callback = Arc::new(WebRtcEventCallback {
        conn_no: 7,
        channel_id: "control".to_string(),
        conversation_id: "conversation".to_string(),
        terminal: terminal.clone(),
        send_queue_tx: tx,
        handler_senders: handler_senders.clone(),
    });
    (
        callback,
        rx,
        terminal,
        HandlerOutput {
            conn_no: 7,
            channel_id: "control".to_string(),
            buffer_pool: crate::buffer_pool::BufferPool::default(),
            channel_close_reason: Arc::new(tokio::sync::Mutex::new(None)),
            conn_closed_tx: closed_tx,
            handler_senders,
            finalization_deadline: std::time::Duration::from_secs(30),
        },
        closed_rx,
    )
}

#[test]
fn configured_finalization_backstop_reports_sql_shutdown_conflict() {
    const DRAIN: std::time::Duration = std::time::Duration::from_secs(5);
    let sql_shutdown_budget =
        DRAIN * 2 + std::time::Duration::from_secs(1) + DRAIN * 2 + DRAIN + DRAIN;
    let finalization_backstop = crate::models::TunnelTimeouts::default().handler_finalization;
    assert_eq!(finalization_backstop, std::time::Duration::from_secs(30));
    assert!(
        sql_shutdown_budget > finalization_backstop,
        "the finalization backstop must preserve an incomplete outcome when SQL's sequential bounded cleanup exceeds it"
    );
}

fn data_payload(encoded: &Bytes) -> Bytes {
    assert_eq!(u32::from_be_bytes(encoded[..4].try_into().unwrap()), 7);
    let len = u32::from_be_bytes(encoded[12..16].try_into().unwrap()) as usize;
    encoded.slice(16..16 + len)
}

fn assert_close(encoded: &Bytes, reason: CloseConnectionReason) {
    assert_eq!(u32::from_be_bytes(encoded[..4].try_into().unwrap()), 0);
    assert_eq!(u32::from_be_bytes(encoded[12..16].try_into().unwrap()), 7);
    assert_eq!(
        u16::from_be_bytes(encoded[16..18].try_into().unwrap()),
        ControlMessage::CloseConnection as u16
    );
    assert_eq!(u32::from_be_bytes(encoded[18..22].try_into().unwrap()), 7);
    assert_eq!(encoded[22], reason as u8);
}

async fn next_frame(rx: &mut mpsc::UnboundedReceiver<Bytes>) -> Bytes {
    tokio::time::timeout(std::time::Duration::from_secs(1), rx.recv())
        .await
        .expect("sender stalled")
        .expect("sender closed")
}

#[tokio::test]
async fn blocked_final_instruction_then_close_then_local_cleanup() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let handler_senders = output.handler_senders.clone();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let release = Arc::new(Semaphore::new(0));
    let send_release = release.clone();
    let session = tokio::spawn(run_handler_session(
        async move {
            callback
                .send_instruction(Bytes::from_static(b"final result"))
                .await?;
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            let release = send_release.clone();
            let sent = sent_tx.clone();
            async move {
                sent.send(encoded).unwrap();
                release.acquire().await.unwrap().forget();
                Ok(())
            }
        },
    ));
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"final result")
    );
    assert!(!session.is_finished());
    assert!(
        sent_rx.try_recv().is_err(),
        "close must not overtake blocked final data"
    );
    assert!(closed.try_recv().is_err());
    assert!(handler_senders.contains_key(&7));
    release.add_permits(1);
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::Normal,
    );
    assert!(
        closed.try_recv().is_err(),
        "cleanup must wait for the wire close send"
    );
    assert!(handler_senders.contains_key(&7));
    release.add_permits(1);
    session.await.unwrap().unwrap();
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
    assert!(!handler_senders.contains_key(&7));
    assert!(sent_rx.try_recv().is_err());
}

#[tokio::test]
async fn fifo_final_output_and_duplicate_events_keep_error_reason() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let reason = output.channel_close_reason.clone();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let result = run_handler_session(
        async move {
            callback
                .send_instruction(Bytes::from_static(b"\x20first"))
                .await?;
            callback
                .send_instruction(Bytes::from_static(b"final text"))
                .await?;
            callback.on_event(HandlerEvent::Error {
                message: "private error".to_string(),
                code: Some(519),
            });
            callback.on_event(HandlerEvent::Disconnect {
                reason: "done".to_string(),
            });
            callback.on_event(HandlerEvent::Error {
                message: "duplicate".to_string(),
                code: None,
            });
            callback.on_event(HandlerEvent::Disconnect {
                reason: "duplicate".to_string(),
            });
            Err(HandlerError::RecordingFailed(
                "private recording error".to_string(),
            ))
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    )
    .await;
    assert!(matches!(result, Err(HandlerError::RecordingFailed(_))));
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"\x20first")
    );
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"final text")
    );
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::HandlerError,
    );
    assert!(
        sent_rx.try_recv().is_err(),
        "terminal events must not emit duplicate closes"
    );
    assert_eq!(
        *reason.lock().await,
        Some(CloseConnectionReason::HandlerError)
    );
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}

#[tokio::test]
async fn dropping_callback_does_not_close_before_recording_finalization() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let (recording_tx, recording_rx) = oneshot::channel();
    let (finish_tx, finish_rx) = oneshot::channel();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let session = tokio::spawn(run_handler_session(
        async move {
            callback
                .send_instruction(Bytes::from_static(b"last"))
                .await?;
            callback.on_event(HandlerEvent::Disconnect {
                reason: "quit".to_string(),
            });
            drop(callback);
            recording_tx.send(()).unwrap();
            finish_rx.await.unwrap();
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    ));
    recording_rx.await.unwrap();
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"last")
    );
    assert!(!session.is_finished());
    assert!(sent_rx.try_recv().is_err());
    assert!(closed.try_recv().is_err());
    finish_tx.send(()).unwrap();
    session.await.unwrap().unwrap();
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::Normal,
    );
    assert!(sent_rx.try_recv().is_err());
}

#[tokio::test]
async fn threat_closes_input_and_discards_output_before_finalization() {
    let (callback, rx, terminal, mut output, mut closed) = fixture();
    output.finalization_deadline = std::time::Duration::from_millis(300);
    let (input_tx, mut input_rx) = mpsc::channel::<Bytes>(8);
    output.handler_senders.insert(7, input_tx);
    let handler_senders = output.handler_senders.clone();
    let finalized = Arc::new(AtomicBool::new(false));
    let producer_finalized = finalized.clone();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let session = tokio::spawn(run_handler_session(
        async move {
            callback
                .send_instruction(Bytes::from_static(b"discarded"))
                .await?;
            callback.on_event(HandlerEvent::ThreatDetected {
                level: "critical".to_string(),
                description: "private threat".to_string(),
            });
            while input_rx.recv().await.is_some() {}
            tokio::time::sleep(std::time::Duration::from_millis(20)).await;
            producer_finalized.store(true, Ordering::Release);
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    ));
    let close = next_frame(&mut sent_rx).await;
    assert_close(&close, CloseConnectionReason::SecurityThreat);
    assert!(
        sent_rx.try_recv().is_err(),
        "threat must discard queued output"
    );
    assert!(
        !handler_senders.contains_key(&7),
        "threat must remove input route"
    );
    assert!(
        !finalized.load(Ordering::Acquire),
        "close must not wait for finalization"
    );
    assert!(matches!(
        session.await.unwrap(),
        Err(HandlerError::SecurityViolation(_))
    ));
    assert!(finalized.load(Ordering::Acquire));
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}

#[tokio::test]
async fn send_failure_allows_live_handler_async_finalization_before_close() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let handler_senders = output.handler_senders.clone();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let finalized = Arc::new(AtomicBool::new(false));
    let producer_finalized = finalized.clone();
    let send_finalized = finalized.clone();
    let result = tokio::time::timeout(
        std::time::Duration::from_secs(1),
        run_handler_session(
            async move {
                callback
                    .send_instruction(Bytes::from_static(b"rejected"))
                    .await?;
                tokio::time::sleep(std::time::Duration::from_millis(20)).await;
                producer_finalized.store(true, Ordering::Release);
                Ok(())
            },
            rx,
            terminal,
            output,
            move |encoded| {
                if encoded[..4] == [0, 0, 0, 0] {
                    assert!(
                        send_finalized.load(Ordering::Acquire),
                        "error close must follow producer finalization"
                    );
                }
                sent_tx.send(encoded).unwrap();
                std::future::ready(Err("private transport failure".to_string()))
            },
        ),
    )
    .await
    .expect("transport failure must not hang the handler");
    assert!(matches!(result, Err(HandlerError::ChannelError(_))));
    assert!(finalized.load(Ordering::Acquire));
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"rejected")
    );
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::HandlerError,
    );
    assert!(sent_rx.try_recv().is_err());
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
    assert!(!handler_senders.contains_key(&7));
}

#[tokio::test]
async fn terminal_batching_preserves_text_boundary_before_close() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    callback
        .send_instruction(Bytes::from_static(b"\x20one"))
        .await
        .unwrap();
    callback
        .send_instruction(Bytes::from_static(b"\x20two"))
        .await
        .unwrap();
    callback
        .send_instruction(Bytes::from_static(b"text boundary"))
        .await
        .unwrap();
    callback
        .send_instruction(Bytes::from_static(b"\x20last"))
        .await
        .unwrap();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    run_handler_session(
        async move {
            drop(callback);
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    )
    .await
    .unwrap();
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"\x20one\x20two")
    );
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"text boundary")
    );
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"\x20last")
    );
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::Normal,
    );
    assert!(sent_rx.try_recv().is_err());
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}

#[tokio::test]
async fn explicit_error_survives_successful_completion_and_disconnect_duplicates() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    run_handler_session(
        async move {
            callback.on_event(HandlerEvent::Error {
                message: "private".to_string(),
                code: Some(256),
            });
            callback.on_event(HandlerEvent::Disconnect {
                reason: "done".to_string(),
            });
            callback
                .send_instruction(Bytes::from_static(b"final error instruction"))
                .await?;
            callback.on_event(HandlerEvent::Disconnect {
                reason: "duplicate".to_string(),
            });
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    )
    .await
    .unwrap();
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"final error instruction")
    );
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::HandlerError,
    );
    assert!(sent_rx.try_recv().is_err());
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}

#[tokio::test]
async fn producer_panic_drains_admitted_output_before_error_close() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let result = run_handler_session(
        async move {
            callback
                .send_instruction(Bytes::from_static(b"before panic"))
                .await?;
            panic!("handler panic")
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    )
    .await;
    assert!(matches!(result, Err(HandlerError::ChannelError(_))));
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"before panic")
    );
    assert_close(
        &next_frame(&mut sent_rx).await,
        CloseConnectionReason::HandlerError,
    );
    assert!(sent_rx.try_recv().is_err());
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}

#[tokio::test]
async fn normal_completion_seals_retained_callback_clone() {
    let (callback, rx, terminal, output, mut closed) = fixture();
    let (sent_tx, mut sent_rx) = mpsc::unbounded_channel();
    let (release_tx, release_rx) = oneshot::channel::<()>();
    let session = tokio::spawn(run_handler_session(
        async move {
            let retained = callback.clone();
            tokio::spawn(async move {
                let _ = release_rx.await;
                drop(retained);
            });
            callback
                .send_instruction(Bytes::from_static(b"final"))
                .await?;
            Ok(())
        },
        rx,
        terminal,
        output,
        move |encoded| {
            sent_tx.send(encoded).unwrap();
            std::future::ready(Ok(()))
        },
    ));
    assert_eq!(
        data_payload(&next_frame(&mut sent_rx).await),
        Bytes::from_static(b"final")
    );
    assert_close(
        &tokio::time::timeout(std::time::Duration::from_secs(1), sent_rx.recv())
            .await
            .expect("retained callback must not delay normal close")
            .expect("sender closed"),
        CloseConnectionReason::Normal,
    );
    release_tx.send(()).unwrap();
    session.await.unwrap().unwrap();
    assert_eq!(closed.recv().await.unwrap(), (7, "control".to_string()));
    assert!(closed.try_recv().is_err());
}
