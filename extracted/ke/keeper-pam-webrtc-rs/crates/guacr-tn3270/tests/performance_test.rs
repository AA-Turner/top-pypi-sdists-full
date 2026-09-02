// Performance tests for TN3270 handler.
// Run with: cargo test -p guacr-tn3270 --test performance_test -- --include-ignored --test-threads=1
#[cfg(test)]
mod performance_tests {
    use std::time::Instant;

    #[tokio::test]
    #[ignore]
    async fn test_tn3270_connection_throughput() {
        // Requires a running TN3270 server on localhost:3270
        // docker-compose -f docker-compose.guacr-test.yml up -d tn3270
        let start = Instant::now();
        let elapsed = start.elapsed();
        println!("TN3270 connection throughput: {:?}", elapsed);
        println!("Implement with actual TN3270 session against test server");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn3270_frame_throughput() {
        // Measure screen update rate: parse data streams and render to JPEG
        // Target: > 30 screen updates/sec for 24x80
        use guacr_terminal::TerminalRenderer;
        use guacr_tn3270::datastream::parse_data_stream;
        use guacr_tn3270::renderer;
        use guacr_tn3270::screen::ScreenBuffer;

        let char_width = 9u32;
        let char_height = 18u32;
        let font_size = char_height as f32 * 0.70;
        let term_renderer =
            TerminalRenderer::new_with_dimensions(char_width, char_height, font_size)
                .expect("renderer init");

        let frames = 100;
        let start = Instant::now();

        for _ in 0..frames {
            // Minimal Erase/Write + WCC
            let data = [0x05u8, 0x60];
            if let Ok(ds) = parse_data_stream(&data) {
                let mut screen = ScreenBuffer::new(24, 80);
                screen.apply_data_stream(&ds);
                let _ = renderer::render_with_renderer(&screen, &term_renderer, 85);
            }
        }

        let elapsed = start.elapsed();
        let fps = frames as f64 / elapsed.as_secs_f64();
        println!(
            "TN3270 frame throughput: {:.1} fps ({} frames in {:?})",
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
    async fn test_tn3270_data_stream_parse_throughput() {
        // Measure parse throughput for large data streams
        // Construct a realistic login-screen data stream
        use guacr_tn3270::datastream::{encode_buffer_address, parse_data_stream};

        let (b0, b1) = encode_buffer_address(0);
        let (b80, b81) = encode_buffer_address(80);

        let mut data = vec![
            0x05, 0x60, // EraseWrite, WCC
            0x11, b0, b1, // SBA(0)
            0x1D, 0x20, // SF(protected)
        ];
        // Fill with EBCDIC data (approx 24*80 characters)
        data.extend(vec![0xC8u8; 1920]);
        data.extend(&[0x11, b80, b81, 0x1D, 0x00, 0x13]); // SBA, SF, IC

        let iterations = 10_000;
        let start = Instant::now();

        for _ in 0..iterations {
            let _ = parse_data_stream(&data);
        }

        let elapsed = start.elapsed();
        let rate = iterations as f64 / elapsed.as_secs_f64();
        println!("TN3270 parse rate: {:.0} parses/sec", rate);
        assert!(
            rate > 1000.0,
            "Parse rate {:.0}/sec below 1000/sec threshold",
            rate
        );
    }
}
