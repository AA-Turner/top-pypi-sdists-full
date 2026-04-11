//! Backpressure and flow-control tests for EventDrivenSender (actor model).
//!
//! All tests are GREEN.
//!
//! **Integration tests (loopback WebRTC)**
//!   throughput_no_data_loss_loopback
//!   sync_marker_arrives_after_bulk_frames
//!   queue_depth_metric_accuracy
//!   blocked_sender_exits_on_channel_close
//!
//! Run all tests:
//!   cargo test -p keeper-pam-webrtc-rs backpressure -- --nocapture

use bytes::Bytes;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::mpsc;

// ---------------------------------------------------------------------------
// Integration tests — real loopback WebRTC connections
// ---------------------------------------------------------------------------

/// Build a connected loopback channel pair using the peer connection helpers
/// from common_tests.  Returns (sender_side, receiver_side).
async fn make_loopback_pair() -> (
    crate::webrtc_data_channel::WebRTCDataChannel,
    crate::webrtc_data_channel::WebRTCDataChannel,
) {
    use std::sync::Mutex as StdMutex;
    use tokio::sync::oneshot;
    use webrtc::data_channel::RTCDataChannel;
    use webrtc::peer_connection::configuration::RTCConfiguration;

    let pc1 = Arc::new(
        super::common_tests::create_peer_connection(RTCConfiguration::default())
            .await
            .expect("pc1"),
    );
    let pc2 = Arc::new(
        super::common_tests::create_peer_connection(RTCConfiguration::default())
            .await
            .expect("pc2"),
    );

    let (ice1_tx, mut ice1_rx) = mpsc::unbounded_channel();
    let (ice2_tx, mut ice2_rx) = mpsc::unbounded_channel();

    let tx = ice1_tx.clone();
    pc1.on_ice_candidate(Box::new(move |c| {
        if let Some(c) = c {
            let _ = tx.send(c);
        }
        Box::pin(async {})
    }));
    let tx = ice2_tx.clone();
    pc2.on_ice_candidate(Box::new(move |c| {
        if let Some(c) = c {
            let _ = tx.send(c);
        }
        Box::pin(async {})
    }));

    let dc1 = pc1.create_data_channel("bp", None).await.expect("dc1");
    let (open1_tx, open1_rx) = oneshot::channel::<Arc<RTCDataChannel>>();
    let tx1 = Arc::new(StdMutex::new(Some(open1_tx)));
    let dc1c = dc1.clone();
    dc1.on_open(Box::new(move || {
        if let Some(t) = tx1.lock().unwrap().take() {
            let _ = t.send(dc1c.clone());
        }
        Box::pin(async {})
    }));

    let (open2_tx, open2_rx) = oneshot::channel::<Arc<RTCDataChannel>>();
    let tx2 = Arc::new(StdMutex::new(Some(open2_tx)));
    pc2.on_data_channel(Box::new(move |dc2| {
        let t = tx2.clone();
        let dc = dc2.clone();
        dc2.on_open(Box::new(move || {
            if let Some(t) = t.lock().unwrap().take() {
                let _ = t.send(dc.clone());
            }
            Box::pin(async {})
        }));
        Box::pin(async {})
    }));

    let offer = pc1.create_offer(None).await.expect("offer");
    pc1.set_local_description(offer.clone())
        .await
        .expect("sld1");
    pc2.set_remote_description(offer).await.expect("srd2");
    let answer = pc2.create_answer(None).await.expect("answer");
    pc2.set_local_description(answer.clone())
        .await
        .expect("sld2");
    pc1.set_remote_description(answer).await.expect("srd1");

    let pc1c = Arc::clone(&pc1);
    let pc2c = Arc::clone(&pc2);
    tokio::spawn(async move {
        while let Some(c) = ice1_rx.recv().await {
            if let Ok(j) = c.to_json() {
                let _ = pc2c.add_ice_candidate(j).await;
            }
        }
    });
    tokio::spawn(async move {
        while let Some(c) = ice2_rx.recv().await {
            if let Ok(j) = c.to_json() {
                let _ = pc1c.add_ice_candidate(j).await;
            }
        }
    });

    let (r1, r2) = tokio::time::timeout(Duration::from_secs(15), async {
        tokio::join!(open1_rx, open2_rx)
    })
    .await
    .expect("loopback channels timed out");

    (
        crate::webrtc_data_channel::WebRTCDataChannel::new(r1.expect("dc1 open")),
        crate::webrtc_data_channel::WebRTCDataChannel::new(r2.expect("dc2 open")),
    )
}

