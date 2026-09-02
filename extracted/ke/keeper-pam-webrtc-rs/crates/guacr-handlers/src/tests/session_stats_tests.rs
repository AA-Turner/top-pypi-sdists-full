use crate::session_stats::{FpsCounter, SessionStats};
use std::time::{Duration, Instant};

#[test]
fn test_new_stats_all_zero() {
    let stats = SessionStats::new("ssh");
    assert_eq!(stats.frames_sent, 0);
    assert_eq!(stats.bytes_sent, 0);
    assert_eq!(stats.input_events_received, 0);
    assert_eq!(stats.protocol, "ssh");
}

#[test]
fn test_record_frame_increments_both_counters() {
    let mut stats = SessionStats::new("rdp");
    stats.record_frame(500);
    stats.record_frame(300);
    assert_eq!(stats.frames_sent, 2);
    assert_eq!(stats.bytes_sent, 800);
}

#[test]
fn test_record_input_increments_counter() {
    let mut stats = SessionStats::new("telnet");
    for _ in 0..5 {
        stats.record_input();
    }
    assert_eq!(stats.input_events_received, 5);
}

#[test]
fn test_summary_contains_all_fields() {
    let mut stats = SessionStats::new("vnc");
    stats.record_frame(1024);
    stats.record_frame(2048);
    stats.record_input();
    stats.record_input();
    stats.record_input();
    let s = stats.summary();
    assert!(s.contains("protocol=vnc"), "missing protocol: {s}");
    assert!(s.contains("frames=2"), "missing frames: {s}");
    assert!(s.contains("bytes=3072"), "missing bytes: {s}");
    assert!(s.contains("inputs=3"), "missing inputs: {s}");
    assert!(s.contains("duration_ms="), "missing duration_ms: {s}");
}

#[test]
fn test_summary_key_value_format() {
    let stats = SessionStats::new("ssh");
    let s = stats.summary();
    // Each key=value pair must be present in order
    assert!(
        s.starts_with("protocol=ssh "),
        "summary must start with 'protocol=ssh ': {s}"
    );
    let parts: Vec<&str> = s.split_whitespace().collect();
    assert_eq!(
        parts.len(),
        5,
        "summary must have 5 space-separated key=value pairs: {s}"
    );
    for part in &parts {
        assert!(part.contains('='), "each part must be key=value: {part}");
    }
}

#[test]
fn test_elapsed_ms_increases_over_time() {
    let stats = SessionStats::new("ssh");
    std::thread::sleep(Duration::from_millis(5));
    assert!(
        stats.elapsed_ms() >= 5,
        "elapsed_ms must be at least 5ms after sleeping 5ms"
    );
}

#[test]
fn test_fps_counter_delegates_to_stats() {
    let mut fps = FpsCounter::new();
    let mut stats = SessionStats::new("rdp");
    fps.record_frame(&mut stats, 100, "c1");
    fps.record_frame(&mut stats, 200, "c1");
    assert_eq!(stats.frames_sent, 2);
    assert_eq!(stats.bytes_sent, 300);
}

#[test]
fn test_fps_counter_window_reset() {
    // Force the window to appear elapsed by backdating window_start.
    let mut fps = FpsCounter {
        window_start: Instant::now() - Duration::from_secs(6),
        window_frames: 30,
        window_secs: 5.0,
    };
    let mut stats = SessionStats::new("vnc");
    // This record_frame call should detect the elapsed window, log, and reset.
    fps.record_frame(&mut stats, 1, "test-conn");
    // After reset: window_frames is 0 (frame was counted in the logged window; new window starts fresh).
    assert_eq!(
        fps.window_frames, 0,
        "window_frames must reset to 0 after window elapsed"
    );
}

#[test]
fn test_fps_counter_no_reset_before_window() {
    let mut fps = FpsCounter::new();
    let mut stats = SessionStats::new("rdp");
    for _ in 0..10 {
        fps.record_frame(&mut stats, 1, "conn");
    }
    // Window cannot have elapsed in < 5 s.
    assert_eq!(
        fps.window_frames, 10,
        "window_frames must not reset before 5s window"
    );
}
