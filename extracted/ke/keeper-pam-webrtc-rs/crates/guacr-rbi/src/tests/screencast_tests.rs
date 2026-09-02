use crate::screencast::{
    ScreencastConfig, ScreencastFormat, ScreencastFrame, ScreencastFrameMetadata,
    ScreencastProcessor, ScreencastStats,
};

#[test]
fn test_screencast_config_default() {
    let config = ScreencastConfig::default();
    assert_eq!(config.format, ScreencastFormat::Jpeg);
    assert_eq!(config.quality, 80);
    assert_eq!(config.max_width, 1920);
    assert_eq!(config.max_height, 1080);
    assert_eq!(config.every_nth_frame, 1);
}

#[test]
fn test_screencast_format() {
    assert_eq!(ScreencastFormat::Jpeg.as_str(), "jpeg");
    assert_eq!(ScreencastFormat::Png.as_str(), "png");
    assert_eq!(ScreencastFormat::Jpeg.guacamole_format(), 1);
    assert_eq!(ScreencastFormat::Png.guacamole_format(), 0);
}

#[test]
fn test_screencast_stats() {
    let mut stats = ScreencastStats::default();

    stats.record_frame(100_000, true);
    stats.record_frame(100_000, true);
    stats.record_frame(100_000, false);

    assert_eq!(stats.frames_received, 3);
    assert_eq!(stats.frames_sent, 2);
    assert_eq!(stats.frames_dropped, 1);
    assert_eq!(stats.avg_frame_size_kb, 97);
    assert!((stats.compression_ratio() - 33.33).abs() < 0.1);
}

#[test]
fn test_screencast_processor() {
    let config = ScreencastConfig::default();
    let mut processor = ScreencastProcessor::new(config);

    let test_data = b"test image data";
    use base64::Engine;
    let encoded = base64::engine::general_purpose::STANDARD.encode(test_data);

    let frame = ScreencastFrame {
        data: encoded,
        metadata: ScreencastFrameMetadata {
            page_scale_factor: 1.0,
            offset_top: 0.0,
            offset_left: 0.0,
            device_width: 1920.0,
            device_height: 1080.0,
            scroll_offset_x: 0.0,
            scroll_offset_y: 0.0,
            timestamp: Some(123.456),
        },
        session_id: 42,
    };

    let result = processor.process_frame(frame);
    assert!(result.is_ok());

    let (data, should_send) = result.unwrap();
    assert_eq!(data.as_ref(), test_data);
    assert!(should_send);
    assert_eq!(processor.last_session_id(), Some(42));

    let stats = processor.stats();
    assert_eq!(stats.frames_received, 1);
    assert_eq!(stats.frames_sent, 1);
}
