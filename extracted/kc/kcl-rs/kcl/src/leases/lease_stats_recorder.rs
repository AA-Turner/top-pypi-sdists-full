//! Port of `software.amazon.kinesis.leases.LeaseStatsRecorder`.

use std::collections::HashMap;
use std::collections::VecDeque;
use std::sync::{Arc, Mutex};

use crate::utils::ExponentialMovingAverage;

/// Default EMA smoothing factor, chosen empirically between a simple average
/// and a moving average.
const DEFAULT_ALPHA: f64 = 0.5;

/// Bytes per kilobyte.
pub const BYTES_PER_KB: f64 = 1024.0;

/// A single byte-throughput sample for a lease.
///
/// Java nested `@Builder @Getter LeaseStats` value class.
#[derive(Debug, Clone)]
pub struct LeaseStats {
    lease_key: String,
    bytes: i64,
    creation_time_millis: i64,
}

impl LeaseStats {
    /// Construct a sample with an explicit creation time. Mirrors the Java
    /// builder where `creationTimeMillis` defaults to `System.currentTimeMillis()`.
    pub fn new(lease_key: impl Into<String>, bytes: i64, creation_time_millis: i64) -> Self {
        Self {
            lease_key: lease_key.into(),
            bytes,
            creation_time_millis,
        }
    }

    pub fn lease_key(&self) -> &str {
        &self.lease_key
    }
    pub fn bytes(&self) -> i64 {
        self.bytes
    }
    pub fn creation_time_millis(&self) -> i64 {
        self.creation_time_millis
    }
}

/// Injectable millisecond clock (Java `Callable<Long> timeProviderInMillis`).
///
/// The Java `getCurrenTimeInMillis()` falls back to `System.currentTimeMillis()`
/// on any exception from the callable; a Rust `Fn() -> i64` cannot fail, so no
/// fallback is needed.
pub type TimeProvider = Arc<dyn Fn() -> i64 + Send + Sync>;

/// Records per-lease byte-throughput samples over a sliding time window and
/// exposes an exponentially-smoothed KBps estimate per lease.
///
/// # Concurrency
///
/// Java uses two lock-free `ConcurrentHashMap`s plus per-key
/// `ConcurrentLinkedQueue`s. Following the porting guidance, this port uses a
/// single `std::sync::Mutex<Inner>` guarding both maps (the critical sections
/// are short and contention here is low — the renewer touches one lease key at
/// a time). Behavior — the sliding-window eviction, the "stop at the first
/// still-valid / still-future element" short-circuiting, and the persistent EMA
/// per key — is preserved exactly.
pub struct LeaseStatsRecorder {
    renewer_frequency_in_millis: i64,
    time_provider_in_millis: TimeProvider,
    inner: Mutex<Inner>,
}

#[derive(Default)]
struct Inner {
    lease_stats_map: HashMap<String, VecDeque<LeaseStats>>,
    lease_key_to_ema: HashMap<String, ExponentialMovingAverage>,
}

impl LeaseStatsRecorder {
    /// Java `@RequiredArgsConstructor(renewerFrequencyInMillis, timeProviderInMillis)`.
    pub fn new(renewer_frequency_in_millis: i64, time_provider_in_millis: TimeProvider) -> Self {
        Self {
            renewer_frequency_in_millis,
            time_provider_in_millis,
            inner: Mutex::new(Inner::default()),
        }
    }

    /// Record a stats sample (append-only, thread safe).
    pub fn record_stats(&self, lease_stats: LeaseStats) {
        let mut inner = self.inner.lock().unwrap();
        inner
            .lease_stats_map
            .entry(lease_stats.lease_key.clone())
            .or_default()
            .push_back(lease_stats);
    }

    /// Calculate the smoothed throughput in KBps for `lease_key`.
    ///
    /// First evicts samples older than `renewer_frequency_in_millis`, then sums
    /// the bytes of the remaining "current" samples, converts to KBps, and feeds
    /// that into a per-key EMA (`alpha = 0.5`), returning its current value.
    ///
    /// Returns `None` if there are no stats for the lease key yet. Note that
    /// repeated calls shift the EMA even without new data (documented caveat).
    pub fn get_throughput_kbps(&self, lease_key: &str) -> Option<f64> {
        let current_time_filter = self.current_time_in_millis();
        let current_time_read = &self.time_provider_in_millis;

        let mut inner = self.inner.lock().unwrap();

        if !inner.lease_stats_map.contains_key(lease_key) {
            // No entry for this lease key yet.
            return None;
        }

        // filterExpiredEntries: poll from head while the oldest entry is expired.
        {
            let queue = inner.lease_stats_map.get_mut(lease_key).unwrap();
            while let Some(front) = queue.front() {
                if current_time_filter - front.creation_time_millis
                    < self.renewer_frequency_in_millis
                {
                    break;
                }
                queue.pop_front();
            }
        }

        // readQueue: iterate, stopping at the first element whose creation time
        // is in the future (assumes FIFO chronological order). Re-read the clock
        // to match Java's second getCurrenTimeInMillis() call.
        let current_time_millis = current_time_read();
        let sum_bytes: i64 = {
            let queue = inner.lease_stats_map.get(lease_key).unwrap();
            let mut sum = 0i64;
            for stats in queue.iter() {
                if stats.creation_time_millis > current_time_millis {
                    break;
                }
                sum += stats.bytes;
            }
            sum
        };

        // Divide by 1000.0 (not Duration) to avoid seconds-rounding precision loss.
        let frequency = self.renewer_frequency_in_millis as f64 / 1000.0;
        let throughput = sum_bytes as f64 / BYTES_PER_KB / frequency;

        let ema = inner
            .lease_key_to_ema
            .entry(lease_key.to_string())
            .or_insert_with(|| ExponentialMovingAverage::new(DEFAULT_ALPHA));
        ema.add(throughput);
        Some(ema.value())
    }

