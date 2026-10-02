//! Port of `LinuxNetworkWorkerMetricTest`.

use super::linux_network_worker_metric_base::mocked_stopwatch;
use super::{LinuxNetworkInWorkerMetric, LinuxNetworkOutWorkerMetric};
use crate::worker::metric::test_util::{cleanup, temp_dir, write_line_to_file};
use crate::worker::metric::{OperatingRange, WorkerMetric};

const INPUT_1: &str = "Inter-|   Receive                                                |  Transmit\n face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n     lo: 51335658  460211    0    0    0     0          0         0 51335658  460211    0    0    0     0       0          0\n   eth0: 0 11860562    0    0    0     0          0   4234156 0 3248505    0    0    0     0       0          0\n";

const INPUT_2: &str = "Inter-|   Receive                                                |  Transmit\n face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n     lo: 51335668  460211    0    0    0     0          0         0 51335678  460211    0    0    0     0       0          0\n   eth0: 1048576 11860562    0    0    0     0          0   4234156 2097152 3248505    0    0    0     0       0          0\n";

const NO_WHITESPACE_INPUT_1: &str = "Inter-|   Receive                                                |  Transmit\n face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n     lo:51335658  460211    0    0    0     0          0         0 51335658  460211    0    0    0     0       0          0\n   eth0:3120842478 11860562    0    0    0     0          0   4234156 336491180 3248505    0    0    0     0       0          0\n";

const NO_WHITESPACE_INPUT_2: &str = "Inter-|   Receive                                                |  Transmit\n face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed\n     lo:51335668  460211    0    0    0     0          0         0 51335678  460211    0    0    0     0       0          0\n   eth0:3121891054 11860562    0    0    0     0          0   4234156 338588332 3248505    0    0    0     0       0          0\n";

fn test_operating_range() -> OperatingRange {
    OperatingRange::builder().max_utilization(0).build()
}

fn write_and_run(
    metric: &dyn WorkerMetric,
    stat_file: &std::path::Path,
    input1: &str,
    input2: &str,
    expected: f64,
) {
    write_line_to_file(stat_file, input1);
    assert_eq!(metric.capture().value(), 0.0);
    write_line_to_file(stat_file, input2);
    assert_eq!(metric.capture().value(), expected);
}

fn execute_test_for_in_and_out(
    input1: &str,
    input2: &str,
    tick_millis: i64,
    expected_in: f64,
    expected_out: f64,
) {
    let dir = temp_dir("net");
    let stat_file = dir.join("netStat");
    let path = stat_file.to_str().unwrap();

    let in_metric = LinuxNetworkInWorkerMetric::new(
        test_operating_range(),
        "eth0",
        path,
        10.0,
        mocked_stopwatch(tick_millis),
    );
    write_and_run(&in_metric, &stat_file, input1, input2, expected_in);

    let out_metric = LinuxNetworkOutWorkerMetric::new(
        test_operating_range(),
        "eth0",
        path,
        10.0,
        mocked_stopwatch(tick_millis),
    );
    write_and_run(&out_metric, &stat_file, input1, input2, expected_out);

    cleanup(&dir);
}

#[test]
fn capture_sanity_with_1_second_ticker() {
    execute_test_for_in_and_out(INPUT_1, INPUT_2, 1000, 10.0, 20.0);
    execute_test_for_in_and_out(
        NO_WHITESPACE_INPUT_1,
        NO_WHITESPACE_INPUT_2,
        1000,
        10.0,
        20.0,
    );
}

#[test]
fn capture_sanity_with_500ms_ticker() {
    execute_test_for_in_and_out(INPUT_1, INPUT_2, 500, 20.0, 40.0);
    execute_test_for_in_and_out(
        NO_WHITESPACE_INPUT_1,
        NO_WHITESPACE_INPUT_2,
        500,
        20.0,
        40.0,
    );
}

#[test]
#[should_panic(expected = "elapsedTimeInSecond is zero")]
fn capture_with_no_time_elapsed() {
    execute_test_for_in_and_out(INPUT_1, INPUT_2, 0, 20.0, 40.0);
}

#[test]
#[should_panic(expected = "does not exists")]
fn capture_non_existing_file() {
    let in_metric = LinuxNetworkInWorkerMetric::new(
        test_operating_range(),
        "eth0",
        "/non/existing/file",
        10.0,
        mocked_stopwatch(1000),
    );
    in_metric.capture();
}

#[test]
#[should_panic(expected = "find interface")]
fn capture_non_existing_network_interface() {
    let dir = temp_dir("net_iface");
    let stat_file = dir.join("netStat");
    let in_metric = LinuxNetworkInWorkerMetric::new(
        test_operating_range(),
        "randomName",
        stat_file.to_str().unwrap(),
        10.0,
        mocked_stopwatch(1000),
    );
    write_line_to_file(&stat_file, INPUT_1);
    in_metric.capture();
}

#[test]
fn capture_configured_max_less_than_utilized_asserts_100_percent() {
    let dir = temp_dir("net_max");
    let stat_file = dir.join("netStat");
    // configured 1 MB, utilized 2 MB.
    let out_metric = LinuxNetworkOutWorkerMetric::new(
        test_operating_range(),
        "eth0",
        stat_file.to_str().unwrap(),
        1.0,
        mocked_stopwatch(1000),
    );
    write_and_run(
        &out_metric,
        &stat_file,
        NO_WHITESPACE_INPUT_1,
        NO_WHITESPACE_INPUT_2,
        100.0,
    );
    cleanup(&dir);
}

#[test]
#[should_panic(expected = "maxBandwidthInMBps should be greater than 0.")]
fn capture_max_bandwidth_zero_panics() {
    let dir = temp_dir("net_zero");
    let stat_file = dir.join("netStat");
    let _ = LinuxNetworkOutWorkerMetric::new(
        test_operating_range(),
        "eth0",
        stat_file.to_str().unwrap(),
        0.0,
        mocked_stopwatch(1000),
    );
}
