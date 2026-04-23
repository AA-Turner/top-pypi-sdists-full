use bytes::Bytes;
#[cfg(test)]
use futures::future::BoxFuture;
use log::{debug, warn};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::{mpsc, Semaphore};
use webrtc::data_channel::RTCDataChannel;

// Lock-free queue for pending frames - uses crossbeam's SegQueue
use crossbeam_queue::SegQueue;

/// WebRTC RECEIVE_MTU (8 KB). Used by adaptive_pool and core.rs to compare against
/// the native buffered-amount counter — not related to EventDrivenSender frame counts.
pub const STANDARD_BUFFER_THRESHOLD: u64 = 8 * 1024; // 8 KB

/// Actor byte budget: maximum bytes buffered in the per-tube send queue before
/// send_with_natural_backpressure blocks. Acts as a hard OOM guard.
pub const ACTOR_BYTE_BUDGET: usize = 512 * 1024; // 512 KB per tube

/// SCTP send buffer high-water mark. The outbound task stops reading from the backend
/// when buffered_amount exceeds this, preventing unbounded queue growth on any protocol.
/// At 160 KB/s TURN this caps queue latency at ~200ms — well under guacd's 15s sync
/// timeout and natural for TCP-based protocols (port forward, database proxy, etc.).
pub const SCTP_HIGH_WATER: usize = 32 * 1024; // 32 KB

const DATACHANNEL_CLOSED_ERROR: &str = "DataChannel closed";
pub(crate) const QUEUE_FULL_ERROR: &str = "DataChannel queue full";

#[cfg(test)]
type TestSendHook = Arc<
    std::sync::Mutex<Option<Box<dyn Fn(Bytes) -> BoxFuture<'static, ()> + Send + Sync + 'static>>>,
>;

// Async-first wrapper for data channel functionality
pub struct WebRTCDataChannel {
    pub data_channel: Arc<RTCDataChannel>,
    pub(crate) is_closing: Arc<AtomicBool>,
    /// Notification for when data channel opens - allows multiple waiters without callback conflicts
    pub(crate) open_notify: Arc<tokio::sync::Notify>,
    /// Flag indicating if data channel is open - set once and never reset
    pub(crate) is_open: Arc<AtomicBool>,

    /// Early message buffer - captures messages arriving before handlers are ready.
    /// This is critical for on_data_channel callbacks where messages can arrive
    /// before setup_channel_for_data_channel completes (~100ms race window).
    /// Uses lock-free SegQueue for zero-contention message capture.
    pub(crate) early_message_buffer: Arc<SegQueue<Bytes>>,
    /// Count of messages in early buffer (for logging/debugging)
    pub(crate) early_message_count: Arc<AtomicUsize>,
    /// Flag indicating if early buffering is active (set to false once real handler takes over)
    pub(crate) early_buffering_active: Arc<AtomicBool>,

    #[cfg(test)]
    pub(crate) test_send_hook: TestSendHook,
}

impl Clone for WebRTCDataChannel {
    fn clone(&self) -> Self {
        Self {
            data_channel: Arc::clone(&self.data_channel),
            is_closing: Arc::clone(&self.is_closing),
            open_notify: Arc::clone(&self.open_notify),
            is_open: Arc::clone(&self.is_open),
            early_message_buffer: Arc::clone(&self.early_message_buffer),
            early_message_count: Arc::clone(&self.early_message_count),
            early_buffering_active: Arc::clone(&self.early_buffering_active),

            #[cfg(test)]
            test_send_hook: Arc::clone(&self.test_send_hook),
        }
    }
}

