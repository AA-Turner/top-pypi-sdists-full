//! Port of `software.amazon.kinesis.metrics.MetricAccumulatingQueue`.

use std::collections::{HashMap, VecDeque};
use std::hash::Hash;

use aws_sdk_cloudwatch::types::{MetricDatum, StatisticSet};

use crate::metrics::MetricDatumWithKey;

/// A bounded FIFO queue paired with a map for O(1) lookup, accumulating/merging
/// [`MetricDatumWithKey`] entries that share a key before they are drained for
/// publishing.
///
/// **Concurrency note:** Java makes every public method `synchronized` on the
/// queue instance, and `CloudWatchPublisherRunnable` *also* synchronizes on the
/// same instance (reentrantly) for its `wait`/`notify` coordination. To avoid
/// the reentrancy pitfalls of a naive Rust translation, this port makes the
/// queue a **plain, non-locking** data structure; the single owning
/// `CloudWatchPublisherRunnable` holds it behind one `tokio::sync::Mutex` and
/// calls these methods while already holding the guard. This matches the arch
/// map's recommended design (one mutex guarding all of it, queue methods lock
/// nothing).
#[derive(Debug)]
pub struct MetricAccumulatingQueue<K: Eq + Hash + Clone> {
    /// FIFO order.
    queue: VecDeque<MetricDatumWithKey<K>>,
    /// Constant-time lookup by key -> the queue index's datum. We store the
    /// datum here and mirror updates into the queue entry to keep both
    /// consistent (Java shares one object reference across queue+map).
    keys: HashMap<K, ()>,
    max_queue_size: usize,
}

impl<K: Eq + Hash + Clone> MetricAccumulatingQueue<K> {
    /// Creates a queue bounded to `max_queue_size` distinct entries.
    pub fn new(max_queue_size: usize) -> Self {
        Self {
            queue: VecDeque::new(),
            keys: HashMap::new(),
            max_queue_size,
        }
    }

    /// Removes up to `max_items` entries in FIFO order and returns them,
    /// removing their keys from the lookup map. Port of `drain`.
    pub fn drain(&mut self, max_items: usize) -> Vec<MetricDatumWithKey<K>> {
        let n = max_items.min(self.queue.len());
        let mut drained = Vec::with_capacity(n);
        for _ in 0..n {
            if let Some(item) = self.queue.pop_front() {
                self.keys.remove(&item.key);
                drained.push(item);
            }
        }
        drained
    }

    /// Port of `isEmpty`.
    pub fn is_empty(&self) -> bool {
        self.queue.is_empty()
    }

    /// Port of `size`.
    pub fn size(&self) -> usize {
        self.queue.len()
    }

    /// Offers a datum under `key`. Port of `offer`.
    ///
    /// If the key is new, a new entry is appended if there is capacity
    /// (returning whether it was inserted — `false` when the queue is full, and
    /// nothing is stored, keeping queue and map consistent). If the key already
    /// exists, the datum is merged into the existing entry via
    /// [`accumulate`](Self::accumulate) and `true` is returned unconditionally.
    pub fn offer(&mut self, key: K, datum: MetricDatum) -> bool {
        if self.keys.contains_key(&key) {
            // Existing entry: accumulate in place.
            if let Some(existing) = self.queue.iter_mut().find(|e| e.key == key) {
                Self::accumulate(existing, &datum);
            }
            true
        } else {
            // New entry: honor capacity (LinkedBlockingQueue.offer semantics).
            if self.queue.len() >= self.max_queue_size {
                return false;
            }
            self.keys.insert(key.clone(), ());
            self.queue.push_back(MetricDatumWithKey::new(key, datum));
            true
        }
    }

