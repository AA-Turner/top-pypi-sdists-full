// Performance tests for RBI (Remote Browser Isolation) handler.
// Run with: cargo test -p guacr-rbi --test performance_test -- --include-ignored --test-threads=1
#[cfg(test)]
mod performance_tests {
    use std::time::Instant;

    #[tokio::test]
    #[ignore]
    async fn test_rbi_connection_throughput() {
        // Requires Chrome/Chromium to be installed
        // CHROMIUM_PATH=/usr/bin/chromium cargo test -p guacr-rbi --test performance_test
        let start = Instant::now();
        let elapsed = start.elapsed();
        println!("RBI connection throughput: {:?}", elapsed);
        println!("Implement with actual Chrome session via chromiumoxide");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_frame_throughput() {
        // Measure screen capture + encode rate
        // Target: > 15 FPS capture throughput
        println!("Frame throughput test — implement with actual Chrome screencast session");
        println!("Target: > 15 FPS at 1920x1080 JPEG quality 80");
    }

    #[tokio::test]
    #[ignore]
    async fn test_rbi_adaptive_fps_behavior() {
        // Verify that AdaptiveFps correctly drops from max to min FPS
        // when the browser session is idle
        use guacr_rbi::adaptive_fps::AdaptiveFps;

        let mut fps = AdaptiveFps::new(5, 30);
        let start = Instant::now();

        // Simulate active phase
        for _ in 0..30 {
            fps.update(true);
        }
        assert_eq!(fps.current_fps(), 30);

        // Simulate idle phase
        for _ in 0..100 {
            fps.update(false);
        }
        assert_eq!(fps.current_fps(), 5, "Should drop to min FPS when idle");

        // Simulate active again
        fps.update(true);
        assert_eq!(
            fps.current_fps(),
            30,
            "Should recover to max FPS on activity"
        );

        let elapsed = start.elapsed();
        println!("AdaptiveFps state machine verified in {:?}", elapsed);
    }
}
