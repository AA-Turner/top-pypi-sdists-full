//! Port of `WorkerMetricsManagerTest`.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

use aws_sdk_cloudwatch::types::StandardUnit;

use super::super::worker_metric_stats_manager::{
    WorkerMetricStatsManager, METRICS_IN_MEMORY_REPORTER_FAILURE,
};
use crate::metrics::{MetricsFactory, MetricsLevel, MetricsScope};
use crate::worker::metric::{OperatingRange, WorkerMetric, WorkerMetricType, WorkerMetricValue};

const TEST_STATS_COUNT: usize = 10;

// A metrics scope that records add_data into a shared map (Java's anonymous
// MetricsScope in the test).
#[derive(Clone, Default)]
struct RecordingMetrics {
    map: Arc<Mutex<std::collections::HashMap<String, Vec<f64>>>>,
}

impl MetricsScope for RecordingMetrics {
    fn add_data(&mut self, name: &str, value: f64, _unit: StandardUnit) {
        self.map
            .lock()
            .unwrap()
            .entry(name.to_string())
            .or_default()
            .push(value);
    }
    fn add_data_with_level(
        &mut self,
        name: &str,
        value: f64,
        _unit: StandardUnit,
        _level: MetricsLevel,
    ) {
        self.map
            .lock()
            .unwrap()
            .entry(name.to_string())
            .or_default()
            .push(value);
    }
    fn add_dimension(&mut self, _name: &str, _value: &str) {}
    fn end(&mut self) {}
}

struct RecordingFactory {
    map: Arc<Mutex<std::collections::HashMap<String, Vec<f64>>>>,
}

impl MetricsFactory for RecordingFactory {
    fn create_metrics(&self) -> Box<dyn MetricsScope + Send> {
        Box::new(RecordingMetrics {
            map: Arc::clone(&self.map),
        })
    }
}

// A worker metric that increments a counter each capture and optionally
// panics/returns a value (Java's TestWorkerMetric; a null value → panic on
// build, matching `WorkerMetricValue.builder().value(null)`).
#[derive(Debug)]
struct TestWorkerMetric {
    counter: Arc<AtomicUsize>,
    value: Option<f64>, // None => Java `null` value (panics WorkerMetricValue build)
    should_throw: bool,
}

impl WorkerMetric for TestWorkerMetric {
    fn short_name(&self) -> String {
        WorkerMetricType::Cpu.short_name().to_string()
    }
    fn capture(&self) -> WorkerMetricValue {
        self.counter.fetch_add(1, Ordering::SeqCst);
        if self.should_throw {
            panic!("Test exception");
        }
        match self.value {
            Some(v) => WorkerMetricValue::builder().value(v).build(),
            None => WorkerMetricValue::builder().build(), // panics (null value)
        }
    }
    fn operating_range(&self) -> OperatingRange {
        OperatingRange::builder().max_utilization(0).build()
    }
    fn worker_metric_type(&self) -> WorkerMetricType {
        WorkerMetricType::Cpu
    }
}

fn create_manager_and_wait(
    counter: Arc<AtomicUsize>,
    target: usize,
    value: Option<f64>,
    should_throw: bool,
    map: Arc<Mutex<std::collections::HashMap<String, Vec<f64>>>>,
) -> Arc<WorkerMetricStatsManager> {
    let metric = Arc::new(TestWorkerMetric {
        counter: Arc::clone(&counter),
        value,
        should_throw,
    });
    let factory = Arc::new(RecordingFactory { map });
    let manager = WorkerMetricStatsManager::new(TEST_STATS_COUNT, vec![metric], factory, 10);
    manager.start_manager();
    let deadline = Instant::now() + Duration::from_millis(5000);
    while counter.load(Ordering::SeqCst) < target && Instant::now() < deadline {
        std::thread::sleep(Duration::from_millis(2));
    }
    manager.stop_manager();
    assert!(
        counter.load(Ordering::SeqCst) >= target,
        "counter did not reach target"
    );
    manager
}

#[test]
fn compute_stats_sanity() {
    let counter = Arc::new(AtomicUsize::new(0));
    let map = Arc::new(Mutex::new(std::collections::HashMap::new()));
    let manager = create_manager_and_wait(Arc::clone(&counter), 10, Some(10.0), false, map);

    assert!(manager.raw_high_freq_len(0) >= 10);
    for v in manager.raw_high_freq_snapshot(0) {
        assert_eq!(v, 10.0, "in memory stats map has incorrect value");
    }

    let values1 = manager.compute_metrics();
    let list1 = values1.get(WorkerMetricType::Cpu.short_name()).unwrap();
    assert_eq!(list1.len(), 1);
    assert_eq!(list1[0], 10.0);
    // Queue drained.
    assert_eq!(manager.raw_high_freq_len(0), 0);

    // Calling again without new data => -1 for the last value.
    let values2 = manager.compute_metrics();
    let list2 = values2.get(WorkerMetricType::Cpu.short_name()).unwrap();
    assert_eq!(list2.len(), 2);
    assert_eq!(list2[1], -1.0);
}

#[test]
fn compute_stats_more_than_6_digits_after_decimal_trims() {
    let counter = Arc::new(AtomicUsize::new(0));
    let map = Arc::new(Mutex::new(std::collections::HashMap::new()));
    let manager = create_manager_and_wait(
        Arc::clone(&counter),
        5,
        Some(10.123_456_378_882_342),
        false,
        map,
    );
    let values1 = manager.compute_metrics();
    let list1 = values1.get(WorkerMetricType::Cpu.short_name()).unwrap();
    assert_eq!(list1[0], 10.123456);
}

#[test]
fn compute_stats_worker_metric_returning_null_expects_failure_stats() {
    let counter = Arc::new(AtomicUsize::new(0));
    let map = Arc::new(Mutex::new(std::collections::HashMap::new()));
    let manager = create_manager_and_wait(Arc::clone(&counter), 10, None, false, map);

    // null value => capture panics => no raw value recorded.
    assert_eq!(manager.raw_high_freq_len(0), 0);
    let values = manager.compute_metrics();
    assert_eq!(
        values
            .get(WorkerMetricType::Cpu.short_name())
            .unwrap()
            .len(),
        1
    );
}

#[test]
fn record_stats_invalid_values_no_data_and_failure_metric() {
    // Java @CsvSource {"101,false","50,true","-10,false",",false"}.
    // Cases: out-of-range value (panics on build), throwing metric, negative
    // (panics), null (panics). All should record no raw data and emit the
    // failure metric.
    let cases: Vec<(Option<f64>, bool)> = vec![
        (Some(101.0), false),
        (Some(50.0), true),
        (Some(-10.0), false),
        (None, false),
    ];
    for (value, should_throw) in cases {
        let counter = Arc::new(AtomicUsize::new(0));
        let map = Arc::new(Mutex::new(std::collections::HashMap::new()));
        let manager = create_manager_and_wait(
            Arc::clone(&counter),
            10,
            value,
            should_throw,
            Arc::clone(&map),
        );

        let recorded = map.lock().unwrap();
        let failures = recorded
            .get(METRICS_IN_MEMORY_REPORTER_FAILURE)
            .cloned()
            .unwrap_or_default();
        assert!(!failures.is_empty(), "failure metric not published");
        assert_eq!(failures[0], 1.0);
        drop(recorded);
        assert_eq!(manager.raw_high_freq_len(0), 0);
    }
}