    /// Clear the in-memory stats for a lease when it is reassigned.
    pub fn drop_lease_stats(&self, lease_key: &str) {
        let mut inner = self.inner.lock().unwrap();
        inner.lease_stats_map.remove(lease_key);
        inner.lease_key_to_ema.remove(lease_key);
    }

    fn current_time_in_millis(&self) -> i64 {
        (self.time_provider_in_millis)()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::time::{SystemTime, UNIX_EPOCH};

    fn now_millis() -> i64 {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_millis() as i64
    }

    const TEST_RENEWER_FREQ: i64 = 60_000; // Duration.ofMinutes(1)

    /// A time provider that returns a fixed value.
    fn fixed(t: i64) -> TimeProvider {
        Arc::new(move || t)
    }

    /// A time provider that returns each value in `seq` in turn, repeating the
    /// last one thereafter (matching Mockito `.thenReturn().thenReturn()...`).
    fn sequence(seq: Vec<i64>) -> TimeProvider {
        let idx = Arc::new(AtomicUsize::new(0));
        Arc::new(move || {
            let i = idx.fetch_add(1, Ordering::SeqCst);
            let last = seq.len() - 1;
            seq[i.min(last)]
        })
    }

    fn gen_stat_bytes(lease_key: &str, creation_time_millis: i64, bytes: i64) -> LeaseStats {
        LeaseStats::new(lease_key, bytes, creation_time_millis)
    }

    fn gen_stat(lease_key: &str, creation_time_millis: i64) -> LeaseStats {
        // 1 MB data
        gen_stat_bytes(lease_key, creation_time_millis, 1024 * 1024)
    }

    #[test]
    fn sanity() {
        let now = now_millis();
        let recorder = LeaseStatsRecorder::new(TEST_RENEWER_FREQ, fixed(now + 1));
        for _ in 0..5 {
            recorder.record_stats(gen_stat("lease-key1", now));
        }
        // 5 MB over 60s -> 5*1024 KB / 60 = 85.33 KBps; floor = 85.
        assert_eq!(
            recorder.get_throughput_kbps("lease-key1").unwrap().floor(),
            85.0
        );
        // idempotent: EMA with same input stays at same value.
        assert_eq!(
            recorder.get_throughput_kbps("lease-key1").unwrap().floor(),
            85.0
        );
    }

    #[test]
    fn validate_decay_to_zero() {
        let current_time = now_millis();
        let recorder = LeaseStatsRecorder::new(
            TEST_RENEWER_FREQ,
            sequence(vec![
                current_time + 1,
                current_time + 1,
                current_time - TEST_RENEWER_FREQ - 5,
            ]),
        );
        recorder.record_stats(gen_stat_bytes("lease-key1", current_time, 1));
        for _ in 0..2000 {
            recorder.get_throughput_kbps("lease-key1");
        }
        // After decaying for a long time it eventually reaches zero.
        assert_eq!(recorder.get_throughput_kbps("lease-key1"), Some(0.0));
    }

    #[test]
    fn validate_very_high_throughput() {
        let current_time = now_millis();
        let recorder = LeaseStatsRecorder::new(TEST_RENEWER_FREQ, fixed(now_millis() + 1));
        for _ in 0..1000 {
            // 1 GB per stat
            recorder.record_stats(gen_stat_bytes(
                "lease-key1",
                current_time,
                1024 * 1024 * 1024,
            ));
        }
        assert_eq!(
            recorder.get_throughput_kbps("lease-key1").unwrap().floor(),
            17476266.0
        );
    }

    #[test]
    fn expired_items_assert_zero_output() {
        let now = now_millis();
        let recorder = LeaseStatsRecorder::new(TEST_RENEWER_FREQ, fixed(now + 1));
        recorder.record_stats(gen_stat("lease-key1", now - TEST_RENEWER_FREQ - 10));
        assert_eq!(recorder.get_throughput_kbps("lease-key1"), Some(0.0));
    }

    #[test]
    fn no_entry_present_returns_none() {
        let recorder = LeaseStatsRecorder::new(TEST_RENEWER_FREQ, fixed(now_millis()));
        assert_eq!(recorder.get_throughput_kbps("does-not-exist"), None);
    }

    #[test]
    fn drop_lease_stats_sanity() {
        let now = now_millis();
        let recorder = LeaseStatsRecorder::new(TEST_RENEWER_FREQ, fixed(now + 1));
        recorder.record_stats(gen_stat("lease-key1", now));
        // 1 MB / 60s -> 1024/60 = 17.06 KBps; floor = 17.
        assert_eq!(
            recorder.get_throughput_kbps("lease-key1").unwrap().floor(),
            17.0
        );
        recorder.drop_lease_stats("lease-key1");
        assert_eq!(recorder.get_throughput_kbps("lease-key1"), None);
    }
}