impl WebRTCDataChannel {
    pub fn new(data_channel: Arc<RTCDataChannel>) -> Self {
        let open_notify = Arc::new(tokio::sync::Notify::new());
        let is_open = Arc::new(AtomicBool::new(false));

        // Early message buffering - captures messages before real handler is set up
        let early_message_buffer = Arc::new(SegQueue::new());
        let early_message_count = Arc::new(AtomicUsize::new(0));
        let early_buffering_active = Arc::new(AtomicBool::new(true));

        // Check if already open (for received data channels that may already be open)
        let already_open = data_channel.ready_state()
            == webrtc::data_channel::data_channel_state::RTCDataChannelState::Open;
        if already_open {
            is_open.store(true, Ordering::Release);
            open_notify.notify_waiters();
        }

        // Set up on_open callback to notify waiters (this is the ONLY place on_open is set)
        let is_open_for_callback = Arc::clone(&is_open);
        let open_notify_for_callback = Arc::clone(&open_notify);
        data_channel.on_open(Box::new(move || {
            is_open_for_callback.store(true, Ordering::Release);
            open_notify_for_callback.notify_waiters();
            Box::pin(async {})
        }));

        // CRITICAL: Set up early message buffering IMMEDIATELY.
        // This captures messages that arrive before setup_channel_for_data_channel
        // completes (there can be a ~100ms race window in on_data_channel callbacks).
        let early_buffer_for_callback = Arc::clone(&early_message_buffer);
        let early_count_for_callback = Arc::clone(&early_message_count);
        let early_active_for_callback = Arc::clone(&early_buffering_active);
        let label_for_log = data_channel.label().to_string();
        data_channel.on_message(Box::new(move |msg| {
            let buffer = Arc::clone(&early_buffer_for_callback);
            let count = Arc::clone(&early_count_for_callback);
            let active = Arc::clone(&early_active_for_callback);
            let label = label_for_log.clone();
            let data = Bytes::copy_from_slice(&msg.data);

            Box::pin(async move {
                // Only buffer if early buffering is still active
                if active.load(Ordering::Acquire) {
                    let msg_count = count.fetch_add(1, Ordering::AcqRel) + 1;
                    buffer.push(data);
                    debug!(
                        "[EARLY_BUFFER] Captured early message #{} ({} bytes) on channel '{}' before handler ready",
                        msg_count, buffer.len(), label
                    );
                }
                // If early_buffering_active is false, this callback should have been
                // replaced by the real handler - but if not, the message is dropped
                // (this shouldn't happen in normal operation)
            })
        }));

        Self {
            data_channel,
            is_closing: Arc::new(AtomicBool::new(false)),
            open_notify,
            is_open,
            early_message_buffer,
            early_message_count,
            early_buffering_active,

            #[cfg(test)]
            test_send_hook: Arc::new(std::sync::Mutex::new(None)),
        }
    }

    // Add a test method to set the sending hook for testing
    #[cfg(test)]
    pub fn set_test_send_hook<F>(&self, hook: F)
    where
        F: Fn(Bytes) -> BoxFuture<'static, ()> + Send + Sync + 'static,
    {
        if let Ok(mut guard) = self.test_send_hook.lock() {
            *guard = Some(Box::new(hook));
        }
    }

    pub async fn send(&self, data: Bytes) -> Result<(), String> {
        // Check if closing
        if self.is_closing.load(Ordering::Acquire) {
            return Err("Channel is closing".to_string());
        }

        // For testing: call the test hook if set
        #[cfg(test)]
        {
            if let Ok(hook_guard) = self.test_send_hook.lock() {
                if let Some(ref hook) = *hook_guard {
                    // Clone the data for the hook
                    let data_clone = data.clone();

                    // Call the hook with a clone of the data
                    let hook_future = hook(data_clone);

                    // Spawn the hook execution to avoid blocking
                    tokio::spawn(hook_future);
                }
            }
        }

        // Send data with detailed error handling
        let result = self
            .data_channel
            .send(&data)
            .await
            .map(|_| ())
            .map_err(|e| format!("Failed to send data: {e}"));

        // No need to manually monitor buffered amount - we rely on the native WebRTC event
        // The onBufferedAmountLow event will fire when the buffer drops below the threshold

        result
    }

    pub async fn buffered_amount(&self) -> u64 {
        // Early return if the channel is closing
        if self.is_closing.load(Ordering::Acquire) {
            return 0;
        }

        self.data_channel.buffered_amount().await as u64
    }