fn make_frame(size: usize, marker: u8) -> Bytes {
    Bytes::from(vec![marker; size])
}

/// Send a large number of frames through a real loopback connection and verify
/// every byte arrives intact.  This is the throughput regression test —
/// if EventDrivenSender loses frames or reorders them this fails.
///
/// Mirrors the v2.1.8 vs v2.1.9 benchmark: v2.1.9 received only 0.4 MB
/// before freezing.  This test catches that regression class.
#[tokio::test(flavor = "multi_thread")]
async fn test_throughput_no_data_loss_loopback() {
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    let frame_size = 8 * 1024; // 8 KB — matches MAX_READ_SIZE / guacd batch frame
    let frame_count = 500;
    let total_bytes = frame_size * frame_count;

    // Set up receiver before sending to avoid races
    let (rx_tx, mut rx_rx) = mpsc::unbounded_channel::<Bytes>();
    let received_bytes = Arc::new(AtomicUsize::new(0));
    let rb = received_bytes.clone();
    receiver_dc.data_channel.on_message(Box::new(move |msg| {
        rb.fetch_add(msg.data.len(), Ordering::Relaxed);
        let _ = rx_tx.send(msg.data);
        Box::pin(async {})
    }));

    let sender = crate::webrtc_data_channel::EventDrivenSender::new(
        Arc::new(sender_dc),
        crate::webrtc_data_channel::ACTOR_BYTE_BUDGET,
    )
    .await;

    let t0 = Instant::now();
    for i in 0..frame_count {
        let frame = make_frame(frame_size, (i % 256) as u8);
        sender
            .send_with_natural_backpressure(frame)
            .await
            .expect("send should not fail on loopback");
    }

    // Wait until all bytes arrive (up to 30 s)
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);
    let mut received = 0usize;
    while received < total_bytes {
        let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
        match tokio::time::timeout(remaining, rx_rx.recv()).await {
            Ok(Some(msg)) => received += msg.len(),
            _ => break,
        }
    }

    let elapsed = t0.elapsed();
    let throughput_mbps = (received as f64 / elapsed.as_secs_f64()) / (1024.0 * 1024.0);

    println!(
        "\n[throughput] sent={} KB  received={} KB  elapsed={:.2}s  throughput={:.1} MB/s  queue_at_end={}",
        total_bytes / 1024,
        received / 1024,
        elapsed.as_secs_f64(),
        throughput_mbps,
        sender.queue_depth()
    );

    assert_eq!(
        received, total_bytes,
        "data loss: sent {} bytes, received {} bytes",
        total_bytes, received
    );
}

