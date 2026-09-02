// Performance tests for TN5250 handler.
// Run with: cargo test -p guacr-tn5250 --test performance_test -- --include-ignored --test-threads=1
#[cfg(test)]
mod performance_tests {
    use std::time::Instant;

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_connection_throughput() {
        let start = Instant::now();
        let elapsed = start.elapsed();
        println!("TN5250 connection throughput: {:?}", elapsed);
        println!("Implement with actual TN5250 session against test server");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_frame_throughput() {
        // Measure screen update rate: parse WTD records and render to JPEG
        // Target: > 30 screen updates/sec for 24x80
        use guacr_tn5250::datastream::{parse_5250_record, OpCode};
        use guacr_tn5250::renderer;
        use guacr_tn5250::screen::ScreenBuffer5250;

        // Build a minimal WTD record: 5-byte header only
        let data = [
            0x00u8, 0x05, // length = 5
            0x04, // record type
            0x00, // reserved
            0x01, // opcode: WriteToDisplay
        ];

        let frames = 100;
        let start = Instant::now();

        for _ in 0..frames {
            if let Ok(record) = parse_5250_record(&data) {
                assert_eq!(record.opcode, OpCode::WriteToDisplay);
                let mut screen = ScreenBuffer5250::new(24, 80);
                screen.apply_record(&record);
                let _ = renderer::render_to_jpeg(&screen, 9, 18, 85);
            }
        }

        let elapsed = start.elapsed();
        let fps = frames as f64 / elapsed.as_secs_f64();
        println!(
            "TN5250 frame throughput: {:.1} fps ({} frames in {:?})",
            fps, frames, elapsed
        );
        assert!(
            fps > 30.0,
            "Frame throughput {:.1} fps below 30 fps threshold",
            fps
        );
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_record_parse_throughput() {
        // Measure parse throughput for typical WTD records
        use guacr_tn5250::datastream::parse_5250_record;

        // Build a more complex WTD record: SBA + characters
        let mut data = vec![0x00u8, 0x00, 0x04, 0x00, 0x01]; // header placeholder
        data.extend(&[0x10, 0x01, 0x01]); // SBA(1,1)
        data.extend(vec![0xC1u8; 80]); // 80 'A' characters
        let len = data.len() as u16;
        data[0] = (len >> 8) as u8;
        data[1] = (len & 0xFF) as u8;

        let iterations = 10_000;
        let start = Instant::now();

        for _ in 0..iterations {
            let _ = parse_5250_record(&data);
        }

        let elapsed = start.elapsed();
        let rate = iterations as f64 / elapsed.as_secs_f64();
        println!("TN5250 parse rate: {:.0} parses/sec", rate);
        assert!(
            rate > 1000.0,
            "Parse rate {:.0}/sec below 1000/sec threshold",
            rate
        );
    }
}