    /// Wait for the data channel to be open, with an optional timeout.
    /// Returns Ok(true) if channel opened, Ok(false) if closed/timeout, Err if closing.
    /// This is essential for server-mode channels to wait before accepting TCP connections.
    ///
    /// This uses a simple polling approach combined with the shared notification to be
    /// robust against callback conflicts. Even if callbacks are overwritten elsewhere,
    /// we'll still detect the open state via polling.
    pub async fn wait_for_channel_open(&self, timeout: Option<Duration>) -> Result<bool, String> {
        let timeout_duration = timeout.unwrap_or(Duration::from_secs(10));
        let poll_interval = Duration::from_millis(50);
        let deadline = tokio::time::Instant::now() + timeout_duration;
        let label = self.data_channel.label().to_string();

        debug!(
            "Waiting for data channel to open: {} (timeout: {:?})",
            label, timeout_duration
        );

        loop {
            let current_state = self.data_channel.ready_state();

            // Check if already closed (expected during cleanup, not an error)
            if self.is_closing.load(Ordering::Acquire) {
                debug!(
                    "wait_for_channel_open: channel closing (expected during cleanup): channel={}",
                    label
                );
                return Err("Data channel is closing".to_string());
            }

            // Check if open via our flag (set by on_open callback)
            if self.is_open.load(Ordering::Acquire) {
                return Ok(true);
            }

            // Also check native state (in case callback was overwritten)
            if current_state == webrtc::data_channel::data_channel_state::RTCDataChannelState::Open
            {
                // Update our flag to match
                debug!(
                    "Data channel opened (detected via native state polling): {}",
                    label
                );
                self.is_open.store(true, Ordering::Release);
                self.open_notify.notify_waiters();
                return Ok(true);
            }

            // Check for timeout
            if tokio::time::Instant::now() >= deadline {
                warn!(
                    "Data channel did not open within timeout ({:?}), final state: {:?} (channel: {})",
                    timeout_duration, current_state, label
                );
                return Ok(false);
            }

            // Use select to wait for either notification or poll interval
            // This combines event-driven and polling for robustness
            tokio::select! {
                _ = self.open_notify.notified() => {
                    // Notification received, check state again
                    continue;
                }
                _ = tokio::time::sleep(poll_interval) => {
                    // Poll interval, check state again
                    continue;
                }
            }
        }
    }

    pub async fn close(&self) -> Result<(), String> {
        // Avoid duplicate close operations
        if self.is_closing.swap(true, Ordering::AcqRel) {
            return Ok(()); // Already closing or closed
        }

        // Close with timeout to avoid hanging
        match tokio::time::timeout(Duration::from_secs(3), self.data_channel.close()).await {
            Ok(result) => result.map_err(|e| format!("Failed to close data channel: {e}")),
            Err(_) => {
                warn!("Data channel close operation timed out, forcing abandonment");
                Ok(()) // Force success even though it timed out
            }
        }
    }

    /// Wait for the WebRTC buffer to drain (without closing the channel).
    ///
    /// Use this when you've just sent an important message (like an error or
    /// disconnect notification) and want to ensure it's transmitted before
    /// the connection task exits. Does NOT close the channel.
    ///
    /// # Arguments
    /// * `timeout` - Maximum time to wait for buffer to drain
    ///
    /// # Returns
    /// * `true` - Buffer drained completely
    /// * `false` - Timeout reached, data may still be buffered
    pub async fn drain(&self, timeout: Duration) -> bool {
        let start = std::time::Instant::now();

        while start.elapsed() < timeout {
            // Check if already closing (buffer will report 0)
            if self.is_closing.load(Ordering::Acquire) {
                return true;
            }

            let buffered = self.data_channel.buffered_amount().await;
            if buffered == 0 {
                return true;
            }
            // Cooperative yield - avoids busy loop, no timer overhead
            tokio::task::yield_now().await;
        }

        warn!(
            "WebRTC buffer drain timeout after {:?}, data may still be buffered",
            timeout
        );
        false
    }

    pub fn ready_state(&self) -> String {
        // Fast path for closing
        if self.is_closing.load(Ordering::Acquire) {
            return "Closed".to_string();
        }

        format!("{:?}", self.data_channel.ready_state())
    }

    pub fn label(&self) -> String {
        self.data_channel.label().to_string()
    }

    /// Take ownership of all early-buffered messages and disable early buffering.
    ///
    /// CRITICAL: This must be called by setup_channel_for_data_channel AFTER
    /// setting the real on_message handler. The correct order is:
    /// 1. Set new on_message handler (replaces early buffer callback)
    /// 2. Call take_early_messages() to drain buffer
    /// 3. Forward returned messages to the channel
    ///
    /// This order ensures no messages are lost:
    /// - Messages arriving after step 1 go directly to new handler
    /// - Messages that arrived before step 1 are returned by step 2
    ///
    /// After this call:
    /// - early_buffering_active is set to false
    /// - All buffered messages are returned
    ///
    /// # Returns
    /// Vec of early messages in arrival order, empty if none were buffered
    pub fn take_early_messages(&self) -> Vec<Bytes> {
        // Disable early buffering FIRST (atomic release)
        self.early_buffering_active.store(false, Ordering::Release);

        // Drain all buffered messages
        let mut messages = Vec::new();
        while let Some(msg) = self.early_message_buffer.pop() {
            messages.push(msg);
        }

        let count = self.early_message_count.load(Ordering::Acquire);
        if !messages.is_empty() {
            log::info!(
                "[EARLY_BUFFER] Drained {} early messages from channel '{}' (total captured: {})",
                messages.len(),
                self.label(),
                count
            );
        }

        messages
    }
}