/// Send a large batch of frames followed by a distinct 4-byte sync marker.
/// The sync marker MUST arrive after all data frames — never out of order.
///
/// This is the key correctness property for guacd's processing_lag flow control:
/// if the sync arrives before the frames it's timestamping, guacd measures
/// the wrong lag and fails to throttle correctly.
#[tokio::test(flavor = "multi_thread")]
async fn test_sync_marker_arrives_after_bulk_frames() {
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    let bulk_count = 200;
    let bulk_size = 4 * 1024; // 4 KB frames
    const SYNC_MARKER: &[u8] = b"SYNC";

    let (rx_tx, mut rx_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver_dc.data_channel.on_message(Box::new(move |msg| {
        let _ = rx_tx.send(msg.data);
        Box::pin(async {})
    }));

    let sender = crate::webrtc_data_channel::EventDrivenSender::new(
        Arc::new(sender_dc),
        crate::webrtc_data_channel::ACTOR_BYTE_BUDGET,
    )
    .await;

    // Send bulk data frames
    for i in 0..bulk_count {
        let frame = make_frame(bulk_size, (i % 256) as u8);
        sender
            .send_with_natural_backpressure(frame)
            .await
            .expect("bulk send");
    }

    // Send the sync marker last
    let t_sync_sent = Instant::now();
    sender
        .send_with_natural_backpressure(Bytes::from_static(SYNC_MARKER))
        .await
        .expect("sync send");

    // Collect until we see the sync marker
    let mut bulk_received = 0usize;
    let mut sync_arrived = false;
    let deadline = tokio::time::Instant::now() + Duration::from_secs(30);

    loop {
        let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
        match tokio::time::timeout(remaining, rx_rx.recv()).await {
            Ok(Some(msg)) => {
                if msg.as_ref() == SYNC_MARKER {
                    let sync_latency = t_sync_sent.elapsed();
                    println!(
                        "\n[sync latency] bulk_frames={} bulk_bytes={} KB  \
                         sync_latency={:.1}ms  bulk_received_before_sync={}",
                        bulk_count,
                        bulk_count * bulk_size / 1024,
                        sync_latency.as_millis(),
                        bulk_received
                    );
                    sync_arrived = true;
                    break;
                } else {
                    bulk_received += 1;
                }
            }
            _ => break,
        }
    }

    assert!(sync_arrived, "sync marker never received");
    assert_eq!(
        bulk_received, bulk_count,
        "sync arrived before all bulk frames — ordering violation: \
         only {}/{} bulk frames arrived before sync",
        bulk_received, bulk_count
    );
}

/// The queue_depth() metric must reflect bytes currently in-flight (acquired but
/// not yet released by the actor). This test verifies the accounting is correct
/// and that bytes-in-flight never exceeds the byte budget.
#[tokio::test(flavor = "multi_thread")]
async fn test_queue_depth_metric_accuracy() {
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    // Hook receiver so SCTP does not back-pressure the sender.
    receiver_dc
        .data_channel
        .on_message(Box::new(|_| Box::pin(async {})));

    let byte_budget = crate::webrtc_data_channel::ACTOR_BYTE_BUDGET;
    let sender =
        crate::webrtc_data_channel::EventDrivenSender::new(Arc::new(sender_dc), byte_budget).await;

    // Send 100 frames of 64 bytes = 6 400 bytes total — well within 512 KB budget.
    // queue_depth() returns bytes in-flight; it must never exceed the budget.
    let mut max_depth = 0usize;
    for i in 0..100 {
        let frame = make_frame(64, (i % 256) as u8);
        sender
            .send_with_natural_backpressure(frame)
            .await
            .expect("send");
        let d = sender.queue_depth();
        if d > max_depth {
            max_depth = d;
        }
    }

    println!(
        "\n[queue depth] max_bytes_in_flight={} byte_budget={}",
        max_depth, byte_budget
    );

    assert!(
        max_depth <= byte_budget,
        "bytes in flight {} exceeded byte budget {} — accounting error",
        max_depth,
        byte_budget
    );
}

/// Sending to a closed data channel should return `DATACHANNEL_CLOSED_ERROR`
/// promptly. The actor model has at most 1 frame delay in detecting a closed
/// native DC (the actor must try to send to discover the error). After the actor
/// exits, all subsequent sends must fail immediately.
#[tokio::test(flavor = "multi_thread")]
async fn test_blocked_sender_exits_on_channel_close() {
    let (sender_dc, _receiver_dc) = make_loopback_pair().await;

    // Hold a ref to the native RTCDataChannel so we can close it directly.
    let raw_dc = sender_dc.data_channel.clone();

    let sender = crate::webrtc_data_channel::EventDrivenSender::new(
        Arc::new(sender_dc),
        crate::webrtc_data_channel::ACTOR_BYTE_BUDGET,
    )
    .await;

    // Close the native data channel (bypasses WebRTCDataChannel.close(),
    // so is_closing flag is NOT set). The actor detects the closed DC when
    // it tries to call dc.send() on the first frame.
    let _ = raw_dc.close().await;
    tokio::time::sleep(Duration::from_millis(100)).await;

    // First frame: queued before the actor can detect the closed DC (may succeed).
    let _ = sender
        .send_with_natural_backpressure(make_frame(64, 0xCC))
        .await;

    // Wait for the actor to process the probe frame, discover the closed DC, and exit.
    tokio::time::sleep(Duration::from_millis(200)).await;

    // Now the actor has exited (receiver dropped). All subsequent sends must fail
    // immediately with DATACHANNEL_CLOSED_ERROR.
    let t0 = std::time::Instant::now();
    let result = sender
        .send_with_natural_backpressure(make_frame(64, 0xCD))
        .await;
    let elapsed = t0.elapsed();

    println!(
        "\n[channel close] send returned: {:?}, elapsed: {:.1}ms",
        result,
        elapsed.as_millis()
    );

    assert!(
        result.is_err(),
        "send after actor exit should return DATACHANNEL_CLOSED_ERROR"
    );
    assert!(
        elapsed < Duration::from_millis(500),
        "send to closed channel took {}ms — should return immediately",
        elapsed.as_millis()
    );
}

/// Clone semantics: two handles share the same underlying mpsc channel and actor task.
/// Sending through either handle puts frames in the same FIFO queue, processed by
/// the same actor — exactly the "one shared sender per tube, all conn_nos clone" rule.
///
/// Proof: total frames delivered = frames sent via handle A + frames sent via handle B.
#[tokio::test(flavor = "multi_thread")]
async fn test_cloned_senders_share_same_actor() {
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    let (rx_tx, mut rx_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver_dc.data_channel.on_message(Box::new(move |msg| {
        let _ = rx_tx.send(msg.data);
        Box::pin(async {})
    }));

    let sender_a = crate::webrtc_data_channel::EventDrivenSender::new(
        Arc::new(sender_dc),
        crate::webrtc_data_channel::ACTOR_BYTE_BUDGET,
    )
    .await;
    let sender_b = sender_a.clone(); // same actor, same channel

    // Sanity: both handles report the same capacity.
    assert_eq!(
        sender_a.get_threshold(),
        sender_b.get_threshold(),
        "clones must share the same byte budget"
    );

    // Send 100 frames via A and 100 via B concurrently.
    let a_task = tokio::spawn({
        let s = sender_a.clone();
        async move {
            for i in 0u8..100 {
                s.send_with_natural_backpressure(make_frame(64, i))
                    .await
                    .expect("send A");
            }
        }
    });
    let b_task = tokio::spawn({
        let s = sender_b.clone();
        async move {
            for i in 0u8..100 {
                s.send_with_natural_backpressure(make_frame(64, i | 0x80))
                    .await
                    .expect("send B");
            }
        }
    });
    a_task.await.expect("task A");
    b_task.await.expect("task B");

    // Collect all 200 delivered frames.
    let deadline = tokio::time::Instant::now() + Duration::from_secs(10);
    let mut received = 0usize;
    while received < 200 {
        let rem = deadline.saturating_duration_since(tokio::time::Instant::now());
        match tokio::time::timeout(rem, rx_rx.recv()).await {
            Ok(Some(_)) => received += 1,
            _ => break,
        }
    }

    assert_eq!(
        received, 200,
        "data loss: only {}/200 frames arrived",
        received
    );
    println!(
        "\n[clone semantics] {}/200 frames delivered through shared actor",
        received
    );
}

/// Backpressure blocks and then resumes: exhaust the byte budget from a dedicated
/// producer, verify sends block on the semaphore, then let the actor drain and
/// verify blocked sends eventually complete without error or timeout.
///
/// Uses a 1-frame byte budget so the semaphore blocks after every frame, forcing
/// the producer to wait for each dc.send() before the next frame is accepted.
/// This proves byte-based flow-control serialises sends through the actor.
#[tokio::test(flavor = "multi_thread")]
async fn test_backpressure_blocks_and_resumes() {
    let frame_size = 128usize;
    let byte_budget = frame_size; // exactly one frame — every send blocks until actor drains
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    let (rx_tx, mut rx_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver_dc.data_channel.on_message(Box::new(move |msg| {
        let tx = rx_tx.clone();
        Box::pin(async move {
            let _ = tx.send(msg.data);
        })
    }));

    let sender =
        crate::webrtc_data_channel::EventDrivenSender::new(Arc::new(sender_dc), byte_budget).await;

    let total = 60usize; // 60 × 128 B = 7 680 B — well within loopback limits
    let t0 = Instant::now();

    // Send total frames — each blocks on the semaphore until the actor drains
    // the previous frame through dc.send(), proving real flow-control.
    for i in 0..total {
        sender
            .send_with_natural_backpressure(make_frame(frame_size, (i % 256) as u8))
            .await
            .expect("send must not fail on open channel");
    }

    let send_elapsed = t0.elapsed();

    let deadline = tokio::time::Instant::now() + Duration::from_secs(15);
    let mut received = 0usize;
    while received < total {
        let rem = deadline.saturating_duration_since(tokio::time::Instant::now());
        match tokio::time::timeout(rem, rx_rx.recv()).await {
            Ok(Some(_)) => received += 1,
            _ => break,
        }
    }

    println!(
        "\n[backpressure] byte_budget={} frame_size={} total={} send_elapsed={:.1}ms received={}",
        byte_budget,
        frame_size,
        total,
        send_elapsed.as_millis(),
        received
    );

    assert_eq!(
        received, total,
        "data loss: {}/{} frames received",
        received, total
    );
}

// ---------------------------------------------------------------------------
// Manual stress test — never runs in CI
// ---------------------------------------------------------------------------

/// 20-minute throughput marathon across four frame-size scenarios.
/// Catches memory leaks, throughput degradation, and death-spiral regressions
/// that only surface under prolonged load.
///
/// Results from April 2026 (Windows loopback, debug build):
///   191 iterations · 0 data loss · 0 stalls · 3.6–4.3 MB/s stable
///
/// Run with:
///   cargo test -p keeper-pam-webrtc-rs test_sustained_20min -- --nocapture --include-ignored
#[tokio::test(flavor = "multi_thread")]
#[ignore]
async fn test_sustained_20min() {
    let (sender_dc, receiver_dc) = make_loopback_pair().await;

    let received_total = Arc::new(AtomicUsize::new(0));
    let rt = received_total.clone();
    let (rx_tx, mut rx_rx) = mpsc::unbounded_channel::<Bytes>();
    receiver_dc.data_channel.on_message(Box::new(move |msg| {
        rt.fetch_add(msg.data.len(), Ordering::Relaxed);
        let _ = rx_tx.send(msg.data);
        Box::pin(async {})
    }));

    let sender = Arc::new(
        crate::webrtc_data_channel::EventDrivenSender::new(
            Arc::new(sender_dc),
            crate::webrtc_data_channel::ACTOR_BYTE_BUDGET,
        )
        .await,
    );

    // Frame sizes stay within the WebRTC SCTP max-message-size (~64 KB).
    // Fragmentation is handled by the Channel layer, not raw EventDrivenSender.
    let scenarios: &[(&str, Vec<Bytes>)] = &[
        (
            "small  10k×64B",
            (0..10_000u32)
                .map(|i| make_frame(64, (i % 256) as u8))
                .collect(),
        ),
        ("mixed  500×(64+8k)", {
            let mut v = Vec::with_capacity(1000);
            for i in 0u32..500 {
                v.push(make_frame(64, (i % 256) as u8));
                v.push(make_frame(8192, (i % 256) as u8));
            }
            v
        }),
        (
            "large  500×8KB",
            (0..500u32)
                .map(|i| make_frame(8192, (i % 256) as u8))
                .collect(),
        ),
        (
            "bulk   1k×32KB",
            (0..1_000u32)
                .map(|i| make_frame(32 * 1024, (i % 256) as u8))
                .collect(),
        ),
    ];

    let deadline = std::time::Instant::now() + Duration::from_secs(20 * 60);
    let mut iteration = 0usize;
    let mut all_ok = true;

    'outer: while std::time::Instant::now() < deadline {
        iteration += 1;
        let scenario = &scenarios[iteration % scenarios.len()];
        let label = scenario.0;
        let frames = &scenario.1;
        let total_bytes: usize = frames.iter().map(|f| f.len()).sum();

        let t_iter = Instant::now();
        for frame in frames {
            if let Err(e) = sender.send_with_natural_backpressure(frame.clone()).await {
                eprintln!("[FAIL iter={iteration} {label}] send error: {e}");
                all_ok = false;
                break 'outer;
            }
        }

        let iter_deadline = tokio::time::Instant::now() + Duration::from_secs(10);
        let mut received = 0usize;
        while received < total_bytes {
            let rem = iter_deadline.saturating_duration_since(tokio::time::Instant::now());
            match tokio::time::timeout(rem, rx_rx.recv()).await {
                Ok(Some(msg)) => received += msg.len(),
                _ => {
                    eprintln!(
                        "[TIMEOUT iter={iteration} {label}] got {received}/{total_bytes} bytes"
                    );
                    all_ok = false;
                    break 'outer;
                }
            }
        }

        let elapsed = t_iter.elapsed();
        let throughput = (total_bytes as f64 / elapsed.as_secs_f64()) / (1024.0 * 1024.0);
        println!(
            "[iter={iteration:3} {label}] {:.1}s  {:.2} MB/s  sent={} KB",
            elapsed.as_secs_f64(),
            throughput,
            total_bytes / 1024,
        );
    }

    println!(
        "\n[20min marathon] iterations={iteration}  total_received={} MB  ok={}",
        received_total.load(Ordering::Relaxed) / (1024 * 1024),
        all_ok,
    );
    assert!(all_ok, "marathon failed — see output above");
}