    /// Merges `new_datum` into `entry`'s datum, porting `accumulate`.
    ///
    /// Panics on a unit mismatch with `"Unit mismatch for datum named <name>"`.
    fn accumulate(entry: &mut MetricDatumWithKey<K>, new_datum: &MetricDatum) {
        let old = &entry.datum;
        if old.unit() != new_datum.unit() {
            panic!(
                "Unit mismatch for datum named {}",
                old.metric_name().unwrap_or_default()
            );
        }

        let old_stats = old
            .statistic_values()
            .expect("queued datum always has statistic values");
        let new_stats = new_datum
            .statistic_values()
            .expect("offered datum always has statistic values");

        let statistic_set = StatisticSet::builder()
            .sum(old_stats.sum().unwrap_or(0.0) + new_stats.sum().unwrap_or(0.0))
            .minimum(
                old_stats
                    .minimum()
                    .unwrap_or(f64::INFINITY)
                    .min(new_stats.minimum().unwrap_or(f64::INFINITY)),
            )
            .maximum(
                old_stats
                    .maximum()
                    .unwrap_or(f64::NEG_INFINITY)
                    .max(new_stats.maximum().unwrap_or(f64::NEG_INFINITY)),
            )
            .sample_count(
                old_stats.sample_count().unwrap_or(0.0) + new_stats.sample_count().unwrap_or(0.0),
            )
            .build();

        // Rebuild the datum preserving name/unit/dimensions with merged stats
        // (SDK models are immutable; Java uses oldDatum.toBuilder()).
        let mut builder = MetricDatum::builder().statistic_values(statistic_set);
        if let Some(name) = old.metric_name() {
            builder = builder.metric_name(name);
        }
        if let Some(unit) = old.unit() {
            builder = builder.unit(unit.clone());
        }
        let dims = old.dimensions().to_vec();
        if !dims.is_empty() {
            builder = builder.set_dimensions(Some(dims));
        }
        entry.datum = builder.build();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::metrics::test_helper::construct_datum;
    use crate::metrics::CloudWatchMetricKey;
    use aws_sdk_cloudwatch::types::{Dimension, StandardUnit};

    const MAX_QUEUE_SIZE: usize = 5;

    fn with_dims(datum: MetricDatum, dims: &[(&str, &str)]) -> MetricDatum {
        let dimensions: Vec<Dimension> = dims
            .iter()
            .map(|(n, v)| Dimension::builder().name(*n).value(*v).build())
            .collect();
        datum.to_builder_with_dimensions(dimensions)
    }

    // Helper to rebuild a datum with dimensions (SDK has no to_builder()).
    trait WithDimensions {
        fn to_builder_with_dimensions(&self, dims: Vec<Dimension>) -> MetricDatum;
    }
    impl WithDimensions for MetricDatum {
        fn to_builder_with_dimensions(&self, dims: Vec<Dimension>) -> MetricDatum {
            let mut b = MetricDatum::builder();
            if let Some(n) = self.metric_name() {
                b = b.metric_name(n);
            }
            if let Some(u) = self.unit() {
                b = b.unit(u.clone());
            }
            if let Some(s) = self.statistic_values() {
                b = b.statistic_values(s.clone());
            }
            b.set_dimensions(Some(dims)).build()
        }
    }

    // Ported from MetricAccumulatingQueueTest.testAccumulation.
    #[test]
    fn test_accumulation() {
        let mut queue: MetricAccumulatingQueue<CloudWatchMetricKey> =
            MetricAccumulatingQueue::new(MAX_QUEUE_SIZE);
        let key_a = "a";
        let key_b = "b";

        let datum1 = with_dims(
            construct_datum(key_a, StandardUnit::Count, 10.0, 5.0, 15.0, 2.0),
            &[("name", "a")],
        );
        queue.offer(CloudWatchMetricKey::new(&datum1), datum1);

        let datum2 = with_dims(
            construct_datum(key_a, StandardUnit::Count, 1.0, 1.0, 2.0, 2.0),
            &[("name", "a")],
        );
        queue.offer(CloudWatchMetricKey::new(&datum2), datum2);

        let datum3 = with_dims(
            construct_datum(key_a, StandardUnit::Count, 1.0, 1.0, 2.0, 2.0),
            &[("name", "b")],
        );
        queue.offer(CloudWatchMetricKey::new(&datum3), datum3.clone());

        let datum4 = construct_datum(key_a, StandardUnit::Count, 1.0, 1.0, 2.0, 2.0);
        queue.offer(CloudWatchMetricKey::new(&datum4), datum4.clone());
        queue.offer(CloudWatchMetricKey::new(&datum4), datum4.clone());

        let datum5 = with_dims(
            construct_datum(key_b, StandardUnit::Count, 100.0, 10.0, 110.0, 2.0),
            &[("name", "a")],
        );
        queue.offer(CloudWatchMetricKey::new(&datum5), datum5.clone());

        assert_eq!(queue.size(), 4);
        let items = queue.drain(4);

        assert_eq!(
            items[0].datum,
            with_dims(
                construct_datum(key_a, StandardUnit::Count, 10.0, 1.0, 17.0, 4.0),
                &[("name", "a")]
            )
        );
        assert_eq!(items[1].datum, datum3);
        assert_eq!(
            items[2].datum,
            construct_datum(key_a, StandardUnit::Count, 1.0, 1.0, 4.0, 4.0)
        );
        assert_eq!(
            items[3].datum,
            with_dims(
                construct_datum(key_b, StandardUnit::Count, 100.0, 10.0, 110.0, 2.0),
                &[("name", "a")]
            )
        );
    }

    // Ported from MetricAccumulatingQueueTest.testDrop.
    #[test]
    fn test_drop() {
        let mut queue: MetricAccumulatingQueue<CloudWatchMetricKey> =
            MetricAccumulatingQueue::new(MAX_QUEUE_SIZE);
        for i in 0..MAX_QUEUE_SIZE {
            let datum = construct_datum(&i.to_string(), StandardUnit::Count, 1.0, 1.0, 2.0, 2.0);
            let key = CloudWatchMetricKey::new(&datum);
            assert!(queue.offer(key, datum));
        }

        let datum = construct_datum("foo", StandardUnit::Count, 1.0, 1.0, 2.0, 2.0);
        assert!(!queue.offer(CloudWatchMetricKey::new(&datum), datum));
        assert_eq!(queue.size(), MAX_QUEUE_SIZE);
    }
}