/// Actor-model sender: one background tokio task per tube is the sole caller of
/// `dc.send()`. TCP reader tasks acquire byte permits then push to an unbounded
/// channel; the actor releases permits after each successful send.
///
/// Using a byte-based semaphore rather than a fixed frame count bounds memory
/// regardless of frame size — 64-byte SSH frames get ~8 000 slots before blocking;
/// 32-KB RDP tiles get ~16. Both stay within `byte_budget` per tube.
///
/// This eliminates the drain callback, two-queue system, drain_active flag,
/// adaptive EMA, and drain_notify machinery that the previous EventDrivenSender
/// required to prevent concurrent SCTP writes on Windows IOCP.
pub struct EventDrivenSender {
    tx: mpsc::UnboundedSender<Bytes>,
    budget: Arc<Semaphore>,
    byte_budget: usize,
    /// Mirrors WebRTCDataChannel.is_closing — lets send_with_natural_backpressure
    /// return DATACHANNEL_CLOSED_ERROR immediately when the channel is going away
    /// without needing the full WebRTCDataChannel reference.
    is_closing: Arc<AtomicBool>,
}

impl Clone for EventDrivenSender {
    fn clone(&self) -> Self {
        Self {
            tx: self.tx.clone(),
            budget: Arc::clone(&self.budget),
            byte_budget: self.byte_budget,
            is_closing: Arc::clone(&self.is_closing),
        }
    }
}

impl EventDrivenSender {
    /// Spawn the per-tube send actor and return the sender handle.
    ///
    /// `byte_budget` is the maximum bytes that may be queued before sends block.
    /// Use `ACTOR_BYTE_BUDGET` (512 KB) for normal connections.
    pub async fn new(data_channel: Arc<WebRTCDataChannel>, byte_budget: usize) -> Self {
        let (tx, mut rx) = mpsc::unbounded_channel::<Bytes>();
        let budget = Arc::new(Semaphore::new(byte_budget));
        let is_closing = Arc::clone(&data_channel.is_closing);
        let dc_for_actor = Arc::clone(&data_channel);
        let budget_for_actor = Arc::clone(&budget);

        tokio::spawn(async move {
            // Last-resort escape hatch: if dc.send() hangs longer than this (e.g. the
            // WebRTC connection is dead but ICE hasn't timed out yet), treat it as a
            // permanent failure rather than blocking the actor forever.
            const ACTOR_SEND_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(30);

            while let Some(frame) = rx.recv().await {
                let permits = (frame.len().min(byte_budget) as u32).max(1) as usize;
                match tokio::time::timeout(ACTOR_SEND_TIMEOUT, dc_for_actor.send(frame)).await {
                    Ok(Ok(_)) => {
                        budget_for_actor.add_permits(permits);
                    }
                    Ok(Err(e)) => {
                        debug!("Actor send failed, closing channel: {}", e);
                        budget_for_actor.close();
                        return;
                    }
                    Err(_) => {
                        debug!("Actor dc.send() timed out after 30s, closing channel");
                        budget_for_actor.close();
                        return;
                    }
                }
            }
            // rx.recv() returned None: all senders dropped, normal shutdown.
        });

        Self {
            tx,
            budget,
            byte_budget,
            is_closing,
        }
    }

    /// Non-blocking send: acquires byte-budget permits and pushes `frame` to the actor.
    ///
    /// Returns immediately with:
    /// - `Ok(())` — permits acquired, frame queued.
    /// - `Err(QUEUE_FULL_ERROR)` — budget exhausted; caller should back off and retry.
    /// - `Err(DATACHANNEL_CLOSED_ERROR)` — channel closing or actor dead.
    pub fn try_send(&self, frame: Bytes) -> Result<(), &'static str> {
        if self.is_closing.load(Ordering::Acquire) {
            return Err(DATACHANNEL_CLOSED_ERROR);
        }
        let permits = (frame.len().min(self.byte_budget) as u32).max(1);
        match self.budget.try_acquire_many(permits) {
            Ok(permit) => {
                permit.forget();
                match self.tx.send(frame) {
                    Ok(()) => Ok(()),
                    Err(_) => {
                        self.budget.add_permits(permits as usize);
                        Err(DATACHANNEL_CLOSED_ERROR)
                    }
                }
            }
            Err(tokio::sync::TryAcquireError::NoPermits) => Err(QUEUE_FULL_ERROR),
            Err(tokio::sync::TryAcquireError::Closed) => Err(DATACHANNEL_CLOSED_ERROR),
        }
    }

    /// Push a frame into the actor's channel, backing off 10 ms when the budget is
    /// exhausted rather than blocking indefinitely on the semaphore.
    ///
    /// The caller is never stuck: if the actor is genuinely dead (semaphore closed
    /// by the actor's error path, or `is_closing` set), the loop exits immediately
    /// with `Err(DATACHANNEL_CLOSED_ERROR)`.
    pub async fn send_with_natural_backpressure(&self, frame: Bytes) -> Result<(), &'static str> {
        loop {
            match self.try_send(frame.clone()) {
                Ok(()) => return Ok(()),
                Err(QUEUE_FULL_ERROR) => {
                    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
                }
                Err(e) => return Err(e),
            }
        }
    }

    /// Bytes currently queued (acquired permits not yet released by the actor).
    pub fn queue_depth(&self) -> usize {
        self.byte_budget
            .saturating_sub(self.budget.available_permits())
    }

    /// True if the byte budget has at least one permit available.
    pub fn can_send_immediate(&self) -> bool {
        self.budget.available_permits() > 0
    }

    /// True if the byte budget is fully exhausted (next send will block).
    pub fn is_over_threshold(&self) -> bool {
        self.budget.available_permits() == 0
    }

    /// Total byte budget for this sender.
    pub fn get_threshold(&self) -> u64 {
        self.byte_budget as u64
    }

    /// Check whether the actor queue needs backpressure and pause if so.
    ///
    /// Returns `(should_break, pause_us)`:
    /// - `should_break`: cancellation token fired — caller should exit the outbound loop.
    /// - `pause_us`: wall-clock microseconds spent waiting (0 if no pause was needed).
    ///
    /// ## Design
    ///
    /// `queue_depth()` is the number of bytes the outbound task has pushed into the
    /// actor's channel that the actor has not yet sent (semaphore permits acquired but
    /// not yet released).  When the actor stalls inside `dc.send()` — because the SCTP
    /// pending queue is full and its write loop is delayed on a large IOCP completion
    /// backlog on Windows — it stops releasing permits and `queue_depth()` rises.
    ///
    /// This is a pure atomic semaphore read: no RTCDataChannel mutex, no SCTP calls,
    /// no contention with the actor hot path on any platform.
    ///
    /// The previous approach called `buffered_amount()` which acquires the RTCDataChannel
    /// `data_channel` mutex.  `RTCDataChannel::send()` holds that same mutex while
    /// awaiting `pending_queue.append()`, which blocks when the 128 KB SCTP pending
    /// queue is full.  On Windows CI (after many tests accumulate an IOCP completion
    /// backlog), this caused `maybe_pause_for_sctp` to hang indefinitely, triggering
    /// the 60-second socket timeout.
    ///
    /// ## Why no on_buffered_amount_low callback
    ///
    /// That callback fires from inside the SCTP send path.  Awaiting a future there
    /// causes reentrancy hazards on Windows IOCP — the same problem the actor model
    /// was built to eliminate.
    pub async fn maybe_pause_for_sctp(
        &self,
        cancel: &tokio_util::sync::CancellationToken,
    ) -> (bool, u64) {
        if self.queue_depth() <= SCTP_HIGH_WATER {
            return (false, 0);
        }

        // Actor queue is above the high-water mark — SCTP path is congested.
        // Pause reading from the TCP backend until the actor drains below threshold.
        // All checks are lock-free atomic reads.
        const SCTP_POLL_MS: u64 = 5;
        let pause_start = std::time::Instant::now();
        let deadline = pause_start + std::time::Duration::from_secs(2);

        loop {
            tokio::select! {
                biased;
                _ = cancel.cancelled() => return (true, 0),
                _ = tokio::time::sleep(std::time::Duration::from_millis(SCTP_POLL_MS)) => {}
            }

            if self.queue_depth() <= SCTP_HIGH_WATER {
                break;
            }

            if std::time::Instant::now() >= deadline {
                debug!("SCTP backpressure: actor queue still high after 2s — forcing resume");
                break;
            }
        }

        (false, pause_start.elapsed().as_micros() as u64)
    }
}
